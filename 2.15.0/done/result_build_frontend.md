
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
- Support building C++/CUDA extensions with `torch.utils.cpp_extension` on Windows ARM64: the CUDA and cuDNN libraries are now looked up under `lib/arm64` instead of the x64 directories ([#191656](https://github.com/pytorch/pytorch/pull/191656))
### bug fixes
- Fix Windows source builds with MSVC silently computing wrong results in `parallel_for` kernels. `torch_cpu` linked both the `vcomp` and `libomp` OpenMP runtimes, so every worker thread saw itself as thread 0 of 1 and processed the whole range. This also fixes wrong CPU `scaled_dot_product_attention` results with multiple intra-op threads ([#193792](https://github.com/pytorch/pytorch/pull/193792))
- Fix cross-compiled builds producing an untagged `_C.so` that the target interpreter cannot import, by setting `Python_SOABI` when cross-compiling ([#189388](https://github.com/pytorch/pytorch/pull/189388))
- Fix BLAS/LAPACK detection for ATLAS, vecLib, BLIS and FlexiBLAS. A successful lookup could leave `BLAS_LIBRARIES` unset or let LAPACK detection pick a different BLAS than the one requested ([#196427](https://github.com/pytorch/pytorch/pull/196427), [#196428](https://github.com/pytorch/pytorch/pull/196428), [#196430](https://github.com/pytorch/pytorch/pull/196430))
- Fix the Metal 4.0 capability check accepting SDKs that support `-std=metal4.0` but lack the MPP cooperative-tensor APIs, which made the build fail later when compiling the Metal 4 attention kernels ([#195302](https://github.com/pytorch/pytorch/pull/195302))
- Fix the embedded Metal shaders not being regenerated when headers under `c10/metal` change, which left stale shaders in incremental macOS builds that only have the Command Line Tools installed ([#196202](https://github.com/pytorch/pytorch/pull/196202))
### performance
### docs
### devs
- Add an opt-in `USE_CMAKE_INSTRUMENTATION=1` build option that uses CMake's build instrumentation (CMake >= 4.3) to collect and summarize build metrics ([#189455](https://github.com/pytorch/pytorch/pull/189455))
- Turn off `USE_FLASH_ATTENTION` automatically when none of the target CUDA architectures is sm80 or newer, instead of compiling kernels that can never run ([#194502](https://github.com/pytorch/pytorch/pull/194502))
- Fix the misspelled `CUDA_LIMIT_GPU_ARCHITECTURE` in CUDA arch autodetection. The limit is now derived from the newest architecture the CUDA toolkit knows, and newer GPUs are clamped to that architecture plus PTX ([#195695](https://github.com/pytorch/pytorch/pull/195695))
- Honor `USE_MIMALLOC=OFF` on Windows and AArch64, where it was previously ignored ([#199064](https://github.com/pytorch/pytorch/pull/199064))
- Fix the FlashAttention CUDA build on Windows with MSVC in C++20 mode ([#197382](https://github.com/pytorch/pytorch/pull/197382))
### not user facing
### security
