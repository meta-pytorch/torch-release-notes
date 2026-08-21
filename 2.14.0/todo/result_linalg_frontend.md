
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
- Fix segfault in torch.lu_unpack with mismatched LU_pivots shape ([#187660](https://github.com/pytorch/pytorch/pull/187660))
- Add linalg polar backward for CPU/MPS/CUDA ([#189732](https://github.com/pytorch/pytorch/pull/189732))
### bug fixes
### performance
- Avoid D2D copy for addmm with distinct C and D ([#191706](https://github.com/pytorch/pytorch/pull/191706))
- Avoid D2D copy for addmm with distinct C and D ([#191706](https://github.com/pytorch/pytorch/pull/191706))
- Avoid D2D copy for addmm with distinct C and D ([#191706](https://github.com/pytorch/pytorch/pull/191706))
### docs
- [Docs] Clarify norm docs for complex inputs ([#190381](https://github.com/pytorch/pytorch/pull/190381))
### devs
### Untopiced
- Fix incorrect rank in torch.linalg.lstsq(driver='gelsy') due to stale JPVT values ([#187436](https://github.com/pytorch/pytorch/pull/187436))
- [ROCm] Split CK SDPA vs CK GEMM arch gating ([#187267](https://github.com/pytorch/pytorch/pull/187267))
- Add `torch.linalg.matrix_sqrth` for Symmetric/Hermitian Positive-Definite Matrices ([#187987](https://github.com/pytorch/pytorch/pull/187987))
- [CUDA] Add TunableOp support for cublasLt ([#186270](https://github.com/pytorch/pytorch/pull/186270))
- Fix misleading error for complex order in torch.linalg.cond ([#188591](https://github.com/pytorch/pytorch/pull/188591))
- Use sym_numel in linalg_cond string overload ([#187614](https://github.com/pytorch/pytorch/pull/187614))
- [TunableOp] Fix offline sub-matrix detection when a leading dimension aliases a GEMM dim ([#189355](https://github.com/pytorch/pytorch/pull/189355))
- [BE][Ez]: Add c10::SmallVector reserve calls and simplify log func calls ([#185821](https://github.com/pytorch/pytorch/pull/185821))
### not user facing
- CUDA linalg: hoist cuSOLVER GETRF workspace allocation out of lu_factor_looped_cusolver batch loop ([#181998](https://github.com/pytorch/pytorch/pull/181998))
- [ROCm] Re-enable test_preferred_linalg_library test for ROCm ([#187703](https://github.com/pytorch/pytorch/pull/187703))
- Fix linalg.vector_norm docstring: ord does not accept 'fro'/'nuc' ([#188204](https://github.com/pytorch/pytorch/pull/188204))
- [ROCm] Enable linalg tests for eig, ldl_solve operator (hipsolver) & enable test_linalg_solve, test_triangular_solve linalg tests with cuBLAS path ([#185557](https://github.com/pytorch/pytorch/pull/185557))
- [ROCm] Merge test_norm_matrix_degenerate_shapes_old_numpy & test_norm_matrix_degenerate_shapes to run for older & newer Numpy versions ([#187011](https://github.com/pytorch/pytorch/pull/187011))
- [CUDA][cuBLAS] Change cuBLAS default workspace size for SM 11.0 to 32 MiB  ([#189312](https://github.com/pytorch/pytorch/pull/189312))
- [Test] [CUDA] Refactor test_cublaslt_candidate_tunableop ([#189459](https://github.com/pytorch/pytorch/pull/189459))
- Skip test_polar_matches_svd when cuSOLVER lacks Xpolar ([#189875](https://github.com/pytorch/pytorch/pull/189875))
- Fix matmul folding when an inner folded dim has size 1 ([#186178](https://github.com/pytorch/pytorch/pull/186178))
### security
