#include "sampling.h"

struct llama_sampling_context * llama_sampling_init(const struct llama_sampling_params & params) {
    struct llama_sampling_context * result = new llama_sampling_context();

    result->params  = params;
    result->grammar = nullptr;

    // if there is a grammar, parse it
    if (!params.grammar.empty()) {
        result->parsed_grammar = grammar_parser::parse(params.grammar.c_str());

        // will be empty (default) if there are parse errors
        if (result->parsed_grammar.rules.empty()) {
            fprintf(stderr, "%s: failed to parse grammar\n", __func__);
            delete result;
            return nullptr;
        }

        std::vector<const llama_grammar_element *> grammar_rules(result->parsed_grammar.c_rules());

        result->grammar = llama_grammar_init(
                grammar_rules.data(),
                grammar_rules.size(), result->parsed_grammar.symbol_ids.at("root"));
    }

    result->prev.resize(params.n_prev);

    return result;
}

void llama_sampling_free(struct llama_sampling_context * ctx) {
    if (ctx->grammar != NULL) {
        llama_grammar_free(ctx->grammar);
    }

    delete ctx;
}

void llama_sampling_reset(llama_sampling_context * ctx) {
    if (ctx->grammar != NULL) {
        llama_grammar_free(ctx->grammar);
        ctx->grammar = NULL;
    }

    if (!ctx->parsed_grammar.rules.empty()) {
        std::vector<const llama_grammar_element *> grammar_rules(ctx->parsed_grammar.c_rules());

        ctx->grammar = llama_grammar_init(
                grammar_rules.data(),
                grammar_rules.size(), ctx->parsed_grammar.symbol_ids.at("root"));
    }

    std::fill(ctx->prev.begin(), ctx->prev.end(), 0);
    ctx->cur.clear();
}

void llama_sampling_cp(llama_sampling_context * src, llama_sampling_context * dst) {
    if (dst->grammar) {
        llama_grammar_free(dst->grammar);
        dst->grammar = nullptr;
    }

    if (src->grammar) {
        dst->grammar = llama_grammar_copy(src->grammar);
    }

    dst->prev = src->prev;
}

llama_token llama_sampling_last(llama_sampling_context * ctx) {
    return ctx->prev.back();
}

std::string llama_sampling_prev_str(llama_sampling_context * ctx_sampling, llama_context * ctx_main, int n) {
    const int size = ctx_sampling->prev.size();

    n = std::min(n, size);

    std::string result;

    for (int i = size - n; i < size; i++) {
        result += llama_token_to_piece(ctx_main, ctx_sampling->prev[i]);
    }

    return result;
}

std::string llama_sampling_print(const llama_sampling_params & params) {
    char result[1024];

    snprintf(result, sizeof(result),
            "\trepeat_last_n = %d, repeat_penalty = %.3f, frequency_penalty = %.3f, presence_penalty = %.3f\n"
            "\ttop_k = %d, tfs_z = %.3f, top_p = %.3f, min_p = %.3f, typical_p = %.3f, temp = %.3f\n"
            "\tmirostat = %d, mirostat_lr = %.3f, mirostat_ent = %.3f",
            params.penalty_last_n, params.penalty_repeat, params.penalty_freq, params.penalty_present,
            params.top_k, params.tfs_z, params.top_p, params.min_p, params.typical_p, params.temp,
            params.mirostat, params.mirostat_eta, params.mirostat_tau);

    return std::string(result);
}

std::string llama_sampling_order_print(const llama_sampling_params & params) {
    std::string result = "CFG -> Penalties ";
    if (params.mirostat == 0) {
        for (auto s : params.samplers_sequence) {
            switch (s) {
                case 'k': result += "-> top_k "; break;
                case 'f': result += "-> tfs_z "; break;
                case 'y': result += "-> typical_p "; break;
                case 'p': result += "-> top_p "; break;
                case 'm': result += "-> min_p "; break;
                case 't': result += "-> temp "; break;
                default : break;
            }
        }
    } else {
        result += "-> mirostat ";
    }

    return result;
}

