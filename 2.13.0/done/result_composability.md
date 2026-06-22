
# Release Notes worksheet composability

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

## composability
### bc breaking
### deprecation
- Custom operators that return an output aliasing one of their inputs are deprecated ([#182063](https://github.com/pytorch/pytorch/pull/182063))

  When a custom operator returns an output that is the same tensor as (or otherwise aliases) one of its inputs under `torch.compile`, PyTorch now emits a `UserWarning` stating that this is deprecated and will become an error in a future version of PyTorch. Previously the warning stated the change would land in PyTorch 2.12; that timeline has been pushed back. To update your code, return a clone of the offending output instead of the input, or refactor the operator so it does not return the aliased tensor.

  Deprecated:
  ```python
  @torch.library.custom_op("mylib::foo", mutates_args=())
  def foo(x: torch.Tensor) -> torch.Tensor:
      return x  # output aliases the input -- deprecated
  ```

  Updated:
  ```python
  @torch.library.custom_op("mylib::foo", mutates_args=())
  def foo(x: torch.Tensor) -> torch.Tensor:
      return x.clone()  # return a clone instead
  ```
### new features
- Formalize in-place operators with `torch.Tag.inplace` and `torch.Tag.out`. Native in-place operators are now automatically tagged via torchgen, and custom operators (defined via `torch.library`) can opt in by adding the tag. An in-place operator mutates its first positional argument and returns it; for custom operators the first argument must be the only mutable argument, a plain `Tensor(a!)`, and must be the returned tensor. Custom operators tagged with `torch.Tag.inplace` now go through `auto_functionalize` during `torch.compile`, enabling the reinplacing pass to do clone analysis and avoid unnecessary copies. Ops tagged with `torch.Tag.inplace` and `torch.Tag.out` also have their fake kernels autogenerated. ([#181100](https://github.com/pytorch/pytorch/pull/181100), [#181099](https://github.com/pytorch/pytorch/pull/181099), [#184199](https://github.com/pytorch/pytorch/pull/184199), [#184200](https://github.com/pytorch/pytorch/pull/184200), [#184201](https://github.com/pytorch/pytorch/pull/184201), [#184202](https://github.com/pytorch/pytorch/pull/184202), [#184203](https://github.com/pytorch/pytorch/pull/184203))
### improvements
- Add `op_overloads` to `OpOverloadPacket` to enumerate an operator's overloads ([#182993](https://github.com/pytorch/pytorch/pull/182993))
- Add fake tensor support for `_transformer_encoder_layer_fwd` so it traces under `torch.compile` ([#183916](https://github.com/pytorch/pytorch/pull/183916))
### bug fixes
- Add differentiable decomposition for `max_pool2d/3d_with_indices` ([#179104](https://github.com/pytorch/pytorch/pull/179104))
- Add validation for invalid `MaxUnpool` output sizes in meta/decomposition kernels ([#184706](https://github.com/pytorch/pytorch/pull/184706))
- Add validation for invalid `conv2d` kernel size in meta and symbolic-shape kernels ([#180448](https://github.com/pytorch/pytorch/pull/180448))
- Add `addmv` decomposition dtype validation ([#184140](https://github.com/pytorch/pytorch/pull/184140))
- Add `fill_` meta value-tensor dimensionality validation ([#179363](https://github.com/pytorch/pytorch/pull/179363))
- Add `_weight_int8pack_mm` meta inner-dims and scales validation ([#179364](https://github.com/pytorch/pytorch/pull/179364))
- Fix `torch.empty(..., out=...)` shape validation under `torch.compile` ([#182349](https://github.com/pytorch/pytorch/pull/182349))
- Fix `torch.compile` wrong output shape for `norm()` with a negative `dim` ([#182405](https://github.com/pytorch/pytorch/pull/182405))
- Fix `frac` decomposition signed-zero handling ([#183640](https://github.com/pytorch/pytorch/pull/183640))
- Fix `pad_sequence` mixed-dtype padding decomposition ([#184173](https://github.com/pytorch/pytorch/pull/184173))
- Fix `istft` fake tensor length padding ([#184532](https://github.com/pytorch/pytorch/pull/184532))
- Fix `unfold_backward` decomposition for overlapping windows ([#183996](https://github.com/pytorch/pytorch/pull/183996))
- Fix split `Tensor` decomposition in Inductor ([#184134](https://github.com/pytorch/pytorch/pull/184134))
- Fix embedding negative indices in Inductor ([#184107](https://github.com/pytorch/pytorch/pull/184107))
- Fix flash SDPA activation dtype mismatch between meta and CPU implementations ([#185573](https://github.com/pytorch/pytorch/pull/185573))
- Preserve 5D nearest upsample decomposition layout ([#184553](https://github.com/pytorch/pytorch/pull/184553))
- Preserve `aten.hardtanh` meta semantics for export ([#185298](https://github.com/pytorch/pytorch/pull/185298))
- Fix `_fused_dropout` decomposition at keep-probability zero ([#184979](https://github.com/pytorch/pytorch/pull/184979))
- Fix `addmm` decomposition crash with `out_dtype` under `FakeTensorMode` ([#179634](https://github.com/pytorch/pytorch/pull/179634))
- Fix `torch.split` decomposition for empty dim with nonzero `split_size` ([#181493](https://github.com/pytorch/pytorch/pull/181493))
- Fix `torch.distributions.Gamma` under `torch.compile` ([#174090](https://github.com/pytorch/pytorch/pull/174090))
- Fix `miopen_batch_norm` meta `save_mean`/`save_var` dtype ([#179365](https://github.com/pytorch/pytorch/pull/179365))
- Fix reflection/replication pad stride mismatch under `torch.compile` ([#179837](https://github.com/pytorch/pytorch/pull/179837))
- Fix symbolic float `lp_pool2d` compilation ([#184000](https://github.com/pytorch/pytorch/pull/184000))
- Compare in opmath in `hardtanh_backward` decomposition ([#185840](https://github.com/pytorch/pytorch/pull/185840))
- Use `torch.sigmoid()` in `silu_backward` decomposition ([#185041](https://github.com/pytorch/pytorch/pull/185041))
- Fix `index_copy` decomposition shape checks ([#184338](https://github.com/pytorch/pytorch/pull/184338))
- Fix LSTM export hidden state metadata ([#185716](https://github.com/pytorch/pytorch/pull/185716))
- Fix private convolution fake symint handling ([#185081](https://github.com/pytorch/pytorch/pull/185081))
- Preserve strides in meta `zero` ([#185360](https://github.com/pytorch/pytorch/pull/185360))
- Fix runtime check for `non_overlapping_and_dense` ([#186785](https://github.com/pytorch/pytorch/pull/186785))
- Update `_cslt_sparse_mm` meta registration for hipSPARSELt ([#181609](https://github.com/pytorch/pytorch/pull/181609))
- Fix reflection/replication pad output memory format to match eager behavior on XPU ([#184484](https://github.com/pytorch/pytorch/pull/184484))
- Handle unbacked dims in folded matmul under FakeTensor ([#183397](https://github.com/pytorch/pytorch/pull/183397))
- Preserve unbacked batch dims in SDPA tracing under ProxyTensor ([#183398](https://github.com/pytorch/pytorch/pull/183398))
- Fix `torch.compile` crash from `aten.lift` functionalization on an already-functionalized tensor (e.g. `randint` followed by `lift`) ([#185805](https://github.com/pytorch/pytorch/pull/185805))
### performance
- Use `torch.var_mean` to fuse paired var/mean reductions ([#184843](https://github.com/pytorch/pytorch/pull/184843))
### docs
### devs
- Change most HOPs to use `@register_fake` instead of `py_impl(FakeTensorMode)` ([#186247](https://github.com/pytorch/pytorch/pull/186247))
- Genericize graphsafe RNG in `aot_autograd` to support non-CUDA device backends ([#182391](https://github.com/pytorch/pytorch/pull/182391))
- Mark `graphsafe_run_with_rng_state` as cacheable for `FxGraphCache` ([#185562](https://github.com/pytorch/pytorch/pull/185562))
### Untopiced
### not user facing
- Enable `opcheck` stride checking for CPU tensors ([#183002](https://github.com/pytorch/pytorch/pull/183002), [#183353](https://github.com/pytorch/pytorch/pull/183353))
- Make data-dependent-safe shape handling for unbacked `SymInt`s in `is_same_shape` (via `sym_eq`) ([#184943](https://github.com/pytorch/pytorch/pull/184943)) and pooling meta functions ([#183774](https://github.com/pytorch/pytorch/pull/183774))
- Unify output dimension handling between `scan` and `associative_scan` so `scan` now moves the scan dimension back to its original position in its outputs ([#182673](https://github.com/pytorch/pytorch/pull/182673))
- Error on raw SymInt args in fx graph call function nodes, and add Graph helpers for sym shape/stride/storage_offset nodes ([#183664](https://github.com/pytorch/pytorch/pull/183664))
- Make `isinstance(x, OpaqueBase)` reliably detect all opaque types, including value-type opaques and metaclass-registered reference types ([#180530](https://github.com/pytorch/pytorch/pull/180530))
- [ShapesSpec] Refactor lookup_spec_from_dynamo_source ([#184299](https://github.com/pytorch/pytorch/pull/184299))
- [ShapesSpec] unify variables with same shape var ([#184853](https://github.com/pytorch/pytorch/pull/184853))
- Add @requires_gpu decorator to user_defined_triton_kernel_autotune test ([#185229](https://github.com/pytorch/pytorch/pull/185229))
- Tighten generalized scatter graph target ([#184075](https://github.com/pytorch/pytorch/pull/184075))
- [ShapesSpec] Support derived expressions as leaf specs in shapes_spec and setup path for assumptions ([#185154](https://github.com/pytorch/pytorch/pull/185154))
- [ShapesSpec] Support ShapesSpec.assumptions for cross-input shape invariants ([#185161](https://github.com/pytorch/pytorch/pull/185161))
- Rename `TensorWithFlatten` to `TraceableWrapperSubclass` and improve typing ([#180359](https://github.com/pytorch/pytorch/pull/180359))
- Handle `dict` arguments in `_iterate_exprs` for Triton kernel wrapper nodes ([#180471](https://github.com/pytorch/pytorch/pull/180471))
- Cache `_sub_unbacked_exprs` to avoid repeated slow `sympy.subs` calls ([#184915](https://github.com/pytorch/pytorch/pull/184915))
- Fix deferred `SymFloat` runtime assertions being dropped at runtime by including unbacked `SymFloat` symbols in the deferred assertion bucket key ([#185692](https://github.com/pytorch/pytorch/pull/185692))
- Add `Graph.materialize_symints` along with `create_size_node`, `create_stride_node`, and `create_storage_offset_node` helpers for materializing symbolic shape values as FX nodes. Passing raw `SymInt`/`SymFloat`/`SymBool` values to `Graph.create_node` now emits a warning ([#186665](https://github.com/pytorch/pytorch/pull/186665))
- Prefer cross-symbol duck specialization over specializing to 0/1 in the unbacked size-oblivious meta fallback ([#183342](https://github.com/pytorch/pytorch/pull/183342))
### security
