
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
- [CUDA] [PERFORMANCE] Improve performance for `ScaledGroupMM.cu` by avoiding redundant IO/compute via indicating that indicating that `ElementC` type is void ([#178325](https://github.com/pytorch/pytorch/pull/178325))
- [CUDA] [PERFORMANCE] Improve performance for `RowwiseScaledMM.cu` by avoiding redundant IO/compute via indicating that indicating that `ElementC` type is void ([#178644](https://github.com/pytorch/pytorch/pull/178644))
### bug fixes
### performance
- Update eigh CUDA heuristics ([#175403](https://github.com/pytorch/pytorch/pull/175403))
### docs
### devs
### Untopiced
- [CUBLAS][Blackwell] Try to reenable 32MiB workspaces on Blackwell ([#175344](https://github.com/pytorch/pytorch/pull/175344))
- [CUDA][TensorIterator] Improve vectorized elementwise kernel: instruction cache ([#175336](https://github.com/pytorch/pytorch/pull/175336))
- [CUDA] Fix offset_t operators to be __host__ __device__ in SortStable.cu ([#175997](https://github.com/pytorch/pytorch/pull/175997))
- [pt] Reland vec8 vectorization ([#176352](https://github.com/pytorch/pytorch/pull/176352))
- fix cuda torch.topk index bug for super long input which are over 32-bit INT_MAX length ([#176095](https://github.com/pytorch/pytorch/pull/176095))
- Fix `test/inductor/test_fp8.py` hang on sm89 ([#177573](https://github.com/pytorch/pytorch/pull/177573))
- Use fp8 conversion intrinsics on Hopper+ to work around ptxas codegen bug ([#177870](https://github.com/pytorch/pytorch/pull/177870))
- [CUDA] [Green Context] Add support for workqueue limit ([#177242](https://github.com/pytorch/pytorch/pull/177242))
- Remove dead avg_pool3d backward shape-check variables in CUDA ([#178893](https://github.com/pytorch/pytorch/pull/178893))
- [AMD] Use optimized tiled kernel for LayerNorm gamma beta backward ([#179019](https://github.com/pytorch/pytorch/pull/179019))
- [Typing] ot -> to ([#179265](https://github.com/pytorch/pytorch/pull/179265))
- [CUDA] Fix wrong non-atomic handling in `AdaptiveMaxPooling2d.cu` ([#179261](https://github.com/pytorch/pytorch/pull/179261))
- [Typo] Quiet -> Quite ([#179266](https://github.com/pytorch/pytorch/pull/179266))
- [CUDA] Fix wrong ComplexTransform const kTransformB in fpA_intB_gemm.h ([#179271](https://github.com/pytorch/pytorch/pull/179271))
- [CUDA] Fix wrong LayoutB in fpA_intB_gemm.h ([#179269](https://github.com/pytorch/pytorch/pull/179269))
- [reland 2][pytorch] Preemptive OOM rejection using per_process_memory_fraction + throw_on_cudamalloc_oom (#179473) ([#179473](https://github.com/pytorch/pytorch/pull/179473))
- [cuda graphs] Add enable_annotations kwarg to torch.cuda.graph ([#179867](https://github.com/pytorch/pytorch/pull/179867))
### not user facing
- [BE] add missing assert on cuda device synchronize in ATen tests ([#174966](https://github.com/pytorch/pytorch/pull/174966))
- [BE] Tesor -> Tensor ([#175061](https://github.com/pytorch/pytorch/pull/175061))
- [CUDA/ROCm] avoid double casting in ReduceLogicKernel ([#176132](https://github.com/pytorch/pytorch/pull/176132))
- Back out "[CUDA][cuBLASLt] set cuBLASLt as a default BLAS backend when available (#174594)" (#177703) ([#177703](https://github.com/pytorch/pytorch/pull/177703))
- Use aminmax instead of min and max kernels in histc ([#178011](https://github.com/pytorch/pytorch/pull/178011))
- Nit fix: Align state_step tensor max to param tensor max ([#178913](https://github.com/pytorch/pytorch/pull/178913))
### security
