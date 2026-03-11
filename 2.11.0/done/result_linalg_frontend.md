
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
- The MAGMA backend for linear algebra operations is now deprecated and will be removed in a future release. Setting `torch.backends.cuda.preferred_linalg_library("magma")` or retrieving a previously-set MAGMA preference will now issue a deprecation warning. cuSOLVER remains the default backend. ([#172823](https://github.com/pytorch/pytorch/pull/172823))

  If you see any errors when using cuSOLVER that did not occur with MAGMA, please file an issue on GitHub. To silence the warning, stop explicitly selecting the MAGMA backend:

  Version 2.10:
  ```python
  # No warning
  torch.backends.cuda.preferred_linalg_library("magma")
  ```

  Version 2.11:
  ```python
  # Issues a deprecation warning — remove this call to use the default cuSOLVER backend
  torch.backends.cuda.preferred_linalg_library("magma")
  ```

- `torch.linalg.svd` no longer dispatches to MAGMA. The MAGMA backend is deprecated and cuSOLVER is now used unconditionally, providing significant speedups (2x–400x depending on matrix size and batch dimensions). ([#172824](https://github.com/pytorch/pytorch/pull/172824))

  Previously, setting `torch.backends.cuda.preferred_linalg_library("magma")` would route SVD through MAGMA. This setting is now ignored for SVD, and cuSOLVER is always used.

  Version 2.10:
  ```python
  torch.backends.cuda.preferred_linalg_library("magma")
  U, S, Vh = torch.linalg.svd(x)  # Uses MAGMA
  ```

  Version 2.11:
  ```python
  # MAGMA preference is ignored; cuSOLVER is always used
  U, S, Vh = torch.linalg.svd(x)  # Uses cuSOLVER
  ```

- `torch.linalg.solve_triangular` and `torch.triangular_solve` no longer dispatch to MAGMA. cuBLAS is now used unconditionally, providing speedups of 2x–24x for most matrix sizes (small matrices may see minor regressions of ~0.6x). ([#174109](https://github.com/pytorch/pytorch/pull/174109))

  Version 2.10:
  ```python
  torch.backends.cuda.preferred_linalg_library("magma")
  torch.linalg.solve_triangular(A, B, upper=False)  # Uses MAGMA
  ```

  Version 2.11:
  ```python
  # MAGMA preference is ignored; cuBLAS is always used
  torch.linalg.solve_triangular(A, B, upper=False)  # Uses cuBLAS
  ```

- `torch.linalg.lstsq` no longer dispatches to MAGMA. cuSOLVER/cuBLAS are now used unconditionally, providing speedups of 1.7x–620x depending on matrix size and batch dimensions. ([#174779](https://github.com/pytorch/pytorch/pull/174779))

  Version 2.10:
  ```python
  torch.backends.cuda.preferred_linalg_library("magma")
  result = torch.linalg.lstsq(A, B)  # Uses MAGMA
  ```

  Version 2.11:
  ```python
  # MAGMA preference is ignored; cuSOLVER/cuBLAS is always used
  result = torch.linalg.lstsq(A, B)  # Uses cuSOLVER/cuBLAS
  ```

### new features
### improvements
### bug fixes
### performance
### docs
### devs
### not user facing
- Fix build warnings and update mcf dependency in xplat ([#170102](https://github.com/pytorch/pytorch/pull/170102))
- Remove outdated CUDA and ROCm skip conditions ([#170868](https://github.com/pytorch/pytorch/pull/170868))
- Sort eigenvalues in eig/eigvals comparison tests ([#171717](https://github.com/pytorch/pytorch/pull/171717))
- Allow for unaligned CPU inputs ([#173395](https://github.com/pytorch/pytorch/pull/173395))
- More test file assert removal ([#174255](https://github.com/pytorch/pytorch/pull/174255))
- Skip test__int4_mm and test_compile_int4_mm on <CDNA2 ([#173358](https://github.com/pytorch/pytorch/pull/173358))
### security
### Untopiced
