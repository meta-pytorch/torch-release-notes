
# Release Notes worksheet optim

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

## optim
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- Fix `lr_scheduler` unexpectedly calls `step()` when init argument last_epoch is larger than -1 ([#149312](https://github.com/pytorch/pytorch/pull/149312))
### performance
### docs
- Add scripts to generate plots of LRSchedulers ([#149189](https://github.com/pytorch/pytorch/pull/149189))
- Include other accelerators in capturable docstr for optimizers ([#149770](https://github.com/pytorch/pytorch/pull/149770))
- Document that dampening is skipped in SGD momentum first step ([#152833](https://github.com/pytorch/pytorch/pull/152833))
- Fix doc cosineannealinglr 152081 ([#152936](https://github.com/pytorch/pytorch/pull/152936))
### devs
### Untopiced
- Convert Tensor lr to 0-dim as needed for the optimizer to normally work ([#145674](https://github.com/pytorch/pytorch/pull/145674))
- Clean up duplicated code in lr_scheduler ([#150984](https://github.com/pytorch/pytorch/pull/150984))
- Optimize typing in `lr_scheduler.py` ([#151219](https://github.com/pytorch/pytorch/pull/151219))
- Fix CosineAnnealingWarmRestarts reset T_cur ([#151289](https://github.com/pytorch/pytorch/pull/151289))
- Add lr_lambda type check in MultiplicativeLR ([#151973](https://github.com/pytorch/pytorch/pull/151973))
- Update SGD documentation to match implementation ([#149884](https://github.com/pytorch/pytorch/pull/149884))
- Fix incorrect citation of authors in documentation ([#145209](https://github.com/pytorch/pytorch/pull/145209))
- Fix the type hint of `step()` with default value ([#153367](https://github.com/pytorch/pytorch/pull/153367))
- [BE]: Improve decorator typing for Optimizer subclasses ([#153374](https://github.com/pytorch/pytorch/pull/153374))
- Add TensorLR variant for fused Adagrad on CPU ([#153078](https://github.com/pytorch/pytorch/pull/153078))
- Add `load_state_dict` hint doc about invoke order work with lr_scheduler ([#149942](https://github.com/pytorch/pytorch/pull/149942))
### not user facing
### security
