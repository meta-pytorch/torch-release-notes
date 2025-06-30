
# Release Notes worksheet sparse_frontend

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

## sparse_frontend
### bc breaking
- API change for new enum in cusparseltsplitkmode-t for cusparseLT 0.7.0+ ([#150536](https://github.com/pytorch/pytorch/pull/150536))
### deprecation
### new features
### improvements
### bug fixes
### performance
- User-controlled sparse tensor validation when loading data from external storage ([#154610](https://github.com/pytorch/pytorch/pull/154610))
### docs
- [Docs] Reformat sparse example ([#154785](https://github.com/pytorch/pytorch/pull/154785))
### devs
### Untopiced
- Fix spelling ([#149277](https://github.com/pytorch/pytorch/pull/149277))
- Fix missing braces for clang CUDA ([#150736](https://github.com/pytorch/pytorch/pull/150736))
- Fix `-Wmissing-braces` in a few files ([#150802](https://github.com/pytorch/pytorch/pull/150802))
- [PrivateUse1] Allow out-of-tree devices to pass check when validating csr tensor args ([#149374](https://github.com/pytorch/pytorch/pull/149374))
- [ROCm] improve sparse addmm, enable complex ([#153262](https://github.com/pytorch/pytorch/pull/153262))
- Fix signature of torch.sparse_coo_tensor() ([#152681](https://github.com/pytorch/pytorch/pull/152681))
- ROCm Sparsity through HipSparseLT ([#150578](https://github.com/pytorch/pytorch/pull/150578))
- [BE] Delete pre-CUDA-10.1 code from SparseCUDABlas ([#155079](https://github.com/pytorch/pytorch/pull/155079))
### not user facing
- Fix sparse CUTLASS-based kernels ([#150023](https://github.com/pytorch/pytorch/pull/150023))
- Add optional check_pinning argument to _validate_sparse_compressed_tensor/coo_args ([#154759](https://github.com/pytorch/pytorch/pull/154759))
- [BE] Delete IS_SPMM_AVAILABLE() logic ([#155296](https://github.com/pytorch/pytorch/pull/155296))
### security
