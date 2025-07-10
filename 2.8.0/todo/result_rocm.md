
# Release Notes worksheet rocm

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

## rocm
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [ROCm] Improve softmax performance ([#149076](https://github.com/pytorch/pytorch/pull/149076))
- [ROCm] NLLLoss (torch.nll_loss) Performance Tuning by Dynamically Selecting # of GPU threads ([#149548](https://github.com/pytorch/pytorch/pull/149548))
- [ROCm] Extend vectorized elementwise kernel to more heterogenous tensor types. ([#149738](https://github.com/pytorch/pytorch/pull/149738))
- Removed ROCM ifdef that governs thread count + smem parallel reduction. ([#149779](https://github.com/pytorch/pytorch/pull/149779))
- [ROCM] Fix in-place aten sum with specialized templated kernels. ([#151230](https://github.com/pytorch/pytorch/pull/151230))
- Document non-pytorch CUDA memory allocation and how to query it ([#150880](https://github.com/pytorch/pytorch/pull/150880))
- [ROCm] opportunistic fastatomics - fix build error with newer compilers ([#152841](https://github.com/pytorch/pytorch/pull/152841))
- [ROCm] Maxpool backward NHWC Perf Improvement targeting Resnet scenarios ([#152267](https://github.com/pytorch/pytorch/pull/152267))
- [ROCm] Improvements to non-vectorized elementwise kernels ([#153184](https://github.com/pytorch/pytorch/pull/153184))
- [ROCm] Fix 3D tensor perf degradation with NHWC format ([#154522](https://github.com/pytorch/pytorch/pull/154522))
- [ROCm] Update maxpool launch config ([#154619](https://github.com/pytorch/pytorch/pull/154619))
- support CUBLASLT_MATMUL_MATRIX_SCALE_OUTER_VEC_32F ([#154680](https://github.com/pytorch/pytorch/pull/154680))
- [ROCm] Enable more parallelism for multi-dimensional reductions ([#155806](https://github.com/pytorch/pytorch/pull/155806))
- [ROCm] Update spack includes ([#152569](https://github.com/pytorch/pytorch/pull/152569))
- [ROCm] cpp_extension allow user to override default flags ([#152432](https://github.com/pytorch/pytorch/pull/152432))
- [ROCm] Exposing Some MIOpen Symbols (#2176) ([#154545](https://github.com/pytorch/pytorch/pull/154545))
- [ROCm] MIOpen: Get current device from Torch rather than HIP in handle creation ([#154549](https://github.com/pytorch/pytorch/pull/154549))
- [ROCm] Enable BF16 NCHW Mixed batchnorm on MIOpen if ROCm>=6.4 ([#154611](https://github.com/pytorch/pytorch/pull/154611))
### not user facing
### security
