
# Release Notes worksheet sparse_frontend

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

## sparse_frontend
### bc breaking
- `torch.load(..., weights_only=True)` now always validates sparse-tensor invariants ([#184750](https://github.com/pytorch/pytorch/pull/184750))

  Sparse tensors loaded in restricted `weights_only` mode now undergo an O(nnz) validation scan regardless of the global `torch.sparse.check_sparse_tensor_invariants` setting. Valid sparse checkpoints emit a warning explaining the scan. Malformed checkpoints whose indices are inconsistent with the tensor size now raise an error such as `RuntimeError: size is inconsistent with indices` instead of creating an invalid tensor that could later read out of bounds.

  Before, disabling global invariant checks also disabled validation during a restricted load:

  ```python
  with torch.sparse.check_sparse_tensor_invariants(False):
      tensor = torch.load("sparse.pt", weights_only=True)
  ```

  In PyTorch 2.14, fix or regenerate malformed sparse checkpoints and continue using the safe restricted loader:

  ```python
  tensor = torch.load("sparse.pt", weights_only=True)
  ```

  Trusted checkpoints can retain the old no-validation behavior by using `weights_only=False` while global invariant checks are disabled, but this invokes the unrestricted pickle loader and must not be used with untrusted files.
### deprecation
### new features
### improvements
- Add CUDA `float16` and `bfloat16` support to `torch.sparse.sampled_addmm`, including supported sparse-CSR backward paths ([#187681](https://github.com/pytorch/pytorch/pull/187681))
- Add sparse COO dispatch for `torch.linalg.vector_norm`, allowing it to replace deprecated `torch.norm` calls on sparse COO tensors ([#185309](https://github.com/pytorch/pytorch/pull/185309))
### bug fixes
- Create cuSPARSELt handles per device so sparse operations remain valid when a thread switches between CUDA devices ([#189048](https://github.com/pytorch/pytorch/pull/189048))
### performance
### docs
### devs
### not user facing
- Avoid unnecessary tuple-element and vector copies in sparse and other internal kernels ([#191107](https://github.com/pytorch/pytorch/pull/191107))
- Centralize the internal CUDA/ROCm standard-library compatibility alias used by sparse CUDA kernels ([#191491](https://github.com/pytorch/pytorch/pull/191491))
### security
- Reject negative `size` values in the private COO-to-CSR index conversion operator before CPU or CUDA kernels can write out of bounds ([#188540](https://github.com/pytorch/pytorch/pull/188540))
