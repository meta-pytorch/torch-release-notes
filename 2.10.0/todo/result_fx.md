
# Release Notes worksheet fx

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

## fx
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
- torch.cond supports autograd now ([#165908](https://github.com/pytorch/pytorch/pull/165908))
- [BE] adding documentation ([#167334](https://github.com/pytorch/pytorch/pull/167334))
### devs
### Untopiced
- [Lowering] Fix the edge case of empty subgraph split due to dataclass node ([#161716](https://github.com/pytorch/pytorch/pull/161716))
- paths to exclude shape guards ([#162684](https://github.com/pytorch/pytorch/pull/162684))
- repro 161902 ([#162416](https://github.com/pytorch/pytorch/pull/162416))
- Fix rebind_unbacked in torch.fx.experimental.symbolic_shapes ([#162788](https://github.com/pytorch/pytorch/pull/162788))
- [AOTI-FX] Solve for undefined symbols in dynamic input shapes ([#163044](https://github.com/pytorch/pytorch/pull/163044))
- Improve fake tensor leakage detection in export by not relying on gc too much ([#163516](https://github.com/pytorch/pytorch/pull/163516))
- [Inductor-FX] Support symbol and dynamic scalar graph inputs and outputs ([#163596](https://github.com/pytorch/pytorch/pull/163596))
- Reapply "Make functionalization `ViewMeta` serializable with pickle. (#143712)"  ([#163769](https://github.com/pytorch/pytorch/pull/163769))
- [WIP][precompile] Set fake_mode of base tensor in fx graph pickler ([#163738](https://github.com/pytorch/pytorch/pull/163738))
- Adjust ...mark_unbacked() -> ...decorators.mark_unbacked() in logs. ([#164131](https://github.com/pytorch/pytorch/pull/164131))
- [Inductor-FX] Support unbacked symbol definitions ([#163729](https://github.com/pytorch/pytorch/pull/163729))
- [Inductor-FX] Generalize FloorDiv conversion to handle more complex launch grids. Remove python_slow grid mode. ([#163828](https://github.com/pytorch/pytorch/pull/163828))
- add tensor subclass printing support in fx/graph.py ([#164403](https://github.com/pytorch/pytorch/pull/164403))
- [fx][traceback] Actually disable preservation of node metadata when enable=False ([#164772](https://github.com/pytorch/pytorch/pull/164772))
- do not suggest torch._check_is_size() ([#164664](https://github.com/pytorch/pytorch/pull/164664))
- remove size-like based size-oblivious special max simplifications ([#164665](https://github.com/pytorch/pytorch/pull/164665))
- Use tuples to have a deterministic ordering. ([#164851](https://github.com/pytorch/pytorch/pull/164851))
- [annotate] Annotation should be mapped across submod ([#165202](https://github.com/pytorch/pytorch/pull/165202))
- [8/N] Apply ruff UP035 rule  ([#165214](https://github.com/pytorch/pytorch/pull/165214))
- [Bugfix][Precompile][vLLM] Support for pickling einops for aot_autograd serialization in vLLM ([#165359](https://github.com/pytorch/pytorch/pull/165359))
- minor proxy_tensor reorg ([#165266](https://github.com/pytorch/pytorch/pull/165266))
- [annotate] Annotate bw nodes before eliminate dead code ([#165782](https://github.com/pytorch/pytorch/pull/165782))
- [annotation] add logging for debugging annotation ([#165797](https://github.com/pytorch/pytorch/pull/165797))
- [reland][fx] Move Node._prepend/Node._remove_from_list to C++ ([#165882](https://github.com/pytorch/pytorch/pull/165882))
- Enable new tracer by default ([#165332](https://github.com/pytorch/pytorch/pull/165332))
- [FX][ez] fix the split_module tutorial code ([#166154](https://github.com/pytorch/pytorch/pull/166154))
- [fx] Optimize torch.fx.Node.replace_all_uses_with ([#165889](https://github.com/pytorch/pytorch/pull/165889))
- [rfc] add debug mode to print meta in fx graphs ([#165874](https://github.com/pytorch/pytorch/pull/165874))
- Support regional inductor with custom config ([#166269](https://github.com/pytorch/pytorch/pull/166269))
- [Inductor-FX] Don't flatten constant args ([#166144](https://github.com/pytorch/pytorch/pull/166144))
- [annotation] Override metadata on regenerated node in functional mode ([#166200](https://github.com/pytorch/pytorch/pull/166200))
- add new line in log ([#164240](https://github.com/pytorch/pytorch/pull/164240))
- Fix syntax for pyrefly errors ([#166496](https://github.com/pytorch/pytorch/pull/166496))
- [devx] Fix invalid symbol definition emitted in fx_graph_runnable.py ([#166529](https://github.com/pytorch/pytorch/pull/166529))
- make FXConverter.generate use V.fake_mode instead of _detect_fake_mode_from_gm ([#166591](https://github.com/pytorch/pytorch/pull/166591))
- update Node.is_impure check if subgraph contains impure ops ([#166609](https://github.com/pytorch/pytorch/pull/166609))
- [opaque_obj_v2] make_fx support ([#165005](https://github.com/pytorch/pytorch/pull/165005))
- explicitly remove call_mod_node_to_replace after inlining the submodule in const_fold._inline_module` ([#166871](https://github.com/pytorch/pytorch/pull/166871))
- Add model code stack trace to cuda.memory._snapshot ([#166676](https://github.com/pytorch/pytorch/pull/166676))
- [fx] Add strict argument validation to Interpreter.boxed_run ([#166784](https://github.com/pytorch/pytorch/pull/166784))
- Reland "Add model code stack trace to torch.profile (#166677)" ([#167110](https://github.com/pytorch/pytorch/pull/167110))
- torch.fx: add debug-level logging to Interpreter.run_node (#117351) ([#166622](https://github.com/pytorch/pytorch/pull/166622))
- [4/N] Use key in dict for existence checks ([#167285](https://github.com/pytorch/pytorch/pull/167285))
- move subgraph_has_impure_ops from `node.is_impure`  into const_fold to unblock production ([#167443](https://github.com/pytorch/pytorch/pull/167443))
- [annotation] Skip copying custom meta for gradient accumulation nodes; tag with is_gradient_acc=True ([#167572](https://github.com/pytorch/pytorch/pull/167572))
- ProxyTorchDispatchMode: Decomposing missing sympy.SymExpr should handle constant literals ([#167585](https://github.com/pytorch/pytorch/pull/167585))
- [opqaue obj] Add attribute support ([#167230](https://github.com/pytorch/pytorch/pull/167230))
- Always track _local_scalar_dense output in tensorify_python_scalars.  ([#166573](https://github.com/pytorch/pytorch/pull/166573))
- Support SymInt placeholder in wrapper fxir ([#167757](https://github.com/pytorch/pytorch/pull/167757))
- Fix an unsafe indexing in fx exception handling ([#169140](https://github.com/pytorch/pytorch/pull/169140))
- add back legalize_graph for BC reason ([#169541](https://github.com/pytorch/pytorch/pull/169541))
- Type annotations for torch/_higher_order_ops/flat_apply.py ([#168933](https://github.com/pytorch/pytorch/pull/168933))
- [annotation][export] Add metadata hook for all nodes created in runtime_assert pass ([#169497](https://github.com/pytorch/pytorch/pull/169497))
- add recompute tags (from AC) into GraphModule.print_readable() by default ([#167735](https://github.com/pytorch/pytorch/pull/167735))
### not user facing
- Fix flaky AOTFxirTestCase ([#162472](https://github.com/pytorch/pytorch/pull/162472))
- Do not use // but use CleanDiv or FloorDiv instead ([#162869](https://github.com/pytorch/pytorch/pull/162869))
- add support for hint_override in mark_unbacked ([#162652](https://github.com/pytorch/pytorch/pull/162652))
- [Inductor-FX] Support torch.cond ([#163234](https://github.com/pytorch/pytorch/pull/163234))
- [Code Clean] Remove deadcodes about Python3.9 [4/N] ([#163643](https://github.com/pytorch/pytorch/pull/163643))
- [Code Clean] Remove deadcodes about Python3.9 [8/N] ([#163728](https://github.com/pytorch/pytorch/pull/163728))
- remove allow-untyped-defs from ./torch/fx/experimental/unification/multipledispatch/core.py ([#163478](https://github.com/pytorch/pytorch/pull/163478))
- Update ruff to 0.13.1 ([#163744](https://github.com/pytorch/pytorch/pull/163744))
- Update ruff to 0.13.1 ([#163744](https://github.com/pytorch/pytorch/pull/163744))
- [3.14] make unbacked_sym[int/float]_counter integers ([#163920](https://github.com/pytorch/pytorch/pull/163920))
- Use codegen for the boxed interpreters ([#164573](https://github.com/pytorch/pytorch/pull/164573))
- [ez] fix typo ([#165282](https://github.com/pytorch/pytorch/pull/165282))
- Teach ProxyTorchDispatchMode how to decompose sympy.Expr into known inputs ([#164717](https://github.com/pytorch/pytorch/pull/164717))
- Update gm.print_readable to include Annotation ([#165397](https://github.com/pytorch/pytorch/pull/165397))
- Implement an AOT precompile mode for standalone_compile ([#165843](https://github.com/pytorch/pytorch/pull/165843))
- Add GraphModule.recompile_submodules, use for regional inductor ([#166002](https://github.com/pytorch/pytorch/pull/166002))
- [dynamo, 3.14] fix misc. bugs to get most dynamo unittests passing locally in 3.14 ([#164631](https://github.com/pytorch/pytorch/pull/164631))
- Update gm.print_readable to include Annotation ([#165397](https://github.com/pytorch/pytorch/pull/165397))
- [symbolic shapes] remove maybe_guard_rel warning ([#166553](https://github.com/pytorch/pytorch/pull/166553))
- [xpu][test] Enable test_fxir_backend tests for XPU ([#166493](https://github.com/pytorch/pytorch/pull/166493))
- [annotate][export] Add annotation to assertion nodes in export  ([#167171](https://github.com/pytorch/pytorch/pull/167171))
- Move enrich_profiler_metadata config import out of gm.recompile() ([#167114](https://github.com/pytorch/pytorch/pull/167114))
- Move enrich_profiler_metadata config import out of gm.recompile() ([#167114](https://github.com/pytorch/pytorch/pull/167114))
- [Inductor-FX] Allocate tensors on device type instead of indexed device ([#167358](https://github.com/pytorch/pytorch/pull/167358))
- Use stable topological sort in fuse_by_partitions ([#167397](https://github.com/pytorch/pytorch/pull/167397))
- remove allocation of new unbacked symbols during mod eval ([#167123](https://github.com/pytorch/pytorch/pull/167123))
- [fx, 3.14] fix assert detection for 3.14 ([#167700](https://github.com/pytorch/pytorch/pull/167700))
- [inductor_on_demand] Refactor - scoop regions and then compile regions ([#169457](https://github.com/pytorch/pytorch/pull/169457))
- Use stable topological sort in fuse_by_partitions ([#167397](https://github.com/pytorch/pytorch/pull/167397))
- Add regional inductor activation refcount and Boxed backend tests ([#169103](https://github.com/pytorch/pytorch/pull/169103))
- fix PythonMod bound_sympy ([#169612](https://github.com/pytorch/pytorch/pull/169612))
### security
