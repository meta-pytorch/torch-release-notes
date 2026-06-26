# Release Notes worksheet xpu

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

## xpu
### bc breaking
### deprecation
### new features
- Add XPU device telemetry APIs for temperature, frequency, power draw, engine utilization, memory bandwidth usage, and used device memory through `torch.xpu.*` ([#181082](https://github.com/pytorch/pytorch/pull/181082), [#183427](https://github.com/pytorch/pytorch/pull/183427), [#183428](https://github.com/pytorch/pytorch/pull/183428), [#183429](https://github.com/pytorch/pytorch/pull/183429), [#183430](https://github.com/pytorch/pytorch/pull/183430), [#183431](https://github.com/pytorch/pytorch/pull/183431))
- Add FP8 blockwise scaling support for `scaled_mm` on XPU ([#173630](https://github.com/pytorch/pytorch/pull/173630), [#176043](https://github.com/pytorch/pytorch/pull/176043))
- Extends XCCL backend support to the latest Intel® Arc™ B-Series GPUs on Linux ([#182003](https://github.com/pytorch/pytorch/pull/182003))

### improvements
- Add `last_level_cache_size` and `is_integrated_gpu` to XPU device properties ([#184499](https://github.com/pytorch/pytorch/pull/184499), [#182624](https://github.com/pytorch/pytorch/pull/182624))
- Add XPU dispatch for `_fused_adagrad_` ([#185577](https://github.com/pytorch/pytorch/pull/185577))
- Support mixed-type operations between Nested and Dense tensors on XPU ([#182654](https://github.com/pytorch/pytorch/pull/182654))
- Support `torch.xpu.device` in Dynamo device management ([#181847](https://github.com/pytorch/pytorch/pull/181847))
- Recognize additional Intel BMG device IDs on XPU ([#183414](https://github.com/pytorch/pytorch/pull/183414))
- Enable XPU device support for sparse Triton ops ([#179805](https://github.com/pytorch/pytorch/pull/179805))
- Enable the `bmm_outer_product` Triton override on XPU ([#180441](https://github.com/pytorch/pytorch/pull/180441))
- Improve test coverage for the XPU backend ([#174370](https://github.com/pytorch/pytorch/pull/174370), [#180881](https://github.com/pytorch/pytorch/pull/180881), [#171154](https://github.com/pytorch/pytorch/pull/171154))
- Support non-blocking pinned device-to-host copies on XPU ([#186224](https://github.com/pytorch/pytorch/pull/186224))
- Refactor the XPU oneDNN integration from the C API to the C++ API ([#184486](https://github.com/pytorch/pytorch/pull/184486))

### bug fixes
- Avoid generating fp64 Triton code for XPU devices that do not support fp64 ([#180854](https://github.com/pytorch/pytorch/pull/180854))
- Fix stream selection for XPU outputs in `CurrentWorkStream` ([#179140](https://github.com/pytorch/pytorch/pull/179140))
- Fix reflection and replication padding on XPU to preserve eager-mode output memory format ([#184484](https://github.com/pytorch/pytorch/pull/184484))
- Fix `addmm` shape handling and `addmv_out` stride preservation on XPU ([#180985](https://github.com/pytorch/pytorch/pull/180985), [#178498](https://github.com/pytorch/pytorch/pull/178498))
- Fix XPU deallocation handling and `XPUPluggableAllocator` registration ([#183865](https://github.com/pytorch/pytorch/pull/183865), [#179392](https://github.com/pytorch/pytorch/pull/179392))
- Fix numerical instability in `logcumsumexp` with complex inputs on XPU ([#174492](https://github.com/pytorch/pytorch/pull/174492))
- Fix `SyclExtension` Windows builds for oneAPI 2025.3 and later ([#170701](https://github.com/pytorch/pytorch/pull/170701))
- Fix `getGlobalIdxFromDevice(-1)` handling on XPU ([#181361](https://github.com/pytorch/pytorch/pull/181361))

### performance
- Add oneDNN-backed `nn.LSTM` inference support on XPU, replacing the per-timestep fused-cell path with a sequence-level primitive ([#185531](https://github.com/pytorch/pytorch/pull/185531))

### docs

### devs
- Respect `MKLROOT`, `CMPLR_ROOT`, and `ONEAPI_ROOT` from `setvars.sh` in `FindMKL.cmake` so custom oneAPI installs are detected correctly ([#183506](https://github.com/pytorch/pytorch/pull/183506))

### not user facing

### security