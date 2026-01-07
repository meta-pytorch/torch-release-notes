
# Release Notes worksheet jit

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

## jit
### bc breaking
### deprecation
- `torch.jit` is not guaranteed to work in Python 3.14. Deprecation warnings have been added to user-facing `torch.jit` API ([#167669](https://github.com/pytorch/pytorch/pull/167669)).
  `torch.jit` should be replaced with `torch.compile` or `torch.export`.
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
### not user facing
- [torch] DRY a couple of lines in unpickler ([#163447](https://github.com/pytorch/pytorch/pull/163447))
- Better error handling in torch/csrc/jit/ir/* ([#163757](https://github.com/pytorch/pytorch/pull/163757))
- Better error handling in torch/csrc/jit/codegen/* ([#163948](https://github.com/pytorch/pytorch/pull/163948))
- [opaque_obj] Add __eq__ and __deepcopy__ ([#163279](https://github.com/pytorch/pytorch/pull/163279))
- Fix missing brackets ([#165138](https://github.com/pytorch/pytorch/pull/165138))
- Better error handling in torch/csrc/jit/frontend/* ([#165213](https://github.com/pytorch/pytorch/pull/165213))
- Better error handling in torch/csrc/jit/runtime/*  ([#165118](https://github.com/pytorch/pytorch/pull/165118))
- [Fix] Add generator and tensor variant signatures for `rand*_like()` functions ([#167824](https://github.com/pytorch/pytorch/pull/167824))
- [opaque_obj] Remove free registration ([#167739](https://github.com/pytorch/pytorch/pull/167739))
- [opaque_obj] Remove inital opaque obj ([#167740](https://github.com/pytorch/pytorch/pull/167740))
- Fix missing moves in initJITBindings ([#162428](https://github.com/pytorch/pytorch/pull/162428))
- [easy] Don't force copy result of getAllOperatorsFor in init.cpp ([#162218](https://github.com/pytorch/pytorch/pull/162218))
- Fix excess refcounting in ObjLoaderFunc ([#161528](https://github.com/pytorch/pytorch/pull/161528))
- Deprecate Lite Interpreter ([#163289](https://github.com/pytorch/pytorch/pull/163289))
- [opaque obj] Initial OpaqueObject ([#162660](https://github.com/pytorch/pytorch/pull/162660))
- [PyTorch][aarch64] Cast to signed char to fix aarch64 build ([#165021](https://github.com/pytorch/pytorch/pull/165021))
- Save Python refcount bump on each arg in maybe_handle_torch_function ([#164625](https://github.com/pytorch/pytorch/pull/164625))
- [TorchScript] clearer debug for ConcreteModuleType::findSubmoduleConcreteType ([#166192](https://github.com/pytorch/pytorch/pull/166192))
- add support for ir scalar literal parsing for inf/-inf/True/False  ([#163924](https://github.com/pytorch/pytorch/pull/163924))
- [3/N] Add return types of Python functions ([#167287](https://github.com/pytorch/pytorch/pull/167287))
- Fix longstanding race condition around getAllOperatorsFor ([#167860](https://github.com/pytorch/pytorch/pull/167860))
- Fix missing ConstantPooling header in passes.cpp ([#169420](https://github.com/pytorch/pytorch/pull/169420))
- Revert getAllOperatorsFor changes (#167860, #162218) ([#169281](https://github.com/pytorch/pytorch/pull/169281))
### security
