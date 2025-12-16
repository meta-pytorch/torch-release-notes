
# Release Notes worksheet python_frontend

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

## python_frontend
### bc breaking
- Fix arg parser one pos arg ([#163081](https://github.com/pytorch/pytorch/pull/163081))
### deprecation
### new features
- Add min/max support for barebones uint types ([#166813](https://github.com/pytorch/pytorch/pull/166813))
- Add min/max support for barebones uint types ([#166813](https://github.com/pytorch/pytorch/pull/166813))
### improvements
- [BE] Cleanup stale comments/copy from `gemm`  ([#162001](https://github.com/pytorch/pytorch/pull/162001))
- Add view support for library custom Function ([#164520](https://github.com/pytorch/pytorch/pull/164520))
- Fix #165125: Type "str" is not assignable to return type "None" ([#165128](https://github.com/pytorch/pytorch/pull/165128))
- Add `torch.backends.mkldnn.is_acl_available()` method ([#165678](https://github.com/pytorch/pytorch/pull/165678))
- Rework PyObject preservation ([#166342](https://github.com/pytorch/pytorch/pull/166342))
- Rework PyObject preservation (v2) ([#167564](https://github.com/pytorch/pytorch/pull/167564))
### bug fixes
- PyTorch `histc` fix for values with large magnitudes ([#163506](https://github.com/pytorch/pytorch/pull/163506))
- Fix tensor creation with empty names crash ([#163957](https://github.com/pytorch/pytorch/pull/163957))
- Quick fix of torch.save memory leak ([#165204](https://github.com/pytorch/pytorch/pull/165204))
- added type annotation to _NoParamDecoratorContextManager.__new__ ([#166414](https://github.com/pytorch/pytorch/pull/166414))
- [3.14] Fix torch.package.importer ([#166767](https://github.com/pytorch/pytorch/pull/166767))
- Handle only a Tensor for IntList parsing ([#167606](https://github.com/pytorch/pytorch/pull/167606))
- Fix EmbeddingBag when input is 2D and include_last_offset is True ([#168159](https://github.com/pytorch/pytorch/pull/168159))
### performance
### docs
- Update docs for torch.mode ([#165614](https://github.com/pytorch/pytorch/pull/165614))
- Document limitations of weights_only in SECURITY.md and torch.load doc ([#165645](https://github.com/pytorch/pytorch/pull/165645))
### devs
### Untopiced
- Update docs for quantile to be clearer for nearest ([#162423](https://github.com/pytorch/pytorch/pull/162423))
- fix high=0 bug in nll_loss test ([#162763](https://github.com/pytorch/pytorch/pull/162763))
- Update documentation for torch.index_select ([#163616](https://github.com/pytorch/pytorch/pull/163616))
- Clarrifying input output angle unit in the docs for trigonometric fun… ([#161248](https://github.com/pytorch/pytorch/pull/161248))
- [random] Add `generator` arg to `rand*_like` APIs  ([#166160](https://github.com/pytorch/pytorch/pull/166160))
- [HOP][print] Add HOP subclass for printing ([#166660](https://github.com/pytorch/pytorch/pull/166660))
- [HOP][print]Add make_fx for the proxy with graph module print ([#166920](https://github.com/pytorch/pytorch/pull/166920))
- Updated hypot to accept cpu scalar Tensor even on GPU. ([#169302](https://github.com/pytorch/pytorch/pull/169302))
- [DLPack] Enable cross-device transfers in from_dlpack ([#169572](https://github.com/pytorch/pytorch/pull/169572))
### not user facing
### security
