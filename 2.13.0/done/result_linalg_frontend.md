
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
- Add `Half` and `BFloat16` dispatch support for `torch.trace` on CPU ([#184874](https://github.com/pytorch/pytorch/pull/184874))
- Improve heuristics for the cuSOLVER vs cuBLAS backend switch in `torch.linalg.lu` ([#185344](https://github.com/pytorch/pytorch/pull/185344))
### bug fixes
- Validate pivot range in `torch.linalg.ldl_solve` CPU kernel ([#181032](https://github.com/pytorch/pytorch/pull/181032))
- Fix rocBLAS tunable GEMM solution handling in TunableOp ([#182380](https://github.com/pytorch/pytorch/pull/182380))
- Route fp16 backward GEMMs to rocBLAS to preserve subnormals ([#183766](https://github.com/pytorch/pytorch/pull/183766))
### performance
### docs
### devs
### Untopiced
### not user facing
- [ROCm] Replace MI300 TF32 test skips with measured dispositions ([#180926](https://github.com/pytorch/pytorch/pull/180926))
- Add type annotations to torch/_linalg_utils.py ([#181464](https://github.com/pytorch/pytorch/pull/181464))
- [ROCm] Enabled test_linalg tests that were skipped due to skipCUDAIfNoMagmaAndNoCusolver ([#180303](https://github.com/pytorch/pytorch/pull/180303))
- [ROCm] Add CK BLAS backend torch.mm test ([#182195](https://github.com/pytorch/pytorch/pull/182195))
- [ROCm] Enable float8 scaled GEMM TunableOp tests for MI350 ([#182079](https://github.com/pytorch/pytorch/pull/182079))
- [ROCm] Enable TF32 TunableOp tests for all ROCm architectures ([#183474](https://github.com/pytorch/pytorch/pull/183474))
- [Docs] Fix linalg.norm docstring: rename parameter `A` to `input` ([#181764](https://github.com/pytorch/pytorch/pull/181764))
- [ROCm] Enable test_preferred_linalg_library test for ROCm ([#184427](https://github.com/pytorch/pytorch/pull/184427))
- [Test] Extract CUDA-only tests into TestLinalgCUDA for test_linalg ([#183586](https://github.com/pytorch/pytorch/pull/183586))
- [Test] Convert 8 @onlyCUDA to @onlyAccelerator for test_linalg ([#183587](https://github.com/pytorch/pytorch/pull/183587))
- [Test] Replace wrong-device patterns with torch.accelerator for test_linalg ([#183588](https://github.com/pytorch/pytorch/pull/183588))
### security
