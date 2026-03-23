# PyTorch 2.11.0 Release Notes
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
      Added Support for <strong>Differentiable Collectives</strong> for Distributed Training
    </td>
  </tr>
  <tr>
    <td>
      <strong>FlexAttention</strong> now has a <strong>FlashAttention-4</strong> backend on <strong>Hopper</strong> and <strong>Blackwell</strong> GPUs
    </td>
  </tr>
  <tr>
    <td>
      <strong>MPS (Apple Silicon)</strong> Comprehensive Operator Expansion
    </td>
  </tr>
  <tr>
    <td>
      Added <strong>RNN/LSTM</strong> GPU Export Support
    </td>
  </tr>
  <tr>
    <td>
      Added <strong>XPU Graph</strong> Support
    </td>
  </tr>
</table>

For more details about these highlighted features, you can look at the [release blogpost](https://pytorch.org/blog/pytorch-2-11-release-blog/). Below are the full release notes for this release.

# Backwards Incompatible Changes

## Release Engineering

### Volta (SM 7.0) GPU support removed from CUDA 12.8 and 12.9 binary builds (#172598)

  Starting with PyTorch 2.11, the CUDA 12.8 and 12.9 pre-built binaries no longer include support for Volta GPUs (compute capability 7.0, e.g. V100). This change was necessary to enable updating to CuDNN 9.15.1, which is incompatible with Volta.

  Users with Volta GPUs who need CUDA 12.8+ should use the CUDA 12.6 builds, which continue to include Volta support. Alternatively, build PyTorch from source with Volta included in `TORCH_CUDA_ARCH_LIST`.

  Version 2.10:
  ```
  # CUDA 12.8 builds supported Volta (SM 7.0)
  pip install torch --index-url https://download.pytorch.org/whl/cu128
  # Works on V100
  ```

  Version 2.11:
  ```
  # CUDA 12.8 builds no longer support Volta
  # For V100 users, use CUDA 12.6 builds instead:
  pip install torch --index-url https://download.pytorch.org/whl/cu126
  ```

### PyPI wheels now ship with CUDA 13.0 instead of CUDA 12.x ([#172663](https://github.com/pytorch/pytorch/issues/172663), [announcement](https://dev-discuss.pytorch.org/t/transitioning-pypi-cuda-wheels-to-cuda-13-0-as-the-stable-release-2-11/3325))

  Starting with PyTorch 2.11, `pip install torch` on PyPI installs CUDA 13.0 wheels by default for both Linux x86_64 and Linux aarch64. Previously, PyPI wheels shipped with CUDA 12.x and only Linux x86_64 CUDA wheels were available on PyPI. Users whose systems have only CUDA 12.x drivers installed may encounter errors when running `pip install torch` without specifying an index URL.

  Additionally, CUDA 13.0 only supports Turing (SM 7.5) and newer GPU architectures on Linux x86_64. Maxwell and Pascal GPUs are no longer supported under CUDA 13.0. Users with these older GPUs should use the CUDA 12.6 builds instead.

  CUDA 12.6 and 12.8 binaries remain available via `download.pytorch.org`.

  Version 2.10:
  ```bash
  # PyPI wheel used CUDA 12.x
  pip install torch
  ```

  Version 2.11:
  ```bash
  # PyPI wheel now uses CUDA 13.0
  pip install torch

  # To get CUDA 12.8 wheels instead:
  pip install torch --index-url https://download.pytorch.org/whl/cu128

  # To get CUDA 12.6 wheels (includes Maxwell/Pascal/Volta support):
  pip install torch --index-url https://download.pytorch.org/whl/cu126
  ```

## Python Frontend

### `torch.hub.list()`, `torch.hub.load()`, and `torch.hub.help()` now default the `trust_repo` parameter to `"check"` instead of `None`. The `trust_repo=None` option has been removed. (#174101)

  Previously, passing `trust_repo=None` (or relying on the default) would silently download and run code from untrusted repositories with only a warning. Now, the default `"check"` behavior will prompt the user for explicit confirmation before running code from repositories not on the trusted list.

  Users who were explicitly passing `trust_repo=None` must update their code. Users who were already passing `trust_repo=True`, `trust_repo=False`, or `trust_repo="check"` are not affected.

  Version 2.10:
  ```python
  # Default trust_repo=None — downloads with a warning
  torch.hub.load("user/repo", "model")
  # Explicit None — same behavior
  torch.hub.load("user/repo", "model", trust_repo=None)
  ```

  Version 2.11:
  ```python
  # Default trust_repo="check" — prompts for confirmation if repo is not trusted
  torch.hub.load("user/repo", "model")
  # To skip the prompt, explicitly trust the repo
  torch.hub.load("user/repo", "model", trust_repo=True)
  ```

## torch.nn

### Add sliding window support to `varlen_attn` via `window_size`, making optional arguments keyword-only (#172238)

  The signature of `torch.nn.attention.varlen_attn` has changed: a `*` (keyword-only separator) has been inserted before the optional arguments. Previously, optional arguments like `is_causal`, `return_aux`, and `scale` could be passed positionally; they must now be passed as keyword arguments. A new `window_size` keyword argument has also been added.

  ```python
  # Before (2.10)
  output = varlen_attn(query, key, value, cu_seq_q, cu_seq_k, max_q, max_k, True, None, 1.0)

  # After (2.11) — pass as keyword argument
  output = varlen_attn(query, key, value, cu_seq_q, cu_seq_k, max_q, max_k, window_size=(-1, 0), return_aux=None, scale=1.0)
  ```

### Remove `is_causal` flag from `varlen_attn` (#172245)

  The `is_causal` parameter has been removed from `torch.nn.attention.varlen_attn`. Causal attention is now expressed through the `window_size` parameter: use `window_size=(-1, 0)` for causal masking, or `window_size=(W, 0)` for causal attention with a sliding window of size `W`. The default `window_size=(-1, -1)` corresponds to full (non-causal) attention.

  ```python
  # Before (2.10)
  output = varlen_attn(query, key, value, cu_seq_q, cu_seq_k, max_q, max_k, is_causal=True)

  # After (2.11) — use window_size instead
  output = varlen_attn(query, key, value, cu_seq_q, cu_seq_k, max_q, max_k, window_size=(-1, 0))
  ```

## Distributed

### `DebugInfoWriter` now honors `$XDG_CACHE_HOME` for its cache directory in C++ code, consistent with the Python side. Previously it always used `~/.cache/torch`. (#168232)

  This avoids issues where `$HOME` is not set or not writable. Users who relied on `~/.cache/torch` being used regardless of `$XDG_CACHE_HOME` may see debug info written to a different location.

  Version 2.10:
  ```
  # C++ DebugInfoWriter always wrote to ~/.cache/torch
  ```

  Version 2.11:
  ```
  # C++ DebugInfoWriter now respects $XDG_CACHE_HOME/torch (same as Python code)
  # Falls back to ~/.cache/torch if $XDG_CACHE_HOME is not set
  ```

### `DeviceMesh` now stores a process group registry (`_pg_registry`) directly, enabling `torch.compile` to trace through `get_group()`. (#172272)

  This may break code that skips `init_process_group`, loads a saved DTensor (constructing a DeviceMesh with no PGs), and later creates PGs separately — during `torch.compile` runtime the PG lookup will fail. Users should ensure process groups are initialized before constructing the DeviceMesh.

  Version 2.10:
  ```python
  # PGs resolved via global _resolve_process_group at runtime
  mesh = DeviceMesh(...)  # PGs could be created later
  ```

  Version 2.11:
  ```python
  # PGs now stored on DeviceMesh._pg_registry; must exist at mesh creation
  dist.init_process_group(...)  # Must be called before creating mesh
  mesh = DeviceMesh(...)
  ```

## Distributed (DTensor)

### `DTensor.to_local()` backward now converts `Partial` placements to `Replicate` by default when `grad_placements` is not provided. (#173454)

  Previously, calling `to_local()` on a `Partial` DTensor would preserve the `Partial` placement in the backward gradient, which could produce incorrect gradients when combined with `from_local()`. Now, the backward pass automatically maps `Partial` forward placements to `Replicate` gradient placements, matching the behavior of `from_local()`.

  Users who relied on the previous behavior (where `to_local()` backward preserved `Partial` gradients) may see different gradient values. To ensure correctness, explicitly pass `grad_placements` to `to_local()`.

  Version 2.10:
  ```python
  # Partial placement preserved in backward — could produce incorrect gradients
  local_tensor = partial_dtensor.to_local()
  ```

  Version 2.11:
  ```python
  # Partial → Replicate in backward by default (correct behavior)
  local_tensor = partial_dtensor.to_local()
  # Or explicitly specify grad_placements for full control:
  local_tensor = partial_dtensor.to_local(grad_placements=[Replicate()])
  ```

### `_PhiloxState.seed` and `_PhiloxState.offset` now return `torch.Tensor` instead of `int` (#173876)

  The DTensor RNG internal `_PhiloxState` class changed its `seed` and `offset` properties to return tensors instead of Python ints, and the setters now expect tensors. This makes the RNG state compatible with PT2 tracing (the previous `.item()` calls were not fake-tensor friendly).

  Code that directly reads `_PhiloxState.seed` or `_PhiloxState.offset` and treats them as ints will break. Call `.item()` to get the int value. When setting, wrap the value in a tensor.

  Version 2.10:
  ```python
  from torch.distributed.tensor._random import _PhiloxState

  philox = _PhiloxState(state)
  seed: int = philox.seed          # returned int
  philox.offset = 42               # accepted int
  ```

  Version 2.11:
  ```python
  from torch.distributed.tensor._random import _PhiloxState

  philox = _PhiloxState(state)
  seed: int = philox.seed.item()   # now returns Tensor; call .item() for int
  philox.offset = torch.tensor([42], dtype=torch.int64)  # must pass Tensor
  ```

## ROCm

### caffe2 support is fully removed from ROCm PyTorch's hipify preprocessing. This is known as "hipify v2" behavior. (#174087, #174300, #174388, #174499, #175098)
#### hipify v1 background
When caffe2 and PyTorch were separate projects, the ROCm support strategies were different.  For caffe2, all files and classes would be renamed following the pattern of CUDA to HIP, Cuda to Hip, cuda to hip, and so on.  PyTorch did not rename classes, but would create new files following the same renaming pattern (e.g., aten/src/ATen/cuda/CUDABlas.h to aten/src/ATen/hip/HIPBlas.h).  As a consequence, caffe2 had a distinct device backend named "HIP" (renamed from "CUDA") while ROCm PyTorch masquerades as the "cuda" device (`torch.empty(1, device="cuda")`).  Once caffe2 and PyTorch projects were merged, this caused a mismatch between caffe2 expecting to use a "HIP" device while PyTorch expecting a "cuda" device.  To alleviate this mismatch, "Masquerading" classes were created under aten/src/ATen/hip/impl.
- HIPAllocatorMasqueradingAsCUDA.h
- HIPCachingAllocatorMasqueradingAsCUDA.h
- HIPGuardImplMasqueradingAsCUDA.h
- HIPStreamMasqueradingAsCUDA.h
These classes were often transparently utilized during ROCm PyTorch's hipify preprocessing of source files.  All files under c10/ and caffe2/ were hipified using the caffe2 renaming behavior, while all other "PyTorch" files used the other strategy.  The Masquerading classes would replace their CUDA counterpart during hipify preprocessing.  For example, c10/cuda/CUDAStream.h's CUDAStream would be replaced by aten/src/ATen/hip/impl/HIPStreamMasqueradingAsCUDA.h's HIPStreamMasqueradingAsCUDA.  These Masquerading classes call the underlying caffe2 code and create "HIP" devices, and the device would be reset to "cuda" by the Masquerading classes.
#### hipify v2 new behavior
Hipify v2 (#174087, #174300, #174388, #174499, #175098) makes the following changes:
- "Masquerading" classes are deprecated. Reworked to be thin shells around existing classes, for backward compatibility.
- Do not rename "CUDA" classes to "HIP". Only rename CUDA Runtime APIs. Files are still renamed out of place.
- Removes caffe2 work-arounds for HIP device versus CUDA device.
Great care has been taken to make this change backwards compatible.  Though PyTorch today builds cleanly using hipify v2 behavior, downstream PyTorch extension projects that explicitly included Masquerading headers or called Masquerading APIs could be affected, resulting in failed builds.  As an example, before backwards compatibility was realized, the xformers project had failed to build using the hipify v2 changes.  A [PR demonstrates the changes that were initially necessary to work around the build failures,](https://github.com/facebookresearch/xformers/pull/1351) but such changes are no longer necessary after hipify v2 BC-breaking behavior was improved.

## torch.export

### `torch.export.export_for_training` has been removed (#171714)

  `export_for_training` was previously available as a separate API for exporting models while preserving training semantics. This function has been removed. Users should use `torch.export.export` instead, which returns the same graph as the previous `export_for_training`.

## ONNX

### **Remove the `fallback` option from `torch.onnx.export`** (#173189)

  The `fallback` parameter has been removed from `torch.onnx.export()`. Previously, when `fallback=True`, the exporter would automatically fall back to the legacy TorchScript-based exporter if the dynamo exporter failed. This fallback was removed because it was overly complicated, required different inputs, produced different models, and hid errors from the new exporter.

  **Migration:** Remove `fallback=True` (or `fallback=False`) from your `torch.onnx.export()` calls. If you need fallback behavior, implement it explicitly in your own code by catching exceptions and calling the legacy exporter separately.

  ```python
  # Before
  torch.onnx.export(model, args, "model.onnx", dynamo=True, fallback=True)

  # After
  torch.onnx.export(model, args, "model.onnx", dynamo=True)
  ```

### **Remove overload matching logic from the ONNX dispatcher** (#165083)

  The `custom_translation_table` parameter in `torch.onnx.export()` no longer accepts a list of functions for each torch op. Previously, users could pass a list of overloaded ONNX functions (e.g., one for float tensors, another for bool tensors), and the dispatcher would automatically select the correct overload based on input types. This complex type-matching logic has been removed because torchlib no longer uses overloads for the same opset version.

  The type of `custom_translation_table` changed from `dict[Callable, Callable | Sequence[Callable]]` to `dict[Callable, Callable]`. Passing a `Sequence` as a value now raises a `TypeError`.

  **Migration:** Provide a single function per operator instead of a list of overloads. If you need type-dependent behavior, handle it inside the single function.

  ```python
  # Before
  custom_translation_table = {
      torch.ops.aten.logical_and.default: [custom_impl_float, custom_impl_bool],
  }

  # After
  custom_translation_table = {
      torch.ops.aten.logical_and.default: custom_impl,
  }
  ```

## Quantization

### The PT2E quantization flow (`torch.ao.quantization.pt2e` and `torch.ao.quantization.quantizer`) has been removed from PyTorch and migrated to [torchao](https://github.com/pytorch/ao). (#169151)

  The following modules and classes have been removed:
  - `torch.ao.quantization.pt2e` (including `DuplicateDQPass`, `PortNodeMetaForQDQ`, export utils, graph utils, numeric debugger, lowering utilities)
  - `torch.ao.quantization.quantizer` (including `ComposableQuantizer`, `EmbeddingQuantizer`, `X86InductorQuantizer`, `XPUInductorQuantizer`, `XNNPACKQuantizer`, `QuantizationSpec`, `QuantizationAnnotation`, `QuantizationConfig`, etc.)

  Users relying on the PT2E quantization flow should migrate to the `torchao` package, which now hosts these APIs.

  Version 2.10:
  ```python
  from torch.ao.quantization.pt2e import prepare_pt2e, convert_pt2e
  from torch.ao.quantization.quantizer.x86_inductor_quantizer import X86InductorQuantizer
  ```

  Version 2.11:
  ```python
  # Install torchao: pip install torchao
  from torchao.quantization.pt2e import prepare_pt2e, convert_pt2e
  from torchao.quantization.pt2e.quantizer.x86_inductor_quantizer import X86InductorQuantizer
  ```


# Deprecations

## Linear Algebra

- The MAGMA backend for linear algebra operations is now deprecated and will be removed in a future release. Setting `torch.backends.cuda.preferred_linalg_library("magma")` or retrieving a previously-set MAGMA preference will now issue a deprecation warning. cuSOLVER remains the default backend. (#172823)

  If you see any errors when using cuSOLVER that did not occur with MAGMA, please file an issue on GitHub. To silence the warning, stop explicitly selecting the MAGMA backend:

  Version 2.10:
  ```python
  # No warning
  torch.backends.cuda.preferred_linalg_library("magma")
  ```

  Version 2.11:
  ```python
  # Issues a deprecation warning — remove this call to use the default cuSOLVER backend
  torch.backends.cuda.preferred_linalg_library("magma")
  ```

- `torch.linalg.svd` no longer dispatches to MAGMA. The MAGMA backend is deprecated and cuSOLVER is now used unconditionally, providing significant speedups (2x–400x depending on matrix size and batch dimensions). (#172824)

  Previously, setting `torch.backends.cuda.preferred_linalg_library("magma")` would route SVD through MAGMA. This setting is now ignored for SVD, and cuSOLVER is always used.

  Version 2.10:
  ```python
  torch.backends.cuda.preferred_linalg_library("magma")
  U, S, Vh = torch.linalg.svd(x)  # Uses MAGMA
  ```

  Version 2.11:
  ```python
  # MAGMA preference is ignored; cuSOLVER is always used
  U, S, Vh = torch.linalg.svd(x)  # Uses cuSOLVER
  ```

- `torch.linalg.solve_triangular` and `torch.triangular_solve` no longer dispatch to MAGMA on CUDA. cuBLAS is now used unconditionally, providing speedups of 2x–24x for most matrix sizes (small matrices may see minor regressions of ~0.6x). (#174109)

  Version 2.10:
  ```python
  torch.backends.cuda.preferred_linalg_library("magma")
  torch.linalg.solve_triangular(A, B, upper=False)  # Uses MAGMA
  ```

  Version 2.11:
  ```python
  # MAGMA preference is ignored; cuBLAS is always used
  torch.linalg.solve_triangular(A, B, upper=False)  # Uses cuBLAS
  ```

- `torch.linalg.lstsq` no longer dispatches to MAGMA. cuSOLVER/cuBLAS are now used unconditionally, providing speedups of 1.7x–620x depending on matrix size and batch dimensions. (#174779)

  Version 2.10:
  ```python
  torch.backends.cuda.preferred_linalg_library("magma")
  result = torch.linalg.lstsq(A, B)  # Uses MAGMA
  ```

  Version 2.11:
  ```python
  # MAGMA preference is ignored; cuSOLVER/cuBLAS is always used
  result = torch.linalg.lstsq(A, B)  # Uses cuSOLVER/cuBLAS
  ```

## Distributed

### `torch.distributed.symmetric_memory.enable_symm_mem_for_group` is deprecated. The store can be retrieved directly via `ProcessGroup.getStore()` in C++, making this call unnecessary. (#172163)

  Version 2.10:
  ```python
  from torch.distributed.symmetric_memory import enable_symm_mem_for_group
  enable_symm_mem_for_group(group)
  ```

  Version 2.11:
  ```python
  # No longer needed — store is accessed directly from the ProcessGroup
  ```




# New features

## Python Frontend
- Added `native_handle` property to `torch.Stream`, providing a unified way to retrieve the backend-specific opaque stream handle (e.g., `cudaStream_t` for CUDA, `sycl::queue*` for XPU). This is useful for passing stream handles to third-party libraries such as Triton. (#171040)

  ```python
  stream = torch.accelerator.current_stream()
  handle = stream.native_handle  # backend-specific stream handle
  ```
## Autograd
- Add `Function.clear_saved_tensors_on_access` class attribute to automatically free saved tensors after they are accessed (#173833)
## torch.nn
- Add mechanism to restore default flash attn impl after `activate_flash_attention_impl` (#169866)
- Add `scale` for softmax to varlen attn (#171199)
## Distributed
- Add `start_method` option to `torch.distributed.debug.start_debug_server` to select the multiprocessing start method (`fork`, `spawn`, or `forkserver`), enabling CUDA-safe server startup (#173196)
- Add support for periodic dumping in `torch.distributed.debug` (#174808)
- Non-functional collectives (e.g. `torch.distributed.all_gather`) now automatically work with `FakeTensorMode` — meta implementations are registered at `import torch` time (#162119)
- Implement NCCL 2.29 one-sided APIs for symmetric memory (#172425)
- Bind `SymmetricMemory` as a torch class for use in op definitions (#174019)
- Enable `torchcomms` `_BackendWrapper` shim layer in c10d (#174202)
- Expose SymmetricMemory window API (#170740)
## CUDA
- Make (pinned) host memory allocations work with memory pools. (#167507)
- Make large segment size configurable for allocation performance tuning (esp. re: Expandable Segments). (#172056)
## MPS
- Async error reporting from GPU operations (#170002, #170050)
    ```python
    import torch
    x = torch.rand(10, 1, 10, device='mps')
    y = x[:, [1]]
    torch.mps.synchronize()  # will raise index out of bounds error
    ```
- Added support for Metal 4 (#172229, #172230)
## ROCm
- Expose device properties `clock_rate`, `memory_clock_rate`, `memory_bus_width`, `memory_per_block`, `shared_memory_per_block`. (#170572)
- Support for device-side assertions via `TORCH_USE_HIP_DSA`. (#172679)
- Attention operator support on gfx1151/1152/1153 via AOTriton 0.11.2b update (#174105)
- Enable scaled group mm on gfx950. (#173737)
- Enable group gemm on gfx90a. (#169356)
- Enable MIOpen backend for CTC Loss. (#170749)
- Add hipsparseSpSV and hipsparseSpSM support for triangular solve. (#171097)
- Support for PyTorch's StaticCudaLauncher, which provides static compilation and launching of Triton kernels. (#166492)
## XPU
- Introduce XPUGraph, a runtime optimization feature designed to reduce kernel host overhead on XPU devices, detail in: [design](https://github.com/pytorch/pytorch/issues/162143) and [usage](https://docs.pytorch.org/docs/2.11/xpu.html#graphs). (#166285, #174041, #174351, #174059, #174046, #166843)
## torch.compile
#### Dynamo
- `torch.compile` now supports tracing through `contextlib.ExitStack` and `contextlib.suppress` context managers, allowing code that uses these patterns to be compiled without graph breaks (#146506, #147990)
- Added `torch._dynamo.config.ignore_logging_functions` config to skip arbitrary logging callables during tracing without causing graph breaks. Add functions to this set to have Dynamo treat them as no-ops during compilation (#168913)
- Added `TORCH_DYNAMO_AUTOMATIC_DYNAMIC_SHAPES=0` environment variable to globally disable automatic dynamic shapes without modifying Python code (#172334)
- Added `TORCH_COMPILE_OVERRIDE_BACKENDS` environment variable for per-graph backend override, enabling binary search to find problematic compiled graphs. Supports filter syntax like `">10:eager"` or `"0-5:aot_eager;6-10:inductor"` (#172411)
- Added initial support for `torch._dynamo.decorators.leaf_function`, which allows annotating functions as leaf operations that Dynamo and AOTAutograd will not trace into (#170471)
- Added support for tracing backward hooks on intermediate tensors, fixing cases where `register_hook` on non-leaf tensors would fail under `torch.compile` (#172126)
#### Inductor
- FlexAttention supports deterministic mode, wired through both Flex and Flash backends (#173126)
- Added range-based autotuning for custom ops, enabling selection of optimal implementations based on runtime tensor dimension values with per-range benchmarking and automatic `torch.cond` dispatch generation (#167617)
- FlexAttention: Added support for low precision K/V inputs in compiled mode. Keys and Values can now be in lower precision than Queries for memory efficiency (#171761)
- Added native `ldexp` lowering with `libdevice.ldexp` (CUDA) and `std::ldexp` (CPU) codegen (#171721)
- Inductor now supports `pin_memory` for `torch.empty` (#172578)
- Exposed `triton_meta` to TritonTemplate `maybe_append_choice` API for custom template development (#174292)
- Added Async Pipelined Autotuning for `max-autotune-gemm`, which overlaps autotuning with lowering/scheduling in a subprocess to reduce compilation overhead (#170407)
- FlexFlash: Added BlockSparse backward pass, dynamic shapes, and backward score-mod support (#170397, #170611, #171465)
- Added FP8 `(BlockWise128x128, BlockWise1x128)` scaling support in Inductor Triton templates (#170748)
- Autochunker: Added gradient accumulation support and ability to override number of chunks (#171359, #171477)
- Added NVGEMM backend for GEMM operations using NVIDIA's native matmul library, with support for BMM, grouped GEMM, scaled MM, dynamic shapes (#171205, #171362, #172280, #172283, #172378, #172388, #172391, #172402, #172417, #172525, #172582, #172607, #174827)
## torch.export
- Add nested tensor serialization support for `torch.export` (#174720)
- RNN modules (LSTM, GRU, etc.) can now be exported on GPUs (#169710)
- Add patch to enable tracing LSTM with dynamic shapes (#168095)
## ONNX
- Added `ExportableModule` wrapper for ONNX export (#170810)
- Added `InputObserver` to infer dynamic shapes for export (#172838)
- Add a parameter to force the first dimension to be dynamic in InputObserver.infer_dynamic_shapes (#173533)
- Implement while_loop (#162645)
- Add invoke_subgraph HOP export support (#174283)
- Expose ONNXProgram.rename_axes for renaming dims (#172032)
- Support custom empty tensor shapes in `InputObserver` for multimodal LLM export (#174964)
## Foreach
- Added `torch.linalg._powsum` and `torch._foreach_powsum` as fused kernels that compute `sum(abs(x)**ord)` (equivalent to `vector_norm` without the root extraction) (#172685)




# Improvements
## Release Engineering
- Upgrade to ROCm 7.2 with new Docker images, magma tarball, and binary builds (#173096, #173106, #173187, #174234)
- Add an option to install cuda if required cuda/cudnn on windows AMI do not match (#177273)
## Python Frontend
- `torch.load` now produces clearer error messages when encountering miniz errors from `PyTorchStreamReader`, explicitly indicating that the checkpoint file is likely corrupt (#170244)
- `torch.load(map_location='meta')` no longer reads storage data from the filesystem, improving performance when loading checkpoints onto the meta device (#170619)
## Composability
- Add `check_out_variant` and `to_out_variant` utilities for custom operator out variant validation. `check_out_variant` verifies that a custom op's out variant is compatible with Inductor's out_variant pass, and `to_out_variant` converts an `OpOverload` to its out variant. (#174473)
## torch.nn
- Add `remove_duplicate` parameter to `nn.Module.modules()` function (#174383)
- Add support for low precision K/V inputs to `nn.attention.flex_attention` (#171744)
## C++ Frontend
- Added support for `Float8_e8m0fnu` and `Float4_e2m1fn_x2` dtypes to stable ABI (#173669)
- Added `torch::stable::Tensor::layout()` (#174735)
## Distributed
- Set thread name for Gloo internal loop for easier debugging (#169979)
- Make `context_parallel_shard` more general (#170200)
- Polish NCCL symmetric memory code (#170582)
- Add MemPool support for NCCL symmetric memory backend (#171727)
- Extend symmetric memory barrier to both LSA and GIN (#172701)
- Implement `get_offset` for symmetric memory (#172044)
- `ProcessGroupNCCL`: workaround for `reduce_scatter` with `world_size=1` (#170922)
- Add XCCL backend support for `ProcessGroupWrapper` (#171920)
- Lazy import `pdb` only when user calls `breakpoint()` in `torch.distributed` (#171818)
- Remove MB < PP check for GPipe pipeline schedule (#171462)
- Pass DDP bucket cap size list for finer-grained control (#169026)
- Enable ProcessGroup round-trip through JIT via CapsuleType (#172794)
- Don't repeatedly log environment variables (#170399)
- Set NCCL group desc before creating comm so it propagates (#171159)
- `ProcessGroupNCCL`: use lowest rank as split color (#173687)
#### DTensor
- Add OpSchema.args_meta, kwargs_meta helpers (#170358)
- Support misc sym ops (#172268)
- DTensor Ops: Add linearity support for neg operation (#172563)
- Add SymInt support for DTensor mesh coordinate computation in PT2 (#169552)
- Enable single-dim strategy for addmm and baddbmm (#172387)
- Support uneven _StridedShard redistribution (#172266)
- Update TP api to support single-dim strategies (#173567)
- Initial support for decomps + sharding prop (#171652)
- Add shard prop cache logging (#173775)
- Optimize redistribute comms using flattened meshes (#174630)
## CPU
- Added support for FP16 half-precision GEMM via OpenBLAS on CPU, enabling faster FP16 inference (#169042)
## CUDA
- Remove _scaled_mm layout check on Blackwells (#170693)
- Add uint16, uint32, uint64 support to JIT CUDA kernels (#174303)
- Remove fallback paths for pinned memory allocation during CUDA graph capture (#170710)
- Improve numerics of UpSample kernel by using `accscalar_t` for interpolation accumulators (#170661)
- Reinstate error message details in CUDA_KERNEL_ASSERT_VERBOSE call in IndexKernelUtils.cu (#170913)
- Switch order of blocked reduce in reduction_template.cuh (#173425)
## cuDNN
- Upgrade cuDNN to 9.15.1 for CUDA 13 builds (#169412)
- Upgrade CUDA 13.0 wheels to cuDNN 9.17.1 (#173216)
- Enhance cuDNN tensor shape checks in sdp_utils.cpp to support Blackwell GPUs (#172621)
## MPS
- Improved support for distributions operations (#172187, #172675, #173287)
- Enabling `index_fill` backward pass (#174238)
- Extended `baddbmm` and `addbmm` to integer and complex types (#170895)
- Improved error messages for distributed ops on MPS (#173954)
- Added MPS support for `torch.special.erfcx` (scaled complementary error function) (#172910)
## ROCm
- `addmm` behavior now takes into account preferred BLAS backend instead of forcing hipblaslt. (#174350)
- Enable hipBLASLt on gfx1103. (#172180)
## Sparse Frontend
- `torch.view_as_real` and `torch.view_as_complex` now support sparse tensors (#164964)
- Sparse tensor invariants check warning is now raised only once when the check is disabled, instead of on every operation (#171695)
## XPU
- Add `torch.xpu._dump_snapshot` API (#170186)
- Add `torch.xpu._record_memory_history` API (#169559)
- Add `torch.xpu.memory_snapshot` (#169442)
- Add `local_mem_size` to XPU device properties (#172314)
- Support `torch.accelerator.get_device_capability` on XPU (#170747)
- Enable Triton online softmax kernels on XPU (#163251)
- Support woq_int8 Inductor pattern on Intel GPU (#163615)
- Add XPU ATen GEMM overloads with output dtype (#170523)
- Support `aot_inductor.emit_multi_arch_kernel` on XPU (#171432)
- Improve Inductor UT coverage for XPU (#171280, #166376, #169181, #166504)
- Enable Triton mm template `decompose_k` choice for XPU (#170541)
- Support AOTInductor standalone compile API for XPU (#171450)
## Profiler
- The memory visualizer now has a checkbox to toggle showing the trace, useful for large traces that take
a long time to load (#174717). The memory profiler
now exposes a new `skip_actions` flag to filter out specific events (#168183).
- The profiler now exposes a `post_process_timeout_s` field to prevent post processing from blocking
further execution (#173957).
## torch.compile
#### Dynamo
- Suppressed repeated "triton not found" messages during import — previously 12 identical warnings were printed (#172614)
- `fullgraph=True` now recursively disables dynamo on compiled code to prevent unintentional re-invocation of `torch.compile` (#173080)
- Miscellaneous smaller tracing support additions:
  - Support for `Enum.__contains__` and constants (#173223)
  - Updated nn module hook handling to work with `kwargs=True` (#172519)
  - Support `object` type in dynamo tracing (#171457)
- Add args print support to hop print (#170880)
- Don't register einops ops with `allow_in_graph` (#173611)
#### Inductor
- Improved heuristics for reduction kernels (#170931)
- CUDAGraph partitioning now supports cudagraph-unsafe symints (#173159)
- MixOrderReduction: Added low precision reduction support, non-strict mode, and avoid recompile (#169978, #171941, #174947)
- Triton compilation timeout is now configurable and defaults to 5 minutes (lowered from previous default) (#172674)
- User stack traces are now reported when a `LoweringException` occurs, making debugging easier (#171846)
- Added B300 (Blackwell) support: GPU architecture `120a` for `.ptx` to `.fatbin` compilation and cpp codegen (#174162, #172263)
- Autotune process pool now inherits tf32 options from the parent process (#174742)
- Epilogues can now be statically analyzed for fusion decisions (#170001)
- Added `cvt_e8m0_rceil` prim with PTX lowering for SM100+ GPUs (#172497)
- Basic comm buffer reuse for Symmetric Memory (#171909)
- Added `launch_cooperative_grid` flag for cooperative reduction kernels (#167800)
- Updated CUTLASS codegen to support `torch.float8_e5m2`, enabling mixed FP8 (e4m3fn x e5m2) matrix multiplication (#171167)
- Improved mkldnn convolution layout propagation in Inductor (#169260)
- Optimal Epilogue fusion overlapping with Async Pipelined Autotuning (#171011)
- FlexAttention improvements: Enabled SM90 blocksparse backwards, updated configuration for Thor and DGX Spark hardware, and enabled TMA path by default on Intel GPU (#171685, #173898, #172316)
- Added support for torchcomms lowering in inductor IR (#171634)
- Allow int8 layout dtype for cpp gemm template on CPU (#169161)
- Improved batch matmul codegen (#172678)
- Improved error message in standalone_compile when there are no aot_autograd artifacts (#174086)
- Removed unnecessary synchronize before launcher creation (#169432)
- Removed implicit float64 upcast in Triton codegen, improving performance and reducing unnecessary precision casting (#172143)
- Added torch.compile compatibility to FP8 SDPA using FlashAttention3, including meta registration and inductor lowering fallback for the new `scaled_dot_product_flash_attention.low_p` overload (#172622)
- Replace `record_function` with `_RecordFunctionFast` in CompiledFxGraph for reduced profiling overhead (#163976)
- Relaxed restriction on triton template `mutated_inputs`, allowing more flexible template usage (#170721)
- Added `combo_kernels_pointwise_only` config option to exclude reduction kernels from combo kernel fusion (#174894)
- Add a fusion region utility for grouping inductor fusible nodes for aten estimation (#170559)
- Pallas backend: Added support for pooling with strided indexing, masked operations, random, FloorDiv, flattened indexing, welford fallback, ModularIndexing, transpose, im2col gather pattern detection, element-wise pairing, sympy min/max, FMA, automatic padding to WARPGROUP_SIZE, atomic_add store mode, TMA for OOB masking on Mosaic GPU, jax/cuda stream sync, better iter var tracking, and interleaved rope (#170014, #170145, #170221, #170222, #170232, #170595, #170616, #170627, #170738, #170741, #171449, #171475, #171518, #171539, #171567, #172306, #173840, #174249, #174797)
- Add per-graph inductor config override for debugging/bisecting (#174228)
## torch.fx
- `torch.fx.symbolic_trace` now supports tracing `HigherOrderOperator`s that do not take callable arguments (#173839)
- Rename `hint_int` to `size_hint`, support `size_hint` in user code. (#171944)
- Add metadata hook for all nodes created in runtime_assert pass (#173970)
- Add `_disable_torch_fn_metadata_mode` option to `make_fx` and `aot_export_joint_with_descriptors` (#172087)
- Add nested value-type opaque object support (#169845)
## torch.export
- `from_node` provenance information is now preserved when serializing exported programs (#171726)
- Bitwise shift operations are now supported in the export serializer (#167913)
- Improve leak detection in non-strict export mode (#172597)
## Quantization
- Use `expm1` for computing quantized ELU, improving numerical stability (#173968)
## ONNX
- Implement torch.sym_sum and torch.sym_ite (#170263)
- Raise an error if there are duplicated input/output names (#173077)
- Refactor optimize and version conversion logic (#173185)
## Optimizer
- Optimizer graph capture check now supports XPU devices in addition to CUDA (#172759)
## DevX
- The `spin lint` command now supports pass-through arguments to lintrunner, including `--take`, `--skip`, and `--tee-json` flags, giving developers more control over which linters run (#169373)
## Ahead-Of-Time Inductor (AOTI)
- Better error message for mixed device tensors (#173982)
- Support mixed-device constants (#169504)
- Change `cpp_kernel_name` to public API to match AOTI shim gen; add `mm_type_out` to AOTI fallback kernel (#174489)




# Bug fixes
## Release Engineering
- Fixed macOS wheel metadata where setuptools misinterpreted the platform version string, producing incorrect wheel tags for macOS arm64 builds (#173541)
- Fixed incorrect wheel naming (#173945)
- Fixed macOS arm64 libtorch release upload failure (#175100)
- Fix pep517 release handling (#175635)
## Python Frontend
- Fixed a bug where `torch.load` with `FakeTensorMode` or `skip_data` context would compute incorrect storage sizes (#170618)
- Fixed PrivateUse1 backend aliasing during deserialization so custom backends are correctly recognized when loading checkpoints (#165456)
- Fixed `torch.ops.aten.index.Tensor` to properly raise an `IndexError` when called with an empty indices list, instead of producing undefined behavior (#174009)
## Autograd
- Fixes absolute tolerance scaling for complex backpropagation in `torch.autograd.gradcheck` when `fast_mode=True` (#166386)
## Complex Frontend
- Fixed `torch.view_as_complex()` not working on the memory layout produced by `.contiguous()` after `.transpose()` (#169780)
## Composability
- Fix `torch.bucketize` crash during `torch.export` when `test_elements` is a scalar (#170751)
- Fix `MaxUnpool` crash when input tensors are small (#169359)
## Dataloader
- Fix DataLoader to respect overridden `__getitem__` in Subset subclasses (#163961)
## Nested Tensor (NJT)
- Fix NestedTensor min/max operations for integer dtypes (#167685)
## torch.nn
- Fix Illegal Memory Access in FlashAttention 2 by syncing with upstream (#174114)
- Propagate `max_q` and `max_k` for `varlen_attn` (#173681)
## C++ Frontend
- Fixed bug in stable ABI shim to handle special types (`SymInt`, `MemoryFormat`, `ScalarType`, `Layout`) correctly (#174734)
## Distributed
- Add half precision binding for MPI backend (#170074)
- Fix incorrect boolean logic in `std::string::find` method in c10d (#170057)
- Fix `_set_pg_timeout` not working for Gloo backend (#167052)
- Fix DeviceMesh corner case for coalesce in cute layout and mesh slicing (#169454)
- Fix Context Parallel `flex_input_fn` argument unwrapping issue (#170201)
- Fix FSDP `_unshard()` passing `Stream` instead of `Event` (#170525)
- Ensure threadblock size >= world size in CUDA symmetric memory barrier (#170785)
- Fix `ProcessGroupGloo` CUDA tensor stream handling with futures (#170812)
- Fix env variable to retrieve HCA list for NVSHMEM (#170891)
- Fix FSDP `split_with_sizes_copy()` missing `dim` argument (#169173)
- Fix cross-thread work registry lookup in `wait_tensor` (#171614)
- Fix `fully_shard` arg typehint inconsistency (#171574)
- Fix Flight Recorder default buffer size inconsistency (#172843)
- Remove mixed dtype rejection for `clip_grad_norm` to align with documentation (FSDP) (#173641)
- Fix all-reduce strides in compiled code (#171616)
- Fix `ProcessGroupWrapper` missing method forwarding (#173599)
- Fix syntax for suppression comments. (#167088)
#### Distributed Checkpoint (DCP)
- Fix TypedStorage deprecation warning in distributed checkpoint (#170759)
- Fix typo in variable name from 'statetful_sd' to 'stateful_sd' (#171292)
#### DTensor
- Preserve `Partial(max/min)` reduce op type on `torch.max`/`torch.min` output DTensors (#170203)
- Prevent pointwise operations between `Partial` DTensors with different reduce ops (#170209)
- Fix OpInfo.schema type and add asserts (#170790)
- Fix _StridedShard(sf=) bug in single dim strategy (#171942)
- Fix incorrect Tensor Meta Population (#172304)
- Single_dim fix symint + _create_expanded_strategy (#172421)
- Single dim fix inplace op expansion (#172477)
- Fix single-dim output_meta validation (#172293)
- Fix redistribute cost crashing on non-participating ranks (#172478)
- Fix t() sharding strategy for 1D tensors (#173964)
- Fix unsupported op error (#170889)
- Fix DTensor honor single-dim RuntimeSchemaInfo (#174312)
- Fix device_mesh extraction from kwargs (#173489)
- Fix StridedShard usage conflict with shard order (#174831)
- Fix bucketize with Partial inputs (#173937)
- Fix embedding_dense_backward cache key missing num_weights (#174727)
#### FullyShardedDataParallel2 (FSDP2)
- Fix mixed DTensor error with nested FSDP and activation checkpoint (#171779)
## CUDA
- Don't false-positive on record_stream and account for 0-element tensors in CUDA stream sanitizer (#172562)
- Fix failures due to launch bounds for `ctc_loss_gpu_template` on SM12+ (#172447)
- Fix the torch.Stream context manager reentrance (#176568)
## cuDNN
- Disable a cuDNN Convolution engine preemptively (#171747)
## MPS
- Fixed non-contiguous grid sampler on MPS (#171619)
- Fixed large reductions when compiling for MPS (#171479)
- Fixed MPS Inductor `tanh` implementation (#172406)
- Fixed complex to real power scalar on MPS (#174147)
- Fixed masked op logic in MPS Inductor (#170134)
- Fixed `orgqr` race condition on MPS (#174143)
- Fixed 2-pass SDPA memory corruption by forcing float accumulators, resolving nondeterministic/corrupt results with bf16/fp16 and GQA when seq_len > 1023 (#174945)
- Fix half-precision type mismatches in Metal shader codegen (#176436)
## ROCm
- Sliding window attention NaN issue is fixed by AOTriton 0.11.2b. (#173204, #174105)
- Increase the event_name attribute of autograd's profiler_util.py to avoid truncation of long HIP events. (#174366)
- Cholesky operator via MAGMA was missing a sync operation. (#172112)
- Updated patched libdrm in bundled release wheels to avoid missing amdgpu.ids warning and properly return AMDGPU marketing names. (#174811)
- Fix fake_quantize undefined behavior with inf. (#171777)
- Fix deterministic scan kernel edge case. (#170763)
- Use torch's caching allocator for CK workspaces, for better memory behavior and hipGraph capture. (#172311)
- Fixes grouped gemm 2d2d for edge cases with uninitialized data. (#174314)
## Sparse Frontend
- Fixed `torch.sparse.spdiags` crashing with zero-dimension shapes (#174052)
## torch.func
- Fixed `GradTrackingTensor.tolist()` not working on MPS (macOS) device tensors when used inside `torch.func.grad` or other function transforms (#171317)
## XPU
- Fix T5 model SDPA pattern matcher on XPU (#171774)
- Fix `torch.xpu.memory_allocated` / `torch.xpu.memory_reserved` reporting incorrect memory sizes (#171453)
## torch.compile
#### Dynamo
- Fixed memory leaks: cleared weakrefs from memos/guards after compilation (#165367), cleared weak references from `FakeTensorMode` after compile (#171209), fixed CUDA memory usage for CPU-only compile (#163841)
- Fixed overguarding on `OrderedSet`, `set`, and `frozenset` with activation checkpointing (#169535, #170291)
- Fixed `MATCH_MAPPING`, `MATCH_KEYS`, and `MATCH_SEQUENCE` opcodes for Python pattern matching (`match`/`case`) support (#173085, #173086, #173087)
- Handle List/Dict comprehension graph breaks for Python 3.12+, including nested comprehensions (#173558, #174413)
- Fixed support for self-referential lists and dicts (#173672, #174498)
- Fixed `share_memory_` compile failure (#171162)
- Fixed `defaultdict` default factory and union functionality (#168028)
- Fixed property setter on `MutableMapping` subclasses (#173184)
- Various tensor subclass fixes: subclass handling (#170871), sequence conversion (#172103), metadata propagation for in-place ops (#167583)
- Correctly pass `is_inference` in the cudagraphs `torch.compile` backend (#174713)
#### AOTDispatcher
- Fixed effect token handling when a graph contains subgraphs without tokens (#173226)
#### Inductor
- Avoid TMA assert and honor descriptor min block sizes in mix-order (#170949)
- Prevent fusing atomic scatter ops with dependent reads (#172301)
- Combo kernel fixes: missing store masks, `persistent_reduction` heuristics, `FusedMixOrderReductions` grouping, and scalar store broadcast shape mismatch (#168939, #169509, #169721, #172658)
- Fix `torch.cond` stride mismatch when subgraph outputs are padded (#169963)
- Fix `view_copy` decomposition to handle dtype size changes (#171442)
- Fix output shape mismatch for `aten.isin` with scalar inputs (#171272)
- Fix segfault with DeviceContext and python scalar (#172660)
- Fix WeakDeps for clone ops in scheduler (#173703)
- Fix strides for `aten.uniform` (#170794)
- Handle negative scaling factors in `upsample_nearest` (#171151)
- FlexAttention fixes: non-power-of-2 head dimensions in decode, score mod captured grad dtype, GQA/MQA, force last dim contiguous, deterministic semantics, and TMA availability fallback (#164931, #170842, #171271, #172690, #174251, #174427)
- Fix compatibility with new TF32 API by removing legacy `allow_tf32` usage from inductor internals (#173731)
- Fix out of shared memory issue with too high `num_stages` (#170071)
- Fix cooperative reduction deadlocks due to too many CTAs (#170162)
- Fix `select_scatter` dtype assertion error (#171311)
- Fix bug in `aten.pow` lowering (#170960)
- Make `silu` output match eager mode in inductor (#171723)
- Fix constant folding crash on 0-d complex tensors (#172181)
- Fix `bucketize` crash in compile mode (#171595)
- Fix `OverflowError` when truncating infinity numbers (#166636)
- Fix non-contiguous valid reshape handling for dynamic shapes (#173062)
- Fix strides for `narrow_copy` decomposition (#173043)
- Fix race condition in FxGraphCache when reading temp files (#172144)
- Fix dynamic shapes infinity check (#173426)
- Fix DDE in inductor/scheduler fusion (#173412)
- Fix clone removal for conjugated tensors in `remove_noop_ops` (#172160)
- Fix edge case with `next_power_of_2` (#174330)
- Fix conditions to apply TMA (#174480)
- Fix CUTLASS import error (#174924)
- Fix persistent reduction codegen (#174928)
- Fix lowering fallback for `_pdist_forward` and `_pdist_backward` (#170959)
- Fix coalesce analysis to work with symints (#161819)
- Fix `libdevice.pow` type mismatch in Triton codegen (#173685)
- Fix missed symbol propagation in cudagraphs partition (#174729)
- Fix dtype issue in `exclusive_scan_decoupled_lookback_64` (#171153)
- Skip fuse attention on fp32 if not tf32 (#172951)
- Fix `RuntimeError` in `FxGraphCachePickler.dumps()` for unpickleable pybind11 objects (#173577)
- Fix loop split optimization when nodes have mismatched `var_ranges` (#173607)
- Fix error parameter handling (#170952)
- Guard `n_spills` None before threshold comparison in Triton heuristics (#169940)
- Autotuning fixes: TMA workspace pickling in async-pipelined mode, synthetic offsets for grouped MM, and GEMM inputs that are views of the same buffer (#173089, #171316, #171363)
- Fix reduction hint for inner-dimension reductions (#167472)
- Fix crash when Triton compile fails in `identify_mutated_tensors()` (#170808)
- Handle unbacked symbols in `should_use_persistent_reduction` (#172534)
- Pallas backend: Multiple bug fixes including store for scalar values, index_put, scatter, cat, mean reduction codegen, negative index handling, iteration variable ordering, batch norm broadcasting, scalar store shape mismatch, square buffer transpose detection, strided tensor handling, and rope (#170026, #170027, #170028, #170464, #170593, #170594, #170653, #171215, #171476, #171504, #171571, #171581, #171612, #174791)
- Fix `use_compute_types` parameter name mismatch in CPP backend `to_dtype()` that caused `TypeError` when enabling `emulate_precision_casts=True` on CPU (#168125)
- Fix Invalid Memory Access in TMA mm kernel by limiting GEMM to valid MNK dimensions (#171871)
- Guard against zero timing in combo kernel benchmarking to prevent division by zero (#172918)
- XPU: Fix SDPA pattern matcher for T5 models (#171774)
- Fix extern kernel kwargs with IR nodes not being materialized in FXIR backend, causing errors with ops like `torch.segment_reduce` (#172981)
- Fix `torch.isin` compile shape for scalar `test_elements` (#172531)
- Fix kernel benchmark runner (#169976)
## torch.fx
- Fix `torch.fx.symbolic_trace` `to_folder` with `torch.nn.Sequential` modules (#169279)
- Fix `Node.type` pickling in `torch.fx` (#169172)
- Raise ValueError for invalid fusion strategy and add test (#171573)
- Fix typos (#171042)
- Fix input mutation handling for subclasses (DTensor copy_) (#170467)
## torch.export
- Fix graph signature mutation when unlifting exported programs (#170461)
- Fix tensor name inconsistency when round-tripping through `torch.export.save` and `torch.export.load` (#171954)
- Fix handling of incomplete tensors (cuDNN packed format) in `torch.export` (#172805)
## Quantization
- Fix incorrect dilation check in quantized `MaxPool3d` that could produce negative values (#171790)
- Fix incorrect values displayed in quantization error messages and log strings (#171868)
- Add validation for `out_channels` in quantized `ConvTranspose` modules (#171628)
- Fix crash when creating quantized tensors with empty dimensions (#163487)
- Fix context cache for FP8 quantized linear operations where weight scales could become invalid (#172553)
## ONNX
- Handle complex initializers (#170231)
- Fix export of torch.cdist with dynamic axes (#172758)
- Fix InputObserver.infer_arguments with empty caches (#174205)
## Foreach
- Fixed `_foreach_copy_` producing incorrect results when destination tensors have mixed dtypes (#173531)
- Fixed `_foreach_max` returning incorrect results when tensors contain negative values, by initializing output with `lowest()` instead of zeros (#173241)
- `_foreach_norm` now properly raises an error when computing infinity norm on empty tensors, instead of returning undefined results (#173238)
- Fixed `_foreach_norm` to support symbolic tensors with dynamic shapes (#174026)
## Ahead-Of-Time Inductor (AOTI)
- Fix import error in aoti load (#173751)
- Fix mixed-device zero-size constant indexing error (#172748)






# Performance
## Python Frontend
- Added `__slots__` to pytree `TreeSpec` dataclasses, reducing memory usage and improving attribute access speed (#172172)
## Composability
- Multiple optimizations to symbolic shape reasoning, including faster symbol sorting, reduced redundant hint computations, and optimized construction of relational expressions (#174615, #174655, #174664, #174652, #174665, #174662)
## Distributed
- Sort mempool registrations via allocation-time counter for CUDA mempools (#167662)
- Improve `_get_param_to_fqns` from O(N^2) to O(N) in FSDP (#174675)
## CUDA
- Speedup `grouped_mm` a bit (#170802)
- Add fast memory snapshot option which skips traces (#173949)
- Allow all 10.x compute capabilities to use vec8 kernel for higher realized memory bandwidth (#174362)
## MPS
- Migrated `atan2` to native MPS Metal kernel (#173405)
- Migrated `pow_tensor_scalar` and `reciprocal` to Metal shaders (#170077)
- Reimplemented Cauchy distribution with native Metal kernel (#174062)
- Rewrote `log_normal` and `geometric` distributions as Metal shaders (#174189)
- Migrated `grid_sampler_2d` to Metal (#174343)
## ROCm
- Revert MIOpen channels last support back to opt-in using the environment variables PYTORCH_MIOPEN_SUGGEST_NHWC=1 and PYTORCH_MIOPEN_SUGGEST_NHWC_BATCHNORM=1. (#170780)
- New fx pass to reduce atomic contention. (#168073)
- TopK performance improvements; single-block warp-level compaction (#171940), warp merge sort (#170029).
- Enable fastSpecializedAtomicAdd for gfx950, improving performance of index-based operators like embedding bag, sampling, and scatter/gather. (#170330)
- Optimize radix select by caching data on shared memory. (#172517)
- Optimize reduction operator launch configuration for better performance. (#173576)
- Improvements to inductor reduction kernel heuristics for MI350. (#170931)
## XPU
- Optimize `int_mm` performance on Intel GPU when `mat2` is non-contiguous (#169555)
- Enable static Triton kernel launcher for XPU backend to reduce model compilation time (#169938)
## torch.compile
#### Dynamo
- Various compile time improvements: caching for `inspect.signature`, `var_getattr`, attr source construction, and higher-order ops; fast paths for `bind_args`, `GET_ITER` on tuples, and `tree_map` on namedtuples; lazy variable tracker optimizations (#170100, #169959, #173582, #174437, #174438, #174141, #174020, #174130, #174901, #174598)
#### Inductor
- FlexAttention performance: Improved flex decoding by avoiding unbalanced splitting, support multi BLOCK_M for flex-decoding, elide score-mod when not needed, and avoid materializing lse grad (#167935, #170343, #172380, #173481)
- Compile-time improvements: optimized reorder/sink passes, removed expensive `dynamo_timed` calls, used `_has_symbolic_sizes_strides` more pervasively, overlapped template fusion with async_compile, and optimized Triton template heuristics (#169370, #169661, #169662, #170444, #170565, #172249, #174408)
- Apply gumbel max trick for sampling (#171143)
- Improved combo kernels design, add per-sub-kernel block dimensions for combo kernels and flattened grid dispatch (#171671, #172527)
- Rewrote `avg_pool2d` as a reduction for improved performance (#167228)
- Optimized tensor broadcasting (#170772)
- Reduced autotune search space for pointwise Triton kernels (#169508)
- Added BLOCK_K=64 and 128 autotuning configs for Triton conv, improving performance for larger channel sizes (#174752)
## torch.fx
- Improve node index lookup performance in FX graphs by using an index lookup map (#173385)
## Quantization
- Use oneDNN primitive for FP8 quantized convolution on x86, replacing the previous reference kernel (#172551)
## Optimizer
- Use fused multiply-add (FMA) instructions for fused Adam and AdamW on CUDA, improving numerical accuracy and performance (#173224)
- Improve performance of fused Adam, AdamW and SGD by not using double compute (#173227)
## Foreach
- Enabled fast path for `_foreach_addcmul` and `_foreach_addcdiv` when `tensor1` is a 0D (scalar) tensor (#172731)





# Documentation
## Release Engineering
- Fixed stable C++ docs rendering (#171957)
- Updated pytorch_sphinx_theme2 version to 0.4.3 (#174806)
- Updated pytorch_sphinx_theme2 version to 0.4.6 (#177562)
## Python Frontend
- Clarified `torch.unique` behavior when using the `dim` parameter (#171608)
- Clarified `torch.as_tensor` signature to document that `dtype` and `device` are keyword-only arguments (#173073)
- Fixed `torch.tensordot` documentation (#173893)
- Added dedicated docstring for `torch.Tensor.permute` to clarify it accepts variadic arguments unlike `torch.permute` (#170689)
## Autograd
- Improve `torch.autograd.set_multithreading_enabled` docs (#170204)
## Nested Tensor (NJT)
- Add warning about inactive development to NJT docs (#172645)
## C++ Frontend
- Added C++ docs for `torch::stable` namespace (#170912)
## Sparse Frontend
- Fixed incorrect gradient support documentation for `torch.sparse.mm` and `torch.sparse.addmm` (#174039)
## XPU
- Update XPU Get Started guide with new client GPU and formatting (#169810)
- Document previous version of Torch XPU installation (#174453)
- Update previous version 2.10 installation in XPU Get Started guide (#176141)
## torch.fx
- Add documentation for previously undocumented functions (#170581)
- Remove outdated jit files (#173015)
## Quantization
- Update `tensor_attributes.rst` with additional `torch.float4_e2m1fn_x2` dtype documentation (#170448)
## ONNX
- Change warning to debug log for missing annotations (#172247)
## Optimizer
- Improved EMA (Exponential Moving Average) equation documentation in optimizer docs (#172423)



# Security
## Python Frontend
- Fixed a ZipSlip directory traversal vulnerability in `torch.hub` that could allow malicious zip files to extract files outside the target directory. `torch.hub` now validates all extracted paths and raises a `ValueError` if an archive attempts to write outside the expected folder. (#171754)




# Developers
## Release Engineering
- Clarified needs-repro guidelines and edge cases for issue triage (#174028)
- Updated tlparse instructions in PT2 bug report template (#172392)
- Remove +ptx from CUDA 13.0 builds (#175567)
- Update inductor CI jobs to CUDA 13.0 (#175826)
- Upgrade ROCm CI to 7.2 (#173188)
- Switch vLLM test and benchmark workflows to CUDA 13.0 (#175393)
- Windows override AMI pre-installed cudnn (#177027)
- Unpin cuda-bindings dependencies (#176042)
- Stop using G3 runners (#175938)
## Autograd
- Fix grad_outputs type hints and parameter descriptions for a few autograd APIs (#164838)
## Distributed
- Fix `USE_NCCL=0` build failure in `nccl_dev_cap.hpp` (#171694)
#### DTensor
- Add DTensor performance benchmarks for collectives, `from_local`/`to_local`, and backward passes (#171576)
- Add DTensor benchmarks for miscellaneous dispatch paths (#171847)
## CPU
- Fixed compilation failure with GCC 14.2.0 on ARM SVE targets (e.g., `-march=armv8-a+sve+bf16` on Debian 13) by broadening the GCC version workaround for SVE compilation (#174647)
## CUDA
- Cleanup `at::numeric_limits` (#171111)
- Move EventPool::Event to c10 (#158220)
- Reuse CUDAEventPool in CUDA caching host allocator (#168345)
- Move CUDAEvent to c10 (#158219)
## cuDNN
- Upgrade cuDNN to 9.19 for 12.8 and 13.0 wheels (#174310, #175547)
## MPS
- Migrated `_local_scalar_dense_mps` to DispatchV2 (#172967)
## ROCm
- Fix unused-result warning in UniqueCub.cu (#174203)
- Use rocm_sdk preloaded libraries for hiprtc and amdhip64. (#169855)
- Fix torch.utils.cpp_extension build folder accelerator detection ROCm (#170784)
- Unify hipBLASLt architecture lists into common hook methods. (#172791)
## XPU
- Switch Intel Triton compiled kernel format from `spv` to `zebin` (#167972)
## torch.compile
#### Inductor
- Improved cudagraph logging: updated partition format, added tree logging, and `[compile_id]` prefix style (#170217, #170218, #174110)
- Added Proton profiling support for inductor (#171192)
- Added support for dumping input tensors for Triton kernels generated with Inductor backend (#171575)
- Inductor compiler bisector: added run mode for debugging and cudagraph application (#170717, #172461)
- Autotune configurability: number of choices displayed is now settable via environment variable, and rep options are easily overridable (#171429, #171629)
- Added template codegen/emission override hooks for external template buffers (Helion integration) (#174148)
- `fx_graph_runnable` improvements: fixed single quotes in envvars, missing symints, nested triton kernels, and global constexpr support (#173704, #174035, #174038, #174533)
- Added perfetto trace events to graph pass application with envvar to disable (#172460)
## torch.fx
- `GraphModule.print_readable()` improvements: new `additional_meta` argument for displaying additional node metadata (#173734), long annotations are now truncated for readability (#173119), and fix trailing whitespace with inner graphs (#172644)
- `GraphPickler` improvements: support for custom ignored metadata field keys (#172587), a `debug_dumps` method for debugging pickle failures (#173675), respecting `__getstate__` for `GraphModule` serialization (#173810), and automatic fallback to dill if available (#173801)
- Stack traces on `invoke_subgraph` nodes now point to the original model code for easier debugging (#170927)
- Add process group support to `fx_graph_runnable` (#173932)
- Strict type coverage in dispatch and partial subclass (#171808)
## torch.export
- Add strobelight profiling support for the export process (#174606)
## Mobile
- Fix spin lint on arm (#172965)
