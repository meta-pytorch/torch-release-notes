
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
- Added node metadata annotation API
    - Disable preservation of node metadata when enable=False ([#164772](https://github.com/pytorch/pytorch/pull/164772))
    - Annotation should be mapped across submod ([#165202](https://github.com/pytorch/pytorch/pull/165202))
    - Annotate bw nodes before eliminate dead code ([#165782](https://github.com/pytorch/pytorch/pull/165782))
    - Add logging for debugging annotation ([#165797](https://github.com/pytorch/pytorch/pull/165797))
    - Override metadata on regenerated node in functional mode ([#166200](https://github.com/pytorch/pytorch/pull/166200))
    - Skip copying custom meta for gradient accumulation nodes; tag with is_gradient_acc=True ([#167572](https://github.com/pytorch/pytorch/pull/167572))
    - Add metadata hook for all nodes created in runtime_assert pass ([#169497](https://github.com/pytorch/pytorch/pull/169497))
    - Update gm.print_readable to include Annotation ([#165397](https://github.com/pytorch/pytorch/pull/165397))
    - Add annotation to assertion nodes in export  ([#167171](https://github.com/pytorch/pytorch/pull/167171))
- Add debug mode to print meta in fx graphs ([#165874](https://github.com/pytorch/pytorch/pull/165874))
### improvements
- Add tensor subclass printing support in fx/graph.py ([#164403](https://github.com/pytorch/pytorch/pull/164403))
- Update Node.is_impure check if subgraph contains impure ops ([#166609](https://github.com/pytorch/pytorch/pull/166609), [#167443](https://github.com/pytorch/pytorch/pull/167443))
- Explicitly remove call_mod_node_to_replace after inlining the submodule in const_fold._inline_module` ([#166871](https://github.com/pytorch/pytorch/pull/166871))
- Add strict argument validation to Interpreter.boxed_run ([#166784](https://github.com/pytorch/pytorch/pull/166784))
- Use stable topological sort in fuse_by_partitions ([#167397](https://github.com/pytorch/pytorch/pull/167397))
### bug fixes
- Fix splitter for empty subgraph case ([#161716](https://github.com/pytorch/pytorch/pull/161716))
- Use tuples to have a deterministic ordering in shape prop. ([#164851](https://github.com/pytorch/pytorch/pull/164851))
### performance
- Move Node._prepend/Node._remove_from_list to C++ ([#165882](https://github.com/pytorch/pytorch/pull/165882))
- Optimize torch.fx.Node.replace_all_uses_with ([#165889](https://github.com/pytorch/pytorch/pull/165889))
### docs
- Add docs for torch.fx.experimental.unification ([#167334](https://github.com/pytorch/pytorch/pull/167334))
- Fix the split_module tutorial code ([#166154](https://github.com/pytorch/pytorch/pull/166154))
### devs
- Refactor proxy_tensor ([#165266](https://github.com/pytorch/pytorch/pull/165266))
- Fix invalid symbol definition emitted in fx_graph_runnable.py ([#166529](https://github.com/pytorch/pytorch/pull/166529))
- Add debug-level logging to Interpreter.run_node (#117351) ([#166622](https://github.com/pytorch/pytorch/pull/166622))
- Fix an unsafe indexing in fx exception handling ([#169140](https://github.com/pytorch/pytorch/pull/169140))
- Type annotations for torch/_higher_order_ops/flat_apply.py ([#168933](https://github.com/pytorch/pytorch/pull/168933))
- Add recompute tags (from AC) into GraphModule.print_readable() by default ([#167735](https://github.com/pytorch/pytorch/pull/167735))
- Apply ruff UP035 rule  ([#165214](https://github.com/pytorch/pytorch/pull/165214), [#163744](https://github.com/pytorch/pytorch/pull/163744))
- Add model code stack trace to cuda.memory._snapshot ([#166676](https://github.com/pytorch/pytorch/pull/166676))
- Add model code stack trace to torch.profile ([#167110](https://github.com/pytorch/pytorch/pull/167110))
- Move enrich_profiler_metadata config import out of gm.recompile() ([#167114](https://github.com/pytorch/pytorch/pull/167114))
### Untopiced
### not user facing
- remove allow-untyped-defs from ./torch/fx/experimental/unification/multipledispatch/core.py ([#163478](https://github.com/pytorch/pytorch/pull/163478))
- Use codegen for the boxed interpreters ([#164573](https://github.com/pytorch/pytorch/pull/164573))
- Remove deadcodes about Python3.9 [4/N] ([#163643](https://github.com/pytorch/pytorch/pull/163643), [#163728](https://github.com/pytorch/pytorch/pull/163728))
- Fix assert detection for 3.14 ([#167700](https://github.com/pytorch/pytorch/pull/167700))
### security
