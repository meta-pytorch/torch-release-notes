# PyTorch 2.8.0 Release Notes
- [Highlights](#highlights)
- [Backwards Incompatible Changes](#backwards-incompatible-changes)
- [Deprecations](#deprecations)
- [New Features](#new-features)
- [Improvements](#improvements)
- [Bug fixes](#bug-fixes)
- [Performance](#performance)
- [Documentation](#documentation)
- [Developers](#developers)


# Highlights
<table>
  <tr>
   <td><strong>Stable</strong>
   </td>
   <td><strong>Unstable</strong>
   </td>
  </tr>
  <tr>
   <td>TODO
   </td>
   <td>TODO
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>torch::stable::Tensor
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>Hierarchical compilation with torch.compile
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>Support for Intel GPU distributed backend (XCCL)
   </td>
  </tr>
</table>

For more details about these highlighted features, you can look at the release blogpost.
Below are the full release notes for this release.

# Tracked Regressions
### Windows wheel builds with CUDA 12.9.1 stack overflow during build ([#156181](https://github.com/pytorch/pytorch/issues/156181))
Due to a bug introduced in CUDA 12.9.1, we are unable to complete full Windows wheel builds with this
version, as compilation of `torch.segment_reduce()` crashes the build. Thus, we provide a wheel
without `torch.segment_reduce()` included in order to sidestep the issue. If you need support
for `torch.segment_reduce()`, please utilize a different version.

# Backwards Incompatible Changes

## CUDA Support
### Removed support for Maxwell, Pascal, and Volta architectures with CUDA 12.8 and 12.9 builds ([#157517](https://github.com/pytorch/pytorch/issues/157517), [#158478](https://github.com/pytorch/pytorch/pull/158478), [#158744](https://github.com/pytorch/pytorch/pull/158744))
Due to binary size limitations, support for sm50 - sm70 architectures with CUDA 12.8 and 12.9 has
been dropped for the 2.8.0 release. If you need support for these architectures, please utilize
CUDA 12.6 instead.

## Python Frontend
### Calling an op with an input dtype that is unsupported now raises `NotImplementedError` instead of `RuntimeError` ([#155470](https://github.com/pytorch/pytorch/pull/155470))
Please update exception handling logic to reflect this.

In 2.7.0
```
try:
    torch.nn.Hardshrink()(torch.randint(0, 5, (10,)))
except RuntimeError:
    ...
```

In 2.8.0
```
try:
    torch.nn.Hardshrink()(torch.randint(0, 5, (10,)))
except NotImplementedError:
    ...
```

### Added missing in-place on view check to custom `autograd.Function` ([#153094](https://github.com/pytorch/pytorch/pull/153094))

In 2.8.0, if a custom `autograd.Function` mutates a view of a leaf requiring grad,
it now properly raises an error. Previously, it would silently leak memory.
```
   class Func(torch.autograd.Function):
        @staticmethod
        def forward(ctx, inp):
            inp.add_(1)
            ctx.mark_dirty(inp)
            return inp

        @staticmethod
        def backward(ctx, gO):
            pass

    a = torch.tensor([1.0, 2.0], requires_grad=True)
    b = a.view_as(a)
    Func.apply(b)
```
Output:

Version 2.7.0
```
Runs without error, but leaks memory
```
Version 2.8.0
```
RuntimeError: a view of a leaf Variable that requires grad is being used in an in-place operation
```

### An error is now properly thrown for the out variant of `tensordot` when called with a `requires_grad=True` tensor ([#150270](https://github.com/pytorch/pytorch/pull/150270))

Please avoid passing an out tensor with `requires_grad=True` as gradients cannot be
computed for this tensor.

In 2.7.0
```
a = torch.empty((4, 2), requires_grad=True)
b = torch.empty((2, 4), requires_grad=True)
c = torch.empty((2, 2), requires_grad=True)
# does not error, but gradients for c cannot be computed
torch.tensordot(a, b, dims=([1], [0]), out=c)
```

In 2.8.0
```
a = torch.empty((4, 2), requires_grad=True)
b = torch.empty((2, 4), requires_grad=True)
c = torch.empty((2, 2), requires_grad=True)
torch.tensordot(a, b, dims=([1], [0]), out=c)
# RuntimeError: tensordot(): the 'out' tensor was specified and requires gradients, and
# its shape does not match the expected result. Either remove the 'out' argument, ensure
# it does not require gradients, or make sure its shape matches the expected output.
```

## torch.compile
### Specialization of a tensor shape with `mark_dynamic` applied now correctly errors ([#152661](https://github.com/pytorch/pytorch/pull/152661))

Prior to 2.8, it was possible for a guard on a symbolic shape to be incorrectly
omitted if the symbolic shape evaluation was previously tested with guards
suppressed (this often happens within the compiler itself). This has been fixed
in 2.8 and usually will just silently "do the right thing" and add the correct
guard. However, if the new guard causes a tensor marked with `mark_dynamic` to become
specialized, this can result in an error. One workaround is to use
`maybe_mark_dynamic` instead of `mark_dynamic`.

See the discussion in issue [#157921](https://github.com/pytorch/pytorch/issues/157921) for more
context.

Version 2.7.0
```python
import torch

embed = torch.randn(2, 8192)
x = torch.zeros(8192)

torch._dynamo.mark_dynamic(x, 0)

@torch.compile
def f(embedding_indices, x):
    added_tokens_mask = torch.where(x > 10000, 1, 0)
    ei = torch.narrow(embedding_indices, 1, 0, x.size(0))
    return ei.clone()

f(embed, x)
```

Version 2.8.0
```python
import torch

embed = torch.randn(2, 8192)
x = torch.zeros(8192)

torch._dynamo.maybe_mark_dynamic(x, 0)

@torch.compile
def f(embedding_indices, x):
    added_tokens_mask = torch.where(x > 10000, 1, 0)
    ei = torch.narrow(embedding_indices, 1, 0, x.size(0))
    return ei.clone()

f(embed, x)
```

### Several config variables related to `torch.compile` have been renamed or removed
- Dynamo config variable `enable_cpp_framelocals_guard_eval` has changed to no longer have any effect ([#151008](https://github.com/pytorch/pytorch/pull/151008)).
- Inductor config variable `rocm.n_max_profiling_configs` is deprecated ([#152341](https://github.com/pytorch/pytorch/pull/152341)).
Instead, use ck-tile based configs `rocm.ck_max_profiling_configs` and
`rocm.ck_tile_max_profiling_configs`.
- Inductor config variable `autotune_fallback_to_aten` is deprecated ([#154331](https://github.com/pytorch/pytorch/pull/154331)).
Inductor will no longer silently fall back to `ATen`. Please add `"ATEN"` to
`max_autotune_gemm_backends` for the old behavior.
- Inductor config variables `use_mixed_mm` and `mixed_mm_choice` are deprecated ([#152071](https://github.com/pytorch/pytorch/pull/152071)). Inductor now supports prologue fusion, so there is no need for
special cases now.
- Inductor config setting `descriptive_names = False` is deprecated ([#151481](https://github.com/pytorch/pytorch/pull/151481)). Please use one of the other available
options: `"torch"`, `"original_aten"`, or `"inductor_node"`.
- `custom_op_default_layout_constraint` has moved from inductor config to functorch config ([#148104](https://github.com/pytorch/pytorch/pull/148104)). Please reference it via
`torch._functorch.config.custom_op_default_layout_constraint` instead of
`torch._inductor.config.custom_op_default_layout_constraint`.
- AOTI config variable `emit_current_arch_binary` is deprecated ([#155768](https://github.com/pytorch/pytorch/pull/155768)).
- AOTI config variable `aot_inductor.embed_cubin` has been renamed to `aot_inductor.embed_kernel_binary` ([#154412](https://github.com/pytorch/pytorch/pull/154412)).
- AOTI config variable `aot_inductor.compile_wrapper_with_O0` has been renamed to `compile_wrapper_opt_level` ([#148714](https://github.com/pytorch/pytorch/pull/148714)).

### Added a stricter aliasing/mutation check for `HigherOrderOperator`s (e.g. `cond`), which will explicitly error out if alias/mutation among inputs and outputs is unsupported ([#148953](https://github.com/pytorch/pytorch/pull/148953), [#146658](https://github.com/pytorch/pytorch/pull/146658)).

For affected `HigherOrderOperator`s, add `.clone()` to aliased outputs to address this.

Version 2.7.0
```python
import torch

@torch.compile(backend="eager")
def fn(x):
    return torch.cond(x.sum() > 0, lambda x: x, lambda x: x + 1, [x])

fn(torch.ones(3))
```

Version 2.8.0
```python
import torch

@torch.compile(backend="eager")
def fn(x):
    return torch.cond(x.sum() > 0, lambda x: x.clone(), lambda x: x + 1, [x])

fn(torch.ones(3))
```

### `guard_or_x` and `definitely_x` have been consolidated ([#152463](https://github.com/pytorch/pytorch/pull/152463))
We removed `definitely_true` / `definitely_false` and associated APIs, replacing them with
`guard_or_true` / `guard_or_false`, which offer similar functionality and can be used to
achieve the same effect. Please migrate to the latter.

Version 2.7.0
```python
from torch.fx.experimental.symbolic_shapes import definitely_false, definitely_true

...
if definitely_true(x):
  ...

if definitely_false(y):
  ...
```

Version 2.8.0
```python
from torch.fx.experimental.symbolic_shapes import guard_or_false, guard_or_true

...
if guard_or_false(x):
  ...

# alternatively: if guard_or_false(torch.sym_not(y))
if not guard_or_true(y):
  ...
```

## torch.export
### `torch.export.export_for_inference` has been removed in favor of `torch.export.export_for_training().run_decompositions()` ([#149078](https://github.com/pytorch/pytorch/pull/149078))

Version 2.7.0
```python
import torch

...
exported_program = torch.export.export_for_inference(mod, args, kwargs)
```

Version 2.8.0
```python
import torch

...
exported_program = torch.export.export_for_training(
    mod, args, kwargs
).run_decompositions(decomp_table=decomp_table)
```

### Switched default to `strict=False` in `torch.export.export` and `export_for_training` ([#148790](https://github.com/pytorch/pytorch/pull/148790), [#150941](https://github.com/pytorch/pytorch/pull/150941))

This differs from the previous release default of `strict=True`. To revert to the old default
behavior, please explicitly pass `strict=True`.

Version 2.7.0
```python
import torch

# default behavior is strict=True
torch.export.export(...)
torch.export.export_for_training(...)
```

Version 2.8.0
```python
import torch

# strict=True must be explicitly passed to get the old behavior
torch.export.export(..., strict=True)
torch.export.export_for_training(..., strict=True)
```

## Build Frontend
### Removed the `torch/types.h` include from `Dispatcher.h` ([#149557](https://github.com/pytorch/pytorch/pull/149557))
This can cause build errors in C++ code that implicitly relies on this include (e.g. very old versions of `torchvision`).

Note that `Dispatcher.h` does not belong as an include from `torch/types.h` and was only present as a
short-term hack to appease `torchvision`. If you run into `torchvision` build errors, please
update to a more recent version of `torchvision` to resolve this.

### Upgraded `DLPack` to 1.0 ([#145000](https://github.com/pytorch/pytorch/pull/145000))
As part of the upgrade, some of the `DLDeviceType` enum values have been renamed. Please switch
to the new names.

Version 2.7.0
```
from torch.utils.dlpack import DLDeviceType

d1 = DLDeviceType.kDLGPU
d2 = DLDeviceType.kDLCPUPinned
...
```

Version 2.8.0
```
from torch.utils.dlpack import DLDeviceType

d1 = DLDeviceType.kDLCUDA  # formerly kDLGPU
d2 = DLDeviceType.kDLCUDAHost  # formerly kDLCPUPinned
...
```

### NVTX3 code has been moved from `cmake/public/cuda.cmake` to `cmake/Dependencies.cmake` ([#151583](https://github.com/pytorch/pytorch/pull/151583))

This is a BC-breaking change for the build system interface. Downstream projects that previously got NVTX3 through `cmake/public/cuda.cmake`
(i.e.. calling `find_package(TORCH REQUIRED)`) will now need to explicitly configure NVTX3 support in the library itself (i.e. use `USE_SYSTEM_NVTX=1`).
The change is to fix the broken behavior where downstream projects couldn't find NVTX3 anyway due to the `PROJECT_SOURCE_DIR` mismatch.

Version 2.7.0:
- A downstream project using `-DUSE_SYSTEM_NVTX` would be able to find NVTX3 and `torch::nvtx3` via PyTorch's `cmake/public/cuda.cmake` logic.
- A downstream project NOT using `-DUSE_SYSTEM_NVTX` would encounter build errors with CUDA 12.8 or above.

Version 2.8.0:
- A downstream project using `-DUSE_SYSTEM_NVTX` will not be able to find NVTX3 or `torch::nvtx3` via PyTorch's `cmake/public/cuda.cmake`. The downstream project now needs to explicitly find NVTX3 and torch::nvtx3 by implementing the same logic in PyTorch's `cmake/Dependences.cmake`.
- A downstream project NOT using `-DUSE_SYSTEM_NVTX` will proceed building without NVTX unless another part of the build process re-enables NVTX.

# Deprecations
### MPS support for MacOS Ventura will be removed in 2.9
PyTorch 2.8 is the last release that will support GPU acceleration on MacOS Ventura. In the next
release (2.9), MacOS Sonoma (released in Sept. 2023) or above will be required to use the MPS
backend.

### `torch.ao.quantization` is deprecated and will be removed in 2.10 ([#153892](https://github.com/pytorch/pytorch/pull/153892))
To migrate:
- Eager mode quantization (`torch.ao.quantization.quantize`, `torch.ao.quantization.quantize_dynamic`)
  - Weight-only and dynamic quantization: use `torchao` eager mode `quantize_`.
  - Static quantization: use `torchao` PT2E quantization.
- FX graph mode quantization (`torch.ao.quantization.quantize_fx.prepare_fx`, `torch.ao.quantization.quantize_fx.convert_fx`): use `torchao` PT2E quantization (`torchao.quantization.quantize_pt2e.prepare_pt2e`, `torchao.quantization.quantize_pt2e.convert_pt2e`).

Note that PT2E quantization has been migrated to `torchao` (https://github.com/pytorch/ao/tree/main/torchao/quantization/pt2e). See https://github.com/pytorch/ao/issues/2259 and https://docs.pytorch.org/ao/main/quick_start.html#pytorch-2-export-quantization for more details.

# New Features
## CUDA
- Support capture of event record and wait in CUDAGraphs for timing ([#155372](https://github.com/pytorch/pytorch/pull/155372))

## torch.compile
#### Dynamo
- Added support for hierarchical compilation via `nested_compile_region` ([#156449](https://github.com/pytorch/pytorch/pull/156449))
- Allow guards to be dropped with custom filter functions via `guard_filter_fn` ([#150936](https://github.com/pytorch/pytorch/pull/150936))
- Added `dont_skip_tracing` decorator to skip over most Dynamo `skipfiles` rules ([#150586](https://github.com/pytorch/pytorch/pull/150586))

#### Inductor
- Added support for mapping a Dynamo graph to multiple different Inductor graphs, which can be optimized separately ([#147648](https://github.com/pytorch/pytorch/pull/147648), [#147038](https://github.com/pytorch/pytorch/pull/147038))

## torch.export
- Introduced [`draft-export`](https://docs.pytorch.org/docs/main/export/draft_export.html), an export variant designed to consistently produce a graph and generate a debugging report of issues encountered during tracing ([#152637](https://github.com/pytorch/pytorch/pull/152637), [#153219](https://github.com/pytorch/pytorch/pull/153219), [#149465](https://github.com/pytorch/pytorch/pull/149465), [#153627](https://github.com/pytorch/pytorch/pull/153627), [#154190](https://github.com/pytorch/pytorch/pull/154190), [#155744](https://github.com/pytorch/pytorch/pull/155744), [#150876](https://github.com/pytorch/pytorch/pull/150876), [#150948](https://github.com/pytorch/pytorch/pull/150948), [#151051](https://github.com/pytorch/pytorch/pull/151051), [#151065](https://github.com/pytorch/pytorch/pull/151065), [#150809](https://github.com/pytorch/pytorch/pull/150809), [#151797](https://github.com/pytorch/pytorch/pull/151797))

## Ahead-Of-Time Inductor (AOTI)
- Added support for `TorchBind` objects ([#150196](https://github.com/pytorch/pytorch/pull/150196), [#154265](https://github.com/pytorch/pytorch/pull/154265))
- Added config variable `aot_inductor.model_name_for_generated_files` for specifying model name ([#154129](https://github.com/pytorch/pytorch/pull/154129))

## MPS
- `MPSInductor`: `torch.compile` for Apple GPUs ([#150121](https://github.com/pytorch/pytorch/issues/150121), [#149342](https://github.com/pytorch/pytorch/pull/149342), [#151449](https://github.com/pytorch/pytorch/pull/151449), [#151754](https://github.com/pytorch/pytorch/pull/151754), [#149687](https://github.com/pytorch/pytorch/pull/149687), [#149180](https://github.com/pytorch/pytorch/pull/149180), [#149221](https://github.com/pytorch/pytorch/pull/149221), [#153598](https://github.com/pytorch/pytorch/pull/153598), [#152788](https://github.com/pytorch/pytorch/pull/152788), [#153787](https://github.com/pytorch/pytorch/pull/153787), [#152214](https://github.com/pytorch/pytorch/pull/152214), [#151152](https://github.com/pytorch/pytorch/pull/151152), [#155891](https://github.com/pytorch/pytorch/pull/155891), [#154578](https://github.com/pytorch/pytorch/pull/154578), [#151272](https://github.com/pytorch/pytorch/pull/151272), [#151288](https://github.com/pytorch/pytorch/pull/151288), [#153997](https://github.com/pytorch/pytorch/pull/153997), [#151871](https://github.com/pytorch/pytorch/pull/151871), [#153362](https://github.com/pytorch/pytorch/pull/153362), [#156566](https://github.com/pytorch/pytorch/pull/156566), [#150661](https://github.com/pytorch/pytorch/pull/150661), [#153582](https://github.com/pytorch/pytorch/pull/153582))

## Python Frontend
- Added Generalized Pareto Distribution (GPD) ([#135968](https://github.com/pytorch/pytorch/pull/135968))

## Quantization
- Introduced `torch.float4_e2m1fn_x2` dtype ([#148791](https://github.com/pytorch/pytorch/pull/148791))

## XPU
- Support Intel distributed backend (XCCL) ([#141856](https://github.com/pytorch/pytorch/pull/141856))
- Support SYCL kernels through C++ extension ([#132945](https://github.com/pytorch/pytorch/pull/132945))

# Improvements
## Build Frontend
- Removed outdated warning about `TORCH_CUDA_ARCH_LIST` ([#152715](https://github.com/pytorch/pytorch/pull/152715), [#155314](https://github.com/pytorch/pytorch/pull/155314))
- Made Eigen an optional build dependency ([#155955](https://github.com/pytorch/pytorch/pull/155955))
- Updated CUTLASS to 3.9.2 ([#152779](https://github.com/pytorch/pytorch/pull/152779))

## Composability
- Enhanced custom op support with serializable op profiles and fake registration overrides ([#151817](https://github.com/pytorch/pytorch/pull/151817), [#150807](https://github.com/pytorch/pytorch/pull/150807), [#150806](https://github.com/pytorch/pytorch/pull/150806))

## C++ Frontend
- Exposed `bicubic` mode for `torch::nn::functional::grid_sample` ([#150817](https://github.com/pytorch/pytorch/pull/150817))

## CUDA
- Introduced `no_implicit_headers` mode for `load_inline()` on custom CUDA extensions ([#149480](https://github.com/pytorch/pytorch/pull/149480))
- Support large batch sizes in SDPA memory-efficient attention backend ([#154029](https://github.com/pytorch/pytorch/pull/154029), [#154663](https://github.com/pytorch/pytorch/pull/154663))
- Fixed invalid indexing in SDPA memory-efficient attention backward ([#155397](https://github.com/pytorch/pytorch/pull/155397))
- Support SDPA attention backends on sm121 (DGX Spark) ([#152314](https://github.com/pytorch/pytorch/pull/152314))
- Added FP8 row-wise scaled-mm for sm12x (GeForce Blackwell) ([#155991](https://github.com/pytorch/pytorch/pull/155991))

## cuDNN
- Updated cuDNN frontend version to 1.12 ([#153888](https://github.com/pytorch/pytorch/pull/153888))

## Distributed
#### c10d
- Enhanced `TCPStore` with clone and queuing features ([#150966](https://github.com/pytorch/pytorch/pull/150966), [#151045](https://github.com/pytorch/pytorch/pull/151045), [#150969](https://github.com/pytorch/pytorch/pull/150969), [#151485](https://github.com/pytorch/pytorch/pull/151485))
- Added a collective time estimator for NCCL comms ([#149343](https://github.com/pytorch/pytorch/pull/149343))
- Made `getDefaultBackend` more fault tolerant without relying on exceptions ([#149152](https://github.com/pytorch/pytorch/pull/149152))
- Update error message in `get_backend()` with more details ([#141796](https://github.com/pytorch/pytorch/pull/141796))
- Specified the default PyTorch Distributed backend for MPS ([#149538](https://github.com/pytorch/pytorch/pull/149538))
- Supported `masterListenFd` in `TCPStoreLibUvBackend` ([#150215](https://github.com/pytorch/pytorch/pull/150215))
- Use shared stores in gloo ([#150230](https://github.com/pytorch/pytorch/pull/150230))
- Improved FR dump robustness with all watchdog broadcast wait and more frequent store check ([#150652](https://github.com/pytorch/pytorch/pull/150652))
- Implemented safer book-keeping of NCCL communicators ([#150681](https://github.com/pytorch/pytorch/pull/150681))
- Clarified behavior of `TORCH_NCCL_USE_TENSOR_REGISTER_ALLOCATOR_HOOK` ([#150682](https://github.com/pytorch/pytorch/pull/150682))
- Registered also future allocations in mempool with NCCL ([#150684](https://github.com/pytorch/pytorch/pull/150684))
- Added the record of each individual collective being coalesced in FR ([#151238](https://github.com/pytorch/pytorch/pull/151238))
- Added counters for FR dump and reduce its timeout to finish dump before watchdog timeout ([#151329](https://github.com/pytorch/pytorch/pull/151329))
- Avoided computing `global_rank` when `group_rank` is used ([#151373](https://github.com/pytorch/pytorch/pull/151373))
- Exposed NCCL communicator from `ProcessGroupNCCL` via an unsafe API ([#152496](https://github.com/pytorch/pytorch/pull/152496))
- Added split sizes info dump for uneven all2all bw calculation ([#151438](https://github.com/pytorch/pytorch/pull/151438))
- Made FR vendor neutral so that other backends can use it ([#152585](https://github.com/pytorch/pytorch/pull/152585), [#152563](https://github.com/pytorch/pytorch/pull/152563), [#154929](https://github.com/pytorch/pytorch/pull/154929))
- Integrated vendor generic FR into gloo ([#152614](https://github.com/pytorch/pytorch/pull/152614))
- Added `needs_contiguous_strides` tag in functional collective ([#153399](https://github.com/pytorch/pytorch/pull/153399), [#153523](https://github.com/pytorch/pytorch/pull/153523))
- Allowed `split_group` to work with non-nccl backends ([#152175](https://github.com/pytorch/pytorch/pull/152175))
- Simplified `new_subgroups()` by using `new_subgroups_by_enumeration()` ([#153843](https://github.com/pytorch/pytorch/pull/153843))
- Made only current thread allocate to pool in `ProcessGroupNCCL` ([#153990](https://github.com/pytorch/pytorch/pull/153990))
- Enabled using `c10::Half` for gloo ([#153862](https://github.com/pytorch/pytorch/pull/153862))
- Released GIL in PG destructor ([#154976](https://github.com/pytorch/pytorch/pull/154976))
- Enhanced `get_process_group_ranks()` to accept `group=None` ([#154902](https://github.com/pytorch/pytorch/pull/154902))
- Skipped updating the default device distributed backend if already registered ([#155320](https://github.com/pytorch/pytorch/pull/155320))
- Shrinked the range of mutex lock to avoid deadlock ([#155949](https://github.com/pytorch/pytorch/pull/155949))
- Enabled querying the build and runtime NCCL versions ([#156305](https://github.com/pytorch/pytorch/pull/156305))
- Disabled NCCL NVLS when using deterministic mode ([#156381](https://github.com/pytorch/pytorch/pull/156381))
- Made `init_process_group` support index-only device id ([#156214](https://github.com/pytorch/pytorch/pull/156214))
- Support enabling / disabling NaN detector per-`ProcessGroup` ([#151723](https://github.com/pytorch/pytorch/pull/151723))
- Added support for `ReduceOp::AVG` in `ProcessGroupGloo` ([#149781](https://github.com/pytorch/pytorch/pull/149781))
- Added support for `reduce_scatter` + updated support chart in `ProcessGroupGloo` ([#149869](https://github.com/pytorch/pytorch/pull/149869))
- Added FP8 support in `ProcessGroupNCCL` ([#152706](https://github.com/pytorch/pytorch/pull/152706))
- Added `ibverbs` backend in gloo ([#153015](https://github.com/pytorch/pytorch/pull/153015), [#153425](https://github.com/pytorch/pytorch/pull/153425))
- Enabled gloo CUDA when used with a backend that supports `GPUDirect` ([#153406](https://github.com/pytorch/pytorch/pull/153406))

#### DeviceMesh
- Improved device selection logic ([#150897](https://github.com/pytorch/pytorch/pull/150897))

#### DistributedDataParallel (DDP)
- Added one option to allow skipping all reduce unused parameters ([#151503](https://github.com/pytorch/pytorch/pull/151503))
- Added check on received data to avoid segfault in the DDP reducer ([#152143](https://github.com/pytorch/pytorch/pull/152143))
- Propagated `use_python_reducer` to C++ reducer ([#152735](https://github.com/pytorch/pytorch/pull/152735))
`DistributedStateDict` (DSD)
- Supported non-tensor-data `write_size` in planner write items ([#149699](https://github.com/pytorch/pytorch/pull/149699))
- Skip popping meta device tensors ([#153185](https://github.com/pytorch/pytorch/pull/153185))

#### DTensor
- Made `StridedShard` support uneven sharding ([#150490](https://github.com/pytorch/pytorch/pull/150490))
- Added op support for `torch.cumsum` ([#151071](https://github.com/pytorch/pytorch/pull/151071))
- Added `DTensor` `redistribute` fwd/bwd datatype conversion to enable `SimpleFSDP` mixed precision training ([#150740](https://github.com/pytorch/pytorch/pull/150740))
- Added rich support to `torch.distributed.tensor.debug.visualize_sharding` ([#152027](https://github.com/pytorch/pytorch/pull/152027))

#### FullyShardedDataParallel2 (FSDP2)
- Added `PrivateUse1` backend in FSDP collectives ([#147260](https://github.com/pytorch/pytorch/pull/147260))
- Added `set_reshard_after_forward` ([#149103](https://github.com/pytorch/pytorch/pull/149103))
- Added `PrivateUse1` device type to pre forward hook of FSDP ([#149487](https://github.com/pytorch/pytorch/pull/149487))
- Allowed different dtypes for no grad model params ([#154103](https://github.com/pytorch/pytorch/pull/154103))
- Respected `reshard_after_forward=True` for root model ([#154704](https://github.com/pytorch/pytorch/pull/154704))
- Kept root unsharded when not specifying `reshard_after_forward` ([#155319](https://github.com/pytorch/pytorch/pull/155319))
- Allowed forcing FSDP2 to always use SUM reductions ([#155915](https://github.com/pytorch/pytorch/pull/155915))
- Made assert on `all_reduce_event` only if it's not CPU device ([#150316](https://github.com/pytorch/pytorch/pull/150316))
- Enabled NCCL zero-copy (user buffer registration) for FSDP2 ([#150564](https://github.com/pytorch/pytorch/pull/150564))

#### Pipeline Parallelism
- Added schedule visualizer ([#150347](https://github.com/pytorch/pytorch/pull/150347))
- Allowed unused kwargs in ZB path ([#153498](https://github.com/pytorch/pytorch/pull/153498))
- Added `get_pipeline_order()` for Gpipe and 1F1B ([#155935](https://github.com/pytorch/pytorch/pull/155935))

#### ShardedTensor
- Added support for 0-size `ShardedTensor` and recalculated metadata from `all_gather` ([#152583](https://github.com/pytorch/pytorch/pull/152583))

#### TensorParallel
- Added a `ParallelStyle PrepareModuleInputOutput` ([#150372](https://github.com/pytorch/pytorch/pull/150372))

#### torchelastic
- No shutdown of rendezvous on leaving workers ([#152525](https://github.com/pytorch/pytorch/pull/152525))

## torch.compile
#### Dynamo
- Improved tracing support for python sets, tensor subclasses with `__torch_function__`, and `namedtuple` subclasses ([#153150](https://github.com/pytorch/pytorch/pull/153150), [#149792](https://github.com/pytorch/pytorch/pull/149792), [#153982](https://github.com/pytorch/pytorch/pull/153982))
- Eliminated all Compiled Autograd dynamic shapes recompiles for compile time reduction ([#151962](https://github.com/pytorch/pytorch/pull/151962), [#152119](https://github.com/pytorch/pytorch/pull/152119),
[#151962](https://github.com/pytorch/pytorch/pull/151962), [#149707](https://github.com/pytorch/pytorch/pull/149707), [#149709](https://github.com/pytorch/pytorch/pull/149709),
[#148799](https://github.com/pytorch/pytorch/pull/148799), [#148801](https://github.com/pytorch/pytorch/pull/148801))
- Added `reason` field to `torch.compiler.disable` ([#150341](https://github.com/pytorch/pytorch/pull/150341))
- Removed `lru_cache` warnings for functions in the top-level `torch` namespace ([#157718](https://github.com/pytorch/pytorch/pull/157718))

#### Inductor
- Added block sparse support for FlexAttention on CPU ([#147196](https://github.com/pytorch/pytorch/pull/147196))
- Introduced new config settings:
  - `aot_inductor.custom_ops_to_c_shims` and `aot_inductor.custom_op_libs`: allow for specifying custom op C shim ([#153968](https://github.com/pytorch/pytorch/pull/153968))
  - `max_fusion_buffer_group_pairwise_attempts`: limits fusions to specified node distance ([#154688](https://github.com/pytorch/pytorch/pull/154688))
  - `cuda.cutlass_enabled_ops`: controls CUTLASS operation selection ([#155770](https://github.com/pytorch/pytorch/pull/155770))
  - `triton.cudagraph_capture_sizes`: allows specifying certain shapes for which to capture CUDAGraphs; skips CUDAGraphs for other shapes ([#156551](https://github.com/pytorch/pytorch/pull/156551))
  - `use_static_cuda_launcher`: enables launching compiled triton statically to improve cold start times ([#148890](https://github.com/pytorch/pytorch/pull/148890))
  - `assume_unaligned_fallback_output`: allows inductor to track unaligned outputs ([#150777](https://github.com/pytorch/pytorch/pull/150777))
  - `cuda.cutlass_tma_only`: controls whether or not to only use TMA-compatible kernels in CUTLASS ([#152815](https://github.com/pytorch/pytorch/pull/152815))
  - `static_launch_user_defined_triton_kernels`: enables statically launching user defined triton kernels ([#153725](https://github.com/pytorch/pytorch/pull/153725))
  - `precompilation_timeout_seconds`: controls the timeout on precompilation ([#153788](https://github.com/pytorch/pytorch/pull/153788))
  - `disable_decompose_k`: disables new `DecomposeK` GEMM Kernels ([#154421](https://github.com/pytorch/pytorch/pull/154421))
  - `min_num_split`: sets the minimum number of splits in a split reduction ([#155941](https://github.com/pytorch/pytorch/pull/155941))
  - `max_autotune_flex_search_space`: allows specifying the size of the search space for flex attention autotuning ([#156307](https://github.com/pytorch/pytorch/pull/156307))
- Introduced environment variable `LOG_AUTOTUNE_RESULTS` for autotune log ([#156254](https://github.com/pytorch/pytorch/pull/156254))
- Improved numerical stability of CPU Welford reduction for normalizations ([#145061](https://github.com/pytorch/pytorch/pull/145061))

## torch.export
- Improved handling of builtin ops (`min`, `max`, `math.pow`) ([#151348](https://github.com/pytorch/pytorch/pull/151348))
- Added min/max ranges for dim hints ([#149590](https://github.com/pytorch/pytorch/pull/149590))
- Allow registering normal classes to `pytree.register_dataclass` ([#147752](https://github.com/pytorch/pytorch/pull/147752))
- Allow specifying integer inputs as dynamic ([#151842](https://github.com/pytorch/pytorch/pull/151842))
- Inline `jit.script`ed functions in export ([#155180](https://github.com/pytorch/pytorch/pull/155180))
- Pretty printing for graph signature ([#149710](https://github.com/pytorch/pytorch/pull/149710))

## Ahead-Of-Time Inductor (AOTI)
- Support for device-side TMA ([#157241](https://github.com/pytorch/pytorch/pull/157241))
- Added `num_runners` to `AOTIModelPackageLoader` ([#149364](https://github.com/pytorch/pytorch/pull/149364))

## FX
- Updated codegen compare op to `==` ([#150611](https://github.com/pytorch/pytorch/pull/150611))
- Map names to operand indices when const folding submodules ([#150692](https://github.com/pytorch/pytorch/pull/150692))
- Improved stacktrace when tracing ([#151029](https://github.com/pytorch/pytorch/pull/151029), [#155486](https://github.com/pytorch/pytorch/pull/155486))
- Support edge dialect ops in `normalize_function` ([#143689](https://github.com/pytorch/pytorch/pull/143689))
- Fixed path naming in minifier ([#153130](https://github.com/pytorch/pytorch/pull/153130))
- Added `graph_code_verbose_log` artifact for FX passes ([#153775](https://github.com/pytorch/pytorch/pull/153775))
- Improved cache key graph printing performance ([#151928](https://github.com/pytorch/pytorch/pull/151928))
- Added flag to `fx.passes.split_module` to normalize input names ([#157793](https://github.com/pytorch/pytorch/pull/157793))

## Linear Algebra Frontend
- Add tensor overlap check for `cross` ([#154999](https://github.com/pytorch/pytorch/pull/154999))

## MPS
- Added support for a number of `torch.special` operations as well as `index_copy`, `hardshrink`, `rsub`, `col2im`, and `isin` ([#149174](https://github.com/pytorch/pytorch/pull/149174), [#149203](https://github.com/pytorch/pytorch/pull/149203) [#149123](https://github.com/pytorch/pytorch/pull/149123), [#149368](https://github.com/pytorch/pytorch/pull/149368), [#149378](https://github.com/pytorch/pytorch/pull/149378), [#149563](https://github.com/pytorch/pytorch/pull/149563), [#149687](https://github.com/pytorch/pytorch/pull/149687), [#149705](https://github.com/pytorch/pytorch/pull/149705), [#149783](https://github.com/pytorch/pytorch/pull/149783), [#149407](https://github.com/pytorch/pytorch/pull/149407)/[#149680](https://github.com/pytorch/pytorch/pull/149680), [#150279](https://github.com/pytorch/pytorch/pull/150279), [#151754](https://github.com/pytorch/pytorch/pull/151754), [#153786](https://github.com/pytorch/pytorch/pull/153786), [#154326](https://github.com/pytorch/pytorch/pull/154326), [#155304](https://github.com/pytorch/pytorch/pull/155304), [#156263](https://github.com/pytorch/pytorch/pull/156263), [#155382](https://github.com/pytorch/pytorch/pull/155382), [#154010](https://github.com/pytorch/pytorch/pull/154010), [#149816](https://github.com/pytorch/pytorch/pull/149816), [#152282](https://github.com/pytorch/pytorch/pull/152282), [#156090](https://github.com/pytorch/pytorch/pull/156090), [#150060](https://github.com/pytorch/pytorch/pull/150060), [#151600](https://github.com/pytorch/pytorch/pull/151600), [#155002](https://github.com/pytorch/pytorch/pull/155002), [#154671](https://github.com/pytorch/pytorch/pull/154671))
- Extended dtype support for:
  * `index_put` with half precision floats ([#151869](https://github.com/pytorch/pytorch/pull/151869))
  * `ConvTranspose3D` with FP32 and complex ([#154696](https://github.com/pytorch/pytorch/pull/154696))
  * `log1p` and `sigmoid` with int64 ([#151791](https://github.com/pytorch/pytorch/pull/151791))
- Compute activation kernels at float precision ([#155735](https://github.com/pytorch/pytorch/pull/155735))

## Nested Tensor (NJT)
- Fixed contiguity in NJT string representation ([#153529](https://github.com/pytorch/pytorch/pull/153529))

## torch.nn
- Added warning for module full backward hook when no input requires gradient ([#155339](https://github.com/pytorch/pytorch/pull/155339))
- Added Half support for `weight_norm` on CPU ([#148878](https://github.com/pytorch/pytorch/pull/148878))

## ONNX
- Added `asdict` method to `VerificationInfo` class ([#151024](https://github.com/pytorch/pytorch/pull/151024))
- Support running bfloat16 models with ONNX Runtime ([#149646](https://github.com/pytorch/pytorch/pull/149646))
- Updated ONNX program doc formatting and improve robustness ([#151623](https://github.com/pytorch/pytorch/pull/151623))
- Updated `dynamic_shapes` behavior to use `torch.export.dim.DYNAMIC` ([#153065](https://github.com/pytorch/pytorch/pull/153065))
- Set the name of the producing node using the value name ([#155413](https://github.com/pytorch/pytorch/pull/155413))

## Optimizer
- Added `TensorLR` variant for fused Adagrad on CPU ([#153078](https://github.com/pytorch/pytorch/pull/153078))
- Convert tensor lr to 0-dim as needed for the optimizer to normally work ([#145674](https://github.com/pytorch/pytorch/pull/145674))
- Added `lr_lambda` type check in `MultiplicativeLR` ([#151973](https://github.com/pytorch/pytorch/pull/151973))

## Profiler
- Added support for on-demand memory snapshot ([#150559](https://github.com/pytorch/pytorch/pull/150559))
- Added PT2 compile context to visualizer ([#152862](https://github.com/pytorch/pytorch/pull/152862))
- Added PT2 to memory snapshot ([#152707](https://github.com/pytorch/pytorch/pull/152707))
- Added flag to toggle global and local callbacks for annotations ([#154932](https://github.com/pytorch/pytorch/pull/154932))
- Pass overload names to Kineto ([#149333](https://github.com/pytorch/pytorch/pull/149333))
- Set duration to -1 for unfinished CPU events ([#150131](https://github.com/pytorch/pytorch/pull/150131))
- Start at index with most events ([#154571](https://github.com/pytorch/pytorch/pull/154571))

## Python Frontend
- Introduced `torch.AcceleratorError` ([#152023](https://github.com/pytorch/pytorch/pull/152023))
- Implemented `Size.__radd__()` ([#152554](https://github.com/pytorch/pytorch/pull/152554))
- Updated `get_default_device()` to also respect `torch.device` context manager ([#148621](https://github.com/pytorch/pytorch/pull/148621))

## Quantization
- Improved x86 PT2E quantization support with new uint8 ops (pointwise `mul` / `add` / `add_relu` and `batch_norm2d`), qconv1d-relu fusion, and lowering pass ([#151112](https://github.com/pytorch/pytorch/pull/151112), [#152411](https://github.com/pytorch/pytorch/pull/152411), [#152811](https://github.com/pytorch/pytorch/pull/152811), [#150751](https://github.com/pytorch/pytorch/pull/150751), [#149708](https://github.com/pytorch/pytorch/pull/149708))
- Support boolean tensor for `torch.fused_moving_avg_obs_fake_quant` on CUDA ([#153699](https://github.com/pytorch/pytorch/pull/153699))

## Release Engineering
- Updated gcc11 to gcc13 in manylinux images ([#152825](https://github.com/pytorch/pytorch/pull/152825), [#152825](https://github.com/pytorch/pytorch/pull/152825), [#150635](https://github.com/pytorch/pytorch/pull/150635), [#158445](https://github.com/pytorch/pytorch/pull/158445))
- Updated to cmake 3.27.2 ([#154783](https://github.com/pytorch/pytorch/pull/154783), [#150549](https://github.com/pytorch/pytorch/pull/150549), [#153380](https://github.com/pytorch/pytorch/pull/153380))

## ROCm
- Allow user to override default flags for `cpp_extension` ([#152432](https://github.com/pytorch/pytorch/pull/152432))
- Enabled support for sparse compressed `mm`/`bmm`/`addmm` ([#153262](https://github.com/pytorch/pytorch/pull/153262))

## Sparse Frontend
- Enabled sparse compressed tensor invariant checks for `PrivateUse1` extension ([#149374](https://github.com/pytorch/pytorch/pull/149374))

## torch.func
- Add batching rules for ops: `torch.Tensor.scatter_add_` ([#150543](https://github.com/pytorch/pytorch/pull/150543)), `torch.matrix_exp` ([#155202](https://github.com/pytorch/pytorch/pull/155202))

## XPU
- Support safe softmax, GQA, fp32 causal mask for SDP and increase maximum head dim from 256 to 576 on Intel GPU ([#151999](https://github.com/pytorch/pytorch/pull/151999), [#150992](https://github.com/pytorch/pytorch/pull/150992), [#152091](https://github.com/pytorch/pytorch/pull/152091))
- Add memory reporting to Memory Profiler for Intel GPU ([#152842](https://github.com/pytorch/pytorch/pull/152842))
- Support Intel GPU profiler toggle functionality ([#155135](https://github.com/pytorch/pytorch/pull/155135))
- Support distributed memory tracker integration for Intel GPU ([#150703](https://github.com/pytorch/pytorch/pull/150703))
- Improved error handling and reporting in Intel GPU CMake files ([#149353](https://github.com/pytorch/pytorch/pull/149353))
- Support `embed_cubin` and `multi_arch_kernel_binary` options in AOTI for Intel GPU ([#154514](https://github.com/pytorch/pytorch/pull/154514), [#153924](https://github.com/pytorch/pytorch/pull/153924))
- Added generic and Intel GPU specific Stream and Event in `UserDefineClass` ([#155787](https://github.com/pytorch/pytorch/pull/155787))
- Support int4 WOQ GEMM on Intel GPU ([#137566](https://github.com/pytorch/pytorch/pull/137566))

# Bug Fixes
## Build Frontend
- Support builds with `CMake-4.x` ([#150203](https://github.com/pytorch/pytorch/pull/150203))
- Fixed fbgemm build with `gcc-12+` ([#150847](https://github.com/pytorch/pytorch/pull/150847))
- Force build to conform to C++ standard on Windows by adding `/permissive-` flag ([#149035](https://github.com/pytorch/pytorch/pull/149035))

## Composability
- Fixed support for 1-element tuple returns from custom ops ([#155447](https://github.com/pytorch/pytorch/pull/155447))
- Avoid overflow in `torch.norm` for scalar input ([#144073](https://github.com/pytorch/pytorch/pull/144073))

## CPU (x86)
- Fixed apparent copy-paste bug in `log_softmax` reduced-precision fp kernel ([#156379](https://github.com/pytorch/pytorch/pull/156379))

## CUDA
- Fixed deterministic indexing with broadcast ([#154296](https://github.com/pytorch/pytorch/pull/154296))
- Fixed `torch.backends.cuda.matmul.allow_fp16_accumulation` crash when using cuBLASLt ([#153083](https://github.com/pytorch/pytorch/pull/153083))
- Enable `AsyncMM` on Blackwell ([#153519](https://github.com/pytorch/pytorch/pull/153519))
- Fixed `torch.cuda.MemPool` for multithreaded use-cases ([#153356](https://github.com/pytorch/pytorch/pull/153356))
- Fix to avoid calling `sum()` on a default-constructed gamma / beta in `layer_norm` ([#156600](https://github.com/pytorch/pytorch/pull/156600))
- Avoid hangs by erroring out for negative offsets or K=0 in grouped GEMMs ([#153226](https://github.com/pytorch/pytorch/pull/153226))
- Don't error out in `empty_cache` under mempool context ([#158180](https://github.com/pytorch/pytorch/pull/158180))

## Distributed
#### c10d
- Fixed extra CUDA context created by barrier ([#149144](https://github.com/pytorch/pytorch/pull/149144))
- Fixed the logic to use group rank instead of global rank when possible ([#149488](https://github.com/pytorch/pytorch/pull/149488))
- Fixed ET trace collection of `all_to_all` ([#149485](https://github.com/pytorch/pytorch/pull/149485))
- Disabled start event recording for coalesced col and improved profile title ([#150863](https://github.com/pytorch/pytorch/pull/150863))
- Fixed connection reset caused by wrong socket close in tcp store ([#150987](https://github.com/pytorch/pytorch/pull/150987))
- Added back correct EOF case check in the libuv backend of `TCPStore` ([#151052](https://github.com/pytorch/pytorch/pull/151052))
- Fixed unused `group` input argument in `new_subgroups()` ([#152765](https://github.com/pytorch/pytorch/pull/152765))
- Fixed `new_subgroups(group=)` bug ([#153798](https://github.com/pytorch/pytorch/pull/153798))
- Fixed tcp init when using port 0 ([#154156](https://github.com/pytorch/pytorch/pull/154156))
- Adopted a vector to temporarily keep the reference to future object to avoid block ([#156653](https://github.com/pytorch/pytorch/pull/156653))

#### Distributed Checkpointing (DCP)
- Fix to use global coordinator rank in `broadcast_object` util function ([#155912](https://github.com/pytorch/pytorch/pull/155912))

#### DistributedDataParallel (DDP)
- Fixed `DDPOptimizer` issue on static tensor index ([#155746](https://github.com/pytorch/pytorch/pull/155746))

#### DTensor
- Fixed `local_map` with multi-threading ([#149070](https://github.com/pytorch/pytorch/pull/149070))
- Fixed `new_local_tensor` in `redistribute` be None case ([#152303](https://github.com/pytorch/pytorch/pull/152303))
- Fixed bug visualizing 1D Tensor using rich ([#152871](https://github.com/pytorch/pytorch/pull/152871))

#### Pipeline Parallelism
- Optimized memory usage by releasing output memory earlier ([#153383](https://github.com/pytorch/pytorch/pull/153383))

#### RPC
- Made torch importable if compiled without `TensorPipe` ([#154382](https://github.com/pytorch/pytorch/pull/154382))

#### ShardedTensor
- Fixed sharded tensor `gather` when a local tensor on certain ranks has zero elements ([#150914](https://github.com/pytorch/pytorch/pull/150914))

#### TensorParallel
- Turn async-TP applicability asserts back into silent skips ([#158736](https://github.com/pytorch/pytorch/pull/158736))

## torch.compile
#### Dynamo
- Eliminated silent incorrectness issues in the Compiled Autograd initial trace ([#149014](https://github.com/pytorch/pytorch/pull/149014), [#155521](https://github.com/pytorch/pytorch/pull/155521), [#155289](https://github.com/pytorch/pytorch/pull/155289), [#149336](https://github.com/pytorch/pytorch/pull/149336))
- Fixed various tracing errors involving einops, `dict(mapping_proxy)`, and the FlexAttention HOP ([#157754](https://github.com/pytorch/pytorch/pull/157754), [#157515](https://github.com/pytorch/pytorch/pull/157515), [#157519](https://github.com/pytorch/pytorch/pull/157519))
- Fixed unpack hook semantics for memory savings in checkpointing and offloading for Compiled Autograd ([#147242](https://github.com/pytorch/pytorch/pull/147242), [#153300](https://github.com/pytorch/pytorch/pull/153300))
- Fixed sources for dataclass defaults and the `lru_cache` method ([#158689](https://github.com/pytorch/pytorch/pull/158689), [#157308](https://github.com/pytorch/pytorch/pull/157308))
- Fixed spammy errors when an invalid `TORCH_LOGS` argument is passed ([#151678](https://github.com/pytorch/pytorch/pull/151678))

#### Inductor
- Support special kwargs in AMD triton configs ([#154605](https://github.com/pytorch/pytorch/pull/154605))
- Fixed minifier when one has multiple Python runtimes ([#155918](https://github.com/pytorch/pytorch/pull/155918))
- Bug fix for int8 GEMM compensation epilogue ([#152408](https://github.com/pytorch/pytorch/pull/152408))

## torch.export
- Fixed tracing of the following: `aten.is_nonzero` ([#149637](https://github.com/pytorch/pytorch/pull/149637)), `torch.bincount()` ([#152497](https://github.com/pytorch/pytorch/pull/152497)), `aten.div` ([#150874](https://github.com/pytorch/pytorch/pull/150874)) slicing ([#150104](https://github.com/pytorch/pytorch/pull/150104)), and `attn_mask` ([#158618](https://github.com/pytorch/pytorch/pull/158618)), `aten.to` ([#153972](https://github.com/pytorch/pytorch/pull/153972)), scalar tensor construction ([#154661](https://github.com/pytorch/pytorch/pull/154661))
- Fixed `dynamic_shapes` spec for kwargs ([#148772](https://github.com/pytorch/pytorch/pull/148772), [#149528](https://github.com/pytorch/pytorch/pull/149528), [#150103](https://github.com/pytorch/pytorch/pull/150103))
- Fixed input bugs in unflattener ([#149206](https://github.com/pytorch/pytorch/pull/149206), [#153474](https://github.com/pytorch/pytorch/pull/153474), [#153000](https://github.com/pytorch/pytorch/pull/153000))
- Fix nonstrict tracing of `functools.partial` ([#153408](https://github.com/pytorch/pytorch/pull/153408)), and higher order ops ([#149295](https://github.com/pytorch/pytorch/pull/149295))
- Fixed serialization/deserialization of `None` inputs ([#150515](https://github.com/pytorch/pytorch/pull/150515)), `math` module ([#154643](https://github.com/pytorch/pytorch/pull/154643)), `call_torchbind` ([#155647](https://github.com/pytorch/pytorch/pull/155647)), and enums ([#154821](https://github.com/pytorch/pytorch/pull/154821))
- Fixed state dict modification in run_decompositions ([#151436](https://github.com/pytorch/pytorch/pull/151436))
- Fixed subclass access custom op bug ([#149698](https://github.com/pytorch/pytorch/pull/149698))


## Ahead-Of-Time Inductor (AOTI)
- Fixed AOTI `update_constant_buffer` issue ([#149243](https://github.com/pytorch/pytorch/pull/149243))
- Fixed a memory leak in `model_package_loader` ([#152334](https://github.com/pytorch/pytorch/pull/152334))
- Don't alloc weights in `AOTIModel` if they don't exist ([#152692](https://github.com/pytorch/pytorch/pull/152692))
- Fixed state of `ConstantFolding` ([#153152](https://github.com/pytorch/pytorch/pull/153152))
- Fixed index offset for optional tensor return ([#155073](https://github.com/pytorch/pytorch/pull/155073))
- Fixed float8 type printing for min/max value printing ([#154466](https://github.com/pytorch/pytorch/pull/154466))

## Linear Algebra Frontend
- Fix to workaround LAPACK workspace size being returned as a floating point value ([#149682](https://github.com/pytorch/pytorch/pull/149682))
- Fixed the accumulation type for `dot` and `gemv` ([#152676](https://github.com/pytorch/pytorch/pull/152676))
- Fixed `torch.lobpcg` to compute same largest eigenvalue as scipy and `np.linalg.eig` ([#152789](https://github.com/pytorch/pytorch/pull/152789))
- Fixed 32-bit indexing overflows in `ReducedPrecisionGemV` ([#150949](https://github.com/pytorch/pytorch/pull/150949))

## MPS
- Fixed various op support issues: unary/binary ops with `2**32`+ element inputs, binary ops with inputs with different dtypes, ops with complex scalar inputs, `cholesky` decomp, `floor_divide` type promotion, `index_kernel` with large inputs, `lerp` with complex inputs, `logit` with half/bfloat16 inputs, SDPA memory leak, `torch.special.entr`, `tri[ul]`, matrix inversion with `N>1024`, and `where` with non-contiguous `cond` ([#152479](https://github.com/pytorch/pytorch/pull/152479), [#155183](https://github.com/pytorch/pytorch/pull/155183), [#149233](https://github.com/pytorch/pytorch/pull/149233), [#151176](https://github.com/pytorch/pytorch/pull/151176), [#151282](https://github.com/pytorch/pytorch/pull/151282), [#158239](https://github.com/pytorch/pytorch/pull/158239), [#152371](https://github.com/pytorch/pytorch/pull/152371), [#149974](https://github.com/pytorch/pytorch/pull/149974), [#158237](https://github.com/pytorch/pytorch/pull/158237), [#146754](https://github.com/pytorch/pytorch/pull/146754), [#158867](https://github.com/pytorch/pytorch/pull/158867), [#155184](https://github.com/pytorch/pytorch/pull/155184), [#152204](https://github.com/pytorch/pytorch/pull/152204))

## torch.nn
- Fixed `load_state_dict` behavior for `nn.LazyLinear` ([#147599](https://github.com/pytorch/pytorch/pull/147599))

## ONNX
- Fixed bfloat16 support in `onnx_program` callable ([#151121](https://github.com/pytorch/pytorch/pull/151121))
- Produce correct dtypes for bf16/f8 in IR TorchTensor ([#151259](https://github.com/pytorch/pytorch/pull/151259))
- Preserve all legacy exporter params in fallback ([#156659](https://github.com/pytorch/pytorch/pull/156659))
- Fixed 4D tensor conversion for SDPA ([#157509](https://github.com/pytorch/pytorch/pull/157509))

## Optimizer
- Fixed bug where `lr_scheduler` unexpectedly calls `step()` when init argument `last_epoch > -1` ([#149312](https://github.com/pytorch/pytorch/pull/149312))
- Fixed `CosineAnnealingWarmRestarts` resetting `T_cur` ([#151289](https://github.com/pytorch/pytorch/pull/151289))

## Profiler
- Fixed empty C call queue in python tracer ([#150370](https://github.com/pytorch/pytorch/pull/150370))
- Removed decref from python context in python tracer ([#151625](https://github.com/pytorch/pytorch/pull/151625))
- Enable all configured activities in CUPTI Range Profiler mode ([#154749](https://github.com/pytorch/pytorch/pull/154749))

## Python Frontend
- Fixed segfault during numpy string tensor conversion ([#155364](https://github.com/pytorch/pytorch/pull/155364))
- Added checks for empty tensor list ([#155383](https://github.com/pytorch/pytorch/pull/155383))
- Fixed sample validation for `MixtureSameFamily` distribution ([#151317](https://github.com/pytorch/pytorch/pull/151317))
- Fixed bug where creating a second `Wishart` or `Uniform` distribution modifies constraints on the first ([#154361](https://github.com/pytorch/pytorch/pull/154361))
- Fix to properly export `torch::utils::tensor_to_numpy` symbol ([#154178](https://github.com/pytorch/pytorch/pull/154178))
- Fixed `torch.[con]cat[enate]` to avoid crashing on empty inputs ([#155460](https://github.com/pytorch/pytorch/pull/155460))
- Unify `torch.tensor` and `torch.ops.aten.scalar_tensor` behavior ([#158655](https://github.com/pytorch/pytorch/pull/158655))

## Release Engineering
- Checkout optional submodules when publishing a release tarball ([#156615](https://github.com/pytorch/pytorch/pull/156615))
- Fixed MacOS MP hang in Python-3.12+ ([#155698](https://github.com/pytorch/pytorch/pull/155698))
- Fixed static functions when using module in MSVC ([#148675](https://github.com/pytorch/pytorch/pull/148675))
- Fixed VS2022-caused AVX512 illegal instruction issue ([#153480](https://github.com/pytorch/pytorch/pull/153480))

## ROCm
- Fixed build error for opportunistic fastatomics with newer compilers ([#152841](https://github.com/pytorch/pytorch/pull/152841))

#### TunableOp
- More TF32 support ([#149088](https://github.com/pytorch/pytorch/pull/149088))
- Fixed offline tuning for `ScaledGEMM` ([#149677](https://github.com/pytorch/pytorch/pull/149677))
- Fixed row-wise `ScaledGEMM` ([#152403](https://github.com/pytorch/pytorch/pull/152403))
- Support submatrices in offline tuning for ROCm ([#151138](https://github.com/pytorch/pytorch/pull/151138))

## Vulkan
- Fixed `torch.is_vulkan_available()` on Mac ([#155595](https://github.com/pytorch/pytorch/pull/155595))

## XPU
- Fixed matmul accuracy when `offset > 0` ([#154495](https://github.com/pytorch/pytorch/pull/154495))
- Fixed `torch.xpu.is_bf16_supported` to correctly report presence of Intel GPU ([#152317](https://github.com/pytorch/pytorch/pull/152317))
- Fixed AOT compilation in SYCL C++ extension ([#156364](https://github.com/pytorch/pytorch/pull/156364))

# Performance
## Autograd
- Improved autograd streams synchronization ([#151079](https://github.com/pytorch/pytorch/pull/151079), [#157914](https://github.com/pytorch/pytorch/pull/157914))

## CPU (AArch64)
- Compute `ELU(0)` with the cheaper definition ([#155765](https://github.com/pytorch/pytorch/pull/155765))

## CUDA
- Improved performance of `cat` and `index_select` ([#150233](https://github.com/pytorch/pytorch/pull/150233), [#152380](https://github.com/pytorch/pytorch/pull/152380), [#151715](https://github.com/pytorch/pytorch/pull/151715))

## Dataloader Frontend
- Reduced memory usage of `SubsetRandomSampler` by iterating over list instead of tensor ([#149126](https://github.com/pytorch/pytorch/pull/149126))

## torch.compile
#### Inductor
- Improved performance of GEMMs ([#147315](https://github.com/pytorch/pytorch/pull/147315), [#151530](https://github.com/pytorch/pytorch/pull/151530), [#149373](https://github.com/pytorch/pytorch/pull/149373), [#156174](https://github.com/pytorch/pytorch/pull/156174), [#155444](https://github.com/pytorch/pytorch/pull/155444))
- Added a config option `cpp.use_small_dequant_buffer` to use a small dequant buffer for WOQ int4 GEMM ([#156395](https://github.com/pytorch/pytorch/pull/156395))
- Support graph partitioning on custom ops ([#149782](https://github.com/pytorch/pytorch/pull/149782))
- Optimized the heuristics of parallel reduction on CPU ([#149614](https://github.com/pytorch/pytorch/pull/149614))

## torch.export
- Cache unflattened graph module ([#150030](https://github.com/pytorch/pytorch/pull/150030))

## JIT
- Improved Dead Code Elimination (DCE) compile times for large graphs ([#153645](https://github.com/pytorch/pytorch/pull/153645))

## Linear Algebra Frontend
- Introduced fast path for `torch.dot` with float16/bfloat16 ([#152799](https://github.com/pytorch/pytorch/pull/152799))

## MPS
- Improved performance of `LayerNorm`, `mm` / `bmm`, `sum` / `prod` reductions, arithmetic ops,
binary kernels, SDPA, `linear`, and `cumsum` / `cumprod` ([#152010](https://github.com/pytorch/pytorch/pull/152010), [#150541](https://github.com/pytorch/pytorch/pull/150541), [#150566](https://github.com/pytorch/pytorch/pull/150566), [#147644](https://github.com/pytorch/pytorch/pull/147644), [#149730](https://github.com/pytorch/pytorch/pull/149730), [#152781](https://github.com/pytorch/pytorch/pull/152781), [#152210](https://github.com/pytorch/pytorch/pull/152210), [#157494](https://github.com/pytorch/pytorch/pull/157494))

## Python Frontend
- Optimized SVE embedding performance ([#150176](https://github.com/pytorch/pytorch/pull/150176))
- Improved performance for `torch.tensordot` when contracting to a scalar ([#145936](https://github.com/pytorch/pytorch/pull/145936))

## ROCm
- Improved performance of `softmax`, `NLLLoss`, in-place sum, max pooling backward / reductions on NHWC
inputs, max pooling, multi-dimensional reductions, and non-vectorized elementwise kernels ([#149076](https://github.com/pytorch/pytorch/pull/149076), [#149779](https://github.com/pytorch/pytorch/pull/149779), [#149548](https://github.com/pytorch/pytorch/pull/149548), [#151230](https://github.com/pytorch/pytorch/pull/151230), [#152267](https://github.com/pytorch/pytorch/pull/152267), [#154522](https://github.com/pytorch/pytorch/pull/154522), [#154619](https://github.com/pytorch/pytorch/pull/154619), [#155806](https://github.com/pytorch/pytorch/pull/155806), [#153184](https://github.com/pytorch/pytorch/pull/153184))
- Improved scatter add performance on MI250X ([#151724](https://github.com/pytorch/pytorch/pull/151724))
- Extended vectorized elementwise kernel to more heterogenous tensor types ([#149738](https://github.com/pytorch/pytorch/pull/149738))
- Use `HipSparseLT` to further accelerate semi-structured (e.g. 2:4) sparsity ([#150578](https://github.com/pytorch/pytorch/pull/150578))

## Sparse Frontend
- Skip sparse tensor invariant validation when loading sparse Tensors from external storage ([#154610](https://github.com/pytorch/pytorch/pull/154610), [#154759](https://github.com/pytorch/pytorch/pull/154759), [#154638](https://github.com/pytorch/pytorch/pull/154638))

## XPU
- Enabled post-op fusion for oneDNN convolution on Intel GPU ([#150287](https://github.com/pytorch/pytorch/pull/150287))
- Reduced host overhead for Intel GPU by eliminating meaningless API calls ([#151111](https://github.com/pytorch/pytorch/pull/151111))
- Improved INT4 WOQ GEMM for Intel GPU by introducing a cache mechanism to reduce the oneDNN integration overhead further ([#147693](https://github.com/pytorch/pytorch/pull/147693))
- Improved scalar tensor case handling in `addmm`, `baddmm` to reduce oneDNN integration overhead on Intel GPU ([#153051](https://github.com/pytorch/pytorch/pull/153051))

# Documentation
## Autograd
- Added more details on why `ctx.save_for_backward` is important in note about extending autograd ([#153005](https://github.com/pytorch/pytorch/pull/153005))
- Updated docs of `torch.autograd.graph.saved_tensors_hooks` to avoid refcycle ([#153049](https://github.com/pytorch/pytorch/pull/153049))
- Updated gradient behavior note in `torch.amin` and `torch.amax` ([#155071](https://github.com/pytorch/pytorch/pull/155071))

## CUDA
- Fixed deprecated amp APIs in docs ([#154553](https://github.com/pytorch/pytorch/pull/154553))
- Documented device memory apis in correct module ([#155126](https://github.com/pytorch/pytorch/pull/155126))
- Documented non-pytorch CUDA memory allocation and how to query it ([#150880](https://github.com/pytorch/pytorch/pull/150880))

## Distributed
#### c10d
- Documented object collectives limitations ([#150815](https://github.com/pytorch/pytorch/pull/150815))
- Updated `NCCLConfig` with QOS variable ([#151821](https://github.com/pytorch/pytorch/pull/151821))
- Document `get_default_backend_for_device` ([#158236](https://github.com/pytorch/pytorch/pull/158236))

#### FullyShardedDataParallel2 (FSDP2)
- Updated `ignored_params` docstring and added unit tests ([#149074](https://github.com/pytorch/pytorch/pull/149074))
- Added pointer to torchtitan ([#153079](https://github.com/pytorch/pytorch/pull/153079))
- Added warning for incorrected grad results at world size 1 ([#154928](https://github.com/pytorch/pytorch/pull/154928))

## torch.export
- Added mini tutorial for provenance tracking ([#152211](https://github.com/pytorch/pytorch/pull/152211))
- Updated docs for `Dims` and `ExportGraphSignature` ([#156262](https://github.com/pytorch/pytorch/pull/156262), [#156244](https://github.com/pytorch/pytorch/pull/156244))

## Linear Algebra Frontend
- Addressed ambiguity in docs for `torch.linalg.norm()`'s ord argument of +2 & -2 ([#155148](https://github.com/pytorch/pytorch/pull/155148))

## torch.nn
- Improved documentation for transformer-related layers, `nn.RNN`, `nn.functional` loss functions, `interpolate` saturate cast behavior, `ConvTranspose2d` `stride` / `output_size` arguments, and `register_full_backward_hook` ([#155123](https://github.com/pytorch/pytorch/pull/155123), [#153620](https://github.com/pytorch/pytorch/pull/153620), [#148436](https://github.com/pytorch/pytorch/pull/148436), [#151304](https://github.com/pytorch/pytorch/pull/151304), [#150819](https://github.com/pytorch/pytorch/pull/150819), [#150609](https://github.com/pytorch/pytorch/pull/150609), [#151785](https://github.com/pytorch/pytorch/pull/151785))
- Fixed examples for `nn.Sequential` and `nn.LazyModuleMixin` ([#147304](https://github.com/pytorch/pytorch/pull/147304), [#150596](https://github.com/pytorch/pytorch/pull/150596))
- Documented padding size limitations in `nn.modules.padding` and `AvgPoolND` ([#155618](https://github.com/pytorch/pytorch/pull/155618), [#152680](https://github.com/pytorch/pytorch/pull/152680))

## ONNX
- Convert .rst doc files to markdown ([#155228](https://github.com/pytorch/pytorch/pull/155228), [#155556](https://github.com/pytorch/pytorch/pull/155556))
- Improved docstring of ONNX symbolic ops ([#149668](https://github.com/pytorch/pytorch/pull/149668))
- Added note for attention op symbolic function ([#156441](https://github.com/pytorch/pytorch/pull/156441))
- Added ONNX Dynamo metadata documentation ([#155816](https://github.com/pytorch/pytorch/pull/155816))

## Optimizer
- Added scripts to generate plots of `LRScheduler`s ([#149189](https://github.com/pytorch/pytorch/pull/149189))
- Included other accelerators in capturable docstr for optimizers ([#149770](https://github.com/pytorch/pytorch/pull/149770))
- Updated SGD documentation to match implementation and document that dampening is skipped in SGD first step ([#149884](https://github.com/pytorch/pytorch/pull/149884), [#152833](https://github.com/pytorch/pytorch/pull/152833))
- Fixed doc for `CosineAnnealingLR` to accurately reflect its recursive learning rate schedule ([#152936](https://github.com/pytorch/pytorch/pull/152936))
- Fixed incorrect citation of authors in `Adafactor` documentation ([#145209](https://github.com/pytorch/pytorch/pull/145209))
- Added `load_state_dict` hint doc about invoke order work with `lr_scheduler` ([#149942](https://github.com/pytorch/pytorch/pull/149942))

## Python Frontend
- Make `torch.Library`'s `kind` have no default value to be consistent with the code ([#149390](https://github.com/pytorch/pytorch/pull/149390))
- Added 32-bit complex to the list of dtypes ([#144590](https://github.com/pytorch/pytorch/pull/144590))
- Clarified behavior when integer dtype is used with `requires_grad=True` in `tensor.to()` ([#150913](https://github.com/pytorch/pytorch/pull/150913))
- Optimized `cdist` param description ([#151178](https://github.com/pytorch/pytorch/pull/151178))
- Updated serialization docs ([#153631](https://github.com/pytorch/pytorch/pull/153631))
- Render `Example:` and not `Example::` in docs ([#153978](https://github.com/pytorch/pytorch/pull/153978))
- Added docstring indicating undefined behavior for converting inf to int ([#154781](https://github.com/pytorch/pytorch/pull/154781))
- Updated `as_strided()` docs ([#149146](https://github.com/pytorch/pytorch/pull/149146))
- Fixed `keepdim` param optional description ([#151197](https://github.com/pytorch/pytorch/pull/151197))
- Clarify that x and dx are mutually exclusive in `torch.trapezoid` docs ([#151190](https://github.com/pytorch/pytorch/pull/151190))
- Documented `out_dtype` arg for torch GEMM operations ([#151704](https://github.com/pytorch/pytorch/pull/151704))
- Fixed the basic description of `torch.min()`, `torch.max()`, `torch.all()`, and `torch.any()` ([#152658](https://github.com/pytorch/pytorch/pull/152658))
- Added `torch.triu_indices`, `torch.tril_indices` dtype description ([#150749](https://github.com/pytorch/pytorch/pull/150749))
- Optimized `torch.equal` description ([#149618](https://github.com/pytorch/pytorch/pull/149618))

## Quantization
- Fixed incorrect `get_default_qat_qconfig` in `prepare_qat_fx` docs ([#155100](https://github.com/pytorch/pytorch/pull/155100))

## Release Engineering
- Migrated to new theme ([#149331](https://github.com/pytorch/pytorch/pull/149331))

## XPU
- Improved "Getting Started on Intel GPU" hardware requirements and notes ([#151886](https://github.com/pytorch/pytorch/pull/151886))

# Developers
## Distributed
#### c10d
- Added param recording for uniqueID broadcasting and allgather ([#149166](https://github.com/pytorch/pytorch/pull/149166))
- Added logger config for flight record in PGNCCL ([#150356](https://github.com/pytorch/pytorch/pull/150356))
- Added logging for desync debug report ([#150513](https://github.com/pytorch/pytorch/pull/150513))
- Surfaced error type when we unlink and create named pipe for DumpPipe ([#150648](https://github.com/pytorch/pytorch/pull/150648))
- Added logging of `nccl_version` into fr and its dump ([#151048](https://github.com/pytorch/pytorch/pull/151048))
- Added logging after FR dump completed ([#152648](https://github.com/pytorch/pytorch/pull/152648))
- Improved the logs on remote shutdown of tcpstore ([#153586](https://github.com/pytorch/pytorch/pull/153586))
- Enhanced Error Logging in `new_subgroups()` for Non-Divisible World Sizes ([#154124](https://github.com/pytorch/pytorch/pull/154124))
- Added the log of thread name and thread id into fr ([#155142](https://github.com/pytorch/pytorch/pull/155142))
- Added log when fr dump triggered from pipe in `ProcessGroupNCCL` ([#155754](https://github.com/pytorch/pytorch/pull/155754))
- Added a logger for all nccl collectives with its time duration when completed ([#156008](https://github.com/pytorch/pytorch/pull/156008))

#### FullyShardedDataParallel (FSDP1)
- Print FQNs when debugging `FlatParamHandle` ([#151336](https://github.com/pytorch/pytorch/pull/151336))

#### FullyShardedDataParallel2 (FSDP2)
- Added FSDP2 logging ([#155826](https://github.com/pytorch/pytorch/pull/155826))

#### RPC
- Correctly pass exceptions raised from `rpc_init` to CPython ([#154325](https://github.com/pytorch/pytorch/pull/154325))

#### torchelastic
- Added the logging of start of torch elastic workers ([#150849](https://github.com/pytorch/pytorch/pull/150849))
- Passed event log handler to record function calls ([#155457](https://github.com/pytorch/pytorch/pull/155457))
- Added `torch.distributed.run` option to provide destination for event logging ([#155268](https://github.com/pytorch/pytorch/pull/155268))

## torch.export
- Add `TracingContext` ([#149294](https://github.com/pytorch/pytorch/pull/149294))
- Monkeypatch fake mode so it errors on invalid custom ops ([#149410](https://github.com/pytorch/pytorch/pull/149410))
- Fixed torch export docs for preserve_module_call_signature ([#151140](https://github.com/pytorch/pytorch/pull/151140))
- Improved error message for deserializing custom triton op ([#152029](https://github.com/pytorch/pytorch/pull/152029))
- Better type annotation for lift_constants_pass ([#152072](https://github.com/pytorch/pytorch/pull/152072))
- Fixed bug in `detect_attr_assignment` ([#151824](https://github.com/pytorch/pytorch/pull/151824))

## Ahead-Of-Time Inductor (AOTI)
- Refactor `AOTInductor` runtime API for Intel GPU ([#153929](https://github.com/pytorch/pytorch/pull/153929))
- Improve stable library APIs ([#152040](https://github.com/pytorch/pytorch/pull/152040))
- Add a basic shim and `stable::Tensor is_contiguous` API ([#156228](https://github.com/pytorch/pytorch/pull/156228))

## FX
- Gracefully exit minimizer when there is no discrepancy in block mode ([#154076](https://github.com/pytorch/pytorch/pull/154076))

## Optimizer
- Improve decorator typing for Optimizer subclasses ([#153374](https://github.com/pytorch/pytorch/pull/153374))
- Optimize typing in `lr_scheduler.py` ([#151219](https://github.com/pytorch/pytorch/pull/151219))
- Fixed the type hint of `step()` with default value ([#153367](https://github.com/pytorch/pytorch/pull/153367))

## Release Engineering
- Added support for CUDA 12.9 in CI/CD ([#154980](https://github.com/pytorch/pytorch/pull/154980), [#156630](https://github.com/pytorch/pytorch/pull/156630), [#155895](https://github.com/pytorch/pytorch/pull/155895), [#155799](https://github.com/pytorch/pytorch/pull/155799), [#155496](https://github.com/pytorch/pytorch/pull/155496), [#155340](https://github.com/pytorch/pytorch/pull/155340), [#155819](https://github.com/pytorch/pytorch/pull/155819), [#156108](https://github.com/pytorch/pytorch/pull/156108))
- Added support for ROCm 6.4 in CI/CD ([#151236](https://github.com/pytorch/pytorch/pull/151236), [#151345](https://github.com/pytorch/pytorch/pull/151345), [#151355](https://github.com/pytorch/pytorch/pull/151355), [#153253](https://github.com/pytorch/pytorch/pull/153253), [#156112](https://github.com/pytorch/pytorch/pull/156112))
- Moved CI from ubuntu 20.04 images to ubuntu 22.04 and 24.04 ([#154437](https://github.com/pytorch/pytorch/pull/154437), [#154153](https://github.com/pytorch/pytorch/pull/154153), [#149142](https://github.com/pytorch/pytorch/pull/149142))
- Moved CI to CUDA 12.8 ([#154004](https://github.com/pytorch/pytorch/pull/154004), [#152810](https://github.com/pytorch/pytorch/pull/152810), [#155087](https://github.com/pytorch/pytorch/pull/155087), [#148963](https://github.com/pytorch/pytorch/pull/148963))
- Enabled CI on MI300 ([#150667](https://github.com/pytorch/pytorch/pull/150667), [#152133](https://github.com/pytorch/pytorch/pull/152133), [#148394](https://github.com/pytorch/pytorch/pull/148394), [#153134](https://github.com/pytorch/pytorch/pull/153134))
- Enabled CI on H100 ([#153900](https://github.com/pytorch/pytorch/pull/153900), [#154562](https://github.com/pytorch/pytorch/pull/154562), [#153170](https://github.com/pytorch/pytorch/pull/153170), [#155861](https://github.com/pytorch/pytorch/pull/155861), [#155719](https://github.com/pytorch/pytorch/pull/155719), [#156429](https://github.com/pytorch/pytorch/pull/156429))
- Enabled CD for Windows Arm64 ([#150310](https://github.com/pytorch/pytorch/pull/150310), [#152109](https://github.com/pytorch/pytorch/pull/152109), [#149850](https://github.com/pytorch/pytorch/pull/149850), [#152099](https://github.com/pytorch/pytorch/pull/152099))
- Enabled testing of binary Docker builds in CI/CD ([#151483](https://github.com/pytorch/pytorch/pull/151483), [#151488](https://github.com/pytorch/pytorch/pull/151488), [#151489](https://github.com/pytorch/pytorch/pull/151489), [#151706](https://github.com/pytorch/pytorch/pull/151706))
- Added smoke test to validate NCCL and cuDNN versions in PyPI packages ([#149885](https://github.com/pytorch/pytorch/pull/149885), [#150194](https://github.com/pytorch/pytorch/pull/150194))
- Enabled monitoring for performance tests ([#153452](https://github.com/pytorch/pytorch/pull/153452), [#153453](https://github.com/pytorch/pytorch/pull/153453), [#153454](https://github.com/pytorch/pytorch/pull/153454), [#153456](https://github.com/pytorch/pytorch/pull/153456))
- Improved benchmarking and performance testing on MacOS ([#151721](https://github.com/pytorch/pytorch/pull/151721), [#151747](https://github.com/pytorch/pytorch/pull/151747), [#151748](https://github.com/pytorch/pytorch/pull/151748), [#153897](https://github.com/pytorch/pytorch/pull/153897), [#155493](https://github.com/pytorch/pytorch/pull/155493), [#153897](https://github.com/pytorch/pytorch/pull/153897), [#155493](https://github.com/pytorch/pytorch/pull/155493))
- Use `setup-python` from for Mac tests ([#155698](https://github.com/pytorch/pytorch/pull/155698))
- Removed CUDA 11.8 and 12.4 support in CI/CD ([#155509](https://github.com/pytorch/pytorch/pull/155509), [#154169](https://github.com/pytorch/pytorch/pull/154169), [#152362](https://github.com/pytorch/pytorch/pull/152362), [#155555](https://github.com/pytorch/pytorch/pull/155555), [#154893](https://github.com/pytorch/pytorch/pull/154893))
- Removed Anaconda support in CI/CD ([#147789](https://github.com/pytorch/pytorch/pull/147789), [#152338](https://github.com/pytorch/pytorch/pull/152338), [#152431](https://github.com/pytorch/pytorch/pull/152431), [#152377](https://github.com/pytorch/pytorch/pull/152377), [#152433](https://github.com/pytorch/pytorch/pull/152433), [#147476](https://github.com/pytorch/pytorch/pull/147476), [#151035](https://github.com/pytorch/pytorch/pull/151035), [#152860](https://github.com/pytorch/pytorch/pull/152860), [#152702](https://github.com/pytorch/pytorch/pull/152702), [#154303](https://github.com/pytorch/pytorch/pull/154303), [#154309](https://github.com/pytorch/pytorch/pull/154309))
