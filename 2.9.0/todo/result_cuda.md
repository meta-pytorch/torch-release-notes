
# Release Notes worksheet cuda

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.
* Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

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

## cuda
### bc breaking
### deprecation
### new features
- MXFP8 grouped GEMM support for torch._scaled_grouped_mm + submodule bump ([#162209](https://github.com/pytorch/pytorch/pull/162209))
### improvements
### bug fixes
- [FlexAttention][TF32] Handle uninitialized `torch.backends.cuda.matmul.fp32_precision` ([#161102](https://github.com/pytorch/pytorch/pull/161102))
### performance
### docs
### devs
### Untopiced
- Prevent cudaStreamSync when indexing GPU tensors with boolean CPU mask ([#156384](https://github.com/pytorch/pytorch/pull/156384))
- cublaslt/hipblaslt persistent workspace ([#156495](https://github.com/pytorch/pytorch/pull/156495))
- Remove unnecessary warnings during the ATen compilation process. ([#157703](https://github.com/pytorch/pytorch/pull/157703))
- Slightly improve error message from repeat_interleave kernel ([#157996](https://github.com/pytorch/pytorch/pull/157996))
- Add framework for explanations for common CUDA errors ([#158395](https://github.com/pytorch/pytorch/pull/158395))
- [ROCm] delete un-needed workaround for tensor.item() ([#158486](https://github.com/pytorch/pytorch/pull/158486))
- [CUDA] fix nansum in non-JIT build ([#158633](https://github.com/pytorch/pytorch/pull/158633))
- [fbgemm_gpu] Upgrade KernelLauncher kernelLaunchCheck to print help string ([#158896](https://github.com/pytorch/pytorch/pull/158896))
- [cutlass] Prep for cutlass upgrade by ignoring Wunused-but-set-variable ([#159276](https://github.com/pytorch/pytorch/pull/159276))
- Disable cudagraph GCs by default ([#158649](https://github.com/pytorch/pytorch/pull/158649))
- [CUDA] Decrease launch bounds of CTCLoss backward for blackwell ([#159522](https://github.com/pytorch/pytorch/pull/159522))
- [ROCm] Set thread_work_size to 16 for vectorized elementwise kernels for MI300X ([#160444](https://github.com/pytorch/pytorch/pull/160444))
- [ROCm] Improve reduction sum performance ([#160466](https://github.com/pytorch/pytorch/pull/160466))
- [ROCm] fix large tensor sort on MI350 ([#161054](https://github.com/pytorch/pytorch/pull/161054))
- Workaround ATen SFINAE under libc++ ([#161101](https://github.com/pytorch/pytorch/pull/161101))
- [ROCm] Unroll loads in global_reduce ([#161181](https://github.com/pytorch/pytorch/pull/161181))
- [CUDAGraph] Add getter for cuda graph exec ([#161294](https://github.com/pytorch/pytorch/pull/161294))
- [ROCm] No-fence global reduce ([#161180](https://github.com/pytorch/pytorch/pull/161180))
### not user facing
- [ATen][CUDA][CUB] Implement changes to CCCL (CUB/Thrust/LibCUDACXX) usage in ATen ([#153373](https://github.com/pytorch/pytorch/pull/153373))
- [Refactor] Add maybe unused flag to remove warning ([#157655](https://github.com/pytorch/pytorch/pull/157655))
- [ROCm]  Use opportunistic fastatomics based on hueristics ([#159430](https://github.com/pytorch/pytorch/pull/159430))
- [ROCm] Limit number of values per thread for reductions on three dimensions ([#159652](https://github.com/pytorch/pytorch/pull/159652))
- [ATen][CUDA] Use new CCCL API in v2.8 ([#160554](https://github.com/pytorch/pytorch/pull/160554))
### security
