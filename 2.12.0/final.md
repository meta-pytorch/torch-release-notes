# PyTorch 2.12.0 Release Notes

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
  <tr><td><strong>Batched linalg.eigh on CUDA</strong> is up to 100x faster due to updated cuSolver backend selection.</td></tr>
  <tr><td>New <strong>torch.accelerator.Graph</strong> API unifies graph capture and replay across CUDA, XPU, and out-of-tree backends.</td></tr>
  <tr><td><strong>torch.export.save</strong> now supports Microscaling (MX) quantization formats, enabling full export of aggressively compressed models.</td></tr>
  <tr><td><strong>Adagrad</strong> now supports <code>fused=True</code>, joining Adam, AdamW, and SGD with a single-kernel optimizer implementation.</td></tr>
  <tr><td><strong>torch.cond</strong> control flow can now be captured and replayed inside CUDA Graphs.</td></tr>
  <tr><td><strong>ROCm</strong> users gain expandable memory segments, rocSHMEM symmetric memory collectives, and FlexAttention pipelining.</td></tr>
</table>

For more details about these highlighted features, you can look at the release blogpost. Below are the full release notes for this release.

# Backwards Incompatible Changes

## Build Frontend

- Strengthened SVE compile checks in `FindARM.cmake`, which may reject previously accepted but incorrect SVE configurations ([#176646](https://github.com/pytorch/pytorch/pull/176646))

  Source builds that enable SVE now validate the compiler configuration more strictly. If a build previously passed with an incomplete or mismatched SVE setup, it may now fail during CMake configuration instead of later in compilation. Update the compiler/toolchain flags so they accurately describe the target SVE support, or disable SVE for that build.

- Updated the minimum CUDA version required to build PyTorch from source to CUDA 12.6 ([#178925](https://github.com/pytorch/pytorch/pull/178925))

  Building PyTorch from source with CUDA versions older than 12.6 is no longer supported. Users building custom binaries should install CUDA 12.6 or newer and make sure `CUDA_HOME` points to that installation.

  Version 2.11:
  ```bash
  CUDA_HOME=/usr/local/cuda-12.4 python setup.py develop
  ```

  Version 2.12:
  ```bash
  CUDA_HOME=/usr/local/cuda-12.6 python setup.py develop
  ```

- Enforced a C++20 minimum in CMake build files ([#178662](https://github.com/pytorch/pytorch/pull/178662))

  Source builds now require a compiler and build configuration that support C++20. If you maintain custom build scripts or downstream extensions that build PyTorch from source, update the compiler and remove assumptions that PyTorch can be built as C++17.

## Distributed

- `torch.distributed.nn.functional` ops now raise `RuntimeError` under `torch.compile` ([#177342](https://github.com/pytorch/pytorch/pull/177342))

  All ops in `torch.distributed.nn.functional` (e.g., `broadcast`, `all_reduce`, `all_gather`, `reduce_scatter`, `all_to_all_single`) now raise `RuntimeError` when called inside `torch.compile`. Users should migrate to the functional collectives API in `torch.distributed._functional_collectives`.

  Version 2.11:
  ```python
  @torch.compile
  def my_func(x):
      return torch.distributed.nn.functional.all_reduce(x, op=ReduceOp.SUM)
  ```

  Version 2.12:
  ```python
  @torch.compile
  def my_func(x):
      return torch.distributed._functional_collectives.all_reduce(x, reduceOp="sum", group=group)
  ```

## TorchElastic

- `torchrun` now defaults to an OS-assigned free port for single-node training instead of port 29500 ([#175699](https://github.com/pytorch/pytorch/pull/175699))

  When running `torchrun --nproc-per-node=N script.py` without specifying `--master-port` or `--standalone`, the default behavior now automatically uses an OS-assigned free port via the `c10d` rendezvous backend. This eliminates "Address already in use" errors when running multiple training jobs concurrently. Multi-node training, explicit `--master-port`, `PET_MASTER_PORT` env var, and `--standalone` are unchanged.

  Version 2.11:
  ```bash
  # Used static rendezvous on port 29500 by default
  torchrun --nproc-per-node=4 train.py
  ```

  Version 2.12:
  ```bash
  # Uses OS-assigned free port by default
  torchrun --nproc-per-node=4 train.py

  # To explicitly use a fixed port:
  torchrun --nproc-per-node=4 --master-port=29500 train.py
  ```

## MPS

- All MPS tensors are now allocated in unified memory ([#175818](https://github.com/pytorch/pytorch/pull/175818))

  Previously, MPS tensors could be allocated in either device-only or unified memory. Now all MPS tensors use unified memory unconditionally. This simplifies memory management and enables CPU access to MPS tensor data without explicit copies. Code that relied on device-only memory placement may observe different performance characteristics.

## Inductor

- The `max_autotune` layout-constraint deferral introduced in 2.11 is now opt-in ([#175330](https://github.com/pytorch/pytorch/pull/175330))

  In 2.11, Inductor deferred layout freezing for `max_autotune` templates to expose more fusion opportunities. This caused a regional-inductor failure mode, so the default in 2.12 reverts to immediate layout freezing. Users who relied on the deferred behavior for fusion opportunities should opt in explicitly via `torch._inductor.config.max_autotune_defer_layout_freezing` or `TORCHINDUCTOR_MAX_AUTOTUNE_DEFER_LAYOUT_FREEZING=1`.

  Version 2.11:
  ```python
  # Deferred layout freezing was the default
  torch.compile(model, mode="max-autotune")
  ```

  Version 2.12:
  ```python
  import torch._inductor.config as cfg
  cfg.max_autotune_defer_layout_freezing = True
  # or set TORCHINDUCTOR_MAX_AUTOTUNE_DEFER_LAYOUT_FREEZING=1
  torch.compile(model, mode="max-autotune")
  ```

# Deprecations

## Release Engineering

- Deprecate CUDA 12.8 builds in favor of CUDA 13.0 ([#179072](https://github.com/pytorch/pytorch/pull/179072))

  CUDA 12.8 binaries have been removed from the PyTorch binary build matrix. CUDA 13.0 is now the stable default and CUDA 12.6 remains available for users on older drivers. Users explicitly pinning the `cu128` index URL will need to switch to `cu130` (recommended) or `cu126`.

  Version 2.11:
  ```bash
  pip install torch --index-url https://download.pytorch.org/whl/cu128
  ```

  Version 2.12:
  ```bash
  # Use CUDA 13.0 (default on PyPI):
  pip install torch
  # Or explicitly:
  pip install torch --index-url https://download.pytorch.org/whl/cu130
  # Older driver fallback:
  pip install torch --index-url https://download.pytorch.org/whl/cu126
  ```
- Compatibility with CMake < 3.10 will be removed in a future release ([#166259](https://github.com/pytorch/pytorch/pull/166259))

  Source builds against CMake versions older than 3.10 now emit a deprecation warning. A future release will require CMake 3.10 or newer; please upgrade CMake before then.

## Linear Algebra

- Several CUDA linear algebra operators no longer use the MAGMA backend and now dispatch to cuSolver or cuBLAS unconditionally:
  - `torch.linalg.eigh` now dispatches to cuSolver ([#174619](https://github.com/pytorch/pytorch/pull/174619))
  - `torch.linalg.lu_solve` now dispatches to cuSolver/cuBLAS ([#174248](https://github.com/pytorch/pytorch/pull/174248))
  - `torch.linalg.cholesky_inverse` now dispatches to cuSolver ([#174681](https://github.com/pytorch/pytorch/pull/174681))
  - `torch.linalg.cholesky_solve` now dispatches to cuSolver ([#174769](https://github.com/pytorch/pytorch/pull/174769))

  User code calling these APIs does not need to change. The practical impact is for users who depended on MAGMA-specific numerical behavior, performance characteristics, or debugging. Those calls now use the cuSolver/cuBLAS implementations on CUDA.

## FullyShardedDataParallel2 (FSDP2)

- Compiling through FSDP2 hooks without graph breaks is no longer supported ([#174863](https://github.com/pytorch/pytorch/pull/174863), [#174906](https://github.com/pytorch/pytorch/pull/174906)). If you use compiled autograd with FSDP2, update your code to allow graph breaks around FSDP2 hooks or disable compiled autograd for the FSDP2 training step.

  Version 2.11:
  ```python
  with torch._dynamo.config.patch(compiled_autograd=True):
      compiled_model = torch.compile(fsdp_model, fullgraph=True)
      loss = compiled_model(input).sum()
      loss.backward()
  ```

  Version 2.12:
  ```python
  # Either run FSDP2 backward without fullgraph.
  compiled_model = torch.compile(fsdp_model, fullgraph=False)
  loss = compiled_model(input).sum()
  loss.backward()

  # Or apply compile before applying FSDP.
  compiled_model_pre_fsdp = torch.compile(model, fullgraph=True)
  compiled_model = fully_shard(compiled_model_pre_fsdp, ...)
  loss = compiled_model(input).sum()
  loss.backward()
  ```

## Profiler

- Profiler's `metadata_json` field is now deprecated; use `event_metadata` instead ([#179417](https://github.com/pytorch/pytorch/pull/179417))

  Version 2.11:
  ```python
  metadata = event.metadata_json
  ```

  Version 2.12:
  ```python
  metadata = event.event_metadata
  ```

## Dynamo

- `torch.compile(fullgraph=True)` now warns when a call runs no compiled code; will error in 2.13 ([#181940](https://github.com/pytorch/pytorch/pull/181940))

  Previously `fullgraph=True` was only validated once Dynamo actually compiled and ran the function. If Dynamo was bypassed at call time (e.g. under a user-defined `TorchDispatchMode`), the annotation silently had no effect. 2.12 emits a warning; **2.13 will raise.** For graph-break errors without `fullgraph`'s stronger guarantees, use `torch._dynamo.error_on_graph_break`.

  Version 2.12:
  ```python
  from torch.utils._python_dispatch import TorchDispatchMode

  class LoggingMode(TorchDispatchMode):
      def __torch_dispatch__(self, func, types, args=(), kwargs=None):
          return func(*args, **(kwargs or {}))

  @torch.compile(fullgraph=True)
  def model(x):
      return x.sin() + 1

  # A user-defined TorchDispatchMode is active, so Dynamo skips the frame
  # and no compiled code runs — emits a warning in 2.12, will raise in 2.13.
  with LoggingMode(): # Remove this to fix warning
      model(torch.randn(3, 4))

  ```
- The `inline_inbuilt_nn_modules` Dynamo config is deprecated ([#177489](https://github.com/pytorch/pytorch/pull/177489), [#178205](https://github.com/pytorch/pytorch/pull/178205))

  Inlining of in-built `nn.Module` instances is now the default; setting the flag emits a deprecation warning and it will be removed in a future release.

  Version 2.11:
  ```python
  import torch._dynamo.config as cfg
  cfg.inline_inbuilt_nn_modules = True  # was a tunable knob
  ```

  Version 2.12:
  ```python
  # No action needed — inlining is on by default.
  # Remove any explicit references to torch._dynamo.config.inline_inbuilt_nn_modules.
  ```
- Added a deprecation framework to the `torch.compile` config module so individual options can be marked deprecated ([#169837](https://github.com/pytorch/pytorch/pull/169837))

# New Features

## Release Engineering

- Add Claude-powered autorevert AI advisor workflow ([#177404](https://github.com/pytorch/pytorch/pull/177404), [#178810](https://github.com/pytorch/pytorch/pull/178810))
- Add torchtitan tests to PyTorch CI ([#175901](https://github.com/pytorch/pytorch/pull/175901), [#176774](https://github.com/pytorch/pytorch/pull/176774), [#179749](https://github.com/pytorch/pytorch/pull/179749), [#177572](https://github.com/pytorch/pytorch/pull/177572))
- Add Pallas TPU CI configuration ([#173870](https://github.com/pytorch/pytorch/pull/173870), [#174532](https://github.com/pytorch/pytorch/pull/174532), [#175650](https://github.com/pytorch/pytorch/pull/175650), [#175590](https://github.com/pytorch/pytorch/pull/175590))
- Add downloadable profiler traces and TLParse output from CI runs ([#178488](https://github.com/pytorch/pytorch/pull/178488))
- Enable full AArch64 unit testing for pull requests, with periodic m7g coverage maintained on trunk ([#178270](https://github.com/pytorch/pytorch/pull/178270))

## Python Frontend

- Introduced `torch.accelerator.Graph` as a unified frontend Graph interface ([#171285](https://github.com/pytorch/pytorch/pull/171285))

## Foreach

- Add `_foreach_clone` operator, with a fast path for CUDA utilizing `_foreach_copy_` ([#177421](https://github.com/pytorch/pytorch/pull/177421))

## Distributed

- Add `Store::barrier` API and TCPStore client `BARRIER` support, reducing synchronization round trips compared to the existing `ADD`+`WAIT` pattern ([#174920](https://github.com/pytorch/pytorch/pull/174920))
- Add NCCL communicator `suspend()`, `resume()`, and `memory_stats()` APIs for managing communicator memory lifecycle ([#176300](https://github.com/pytorch/pytorch/pull/176300))
- Add `all_to_all` support in the Gloo backend ([#165435](https://github.com/pytorch/pytorch/pull/165435))
- Add `reduce_scatter_offset` to symmetric memory, supporting variable-sized block reductions with NVLink multicast or LSA fallback ([#177791](https://github.com/pytorch/pytorch/pull/177791))
- Enable `batch_isend_irecv` to work under `torch.compile` ([#161213](https://github.com/pytorch/pytorch/pull/161213))
- Add `torch.distributed.symmetric_memory.is_symm_mem_tensor()` API to check if a tensor is a symmetric memory tensor ([#178947](https://github.com/pytorch/pytorch/pull/178947))
- Convert `NanCheck` to a standalone op (`torch.ops.c10d.check_for_nan`) usable outside of `ProcessGroupNCCL` ([#174990](https://github.com/pytorch/pytorch/pull/174990))

## DTensor

- Add support for twice-differentiable DTensor redistribution ([#160509](https://github.com/pytorch/pytorch/pull/160509))
- DeviceMesh is now traceable by torch.compile. Make DeviceMesh opaque ([#176661](https://github.com/pytorch/pytorch/pull/176661)), Make placements opaque ([#171482](https://github.com/pytorch/pytorch/pull/171482)).
- Add `grad_placements` parameter to `DTensor.from_local()`, allowing explicit control over gradient placements in the backward pass ([#175867](https://github.com/pytorch/pytorch/pull/175867))

## FullyShardedDataParallel2 (FSDP2)

- Support per-parameter meshes in FSDP2, enabling different parameter groups to shard over different meshes ([#173509](https://github.com/pytorch/pytorch/pull/173509))
- Support `fully_shard` with DTensors on a full SPMD mesh via `DataParallelMeshDims` ([#176334](https://github.com/pytorch/pytorch/pull/176334))
- Add FSDP2 support for non-floating-point parameters by excluding non-float parameters from reduce-scatter while still sharding and all-gathering them as needed ([#177948](https://github.com/pytorch/pytorch/pull/177948))

## TorchElastic

- Add configurable `--shutdown-timeout` to `torchrun` for controlling the SIGTERM-to-SIGKILL timeout during worker shutdown ([#172596](https://github.com/pytorch/pytorch/pull/172596))

## CPU x86

- Expose a `CPUBlas` brgemm API for fp8 (e4m3 & e5m2) GEMM, backed by oneDNN ([#172548](https://github.com/pytorch/pytorch/pull/172548))

## CUDA

- Added support for `torch.cond` with CUDA graphs, using conditional graph nodes (CUDA 12.4+) so data-dependent control flow can be captured entirely inside a single CUDA graph. Works with the `eager` and `cudagraphs` `torch.compile` backends (no Inductor support yet). ([#168912](https://github.com/pytorch/pytorch/pull/168912))

## MPS

- Implemented `linalg_qr` for MPS ([#172536](https://github.com/pytorch/pytorch/pull/172536))
- Added `cholesky_solve` support on MPS ([#176703](https://github.com/pytorch/pytorch/pull/176703))
- Added `index_reduce` on MPS ([#174936](https://github.com/pytorch/pytorch/pull/174936))
- Implemented `torch.distributions.Gamma` (forward + backward) on MPS ([#179228](https://github.com/pytorch/pytorch/pull/179228))
- Enabled `mvlgamma` on MPS ([#178914](https://github.com/pytorch/pytorch/pull/178914))
- Added `nonzero_static` implementation on MPS ([#179589](https://github.com/pytorch/pytorch/pull/179589)) _(from miscategorized)_

## ROCm

- Enable expandable segments ([#173330](https://github.com/pytorch/pytorch/pull/173330), [#177974](https://github.com/pytorch/pytorch/pull/177974), [#179930](https://github.com/pytorch/pytorch/pull/179930), [#179781](https://github.com/pytorch/pytorch/pull/179781))
- hipSPARSELt
  - Enable for ROCm >= 7.12 ([#170852](https://github.com/pytorch/pytorch/pull/170852), [#178285](https://github.com/pytorch/pytorch/pull/178285))
  - Enable FP8 semi-structured sparsity ([#179310](https://github.com/pytorch/pytorch/pull/179310))
- amdgcnspirv is now a supported offload target, not enabled by default ([#172559](https://github.com/pytorch/pytorch/pull/172559))

## XPU

- Support `torch.accelerator.Graph` on XPU ([#176421](https://github.com/pytorch/pytorch/pull/176421))
- Added `memory_clock_rate` and `memory_bus_width` to XPU device properties ([#171967](https://github.com/pytorch/pytorch/pull/171967))
- Enable `split_group` API when TorchComms is used as a backend for TorchTitan on XPU ([#178236](https://github.com/pytorch/pytorch/pull/178236))

## Profiler

- Profiler's Activity selection allows for fine-grained activity type selection. ([#176351](https://github.com/pytorch/pytorch/pull/176351))
- Memory visualize has a new tab to show private pool memory view ([#177289](https://github.com/pytorch/pytorch/pull/177289))

## Dynamo

- Made `torch._dynamo.aot_compile` public, with `aot_eager` and `inductor` backend support and docs ([#179917](https://github.com/pytorch/pytorch/pull/179917), [#180008](https://github.com/pytorch/pytorch/pull/180008))
- Added a `recompile_limit` keyword argument to `torch.compile` to override the per-function recompile cap without touching global config ([#177936](https://github.com/pytorch/pytorch/pull/177936))
- Added min/max bounds to `torch._dynamo.mark_unbacked` for communicating value ranges to the symbolic shape system ([#176313](https://github.com/pytorch/pytorch/pull/176313))
- Added `bdb`, a `pdb`-style debugger for stepping through nested frames during Dynamo tracing (`n`, `u`, `d`, `r`, `bt`), plus a user-callable `breakpoint()` that auto-starts it ([#174626](https://github.com/pytorch/pytorch/pull/174626), [#174746](https://github.com/pytorch/pytorch/pull/174746), [#175200](https://github.com/pytorch/pytorch/pull/175200))

## Inductor

- Added user-defined stream support to `torch.compile`. Inductor now codegens stream context managers (enter/exit) and `record_stream` calls in the wrapper, enabling user streams to flow through compiled regions with proper synchronization, scheduler integration, and cross-stream dependency tracking ([#165390](https://github.com/pytorch/pytorch/pull/165390), [#165391](https://github.com/pytorch/pytorch/pull/165391), [#165504](https://github.com/pytorch/pytorch/pull/165504), [#165505](https://github.com/pytorch/pytorch/pull/165505), [#174223](https://github.com/pytorch/pytorch/pull/174223), [#176700](https://github.com/pytorch/pytorch/pull/176700), [#177694](https://github.com/pytorch/pytorch/pull/177694))
- Added `ao::offload`, `ao::reload`, and `ao::wait` ops for asynchronous activation offloading. These ops encapsulate async CPU offloading stream management following the same async 2-op pattern as c10d functional collectives, reducing IR size from 7 nodes (offload) and 5 nodes (reload) down to 2 nodes each ([#177621](https://github.com/pytorch/pytorch/pull/177621))
- Added user-defined Triton kernel unary epilogue fusion. Inductor can now fuse user Triton kernels with downstream pointwise epilogues (e.g. `relu()`), parsing the user kernel source via AST and inlining the epilogue into the `tl.store` expression ([#173662](https://github.com/pytorch/pytorch/pull/173662))
- Added out-variant discovery and lowering for custom ops. When a custom op registers both functional and `.out` overloads, Inductor automatically lowers single-output and multi-output functional ops to their `.out` variants as `ExternKernelOut`, enabling memory planner buffer reuse ([#175116](https://github.com/pytorch/pytorch/pull/175116), [#176117](https://github.com/pytorch/pytorch/pull/176117))
- `max_autotune` now extends to combo kernels. The autotuning pipeline generates and benchmarks per-sub-kernel block-size phase configs, with chained sequential autotuning and per-sub-kernel reduction hints ([#177715](https://github.com/pytorch/pytorch/pull/177715), [#178936](https://github.com/pytorch/pytorch/pull/178936), [#179317](https://github.com/pytorch/pytorch/pull/179317))
- Added non-TMA persistent Triton templates for `mm` and `addmm` for max-autotune, enabling persistent kernels on hardware without TMA ([#177781](https://github.com/pytorch/pytorch/pull/177781), [#179095](https://github.com/pytorch/pytorch/pull/179095))
- Added CUTLASS backend support for `torch.float8_e5m2` dtype, including registration for FP8 GEMM autotuning ([#171176](https://github.com/pytorch/pytorch/pull/171176))
- Added XPU CUTLASS GEMM kernel codegen and codecache to `max-autotune-gemm`, allowing CUTLASS-style GEMM templates to target Intel GPUs ([#161938](https://github.com/pytorch/pytorch/pull/161938), [#161939](https://github.com/pytorch/pytorch/pull/161939))
- Added MTIA Triton codegen for `sort`, `median`, and `mode` operations ([#178525](https://github.com/pytorch/pytorch/pull/178525))
- Added a Triton template for depthwise `conv1d` ([#175280](https://github.com/pytorch/pytorch/pull/175280))
- Added AVX10.2 fp32↔fp8 intrinsics in `at::vec::convert` for the Inductor C++ x86 backend ([#172309](https://github.com/pytorch/pytorch/pull/172309))
- Pallas backend: added scalar prefetch and indirect access support ([#177212](https://github.com/pytorch/pytorch/pull/177212))
- Added a `disable_welford_reduction` config flag to opt out of Welford reduction in codegen ([#175778](https://github.com/pytorch/pytorch/pull/175778))

## Ahead-Of-Time Inductor (AOTI)

- Add MXFP4 dtype support (`float8_e8m0fnu` and `float4_e2m1fn_x2`) to the AOTInductor C shim layer, enabling MXFP4 quantization (e.g., for AMD MI350) ([#176496](https://github.com/pytorch/pytorch/pull/176496))
- Add a compile backend registry and custom device support for AOTI Eager, letting out-of-tree device backends plug into the AOTI eager compile/load flow without modifying upstream code ([#175605](https://github.com/pytorch/pytorch/pull/175605))

## torch.fx

- Add `tuple_return` option to `split_module` that wraps submodule outputs in a tuple ([#179007](https://github.com/pytorch/pytorch/pull/179007))
- Add `ignore_raw_node` option to `GraphPickler` ([#176939](https://github.com/pytorch/pytorch/pull/176939))
- Add `_merge_overlapping_fusions()` method to `FxNetSplitter` which detects and merges overlapping fusion groups ([#177099](https://github.com/pytorch/pytorch/pull/177099))

## torch.export

- Add serialization support for `float8_e8m0fnu` dtype ([#176270](https://github.com/pytorch/pytorch/pull/176270))
- Add serialization support for `torch.uint32` and `torch.uint64` dtypes ([#179434](https://github.com/pytorch/pytorch/pull/179434))
- Add serialization support for nested float lists (`List[List[float]]`) ([#178081](https://github.com/pytorch/pytorch/pull/178081))

## JIT

- Added input-independent graph optimization API ([#179393](https://github.com/pytorch/pytorch/pull/179393))

# Improvements

## Release Engineering

- Add support for CUDA 13.2 in CI/CD including binary builds, magma builds, and Windows CD workflows; update binaries to CUDA 13.2.1 ([#177083](https://github.com/pytorch/pytorch/pull/177083), [#177197](https://github.com/pytorch/pytorch/pull/177197), [#177918](https://github.com/pytorch/pytorch/pull/177918), [#178660](https://github.com/pytorch/pytorch/pull/178660), [#180288](https://github.com/pytorch/pytorch/pull/180288), [#177975](https://github.com/pytorch/pytorch/pull/177975), [#177567](https://github.com/pytorch/pytorch/pull/177567), [#180293](https://github.com/pytorch/pytorch/pull/180293))
- Upgrade Triton to 3.7 ([#174896](https://github.com/pytorch/pytorch/pull/174896), [#178821](https://github.com/pytorch/pytorch/pull/178821), [#179586](https://github.com/pytorch/pytorch/pull/179586), [#179971](https://github.com/pytorch/pytorch/pull/179971), [#177364](https://github.com/pytorch/pytorch/pull/177364), [#177723](https://github.com/pytorch/pytorch/pull/177723))
- Upgrade NCCL to 2.29.7 ([#176299](https://github.com/pytorch/pytorch/pull/176299))
- Upgrade cusparseLt to 0.8.1 for CUDA 12.9 / 13.0 builds ([#177456](https://github.com/pytorch/pytorch/pull/177456))
- Migrate clang15 CI jobs to clang18 and consolidate ASAN/ONNX images ([#178801](https://github.com/pytorch/pytorch/pull/178801), [#178803](https://github.com/pytorch/pytorch/pull/178803), [#178928](https://github.com/pytorch/pytorch/pull/178928))
- Bump MACOSX_DEPLOYMENT_TARGET to 14.0 ([#179083](https://github.com/pytorch/pytorch/pull/179083))
- Bump numpy pin to 2.3.4 for Python 3.14 builds ([#179720](https://github.com/pytorch/pytorch/pull/179720))
- Add macOS wheel platform tag vs dylib minos validation ([#177609](https://github.com/pytorch/pytorch/pull/177609), [#177993](https://github.com/pytorch/pytorch/pull/177993))
- Enable Metal-4 shaders offline compilation ([#179378](https://github.com/pytorch/pytorch/pull/179378))
- Migrate lint and other workflows from EC2 to k8s ARC runners (OSDC) ([#177431](https://github.com/pytorch/pytorch/pull/177431), [#177899](https://github.com/pytorch/pytorch/pull/177899), [#177950](https://github.com/pytorch/pytorch/pull/177950), [#177953](https://github.com/pytorch/pytorch/pull/177953), [#177954](https://github.com/pytorch/pytorch/pull/177954), [#178585](https://github.com/pytorch/pytorch/pull/178585), [#178973](https://github.com/pytorch/pytorch/pull/178973), [#179058](https://github.com/pytorch/pytorch/pull/179058))
- Add XPU client docker image and CI tests ([#174188](https://github.com/pytorch/pytorch/pull/174188), [#177831](https://github.com/pytorch/pytorch/pull/177831), [#178380](https://github.com/pytorch/pytorch/pull/178380), [#178383](https://github.com/pytorch/pytorch/pull/178383), [#178143](https://github.com/pytorch/pytorch/pull/178143), [#179786](https://github.com/pytorch/pytorch/pull/179786))
- Merge majority of libtorch builds into wheel CD builds ([#174753](https://github.com/pytorch/pytorch/pull/174753), [#177802](https://github.com/pytorch/pytorch/pull/177802))
- Enable R2/S3 dual upload for torch nightly packages ([#175352](https://github.com/pytorch/pytorch/pull/175352), [#175570](https://github.com/pytorch/pytorch/pull/175570))
- Make CUDA 13.0 cross-compilation work ([#181287](https://github.com/pytorch/pytorch/pull/181287))

## Python Frontend

- Used compiler wrapper when building C++ extensions ([#175696](https://github.com/pytorch/pytorch/pull/175696))
- Updated `uniform` and `normal` sampling on CPU to improve fp16/bf16 results ([#175988](https://github.com/pytorch/pytorch/pull/175988))
- Changed `requires_grad` to `Optional[bool]` in `torch.asarray` ([#170897](https://github.com/pytorch/pytorch/pull/170897))

## Autograd

- Implemented `narrow_copy` derivative ([#175609](https://github.com/pytorch/pytorch/pull/175609))
- Implemented higher-order derivatives for `grid_sample` ([#177487](https://github.com/pytorch/pytorch/pull/177487))
- Implemented backward and forward AD for `torch.aminmax` ([#175215](https://github.com/pytorch/pytorch/pull/175215))
- Exposed `num_splits` in varlen attention to allow disabling split_kv ([#176905](https://github.com/pytorch/pytorch/pull/176905))
- Added user `AutoNamingMode` support in Selective Activation Checkpointing ([#175348](https://github.com/pytorch/pytorch/pull/175348))
- Refactored `torch.utils.checkpoint` to no longer use `autograd.Function` for saving inputs ([#174327](https://github.com/pytorch/pytorch/pull/174327))

## Dataloader

- Added a thread-safe RNG utility function ([#175375](https://github.com/pytorch/pytorch/pull/175375))

## Linear Algebra

- Added `_int_mm` unsigned int8 × signed int8 (u8s8) support on CPU ([#168226](https://github.com/pytorch/pytorch/pull/168226))
- Added FP64 support for TunableOp on ROCm via hipBLASLt ([#178195](https://github.com/pytorch/pytorch/pull/178195))

## Nested Tensor (NJT)

- Added nested tensor deserialization support ([#174843](https://github.com/pytorch/pytorch/pull/174843))

## torch.nn

- Added `bias` argument to `nn` normalization methods (`LayerNorm`, `GroupNorm`, `RMSNorm`, etc.) ([#176573](https://github.com/pytorch/pytorch/pull/176573))
- Improved `MultiMarginLoss` error message for inconsistent target size ([#174072](https://github.com/pytorch/pytorch/pull/174072))
- Added `enable_gqa` flag to `varlen_attn` ([#179468](https://github.com/pytorch/pytorch/pull/179468))
- Allowed `eps=0` in `batch_norm` during eval mode ([#175508](https://github.com/pytorch/pytorch/pull/175508))
- Added meta device support in `trunc_normal_` initialization ([#176240](https://github.com/pytorch/pytorch/pull/176240))
- Split onehot checks for CPU and accelerators ([#181211](https://github.com/pytorch/pytorch/pull/181211))

## Sparse

- Implemented `clone` operator for semi-structured sparse tensors ([#174991](https://github.com/pytorch/pytorch/pull/174991))
- Allowed semi-structured sparse tensors to be instantiated with `alg_id` ([#178659](https://github.com/pytorch/pytorch/pull/178659))
- Enabled FP8 semi-structured sparsity on ROCm via hipSPARSELt ([#179310](https://github.com/pytorch/pytorch/pull/179310))

## Build Frontend

- Simplified SVE256 detection ([#176247](https://github.com/pytorch/pytorch/pull/176247))
- Removed ARMv7 checks ([#176645](https://github.com/pytorch/pytorch/pull/176645))

## C++ Frontend

- Upgraded `cpp_extension` and `cpp_builder` to C++20 ([#176659](https://github.com/pytorch/pytorch/pull/176659))
- Reland `at::Tag` header-only changes and add a `library.def` override for tags ([#181608](https://github.com/pytorch/pytorch/pull/181608))

## Distributed

- Add configurable worker timeout and partial data support to the distributed debug server ([#176058](https://github.com/pytorch/pytorch/pull/176058))
- Add `timeout` parameter to `torch.distributed.barrier()` ([#174974](https://github.com/pytorch/pytorch/pull/174974))
- Add `reduce_scatter_tensor_coalesced` support to `ProcessGroupWrapper` ([#168961](https://github.com/pytorch/pytorch/pull/168961))
- Functional collectives API now automatically handles non-contiguous inputs instead of asserting ([#177965](https://github.com/pytorch/pytorch/pull/177965))
- DDP: Add `batched_grad_copy` option to reduce per-parameter kernel launches to 2 kernels per bucket ([#176638](https://github.com/pytorch/pytorch/pull/176638))
- DDP: Refactor bucket capacity config into `BucketCapacityConfig` dataclass ([#175217](https://github.com/pytorch/pytorch/pull/175217))
- Add signal name to `ChildFailedError` exitcode output for better debugging ([#175254](https://github.com/pytorch/pytorch/pull/175254))
- Add CUDA-aware detection for Cray MPICH ([#178323](https://github.com/pytorch/pytorch/pull/178323))
- Support `dist.broadcast` for FP8 tensors on GPUs older than SM90 ([#175884](https://github.com/pytorch/pytorch/pull/175884))
- Add `__torch_function__` handlers for distributed functions ([#176376](https://github.com/pytorch/pytorch/pull/176376))
- Enable `split_group` API for TorchComms on XPU ([#178236](https://github.com/pytorch/pytorch/pull/178236))
- Make py-spy dumps nonblocking by default ([#178312](https://github.com/pytorch/pytorch/pull/178312))
- Add `ncclx` and `gloo` to FlightRecorder trace analyzer backend allowlist ([#180268](https://github.com/pytorch/pytorch/pull/180268))
- Improve error message on symmetric memory handle exchange ([#178989](https://github.com/pytorch/pytorch/pull/178989))
- SymmMem: Add thread safety to NCCL and NVSHMEM backends ([#176551](https://github.com/pytorch/pytorch/pull/176551))
- Check NCCL terminate signal more frequently when exiting from heartbeat monitor ([#170000](https://github.com/pytorch/pytorch/pull/170000))
- `Implement missing methods in ProcessGroupWrapper` ([#178779](https://github.com/pytorch/pytorch/pull/178779))
- Add compute_estimator option for overlap scheduling ([#175204](https://github.com/pytorch/pytorch/pull/175204))
- [local_tensor] Add standalone rank_map/tensor_map functions ([#174795](https://github.com/pytorch/pytorch/pull/174795))

## Distributed Checkpoint (DCP)

- DCP: Improve save plan validation error messaging ([#176728](https://github.com/pytorch/pytorch/pull/176728))
- DCP: Preserve original exception in metadata read failure for better debuggability ([#177739](https://github.com/pytorch/pytorch/pull/177739))

## DTensor

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

## FullyShardedDataParallel (FSDP)

- Remove mixed-dtype rejection from FSDP `clip_grad_norm` to match the documented behavior ([#173641](https://github.com/pytorch/pytorch/pull/173641))

## FullyShardedDataParallel2 (FSDP2)

- Allow `ModuleList`/`ModuleDict` subclasses that implement `forward()` ([#175033](https://github.com/pytorch/pytorch/pull/175033))
- FSDP2: Support dataclass args/kwargs output without memory leakage ([#174692](https://github.com/pytorch/pytorch/pull/174692))
- Share more implementation code between replicate and FSDP2 `fully_shard` ([#173580](https://github.com/pytorch/pytorch/pull/173580))
- Consolidate FSDP2 `shard_mesh` and `shard_mesh_from_root` handling ([#174107](https://github.com/pytorch/pytorch/pull/174107))

## Distributed Pipeline

- DTensor metadata foundation for Pipeline Parallelism with DTensor-aware stage and schedule refactoring ([#177727](https://github.com/pytorch/pytorch/pull/177727), [#177728](https://github.com/pytorch/pytorch/pull/177728))
- Pipeline Parallel: Dispatch homogeneous P2P ops individually to avoid stream serialization ([#175712](https://github.com/pytorch/pytorch/pull/175712))

## TorchElastic

- [elastic] Add Windows support for stdout/stderr redirects ([#176789](https://github.com/pytorch/pytorch/pull/176789))
- torchelastic: Keep health check alive during exit barrier ([#178197](https://github.com/pytorch/pytorch/pull/178197))

## CUDA

- [CUDA] Fix `offset_t` operators to be `__host__` `__device__` in `SortStable.cu` ([#175997](https://github.com/pytorch/pytorch/pull/175997))
- [CUDA] [Green Context] Add support for workqueue limit ([#177242](https://github.com/pytorch/pytorch/pull/177242))
- Remove dead `avg_pool3d` backward shape-check variables in CUDA ([#178893](https://github.com/pytorch/pytorch/pull/178893))
- [BE] add missing assert on cuda device synchronize in ATen tests ([#174966](https://github.com/pytorch/pytorch/pull/174966))
- [reland 2][pytorch] Preemptive OOM rejection using `per_process_memory_fraction` + `throw_on_cudamalloc_oom` (#179473) ([#179473](https://github.com/pytorch/pytorch/pull/179473))
- [cuda graphs] Add `enable_annotations kwarg to `torch.cuda.graph` ([#179867](https://github.com/pytorch/pytorch/pull/179867))
- [CUDA/ROCm] avoid double casting in `ReduceLogicKernel` ([#176132](https://github.com/pytorch/pytorch/pull/176132))
- Nit fix: Align state_step tensor max to param tensor max ([#178913](https://github.com/pytorch/pytorch/pull/178913))

## cuDNN

- Upgrade 12.8, 13.0 (and 12.9) wheels to cuDNN 9.20.0.48 ([#177321](https://github.com/pytorch/pytorch/pull/177321))

## MPS

- Fixed `abs` complex overflow/underflow on MPS ([#174346](https://github.com/pytorch/pytorch/pull/174346))
- Migrated `index_fill_` to native Metal ([#175822](https://github.com/pytorch/pytorch/pull/175822))
- Extended `histogram` to float/bfloat types on MPS ([#176913](https://github.com/pytorch/pytorch/pull/176913))
- Extended `unfold_backward` to `torch.complex64` on MPS ([#177274](https://github.com/pytorch/pytorch/pull/177274))
- Added complex input support to `scatter`, `gather`, `repeat`, `cumsum`, `logcumsumexp`, `cumprod`, and `nn.functional.linear` on MPS ([#177794](https://github.com/pytorch/pytorch/pull/177794), [#178198](https://github.com/pytorch/pytorch/pull/178198), [#178328](https://github.com/pytorch/pytorch/pull/178328), [#178411](https://github.com/pytorch/pytorch/pull/178411), [#178436](https://github.com/pytorch/pytorch/pull/178436), [#178799](https://github.com/pytorch/pytorch/pull/178799))
- Migrated `lerp`, `eye`, `relu`, `silu`, `fill_`, `xlogy`, `norm` to native Metal kernels ([#177093](https://github.com/pytorch/pytorch/pull/177093), [#178683](https://github.com/pytorch/pytorch/pull/178683), [#178866](https://github.com/pytorch/pytorch/pull/178866), [#179071](https://github.com/pytorch/pytorch/pull/179071), [#176101](https://github.com/pytorch/pytorch/pull/176101), [#177749](https://github.com/pytorch/pytorch/pull/177749), [#177328](https://github.com/pytorch/pytorch/pull/177328))
- Registered `DeviceCapability` for MPS backend ([#178180](https://github.com/pytorch/pytorch/pull/178180))
- Switched exponential distribution to native Metal ([#174277](https://github.com/pytorch/pytorch/pull/174277))
- Add `enable_gqa` parameter to SDPA MPS meta registration ([#181550](https://github.com/pytorch/pytorch/pull/181550))

## ROCm

- CPP extensions only compile for user's detected arch ([#168998](https://github.com/pytorch/pytorch/pull/168998))
- Remove obsolete HIP NaN handling workarounds; remove technical debt ([#171104](https://github.com/pytorch/pytorch/pull/171104))

## XPU

- Support half precision FFT on XPU backend ([#171231](https://github.com/pytorch/pytorch/pull/171231))
- Add proper float64 handling for `addmv`, `addmm`, and `baddbmm` on XPU ([#174590](https://github.com/pytorch/pytorch/pull/174590))
- Enable FMA-based `addcdiv` lowering for XPU ([#176163](https://github.com/pytorch/pytorch/pull/176163))
- Enable `bmm_outer_product` Triton override for XPU ([#180816](https://github.com/pytorch/pytorch/pull/180816))
- Use version check for XPU fallback registration in Inductor ([#174679](https://github.com/pytorch/pytorch/pull/174679))
- Catch Intel Triton compilation/runtime errors as `IntelGPUError` in Inductor ([#169167](https://github.com/pytorch/pytorch/pull/169167))
- Improve Inductor UT coverage for XPU ([#174053](https://github.com/pytorch/pytorch/pull/174053), [#174054](https://github.com/pytorch/pytorch/pull/174054), [#174055](https://github.com/pytorch/pytorch/pull/174055), [#174056](https://github.com/pytorch/pytorch/pull/174056), [#174057](https://github.com/pytorch/pytorch/pull/174057), [#174058](https://github.com/pytorch/pytorch/pull/174058))
- Added Uint16/Uint32/Uint64/FP8 support to XPU device capability reporting ([#178467](https://github.com/pytorch/pytorch/pull/178467))

## Profiler

- Profiler's events() method now has parity with information returned in export_chrome_trace(). ([#177662](https://github.com/pytorch/pytorch/pull/177662), [#177888](https://github.com/pytorch/pytorch/pull/177888), [#178168](https://github.com/pytorch/pytorch/pull/178168), [#178597](https://github.com/pytorch/pytorch/pull/178597), [#178901](https://github.com/pytorch/pytorch/pull/178901), [#179714](https://github.com/pytorch/pytorch/pull/179714))
- Restructure Memviz and add tests ([#179488](https://github.com/pytorch/pytorch/pull/179488))

## Dynamo

- Broader Python tracing: `enum.Enum` iteration, `nn.Module.__getattribute__`, `_enter_autocast`/`_exit_autocast` and other context managers, `next()` on `itertools.count`, `itertools.takewhile`, `bool(OrderedDict)`, `NamedTuple.__eq__(tuple)`, numpy `ndarray.flat`, and `locals()`/`vars()` ([#175176](https://github.com/pytorch/pytorch/pull/175176), [#175527](https://github.com/pytorch/pytorch/pull/175527), [#173877](https://github.com/pytorch/pytorch/pull/173877), [#176521](https://github.com/pytorch/pytorch/pull/176521), [#178818](https://github.com/pytorch/pytorch/pull/178818), [#177876](https://github.com/pytorch/pytorch/pull/177876), [#175394](https://github.com/pytorch/pytorch/pull/175394), [#176729](https://github.com/pytorch/pytorch/pull/176729), [#175787](https://github.com/pytorch/pytorch/pull/175787), [#179595](https://github.com/pytorch/pytorch/pull/179595))
- CPython `nb_index`/`nb_bool`/`nb_float` slots so Dynamo can trace `operator.index(tensor)`, `bool(...)`, and `float(...)`; graph-break on `torch.Generator` methods ([#178921](https://github.com/pytorch/pytorch/pull/178921), [#178931](https://github.com/pytorch/pytorch/pull/178931), [#179114](https://github.com/pytorch/pytorch/pull/179114), [#180198](https://github.com/pytorch/pytorch/pull/180198), [#178519](https://github.com/pytorch/pytorch/pull/178519))
- Higher-order ops & subgraphs: `cond` supports aliases and mutations under `no_grad`, autogradable leaf modules support pytree outputs, `nonstrict_trace` accepts `nn.Module` inputs, and `invoke_subgraph` supports subgraph reuse ([#172836](https://github.com/pytorch/pytorch/pull/172836), [#172152](https://github.com/pytorch/pytorch/pull/172152), [#175010](https://github.com/pytorch/pytorch/pull/175010), [#172372](https://github.com/pytorch/pytorch/pull/172372), [#176644](https://github.com/pytorch/pytorch/pull/176644))
- Streams & Triton: current-stream handling via `torch.cuda.stream`, sync barriers via a dependency HOP, `triton.set_allocator` inside `torch.compile`, and reuse of tracked objects for Triton `prune_configs_by` ([#177610](https://github.com/pytorch/pytorch/pull/177610), [#168894](https://github.com/pytorch/pytorch/pull/168894), [#177470](https://github.com/pytorch/pytorch/pull/177470), [#177874](https://github.com/pytorch/pytorch/pull/177874))

## Inductor

- Unified `OUT_DTYPE`, `ACC_TYPE`, and `INDEX_DTYPE` codegen flow in Triton templates ([#179453](https://github.com/pytorch/pytorch/pull/179453))
- Enabled cudagraph w/o partition for cpp-wrapper ([#179249](https://github.com/pytorch/pytorch/pull/179249))
- Added FMA-based `addcdiv` lowering for CUDA parity with eager and matching `_foreach_addcdiv` to `_foreach_addcmul` ([#174912](https://github.com/pytorch/pytorch/pull/174912), [#175309](https://github.com/pytorch/pytorch/pull/175309), [#175310](https://github.com/pytorch/pytorch/pull/175310), [#175839](https://github.com/pytorch/pytorch/pull/175839), [#176237](https://github.com/pytorch/pytorch/pull/176237))
- Added `lerp` decompositions for bitwise parity with eager ([#176804](https://github.com/pytorch/pytorch/pull/176804))
- Added outer-product decomposition ([#176552](https://github.com/pytorch/pytorch/pull/176552))
- Enabled padding fusion with `torch.cat` and avoided duplicate computation in `cat`/`pad` when inputs have multiple consumers ([#175729](https://github.com/pytorch/pytorch/pull/175729))
- Lowered functional symmetric memory ops to `ExternKernelOut` for output buffer reuse, and added `symm_mem` planning for graph inputs and fallback regions ([#174856](https://github.com/pytorch/pytorch/pull/174856), [#175449](https://github.com/pytorch/pytorch/pull/175449))
- Modified addmm template call to support hipblaslt bias-fused kernels on ROCm ([#177130](https://github.com/pytorch/pytorch/pull/177130))
- Newly trained PadMM AutoHeuristics for A100 and H200, plus support for `pad_mm` AutoHeuristics in deterministic mode ([#176186](https://github.com/pytorch/pytorch/pull/176186), [#179826](https://github.com/pytorch/pytorch/pull/179826))
- Propagate metadata in pattern matcher and add validation ([#179113](https://github.com/pytorch/pytorch/pull/179113))
- FlexAttention: raise a clear `NotImplementedError` when `return_aux=AuxRequest(max_scores=True)` is requested with `BACKEND='FLASH'` instead of failing later with an opaque error ([#177434](https://github.com/pytorch/pytorch/pull/177434))
- Migrated Inductor internals from legacy `allow_tf32` to `fp32_precision` to avoid divergence with the new TF32 API ([#176098](https://github.com/pytorch/pytorch/pull/176098))
- Pallas backend: enabled element-wise ops, native TPU OOB DMA masking via aligned block specs, and generalized N-D transpose permutation detection ([#174743](https://github.com/pytorch/pytorch/pull/174743), [#175458](https://github.com/pytorch/pytorch/pull/175458), [#176952](https://github.com/pytorch/pytorch/pull/176952))
- Registered lowerings for `prims.scalar_tensor` and `aten.arange.start_step` ([#179017](https://github.com/pytorch/pytorch/pull/179017), [#179028](https://github.com/pytorch/pytorch/pull/179028))
- Added SDPA pattern matching support for visformer ([#177826](https://github.com/pytorch/pytorch/pull/177826))
- Relaxed concat-linear fusion to support GQA QKV ([#178523](https://github.com/pytorch/pytorch/pull/178523))
- Allowed subgraphs to be benchmarked with async pipelined autotuning ([#175455](https://github.com/pytorch/pytorch/pull/175455))
- Added `convert_element_type` lowering to emulate PyTorch eager numerics ([#176781](https://github.com/pytorch/pytorch/pull/176781))
- Added GEMM configs to XPU autotuning heuristic ([#177647](https://github.com/pytorch/pytorch/pull/177647))
- Added `kpack` Triton compile options on ROCm ([#173179](https://github.com/pytorch/pytorch/pull/173179))
- ROCm: enabled exhaustive autotuning for FP8 ([#177797](https://github.com/pytorch/pytorch/pull/177797))
- Override decomposition for `aten.index_add` ([#179486](https://github.com/pytorch/pytorch/pull/179486))
- Drop `tile_k` from nvMatmulHeuristics matching ([#176845](https://github.com/pytorch/pytorch/pull/176845))

## Ahead-Of-Time Inductor (AOTI)

- Add `aten._grouped_mm` to AOTInductor fallback ops, enabling cpp-wrapper mode for grouped_mm ([#177307](https://github.com/pytorch/pytorch/pull/177307))
- Support lazy Triton kernel compilation for cpp-wrapper on XPU ([#179239](https://github.com/pytorch/pytorch/pull/179239))
- Add dynamic shapes support to AOTI Eager via `AOTIPythonKernelHolder`, allowing a single compiled kernel to serve multiple input shapes ([#176018](https://github.com/pytorch/pytorch/pull/176018))
- Support multi-return ops in AOTI Eager (e.g., `native_layer_norm`, `aminmax`) ([#176019](https://github.com/pytorch/pytorch/pull/176019))
- Allow custom ops with `Optional[List[T]]` arguments in cpp wrapper ([#174460](https://github.com/pytorch/pytorch/pull/174460))
- Add lazy Triton kernel compilation for cpp-wrapper ([#175416](https://github.com/pytorch/pytorch/pull/175416))
- Add TMA support for lazy Triton kernel compilation ([#175548](https://github.com/pytorch/pytorch/pull/175548))
- Call latest c_shim version for versioned fallback ops ([#181548](https://github.com/pytorch/pytorch/pull/181548))
- Add BC-safe c_shim v2 for `_scaled_dot_product_attention_math_for_mps` `enable_gqa` ([#181549](https://github.com/pytorch/pytorch/pull/181549))

## torch.fx

- Update `get_source_partitioner` to parse `nn_module_stack` metadata for improved source-based graph partitioning ([#175788](https://github.com/pytorch/pytorch/pull/175788))
- `split_module` now uses `_make_graph_module` to support lazy recompile ([#177907](https://github.com/pytorch/pytorch/pull/177907))
- Fix `fuser_utils.topo_sort` to produce a stable ordering ([#175378](https://github.com/pytorch/pytorch/pull/175378))
- Fix GraphPickler to support nodes with slice() arguments ([#175996](https://github.com/pytorch/pytorch/pull/175996))

## Composability

- Added `DynamicInt` `__pow__` and `__rpow__` methods ([#179868](https://github.com/pytorch/pytorch/pull/179868))
- Added `scaled_mm_v2` CPU implementation ([#176266](https://github.com/pytorch/pytorch/pull/176266))

# Bug fixes

## Release Engineering

- Fix periodic inductor CI silently skipping all tests ([#177695](https://github.com/pytorch/pytorch/pull/177695))
- Fix python docs build hanging in CI ([#180177](https://github.com/pytorch/pytorch/pull/180177))
- Avoid installing test dll into Windows wheel and fix libuv copy path ([#179024](https://github.com/pytorch/pytorch/pull/179024))
- Fix aarch64 build-osdc using x86 runner on ARC ([#179783](https://github.com/pytorch/pytorch/pull/179783))
- Fix stale `PYTORCH_RELEASES_CODE_CC` dict ([#182369](https://github.com/pytorch/pytorch/pull/182369))

## Python Frontend

- Fixed `torch.isclose` broadcast failure with `equal_nan=True` ([#175244](https://github.com/pytorch/pytorch/pull/175244))

## Autograd

- Fixed `torch.trace` backward for non-square matrices ([#175068](https://github.com/pytorch/pytorch/pull/175068))
- Added explicit error when `layer_norm` computes 3rd order derivatives ([#176234](https://github.com/pytorch/pytorch/pull/176234))
- Fixed `_wrap_sync_node` to replace deps in output node's nested args ([#178471](https://github.com/pytorch/pytorch/pull/178471))
- Fixed thread-unsafe lazy init of `setup_context` cache ([#179475](https://github.com/pytorch/pytorch/pull/179475))

## Linear Algebra

- Fixed `addmv` backward pass failure ([#165777](https://github.com/pytorch/pytorch/pull/165777))
- Fixed determinant gradient for 1×1 matrices ([#171225](https://github.com/pytorch/pytorch/pull/171225))
- Fixed `linalg.det` backward for 0-dimensional inputs ([#177498](https://github.com/pytorch/pytorch/pull/177498))
- Fixed `cholesky(upper=True)` on macOS for matrices larger than block size ([#179154](https://github.com/pytorch/pytorch/pull/179154))
- Revert pytorch/pytorch#172340 ([#181364](https://github.com/pytorch/pytorch/pull/181364))

## torch.nn

- Fixed `trunc_normal_` low precision issue when used with half-precision dtypes ([#174997](https://github.com/pytorch/pytorch/pull/174997))
- Added dtype check to `nll_loss` meta function to prevent invalid input types ([#175151](https://github.com/pytorch/pytorch/pull/175151))
- Fixed numerical inconsistency in `Conv3d.reset_parameters` for channels_last format ([#175990](https://github.com/pytorch/pytorch/pull/175990))
- Fixed `MSELoss` failing to compute gradients when inputs have different dtypes ([#175743](https://github.com/pytorch/pytorch/pull/175743))
- Fixed `GroupNorm` backward correctness bug on AMD wavefront-64 GPUs ([#178872](https://github.com/pytorch/pytorch/pull/178872))
- Fixed `nn.functional.pad` compile crash with deterministic mode and replication padding ([#177166](https://github.com/pytorch/pytorch/pull/177166))
- Fixed issue #110505 ([#176559](https://github.com/pytorch/pytorch/pull/176559))
- Fix FA4 integration for varlen ([#177675](https://github.com/pytorch/pytorch/pull/177675))

## Sparse

- Fixed `torch.bmm(COO, Dense)` memory misalignment on CUDA ([#175347](https://github.com/pytorch/pytorch/pull/175347))

## Build Frontend

- Fixed `TORCH_BUILD_VERSION` not updating when `version.txt` changes ([#176167](https://github.com/pytorch/pytorch/pull/176167))

## Distributed

- Fix `_CoalescingManager` not passing `Opts` to `allgather_into_tensor_coalesced()` ([#175379](https://github.com/pytorch/pytorch/pull/175379))
- Fix `_CoalescingManager` to raise exception when ops in the coalesced list are not the same type ([#175573](https://github.com/pytorch/pytorch/pull/175573))
- Fix `getenv`/`setenv` race condition causing segfault during NCCL initialization with heartbeat thread ([#167523](https://github.com/pytorch/pytorch/pull/167523))
- Fix `AsyncCollectiveTensor` inputs leaking into compiled regions, causing `RuntimeError` or silent data corruption in TP + compile workflows ([#179849](https://github.com/pytorch/pytorch/pull/179849))
- Fix potential infinite loop in FlightRecorder when multiple ProcessGroups run into barrier ([#179449](https://github.com/pytorch/pytorch/pull/179449))
- Fix two forward passes of DDP-wrapped BatchNorm raising error ([#175851](https://github.com/pytorch/pytorch/pull/175851))
- Fix `USE_RCOM` typo to `USE_ROCM` in `intra_node_comm.cpp` ([#175078](https://github.com/pytorch/pytorch/pull/175078))
- Fix HPU backend mapping issue ([#174764](https://github.com/pytorch/pytorch/pull/174764))
- Fix NCCL symmetric memory mismatch by using allocation-time counter for Block ordering ([#178362](https://github.com/pytorch/pytorch/pull/178362))
- Fix `NCCLPeerAllocInfo` destructor to properly deregister windows and free resources ([#177459](https://github.com/pytorch/pytorch/pull/177459))
- Fix nested DDP causing _active_ddp_module cleared by inner _inside_ddp_module() ([#178364](https://github.com/pytorch/pytorch/pull/178364))
- Fix extra deps mapping and cycles after bucketing ([#177688](https://github.com/pytorch/pytorch/pull/177688))
- Add proper skips for FP8 on sm < 89 ([#170528](https://github.com/pytorch/pytorch/pull/170528))
- Fix cross type bucketing ([#175150](https://github.com/pytorch/pytorch/pull/175150))

## Distributed Checkpoint (DCP)

- DCP: Fix save plan caching bug during validation failures ([#176289](https://github.com/pytorch/pytorch/pull/176289))
- DCP: Fix `Metadata.storage_meta` regression from `dataclasses.replace()` ([#178001](https://github.com/pytorch/pytorch/pull/178001))
- DCP: Fix unpicklable `FrameSummary._code` on Python 3.13+ ([#177754](https://github.com/pytorch/pytorch/pull/177754))

## DTensor

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

## FullyShardedDataParallel (FSDP)

- Fix FSDP `_unshard()` passing a CUDA stream where an event was expected ([#170525](https://github.com/pytorch/pytorch/pull/170525))
- Fix symbolic context reuse for gradients when creating meta tensors ([#176864](https://github.com/pytorch/pytorch/pull/176864))
- Fix HSDP `sync_module_states` broadcast order for buffers with meta-device initialization ([#178569](https://github.com/pytorch/pytorch/pull/178569))
- Fix activation checkpointing crash when passing `BlockMask` as an argument ([#179215](https://github.com/pytorch/pytorch/pull/179215))
- Revert a FSDP1 all-gather prefetching regression ([#181667](https://github.com/pytorch/pytorch/pull/181667))
- Revert PR 178223 to bring back all-gather prefetching ([#181669](https://github.com/pytorch/pytorch/pull/181669))

## FullyShardedDataParallel2 (FSDP2)

- Fix FSDP2 `split_with_sizes_copy()` missing `dim` argument ([#169173](https://github.com/pytorch/pytorch/pull/169173))
- Fix mixed DTensor errors with nested FSDP and activation checkpointing ([#171779](https://github.com/pytorch/pytorch/pull/171779))
- Fix tied weights with uneven sharding across separate FSDP groups ([#176225](https://github.com/pytorch/pytorch/pull/176225))
- Revert FSDP2 communication-op FQN annotations due to `async_op=True` profiler trace issues ([#182100](https://github.com/pytorch/pytorch/pull/182100))
- Revert "[FSDP2] add fqn to communication ops" ([#182157](https://github.com/pytorch/pytorch/pull/182157))

## Distributed Pipeline

- Fix `stage_backward_weight` with multi-output intermediate in pipeline parallelism ([#175705](https://github.com/pytorch/pytorch/pull/175705))

## CPU aarch64

- Add vectorized BF16 `transpose_mxn` specialization for AArch64 SVE, providing a deterministic vectorized BF16 transpose implementation independent of fixed vector widths ([#174097](https://github.com/pytorch/pytorch/pull/174097))

## CUDA

- Fix cuda torch.topk index bug for inputs over 32-bit length ([#176095](https://github.com/pytorch/pytorch/pull/176095))
- Fix `test/inductor/test_fp8.py` hang on sm89 ([#177573](https://github.com/pytorch/pytorch/pull/177573))
- Use fp8 conversion intrinsics on Hopper+ to work around ptxas codegen bug ([#177870](https://github.com/pytorch/pytorch/pull/177870))
- [CUDA] Fix wrong non-atomic handling in `AdaptiveMaxPooling2d.cu` ([#179261](https://github.com/pytorch/pytorch/pull/179261))
- [CUDA] Fix wrong `ComplexTransform` `const kTransformB` in `fpA_intB_gemm.h` ([#179271](https://github.com/pytorch/pytorch/pull/179271))
- [CUDA] Fix wrong `LayoutB` in `fpA_intB_gemm.h` ([#179269](https://github.com/pytorch/pytorch/pull/179269))
- Back out "[CUDA][cuBLASLt] set cuBLASLt as a default BLAS backend when available (#174594)" (#177703) ([#177703](https://github.com/pytorch/pytorch/pull/177703))
- Fix CUTLASS illegal memory access via subprocess isolation ([#172123](https://github.com/pytorch/pytorch/pull/172123))

## cuDNN

- [cuDNN][SDPA] Don't route to cuDNN SDPA when dropout probability is not a multiple of 1/16 ([#174245](https://github.com/pytorch/pytorch/pull/174245))
- Fix cuDNN SDPA with zero-stride (broadcast) Q/K/V inputs ([#175764](https://github.com/pytorch/pytorch/pull/175764))
- [cuDNN][SDPA] Fix attn-mask conversion constant ([#177868](https://github.com/pytorch/pytorch/pull/177868))

## MPS

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
- Fix sliced `channels_last` tensor handling ([#181107](https://github.com/pytorch/pytorch/pull/181107))
- Fix SDPA wrong output for permuted q/k/v with `B > 1` ([#181886](https://github.com/pytorch/pytorch/pull/181886))
- Fix bool mask handling in the 1-pass SDPA decode kernel ([#182311](https://github.com/pytorch/pytorch/pull/182311))

## ROCm

- Fix SDPA build error when USE_FLASH_ATTENTION=0 USE_MEM_EFF_ATTENTION=1 ([#177552](https://github.com/pytorch/pytorch/pull/177552))
- Fix `_get_amdsmi_device_index` to return devices in correct order ([#178398](https://github.com/pytorch/pytorch/pull/178398))
- Fix scaled_mm incorrectly validating unsupported swizzle ([#178688](https://github.com/pytorch/pytorch/pull/178688))
- Move rocblas.h include out of anonymous namespace ([#178767](https://github.com/pytorch/pytorch/pull/178767))
- Don't crash for MHA backward with head dim > 192, fall back to CK tile ([#178946](https://github.com/pytorch/pytorch/pull/178946))
- Don't fail torch.cuda.device_count() if pynvml is installed ([#175077](https://github.com/pytorch/pytorch/pull/175077))
- Fix hipblaslt GEMMs executing concurrently on multiple HIP streams ([#179053](https://github.com/pytorch/pytorch/pull/179053))
- Windows
  - Fix linker failure caused by missing DLL export directives via native headers ([#179138](https://github.com/pytorch/pytorch/pull/179138))
  - Fix int4mm std::memcpy build error ([#175410](https://github.com/pytorch/pytorch/pull/175410))
  - Fix Windows access violation in MIOpen CTC loss dispatch ([#178284](https://github.com/pytorch/pytorch/pull/178284))
  - Fix Windows DLL linkage for batch norm (`-Winconsistent-dllimport`) ([#179706](https://github.com/pytorch/pytorch/pull/179706))
- Workaround hipGraph event query errors in NCCL watchdog ([#175377](https://github.com/pytorch/pytorch/pull/175377))
- Fix linker error for aotriton when USE_MEM_EFF_ATTENTION=ON but USE_FLASH_ATTENTION=OFF ([#175079](https://github.com/pytorch/pytorch/pull/175079))
- Fix build_amd.py (hipify) failure when MSLK submodule is missing ([#175180](https://github.com/pytorch/pytorch/pull/175180))
- Hipify CUdeviceptr in lazy scratch allocation codegen ([#179978](https://github.com/pytorch/pytorch/pull/179978))

## XPU

- Fix `torch.compile` graph break inside `torch.autocast('xpu')` causing dtype mismatch ([#180309](https://github.com/pytorch/pytorch/pull/180309))
- Fix `conv2d` incorrect results and alignment errors for non-64-byte-aligned tensors on XPU ([#177956](https://github.com/pytorch/pytorch/pull/177956))
- Fix `nn.Embedding` module failures on XPU ([#178987](https://github.com/pytorch/pytorch/pull/178987))
- Fix XPU OneDNN symbol leak ([#172437](https://github.com/pytorch/pytorch/pull/172437))
- Fix meta kernel for `_scaled_dot_product_fused_attention_overrideable` to preserve query layout ([#178986](https://github.com/pytorch/pytorch/pull/178986))
- Fix tensorwise scaling settings on XPU ([#177810](https://github.com/pytorch/pytorch/pull/177810))
- Fix `DeviceOpOverrides` registered incorrectly on XPU ([#178959](https://github.com/pytorch/pytorch/pull/178959))
- Fix `SyclExtension` Windows build for oneAPI 2025.3+ breaking change ([#170701](https://github.com/pytorch/pytorch/pull/170701))

## Dynamo

- Guard correctness: missing source annotation on float guard after recompile, missing guards on class attribute access for literals/enums, guard on constant function `__defaults__`, guard tensor-method fallthrough against unknown methods, and closure-hash in `CodeId` so factory functions don't reuse stale graphs ([#177103](https://github.com/pytorch/pytorch/pull/177103), [#177191](https://github.com/pytorch/pytorch/pull/177191), [#178420](https://github.com/pytorch/pytorch/pull/178420), [#177737](https://github.com/pytorch/pytorch/pull/177737), [#173512](https://github.com/pytorch/pytorch/pull/173512))
- Tracing: `@property` setters bypassed by `torch.compile`, `AttributeError` swallowed by `try`/`except` on tensor attributes, `torch.Size` dict lookups with tensor-backed keys, graph break on enum members with class values, `detach_` autograd metadata, `allow_in_graph` crash inside compiled functions, preserve original exception in `GuardOnDataDependentSymNode`, and `einops` 0.6.1 backwards patch ([#176624](https://github.com/pytorch/pytorch/pull/176624), [#175611](https://github.com/pytorch/pytorch/pull/175611), [#177313](https://github.com/pytorch/pytorch/pull/177313), [#177439](https://github.com/pytorch/pytorch/pull/177439), [#177875](https://github.com/pytorch/pytorch/pull/177875), [#178524](https://github.com/pytorch/pytorch/pull/178524), [#176016](https://github.com/pytorch/pytorch/pull/176016), [#177165](https://github.com/pytorch/pytorch/pull/177165))
- Nested graph breaks: global-scope bug in nested closures, decorators in the compiled region, graph break in `contextlib.contextmanager` init, and parent-stack corruption in `step_graph_break` ([#176906](https://github.com/pytorch/pytorch/pull/176906), [#177090](https://github.com/pytorch/pytorch/pull/177090), [#177195](https://github.com/pytorch/pytorch/pull/177195), [#177408](https://github.com/pytorch/pytorch/pull/177408))
- Compile-state & integration: `torch.compiler.is_exporting()` returning `True` during `torch.compile`, activation-checkpoint metadata loss through custom `autograd.Function`, mixed-dtype `bmm`/`matmul`, `vjp_fn` under `torch.compile`, `_extract_distributed_info` crash on FX-`Node` `group_name`, `nested_compile_region` cache keyed on `fn.__code__`, and reverting `allow_in_graph` deprecation warn-spam ([#176499](https://github.com/pytorch/pytorch/pull/176499), [#177396](https://github.com/pytorch/pytorch/pull/177396), [#177696](https://github.com/pytorch/pytorch/pull/177696), [#173883](https://github.com/pytorch/pytorch/pull/173883), [#178108](https://github.com/pytorch/pytorch/pull/178108), [#179148](https://github.com/pytorch/pytorch/pull/179148), [#178340](https://github.com/pytorch/pytorch/pull/178340))
- Fix `cuda_stream` pointer extraction for generic `torch.Stream` ([#181019](https://github.com/pytorch/pytorch/pull/181019))
- Warn instead of erroring on `fullgraph=True` fallback to eager ([#181940](https://github.com/pytorch/pytorch/pull/181940))

## AOTDispatcher

- Fixed AOTAutograd crash on `no_grad` views of differentiable intermediates ([#175673](https://github.com/pytorch/pytorch/pull/175673))
- Fixed inplace checks in autograd backward functions during functionalization ([#177213](https://github.com/pytorch/pytorch/pull/177213))

## Inductor

- Fix `floordiv` Inductor lowering for mixed signedness (Triton workaround) ([#175168](https://github.com/pytorch/pytorch/pull/175168))
- Use `Sm100CollectiveEpilogue` on SM100 ([#175305](https://github.com/pytorch/pytorch/pull/175305))
- Fix `aten.resize` on overlapping-stride views ([#176651](https://github.com/pytorch/pytorch/pull/176651))
- Fix `ConstructorMoverPass` replacing CPU placeholder in graph output and creating mixed-device pointwise ops ([#176164](https://github.com/pytorch/pytorch/pull/176164), [#177646](https://github.com/pytorch/pytorch/pull/177646))
- Use `VecMask::from` for scalar masks in CPU codegen ([#178148](https://github.com/pytorch/pytorch/pull/178148))
- Fix `triton_main_loop_scaled_mm` template to use correct scale recipe ([#178005](https://github.com/pytorch/pytorch/pull/178005))
- Fix `cpp_wrapper` lazy compile stale state across `fresh_cache` resets ([#178162](https://github.com/pytorch/pytorch/pull/178162))
- Fix int64 indexing with >65k M/N size ([#172925](https://github.com/pytorch/pytorch/pull/172925))
- Fix BMM Triton template `grid_y` overflow for large batch dims and i32 overflow in template kernel signature for large storage offsets ([#178617](https://github.com/pytorch/pytorch/pull/178617), [#179333](https://github.com/pytorch/pytorch/pull/179333))
- Fix `remove_no_ops` incorrectly eliminating ops on mutated values ([#174938](https://github.com/pytorch/pytorch/pull/174938))
- Fix negative-zero constant codegen for the Triton backend ([#176035](https://github.com/pytorch/pytorch/pull/176035))
- Fix coordinate descent tuner incorrectly re-running on warm cache ([#173391](https://github.com/pytorch/pytorch/pull/173391))
- Fix BF16/FP16 scalar comparison to match eager ([#175807](https://github.com/pytorch/pytorch/pull/175807))
- Defensively check `name` is in `buffer_read_counts` before access ([#171245](https://github.com/pytorch/pytorch/pull/171245))
- Fix cpp-wrapper `SyntaxError` when Triton kernel has docstrings ([#176796](https://github.com/pytorch/pytorch/pull/176796))
- Fix `fallback_random` dropout stride mismatch ([#177077](https://github.com/pytorch/pytorch/pull/177077))
- Fix `AssertionError` in `ForeachKernelSchedulerNode` loop reordering after fusion ([#176849](https://github.com/pytorch/pytorch/pull/176849))
- Fix incorrect rounding of `floordiv` ([#177926](https://github.com/pytorch/pytorch/pull/177926))
- Fix issue in AMD `persistent_mm_template` selection ([#178178](https://github.com/pytorch/pytorch/pull/178178))
- Pointwise configs with `max_autotune` must include pointwise configs with `max_autotune_pointwise` ([#177995](https://github.com/pytorch/pytorch/pull/177995))
- Fix `num_warps` when max_autotune is enabled on HIP ([#178023](https://github.com/pytorch/pytorch/pull/178023))
- Fix `nn.Dropout` accuracy discrepancies between Triton and torch implementations ([#178843](https://github.com/pytorch/pytorch/pull/178843))
- Fix eager/compiled mismatch for integer `floor_divide` with zero divisor ([#178016](https://github.com/pytorch/pytorch/pull/178016))
- Accept 1D bias in addmm ATen heuristic on ROCm ([#179087](https://github.com/pytorch/pytorch/pull/179087))
- Fix `randn_like` inconsistency between eager and compile with `fallback_random=True` ([#177994](https://github.com/pytorch/pytorch/pull/177994))
- Fix `MetalScheduling` constructor in MPSInductor ([#179646](https://github.com/pytorch/pytorch/pull/179646))
- Prevent cross-stream inplace and memory-planning buffer reuse for user-streams ([#178548](https://github.com/pytorch/pytorch/pull/178548), [#178549](https://github.com/pytorch/pytorch/pull/178549))
- Fix `argmax`/`argmin` returning incorrect indices for boolean tensors on CUDA ([#174076](https://github.com/pytorch/pytorch/pull/174076))
- Fix block-pointer advancement for broadcasted tensors ([#175008](https://github.com/pytorch/pytorch/pull/175008))
- Fix masked vectorization for the Inductor C++ backend ([#174648](https://github.com/pytorch/pytorch/pull/174648))
- Fix bucketize NaN handling in Triton codegen and Pallas `sign` to match PyTorch NaN semantics ([#176579](https://github.com/pytorch/pytorch/pull/176579), [#176814](https://github.com/pytorch/pytorch/pull/176814))
- Fix `UnicodeDecodeError` in Triton depthwise conv template ([#176484](https://github.com/pytorch/pytorch/pull/176484))
- Handle 0-sized dimensions in Pallas codegen ([#176813](https://github.com/pytorch/pytorch/pull/176813))
- Fix `torch._check` divisibility propagation to Triton `tt.divisibility` ([#175755](https://github.com/pytorch/pytorch/pull/175755))
- Fix SIGSEGV on AMD RDNA (Wave32) from removed reduction masks in persistent kernels ([#176269](https://github.com/pytorch/pytorch/pull/176269))
- Pallas: fix non-stride-1 reductions and prevent incompatible reduction fusion ([#176489](https://github.com/pytorch/pytorch/pull/176489))
- Fix `block_ptr` store dtype for inplace-mutated buffers ([#177860](https://github.com/pytorch/pytorch/pull/177860))
- Fix constants handling for Triton `constexpr` ([#172354](https://github.com/pytorch/pytorch/pull/172354))
- Fix Inductor reinplace bool shadowing (`'bool' object not callable`) ([#176090](https://github.com/pytorch/pytorch/pull/176090))
- Fix Inductor `_split_iteration_ranges` silently dropping dimensions ([#177673](https://github.com/pytorch/pytorch/pull/177673))
- Fix `sym_sum` lowering to accept varargs ([#178661](https://github.com/pytorch/pytorch/pull/178661))
- Fix `bias_addmm` for AMD ([#178929](https://github.com/pytorch/pytorch/pull/178929))
- Define unbacked slice size symbol when bounds become provable after tracing ([#178897](https://github.com/pytorch/pytorch/pull/178897))
- Add `isinf()` to `Float8_e4m3fn` to fix `nan_asserts` crash with fp8 inputs ([#160641](https://github.com/pytorch/pytorch/pull/160641))
- Fix division by zero in the Triton kernel launcher when `Grid2DWithYZOverflow` ([#178878](https://github.com/pytorch/pytorch/pull/178878))
- Prevent user-kernel fusion with non-unary epilogues ([#179735](https://github.com/pytorch/pytorch/pull/179735))
- Preserve order of `torch.cond` ([#179457](https://github.com/pytorch/pytorch/pull/179457))
- Fix performance regression caused by user kernel epilogue fusion ([#176772](https://github.com/pytorch/pytorch/pull/176772))
- Fix `torch.compile` performance regression for `cumprod` backward ([#170388](https://github.com/pytorch/pytorch/pull/170388))
- Include `lazy_triton_compile.h` in the XPU `cpp_wrapper` header ([#180815](https://github.com/pytorch/pytorch/pull/180815))
- Fix cudagraphs compatibility with the current stream ([#180916](https://github.com/pytorch/pytorch/pull/180916))
- Revert native API stamp-out for BMM outer product ([#181658](https://github.com/pytorch/pytorch/pull/181658))
- Fix dynamic shape tile issue ([#181795](https://github.com/pytorch/pytorch/pull/181795))
- Avoid raw stream name collisions in Inductor ([#182178](https://github.com/pytorch/pytorch/pull/182178))

## Ahead-Of-Time Inductor (AOTI)

- Fix AOTI incorrect loads from bool tensor pointers in user-defined Triton kernels ([#176353](https://github.com/pytorch/pytorch/pull/176353))
- Fix lazy compile kernel state collisions across modules by making it per-module instead of global ([#178163](https://github.com/pytorch/pytorch/pull/178163))
- Fix expression-nesting limit in cpp-wrapper when combo kernel gets too large ([#180217](https://github.com/pytorch/pytorch/pull/180217))
- Fix const folding in `run_single_threaded` ([#174998](https://github.com/pytorch/pytorch/pull/174998))
- Fix AOTI Eager caching to populate the in-memory cache after first compilation, avoiding repeated disk round-trips on every dispatch ([#176017](https://github.com/pytorch/pytorch/pull/176017))
- Fix SIGPE by adding additional check logics in the codegen ([#170669](https://github.com/pytorch/pytorch/pull/170669))
- Fix scratch size for TMA in C++ wrapper ([#175385](https://github.com/pytorch/pytorch/pull/175385))
- Emit `int64_t` type declaration for kernel numel variables ([#176922](https://github.com/pytorch/pytorch/pull/176922))
- Fix CPP wrapper lazy compile for scalar tensor args ([#178478](https://github.com/pytorch/pytorch/pull/178478))
- Fix Triton kernel stream for user stream contexts ([#178547](https://github.com/pytorch/pytorch/pull/178547))

## torch.fx

- Fix edge case in `get_source_partitioner` ([#175935](https://github.com/pytorch/pytorch/pull/175935))
- Fix `make_fx` handling of value types for opaque objects so values are inlined into the graph consistently with dynamo behavior ([#178036](https://github.com/pytorch/pytorch/pull/178036))
- Fix `meta["val"]` not being populated for reconstructed opaque nodes, resolving partitioner classification issues ([#179660](https://github.com/pytorch/pytorch/pull/179660))
- Fix `repeat_interleave` fx graph to be runnable ([#177909](https://github.com/pytorch/pytorch/pull/177909))
- Fix fuse_by_partitions crash when partition has no external outputs ([#175203](https://github.com/pytorch/pytorch/pull/175203))
- Fix set_stack_trace ([#177332](https://github.com/pytorch/pytorch/pull/177332))
- Handle weakref objects during graph serialization in GraphPickler ([#178190](https://github.com/pytorch/pytorch/pull/178190))
- Fix horizontal fusion bug and add partition tests for regional inductor ([#178421](https://github.com/pytorch/pytorch/pull/178421))

## torch.export

- Fix export serialization to handle unused `List[Tensor]` outputs ([#176677](https://github.com/pytorch/pytorch/pull/176677))
- Fix MPS SDPA meta kernel to avoid data-dependent branching ([#177620](https://github.com/pytorch/pytorch/pull/177620))
- Fix `torch.export.unflatten` `KeyError` when module FQNs contain `@N` suffixes ([#179278](https://github.com/pytorch/pytorch/pull/179278))
- Fix `run_decompositions()` failure for custom ops with `List[List[Tensor]]` arguments ([#176355](https://github.com/pytorch/pytorch/pull/176355))
- Fix `torch.quantile` `DataDependentOutputException` failure ([#174859](https://github.com/pytorch/pytorch/pull/174859))
- Fix `isin` decomposition with using symbolic shapes ([#178076](https://github.com/pytorch/pytorch/pull/178076))

## Quantization

- Fix activation quantization creating duplicate backward placeholders ([#180287](https://github.com/pytorch/pytorch/pull/180287))

## JIT

- Silenced CPython 3.13.8 `inspect.getsourcelines()` bug ([#179066](https://github.com/pytorch/pytorch/pull/179066))
- Fixed data race in opaque type registry ([#175694](https://github.com/pytorch/pytorch/pull/175694))
- Fixed xplat build: use `PyObjectType::get()` directly ([#178786](https://github.com/pytorch/pytorch/pull/178786))

## Functorch

- Fixed `grad`/`vjp`/`jvp` returning zeros under `inference_mode` ([#177596](https://github.com/pytorch/pytorch/pull/177596))
- Fixed `vmap` batch rules for `group_norm` backward operator ([#176272](https://github.com/pytorch/pytorch/pull/176272))
- [functorch] Fix double-pop in popDynamicLayerStackToDepth ([#177585](https://github.com/pytorch/pytorch/pull/177585))

## torch.func

- Fixed scatter error messages for inplace operations ([#179420](https://github.com/pytorch/pytorch/pull/179420))

## Composability

- Fixed stride handling in FFT meta registrations ([#175731](https://github.com/pytorch/pytorch/pull/175731))
- Fixed exception messages displaying as tuples instead of formatted strings ([#175957](https://github.com/pytorch/pytorch/pull/175957))
- Fixed `one_hot` runtime error ([#177160](https://github.com/pytorch/pytorch/pull/177160))
- Fixed wrong bool-to-int conversion in symbolic tracing ([#177178](https://github.com/pytorch/pytorch/pull/177178))
- Preserved scalar `item()` semantics for size-1 tensors ([#177270](https://github.com/pytorch/pytorch/pull/177270))
- Fixed `_build_proxy_for_sym_expr` for n-ary `sympy.Add` by mapping to `torch.sym_sum` ([#175398](https://github.com/pytorch/pytorch/pull/175398))

## FX

- Fix the `MetaProxy` error caused by skipping dispatch ([#181170](https://github.com/pytorch/pytorch/pull/181170))
- Preserve `FakeScriptObject` for value-type opaques ([#181454](https://github.com/pytorch/pytorch/pull/181454))

# Performance

## Release Engineering

- Add deterministic mode for benchmark perf tests ([#178233](https://github.com/pytorch/pytorch/pull/178233))
- Fix subprocess benchmark crash for addmm with input_reorder ([#177930](https://github.com/pytorch/pytorch/pull/177930))
- Add unbacked perf testing to inductor periodic ([#177034](https://github.com/pytorch/pytorch/pull/177034))

## Autograd

- Used non-blocking copy in `save_on_cpu` pack hook for faster activation offloading ([#175421](https://github.com/pytorch/pytorch/pull/175421))

## Linear Algebra

- Improved `torch.cholesky_solve` performance for batched inputs on CUDA via cuSolver ([#175898](https://github.com/pytorch/pytorch/pull/175898))

## torch.nn

- Added NEON implementation of `interpolate` for bilinear/bicubic with antialias on ChannelsLast RGB images on ARM ([#176217](https://github.com/pytorch/pytorch/pull/176217))
- Parallelized `upsample_bicubic2d` across batch/channel dimensions — 4-43x speedup for VLM position embedding resizing ([#174578](https://github.com/pytorch/pytorch/pull/174578))
- Freed q, k, v early in `multi_head_attention_forward` to reduce peak memory usage ([#178452](https://github.com/pytorch/pytorch/pull/178452))

## Foreach

- Increase kernel argument size 4KB -> 32KB for CUDA 13+ ([#178641](https://github.com/pytorch/pytorch/pull/178641))
- Add multi-tensor fast path for p=0 norm ([#179869](https://github.com/pytorch/pytorch/pull/179869))

## Sparse

- Reduced CPU overhead in sparse operations for improved performance ([#179193](https://github.com/pytorch/pytorch/pull/179193))
- Minor performance improvements for `torch.bmm(COO, Dense)` ([#175347](https://github.com/pytorch/pytorch/pull/175347))

## Distributed

- Improve `AsyncMM.cu` performance by avoiding redundant IO/compute via `ElementC` void type ([#178653](https://github.com/pytorch/pytorch/pull/178653))
- Improve Context Parallel head-tail load balancer indices creation performance (up to 1555x speedup for 1M sequence length) ([#178199](https://github.com/pytorch/pytorch/pull/178199))
- Improve tensor-to-allocation lookup in NCCL Symmetric Memory ([#176744](https://github.com/pytorch/pytorch/pull/176744))
- Avoid two probes when inserting handle into SymmMem cache ([#177463](https://github.com/pytorch/pytorch/pull/177463))

## Distributed Checkpoint (DCP)

- Optimize DCP consolidation I/O for remote mounts (from ~2h to 35s) ([#175762](https://github.com/pytorch/pytorch/pull/175762))

## DTensor

- Improve DTensor performance for `torch.cat` and pytree ops ([#174879](https://github.com/pytorch/pytorch/pull/174879))
- Skip unnecessary all-reduce of `total_weight` in DTensor `nll_loss_backward` for `reduction='sum'` ([#177233](https://github.com/pytorch/pytorch/pull/177233))
- Cache `DecompStrategy` and fake mesh in DTensor ([#175205](https://github.com/pytorch/pytorch/pull/175205))

## FullyShardedDataParallel (FSDP)

- Use SymmMem for reduce-scatter in FSDP ([#177111](https://github.com/pytorch/pytorch/pull/177111))

## FullyShardedDataParallel2 (FSDP2)

- Improve FSDP2 parameter FQN lookup from quadratic to linear complexity ([#174675](https://github.com/pytorch/pytorch/pull/174675))
- Overlap FSDP2 reduce-scatter with compute for per-parameter meshes ([#177319](https://github.com/pytorch/pytorch/pull/177319))
- Cache FSDP2 `shard_mesh` to avoid repeated submesh creation ([#179655](https://github.com/pytorch/pytorch/pull/179655))

## CPU aarch64

- Add TLS `stack_bounds` to avoid expensive reads ([#181137](https://github.com/pytorch/pytorch/pull/181137))

## CUDA

- Update eigh CUDA heuristics ([#175403](https://github.com/pytorch/pytorch/pull/175403))
- [CUBLAS][Blackwell] Enable 32MiB cuBLAS workspaces on Blackwell ([#175344](https://github.com/pytorch/pytorch/pull/175344))
- [CUDA] [PERFORMANCE] Improve performance for `RowwiseScaledMM.cu` by avoiding redundant IO/compute via indicating that indicating that `ElementC` type is void ([#178644](https://github.com/pytorch/pytorch/pull/178644))
- [CUDA] [PERFORMANCE] Improve performance for `ScaledGroupMM.cu` by avoiding redundant IO/compute via indicating that indicating that `ElementC` type is void ([#178325](https://github.com/pytorch/pytorch/pull/178325))
- [CUDA][TensorIterator] Improve vectorized elementwise kernel: instruction cache ([#175336](https://github.com/pytorch/pytorch/pull/175336))
- [pt] Reland vec8 vectorization ([#176352](https://github.com/pytorch/pytorch/pull/176352))
- Use aminmax instead of min and max kernels in histc ([#178011](https://github.com/pytorch/pytorch/pull/178011))

## MPS

- Reimplemented `cross` as single-stage Metal kernel ([#175498](https://github.com/pytorch/pytorch/pull/175498))
- Replaced MPSGraph `nonzero` with native Metal prefix-sum + scatter ([#178484](https://github.com/pytorch/pytorch/pull/178484))
- Sped up `RMSNorm` on MPS ([#180173](https://github.com/pytorch/pytorch/pull/180173))
- Removed `.item()` sync in `_amp_non_finite_check_and_unscale_mps` ([#180267](https://github.com/pytorch/pytorch/pull/180267))

## ROCm

- Directly access GPU scalars if largeBar is enabled, avoiding D2H copy ([#177023](https://github.com/pytorch/pytorch/pull/177023))
- TopK operator performance improvement via RadixSelect prefetching ([#174897](https://github.com/pytorch/pytorch/pull/174897), [#177149](https://github.com/pytorch/pytorch/pull/177149), [#178188](https://github.com/pytorch/pytorch/pull/178188), [#174837](https://github.com/pytorch/pytorch/pull/174837))
- Improved kernel loop unrolling by leveraging compiler ([#177697](https://github.com/pytorch/pytorch/pull/177697))
- Remove need for expensive fence in normalization kernel ([#175286](https://github.com/pytorch/pytorch/pull/175286))
- Avoid double casting in ReduceLogicKernel ([#176132](https://github.com/pytorch/pytorch/pull/176132))
- In group_gemm, use new kernel for all K equal cases ([#173502](https://github.com/pytorch/pytorch/pull/173502))
- Use BFloat16 native hardware type casting ([#178814](https://github.com/pytorch/pytorch/pull/178814))
- Use optimized tiled kernel for LayerNorm gamma beta backward ([#179019](https://github.com/pytorch/pytorch/pull/179019))
- Tune Flex-Attention occupancy on gfx942 for head_dim 64/128/256 ([#176261](https://github.com/pytorch/pytorch/pull/176261))

## XPU

- Remove unnecessary device-to-host synchronization in `torch.nn.functional.one_hot` for XPU by skipping boundary validation checks only needed on CPU ([#179831](https://github.com/pytorch/pytorch/pull/179831))
- Add GEMM configs to XPU autotuning heuristic ([#177647](https://github.com/pytorch/pytorch/pull/177647))

## Dynamo

- Faster guards: `GUARD_VALUE_DISPATCH` dispatch table, fast-path `requires_grad`, `DICT_NOT_CONTAINS`/`SET_NOT_CONTAINS`, `PyType_GetDict` on Python ≥3.12, thread-safe dict-version tracking, no recompiles on hoistable opaque objects, and a general guard-optimization pass ([#176033](https://github.com/pytorch/pytorch/pull/176033), [#177158](https://github.com/pytorch/pytorch/pull/177158), [#176053](https://github.com/pytorch/pytorch/pull/176053), [#179170](https://github.com/pytorch/pytorch/pull/179170), [#178703](https://github.com/pytorch/pytorch/pull/178703), [#176643](https://github.com/pytorch/pytorch/pull/176643), [#175006](https://github.com/pytorch/pytorch/pull/175006))
- Faster tracing: `tree_map_with_path`, constant-folding `elementwise_dtypes`, `inline_invoke_subgraph` post-tracing pass, emit subgraph output intermediates only on observed side effects, drop unnecessary `realize_all` in `speculate_subgraph`, skip `SymInt` copies in `TENSOR_SUBCLASS_METADATA_MATCH`, and avoid closure refcycle in `_empty_create_subclass` ([#174146](https://github.com/pytorch/pytorch/pull/174146), [#177743](https://github.com/pytorch/pytorch/pull/177743), [#176082](https://github.com/pytorch/pytorch/pull/176082), [#177368](https://github.com/pytorch/pytorch/pull/177368), [#176742](https://github.com/pytorch/pytorch/pull/176742), [#175596](https://github.com/pytorch/pytorch/pull/175596), [#175660](https://github.com/pytorch/pytorch/pull/175660))

## AOTAutograd

- Skipped expensive `debug_lines` computation in AOT autograd cache ([#179733](https://github.com/pytorch/pytorch/pull/179733))
- Sped up `ConfigModule._get_dict` by avoiding unnecessary work ([#179734](https://github.com/pytorch/pytorch/pull/179734))

## Inductor

- Add `donate_graph_module` option to `standalone_compile` to avoid extra graph module copies ([#179910](https://github.com/pytorch/pytorch/pull/179910))
- Rewrite multi-consumer `F.pad` as `torch.cat` for zero-copy ([#177216](https://github.com/pytorch/pytorch/pull/177216))
- ROCm: enable pipelining for FlexAttention ([#176676](https://github.com/pytorch/pytorch/pull/176676))
- CPU: make `remove_identity` in-place for inference to align with `pre_grad_passes` ([#177805](https://github.com/pytorch/pytorch/pull/177805))
- CPU: fuse `round` and `to` in quant ([#171699](https://github.com/pytorch/pytorch/pull/171699))
- Fix hardcoded OMP thread counts in `torch.compile` ([#170585](https://github.com/pytorch/pytorch/pull/170585))

## Ahead-Of-Time Inductor (AOTI)

- Batch cubin-to-obj conversion using `.incbin` assembly, dramatically reducing AOTI compile time for models with many Triton kernels (e.g., ~640x speedup on the cubin embedding phase for a 4-layer MoE with 661 cubins) ([#177864](https://github.com/pytorch/pytorch/pull/177864))
- Parallelize PTX-to-fatbin compilation when `emit_multi_arch_kernel` is enabled, saving several minutes on AOTI export for large models ([#177904](https://github.com/pytorch/pytorch/pull/177904))

## torch.fx

- Fix quadratic name generation in `_NamespaceBase.create_name`, significantly improving performance for graphs with many nodes ([#176515](https://github.com/pytorch/pytorch/pull/176515), [#177217](https://github.com/pytorch/pytorch/pull/177217))
- Propagate custom annotations to runtime asserts ([#170796](https://github.com/pytorch/pytorch/pull/170796))

## torch.export

- Skip duplicate tensor serialization when saving multiple exported programs ([#176880](https://github.com/pytorch/pytorch/pull/176880))

## ONNX

- Optimized `_jit_pass_onnx_deduplicate_initializers` from O(N^2) to O(N) ([#175888](https://github.com/pytorch/pytorch/pull/175888))

## JIT

- Cached `can_compile_class` and short-circuited type inference for ProcessGroup ([#179396](https://github.com/pytorch/pytorch/pull/179396))

## Functorch

- [FUNCTORCH] Use [] instead of list() for improved performance ([#175491](https://github.com/pytorch/pytorch/pull/175491))

## Composability

- Decomposed `mm`/`addmm` to pointwise multiply when K==1, yielding up to 1.55x speedup for outer-product-like matrix multiplications ([#175825](https://github.com/pytorch/pytorch/pull/175825))
- Improved tracing speed via the `aggressive_guard_free_semantics` config flag ([#174654](https://github.com/pytorch/pytorch/pull/174654))
- Reduced threshold for calling `sympy.factor` to 50, avoiding expensive symbolic simplification on large expressions ([#177779](https://github.com/pytorch/pytorch/pull/177779))
- Added per-SymNode expression cache, reducing redundant symbolic computation ([#175353](https://github.com/pytorch/pytorch/pull/175353))

# Documentation

## Release Engineering

- Auto-detect missing doc redirects for moved/deleted files ([#173805](https://github.com/pytorch/pytorch/pull/173805))
- Add `.nojekyll` file creation in CPP doc push script ([#179721](https://github.com/pytorch/pytorch/pull/179721))
- Simplify condition for linux-docs job ([#180391](https://github.com/pytorch/pytorch/pull/180391))
- Skip `llms-full.txt` during Sphinx builds and generate it in nightly push ([#181070](https://github.com/pytorch/pytorch/pull/181070))
- Disable `llms-full.txt` ([#181141](https://github.com/pytorch/pytorch/pull/181141))
- Fix link to C++ torch stable docs ([#181613](https://github.com/pytorch/pytorch/pull/181613))
- Use full clone for docs build to fix nightly hang ([#181661](https://github.com/pytorch/pytorch/pull/181661))
- Add checkout-mode input to setup-linux action ([#181702](https://github.com/pytorch/pytorch/pull/181702))
- Make docs build behave the same for `push=true` and `push=false` ([#181921](https://github.com/pytorch/pytorch/pull/181921))
- Reduce sidebar navigation size for generated API pages ([#181943](https://github.com/pytorch/pytorch/pull/181943))

## Python Frontend

- Documented `get_device_capability` and clarified supported dtypes ([#178397](https://github.com/pytorch/pytorch/pull/178397))
- Fixed typo in `index_copy` doc ([#175843](https://github.com/pytorch/pytorch/pull/175843))
- Updated `amax` doc ([#175863](https://github.com/pytorch/pytorch/pull/175863))
- Updated `take_along_dim` doc ([#175844](https://github.com/pytorch/pytorch/pull/175844))

## torch.nn

- Fixed varlen attention docstring ([#175261](https://github.com/pytorch/pytorch/pull/175261))
- Fixed device mismatch in `scaled_dot_product_attention` docstring example ([#178684](https://github.com/pytorch/pytorch/pull/178684))
- Fixed incorrect `attn_mask` shape in `scaled_dot_product_attention` docs ([#177999](https://github.com/pytorch/pytorch/pull/177999))
- Clarified `RMSNorm` `eps` parameter default behavior ([#173887](https://github.com/pytorch/pytorch/pull/173887))
- Improved `Conv2d` docs: clarified math variable to parameter mapping and fixed cross-correlation link ([#178965](https://github.com/pytorch/pytorch/pull/178965))

## torch.optim

- Add minimal usage example to Muon optimizer docstring (#177029) ([#177262](https://github.com/pytorch/pytorch/pull/177262))

## C++ Frontend

- Improved stable ABI docs for header-only dispatch macros and `STD_TORCH_CHECK` ([#177996](https://github.com/pytorch/pytorch/pull/177996), [#177997](https://github.com/pytorch/pytorch/pull/177997))
- Restructured C++ docs ([#174096](https://github.com/pytorch/pytorch/pull/174096))

## Distributed

- Document FSDP2 communication grouping and scheduling semantics ([#176318](https://github.com/pytorch/pytorch/pull/176318))

## CUDA

- [Typo] ot -> to ([#179265](https://github.com/pytorch/pytorch/pull/179265))
- [BE] Tesor -> Tensor ([#175061](https://github.com/pytorch/pytorch/pull/175061))
- [Typo] Quiet -> Quite ([#179266](https://github.com/pytorch/pytorch/pull/179266))
- Document public APIs using a Claude Skill ([#175578](https://github.com/pytorch/pytorch/pull/175578))

## Dynamo

- Improve `nonstrict_trace` documentation ([#172395](https://github.com/pytorch/pytorch/pull/172395))

## AOTDispatcher

- Documented supported input and output dtypes for custom ops ([#175452](https://github.com/pytorch/pytorch/pull/175452))

## Inductor

- Fix incorrect remediation instructions in cudagraph pending-backward warning ([#176865](https://github.com/pytorch/pytorch/pull/176865))

## torch.fx

- Update and correct the documentation for Cond operator ([#175419](https://github.com/pytorch/pytorch/pull/175419))

# Developers

## Release Engineering

- Update CXX_STANDARD to C++20 across build targets ([#178343](https://github.com/pytorch/pytorch/pull/178343))
- Remove legacy_nvidia_driver code ([#175363](https://github.com/pytorch/pytorch/pull/175363))
- Change default CUDA arch list to sm_7.5 ([#175574](https://github.com/pytorch/pytorch/pull/175574))
- Move binary build scripts from `.circleci/` to `.ci/pytorch/` and clean up old copies ([#175930](https://github.com/pytorch/pytorch/pull/175930), [#175915](https://github.com/pytorch/pytorch/pull/175915), [#175917](https://github.com/pytorch/pytorch/pull/175917))
- Add ARC runner label mapping config and experiment support to runner determinator ([#177803](https://github.com/pytorch/pytorch/pull/177803), [#177804](https://github.com/pytorch/pytorch/pull/177804))
- Use sccache when available for faster builds ([#175556](https://github.com/pytorch/pytorch/pull/175556))
- Standardize ninja installation to PyPI ([#179508](https://github.com/pytorch/pytorch/pull/179508))
- Remove ancient OpenSSL 1.1.1k build ([#179513](https://github.com/pytorch/pytorch/pull/179513))
- Remove stale CentOS-7 references ([#179507](https://github.com/pytorch/pytorch/pull/179507))
- Remove UCC/UCX from Docker builds ([#175607](https://github.com/pytorch/pytorch/pull/175607))

## Autograd

- Registered `numel`, `dim`, `get_device`, `storage_offset`, `is_contiguous` in `native_functions.yaml` ([#177200](https://github.com/pytorch/pytorch/pull/177200))

## torch.nn

- Added flop registration to varlen attention ([#179500](https://github.com/pytorch/pytorch/pull/179500))

## Sparse

- Included `thrust/pair.h` in each translation unit where `thrust::pair` is used ([#169267](https://github.com/pytorch/pytorch/pull/169267))
- Implemented branch-free and guard-free padding+mul operator for semi-structured sparsity ([#177699](https://github.com/pytorch/pytorch/pull/177699))

## Build Frontend

- Included `CMAKE_CUDA_FLAGS` in build settings report ([#175236](https://github.com/pytorch/pytorch/pull/175236))
- Enforced C++20 for XPU SYCL device compilation ([#179497](https://github.com/pytorch/pytorch/pull/179497))

## Distributed

- Add profiling name to NCCL collectives ([#173837](https://github.com/pytorch/pytorch/pull/173837))
- Add NCCL collective sequence number (`seq_num`) to Kineto profiler traces ([#177148](https://github.com/pytorch/pytorch/pull/177148))
- Add `RECORD_PARAM_COMMS` to symmetric memory CUDA ops for ProcessGroup metadata in profiler traces ([#178571](https://github.com/pytorch/pytorch/pull/178571))
- Capture async flag of collectives in PyTorch execution trace ([#169416](https://github.com/pytorch/pytorch/pull/169416))
- TorchComms: Flight Recorder debug server integration and hook support ([#175270](https://github.com/pytorch/pytorch/pull/175270), [#175561](https://github.com/pytorch/pytorch/pull/175561), [#178359](https://github.com/pytorch/pytorch/pull/178359))
- Refactor `NCCLDevCommManager` API design ([#177380](https://github.com/pytorch/pytorch/pull/177380))
- ROCm: Use `amdsmi` instead of `rocmsmi` for intra-node communication ([#176506](https://github.com/pytorch/pytorch/pull/176506))
- SymmMem: Improve CUDA hygiene ([#175616](https://github.com/pytorch/pytorch/pull/175616))
- SymmMem: Use host API to get NCCL peer pointer ([#176570](https://github.com/pytorch/pytorch/pull/176570))
- Split `_BackendWrapper` import to `torchcomms._backend_wrapper` module ([#177157](https://github.com/pytorch/pytorch/pull/177157), [#178352](https://github.com/pytorch/pytorch/pull/178352))
- ROCm: Enable cpp/c10d unit tests ([#169063](https://github.com/pytorch/pytorch/pull/169063))
- Fix FR script for coalesced collective not scheduled ([#177076](https://github.com/pytorch/pytorch/pull/177076))

## DTensor

- Add `_dtensor::mesh_get_process_group` custom op ([#178116](https://github.com/pytorch/pytorch/pull/178116))
- Add custom op for flattened submesh lookup during `compile_on_one_rank` tracing ([#178889](https://github.com/pytorch/pytorch/pull/178889))

## FullyShardedDataParallel2 (FSDP2)

- Fix `fully_shard` argument type hints for better type-checking consistency ([#171574](https://github.com/pytorch/pytorch/pull/171574))

## MPS

- Standardized Metal kernel compilation around `AsyncCompile` ([#179838](https://github.com/pytorch/pytorch/pull/179838))
- Removed pre-MacOS14 check from `MpsDeviceInterface` ([#175804](https://github.com/pytorch/pytorch/pull/175804)) _(from miscategorized)_

## XPU

- Enforce C++20 for XPU SYCL device compilation ([#179497](https://github.com/pytorch/pytorch/pull/179497), [#179613](https://github.com/pytorch/pytorch/pull/179613))

## Dynamo

- Repro/debug: `after_aot` repro generator in `fx_graph_runnable`, dumping resumption-frame bytecode in `tlparse`, and running the early pre-grad pass before `prepare_aot_module_simplified` ([#179657](https://github.com/pytorch/pytorch/pull/179657), [#166940](https://github.com/pytorch/pytorch/pull/166940), [#178394](https://github.com/pytorch/pytorch/pull/178394))
- Export plumbing: drop an unneeded flag from `dynamo_graph_capture_for_export` and support `torch._ops.Overload` ([#175646](https://github.com/pytorch/pytorch/pull/175646), [#175647](https://github.com/pytorch/pytorch/pull/175647))

## AOTDispatcher

- Codegen `AOTDispatchSubclassWrapper` ([#176741](https://github.com/pytorch/pytorch/pull/176741))
- Added UUID-based cache key support for pre-grad custom passes ([#177403](https://github.com/pytorch/pytorch/pull/177403)) _(from miscategorized)_

## Inductor

- Refactor `autotune_select_algorithm` to always return a `(node, choice)` tuple ([#177181](https://github.com/pytorch/pytorch/pull/177181))
- Add min/max input distance metric to scheduler nodes ([#175730](https://github.com/pytorch/pytorch/pull/175730))
- Refactor `autoheuristic_use`/`collect` to facilitate configuring/defaulting AH for different ops ([#180276](https://github.com/pytorch/pytorch/pull/180276))

## torch.fx

- Add type annotations to core torch/fx types ([#179590](https://github.com/pytorch/pytorch/pull/179590))
- Add type annotations to torch/fx `operator_schemas` and `subgraph_rewriter` ([#179761](https://github.com/pytorch/pytorch/pull/179761))
- Add type annotations to `torch/fx/experimental/migrate_gradual_types` ([#180070](https://github.com/pytorch/pytorch/pull/180070))
- Add type annotations to torch/fx proxy, interpreter, symbol ([#179718](https://github.com/pytorch/pytorch/pull/179718))
- Add type annotations to torch/fx/experimental proxy_tensor ([#179864](https://github.com/pytorch/pytorch/pull/179864))
- Improve consistency between variable name and typing annotation ([#176291](https://github.com/pytorch/pytorch/pull/176291))
- Add timing to GraphPickler.loads method ([#175440](https://github.com/pytorch/pytorch/pull/175440))
- Apply up007 and up045 to torch/fx ([#176308](https://github.com/pytorch/pytorch/pull/176308))
- Remove more undocumented functions ([#175663](https://github.com/pytorch/pytorch/pull/175663))

## JIT

- Removed `torch/csrc/utils/six.h` ([#179110](https://github.com/pytorch/pytorch/pull/179110))
- Upgraded runtime JIT/Inductor codegen to C++20 ([#176502](https://github.com/pytorch/pytorch/pull/176502)) _(from miscategorized)_

## Composability

- Deleted `size_vars` / `size_hint` API ([#175365](https://github.com/pytorch/pytorch/pull/175365))
- Changed symbolic expressions to use `FloorDiv` and `Mod` instead of `//` and `%` on SymPy exprs ([#177051](https://github.com/pytorch/pytorch/pull/177051))
- Tagged backward nodes via `_patch_autograd_grad` and updated remat pass ([#179105](https://github.com/pytorch/pytorch/pull/179105))
- Added `fast_bind` support in `normalize_function` for FakeTensor ([#175740](https://github.com/pytorch/pytorch/pull/175740))

## Caffe2

- Enabled hipsparselt in caffe2 HIP builds for ROCm ([#175810](https://github.com/pytorch/pytorch/pull/175810))
- Fixed pybind11 3.0.3 ambiguous return type deduction in caffe2 ([#179277](https://github.com/pytorch/pytorch/pull/179277))

## Developer Experience

- Added `clean` command to spin config ([#167550](https://github.com/pytorch/pytorch/pull/167550))
- Moved environment variable handling from `setup.py` to CMake ([#177640](https://github.com/pytorch/pytorch/pull/177640))

# Security

## Release Engineering

- Pin third-party GitHub Actions to SHA and extract unsafe expressions ([#178638](https://github.com/pytorch/pytorch/pull/178638))
