
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
- MAGMA is deprecated as the backend for pivoted LU factorization on CUDA; `torch.linalg.lu_factor` (and ops built on it) with `pivot=True` now always uses cuSOLVER ([#190661](https://github.com/pytorch/pytorch/pull/190661))

  With `pivot=True`, LU now dispatches to cuSOLVER even when `torch.backends.cuda.preferred_linalg_library("magma")` is set; a new built-in batched LU kernel replaces MAGMA's for large batches. When MAGMA is preferred, the first call warns: `linalg.lu_factor: MAGMA, as a linear algebra backend, is deprecated and will be removed in future releases.` `pivot=False` still uses MAGMA when it is preferred. To avoid the warning, use the default or cuSOLVER backend.

  ```python
  torch.backends.cuda.preferred_linalg_library("magma")
  LU, pivots = torch.linalg.lu_factor(A)  # 2.14: MAGMA; 2.15: cuSOLVER + UserWarning
  torch.backends.cuda.preferred_linalg_library("default")  # recommended
  ```

### new features
### improvements
- Add CUDA TunableOp support for `torch._scaled_mm` ([#186271](https://github.com/pytorch/pytorch/pull/186271))
- Unify matmul shape-check error messages ([#193583](https://github.com/pytorch/pytorch/pull/193583))
### bug fixes
- Fix silently wrong second-order forward AD for `linalg.det`, `slogdet` and `solve` ([#192667](https://github.com/pytorch/pytorch/pull/192667))
- Fix wrong `torch.linalg.matrix_exp` results for some inputs ([#196658](https://github.com/pytorch/pytorch/pull/196658))
- Fix wrong CPU `torch._int_mm` results for strided size-1 dimensions ([#194682](https://github.com/pytorch/pytorch/pull/194682))
### performance
- Add a built-in CUDA batched LU kernel that matches MAGMA, and improve LU backend selection without pivoting ([#190329](https://github.com/pytorch/pytorch/pull/190329), [#193004](https://github.com/pytorch/pytorch/pull/193004))
### docs
### devs
### Untopiced
### not user facing
- Move `grouped_mm` tests to shared device tests and extend their coverage ([#194917](https://github.com/pytorch/pytorch/pull/194917), [#196075](https://github.com/pytorch/pytorch/pull/196075))
- Fix and enable TunableOp, `grouped_mm` and `cholesky_solve` tests on GB200, B200 and ROCm ([#196445](https://github.com/pytorch/pytorch/pull/196445), [#196775](https://github.com/pytorch/pytorch/pull/196775), [#195956](https://github.com/pytorch/pytorch/pull/195956), [#197361](https://github.com/pytorch/pytorch/pull/197361))
- Deduplicate CUDA Kineto setup in tests ([#198209](https://github.com/pytorch/pytorch/pull/198209))
- Remove the no-op test decorator `skipCUDAIfNoMagmaAndNoLinalgsolver` ([#198986](https://github.com/pytorch/pytorch/pull/198986))
- Remove redundant `dtypesIfMPS` test decorators ([#199652](https://github.com/pytorch/pytorch/pull/199652))
- Replace `data_ptr` with `mutable_data_ptr` in quantized kernels ([#182809](https://github.com/pytorch/pytorch/pull/182809))
- Reduce dispatch overhead in `bmm` and `baddbmm` by reusing batch-dimension views ([#198570](https://github.com/pytorch/pytorch/pull/198570)) (cut for length)
- Reduce TunableOp tuning time for expensive GEMMs by sizing the candidate screening runs by the configured tuning limits ([#192403](https://github.com/pytorch/pytorch/pull/192403)) (cut for length)
### security
