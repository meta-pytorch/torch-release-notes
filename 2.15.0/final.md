# PyTorch 2.15.0 Release Notes

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

TODO

For more details about these highlighted features, you can look at the release blogpost. Below are the full release notes for this release.

# Backwards Incompatible Changes

## Python Frontend

- `import torch` can no longer be re-executed in the same process, including via `importlib.reload(torch)` ([#194654](https://github.com/pytorch/pytorch/pull/194654))

  `importlib.reload(torch)` and `del sys.modules["torch"]` + re-import now raise, as does retrying `import torch` after it failed. Re-running the module body was already unsafe in exactly the same way as the retry, so the new check does not distinguish the two. Normal use is unaffected: a successful import leaves `torch` in `sys.modules` so the body never re-runs, and re-entrant imports from a backend extension during autoload still short-circuit on `sys.modules` without reaching the check.

  Version 2.14:
  ```python
  import importlib
  import torch

  importlib.reload(torch)
  # RuntimeError: Only a single TORCH_LIBRARY can be used to register the namespace triton; ...
  # (re-importing after a failed `import torch` failed with similarly misleading errors or could segfault)
  ```

  Version 2.15:
  ```python
  import importlib
  import torch

  importlib.reload(torch)
  # ImportError: `torch` can only be initialized once per process, so this module cannot
  # be imported again: neither via `importlib.reload(torch)`, nor by re-importing after
  # a failed `import torch`.
  ```

- Nested tensors are no longer allowlisted for `torch.load(..., weights_only=True)` ([#194380](https://github.com/pytorch/pytorch/pull/194380))

  Nested jagged and strided nested tensors are no longer on the default `weights_only` allowlist. Loading a checkpoint that contains one with `weights_only=True` (the default) now fails with `Unsupported global: GLOBAL torch.nested._internal.nested_tensor._rebuild_njt was not an allowed global by default` (or `GLOBAL torch._utils._rebuild_nested_tensor` for strided nested tensors). To load checkpoints containing nested tensors, allow them explicitly with `torch.serialization.safe_globals` (see below), or use `weights_only=False` for trusted files.

  Version 2.14:
  ```python
  loaded = torch.load("njt.pt", weights_only=True)  # works
  ```

  Version 2.15:
  ```python
  from torch.nested._internal.nested_tensor import _rebuild_njt, NestedTensor
  with torch.serialization.safe_globals([_rebuild_njt, NestedTensor]):
      loaded = torch.load("njt.pt", weights_only=True)
  ```

- Operators called through `torch.ops.*` and `torch._C._dispatch_call_boxed` now use PyTorch's own warning and exception translation instead of pybind11's ([#193451](https://github.com/pytorch/pytorch/pull/193451))

  We make `torch.ops.*` calls go through the same exception and warning translation as the rest of the library. This means that some exception translation that used to be handled by pybind is now handled natively. User-defined pybind exception translation is thus lost. Restoring it may be done in a future release as part of a broader exception handler improvement.

  In addition, `TORCH_WARN` warnings from these operators now reach Python's `warnings` module, so they raise when warnings are turned into errors (`-W error`). `std::out_of_range` still becomes `IndexError` ([#195713](https://github.com/pytorch/pytorch/pull/195713)).

  Version 2.14:

  ```python
  # C++ op: throw std::invalid_argument("bad size");
  try:
      torch.ops.my_lib.my_op(x)
  except ValueError:  # pybind11 translation
      ...
  ```

  Version 2.15:

  ```python
  # C++ op: TORCH_CHECK_VALUE(false, "bad size");
  try:
      torch.ops.my_lib.my_op(x)
  except ValueError:
      ...

  # TORCH_WARN from the op is now a Python warning
  with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      torch.ops.my_lib.my_op(x)
  ```

## Autograd

- Selective activation checkpointing now saves, rather than recomputes, the outputs of operators with an ordered effect unless the policy returns `CheckpointPolicy.MUST_RECOMPUTE` ([#196956](https://github.com/pytorch/pytorch/pull/196956))

  In eager mode, if a `create_selective_checkpoint_contexts` policy returns `PREFER_RECOMPUTE`, `PREFER_CPU_OFFLOAD` or `MUST_CPU_OFFLOAD` for a non-aliasing operator with an ordered effect (e.g. via `register_effect(torch.library.EffectType.ORDERED)`), its outputs are now saved as with `MUST_SAVE` instead of recomputed, so the side effect is no longer replayed during backward. This can increase activation memory. Operators in the `c10d` namespace are excluded. Under `torch.compile`, `MUST_RECOMPUTE` on an effectful operator now raises at compile time: `RuntimeError: AOTAutograd does not support MUST_RECOMPUTE for effectful operations because forward effects cannot join the backward effect-token chain.` Use a save policy instead.

  ```python
  policy = lambda ctx, op, *args, **kwargs: CheckpointPolicy.PREFER_RECOMPUTE
  checkpoint(fn, x, use_reentrant=False, context_fn=lambda: create_selective_checkpoint_contexts(policy))
  # 2.14: an effectful op in fn runs twice; 2.15: once (use MUST_RECOMPUTE to replay)
  ```

## Distributed (c10d)

- The `nccl` backend now uses a rewritten, cleaned-up NCCL implementation by default ([#192281](https://github.com/pytorch/pytorch/pull/192281), [#192895](https://github.com/pytorch/pytorch/pull/192895), [#193237](https://github.com/pytorch/pytorch/pull/193237), [#193241](https://github.com/pytorch/pytorch/pull/193241))

  `backend="nccl"` (also the default CUDA backend of `init_process_group()`) now creates the new implementation. The legacy implementation is available as `backend="nccl-legacy"` for this release only: **`nccl-legacy` and `TORCH_DIST_USE_NCCL2=0` will be removed in the next release**, so migrate to `nccl` or `nccl-lazy`.

  Use `nccl` (eager initialization) by default. Use `nccl-lazy` when you need independent point-to-point communicators: collectives run on one eagerly created communicator, and each send/recv peer pair gets its own lazily created communicator and stream, so concurrent P2P to different peers can overlap (as in the legacy backend).

  Differences from the legacy backend:

  - Communicators are created eagerly in `init_process_group()`/`new_group()`, allocating GPU memory even for unused groups.
  - Each group is bound to one CUDA device: `device_id`, else `LOCAL_RANK % torch.cuda.device_count()` (or the global rank modulo the device count); `torch.cuda.set_device()` is not used. Tensors on another GPU fail with `Expected tensor on cuda:X but found tensor on cuda:Y` or `ProcessGroupNCCL is bound to device cuda:X but an operation was issued on cuda:Y`. Pass `device_id` if needed; several GPUs per process requires `nccl-legacy`.
  - `dist.get_backend_impl(...)` returns the new backend class, so `isinstance(..., ProcessGroupNCCL)` is `False` and legacy-only methods such as `comm_split_count()` are missing.
  - An async `all_gather`'s `work.get_future()` value is the list of per-rank outputs, not a one-element list holding a stacked tensor; read the output list passed to `all_gather` instead (works on both backends).

  To temporarily restore the legacy behavior in 2.15, set `TORCH_DIST_USE_NCCL2=0` on every rank before creating the process group, or use `nccl-legacy`:

  Version 2.14:
  ```python
  dist.init_process_group("nccl")  # ProcessGroupNCCL
  ```

  Version 2.15:
  ```python
  dist.init_process_group("nccl", device_id=torch.device("cuda", local_rank))  # new implementation
  dist.init_process_group("nccl-lazy", device_id=torch.device("cuda", local_rank))  # independent P2P communicators
  dist.init_process_group("nccl-legacy")  # legacy implementation, removed in the next release
  ```

## Distributed Checkpointing

- Distributed checkpoint metadata now records tensor strides, so checkpoints saved with PyTorch 2.15 cannot be loaded by PyTorch 2.14 or earlier ([#194251](https://github.com/pytorch/pytorch/pull/194251))

  `TensorProperties` gains an optional `strides` field in the pickled `.metadata` file. In older versions `dcp.load` raises a `CheckpointException` reporting `too many values to unpack (expected 5)`. There is no flag to write the old format.

  Version 2.14 (loading a 2.15 checkpoint):
  ```python
  dcp.load(state_dict, checkpoint_id="/ckpt/step_100")
  # CheckpointException: ... too many values to unpack (expected 5)
  ```

  Version 2.15:
  ```python
  dcp.load(state_dict, checkpoint_id="/ckpt/step_100")  # loads 2.14 and 2.15 checkpoints
  ```

## Distributed FSDP2

- With `MixedPrecisionPolicy(reduce_dtype=None)`, `fully_shard` now accumulates and reduces gradients in the parameter's `grad_dtype` (its original dtype by default) instead of in `param_dtype` ([#194434](https://github.com/pytorch/pytorch/pull/194434))

  **This is BC-breaking**: `mp_policy.reduce_dtype=None` no longer defaults to `mp_policy.param_dtype`.
  * [popular case] fp32 params, `MixedPrecisionPolicy(param_dtype=bf16)`
    * before: grad accumulation and reduce happen in bf16
    * after: grad accumulation and reduce happen in fp32 (2x reduce-scatter bytes)
  * [rare case] bf16 params, `MixedPrecisionPolicy(param_dtype=fp32)`
    * before: grad accumulation and reduce happen in fp32
    * after: grad accumulation and reduce happen in bf16

  How to deal with BC: explicitly set `mp_policy.reduce_dtype`.

  In grad accumulation (no reduce-scatter), the unsharded param's `.grad` always holds the accumulated value, visible via `model.parameters()` while unsharded. Before this change, `.grad` was `None` when `reduce_dtype` was set and differed from `param_dtype` (FSDP kept the sum in a hidden `reduce_dtype` buffer).

  Version 2.14:
  ```python
  # fp32 parameters
  mp_policy = MixedPrecisionPolicy(param_dtype=torch.bfloat16)
  fully_shard(model, mp_policy=mp_policy)
  # gradients accumulate and reduce-scatter in bf16
  ```

  Version 2.15:
  ```python
  # fp32 parameters
  mp_policy = MixedPrecisionPolicy(param_dtype=torch.bfloat16)
  fully_shard(model, mp_policy=mp_policy)
  # gradients accumulate and reduce-scatter in fp32

  # to keep the 2.14 behavior, set reduce_dtype explicitly
  mp_policy = MixedPrecisionPolicy(param_dtype=torch.bfloat16, reduce_dtype=torch.bfloat16)
  fully_shard(model, mp_policy=mp_policy)
  ```

## Distributed Pipelining

- `torch.distributed.config.pipeline_per_direction_p2p` is renamed to `pipeline_per_edge_p2p` and now uses one communicator per directed rank-to-rank edge ([#196666](https://github.com/pytorch/pytorch/pull/196666))

  The old names were removed with no alias: setting the attribute raises `AttributeError: torch.distributed.config.pipeline_per_direction_p2p does not exist`, and `TORCH_DISTRIBUTED_PIPELINE_PER_DIRECTION_P2P` is silently ignored.

  Version 2.14:
  ```python
  dist_config.pipeline_per_direction_p2p = True
  ```

  Version 2.15:
  ```python
  dist_config.pipeline_per_edge_p2p = True  # or TORCH_DISTRIBUTED_PIPELINE_PER_EDGE_P2P=1
  ```

## Profiler

- C++ stack traces are now symbolized with `dladdr` instead of `addr2line` by default ([#195462](https://github.com/pytorch/pytorch/pull/195462))

  `TORCH_DISABLE_ADDR2LINE` now defaults to on, since `addr2line` is slow and can hang. C++ frames in `TORCH_SHOW_CPP_STACKTRACES=1` errors and CUDA memory snapshots now show the library path and offset, plus the symbol name only if exported (otherwise `??`). To restore `addr2line`, set `TORCH_DISABLE_ADDR2LINE=0` or `TORCH_SYMBOLIZE_MODE=addr2line`.

  ```bash
  TORCH_SHOW_CPP_STACKTRACES=1 TORCH_DISABLE_ADDR2LINE=0 python train.py
  ```

- CUDA memory snapshots record the allocator's `mallocWithAddress` tag in a new `internal_metadata` field instead of appending it to `user_metadata` ([#193432](https://github.com/pytorch/pytorch/pull/193432))

  `user_metadata` in `torch.cuda.memory._snapshot()` trace entries is now exactly what was set with `torch.cuda.memory._set_memory_metadata` (which now also accepts a dict). Tools that searched `user_metadata` for `mallocWithAddress` must read `internal_metadata` instead.

  ```python
  # 2.14
  tagged = [e for e in trace if "mallocWithAddress" in e["user_metadata"]]
  # 2.15
  tagged = [e for e in trace if e.get("internal_metadata") == "mallocWithAddress"]
  ```

- Remove the deprecated `FunctionEvent.metadata_json` property ([#198265](https://github.com/pytorch/pytorch/pull/198265))

  Accessing it now raises `AttributeError: 'FunctionEvent' object has no attribute 'metadata_json'`, and the `metadata_json` constructor argument is removed. Use `FunctionEvent.metadata`, a dict populated when `_ExperimentalConfig(expose_kineto_event_metadata=True)` is set (not the deprecated `event_metadata`).

  ```python
  metadata = event.metadata_json  # 2.14: JSON string
  metadata = event.metadata  # 2.15: dict[str, Any] or None
  ```

- Rename the experimental CUPTI monitor profiler backend to Cuspy, without aliases for the old names ([#195881](https://github.com/pytorch/pytorch/pull/195881))

  In `_ExperimentalConfig(custom_profiler_config=...)`, `"cupti_monitor"` is now `"cuspy"` and `"cupti_monitor_async_export"` is now `"cuspy_async_export"`; old names silently fall back to the default Kineto backend. `prof.take_pending_cupti_export()` is now `take_pending_cuspy_export()` (the old name raises `AttributeError`). Prefer the new `torch.profiler.CuspyConfig`.

  ```python
  # 2.14
  cfg = _ExperimentalConfig(custom_profiler_config='{"backend":"cupti_monitor"}')
  # 2.15
  cfg = _ExperimentalConfig(custom_profiler_config='{"backend":"cuspy"}')
  ```

## Dynamo

- Higher-order ops now reject input mutation and aliasing in their bodies unless the op opts in ([#185738](https://github.com/pytorch/pytorch/pull/185738))

  Before, Dynamo let any higher-order op body mutate or alias its inputs by default. Ops that do not implement those semantics could silently produce invalid graphs. Mutation and aliasing are now off by default. The built-in wrappers that support them (`wrap`, checkpoint, `autograd.Function`, autocast/set-grad wrappers) opt in. A `flex_attention` `mask_mod` may read captured views but must not mutate inputs or return aliases. Under `fullgraph=True`, unsupported mutation or aliasing raises `Encountered input mutation during higher order op tracing` or `Encountered aliasing during higher order op tracing`; otherwise, Dynamo graph breaks and falls back to eager execution. Rewrite the higher-order op body to avoid mutation or aliasing.

  For example, rewrite an in-place `flex_attention` score modifier as an out-of-place operation:

  Version 2.14:
  ```python
  def score_mod(score, b, h, q, k):
      score.add_(1)
      return score.clone()
  ```

  Version 2.15:
  ```python
  def score_mod(score, b, h, q, k):
      return score + 1
  ```

## Inductor

- `torch.compiler.nested_compile_region(options=...)` now accepts only an allowlist of Inductor config patches ([#195864](https://github.com/pytorch/pytorch/pull/195864), [#195865](https://github.com/pytorch/pytorch/pull/195865))

  Patches passed through `get_invoke_subgraph_compile_options(fw_inductor_config_patches=..., bw_inductor_config_patches=...)` used to accept any `torch._inductor.config` key, though many were silently ignored. Only `fallback_by_default` and `max_autotune` are now accepted; other keys raise `ValueError: Inductor config key '<key>' is not supported in forward nested compile-region options` (or `backward`). Apply other options to the whole compiled function. Patch dictionaries are now snapshotted when the options are created, so later mutation has no effect, and the default no longer implicitly sets `triton.autotune_at_compile_time=True`.

  Version 2.14:
  ```python
  opts = get_invoke_subgraph_compile_options(fw_inductor_config_patches={"triton.multi_kernel": 1})
  ```

  Version 2.15:
  ```python
  opts = get_invoke_subgraph_compile_options(fw_inductor_config_patches={"max_autotune": True})
  compiled = torch.compile(fn, options={"triton.multi_kernel": 1})
  ```

- `torch.compiler.precompile` is now a module instead of a callable; capture with `torch.compiler.precompile.capture(...)` and reload with `torch.compiler.precompile.load(...)` ([#197993](https://github.com/pytorch/pytorch/pull/197993), [#198135](https://github.com/pytorch/pytorch/pull/198135), [#198213](https://github.com/pytorch/pytorch/pull/198213))

  Calling `torch.compiler.precompile(fn, *example_inputs)` now raises `TypeError: 'module' object is not callable`. `capture(fn, *, artifact_path, cache_path)` returns a context manager that you call once inside the `with` block; it writes both files when the block exits cleanly (or on `cap.save()`), and `load` now takes those paths. `decompositions=` moves to `tracer=MakeFxTracer(decompositions=...)`.

  Version 2.14:
  ```python
  python_code, cache = torch.compiler.precompile(lambda m, x: m(x), model, x)
  f = torch.compiler.precompile.load(python_code, cache)
  ```

  Version 2.15:
  ```python
  with torch.compiler.precompile.capture(lambda m, x: m(x), artifact_path="m.py", cache_path="m.cache") as cap:
      cap(model, x)
  f = torch.compiler.precompile.load("m.py", "m.cache")
  ```

## Composability

- Under functionalization, a regenerated output of `split`, `split_with_sizes` or `unbind` is now rebuilt as a single `slice` or `select` of its base, so its `grad_fn` is `SliceBackward0`/`SelectBackward0` instead of `SplitBackward0`/`SplitWithSizesBackward0`/`UnbindBackward0` ([#194037](https://github.com/pytorch/pytorch/pull/194037))

  This greatly reduces compile time for code that mutates many `split()` views (for example 32s to 15s with 128 views). Gradients are unchanged, but the in-place error now names the new op with output index 0: `RuntimeError: Output 0 of Select is a view and is being modified inplace.` Code that inspects `grad_fn` names, matches the old error text, or pattern-matches `split`/`unbind` nodes in functionalized graphs needs updating. There is no option to restore the previous behavior.

  Version 2.14:
  ```python
  >>> out = torch.func.functionalize(f)(x)  # f returns base.unbind(0)[1] after base.add_(1)
  >>> out.grad_fn
  <UnbindBackward0 object at 0x...>
  ```

  Version 2.15:
  ```python
  >>> out = torch.func.functionalize(f)(x)
  >>> out.grad_fn
  <SelectBackward0 object at 0x...>
  ```

## Release Engineering

- PyPI wheels now ship with CUDA 13.2, and CUDA 12.6 and CUDA 13.0 wheels are no longer published ([#196249](https://github.com/pytorch/pytorch/pull/196249), [#198913](https://github.com/pytorch/pytorch/pull/198913))

  The default PyPI wheel moves from CUDA 13.0 to CUDA 13.2. The 2.15 wheels are `cu132` and `cu134`; `cu126` and `cu130` are no longer built. CUDA 13 wheels need NVIDIA driver 580 or newer and a GPU of Turing (`sm_75`) or newer, so Maxwell, Pascal and Volta GPUs and hosts with a CUDA 12.x driver should stay on 2.14.

  Version 2.15:
  ```bash
  # PyPI wheel now uses CUDA 13.2
  pip install torch

  # CUDA 13.4 wheels
  pip install torch --index-url https://download.pytorch.org/whl/cu134

  # To stay on CUDA 12.6 or CUDA 13.0, pin PyTorch 2.14:
  pip install torch==2.14.0 --index-url https://download.pytorch.org/whl/cu126  # or cu130
  ```

- Python 3.10 wheels are no longer published ([#198233](https://github.com/pytorch/pytorch/pull/198233), [#199398](https://github.com/pytorch/pytorch/pull/199398))

  PyTorch 2.15 raises the minimum supported Python version for binaries to 3.11: no `cp310` wheels are built for `torch` or the Triton wheels, and CI no longer tests on Python 3.10. On Python 3.10, `pip` cannot find a 2.15 wheel. Upgrade to Python 3.11 or newer, or stay on PyTorch 2.14.

  Version 2.14:
  ```bash
  python3.10 -m pip install torch  # cp310 wheel available
  ```

  Version 2.15:
  ```bash
  python3.11 -m pip install torch==2.15.0  # Python 3.11 through 3.15 (including 3.14t and 3.15t)
  ```

- ROCm wheels move to ROCm 7.14 and 10.0; ROCm 7.2 wheels and gfx900/gfx906 kernels are dropped ([#194919](https://github.com/pytorch/pytorch/pull/194919))

  gfx900 (MI25) and gfx906 (MI50/MI60, Radeon VII) users can stay on 2.14 (`rocm7.2`) or build from source with those targets in `PYTORCH_ROCM_ARCH`.
  ```bash
  pip install torch --index-url https://download.pytorch.org/whl/rocm7.14  # or rocm10.0
  ```

- Linux CUDA wheels no longer depend on the cuRAND library ([#194850](https://github.com/pytorch/pytorch/pull/194850))

  PyTorch only uses the cuRAND device API, so `torch` no longer links `libcurand`, no longer preloads it on `import torch`, and the wheel's CUDA requirements no longer include cuRAND. Extensions or libraries that call the cuRAND host API (for example `curandCreateGenerator`) and relied on `pip install torch` bringing in the cuRAND library can fail to load `libcurand.so` and must now install it themselves.

  Version 2.15:
  ```bash
  pip install torch
  pip install "cuda-toolkit[curand]==13.2.2"  # match the toolkit version of your wheel
  ```

## CUDA

- `torch.histc(..., out=...)` on CUDA now raises an error when `out` does not have the same dtype as the input ([#196100](https://github.com/pytorch/pytorch/pull/196100))

  CUDA used to silently cast into any `out` dtype. It now matches CPU and MPS and rejects mismatches, even widening ones. Compute without `out` and cast instead.

  Version 2.14:
  ```python
  >>> torch.histc(x, bins=4, min=-2.0, max=2.0, out=int64_out)  # silently truncated
  ```

  Version 2.15:
  ```python
  RuntimeError: torch.histogram: input tensor and hist tensor should have the same dtype, but got input float and hist long int
  >>> int64_out.copy_(torch.histc(x, bins=4, min=-2.0, max=2.0))  # workaround
  ```

- On CUDA, cuBLAS and cuBLASLt workspaces are now allocated for each operation instead of being cached per handle and stream ([#194311](https://github.com/pytorch/pytorch/pull/194311))

  Graphs captured separately on one stream could share the cached workspace and fail on replay with `CUDA error: an illegal memory access was encountered`. Workspaces are now freed after each op, so `torch.cuda.memory_allocated()` excludes them and the handle from `torch.cuda.current_blas_handle()` has no ATen workspace attached. Set `TORCH_CUBLAS_WORKSPACE_CACHE=1` to restore caching (unsafe with multiple graphs on one stream). `TORCH_CUBLASLT_UNIFIED_WORKSPACE` now only takes effect with caching enabled. ROCm has a matching change ([#196920](https://github.com/pytorch/pytorch/pull/196920)).

  Version 2.14:
  ```python
  >>> torch.mm(a, a, out=out)
  >>> torch.cuda.memory_allocated() - before > 0  # workspace stays allocated
  True
  ```

  Version 2.15:
  ```python
  >>> torch.cuda.memory_allocated() - before  # freed after the op
  0
  ```

## CPU (AArch64)

- Float32 `torch.sin` and `torch.cos` on Arm CPUs (NEON and SVE) now use SLEEF's 3.5-ULP kernels instead of the 1.0-ULP kernels, matching the accuracy of the x86 AVX2 implementation and running 1.7x-2.4x faster on Neoverse V1/V2 ([#196315](https://github.com/pytorch/pytorch/pull/196315))

  Float32 `sin` and `cos` results on Arm can now differ from earlier releases in the last bits. Bit-for-bit comparisons against stored golden outputs, `torch.equal`, or `torch.testing.assert_close` with `rtol=0, atol=0` may fail; default `assert_close` tolerances are unaffected. There is no switch to restore the previous kernels; if you need tighter accuracy, compute in float64 and cast back.

  Version 2.14:
  ```python
  >>> x.cos()  # float32 on Arm: within 1 ULP
  ```

  Version 2.15:
  ```python
  >>> x.cos()  # float32 on Arm: within 2 ULP
  >>> x.double().cos().float()  # workaround: correctly rounded
  ```

## MPS

- The MPS backend now requires macOS 15 (Sequoia) or newer ([#199261](https://github.com/pytorch/pytorch/pull/199261), [#200290](https://github.com/pytorch/pytorch/pull/200290))

  macOS 14 has reached end of life, so its MPS workarounds were removed. On macOS 14, `torch.backends.mps.is_available()` returns `False` and allocating on `mps` raises the error below. To keep using MPS, stay on PyTorch 2.14 or upgrade macOS; CPU builds still run on older macOS. C++ extensions: `at::mps::MacOSVersion::MACOS_14_4` was removed.

  ```python
  >>> torch.ones(2, device="mps")  # 2.15 on macOS 14
  RuntimeError: The MPS backend is supported on macOS 15.0+. Current OS version can be queried using `sw_vers`
  ```

## XPU

- Remove the `allocator` property from `torch.xpu.MemPool`, aligning with other accelerators ([#192041](https://github.com/pytorch/pytorch/pull/192041))

  `torch.xpu.MemPool` no longer exposes the allocator it was constructed with, so `pool.allocator` now raises `AttributeError`. Keep your own reference to the allocator instead; passing one to the `MemPool` constructor is unchanged.

  Before:

  ```python
  pool = torch.xpu.MemPool(allocator.allocator())
  my_allocator = pool.allocator
  ```

  After:

  ```python
  my_allocator = allocator.allocator()
  pool = torch.xpu.MemPool(my_allocator)
  ```

## Complex Frontend

- Ops that are undefined for complex inputs now raise `TypeError` instead of `RuntimeError` ([#192350](https://github.com/pytorch/pytorch/pull/192350))

  This covers order-dependent ops (`sort`, `argsort`, `topk`, `argmax`/`argmin`, `max`/`min` with `dim`, `maximum`/`minimum`, `fmax`/`fmin`, `aminmax`), `isposinf`/`isneginf`, `view_as_real`/`imag` on real tensors, and `view_as_complex` on complex tensors, matching Python (`1j < 2j` is a `TypeError`). `except RuntimeError:` no longer catches these; catch `(RuntimeError, TypeError)`. Ops not yet implemented for a dtype (e.g. `rad2deg`, `nansum`, `heaviside` on complex, `topk`/`argmax` on bool) now raise `NotImplementedError`, which `except RuntimeError:` still catches. Full `max()`/`min()`/`amax`/`amin` are unchanged.

  ```python
  torch.sort(torch.randn(3, dtype=torch.cfloat))
  # 2.14: RuntimeError:  Sort does not support complex dtypes on CPU
  # 2.15: TypeError:  Sort does not support complex dtypes on CPU
  ```

# Deprecations

## Optimizer

- Passing a bare `set` of parameters to an optimizer is deprecated and now emits a `FutureWarning`; it will become an error in a future release ([#198710](https://github.com/pytorch/pytorch/pull/198710))

  Set iteration order can change between runs, so optimizer state could silently mismatch parameters on reload. The warning reads: `optimizer parameters need to be organized in ordered collections, but the ordering of tensors in sets will change between runs. Please use a list instead.`

  ```python
  opt = torch.optim.Adam(set(model.parameters()))  # 2.15: FutureWarning
  opt = torch.optim.Adam(list(model.parameters()))  # recommended
  ```

## Linear Algebra Frontend

- MAGMA is deprecated for LU factorization with pivoting on CUDA: `torch.linalg.lu_factor`, `torch.linalg.lu`, and the ops that use it internally (`torch.linalg.solve`, `torch.linalg.inv`, `torch.linalg.det`, `torch.linalg.slogdet`) now always use cuSOLVER ([#190661](https://github.com/pytorch/pytorch/pull/190661))

  This only affects code that sets `torch.backends.cuda.preferred_linalg_library("magma")`: pivoted LU now uses cuSOLVER anyway; a new built-in batched LU kernel replaces MAGMA's for large batches. When MAGMA is preferred, the first call warns: `linalg.lu_factor: MAGMA, as a linear algebra backend, is deprecated and will be removed in future releases.` `pivot=False` still uses MAGMA when it is preferred. To avoid the warning, use the default or cuSOLVER backend.

  ```python
  torch.backends.cuda.preferred_linalg_library("magma")
  LU, pivots = torch.linalg.lu_factor(A)  # 2.14: MAGMA; 2.15: cuSOLVER + UserWarning
  torch.backends.cuda.preferred_linalg_library("default")  # recommended
  ```

## Profiler

- `torch.autograd.profiler.load_nvprof`, `parse_nvprof_trace` and `EnforceUnique` are deprecated and will be removed in PyTorch 2.17 ([#198396](https://github.com/pytorch/pytorch/pull/198396))

  `nvprof` does not support recent GPUs. They now emit a `FutureWarning` such as `` `torch.autograd.profiler.load_nvprof` is deprecated and will be removed in PyTorch 2.17. `` Use `torch.profiler.profile` or Nsight Systems with `torch.autograd.profiler.emit_nvtx()`.

  ```python
  events = torch.autograd.profiler.load_nvprof("trace.prof")  # 2.14
  with torch.profiler.profile() as prof:  # 2.15
      run_workload()
  ```

- `FunctionEvent.event_metadata` is deprecated in favor of `FunctionEvent.metadata` ([#198405](https://github.com/pytorch/pytorch/pull/198405))

  `metadata` is a typed `dict[str, Any]` with everything `event_metadata` had. Accessing `event_metadata` emits `FutureWarning: `event_metadata` is deprecated. Use `metadata` instead.`

  ```python
  grid = event.event_metadata.grid  # 2.14
  grid = event.metadata["grid"]  # 2.15
  ```

## Inductor

- Deprecate `torch._inductor.config.triton.use_block_ptr` because Triton removed its block-pointer API ([#191007](https://github.com/pytorch/pytorch/pull/191007))

  With a Triton that no longer provides block pointers, `use_block_ptr=True` is now a no-op that falls back to the default indexing path with a one-time `FutureWarning: config.triton.use_block_ptr=True but the installed Triton no longer provides the block-pointer frontend API`, instead of failing with `CompilationError: ... Block pointers have been removed in favor of the tensor descriptor API`. Use tensor descriptors instead.

  Version 2.14:
  ```python
  torch._inductor.config.triton.use_block_ptr = True
  ```

  Version 2.15:
  ```python
  torch._inductor.config.triton.use_tensor_descriptor = True
  ```

- Deprecate the no-op `torch._inductor.config.use_mixed_mm` and `torch._inductor.config.mixed_mm_choice` settings ([#193721](https://github.com/pytorch/pytorch/pull/193721))

  These settings have been ignored since the tuned `mixed_mm` path was removed. Reading or setting either now emits a one-time `FutureWarning` such as `torch._inductor.config.use_mixed_mm is deprecated and does not do anything`. `autoheuristic_collect.mixed_mm` and `autoheuristic_use.mixed_mm` were removed, and `"mixed_mm"` is no longer the `TORCHINDUCTOR_AUTOHEURISTIC_USE` default. Delete these settings from your code.

  Version 2.14:
  ```python
  torch._inductor.config.use_mixed_mm = True  # silently ignored
  ```

  Version 2.15:
  ```python
  # FutureWarning; delete the line
  ```

- Rename `torch._inductor.config.benchmark_epilogue_fusion` to `benchmark_template_fusion` and `max_epilogue_benchmarked_choices` to `max_template_fusion_benchmarked_choices` ([#198430](https://github.com/pytorch/pytorch/pull/198430))

  The settings also cover prologue fusion, so the old names were misleading. The old names remain as deprecated aliases that emit a one-time `FutureWarning`. The environment variable is now `TORCHINDUCTOR_BENCHMARK_TEMPLATE_FUSION`; `TORCHINDUCTOR_BENCHMARK_EPILOGUE_FUSION` is still read as a fallback.

  Version 2.14:
  ```python
  torch._inductor.config.benchmark_epilogue_fusion = False
  ```

  Version 2.15:
  ```python
  torch._inductor.config.benchmark_template_fusion = False
  ```

## CUDA

- `torch.cuda.graph_annotations.clear_kernel_annotations()` is deprecated and now emits a `FutureWarning` ([#195398](https://github.com/pytorch/pytorch/pull/195398))

  The CUDA graph kernel annotation registry now cleans up after itself: annotations are rekeyed to the executable graph when it is instantiated and dropped when that graph is destroyed. A global clear also discards annotations for graphs that are still live. Remove the call, and reset or delete a graph to drop its annotations.

  Version 2.14:
  ```python
  annotations = get_kernel_annotations()
  clear_kernel_annotations()
  ```

  Version 2.15:
  ```python
  annotations = get_kernel_annotations()
  # No clear needed; g's annotations are dropped when g is reset or destroyed.
  ```

# New Features

## torch.nn

- Add `torch.nn.functional.scaled_addmm` and in-place `scaled_addmm_`, which compute `beta * input + alpha * scaled_mm(mat1, mat2)` in a single cuBLASLt GEMM on CUDA with the same scaling recipes as `scaled_mm`; also supported under `torch.compile` ([#195409](https://github.com/pytorch/pytorch/pull/195409), [#195410](https://github.com/pytorch/pytorch/pull/195410))

## Optimizer

- Add `torch.optim.functional`, a public module of functional optimizers (`adam`, `adamw`, `sgd`, `muon` and others) that run the same implementations as the optimizer classes while the caller manages parameters, gradients and state ([#194986](https://github.com/pytorch/pytorch/pull/194986))

## Autograd

- Add `ctx.input_grad_buffers` to custom `torch.autograd.Function` backward, exposing the engine's gradient accumulation buffers (or `None` when unavailable) so a fused kernel can accumulate an input's gradient in place and return `None` for it. Availability depends on backward order, so keep an out-of-place fallback; buffers must be updated synchronously within the current `backward` call, and the property is unavailable with `create_graph=True`, anomaly detection, or post-hooks on the producing node ([#196491](https://github.com/pytorch/pytorch/pull/196491))
- Add `torch.autograd.graph.queue_callback(callback)`, a public API to run a callback when the current backward pass finishes ([#193958](https://github.com/pytorch/pytorch/pull/193958))

## Distributed (c10d)

- Add an experimental one-sided transport API, `torch.distributed._transport`, with a NIXL backend and CUDA-graph-capturable stream-ordered transfers ([#195643](https://github.com/pytorch/pytorch/pull/195643), [#197032](https://github.com/pytorch/pytorch/pull/197032), [#198889](https://github.com/pytorch/pytorch/pull/198889), [#198918](https://github.com/pytorch/pytorch/pull/198918))
- Add an experimental pure-Python watchdog, `torch.distributed._watchdog`, that detects hung CPU and GPU operations in Python distributed backends and dumps thread stacks on timeout ([#192075](https://github.com/pytorch/pytorch/pull/192075))
- Add `get_peer_cft_handle(peer)` and `get_multimem_cft_handle()` to NCCL symmetric memory for NCCL Compute Fabric Transport ([#191685](https://github.com/pytorch/pytorch/pull/191685))
- Add `ProcessGroupNCCL.Options.lazy_init` so `nccl` and `nccl-lazy` groups create their communicator on first use instead of allocating ~200 MiB in `new_group` ([#200020](https://github.com/pytorch/pytorch/pull/200020))

## Distributed Checkpointing

- `FsspecReader` and `FsspecWriter` are now public in `torch.distributed.checkpoint`, and `FsspecWriter` supports `dcp.async_save` through a new `cache_staged_state_dict` argument placed before `overwrite` (pass `overwrite` and later arguments by keyword); importing the old private `_fsspec_filesystem` module emits a `DeprecationWarning` ([#188698](https://github.com/pytorch/pytorch/pull/188698))

## Distributed FSDP2

- Add `FSDPModule.set_manual_backward_finalization(True)` and `FSDPModule.finalize_backward()` to run gradient reduction and resharding at a chosen point instead of in the autograd final callback ([#196640](https://github.com/pytorch/pytorch/pull/196640))
- Add `finalize_backward(async_op=True)`, which returns a `GradientReductionHandle` so gradient reduction can overlap other compute ([#196724](https://github.com/pytorch/pytorch/pull/196724))
- Add `FSDPModule.set_keep_unsharded_storage()` to keep unsharded parameter storage allocated across `reshard()` ([#198417](https://github.com/pytorch/pytorch/pull/198417))
- Let tensor-subclass parameters free raw all-gather buffers right after `fsdp_post_all_gather` by implementing `fsdp_should_release_all_gather_outputs_after_post_all_gather()` ([#194114](https://github.com/pytorch/pytorch/pull/194114))

## Distributed Pipelining

- Add `PipelineStage.register_forward_context(factory)` to wrap each stage forward in a context manager that receives the stage and microbatch indices ([#196462](https://github.com/pytorch/pytorch/pull/196462))
- Add `torch.distributed.pipelining.analyze_pipeline_activation_liveness`, which computes activation lifetimes and reusable storage slots from a schedule ([#196464](https://github.com/pytorch/pytorch/pull/196464))

## DeviceMesh

- Add the experimental `DeviceMesh.abort()` to abort all process groups of a root mesh, avoiding hangs when a peer exits early ([#189655](https://github.com/pytorch/pytorch/pull/189655))

## Profiler

- Add `torch.profiler.ProfilerActivityConfig` and `torch.profiler.PerformanceMetricsConfig` to configure collection per activity group, such as CUDA hardware performance counters ([#196065](https://github.com/pytorch/pytorch/pull/196065))
- Add `torch.profiler.CuspyConfig` to enable the experimental Cuspy CUDA collection backend without `_ExperimentalConfig` ([#196066](https://github.com/pytorch/pytorch/pull/196066))

## Dynamo

- Add `torch.compiler.config.static_sources` (`TORCH_COMPILE_STATIC_SOURCES`), the inverse of `dynamic_sources`, listing sources that stay static even under automatic dynamic shapes, PGO, or `dynamic=True`, but not explicit `mark_dynamic` ([#193626](https://github.com/pytorch/pytorch/pull/193626))
- Let custom backends define a `_dynamo_backend_init` callable that runs when `torch.compile()` resolves the backend, so out-of-tree backends can load native libraries or set up devices and fail fast ([#192345](https://github.com/pytorch/pytorch/pull/192345))

## Inductor

- Add thread-based Inductor compile workers for free-threaded Python, selected with `TORCH_COMPILE_WORKER_MODE=thread` or `auto` to avoid process-spawn and pickling overhead ([#179547](https://github.com/pytorch/pytorch/pull/179547), [#179548](https://github.com/pytorch/pytorch/pull/179548))
- Add an experimental FlyDSL GEMM autotuning backend for ROCm gfx950, covering FP16/BF16 `mm`, `grouped_mm` and MXFP4/MXFP8 `scaled_mm`, enabled by adding `FLYDSL` to `torch._inductor.config.max_autotune_gemm_backends` ([#190903](https://github.com/pytorch/pytorch/pull/190903), [#192877](https://github.com/pytorch/pytorch/pull/192877), [#194032](https://github.com/pytorch/pytorch/pull/194032), [#194303](https://github.com/pytorch/pytorch/pull/194303), [#194981](https://github.com/pytorch/pytorch/pull/194981), [#196719](https://github.com/pytorch/pytorch/pull/196719))

## Ahead-Of-Time Inductor (AOTI)

- Add `num_runners` and `use_stream_affinity` arguments to `torch._inductor.aoti_load_package`, which keep each non-null CUDA or XPU stream on the same model instance across calls ([#194783](https://github.com/pytorch/pytorch/pull/194783))
- Add an optional lifecycle observer to the C++ `AOTIModelContainerRunner`: attach a `torch::inductor::AOTIModelContainerObserver` with `set_observer()` to get begin/end callbacks around inference, constant swaps and constant folding ([#193999](https://github.com/pytorch/pytorch/pull/193999))

## Foreach

- Add the public `torch.foreach` module (beta), which exposes the multi-tensor `torch._foreach_*` operations under stable, documented names (e.g. `torch.foreach.mul_(params, 3)`) with parameter names that follow the ordinary ops ([#193607](https://github.com/pytorch/pytorch/pull/193607))

## C++ Frontend

- Added `torch::stable::sort` to the stable ABI ([#198038](https://github.com/pytorch/pytorch/pull/198038))
- Made more `c10/util` helpers available header-only under `torch/headeronly/util` ([#194673](https://github.com/pytorch/pytorch/pull/194673), [#194781](https://github.com/pytorch/pytorch/pull/194781))
- Add stable ABI conversions for `torch.dtype`/`torch.device` Python objects and a `torch::stable::is_tensor_pyobject` check ([#192774](https://github.com/pytorch/pytorch/pull/192774))

## Release Engineering

- Enable the FlashAttention backend of `scaled_dot_product_attention` in Windows CUDA builds and wheels for Ampere and newer GPUs. It was previously disabled on Windows, so SDPA fell back to the math backend; in a GQA benchmark (bf16, sequence length 2048) on an RTX 5090 the forward pass drops from 11.5 ms to 0.49 ms ([#186343](https://github.com/pytorch/pytorch/pull/186343))
- `torch.compile` now works on Python 3.15 (previously it raised `RuntimeError: torch.compile is not supported on Python 3.15+`; the check now applies to Python 3.16 and newer), and the Python 3.15 and 3.15t wheels are built against CPython 3.15.0rc2, after the ABI freeze, instead of beta releases ([#178393](https://github.com/pytorch/pytorch/pull/178393), [#199356](https://github.com/pytorch/pytorch/pull/199356))

## CUDA

- Add `GreenContext.split` and `torch.cuda.green_contexts.SMPartition` for creating green contexts with disjoint SM allocations, plus a `GreenContext.sm_count` property reporting the SMs actually allocated; requires a CUDA driver and `cuda.bindings` 13.1 or newer ([#198278](https://github.com/pytorch/pytorch/pull/198278))
- Add `locality_domain_ids` to `GreenContext.split` and `SMPartition.split`, together with `get_num_locality_domains()` and `is_localization_supported()`, to restrict SM partitions to hardware locality domains; requires a CUDA driver and `cuda.bindings` 13.4 or newer ([#198279](https://github.com/pytorch/pytorch/pull/198279))
- Add a `"bfx9"` mode for `torch.backends.cuda.matmul.fp32_precision` that keeps FP32 inputs and outputs but lets cuBLAS use its BF16x9 algorithm on compute capability 10.0 and 10.3 GPUs; requires a CUDA 12.9 or newer build ([#195301](https://github.com/pytorch/pytorch/pull/195301))
- Record the Python launch stack of each CUDA graph node during capture with `annotation_config={"record_py_stacks": True}`, read via `torch.cuda.graph_annotations.get_kernel_py_stacks()` (requires CUPTI >= 13.3) ([#198419](https://github.com/pytorch/pytorch/pull/198419))

## cuDNN

- Support causal grouped-query attention with a paged KV cache in the cuDNN backend of `torch.nn.attention.varlen` (`varlen_attn` and `varlen_attn_out`), enabling head dimension 256 with a paged KV cache on Blackwell GPUs; requires cuDNN 9.24 or newer ([#195650](https://github.com/pytorch/pytorch/pull/195650))

## MPS

- Add a public MPS stream API (`torch.mps.Stream`, `current_stream()`, `default_stream()`, `set_stream()`, the `torch.mps.stream()` context manager) and `Tensor.record_stream` on MPS ([#191415](https://github.com/pytorch/pytorch/pull/191415), [#193464](https://github.com/pytorch/pytorch/pull/193464))
- Add `torch.float8_e4m3fn` support on MPS ([#194074](https://github.com/pytorch/pytorch/pull/194074), [#196915](https://github.com/pytorch/pytorch/pull/196915), [#196918](https://github.com/pytorch/pytorch/pull/196918), [#196945](https://github.com/pytorch/pytorch/pull/196945), [#196955](https://github.com/pytorch/pytorch/pull/196955), [#197383](https://github.com/pytorch/pytorch/pull/197383), [#197801](https://github.com/pytorch/pytorch/pull/197801))
- Support `float8_e4m3fn` inputs in `torch.nn.functional.scaled_mm` on MPS ([#196916](https://github.com/pytorch/pytorch/pull/196916))

## XPU

- SYCL Kernel Programming Simplified: Add SYCL free-function kernel support to the XPU backend and migrate most existing SYCL kernels to it, so device code can be written as explicit free functions in a more intuitive style instead of verbose functors ([#196387](https://github.com/pytorch/pytorch/pull/196387), [#196932](https://github.com/pytorch/pytorch/pull/196932), [#198200](https://github.com/pytorch/pytorch/pull/198200), [#198720](https://github.com/pytorch/pytorch/pull/198720), [#200289](https://github.com/pytorch/pytorch/pull/200289))
- Enhanced XPU Runtime Capabilities: Support sharing `torch.xpu.Event` across processes, through `torch.multiprocessing` or `ipc_handle()` / `from_ipc_handle()` on an event created with `interprocess=True` ([#191182](https://github.com/pytorch/pytorch/pull/191182), [#192495](https://github.com/pytorch/pytorch/pull/192495), [#193399](https://github.com/pytorch/pytorch/pull/193399), [#192514](https://github.com/pytorch/pytorch/pull/192514))
- Improved XPU Profiling Experience: Add kernel-level visibility into XPU Graph replay, cross-rank correlation for XCCL collectives, and per-kernel hardware counter collection across all Intel GPUs in multi-GPU workloads to the XPU profiler ([#195128](https://github.com/pytorch/pytorch/pull/195128), [#198200](https://github.com/pytorch/pytorch/pull/198200))

# Improvements

## Python Frontend

- Saturate out-of-range integer scalar bounds in `clamp` and `hardtanh` instead of wrapping or raising (e.g. `torch.clamp(uint8_tensor, min=-255)` is a no-op) ([#193169](https://github.com/pytorch/pytorch/pull/193169))
- Support empty batch dimensions in FFT operations on CPU, CUDA and MPS ([#190483](https://github.com/pytorch/pytorch/pull/190483))
- Add `skip_unsupported` to `FlopCounterMode` to warn instead of failing on higher-order operators without a FLOP formula, and count `flex_attention` FLOPs ([#167224](https://github.com/pytorch/pytorch/pull/167224))
- Support `Optional[list[Tensor]]` annotations in `torch.library.infer_schema` and `custom_op` ([#187012](https://github.com/pytorch/pytorch/pull/187012))
- Make `torch.iinfo` and `torch.finfo` hashable ([#193290](https://github.com/pytorch/pytorch/pull/193290))
- Name the context manager in tracebacks through `torch.no_grad`-style decorators ([#186502](https://github.com/pytorch/pytorch/pull/186502))
- Improve type stubs for `Tensor @ scalar` and `torch.utils` re-exports ([#195220](https://github.com/pytorch/pytorch/pull/195220), [#195289](https://github.com/pytorch/pytorch/pull/195289))
- Add `uint16`, `uint32` and `uint64` support to `torch.clamp`, `torch.maximum` and `torch.minimum` on CPU and CUDA ([#189953](https://github.com/pytorch/pytorch/pull/189953))

## torch.nn

- Support soft-label targets with `reduction="none"` on the chunked `linear_cross_entropy` path ([#188296](https://github.com/pytorch/pytorch/pull/188296))
- Allow FlashAttention-4 in `scaled_dot_product_attention` with different query/key and value head dimensions ([#193039](https://github.com/pytorch/pytorch/pull/193039))
- Support deterministic `bicubic` `F.interpolate` backward ([#193707](https://github.com/pytorch/pytorch/pull/193707))
- Support `bicubic` mode for 5-D input in `F.grid_sample` ([#194787](https://github.com/pytorch/pytorch/pull/194787))
- Allow `varlen_attn` to dispatch causal attention to cuDNN ([#193630](https://github.com/pytorch/pytorch/pull/193630))
- Add `weight` to the `F.mse_loss` type stub ([#196126](https://github.com/pytorch/pytorch/pull/196126))

## Optimizer

- Validate `lambd` and `alpha` in `torch.optim.ASGD` ([#193303](https://github.com/pytorch/pytorch/pull/193303))
- Run the optimizer graph-capture health check on all accelerators ([#194362](https://github.com/pytorch/pytorch/pull/194362))

## Autograd

- Add backward and forward-mode AD for the `torch.special` Bessel functions ([#189872](https://github.com/pytorch/pytorch/pull/189872))
- Add forward-mode AD for `F.grid_sample` ([#195280](https://github.com/pytorch/pytorch/pull/195280))
- Add `torch._functorch.config.activation_memory_budget_require_full_coverage` to let `region_activation_memory_budget` apply to a whole compiled graph ([#195932](https://github.com/pytorch/pytorch/pull/195932))
- Allow reading `Tensor.grad_dtype` on non-leaf tensors ([#190852](https://github.com/pytorch/pytorch/pull/190852))

## Distributed

- Make Dynamo guards rank-portable under `compile_on_one_rank` ([#196150](https://github.com/pytorch/pytorch/pull/196150), [#196938](https://github.com/pytorch/pytorch/pull/196938), [#196939](https://github.com/pytorch/pytorch/pull/196939), [#196940](https://github.com/pytorch/pytorch/pull/196940))

## Distributed (c10d)

- Extend the new NCCL backend: collective runtime estimation, the NCCL allocator for backend tensors, an opt-in shrink/grow `reconfigure()` path, legacy-matching errors, and windows and reconfiguration on ROCm ([#192854](https://github.com/pytorch/pytorch/pull/192854), [#192855](https://github.com/pytorch/pytorch/pull/192855), [#199240](https://github.com/pytorch/pytorch/pull/199240), [#194953](https://github.com/pytorch/pytorch/pull/194953), [#193282](https://github.com/pytorch/pytorch/pull/193282), [#194774](https://github.com/pytorch/pytorch/pull/194774))
- Add a `comm_ptr` property returning the `ncclComm_t` on all NCCL backends ([#197558](https://github.com/pytorch/pytorch/pull/197558), [#198865](https://github.com/pytorch/pytorch/pull/198865))
- Support `ReduceOp.PREMUL_SUM` in functional `all_reduce` and under `LocalTensorMode`, and backward for `MIN`/`MAX` ([#190942](https://github.com/pytorch/pytorch/pull/190942), [#193868](https://github.com/pytorch/pytorch/pull/193868), [#191947](https://github.com/pytorch/pytorch/pull/191947))
- Stop emitting a `FutureWarning` from `all_gather_into_tensor` and `reduce_scatter_tensor` ([#193874](https://github.com/pytorch/pytorch/pull/193874))
- Allow a CPU `device_id` in `init_process_group` ([#198340](https://github.com/pytorch/pytorch/pull/198340))
- Add `TORCH_NCCL_TEARDOWN_ON_TIMEOUT` to terminate on a legacy NCCL timeout instead of hanging ([#196187](https://github.com/pytorch/pytorch/pull/196187))
- Record the flight recorder for backends without built-in support (the new NCCL backend, MPI, UCC) and dump it on new NCCL backend health-check failures ([#192233](https://github.com/pytorch/pytorch/pull/192233), [#199092](https://github.com/pytorch/pytorch/pull/199092))
- Add an expert-major receive layout and zero-copy dispatch/combine to the experimental token-switch MoE dispatch API ([#187784](https://github.com/pytorch/pytorch/pull/187784), [#187785](https://github.com/pytorch/pytorch/pull/187785))
- Pass timeout and `enable_reconfigure` to dynamically created TorchComms communicators ([#199099](https://github.com/pytorch/pytorch/pull/199099))
- `is_symm_mem_enabled_for_group()` no longer requires the deprecated `enable_symm_mem_for_group()` call ([#193115](https://github.com/pytorch/pytorch/pull/193115))

## DTensor

- Support `torch.compile` for DTensor random ops on XPU ([#187969](https://github.com/pytorch/pytorch/pull/187969))

## DistributedDataParallel (DDP)

- Add manual backward finalization to `DistributedDataParallel`: set `ddp.require_manual_backward_finalization = True` and call `ddp.finalize_backward()`, so other work can overlap the in-flight gradient all-reduce ([#196651](https://github.com/pytorch/pytorch/pull/196651))
- Add a `lazy_bucket_allocation` option to `DistributedDataParallel` that allocates gradient buckets during backward and frees them afterward, lowering peak memory ([#199110](https://github.com/pytorch/pytorch/pull/199110))

## Distributed FSDP2

- Add `param_dtype_override_fn` to `MixedPrecisionPolicy` for per-parameter mixed precision in `fully_shard`, keeping one all-gather per group ([#196626](https://github.com/pytorch/pytorch/pull/196626))

## Distributed Pipelining

- Add `WAIT_SEND_F`/`WAIT_SEND_B` schedule actions and an optional `max_outstanding_sends` limit on pending sends ([#196726](https://github.com/pytorch/pytorch/pull/196726), [#196727](https://github.com/pytorch/pytorch/pull/196727))
- Add a `max_active_stages` argument to multi-stage schedules to control how many FSDP stages stay unsharded at once ([#193972](https://github.com/pytorch/pytorch/pull/193972))
- Label pipeline schedule actions in CUDA graph traces captured with `enable_annotations=True` ([#195072](https://github.com/pytorch/pytorch/pull/195072))
- Add `finalize_gradients` to pipeline schedule `step()` for gradient accumulation across several schedule runs with FSDP stages ([#196641](https://github.com/pytorch/pytorch/pull/196641))

## TorchElastic

- Add a `cas_backoff_max_seconds` rendezvous option that adds random backoff after failed rendezvous state writes ([#185930](https://github.com/pytorch/pytorch/pull/185930))
- Let custom `ErrorHandler`s see the `@record` entrypoint name and observe success through `record_success()` ([#194269](https://github.com/pytorch/pytorch/pull/194269), [#194746](https://github.com/pytorch/pytorch/pull/194746), [#195034](https://github.com/pytorch/pytorch/pull/195034))

## DeviceMesh

- Add a `preserve_rank_order` option to `DeviceMesh` so subgroups keep the mesh's rank order ([#193224](https://github.com/pytorch/pytorch/pull/193224))

## Linear Algebra Frontend

- Add CUDA TunableOp support for `torch._scaled_mm` ([#186271](https://github.com/pytorch/pytorch/pull/186271))
- Unify matmul shape-check error messages ([#193583](https://github.com/pytorch/pytorch/pull/193583))
- Add dynamic-shape TunableOp GEMM tuning with `torch.cuda.tunable.dynamic_dims_mask` and wildcard fallback (`PYTORCH_TUNABLEOP_WILDCARD_FALLBACK=1`) ([#191658](https://github.com/pytorch/pytorch/pull/191658))

## Dynamo

- Support more Python in compiled regions: `bytearray`, `types.SimpleNamespace`, `bytes()`, calling `classmethod`/`staticmethod`, list subclasses overriding `__new__`, `del` of captured variables, and more of `math`, `cmath`, `operator` and `heapq` ([#192205](https://github.com/pytorch/pytorch/pull/192205), [#199252](https://github.com/pytorch/pytorch/pull/199252), [#193719](https://github.com/pytorch/pytorch/pull/193719), [#196103](https://github.com/pytorch/pytorch/pull/196103), [#197499](https://github.com/pytorch/pytorch/pull/197499), [#197781](https://github.com/pytorch/pytorch/pull/197781), [#191512](https://github.com/pytorch/pytorch/pull/191512), [#189216](https://github.com/pytorch/pytorch/pull/189216), [#196867](https://github.com/pytorch/pytorch/pull/196867), [#197498](https://github.com/pytorch/pytorch/pull/197498), [#197222](https://github.com/pytorch/pytorch/pull/197222), [#198685](https://github.com/pytorch/pytorch/pull/198685), [#195999](https://github.com/pytorch/pytorch/pull/195999), [#192942](https://github.com/pytorch/pytorch/pull/192942), [#192834](https://github.com/pytorch/pytorch/pull/192834), [#195765](https://github.com/pytorch/pytorch/pull/195765))
- Improve exception and object-model support: exception identity checks, `delattr` and `super().__init__(msg)` on exceptions, non-string `assert` messages, `property` attributes, `types.DynamicClassAttribute`, and closure-cell comparison ([#191404](https://github.com/pytorch/pytorch/pull/191404), [#196722](https://github.com/pytorch/pytorch/pull/196722), [#196051](https://github.com/pytorch/pytorch/pull/196051), [#197798](https://github.com/pytorch/pytorch/pull/197798), [#194642](https://github.com/pytorch/pytorch/pull/194642), [#199260](https://github.com/pytorch/pytorch/pull/199260), [#197189](https://github.com/pytorch/pytorch/pull/197189))
- Raise the real Python exception (e.g. `TypeError`) for user errors detected while tracing instead of graph breaking ([#196432](https://github.com/pytorch/pytorch/pull/196432))
- Trace more without graph breaks: setting `requires_grad = True` on in-region tensors, `Tensor.storage_offset()` on inputs, `Tensor.is_pinned()`, builtin function `__name__`, `hasattr`/`getattr` on opaque objects such as `ProcessGroup`, attribute reads on `autograd.Function` subclasses, `setattr` on `torch.split` outputs, and torchvision `roi_align` ([#191129](https://github.com/pytorch/pytorch/pull/191129), [#197224](https://github.com/pytorch/pytorch/pull/197224), [#186494](https://github.com/pytorch/pytorch/pull/186494), [#196049](https://github.com/pytorch/pytorch/pull/196049), [#196050](https://github.com/pytorch/pytorch/pull/196050), [#185316](https://github.com/pytorch/pytorch/pull/185316), [#198514](https://github.com/pytorch/pytorch/pull/198514), [#185528](https://github.com/pytorch/pytorch/pull/185528))
- With `allow_rnn` disabled, graph break at the `nn.RNN`/`nn.GRU`/`nn.LSTM` call so the rest of the frame compiles ([#186614](https://github.com/pytorch/pytorch/pull/186614))
- Avoid recompiles when ops on constant inputs produce unused results ([#191143](https://github.com/pytorch/pytorch/pull/191143), [#191144](https://github.com/pytorch/pytorch/pull/191144), [#191145](https://github.com/pytorch/pytorch/pull/191145))
- Improve out-of-tree accelerator support: `DeviceInterface` streams and events, renamed PrivateUse1 tensor classes, cross-stream deallocation safety, and `torch.mtia` streams ([#194343](https://github.com/pytorch/pytorch/pull/194343), [#195432](https://github.com/pytorch/pytorch/pull/195432), [#197187](https://github.com/pytorch/pytorch/pull/197187), [#195649](https://github.com/pytorch/pytorch/pull/195649))
- Forward `torch.compile(..., name=...)` to custom backends as `kwargs["name"]` ([#196229](https://github.com/pytorch/pytorch/pull/196229))
- Improve diagnostics: less warning spam on backend fallbacks, carets in graph-break stacks, and clearer recompile reasons and error hints ([#185155](https://github.com/pytorch/pytorch/pull/185155), [#186249](https://github.com/pytorch/pytorch/pull/186249), [#185466](https://github.com/pytorch/pytorch/pull/185466), [#185419](https://github.com/pytorch/pytorch/pull/185419), [#197464](https://github.com/pytorch/pytorch/pull/197464), [#197450](https://github.com/pytorch/pytorch/pull/197450), [#195691](https://github.com/pytorch/pytorch/pull/195691))
- `aot_compile` serializes more functions (`functools.wraps` helpers, `types.MethodType`, closure cells) and prunes unpicklable values no guard reads ([#196472](https://github.com/pytorch/pytorch/pull/196472), [#196473](https://github.com/pytorch/pytorch/pull/196473), [#196474](https://github.com/pytorch/pytorch/pull/196474), [#196476](https://github.com/pytorch/pytorch/pull/196476), [#196478](https://github.com/pytorch/pytorch/pull/196478), [#196479](https://github.com/pytorch/pytorch/pull/196479), [#196481](https://github.com/pytorch/pytorch/pull/196481), [#196684](https://github.com/pytorch/pytorch/pull/196684), [#196685](https://github.com/pytorch/pytorch/pull/196685), [#196686](https://github.com/pytorch/pytorch/pull/196686), [#196687](https://github.com/pytorch/pytorch/pull/196687), [#196691](https://github.com/pytorch/pytorch/pull/196691), [#196692](https://github.com/pytorch/pytorch/pull/196692), [#197750](https://github.com/pytorch/pytorch/pull/197750), [#197752](https://github.com/pytorch/pytorch/pull/197752), [#197754](https://github.com/pytorch/pytorch/pull/197754), [#197755](https://github.com/pytorch/pytorch/pull/197755), [#197833](https://github.com/pytorch/pytorch/pull/197833), [#197762](https://github.com/pytorch/pytorch/pull/197762))
- `load_compiled_function(..., f_globals=...)` and loaded `aot_compile` modules resolve guarded globals against the live scope and re-read them on each call; a guarded global missing from `f_globals` fails with `KeyError on G['NAME']` ([#196815](https://github.com/pytorch/pytorch/pull/196815), [#196817](https://github.com/pytorch/pytorch/pull/196817), [#196818](https://github.com/pytorch/pytorch/pull/196818), [#196908](https://github.com/pytorch/pytorch/pull/196908), [#196897](https://github.com/pytorch/pytorch/pull/196897), [#197218](https://github.com/pytorch/pytorch/pull/197218), [#196904](https://github.com/pytorch/pytorch/pull/196904))
- Make `aot_compile` module dispatch more robust and improve its error messages for guard mismatches, missing globals, unpicklable values and incompatible artifacts ([#197055](https://github.com/pytorch/pytorch/pull/197055), [#196826](https://github.com/pytorch/pytorch/pull/196826), [#197047](https://github.com/pytorch/pytorch/pull/197047), [#196823](https://github.com/pytorch/pytorch/pull/196823), [#197149](https://github.com/pytorch/pytorch/pull/197149), [#197048](https://github.com/pytorch/pytorch/pull/197048), [#197220](https://github.com/pytorch/pytorch/pull/197220), [#197050](https://github.com/pytorch/pytorch/pull/197050), [#197257](https://github.com/pytorch/pytorch/pull/197257), [#197319](https://github.com/pytorch/pytorch/pull/197319), [#196816](https://github.com/pytorch/pytorch/pull/196816), [#196693](https://github.com/pytorch/pytorch/pull/196693), [#196819](https://github.com/pytorch/pytorch/pull/196819), [#197391](https://github.com/pytorch/pytorch/pull/197391), [#198061](https://github.com/pytorch/pytorch/pull/198061), [#196470](https://github.com/pytorch/pytorch/pull/196470), [#197756](https://github.com/pytorch/pytorch/pull/197756))
- `maybe_mark_dynamic` accepts `min`/`max` for an initial value range, and passing only one of them to `mark_dynamic` no longer crashes ([#194625](https://github.com/pytorch/pytorch/pull/194625))
- Keep the device index of `torch.cuda.synchronize()` unresolved under the experimental `torch.distributed.config.compile_on_one_rank` mode, so the artifact is not rank-specific ([#196937](https://github.com/pytorch/pytorch/pull/196937))

## Inductor

- Extend NVGEMM epilogue fusion (CuTeDSL-generated dense epilogues, grouped reduction epilogues, `swap_ab` configs) and support `nvidia-cutlass-operators` 0.2.0 ([#190820](https://github.com/pytorch/pytorch/pull/190820), [#190821](https://github.com/pytorch/pytorch/pull/190821), [#190822](https://github.com/pytorch/pytorch/pull/190822), [#191514](https://github.com/pytorch/pytorch/pull/191514), [#191515](https://github.com/pytorch/pytorch/pull/191515), [#192298](https://github.com/pytorch/pytorch/pull/192298), [#194792](https://github.com/pytorch/pytorch/pull/194792), [#194793](https://github.com/pytorch/pytorch/pull/194793), [#194873](https://github.com/pytorch/pytorch/pull/194873), [#195231](https://github.com/pytorch/pytorch/pull/195231), [#195538](https://github.com/pytorch/pytorch/pull/195538), [#193940](https://github.com/pytorch/pytorch/pull/193940), [#196984](https://github.com/pytorch/pytorch/pull/196984))
- Extend host-side TMA descriptors to the Blackwell persistent TMA GEMM template, and support Triton kernels that need global scratch memory in the static launcher ([#191133](https://github.com/pytorch/pytorch/pull/191133), [#193857](https://github.com/pytorch/pytorch/pull/193857), [#194126](https://github.com/pytorch/pytorch/pull/194126), [#196410](https://github.com/pytorch/pytorch/pull/196410), [#196998](https://github.com/pytorch/pytorch/pull/196998))
- Add CUDA Graph Trees options `triton.cudagraph_managed_input_rerecord_limit`, `triton.cudagraph_initial_mempool_allocation_gb` and `triton.cudagraph_dynamic_shape_rerecord_limit` to limit re-recording and memory-pool fragmentation ([#191369](https://github.com/pytorch/pytorch/pull/191369), [#196378](https://github.com/pytorch/pytorch/pull/196378), [#197433](https://github.com/pytorch/pytorch/pull/197433))
- Add `autotune_cudagraph_benchmarking_iters` and hold the benchmark lock across multi-kernel comparisons to reduce autotuning noise ([#196413](https://github.com/pytorch/pytorch/pull/196413), [#192876](https://github.com/pytorch/pytorch/pull/192876))
- Add B200, GB300 and more ROCm GPUs to Inductor's device table so roofline heuristics such as `pad_mm` use datasheet values ([#194297](https://github.com/pytorch/pytorch/pull/194297), [#196398](https://github.com/pytorch/pytorch/pull/196398), [#196506](https://github.com/pytorch/pytorch/pull/196506), [#196944](https://github.com/pytorch/pytorch/pull/196944), [#198220](https://github.com/pytorch/pytorch/pull/198220))
- Improve combo kernels with runtime per-subkernel block-size tuning and grouping across dependency layers ([#189003](https://github.com/pytorch/pytorch/pull/189003), [#192622](https://github.com/pytorch/pytorch/pull/192622))
- Support the ROCm 7.14+ CK-Tile GEMM API and avoid compile-time blowups in ROCm Composable Kernel builds ([#189646](https://github.com/pytorch/pytorch/pull/189646), [#195023](https://github.com/pytorch/pytorch/pull/195023))
- Add `fusion_memory_timeline_peak_memory_increase_gb` and `fusion_memory_timeline_peak_memory_pct_threshold` to reject fusions that raise peak memory ([#190344](https://github.com/pytorch/pytorch/pull/190344))
- Add an opt-in Triton `bmm` template for a batch-broadcast left operand (`bmm_shared_a`) ([#193049](https://github.com/pytorch/pytorch/pull/193049))
- Add `alignment_asserts_inputs` to assert, rather than silently clone, misaligned graph inputs ([#196379](https://github.com/pytorch/pytorch/pull/196379))
- Accept out-of-tree backend config values as `"<device>.<key>"` in `torch.compile(options=...)` ([#194998](https://github.com/pytorch/pytorch/pull/194998))
- Honor `assume_32bit_indexing` for dynamic size arguments ([#194127](https://github.com/pytorch/pytorch/pull/194127))
- Keep Triton FP fusion on for templates to preserve numerics with Triton 3.9 ([#199500](https://github.com/pytorch/pytorch/pull/199500))
- Apply split/cat optimizations to `torch.concatenate` ([#195174](https://github.com/pytorch/pytorch/pull/195174))
- Reuse the CUTLASS sm120 kernel generators on sm121 GPUs ([#197621](https://github.com/pytorch/pytorch/pull/197621))
- Add an opt-in `bmm_skip_dynamic_shape_dim_check` to decompose CPU `bmm` whose batch size cannot be proven ([#197016](https://github.com/pytorch/pytorch/pull/197016))
- Add `"strict_pointwise"` and `"strict_reduction"` values to `torch._inductor.config.numerics` and make `"strict"` match eager numerics more closely ([#192883](https://github.com/pytorch/pytorch/pull/192883), [#195640](https://github.com/pytorch/pytorch/pull/195640))

## Ahead-Of-Time Inductor (AOTI)

- Support `torch.compiler.nested_compile_region` in the AOTInductor C++ wrapper ([#194703](https://github.com/pytorch/pytorch/pull/194703), [#194704](https://github.com/pytorch/pytorch/pull/194704))
- Support host-side TMA `TensorDescriptor` arguments in `torch.library.triton_op` ([#193608](https://github.com/pytorch/pytorch/pull/193608)) and Triton's `launch_pdl` option ([#194079](https://github.com/pytorch/pytorch/pull/194079)) in AOTInductor C++ wrappers
- Return `AOTI_RUNTIME_FAILURE` from AOTInductor runtime entry points instead of letting C++ exceptions unwind across the C ABI ([#194613](https://github.com/pytorch/pytorch/pull/194613))
- Add `config.aot_inductor.check_upperbound` to control whether `AOTI_RUNTIME_CHECK_INPUTS=1` rejects dimensions above the compile-time upper bound ([#196131](https://github.com/pytorch/pytorch/pull/196131))
- Add `TORCHINDUCTOR_LITE_MODE=1` to apply `torch.compile(mode="lite")` globally, including to AOTInductor compilation ([#195880](https://github.com/pytorch/pytorch/pull/195880))
- Add `torch._inductor.config.unsafe_skip_scalar_range_asserts` to skip generated range asserts when compile-time bounds are too strict ([#192857](https://github.com/pytorch/pytorch/pull/192857))
- Reduce peak device memory during AOTInductor compilation ([#197462](https://github.com/pytorch/pytorch/pull/197462), [#197659](https://github.com/pytorch/pytorch/pull/197659))
- Extend AOTInductor C++ wrapper kernel profiling to fallback, template and combo kernels ([#179699](https://github.com/pytorch/pytorch/pull/179699), [#198433](https://github.com/pytorch/pytorch/pull/198433), [#179700](https://github.com/pytorch/pytorch/pull/179700), [#191063](https://github.com/pytorch/pytorch/pull/191063))
- `torch._inductor.aoti_load_package` now loads an extracted package directory directly ([#195115](https://github.com/pytorch/pytorch/pull/195115))
- Explain how to fix a missing pytree registration when loading a package that returns a custom type ([#186900](https://github.com/pytorch/pytorch/pull/186900))
- Add `AOTI_TORCH_SAVE_DIR` to choose where the AOTInductor debug printer saves tensors ([#195869](https://github.com/pytorch/pytorch/pull/195869))

## Export

- Include compile and frame IDs in non-strict export `TORCH_TRACE` logs ([#186495](https://github.com/pytorch/pytorch/pull/186495))

## AOTDispatcher

- Stop bypassing the AOTAutograd cache for `inference_mode` regions ([#191409](https://github.com/pytorch/pytorch/pull/191409))

## Composability

- Add meta implementations for `torch.histogramdd` helper ops, enabling fake-tensor tracing ([#198897](https://github.com/pytorch/pytorch/pull/198897))
- Keep backed dimensions with hint 1 symbolic in `expand` and broadcasting ([#198258](https://github.com/pytorch/pytorch/pull/198258))
- Support fake-tensor tracing of sparse compressed tensor constructors and `_to_dense` ([#192091](https://github.com/pytorch/pytorch/pull/192091))

## Quantization

- Support pruned tables in quantized `embedding_bag` on CUDA ([#194934](https://github.com/pytorch/pytorch/pull/194934))

## C++ Frontend

- Added support for no-GIL-compatible inline C++ extensions ([#196802](https://github.com/pytorch/pytorch/pull/196802))
- Added check for compatible `TORCH_TARGET_VERSION` and `libtorch` headers ([#193962](https://github.com/pytorch/pytorch/pull/193962))
- Clarified the error for unsupported symbolic C++ kernel signatures ([#197736](https://github.com/pytorch/pytorch/pull/197736))
- Support `torch.utils.cpp_extension` CUDA builds on Windows ARM64 ([#191656](https://github.com/pytorch/pytorch/pull/191656))

## Release Engineering

- Add CUDA 13.4 (GA release, `cu134`) wheel and libtorch builds for Linux x86_64, Linux aarch64 and Windows, with cuBLAS 13.8.1 and cuDNN 9.26; the Linux wheels depend on `cupti-python` 13.4.0 (not installed on Python 3.15 and free-threaded interpreters) ([#196560](https://github.com/pytorch/pytorch/pull/196560), [#194996](https://github.com/pytorch/pytorch/pull/194996), [#196014](https://github.com/pytorch/pytorch/pull/196014), [#199269](https://github.com/pytorch/pytorch/pull/199269), [#194942](https://github.com/pytorch/pytorch/pull/194942), [#197212](https://github.com/pytorch/pytorch/pull/197212), [#198912](https://github.com/pytorch/pytorch/pull/198912), [#194905](https://github.com/pytorch/pytorch/pull/194905), [#192769](https://github.com/pytorch/pytorch/pull/192769), [#197764](https://github.com/pytorch/pytorch/pull/197764))
- Update the CUDA 13.2 wheels to CUDA 13.2.2, on Linux and Windows ([#196351](https://github.com/pytorch/pytorch/pull/196351), [#198843](https://github.com/pytorch/pytorch/pull/198843))
- Update the bundled Triton to 3.9, including the Intel XPU Triton ([#190440](https://github.com/pytorch/pytorch/pull/190440), [#195006](https://github.com/pytorch/pytorch/pull/195006))
- Add gfx1250 (MI450) to the ROCm wheel architectures and build the ROCm CI against ROCm 10.0 ([#196610](https://github.com/pytorch/pytorch/pull/196610), [#194794](https://github.com/pytorch/pytorch/pull/194794))
- Update the XPU wheels to Intel Deep Learning Essentials 2026.1.3 (`intel-sycl-rt`, `dpcpp-cpp-rt` and `intel-opencl-rt` 2026.1.2, `oneccl` 2022.1.2, `intel-pti` 1.1.0), and build the Linux XPU CI and CD images with Intel OMIX ([#195128](https://github.com/pytorch/pytorch/pull/195128), [#187900](https://github.com/pytorch/pytorch/pull/187900))
- Upgrade NVSHMEM to 3.7.2 ([#194279](https://github.com/pytorch/pytorch/pull/194279))

## CUDA

- Support scalar `scatter` for float8 dtypes on CUDA ([#197199](https://github.com/pytorch/pytorch/pull/197199))
- Extend CUDA graph kernel annotations: an `annotation_config` argument to `torch.cuda.graph` with a CUPTI backend ([#191999](https://github.com/pytorch/pytorch/pull/191999)), `key_by="source"` and `"auto"` modes that can annotate kernels inside nested `torch.cond` / `torch.while_loop` bodies ([#196528](https://github.com/pytorch/pytorch/pull/196528), [#196530](https://github.com/pytorch/pytorch/pull/196530), [#197577](https://github.com/pytorch/pytorch/pull/197577)), and a `cuda_graph_annotations` argument to `export_chrome_trace` that writes them into the trace ([#194854](https://github.com/pytorch/pytorch/pull/194854))
- `CUDAGraph.get_graph_data()` now reports kernel grid and block dimensions, dynamic shared memory size, and programmatic dependency edges ([#196018](https://github.com/pytorch/pytorch/pull/196018), [#196527](https://github.com/pytorch/pytorch/pull/196527))
- Add `PYTORCH_CUDA_ALLOC_CONF` options `expandable_segments_reserve` and `expandable_segments_reserve_by_class` to shrink the virtual-address reservation of expandable segments ([#192269](https://github.com/pytorch/pytorch/pull/192269)), and explain these options when that reservation fails ([#193211](https://github.com/pytorch/pytorch/pull/193211))
- CUDA out-of-memory errors now say when a custom `MemPool` allocator returned a null pointer ([#199363](https://github.com/pytorch/pytorch/pull/199363))
- Add opt-in `TORCH_CUDA_CHECK_STRAY_CONTEXT=warn|error`, which makes `torch.cuda.set_device` warn or raise when another device already holds a CUDA primary context ([#191036](https://github.com/pytorch/pytorch/pull/191036))

## CPU (AArch64)

- Make float32 `sum` and `norm` on NEON use the same accumulation order as AVX2 and SVE256, so results are bitwise identical across these CPU types; NEON results can differ from earlier releases in the last bits ([#197037](https://github.com/pytorch/pytorch/pull/197037), [#197252](https://github.com/pytorch/pytorch/pull/197252))

## MPS

- Add MPS support for `torch.logspace`, `torch.take`/`Tensor.put_`, `torch.frexp`, `torch.heaviside`, `torch.special.laguerre_polynomial_l`, and unsigned integer comparisons ([#190495](https://github.com/pytorch/pytorch/pull/190495), [#192980](https://github.com/pytorch/pytorch/pull/192980), [#194110](https://github.com/pytorch/pytorch/pull/194110), [#195265](https://github.com/pytorch/pytorch/pull/195265), [#195225](https://github.com/pytorch/pytorch/pull/195225), [#198860](https://github.com/pytorch/pytorch/pull/198860))
- Add complex64 support on MPS for `linalg.lu_factor`, `linalg.lu_solve`, triangular solves and `tanh` backward ([#188473](https://github.com/pytorch/pytorch/pull/188473), [#195369](https://github.com/pytorch/pytorch/pull/195369), [#195861](https://github.com/pytorch/pytorch/pull/195861), [#195601](https://github.com/pytorch/pytorch/pull/195601))
- Support `sinh`, `hypot`, `ldexp` and other math ops in `torch.compile` on MPS ([#197403](https://github.com/pytorch/pytorch/pull/197403))
- Add `PYTORCH_MPS_METAL_VERSION` to choose the Metal language version ([#196881](https://github.com/pytorch/pytorch/pull/196881))
- Raise an error under `torch.use_deterministic_algorithms(True)` for nondeterministic MPS ops ([#195754](https://github.com/pytorch/pytorch/pull/195754))
- Compute half and bfloat16 `torch.lerp` in float on MPS ([#196923](https://github.com/pytorch/pytorch/pull/196923))
- Add a native MPS implementation of `torch.nn.functional.grouped_mm` for mixture-of-experts models ([#194933](https://github.com/pytorch/pytorch/pull/194933), [#198725](https://github.com/pytorch/pytorch/pull/198725))
- Add a native MPS implementation of `torch._int_mm`, which also enables it in AOTInductor on MPS ([#193153](https://github.com/pytorch/pytorch/pull/193153))

## ROCm

- Enable Composable Kernel (CK) SDPA flash attention on RDNA4 (gfx1200/gfx1201) ([#188114](https://github.com/pytorch/pytorch/pull/188114))
- Update AOTriton to 0.14.2b, adding FlyDSL SDPA kernels for gfx950 and gfx1201 and several attention correctness fixes ([#197747](https://github.com/pytorch/pytorch/pull/197747))
- Add a gfx950 pre-swizzled MX FP4/FP8 block-scale layout for `scaled_mm` (`SwizzleType.SWIZZLE_32_8`) ([#190290](https://github.com/pytorch/pytorch/pull/190290)), and allow all operand layouts in `torch._scaled_mm` with FP8 tensorwise scaling ([#196884](https://github.com/pytorch/pytorch/pull/196884))
- Add gfx1250 Tensor Data Mover support to Inductor for `mm`/`addmm`, pointwise and reduction codegen, and FlexAttention ([#191166](https://github.com/pytorch/pytorch/pull/191166), [#196525](https://github.com/pytorch/pytorch/pull/196525), [#197329](https://github.com/pytorch/pytorch/pull/197329))
- Fall back to the native RNN implementation when MIOpen RNN fails at runtime ([#189658](https://github.com/pytorch/pytorch/pull/189658))
- Report AOTriton attention launch failures from the attention op that caused them ([#194100](https://github.com/pytorch/pytorch/pull/194100))

## XPU

- Add `no_split` and `use_on_oom` support to `torch.xpu.MemPool` ([#192048](https://github.com/pytorch/pytorch/pull/192048), [#192033](https://github.com/pytorch/pytorch/pull/192033), [#192038](https://github.com/pytorch/pytorch/pull/192038))
- Support `torch.xpu.mem_get_info` and `torch.accelerator.get_memory_info` with a pluggable XPU allocator ([#197412](https://github.com/pytorch/pytorch/pull/197412))
- Add XPU support for `linalg.polar`, `linalg.qr` (out variant), `geqrf`, `linalg.householder_product`, `sparse.spsolve` and sparse `linalg.vector_norm`; `linalg.qr`, `geqrf` and `linalg.householder_product` now run natively instead of falling back to CPU ([#188253](https://github.com/pytorch/pytorch/pull/188253), [#187564](https://github.com/pytorch/pytorch/pull/187564), [#189372](https://github.com/pytorch/pytorch/pull/189372), [#194165](https://github.com/pytorch/pytorch/pull/194165), [#189238](https://github.com/pytorch/pytorch/pull/189238), [#193110](https://github.com/pytorch/pytorch/pull/193110))
- Use the XPU SDPA backend for multi-query attention even when `enable_gqa=True` is not passed, consistent with the CUDA and CPU checks ([#196731](https://github.com/pytorch/pytorch/pull/196731))
- Support unsigned integer dtypes in `where` and float8 in `scatter` fill on XPU ([#198720](https://github.com/pytorch/pytorch/pull/198720))
- Add mixed-precision support to the fused `Adam` and `AdamW` implementations on XPU ([#200289](https://github.com/pytorch/pytorch/pull/200289))
- Support large tensors in `upsample_bilinear2d` channels-last by using 64-bit indexing ([#200289](https://github.com/pytorch/pytorch/pull/200289))
- Support stateless Philox RNG operations `_philox_normal` and `_philox_uniform` on XPU ([#198200](https://github.com/pytorch/pytorch/pull/198200))
- Enable symmetric memory on XPU by registering a SymmetricMemory allocator for `torch.xpu.MemPool` ([#197065](https://github.com/pytorch/pytorch/pull/197065), [#198720](https://github.com/pytorch/pytorch/pull/198720))
- Support `Float4_e2m1fn_x2` and `Float8_e8m0fnu` in XCCL non-reduction collectives ([#198200](https://github.com/pytorch/pytorch/pull/198200))

## Sparse Frontend

- Enable FP8 2:4 sparsity on ROCm MI300 ([#191682](https://github.com/pytorch/pytorch/pull/191682))

# Bug Fixes

## Python Frontend

- Fix `torch.asarray` on buffer-protocol objects to take the dtype from the buffer format ([#188784](https://github.com/pytorch/pytorch/pull/188784))
- Fix `torch.load` with `map_location="meta"` or `FakeTensorMode` losing storage sharing ([#193566](https://github.com/pytorch/pytorch/pull/193566))
- Fix `torch.aminmax` returning wrong results for overlapping `out=` tensors ([#195342](https://github.com/pytorch/pytorch/pull/195342))
- Fix `torch.accelerator.empty_host_cache()` segfaulting on MPS ([#197593](https://github.com/pytorch/pytorch/pull/197593))
- Fix `Multinomial.entropy()` precision for `float64` and after `expand()` ([#198006](https://github.com/pytorch/pytorch/pull/198006))
- Fix `torch.finfo(torch.float8_e5m2fnuz).eps` being off by 2x ([#198855](https://github.com/pytorch/pytorch/pull/198855))
- Fix `Tensor.__dlpack__` exporting tensors on a non-current non-CUDA device ([#195721](https://github.com/pytorch/pytorch/pull/195721))
- Fix `torch.isinf`/`isfinite` raising for fp8 dtypes without infinity ([#197444](https://github.com/pytorch/pytorch/pull/197444))
- Fix `torch.isfinite` reporting NaN as finite for `float8_e8m0fnu` ([#199878](https://github.com/pytorch/pytorch/pull/199878))
- Fix `torch.linspace` for `float16` and `bfloat16` on CPU, and `torch.linspace` and `torch.logspace` on CUDA, losing precision because the step was rounded to the output dtype; for example element 3 of `torch.linspace(0, 10, 38, dtype=torch.half)` on CPU was `0.8105` instead of the correctly rounded `0.8110` ([#198415](https://github.com/pytorch/pytorch/pull/198415))

## torch.nn

- Fix wrong gradients in cuDNN/MIOpen RNN backward with non-contiguous saved outputs, a repeated dropout mask in multi-layer MIOpen RNNs, and segfaults in RNN cells and the packed RNN fallback ([#198773](https://github.com/pytorch/pytorch/pull/198773), [#189285](https://github.com/pytorch/pytorch/pull/189285), [#191232](https://github.com/pytorch/pytorch/pull/191232), [#197560](https://github.com/pytorch/pytorch/pull/197560))
- Fix CUDA `softmax`/`log_softmax` gradients, `layer_norm` (CUDA backward and ROCm forward) and memory-efficient SDPA on very large tensors ([#188031](https://github.com/pytorch/pytorch/pull/188031), [#193016](https://github.com/pytorch/pytorch/pull/193016), [#199438](https://github.com/pytorch/pytorch/pull/199438), [#199594](https://github.com/pytorch/pytorch/pull/199594))
- Fix `varlen_attn` ignoring the `sdpa_kernel` backend selection, defects in its cuDNN backend, and FlashAttention-4 split selection ([#193631](https://github.com/pytorch/pytorch/pull/193631), [#194818](https://github.com/pytorch/pytorch/pull/194818), [#198872](https://github.com/pytorch/pytorch/pull/198872))
- Fix memory-efficient SDPA with `causal_lower_right` when the query is longer than the key ([#193632](https://github.com/pytorch/pytorch/pull/193632))
- Fix `grid_sample` returning zeros with the AVX512 CPU kernel ([#197635](https://github.com/pytorch/pytorch/pull/197635))
- Fix `weight_norm` producing `nan` gradients for empty inputs on CPU ([#192179](https://github.com/pytorch/pytorch/pull/192179))
- Raise errors instead of segfaulting in eval-mode `native_batch_norm` without running stats and in `max_pool1d`/`F.unfold` with overflowing sizes ([#194031](https://github.com/pytorch/pytorch/pull/194031), [#194112](https://github.com/pytorch/pytorch/pull/194112))
- Fix `rms_norm` with an engaged but undefined C++ weight ([#195574](https://github.com/pytorch/pytorch/pull/195574))
- Fix `pixel_shuffle`/`pixel_unshuffle` meta errors for non-positive factors ([#195224](https://github.com/pytorch/pytorch/pull/195224))
- Keep the `Module.to_empty()` hint in meta-module `to()` errors with `TORCH_SHOW_CPP_STACKTRACES=1` ([#191151](https://github.com/pytorch/pytorch/pull/191151))
- Fix nondeterministic NaNs in memory-efficient attention forward with head dimension 256 or larger on Ampere, Ada and consumer Blackwell GPUs ([#198922](https://github.com/pytorch/pytorch/pull/198922))
- Unify padding and pooling shape checks across CPU, CUDA and MPS ([#196457](https://github.com/pytorch/pytorch/pull/196457), [#196230](https://github.com/pytorch/pytorch/pull/196230))

## Optimizer

- Fix `Muon` overwriting momentum with bf16 grads ([#194664](https://github.com/pytorch/pytorch/pull/194664))

## Autograd

- Fix `torch.fmin`/`fmax` gradients when one input is NaN ([#193035](https://github.com/pytorch/pytorch/pull/193035))
- Fix hooks on a view after an in-place update of its base using a stale `grad_fn` ([#196514](https://github.com/pytorch/pytorch/pull/196514))
- Fix fast-mode `gradcheck` checking the wrong output or raising `IndexError` ([#194222](https://github.com/pytorch/pytorch/pull/194222), [#194991](https://github.com/pytorch/pytorch/pull/194991))
- Fix `region_activation_memory_budget` across graph breaks ([#194808](https://github.com/pytorch/pytorch/pull/194808))
- Fix a segfault accessing a saved tensor after a pack hook raised ([#189160](https://github.com/pytorch/pytorch/pull/189160))

## Distributed (c10d)

- Fix new NCCL backend lifetime bugs: a crash or hang when `Work` outlives `destroy_process_group()`, tensors kept alive after `wait_tensor`, a stray CUDA context on GPU 0, failed nonblocking splits treated as ready, and errors destroying a group used in CUDA graphs ([#195485](https://github.com/pytorch/pytorch/pull/195485), [#193239](https://github.com/pytorch/pytorch/pull/193239), [#198339](https://github.com/pytorch/pytorch/pull/198339), [#199263](https://github.com/pytorch/pytorch/pull/199263), [#199226](https://github.com/pytorch/pytorch/pull/199226))
- Fix the flight recorder not attaching to `nccl` groups that use the new NCCL backend ([#192858](https://github.com/pytorch/pytorch/pull/192858))
- Fix single-rank legacy NCCL `reduce_scatter` dropping the `PREMUL_SUM` factor ([#198961](https://github.com/pytorch/pytorch/pull/198961))
- Fix all-zero gradients from coalesced functional collectives under `torch.compile` ([#196077](https://github.com/pytorch/pytorch/pull/196077))
- Fix functional `all_gather_single` with a negative `gather_dim` ([#194865](https://github.com/pytorch/pytorch/pull/194865))
- Fix `split_group` rejecting valid splits or hanging when backends differ from the default group ([#195758](https://github.com/pytorch/pytorch/pull/195758), [#197568](https://github.com/pytorch/pytorch/pull/197568))
- Fix a segfault when registering a second device for a backend type without passing a backend ([#195536](https://github.com/pytorch/pytorch/pull/195536))
- Fix Python `ProcessGroup` subclasses' `reconfigure` overrides being bypassed from C++ ([#198251](https://github.com/pytorch/pytorch/pull/198251))
- Fix `LocalTensorMode` collectives on groups with unsorted ranks ([#192777](https://github.com/pytorch/pytorch/pull/192777))
- Fix `NCCL host communicator for group ... not found` errors from separately linked extensions ([#193942](https://github.com/pytorch/pytorch/pull/193942))
- Fix symmetric memory synchronization: no-op NVSHMEM `barrier()`/`put_signal()`/`wait_signal()`, stream ordering, rendezvous and multicast hangs, signal-pad races, and freeing memory still in use ([#192579](https://github.com/pytorch/pytorch/pull/192579), [#195947](https://github.com/pytorch/pytorch/pull/195947), [#196350](https://github.com/pytorch/pytorch/pull/196350), [#195596](https://github.com/pytorch/pytorch/pull/195596), [#196546](https://github.com/pytorch/pytorch/pull/196546), [#192300](https://github.com/pytorch/pytorch/pull/192300), [#198306](https://github.com/pytorch/pytorch/pull/198306), [#196003](https://github.com/pytorch/pytorch/pull/196003))
- Fix `register_mem_pool(pool, symm=True)` on the `nccl` backend not registering later pool segments as symmetric windows ([#200771](https://github.com/pytorch/pytorch/pull/200771))
- Fix `all_gather` on the `nccl` backend failing with `RuntimeError: shape '[...]' is invalid for input of size 0` when outputs contain zero-element tensors ([#200585](https://github.com/pytorch/pytorch/pull/200585)) (not in the final RC; ships only if another RC is cut)

## DTensor

- Fix context parallel FlexAttention with load balancing under graph capture and with non-default `BlockMask` block sizes ([#188766](https://github.com/pytorch/pytorch/pull/188766), [#198250](https://github.com/pytorch/pytorch/pull/198250))
- Fix graph capture with uneven shards and symbolic-size `Shard` splits that leave trailing ranks empty ([#195641](https://github.com/pytorch/pytorch/pull/195641), [#198168](https://github.com/pytorch/pytorch/pull/198168))

## Distributed FSDP

- Fix silently wrong gradients with `NO_SHARD` plus `CPUOffload(offload_params=True)` ([#194519](https://github.com/pytorch/pytorch/pull/194519))
- Fix mixed precision wrap overrides leaking between modules ([#194895](https://github.com/pytorch/pytorch/pull/194895))

## Distributed FSDP2

- Fix FSDP2 unshard under `torch.inference_mode()` ([#197327](https://github.com/pytorch/pytorch/pull/197327))
- Fix silently wrong gradients with `set_all_reduce_hook` on a separate stream ([#198804](https://github.com/pytorch/pytorch/pull/198804))
- Fix `AttributeError: 'FSDPParam' object has no attribute '_unsharded_param'` in gradient accumulation with unused parameters ([#194058](https://github.com/pytorch/pytorch/pull/194058))
- Fix `fully_shard` keeping prefetched all-gather outputs alive, a reduce-scatter use-after-free, and `cudaErrorStreamCaptureUnjoined` under CUDA graph capture ([#196460](https://github.com/pytorch/pytorch/pull/196460), [#193686](https://github.com/pytorch/pytorch/pull/193686), [#199677](https://github.com/pytorch/pytorch/pull/199677))
- Fix wrong float8 values in the single-rank all-gather path for `uint8` views ([#199733](https://github.com/pytorch/pytorch/pull/199733))

## Distributed (Miscellaneous)

- Fix `multiprocessing.spawn` treating a child's `KeyboardInterrupt` as success ([#194439](https://github.com/pytorch/pytorch/pull/194439))

## TorchElastic

- Fix the etcd server's `find_free_port()` raising `UnboundLocalError` and `EtcdServer` leaking its subprocess ([#191451](https://github.com/pytorch/pytorch/pull/191451), [#197711](https://github.com/pytorch/pytorch/pull/197711), [#197744](https://github.com/pytorch/pytorch/pull/197744))
- Fix `get_socket_with_port()` returning in-use ports (TCPStore `EADDRINUSE`) and a file-store rendezvous file descriptor leak ([#199015](https://github.com/pytorch/pytorch/pull/199015), [#191425](https://github.com/pytorch/pytorch/pull/191425))
- Fix truncated tailed worker logs and `launch_agent` shutdown errors hiding `ChildFailedError` ([#195211](https://github.com/pytorch/pytorch/pull/195211), [#195316](https://github.com/pytorch/pytorch/pull/195316))

## Distributed RPC

- Fix a use-after-free in `RRef` error handling ([#192960](https://github.com/pytorch/pytorch/pull/192960))

## Linear Algebra Frontend

- Fix silently wrong second-order forward AD for `linalg.det`, `slogdet` and `solve` ([#192667](https://github.com/pytorch/pytorch/pull/192667))
- Fix wrong `torch.linalg.matrix_exp` results for some inputs ([#196658](https://github.com/pytorch/pytorch/pull/196658))
- Fix wrong CPU `torch._int_mm` results for strided size-1 dimensions ([#194682](https://github.com/pytorch/pytorch/pull/194682))

## Profiler

- Fix inflated profiler device times from events sharing a correlation id ([#196282](https://github.com/pytorch/pytorch/pull/196282))
- Fix Cuspy teardown heap corruption and `record_function` kwargs sent as raw JSON ([#195471](https://github.com/pytorch/pytorch/pull/195471), [#196352](https://github.com/pytorch/pytorch/pull/196352))
- Fix several memory visualizer (MemoryViz) bugs, including wrong pool attribution and underreported peaks ([#199335](https://github.com/pytorch/pytorch/pull/199335), [#199415](https://github.com/pytorch/pytorch/pull/199415), [#193989](https://github.com/pytorch/pytorch/pull/193989))

## FX

- Keep `torch._check(not expr)` on a symbolic boolean as a runtime assertion, and fix a `TypeError` comparing two symbolic booleans ([#186043](https://github.com/pytorch/pytorch/pull/186043), [#186461](https://github.com/pytorch/pytorch/pull/186461))
- Fix stale results from a float argument baked into a cached graph under `specialize_float=False` ([#195040](https://github.com/pytorch/pytorch/pull/195040))
- Fix pickling `GraphModule`s from `aot_export_module` and non-strict export, and graphs with fake view tensors in metadata ([#186418](https://github.com/pytorch/pytorch/pull/186418), [#194771](https://github.com/pytorch/pytorch/pull/194771))
- Fix printing FX graphs with BSR or BSC tensors in node metadata ([#195253](https://github.com/pytorch/pytorch/pull/195253))
- Fix `replace_pattern` producing an invalid graph when adjacent matches share a node ([#185365](https://github.com/pytorch/pytorch/pull/185365))
- Fix memory leaks from `torch.fx.wrap` keeping caller frames alive and `torch.export` retaining every traced graph ([#198561](https://github.com/pytorch/pytorch/pull/198561), [#198295](https://github.com/pytorch/pytorch/pull/198295))
- Make the FX accelerator splitter's fusion discovery deterministic ([#198684](https://github.com/pytorch/pytorch/pull/198684))

## Dynamo

- Fix guards treating `-0.0` and `0.0` as equal and rejecting `NaN` constants, which reused graphs with the wrong float ([#192604](https://github.com/pytorch/pytorch/pull/192604), [#192608](https://github.com/pytorch/pytorch/pull/192608))
- Fix relational guards being skipped by the dict-version shortcut ([#185911](https://github.com/pytorch/pytorch/pull/185911))
- Guard autocast objects by value, fixing spurious recompiles and stale graphs ([#194754](https://github.com/pytorch/pytorch/pull/194754))
- Fix silently wrong results from `isinstance` with `@runtime_checkable` Protocols, zero-argument `super()` in classmethods, user descriptors, and closure-list mutations in local classes ([#196124](https://github.com/pytorch/pytorch/pull/196124), [#198435](https://github.com/pytorch/pytorch/pull/198435), [#198410](https://github.com/pytorch/pytorch/pull/198410), [#197830](https://github.com/pytorch/pytorch/pull/197830))
- Fix `random` module draws returning stale values on cache hits, ignoring `random.seed()`, or using float32 ([#196921](https://github.com/pytorch/pytorch/pull/196921), [#197221](https://github.com/pytorch/pytorch/pull/197221), [#199075](https://github.com/pytorch/pytorch/pull/199075))
- Fix `torch.Tensor(torch.Size([...]))` selecting the wrong overload ([#196717](https://github.com/pytorch/pytorch/pull/196717))
- Fix wrong or missing gradients with custom `autograd.Function`s under `torch.func`, graph breaks at `torch.autograd.grad`, and shape-changing `Parameter.data` assignments ([#193724](https://github.com/pytorch/pytorch/pull/193724), [#185829](https://github.com/pytorch/pytorch/pull/185829), [#186512](https://github.com/pytorch/pytorch/pull/186512))
- Fix compiled optimizer tracing permanently setting `capturable=True` in the optimizer's `param_groups` (visible after a graph break, e.g. in `optimizer.state_dict()`) ([#184704](https://github.com/pytorch/pytorch/pull/184704))
- Fix `out=` variants of `torch.max`, `torch.min` and `torch.topk` recompiling on every new shape ([#187952](https://github.com/pytorch/pytorch/pull/187952))
- Fix memory leaks keeping CUDA tensors, Python stacks, and higher-order op inputs alive after compilation ([#193015](https://github.com/pytorch/pytorch/pull/193015), [#197567](https://github.com/pytorch/pytorch/pull/197567), [#195954](https://github.com/pytorch/pytorch/pull/195954))
- Fix crashes, internal errors and guard edge cases, including `list.pop()` with a shape-derived index, in-place ops on `__torch_function__` subclasses, activation checkpointing with dynamic shapes, `torch._C._infer_size`, nested `torch.compile` calls, and `torch.random.fork_rng` ([#196590](https://github.com/pytorch/pytorch/pull/196590), [#193969](https://github.com/pytorch/pytorch/pull/193969), [#193254](https://github.com/pytorch/pytorch/pull/193254), [#185471](https://github.com/pytorch/pytorch/pull/185471), [#185742](https://github.com/pytorch/pytorch/pull/185742), [#184793](https://github.com/pytorch/pytorch/pull/184793), [#195413](https://github.com/pytorch/pytorch/pull/195413), [#191977](https://github.com/pytorch/pytorch/pull/191977), [#184977](https://github.com/pytorch/pytorch/pull/184977), [#185373](https://github.com/pytorch/pytorch/pull/185373), [#185462](https://github.com/pytorch/pytorch/pull/185462), [#186168](https://github.com/pytorch/pytorch/pull/186168), [#196865](https://github.com/pytorch/pytorch/pull/196865), [#198330](https://github.com/pytorch/pytorch/pull/198330), [#197191](https://github.com/pytorch/pytorch/pull/197191), [#197745](https://github.com/pytorch/pytorch/pull/197745), [#198153](https://github.com/pytorch/pytorch/pull/198153), [#194749](https://github.com/pytorch/pytorch/pull/194749), [#197049](https://github.com/pytorch/pytorch/pull/197049), [#197585](https://github.com/pytorch/pytorch/pull/197585), [#185300](https://github.com/pytorch/pytorch/pull/185300), [#198060](https://github.com/pytorch/pytorch/pull/198060))
- Fix stable Triton TMA descriptors, value-opaque object methods, and nanobind-bound C++ methods under `torch.compile` ([#185469](https://github.com/pytorch/pytorch/pull/185469), [#188799](https://github.com/pytorch/pytorch/pull/188799), [#188632](https://github.com/pytorch/pytorch/pull/188632), [#194556](https://github.com/pytorch/pytorch/pull/194556))
- Fix a graph-breaking debug f-string (`f"{x=}"`) abandoning the whole frame ([#186500](https://github.com/pytorch/pytorch/pull/186500))
- Fix thread-safety issues on Python 3.14 and free-threaded builds, and eval-frame state such as `set_stance(skip_guard_eval_unsafe=True)` leaking between threads ([#191281](https://github.com/pytorch/pytorch/pull/191281), [#199210](https://github.com/pytorch/pytorch/pull/199210), [#196637](https://github.com/pytorch/pytorch/pull/196637))
- Match CPython behavior for builtin container subclasses, `dict_keys` views, `frozenset`, `deque` edge cases, `range.index`, `operator.length_hint`, and unbound numeric dunders ([#193679](https://github.com/pytorch/pytorch/pull/193679), [#193649](https://github.com/pytorch/pytorch/pull/193649), [#193580](https://github.com/pytorch/pytorch/pull/193580), [#197454](https://github.com/pytorch/pytorch/pull/197454), [#195010](https://github.com/pytorch/pytorch/pull/195010), [#195029](https://github.com/pytorch/pytorch/pull/195029), [#195030](https://github.com/pytorch/pytorch/pull/195030), [#196711](https://github.com/pytorch/pytorch/pull/196711), [#196901](https://github.com/pytorch/pytorch/pull/196901), [#198482](https://github.com/pytorch/pytorch/pull/198482), [#198604](https://github.com/pytorch/pytorch/pull/198604), [#198726](https://github.com/pytorch/pytorch/pull/198726))
- Match CPython exception types and messages for constant-folded ops, `except X as e` scoping, `getattr()` argument checks, `.index()`, and attribute errors ([#198590](https://github.com/pytorch/pytorch/pull/198590), [#198380](https://github.com/pytorch/pytorch/pull/198380), [#196526](https://github.com/pytorch/pytorch/pull/196526), [#197443](https://github.com/pytorch/pytorch/pull/197443), [#198476](https://github.com/pytorch/pytorch/pull/198476), [#198512](https://github.com/pytorch/pytorch/pull/198512), [#192509](https://github.com/pytorch/pytorch/pull/192509), [#196080](https://github.com/pytorch/pytorch/pull/196080), [#195496](https://github.com/pytorch/pytorch/pull/195496))
- Fix minifier repros for non-UTF-8 output, symbolic shapes, FP64 softmax and `is_inference`, and keep the original backend failure ([#186546](https://github.com/pytorch/pytorch/pull/186546), [#196620](https://github.com/pytorch/pytorch/pull/196620), [#194827](https://github.com/pytorch/pytorch/pull/194827), [#194595](https://github.com/pytorch/pytorch/pull/194595), [#193565](https://github.com/pytorch/pytorch/pull/193565))
- Fix precompile and `aot_compile` artifacts: pruned interned values such as `torch.float32` failing on load (`argument 'dtype' must be torch.dtype, not _Missing`), one unserializable compile discarding others, and global-name collisions ([#197749](https://github.com/pytorch/pytorch/pull/197749), [#196505](https://github.com/pytorch/pytorch/pull/196505), [#196756](https://github.com/pytorch/pytorch/pull/196756), [#196895](https://github.com/pytorch/pytorch/pull/196895), [#196822](https://github.com/pytorch/pytorch/pull/196822), [#196814](https://github.com/pytorch/pytorch/pull/196814))
- Fix `canonicalize_output_graph_node_order` moving ops out of `inference_mode`, making outputs require grad ([#195518](https://github.com/pytorch/pytorch/pull/195518))
- Fix minifier repros failing for `repeat_interleave` with `int32` repeats ([#197035](https://github.com/pytorch/pytorch/pull/197035))

## Inductor

- Disable the 4x-vectorized Triton RNG path, which produced correlated CUDA dropout masks since 2.13 (`TORCHINDUCTOR_USE_RAND4X=1` restores it) ([#198680](https://github.com/pytorch/pytorch/pull/198680))
- Fix silently wrong results from in-place mutations: reinplaced scatters and `index_put` whose sources alias the input, `remove_noop_ops` on copies of mutated inputs, fusions across repeated mutations of one buffer, and mutations of buffers already referenced by views ([#198010](https://github.com/pytorch/pytorch/pull/198010), [#198132](https://github.com/pytorch/pytorch/pull/198132), [#198325](https://github.com/pytorch/pytorch/pull/198325), [#198549](https://github.com/pytorch/pytorch/pull/198549), [#198637](https://github.com/pytorch/pytorch/pull/198637))
- Fix silently wrong results for non-contiguous reshape views and `torch.while_loop` whose `cond_fn` mutates a captured tensor ([#192575](https://github.com/pytorch/pytorch/pull/192575), [#195393](https://github.com/pytorch/pytorch/pull/195393))
- Fix silently wrong gradients and results from mix-order reductions with views into a shared buffer (a regression since 2.10) or row counts not divisible by `XBLOCK` ([#193103](https://github.com/pytorch/pytorch/pull/193103), [#196565](https://github.com/pytorch/pytorch/pull/196565))
- Fix corrupted gradients from a reused `nested_compile_region` that inherited donated-buffer indices ([#193960](https://github.com/pytorch/pytorch/pull/193960))
- Fix wrong results from the Triton FP8 blockwise `scaled_mm` template, including DeepSeek-style scales ([#195751](https://github.com/pytorch/pytorch/pull/195751), [#197028](https://github.com/pytorch/pytorch/pull/197028), [#197458](https://github.com/pytorch/pytorch/pull/197458))
- Fix wrong results from SDPA pattern fusion when the key is permuted other than `key.transpose(-2, -1)`, and failures with a 0-d tensor scale ([#195383](https://github.com/pytorch/pytorch/pull/195383), [#191496](https://github.com/pytorch/pytorch/pull/191496))
- Fix wrong results in pre-/post-grad fusion passes: batched `aten.sub` dropping `alpha`, batched linear mixing dtypes, one-element tuple replacements, `merge_select_cat_aten`, and batch math fusion of `torch.clamp` and in-place dropout ([#195463](https://github.com/pytorch/pytorch/pull/195463), [#197069](https://github.com/pytorch/pytorch/pull/197069), [#197832](https://github.com/pytorch/pytorch/pull/197832), [#198638](https://github.com/pytorch/pytorch/pull/198638), [#198285](https://github.com/pytorch/pytorch/pull/198285))
- Fix compile failures in the partitioned scatter, joint-graph no-op removal and view cleanup passes and the constant `cumsum` pattern ([#194366](https://github.com/pytorch/pytorch/pull/194366), [#193052](https://github.com/pytorch/pytorch/pull/193052), [#193708](https://github.com/pytorch/pytorch/pull/193708), [#193422](https://github.com/pytorch/pytorch/pull/193422), [#193959](https://github.com/pytorch/pytorch/pull/193959))
- Fix compiled `torch.special.log_ndtr`, `torch.frexp` and `torch.nextafter` edge cases (signed zeros, subnormals, `float16`/`bfloat16`), `torch.randn` with `align_random_eager=True`, and `torch.nan_to_num` on complex inputs ([#191339](https://github.com/pytorch/pytorch/pull/191339), [#195041](https://github.com/pytorch/pytorch/pull/195041), [#196578](https://github.com/pytorch/pytorch/pull/196578), [#194118](https://github.com/pytorch/pytorch/pull/194118), [#190428](https://github.com/pytorch/pytorch/pull/190428))
- Accumulate `float16`/`bfloat16` Triton scans such as `cumsum` in `float32` ([#199088](https://github.com/pytorch/pytorch/pull/199088))
- Fix boolean `index_put(..., accumulate=True)` on GPU ([#193584](https://github.com/pytorch/pytorch/pull/193584))
- Fix compiled max pooling with indices returning transposed indices for non-contiguous inputs, and `adaptive_max_pool3d` gradients on channels-last inputs ([#197596](https://github.com/pytorch/pytorch/pull/197596), [#199068](https://github.com/pytorch/pytorch/pull/199068))
- Fix wrong `argmax`/`argmin` indices after layout changes or loop reordering ([#195178](https://github.com/pytorch/pytorch/pull/195178))
- Fix wrong results under `dynamic=True` when a dimension guarded equal to 1 is broadcast ([#198774](https://github.com/pytorch/pytorch/pull/198774))
- Fix dynamic-shape compile errors (`cannot determine truth value of Relational`, `GuardOnDataDependentSymNode`, `ValueRangeError`) with symbolic strides, unbacked tiling and reshapes, and negative `constant_pad_nd` padding ([#185871](https://github.com/pytorch/pytorch/pull/185871), [#196081](https://github.com/pytorch/pytorch/pull/196081), [#199105](https://github.com/pytorch/pytorch/pull/199105), [#195465](https://github.com/pytorch/pytorch/pull/195465))
- Fix wrong results on XPU from the `mm_plus_mm` and `bmm`/`baddbmm` Triton templates ([#189516](https://github.com/pytorch/pytorch/pull/189516))
- Fix crashes and wrong output from the Triton `grouped_mm` template on very large inputs ([#192649](https://github.com/pytorch/pytorch/pull/192649))
- Fix static-launcher `float16`/`bfloat16` scalar arguments being passed with the wrong width ([#184065](https://github.com/pytorch/pytorch/pull/184065))
- Fix CUDA Graph Trees capturing cross-device extern kernels, `Detected N tensor(s) in the cudagraph pool not tracked as outputs` errors with pending backwards, static kernels partitioned out under `cudagraph_skip_dynamic_graphs`, and backward graphs treating activations as static inputs ([#190555](https://github.com/pytorch/pytorch/pull/190555), [#194124](https://github.com/pytorch/pytorch/pull/194124), [#197139](https://github.com/pytorch/pytorch/pull/197139), [#197438](https://github.com/pytorch/pytorch/pull/197438))
- Fix `NameError` for complex indexed assignment with `mode="reduce-overhead"` and graph partitioning ([#199414](https://github.com/pytorch/pytorch/pull/199414))
- Fix `CUDA driver error: misaligned address` in backward for misaligned saved inputs ([#192263](https://github.com/pytorch/pytorch/pull/192263))
- Emit runtime asserts for backed `SymInt` inputs when `prefer_deferred_runtime_asserts_over_guards=True` ([#185588](https://github.com/pytorch/pytorch/pull/185588))
- Fix reordering of consecutive side-effectful ops that lower to different kernel types ([#188301](https://github.com/pytorch/pytorch/pull/188301))
- Fix a CPU buffer being passed to a CUDA kernel after an incorrect device-copy elimination ([#199402](https://github.com/pytorch/pytorch/pull/199402))
- Fix wrong results on MPS when masked loads were deduplicated ([#199673](https://github.com/pytorch/pytorch/pull/199673))
- Fix user-defined Triton kernels with mutated offset views (out-of-bounds reads), non-builtin `tl.constexpr` values, aliased `triton.language` imports, `float` literals, and buffer views in the FX wrapper backend ([#192227](https://github.com/pytorch/pytorch/pull/192227), [#189692](https://github.com/pytorch/pytorch/pull/189692), [#196237](https://github.com/pytorch/pytorch/pull/196237), [#190340](https://github.com/pytorch/pytorch/pull/190340), [#193820](https://github.com/pytorch/pytorch/pull/193820))
- Fix autotuning errors with deduplicated `bmm` inputs, pipelined autotuning, stale benchmark futures, decompose-K or ROCm `multi_kernel_hints` (`NoValidChoicesError`), 0-d `addmm` biases, `CantSplit` template-fusion choices, and deterministic combo kernels ([#188268](https://github.com/pytorch/pytorch/pull/188268), [#193094](https://github.com/pytorch/pytorch/pull/193094), [#196148](https://github.com/pytorch/pytorch/pull/196148), [#196453](https://github.com/pytorch/pytorch/pull/196453), [#196510](https://github.com/pytorch/pytorch/pull/196510), [#197214](https://github.com/pytorch/pytorch/pull/197214), [#199113](https://github.com/pytorch/pytorch/pull/199113), [#189724](https://github.com/pytorch/pytorch/pull/189724))
- Honor `max_autotune_gemm_search_space="EXHAUSTIVE"` with decompose-K and benchmark all candidates under the same CUDA graph policy ([#192285](https://github.com/pytorch/pytorch/pull/192285), [#194649](https://github.com/pytorch/pytorch/pull/194649))
- Fix crashes, stack overflows and graph cycles in overlap scheduling, `control_deps` lowering and manual collective bucketing, and remove duplicate waits on one collective ([#192268](https://github.com/pytorch/pytorch/pull/192268), [#192628](https://github.com/pytorch/pytorch/pull/192628), [#192903](https://github.com/pytorch/pytorch/pull/192903), [#195517](https://github.com/pytorch/pytorch/pull/195517), [#197323](https://github.com/pytorch/pytorch/pull/197323), [#199227](https://github.com/pytorch/pytorch/pull/199227), [#199228](https://github.com/pytorch/pytorch/pull/199228))
- Fix FlexAttention decoding reading the query at wrong offsets after a pointwise op, max-autotune failures with inlined captured buffers, and `TORCHINDUCTOR_EMIT_POINTER_RANGE_32=0` being ignored ([#198543](https://github.com/pytorch/pytorch/pull/198543), [#194555](https://github.com/pytorch/pytorch/pull/194555), [#194136](https://github.com/pytorch/pytorch/pull/194136))
- Fix NVGEMM errors in block-scaled GEMMs, with a broken optional `cutlass.operators` install, and when benchmarking aliased inputs ([#194727](https://github.com/pytorch/pytorch/pull/194727), [#198292](https://github.com/pytorch/pytorch/pull/198292), [#199072](https://github.com/pytorch/pytorch/pull/199072))
- Fix CPU backend compile errors for boolean vector masks, a spurious `ZeroDivisionError` from integer `%`, wrong mkldnn transposed-convolution channels, and integer `bmm` returning `int64` ([#184155](https://github.com/pytorch/pytorch/pull/184155), [#199560](https://github.com/pytorch/pytorch/pull/199560), [#192025](https://github.com/pytorch/pytorch/pull/192025), [#184950](https://github.com/pytorch/pytorch/pull/184950), [#191324](https://github.com/pytorch/pytorch/pull/191324))
- Fix ROCm CK-Tile GEMM autotuning dropping all `float16` kernels and `float8_e4m3fnuz`/`float8_e5m2fnuz` cast errors ([#193902](https://github.com/pytorch/pytorch/pull/193902), [#197905](https://github.com/pytorch/pytorch/pull/197905))
- Fix failures after fp32 matmul precision was set through `torch.backends.cuda.matmul.fp32_precision` ([#189955](https://github.com/pytorch/pytorch/pull/189955), [#196860](https://github.com/pytorch/pytorch/pull/196860))
- Fix kernel builds with only `libcuda.so.1`, the `CUDA_HOME` fallback for `nvcc`, ROCm on Windows, and DSL ops with `triton-rocm` ([#186538](https://github.com/pytorch/pytorch/pull/186538), [#197573](https://github.com/pytorch/pytorch/pull/197573), [#194471](https://github.com/pytorch/pytorch/pull/194471), [#195022](https://github.com/pytorch/pytorch/pull/195022))
- Fail instead of hanging when a compile worker dies, and treat a cleared local cache as a miss ([#192301](https://github.com/pytorch/pytorch/pull/192301), [#196189](https://github.com/pytorch/pytorch/pull/196189))
- Fix `AttributeError` with `torch._foreach_pow` on integer tensors ([#198675](https://github.com/pytorch/pytorch/pull/198675))
- Fix compile crashes for `float16`/`bfloat16` floor division of `arange` values, nested grouped-reduction epilogues, fallback kernels without tensor inputs, and an early `FakeTensorUpdater` ([#197132](https://github.com/pytorch/pytorch/pull/197132), [#195874](https://github.com/pytorch/pytorch/pull/195874), [#197584](https://github.com/pytorch/pytorch/pull/197584), [#196946](https://github.com/pytorch/pytorch/pull/196946))
- Fix symmetric-memory `alloc_id` size-mismatch errors after reseeding `random` between compilations ([#192089](https://github.com/pytorch/pytorch/pull/192089))
- Fix Triton-based TFLOPS estimates being off by 1000x ([#196372](https://github.com/pytorch/pytorch/pull/196372))
- Fix Triton template kernels being compiled twice when the worker pool is warm ([#197471](https://github.com/pytorch/pytorch/pull/197471))
- Fix wrong results from fusions that dropped non-default kwargs such as `add(..., alpha=a)`; `add` with `alpha != 1` is no longer fused into `addmm` ([#199871](https://github.com/pytorch/pytorch/pull/199871), [#200442](https://github.com/pytorch/pytorch/pull/200442))
- Fix `InductorError: AttributeError: 'NotImplementedType' object has no attribute 'expr'` when fusing a prologue with a `float16`/`bfloat16` cast into a Triton matmul ([#201029](https://github.com/pytorch/pytorch/pull/201029))

## Ahead-Of-Time Inductor (AOTI)

- Fix AOTInductor failures when operators fall back to ATen through the proxy executor or C shim, as under `torch.compile(mode="lite")` ([#193767](https://github.com/pytorch/pytorch/pull/193767), [#199204](https://github.com/pytorch/pytorch/pull/199204), [#193768](https://github.com/pytorch/pytorch/pull/193768), [#194261](https://github.com/pytorch/pytorch/pull/194261), [#194262](https://github.com/pytorch/pytorch/pull/194262), [#194324](https://github.com/pytorch/pytorch/pull/194324), [#194700](https://github.com/pytorch/pytorch/pull/194700))
- Fix AOTInductor C++ wrapper compile failures: undeclared `int_array_N` ([#193621](https://github.com/pytorch/pytorch/pull/193621)), duplicate stream variables in `while_loop` ([#196324](https://github.com/pytorch/pytorch/pull/196324)), kernel profiling ([#179698](https://github.com/pytorch/pytorch/pull/179698)), unbacked symbols in `torch.cond` predicates ([#186094](https://github.com/pytorch/pytorch/pull/186094)), and custom ops returning nested tensor lists ([#194644](https://github.com/pytorch/pytorch/pull/194644))
- Fix AOTInductor packages losing buffer mutations to constant folding ([#185077](https://github.com/pytorch/pytorch/pull/185077))
- Fix `cond`/`while_loop` models with subgraph tensor constants failing with `Can not find the original value for ..._constant0` ([#199188](https://github.com/pytorch/pytorch/pull/199188))
- Fix runtime constant folding dispatching the wrong kernel through the proxy executor ([#199295](https://github.com/pytorch/pytorch/pull/199295))
- Fix AOTInductor runtime leaks of constant handles and mmap-backed constants ([#194480](https://github.com/pytorch/pytorch/pull/194480), [#195090](https://github.com/pytorch/pytorch/pull/195090)) and of hardware queues on ROCm ([#193249](https://github.com/pytorch/pytorch/pull/193249))
- Fix AOTInductor MPS artifacts failing to `dlopen` on other machines ([#198232](https://github.com/pytorch/pytorch/pull/198232)) and segfaulting on Metal compile errors ([#196634](https://github.com/pytorch/pytorch/pull/196634))
- Fix packaging of models that return `torch.return_types` outputs, e.g. from `torch.max` ([#197128](https://github.com/pytorch/pytorch/pull/197128))
- Fix AOTInductor dropping runtime assertions on data-dependent sizes in lite mode ([#199294](https://github.com/pytorch/pytorch/pull/199294))

## Export

- Fix data-dependent guard errors in export for tensor-valued `torch._assert` (now a runtime assertion), `scaled_dot_product_attention` with data-dependent head dims, and `torch.distributions` argument validation ([#186306](https://github.com/pytorch/pytorch/pull/186306), [#184983](https://github.com/pytorch/pytorch/pull/184983), [#186291](https://github.com/pytorch/pytorch/pull/186291))
- Fix `move_to_device_pass` leaving stale device arguments in generated code ([#185105](https://github.com/pytorch/pytorch/pull/185105))
- Fix deserializing exported programs with symbolic-size fake tensor constants ([#185025](https://github.com/pytorch/pytorch/pull/185025))
- Fix `... is not tracked with proxy` errors from the fake tensor dispatch cache ([#185100](https://github.com/pytorch/pytorch/pull/185100))
- Fix `torch.export.export` raising `GuardOnDataDependentSymNode` for `x[mask] = scalar` when `x` has a data-dependent size ([#200412](https://github.com/pytorch/pytorch/pull/200412))

## AOTDispatcher

- Fix compiling matmul or view ops on `Tensor` subclasses without `__torch_dispatch__` ([#193968](https://github.com/pytorch/pytorch/pull/193968))
- Fix a wrong copy-back into mutated inputs under `keep_inference_input_mutations` ([#198622](https://github.com/pytorch/pytorch/pull/198622))
- Fix AOTAutograd cache-key misses and crashes for some subclass metadata, and identical precompile fallback keys across ranks ([#193419](https://github.com/pytorch/pytorch/pull/193419), [#190080](https://github.com/pytorch/pytorch/pull/190080), [#191427](https://github.com/pytorch/pytorch/pull/191427))
- Fix `PendingUnbackedSymbolNotFound` when a compiled `saved_tensors_hooks` pack hook allocates unbacked SymInts ([#193258](https://github.com/pytorch/pytorch/pull/193258))
- Fix corrupted opaque constants in compiled graphs with tensor-subclass outputs ([#193190](https://github.com/pytorch/pytorch/pull/193190))
- Fix a min-cut partitioner crash on graphs with `torch.device` nodes ([#196146](https://github.com/pytorch/pytorch/pull/196146))
- Fix misaligned inputs reaching Inductor kernels after effect-token removal ([#198005](https://github.com/pytorch/pytorch/pull/198005))
- Fix version-counter errors in backward for inputs mutated outside the compiled graph ([#185876](https://github.com/pytorch/pytorch/pull/185876))
- Fix silently wrong results for `resize_()` on a no-op view of a returned intermediate ([#191844](https://github.com/pytorch/pytorch/pull/191844))
- Fix `assert_size_stride` failures on the second call of a compiled training graph under dynamic shapes ([#194420](https://github.com/pytorch/pytorch/pull/194420))

## Composability

- Fix wrong values and `nan` gradients when compiling `weight_norm` on 1-D parameters ([#198772](https://github.com/pytorch/pytorch/pull/198772))
- Fix compiled `torch.normal(mean, std)` output dtype with mixed float dtypes ([#194557](https://github.com/pytorch/pytorch/pull/194557))
- Fix fake/meta kernels: eager-matching `out=` dtype checks for many ops, symbolic `out=` bitwise shifts, and data-dependent `linalg.cross` ([#192383](https://github.com/pytorch/pytorch/pull/192383), [#193050](https://github.com/pytorch/pytorch/pull/193050), [#193555](https://github.com/pytorch/pytorch/pull/193555), [#194375](https://github.com/pytorch/pytorch/pull/194375), [#195767](https://github.com/pytorch/pytorch/pull/195767))
- Add fused GRU cell meta kernels so CUDA `nn.GRUCell` can be compiled ([#191156](https://github.com/pytorch/pytorch/pull/191156))
- Match eager in decompositions and refs on XPU (`native_layer_norm`), MPS (FFT strides, `logspace`) and MTIA (`masked_fill`) ([#198647](https://github.com/pytorch/pytorch/pull/198647), [#199030](https://github.com/pytorch/pytorch/pull/199030), [#195611](https://github.com/pytorch/pytorch/pull/195611))
- Fix `torch.cond` branch metadata mismatches from `math.trunc(s / 1)` on a `SymInt` ([#186194](https://github.com/pytorch/pytorch/pull/186194))
- Fix spurious `Tensor device mismatch` errors from the FakeTensor dispatch cache ([#197583](https://github.com/pytorch/pytorch/pull/197583))
- Raise `NotImplementedError` instead of `RuntimeError` for unsupported dtypes in linalg and norm ops, and for `mean`, `var`, `std` and related ops on integer tensors ([#192352](https://github.com/pytorch/pytorch/pull/192352), [#192351](https://github.com/pytorch/pytorch/pull/192351))
- Validate `attn_bias` and key/value shapes in the overrideable fused SDPA fake kernel ([#194271](https://github.com/pytorch/pytorch/pull/194271), [#198303](https://github.com/pytorch/pytorch/pull/198303))
- Match eager shape errors for meta transposed convolution and over-broadcast `addmm`/`addmv` inputs ([#188328](https://github.com/pytorch/pytorch/pull/188328), [#195594](https://github.com/pytorch/pytorch/pull/195594))
- Fix a crash on modulo of plain ints in symbolic shapes, and simplify `C * (x // C)` back to `x` ([#198395](https://github.com/pytorch/pytorch/pull/198395), [#198808](https://github.com/pytorch/pytorch/pull/198808))
- Fix guard errors for jagged `NestedTensor` inputs whose batch size changes or with `keepdim=True` reductions ([#193059](https://github.com/pytorch/pytorch/pull/193059), [#184628](https://github.com/pytorch/pytorch/pull/184628))

## Quantization

- Fix FX FP16/BF16 linear weight folding `KeyError` for shared weights ([#194292](https://github.com/pytorch/pytorch/pull/194292))

## ONNX

- Fix `torch.onnx.export(dynamo=True)` hardcoding LSTM/GRU output length under dynamic shapes ([#193192](https://github.com/pytorch/pytorch/pull/193192))

## C++ Frontend

- Fixed `torch::nn::Sequential::clone()` renaming submodules ([#195107](https://github.com/pytorch/pytorch/pull/195107))
- Fixed `multi_head_attention_forward` crashing with `num_heads=0` ([#195381](https://github.com/pytorch/pytorch/pull/195381))
- Fixed `std::numeric_limits<c10::BFloat16>::signaling_NaN()` returning infinity ([#195415](https://github.com/pytorch/pytorch/pull/195415))
- Fix a clang `time_t` compile error in `torch/csrc/stable/macros.h` ([#197021](https://github.com/pytorch/pytorch/pull/197021))

## Build Frontend

- Fix Windows MSVC source builds computing wrong results in `parallel_for` kernels, including CPU `scaled_dot_product_attention` ([#193792](https://github.com/pytorch/pytorch/pull/193792))
- Fix cross-compiled builds producing a `_C.so` that the target interpreter cannot import ([#189388](https://github.com/pytorch/pytorch/pull/189388))
- Fix BLAS/LAPACK detection for ATLAS, vecLib, BLIS and FlexiBLAS ([#196427](https://github.com/pytorch/pytorch/pull/196427), [#196428](https://github.com/pytorch/pytorch/pull/196428), [#196430](https://github.com/pytorch/pytorch/pull/196430))
- Fix the C++20 requirement not propagating through the CMake `torch` target or being checked on MSVC ([#190784](https://github.com/pytorch/pytorch/pull/190784), [#197417](https://github.com/pytorch/pytorch/pull/197417))

## Release Engineering

- Fix C++ compilation failures of `argmax` and `argmin` under `torch.compile` on s390x by moving the ZVECTOR `Vectorized` implementation to 16-byte vectors; s390x CPU builds now target z15 ([#173072](https://github.com/pytorch/pytorch/pull/173072))
- Fix the PEP 517 source distribution being left out of the GitHub release because it exceeded the 2 GiB asset limit (the plain source archive leaked into it), and check release asset sizes on every tag ([#195783](https://github.com/pytorch/pytorch/pull/195783))
- Fix CUDA builds from the source distribution or release tarball failing with "No download info given for 'nccl_external'": the NCCL pin files are now shipped, and a missing NCCL now fails with a message that names the fixes (`USE_SYSTEM_NCCL=1` or `USE_NCCL=0`) ([#197544](https://github.com/pytorch/pytorch/pull/197544))
- Fix ROCm 7.14 wheels printing `rocSHMEM Could not open libnuma` on `import torch` ([#195672](https://github.com/pytorch/pytorch/pull/195672))
- Fix Windows wheels failing to import with `[WinError 1114]` when an older `msvcp140.dll` (before 14.40) is already loaded ([#196987](https://github.com/pytorch/pytorch/pull/196987))
- Fix wheel license metadata listing license files for code that is not shipped, and Windows `MAX_PATH` failures while packaging them ([#185813](https://github.com/pytorch/pytorch/pull/185813))
- Fix standalone `cmake --install` scattering Python package files across the install prefix and writing into the source checkout ([#191494](https://github.com/pytorch/pytorch/pull/191494))
- Make Python 3.15 Linux wheels depend on `triton`, so `torch.compile` works on GPU after `pip install torch` ([#200294](https://github.com/pytorch/pytorch/pull/200294))
- Ship `top_level.txt` in wheels again, fixing slow `importlib.metadata.packages_distributions()` calls that delayed importing libraries like `transformers` ([#201347](https://github.com/pytorch/pytorch/pull/201347))

## CUDA

- Fix silently wrong results or illegal memory accesses from 32-bit index overflow on CUDA in `arange`, `range`, `linspace` and `logspace` ([#197713](https://github.com/pytorch/pytorch/pull/197713)), `cdist` backward ([#198452](https://github.com/pytorch/pytorch/pull/198452)), `bincount` ([#189685](https://github.com/pytorch/pytorch/pull/189685)), and `bmm` ([#196431](https://github.com/pytorch/pytorch/pull/196431))
- Fix CUDA batch norm under AMP overflowing to `inf` ([#196125](https://github.com/pytorch/pytorch/pull/196125))
- Fix a deadlock when a lazy-init callback such as `torch.cuda.manual_seed` re-enters CUDA lazy initialization ([#182948](https://github.com/pytorch/pytorch/pull/182948))
- Fix device-side assertions on CUDA 13 builds failing with `CUDA error: invalid argument` instead of reporting the assertion ([#195899](https://github.com/pytorch/pytorch/pull/195899))
- Fix CUDA graph annotation bugs: `mark_stream` mutating the caller's dict ([#194851](https://github.com/pytorch/pytorch/pull/194851)), leaked annotations ([#198418](https://github.com/pytorch/pytorch/pull/198418)), missing backward annotations with the CUPTI backend ([#194853](https://github.com/pytorch/pytorch/pull/194853)), and `get_graph_data()` failing on batch memory-operation nodes ([#193091](https://github.com/pytorch/pytorch/pull/193091))
- Fix `torch.cuda.make_graphed_callables` graphs being garbage-collected during an unrelated capture ([#195397](https://github.com/pytorch/pytorch/pull/195397))
- Fix `torch.cuda.empty_cache()` unmapping expandable segments on another device without synchronizing it ([#197159](https://github.com/pytorch/pytorch/pull/197159)), and expandable segments imported over IPC each reserving about 9/8 of device memory ([#198129](https://github.com/pytorch/pytorch/pull/198129))
- Recover from a corrupted or truncated JITerator kernel cache entry by recompiling the kernel ([#186346](https://github.com/pytorch/pytorch/pull/186346))
- Fix an illegal memory access in CUDA `embedding_bag` backward with `per_sample_weights` by adding the index bounds check the forward kernels already have ([#193408](https://github.com/pytorch/pytorch/pull/193408))
- Fall back to the ATen implementation of outer-product `bmm` when the Triton driver cannot be set up, instead of failing ([#197695](https://github.com/pytorch/pytorch/pull/197695))

## cuDNN

- Fix `scaled_dot_product_attention` with the cuDNN backend returning NaN query gradients on Hopper (H100/H200) for non-causal attention when the key/value sequence length is 64 modulo 128, and silently corrupting generation on B200 for models with fewer than 8 key/value heads; the wheels now ship cuDNN 9.26, and with older cuDNN versions the affected Hopper shapes fall back to another backend ([#196861](https://github.com/pytorch/pytorch/pull/196861), [#195492](https://github.com/pytorch/pytorch/pull/195492))

## CPU (x86)

- Fix the vectorized `double` to `int64` conversion on AVX2 CPUs, which was only exact within +/-2^51 and rounded to the nearest integer instead of truncating toward zero; it now truncates toward zero across the full `int64` range like other CPU instruction sets. Also fix the vectorized `int64` to `double` conversion returning `-0.0` for `0` when the rounding mode is round-toward-negative ([#196614](https://github.com/pytorch/pytorch/pull/196614), [#196607](https://github.com/pytorch/pytorch/pull/196607))

## CPU (AArch64)

- Fix contiguous float32, float16 and bfloat16 to `uint8` conversions of out-of-range values (for example `Tensor.byte()` on `-1`) on Arm CPUs saturating to `0` instead of wrapping around to `255` as on x86 and for strided inputs ([#196646](https://github.com/pytorch/pytorch/pull/196646), [#198744](https://github.com/pytorch/pytorch/pull/198744))
- Fix `torch.compile` of 4-bit dynamically quantized matmul on Arm CPUs without the dot-product extension ([#197518](https://github.com/pytorch/pytorch/pull/197518))

## MPS

- Fix crashes and wrong results in MPS `linalg.svd`, `linalg.lstsq` and `linalg.solve` ([#195949](https://github.com/pytorch/pytorch/pull/195949), [#196128](https://github.com/pytorch/pytorch/pull/196128), [#195872](https://github.com/pytorch/pytorch/pull/195872), [#196139](https://github.com/pytorch/pytorch/pull/196139), [#199063](https://github.com/pytorch/pytorch/pull/199063), [#199694](https://github.com/pytorch/pytorch/pull/199694), [#199031](https://github.com/pytorch/pytorch/pull/199031))
- Fix `torch.compile` on MPS: wrong `argmax`/`argmin` indices, `channels_last` conv backward stride errors, and a misleading "Not enough SMs" warning ([#199134](https://github.com/pytorch/pytorch/pull/199134), [#199132](https://github.com/pytorch/pytorch/pull/199132), [#174241](https://github.com/pytorch/pytorch/pull/174241), [#192375](https://github.com/pytorch/pytorch/pull/192375))
- Raise errors instead of aborting the process on MPS for mixed-dtype inputs (`batch_norm`, `mse_loss`, `addr`, ...), 1-D-weight `linear` backward, empty `BCELoss`, and failures inside dispatch blocks ([#198740](https://github.com/pytorch/pytorch/pull/198740), [#198738](https://github.com/pytorch/pytorch/pull/198738), [#198739](https://github.com/pytorch/pytorch/pull/198739), [#187989](https://github.com/pytorch/pytorch/pull/187989), [#196204](https://github.com/pytorch/pytorch/pull/196204), [#196893](https://github.com/pytorch/pytorch/pull/196893))
- Fix silent wrong results for large MPS tensors in `torch.cat`, `arange`/`linspace`, `nll_loss`, padding and pooling, and fix `histogram` aborts and out-of-range counts ([#189965](https://github.com/pytorch/pytorch/pull/189965), [#198593](https://github.com/pytorch/pytorch/pull/198593), [#198776](https://github.com/pytorch/pytorch/pull/198776), [#198592](https://github.com/pytorch/pytorch/pull/198592), [#195147](https://github.com/pytorch/pytorch/pull/195147), [#196985](https://github.com/pytorch/pytorch/pull/196985), [#194460](https://github.com/pytorch/pytorch/pull/194460), [#195714](https://github.com/pytorch/pytorch/pull/195714), [#198416](https://github.com/pytorch/pytorch/pull/198416))
- Propagate NaN/Inf in MPS `addmm`/`addbmm`/`baddbmm` with `beta=0` and `add`/`sub` with `alpha=0` ([#193850](https://github.com/pytorch/pytorch/pull/193850), [#194474](https://github.com/pytorch/pytorch/pull/194474), [#196661](https://github.com/pytorch/pytorch/pull/196661))
- Fix MPS `pow` with integer exponents, and complex `std`/`var`, `pow` and logical ops ([#195585](https://github.com/pytorch/pytorch/pull/195585), [#195344](https://github.com/pytorch/pytorch/pull/195344), [#195592](https://github.com/pytorch/pytorch/pull/195592))
- Fix wrong MPS results in large `var`/`std` reductions, permuted `softplus`, `lerp` with a scalar weight, `rand` hitting its upper bound, bfloat16 `nextafter`, and small-input `expm1` ([#198495](https://github.com/pytorch/pytorch/pull/198495), [#197000](https://github.com/pytorch/pytorch/pull/197000), [#196662](https://github.com/pytorch/pytorch/pull/196662), [#197081](https://github.com/pytorch/pytorch/pull/197081), [#193897](https://github.com/pytorch/pytorch/pull/193897), [#198771](https://github.com/pytorch/pytorch/pull/198771))
- Fix MPS `scaled_dot_product_attention` output shape with broadcast batch/head dims, and `scatter_add_`/`index_add_` on offset `bool` views ([#189631](https://github.com/pytorch/pytorch/pull/189631), [#195081](https://github.com/pytorch/pytorch/pull/195081))
- Raise errors for MPS command buffer failures (such as out of memory) and MPS-to-CPU copies to `float64` instead of returning wrong outputs ([#198883](https://github.com/pytorch/pytorch/pull/198883), [#197722](https://github.com/pytorch/pytorch/pull/197722))
- Fix crashes and hangs when running MPS ops from multiple threads, and hangs in MPS event `elapsed_time()` ([#167541](https://github.com/pytorch/pytorch/pull/167541), [#197836](https://github.com/pytorch/pytorch/pull/197836), [#196395](https://github.com/pytorch/pytorch/pull/196395))
- Fix DLPack export of sliced MPS tensors, Metal debug-layer validation failures, and `active_bytes` in MPS memory stats ([#182924](https://github.com/pytorch/pytorch/pull/182924), [#199452](https://github.com/pytorch/pytorch/pull/199452), [#193838](https://github.com/pytorch/pytorch/pull/193838))
- Fix `torch.linalg.svd` returning non-orthonormal `U`/`Vh` with `full_matrices=True`, inaccurate results for very small or large entries, and zero `pinv`/`lstsq` for small singular values ([#200536](https://github.com/pytorch/pytorch/pull/200536), [#200776](https://github.com/pytorch/pytorch/pull/200776), [#200649](https://github.com/pytorch/pytorch/pull/200649))
- Fix complex division (and complex `linalg.solve`, `solve_triangular`, `det`) returning NaN or 0 for extreme magnitudes, and complex `pow` returning 0 for every zero base ([#200765](https://github.com/pytorch/pytorch/pull/200765), [#200564](https://github.com/pytorch/pytorch/pull/200564))
- Fix `var`/`std` returning 0 instead of NaN for NaN/Inf inputs, `float16` `addmm` overflowing to `inf` with `beta=0`, and `grouped_mm` silently accepting mismatched dtypes ([#200758](https://github.com/pytorch/pytorch/pull/200758), [#200657](https://github.com/pytorch/pytorch/pull/200657), [#200659](https://github.com/pytorch/pytorch/pull/200659))
- Fix `torch.compile` truncating `int64` constants to 32 bits ([#201060](https://github.com/pytorch/pytorch/pull/201060))

## ROCm

- Fix flash and memory-efficient attention failing on empty inputs; they now return empty outputs like CUDA ([#195812](https://github.com/pytorch/pytorch/pull/195812), [#195813](https://github.com/pytorch/pytorch/pull/195813), [#196723](https://github.com/pytorch/pytorch/pull/196723), [#198022](https://github.com/pytorch/pytorch/pull/198022))
- Fix CK flash attention dropout returning a wrong seed/offset to autograd when the GPU is busy ([#197563](https://github.com/pytorch/pytorch/pull/197563))
- Fix incorrect SDPA results on gfx11 with AOTriton 0.11 and later ([#194280](https://github.com/pytorch/pytorch/pull/194280))
- Fix launch failures on large inputs in `pdist`/`cdist` ([#188006](https://github.com/pytorch/pytorch/pull/188006)) and the BMM outer-product kernel ([#194131](https://github.com/pytorch/pytorch/pull/194131))
- Fix FP8 GEMMs failing with `HIPBLAS_STATUS_INTERNAL_ERROR` on ROCm 7.14 ([#197201](https://github.com/pytorch/pytorch/pull/197201))
- Fix crashes and hangs when a captured backward pass creates a hipBLASLt handle during CUDA graph capture ([#196399](https://github.com/pytorch/pytorch/pull/196399))
- Fix incorrect Inductor BF16 atomic accumulation, e.g. `index_put_` with repeated indices, on gfx11/gfx12 ([#198199](https://github.com/pytorch/pytorch/pull/198199))
- Fix nondeterministic `torch.topk` output order on slices longer than 256 elements ([#199425](https://github.com/pytorch/pytorch/pull/199425))
- Fix `F.batch_norm` on sharded DTensor inputs ([#197160](https://github.com/pytorch/pytorch/pull/197160))
- Fix hipify narrowing 64-bit and unsigned `std::max`/`std::min` arguments to `int` ([#199444](https://github.com/pytorch/pytorch/pull/199444))
- Fix JIT C++ extensions failing with `hipblas/hipblas.h: No such file or directory` with ROCm from TheRock pip wheels ([#196503](https://github.com/pytorch/pytorch/pull/196503))
- Stop RCCL 2.28+ from printing a deprecation warning on every all-to-all ([#197534](https://github.com/pytorch/pytorch/pull/197534), [#199124](https://github.com/pytorch/pytorch/pull/199124))
- Fix rare incorrect indices from `argmax`, `argmin`, `max` and `min` for large reductions on ROCm ([#193291](https://github.com/pytorch/pytorch/pull/193291))

## XPU

- Fix wrong `conv1d` backward results on XPU for some singleton-dimension layouts, caused by detecting the memory format before the 3D-to-4D view used by the oneDNN path ([#194328](https://github.com/pytorch/pytorch/pull/194328))
- Fix batch norm accuracy, `fft`/`ifft` on empty batches, `norm` global reductions, and half-precision `sampled_addmm` on XPU ([#193929](https://github.com/pytorch/pytorch/pull/193929))
- Fix precision loss in `addmm` and `baddbmm` for bf16/fp16 with non-trivial `alpha`/`beta` on XPU, which now accumulate in fp32 as CPU and CUDA do ([#174864](https://github.com/pytorch/pytorch/pull/174864))
- Fix `torch.xpu.mem_get_info` under-reporting free memory on Xe2 and later GPUs ([#195987](https://github.com/pytorch/pytorch/pull/195987))
- Fix XPU device indices not matching SYCL's order on platforms that enumerate an integrated GPU before the discrete ones ([#198336](https://github.com/pytorch/pytorch/pull/198336))
- Fix oneDNN SDPA with grouped-query attention and a mask broadcast in the head dimension ([#194973](https://github.com/pytorch/pytorch/pull/194973))
- Fix `torch.xpu.Event.record()` enqueueing two commands on first use, which could leave the event without profiling data and intermittently fail Inductor autotuning ([#194609](https://github.com/pytorch/pytorch/pull/194609))
- Fix "An event cannot be enqueued for signaling or waiting behind a command which is not enqueued in the backend" errors with oneCCL on Intel® Arc™ B-Series Graphics, by limiting reusable events to the IPC case ([#197396](https://github.com/pytorch/pytorch/pull/197396))
- Fix `_safe_softmax` incorrectly zeroing rows that contain NaN on XPU ([#195708](https://github.com/pytorch/pytorch/pull/195708))
- Fix incorrect `_weight_int4pack_mm` results on XPU ([#195708](https://github.com/pytorch/pytorch/pull/195708))
- Fix undefined behavior with NaN inputs in `topk`, a spurious `group_reduce` assert, and fused moving-average observer/fake-quantize dtype mismatches on XPU ([#194185](https://github.com/pytorch/pytorch/pull/194185))
- Fix an abort in the XPU flash attention backward with an empty batch, and return BSHD-contiguous input gradients from the XPU efficient attention backward ([#198200](https://github.com/pytorch/pytorch/pull/198200))
- Fix `weight_norm` running out of memory for 1-D inputs on XPU, and a host-to-device metadata race in nested `_transform_bias_rescale_qkv` ([#200289](https://github.com/pytorch/pytorch/pull/200289))
- Fix RNG stream reuse for large tensors on XPU ([#200289](https://github.com/pytorch/pytorch/pull/200289))
- Fix Inductor treating every XPU kernel that uses scratch memory as spilling registers ([#197061](https://github.com/pytorch/pytorch/pull/197061))

## Complex Frontend

- Fix `F.dropout` raising `NotImplementedError` for complex inputs ([#195373](https://github.com/pytorch/pytorch/pull/195373))

## JIT

- Fix `torch.jit.Attribute` and `nn.Module` class annotations being lost on Python 3.14; this requires `typing-extensions>=4.13` ([#195201](https://github.com/pytorch/pytorch/pull/195201), [#199074](https://github.com/pytorch/pytorch/pull/199074))
- Fix constant pooling merging `0.0` with `-0.0` ([#192605](https://github.com/pytorch/pytorch/pull/192605))
- Fix `torch.jit.export_opnames` missing ops inside `torch.jit.fork` subgraphs ([#197333](https://github.com/pytorch/pytorch/pull/197333))

## Mobile

- Fix a race in `CPUCachingAllocator` teardown ([#196759](https://github.com/pytorch/pytorch/pull/196759))

## Sparse Frontend

- Fix concurrent `torch.load` calls interfering in sparse tensor validation ([#194751](https://github.com/pytorch/pytorch/pull/194751))
- Fix wrong values from sparse compressed `add` with `out=` and ROCm COO `coalesce` ([#197564](https://github.com/pytorch/pytorch/pull/197564), [#199484](https://github.com/pytorch/pytorch/pull/199484))
- Fix semi-structured bitmask conversion on non-CUDA devices ([#193943](https://github.com/pytorch/pytorch/pull/193943))

## torch.func

- Fix `torch.vmap` falling back to the slow loop for several loss ops and `addr` under `python -O` ([#192859](https://github.com/pytorch/pytorch/pull/192859))

# Performance

## Python Frontend

- Reduce `TensorIterator` overhead and dtype refcount contention under free-threading ([#194422](https://github.com/pytorch/pytorch/pull/194422), [#194371](https://github.com/pytorch/pytorch/pull/194371))

## torch.nn

- Speed up `nn.Module.__call__` by about 15% ([#196236](https://github.com/pytorch/pytorch/pull/196236))
- Add a channels-last CUDA `GroupNorm` kernel ([#191945](https://github.com/pytorch/pytorch/pull/191945))
- Speed up RMSNorm backward up to 2x on sm12x and chunked `linear_cross_entropy` by 6-10% ([#192400](https://github.com/pytorch/pytorch/pull/192400), [#196134](https://github.com/pytorch/pytorch/pull/196134))

## Distributed (c10d)

- Speed up `all_gather_object` ([#196185](https://github.com/pytorch/pytorch/pull/196185))
- Share the parent `Store` connection across `split_group` child groups ([#196665](https://github.com/pytorch/pytorch/pull/196665))
- Use the NVLS multicast (multimem) barrier for CUDA symmetric memory when a multicast mapping is available ([#192861](https://github.com/pytorch/pytorch/pull/192861))

## DistributedDataParallel (DDP)

- Batch DDP's copy into `.grad` with `batched_grad_copy=True` ([#190524](https://github.com/pytorch/pytorch/pull/190524))

## Distributed FSDP2

- Reduce reduce-scatter gradient memory for size-1 shard groups and low-precision gradients ([#196348](https://github.com/pytorch/pytorch/pull/196348), [#198668](https://github.com/pytorch/pytorch/pull/198668))

## Distributed Pipelining

- Lower peak memory and improve overlap via lazy receive buffers and new `defer_reduce_grad_wait`/`unshard_lookahead` options ([#196463](https://github.com/pytorch/pytorch/pull/196463), [#196963](https://github.com/pytorch/pytorch/pull/196963), [#196725](https://github.com/pytorch/pytorch/pull/196725), [#196706](https://github.com/pytorch/pytorch/pull/196706))

## Linear Algebra Frontend

- Add a built-in CUDA batched LU kernel that matches MAGMA, and improve LU backend selection without pivoting ([#190329](https://github.com/pytorch/pytorch/pull/190329), [#193004](https://github.com/pytorch/pytorch/pull/193004))

## FX

- Reduce compile time in FX `from_node` provenance tracking ([#193051](https://github.com/pytorch/pytorch/pull/193051))
- Speed up the FX accelerator splitter on large graphs ([#198519](https://github.com/pytorch/pytorch/pull/198519), [#198654](https://github.com/pytorch/pytorch/pull/198654))

## Dynamo

- Reduce per-call overhead of compiled code and helpers like `assert_size_stride` ([#190623](https://github.com/pytorch/pytorch/pull/190623), [#195951](https://github.com/pytorch/pytorch/pull/195951), [#198019](https://github.com/pytorch/pytorch/pull/198019), [#196771](https://github.com/pytorch/pytorch/pull/196771), [#197451](https://github.com/pytorch/pytorch/pull/197451), [#197733](https://github.com/pytorch/pytorch/pull/197733))
- Reduce compile time: defer gen-2 GC while compiling (4.2s on one model; see `gc_gen2_threshold_during_compile`), skip empty graphs (custom backends are no longer called for such graphs), and speed up large functions ([#193289](https://github.com/pytorch/pytorch/pull/193289), [#193157](https://github.com/pytorch/pytorch/pull/193157), [#195622](https://github.com/pytorch/pytorch/pull/195622))

## Inductor

- Reduce compile time by caching in fusion search and codegen, hashing sources in the background, and compiling combo-kernel benchmarks in parallel ([#186319](https://github.com/pytorch/pytorch/pull/186319), [#192817](https://github.com/pytorch/pytorch/pull/192817), [#192820](https://github.com/pytorch/pytorch/pull/192820), [#194010](https://github.com/pytorch/pytorch/pull/194010), [#194011](https://github.com/pytorch/pytorch/pull/194011), [#198747](https://github.com/pytorch/pytorch/pull/198747), [#198881](https://github.com/pytorch/pytorch/pull/198881), [#198320](https://github.com/pytorch/pytorch/pull/198320))
- Allow mix-order reduction fusion for more shapes, speeding up RMSNorm backward ([#186370](https://github.com/pytorch/pytorch/pull/186370), [#188660](https://github.com/pytorch/pytorch/pull/188660))
- Reduce `cpp_wrapper` kernel call overhead by 40-50% ([#192287](https://github.com/pytorch/pytorch/pull/192287))
- Improve CPU FlexAttention BF16 performance by 6-29% ([#191780](https://github.com/pytorch/pytorch/pull/191780))
- Use larger reduction tiles on GB300, roughly doubling HBM bandwidth use ([#193774](https://github.com/pytorch/pytorch/pull/193774))
- Add gfx950 FlexAttention backward configs (1.8-2.3x faster) ([#194151](https://github.com/pytorch/pytorch/pull/194151))
- Improve NVGEMM NVFP4 decode performance on Blackwell and widen its autotuning candidates ([#194651](https://github.com/pytorch/pytorch/pull/194651), [#194652](https://github.com/pytorch/pytorch/pull/194652), [#197485](https://github.com/pytorch/pytorch/pull/197485), [#195539](https://github.com/pytorch/pytorch/pull/195539), [#198293](https://github.com/pytorch/pytorch/pull/198293))
- Compute only one triangle for large BF16 `X @ X.T` on SM100 ([#194177](https://github.com/pytorch/pytorch/pull/194177), [#194178](https://github.com/pytorch/pytorch/pull/194178))
- Speed up collective bucketing, including up to 9x faster uneven reduce-scatter padding ([#196647](https://github.com/pytorch/pytorch/pull/196647), [#196621](https://github.com/pytorch/pytorch/pull/196621), [#195616](https://github.com/pytorch/pytorch/pull/195616))
- Simplify `slice_scatter` chains to reduce recomputation and peak memory ([#192136](https://github.com/pytorch/pytorch/pull/192136), [#195608](https://github.com/pytorch/pytorch/pull/195608), [#195631](https://github.com/pytorch/pytorch/pull/195631))
- Fix CPU OpenMP parallelization moving onto inner reduction loops under freezing, and recover an XPU inner-reduction regression ([#190928](https://github.com/pytorch/pytorch/pull/190928), [#190986](https://github.com/pytorch/pytorch/pull/190986))
- Fuse `torch.cat`/`torch.stack` copies into foreach kernels for dynamic shapes ([#198294](https://github.com/pytorch/pytorch/pull/198294))
- Enable nested reduction fusion by default (`TORCHINDUCTOR_NESTED_REDUCTION=0` disables it), fusing patterns such as RMSNorm followed by MXFP8/NVFP4 quantization into one kernel ([#190594](https://github.com/pytorch/pytorch/pull/190594), [#190595](https://github.com/pytorch/pytorch/pull/190595), [#191974](https://github.com/pytorch/pytorch/pull/191974), [#193598](https://github.com/pytorch/pytorch/pull/193598), [#196332](https://github.com/pytorch/pytorch/pull/196332), [#196333](https://github.com/pytorch/pytorch/pull/196333), [#196334](https://github.com/pytorch/pytorch/pull/196334))

## Ahead-Of-Time Inductor (AOTI)

- Parallelize pinned host staging copies when loading CUDA constants ([#195257](https://github.com/pytorch/pytorch/pull/195257))

## AOTDispatcher

- Speed up the min-cut partitioner, reducing cold compile time by about 5% ([#197724](https://github.com/pytorch/pytorch/pull/197724))

## Composability

- Speed up FakeTensor view cache hits ([#192821](https://github.com/pytorch/pytorch/pull/192821))
- Reduce compile time in `ShapeEnv` ([#193219](https://github.com/pytorch/pytorch/pull/193219), [#193161](https://github.com/pytorch/pytorch/pull/193161), [#195623](https://github.com/pytorch/pytorch/pull/195623))

## Quantization

- Speed up AArch64 small-batch QNNPACK linear 2-4x ([#193595](https://github.com/pytorch/pytorch/pull/193595))

## Foreach

- Reduce `_foreach_norm`/`max` CUDA scratch memory ([#190549](https://github.com/pytorch/pytorch/pull/190549))

## CUDA

- Avoid CPU-GPU synchronization when assigning scalars through indexing on CUDA, e.g. `x[mask] = 1.0` ([#189303](https://github.com/pytorch/pytorch/pull/189303), [#188330](https://github.com/pytorch/pytorch/pull/188330), [#198811](https://github.com/pytorch/pytorch/pull/198811))
- Speed up CUDA `upsample_linear1d` by 5-25x for small outputs ([#180885](https://github.com/pytorch/pytorch/pull/180885)), pooling backward ([#191086](https://github.com/pytorch/pytorch/pull/191086), [#195119](https://github.com/pytorch/pytorch/pull/195119), [#196156](https://github.com/pytorch/pytorch/pull/196156)), dtype-conversion copies ([#195542](https://github.com/pytorch/pytorch/pull/195542), [#198723](https://github.com/pytorch/pytorch/pull/198723)), 2D transpose copies ([#194310](https://github.com/pytorch/pytorch/pull/194310)), and `zero_` ([#195303](https://github.com/pytorch/pytorch/pull/195303), [#198565](https://github.com/pytorch/pytorch/pull/198565))
- `torch.topk` on CUDA 13 Linux wheels uses ahead-of-time compiled radix-select kernels on Hopper and Blackwell (median 2.16x on H100) ([#190899](https://github.com/pytorch/pytorch/pull/190899))
- Fix a 10-30x slowdown of `gather`, `index_select`, `x[idx]` and `scatter_add` on rows of 16 or 32 bytes ([#200995](https://github.com/pytorch/pytorch/pull/200995))

## cuDNN

- Prefer the cuDNN backend for SDPA on sm86/sm89 for higher performance ([#192799](https://github.com/pytorch/pytorch/pull/192799))

## CPU (x86)

- Fix the CPU kernel dispatch cache never being populated, which made every dispatch to a CPU kernel repeat the CPU capability selection ([#195328](https://github.com/pytorch/pytorch/pull/195328))

## CPU (AArch64)

- Optimize `libtorch` code layout with LLVM BOLT, using profiles shipped in the repository. The new `USE_LLVM_BOLT` build option is on by default for Linux aarch64 CUDA builds when `llvm-bolt` 21 or newer is found and `USE_PRIORITIZED_TEXT_FOR_LD` is enabled, giving up to 30% faster workloads in some cases and up to 3% slower in others; set `USE_LLVM_BOLT=0` to opt out in source builds ([#186245](https://github.com/pytorch/pytorch/pull/186245))
- Use the native GEMV path for single-column (`n == 1`) BF16 GEMMs on Arm Neoverse CPUs built with oneDNN ACL, for about 5x faster single-thread GPT-2 BF16 decode on Graviton 4 and 5 (1.4x-2.7x with 8-64 threads on Graviton 5) ([#198411](https://github.com/pytorch/pytorch/pull/198411))
- Dispatch non-contiguous FP16 matmuls to oneDNN ACL GEMM kernels instead of the reference implementation on AArch64 ([#198498](https://github.com/pytorch/pytorch/pull/198498))

## MPS

- Move more MPS ops (`softmax`, `nll_loss`, padding, `where`, ...) to native Metal kernels, cutting launch overhead and driver memory growth with variable shapes ([#196071](https://github.com/pytorch/pytorch/pull/196071), [#195441](https://github.com/pytorch/pytorch/pull/195441), [#195153](https://github.com/pytorch/pytorch/pull/195153), [#195368](https://github.com/pytorch/pytorch/pull/195368), [#193826](https://github.com/pytorch/pytorch/pull/193826), [#198719](https://github.com/pytorch/pytorch/pull/198719), [#198688](https://github.com/pytorch/pytorch/pull/198688), [#198497](https://github.com/pytorch/pytorch/pull/198497), [#196924](https://github.com/pytorch/pytorch/pull/196924), [#189548](https://github.com/pytorch/pytorch/pull/189548), [#199687](https://github.com/pytorch/pytorch/pull/199687), [#198878](https://github.com/pytorch/pytorch/pull/198878))
- Speed up MPS reductions, linear algebra, GEMV, convolutions, `histc`, masked fill, dropout and sort ([#198494](https://github.com/pytorch/pytorch/pull/198494), [#198611](https://github.com/pytorch/pytorch/pull/198611), [#198635](https://github.com/pytorch/pytorch/pull/198635), [#197397](https://github.com/pytorch/pytorch/pull/197397), [#198646](https://github.com/pytorch/pytorch/pull/198646), [#199278](https://github.com/pytorch/pytorch/pull/199278), [#198721](https://github.com/pytorch/pytorch/pull/198721), [#197862](https://github.com/pytorch/pytorch/pull/197862), [#196241](https://github.com/pytorch/pytorch/pull/196241), [#196900](https://github.com/pytorch/pytorch/pull/196900), [#195944](https://github.com/pytorch/pytorch/pull/195944), [#198732](https://github.com/pytorch/pytorch/pull/198732), [#195950](https://github.com/pytorch/pytorch/pull/195950), [#193623](https://github.com/pytorch/pytorch/pull/193623), [#193167](https://github.com/pytorch/pytorch/pull/193167), [#192164](https://github.com/pytorch/pytorch/pull/192164), [#196016](https://github.com/pytorch/pytorch/pull/196016), [#195020](https://github.com/pytorch/pytorch/pull/195020), [#195011](https://github.com/pytorch/pytorch/pull/195011), [#198960](https://github.com/pytorch/pytorch/pull/198960), [#196922](https://github.com/pytorch/pytorch/pull/196922))
- Speed up `softmax` over a non-innermost dim and `relu`, `clamp_min`, `leaky_relu` and other scalar-argument unary ops on row-strided views ([#199758](https://github.com/pytorch/pytorch/pull/199758), [#199933](https://github.com/pytorch/pytorch/pull/199933))

## XPU

- Speed up SDPA training on XPU by aligning the oneDNN graph SDPA pattern with oneDNN v3.13 and integrating its GQA and dropout support ([#195419](https://github.com/pytorch/pytorch/pull/195419))
- Fuse the `GroupNorm` forward into a single kernel and speed up contiguous `cat` with vectorized stores on XPU ([#194842](https://github.com/pytorch/pytorch/pull/194842))
- Avoid register spilling in mixed fp32/bf16/fp16 elementwise kernels on XPU by adding vectorized type-casting loads ([#194185](https://github.com/pytorch/pytorch/pull/194185))
- Speed up `col2im` on XPU by replacing its hard-coded work-group size ([#198720](https://github.com/pytorch/pytorch/pull/198720))
- Reduce oneMKL LAPACK overhead on XPU by trimming scratchpad initialization, host synchronizations and re-allocation ([#193110](https://github.com/pytorch/pytorch/pull/193110))

## JIT

- Speed up `torch.jit.load` and graph pre-optimization ([#194035](https://github.com/pytorch/pytorch/pull/194035), [#193107](https://github.com/pytorch/pytorch/pull/193107), [#193250](https://github.com/pytorch/pytorch/pull/193250), [#194009](https://github.com/pytorch/pytorch/pull/194009))

# Documentation

## Python Frontend

- Document undefined behavior of bool tensors holding bytes other than 0/1, and clarify `Tensor.index_add_`'s `index` argument ([#199012](https://github.com/pytorch/pytorch/pull/199012), [#193403](https://github.com/pytorch/pytorch/pull/193403))

## torch.nn

- Fix the `linear_cross_entropy` docstring snippet and `nn.RNN` example, and document bias with probability targets ([#198941](https://github.com/pytorch/pytorch/pull/198941), [#188433](https://github.com/pytorch/pytorch/pull/188433), [#173888](https://github.com/pytorch/pytorch/pull/173888))

## Autograd

- Document that custom `Function`/op backward gradients may have arbitrary strides and that `unpack_hook` order is unspecified ([#195210](https://github.com/pytorch/pytorch/pull/195210), [#198016](https://github.com/pytorch/pytorch/pull/198016))
- Point `torch.utils.checkpoint` docs to `torch_remat` and drop the stale `use_reentrant` "version 2.9" error notice ([#193998](https://github.com/pytorch/pytorch/pull/193998), [#193720](https://github.com/pytorch/pytorch/pull/193720))
- Fix math rendering on the autograd mechanics page ([#192562](https://github.com/pytorch/pytorch/pull/192562))

## Distributed

- Document the remaining NVSHMEM bindings ([#193449](https://github.com/pytorch/pytorch/pull/193449))

## Distributed (c10d)

- Add a tutorial for the distributed debug server ([#178800](https://github.com/pytorch/pytorch/pull/178800))
- Document `Backend.Options` and fix `irecv` and NCCL env var docs ([#196123](https://github.com/pytorch/pytorch/pull/196123), [#189623](https://github.com/pytorch/pytorch/pull/189623), [#194701](https://github.com/pytorch/pytorch/pull/194701))

## Distributed FSDP2

- Document parameter-mutation limits of `fully_shard` ([#198826](https://github.com/pytorch/pytorch/pull/198826))

## TorchElastic

- Fix the `EtcdServer` example and `Worker` docstring ([#198238](https://github.com/pytorch/pytorch/pull/198238), [#199255](https://github.com/pytorch/pytorch/pull/199255))

## Profiler

- Fix the `toggle_collection_dynamic` example ([#190369](https://github.com/pytorch/pytorch/pull/190369))

## Dynamo

- Remove references to the obsolete `dynamic_shapes` config ([#198707](https://github.com/pytorch/pytorch/pull/198707))
- Fix the PGO config example in the dynamic shapes docs ([#191027](https://github.com/pytorch/pytorch/pull/191027))
- Document more `torch._logging.set_logs` options ([#188138](https://github.com/pytorch/pytorch/pull/188138))

## Inductor

- Document the FlexAttention `ROWS_GUARANTEED_SAFE` requirement ([#194154](https://github.com/pytorch/pytorch/pull/194154))

## Foreach

- Fix in-place foreach type stubs to return the input list ([#193466](https://github.com/pytorch/pytorch/pull/193466))

## Release Engineering

- Fix docs search ranking module stub pages above the API symbols they document and listing duplicate results ([#195042](https://github.com/pytorch/pytorch/pull/195042))
- Link the build environment variable reference from `README.md` and `CONTRIBUTING.md`, and fix outdated build instructions there ([#193617](https://github.com/pytorch/pytorch/pull/193617))
- Document the issue and pull request workflow in `CONTRIBUTING.md` and add a maintainer guide to the community docs ([#198527](https://github.com/pytorch/pytorch/pull/198527))

## MPS

- Note MPS lacks `float64` support ([#193545](https://github.com/pytorch/pytorch/pull/193545))

## ROCm

- Document gfx1151 SDPA layouts, hipFile GPUDirect Storage, and MI300 matmul precision issues ([#190771](https://github.com/pytorch/pytorch/pull/190771), [#195478](https://github.com/pytorch/pytorch/pull/195478), [#190736](https://github.com/pytorch/pytorch/pull/190736))

# Security

## Python Frontend

- Fix `torch.load(weights_only=True)` exposing uninitialized pybind11-backed objects (such as DTensor placements) when a checkpoint uses the `NEWOBJ` opcode without a matching `BUILD`; such checkpoints are now rejected as corrupt or malicious ([#194647](https://github.com/pytorch/pytorch/pull/194647))
- Fix a stack buffer overflow in `torch_shm_manager` (libshm) when the Unix socket path is too long (e.g. a long `TMPDIR`); it now raises an error ([#195183](https://github.com/pytorch/pytorch/pull/195183))
- After `import torch.distributed`, `torch.load(weights_only=True)` and `get_unsafe_globals_in_checkpoint` no longer treat builtin exceptions as safe globals (a process-wide allowlist added in 2.14), and loading no longer calls overridden `append`/`extend` on allowlisted `list` subclasses. Checkpoints with pickled exceptions now need `torch.serialization.add_safe_globals`; object collectives are unchanged ([#200956](https://github.com/pytorch/pytorch/pull/200956))

# Developers

## Distributed (c10d)

- Make `FakeProcessGroup` support `all_to_all_single` with any sizes and add a `simulate_uniform_ranks` option ([#193985](https://github.com/pytorch/pytorch/pull/193985), [#194545](https://github.com/pytorch/pytorch/pull/194545))
- Fix a clang build error and add `amd_smi` as a ROCm 7.14+ build dependency ([#194104](https://github.com/pytorch/pytorch/pull/194104), [#192520](https://github.com/pytorch/pytorch/pull/192520))
- Add the private `torch.distributed._functional_collectives.wait_tensors`, which waits on all outputs of a multi-output functional collective at once; `torch.compile` uses it for coalesced collectives and `batch_isend_irecv` ([#193892](https://github.com/pytorch/pytorch/pull/193892))

## Profiler

- Kineto source now lives in `third_party/kineto` instead of a git submodule ([#198648](https://github.com/pytorch/pytorch/pull/198648))
- Remove the ignored `profiler_metrics` and `profiler_measure_per_kernel` `_ExperimentalConfig` arguments (now a `TypeError`), and deprecate the no-op `adjust_profiler_step` option ([#198262](https://github.com/pytorch/pytorch/pull/198262), [#193042](https://github.com/pytorch/pytorch/pull/193042))

## FX

- Fix type annotations on `Tracer(autowrap_modules=...)` and `CodeGen.process_inputs` ([#195467](https://github.com/pytorch/pytorch/pull/195467), [#188287](https://github.com/pytorch/pytorch/pull/188287))

## Inductor

- Add `DeviceInterface` and `DeviceOpOverrides` extension points for out-of-tree accelerator backends ([#190326](https://github.com/pytorch/pytorch/pull/190326), [#190614](https://github.com/pytorch/pytorch/pull/190614), [#192896](https://github.com/pytorch/pytorch/pull/192896), [#193908](https://github.com/pytorch/pytorch/pull/193908), [#190615](https://github.com/pytorch/pytorch/pull/190615))
- Add declarative `implies` support to Inductor/Dynamo `Config` ([#196663](https://github.com/pytorch/pytorch/pull/196663))

## Ahead-Of-Time Inductor (AOTI)

- Add `DeviceOpOverrides.aten_device_type()` so backends provide their ATen device type to AOTInductor C++ codegen ([#193904](https://github.com/pytorch/pytorch/pull/193904))

## C++ Frontend

- `c10::List` iterators satisfy `std::random_access_iterator`, and `List<T>::emplace` now constructs a `T` ([#196002](https://github.com/pytorch/pytorch/pull/196002))

## Developer Experience

- Add `spin test` to run `pytest` or `test/run_test.py` like CI ([#198649](https://github.com/pytorch/pytorch/pull/198649))

## Build Frontend

- Add an opt-in `USE_CMAKE_INSTRUMENTATION=1` build option to collect build metrics (CMake >= 4.3) ([#189455](https://github.com/pytorch/pytorch/pull/189455))
- Turn off `USE_FLASH_ATTENTION` automatically when no target CUDA architecture is sm80 or newer ([#194502](https://github.com/pytorch/pytorch/pull/194502))
- Fix the misspelled `CUDA_LIMIT_GPU_ARCHITECTURE` in CUDA architecture autodetection ([#195695](https://github.com/pytorch/pytorch/pull/195695))
- Honor `USE_MIMALLOC=OFF` on Windows and AArch64 ([#199064](https://github.com/pytorch/pytorch/pull/199064))
- Fix the FlashAttention CUDA build on Windows with MSVC in C++20 mode ([#197382](https://github.com/pytorch/pytorch/pull/197382))

## Release Engineering

- Move the CD wheel build scripts under `.ci/wheel/` (`.ci/manywheel/` to `.ci/wheel/linux/`, `.ci/macwheel/` to `.ci/wheel/mac/`, and the Windows pipeline to `.ci/wheel/windows/`) and share one `numpy` build pin ([#189275](https://github.com/pytorch/pytorch/pull/189275))
- Add a native-AOT stage to CUDA builds that exports CuTeDSL and Triton kernels ahead of time and embeds them into `libtorch_cuda`. The stage skips itself when it does not apply (for example CUDA older than 13 or no supported GPU architecture), but once it decides to export, a missing `nvidia-cutlass-dsl` (or Triton, installable with `scripts/install_triton_wheel.sh`) is a hard error; set `TORCH_NATIVE_AOT=0` to skip the stage ([#194243](https://github.com/pytorch/pytorch/pull/194243), [#196747](https://github.com/pytorch/pytorch/pull/196747), [#196507](https://github.com/pytorch/pytorch/pull/196507))
- Fix the CMake C and C++ compiler flag checks sharing one cache variable, so a result for one language could be reused for the other; the generated `HAS_<FLAG>` variables are now prefixed `HAS_C` and `HAS_CXX` ([#197614](https://github.com/pytorch/pytorch/pull/197614))
- Add a persistent `[no-ci]` PR title prefix that skips build, test and lint jobs, and make `@pytorchbot merge -i` ignore current failures across every PR in a ghstack stack ([#196534](https://github.com/pytorch/pytorch/pull/196534), [#197143](https://github.com/pytorch/pytorch/pull/197143))

## CUDA

- Update the bundled CUTLASS to v4.8.0 and CUTLASS-Operators to v0.3.0 ([#198179](https://github.com/pytorch/pytorch/pull/198179))

## CPU (AArch64)

- Add the `AT_VEC_CUSTOM_MATH` compile definition, which hides the built-in vectorized math functions on AVX2, AVX512, NEON and SVE256 builds so that a vectorized math library other than SLEEF can be plugged in ([#197419](https://github.com/pytorch/pytorch/pull/197419))

## MPS

- Fix building with clang 16 and Apple clang 15 ([#199115](https://github.com/pytorch/pytorch/pull/199115))
- Fix building with a Metal 4 toolchain against older macOS SDKs, and deprecation warnings with the macOS 27 SDK ([#196104](https://github.com/pytorch/pytorch/pull/196104), [#197200](https://github.com/pytorch/pytorch/pull/197200))
- `at::mps::MPSProfiler` `begin*`/`end*` methods take the `MPSStream*`; stream-less `begin*` overloads are deprecated ([#192525](https://github.com/pytorch/pytorch/pull/192525), [#193611](https://github.com/pytorch/pytorch/pull/193611))
- Fix macOS builds failing on SDKs that lack the Metal 4 cooperative-tensor APIs ([#195302](https://github.com/pytorch/pytorch/pull/195302))
- Fix stale embedded Metal shaders in incremental macOS builds ([#196202](https://github.com/pytorch/pytorch/pull/196202))
- Fix MPS shader includes in editable installs ([#195295](https://github.com/pytorch/pytorch/pull/195295))

## ROCm

- `torch.utils.cpp_extension.ROCM_VERSION` now uses the ROCm SDK version instead of the HIP runtime version, and `collect_env` reports both ([#194985](https://github.com/pytorch/pytorch/pull/194985), [#193602](https://github.com/pytorch/pytorch/pull/193602))

## XPU

- Build XPU with pure SYCL compilation and support Clang as the host compiler; expose `USE_SYCLTLA` and enable oneMKL sparse in the build system ([#194185](https://github.com/pytorch/pytorch/pull/194185), [#198720](https://github.com/pytorch/pytorch/pull/198720), [#196387](https://github.com/pytorch/pytorch/pull/196387), [#198200](https://github.com/pytorch/pytorch/pull/198200))
- Upgrade oneDNN to v3.13 ([#196712](https://github.com/pytorch/pytorch/pull/196712))

## Caffe2

- Fix source builds with CUDA 13.3 ([#194659](https://github.com/pytorch/pytorch/pull/194659))
