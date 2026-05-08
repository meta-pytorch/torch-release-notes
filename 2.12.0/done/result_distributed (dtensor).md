
# Release Notes worksheet distributed (dtensor)

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

## distributed (dtensor)
### bc breaking
### deprecation
### new features
- Add support for twice-differentiable DTensor redistribution ([#160509](https://github.com/pytorch/pytorch/pull/160509))
- DeviceMesh is now traceable by torch.compile. Make DeviceMesh opaque ([#176661](https://github.com/pytorch/pytorch/pull/176661)), Make placements opaque ([#171482](https://github.com/pytorch/pytorch/pull/171482)).
- Add `grad_placements` parameter to `DTensor.from_local()`, allowing explicit control over gradient placements in the backward pass ([#175867](https://github.com/pytorch/pytorch/pull/175867))
### improvements
- Support DTensor view ops (flatten/unflatten) with `_StridedSharding` for full `nn.Linear(DTensor)` compatibility ([#166483](https://github.com/pytorch/pytorch/pull/166483))
- Add Dijkstra-based single-dim strategy search for DTensor sharding propagation, avoiding exponential enumeration of strategy combinations ([#169438](https://github.com/pytorch/pytorch/pull/169438))
- DTensor: Add `is_pinned()` support ([#177235](https://github.com/pytorch/pytorch/pull/177235))
- DTensor: Add `print()` HOP support ([#175222](https://github.com/pytorch/pytorch/pull/175222))
- DTensor: Emit zero paddings for uneven shardings to enable SPMD compilation ([#177758](https://github.com/pytorch/pytorch/pull/177758))
- DTensor: Make `run_dtensor_rng_op` compatible with `compile_on_one_rank` ([#177447](https://github.com/pytorch/pytorch/pull/177447))
- DTensor: Lenient handling of view redistributes in decomposition flow ([#175194](https://github.com/pytorch/pytorch/pull/175194))
- DTensor: Redistribute from/to `_StridedShard` through `Replicate` ([#179059](https://github.com/pytorch/pytorch/pull/179059))
- DTensor: Raise clearer error for unsupported `Split(Flatten)` sharding propagation ([#179632](https://github.com/pytorch/pytorch/pull/179632))
- DTensor: Unbacked-safe `view_groups` ([#174629](https://github.com/pytorch/pytorch/pull/174629))
- DTensor: Expanded sharding strategy coverage for `index_select`, `index`, `index_fill`, `index_reduce`, `roll`, `fft`, `constant_pad_nd`, `squeeze.dims`, `interpolate`, `linalg` ops, `LayerNorm`/`RMSNorm` FW/BW, `foreach`/`fused` ops, and einsum linearity ([#176037](https://github.com/pytorch/pytorch/pull/176037), [#176038](https://github.com/pytorch/pytorch/pull/176038), [#178456](https://github.com/pytorch/pytorch/pull/178456), [#175463](https://github.com/pytorch/pytorch/pull/175463), [#175656](https://github.com/pytorch/pytorch/pull/175656), [#173563](https://github.com/pytorch/pytorch/pull/173563), [#176991](https://github.com/pytorch/pytorch/pull/176991), [#176955](https://github.com/pytorch/pytorch/pull/176955), [#179173](https://github.com/pytorch/pytorch/pull/179173), [#177186](https://github.com/pytorch/pytorch/pull/177186), [#177187](https://github.com/pytorch/pytorch/pull/177187), [#176150](https://github.com/pytorch/pytorch/pull/176150), [#174830](https://github.com/pytorch/pytorch/pull/174830))
### bug fixes
- Fix DTensor subclass `__torch_dispatch__` bypass ([#177878](https://github.com/pytorch/pytorch/pull/177878))
- Fix symbolic shape handling by copying symbolic shapes as needed ([#178210](https://github.com/pytorch/pytorch/pull/178210))
- Fix `_StridedShard` not in safe globals for checkpoint loading ([#178560](https://github.com/pytorch/pytorch/pull/178560))
- Fix DTensor `stack` dim normalization ([#174640](https://github.com/pytorch/pytorch/pull/174640))
- Fix DTensor `view_as_complex` with `P(max)`/`P(min)` placements ([#173935](https://github.com/pytorch/pytorch/pull/173935))
- Fix DTensor `get_mesh_from_args` when first arg is not a tensor ([#169265](https://github.com/pytorch/pytorch/pull/169265))
- Fix DTensor `tp_conv` rejecting batch-dim-only sharding for valid configs ([#176448](https://github.com/pytorch/pytorch/pull/176448))
- Fix DTensor `compute_local_stride` for unevenly-sharded tensors ([#177174](https://github.com/pytorch/pytorch/pull/177174))
- Fix DTensor `scaled_mm` sharding strategy ([#177234](https://github.com/pytorch/pytorch/pull/177234))
- Fix DTensor double-shard validation in `propagate_shape_and_sharding` ([#177973](https://github.com/pytorch/pytorch/pull/177973))
- Fix DTensor Dijkstra sharding search shardability checks and graceful fallback ([#177167](https://github.com/pytorch/pytorch/pull/177167))
- Fix DTensor `index_put` sharding strategy for `None` indices ([#179217](https://github.com/pytorch/pytorch/pull/179217))
- Fix DTensor precision loss in `NestedRedistribute` backward dtype handling ([#179495](https://github.com/pytorch/pytorch/pull/179495))
- Fix DTensor backward for value-selecting reductions (`topk`, `sort`, `min`, etc.) ([#178668](https://github.com/pytorch/pytorch/pull/178668))
- Fix DTensor `InputDim.__eq__` type guard to prevent int comparison bugs ([#178599](https://github.com/pytorch/pytorch/pull/178599))
- Fix None IValue == DTensorSpec, cache key collision, and move op_strategy_context ([#178442](https://github.com/pytorch/pytorch/pull/178442))
- Fix `DeviceMesh.__getitem__` by disabling proxy tensor handling ([#176007](https://github.com/pytorch/pytorch/pull/176007))
### performance
- Improve DTensor performance for `torch.cat` and pytree ops ([#174879](https://github.com/pytorch/pytorch/pull/174879))
- Skip unnecessary all-reduce of `total_weight` in DTensor `nll_loss_backward` for `reduction='sum'` ([#177233](https://github.com/pytorch/pytorch/pull/177233))
- Cache `DecompStrategy` and fake mesh in DTensor ([#175205](https://github.com/pytorch/pytorch/pull/175205))
### docs
### devs
- Add `_dtensor::mesh_get_process_group` custom op ([#178116](https://github.com/pytorch/pytorch/pull/178116))
- Add custom op for flattened submesh lookup during `compile_on_one_rank` tracing ([#178889](https://github.com/pytorch/pytorch/pull/178889))
### Untopiced
### not user facing
- Fix CPU test tolerances for low-precision operations ([#174953](https://github.com/pytorch/pytorch/pull/174953))
- [DTensor] Fixes a potential hang in ShardingPropagator when using multi-threading test ([#174820](https://github.com/pytorch/pytorch/pull/174820))
- Attempt to repro ([#175289](https://github.com/pytorch/pytorch/pull/175289))
- Add FakeTensor, ProxyTensor and serialization support to inductor_compiled_code HOP ([#174504](https://github.com/pytorch/pytorch/pull/174504))
- Start removing asserts in torch/distributed ([#174688](https://github.com/pytorch/pytorch/pull/174688))
- [DTensor] Enable Dijkstra search in sharding propagation ([#175999](https://github.com/pytorch/pytorch/pull/175999))
- [dtensor] Register sharding strategy for inductor_prims.fma ([#177424](https://github.com/pytorch/pytorch/pull/177424))
- Centralize use_strided_shard_as_shard_order propagation for all ops ([#179208](https://github.com/pytorch/pytorch/pull/179208))
- Organize DTensor OpInfo xfails ([#175234](https://github.com/pytorch/pytorch/pull/175234))
- DTensor end-to-end test for strategy validator ([#175588](https://github.com/pytorch/pytorch/pull/175588))
- Fix sourceless tracing issue for opaque objects ([#176236](https://github.com/pytorch/pytorch/pull/176236))
- Add reconstruct_fn to opaque type registration for make_fx tracing ([#178970](https://github.com/pytorch/pytorch/pull/178970))
- Fix test interaction: clean up DTensorSpec pytree registration ([#176128](https://github.com/pytorch/pytorch/pull/176128))
- Fix inverted condition in `_unflatten` string dim validation ([#176563](https://github.com/pytorch/pytorch/pull/176563))
- Fix test_comm_mode_with_dtensor for Dijkstra sharding propagation ([#177798](https://github.com/pytorch/pytorch/pull/177798))
- Fix DeviceMesh _sym_get_coordinate crash and register __ne__ for opaque types ([#178110](https://github.com/pytorch/pytorch/pull/178110))
- Add unflatten tests for multi-mesh sharding in view ops ([#176151](https://github.com/pytorch/pytorch/pull/176151))
- Fix flaky DTensor sharding prop cache logging test ([#176119](https://github.com/pytorch/pytorch/pull/176119))
- DTensor: Improve strategy validator denoising for Partial inputs ([#175265](https://github.com/pytorch/pytorch/pull/175265))
- DTensor: Replace prop_index_put with single_dim_strategy ([#172894](https://github.com/pytorch/pytorch/pull/172894))
- DTensor: Strategy Validation (3/3, 4/4) and fixes ([#174800](https://github.com/pytorch/pytorch/pull/174800), [#174995](https://github.com/pytorch/pytorch/pull/174995), [#175821](https://github.com/pytorch/pytorch/pull/175821), [#175589](https://github.com/pytorch/pytorch/pull/175589), [#175892](https://github.com/pytorch/pytorch/pull/175892), [#177595](https://github.com/pytorch/pytorch/pull/177595), [#176020](https://github.com/pytorch/pytorch/pull/176020), [#176034](https://github.com/pytorch/pytorch/pull/176034))
- DTensor: prims ops sharding strategies ([#174442](https://github.com/pytorch/pytorch/pull/174442))
- DTensor: Add _PreparedSingleDimStrategy ([#175462](https://github.com/pytorch/pytorch/pull/175462))
- DTensor: Auto-append output placement for .out variant ops ([#175960](https://github.com/pytorch/pytorch/pull/175960))
- DTensor: Extract monotonic ops from pointwise_ops ([#175685](https://github.com/pytorch/pytorch/pull/175685), [#175686](https://github.com/pytorch/pytorch/pull/175686), [#175687](https://github.com/pytorch/pytorch/pull/175687))
- DTensor: expand_to_full_mesh_op_strategy filters mixed partials ([#173614](https://github.com/pytorch/pytorch/pull/173614))
- DTensor: layernorm output meta ([#175652](https://github.com/pytorch/pytorch/pull/175652))
- DTensor: Validate Dijkstra match feasibility with redistribute_cost ([#177168](https://github.com/pytorch/pytorch/pull/177168))
- DTensor: Remove dead code from pointwise_ops ([#178975](https://github.com/pytorch/pytorch/pull/178975))
### security
