
# Release Notes worksheet fx

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

## fx
### bc breaking
### deprecation
### new features
### improvements
- `torch.fx.symbolic_trace` now supports tracing `HigherOrderOperator`s that do not take callable arguments ([#173839](https://github.com/pytorch/pytorch/pull/173839))
### bug fixes
- Fix `torch.fx.symbolic_trace` `to_folder` with `torch.nn.Sequential` modules ([#169279](https://github.com/pytorch/pytorch/pull/169279))
- Fix `Node.type` pickling in `torch.fx` ([#169172](https://github.com/pytorch/pytorch/pull/169172))
### performance
- Improve node index lookup performance in FX graphs by using an index lookup map ([#173385](https://github.com/pytorch/pytorch/pull/173385))
### docs
- Add documentation for previously undocumented functions ([#170581](https://github.com/pytorch/pytorch/pull/170581))
### devs
- `GraphModule.print_readable()` improvements: new `additional_meta` argument for displaying additional node metadata ([#173734](https://github.com/pytorch/pytorch/pull/173734)), long annotations are now truncated for readability ([#173119](https://github.com/pytorch/pytorch/pull/173119)), and fix trailing whitespace with inner graphs ([#172644](https://github.com/pytorch/pytorch/pull/172644))
- `GraphPickler` improvements: support for custom ignored metadata field keys ([#172587](https://github.com/pytorch/pytorch/pull/172587)), a `debug_dumps` method for debugging pickle failures ([#173675](https://github.com/pytorch/pytorch/pull/173675)), respecting `__getstate__` for `GraphModule` serialization ([#173810](https://github.com/pytorch/pytorch/pull/173810)), and automatic fallback to dill if available ([#173801](https://github.com/pytorch/pytorch/pull/173801))
- Stack traces on `invoke_subgraph` nodes now point to the original model code for easier debugging ([#170927](https://github.com/pytorch/pytorch/pull/170927))
- Add process group support to `fx_graph_runnable` ([#173932](https://github.com/pytorch/pytorch/pull/173932))
- Strict type coverage in dispatch and partial subclass ([#171808](https://github.com/pytorch/pytorch/pull/171808))
### not user facing
### security
### Untopiced
