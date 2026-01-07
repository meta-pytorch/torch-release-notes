
# Release Notes worksheet autograd_frontend

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

## autograd_frontend
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- Fix custom autograd Function memory leak when saving mutated view ([#164407](https://github.com/pytorch/pytorch/pull/164407))
- Fix unused gradient tracking to respect create_graph ([#168295](https://github.com/pytorch/pytorch/pull/168295))
- Fix NaN gradients in atan2_backward when both inputs are zero ([#166787](https://github.com/pytorch/pytorch/pull/166787))
- Bugfix to forward autodiff causing different datatype 2 ([#165784](https://github.com/pytorch/pytorch/pull/165784))
### performance
### docs
- Add `inference_mode` hint message to use `eval` with inference. ([#163619](https://github.com/pytorch/pytorch/pull/163619))
### devs
### Untopiced
### not user facing
- [scan][autograd] clone outputs that's aliasing with inputs or outputs in bw ([#161808](https://github.com/pytorch/pytorch/pull/161808))
- [Autograd] Add Default Autograd Fallback for PrivateUse1 in PyTorch ([#165315](https://github.com/pytorch/pytorch/pull/165315))
- Fix Tril Triu SymInt ([#166627](https://github.com/pytorch/pytorch/pull/166627))
- Fix Tensor use_count check in VariableType.cpp ([#168060](https://github.com/pytorch/pytorch/pull/168060))
- [reland] Allow setting grad_dtype on leaf tensors ([#164751](https://github.com/pytorch/pytorch/pull/164751))
- More ruff SIM fixes ([#164695](https://github.com/pytorch/pytorch/pull/164695))
- [9/N] Apply ruff UP035 rule ([#165515](https://github.com/pytorch/pytorch/pull/165515))
- Expand type checking to mypy strict files ([#165697](https://github.com/pytorch/pytorch/pull/165697))
- Fix pyrefly ignore syntax in  /tools/... ([#166240](https://github.com/pytorch/pytorch/pull/166240))
- Add API to annotate disjoint backward and handle in AC ([#166536](https://github.com/pytorch/pytorch/pull/166536))
### security
