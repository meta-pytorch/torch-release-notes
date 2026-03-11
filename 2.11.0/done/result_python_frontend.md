
# Release Notes worksheet python_frontend

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

## python_frontend
### bc breaking
- `torch.hub.list()`, `torch.hub.load()`, and `torch.hub.get_dir()` now default the `trust_repo` parameter to `"check"` instead of `None`. The `trust_repo=None` option has been removed. ([#174101](https://github.com/pytorch/pytorch/pull/174101))

  Previously, passing `trust_repo=None` (or relying on the default) would silently download and run code from untrusted repositories with only a warning. Now, the default `"check"` behavior will prompt the user for explicit confirmation before running code from repositories not on the trusted list.

  Users who were explicitly passing `trust_repo=None` must update their code. Users who were already passing `trust_repo=True`, `trust_repo=False`, or `trust_repo="check"` are not affected.

  Version 2.10:
  ```python
  # Default trust_repo=None — downloads with a warning
  torch.hub.load("user/repo", "model")
  # Explicit None — same behavior
  torch.hub.load("user/repo", "model", trust_repo=None)
  ```

  Version 2.11:
  ```python
  # Default trust_repo="check" — prompts for confirmation if repo is not trusted
  torch.hub.load("user/repo", "model")
  # To skip the prompt, explicitly trust the repo
  torch.hub.load("user/repo", "model", trust_repo=True)
  ```

### deprecation
### new features
- Added `native_handle` property to `torch.Stream`, providing a unified way to retrieve the backend-specific opaque stream handle (e.g., `cudaStream_t` for CUDA, `sycl::queue*` for XPU). This is useful for passing stream handles to third-party libraries such as Triton. ([#171040](https://github.com/pytorch/pytorch/pull/171040))

  ```python
  stream = torch.accelerator.current_stream()
  handle = stream.native_handle  # backend-specific stream handle
  ```

### improvements
- `torch.load` now produces clearer error messages when encountering miniz errors from `PyTorchStreamReader`, explicitly indicating that the checkpoint file is likely corrupt ([#170244](https://github.com/pytorch/pytorch/pull/170244))
- `torch.load(map_location='meta')` no longer reads storage data from the filesystem, improving performance when loading checkpoints onto the meta device ([#170619](https://github.com/pytorch/pytorch/pull/170619))
### bug fixes
- Fixed a bug where `torch.load` with `FakeTensorMode` or `skip_data` context would compute incorrect storage sizes ([#170618](https://github.com/pytorch/pytorch/pull/170618))
- Fixed PrivateUse1 backend aliasing during deserialization so custom backends are correctly recognized when loading checkpoints ([#165456](https://github.com/pytorch/pytorch/pull/165456))
- Fixed `torch.ops.aten.index.Tensor` to properly raise an `IndexError` when called with an empty indices list, instead of producing undefined behavior ([#174009](https://github.com/pytorch/pytorch/pull/174009))
### performance
- Added `__slots__` to pytree `TreeSpec` dataclasses, reducing memory usage and improving attribute access speed ([#172172](https://github.com/pytorch/pytorch/pull/172172))
### docs
- Clarified `torch.unique` behavior when using the `dim` parameter ([#171608](https://github.com/pytorch/pytorch/pull/171608))
- Clarified `torch.as_tensor` signature to document that `dtype` and `device` are keyword-only arguments ([#173073](https://github.com/pytorch/pytorch/pull/173073))
- Fixed `torch.tensordot` documentation ([#173893](https://github.com/pytorch/pytorch/pull/173893))
- Added dedicated docstring for `torch.Tensor.permute` to clarify it accepts variadic arguments unlike `torch.permute` ([#170689](https://github.com/pytorch/pytorch/pull/170689))
### devs
### not user facing
- Update scaled_mm opinfo to generate appropriately scaled sample inputs ([#168273](https://github.com/pytorch/pytorch/pull/168273))
- Add CUDA version check for blockwise scaling in sample_inputs_scaled_mm_v2 ([#172228](https://github.com/pytorch/pytorch/pull/172228))
- Prepare CUDA inputs only on CUDA device ([#171993](https://github.com/pytorch/pytorch/pull/171993))
- Skip test_compare_cpu for _scaled_mm_v2 (CUDA-only operator) ([#170918](https://github.com/pytorch/pytorch/pull/170918))
- Adjust cdist tolerances for MPS ([#173326](https://github.com/pytorch/pytorch/pull/173326))
- Expose CPUInfo properties ([#173433](https://github.com/pytorch/pytorch/pull/173433))
- Delete skips for block_diags on MPS ([#174158](https://github.com/pytorch/pytorch/pull/174158))
- Remove stale Ventura skips ([#174410](https://github.com/pytorch/pytorch/pull/174410))
- Enable rsqrt tests for XPU ([#174471](https://github.com/pytorch/pytorch/pull/174471))
- Adjust error_inputs conv tests for MPS ([#174776](https://github.com/pytorch/pytorch/pull/174776))
- Add typing utils to copy signatures from methods or signatures ([#163418](https://github.com/pytorch/pytorch/pull/163418))
### security
- Fixed a ZipSlip directory traversal vulnerability in `torch.hub` that could allow malicious zip files to extract files outside the target directory. `torch.hub` now validates all extracted paths and raises a `ValueError` if an archive attempts to write outside the expected folder. ([#171754](https://github.com/pytorch/pytorch/pull/171754))
### Untopiced