// no reasons to expose this function in header
static void sampler_queue(
                   struct llama_context * ctx_main,
            const llama_sampling_params & params,
                 llama_token_data_array & cur_p,
                                 size_t & min_keep) {
    const int n_vocab = llama_n_vocab(llama_get_model(ctx_main));

    const float         temp              = params.temp;
    const float         dynatemp_range    = params.dynatemp_range;
    const float         dynatemp_exponent = params.dynatemp_exponent;
    const int32_t       top_k             = params.top_k <= 0 ? n_vocab : params.top_k;
    const float         top_p             = params.top_p;
    const float         min_p             = params.min_p;
    const float         tfs_z             = params.tfs_z;
    const float         typical_p         = params.typical_p;
    const std::string & samplers_sequence = params.samplers_sequence;

    for (auto s : samplers_sequence) {
        switch (s){
            case 'k': llama_sample_top_k    (ctx_main, &cur_p, top_k,     min_keep); break;
            case 'f': llama_sample_tail_free(ctx_main, &cur_p, tfs_z,     min_keep); break;
            case 'y': llama_sample_typical  (ctx_main, &cur_p, typical_p, min_keep); break;
            case 'p': llama_sample_top_p    (ctx_main, &cur_p, top_p,     min_keep); break;
            case 'm': llama_sample_min_p    (ctx_main, &cur_p, min_p,     min_keep); break;
            case 't':
                if (dynatemp_range > 0) {
                    float dynatemp_min = std::max(0.0f, temp - dynatemp_range);
                    float dynatemp_max = std::max(0.0f, temp + dynatemp_range);
                    llama_sample_entropy(ctx_main, &cur_p, dynatemp_min, dynatemp_max, dynatemp_exponent);
                } else {
                    llama_sample_temp(ctx_main, &cur_p, temp);
                }
                break;
            default : break;
        }
    }
}

