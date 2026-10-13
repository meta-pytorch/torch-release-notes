
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
### improvements
### bug fixes
- [SDPA] Support mixed head dimensions with FA4 ([#193039](https://github.com/pytorch/pytorch/pull/193039))
- Treat an engaged-but-undefined optional weight as no weight in rms_norm ([#195574](https://github.com/pytorch/pytorch/pull/195574))
### performance
### docs
- [docs] Fix the linear_cross_entropy reference snippet ([#198941](https://github.com/pytorch/pytorch/pull/198941))
### devs
### Untopiced
- linear_cross_entropy: support probability targets with reduction='none' ([#188296](https://github.com/pytorch/pytorch/pull/188296))
- [ROCm][NN] Preserve Module.to meta tensor guidance with C++ stack traces ([#191151](https://github.com/pytorch/pytorch/pull/191151))
- Fix nan g gradient and null pointer in weight_norm CPU kernel for empty input ([#192179](https://github.com/pytorch/pytorch/pull/192179))
- Fix 64-bit indexing in spatial softmax backward ([#188031](https://github.com/pytorch/pytorch/pull/188031))
- [kimi 2.7] Support deterministic upsample bicubic backward ([#193707](https://github.com/pytorch/pytorch/pull/193707))
- [ROCm][NN] Preserve Module.to meta tensor guidance with C++ stack traces ([#191151](https://github.com/pytorch/pytorch/pull/191151))
- [ROCm] Fix MIOpen RNN dropout mask reuse and gradient stall ([#189285](https://github.com/pytorch/pytorch/pull/189285))
- Fix native_batch_norm segfaulting in eval mode without running stats ([#194031](https://github.com/pytorch/pytorch/pull/194031))
- [CUDA] Fix out-of-bounds/invalid-gradient in layer_norm's huge-M gamma/beta backward ([#193016](https://github.com/pytorch/pytorch/pull/193016))
- Use `_unsafe_view` in the nD `linear` fast path ([#194077](https://github.com/pytorch/pytorch/pull/194077))
- [PERFORMANCE] [NN] Change `torch._C._get_tracing_state()` to `torch._C._is_tracing()` for around 15% improved performance of `module.py` `_call_impl()` ([#196236](https://github.com/pytorch/pytorch/pull/196236))
- Clear ModuleTest/CriterionTest arg cache at every entry point ([#196609](https://github.com/pytorch/pytorch/pull/196609))
- [PERFORMANCE] [NN] Change `torch._C._get_tracing_state()` to `torch._C._is_tracing()` for around 15% improved performance of `module.py` `_call_impl()` ([#196236](https://github.com/pytorch/pytorch/pull/196236))
- [meta] Reject a non-positive pixel_shuffle/unshuffle factor ([#195224](https://github.com/pytorch/pytorch/pull/195224))
- MPS: also gate int64 scatter_reduce and the large-tensor tests on M1 ([#198689](https://github.com/pytorch/pytorch/pull/198689))
- MPS: also gate int64 scatter_reduce and the large-tensor tests on M1 ([#198689](https://github.com/pytorch/pytorch/pull/198689))
- Fix AVX512 grid sampler mask gather ([#197635](https://github.com/pytorch/pytorch/pull/197635))
- varlen bug fix: auto num splits ([#198872](https://github.com/pytorch/pytorch/pull/198872))
- Fix cuDNN/MIOpen RNN backward reading the saved output with assumed strides ([#198773](https://github.com/pytorch/pytorch/pull/198773))
- [ROCm] Fix layer_norm vectorized chunk offset overflow ([#199438](https://github.com/pytorch/pytorch/pull/199438))
- Preserve channels_last_3d in InstanceNorm3d (#199112) ([#199112](https://github.com/pytorch/pytorch/pull/199112))
- Fix CUDA SDPA grid overflow for large batches and heads ([#199594](https://github.com/pytorch/pytorch/pull/199594))
### not user facing
- linear_cross_entropy: test and document bias with probability targets ([#188433](https://github.com/pytorch/pytorch/pull/188433))
- [CUDA][CuTeDSL] Wire up Quack RMSNorm to `sm12x` ([#192400](https://github.com/pytorch/pytorch/pull/192400))
- [CUDA] Add NHWC GroupNorm Implementation ([#191945](https://github.com/pytorch/pytorch/pull/191945))
- [Test] Refactor test/test_nn.py to be device-agnostic [7/N] ([#189536](https://github.com/pytorch/pytorch/pull/189536))
- [ROCm] Fix MI200 CI test failures: measured tolerances, skips ([#192993](https://github.com/pytorch/pytorch/pull/192993))
- [Test] Add tf32_on_and_off tolerance to previously skipped tests ([#193949](https://github.com/pytorch/pytorch/pull/193949))
- Consolidate device-side assert stderr checks into shared helper ([#193613](https://github.com/pytorch/pytorch/pull/193613))
- [BE] Gate test_ReplicationPad2d_large expected failure pre macOS 27 ([#194726](https://github.com/pytorch/pytorch/pull/194726))
- [cuDNN][CTCLoss][TEST] Don't use blank targets in cuDNN CTCLoss tests ([#195620](https://github.com/pytorch/pytorch/pull/195620))
- Fix type stub for torch.nn.functional.mse_loss by adding weight argument ([#196126](https://github.com/pytorch/pytorch/pull/196126))
- linear_cross_entropy: extract what a backend override has to reuse ([#195331](https://github.com/pytorch/pytorch/pull/195331))
- [ROCm] Unskip batchnorm, RNN and 64-bit upsampling tests in test_nn ([#197904](https://github.com/pytorch/pytorch/pull/197904))
- [Test] Refactor test/test_nn.py to be device-agnostic [9/N] ([#189538](https://github.com/pytorch/pytorch/pull/189538))
- [Test] Refactor test/test_nn.py to be device-agnostic [10/N] ([#194038](https://github.com/pytorch/pytorch/pull/194038))
- [Test] Refactor test/test_nn.py to be device-agnostic [11/N] ([#194045](https://github.com/pytorch/pytorch/pull/194045))
- Validate input/hidden dimension consistency in RNN cells ([#191232](https://github.com/pytorch/pytorch/pull/191232))
- [Test] Refactor test/test_nn.py to be device-agnostic [12/N] ([#194191](https://github.com/pytorch/pytorch/pull/194191))
- [Test] Refactor test/test_nn.py to be device-agnostic [13/N] ([#194863](https://github.com/pytorch/pytorch/pull/194863))
- [Test] Refactor test/test_nn.py to be device-agnostic [14/N] ([#198467](https://github.com/pytorch/pytorch/pull/198467))
- [Test] Refactor test/test_nn.py to be device-agnostic [15/N] ([#198848](https://github.com/pytorch/pytorch/pull/198848))
- [Test] Add hw_classification in test_nn.py ([#198859](https://github.com/pytorch/pytorch/pull/198859))
- [BE] Mark test_large_max_pool2d_ch_last as expected failure on MPS ([#199006](https://github.com/pytorch/pytorch/pull/199006))
- [docs] Fix RNN example to support backward pass ([#173888](https://github.com/pytorch/pytorch/pull/173888))
### security
