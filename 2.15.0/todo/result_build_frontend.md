
# Release Notes worksheet build_frontend

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

## build_frontend
### bc breaking
### deprecation
### new features
### improvements
- Support `torch.utils.cpp_extension` CUDA builds on Windows ARM64 ([#191656](https://github.com/pytorch/pytorch/pull/191656))
### bug fixes
- Fix Windows MSVC source builds computing wrong results in `parallel_for` kernels, including CPU `scaled_dot_product_attention` ([#193792](https://github.com/pytorch/pytorch/pull/193792))
- Fix cross-compiled builds producing a `_C.so` that the target interpreter cannot import ([#189388](https://github.com/pytorch/pytorch/pull/189388))
- Fix BLAS/LAPACK detection for ATLAS, vecLib, BLIS and FlexiBLAS ([#196427](https://github.com/pytorch/pytorch/pull/196427), [#196428](https://github.com/pytorch/pytorch/pull/196428), [#196430](https://github.com/pytorch/pytorch/pull/196430))
- Fix macOS builds failing on SDKs that lack the Metal 4 cooperative-tensor APIs ([#195302](https://github.com/pytorch/pytorch/pull/195302))
- Fix stale embedded Metal shaders in incremental macOS builds ([#196202](https://github.com/pytorch/pytorch/pull/196202))
- Fix the C++20 requirement not propagating through the CMake `torch` target or being checked on MSVC ([#190784](https://github.com/pytorch/pytorch/pull/190784), [#197417](https://github.com/pytorch/pytorch/pull/197417))
- Fix a clang `time_t` compile error in `torch/csrc/stable/macros.h` ([#197021](https://github.com/pytorch/pytorch/pull/197021))
### performance
### docs
### devs
- Add an opt-in `USE_CMAKE_INSTRUMENTATION=1` build option to collect build metrics (CMake >= 4.3) ([#189455](https://github.com/pytorch/pytorch/pull/189455))
- Turn off `USE_FLASH_ATTENTION` automatically when no target CUDA architecture is sm80 or newer ([#194502](https://github.com/pytorch/pytorch/pull/194502))
- Fix the misspelled `CUDA_LIMIT_GPU_ARCHITECTURE` in CUDA architecture autodetection ([#195695](https://github.com/pytorch/pytorch/pull/195695))
- Honor `USE_MIMALLOC=OFF` on Windows and AArch64 ([#199064](https://github.com/pytorch/pytorch/pull/199064))
- Fix the FlashAttention CUDA build on Windows with MSVC in C++20 mode ([#197382](https://github.com/pytorch/pytorch/pull/197382))
### not user facing
### security
