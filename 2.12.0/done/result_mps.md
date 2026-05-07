
# Release Notes worksheet mps

## mps
### bc breaking
- All MPS tensors are now allocated in unified memory ([#175818](https://github.com/pytorch/pytorch/pull/175818))

  Previously, MPS tensors could be allocated in either device-only or unified memory. Now all MPS tensors use unified memory unconditionally. This simplifies memory management and enables CPU access to MPS tensor data without explicit copies. Code that relied on device-only memory placement may observe different performance characteristics.

### deprecation
### new features
- Implemented `linalg_qr` for MPS ([#172536](https://github.com/pytorch/pytorch/pull/172536))
- Added `cholesky_solve` support on MPS ([#176703](https://github.com/pytorch/pytorch/pull/176703))
- Added `index_reduce` on MPS ([#174936](https://github.com/pytorch/pytorch/pull/174936))
- Implemented `torch.distributions.Gamma` (forward + backward) on MPS ([#179228](https://github.com/pytorch/pytorch/pull/179228))
- Enabled `mvlgamma` on MPS ([#178914](https://github.com/pytorch/pytorch/pull/178914))
- Added `nonzero_static` implementation on MPS ([#179589](https://github.com/pytorch/pytorch/pull/179589)) _(from miscategorized)_
### improvements
- Fixed `abs` complex overflow/underflow on MPS ([#174346](https://github.com/pytorch/pytorch/pull/174346))
- Migrated `index_fill_` to native Metal ([#175822](https://github.com/pytorch/pytorch/pull/175822))
- Extended `histogram` to float/bfloat types on MPS ([#176913](https://github.com/pytorch/pytorch/pull/176913))
- Extended `unfold_backward` to `torch.complex64` on MPS ([#177274](https://github.com/pytorch/pytorch/pull/177274))
- Added complex input support to `scatter`, `gather`, `repeat`, `cumsum`, `logcumsumexp`, `cumprod`, and `nn.functional.linear` on MPS ([#177794](https://github.com/pytorch/pytorch/pull/177794), [#178198](https://github.com/pytorch/pytorch/pull/178198), [#178328](https://github.com/pytorch/pytorch/pull/178328), [#178411](https://github.com/pytorch/pytorch/pull/178411), [#178436](https://github.com/pytorch/pytorch/pull/178436), [#178799](https://github.com/pytorch/pytorch/pull/178799))
- Migrated `lerp`, `eye`, `relu`, `silu`, `fill_`, `xlogy`, `norm` to native Metal kernels ([#177093](https://github.com/pytorch/pytorch/pull/177093), [#178683](https://github.com/pytorch/pytorch/pull/178683), [#178866](https://github.com/pytorch/pytorch/pull/178866), [#179071](https://github.com/pytorch/pytorch/pull/179071), [#176101](https://github.com/pytorch/pytorch/pull/176101), [#177749](https://github.com/pytorch/pytorch/pull/177749), [#177328](https://github.com/pytorch/pytorch/pull/177328))
- Registered `DeviceCapability` for MPS backend ([#178180](https://github.com/pytorch/pytorch/pull/178180))
- Switched exponential distribution to native Metal ([#174277](https://github.com/pytorch/pytorch/pull/174277))
### bug fixes
- Fixed `AvgPool` for channels_last + offset inputs ([#175235](https://github.com/pytorch/pytorch/pull/175235))
- Fixed `linalg_solve` to return pivots ([#175284](https://github.com/pytorch/pytorch/pull/175284))
- Fixed `lu_solve` for broadcasted bias ([#175332](https://github.com/pytorch/pytorch/pull/175332))
- Fixed `addmm`/`mm` to return zero-filled matrix when an input is empty ([#175905](https://github.com/pytorch/pytorch/pull/175905))
- Fixed `index_reduce` atomic misalignment for sub-32-bit types ([#176009](https://github.com/pytorch/pytorch/pull/176009))
- Fixed `masked_fill` for non-contiguous outputs ([#176171](https://github.com/pytorch/pytorch/pull/176171))
- Fixed `layer_norm` with noncontiguous bias ([#176238](https://github.com/pytorch/pytorch/pull/176238))
- Added unsigned int types to Metal cast operations ([#176343](https://github.com/pytorch/pytorch/pull/176343))
- Fixed `solve_triangular` for noncontiguous inputs ([#176335](https://github.com/pytorch/pytorch/pull/176335))
- Fixed `histogram`/`histogramdd` with noncontiguous weight ([#175906](https://github.com/pytorch/pytorch/pull/175906))
- Fixed MPS memory leak in `getStridedMPSNDArray` ([#176648](https://github.com/pytorch/pytorch/pull/176648))
- Added error checking for `bmm` on MPS ([#176771](https://github.com/pytorch/pytorch/pull/176771))
- Fixed half-precision type mismatches in Metal shader codegen ([#176436](https://github.com/pytorch/pytorch/pull/176436))
- Fixed SDPA output shape when value head dim differs ([#176843](https://github.com/pytorch/pytorch/pull/176843))
- Added error when creating `torch.cdouble` tensor on MPS ([#176985](https://github.com/pytorch/pytorch/pull/176985))
- Fixed `_copy_from_and_resize` logic ([#177606](https://github.com/pytorch/pytorch/pull/177606))
- Fixed linear backward crash with channels_last grad ([#178278](https://github.com/pytorch/pytorch/pull/178278))
- Fixed mm padding overflow and incorrect alignment conditions ([#178203](https://github.com/pytorch/pytorch/pull/178203))
- Fixed nested `ops.masked` variable name collisions in Metal codegen ([#178304](https://github.com/pytorch/pytorch/pull/178304))
- Fixed in-place `self.add_(other, alpha)` RuntimeErrors with type promotion ([#178724](https://github.com/pytorch/pytorch/pull/178724))
- Fixed `BatchNorm` with mixed input/weight dtypes ([#178775](https://github.com/pytorch/pytorch/pull/178775))
- Fixed hi/lo swap typo in Metal Philox RNG ([#179227](https://github.com/pytorch/pytorch/pull/179227))
- Allowed `getMPSScalar` construction for uint64 ([#179230](https://github.com/pytorch/pytorch/pull/179230))
- Fixed `mm` with stride-0 inputs on macOS < 26.4 ([#180236](https://github.com/pytorch/pytorch/pull/180236))
- Fixed `masked_scatter` side-effect and aligned behavior with CPU ([#175622](https://github.com/pytorch/pytorch/pull/175622))
- Fixed `lgamma`/`digamma`/`polygamma` noncontiguous behavior ([#175603](https://github.com/pytorch/pytorch/pull/175603))
- Fixed `masked_scatter` to preserve scalar tensor shape ([#174381](https://github.com/pytorch/pytorch/pull/174381))
### performance
- Reimplemented `cross` as single-stage Metal kernel ([#175498](https://github.com/pytorch/pytorch/pull/175498))
- Replaced MPSGraph `nonzero` with native Metal prefix-sum + scatter ([#178484](https://github.com/pytorch/pytorch/pull/178484))
- Sped up `RMSNorm` on MPS ([#180173](https://github.com/pytorch/pytorch/pull/180173))
- Removed `.item()` sync in `_amp_non_finite_check_and_unscale_mps` ([#180267](https://github.com/pytorch/pytorch/pull/180267))
### docs
### devs
- Standardized Metal kernel compilation around `AsyncCompile` ([#179838](https://github.com/pytorch/pytorch/pull/179838))
- Removed pre-MacOS14 check from `MpsDeviceInterface` ([#175804](https://github.com/pytorch/pytorch/pull/175804)) _(from miscategorized)_
### not user facing
- [BE][MPS] Use `fmt::format` to compute key ([#175249](https://github.com/pytorch/pytorch/pull/175249))
- [BE][MPS] Add `_3d` suffix `grid_sampler` kernel ([#175060](https://github.com/pytorch/pytorch/pull/175060))
- [MPS] Update `test_noncontiguous_samples` decorators and error comments ([#176348](https://github.com/pytorch/pytorch/pull/176348))
- [MPS] Migrate minimum/maximum from MPSGraph to native Metal ([#177747](https://github.com/pytorch/pytorch/pull/177747))
- [MPS] Remove some usages of double dtype in MPS tests ([#177766](https://github.com/pytorch/pytorch/pull/177766))
- [BE] Fix compilation warning in Indexing.metal ([#178507](https://github.com/pytorch/pytorch/pull/178507))
- [MPS] bundled shared library typo ([#179447](https://github.com/pytorch/pytorch/pull/179447))
- [BE] Refactor shared interpolation helpers into SamplingHelpers.h ([#179751](https://github.com/pytorch/pytorch/pull/179751))
- [MPS] Support instrumentation of Objective-C++ ([#178702](https://github.com/pytorch/pytorch/pull/178702))
- [MPS][BE] Replace `.count(hash) = 0` with `.contains(hash)` ([#178337](https://github.com/pytorch/pytorch/pull/178337))
- [BE] [MPS] Improve call site of `_scaled_dot_product_attention_math_mps` ([#179309](https://github.com/pytorch/pytorch/pull/179309))
### security
