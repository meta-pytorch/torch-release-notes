
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
- Fix require_hint shall use fallback value.  ([#170155](https://github.com/pytorch/pytorch/pull/170155))
- [BE] documenting functions ([#170581](https://github.com/pytorch/pytorch/pull/170581))
- Fix torch.fx.symbolic_trace to_folder with torch.nn.Sequential ([#169279](https://github.com/pytorch/pytorch/pull/169279))
- [fx] Fix Node.type pickling ([#169172](https://github.com/pytorch/pytorch/pull/169172))
- Remove export_for_training ([#171714](https://github.com/pytorch/pytorch/pull/171714))
- [invoke_subgraph] Make the stack trace on invoke_subgraph nodes point to model code ([#170927](https://github.com/pytorch/pytorch/pull/170927))
- [BE][torch.compile][Type Coverage] Strict type coverage in dispatch, partial subclass ([#171808](https://github.com/pytorch/pytorch/pull/171808))
- Fix mark_dynamic hint_override should update stride hint. ([#171961](https://github.com/pytorch/pytorch/pull/171961))
- [precompile][ez] Check attribute existence for graph pickler. ([#172104](https://github.com/pytorch/pytorch/pull/172104))
- [opaque type] support saving for backward ([#171186](https://github.com/pytorch/pytorch/pull/171186))
- [PyTorch] Graph Pickler supports custom ignored metadata field keys ([#172587](https://github.com/pytorch/pytorch/pull/172587))
- [aot_autograd] Add support for tracking and handling opaque objects. ([#171137](https://github.com/pytorch/pytorch/pull/171137))
- Fix trailing whitespace in print_readable with inner graphs ([#172644](https://github.com/pytorch/pytorch/pull/172644))
- [ROCm] Add partitioned buffer approach for scatter add op ([#168073](https://github.com/pytorch/pytorch/pull/168073))
- explicit dynamic shapes maps namings (#172405) ([#173017](https://github.com/pytorch/pytorch/pull/173017))
- [ROCm] assert HIP events in profiler stack trace ([#174366](https://github.com/pytorch/pytorch/pull/174366))
- soft_pending_unbacked_not_found_error flag to bypass PendingUnbackedSymbolNotFound errors ([#174150](https://github.com/pytorch/pytorch/pull/174150))
- [fx] Allow symbolic tracing of HigherOrderOperators that don't take callable args ([#173839](https://github.com/pytorch/pytorch/pull/173839))
- Add a `additional_meta` arg to gm.print_readable() ([#173734](https://github.com/pytorch/pytorch/pull/173734))
- optimize common pattern 1 in symbolic reasoning ([#174615](https://github.com/pytorch/pytorch/pull/174615))
- optimize _smart_symbol_sort to use direct dict lookup instead of size_hint ([#174655](https://github.com/pytorch/pytorch/pull/174655))
- avoid redundant compute_hint calls using _NO_HINT sentinel ([#174664](https://github.com/pytorch/pytorch/pull/174664))
- skip static eval in guard_or_defer_runtime_assert for unbounded unbacked symbol >= 0 pattern. ([#174652](https://github.com/pytorch/pytorch/pull/174652))
- use sympy.Add._from_args(is_commutative=True) in make_optimized  ([#174665](https://github.com/pytorch/pytorch/pull/174665))
- optimize constructing relational expressions when one side is single unbacked symbol and other is constant.  ([#174662](https://github.com/pytorch/pytorch/pull/174662))
### not user facing
- Symbolic Shapes: Ignorable fresh unbacked symbols ([#169547](https://github.com/pytorch/pytorch/pull/169547))
- [xpu][fix] Enlarge dynamo UT timeout for XPU duet to low CPU ferq of XPU CI machine. ([#170292](https://github.com/pytorch/pytorch/pull/170292))
- [Docs] Fix broken links in torch.compile documentation ([#171700](https://github.com/pytorch/pytorch/pull/171700))
- [ROCm] Enabled and validated correct HIP events  ([#171384](https://github.com/pytorch/pytorch/pull/171384))
- remove unbacked size-like oblivious ([#171843](https://github.com/pytorch/pytorch/pull/171843))
- [precompile] Only wrap RegionalOutputCode under config. ([#172054](https://github.com/pytorch/pytorch/pull/172054))
- [precompile] e2e cross precompilation ([#171600](https://github.com/pytorch/pytorch/pull/171600))
- [torchcomms] opaque objects - autograd support ([#172360](https://github.com/pytorch/pytorch/pull/172360))
- [inductor][overlap] fix circular extra deps; handle artifactos of collapsing fused regions  ([#172081](https://github.com/pytorch/pytorch/pull/172081))
- [fx] nested getitem chains in partitioner reassignment ([#172888](https://github.com/pytorch/pytorch/pull/172888))
- Truncate annotation in gm.print_readable() if too long ([#173119](https://github.com/pytorch/pytorch/pull/173119))
- Use an index lookup map for finding the node index in the graph ([#173385](https://github.com/pytorch/pytorch/pull/173385))
- [fx] Add debug_dumps method to GraphPickler for debugging pickle failures ([#173675](https://github.com/pytorch/pytorch/pull/173675))
- [fx] Respect __getstate__ in GraphPickler for GraphModule serialization ([#173810](https://github.com/pytorch/pytorch/pull/173810))
- Truncate annotation in gm.print_readable() if too long ([#173119](https://github.com/pytorch/pytorch/pull/173119))
- [GraphPickler] switch from pickle to dill if available ([#173801](https://github.com/pytorch/pytorch/pull/173801))
- Finish assert in torch/jit and start torch/fx ([#173960](https://github.com/pytorch/pytorch/pull/173960))
- More assert removal in torch/fx ([#173961](https://github.com/pytorch/pytorch/pull/173961))
- More fx assert removal ([#173962](https://github.com/pytorch/pytorch/pull/173962))
- [GraphPickler] switch from pickle to dill if available ([#173801](https://github.com/pytorch/pytorch/pull/173801))
- Finish fx migration ([#173977](https://github.com/pytorch/pytorch/pull/173977))
- Start functorch assert removal ([#173978](https://github.com/pytorch/pytorch/pull/173978))
- [BE] fx_graph_runnable pgs support ([#173932](https://github.com/pytorch/pytorch/pull/173932))
- More test assert removal ([#174257](https://github.com/pytorch/pytorch/pull/174257))
- Finish assert removal of test top level files ([#174258](https://github.com/pytorch/pytorch/pull/174258))
- More test assert removal, only partial test/fx move ([#174259](https://github.com/pytorch/pytorch/pull/174259))
- [Flex] Dont materialize lse grad ([#173481](https://github.com/pytorch/pytorch/pull/173481))
- Fix: add missing compute_unbacked_binding [HF torchbench] ([#174002](https://github.com/pytorch/pytorch/pull/174002))
### security
