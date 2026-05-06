
# Release Notes worksheet composability

## composability
### bc breaking
### deprecation
### new features
### improvements
- Added `DynamicInt` `__pow__` and `__rpow__` methods ([#179868](https://github.com/pytorch/pytorch/pull/179868))
- Added `scaled_mm_v2` CPU implementation ([#176266](https://github.com/pytorch/pytorch/pull/176266))
### bug fixes
- Fixed stride handling in FFT meta registrations ([#175731](https://github.com/pytorch/pytorch/pull/175731))
- Fixed exception messages displaying as tuples instead of formatted strings ([#175957](https://github.com/pytorch/pytorch/pull/175957))
- Fixed `one_hot` runtime error ([#177160](https://github.com/pytorch/pytorch/pull/177160))
- Fixed wrong bool-to-int conversion in symbolic tracing ([#177178](https://github.com/pytorch/pytorch/pull/177178))
- Preserved scalar `item()` semantics for size-1 tensors ([#177270](https://github.com/pytorch/pytorch/pull/177270))
- Fixed `_build_proxy_for_sym_expr` for n-ary `sympy.Add` by mapping to `torch.sym_sum` ([#175398](https://github.com/pytorch/pytorch/pull/175398))
### performance
- Decomposed `mm`/`addmm` to pointwise multiply when K==1, yielding up to 1.55x speedup for outer-product-like matrix multiplications ([#175825](https://github.com/pytorch/pytorch/pull/175825))
- Improved tracing speed via the `aggressive_guard_free_semantics` config flag ([#174654](https://github.com/pytorch/pytorch/pull/174654))
- Reduced threshold for calling `sympy.factor` to 50, avoiding expensive symbolic simplification on large expressions ([#177779](https://github.com/pytorch/pytorch/pull/177779))
- Added per-SymNode expression cache, reducing redundant symbolic computation ([#175353](https://github.com/pytorch/pytorch/pull/175353))
### docs
### devs
- Deleted `size_vars` / `size_hint` API ([#175365](https://github.com/pytorch/pytorch/pull/175365))
- Changed symbolic expressions to use `FloorDiv` and `Mod` instead of `//` and `%` on SymPy exprs ([#177051](https://github.com/pytorch/pytorch/pull/177051))
- Tagged backward nodes via `_patch_autograd_grad` and updated remat pass ([#179105](https://github.com/pytorch/pytorch/pull/179105))
- Added `fast_bind` support in `normalize_function` for FakeTensor ([#175740](https://github.com/pytorch/pytorch/pull/175740))
### not user facing
- Add partition merging for regions connected by data dependencies in regional inductor ([#178690](https://github.com/pytorch/pytorch/pull/178690))
- Revert to CapabilityBasedPartitioner with per-region partitioning in regional inductor ([#179209](https://github.com/pytorch/pytorch/pull/179209))
- Fix `SYMPY_INTERP` calling convention for `IsNonOverlappingAndDenseIndicator` ([#179031](https://github.com/pytorch/pytorch/pull/179031))
- Handle div by 0 in optimization hint when fallback is 0 ([#177709](https://github.com/pytorch/pytorch/pull/177709))
- Fix clamp(None, nan) to propagate scalar NaNs ([#172200](https://github.com/pytorch/pytorch/pull/172200))
- Fix DDE in meta_copy ([#175582](https://github.com/pytorch/pytorch/pull/175582))
- [meta_registrations] Add bmm out variant support ([#175619](https://github.com/pytorch/pytorch/pull/175619))
- index_select decomposition preserve memory format ([#175638](https://github.com/pytorch/pytorch/pull/175638))
- Use TORCH_SYM_CHECK in nll_loss_nd_symint for symbolic size comparison to avoid DDE  ([#175956](https://github.com/pytorch/pytorch/pull/175956))
- [MXFP4] Fix E8M0 blockwise scale size validation for packed FP4 in _scaled_mm ([#176357](https://github.com/pytorch/pytorch/pull/176357))
- [Bugfix] Fix nll bug via decomposition handling ([#177189](https://github.com/pytorch/pytorch/pull/177189))
- Fix staged CUDA FFT meta strides ([#177323](https://github.com/pytorch/pytorch/pull/177323))
- Fix export for unary torch.where ([#177493](https://github.com/pytorch/pytorch/pull/177493))
- [BE][Ez]: Fused some empty as_strided calls ([#177545](https://github.com/pytorch/pytorch/pull/177545))
- Fix scalar-only add/sub alpha out refs in torch.compile ([#177677](https://github.com/pytorch/pytorch/pull/177677))
- Inductor Decomposition-Fix Return Value Type Mismatch On binary_cross_entropy_with_logits ([#176844](https://github.com/pytorch/pytorch/pull/176844))
- [Bugfix] Fix meta conv backwards strides ([#177175](https://github.com/pytorch/pytorch/pull/177175))
- Support half precision FFT on XPU backend ([#171231](https://github.com/pytorch/pytorch/pull/171231))
- [PyTorch] Add meta kernel for _scaled_dot_product_fused_attention_overrideable_backward (#178494) ([#178494](https://github.com/pytorch/pytorch/pull/178494))
- decomp:add decomposition for aten.hann_window ([#177946](https://github.com/pytorch/pytorch/pull/177946))
- [easy] fix rng decomposition typo ([#174308](https://github.com/pytorch/pytorch/pull/174308))
- Fix _make_dep_token meta to return 0-dim tensor ([#179354](https://github.com/pytorch/pytorch/pull/179354))
- Fix rrelu_with_noise_backward decomposition to match C++ ([#179355](https://github.com/pytorch/pytorch/pull/179355))
- Dynamo bug fix: Missing meta kernel for aten::quantize_per_tensor.tensor_qparams ([#169697](https://github.com/pytorch/pytorch/pull/169697))
- fix: aten.quantize_per_tensor isn't a MKLDNN-specific operator ([#180218](https://github.com/pytorch/pytorch/pull/180218))
- Fix slice_scatter meta overlap handling ([#180166](https://github.com/pytorch/pytorch/pull/180166))
### security
