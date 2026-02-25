
# Release Notes worksheet linalg_frontend

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

## linalg_frontend
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [xplat] Fix build warnings and update mcf dependency ([#170102](https://github.com/pytorch/pytorch/pull/170102))
- linalg._powsum and _foreach_powsum ops ([#172685](https://github.com/pytorch/pytorch/pull/172685))
- [MAGMA] issue a deprecation warning upon retrieving/setting linalg backend ([#172823](https://github.com/pytorch/pytorch/pull/172823))
- [MAGMA] svd: deprecate magma backend and dispatch to cusolver unconditionally ([#172824](https://github.com/pytorch/pytorch/pull/172824))
- [MAGMA][CUDA] triangular_solve: deprecate MAGMA and dispatch to cuBLAS unconditionally ([#174109](https://github.com/pytorch/pytorch/pull/174109))
- [MAGMA][CUDA] lstsq: deprecate MAGMA and dispatch to cuSolver/cuBLAS unconditionally ([#174779](https://github.com/pytorch/pytorch/pull/174779))
- [ROCm] ADDMM behavior now takes into account preferred BLAS backend. ([#174350](https://github.com/pytorch/pytorch/pull/174350))
### not user facing
- [ROCm][CI] skip tests for mi200 ([#170205](https://github.com/pytorch/pytorch/pull/170205))
- Remove outdated CUDA and ROCm skip conditions ([#170868](https://github.com/pytorch/pytorch/pull/170868))
- [ROCm][CI] skip test_addmm_relu_tunableop_rocm_cuda_float64 on MI350 ([#170920](https://github.com/pytorch/pytorch/pull/170920))
- linalg: sort eigenvalues in eig/eigvals comparison tests ([#171717](https://github.com/pytorch/pytorch/pull/171717))
- Allow for unaligned cpu inputs ([#173395](https://github.com/pytorch/pytorch/pull/173395))
- More test file assert removal ([#174255](https://github.com/pytorch/pytorch/pull/174255))
- [ROCm] Skip linalg tests when MAGMA is not available ([#173688](https://github.com/pytorch/pytorch/pull/173688))
- test_linalg: Skip test__int4_mm and test_compile_int4_mm on <CDNA2 ([#173358](https://github.com/pytorch/pytorch/pull/173358))
### security
