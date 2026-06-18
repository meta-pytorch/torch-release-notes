
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
### bug fixes
### performance
### docs
### devs
### Untopiced
- [pyrefly] Add type annotations to torch/fx/experimental/unification ([#180357](https://github.com/pytorch/pytorch/pull/180357))
- [pyrefly] Add type annotations to remaining torch/fx/experimental files ([#180393](https://github.com/pytorch/pytorch/pull/180393))
- [BE] TensorWithFlatten rename to TraceableWrapperSubclass and Improved Typing ([#180359](https://github.com/pytorch/pytorch/pull/180359))
- Handle dict in _iterate_exprs for triton kernel wrapper nodes (#180471) ([#180471](https://github.com/pytorch/pytorch/pull/180471))
- New decorators for expected test failures on windows rtx runners ([#178332](https://github.com/pytorch/pytorch/pull/178332))
- Add differentiable decomposition for max_pool2d/3d_with_indices ([#179104](https://github.com/pytorch/pytorch/pull/179104))
- [fx][split_module]Optimize inference-purposing graph splitting with lazy GraphModule construction ([#179839](https://github.com/pytorch/pytorch/pull/179839))
- Avoid Triton sort compile cliff in create_block_mask ([#182745](https://github.com/pytorch/pytorch/pull/182745))
- prefer duck specialization over 0/1 in unbacked meta fallback for gso (#183342) ([#183342](https://github.com/pytorch/pytorch/pull/183342))
- Fix torch.cat axis handling in Inductor pre-grad fusion ([#183995](https://github.com/pytorch/pytorch/pull/183995))
- [size-hint] Cache _sub_unbacked_exprs (#184915) ([#184915](https://github.com/pytorch/pytorch/pull/184915))
- [torch][fx] Skip GraphModule construction in CSEPass when nothing changed ([#185479](https://github.com/pytorch/pytorch/pull/185479))
- Fix AOT FXIR parallel Triton kernel reload ([#185134](https://github.com/pytorch/pytorch/pull/185134))
- Add option to skip horizontal partition fusion ([#184904](https://github.com/pytorch/pytorch/pull/184904))
- Handle scalar tensor slice bounds in non-strict export ([#184925](https://github.com/pytorch/pytorch/pull/184925))
- reland [fx] Add Graph.materialize_symints + helpers; warn on raw SymInt args (#186665) ([#186665](https://github.com/pytorch/pytorch/pull/186665))
- Fix deferred SymFloat runtime assertions ([#185692](https://github.com/pytorch/pytorch/pull/185692))
### not user facing
- [Oncall][AutoFix] Fix TestFxSplitNodeFinder testMode2/testMode3 expectations ([#180574](https://github.com/pytorch/pytorch/pull/180574))
- Centralize FX graph cacheability validation ([#180795](https://github.com/pytorch/pytorch/pull/180795))
- [dynamo] Fix tensorify recompiles for method-form SymFloat ops ([#179395](https://github.com/pytorch/pytorch/pull/179395))
- [fx] Fix split_module to place placeholders before get_attr nodes ([#179519](https://github.com/pytorch/pytorch/pull/179519))
- [fx] Add fast-path in GraphPickler.reducer_override for primitive types ([#181602](https://github.com/pytorch/pytorch/pull/181602))
- [fx] Move proxy tensor decomposition state onto mode ([#179460](https://github.com/pytorch/pytorch/pull/179460))
- [dynamo] Fix tensorify recompiles for method-form SymFloat ops ([#179395](https://github.com/pytorch/pytorch/pull/179395))
- Cleanup custom op polluting global state for subsequent tests ([#180998](https://github.com/pytorch/pytorch/pull/180998))
- [dynamo] Fix tensorify recompiles for method-form SymFloat ops ([#179395](https://github.com/pytorch/pytorch/pull/179395))
- Add hint-disproves fast path to statically_known_true/false ([#181276](https://github.com/pytorch/pytorch/pull/181276))
- [Docathon]: documented coverage_ignored_functions ([#182547](https://github.com/pytorch/pytorch/pull/182547))
- Replace __args__ with typing.get_args() and TensorType.dims ([#183006](https://github.com/pytorch/pytorch/pull/183006))
- [Inductor] Support dynamic shapes in sort lowering and symbolic floor/ceil in FX wrapper (#182786) ([#182786](https://github.com/pytorch/pytorch/pull/182786))
- [ROCm][CI] Skip tests which consume excessive run time in CI ([#182763](https://github.com/pytorch/pytorch/pull/182763))
- [ShapesSpec] Refactor lookup_spec_from_dynamo_source  ([#184299](https://github.com/pytorch/pytorch/pull/184299))
- [ShapesSpec]  unify variables with same shape var ([#184853](https://github.com/pytorch/pytorch/pull/184853))
- Add @requires_gpu decorator to user_defined_triton_kernel_autotune test ([#185229](https://github.com/pytorch/pytorch/pull/185229))
- Tighten generalized scatter graph target ([#184075](https://github.com/pytorch/pytorch/pull/184075))
- [ShapesSpec] Support derived expressions as leaf specs in shapes_spec and setup path for assumptions ([#185154](https://github.com/pytorch/pytorch/pull/185154))
- [ShapesSpec] Support ShapesSpec.assumptions for cross-input shape invariants ([#185161](https://github.com/pytorch/pytorch/pull/185161))
- [Test] Make test_fx_annotate.py device-agnostic for out-of-tree backends ([#185226](https://github.com/pytorch/pytorch/pull/185226))
### security
