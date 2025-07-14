
# Release Notes worksheet linalg_frontend

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

## linalg_frontend
### bc breaking
**An error is now properly thrown for the out variant of `tensordot` when called with a
`requires_grad=True` tensor. Please avoid passing an out tensor with `requires_grad=True` as
gradients cannot be computed for this tensor.**

In 2.7.0
```
a = torch.empty((4, 2), requires_grad=True)
b = torch.empty((2, 4), requires_grad=True)
c = torch.empty((2, 2), requires_grad=True)
# does not error, but gradients for c cannot be computed
torch.tensordot(a, b, dims=([1], [0]), out=c)
```

In 2.8.0
```
a = torch.empty((4, 2), requires_grad=True)
b = torch.empty((2, 4), requires_grad=True)
c = torch.empty((2, 2), requires_grad=True)
torch.tensordot(a, b, dims=([1], [0]), out=c)
# RuntimeError: tensordot(): the 'out' tensor was specified and requires gradients, and
# its shape does not match the expected result. Either remove the 'out' argument, ensure
# it does not require gradients, or make sure its shape matches the expected output.
```
### deprecation
### new features
### improvements
- Support submatrices in offline tuning for ROCm ([#151138](https://github.com/pytorch/pytorch/pull/151138))
- Add tensor overlap check for `cross` ([#154999](https://github.com/pytorch/pytorch/pull/154999))
### bug fixes
- Fix to workaround LAPACK workspace size being returned as a floating point value ([#149682](https://github.com/pytorch/pytorch/pull/149682))
- Fix the accumulation type for `dot` and `gemv` ([#152676](https://github.com/pytorch/pytorch/pull/152676))
- Fix `torch.lobpcg` to compute same largest eigenvalue as scipy and `np.linalg.eig` ([#152789](https://github.com/pytorch/pytorch/pull/152789))
- Fix `tau` value check for `torch.ormqr` ([#150759](https://github.com/pytorch/pytorch/pull/150759))
- Fix 32-bit indexing overflows in `ReducedPrecisionGemV` ([#150949](https://github.com/pytorch/pytorch/pull/150949))
### performance
- Fast path for `torch.dot` with float16/bfloat16 ([#152799](https://github.com/pytorch/pytorch/pull/152799))
### docs
- Address ambiguity in docs for `torch.linalg.norm()`'s ord argument of +2 & -2 ([#155148](https://github.com/pytorch/pytorch/pull/155148))
### devs
### Untopiced
### not user facing
- ReducedPrecisionFloatGemvFastPathKernel: Correctly type parallel_for lambda arguments as int64_t ([#152233](https://github.com/pytorch/pytorch/pull/152233))
- irangeify ReducedPrecisionFloatGemvKernel.cpp ([#152232](https://github.com/pytorch/pytorch/pull/152232))
- [2/N] Use internal linkage in aten C++ files ([#151070](https://github.com/pytorch/pytorch/pull/151070))
- do not run `test_ck_blas_library` on cpu ([#148316](https://github.com/pytorch/pytorch/pull/148316))
- [ROCm][TunableOp] More TF32 support. ([#149088](https://github.com/pytorch/pytorch/pull/149088))
- [ROCm][TunableOp] Unit test for TunableOp BLAS logging. ([#148982](https://github.com/pytorch/pytorch/pull/148982))
- [ROCm][TunableOp] Fix offline tuning for ScaledGEMM. ([#149677](https://github.com/pytorch/pytorch/pull/149677))
- [ROCm][TunableOp] TunableOp Context Manager for unit tests ([#149930](https://github.com/pytorch/pytorch/pull/149930))
- [ROCm][TunableOp] Stricter unit tests for online and offline tuning ([#150142](https://github.com/pytorch/pytorch/pull/150142))
- [ROCm][TunableOp] Fix UT race condition and reduce UT duration. ([#150463](https://github.com/pytorch/pytorch/pull/150463))
- Remove guard_size_oblivious from vector_norm decomposition. ([#148809](https://github.com/pytorch/pytorch/pull/148809))
- Fix setUpClass() / tearDownClass() for device-specific tests ([#151129](https://github.com/pytorch/pytorch/pull/151129))
- Fix typos in multiple files ([#152254](https://github.com/pytorch/pytorch/pull/152254))
- ROCm: Enable tf32 testing on test_nn ([#148945](https://github.com/pytorch/pytorch/pull/148945))
- [ROCm][TunableOp] Fix ScaledGEMM rowwise ([#152403](https://github.com/pytorch/pytorch/pull/152403))
- [ROCm][TunableOp] Unit test to verify that there is only one kernel launch per PyTorch API invocation. ([#155077](https://github.com/pytorch/pytorch/pull/155077))
- [ez] Mark linalg svd memory allocation test as serial b/c OOMing on cu128 ([#155811](https://github.com/pytorch/pytorch/pull/155811))
- [ROCm][CI] fix mi300 test failure after 6.4.1 update ([#156368](https://github.com/pytorch/pytorch/pull/156368))
### security
