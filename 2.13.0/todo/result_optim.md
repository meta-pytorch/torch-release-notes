
# Release Notes worksheet optim

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

## optim
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
- docs: use \gamma consistently for lr in Adafactor math blocks ([#184773](https://github.com/pytorch/pytorch/pull/184773))
### devs
- Add optimizer reparameterization helper for non-strict tracing ([#181643](https://github.com/pytorch/pytorch/pull/181643))
### Untopiced
- [xpu][fix] Add xpu to maybe_fallback ([#180451](https://github.com/pytorch/pytorch/pull/180451))
- docs: clarify ReduceLROnPlateau threshold_mode behavior ([#180638](https://github.com/pytorch/pytorch/pull/180638))
- Removed  skipIfTorchDynamo from test_set_default_dtype_works_with_foreach unit test ([#177129](https://github.com/pytorch/pytorch/pull/177129))
- Fix SequentialLR wrong learning rate initialization when milestones contain 0 ([#185986](https://github.com/pytorch/pytorch/pull/185986))
### not user facing
- Refine graph capture check in optimizer ([#180453](https://github.com/pytorch/pytorch/pull/180453))
- docs: make optimizer load_state_dict example generic ([#185401](https://github.com/pytorch/pytorch/pull/185401))
- Fix typos in optimizer, distribution, and utility modules ([#185620](https://github.com/pytorch/pytorch/pull/185620))
### security
