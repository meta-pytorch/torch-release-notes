
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
- `split_module` now supports `torch.Size` crossing graph split boundaries by decomposing `size()` calls into per-dimension `sym_size` nodes, and builds submodules lazily for faster inference graph splitting ([#179839](https://github.com/pytorch/pytorch/pull/179839))
- `CapabilityBasedPartitioner` can now opt out of horizontal fusion via `skip_horizontal_fusion=True`, partitioning only through direct data dependencies ([#184904](https://github.com/pytorch/pytorch/pull/184904))
### bug fixes
- Preserve user runtime asserts in FX pass ([#184608](https://github.com/pytorch/pytorch/pull/184608))
### performance
- Skip `GraphModule` reconstruction in `CSEPass` when no common subexpressions were eliminated ([#185479](https://github.com/pytorch/pytorch/pull/185479))
### docs
### devs
- Add fast-path in GraphPickler.reducer_override for primitive types ([#181602](https://github.com/pytorch/pytorch/pull/181602))
### not user facing
- Plumb `ProcessGroup` through `standalone_compile` ([#181964](https://github.com/pytorch/pytorch/pull/181964))
- [pyrefly] Add type annotations to torch/fx/experimental/unification ([#180357](https://github.com/pytorch/pytorch/pull/180357))
- [pyrefly] Add type annotations to remaining torch/fx/experimental files ([#180393](https://github.com/pytorch/pytorch/pull/180393))
- [Oncall][AutoFix] Fix TestFxSplitNodeFinder testMode2/testMode3 expectations ([#180574](https://github.com/pytorch/pytorch/pull/180574))
- Centralize FX graph cacheability validation ([#180795](https://github.com/pytorch/pytorch/pull/180795))
- [fx] Fix split_module to place placeholders before get_attr nodes ([#179519](https://github.com/pytorch/pytorch/pull/179519))
- [fx] Move proxy tensor decomposition state onto mode ([#179460](https://github.com/pytorch/pytorch/pull/179460))
- Cleanup custom op polluting global state for subsequent tests ([#180998](https://github.com/pytorch/pytorch/pull/180998))
- Add hint-disproves fast path to statically_known_true/false ([#181276](https://github.com/pytorch/pytorch/pull/181276))
- [Docathon]: documented coverage_ignored_functions ([#182547](https://github.com/pytorch/pytorch/pull/182547))
- Replace __args__ with typing.get_args() and TensorType.dims ([#183006](https://github.com/pytorch/pytorch/pull/183006))
- [Test] Make test_fx_annotate.py device-agnostic for out-of-tree backends ([#185226](https://github.com/pytorch/pytorch/pull/185226))
- Add type annotations to torch/fx graph and graph_module ([#180994](https://github.com/pytorch/pytorch/pull/180994))
- Fix typos in comments and docstrings ([#181967](https://github.com/pytorch/pytorch/pull/181967))
- Support dynamic shapes in sort lowering and symbolic floor/ceil in FX wrapper ([#182786](https://github.com/pytorch/pytorch/pull/182786))
- Fix indefinite article typos: "a" -> "an" before vowels ([#184216](https://github.com/pytorch/pytorch/pull/184216))
### security
