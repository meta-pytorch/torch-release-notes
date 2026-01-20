# PyTorch 2.10.0 Release Notes

- [Highlights](#highlights)
- [Backwards Incompatible Changes](#backwards-incompatible-changes)
- [Deprecations](#deprecations)
- [New Features](#new-features)
- [Improvements](#improvements)
- [Bug fixes](#bug-fixes)
- [Performance](#performance)
- [Documentation](#documentation)
- [Developers](#developers)
- [Security](#security)

# Highlights

<table>
  <tr>
    <td>
      <strong>Python 3.14</strong> support for <code>torch.compile()</code>. Python 3.14t (freethreaded build) is experimentally supported as well.
    </td>
  <tr>
  <tr>
    <td> Reduced kernel launch overhead with <strong>combo-kernels</strong> horizontal fusion in torchinductor </td>
  <tr>
  <tr>
    <td> A new <strong>varlen_attn()</strong> op providing support for ragged and packed sequences </td>
  <tr>
  <tr>
    <td> Efficient eigenvalue decompositions with <strong>DnXgeev</strong> </td>
  <tr>
  <tr>
    <td> <code>torch.compile()</code> now respects <strong>use_deterministic_mode</strong> </td>
  <tr>
  <tr>
    <td> <strong>DebugMode</strong> for tracking dispatched calls and debugging numerical divergence - This makes it simpler to track down subtle numerical bugs. </td>
  <tr>
  <tr>
    <td> <strong>tlparse & TORCH_TRACE</strong> improvements to make it easier to diagnose and collaborate on compilation issues </td>
  <tr>
</table>

For more details about these highlighted features, you can look at the [release blogpost](https://pytorch.org/blog/pytorch2-10/). Below are the full release notes for this release.

# Backwards Incompatible Changes
## Dataloader Frontend
- Removed unused `data_source` argument from Sampler ([#163134](https://github.com/pytorch/pytorch/pull/163134)). This is a no-op, unless you have a custom sampler that uses this argument. Please update your custom sampler accordingly.

- Removed deprecated imports for torch.utils.data.datapipes.iter.grouping ([#163438](https://github.com/pytorch/pytorch/pull/163438)). `from torch.utils.data.datapipes.iter.grouping import SHARDING_PRIORITIES, ShardingFilterIterDataPipe` is no longer supported. Please import from `torch.utils.data.datapipes.iter.sharding` instead.

## torch.nn
- Remove Nested Jagged Tensor support from `nn.attention.flex_attention` ([#161734](https://github.com/pytorch/pytorch/pull/161734))

## ONNX
- `fallback=False` is now the default in `torch.onnx.export` ([#162726](https://github.com/pytorch/pytorch/pull/162726))
- The exporter now uses the `dynamo=True` option without fallback. This is the recommended way to use the ONNX exporter. To preserve 2.9 behavior, manually set `fallback=True` in the `torch.onnx.export` call.

## Release Engineering
- Rename pytorch-triton package to triton ([#169888](https://github.com/pytorch/pytorch/pull/169888))

# Deprecations
## Distributed
- DeviceMesh
  - Added a warning for slicing flattened dim from root mesh and types for _get_slice_mesh_layout ([#164993](https://github.com/pytorch/pytorch/pull/164993))

We decided to deprecate an existing behavior which goes against the PyTorch design principle (explicit over implicit) for device mesh slicing of flattened dim.

### Version <2.9
```python
import torch
from torch.distributed.device_mesh import

device_type = (
    acc.type
    if (acc := torch.accelerator.current_accelerator(check_available=True))
    else "cpu"
)
mesh_shape = (2, 2, 2)
mesh_3d = init_device_mesh(
    device_type, mesh_shape, mesh_dim_names=("dp", "cp", "tp")
)

mesh_3d["dp", "cp"]._flatten()
mesh_3["dp_cp"]  # This comes with no warning
```

### Version >=2.10
```python
import torch
from torch.distributed.device_mesh import

device_type = (
    acc.type
    if (acc := torch.accelerator.current_accelerator(check_available=True))
    else "cpu"
)
mesh_shape = (2, 2, 2)
mesh_3d = init_device_mesh(
    device_type, mesh_shape, mesh_dim_names=("dp", "cp", "tp")
)

mesh_3d["dp", "cp"]._flatten()
mesh_3["dp_cp"]  # This will come with a warning because it implicitly change the state of the original mesh. We will eventually remove this behavior in future release. User should do the bookkeeping of flattened mesh explicitly.
```

## Ahead-Of-Time Inductor (AOTI)
- Move `from`/`to` to `torch::stable::detail` ([#164956](https://github.com/pytorch/pytorch/pull/164956))

## JIT
- `torch.jit` is not guaranteed to work in Python 3.14. Deprecation warnings have been added to user-facing `torch.jit` API ([#167669](https://github.com/pytorch/pytorch/pull/167669)).
`torch.jit` should be replaced with `torch.compile` or `torch.export`.

## ONNX
- The `dynamic_axes` option in `torch.onnx.export` is deprecated ([#165769](https://github.com/pytorch/pytorch/pull/165769))
- Users should supply the `dynamic_shapes` argument instead. See https://docs.pytorch.org/docs/stable/export.html#expressing-dynamism for more documentation.

## Profiler
- Deprecate `export_memory_timeline` method ([#168036](https://github.com/pytorch/pytorch/pull/168036))

The `export_memory_timeline` method in `torch.profiler` is being deprecated in favor of the newer memory snapshot API (`torch.cuda.memory._record_memory_history` and `torch.cuda.memory._export_memory_snapshot`). This change adds the deprecated decorator from `typing_extensions` and updates the docstring to guide users to the recommended alternative.

# New Features
## Autograd
- Allow setting grad_dtype on leaf tensors ([#164751](https://github.com/pytorch/pytorch/pull/164751))

- Add Default Autograd Fallback for PrivateUse1 in PyTorch ([#165315](https://github.com/pytorch/pytorch/pull/165315))

- Add API to annotate disjoint backward for use with `torch.utils.checkpoint.checkpoint` ([#166536](https://github.com/pytorch/pytorch/pull/166536))

## Complex Frontend
- Add `ComplexTensor` subclass ([#167621](https://github.com/pytorch/pytorch/pull/167621))

## Composability
- Support autograd in torch.cond ([#165908](https://github.com/pytorch/pytorch/pull/165908))

## cuDNN
- BFloat16 support added to cuDNN RNN ([#164411](https://github.com/pytorch/pytorch/pull/164411))

## Distributed
- LocalTensor:
  - LocalTensor is a powerful debugging and simulation tool in PyTorch's distributed tensor ecosystem. It allows you to simulate distributed tensor computations across multiple SPMD (Single Program, Multiple Data) ranks on a single process. This is incredibly valuable for: 1) debugging distributed code without spinning up multiple processes; 2) understanding DTensor behavior by inspecting per-rank tensor states; 3) testing DTensor operations with uneven sharding across ranks; 4) rapid prototyping of distributed algorithms. Note that LocalTensor is designed for debugging purposes only. It has significant overhead and is not suitable for production distributed training.
  - LocalTensor is a torch.Tensor subclass that internally holds a mapping from rank IDs to local tensor shards. When you perform a PyTorch operation on a LocalTensor, the operation is applied independently to each local shard, mimicking distributed computation (LocalTensor simulates collective operations locally without actual network communication.). LocalTensorMode is the context manager that enables LocalTensor dispatch. It intercepts PyTorch operations and routes them appropriately. The @maybe_run_for_local_tensor decorator is essential for handling rank-specific logic when implementing distributed code.
  - To get started with LocalTensor, users import from torch.distributed._local_tensor, initialize a fake process group, and wrap their distributed code in a LocalTensorMode context. Within this context, DTensor operations automatically produce LocalTensors.
  - PRs: ([#164537](https://github.com/pytorch/pytorch/pull/164537), [#166595](https://github.com/pytorch/pytorch/pull/166595), [#168110](https://github.com/pytorch/pytorch/pull/168110),[#168314](https://github.com/pytorch/pytorch/pull/168314),[#169088](https://github.com/pytorch/pytorch/pull/169088),[#169734](https://github.com/pytorch/pytorch/pull/169734))

- c10d:
  - New shrink_group implementation to expose `ncclCommShrink` API ([#164518](https://github.com/pytorch/pytorch/pull/164518))

## Dynamo
- `torch.compile` now fully works in Python 3.14 ([#167384](https://github.com/pytorch/pytorch/pull/167384))

- Add option to error or disable applying side effects ([#167239](https://github.com/pytorch/pytorch/pull/167239))

- Config flag (`skip_fwd_side_effects_in_bwd_under_checkpoint`) to allow eager and compile activation-checkpointing divergence for side-effects ([#165775](https://github.com/pytorch/pytorch/pull/165775))

- `torch._higher_order_ops.print` for enabling printing without graph breaks or reordering ([#167571](https://github.com/pytorch/pytorch/pull/167571))

## FX
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

## Inductor
- Add experimental Pallas TorchInductor backend. ([#166822](https://github.com/pytorch/pytorch/pull/166822))

- Add Pallas TPU backend support. ([#167774](https://github.com/pytorch/pytorch/pull/167774))

- Add Flash Attention support to FlexAttention. ([#161118](https://github.com/pytorch/pytorch/pull/161118))

- Add deterministic mode for Inductor compilation. ([#163589](https://github.com/pytorch/pytorch/pull/163589)) ([#165950](https://github.com/pytorch/pytorch/pull/165950)) ([#164532](https://github.com/pytorch/pytorch/pull/164532))

- Enable custom op autotune decompositions and parameter tuning. ([#164212](https://github.com/pytorch/pytorch/pull/164212))  ([#167193](https://github.com/pytorch/pytorch/pull/167193))

- Expose `torch.compiler.config.force_disable_caches` as a public API. ([#166699](https://github.com/pytorch/pytorch/pull/166699))

- Add HOP for additional control dependencies to enforce explicit scheduling. ([#164568](https://github.com/pytorch/pytorch/pull/164568))

- Add Inductor Lite Mode ([#167115](https://github.com/pytorch/pytorch/pull/167115))

- Add distributed autotuning support ([#163369](https://github.com/pytorch/pytorch/pull/163369))

- Add Native matmul support to inductor ([#157743](https://github.com/pytorch/pytorch/pull/157743))

## Ahead-Of-Time Inductor (AOTI)
- Integrate AOTI as a backend. ([#167338](https://github.com/pytorch/pytorch/pull/167338))

- Add AOTI mingw cross compilation for Windows. ([#163188](https://github.com/pytorch/pytorch/pull/163188))

## MPS
- MPS sparse backend is functional
([#162349](https://github.com/pytorch/pytorch/pull/162349), [#162349](https://github.com/pytorch/pytorch/pull/162349), [#162007](https://github.com/pytorch/pytorch/pull/162007), [#162910](https://github.com/pytorch/pytorch/pull/162910), [#162885](https://github.com/pytorch/pytorch/pull/162885), [#163011](https://github.com/pytorch/pytorch/pull/163011), [#163694](https://github.com/pytorch/pytorch/pull/163694), [#164961](https://github.com/pytorch/pytorch/pull/164961), [#165102](https://github.com/pytorch/pytorch/pull/165102), [#166708](https://github.com/pytorch/pytorch/pull/166708), [#166711](https://github.com/pytorch/pytorch/pull/166711), [#167013](https://github.com/pytorch/pytorch/pull/167013), [#169125](https://github.com/pytorch/pytorch/pull/169125), [#165232](https://github.com/pytorch/pytorch/pull/165232), [#166708](https://github.com/pytorch/pytorch/pull/166708), [#168154](https://github.com/pytorch/pytorch/pull/168154), [#169368](https://github.com/pytorch/pytorch/pull/169368), [#167908](https://github.com/pytorch/pytorch/pull/167908), [#168112](https://github.com/pytorch/pytorch/pull/168112))

## torch.nn
- Add `nn.functional.scaled_mm` ([#164142](https://github.com/pytorch/pytorch/pull/164142))
- Add `nn.functional.scaled_grouped_mm` ([#165154](https://github.com/pytorch/pytorch/pull/165154))
- Add `nn.attention.varlen_attn` ([#164502](https://github.com/pytorch/pytorch/pull/164502), [#164504](https://github.com/pytorch/pytorch/pull/164504))

- Add `nn.functional.grouped_mm` ([#168298](https://github.com/pytorch/pytorch/pull/168298))

## ONNX
- A new testing module `torch.onnx.testing` with a testing utility `assert_onnx_program` ([#162495](https://github.com/pytorch/pytorch/pull/162495))

## Profiler
- Add scope for `RecordFunctionFast` ([#162661](https://github.com/pytorch/pytorch/pull/162661))

## Quantization
- Add `_scaled_mm_v2` API ([#164141](https://github.com/pytorch/pytorch/pull/164141))

- Add `scaled_grouped_mm_v2` and python API ([#165154](https://github.com/pytorch/pytorch/pull/165154))

- Add `embedding_bag_byte_prepack_with_rowwise_min_max` and `embedding_bag_{2/4}bit_prepack_with_rowwise_min_max` ([#162924](https://github.com/pytorch/pytorch/pull/162924))

- Add `MXFP4` support for `_scaled_grouped_mm_v2` via. FBGEMM kernels ([#166530](https://github.com/pytorch/pytorch/pull/166530))

## Release Engineering
- Enabled auto-revert on PyTorch CI ([#163858](https://github.com/pytorch/pytorch/pull/163858), [#164911](https://github.com/pytorch/pytorch/pull/164911), [#165459](https://github.com/pytorch/pytorch/pull/165459))

- Add PEP 517 compliant Python source distribution package to release process ([#157815](https://github.com/pytorch/pytorch/pull/157815))

- Add Pallas CI testing infrastructure with CPU and GPU test ([#167143](https://github.com/pytorch/pytorch/pull/167143), [#167428](https://github.com/pytorch/pytorch/pull/167428), [#169687](https://github.com/pytorch/pytorch/pull/169687), [#169494](https://github.com/pytorch/pytorch/pull/169494), [#169802](https://github.com/pytorch/pytorch/pull/169802))

## ROCm
- Enable grouped GEMM via regular GEMM fallback ([#162419](https://github.com/pytorch/pytorch/pull/162419))

- Enable grouped GEMM via CK ([#166334](https://github.com/pytorch/pytorch/pull/166334), [#167403](https://github.com/pytorch/pytorch/pull/167403))

- Enable ATen GEMM overload for FP32 output from FP16/BF16 inputs ([#162600](https://github.com/pytorch/pytorch/pull/162600))

- Support torch.cuda._compile_kernel ([#162510](https://github.com/pytorch/pytorch/pull/162510))

- Enhanced Windows support
- load_inline ([#162577](https://github.com/pytorch/pytorch/pull/162577))
- Enable AOTriton runtime compile ([#165538](https://github.com/pytorch/pytorch/pull/165538))
- AOTriton scaled_dot_product_attention ([#162330](https://github.com/pytorch/pytorch/pull/162330))

- Add gfx1150 gfx1151 to hipblaslt-supported GEMM lists ([#164744](https://github.com/pytorch/pytorch/pull/164744))

- Add scaled_mm v2 support. ([#165528](https://github.com/pytorch/pytorch/pull/165528))

- Add torch.version.rocm, distinct from torch.version.hip ([#168097](https://github.com/pytorch/pytorch/pull/168097))

## XPU
- Support ATen operators `scaled_mm` and `scaled_mm_v2` for Intel GPU ([#166056](https://github.com/pytorch/pytorch/pull/166056))

- Support ATen operator `_weight_int8pack_mm` for Intel GPU ([#160938](https://github.com/pytorch/pytorch/pull/160938))

- Extend SYCL support in PyTorch CPP Extension API to allow users to implement new custom operators on Windows ([#162579](https://github.com/pytorch/pytorch/pull/162579))

- Add API `torch.xpu.get_per_process_memory_fraction` for Intel GPU ([#165511](https://github.com/pytorch/pytorch/pull/165511))

- Add API `torch.xpu.set_per_process_memory_fraction` for Intel GPU ([#165510](https://github.com/pytorch/pytorch/pull/165510))

- Add API `torch.xpu.is_tf32_supported` for Intel GPU ([#163141](https://github.com/pytorch/pytorch/pull/163141))

- Add API `torch.xpu.can_device_access_peer` for Intel GPU ([#162705](https://github.com/pytorch/pytorch/pull/162705))

- Add API `torch.accelerator.get_memory_info` for Intel GPU ([#162564](https://github.com/pytorch/pytorch/pull/162564))

# Improvements
## Build Frontend
- Abort explicitly requested CUDA build if toolkit could not be found ([#166982](https://github.com/pytorch/pytorch/pull/166982))

- RISC-V build improvements ([#166602](https://github.com/pytorch/pytorch/pull/166602), [#167071](https://github.com/pytorch/pytorch/pull/167071), [#165717](https://github.com/pytorch/pytorch/pull/165717))

- Allow building with arbitrary BLAS library ([#166333](https://github.com/pytorch/pytorch/pull/166333))

- Allow building with LeakSanitizer ([#158686](https://github.com/pytorch/pytorch/pull/158686))

## Composability
- If you are using the `torch.compile(backend="aot_eager")` backend, it should now give bitwise equivalent results in eager. Previously it sometimes would not due to extra compile-only decompositions running ([#165910](https://github.com/pytorch/pytorch/pull/165910))

- Some dynamic shape errors were changed to recommend using `torch._check` over `torch._check_is_size` ([#164889](https://github.com/pytorch/pytorch/pull/164889),

- Some unbacked (dynamic shape) improvements ([#162652](https://github.com/pytorch/pytorch/pull/162652), [#169612](https://github.com/pytorch/pytorch/pull/169612))

- Some bugfixes for symbolic float handling in compile ([#166573](https://github.com/pytorch/pytorch/pull/166573), [#162788](https://github.com/pytorch/pytorch/pull/162788))

## C++ Frontend
- Changed `TORCH_CHECK_{COND}` behavior to be non-fatal ([#167004](https://github.com/pytorch/pytorch/pull/167004))

- Migrated `TypeTraits`, `TypeList`, `Metaprogramming`, `DeviceType`, `MemoryFormat`, `Layout`, `version.h`, and `CppTypeToScalarType` to `torch::headeronly` ([#167386](https://github.com/pytorch/pytorch/pull/167386), [#163999](https://github.com/pytorch/pytorch/pull/163999), [#168034](https://github.com/pytorch/pytorch/pull/168034), [#165153](https://github.com/pytorch/pytorch/pull/165153), [#164381](https://github.com/pytorch/pytorch/pull/164381), [#167610](https://github.com/pytorch/pytorch/pull/167610))

- Bumped `libfmt` submodule version to `12.0.0` ([#163441](https://github.com/pytorch/pytorch/pull/163441))

## CUDA
- Make `torch.cuda.rng_set_state` and `torch.cuda.rng_get_state` work in CUDA graph capture. ([#162505](https://github.com/pytorch/pytorch/pull/162505))

- `torch.cuda._compile_kernel`
- Enable templated kernels ([#162875](https://github.com/pytorch/pytorch/pull/162875))
- Enable pre-compiled kernels ([#162972](https://github.com/pytorch/pytorch/pull/162972))
- Add CUDA headers automatically ([#162634](https://github.com/pytorch/pytorch/pull/162634))
- Remove outdated `header_code` argument ([#163165](https://github.com/pytorch/pytorch/pull/163165))

- Prevent copies of std::vector in CUDA ForeachOps ([#163416](https://github.com/pytorch/pytorch/pull/163416))

- Implement cuda-python CUDA stream protocol ([#163614](https://github.com/pytorch/pytorch/pull/163614))

- Remove outdated checks and docs for cuBLAS determinism ([#161749](https://github.com/pytorch/pytorch/pull/161749))

- Cleanup old workaround code in `launch_logcumsumexp_cuda_kernel` ([#164567](https://github.com/pytorch/pytorch/pull/164567))

- Add a compile-time flag to trigger verbose logging for device-side asserts ([#166171](https://github.com/pytorch/pytorch/pull/166171))

- Support SM 10.3 in custom CUTLASS matmuls ([#162956](https://github.com/pytorch/pytorch/pull/162956))

- Enable CUTLASS matmuls on Thor ([#164836](https://github.com/pytorch/pytorch/pull/164836))

- Add `per_process_memory_fraction` option to `PYTORCH_CUDA_ALLOC_CONF` ([#161035](https://github.com/pytorch/pytorch/pull/161035))

- Support nested memory pools ([#168382](https://github.com/pytorch/pytorch/pull/168382))

## Distributed
- c10d
  - Added handling of discontiguous allgather/reducescatter inputs ([#163712](https://github.com/pytorch/pytorch/pull/163712))
  - Supported high stream for ProcessGroupXCCL ([#163049](https://github.com/pytorch/pytorch/pull/163049))

- Context Parallel
  - Introduced ContextParallal plan for `parallelize_module` ([#162542](https://github.com/pytorch/pytorch/pull/162542))
  - Replaced context_parallel context manager with functional APIs ([#164500](https://github.com/pytorch/pytorch/pull/164500))
  - Introduced `flex_cp_forward` custom op for FlexAttention CP ([#163185](https://github.com/pytorch/pytorch/pull/163185))
  - Add `_templated_ring_attention` to the backward compatility stub ([#166991](https://github.com/pytorch/pytorch/pull/166991))
  - Added `_LoadBalancer` classes, and load-balance interface to Context Parallel APIs with process-time based Round-Robin load-balance ([#161062](https://github.com/pytorch/pytorch/pull/161062), [#163617](https://github.com/pytorch/pytorch/pull/163617))
  - Added python bindings for NCCL CTA policies ([#164309](https://github.com/pytorch/pytorch/pull/164309))

- DeviceMesh
  - Adopted CuTe layout for DeviceMesh internal bookkeepings with a shared 1D _rank_map tensor and related code cleanups ([#162413](https://github.com/pytorch/pytorch/pull/162413), [#162534](https://github.com/pytorch/pytorch/pull/162534), [#163212](https://github.com/pytorch/pytorch/pull/163212), [#163288](https://github.com/pytorch/pytorch/pull/163288), [#163928](https://github.com/pytorch/pytorch/pull/163928), [#163930](https://github.com/pytorch/pytorch/pull/163930), [#164750](https://github.com/pytorch/pytorch/pull/164750), [#164954](https://github.com/pytorch/pytorch/pull/164954), [#164510](https://github.com/pytorch/pytorch/pull/164510), [#166264](https://github.com/pytorch/pytorch/pull/166264), [#167581](https://github.com/pytorch/pytorch/pull/167581), [#162690](https://github.com/pytorch/pytorch/pull/162690), [#163367](https://github.com/pytorch/pytorch/pull/163367), [#166614](https://github.com/pytorch/pytorch/pull/166614))
  - Implemented `_unflatten` on top of CuTe layout bookkeeping ([#161224](https://github.com/pytorch/pytorch/pull/161224), [#165521](https://github.com/pytorch/pytorch/pull/165521))
  - Added support of `_rank` for use with non-global PGs ([#162439](https://github.com/pytorch/pytorch/pull/162439))
  
  - FullyShardDataParallel (FSDP1 and FSDP2)
  - Implemented idempotent `reset_sharded_param`: no-op if _local_tensor is already padded ([#163130](https://github.com/pytorch/pytorch/pull/163130))
  - Added support of AC(FSDP) for torchtitan's MOE ([#164009](https://github.com/pytorch/pytorch/pull/164009))
  - Provided public API to share cuda streams across roots ([#165024](https://github.com/pytorch/pytorch/pull/165024))

- DTensor
  - Extended conv ops to 3D ([#165241](https://github.com/pytorch/pytorch/pull/165241), [#167402](https://github.com/pytorch/pytorch/pull/167402))
  - Added an explicit mode (ExplicitRedistributionContext) for DTensor redistribute ([#166593](https://github.com/pytorch/pytorch/pull/166593), [#167370](https://github.com/pytorch/pytorch/pull/167370), [#169452](https://github.com/pytorch/pytorch/pull/169452))
  - Reduced DTensor CPU overhead by moving logic into c++ and more optimizations to sharding propagation and cache ([#162508](https://github.com/pytorch/pytorch/pull/162508), [#163820](https://github.com/pytorch/pytorch/pull/163820), [#162990](https://github.com/pytorch/pytorch/pull/162990), [#166750](https://github.com/pytorch/pytorch/pull/166750), [#166989](https://github.com/pytorch/pytorch/pull/166989), [#166990](https://github.com/pytorch/pytorch/pull/166990), [#167051](https://github.com/pytorch/pytorch/pull/167051), [#166372](https://github.com/pytorch/pytorch/pull/166372), [#166808](https://github.com/pytorch/pytorch/pull/166808), [#167475](https://github.com/pytorch/pytorch/pull/167475), [#167588](https://github.com/pytorch/pytorch/pull/167588), [#168264](https://github.com/pytorch/pytorch/pull/168264), [#169519](https://github.com/pytorch/pytorch/pull/169519), [#168051](https://github.com/pytorch/pytorch/pull/168051), [#168983](https://github.com/pytorch/pytorch/pull/168983), [#166132](https://github.com/pytorch/pytorch/pull/166132), [#167580](https://github.com/pytorch/pytorch/pull/167580), [#168269](https://github.com/pytorch/pytorch/pull/168269))
  - Enable per-rank RNG state collect/set for XPU devices in DTensor ([#169410](https://github.com/pytorch/pytorch/pull/169410))
  - Added `_foreach_pow`, `logsumexp` and `masked_fill_.Scalar` to sharding propagation list. ([#162895](https://github.com/pytorch/pytorch/pull/162895), [#163879](https://github.com/pytorch/pytorch/pull/163879), [#169668](https://github.com/pytorch/pytorch/pull/169668))

- SymmetricMemory
  - Added MemPool support to CUDA backend and get_mem_pool API ([#169740](https://github.com/pytorch/pytorch/pull/169740), [#170008](https://github.com/pytorch/pytorch/pull/170008), [#169739](https://github.com/pytorch/pytorch/pull/169739))
  - Added op `multimem_one_shot_reduce_out` ([#164517](https://github.com/pytorch/pytorch/pull/164517))
  - Added op `multi_root_tile_reduce` ([#162243](https://github.com/pytorch/pytorch/pull/162243), [#164757](https://github.com/pytorch/pytorch/pull/164757))
  - Added op to get remote tensors ([#167779](https://github.com/pytorch/pytorch/pull/167779))
  - Added `symm_mem_sync` Triton kernel to `torch.ops.symm_mem` ([#168917](https://github.com/pytorch/pytorch/pull/168917))
  - Added a NVSHMEM based one side API ([#159837](https://github.com/pytorch/pytorch/pull/159837), [#163194](https://github.com/pytorch/pytorch/pull/163194))
  - Skipped multicast initialization if it fails ([#163750](https://github.com/pytorch/pytorch/pull/163750))
  - Supported copy engine based all-gather and all-to-all ([#170344](https://github.com/pytorch/pytorch/pull/170344), [#170265](https://github.com/pytorch/pytorch/pull/170265))
  - Added `set_signal_pad_size` API for SymmetricMemory ([#169156](https://github.com/pytorch/pytorch/pull/169156))

- Pipeline Parallelism
  - Made runtime dbg log print custom actions ([#167113](https://github.com/pytorch/pytorch/pull/167113))
  - Moved profiler record_function in schedule and improved visualizer ([#164976](https://github.com/pytorch/pytorch/pull/164976), [#160474](https://github.com/pytorch/pytorch/pull/160474))
  - Enabled inspect of schedule IR with comms ([#162996](https://github.com/pytorch/pytorch/pull/162996))
  - Use default export mode (non-strict) for pipeline parallelism ([#164045](https://github.com/pytorch/pytorch/pull/164045))
  - Enabled PP split BlockMask into micro-BlockMask ([#164111](https://github.com/pytorch/pytorch/pull/164111))
  - Migrate other schedules to use `PipelineScheduleRuntime` ([#164777](https://github.com/pytorch/pytorch/pull/164777))
  - Improvement the composability with FSDP with FSDP reduce scatters moved to end of step and backward_counter updated to schedule class ([#165106](https://github.com/pytorch/pytorch/pull/165106), [#165513](https://github.com/pytorch/pytorch/pull/165513))
  - Added optional argument to not save outputs ([#165822](https://github.com/pytorch/pytorch/pull/165822))
  - Added PP Runtime Features for supporting Graph Based execution ([#167277](https://github.com/pytorch/pytorch/pull/167277))
  - Used same dtype for receive and send tensor when initializing p2p communication. ([#165539](https://github.com/pytorch/pytorch/pull/165539))
  - Support `OVERLAP_F_B` in schedule ([#161072](https://github.com/pytorch/pytorch/pull/161072))
  - Support custom callback functions in schedule ([#162016](https://github.com/pytorch/pytorch/pull/162016))

- torchelastic
  - Added support to handle IGUSR1 and SIGUSR2 in multiprocessing ([#160690](https://github.com/pytorch/pytorch/pull/160690))
  - Captured exit codes after sigterm/sigkill from torch elastic. ([#160908](https://github.com/pytorch/pytorch/pull/160908))
  - Duplicate stdout and stderr and apply custom filter in torchrun ([#160712](https://github.com/pytorch/pytorch/pull/160712))
  - Added flush option to `TailLog` ([#167169](https://github.com/pytorch/pytorch/pull/167169))


## Dynamo
- Turn on `capture_scalar_outputs` and `capture_dynamic_output_shape_ops` when `fullgraph=True` ([#163121](https://github.com/pytorch/pytorch/pull/163121), [#163123](https://github.com/pytorch/pytorch/pull/163123))

- Improved tracing for `dict` key hashing ([#169204](https://github.com/pytorch/pytorch/pull/169204))

- Tracing support for `torch.cuda.stream` ([#166472](https://github.com/pytorch/pytorch/pull/166472))

- Improved tracing of `torch.autograd.Function`s ([#166788](https://github.com/pytorch/pytorch/pull/166788))

- Miscellaneous smaller tracing support additions:
- Extend `collections.defaultdict` support with `*args`, `**kwargs` and custom `default_factory` ([#166793](https://github.com/pytorch/pytorch/pull/166793))
- Support for bitwise xor ([#166065](https://github.com/pytorch/pytorch/pull/166065))
- Support `repr` on user-defined objects ([#167372](https://github.com/pytorch/pytorch/pull/167372))
- Support new typing union syntax `X | Y` ([#166599](https://github.com/pytorch/pytorch/pull/166599))

## Export
- Improved fake tensor leakage detection in export ([#163516](https://github.com/pytorch/pytorch/pull/163516))

- Improved support for tensor subclasses ([#163770](https://github.com/pytorch/pytorch/pull/163770))

## FX
- Add tensor subclass printing support in fx/graph.py ([#164403](https://github.com/pytorch/pytorch/pull/164403))

- Update Node.is_impure check if subgraph contains impure ops ([#166609](https://github.com/pytorch/pytorch/pull/166609), [#167443](https://github.com/pytorch/pytorch/pull/167443))

- Explicitly remove call_mod_node_to_replace after inlining the submodule in const_fold._inline_module` ([#166871](https://github.com/pytorch/pytorch/pull/166871))

- Add strict argument validation to Interpreter.boxed_run ([#166784](https://github.com/pytorch/pytorch/pull/166784))

- Use stable topological sort in fuse_by_partitions ([#167397](https://github.com/pytorch/pytorch/pull/167397))

## Inductor
- Pruned failed compilations from Autotuning candidates ([#162673](https://github.com/pytorch/pytorch/pull/162673))

- Extend triton_mm auto-tune options for HIM shapes ([#163273](https://github.com/pytorch/pytorch/pull/163273))

- Various fixes for AOTI-FX backend
- Solve for undefined symbols in dynamic input shapes ([#163044](https://github.com/pytorch/pytorch/pull/163044))
- Support symbol and dynamic scalar graph inputs and outputs ([#163596](https://github.com/pytorch/pytorch/pull/163596))
- Support unbacked symbol definitions ([#163729](https://github.com/pytorch/pytorch/pull/163729))
- Generalize FloorDiv conversion to handle more complex launch grids. ([#163828](https://github.com/pytorch/pytorch/pull/163828))
- Don't flatten constant args ([#166144](https://github.com/pytorch/pytorch/pull/166144))
- Support SymInt placeholder([#167757](https://github.com/pytorch/pytorch/pull/167757))
- Support torch.cond ([#163234](https://github.com/pytorch/pytorch/pull/163234))

- Add tanh, exp, and sigmoid activations for Cutlass backend. ([#162535](https://github.com/pytorch/pytorch/pull/162535)) ([#162536](https://github.com/pytorch/pytorch/pull/162536))

- Hardened the experimental horizontal fusion `torch._inductor.config.combo_kernels` ([#162442](https://github.com/pytorch/pytorch/pull/162442)) ([#166274](https://github.com/pytorch/pytorch/pull/166274)) ([#162759](https://github.com/pytorch/pytorch/pull/162759)) ([#167781](https://github.com/pytorch/pytorch/pull/167781)) ([#168127](https://github.com/pytorch/pytorch/pull/168127)) ([#168946](https://github.com/pytorch/pytorch/pull/168946)) ([#168109](https://github.com/pytorch/pytorch/pull/168109)) ([#164918](https://github.com/pytorch/pytorch/pull/164918))

- Enable TMA store for TMA matmul templates on Triton. ([#160480](https://github.com/pytorch/pytorch/pull/160480))

- Add Blackwell GPU templates (persistent matmul, FP8 scaled persistent + TMA GEMMs, CuTeDSL grouped GEMM, FlexFlash forward, FlexAttention configs). ([#162916](https://github.com/pytorch/pytorch/pull/162916)) ([#163147](https://github.com/pytorch/pytorch/pull/163147)) ([#167340](https://github.com/pytorch/pytorch/pull/167340)) ([#167040](https://github.com/pytorch/pytorch/pull/167040)) ([#165760](https://github.com/pytorch/pytorch/pull/165760))

- Support `qconv_pointwise.tensor` and `qconv2d_pointwise.binary_tensor` quantized operations. ([#166608](https://github.com/pytorch/pytorch/pull/166608))

- Support `out_dtype` argument for matmul operations. ([#163393](https://github.com/pytorch/pytorch/pull/163393))

- Add support for bound methods in pattern matcher. ([#167795](https://github.com/pytorch/pytorch/pull/167795))

- Add way to register custom rules for graph partitioning. ([#166458](https://github.com/pytorch/pytorch/pull/166458)) ([#163310](https://github.com/pytorch/pytorch/pull/163310))

- Add codegen support for `fast_tanhf` on ROCm. ([#162052](https://github.com/pytorch/pytorch/pull/162052))

- Support deepseek-style FP8 scaling in Inductor. ([#164404](https://github.com/pytorch/pytorch/pull/164404))

- Enable int64 indexing in convolution and matmul templates. ([#162506](https://github.com/pytorch/pytorch/pull/162506))

- Add SDPA patterns for T5 variants when batch size is 1. ([#163252](https://github.com/pytorch/pytorch/pull/163252))

- Add mechanism to get optimal autotune decision for FlexAttention. ([#165817](https://github.com/pytorch/pytorch/pull/165817))

- Add fallback config `fallback_embedding_bag_byte_unpack`. ([#163803](https://github.com/pytorch/pytorch/pull/163803))

- Expose config for FX bucket all_reduces. ([#167634](https://github.com/pytorch/pytorch/pull/167634))

- Add in-kernel NaN check support. ([#166008](https://github.com/pytorch/pytorch/pull/166008))

- Enable `pad_mm` and `decompose_mm_pass` pass on Intel GPU. ([#166618](https://github.com/pytorch/pytorch/pull/166618))  ([#166613](https://github.com/pytorch/pytorch/pull/166613))

- Improve CUDA support for int8pack_mm weight-only quantization pattern. ([#161680](https://github.com/pytorch/pytorch/pull/161680)) ([#161848](https://github.com/pytorch/pytorch/pull/161848)) ([#163461](https://github.com/pytorch/pytorch/pull/163461))

- Improve heuristics for pointwise kernels on ROCm. ([#163197](https://github.com/pytorch/pytorch/pull/163197))

- Enable mix-order reduction fusion earlier and allow fusing more nodes. ([#168209](https://github.com/pytorch/pytorch/pull/168209))

- Make mix order reduction work with dynamic shapes ([#168117](https://github.com/pytorch/pytorch/pull/168117))

- Better use of memory tracking ([#168121](https://github.com/pytorch/pytorch/pull/168121))

- Turn on LOAF (for OSS) by default. ([#162030](https://github.com/pytorch/pytorch/pull/162030))

- Log kernel autotuning results to CSV. ([#164191](https://github.com/pytorch/pytorch/pull/164191))

- Add warning for CUDA graph re-recording from dynamic shapes. ([#162696](https://github.com/pytorch/pytorch/pull/162696))

- Quiesce triton compile workers by default. ([#169485](https://github.com/pytorch/pytorch/pull/169485))

- Support masked vectorization for tail loops with integer and bool datatypes. ([#165885](https://github.com/pytorch/pytorch/pull/165885))

- Support tile-wise (1x128) FP8 scaling in Inductor. ([#165132](https://github.com/pytorch/pytorch/pull/165132))

- Support fallback for all GEMM-like operations. ([#165755](https://github.com/pytorch/pytorch/pull/165755))

- Enable Triton kernels with unbacked inputs. ([#164509](https://github.com/pytorch/pytorch/pull/164509))

- Add AVX512-VNNI-based micro kernel for CPU GEMM template. ([#166846](https://github.com/pytorch/pytorch/pull/166846))

- Support mixed dtype in `native_layer_norm_backward` meta function. ([#159830](https://github.com/pytorch/pytorch/pull/159830))

- Add tech specs for MI350 GPU. ([#166576](https://github.com/pytorch/pytorch/pull/166576))

- Add `assume_32bit_indexing` inductor config option. ([#167784](https://github.com/pytorch/pytorch/pull/167784))

- Wire up mask_mod and blockmask to FlexFlash implementation. ([#166359](https://github.com/pytorch/pytorch/pull/166359))

- More aggressive mix order reduction for better fusion. ([#166382](https://github.com/pytorch/pytorch/pull/166382))

- Mix order reduction heuristics and tuning. ([#166585](https://github.com/pytorch/pytorch/pull/166585))

- CuteDSL flat indexer needs to be colexigraphic in coordinate space ([#166657](https://github.com/pytorch/pytorch/pull/166657))

## MPS
- Add `embedding_bag` operator ([#163012](https://github.com/pytorch/pytorch/pull/163012), [#163931](https://github.com/pytorch/pytorch/pull/163931), [#163281](https://github.com/pytorch/pytorch/pull/163281))

- Continue ops migration to Metal and add complex support ( [#169478](https://github.com/pytorch/pytorch/pull/169478), [#166903](https://github.com/pytorch/pytorch/pull/166903), [#167755](https://github.com/pytorch/pytorch/pull/167755), [#167826](https://github.com/pytorch/pytorch/pull/167826)m [#166216](https://github.com/pytorch/pytorch/pull/166216), [#166670](https://github.com/pytorch/pytorch/pull/166670), [#169407](https://github.com/pytorch/pytorch/pull/169407), [#166210](https://github.com/pytorch/pytorch/pull/166210), [#166090](https://github.com/pytorch/pytorch/pull/166090), [#168120](https://github.com/pytorch/pytorch/pull/168120), [#167569](https://github.com/pytorch/pytorch/pull/167569))

- Asynchronously report out-of-bounds access errors for `embedding_bag` and `index_select` ops ([#166615](https://github.com/pytorch/pytorch/pull/166615), [#168930](https://github.com/pytorch/pytorch/pull/168930), [#166468](https://github.com/pytorch/pytorch/pull/166468))

## Nested Tensor (NJT)
- Added NJT support for `share_memory_` ([#162272](https://github.com/pytorch/pytorch/pull/162272))

## torch.nn
- Support batch size 0 for flash attention in `scaled_dot_product_attention` ([#166318](https://github.com/pytorch/pytorch/pull/166318))

- Raise an error when using a sliced `BlockMask` in `nn.functional.flex_attention` ([#164702](https://github.com/pytorch/pytorch/pull/164702))

## ONNX
- Improved graph capture logic to preserve dynamic shapes and improve conversion success rate
- Cover all FX passes into backed size oblivious ([#166151](https://github.com/pytorch/pytorch/pull/166151))
- Set prefer_deferred_runtime_asserts_over_guards to True ([#165820](https://github.com/pytorch/pytorch/pull/165820))

- Various warning and error messages improvements ([#162819](https://github.com/pytorch/pytorch/pull/162819), [#163074](https://github.com/pytorch/pytorch/pull/163074), [#166412](https://github.com/pytorch/pytorch/pull/166412), [#166558](https://github.com/pytorch/pytorch/pull/166558), [#166692](https://github.com/pytorch/pytorch/pull/166692))

- Improved operator translation logic
- Update weight tensor initialization in RMSNormalization ([#166550](https://github.com/pytorch/pytorch/pull/166550))
- Support enable_gqa when dropout is non-zero ([#162771](https://github.com/pytorch/pytorch/pull/162771))

- Implement `tofile()` in ONNX IR tensors for more efficient ONNX model serialization ([#165195](https://github.com/pytorch/pytorch/pull/165195))

## Optimizer
- Make `Adam`, `AdamW` work with nonzero-dim Tensor betas ([#149939](https://github.com/pytorch/pytorch/pull/149939))

## Profiler
- Expose Kineto event metadata in PyTorch Profiler events ([#161624](https://github.com/pytorch/pytorch/pull/161624))

- Add `user_metadata` display to memory visualizer ([#165939](https://github.com/pytorch/pytorch/pull/165939))

- Add warning for clearing profiler events at the end of each cycle ([#168066](https://github.com/pytorch/pytorch/pull/168066))

## Python Frontend
- Improved `torch.library` and custom ops to support view functions ([#164520](https://github.com/pytorch/pytorch/pull/164520))

- Rework PyObject preservation to make it thread safe, significantly simpler and better handle some edge cases ([#167564](https://github.com/pytorch/pytorch/pull/167564))

- Remove reference cycle in torch.save to improve memory usage ([#165204](https://github.com/pytorch/pytorch/pull/165204))

- Add `generator` arg to `rand*_like` APIs ([#166160](https://github.com/pytorch/pytorch/pull/166160))

- support negative index arguments to torch.take_along_dim negative ([#152161](https://github.com/pytorch/pytorch/pull/152161))

## Quantization
- `half` and `bf16` support for `fused_moving_avg_obs_fake_quant` ([#162620](https://github.com/pytorch/pytorch/pull/162620), [#164175](https://github.com/pytorch/pytorch/pull/164175))

- `bf16` support for `fake_quantize_learnable_per_channel_affine` ([#165098](https://github.com/pytorch/pytorch/pull/165098))

- `bf16` support for backward of `torch._fake_quantize_learnable_per_tensor_affine` ([#165362](https://github.com/pytorch/pytorch/pull/165362))

- Add `NVFP4` two-level scaling to `scaled_mm` ([#165774](https://github.com/pytorch/pytorch/pull/165774))

- Add support for `fp8_input`/`fp8_weight`/`bf16_bias` and `bf16_output` for fp8 qconv in CPU ([#167611](https://github.com/pytorch/pytorch/pull/167611))

- Make the `torch.float4_e2m1fn_x2` dtype support equality comparisons ([#169575](https://github.com/pytorch/pytorch/pull/169575))

- add `copy_` support for `torch.float4_e2m1fn_x2` dtype ([#169595](https://github.com/pytorch/pytorch/pull/169595))

## Release Engineering
- Add support for CUDA 13.0 in CI/CD including binary builds, inductor benchmarks, and upgrade to CUDA 13.0.2 ([#162455](https://github.com/pytorch/pytorch/pull/162455), [#162425](https://github.com/pytorch/pytorch/pull/162425), [#163787](https://github.com/pytorch/pytorch/pull/163787), [#164383](https://github.com/pytorch/pytorch/pull/164383), [#164607](https://github.com/pytorch/pytorch/pull/164607), [#163239](https://github.com/pytorch/pytorch/pull/163239), [#165029](https://github.com/pytorch/pytorch/pull/165029), [#168091](https://github.com/pytorch/pytorch/pull/168091), [#169902](https://github.com/pytorch/pytorch/pull/169902), [#163988](https://github.com/pytorch/pytorch/pull/163988))

- Add B200 GPU support with symmetric memory testing and smoke tests ([#162988](https://github.com/pytorch/pytorch/pull/162988), [#168990](https://github.com/pytorch/pytorch/pull/168990))

- Improve CUDA builds for aarch64, Windows, and legacy driver support ([#162566](https://github.com/pytorch/pytorch/pull/162566), [#163956](https://github.com/pytorch/pytorch/pull/163956), [#164470](https://github.com/pytorch/pytorch/pull/164470), [#165013](https://github.com/pytorch/pytorch/pull/165013), [#163029](https://github.com/pytorch/pytorch/pull/163029), [#167769](https://github.com/pytorch/pytorch/pull/167769), [#167046](https://github.com/pytorch/pytorch/pull/167046))

- Upgrade to ROCm 7.0 and 7.1 ([#163860](https://github.com/pytorch/pytorch/pull/163860), [#163883](https://github.com/pytorch/pytorch/pull/163883), [#163937](https://github.com/pytorch/pytorch/pull/163937), [#163140](https://github.com/pytorch/pytorch/pull/163140), [#164201](https://github.com/pytorch/pytorch/pull/164201), [#165756](https://github.com/pytorch/pytorch/pull/165756), [#166665](https://github.com/pytorch/pytorch/pull/166665), [#166730](https://github.com/pytorch/pytorch/pull/166730), [#166693](https://github.com/pytorch/pytorch/pull/166693), [#167390](https://github.com/pytorch/pytorch/pull/167390), [#166764](https://github.com/pytorch/pytorch/pull/166764))

- Add support for MI355, MI300, gfx1100, gfx1150, gfx1151, and gfx950 GPU architectures ([#160215](https://github.com/pytorch/pytorch/pull/160215), [#167587](https://github.com/pytorch/pytorch/pull/167587), [#148355](https://github.com/pytorch/pytorch/pull/148355), [#165103](https://github.com/pytorch/pytorch/pull/165103), [#165326](https://github.com/pytorch/pytorch/pull/165326), [#165658](https://github.com/pytorch/pytorch/pull/165658), [#165699](https://github.com/pytorch/pytorch/pull/165699), [#167299](https://github.com/pytorch/pytorch/pull/167299), [#167225](https://github.com/pytorch/pytorch/pull/167225), [#169427](https://github.com/pytorch/pytorch/pull/169427), [#166544](https://github.com/pytorch/pytorch/pull/166544))

- Migrate ROCm CI to Ubuntu noble images and expand CI coverage ([#168230](https://github.com/pytorch/pytorch/pull/168230), [#168202](https://github.com/pytorch/pytorch/pull/168202), [#168088](https://github.com/pytorch/pytorch/pull/168088), [#167593](https://github.com/pytorch/pytorch/pull/167593), [#167379](https://github.com/pytorch/pytorch/pull/167379), [#162649](https://github.com/pytorch/pytorch/pull/162649), [#162721](https://github.com/pytorch/pytorch/pull/162721), [#163014](https://github.com/pytorch/pytorch/pull/163014), [#163339](https://github.com/pytorch/pytorch/pull/163339), [#163776](https://github.com/pytorch/pytorch/pull/163776), [#164244](https://github.com/pytorch/pytorch/pull/164244), [#164585](https://github.com/pytorch/pytorch/pull/164585), [#164279](https://github.com/pytorch/pytorch/pull/164279), [#164616](https://github.com/pytorch/pytorch/pull/164616), [#164769](https://github.com/pytorch/pytorch/pull/164769), [#165674](https://github.com/pytorch/pytorch/pull/165674), [#165821](https://github.com/pytorch/pytorch/pull/165821), [#166575](https://github.com/pytorch/pytorch/pull/166575), [#166645](https://github.com/pytorch/pytorch/pull/166645), [#166870](https://github.com/pytorch/pytorch/pull/166870), [#166915](https://github.com/pytorch/pytorch/pull/166915), [#166961](https://github.com/pytorch/pytorch/pull/166961), [#167220](https://github.com/pytorch/pytorch/pull/167220), [#167262](https://github.com/pytorch/pytorch/pull/167262), [#167483](https://github.com/pytorch/pytorch/pull/167483), [#168359](https://github.com/pytorch/pytorch/pull/168359), [#169300](https://github.com/pytorch/pytorch/pull/169300), [#169679](https://github.com/pytorch/pytorch/pull/169679), [#168104](https://github.com/pytorch/pytorch/pull/168104))

- Upgrade XPU support package to 2025.3 ([#166829](https://github.com/pytorch/pytorch/pull/166829))

- Upgrade XPU build infrastructure to GCC 13 and Ubuntu 24.04 ([#162474](https://github.com/pytorch/pytorch/pull/162474), [#162475](https://github.com/pytorch/pytorch/pull/162475), [#164127](https://github.com/pytorch/pytorch/pull/164127))

- Expand XPU testing coverage with profiler tests, inductor benchmarks, and additional unit tests ([#166289](https://github.com/pytorch/pytorch/pull/166289), [#166954](https://github.com/pytorch/pytorch/pull/166954), [#166047](https://github.com/pytorch/pytorch/pull/166047), [#165423](https://github.com/pytorch/pytorch/pull/165423), [#169799](https://github.com/pytorch/pytorch/pull/169799))

- Improve vLLM integration with nightly builds, aarch64 support, and test infrastructure ([#162371](https://github.com/pytorch/pytorch/pull/162371), [#162664](https://github.com/pytorch/pytorch/pull/162664), [#163232](https://github.com/pytorch/pytorch/pull/163232), [#163383](https://github.com/pytorch/pytorch/pull/163383), [#166146](https://github.com/pytorch/pytorch/pull/166146))

## ROCm
- Allow custom OpenBLAS library name for CMake build ([#166333](https://github.com/pytorch/pytorch/pull/166333))

- Add gfx1150 gfx1151 to binary build targets ([#164782](https://github.com/pytorch/pytorch/pull/164782), [#164854](https://github.com/pytorch/pytorch/pull/164854), [#164763](https://github.com/pytorch/pytorch/pull/164763))

- hipSPARSELt support - Update cuda_to_hip_mappings.py ([#167335](https://github.com/pytorch/pytorch/pull/167335))

- New implementation of upsample_bilinear2d_backward ([#164572](https://github.com/pytorch/pytorch/pull/164572))

- Remove env var HIPBLASLT_ALLOW_TF32 from codebase, TF32 always allowed ([#162998](https://github.com/pytorch/pytorch/pull/162998))

- Enable multi-arch compilation and unit tests for AOT Inductor ([#166357](https://github.com/pytorch/pytorch/pull/166357))

- Fix miopen batchnorm changing output format ([#162112](https://github.com/pytorch/pytorch/pull/162112))

- [ROCm] Enable multi-arch compilation and unit tests for AOT Inductor ([#166357](https://github.com/pytorch/pytorch/- pull/166357))

- [ROCm][inductor] autotune support for persistent reduction kernels ([#163908](https://github.com/pytorch/pytorch/- pull/163908))

## Sparse Frontend
- Add MPS support sparse_mask backward and sparse sum backward ([#166260](https://github.com/pytorch/pytorch/pull/166260), [#169240](https://github.com/pytorch/pytorch/pull/169240))

- Add exp support for COO on CPU, CUDA and MPS ([#166801](https://github.com/pytorch/pytorch/pull/166801))

- Remove old CUDA 11 sparse code ([#166048](https://github.com/pytorch/pytorch/pull/166048), [#164531](https://github.com/pytorch/pytorch/pull/164531), [#164199](https://github.com/pytorch/pytorch/pull/164199))

## XPU
- Support `--nproc-per-node` torchrun option for Intel GPU ([#159474](https://github.com/pytorch/pytorch/pull/159474))

- Support complex dtype of Aten operator Matmul for Intel GPU ([#160867](https://github.com/pytorch/pytorch/pull/160867))

- Add SYCL-TLA implementation for aten flash attention ([#169101](https://github.com/pytorch/pytorch/pull/169101))

# Bug Fixes
## Autograd
- Fix custom autograd Function memory leak when saving mutated view ([#164407](https://github.com/pytorch/pytorch/pull/164407))

- Fix unused gradient tracking to respect create_graph ([#168295](https://github.com/pytorch/pytorch/pull/168295))

- Fix NaN gradients in atan2_backward when both inputs are zero ([#166787](https://github.com/pytorch/pytorch/pull/166787))

- Bugfix to forward autodiff causing different datatype 2 ([#165784](https://github.com/pytorch/pytorch/pull/165784))

## Build Frontend
- Fix build targets order ([#169905](https://github.com/pytorch/pytorch/pull/169905),[#169994](https://github.com/pytorch/pytorch/pull/169994), [#164165](https://github.com/pytorch/pytorch/pull/164165))

- Do not restrict optimization flags ([#164894](https://github.com/pytorch/pytorch/pull/164894))

- Fix linking issue for Linux-aarch64 target ([#169723](https://github.com/pytorch/pytorch/pull/169723))

## C++ Frontend
- Fixed C++ extension distributed warning spew ([#162764](https://github.com/pytorch/pytorch/pull/162764))

## CPU
- Fix clang-21 warnings ([#166859](https://github.com/pytorch/pytorch/pull/166859))

## CUDA
- `torch._compile_kernel`
  - Handle python floats as double in CUDA C++ ([#162626](https://github.com/pytorch/pytorch/pull/162626))
  - Use libnvrtc.so path based on CUDA version used by torch ([#163642](https://github.com/pytorch/pytorch/pull/163642))
- Handle python floats as double in CUDA C++ ([#162626](https://github.com/pytorch/pytorch/pull/162626))
- Use libnvrtc.so path based on CUDA version used by torch ([#163642](https://github.com/pytorch/pytorch/pull/163642))

- Fix `torch.nonzero_static` crash on CUDA when the input is a empty tensor ([#162578](https://github.com/pytorch/pytorch/pull/162578))

- Fix caller source location in `C10_CUDA_CHECK` error messages ([#162808](https://github.com/pytorch/pytorch/pull/162808))

- Fix channels-last dimension mapping in CUDA `parallel_cat` ([#165023](https://github.com/pytorch/pytorch/pull/165023))

- 64-bit indexing on CUDA:
  - Fix a large tensor indexding crash ([#164049](https://github.com/pytorch/pytorch/pull/164049))
  - Handle 64-bit outer dimension in `cumsum` ([#167326](https://github.com/pytorch/pytorch/pull/167326))
  - Fix crash in `embedding_dense_backward` ([#165095](https://github.com/pytorch/pytorch/pull/165095))
  - Fix chunk-size for 64-bit indexing in fused adagrad ([#165971](https://github.com/pytorch/pytorch/pull/165971))

- Remove erroneous `const_cast` in CUDA `memcpy` call ([#168165](https://github.com/pytorch/pytorch/pull/168165))

- Handle large shared memory in `torch.cuda._compile_kernel` ([#162647](https://github.com/pytorch/pytorch/pull/162647))

- Fix `torch.unique_consecutive` crash on CUDA ([#162950](https://github.com/pytorch/pytorch/pull/162950))

- Fix correctness of `parallel_cat` ([#165446](https://github.com/pytorch/pytorch/pull/165446))

- Fix race condition and make `torch.kthvalue` deterministic on CUDA ([#165762](https://github.com/pytorch/pytorch/pull/165762))

- Fix shared memory race in `reduce_kernel` ([#162995](https://github.com/pytorch/pytorch/pull/162995))

- Fix `Tensor.__dlpack__(stream=None)` support during CUDA Graph capture ([#163242](https://github.com/pytorch/pytorch/pull/163242))

- Remove explicit casting of complex nansum during accumulation to avoid precision loss ([#165494](https://github.com/pytorch/pytorch/pull/165494))

- Disable jiterator for complex tan and tanh due to numerical issues ([#165250](https://github.com/pytorch/pytorch/pull/165250))

- Fix a few issues with `out_dtype` overload for addmm/baddbmm ([#167931](https://github.com/pytorch/pytorch/pull/167931))

- Fix safety issues when calling cuBLAS from multiple threads ([#167248](https://github.com/pytorch/pytorch/pull/167248))

## cuDNN
- Disable cuDNN for 3D convolutions with kernel size != 1 for cuDNN 9.8+ due to a numerical isssue ([#163581](https://github.com/pytorch/pytorch/pull/163581))

## Dataloader Frontend
- Fix pin memory return type when input is a tuple ([#169690](https://github.com/pytorch/pytorch/pull/169690))

## Distributed
- c10d
  - Enforced P2P tensors to be dense ([#163719](https://github.com/pytorch/pytorch/pull/163719))
  - Fixed `split_group` bug by having the parent pg option deep copied ([#167125](https://github.com/pytorch/pytorch/pull/167125))
  - Fixed `ProcessGroupNCCL` coalseced profiling ([#160680](https://github.com/pytorch/pytorch/pull/160680))

- Context Parallel
  - Fixed cuDNN Context Parallel LSE dimension bug ([#163231](https://github.com/pytorch/pytorch/pull/163231))

- DistributedDataParallel: (DDP)
  - Fixed complex datatype handling in ddp ([#166863](https://github.com/pytorch/pytorch/pull/166863))

- DistributedStateDict
  - Fixed keyerror when loading parameter with unsaved optimizer state ([#165228](https://github.com/pytorch/pytorch/pull/165228))

- DTensor
  - Fixed `foreach_max` op ([#169667](https://github.com/pytorch/pytorch/pull/169667))

- FullyShardDataParallel (FSDP1 and FSDP2)
  - Added skipping `reduce_scatter` when world size is 1 (Collectives) ([#162021](https://github.com/pytorch/pytorch/pull/162021))
  - Used grad div factor when fsdp_degree=1 ([#167178](https://github.com/pytorch/pytorch/pull/167178))

- Pipeline Parallelism:
  - Fixed FSDP unshard/reshard ([#164775](https://github.com/pytorch/pytorch/pull/164775))
  - Fixed pipeline parallelism not correctly initializing backwards stages when evaluating before training. ([#162823](https://github.com/pytorch/pytorch/pull/162823))
  - Fixed split_args_kwargs_into_chunks issues ([#165306](https://github.com/pytorch/pytorch/pull/165306))
  - Fixed edge case with FSDP when stages_per_rank > 3 ([#165467](https://github.com/pytorch/pytorch/pull/165467))

- SymmetricMemory
  - Fixed memory allocation hold-up ([#162680](https://github.com/pytorch/pytorch/pull/162680))

## Distributed Checkpointing
- Avoid multiple storage writer resets in async save ([#159448](https://github.com/pytorch/pytorch/pull/159448))

- DTensor slice dequantization with proper block alignment ([#163532](https://github.com/pytorch/pytorch/pull/163532))

- Add option to use PrefixStore to create checkpoint background process ([#166560](https://github.com/pytorch/pytorch/pull/166560))

## Dynamo
- Fixed `cProfile` usage with `torch.compile` in Python 3.12+ ([#170013](https://github.com/pytorch/pytorch/pull/170013))

- Fix memory leak in tensor subclass metadata guard ([#167352](https://github.com/pytorch/pytorch/pull/167352))

## FX
- Fix splitter for empty subgraph case ([#161716](https://github.com/pytorch/pytorch/pull/161716))

- Use tuples to have a deterministic ordering in shape prop. ([#164851](https://github.com/pytorch/pytorch/pull/164851))

## Inductor
- Fix some edge cases ([#162295](https://github.com/pytorch/pytorch/pull/162295))

- Fix TMA transpose logic to handle 1D shapes + string differences ([#163966](https://github.com/pytorch/pytorch/pull/163966))

- fix flex attention eager: dont round down scores to low-precision (closes #163588) ([#163986](https://github.com/pytorch/pytorch/pull/163986))

- Fix a condition error in torch/_inductor/codegen/debug_utils.py ([#165033](https://github.com/pytorch/pytorch/pull/165033))

- Thread deterministic config vars to subproc compilation ([#165729](https://github.com/pytorch/pytorch/pull/165729))

- Fix identity expansion. ([#165066](https://github.com/pytorch/pytorch/pull/165066))

- Fix FP8 activation quantization for duplicate forward outputs. ([#163364](https://github.com/pytorch/pytorch/pull/163364))

- Fix decomposition issues (`repeat_interleave` out-of-bounds indices, `divmod` error, `alpha`/`beta` handling). ([#165368](https://github.com/pytorch/pytorch/pull/165368)) ([#163482](https://github.com/pytorch/pytorch/pull/163482)) ([#167317](https://github.com/pytorch/pytorch/pull/167317))

- Fix dynamic shaped heads check in FlexFlash. ([#165866](https://github.com/pytorch/pytorch/pull/165866))

- Fix `argmin`/`argmax` returning incorrect indices for non-contiguous tensors. ([#165983](https://github.com/pytorch/pytorch/pull/165983))

- Fix unbacked float symbol handling in kernel codegen. ([#166890](https://github.com/pytorch/pytorch/pull/166890))

- Fix `static_input_indices` subclass remapping under training. ([#167127](https://github.com/pytorch/pytorch/pull/167127))

- Fix `torch.cond` HOP device handling in inductor. ([#167354](https://github.com/pytorch/pytorch/pull/167354))

- Fix `CppTile2DKernel` for FP8 datatype. ([#167451](https://github.com/pytorch/pytorch/pull/167451))

- Fix user-defined Triton kernel output with `.cpu()` correctness issue. ([#168281](https://github.com/pytorch/pytorch/pull/168281))

- Fix viewed outputs getting padded incorrectly. ([#163398](https://github.com/pytorch/pytorch/pull/163398))

- Fix lowering issues (`as_strided` with `.view(dtype)` inputs, symbolic shapes in FlexAttention, `sym_size_`/`sym_stride`). ([#163319](https://github.com/pytorch/pytorch/pull/163319)) ([#168383](https://github.com/pytorch/pytorch/pull/168383)) ([#167565](https://github.com/pytorch/pytorch/pull/167565))

- Fix error from custom CUDA allocators. ([#163422](https://github.com/pytorch/pytorch/pull/163422))

- Fix `copy_` for scalar in inductor. ([#164167](https://github.com/pytorch/pytorch/pull/164167))

- Fix bug with serialization after AOTAutogradCache hit. ([#165474](https://github.com/pytorch/pytorch/pull/165474))

- Fix `searchsorted` for non-dense tensors. ([#165064](https://github.com/pytorch/pytorch/pull/165064))

- Fix constant folder issues. ([#166655](https://github.com/pytorch/pytorch/pull/166655))

- Fix constant creation issues. ([#167398](https://github.com/pytorch/pytorch/pull/167398))

- Fix picking wrong contiguous node. ([#168371](https://github.com/pytorch/pytorch/pull/168371))

- Fix inner reduction decision logic. ([#168391](https://github.com/pytorch/pytorch/pull/168391))

- Fix device determination logic in Conditional. ([#169199](https://github.com/pytorch/pytorch/pull/169199))

- Fix pattern matcher `FailedMatch` format string. ([#169611](https://github.com/pytorch/pytorch/pull/169611))

- Fix SyntaxError from truncated Unicode escape in Windows compile-time auto-tuning block. ([#169286](https://github.com/pytorch/pytorch/pull/169286))

- Optimize sum reduction heuristics. ([#163144](https://github.com/pytorch/pytorch/pull/163144))

- Optimize scalar `welford_reduce`. ([#162709](https://github.com/pytorch/pytorch/pull/162709))

- Disable mixed-order reduction for cpp-wrapper. ([#169859](https://github.com/pytorch/pytorch/pull/169859))

- Capture Triton timeout errors without crashing the job. ([#169064](https://github.com/pytorch/pytorch/pull/169064))

- Correctly set `max_numwarps` in coordinate descent tuner. ([#159146](https://github.com/pytorch/pytorch/pull/159146))

- Fix Triton `group_m` config. ([#169514](https://github.com/pytorch/pytorch/pull/169514))

- Fix convolution autotune check when `groups != 1`. ([#163094](https://github.com/pytorch/pytorch/pull/163094))

- Fix constant shape for float constants. ([#164241](https://github.com/pytorch/pytorch/pull/164241))

- Fix Diode/exhaustive autotune crash on AMD. ([#169225](https://github.com/pytorch/pytorch/pull/169225))

- Fix `get_raw_stream` undefined error. ([#163707](https://github.com/pytorch/pytorch/pull/163707))

- Fix runtime error in context on cpu-only machine when compile for GPU. ([#165220](https://github.com/pytorch/pytorch/pull/165220))

- Fix AMD CPU max-autotune breakage. ([#168079](https://github.com/pytorch/pytorch/pull/168079))

- Fix bad merge duplicate pre pass. ([#165917](https://github.com/pytorch/pytorch/pull/165917))

- Fix layout constraint for `weight_norm` backward. ([#167667](https://github.com/pytorch/pytorch/pull/167667))

- Fix cross-process group overlap. ([#169384](https://github.com/pytorch/pytorch/pull/169384))

- Fix WeakDeps (WAR deps) handling during fusion. ([#162316](https://github.com/pytorch/pytorch/pull/162316))

- Fix unbacked replacement where LHS is purely backed expr and RHS is unbacked expr. ([#164013](https://github.com/pytorch/pytorch/pull/164013))

- Fix stride rounding on Blockwise128x128 to accommodate for small shapes. ([#164953](https://github.com/pytorch/pytorch/pull/164953))

- Fix loop pipelining for 2D/2D case of Triton grouped MM. ([#165265](https://github.com/pytorch/pytorch/pull/165265))

- Fix persistent rblock statically_known_leq error cases. ([#165657](https://github.com/pytorch/pytorch/pull/165657))

- Fix bugs in emulate_precision_casts ([#163520](https://github.com/pytorch/pytorch/pull/163520))

- Support python slicing with tensor inputs. ([#165074](https://github.com/pytorch/pytorch/pull/165074))

## Ahead-Of-Time Inductor (AOTI)
- Bugfix for doing negative padding ([#161639](https://github.com/pytorch/pytorch/pull/161639))

- Fix unbounded number of substitutions when equality checks contain Max expr ([#163685](https://github.com/pytorch/pytorch/pull/163685))

- Use atomic API when trying to apply size hints to input tensor strides. ([#163660](https://github.com/pytorch/pytorch/pull/163660))

- Fix a mixed-device bug for scatter_add ([#167341](https://github.com/pytorch/pytorch/pull/167341))

- Fix a small buffer mutation issue ([#169347](https://github.com/pytorch/pytorch/pull/169347))

- Fix `aot_compile` typing. ([#168320](https://github.com/pytorch/pytorch/pull/168320))

## MPS
- Fix empty tensors handling for `median`/`nanmedian`/`mv`, `dot` ([#162846](https://github.com/pytorch/pytorch/pull/162846), [#166561](https://github.com/pytorch/pytorch/pull/166561)), [#165237](https://github.com/pytorch/pytorch/pull/165237))

- Fix dlpack exports/imports of sliced tensors ([#169272](https://github.com/pytorch/pytorch/pull/169272))

- Fix large tensors silent correctness for `fill` and `cat` operation ([#164108](https://github.com/pytorch/pytorch/pull/164108), [#165373](https://github.com/pytorch/pytorch/pull/165373), [#166556](https://github.com/pytorch/pytorch/pull/166556), [#164416](https://github.com/pytorch/pytorch/pull/164416))

- `torch.compile` bugfixes ([#169648](https://github.com/pytorch/pytorch/pull/169648), [#163021](https://github.com/pytorch/pytorch/pull/163021), [#162776](https://github.com/pytorch/pytorch/pull/162776), [#163452](https://github.com/pytorch/pytorch/pull/163452))

- Silent correctness/input validation fixes ([#163036](https://github.com/pytorch/pytorch/pull/163036), ([#165254](https://github.com/pytorch/pytorch/pull/165254), ([#165267](https://github.com/pytorch/pytorch/pull/165267), ([#167777](https://github.com/pytorch/pytorch/pull/167777), ([#165058](https://github.com/pytorch/pytorch/pull/165058), ([#167961](https://github.com/pytorch/pytorch/pull/167961), ([#169261](https://github.com/pytorch/pytorch/pull/169261), ([#165871](https://github.com/pytorch/pytorch/pull/165871), ([#163507](https://github.com/pytorch/pytorch/pull/163507), ([#168332](https://github.com/pytorch/pytorch/pull/168332))

## Nested Tensor (NJT)
- Fixed NJT min / max operations on integer dtypes ([#162273](https://github.com/pytorch/pytorch/pull/162273))

## torch.nn
- Fix silent correctness when backpropagating to `score_mod` in `nn.functional.flex_attention` ([#163677](https://github.com/pytorch/pytorch/pull/163677))

- Fix bug in `nn.Module.load_state_dict` for singleton tensor ([#166335](https://github.com/pytorch/pytorch/pull/166335))

## ONNX
- Native ONNX ops (`torch.onnx.ops`)
- Fix rotary_embedding_23 implementation ([#162865](https://github.com/pytorch/pytorch/pull/162865))
- Create fake implementations for onnx ops; fix boolean mask in attention ([#165780](https://github.com/pytorch/pytorch/pull/165780))

- Fix onnx export on big endian machines ([#167816](https://github.com/pytorch/pytorch/pull/167816))

## Optimizer
- Fix `SWALR.state_dict` and `load_state_dict` to serialize properly with `weights_only=True` ([#163122](https://github.com/pytorch/pytorch/pull/163122))

- Prevent problematic tensor aliasing in LRScheduler ([#163098](https://github.com/pytorch/pytorch/pull/163098), [#163120](https://github.com/pytorch/pytorch/pull/163120))

- Fix `LBFGS` wolfe max iteration ([#161488](https://github.com/pytorch/pytorch/pull/161488))

## Profiler
- Fix `ProfilerState` typo ('Disable' → 'Disabled') and expose `PRIVATEUSE1` in `ActiveProfilerType` ([#169166](https://github.com/pytorch/pytorch/pull/169166))

## ROCm
- Fix hardsigmoid op ([#162758](https://github.com/pytorch/pytorch/pull/162758))

- Fix GEMM carveout feature ([#164303](https://github.com/pytorch/pytorch/pull/164303))

- Disable `__builtin_amdgcn_rcpf` for gfx90a ([#166454](https://github.com/pytorch/pytorch/pull/166454))

- ROCm 7.0 BC-breaking preparations in JIT support ([#160587](https://github.com/pytorch/pytorch/pull/160587), [#166147](https://github.com/pytorch/pytorch/pull/166147))

## Sparse Frontend
- Fix mul(COO, COO) on MPS for hybrid COO variants ([#166164](https://github.com/pytorch/pytorch/pull/166164))

- Update torch.sparse_coo_tensor error message to include more information about input tensor properties ([#161900](https://github.com/pytorch/pytorch/pull/161900))

- Fix GradTrackingTensor sparse layout propagation ([#165765](https://github.com/pytorch/pytorch/pull/165765))

## XPU
- Fix OneDNN deconvolution with `output_padding` on Intel GPU ([#169176](https://github.com/pytorch/pytorch/pull/169176))

- Fix conv1d precision error on Intel GPU ([#162944](https://github.com/pytorch/pytorch/pull/162944))

- Fix incorrect FLOPs counting of `convolution_overrideable` on Intel GPU([#166839](https://github.com/pytorch/pytorch/pull/166839))

- Fix performance drop in AOTI on Intel GPU ([#163315](https://github.com/pytorch/pytorch/pull/163315))

# Performance
## Benchmark
- Add attention benchmarking numbers to pytorch operator microbenchmarks ([#164155](https://github.com/pytorch/pytorch/pull/164155))

## CPU (AArch64)
- Improved aarch64 performance with optimizations for type conversions (bfloat16, FP16, bool), erf function, and autovectorization enhancements ([#166049](https://github.com/pytorch/pytorch/pull/166049), [#166262](https://github.com/pytorch/pytorch/pull/166262), [#166306](https://github.com/pytorch/pytorch/pull/166306), [#166330](https://github.com/pytorch/pytorch/pull/166330), [#166594](https://github.com/pytorch/pytorch/pull/166594), [#166641](https://github.com/pytorch/pytorch/pull/166641), [#166739](https://github.com/pytorch/pytorch/pull/166739), [#166880](https://github.com/pytorch/pytorch/pull/166880), [#166958](https://github.com/pytorch/pytorch/pull/166958))

## CUDA
- Integrate NVIDIA cuSolver backend into ATen/Linalg (initial implementation for eig/eigval) ([#166715](https://github.com/pytorch/pytorch/pull/166715))

- Reduce register pressure in `radix_sort_pairs` to improve torch.sort performance ([#167094](https://github.com/pytorch/pytorch/pull/167094))

- Add Flash Attention 4 to sdpa ([#167348](https://github.com/pytorch/pytorch/pull/167348))

- Vectorize stores in cat for all dtypes on CUDA ([#162440](https://github.com/pytorch/pytorch/pull/162440))

- Expose `pinned_reserve_segment_size_mb` to speed up pinned memory allocation ([#164501](https://github.com/pytorch/pytorch/pull/164501))

- torch.topk: refactor global histogram/cumsum into a dedicated kernel to improve performance on CUDA ([#164459](https://github.com/pytorch/pytorch/pull/164459))

- Vectorize 8 elements on 16=bit data types for sum/mean to improve performance ([#165055](https://github.com/pytorch/pytorch/pull/165055))

- Switch order of blocked reduce when vectorize loads to improve performance ([#165178](https://github.com/pytorch/pytorch/pull/165178))

- Reduce register pressure to improve `torch.EmbeddingBag` performance ([#167834](https://github.com/pytorch/pytorch/pull/167834))

- Make clamp kernel branchless to improve performance ([#167889](https://github.com/pytorch/pytorch/pull/167889))

## cuDNN
- Reenable cuDNN for 64-bit depthwise convolutions ([#168364](https://github.com/pytorch/pytorch/pull/168364))

## Distributed Checkpointing
- Add timeout for checkpoint background process join ([#162828](https://github.com/pytorch/pytorch/pull/162828))

- Disable GC in process based async checkpointing ([#169613](https://github.com/pytorch/pytorch/pull/169613))

- Optimize global save-plan validation ([#166820](https://github.com/pytorch/pytorch/pull/166820))

- state dict staging fixes ([#166025](https://github.com/pytorch/pytorch/pull/166025))

## Dynamo
- Faster tracing of some pytree functions ([#168342](https://github.com/pytorch/pytorch/pull/168342))

## FX
- Move Node._prepend/Node._remove_from_list to C++ ([#165882](https://github.com/pytorch/pytorch/pull/165882))

- Optimize torch.fx.Node.replace_all_uses_with ([#165889](https://github.com/pytorch/pytorch/pull/165889))

## Inductor
- Naive foreach autotune support ([#162053](https://github.com/pytorch/pytorch/pull/162053))

- Invert unary read and write for better fusion. ([#161404](https://github.com/pytorch/pytorch/pull/161404))

- Generate fused RMS/layer norm backward. ([#165370](https://github.com/pytorch/pytorch/pull/165370))

- Optimize cold compile time when cudagraphs-partition is enabled. ([#167132](https://github.com/pytorch/pytorch/pull/167132))

- Reduce cold compilation time caused by duplicated user-defined Triton kernels. ([#168292](https://github.com/pytorch/pytorch/pull/168292))

- Optimize identity permute in `empty_permuted` decomposition. ([#169731](https://github.com/pytorch/pytorch/pull/169731))

- Properly enlarge XBLOCK/set num_warps=1 for B200 inner persistent reductions. ([#168335](https://github.com/pytorch/pytorch/pull/168335))

- Improved heuristic for operator reordering for peak memory. ([#161810](https://github.com/pytorch/pytorch/pull/161810))

- Add more configs for pointwise kernels on ROCm. ([#166470](https://github.com/pytorch/pytorch/pull/166470))

- Improve A16W8 performance for CPU GEMM template. ([#162479](https://github.com/pytorch/pytorch/pull/162479))

- Make mix-order-reduction split size not depends on split-reduction heuristics ([#166461](https://github.com/pytorch/pytorch/pull/166461))

- Less aggressive persistent reduction when it could induce large masking with dynamic shapes. ([#163365](https://github.com/pytorch/pytorch/pull/163365))

- Improve FlexAttention backward configs for B200  ([#163318](https://github.com/pytorch/pytorch/pull/163318))

## Quantization
- Make prepare and convert faster by caching ([#162550](https://github.com/pytorch/pytorch/pull/162550))

- Add onednn context cache for CPU qlinear to improve performance ([#168150](https://github.com/pytorch/pytorch/pull/168150))

## Release Engineering
- Add operator microbenchmarks for attention, convolution, and optimizer operations to CI ([#165915](https://github.com/pytorch/pytorch/pull/165915), [#166331](https://github.com/pytorch/pytorch/pull/166331), [#168101](https://github.com/pytorch/pytorch/pull/168101))

- Add HuggingFace LLM benchmarks and cleanup benchmark model configurations ([#156967](https://github.com/pytorch/pytorch/pull/156967), [#164815](https://github.com/pytorch/pytorch/pull/164815), [#164816](https://github.com/pytorch/pytorch/pull/164816))

## ROCm
- Use hipSolver instead of MAGMA for Cholesky ([#163977](https://github.com/pytorch/pytorch/pull/163977))

- Layer norm now uses __builtin_amdgcn_rcpf(x) instead of 1.f/x ([#165589](https://github.com/pytorch/pytorch/pull/165589))

- OffsetCalc Unroll Optimization ([#161700](https://github.com/pytorch/pytorch/pull/161700))

- Improve perf for elementwise broadcast with mixed dtype ([#163562](https://github.com/pytorch/pytorch/pull/163562))

- Implement float32 copy kernel ([#163869](https://github.com/pytorch/pytorch/pull/163869))

- Improve non stride-one backwards indexing for small index sets ([#164409](https://github.com/pytorch/pytorch/pull/164409))

- Adjust grid size for non-unit stride backwards indexing ([#165026](https://github.com/pytorch/pytorch/pull/165026))

- Normalization update to block size ([#165941](https://github.com/pytorch/pytorch/pull/165941))

- Deserialize loads in planer sum portion of reduce() of norm. ([#165927](https://github.com/pytorch/pytorch/pull/165927))

- Deserialize loads in planer sum portion of stats() of norm ([#166021](https://github.com/pytorch/pytorch/pull/166021))

- Specialized binary elementwise broadcast kernel for mixed dtypes with float/bfloat16/half ([#167233](https://github.com/pytorch/pytorch/pull/167233))

- Roll kernel as grid stride loop ([#169474](https://github.com/pytorch/pytorch/pull/169474))

- Inductor performance improvements via configs, heurstics, and/or codegen ([#163908](https://github.com/pytorch/pytorch/pull/163908), [#161280](https://github.com/pytorch/pytorch/pull/161280), [#166470](https://github.com/pytorch/pytorch/pull/166470), [#162052](https://github.com/pytorch/pytorch/pull/162052), [#163197](https://github.com/pytorch/pytorch/pull/163197))

## torch.func
- 20x less memory use and 37.25% speedup in min_cut_rematerialization_partition when using the new dp knapsack solver, compared to existing default one (dp) ([#160914](https://github.com/pytorch/pytorch/pull/160914))

# Documentation
## Autograd
- Add `inference_mode` hint message to use `eval` with inference. ([#163619](https://github.com/pytorch/pytorch/pull/163619))

## CUDA
- Add Documentation for Device APIs ([#162834](https://github.com/pytorch/pytorch/pull/162834))

- Adding aliases for CUDA and XPU API documentation ([#162984](https://github.com/pytorch/pytorch/pull/162984))

- Clarify safety of CUDA graph memory pool sharing across graphs in documentation ([#166975](https://github.com/pytorch/pytorch/pull/166975))

## Distributed
- c10d
  - Complete documentations for all distributed c10d apis ([#165194](https://github.com/pytorch/pytorch/pull/165194))

## Dynamo
- Updated documentation for `tlparse` ([#171339](https://github.com/pytorch/pytorch/pull/171339)).
`tlparse` is a compilation report tool that processes `TORCH_TRACE` logs to generate interactive HTML reports showing how your model was compiled.
When reporting bugs to PyTorch developers, we encourage you to attach the trace log or `tlparse` output to provide critical debugging information to help us bisect the issue.

## FX
- Add docs for torch.fx.experimental.unification ([#167334](https://github.com/pytorch/pytorch/pull/167334))

- Fix the split_module tutorial code ([#166154](https://github.com/pytorch/pytorch/pull/166154))

## Inductor
- Updated documentation for `tlparse` ([#171339](https://github.com/pytorch/pytorch/pull/171339))  ([#162975](https://github.com/pytorch/pytorch/pull/162975)). `tlparse` is a compilation report tool that processes `TORCH_TRACE` logs to generate interactive HTML reports showing how your model was compiled. When reporting bugs to PyTorch developers, we encourage you to  attach the trace log or `tlparse` output to provide critical debugging information to help us bisect the issue.

- Update FlexConfig documentation. ([#162533](https://github.com/pytorch/pytorch/pull/162533))

## Ahead-Of-Time Inductor (AOTI)
- [AOTI] Update AOTInductor tutorial ([#163808](https://github.com/pytorch/pytorch/pull/163808))

## torch.nn
- Update CTCLoss docs float32 input required for CuDNN ([#162042](https://github.com/pytorch/pytorch/pull/162042))

- Update LPPool docs to clarify ceil_mode padding semantics when ceil_mode=True ([#163186](https://github.com/pytorch/pytorch/pull/163186))

## ONNX
- Update export docstring ([#162622](https://github.com/pytorch/pytorch/pull/162622))

- Fix incorrect attention example in ONNX exporter docstring ([#167646](https://github.com/pytorch/pytorch/pull/167646))

## Profiler
- Add documentation for `FunctionEvent` ([#167688](https://github.com/pytorch/pytorch/pull/167688))

## Quantization
- Document some quantization public apis ([#165160](https://github.com/pytorch/pytorch/pull/165160))

- Add missing method docstrings for pytorch quantization classes ([#165199](https://github.com/pytorch/pytorch/pull/165199))

## XPU
- Add new supported client GPU Panther Lake in "Get Started with XPU" page ([#170517](https://github.com/pytorch/pytorch/pull/170517))

# Security
# Developers
## Composability
- Removed guard_size_oblivious from internal code, replacing most usages with guard_if_{false|true}. Both APIs are used in framework code that gets traced through to make it more friendly to unbacked symints, but the new APIs are more intuitive ([#164664](https://github.com/pytorch/pytorch/pull/164664), [#164665](https://github.com/pytorch/pytorch/pull/164665), [#167232](https://github.com/pytorch/pytorch/pull/167232))

## Distributed
- c10d
  - Added TCPStore based debug page and fr trace analysis with py-spy support ([#169095](https://github.com/pytorch/pytorch/pull/169095), [#169144](https://github.com/pytorch/pytorch/pull/169144), [#169147](https://github.com/pytorch/pytorch/pull/169147), [#167871](https://github.com/pytorch/pytorch/pull/167871))
  - Modernized c10d code base with python code older than 3.10 removed ([#163613](https://github.com/pytorch/pytorch/pull/163613), [#163456](https://github.com/pytorch/pytorch/pull/163456), [#163440](https://github.com/pytorch/pytorch/pull/163440), [#167173](https://github.com/pytorch/pytorch/pull/167173))
  - Enabled FlightRecorder for torchft with dynamic dumping path and a reset API ([#164752](https://github.com/pytorch/pytorch/pull/164752), [#164988](https://github.com/pytorch/pytorch/pull/164988), [#164591](https://github.com/pytorch/pytorch/pull/164591), [#165639](https://github.com/pytorch/pytorch/pull/165639), [#166970](https://github.com/pytorch/pytorch/pull/166970),[#166182](https://github.com/pytorch/pytorch/pull/166182))
  - Improvement to FakeProcessGroup: direct construction error and error out if comms are invoked ([#162841](https://github.com/pytorch/pytorch/pull/162841), [#163665](https://github.com/pytorch/pytorch/pull/163665))

- DTensor
  - Added guide for what to do about mixed torch.Tensor and DTensor operations ([#162651](https://github.com/pytorch/pytorch/pull/162651))
  - Raised an RuntimeError when checkpointing APIs are used with Partial placement ([#163941](https://github.com/pytorch/pytorch/pull/163941))

- torchelastic
  - Added missing `signals_to_handle` to launcher logging ([#166631](https://github.com/pytorch/pytorch/pull/166631))
  - Added logging exit code for failures to ease debugging ([#160907](https://github.com/pytorch/pytorch/pull/160907))

## FX
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

## Inductor
- Add API for scheduling overlap from inductor configs. ([#169693](https://github.com/pytorch/pytorch/pull/169693))

- Make `LOCK_TIMEOUT` in codecache configurable. ([#165030](https://github.com/pytorch/pytorch/pull/165030))

- Add debug output for specific pattern matching. ([#169603](https://github.com/pytorch/pytorch/pull/169603))

- Add overridable env var for disabling FX graph cache. ([#166138](https://github.com/pytorch/pytorch/pull/166138))

- Add subsystem support to pattern matcher. ([#163922](https://github.com/pytorch/pytorch/pull/163922))

- Add pre-grad graph bisecting support. ([#166344](https://github.com/pytorch/pytorch/pull/166344))

- Decouple flags for optimization and debug symbols. ([#167385](https://github.com/pytorch/pytorch/pull/167385)) ([#167575](https://github.com/pytorch/pytorch/pull/167575))

- Introduce HOP for inductor compiled regions to allow torch dispatch. ([#167844](https://github.com/pytorch/pytorch/pull/167844))

- Record triton kernels, run-to-run determinism checks ([#167028](https://github.com/pytorch/pytorch/pull/167028))

## Release Engineering
- Migrate from setup.py to modern Python build tools (pip install and python -m build) ([#156711](https://github.com/pytorch/pytorch/pull/156711), [#156712](https://github.com/pytorch/pytorch/pull/156712))

## ROCm
- Add Rocm to Operator Microbenchmark CI ([#164173](https://github.com/pytorch/pytorch/pull/164173))

- Enable TD for all ROCm default and distributed config workflows ([#168225](https://github.com/pytorch/pytorch/pull/168225))

- Expand trunk.yml coverage for ROCm ([#168162](https://github.com/pytorch/pytorch/pull/168162))

- cudagraph trees ut fixes ([#163592](https://github.com/pytorch/pytorch/pull/163592))

- test_convolution.py uses miopen immediate mode ([#164598](https://github.com/pytorch/pytorch/pull/164598))

- Keep amdgpu-coerce-illegal-types flag if rocm version is less than 7.2 ([#165789](https://github.com/pytorch/pytorch/pull/165789))

- Use a ROCm version string without hash. ([#166336](https://github.com/pytorch/pytorch/pull/166336))

- Dynamo benchmarks: remove outdated flaky models and enable deterministic algorithms ([#169024](https://github.com/pytorch/pytorch/pull/169024))

## XPU
- Upgrade Intel GPU software stack package to intel-deep-learning-essentials-2025.3 ([#166829](https://github.com/pytorch/pytorch/pull/166829))

