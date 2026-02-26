
# Release Notes worksheet cuda

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

## cuda
### bc breaking
### deprecation
### new features
### improvements
- Remove _scaled_mm layout check on Blackwells ([#170693](https://github.com/pytorch/pytorch/pull/170693))
- Speedup grouped_mm a bit ([#170802](https://github.com/pytorch/pytorch/pull/170802))
- Add uint16, uint32, uint64 support to JIT CUDA kernels ([#174303](https://github.com/pytorch/pytorch/pull/174303))
### bug fixes
### performance
### docs
### devs
### Untopiced
- Make CachingHostAllocator work with memory pools. ([#167507](https://github.com/pytorch/pytorch/pull/167507))
- Fix #169607 ([#170710](https://github.com/pytorch/pytorch/pull/170710))
- Use accscalar_t for interpolation accumulators in CUDA UpSample kernel ([#170661](https://github.com/pytorch/pytorch/pull/170661))
- Fix computation of NVRTC library hash ([#169214](https://github.com/pytorch/pytorch/pull/169214))
- Reinstate format-string args in CUDA_KERNEL_ASSERT_VERBOSE call in IndexKernelUtils.cu ([#170913](https://github.com/pytorch/pytorch/pull/170913))
- Cleanup at::numeric_limits ([#171111](https://github.com/pytorch/pytorch/pull/171111))
- [Allocator] Make large segment size configurable ([#172056](https://github.com/pytorch/pytorch/pull/172056))
- CUDA Stream Sanitizer fixes ([#172562](https://github.com/pytorch/pytorch/pull/172562))
- Update launch bounds for ctc_loss_gpu_template on SM12+ ([#172447](https://github.com/pytorch/pytorch/pull/172447))
- [NATIVE] [CUDA] Switch order of blocked reduce in reduction_template.cuh ([#173425](https://github.com/pytorch/pytorch/pull/173425))
- Use opmath_t and not double compute in fused SGD and Adam ([#173227](https://github.com/pytorch/pytorch/pull/173227))
- Fast memory snapshot ([#173949](https://github.com/pytorch/pytorch/pull/173949))
- Move EventPool::Event to c10 ([#158220](https://github.com/pytorch/pytorch/pull/158220))
- Reuse CUDAEventPool in CUDA caching host allocator ([#168345](https://github.com/pytorch/pytorch/pull/168345))
### not user facing
- Move CUDAEvent to c10 ([#158219](https://github.com/pytorch/pytorch/pull/158219))
- [ATen][NATIVE][CUDA] Allow all 10.x compute capabilities for using vec8 kernel ([#174362](https://github.com/pytorch/pytorch/pull/174362))
### security
