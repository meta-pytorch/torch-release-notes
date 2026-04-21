
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
- Update and correct the documentation for Cond operator ([#175419](https://github.com/pytorch/pytorch/pull/175419))
### devs
### Untopiced
- [torch.fx] Make topo_sort in fuser_utils stable to fix SymInt constraint ordering ([#175378](https://github.com/pytorch/pytorch/pull/175378))
- add aggressive_guard_free_semantics config for faster tracing ([#174654](https://github.com/pytorch/pytorch/pull/174654))
- Fix _build_proxy_for_sym_expr for n-ary sympy.Add by mapping to torch.sym_sum ([#175398](https://github.com/pytorch/pytorch/pull/175398))
- Add per-SymNode expr cache keyed on _replacements_version_counter ([#175353](https://github.com/pytorch/pytorch/pull/175353))
- [reland][fx] Update get_source_partitioner to parse nn_module_stack ([#175788](https://github.com/pytorch/pytorch/pull/175788))
- [fx] Fix edge case ([#175935](https://github.com/pytorch/pytorch/pull/175935))
- [annotate] propagate anotation to runtime asserts ([#170796](https://github.com/pytorch/pytorch/pull/170796))
- [BE] remove more undocumented functions using claude skill ([#175663](https://github.com/pytorch/pytorch/pull/175663))
- [fx] Fix quadratic name generation in _NamespaceBase.create_name ([#176515](https://github.com/pytorch/pytorch/pull/176515))
- Reapply "[fx] Move the rest of torch.fx.Node to C++ (#170946)" (4bc9d7f4ef8)
- Reland [fx] Fix quadratic name generation in create_name ([#177217](https://github.com/pytorch/pytorch/pull/177217))
- Revert "[fx] Move the rest of torch.fx.Node to C++ (#170946)" ([#177183](https://github.com/pytorch/pytorch/pull/177183))
- [mvai][igr] Add _merge_overlapping_fusions() to FxNetSplitter with env var gate (#177099) ([#177099](https://github.com/pytorch/pytorch/pull/177099))
- [Pytorch] Add ignore_raw_node option to GraphPickler ([#176939](https://github.com/pytorch/pytorch/pull/176939))
- Use _make_graph_module in split_module to support lazy recompile ([#177907](https://github.com/pytorch/pytorch/pull/177907))
- reduce threshold for calling symp.factor to 50 ([#177779](https://github.com/pytorch/pytorch/pull/177779))
- [regional_inductor] Fix horizontal fusion bug and add partition tests ([#178421](https://github.com/pytorch/pytorch/pull/178421))
- [GraphPickler] Handle weakref objects during graph serialization (#178190) ([#178190](https://github.com/pytorch/pytorch/pull/178190))
- [opaque obj] Fix make_fx + value types, add pattern matching test ([#178036](https://github.com/pytorch/pytorch/pull/178036))
- [regional_inductor] Add partition merging for regions connected by data dependencies ([#178690](https://github.com/pytorch/pytorch/pull/178690))
- Fix SYMPY_INTERP calling convention for IsNonOverlappingAndDenseIndicator ([#179031](https://github.com/pytorch/pytorch/pull/179031))
- [regional_inductor] Revert to CapabilityBasedPartitioner with per-region partitioning ([#179209](https://github.com/pytorch/pytorch/pull/179209))
- [BE] Refactor proxy tensor to deduplicate, up standard for free thread ([#179199](https://github.com/pytorch/pytorch/pull/179199))
- Add tuple_return option to split_module ([#179007](https://github.com/pytorch/pytorch/pull/179007))
- [pyrefly] Add type annotations to core torch/fx types ([#179590](https://github.com/pytorch/pytorch/pull/179590))
- [opaque_obj] Fix meta["val"] for reconstructed opaque nodes and partitioner classification ([#179660](https://github.com/pytorch/pytorch/pull/179660))
- [pyrefly] Add type annotations to torch/fx operator_schemas and subgr… ([#179761](https://github.com/pytorch/pytorch/pull/179761))
- Add DynamicInt pow operation propagation ([#179868](https://github.com/pytorch/pytorch/pull/179868))
- [pyrefly] Add type annotations to torch/fx/experimental/migrate_gradu… ([#180070](https://github.com/pytorch/pytorch/pull/180070))
### not user facing
- Add timing to GraphPickler.loads method ([#175440](https://github.com/pytorch/pytorch/pull/175440))
- [WIP] Safely handle when decompositions add guards ([#175281](https://github.com/pytorch/pytorch/pull/175281))
- [WIP] Safely handle when decompositions add guards ([#175281](https://github.com/pytorch/pytorch/pull/175281))
- Fix fuse_by_partitions crash when partition has no external outputs ([#175203](https://github.com/pytorch/pytorch/pull/175203))
- [precompile] Fix GraphPickler to support nodes with slice() arguments. ([#175996](https://github.com/pytorch/pytorch/pull/175996))
- [BE] Apply up007 and up045 to torch/fx ([#176308](https://github.com/pytorch/pytorch/pull/176308))
- [BE][pytree] improve consistency between variable name and typing annotation (typing change only) ([#176291](https://github.com/pytorch/pytorch/pull/176291))
- Fix set_stack_trace ([#177332](https://github.com/pytorch/pytorch/pull/177332))
- Preserve scalar item() semantics for size-1 tensors ([#177270](https://github.com/pytorch/pytorch/pull/177270))
- Handle div by 0 in optimization hint when fallback is 0 (#177709) ([#177709](https://github.com/pytorch/pytorch/pull/177709))
- [opaque] Fix tangent/primal proxy collision for opaque inner attrs ([#178113](https://github.com/pytorch/pytorch/pull/178113))
- Fix wrong bool to int conversion ([#177178](https://github.com/pytorch/pytorch/pull/177178))
- Tag backward nodes via _patch_autograd_grad and update remat pass ([#179105](https://github.com/pytorch/pytorch/pull/179105))
- [FakeTensor]: Support fast_bind used in normalize_function ([#175740](https://github.com/pytorch/pytorch/pull/175740))
- Move autograd_backward out of FX custom metadata ([#180251](https://github.com/pytorch/pytorch/pull/180251))
- Windows specific test fixes ([#176024](https://github.com/pytorch/pytorch/pull/176024))
- Move autograd_backward out of FX custom metadata ([#180251](https://github.com/pytorch/pytorch/pull/180251))
### security
