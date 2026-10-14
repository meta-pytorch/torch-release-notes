
# Release Notes worksheet nn_frontend

You should:

1. ensure commit categorization is correct
2. write up major features, bc-breaking changes, deprecations in detail
3. summarize the other sections

## 1. Ensure commit categorization is correct

* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.

The categories below are as follows:

* BC breaking: All commits that are BC-breaking. These are the most important commits. If any pre-sorted commit is actually BC-breaking, do move it to this section. Each commit should contain a paragraph explaining the rational behind the change as well as an example for how to update user code [BC-Guidelines](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit#heading=h.a9htwgvvec1m).
* Deprecations: All commits introducing deprecation. Each commit should include a small example explaining what should be done to update user code.
* new_features: All commits introducing a new feature (new functions, new submodule, new supported platform etc)
* improvements: All commits providing improvements to existing feature should be here (new backend for a function, new argument, better numerical stability)
* bug fixes: All commits that fix bugs and behaviors that do not match the documentation
* performance: All commits that are added mainly for performance (we separate this from improvements above to make it easier for users to look for it)
* documentation: All commits that add/update documentation
* Developers: All commits that are not end-user facing but still impact people that compile from source, develop into pytorch, extend pytorch, etc
* not user facing: All commits that are not public end-user facing and hence should be dropped from the release notes

## 2. Major features, BC-breaking changes, deprecations

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.

## 3. Summarize the other sections

For the other sections (improvements, bug fixes, performance, documentation, developers, not user facing) - use your
judgement to summarize the key PRs. You do not need to make every commit description perfect
(changed in v2.10 to simplify the process).

Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

Feel free to use https://github.com/pytorch/pytorch/releases/tag/v2.10.0 as an example.

## nn_frontend
### bc breaking
### deprecation
### new features
- Add `torch.nn.functional.scaled_addmm` and in-place `scaled_addmm_`, which compute `beta * input + alpha * scaled_mm(mat1, mat2)` in a single cuBLASLt GEMM on CUDA with the same scaling recipes as `scaled_mm` ([#195409](https://github.com/pytorch/pytorch/pull/195409))
- Support `scaled_addmm` and `scaled_addmm_` under `torch.compile` ([#195410](https://github.com/pytorch/pytorch/pull/195410))
### improvements
- Support soft-label targets with `reduction="none"` on the chunked `linear_cross_entropy` path ([#188296](https://github.com/pytorch/pytorch/pull/188296))
- Allow FlashAttention-4 in `scaled_dot_product_attention` with different query/key and value head dimensions ([#193039](https://github.com/pytorch/pytorch/pull/193039))
- Support deterministic `bicubic` `F.interpolate` backward ([#193707](https://github.com/pytorch/pytorch/pull/193707))
- Support `bicubic` mode for 5-D input in `F.grid_sample` ([#194787](https://github.com/pytorch/pytorch/pull/194787))
- Allow `varlen_attn` to dispatch causal attention to cuDNN ([#193630](https://github.com/pytorch/pytorch/pull/193630))
- Add `weight` to the `F.mse_loss` type stub ([#196126](https://github.com/pytorch/pytorch/pull/196126))
### bug fixes
- Fix wrong gradients in cuDNN/MIOpen RNN backward with non-contiguous saved outputs, a repeated dropout mask in multi-layer MIOpen RNNs, and segfaults in RNN cells and the packed RNN fallback ([#198773](https://github.com/pytorch/pytorch/pull/198773), [#189285](https://github.com/pytorch/pytorch/pull/189285), [#191232](https://github.com/pytorch/pytorch/pull/191232), [#197560](https://github.com/pytorch/pytorch/pull/197560))
- Fix CUDA `softmax`/`log_softmax` gradients, `layer_norm` (CUDA backward and ROCm forward) and memory-efficient SDPA on very large tensors ([#188031](https://github.com/pytorch/pytorch/pull/188031), [#193016](https://github.com/pytorch/pytorch/pull/193016), [#199438](https://github.com/pytorch/pytorch/pull/199438), [#199594](https://github.com/pytorch/pytorch/pull/199594))
- Fix `varlen_attn` ignoring the `sdpa_kernel` backend selection, defects in its cuDNN backend, and FlashAttention-4 split selection ([#193631](https://github.com/pytorch/pytorch/pull/193631), [#194818](https://github.com/pytorch/pytorch/pull/194818), [#198872](https://github.com/pytorch/pytorch/pull/198872))
- Fix memory-efficient SDPA with `causal_lower_right` when the query is longer than the key ([#193632](https://github.com/pytorch/pytorch/pull/193632))
- Fix `grid_sample` returning zeros with the AVX512 CPU kernel ([#197635](https://github.com/pytorch/pytorch/pull/197635))
- Fix `weight_norm` producing `nan` gradients for empty inputs on CPU ([#192179](https://github.com/pytorch/pytorch/pull/192179))
- Raise errors instead of segfaulting in eval-mode `native_batch_norm` without running stats and in `max_pool1d`/`F.unfold` with overflowing sizes ([#194031](https://github.com/pytorch/pytorch/pull/194031), [#194112](https://github.com/pytorch/pytorch/pull/194112))
- Fix `rms_norm` with an engaged but undefined C++ weight ([#195574](https://github.com/pytorch/pytorch/pull/195574))
- Fix `pixel_shuffle`/`pixel_unshuffle` meta errors for non-positive factors ([#195224](https://github.com/pytorch/pytorch/pull/195224))
- Keep the `Module.to_empty()` hint in meta-module `to()` errors with `TORCH_SHOW_CPP_STACKTRACES=1` ([#191151](https://github.com/pytorch/pytorch/pull/191151))
### performance
- Speed up `nn.Module.__call__` by about 15% ([#196236](https://github.com/pytorch/pytorch/pull/196236))
- Add a channels-last CUDA `GroupNorm` kernel ([#191945](https://github.com/pytorch/pytorch/pull/191945))
- Speed up RMSNorm backward up to 2x on sm12x and chunked `linear_cross_entropy` by 6-10% ([#192400](https://github.com/pytorch/pytorch/pull/192400), [#196134](https://github.com/pytorch/pytorch/pull/196134))
### docs
- Fix the `linear_cross_entropy` docstring snippet and `nn.RNN` example, and document bias with probability targets ([#198941](https://github.com/pytorch/pytorch/pull/198941), [#188433](https://github.com/pytorch/pytorch/pull/188433), [#173888](https://github.com/pytorch/pytorch/pull/173888))
### devs
### Untopiced
### not user facing
- Refactor `test/test_nn.py` to be device-agnostic and add hardware classification ([#189536](https://github.com/pytorch/pytorch/pull/189536), [#189538](https://github.com/pytorch/pytorch/pull/189538), [#194038](https://github.com/pytorch/pytorch/pull/194038), [#194045](https://github.com/pytorch/pytorch/pull/194045), [#194191](https://github.com/pytorch/pytorch/pull/194191), [#194863](https://github.com/pytorch/pytorch/pull/194863), [#198467](https://github.com/pytorch/pytorch/pull/198467), [#198848](https://github.com/pytorch/pytorch/pull/198848), [#198859](https://github.com/pytorch/pytorch/pull/198859))
- Fix test tolerances, skips and expected failures on ROCm MI200, GB200 and MPS ([#192993](https://github.com/pytorch/pytorch/pull/192993), [#193949](https://github.com/pytorch/pytorch/pull/193949), [#194726](https://github.com/pytorch/pytorch/pull/194726), [#197904](https://github.com/pytorch/pytorch/pull/197904), [#198689](https://github.com/pytorch/pytorch/pull/198689), [#199006](https://github.com/pytorch/pytorch/pull/199006))
- Consolidate device-side assert stderr checks into a shared test helper ([#193613](https://github.com/pytorch/pytorch/pull/193613))
- Don't use blank targets in cuDNN `CTCLoss` tests ([#195620](https://github.com/pytorch/pytorch/pull/195620))
- Clear the `ModuleTest`/`CriterionTest` argument cache at every entry point so test variants are reproducible ([#196609](https://github.com/pytorch/pytorch/pull/196609))
- Extract `linear_cross_entropy` input checks so backend overrides can reuse them ([#195331](https://github.com/pytorch/pytorch/pull/195331))
- Avoid an extra copy in backward when the output of an N-D `F.linear` is modified in place ([#194077](https://github.com/pytorch/pytorch/pull/194077)) (cut for length)
- Speed up the cuDNN path of `varlen_attn` by reusing shared sequence metadata and passing cumulative sequence lengths to cuDNN 9.24+ directly ([#194834](https://github.com/pytorch/pytorch/pull/194834), [#194906](https://github.com/pytorch/pytorch/pull/194906)) (cut for length)
### security
