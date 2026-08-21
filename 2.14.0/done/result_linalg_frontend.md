
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
- Add `torch.linalg.matrix_sqrth` for computing the principal square root of symmetric or Hermitian positive-definite matrices, with support for batched inputs, autograd, `vmap`, and `torch.compile` ([#187987](https://github.com/pytorch/pytorch/pull/187987))
- Add CUDA cuBLASLt support to TunableOp, including controls for the number of heuristic candidates through `torch.cuda.tunable.set_cublaslt_requested_algo_count()` and `PYTORCH_TUNABLEOP_CUBLASLT_REQUESTED_ALGO_COUNT` ([#186270](https://github.com/pytorch/pytorch/pull/186270))
### improvements
- Add backward support for `torch.linalg.polar` on CPU, CUDA, and MPS ([#189732](https://github.com/pytorch/pytorch/pull/189732))
- Allow `torch.backends.cuda.preferred_blas_library("ck")` to select the CK GEMM backend on ROCm `gfx90a` devices by separating GEMM support from CK attention support ([#187267](https://github.com/pytorch/pytorch/pull/187267))
- Expand ROCm backend coverage for `torch.linalg.eig`, `torch.linalg.ldl_solve`, `torch.linalg.solve`, and `torch.linalg.solve_triangular` through hipSOLVER and hipBLAS paths ([#185557](https://github.com/pytorch/pytorch/pull/185557))
- Enable `torch.linalg.eig` and `torch.linalg.cholesky_ex` to use hipSOLVER's newer 64-bit APIs on ROCm 7.14 and later, further reducing their MAGMA dependency ([#188720](https://github.com/pytorch/pytorch/pull/188720))
### bug fixes
- Fix `torch.lu_unpack` segfaulting when `LU_pivots` has a shape inconsistent with `LU_data`; invalid shapes now raise a clear error ([#187660](https://github.com/pytorch/pytorch/pull/187660))
- Fix `torch.linalg.lstsq(driver="gelsy")` returning an incorrect rank on CPU when stale pivot values leaked between batched LAPACK calls ([#187436](https://github.com/pytorch/pytorch/pull/187436))
- Fix `torch.linalg.cond` reporting a misleading overflow error for a complex norm order; invalid orders now raise `ValueError` with a clear message ([#188591](https://github.com/pytorch/pytorch/pull/188591))
- Fix `torch.compile(dynamic=True)` failing on `torch.linalg.cond` with `p="fro"` or `p="nuc"` because symbolic tensor sizes were queried as concrete values ([#187614](https://github.com/pytorch/pytorch/pull/187614))
- Fix offline TunableOp tuning silently using the wrong GEMM shape when a padded leading dimension matches another matrix dimension ([#189355](https://github.com/pytorch/pytorch/pull/189355))
- Fix `CUBLAS_STATUS_NOT_SUPPORTED` failures in matrix multiplication on CUDA compute capability 11.0 by increasing the default cuBLAS workspace to 32 MiB ([#189312](https://github.com/pytorch/pytorch/pull/189312))
### performance
- Speed up CUDA `torch.addmm` when the addend and output are distinct row-major tensors by letting cuBLASLt consume both pointers directly instead of copying the addend into the output first ([#191706](https://github.com/pytorch/pytorch/pull/191706))
- Reduce allocator overhead for batched CUDA LU factorization by allocating the cuSOLVER GETRF workspace once per batch instead of once per matrix ([#181998](https://github.com/pytorch/pytorch/pull/181998))
- Speed up `torch.matmul` for viewable batched inputs with a size-one folded dimension by dispatching through the flattened `mm` path instead of `bmm` ([#186178](https://github.com/pytorch/pytorch/pull/186178))
### docs
- Clarify `torch.linalg.norm`, `matrix_norm`, and `vector_norm` behavior for complex inputs, and correct the documented `ord` values accepted by `vector_norm` ([#190381](https://github.com/pytorch/pytorch/pull/190381), [#188204](https://github.com/pytorch/pytorch/pull/188204))
### devs
### not user facing
- Reserve `c10::SmallVector` capacity and simplify logarithm calls across internal ATen implementations ([#185821](https://github.com/pytorch/pytorch/pull/185821))
- Re-enable the preferred linear algebra library test on ROCm ([#187703](https://github.com/pytorch/pytorch/pull/187703))
- Consolidate matrix-norm degenerate-shape tests across older and newer NumPy versions ([#187011](https://github.com/pytorch/pytorch/pull/187011))
- Refactor the cuBLASLt TunableOp candidate test to avoid timing-dependent failures ([#189459](https://github.com/pytorch/pytorch/pull/189459))
- Skip the direct Xpolar test when the loaded cuSOLVER version does not provide Xpolar; production already falls back to SVD ([#189875](https://github.com/pytorch/pytorch/pull/189875))
- Replace deprecated internal `torch.norm` calls with equivalent `torch.linalg.vector_norm` and `torch.linalg.matrix_norm` calls ([#185097](https://github.com/pytorch/pytorch/pull/185097))
### security
