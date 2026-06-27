
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
### deprecation
### new features
- Add `const_data_ptr()` Python binding to `torch.Tensor` for read-only data pointer access ([#180382](https://github.com/pytorch/pytorch/pull/180382))
- Add `abbr` property to `torch.dtype` exposing the short string abbreviation of a dtype ([#177296](https://github.com/pytorch/pytorch/pull/177296))
- Allow positional arguments to be passed as keyword arguments to autograd custom `Function`s ([#182206](https://github.com/pytorch/pytorch/pull/182206))
- Expose `rearrange` in the `torch.func` namespace for einops-style tensor reshaping ([#173183](https://github.com/pytorch/pytorch/pull/173183))
### improvements
- Make it possible to load safetensors with `torch.load` ([#170592](https://github.com/pytorch/pytorch/pull/170592))
- Make `Storage.pin_memory` / `Storage.is_pinned` device-agnostic ([#186223](https://github.com/pytorch/pytorch/pull/186223))
### bug fixes
- Add `opt_dtype` validation to `torch.nanmean()` for consistent error handling ([#172809](https://github.com/pytorch/pytorch/pull/172809))
- Route `torch.nansum` integer output dtype through `nan_to_num` + `sum` for correct results ([#183808](https://github.com/pytorch/pytorch/pull/183808))
- Fix out-of-bounds read in `CUDAStream::stream()` ([#184237](https://github.com/pytorch/pytorch/pull/184237))
- Align XPU `logspace`/`linspace` ref tests with upstream XFAIL state ([#178734](https://github.com/pytorch/pytorch/pull/178734))
### performance
### docs
- Fix `out_dtype` signatures for `bmm`, `mm`, `addmm`, `baddbmm` ([#179182](https://github.com/pytorch/pytorch/pull/179182))
- Add CUDA SDPA determinism section to `randomness.rst` ([#182551](https://github.com/pytorch/pytorch/pull/182551))
- Convert stub docs pages to MyST Markdown ([#183498](https://github.com/pytorch/pytorch/pull/183498))
- Expose `nonzero_static` docs ([#185674](https://github.com/pytorch/pytorch/pull/185674))
- Note `expand` materialization costs ([#185400](https://github.com/pytorch/pytorch/pull/185400))
- Fix `torch.trapz` documentation signature to match `torch.trapezoid` ([#180571](https://github.com/pytorch/pytorch/pull/180571))
- Clarify that `torch.normal` does not support integer dtypes ([#180580](https://github.com/pytorch/pytorch/pull/180580))
- Document actual keyword argument names for `tensor_split` ([#182075](https://github.com/pytorch/pytorch/pull/182075))
### devs
### Untopiced
### not user facing
- [Native DSL] Split overrides into (cond, impl) callables ([#181385](https://github.com/pytorch/pytorch/pull/181385))
- [Native DSL] Testing infra via OpInfo ([#180351](https://github.com/pytorch/pytorch/pull/180351))
- [TensorIterator] Expose the build pipeline to Python (kwargs API) ([#184603](https://github.com/pytorch/pytorch/pull/184603))
- Set gradcheck nondeterminism tolerance for index_reduce mean/prod ([#178589](https://github.com/pytorch/pytorch/pull/178589))
- Bump tolerance slightly for test_jvp with float32 on CPU ([#181881](https://github.com/pytorch/pytorch/pull/181881))
### security