static llama_token llama_sampling_sample_impl(
                  struct llama_sampling_context * ctx_sampling,
                  struct llama_context * ctx_main,
                  struct llama_context * ctx_cfg,
                  const int idx,
                  bool is_resampling) {  // Add a parameter to indicate if we are resampling
    const llama_sampling_params & params = ctx_sampling->params;

    const int n_vocab = llama_n_vocab(llama_get_model(ctx_main));

    const float   temp            = params.temp;
    const int32_t penalty_last_n  = params.penalty_last_n < 0 ? params.n_prev : params.penalty_last_n;
    const float   penalty_repeat  = params.penalty_repeat;
    const float   penalty_freq    = params.penalty_freq;
    const float   penalty_present = params.penalty_present;
    const int     mirostat        = params.mirostat;
    const float   mirostat_tau    = params.mirostat_tau;
    const float   mirostat_eta    = params.mirostat_eta;
    const bool    penalize_nl     = params.penalize_nl;

    auto & prev = ctx_sampling->prev;
    auto & cur  = ctx_sampling->cur;

    llama_token id = 0;

    // Get a pointer to the logits
    float * logits = llama_get_logits_ith(ctx_main, idx);

    // Declare original_logits at the beginning of the function scope
    std::vector<float> original_logits;

    if (!is_resampling) {
        // Only make a copy of the original logits if we are not in the resampling phase, not sure if I actually have to do this.
        original_logits = std::vector<float>(logits, logits + llama_n_vocab(llama_get_model(ctx_main)));
    }

    // apply params.logit_bias map
    for (auto it = params.logit_bias.begin(); it != params.logit_bias.end(); it++) {
        logits[it->first] += it->second;
    }

    if (ctx_cfg) {
        float * logits_guidance = llama_get_logits_ith(ctx_cfg, idx);
        llama_sample_apply_guidance(ctx_main, logits, logits_guidance, params.cfg_scale);
    }

    cur.clear();

    for (llama_token token_id = 0; token_id < n_vocab; token_id++) {
        cur.emplace_back(llama_token_data{token_id, logits[token_id], 0.0f});
    }

    llama_token_data_array cur_p = { cur.data(), cur.size(), false };

    // apply penalties
    const auto& penalty_tokens = params.use_penalty_prompt_tokens ? params.penalty_prompt_tokens : prev;
    const int penalty_tokens_used_size = std::min((int)penalty_tokens.size(), penalty_last_n);
    if (penalty_tokens_used_size) {
        const float nl_logit = logits[llama_token_nl(llama_get_model(ctx_main))];

        llama_sample_repetition_penalties(ctx_main, &cur_p,
                penalty_tokens.data() + penalty_tokens.size() - penalty_tokens_used_size,
                penalty_tokens_used_size, penalty_repeat, penalty_freq, penalty_present);

        if (!penalize_nl) {
            for (size_t idx = 0; idx < cur_p.size; idx++) {
                if (cur_p.data[idx].id == llama_token_nl(llama_get_model(ctx_main))) {
                    cur_p.data[idx].logit = nl_logit;
                    break;
                }
            }
        }
    }

    // If we are in the resampling phase, apply grammar checks before sampling logic
    if (is_resampling && ctx_sampling->grammar != NULL) {
        llama_sample_grammar(ctx_main, &cur_p, ctx_sampling->grammar);
    }

    if (temp < 0.0) {
        // greedy sampling, with probs
        llama_sample_softmax(ctx_main, &cur_p);
        id = cur_p.data[0].id;
    } else if (temp == 0.0) {
        // greedy sampling, no probs
        id = llama_sample_token_greedy(ctx_main, &cur_p);
    } else {
        if (mirostat == 1) {
            const int mirostat_m = 100;
            llama_sample_temp(ctx_main, &cur_p, temp);
            id = llama_sample_token_mirostat(ctx_main, &cur_p, mirostat_tau, mirostat_eta, mirostat_m, &ctx_sampling->mirostat_mu);
        } else if (mirostat == 2) {
            llama_sample_temp(ctx_main, &cur_p, temp);
            id = llama_sample_token_mirostat_v2(ctx_main, &cur_p, mirostat_tau, mirostat_eta, &ctx_sampling->mirostat_mu);
        } else {
            // temperature sampling
            size_t min_keep = std::max(1, params.n_probs);

            sampler_queue(ctx_main, params, cur_p, min_keep);

            id = llama_sample_token(ctx_main, &cur_p);

            //{
            //    const int n_top = 10;
            //    LOG("top %d candidates:\n", n_top);

            //    for (int i = 0; i < n_top; i++) {
            //        const llama_token id = cur_p.data[i].id;
            //        (void)id; // To avoid a warning that id is unused when logging is disabled.
            //        LOG(" - %5d: '%12s' (%.3f)\n", id, llama_token_to_piece(ctx_main, id).c_str(), cur_p.data[i].p);
            //    }
            //}

            LOG("sampled token: %5d: '%s'\n", id, llama_token_to_piece(ctx_main, id).c_str());
        }
    }

    if (ctx_sampling->grammar != NULL && !is_resampling) {
        // Create an array with a single token data element for the sampled id
        llama_token_data single_token_data = {id, logits[id], 0.0f};
        llama_token_data_array single_token_data_array = { &single_token_data, 1, false };

        // Apply grammar constraints to the single token
        llama_sample_grammar(ctx_main, &single_token_data_array, ctx_sampling->grammar);

        // Check if the token is valid according to the grammar by seeing if its logit has been set to -INFINITY
        bool is_valid = single_token_data_array.data[0].logit != -INFINITY;

        // If the token is not valid according to the grammar, perform resampling
        if (!is_valid) {
            LOG("Resampling because token %d: '%s' does not meet grammar rules\n", id, llama_token_to_piece(ctx_main, id).c_str());

            // Restore logits from the copy
            std::copy(original_logits.begin(), original_logits.end(), logits);

            return llama_sampling_sample_impl(ctx_sampling, ctx_main, ctx_cfg, idx, true);  // Pass true for is_resampling
        }
    }

    return id;
}

llama_token llama_sampling_sample(
                  struct llama_sampling_context * ctx_sampling,
                  struct llama_context * ctx_main,
                  struct llama_context * ctx_cfg,
                  const int idx) {
    // Call the implementation function with is_resampling set to false by default
    return llama_sampling_sample_impl(ctx_sampling, ctx_main, ctx_cfg, idx, false);
}

void llama_sampling_accept(
        struct llama_sampling_context * ctx_sampling,
        struct llama_context * ctx_main,
        llama_token id,
        bool apply_grammar) {
    ctx_sampling->prev.erase(ctx_sampling->prev.begin());
    ctx_sampling->prev.push_back(id);

    if (ctx_sampling->grammar != NULL && apply_grammar) {
        llama_grammar_accept_token(ctx_main, ctx_sampling->grammar, id);
    }
}
