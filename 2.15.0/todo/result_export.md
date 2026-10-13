
# Release Notes worksheet export

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

## export
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [export][serde] Initialize symbol ranges before constants ([#185025](https://github.com/pytorch/pytorch/pull/185025))
- Fix typos in comments, docstrings, and error messages ([#185830](https://github.com/pytorch/pytorch/pull/185830))
- Fix typos and grammatical errors in comments and docstrings ([#194322](https://github.com/pytorch/pytorch/pull/194322))
- reland support min, max in maybe mark dynamic (#194091) (#194625) ([#194625](https://github.com/pytorch/pytorch/pull/194625))
- Keep fake tensor cache synthesis out of proxy traces ([#185100](https://github.com/pytorch/pytorch/pull/185100))
- [PyTorch] Make `has_triton` accelerator-only by default (#195544) ([#195544](https://github.com/pytorch/pytorch/pull/195544))
- Fix incorrect docstring for register_module_as_pytree_input_node ([#196449](https://github.com/pytorch/pytorch/pull/196449))
- Support tensor torch._assert in export ([#186306](https://github.com/pytorch/pytorch/pull/186306))
- Initialize compile context for non-strict export tracing ([#186495](https://github.com/pytorch/pytorch/pull/186495))
- Make SDPA backend checks safe for unbacked head dims ([#184983](https://github.com/pytorch/pytorch/pull/184983))
- Fix export move_to_device_pass device rewrites ([#185105](https://github.com/pytorch/pytorch/pull/185105))
- Preserve CIA ops in AOT joint export ([#184052](https://github.com/pytorch/pytorch/pull/184052))
### not user facing
- support min, max in maybe mark dynamic ([#194091](https://github.com/pytorch/pytorch/pull/194091))
- [RAWTHROW][3] torch/csrc/utils: fix the serialization codegen ([#194378](https://github.com/pytorch/pytorch/pull/194378))
### security
