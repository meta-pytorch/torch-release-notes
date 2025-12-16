
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
- [ROCm/Windows] Support aotriton for scaled_dot_product_attention on Windows. ([#162330](https://github.com/pytorch/pytorch/pull/162330))
- [ROCm/Windows] Support aotriton for scaled_dot_product_attention on Windows. ([#162330](https://github.com/pytorch/pytorch/pull/162330))
### docs
### devs
### Untopiced
- [ROCm] enable grouped gemm fallback ([#162419](https://github.com/pytorch/pytorch/pull/162419))
- [ROCm] rocblas Aten GEMM overload for FP32 output from FP16/BF16 inputs ([#162600](https://github.com/pytorch/pytorch/pull/162600))
- [ROCm] Support torch.cuda._compile_kernel ([#162510](https://github.com/pytorch/pytorch/pull/162510))
- [ROCm/Windows] Support load_inline on windows ([#162577](https://github.com/pytorch/pytorch/pull/162577))
- [ROCm] fix hardsigmoid op ([#162758](https://github.com/pytorch/pytorch/pull/162758))
- [ROCm] use hipSolver instead of MAGMA for Cholesky ([#163977](https://github.com/pytorch/pytorch/pull/163977))
- [ROCm] fix carveout feature ([#164303](https://github.com/pytorch/pytorch/pull/164303))
- [ROCm] add gfx1150 gfx1151 to supported gemm lists ([#164744](https://github.com/pytorch/pytorch/pull/164744))
- [ROCm] Add scaled_mm v2 support. ([#165528](https://github.com/pytorch/pytorch/pull/165528))
- [ROCm][Windows] Enable AOTriton runtime compile on Windows ([#165538](https://github.com/pytorch/pytorch/pull/165538))
- [ROCm][layer_norm] Use __builtin_amdgcn_rcpf(x) instead of 1.f/x ([#165589](https://github.com/pytorch/pytorch/pull/165589))
- [ROCm] add torch.version.rocm, distinct from torch.version.hip ([#168097](https://github.com/pytorch/pytorch/pull/168097))
### not user facing
- [AMD][gfx1100] test_decompose_mem_bound_mm.py tolerance increase ([#165625](https://github.com/pytorch/pytorch/pull/165625))
- [ROCm][CI] Upgrade ROCm CI to 7.1 ([#166743](https://github.com/pytorch/pytorch/pull/166743))
- [ROCm][CI] Upgrade ROCm CI to 7.1 ([#166743](https://github.com/pytorch/pytorch/pull/166743))
### security
