# PyTorch 2.13.0 Release Notes

- [Highlights](#highlights)
- [Tracked Regressions](#tracked-regressions)
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
  <tr><td><strong>FlexAttention</strong> lands on Apple Silicon (MPS), with up to ~12x speedup over SDPA on sparse patterns, and gains a deterministic backward path on CUDA for reproducible gradient computation.</td></tr>
  <tr><td><strong>CuTeDSL "Native DSL" backend</strong> gives Inductor a second high-performance code path (alongside Triton) for key GPU operations, with faster compilation. [Prototype]</td></tr>
  <tr><td><strong><code>nn.LinearCrossEntropyLoss</code></strong> combines the final prediction and loss computation to cut peak GPU memory by up to 4x for large-vocabulary language model training.</td></tr>
  <tr><td><strong>torchcomms</strong>, a new communications backend for PyTorch Distributed, improves fault tolerance, scalability, and debuggability for large-cluster training.</td></tr>
  <tr><td><strong>FSDP2</strong> now overlaps reduce-scatter and all-gather communications via a dedicated process group (opt-in), increasing distributed training throughput.</td></tr>
  <tr><td><strong>Python 3.15 wheel support</strong> for PyTorch on Linux via the pytorch repository index, including builds compatible with free-threaded 3.15t.</td></tr>
  <tr><td><strong>Broader platform support</strong>: ROCm gains AOTriton 0.12b with native HIP CMake, Arm adds Armv9-A <code>torch.compile</code> targeting, and Intel XPU exposes new device telemetry APIs.</td></tr>
</table>

For more details about these highlighted features, you can look at the release blogpost. Below are the full release notes for this release.

# Tracked Regressions

### Convolution failures on CUDA 13 builds when a mismatched system cuDNN is on the loader path

On CUDA 13 builds, a convolution can fail on the first call with `CUDNN_STATUS_SUBLIBRARY_VERSION_MISMATCH` ([#188892](https://github.com/pytorch/pytorch/issues/188892)). This only affects systems that also have a *different* system-wide cuDNN 9.x (e.g. an apt-installed cuDNN >= 9.23) visible to the dynamic loader. Clean pip-only installs and standard CI environments are unaffected and do not reproduce it.

Cause: CUDA 13 builds bundle `nvidia-cudnn-cu13==9.20.0.48`, whose `libcudnn_graph.so.9` `dlopen`s the engine sub-library `libcudnn_engines_tensor_ir.so` by bare soname, but that library is not shipped in the 9.20 wheel (it was introduced in cuDNN >= 9.23). If no other cuDNN installation is present, the failed `dlopen()` is harmless and cuDNN falls back to another implementation. However, if a different cuDNN 9.x installation is visible on the loader search path, the loader resolves `libcudnn_engines_tensor_ir.so` from that installation instead, mixing libraries from different cuDNN versions and resulting in `CUDNN_STATUS_SUBLIBRARY_VERSION_MISMATCH`.

Workaround: Ensure that a different system cuDNN installation is not visible on the loader search path (e.g. remove it or clear it from `LD_LIBRARY_PATH`/`ldconfig`), or use a self-consistent cuDNN installation. A fix (preloading the bundled cuDNN libraries so they take precedence over system copies) is planned for the 2.13.1 patch release.

# Backwards Incompatible Changes

- Stop building CPython 3.13t (free-threaded) binaries ([#182951](https://github.com/pytorch/pytorch/pull/182951))

  Upstream `pypa/manylinux` removed CPython 3.13t (free-threaded) on 2026-05-07, because 3.13t
  was experimental and has been superseded by the now-non-experimental CPython 3.14t. As a result,
  PyTorch 2.13 no longer ships `cp313t` wheels (Linux, Triton, and related artifacts). Users on the
  free-threaded interpreter should move to Python 3.14t.

  PyTorch 2.12:
  ```bash
  # cp313t (free-threaded 3.13) wheels were available
  python3.13t -m pip install torch
  ```

  PyTorch 2.13:
  ```bash
  # Use free-threaded Python 3.14t instead
  python3.14t -m pip install torch
  ```

- Bare `PyObject` is no longer allowed in operator schemas ([#184209](https://github.com/pytorch/pytorch/pull/184209))

  Bare `PyObject` was accidentally accepted in operator schema strings in
  PyTorch 2.12. This was undocumented and is now rejected, since `torch.compile`
  does not support arbitrary `PyObject` inputs to custom ops. If
  you parse or register a schema with a bare `PyObject` argument or return type,
  you will now get a schema parse error.

  PyTorch 2.12:
  ```python
  >>> from torch._C import parse_schema
  >>> parse_schema("foo(PyObject x) -> ()")  # accepted
  ```

  PyTorch 2.13:
  ```python
  >>> from torch._C import parse_schema
  >>> parse_schema("foo(PyObject x) -> ()")  # raises a schema parse error
  ```

- Remove Bazel build support ([#180883](https://github.com/pytorch/pytorch/pull/180883))

  The Bazel build was never broadly adopted and still depended on the antiquated Bazel 6,
  while the wider ecosystem has since moved to Bazel 9. All Bazel build files and CI jobs have
  been removed. Users building PyTorch with Bazel should migrate to the supported CMake/`pip install`
  build flow.

  PyTorch 2.12:
  ```bash
  # Build PyTorch with Bazel
  bazel build //:torch
  ```

  PyTorch 2.13:
  ```bash
  # Bazel build files have been removed; build from source with pip instead
  pip install --no-build-isolation -e .
  ```

- Enforce C++20 minimum in header guards ([#178150](https://github.com/pytorch/pytorch/pull/178150)). In PyTorch 2.13, C++20 is now required to import PyTorch headers.

- `StorageImpl`'s built-in copy-on-write (COW) materialization is replaced by a pluggable materializer hook ([#179063](https://github.com/pytorch/pytorch/pull/179063))

  `StorageImpl` no longer knows about COW directly. Its internal COW entry points
  `StorageImpl::is_cow()`, `StorageImpl::maybe_materialize_cow()`, and the friend
  `cow::materialize_cow_storage()` have been removed in favor of a single pluggable
  `MaterializeFn` hook (`void(*)(StorageImpl*)`) that a backend registers to run once,
  on the first mutable data-pointer access. COW is now just one consumer of this hook
  (`c10::impl::cow::materialize_cow`), and all COW behavior (lazy clone, refcounted
  shared data, copy-on-write) is unchanged. This also gives accelerator backends and
  eager-mode graph compilers a zero-fast-path-cost place to commit deferred allocations
  or materialize symbolic buffers on first mutation.

  This is a C++-only change. It affects out-of-tree backends/extensions that called the
  removed `StorageImpl` COW symbols directly; they will fail to compile against 2.13
  with errors such as `no member named 'is_cow' in 'c10::StorageImpl'`. Migrate to the
  new hook API (`set_materializer()` / `has_materializer()` / `clear_materializer()`).

  PyTorch 2.12:
  ```cpp
  // Detect a COW storage and force it to materialize.
  if (storage.is_cow()) {
    storage.maybe_materialize_cow();
  }
  ```

  PyTorch 2.13:
  ```cpp
  // Register a one-shot materializer; it runs on the next mutable-data access
  // and then clears itself. COW registers c10::impl::cow::materialize_cow this way.
  storage.set_materializer(&my_backend_materialize);  // void(StorageImpl*)

  // `has_materializer()` replaces `is_cow()` for "is a deferred materialization pending?"
  if (storage.has_materializer()) { /* ... */ }
  ```

- Convert `shared_ptr<Node>` to `intrusive_ptr<Node>` ([#181139](https://github.com/pytorch/pytorch/pull/181139)). This changes the signature of `Tensor::grad_fn`. Accesses to `Tensor.grad_fn()` should change from `std::shared_ptr<Node>` to `c10::intrusive_ptr<Node>`. Similarly, construction of a C++ autograd function should change:

  PyTorch 2.12:
  ```cpp
  std::shared_ptr<CustomCppNode> node(new CustomCppNode(), torch::autograd::deleteNode);
  ```

  PyTorch 2.13:
  ```cpp
  auto node = c10::make_intrusive<CustomCppNode>();
  ```

- The minimum supported NCCL version when building from source is now 2.23 ([#186292](https://github.com/pytorch/pytorch/pull/186292))

  PyTorch now requires NCCL >= 2.23 at compile time, and the preprocessor/runtime gates that guarded NCCL features introduced in 2.23 or earlier have been removed. Users who build PyTorch from source against a system NCCL older than 2.23 will hit compile errors against the dropped gates. Upgrade the NCCL installation to >= 2.23 to build. The prebuilt PyTorch wheels already bundle a compatible NCCL, so pip/conda users are unaffected.

- Remove named tensors ([#173895](https://github.com/pytorch/pytorch/pull/173895))

  The named tensor feature (a long-deprecated prototype) has been fully removed to reduce overhead and code bloat. All associated Python and C++ APIs are gone, including `Tensor.names`, `Tensor.rename()`, `Tensor.refine_names()`, `Tensor.align_to()`, `Tensor.align_as()`, `torch.align_tensors()`, the `names=` keyword on factory functions (e.g. `torch.zeros`, `torch.empty`, `torch.ones`), and the C++ `Dimname` / `DimnameList` APIs. Code that previously relied on named dimensions must track dimension order positionally and avoid usage of any of these now-removed APIs or op overloads.

- The `onednn::qconv2d_pointwise.binary` and `.binary_tensor` operators no longer alias their input but rather return fresh tensors. Previously these ops mutated the `qaccum` input buffer and returned it directly, violating the PyTorch invariant that custom operator outputs must not alias inputs. This silently bypassed aliasing checks via the old `-> Tensor(a!)` schema and would become a hard error in a future PyTorch version (as mentioned in [#182063](https://github.com/pytorch/pytorch/pull/182063)), so the schema and implementation were corrected to return a fresh output. Most users are unaffected, only code that calls these ops directly and relies on the in-place mutation of qaccum must now read the returned tensor instead. ([#177171](https://github.com/pytorch/pytorch/pull/177171))

# Deprecations

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

- Creating tensors with the quantized dtypes `quint8`, `qint8`, and `qint32` is now deprecated and emits a warning. This covers both Python and C++ call sites; see [#184982](https://github.com/pytorch/pytorch/issues/184982) for migration guidance ([#184984](https://github.com/pytorch/pytorch/pull/184984))

  PyTorch 2.12:
  ```python
  >>> x = torch.quantize_per_tensor(torch.randn(3), 0.1, 0, torch.quint8)
  ```

  PyTorch 2.13:
  ```python
  >>> x = torch.quantize_per_tensor(torch.randn(3), 0.1, 0, torch.quint8)
  UserWarning: Creating tensors with quantized dtypes (quint8, qint8, qint32) is deprecated
  ```

- Rename distributed collective ops to the `_single` naming scheme and deprecate the old names ([#186123](https://github.com/pytorch/pytorch/pull/186123), [#186124](https://github.com/pytorch/pytorch/pull/186124), [#186125](https://github.com/pytorch/pytorch/pull/186125), [#186134](https://github.com/pytorch/pytorch/pull/186134), [#186135](https://github.com/pytorch/pytorch/pull/186135), [#186144](https://github.com/pytorch/pytorch/pull/186144))

  To align the public `torch.distributed` collective APIs with the naming used by torchcomms' `TorchCommBackend`, `all_gather_into_tensor` is renamed to `all_gather_single` and `reduce_scatter_tensor` to `reduce_scatter_single`. The previous names continue to work as thin wrappers that delegate to the new functions, but now emit a `FutureWarning`.

  PyTorch 2.12:
  ```python
  dist.all_gather_into_tensor(output, input)
  dist.reduce_scatter_tensor(output, input)
  ```

  PyTorch 2.13:
  ```python
  dist.all_gather_single(output, input)
  dist.reduce_scatter_single(output, input)
  ```

# New Features

## Python Frontend

- Add two new operator tags, `torch.Tag.inplace` and `torch.Tag.out`, that let an operator declare how it writes its result: `inplace` means it mutates a tensor in place, and `out` means it writes into a caller-provided output tensor. Native PyTorch operators are tagged automatically, and custom operators defined with `torch.library` can opt in by adding the tag. To be tagged `inplace`, an operator must take the tensor it mutates as its first positional argument (declared as `Tensor(a!)`, and the only mutable argument) and return that same tensor. Tagging a custom operator this way improves its behavior under `torch.compile`: `inplace` ops now go through `auto_functionalize`, so the reinplacing pass can analyze clones and skip unnecessary copies, and both `inplace` and `out` ops get their fake/meta kernels generated for free. See the [Python custom operators tutorial](https://docs.pytorch.org/tutorials/advanced/python_custom_ops.html) for how to author and tag custom operators. ([#181100](https://github.com/pytorch/pytorch/pull/181100), [#181099](https://github.com/pytorch/pytorch/pull/181099), [#184199](https://github.com/pytorch/pytorch/pull/184199), [#184200](https://github.com/pytorch/pytorch/pull/184200), [#184201](https://github.com/pytorch/pytorch/pull/184201), [#184202](https://github.com/pytorch/pytorch/pull/184202), [#184203](https://github.com/pytorch/pytorch/pull/184203), [#180851](https://github.com/pytorch/pytorch/pull/180851), [#180852](https://github.com/pytorch/pytorch/pull/180852))
- Add `const_data_ptr()` Python binding to `torch.Tensor` for read-only data pointer access ([#180382](https://github.com/pytorch/pytorch/pull/180382))
- Add an `abbr` property to `torch.dtype` that returns a dtype's short string abbreviation (e.g. `torch.float32.abbr` returns `"f32"`) ([#177296](https://github.com/pytorch/pytorch/pull/177296))
- Allow positional arguments to be passed as keyword arguments to autograd custom `Function`s ([#182206](https://github.com/pytorch/pytorch/pull/182206))
- Expose `rearrange` in the `torch.func` namespace for einops-style tensor reshaping ([#173183](https://github.com/pytorch/pytorch/pull/173183))

## torch.nn

- Add `nn.LinearCrossEntropyLoss`, a fused linear-projection plus cross-entropy loss module that avoids materializing the full logits tensor ([#181573](https://github.com/pytorch/pytorch/pull/181573), [#185852](https://github.com/pytorch/pytorch/pull/185852), [#172286](https://github.com/pytorch/pytorch/pull/172286), [#186113](https://github.com/pytorch/pytorch/pull/186113))

## Autograd

- Add `torch.autograd.graph.region_activation_memory_budget` ([#185979](https://github.com/pytorch/pytorch/pull/185979))
- Support passing gradient inputs as a `dict` to `torch.autograd.grad` and `torch.autograd.backward` ([#178140](https://github.com/pytorch/pytorch/pull/178140))

## Distributed

- Add a registration API for symmetric memory arguments (`lib.register_symm_mem_args()`), letting operators (including out-of-tree ops) declare which arguments require symmetric-memory allocation ([#173513](https://github.com/pytorch/pytorch/pull/173513))
- Remove `NCCLSymmetricMemory`'s explicit dependency on `ProcessGroupNCCL`, enabling symmetric memory to work with out-of-tree backends such as torchcomms ([#184260](https://github.com/pytorch/pytorch/pull/184260))
- Support accessing the `ReduceOp.PREMUL_SUM` factor from Python when implementing process group backends in Python ([#185863](https://github.com/pytorch/pytorch/pull/185863))
- Expose the NCCL 2.30 `maxP2pPeers` config binding ([#181686](https://github.com/pytorch/pytorch/pull/181686))
- Add rocSHMEM Triton integration for symmetric memory on ROCm ([#178658](https://github.com/pytorch/pytorch/pull/178658))

- Support passing extra keyword arguments to the loss function in pipeline schedules via a new `loss_kwargs` parameter to `step()`, enabling loss functions that require arguments beyond `(output, target)` (such as chunked cross-entropy needing token counts for scaling) ([#181057](https://github.com/pytorch/pytorch/pull/181057))

## Distributed FSDP2

- Add `FSDPModule.set_separate_reduce_scatter_group` to give reduce-scatter its own NCCL communicator, enabling opt-in overlap of all-gather and reduce-scatter ([#186335](https://github.com/pytorch/pytorch/pull/186335))
- Add `set_reduce_scatter_max_input_buffers` to keep multiple reduce-scatter input buffers in flight, so backward compute no longer stalls waiting to recycle a single reduce-scatter buffer ([#186000](https://github.com/pytorch/pytorch/pull/186000))

## Profiler

- Profiler/Kineto now emits channel metadata on CUDA backends ([#185968](https://github.com/pytorch/pytorch/pull/185968))

## Dynamo

- Add `torch.compiler.set_default_backend` to override the default `torch.compile` backend globally, so out-of-tree backend authors don't need to pass `backend=` at every call site (following the pattern of `torch.set_default_dtype`/`torch.set_default_device`). Explicit `backend=` arguments still take precedence ([#178944](https://github.com/pytorch/pytorch/pull/178944))
- Add `torch.compile(f, isolate_recompiles=True)` to give each `torch.compile` call its own isolated cache bucket, preventing cross-compile interference in cache lookups and recompile-limit checks when multiple `torch.compile` calls target the same function ([#178351](https://github.com/pytorch/pytorch/pull/178351))
- Add `register_multi_grad_hook` support to `@leaf_function`, allowing a backward hook to fire once per backward pass when all `requires_grad` inputs have their gradients computed ([#179609](https://github.com/pytorch/pytorch/pull/179609))

## Inductor

- Add flash-decoding support to the CPU `FlexAttention` template (chosen when query length is 1) with a new configurable `PARTITION_SIZE` kernel option ([#159835](https://github.com/pytorch/pytorch/pull/159835))
- Add Triton convolution backward kernels (input and weight gradients) as an autotuning backend in place of the ATen-only fallback ([#178945](https://github.com/pytorch/pytorch/pull/178945))
- Add an Inductor FX pass (`decomp_comms`) that eliminates `all_gather` for Gram-matrix optimizer patterns (Muon/Shampoo) under FSDP, gated by `config.aten_distributed_optimizations.allow_comms_decompositions`, yielding 1.25-1.95x training speedups ([#184370](https://github.com/pytorch/pytorch/pull/184370))

## Ahead-Of-Time Inductor (AOTI)

- Generated C shims for the AOTI stable ABI are now versioned and gated by `TORCH_TARGET_VERSION`, so shims introduced in newer releases are only exposed when the target version supports them ([#181916](https://github.com/pytorch/pytorch/pull/181916))
- Triton CPU AOTI models now work end-to-end through the public `torch._inductor.aoti_compile_and_package` / `aoti_load_package` API, including packaging and loading of the multiple `.so` files emitted per kernel ([#182251](https://github.com/pytorch/pytorch/pull/182251))
- Added stable C shim functions (`torch_exception_get_what`, `torch_exception_get_what_without_backtrace`, and `STABLE_TORCH_ERROR_CODE_CHECK`) so extensions built against the stable ABI can retrieve the original error message across the C API boundary (target version 2.13+) ([#180135](https://github.com/pytorch/pytorch/pull/180135))
- Added a stable AOTI stream shim `aoti_torch_stream_native_handle` and `torch::stable::accelerator::Stream::nativeHandle()`, gated behind `TORCH_FEATURE_VERSION >= 2.13`, for retrieving a native stream handle from the stable ABI ([#183930](https://github.com/pytorch/pytorch/pull/183930))

## Release Engineering

- Add Python 3.15 wheel builds across Linux (CPU/CUDA), Triton, ROCm, and XPU ([#182954](https://github.com/pytorch/pytorch/pull/182954), [#184600](https://github.com/pytorch/pytorch/pull/184600), [#185409](https://github.com/pytorch/pytorch/pull/185409), [#184829](https://github.com/pytorch/pytorch/pull/184829), [#184891](https://github.com/pytorch/pytorch/pull/184891), [#184906](https://github.com/pytorch/pytorch/pull/184906), [#185094](https://github.com/pytorch/pytorch/pull/185094))

## CUDA

- Add `CUDAGraph.get_graph_data()` for graph topology introspection ([#183165](https://github.com/pytorch/pytorch/pull/183165))
- Lightweight API to get private pool reserved memory bytes ([#178240](https://github.com/pytorch/pytorch/pull/178240))

## MPS

- Add FlexAttention support for MPS ([#182552](https://github.com/pytorch/pytorch/pull/182552), [#186215](https://github.com/pytorch/pytorch/pull/186215))
- Add support for `torch.distributions.Dirichlet` on MPS by adding `_sample_dirichlet` and `_dirichlet_grad` Metal implementations ([#185458](https://github.com/pytorch/pytorch/pull/185458), [#185854](https://github.com/pytorch/pytorch/pull/185854))
- Add `grid_sampler_2d` backward support on MPS ([#179756](https://github.com/pytorch/pytorch/pull/179756))
- Add `grid_sampler_3d` backward support on MPS ([#179388](https://github.com/pytorch/pytorch/pull/179388))
- Add `lcm` support on MPS via a new Metal kernel ([#186279](https://github.com/pytorch/pytorch/pull/186279))
- Add complex support to `c10/metal/reduction_utils.h` ([#180708](https://github.com/pytorch/pytorch/pull/180708)) and a complex->bool specialization ([#185938](https://github.com/pytorch/pytorch/pull/185938))

## ROCm

- Enable external events in CUDA graphs ([#178264](https://github.com/pytorch/pytorch/pull/178264))
- Enable GPU Address Sanitizer build ([#183792](https://github.com/pytorch/pytorch/pull/183792), [#176461](https://github.com/pytorch/pytorch/pull/176461))
- Improve Inductor GEMM search space performance using the Origami project ([#172512](https://github.com/pytorch/pytorch/pull/172512))
- Use CMake native HIP language support, `enable_language(HIP)` ([#180485](https://github.com/pytorch/pytorch/pull/180485))
- New Inductor benchmarker based on Torch Profiler ([#175097](https://github.com/pytorch/pytorch/pull/175097))

## XPU

- Add XPU device telemetry APIs for temperature, frequency, power draw, engine utilization, memory bandwidth usage, and used device memory through `torch.xpu.*` ([#181082](https://github.com/pytorch/pytorch/pull/181082), [#183427](https://github.com/pytorch/pytorch/pull/183427), [#183428](https://github.com/pytorch/pytorch/pull/183428), [#183429](https://github.com/pytorch/pytorch/pull/183429), [#183430](https://github.com/pytorch/pytorch/pull/183430), [#183431](https://github.com/pytorch/pytorch/pull/183431))
- Add FP8 blockwise scaling support for `scaled_mm` on XPU ([#173630](https://github.com/pytorch/pytorch/pull/173630), [#176043](https://github.com/pytorch/pytorch/pull/176043))

# Improvements

## Python Frontend

- Make it possible to load safetensors with `torch.load` ([#170592](https://github.com/pytorch/pytorch/pull/170592))
- Make `Storage.pin_memory` / `Storage.is_pinned` device-agnostic ([#186223](https://github.com/pytorch/pytorch/pull/186223))
- Add `op_overloads` to `OpOverloadPacket` to enumerate an operator's overloads ([#182993](https://github.com/pytorch/pytorch/pull/182993))

## torch.nn

- Expose `num_splits` in FlashAttention-2 and bump the flash-attention submodule ([#179760](https://github.com/pytorch/pytorch/pull/179760))
- Support `linear_bias` in `linear_cross_entropy` on the reference and chunked paths ([#185129](https://github.com/pytorch/pytorch/pull/185129), [#185276](https://github.com/pytorch/pytorch/pull/185276))

## Optimizer

- Fix `SequentialLR` wrong learning rate initialization when `milestones` contain 0 ([#185986](https://github.com/pytorch/pytorch/pull/185986))

## Autograd

- Implement autograd derivatives for `torch.nextafter` ([#148820](https://github.com/pytorch/pytorch/pull/148820))
- Add `torch.autograd.enforce_grad_layout_policy` to control the memory layout policy for accumulated gradients ([#180552](https://github.com/pytorch/pytorch/pull/180552))

## Distributed

- When TorchComms is enabled, route `new_group` through `split_group` for subgroup creation, raising `NotImplementedError` for arguments `split_group` cannot honor (e.g. `use_local_synchronization=True`, `sort_ranks=False`) instead of silently falling back ([#185416](https://github.com/pytorch/pytorch/pull/185416))
- Delegate `dist.new_group` to custom process group subclasses ([#184262](https://github.com/pytorch/pytorch/pull/184262))
- Surface started-work metadata in NCCL watchdog timeouts ([#183656](https://github.com/pytorch/pytorch/pull/183656))
- Add a health check endpoint to the distributed debug server ([#179326](https://github.com/pytorch/pytorch/pull/179326))
- Make the `DeviceMesh` non-overlapping check stricter ([#172343](https://github.com/pytorch/pytorch/pull/172343))

- Allow `elastic_launch`/`launch_agent` to accept a pre-created torchelastic health check server, so it can be started before rendezvous ([#180543](https://github.com/pytorch/pytorch/pull/180543))
- Add an `overlap_pp_comm` flag to pipeline schedules (default `True`) that, when set to `False`, defers each pipeline RECV op to immediately before the compute op that consumes it, using rank-parity P2P ordering to avoid deadlock (helps platforms such as AMD ROCm where a pending RECV blocks unrelated compute) ([#178815](https://github.com/pytorch/pytorch/pull/178815))

## DTensor

- Migrate embedding and random ops to single-dim sharding strategies and increase op coverage ([#180281](https://github.com/pytorch/pytorch/pull/180281), [#180503](https://github.com/pytorch/pytorch/pull/180503))
- Add auto-infrastructure that derives single-dim sharding strategies for autogenerated op variants (`.out`, inplace, functional, and `foreach`), expanding strategy coverage to hundreds of additional ops ([#185386](https://github.com/pytorch/pytorch/pull/185386))
- Register sharding strategies for additional ops: `scatter`, upsample/interpolation backward, anti-aliased upsample, batch norm backward, and `aten.detach_.default` ([#186149](https://github.com/pytorch/pytorch/pull/186149), [#180311](https://github.com/pytorch/pytorch/pull/180311), [#184626](https://github.com/pytorch/pytorch/pull/184626), [#182743](https://github.com/pytorch/pytorch/pull/182743), [#181876](https://github.com/pytorch/pytorch/pull/181876))

## Distributed FSDP2

- Support forward-mode automatic differentiation (`torch.func.jvp`) on models wrapped with `fully_shard` or `replicate`, including with mixed precision ([#182732](https://github.com/pytorch/pytorch/pull/182732))

## Linear Algebra Frontend

- Add `Half` and `BFloat16` dispatch support for `torch.trace` on CPU ([#184874](https://github.com/pytorch/pytorch/pull/184874))
- Improve heuristics for the cuSOLVER vs cuBLAS backend switch in `torch.linalg.lu` ([#185344](https://github.com/pytorch/pytorch/pull/185344))

## Profiler

- The memory viz tool now more accurately represents GPU footprint when impacted by fragmentation ([#180515](https://github.com/pytorch/pytorch/pull/180515))
- The memory viz tool now aggregates stripes per-pool to improve visualization for large snapshots ([#180613](https://github.com/pytorch/pytorch/pull/180613))
- Profiler now also exposes CUDA occupancy metadata as a nested dictionary in the `.events()` output ([#180275](https://github.com/pytorch/pytorch/pull/180275))

## FX

- `split_module` now supports `torch.Size` crossing graph split boundaries by decomposing `size()` calls into per-dimension `sym_size` nodes, and builds submodules lazily for faster inference graph splitting ([#179839](https://github.com/pytorch/pytorch/pull/179839))
- `CapabilityBasedPartitioner` can now opt out of horizontal fusion via `skip_horizontal_fusion=True`, partitioning only through direct data dependencies ([#184904](https://github.com/pytorch/pytorch/pull/184904))

- Enable rewriting of FX traces containing complex tensors during compilation ([#169832](https://github.com/pytorch/pytorch/pull/169832))

## Dynamo

- Implement additional Python operators in Dynamo: bitwise and ([#184788](https://github.com/pytorch/pytorch/pull/184788)), bitwise xor ([#184789](https://github.com/pytorch/pytorch/pull/184789)), left/right shift ([#183462](https://github.com/pytorch/pytorch/pull/183462)), floor division ([#185652](https://github.com/pytorch/pytorch/pull/185652)), true division ([#185653](https://github.com/pytorch/pytorch/pull/185653)), remainder ([#185654](https://github.com/pytorch/pytorch/pull/185654)), and `divmod` ([#185655](https://github.com/pytorch/pytorch/pull/185655))
- Support tracing more constructs in Dynamo: `einops` 0.8.2 ([#185619](https://github.com/pytorch/pytorch/pull/185619)), `record_function` as a decorator ([#184703](https://github.com/pytorch/pytorch/pull/184703)), `inference_mode` retracing helpers ([#185066](https://github.com/pytorch/pytorch/pull/185066)), `mark_dirty` in the autograd Function HOP ([#184267](https://github.com/pytorch/pytorch/pull/184267)), `warn_only` deterministic toggles ([#180373](https://github.com/pytorch/pytorch/pull/180373)), and the `_maybe_view_chunk_cat` functional collective ([#180389](https://github.com/pytorch/pytorch/pull/180389))
- Support item assignment and deletion (`__setitem__`/`__delitem__`) on more container types in Dynamo via `sq_ass_item`/`mp_ass_subscript` slots ([#182862](https://github.com/pytorch/pytorch/pull/182862), [#182996](https://github.com/pytorch/pytorch/pull/182996))
- Support `torch.accelerator.device_index` and `torch.xpu.device` in the device context manager ([#181846](https://github.com/pytorch/pytorch/pull/181846), [#181847](https://github.com/pytorch/pytorch/pull/181847))
- Improve Triton support under `torch.compile`: accept `tl.constexpr` values as kernel arguments ([#181783](https://github.com/pytorch/pytorch/pull/181783)) and handle `capture_triton` as a no-op during tracing ([#183555](https://github.com/pytorch/pytorch/pull/183555))
- Improve dynamic shape specification: reduce verbosity in shape specs for the common case ([#184271](https://github.com/pytorch/pytorch/pull/184271)), add `SeqSpec` for list/tuple specs with better walk-spec errors ([#185327](https://github.com/pytorch/pytorch/pull/185327)), add `ObjectSpec` ([#182764](https://github.com/pytorch/pytorch/pull/182764)), pipe dynamic spec through `torch.compile` ([#184501](https://github.com/pytorch/pytorch/pull/184501)), and revisit guarding in `mark_dynamic` APIs ([#181469](https://github.com/pytorch/pytorch/pull/181469))
- Improve `torch.compile` device mismatch errors with a dedicated `FakeTensorDeviceMismatchError` and actionable guidance to place inputs, parameters, and buffers on the same device ([#185412](https://github.com/pytorch/pytorch/pull/185412))
- Improve error messages and diagnostics: clearer data-dependent errors for `.any()`/`.all()` ([#180406](https://github.com/pytorch/pytorch/pull/180406)), clearer `torch._check` tensor predicate errors ([#185777](https://github.com/pytorch/pytorch/pull/185777)), user-friendly reasons for skipped frames ([#183596](https://github.com/pytorch/pytorch/pull/183596)), carets in stack traces ([#182393](https://github.com/pytorch/pytorch/pull/182393)), and reporting why a symbol was created dynamically in `symbolic_shapes` logs ([#168331](https://github.com/pytorch/pytorch/pull/168331))
- Make Dynamo exceptions pickleable ([#185725](https://github.com/pytorch/pytorch/pull/185725))
- Inline decomposed quantization helpers in Dynamo ([#185628](https://github.com/pytorch/pytorch/pull/185628))
- Make Dynamo debug/repro utilities device-agnostic ([#184851](https://github.com/pytorch/pytorch/pull/184851))

## Inductor

- Support `pin_memory` for `torch.ones`, `torch.zeros` and `torch.full` ([#174595](https://github.com/pytorch/pytorch/pull/174595))
- Add a ROCm config flag to disable the `pointer_range_32` optimization ([#179604](https://github.com/pytorch/pytorch/pull/179604))
- Add a peak memory threshold config for combo kernels ([#180578](https://github.com/pytorch/pytorch/pull/180578))
- Enable autotuning and a fast compensation path for CPU static/dynamic smooth-quant qlinear, with correct handling of 0D `x_scale`/`x_zp` and `ReinterpretView` strides ([#181090](https://github.com/pytorch/pytorch/pull/181090))
- Add `aot_inductor.autotune_per_kernel_alloc` config to allocate-run-delete tensors per kernel during AOTI autotuning, avoiding OOM on large models ([#181176](https://github.com/pytorch/pytorch/pull/181176))
- Bound `AsyncCompile` future waits with the `compile_worker_wait_timeout` setting ([#181293](https://github.com/pytorch/pytorch/pull/181293))
- Add `a100_default_flex_config` entries for `head_dim=192` ([#181835](https://github.com/pytorch/pytorch/pull/181835))
- Add an explicit lowering (fallback) for `aten.multinomial` to avoid graph breaks ([#182423](https://github.com/pytorch/pytorch/pull/182423))
- Add an Inductor lowering for `_scaled_mm_v2` ([#182527](https://github.com/pytorch/pytorch/pull/182527))
- Enable `combo_kernel_autotune_grouping` by default ([#182567](https://github.com/pytorch/pytorch/pull/182567))
- Add `cudagraph_partition_memory_budget` config for partition reordering ([#183569](https://github.com/pytorch/pytorch/pull/183569))
- Add ATen fallbacks for `bincount`, `unique` variants, and AMP scale ops so they compile without graph breaks ([#183590](https://github.com/pytorch/pytorch/pull/183590))
- Unfuse the bias add from `addmm` when the bias is a narrowing dtype cast (fp32->bf16/fp16) to preserve bias precision in XPU AMP training ([#183680](https://github.com/pytorch/pytorch/pull/183680))
- Emit a clearer diagnostic when a backward CUDAGraph output installed as a `.grad` buffer is invalidated on a later run (gradient accumulation) ([#184003](https://github.com/pytorch/pytorch/pull/184003))
- Support split online softmax reductions in Inductor ([#184069](https://github.com/pytorch/pytorch/pull/184069))
- Support fusing `index_add`-style atomic scatter mutations into Triton template epilogues behind a config flag ([#184179](https://github.com/pytorch/pytorch/pull/184179))
- Add a `cpp.march` Inductor config knob so AOTInductor cpp-only builds can override or suppress the default CPU architecture flag ([#184297](https://github.com/pytorch/pytorch/pull/184297))
- Improve the Triton cache directory guidance when loading shared objects from a noexec filesystem fails ([#184362](https://github.com/pytorch/pytorch/pull/184362))
- Enable the Bert SDPA pattern rewrite on CUDA while keeping the original matmul/softmax math path ([#184417](https://github.com/pytorch/pytorch/pull/184417))
- Improve the Triton launcher argument-mismatch error with a clearer message and a cached preflight check ([#184522](https://github.com/pytorch/pytorch/pull/184522))
- Add broader CuteDSL op overrides (`rsqrt`, `exp2`, `log2`, `log10`, `tan`, `acos`, `asin`, `atan`, `atan2`, `floor`, `logical_xor`) ([#184538](https://github.com/pytorch/pytorch/pull/184538))
- Add an optional `fake_mode` argument to `standalone_compile` (with `dynamic_shapes="from_example_inputs"`) so it can reuse the caller's `FakeTensorMode`/`ShapeEnv` instead of always creating a fresh one ([#184776](https://github.com/pytorch/pytorch/pull/184776))
- Support `signbit` on unsigned integer dtypes ([#185985](https://github.com/pytorch/pytorch/pull/185985))
- Add a `keep_static_cubin_raw` config to retain cubin bytes in cached kernels so caches restored on another machine avoid recompilation ([#186404](https://github.com/pytorch/pytorch/pull/186404))
- Extend `BatchLinearLHSFusion`'s matcher to also match the inlined `torch._C._nn.linear` form so the (opt-in) fusion can fire on Dynamo-inlined linear ([#186632](https://github.com/pytorch/pytorch/pull/186632))
- Add a clearer error message with install instructions when a compatible Flash Attention package is unavailable for flex attention ([#186827](https://github.com/pytorch/pytorch/pull/186827))
- Add another anchor node to the batch-linear fusion pass so more small `torch._C._nn.linear` operations are grouped into a single batched kernel ([#180477](https://github.com/pytorch/pytorch/pull/180477))
- Extend the batch fusion pass to support `detach()` method calls ([#180513](https://github.com/pytorch/pytorch/pull/180513))
- Add a deterministic backward for the FlexAttention flash kernel ([#174813](https://github.com/pytorch/pytorch/pull/174813))
- Use rand4x for Inductor Triton random number generation ([#184377](https://github.com/pytorch/pytorch/pull/184377))
- Add a Quack-based CuTeDSL RMSNorm kernel ([#182108](https://github.com/pytorch/pytorch/pull/182108))

## Ahead-Of-Time Inductor (AOTI)

- Use fatbinary for multi-arch CUDA kernels ([#184456](https://github.com/pytorch/pytorch/pull/184456))
- Support mixed-device constants in `update_constant_buffer` ([#181114](https://github.com/pytorch/pytorch/pull/181114))
- Add FP8 header files in the AOTI `shim.h` ([#178120](https://github.com/pytorch/pytorch/pull/178120))
- Add throttled `cudaMemcpy` for AOTI constant loading to reduce peak memory usage ([#184823](https://github.com/pytorch/pytorch/pull/184823))
- Preserve AOTI `proxy_executor` error messages ([#180884](https://github.com/pytorch/pytorch/pull/180884))
- Enable Triton kernels in AOTI C++ wrapper on CPU ([#181068](https://github.com/pytorch/pytorch/pull/181068))
- Skip CPU vec ISA setup for device-only `cpp_wrapper` ([#182089](https://github.com/pytorch/pytorch/pull/182089))
- Expose torchbind constants from `AOTIModelPackageLoader` ([#182149](https://github.com/pytorch/pytorch/pull/182149))
- Improve AOTI error for Python custom ops ([#186305](https://github.com/pytorch/pytorch/pull/186305))

## Export

- Support serialization of opaque type constants in `torch.export` save/load ([#181676](https://github.com/pytorch/pytorch/pull/181676))
- Make functorch JVP operator `torch.export`-able ([#179686](https://github.com/pytorch/pytorch/pull/179686))
- Add `UpdateConstantBufferFromCpu` for host-to-device copy ([#181637](https://github.com/pytorch/pytorch/pull/181637))

## AOTAutograd

- Support CPU activation offloading in the rematerialization pass, including marking recomputed nodes for backward and adding a resize-to-0 deallocation op so offloaded tensors are freed after their host-to-device copy ([#181937](https://github.com/pytorch/pytorch/pull/181937), [#181938](https://github.com/pytorch/pytorch/pull/181938))
- Use FX node names in `merge_view_inputs` error messages, so non-differentiable view input mutation errors identify the specific offending inputs ([#180424](https://github.com/pytorch/pytorch/pull/180424))

## Composability

- Add fake tensor support for `_transformer_encoder_layer_fwd` so it traces under `torch.compile` ([#183916](https://github.com/pytorch/pytorch/pull/183916))
- Enable Armv9-A target support for `torch.compile` on AArch64 ([#184555](https://github.com/pytorch/pytorch/pull/184555))
- Functionalize in-place `c10d` collectives in standalone compile ([#181836](https://github.com/pytorch/pytorch/pull/181836))

## Foreach

- Fix/add empty check for `_foreach_max` ([#173483](https://github.com/pytorch/pytorch/pull/173483))

## ONNX

- Add `adaptive_max_pool2d` and `adaptive_max_pool3d` decompositions for ONNX export ([#184396](https://github.com/pytorch/pytorch/pull/184396))

## C++ Frontend

- Add stable ABI for `set_python_module` on `torch::Library` ([#182720](https://github.com/pytorch/pytorch/pull/182720))
- Add `==` overloads for `HeaderOnlyArrayRef` ([#185379](https://github.com/pytorch/pytorch/pull/185379))
- Add `torch::stable::Generator` ([#186423](https://github.com/pytorch/pytorch/pull/186423))
- Add `c10::layout` typecaster for `torch.layout` ([#179607](https://github.com/pytorch/pytorch/pull/179607))
- Add default-args support to `def_static` ([#175644](https://github.com/pytorch/pytorch/pull/175644))
- Add support for controlling scientific notation in C++-side tensor printing ([#173321](https://github.com/pytorch/pytorch/pull/173321))

## Release Engineering

- Move the NCCL pin to 2.30 ([#181313](https://github.com/pytorch/pytorch/pull/181313))
- Advance the Triton pin to 3.7.1 ([#181001](https://github.com/pytorch/pytorch/pull/181001), [#186792](https://github.com/pytorch/pytorch/pull/186792))
- Upgrade the XPU support package to 2026.0 ([#182003](https://github.com/pytorch/pytorch/pull/182003))
- Add a configurable threshold to avoid power-of-two rounding for large pinned memory allocations ([#171662](https://github.com/pytorch/pytorch/pull/171662))
- Move some pre-build steps from `setup.py` to CMake ([#177641](https://github.com/pytorch/pytorch/pull/177641))

## CUDA

- Debugging tool to verify that external inputs to a CUDA graph are alive before replay ([#174649](https://github.com/pytorch/pytorch/pull/174649))
- Add get/set/reset functions for BLAS workspace sizes ([#177912](https://github.com/pytorch/pytorch/pull/177912))
- Cleanup double import in `BinaryDivFloorKernel.cu` ([#179260](https://github.com/pytorch/pytorch/pull/179260))
- Return supported CUDA arch list when no GPU is present but GPU is compiled ([#180356](https://github.com/pytorch/pytorch/pull/180356))
- Detect and fix stale stream references in autograd during CUDA graph capture ([#180090](https://github.com/pytorch/pytorch/pull/180090))
- Use `opmath_t` in `i1` and `i1e` CUDA kernels ([#183778](https://github.com/pytorch/pytorch/pull/183778))
- Support `resize_` with address hint ([#178215](https://github.com/pytorch/pytorch/pull/178215))
- Support `bfloat16` in `_embedding_bag_per_sample_weights_backward` on CUDA ([#185889](https://github.com/pytorch/pytorch/pull/185889))
- Align `parsePerProcessMemoryFraction`'s return type with other parsers ([#185139](https://github.com/pytorch/pytorch/pull/185139))
- Improve error message when `cuda-bindings` version is too old ([#185990](https://github.com/pytorch/pytorch/pull/185990))
- Expose `torch.cuda.current_solver_handle` for cuSOLVER handle sharing ([#176705](https://github.com/pytorch/pytorch/pull/176705))

## cuDNN

- Add flag to select depthwise convolution backend ([#176500](https://github.com/pytorch/pytorch/pull/176500))
- Upgrade `cudnn_frontend` submodule to 1.24 ([#185554](https://github.com/pytorch/pytorch/pull/185554))

## MPS

- Migrate many ops from MPSGraph to native Metal kernels for `bernoulli` ([#182210](https://github.com/pytorch/pytorch/pull/182210)), `native_dropout` ([#182232](https://github.com/pytorch/pytorch/pull/182232)), `uniform`/`normal`/`randint` ([#182386](https://github.com/pytorch/pytorch/pull/182386)), `randperm` ([#182528](https://github.com/pytorch/pytorch/pull/182528)), comparison ops `eq`/`ne`/`lt`/`le`/`gt`/`ge` ([#183019](https://github.com/pytorch/pytorch/pull/183019)), bitwise ops ([#182839](https://github.com/pytorch/pytorch/pull/182839)), scatter/gather ([#184028](https://github.com/pytorch/pytorch/pull/184028)), copy-cast ([#184740](https://github.com/pytorch/pytorch/pull/184740)), `gelu`/`gelu_backward` ([#181451](https://github.com/pytorch/pytorch/pull/181451)), replication pad ([#183065](https://github.com/pytorch/pytorch/pull/183065)), embedding backward ([#185119](https://github.com/pytorch/pytorch/pull/185119)), `trace` ([#183627](https://github.com/pytorch/pytorch/pull/183627)), `count_nonzero` ([#180725](https://github.com/pytorch/pytorch/pull/180725)), `amax`/`amin`/`aminmax`/`all`/`any` ([#180752](https://github.com/pytorch/pytorch/pull/180752)), and `cumsum`/`cumprod` ([#185609](https://github.com/pytorch/pytorch/pull/185609)), `native_group_norm` ([#183830](https://github.com/pytorch/pytorch/pull/183830), `native_group_norm_backward` [#184437](https://github.com/pytorch/pytorch/pull/184437)), `topk` and `kthvalue` Metal kernels ([#184106](https://github.com/pytorch/pytorch/pull/184106)), single-block and multi-block sort, including a stable sort path ([#180714](https://github.com/pytorch/pytorch/pull/180714), [#182242](https://github.com/pytorch/pytorch/pull/182242), [#181736](https://github.com/pytorch/pytorch/pull/181736))
- Support integer inputs to `histc` ([#178624](https://github.com/pytorch/pytorch/pull/178624))
- Support `out` variants of unary ops ([#184743](https://github.com/pytorch/pytorch/pull/184743))
- Improvements to SDPA Metal kernels: prefill attention kernels ([#181575](https://github.com/pytorch/pytorch/pull/181575)), GQA support ([#183280](https://github.com/pytorch/pytorch/pull/183280)), `is_causal` support ([#181855](https://github.com/pytorch/pytorch/pull/181855)), head dim 256 ([#181852](https://github.com/pytorch/pytorch/pull/181852)), float mask support ([#183458](https://github.com/pytorch/pytorch/pull/183458)), and a clearer error for causal + attn mask ([#181856](https://github.com/pytorch/pytorch/pull/181856))
- Add an ILP variant for binary tensor iterators and replace unary VEC4 with a generic ILP-per-thread dense kernel ([#182155](https://github.com/pytorch/pytorch/pull/182155), [#181509](https://github.com/pytorch/pytorch/pull/181509), [#183055](https://github.com/pytorch/pytorch/pull/183055))
- Make several Metal kernels stride-aware to avoid unnecessary `.contiguous()` calls: `Col2Im` ([#181949](https://github.com/pytorch/pytorch/pull/181949)), `Im2Col` ([#182709](https://github.com/pytorch/pytorch/pull/182709)), `Repeat` ([#182718](https://github.com/pytorch/pytorch/pull/182718)), `LossOps` ([#182714](https://github.com/pytorch/pytorch/pull/182714)), and `HistogramKernel` ([#181951](https://github.com/pytorch/pytorch/pull/181951))
- Enable `NDHWC`+`DHWIO` fast path for `Conv3d` on `channels_last_3d` ([#184612](https://github.com/pytorch/pytorch/pull/184612))
- Clear the MPSGraph cache in `torch.mps.empty_cache()` ([#181485](https://github.com/pytorch/pytorch/pull/181485))
- Add a private API to get the host alias of Metal storage ([#180961](https://github.com/pytorch/pytorch/pull/180961))
- Add input validation: `stride > 0` in pool ops ([#184875](https://github.com/pytorch/pytorch/pull/184875)), `F.fold` ([#182067](https://github.com/pytorch/pytorch/pull/182067)), `im2col` ([#183593](https://github.com/pytorch/pytorch/pull/183593)), and bernoulli probabilities ([#185065](https://github.com/pytorch/pytorch/pull/185065))
- Alert on non-deterministic algorithms on MPS ([#185061](https://github.com/pytorch/pytorch/pull/185061))
- Raise a clear not-implemented error for `dropout_p` ([#184126](https://github.com/pytorch/pytorch/pull/184126))
- Use proper precise log functions in unary kernels ([#185381](https://github.com/pytorch/pytorch/pull/185381))

## ROCm

- Additional `cub::DeviceHistogram` hipify mappings ([#180433](https://github.com/pytorch/pytorch/pull/180433))
- SDPA improvements via AOTriton 0.12b: `head_dim != head_dim_v`, `use_deterministic_algorithms`, `gfx1100` and `gfx1151` promoted out of experimental, partial FAv3 support on `gfx950` ([#184288](https://github.com/pytorch/pytorch/pull/184288))

## XPU

- Add `last_level_cache_size` and `is_integrated_gpu` to XPU device properties ([#184499](https://github.com/pytorch/pytorch/pull/184499), [#182624](https://github.com/pytorch/pytorch/pull/182624))
- Add XPU dispatch for `_fused_adagrad_` ([#185577](https://github.com/pytorch/pytorch/pull/185577))
- Support mixed-type operations between Nested and Dense tensors on XPU ([#182654](https://github.com/pytorch/pytorch/pull/182654))
- Support `torch.xpu.device` in Dynamo device management ([#181847](https://github.com/pytorch/pytorch/pull/181847))
- Recognize additional Intel BMG device IDs on XPU ([#183414](https://github.com/pytorch/pytorch/pull/183414))
- Enable XPU device support for sparse Triton ops ([#179805](https://github.com/pytorch/pytorch/pull/179805))
- Enable the `bmm_outer_product` Triton override on XPU ([#180441](https://github.com/pytorch/pytorch/pull/180441))
- Improve test coverage for the XPU backend ([#174370](https://github.com/pytorch/pytorch/pull/174370), [#180881](https://github.com/pytorch/pytorch/pull/180881), [#171154](https://github.com/pytorch/pytorch/pull/171154))
- Support non-blocking pinned device-to-host copies on XPU ([#186224](https://github.com/pytorch/pytorch/pull/186224))
- Refactor the XPU oneDNN integration from the C API to the C++ API ([#184486](https://github.com/pytorch/pytorch/pull/184486))

## Functorch

- Add `vmap` batching rule for `torch.unbind_copy` ([#178035](https://github.com/pytorch/pytorch/pull/178035))
- Add `vmap` batching rule for `Tensor.view(dtype)` (`aten::view.dtype`) ([#180728](https://github.com/pytorch/pytorch/pull/180728))

## Sparse Frontend

- Validate `mat1`/`mat2` layouts in `sspaddmm` and clarify error messages ([#179037](https://github.com/pytorch/pytorch/pull/179037))

# Bug Fixes

## Python Frontend

- Add `opt_dtype` validation to `torch.nanmean()` for consistent error handling ([#172809](https://github.com/pytorch/pytorch/pull/172809))
- Route `torch.nansum` integer output dtype through `nan_to_num` + `sum` for correct results ([#183808](https://github.com/pytorch/pytorch/pull/183808))
- Fix out-of-bounds read in `CUDAStream::stream()` ([#184237](https://github.com/pytorch/pytorch/pull/184237))
- Align XPU `logspace`/`linspace` ref tests with upstream XFAIL state ([#178734](https://github.com/pytorch/pytorch/pull/178734))

## Dataloader Frontend

- Fix `DataLoader` file descriptor leak from `atexit` cleanup ([#176607](https://github.com/pytorch/pytorch/pull/176607))

## torch.nn

- Validate `stride`/`padding`/`kernel_size` length in `slow_conv3d` ([#181063](https://github.com/pytorch/pytorch/pull/181063))
- Validate inputs in `math_channel_shuffle` ([#181029](https://github.com/pytorch/pytorch/pull/181029))
- Validate `delta` type in `nn.HuberLoss` constructor ([#184012](https://github.com/pytorch/pytorch/pull/184012))
- Lowercase the environment variable in `torch/serialization.py` so it matches the true values ([#180959](https://github.com/pytorch/pytorch/pull/180959))
- Fix int32 overflow in `layer_norm` on CUDA for tensors with more than 2^32 elements ([#181600](https://github.com/pytorch/pytorch/pull/181600))
- Reject `NestedTensor` inputs in `flex_attention` with a clear error instead of an unclear backend failure ([#183516](https://github.com/pytorch/pytorch/pull/183516))
- Fix SDPA incorrect early return on 0 head dim qk with valid v ([#184914](https://github.com/pytorch/pytorch/pull/184914))
- Fix `reflection_pad1d` backward CUDA launch for large batches ([#185024](https://github.com/pytorch/pytorch/pull/185024))
- Fix `lp_pool` infinity norm handling ([#183997](https://github.com/pytorch/pytorch/pull/183997))

## Autograd

- Fix checkpoint context cleanup on forward errors ([#184018](https://github.com/pytorch/pytorch/pull/184018))
- Fix `torch.autograd.enforce_grad_layout_policy` decorator state leak ([#183868](https://github.com/pytorch/pytorch/pull/183868))

## Distributed

- Fix `NCCLComm::abort()` to use the correct deregister API for window-registered handles ([#181626](https://github.com/pytorch/pytorch/pull/181626))
- Fix `FakeProcessGroup` `all_gather` on tensors that require grad ([#181790](https://github.com/pytorch/pytorch/pull/181790))
- Fix `gather` and `allgather_coalesced` on `FakeProcessGroup` to copy input to output ([#182364](https://github.com/pytorch/pytorch/pull/182364))
- Fix the `scatter` and `reduce_scatter` family on `FakeProcessGroup` to copy input to output ([#182365](https://github.com/pytorch/pytorch/pull/182365))
- Fix `all_to_all` on `FakeProcessGroup` and validate splits ([#182366](https://github.com/pytorch/pytorch/pull/182366))
- Fix conflict between `broadcast_buffers` and `init_sync` in DDP ([#178054](https://github.com/pytorch/pytorch/pull/178054))
- Fix `gather` on non-destination ranks for the TorchComms backend ([#178533](https://github.com/pytorch/pytorch/pull/178533))
- Fix TCPStore compilation with Clang 20 ([#185785](https://github.com/pytorch/pytorch/pull/185785))
- Fix NCCL symmetric memory mismatch by using an allocation-time counter instead of address for block ordering ([#183489](https://github.com/pytorch/pytorch/pull/183489))
- Fix a symbol lookup issue with the symmetric memory `__init__` ([#186416](https://github.com/pytorch/pytorch/pull/186416))
- Fix the value returned by `Work.exception()` so the exception can be inspected from Python instead of being unusable ([#184697](https://github.com/pytorch/pytorch/pull/184697))
- Fix false assertion errors in the flight recorder when using the `ncclx`, `gloo`, `rccl`, `rcclx`, `mccl`, or `hccl` backends ([#179753](https://github.com/pytorch/pytorch/pull/179753))
- Fix a failure when creating a subgroup on a fake backend via `new_group`, which has no underlying communicator to split ([#186172](https://github.com/pytorch/pytorch/pull/186172))
- Fix `torch.compile` of the `_c10d_functional` `all_gather_tensor_out` and `reduce_scatter_tensor_out` ops, which previously failed functionalization with "Found a custom (non-ATen) operator whose output has alias annotations" ([#183597](https://github.com/pytorch/pytorch/pull/183597))
- Fix `split_group` on multi-backend process groups (e.g. `init_process_group(backend="cpu:gloo,cuda:nccl")`) to split only the relevant backend instead of every backend, avoiding spurious warnings, extra rendezvous overhead, and inconsistent process-group shapes ([#182057](https://github.com/pytorch/pytorch/pull/182057))
- Fix `FakeProcessGroup` to reject `rank >= world_size` at construction time, which previously failed silently and only surfaced later when collectives indexed past `world_size` ([#182363](https://github.com/pytorch/pytorch/pull/182363))

- Fix the torchelastic agent hanging indefinitely (and never exiting) when workers become stuck in an uninterruptible (D-state) process that `SIGKILL` cannot reap; the final `proc.join()`/`proc.wait()` in `_close` is now bounded by a timeout and the unkillable PID is logged ([#185414](https://github.com/pytorch/pytorch/pull/185414))
- Fix pipelining producing incorrect results or cryptic runtime errors when a `PipelineScheduleMulti` topology communicates between non-adjacent stages (e.g. skip connections); this is now detected at initialization and raises a clear `RuntimeError` ([#179293](https://github.com/pytorch/pytorch/pull/179293))
- Fix `RuntimeError: only Tensors of floating point dtype can require gradients` when building a pipeline for models with non-float intermediates (such as Hugging Face transformer models) ([#183582](https://github.com/pytorch/pytorch/pull/183582))
- Make `LocalTensorMode` transparent to `torch.compile` so compilation proceeds as if the debugging mode were not active ([#182667](https://github.com/pytorch/pytorch/pull/182667))
- Fix `AssertionError` in elastic `c10d` rendezvous when a node's rank changes across rendezvous rounds (e.g. a node becomes rank 0 after a peer leaves) ([#182375](https://github.com/pytorch/pytorch/pull/182375))
- Fix shared-weight gradient double-counting in zero-bubble pipeline schedules ([#181365](https://github.com/pytorch/pytorch/pull/181365))
- Fix `None` gradient handling in pipeline backward send/recv ([#182182](https://github.com/pytorch/pytorch/pull/182182))
- Fix a pipelining crash when `split_module` interleaves `get_attr` nodes with placeholder nodes ([#182644](https://github.com/pytorch/pytorch/pull/182644))

## Distributed Checkpointing

- Fix optimizer state-dict save/load using the wrong process group for FSDP models initialized with a non-default process group, by forwarding the FSDP process group to `FSDP.optim_state_dict` and `FSDP.optim_state_dict_to_load` ([#181261](https://github.com/pytorch/pytorch/pull/181261))
- Fix `DefaultStager` crash when reused ([#183424](https://github.com/pytorch/pytorch/pull/183424))

## DTensor

- Fix Context Parallel load balancing for short sequences that cannot be split into the required head/tail chunks, falling back to regular CP sharding for correctness ([#183968](https://github.com/pytorch/pytorch/pull/183968))
- Fix `squeeze` leaving a DTensor's spec and local tensor out of sync (spec shape not matching the local tensor) by preventing `squeeze` from redistributing when `strict_view` is set ([#175798](https://github.com/pytorch/pytorch/pull/175798))
- Fix `.view()` failures (e.g. in `ColwiseParallel`/`RowwiseParallel`) after an uneven `Shard(dim>0)`->`Replicate` redistribute by making the local tensor contiguous ([#184443](https://github.com/pytorch/pytorch/pull/184443))
- Fix a device-side assert crash when tracing tensor-parallel models with `make_fx`, caused by sharding propagation recording dead global-shape shadow nodes into the graph ([#185865](https://github.com/pytorch/pytorch/pull/185865))
- Avoid the native sharding cache for symbolic IValue arguments, fixing stale cached output shardings that confused global and local shard shapes for shape-sensitive ops under compiled autograd ([#183246](https://github.com/pytorch/pytorch/pull/183246))
- Fix `upsample` backward crashes when the input is sharded ([#182595](https://github.com/pytorch/pytorch/pull/182595))
- Fix `Partial` placement being lost during the autograd layout invariant ([#180511](https://github.com/pytorch/pytorch/pull/180511))
- Fix `OpSpec.mesh` crash when specs contain `None` entries ([#181541](https://github.com/pytorch/pytorch/pull/181541))
- Fix `redistribute(backward_dtype=...)` ignoring the backward dtype ([#182032](https://github.com/pytorch/pytorch/pull/182032))
- Fix `_StridedShard` flag conflict during gradient accumulation ([#183517](https://github.com/pytorch/pytorch/pull/183517))
- Fix reduction strategy linearity ([#183794](https://github.com/pytorch/pytorch/pull/183794))
- Fix the cache key hashing for fake meshes ([#184001](https://github.com/pytorch/pytorch/pull/184001))
- Fix `FakeTensor` device hint in sharding propagation ([#183970](https://github.com/pytorch/pytorch/pull/183970))
- Fix `group_norm` scalar adjuster crash when `weight=None` ([#184819](https://github.com/pytorch/pytorch/pull/184819))
- Fix `to_local()` dropping the `_is_param` marker that `nn.Parameter` sets on custom tensors ([#184422](https://github.com/pytorch/pytorch/pull/184422))
- Fix `pad_tensor`/`unpad_tensor` creating unnecessary guards on symbolic pad sizes during tracing ([#180887](https://github.com/pytorch/pytorch/pull/180887))
- Fix DTensor + activation checkpointing + `torch.compile` crash caused by an unbound inner symbol at the root tracer ([#181797](https://github.com/pytorch/pytorch/pull/181797))
- Fix a `DTensorSpec` refcount leak in `OpSchema._recompute_comparison_key` ([#181792](https://github.com/pytorch/pytorch/pull/181792))

## Distributed FSDP2

- Fix stale `post_accumulate_grad_hook` results under `CPUOffloadPolicy` ([#180666](https://github.com/pytorch/pytorch/pull/180666))
- Fix reduce-scatter of unused DTensor parameters that previously raised a mixed `Tensor`/`DTensor` error in `chunk_cat` ([#183040](https://github.com/pytorch/pytorch/pull/183040))
- Fix `IndexError` for modules called with no forward inputs by preserving empty args/kwargs, matching FSDP1 behavior ([#183943](https://github.com/pytorch/pytorch/pull/183943))
- Remove redundant stream waits ([#183983](https://github.com/pytorch/pytorch/pull/183983))
- Fix a tensor-parallel + FSDP2 + mixed-precision bug where the unsharded compute tensor was wrapped back into a `DTensor` with a stale fp32 dtype, causing sharding propagation to fail in eager and `torch.compile` ([#183805](https://github.com/pytorch/pytorch/pull/183805))
- Fix incorrectly reduced gradients when running a partial forward of a `fully_shard([norm, head])` group for chunked loss, where the model forward runs `norm` only and `head` is called standalone per chunk; unshard/reshard previously relied on `_modules_to_run_forward` and produced wrong results for this pattern ([#180428](https://github.com/pytorch/pytorch/pull/180428))
- Add a warning when a grad-requiring forward output is a view tensor, since in-place ops on the view silently drop the pre-backward hook and cause backward to skip the all-gather and fail ([#181850](https://github.com/pytorch/pytorch/pull/181850))
- Fix incorrect `clip_grad_norm` results with multiple data-parallel shard axes (e.g. `dp_shard` + `cp` passed via `DataParallelMeshDims`), which exposed separate `Shard` axes with the wrong float32 reduction order and an incorrect `Shard` instead of `_StridedShard`; the axes are now flattened into a single shard axis in the sharding spec ([#183629](https://github.com/pytorch/pytorch/pull/183629))
- Fix recomputed tensor metadata diverging from the original forward under activation checkpointing when `cast_forward_inputs` is enabled, by casting forward inputs during recompute ([#182580](https://github.com/pytorch/pytorch/pull/182580))
- Fix incorrect resharding of full-DTensor parameters when tensor parallelism is also applied by using `_StridedShard` ([#186126](https://github.com/pytorch/pytorch/pull/186126))

## Linear Algebra Frontend

- Validate pivot range in `torch.linalg.ldl_solve` CPU kernel ([#181032](https://github.com/pytorch/pytorch/pull/181032))
- Fix rocBLAS tunable GEMM solution handling in TunableOp ([#182380](https://github.com/pytorch/pytorch/pull/182380))
- Route fp16 backward GEMMs to rocBLAS to preserve subnormals ([#183766](https://github.com/pytorch/pytorch/pull/183766))
- Make collective bucketing tolerate hinted unbacked SymInts ([#183544](https://github.com/pytorch/pytorch/pull/183544))

## Profiler

- Fix an issue where profiler would issue a "Profiler clears events at the end of each cycle" warning even when no cycles are used in the schedule ([#180387](https://github.com/pytorch/pytorch/pull/180387))
- Ensure that Profiler does not keep driving Kineto transitions even when GPU collection has stopped ([#180698](https://github.com/pytorch/pytorch/pull/180698))

## FX

- Preserve user runtime asserts in FX pass ([#184608](https://github.com/pytorch/pytorch/pull/184608))

## Dynamo

- Fix Python container and operator semantics in Dynamo to match CPython: list ([#185425](https://github.com/pytorch/pytorch/pull/185425)) and tuple ([#185427](https://github.com/pytorch/pytorch/pull/185427)) constructors, `dict` update ([#185428](https://github.com/pytorch/pytorch/pull/185428)), `defaultdict` inplace union ([#185429](https://github.com/pytorch/pytorch/pull/185429)), `frozenset` copy identity ([#185430](https://github.com/pytorch/pytorch/pull/185430)), sequence search ([#185431](https://github.com/pytorch/pytorch/pull/185431)), `iand` on bool constants ([#184503](https://github.com/pytorch/pytorch/pull/184503)), `sequence * SymNode` spurious graph break ([#185260](https://github.com/pytorch/pytorch/pull/185260)), and `torch.Size` tensor shape handling ([#184613](https://github.com/pytorch/pytorch/pull/184613))
- Fix symbolic shape / fake tensor handling: `float`/`bool` + `SymNode` ([#183362](https://github.com/pytorch/pytorch/pull/183362)), `PendingUnbackedSymbolNotFound` for 0-d tensor `Scalar` args ([#182660](https://github.com/pytorch/pytorch/pull/182660)), `GuardOnDataDependentSymNode` on sparse tensors ([#179616](https://github.com/pytorch/pytorch/pull/179616)), and creating symbolic tensors from foreign fake tensors ([#181794](https://github.com/pytorch/pytorch/pull/181794))
- Fix use-after-free issues in `CUDAStream`/`Event` `tp_dealloc` overrides ([#183403](https://github.com/pytorch/pytorch/pull/183403)) and Dynamo dict guard cleanup ([#183753](https://github.com/pytorch/pytorch/pull/183753))
- Fix Dynamo crash when `DeviceMesh` is constructed inside `torch.compile` ([#177201](https://github.com/pytorch/pytorch/pull/177201))
- Fix `torch.compile` crash when an unsupported type is passed to a tensor method inside try/except ([#182106](https://github.com/pytorch/pytorch/pull/182106))
- Skip `wrap_inline` for exec'd Python functions ([#181531](https://github.com/pytorch/pytorch/pull/181531))
- Fix tensor subclass construction under `torch.compile` ([#183337](https://github.com/pytorch/pytorch/pull/183337))
- Preserve eager `torch.full` validation for `nn.Parameter` fill values in Dynamo ([#183915](https://github.com/pytorch/pytorch/pull/183915))
- Prevent accuracy minifier repro recursion ([#184077](https://github.com/pytorch/pytorch/pull/184077))
- Fix AOT export with flex attention `BlockMask` placeholders ([#184611](https://github.com/pytorch/pytorch/pull/184611))
- Accept extra kwargs in `CudagraphsBackend.__call__` ([#182989](https://github.com/pytorch/pytorch/pull/182989))
- Avoid `def forward(self, ..., self, ...)` SyntaxError in `dynamo_graph_capture_for_export` ([#185314](https://github.com/pytorch/pytorch/pull/185314))
- Fix scoped Chromium event reset ([#184973](https://github.com/pytorch/pytorch/pull/184973))
- Fix Dynamo binding of overridden function defaults ([#184852](https://github.com/pytorch/pytorch/pull/184852))
- Fix SAC `context_fn` clobbered by DDPOptimizer's `propagate_metadata` ([#179496](https://github.com/pytorch/pytorch/pull/179496))
- Clear retained fake tensor CUDA constants ([#184445](https://github.com/pytorch/pytorch/pull/184445))
- Fix Dynamo `.grad` reads for new in-graph parameters ([#184972](https://github.com/pytorch/pytorch/pull/184972))
- Graph break on CUDA `manual_seed` in Dynamo so compiled random calls stay reproducible ([#185761](https://github.com/pytorch/pytorch/pull/185761))
- Fix functional tensor `to_dense` no-op ([#184586](https://github.com/pytorch/pytorch/pull/184586))
- Preserve original tensor strides across activation offload/reload ([#186396](https://github.com/pytorch/pytorch/pull/186396))
- Graph break on duplicate autograd Function inputs ([#184281](https://github.com/pytorch/pytorch/pull/184281))
- Raise `IndexError` in compile mode matching eager mode ([#184856](https://github.com/pytorch/pytorch/pull/184856))
- Don't error on a skipped frame when `fullgraph=True` and a non-default stance is set ([#183623](https://github.com/pytorch/pytorch/pull/183623))
- Set the `is_compiling` flag for the whole `torch.compile` session ([#184614](https://github.com/pytorch/pytorch/pull/184614))
- Fix FxGraphCache pickling of opaque types with cyclic references ([#180422](https://github.com/pytorch/pytorch/pull/180422))
- Handle missing Windows C++ compiler in shape guard fallback ([#185447](https://github.com/pytorch/pytorch/pull/185447))

## Inductor

- Fix `max_autotune` BMM correctness with dynamic OpenMP threads ([#169128](https://github.com/pytorch/pytorch/pull/169128))
- Fix NaN output in CPU `LayerNorm` by guarding the Welford variance computation ([#173989](https://github.com/pytorch/pytorch/pull/173989))
- Fix `NameError` from Python name mangling for user-defined Triton kernels whose names start with double underscores ([#176100](https://github.com/pytorch/pytorch/pull/176100))
- Fix backward-pass shape mismatch in mix-order reduction for compiled models ([#178098](https://github.com/pytorch/pytorch/pull/178098))
- Do not apply `pointer_range_32` to user-defined Triton kernels on ROCm to avoid compilation crashes ([#178541](https://github.com/pytorch/pytorch/pull/178541))
- Fix the `e8m0_rceil_log2` pattern failing to register on any CUDA device ([#178698](https://github.com/pytorch/pytorch/pull/178698))
- Fix `cpp_wrapper` backward compilation failing with a `CudaKernelParamCache` assertion when set via `torch.compile` options ([#178847](https://github.com/pytorch/pytorch/pull/178847))
- Fix `FxGraphCachePickler` crash on unpicklable pybind11 extension types during cache key computation ([#178853](https://github.com/pytorch/pytorch/pull/178853))
- Fix C++ compile error when indexing a transposed tensor with an indirect (tensor) index on the CPU backend ([#178962](https://github.com/pytorch/pytorch/pull/178962))
- Fix TPU Pallas codegen to use subscript indexing for scalar and size-1 buffer accesses ([#179099](https://github.com/pytorch/pytorch/pull/179099))
- Fix incorrect `argmax`/`argmin` indices in the CPP Tile2D vectorized kernel for transposed inputs ([#179525](https://github.com/pytorch/pytorch/pull/179525))
- Fix user-kernel fusion to use `mutation_outputs` for the intermediate buffer and add epilogue source to the cache key ([#179803](https://github.com/pytorch/pytorch/pull/179803))
- Fix missing mask on `tl.atomic_add` for constant-index stores ([#179833](https://github.com/pytorch/pytorch/pull/179833))
- Add convolution input/weight dtype-mismatch check to match eager semantics ([#179890](https://github.com/pytorch/pytorch/pull/179890))
- Raise a catchable error instead of crashing on integer divide-by-zero for `fmod`/`remainder` on CPU ([#179923](https://github.com/pytorch/pytorch/pull/179923))
- Fix stride mismatch for user-visible reduction nodes caused by `dislike_padding` conflicting with contiguous storage layout ([#180197](https://github.com/pytorch/pytorch/pull/180197))
- Fix `check_bounds` forward-reference C++ compile error in the CPU backend ([#180212](https://github.com/pytorch/pytorch/pull/180212))
- Preserve Triton HIP compile options (`waves_per_eu`, `matrix_instr_nonkdim`, `kpack`) when combo kernels rewrite per-subkernel configs on ROCm ([#180277](https://github.com/pytorch/pytorch/pull/180277))
- Fix `torch.compile` crash on `cumsum` with broadcast input when the scan dimension is 129 or larger ([#180369](https://github.com/pytorch/pytorch/pull/180369))
- Fix AOTInductor `while_loop` codegen for the minimal-arrayref interface (wrap `ArrayRefTensor` inputs before assign) ([#180370](https://github.com/pytorch/pytorch/pull/180370))
- Fix SM100 `addmm` CUTLASS codegen and relax `addmm` tolerances ([#180432](https://github.com/pytorch/pytorch/pull/180432))
- Fix incorrect storage-offset propagation for `as_strided` ([#180581](https://github.com/pytorch/pytorch/pull/180581))
- Filter CUTLASS kernels by fast-accum only on Hopper to avoid `NoValidChoicesError` for `scaled_mm`/`scaled_grouped_mm` with `use_fast_accum=True` on Blackwell ([#180586](https://github.com/pytorch/pytorch/pull/180586))
- Make persistent-reduction config selection batch-invariant under deterministic mode ([#180832](https://github.com/pytorch/pytorch/pull/180832))
- Fix `UnicodeDecodeError` on Windows when using `icx-cl` as the CXX compiler by decoding subprocess output with `errors='replace'` ([#180853](https://github.com/pytorch/pytorch/pull/180853))
- Avoid emitting `tl.float64` in Triton scalar-shape-math codegen on XPU devices without fp64 support (e.g. Intel Arc A770) ([#180854](https://github.com/pytorch/pytorch/pull/180854))
- Fix silent incorrect results when `adaptive_avg_pool2d` is fused with downstream flatten + reduction for non-power-of-2 channel sizes ([#180898](https://github.com/pytorch/pytorch/pull/180898))
- Fix CPU C++ fusion crash on GroupNorm + SDPA + bmm ([#181015](https://github.com/pytorch/pytorch/pull/181015))
- Fix `num_warps` on AMD RDNA (wave32) GPUs so it is no longer incorrectly halved; only CDNA (`warp_size` 64) is halved ([#181112](https://github.com/pytorch/pytorch/pull/181112))
- Fix unsupported `index_expr`/`kindexpr` error when using `flex_attention` with bias/index expressions ([#181207](https://github.com/pytorch/pytorch/pull/181207))
- Fix unbacked-symbol bindings assertion in the `slice` lowering early-return path ([#181219](https://github.com/pytorch/pytorch/pull/181219))
- Preserve program order of random ops in the scheduler to avoid numerical mismatch vs eager when `fallback_random` is enabled ([#181245](https://github.com/pytorch/pytorch/pull/181245))
- Fix Inductor crash (`NotImplementedError: View`) when a `flatten()`-produced view is passed as the `conv2d` bias ([#181363](https://github.com/pytorch/pytorch/pull/181363))
- Include per-device autocast dtype in the AOTAutograd cache key to prevent reusing a graph compiled under one autocast dtype (e.g. `bfloat16`) when running under another (e.g. `float16`) ([#181564](https://github.com/pytorch/pytorch/pull/181564))
- Fix `_to_copy` decomposition so float64->float32 transfers to XPU devices without fp64 support no longer generate illegal fp64 buffers/crash ([#181607](https://github.com/pytorch/pytorch/pull/181607))
- Prevent `AutoHeuristic` initialization from crashing in non-CUDA (e.g. XPU) environments ([#181745](https://github.com/pytorch/pytorch/pull/181745))
- Fix `AttributeError` crash in `remove_noop_ops` when a node's meta val is a `SymInt`/`SymFloat` (auto dynamic shapes) instead of a Tensor ([#181752](https://github.com/pytorch/pytorch/pull/181752))
- Fix `ConcatKernel` channels_last contiguous check to handle symbolic shapes, avoiding a data-dependent (DDE) `LoweringException` ([#181845](https://github.com/pytorch/pytorch/pull/181845))
- Fix user-defined Triton kernel pointer args with no `tl.load`/`tl.store` being incorrectly eliminated (and not allocated) when epilogue fusion is enabled ([#181868](https://github.com/pytorch/pytorch/pull/181868))
- Properly truncate (downcast then upcast) the accumulator for Triton GEMM epilogue fusions so numerics match eager ([#181918](https://github.com/pytorch/pytorch/pull/181918))
- Skip non-tensor IR nodes (e.g. process groups) when realizing/marking mutated buffers in `_CollectiveKernel.create_inplace` ([#181930](https://github.com/pytorch/pytorch/pull/181930))
- Pass the correct device to `print_performance` in generated `benchmark_compiled_module` so timing works on non-CUDA devices (e.g. XPU) ([#181957](https://github.com/pytorch/pytorch/pull/181957))
- Serialize `CompiledFxGraph._original_gm` via `GraphPickler` to fix AOTAutograd/precompile cache serialization crashes for graphs with HOPs that have lifted buffers (e.g. `flex_attention` with a causal `BlockMask`) ([#182088](https://github.com/pytorch/pytorch/pull/182088))
- Avoid raw stream name collisions in generated Inductor code ([#182139](https://github.com/pytorch/pytorch/pull/182139))
- Disable the overlap-scheduling SPMD check by default to avoid an NCCL hang when ranks diverge on cache hit vs miss ([#182281](https://github.com/pytorch/pytorch/pull/182281))
- Fix CUDA graphs to support self-overlapping inputs and unbacked shapes via a storage-copy fallback instead of erroring on complex memory overlap ([#182524](https://github.com/pytorch/pytorch/pull/182524))
- Pass derived sym-int captures through `maybe_realize` in FlexAttention ([#182610](https://github.com/pytorch/pytorch/pull/182610))
- Fix `AutoHeuristic` crash in non-CUDA environments (e.g. XPU and CPU-only builds) ([#182614](https://github.com/pytorch/pytorch/pull/182614))
- Do not automatically move non-deterministic seed functions to GPU ([#182748](https://github.com/pytorch/pytorch/pull/182748))
- Fix `emulate_precision_casts` on CPU C++ codegen so explicit/emulated fp32->fp16->fp32 precision barriers are no longer optimized away ([#182882](https://github.com/pytorch/pytorch/pull/182882))
- Fix block-descriptor final shape expansion for discontiguous fused pointwise/reduction loads and stores ([#182936](https://github.com/pytorch/pytorch/pull/182936))
- Fix crash in FLOP counting (`count_flops_fx`) for `HigherOrderOperator` targets such as `flex_attention` during overlap/bucketing ([#182992](https://github.com/pytorch/pytorch/pull/182992))
- Raise device-mismatch errors for `index_add`/`index_copy`/`index_reduce` instead of silently succeeding under `torch.compile` ([#183007](https://github.com/pytorch/pytorch/pull/183007))
- Fix Triton `eager_input_vals` propagation ([#183334](https://github.com/pytorch/pytorch/pull/183334))
- Escape backslashes in user-defined Triton kernel source ([#183421](https://github.com/pytorch/pytorch/pull/183421))
- Fix TMA config lowering block sizes below the heuristic choice, which could trigger an illegal memory access on large tensors ([#183438](https://github.com/pytorch/pytorch/pull/183438))
- Fix CPU AOTInductor with user-defined Triton kernels when compile-time autotuning is disabled ([#183463](https://github.com/pytorch/pytorch/pull/183463))
- Fix `is_linear_add_bias` crash when the bias node argument is a Python float ([#183514](https://github.com/pytorch/pytorch/pull/183514))
- Fix convolution lowering and backward decomposition crash when a channel dimension is zero ([#183539](https://github.com/pytorch/pytorch/pull/183539))
- Fix Inductor embedding negative index checks ([#183636](https://github.com/pytorch/pytorch/pull/183636))
- Disable cudagraphs for input storage mutation ([#183645](https://github.com/pytorch/pytorch/pull/183645))
- Fix `torch.compile` crash on `cumprod` backward by disallowing fusion of split-scan nodes with reductions ([#183653](https://github.com/pytorch/pytorch/pull/183653))
- Fix CPU `argmax` logical index for transposed reductions ([#183655](https://github.com/pytorch/pytorch/pull/183655))
- Fix `while_loop` backward expanded gradient strides ([#183658](https://github.com/pytorch/pytorch/pull/183658))
- Fix the SDPA backward constraint for scalar gradient bases ([#183662](https://github.com/pytorch/pytorch/pull/183662))
- Fix Inductor multi-stream codegen on XPU to emit `torch.xpu` stream APIs instead of CUDA-only calls ([#183693](https://github.com/pytorch/pytorch/pull/183693))
- Fix BF16 Inductor failure on Neoverse V3 with GCC 12.4 ([#183698](https://github.com/pytorch/pytorch/pull/183698))
- Fix the tail reduction suffix width ([#183699](https://github.com/pytorch/pytorch/pull/183699))
- Support unused lifted `SymInt`s in `associative_scan` lowering ([#183706](https://github.com/pytorch/pytorch/pull/183706))
- Guard the fast Triton launcher to CUDA/HIP so XPU correctly falls back to the static launcher ([#183707](https://github.com/pytorch/pytorch/pull/183707))
- Fix CPU C++ codegen crash from misaligned loop-split groups after fusion ([#183715](https://github.com/pytorch/pytorch/pull/183715))
- Fix `set_.source_Tensor` lowering when the source is a view ([#183724](https://github.com/pytorch/pytorch/pull/183724))
- Fix CPU GEMM k-slicing cache-block indexing ([#183733](https://github.com/pytorch/pytorch/pull/183733))
- Skip cudagraph capture when the CUDA caching allocator is bypassed ([#183780](https://github.com/pytorch/pytorch/pull/183780))
- Fix bytes-vs-elements mismatch in `select_algorithm` input storage check ([#183791](https://github.com/pytorch/pytorch/pull/183791))
- Use libdevice `log` for strict Inductor numerics ([#183844](https://github.com/pytorch/pytorch/pull/183844))
- Add meta registration and dtype check for `div_` to match eager type-promotion semantics ([#183859](https://github.com/pytorch/pytorch/pull/183859))
- Fix `handle_synced_deallocation` for XPU ([#183865](https://github.com/pytorch/pytorch/pull/183865))
- Use `hipModuleLoadData` in `StaticCudaLauncher` on ROCm ([#183926](https://github.com/pytorch/pytorch/pull/183926))
- Fix `flex_attention` autotune logging to use size hints for symbolic dims, avoiding lowering failures under dynamic shapes ([#183933](https://github.com/pytorch/pytorch/pull/183933))
- Guard the SM100 E8M0 FP8 PTX lowering to NVIDIA so ROCm gfx11 uses the portable bit-manipulation fallback ([#183949](https://github.com/pytorch/pytorch/pull/183949))
- Enable the Python dispatcher when re-running fake propagation for fallback kernels so custom/backend fake implementations supply correct output layout metadata ([#183961](https://github.com/pytorch/pytorch/pull/183961))
- Fix a crash in `tuned_addmm` with max-autotune when the bias is an unrealized view (e.g. a transposed expression) ([#183973](https://github.com/pytorch/pytorch/pull/183973))
- Compute `gelu` backward in opmath dtype for improved numerical accuracy ([#183985](https://github.com/pytorch/pytorch/pull/183985))
- Cap Triton convolution warps for non-1x1 kernels to avoid miscompilation ([#183989](https://github.com/pytorch/pytorch/pull/183989))
- Fix graph partition signatures to only drop buffers removed during that partition's codegen, preserving globally-removed buffers still needed by later partitions ([#184004](https://github.com/pytorch/pytorch/pull/184004))
- Handle `float8_e4m3fn` dequantization on pre-sm89 CUDA devices to match eager bit patterns ([#184008](https://github.com/pytorch/pytorch/pull/184008))
- Fix the native matmul config numel cap ([#184011](https://github.com/pytorch/pytorch/pull/184011))
- Use CUDA libdevice for emulate-precision casts to match eager numerics ([#184022](https://github.com/pytorch/pytorch/pull/184022))
- Fix Inductor compile-worker shutdown so the sidecar's nested worker pool is terminated and shutdown no longer hangs until the parent wait timeout ([#184038](https://github.com/pytorch/pytorch/pull/184038))
- Fix `bucketize`/`searchsorted` on sliced or zero-stride lookup tensors ([#184043](https://github.com/pytorch/pytorch/pull/184043))
- Fix scaled softmax non-finite semantics ([#184046](https://github.com/pytorch/pytorch/pull/184046))
- Fix CPU FlexAttention aliased input lowering ([#184071](https://github.com/pytorch/pytorch/pull/184071))
- Rewrite Triton floating-point self-subtraction to produce exact zero ([#184093](https://github.com/pytorch/pytorch/pull/184093))
- Treat corrupt local autotune cache entries (bad JSON/invalid UTF-8) as cache misses instead of crashing compilation ([#184096](https://github.com/pytorch/pytorch/pull/184096))
- Recurse through list/tuple arguments when applying `needs_fixed_stride_order` so fallback custom ops receive tensor-list inputs in the recorded stride order ([#184098](https://github.com/pytorch/pytorch/pull/184098))
- Fix CPU Inductor vectorized `asinh` overflow ([#184105](https://github.com/pytorch/pytorch/pull/184105))
- Treat low-precision saved-for-backward activations as precision barriers so forward math observes the same truncated value backward will load ([#184110](https://github.com/pytorch/pytorch/pull/184110))
- Fix int to float8 casts in Inductor Triton codegen ([#184115](https://github.com/pytorch/pytorch/pull/184115))
- Fix Inductor random fallback for `RReLU` ([#184136](https://github.com/pytorch/pytorch/pull/184136))
- Fix scalar tensor lowering for `torch.jagged` layout to match eager and meta behavior ([#184146](https://github.com/pytorch/pytorch/pull/184146))
- Preserve `out_dtype` for `scaled_mm` by propagating it to `MMKernelInputs` ([#184168](https://github.com/pytorch/pytorch/pull/184168))
- Fix Inductor CUDA `frexp` exponent for non-finite inputs ([#184176](https://github.com/pytorch/pytorch/pull/184176))
- Fix Inductor cache directory fallback for unmapped users ([#184208](https://github.com/pytorch/pytorch/pull/184208))
- Guard dilation in `convolution_backward` lowering so dilated `conv2d` backward compiles under dynamic shapes ([#184224](https://github.com/pytorch/pytorch/pull/184224))
- Force persistent reduction for `sort` in combo kernels ([#184227](https://github.com/pytorch/pytorch/pull/184227))
- Fix `as_strided` storage offsets for graph input views ([#184232](https://github.com/pytorch/pytorch/pull/184232))
- Guard dilation to ints in `convolution_backward` lowering so the Triton backward conv template no longer references undefined sympy symbols under dynamic shapes ([#184255](https://github.com/pytorch/pytorch/pull/184255))
- Fix reinplacing through view `index_put` ([#184263](https://github.com/pytorch/pytorch/pull/184263))
- Skip CUDA graphs for `aten.topk` on ROCm/HIP to avoid a rocPRIM memory fault on cudagraph-tree replays (MI350 / ROCm 7) ([#184265](https://github.com/pytorch/pytorch/pull/184265))
- Fix module-table exhaustion during long exhaustive autotuning ([#184285](https://github.com/pytorch/pytorch/pull/184285))
- Fix Inductor `gather` bounds for negative indices ([#184287](https://github.com/pytorch/pytorch/pull/184287))
- Fix CUDA graph trees when used from Python-created threads ([#184357](https://github.com/pytorch/pytorch/pull/184357))
- Fix Inductor compile pools hanging when running inside daemonic multiprocessing workers ([#184472](https://github.com/pytorch/pytorch/pull/184472))
- Fix deterministic selection to correctly detect bound extern (`ExternKernelCaller`) choices ([#184493](https://github.com/pytorch/pytorch/pull/184493))
- Fix CPU integer floor-division overflow so `INT_MIN / -1` matches eager instead of trapping ([#184497](https://github.com/pytorch/pytorch/pull/184497))
- Include default dtype in the Inductor FX cache key ([#184500](https://github.com/pytorch/pytorch/pull/184500))
- Fix Triton compilation failure for scan/cumulative reductions (`cumsum`/`cummax`/`cummin`/`cumprod`) on unsigned integer dtypes ([#184514](https://github.com/pytorch/pytorch/pull/184514))
- Fix Inductor fallback aliasing for boxed scalars ([#184516](https://github.com/pytorch/pytorch/pull/184516))
- Extend convolution input/weight dtype-mismatch checks to all devices ([#184518](https://github.com/pytorch/pytorch/pull/184518))
- Fall back to the standard lowering path for CUDA FP8 dtypes that Triton cannot compile for the active target ([#184521](https://github.com/pytorch/pytorch/pull/184521))
- Check `constant_offset` alignment in `TMACompatibilityChecker` ([#184564](https://github.com/pytorch/pytorch/pull/184564))
- Fix `acc_type` for fp8 dtypes in mm autotuning (use `triton_type` and accumulate in fp32) ([#184591](https://github.com/pytorch/pytorch/pull/184591))
- Fix `torch.cond` subgraph buffer reuse by scoping `EfficientPeakEstimate` per subgraph during AOT codegen ([#184623](https://github.com/pytorch/pytorch/pull/184623))
- Fix backward (gradient) support for `addcmul_` and `addcdiv_` under `torch.compile` ([#184629](https://github.com/pytorch/pytorch/pull/184629))
- Fix Inductor loop indexing expression canonicalization ([#184650](https://github.com/pytorch/pytorch/pull/184650))
- Fix `ZeroTensor` view with symbolic sizes ([#184651](https://github.com/pytorch/pytorch/pull/184651))
- Fix invalid assert-message concatenation in CPU `cpp_micro_gemm` that broke AOTI compilation of AVX512 VNNI/WoQ-Int4 kernels ([#184693](https://github.com/pytorch/pytorch/pull/184693))
- Refuse TMA for known-unaligned buffers and fall back to regular loads/stores ([#184717](https://github.com/pytorch/pytorch/pull/184717))
- Record IR reads nested inside `constant_args` and kwargs in `ExternKernel.get_read_writes()` to prevent index producers from being incorrectly eliminated ([#184751](https://github.com/pytorch/pytorch/pull/184751))
- Map float8 types correctly between torch and Triton for Triton template ops to unblock fp8 max-autotune ([#184806](https://github.com/pytorch/pytorch/pull/184806))
- Fix `Py_None` reference counting in the C++ wrapper ([#184869](https://github.com/pytorch/pytorch/pull/184869))
- Emit embedded Triton code and cubin files when loading saved cache artifacts so kernels are not needlessly recompiled ([#184953](https://github.com/pytorch/pytorch/pull/184953))
- Fix Inductor subprocess compile pool leaking named semaphore resources when `torch.compile` runs inside a multiprocessing child process ([#185070](https://github.com/pytorch/pytorch/pull/185070))
- Fix TorchInductor CPU codegen crash during vectorization tiling when an index expression contains relational sub-expressions (e.g. `torch.compile(dynamic=True)` with `torch.func.grad`) ([#185080](https://github.com/pytorch/pytorch/pull/185080))
- Skip TMA codegen for dtypes lacking a tensor-map enum entry instead of crashing at runtime ([#185223](https://github.com/pytorch/pytorch/pull/185223))
- Synchronize non-blocking device-to-host copies before a CPU read to avoid a race condition ([#185252](https://github.com/pytorch/pytorch/pull/185252))
- Fix AOTInductor C++ codegen most-vexing-parse failure when a cached output is initialized from a constructor-call expression ([#185257](https://github.com/pytorch/pytorch/pull/185257))
- Fix CuTeDSL grouped GEMM 'Invalid leading dimension' failure by using `get_stride_order` for assorted A/B layouts ([#185437](https://github.com/pytorch/pytorch/pull/185437))
- Fix a `NameError` in combo kernels when TMA is enabled by handling `DelayReplaceLine` load expressions ([#185514](https://github.com/pytorch/pytorch/pull/185514))
- Make MSVC compiler detection on Windows robust against non-zero exit codes and empty output to avoid crashes ([#185523](https://github.com/pytorch/pytorch/pull/185523))
- Fix a `cat` lowering assertion error with 1-D statically-empty tensors ([#185549](https://github.com/pytorch/pytorch/pull/185549))
- Accept interpreted Triton kernels in `wrap_triton` when `TRITON_INTERPRET=1` is set ([#185597](https://github.com/pytorch/pytorch/pull/185597))
- Fix `wait_stream` reordering by registering it among the synchronization ops that preserve control dependencies ([#185627](https://github.com/pytorch/pytorch/pull/185627))
- Fix `standalone_compile` cache artifact save for grad-enabled graphs whose backward is lowered lazily ([#185635](https://github.com/pytorch/pytorch/pull/185635))
- Preserve explicit lowp-fp (fp16/bf16) round-trip rounding on CPU under `emulate_precision_casts` to match eager ([#185847](https://github.com/pytorch/pytorch/pull/185847))
- Separate value-producing symbolic expressions from indexing so codegen uses the correct dtype width (e.g. int64 `arange`) in tensor value computation ([#185853](https://github.com/pytorch/pytorch/pull/185853))
- Gate the narrowing-cast bias-add unfuse on XPU to fix an accuracy regression on ROCm ([#185856](https://github.com/pytorch/pytorch/pull/185856))
- Apply a layout constraint to the `view.dtype` lowering when falling back ([#185879](https://github.com/pytorch/pytorch/pull/185879))
- Fix pickling of custom decomposition tables that broke FX graph caching ([#185909](https://github.com/pytorch/pytorch/pull/185909))
- Fix `FakeTensorUpdater` handling of higher-order ops and their subgraphs ([#185962](https://github.com/pytorch/pytorch/pull/185962))
- Implement `get_stride` for `PermuteView` to avoid a `NotImplementedError` ([#185992](https://github.com/pytorch/pytorch/pull/185992))
- Preserve NaNs for CPU libm calls by avoiding fast-math rewrites in generated C++ ([#186018](https://github.com/pytorch/pytorch/pull/186018))
- Fix Inductor crash when logging compute estimations that are `SymFloat` under dynamic shapes in overlap scheduling ([#186054](https://github.com/pytorch/pytorch/pull/186054))
- Fix fake dtype inference for weighted `torch.bincount` so downstream codegen uses the correct dtype ([#186077](https://github.com/pytorch/pytorch/pull/186077))
- Preserve tensor dtype in the `scatter_upon_const_tensor` rewrite for low-precision const tensors ([#186481](https://github.com/pytorch/pytorch/pull/186481))
- Fix Inductor Triton compile/runtime crash from codegen emitting `tl.broadcast_to(False, ...)` by using `tl.full` instead ([#186621](https://github.com/pytorch/pytorch/pull/186621))
- Fix `diagonal_scatter` backward under `torch.compile` ([#185146](https://github.com/pytorch/pytorch/pull/185146))
- Fix a `SymInt` crash in the overlap scheduler's collective/compute node benchmarking ([#186065](https://github.com/pytorch/pytorch/pull/186065))
- Allow generator placeholders through control deps ([#183863](https://github.com/pytorch/pytorch/pull/183863))
- Fix `torch.cat` axis handling in Inductor pre-grad fusion ([#183995](https://github.com/pytorch/pytorch/pull/183995))
- Fix stale backed-symbol references in AOTI deferred runtime asserts ([#184624](https://github.com/pytorch/pytorch/pull/184624))
- Fix AOT FXIR parallel Triton kernel reload ([#185134](https://github.com/pytorch/pytorch/pull/185134))
- Fix `fp32`->`bf16`->`fp32` casts being dropped ([#180575](https://github.com/pytorch/pytorch/pull/180575))
- Fix CUDA `atan` numerics in Inductor ([#183984](https://github.com/pytorch/pytorch/pull/183984))
- Fix `flip` on 0-d tensors in the `prims.rev` lowering ([#184104](https://github.com/pytorch/pytorch/pull/184104))
- Fix the `softmax` decomposition for symbolic empty dims ([#184454](https://github.com/pytorch/pytorch/pull/184454))

## Ahead-Of-Time Inductor (AOTI)

- Fix undefined identifier error in `CppWrapper` due to false-positive caching ([#178147](https://github.com/pytorch/pytorch/pull/178147))
- Scale lazy TMA scratch by grid in `cpp_wrapper` ([#182825](https://github.com/pytorch/pytorch/pull/182825))
- Fix folded constant offset indexing in AOTI constant buffer update ([#179225](https://github.com/pytorch/pytorch/pull/179225))
- Add GPU stream synchronization after constant folding in AOTI ([#181945](https://github.com/pytorch/pytorch/pull/181945))
- Fix use-after-free in `pointer_to_optional_list` ([#183764](https://github.com/pytorch/pytorch/pull/183764))
- Fix Windows AOTI self-mmap size seek ([#186386](https://github.com/pytorch/pytorch/pull/186386))
- Promote scalar literals to tensors for AOTI eager compilation ([#185313](https://github.com/pytorch/pytorch/pull/185313))
- Use `c10::make_scope_exit` to avoid exception leaks ([#184520](https://github.com/pytorch/pytorch/pull/184520))
- Fix deadlock in `AOTInductorModelContainer::run()` during concurrent constant folding ([#181941](https://github.com/pytorch/pytorch/pull/181941))
- Track and unload `CUmodule` handles to prevent GPU code object leaks ([#184860](https://github.com/pytorch/pytorch/pull/184860))
- Fix MSVC const pointer emission in `cpp_wrapper` temporary arrays ([#179846](https://github.com/pytorch/pytorch/pull/179846))
- Fix MSVC path append in kernel context stack compression ([#179857](https://github.com/pytorch/pytorch/pull/179857))
- Add explicit headers for `cpp_wrapper` to fix MSVC compilation ([#180120](https://github.com/pytorch/pytorch/pull/180120))
- Fix inductor AOTI codegen for `float('inf')`/`float('-inf')` kernel args ([#180297](https://github.com/pytorch/pytorch/pull/180297))
- Fix `cond` subgraph arrayref dispatch with generic lambda ([#180558](https://github.com/pytorch/pytorch/pull/180558))
- Fix arrayref proxy executor tensor args ([#182751](https://github.com/pytorch/pytorch/pull/182751))
- Defer Triton compile kickoff out of static init ([#182824](https://github.com/pytorch/pytorch/pull/182824))
- Fix `cpp_wrapper` while loop carried mutations ([#183657](https://github.com/pytorch/pytorch/pull/183657))
- Fix AOTI CUDA device copy allocation ([#185634](https://github.com/pytorch/pytorch/pull/185634))
- Resolve relative `TORCHINDUCTOR_CACHE_DIR` ([#185723](https://github.com/pytorch/pytorch/pull/185723))

## Export

- Fix NaN float scalar input handling in export guard codegen and input constraint checks ([#180399](https://github.com/pytorch/pytorch/pull/180399))
- Fix `IndexError` during decomposition by also excluding lifted tensor constants and custom objects when identifying user-input placeholders ([#181179](https://github.com/pytorch/pytorch/pull/181179))
- Fix serialization of predispatch wrapper functions (JVP, vmap) in `torch.export` save/load ([#181263](https://github.com/pytorch/pytorch/pull/181263))
- Fix Triton HOP argument packing to preserve kernel argument metadata ([#182101](https://github.com/pytorch/pytorch/pull/182101))
- Simplify `Min`/`Max` of scaled symbolic terms (e.g. `Min(128*s, 512*s)` reduces to `128*s`) so export no longer rejects valid branch guards ([#185092](https://github.com/pytorch/pytorch/pull/185092))
- Clean up the buffer-registration hook on non-strict export trace failures to avoid a stray `AssertionError` on later eager buffer assignment ([#184956](https://github.com/pytorch/pytorch/pull/184956))
- Fix export dynamic shapes for sparse COO inputs ([#184993](https://github.com/pytorch/pytorch/pull/184993))
- Handle scalar tensor slice bounds in non-strict export ([#184925](https://github.com/pytorch/pytorch/pull/184925))
- Fix `torch.export.load` GIL contention during tensor deserialization ([#175983](https://github.com/pytorch/pytorch/pull/175983))

## AOTAutograd

- Fix `torch.compile` crash with batched matmul in `inference_mode` ([#181913](https://github.com/pytorch/pytorch/pull/181913))
- Fix expanded output tangent stride handling ([#184519](https://github.com/pytorch/pytorch/pull/184519))
- Fix AOT synthetic-base out view returns ([#185029](https://github.com/pytorch/pytorch/pull/185029))
- Preserve linalg error checks in AOT graphs ([#184111](https://github.com/pytorch/pytorch/pull/184111))

## Composability

- Fix data-dependent errors (unbacked SymInts) in `pixel_shuffle`, `pdist`, and reflection/replication padding ops ([#183814](https://github.com/pytorch/pytorch/pull/183814))
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
- Handle unbacked dims in folded matmul under `FakeTensor` ([#183397](https://github.com/pytorch/pytorch/pull/183397))
- Preserve unbacked batch dims in SDPA tracing under `ProxyTensor` ([#183398](https://github.com/pytorch/pytorch/pull/183398))
- Fix `mix_order_reduction` over-fusion via load count check ([#179494](https://github.com/pytorch/pytorch/pull/179494))
- Fix `torch.compile` crash from `aten.lift` functionalization on an already-functionalized tensor (e.g. `randint` followed by `lift`) ([#185805](https://github.com/pytorch/pytorch/pull/185805))

## Quantization

- Fix a segmentation fault when running fp8 qlinear on x86 CPU without AMX, caused by the qlinear primitive cache ([#184317](https://github.com/pytorch/pytorch/pull/184317))

## Foreach

- Fix `_foreach_sub` under compile ([#184421](https://github.com/pytorch/pytorch/pull/184421))

## ONNX

- Remove incorrect `CastLike` handling logic from `OpRecorder` ([#182197](https://github.com/pytorch/pytorch/pull/182197))
- Fix `_rotary_embedding_23_fake_impl` stride drift for 3D and 4D inputs ([#184854](https://github.com/pytorch/pytorch/pull/184854))
- Fix `invoke_subgraph` export with lifted tensor constants ([#182230](https://github.com/pytorch/pytorch/pull/182230))
- Fix ONNX dynamic-shape RNN capture ([#184872](https://github.com/pytorch/pytorch/pull/184872))
- Fix ONNX type promotion overload selection ([#185005](https://github.com/pytorch/pytorch/pull/185005))

## C++ Frontend

- Fix crash with invalid embedding bag `mode` ([#186428](https://github.com/pytorch/pytorch/pull/186428))

## Build Frontend

- Fix `-Winconsistent-dllimport` warning in `tensor_numpy` and `tensor_new` headers on Windows ([#183703](https://github.com/pytorch/pytorch/pull/183703))
- Fix missing symbol exports for `ValueError`/`NotImplementedError` on Windows ([#175340](https://github.com/pytorch/pytorch/pull/175340))

## CUDA

- Workaround for `nvrtcCompileProgram` changing locale in CUDA < 12.6.2 ([#180569](https://github.com/pytorch/pytorch/pull/180569))
- Zero `total_weight` before accumulating in `nll_loss2d` ([#182082](https://github.com/pytorch/pytorch/pull/182082))
- Fix `dtype` promotion in `max`/`min` kernel ([#181505](https://github.com/pytorch/pytorch/pull/181505))
- Round per-process memory fraction cap to avoid spurious OOM ([#179444](https://github.com/pytorch/pytorch/pull/179444))
- Fix `torch.cuda.ExternalStream(0)` to wrap the NULL stream ([#183258](https://github.com/pytorch/pytorch/pull/183258))
- Fix stream pool collision in conditional graph nodes ([#185836](https://github.com/pytorch/pytorch/pull/185836))
- Preserve internal precision for `native_group_norm` in eager ([#183946](https://github.com/pytorch/pytorch/pull/183946))

## cuDNN

- Don't route to cuDNN SDPA for batch size or head dim > 65536 ([#180718](https://github.com/pytorch/pytorch/pull/180718))

## MPS

- Fix LSTM train/eval error ([#180873](https://github.com/pytorch/pytorch/pull/180873)) and LSTM dropout not being applied correctly ([#185351](https://github.com/pytorch/pytorch/pull/185351))
- Fix `multinomial` SIGSEGV ([#180493](https://github.com/pytorch/pytorch/pull/180493))
- Fix async copy failing ([#181017](https://github.com/pytorch/pytorch/pull/181017))
- Work around a MetalPerformancePrimitives bug for `F.linear` on M5+ ([#181466](https://github.com/pytorch/pytorch/pull/181466))
- Fix sliced sum reduction ([#182688](https://github.com/pytorch/pytorch/pull/182688)) and Metal unary operator behavior on large strided tensors ([#183447](https://github.com/pytorch/pytorch/pull/183447))
- Fix `uint32` offset overflow in scatter/gather kernels for strided views crossing 2^32 elements ([#182054](https://github.com/pytorch/pytorch/pull/182054)) and move `col2im` offset/stride to `long` to avoid overflow corruption ([#185664](https://github.com/pytorch/pytorch/pull/185664))
- Fix NaN handling: `relu` ([#183571](https://github.com/pytorch/pytorch/pull/183571)), `softshrink` ([#183710](https://github.com/pytorch/pytorch/pull/183710)), `hardsigmoid` ([#183939](https://github.com/pytorch/pytorch/pull/183939)), `cholesky` ([#184588](https://github.com/pytorch/pytorch/pull/184588)), and `fast::tanh` overflow ([#186286](https://github.com/pytorch/pytorch/pull/186286)); return NaN for `std`/`var` on empty input ([#184510](https://github.com/pytorch/pytorch/pull/184510))
- Fix `layer_norm_backward` silent correctness bug for frozen inputs ([#183893](https://github.com/pytorch/pytorch/pull/183893))
- Fix Welford reduction codegen with dynamic shapes ([#184206](https://github.com/pytorch/pytorch/pull/184206)), a missing barrier in Welford reductions ([#184328](https://github.com/pytorch/pytorch/pull/184328)), and an Inductor undeclared identifier in multi-pass Welford reductions ([#184502](https://github.com/pytorch/pytorch/pull/184502))
- Fix SDPA vector kernel mask offset for partially broadcast masks ([#184180](https://github.com/pytorch/pytorch/pull/184180)) and additive mask scaling in prefill attention ([#184400](https://github.com/pytorch/pytorch/pull/184400))
- Fix `_amp_foreach_non_finite_check_and_unscale_` zeroing fp16/bf16 grads ([#184286](https://github.com/pytorch/pytorch/pull/184286)) and stop ignoring grad scale and `found_inf` ([#186360](https://github.com/pytorch/pytorch/pull/186360))
- Materialize neg bit in `copy_kernel_mps` ([#184403](https://github.com/pytorch/pytorch/pull/184403))
- Fix `sort` returning out-of-bounds indices for bool/int-max/NaN inputs ([#184620](https://github.com/pytorch/pytorch/pull/184620))
- Fix generator clone ([#185002](https://github.com/pytorch/pytorch/pull/185002))
- Fix `fill_` on byte-dtype views with misaligned storage offset ([#183790](https://github.com/pytorch/pytorch/pull/183790))
- Fix complex exp family on the real axis using `precise::sincos` ([#184749](https://github.com/pytorch/pytorch/pull/184749))
- Make `deviceCount()` consistent with Python to fix `at::manual_seed()` ([#164571](https://github.com/pytorch/pytorch/pull/164571))
- Fix `scale` not being cached ([#184122](https://github.com/pytorch/pytorch/pull/184122))
- Fix attention compilation on nightly ([#186399](https://github.com/pytorch/pytorch/pull/186399))
- Fix the FFT warning ([#183061](https://github.com/pytorch/pytorch/pull/183061))
- Disallow bitwise shifts for bool dtype ([#186558](https://github.com/pytorch/pytorch/pull/186558))
- Fix bucketization speed/correctness ([#185622](https://github.com/pytorch/pytorch/pull/185622))
- Make index copy fast ([#185750](https://github.com/pytorch/pytorch/pull/185750))
- Enable and fix large-tensor tests on MPS ([#182863](https://github.com/pytorch/pytorch/pull/182863))

## ROCm

- Support TheRock wheel distribution in `_find_rocm_home` ([#180723](https://github.com/pytorch/pytorch/pull/180723))

- Fix `warpMergeSortTopK` padding sentinel for integer dtypes ([#182212](https://github.com/pytorch/pytorch/pull/182212))

- Guard `ck_group_gemm` on `USE_ROCM_CK_GEMM` ([#182615](https://github.com/pytorch/pytorch/pull/182615))

- Fix large arange launch ([#182657](https://github.com/pytorch/pytorch/pull/182657))

- Fix `triu`/`tril` for 64-bit indexing for large matrices ([#179717](https://github.com/pytorch/pytorch/pull/179717))

- Drop dead CUDA/ROCm version gates from tests and helpers ([#184879](https://github.com/pytorch/pytorch/pull/184879))

- Fix `LayerNorm` backward kernel for AMD Strix Halo GPUs ([#183864](https://github.com/pytorch/pytorch/pull/183864))

- Decline CuteDSL `scatter_add` on ROCm ([#185678](https://github.com/pytorch/pytorch/pull/185678))

- For HSTU, fix CK flash-attn GQA `seqlen_q==1` garbage output ([#186434](https://github.com/pytorch/pytorch/pull/186434))

- Inductor fixes:
  - Add config flag to disable `pointer_range_32` optimization ([#179604](https://github.com/pytorch/pytorch/pull/179604))
  - Fix `maybe_hipify_code_wrapper` for bare-token inputs ([#183725](https://github.com/pytorch/pytorch/pull/183725))
  - Work around file handle limits in `StaticCudaLauncher` ([#183926](https://github.com/pytorch/pytorch/pull/183926))
  - Preserve combo kernel HIP compile options ([#180277](https://github.com/pytorch/pytorch/pull/180277))
  - `lookup_device_info` is now case-insensitive ([#182284](https://github.com/pytorch/pytorch/pull/182284))

- Windows
  - Fix MIOpen CTC loss crash on Windows ([#179264](https://github.com/pytorch/pytorch/pull/179264))
  - Apply per-config HIP optimization flags via `CMAKE_HIP_FLAGS` ([#183856](https://github.com/pytorch/pytorch/pull/183856))
  - Fix inconsistent `dllimport` ([#183690](https://github.com/pytorch/pytorch/pull/183690), [#183324](https://github.com/pytorch/pytorch/pull/183324), [#183282](https://github.com/pytorch/pytorch/pull/183282), [#183694](https://github.com/pytorch/pytorch/pull/183694))
  - Remove redundant cuSPARSE/hipSPARSE error-string forward declarations ([#180327](https://github.com/pytorch/pytorch/pull/180327))
  - Remove MSVC flags from `CMAKE_HIP_FLAGS` ([#183365](https://github.com/pytorch/pytorch/pull/183365))
  - Don't set `USE_ROCM_CK_SDPA` on Windows ([#183962](https://github.com/pytorch/pytorch/pull/183962))

## XPU

- Avoid generating fp64 Triton code for XPU devices that do not support fp64 ([#180854](https://github.com/pytorch/pytorch/pull/180854))
- Fix stream selection for XPU outputs in `CurrentWorkStream` ([#179140](https://github.com/pytorch/pytorch/pull/179140))
- Fix reflection and replication padding on XPU to preserve eager-mode output memory format ([#184484](https://github.com/pytorch/pytorch/pull/184484))
- Fix `addmm` shape handling and `addmv_out` stride preservation on XPU ([#180985](https://github.com/pytorch/pytorch/pull/180985), [#178498](https://github.com/pytorch/pytorch/pull/178498))
- Fix XPU deallocation handling and `XPUPluggableAllocator` registration ([#183865](https://github.com/pytorch/pytorch/pull/183865), [#179392](https://github.com/pytorch/pytorch/pull/179392))
- Fix numerical instability in `logcumsumexp` with complex inputs on XPU ([#174492](https://github.com/pytorch/pytorch/pull/174492))
- Fix `SyclExtension` Windows builds for oneAPI 2025.3 and later ([#170701](https://github.com/pytorch/pytorch/pull/170701))
- Fix `getGlobalIdxFromDevice(-1)` handling on XPU ([#181361](https://github.com/pytorch/pytorch/pull/181361))

## Benchmark

- Fix import-time device loading in benchmark timer ([#181716](https://github.com/pytorch/pytorch/pull/181716))

## TorchScript

- Fix OOB read in `MemoryReadAdapter::read` ([#181193](https://github.com/pytorch/pytorch/pull/181193))
- Validate tensor sizes/strides/storage_offset in C++ Unpickler ([#183381](https://github.com/pytorch/pytorch/pull/183381))
- Fix integer overflow in Unpickler storage size computation ([#181310](https://github.com/pytorch/pytorch/pull/181310))
- Fix `broadcast_shapes` op missing in selective builds ([#180860](https://github.com/pytorch/pytorch/pull/180860))
- Fix `binary_cross_entropy` SymInt error with dynamic shapes by registering `aten::broadcast_shapes` as a TorchScript builtin ([#180583](https://github.com/pytorch/pytorch/pull/180583))
- Fix use-after-free in symbolic-shape runtime fusion guard ([#183760](https://github.com/pytorch/pytorch/pull/183760))
- Apply bugfixes when enabling Link-Time Optimizations ([#180868](https://github.com/pytorch/pytorch/pull/180868))

# Performance

## Autograd

- Use indexed storage for selective activation checkpointing (SAC) to avoid calling `policy_fn` during recompute ([#176455](https://github.com/pytorch/pytorch/pull/176455))

## Distributed

- Speed up store-based metadata exchange on `TCPStore` by using `multiGet` and a server-side `barrier`, reducing network round trips from `2*(world_size-1)` to `1` ([#182132](https://github.com/pytorch/pytorch/pull/182132))
- Coalesce the NCCL buffer and signal pad into a single symmetric-memory allocation so window registration runs only once ([#183344](https://github.com/pytorch/pytorch/pull/183344))

- Fuse slice-cat TP collective patterns ([#184911](https://github.com/pytorch/pytorch/pull/184911))

## FX

- Skip `GraphModule` reconstruction in `CSEPass` when no common subexpressions were eliminated ([#185479](https://github.com/pytorch/pytorch/pull/185479))

## Dynamo

- Fast path guardless cache hits ([#184683](https://github.com/pytorch/pytorch/pull/184683))
- Optimize jagged NestedTensor compile guards ([#184053](https://github.com/pytorch/pytorch/pull/184053))
- Skip Dynamo graph break for scalar-only binary ops when tensorify is enabled ([#183584](https://github.com/pytorch/pytorch/pull/183584))
- Avoid `repr` in Dynamo `ID_MATCH` guard text ([#184796](https://github.com/pytorch/pytorch/pull/184796))
- Add a pinned memory pool for activation-offloading `ao::offload` ops to avoid per-tensor `cudaHostAlloc` overhead (gated by the `pinned_memory_pool()` context manager) ([#186162](https://github.com/pytorch/pytorch/pull/186162))

## Inductor

- Eliminate unnecessary clones for dtype views in `auto_functionalize`, improving FP8 KV-cache performance ([#173177](https://github.com/pytorch/pytorch/pull/173177))
- Fix `basic_gnn_sage` fp32 single-thread performance regression ([#177958](https://github.com/pytorch/pytorch/pull/177958))
- Add a tail-size heuristic for CPP tail-loop vectorization to avoid masking/cast overhead in unprofitable cases ([#178243](https://github.com/pytorch/pytorch/pull/178243))
- Raise the split-reduction threshold to 524K on Blackwell+ to avoid over-splitting moderate reductions like softmax/entropy ([#179729](https://github.com/pytorch/pytorch/pull/179729))
- Add a pass to replace NVLink collectives with CopyEngine collectives during overlap to remove SM contention with matmuls ([#179937](https://github.com/pytorch/pytorch/pull/179937))
- Recalibrate the NCCL analytical model for comm/compute-overlap bucketing with auto-detected bandwidths and per-GPU-generation parameters, improving overlap (up to +14% MFU) ([#180463](https://github.com/pytorch/pytorch/pull/180463))
- Add `_FastCudaLauncher`, a vectorcall C extension for pre-bound kernel launch that reduces per-launch overhead ([#180507](https://github.com/pytorch/pytorch/pull/180507))
- Enable PadMM AutoHeuristics by default in deterministic mode, improving deterministic-mode inference speed (~14% on HuggingFace) ([#181038](https://github.com/pytorch/pytorch/pull/181038))
- Skip catastrophically slow polynomial `sympy.gcd` on very wide shape expressions, cutting some backward compiles from over 50 minutes to about 6 ([#181275](https://github.com/pytorch/pytorch/pull/181275))
- Add a 128x256x64 (`num_stages=4`) matmul config that speeds up large Hopper matmul shapes by ~1.3x and up ([#181413](https://github.com/pytorch/pytorch/pull/181413))
- Run Inductor joint-graph passes on `nested_compile_region` (`invoke_subgraph`) subgraphs created with options, which were previously skipped ([#181834](https://github.com/pytorch/pytorch/pull/181834))
- Use scaled persistent configs for the Blackwell scaled-mm TMA autotuning heuristic ([#182009](https://github.com/pytorch/pytorch/pull/182009))
- Generate vectorized loads in score-mods for speedups on contiguous, aligned key/value-dimension loads ([#183406](https://github.com/pytorch/pytorch/pull/183406))
- Enable reduction-broadcast vertical fusion for block-wise quantization (e.g. MXFP8/MXFP4) by reindexing pointwise nodes before `can_fuse_vertical`, reducing kernel count ([#183521](https://github.com/pytorch/pytorch/pull/183521))
- Use int32 indices in `grid_sampler_2d` lowering on CUDA/XPU when sizes fit, avoiding unnecessary int64 arithmetic ([#184269](https://github.com/pytorch/pytorch/pull/184269))
- Use the two-step variance path for small non-split CUDA reductions for better performance ([#184383](https://github.com/pytorch/pytorch/pull/184383))
- Emit `evict_first` for coalesced last-use loads in persistent reductions ([#184395](https://github.com/pytorch/pytorch/pull/184395))
- Use CPU-specific realization heuristic defaults to keep moderate pointwise bodies fused ([#184411](https://github.com/pytorch/pytorch/pull/184411))
- Faster FlexAttention CuteDSL codegen via vectorized mask-mod loads and packed-interval span lowering ([#184438](https://github.com/pytorch/pytorch/pull/184438))
- Avoid recomputing `log` in reused CPU pointwise so T5-style softmax bias inputs are materialized once ([#184473](https://github.com/pytorch/pytorch/pull/184473))
- Use an Inductor-owned CUDA benchmarking path with an L2-sized cache buffer to avoid Triton's fixed 256MB autotune cache allocation ([#184479](https://github.com/pytorch/pytorch/pull/184479))
- Improve compute/collective overlap scheduling by prioritizing collective prefetch candidates that fill more of the available overlap window ([#185186](https://github.com/pytorch/pytorch/pull/185186))
- Fuse the decomposed `_safe_softmax` SDPA math path back into a native `scaled_dot_product_attention` call (new SFDP patterns 29/30) ([#185574](https://github.com/pytorch/pytorch/pull/185574))
- Support CUTLASS EVT epilogue fusion through view/reshape between a GEMM and its pointwise consumer ([#185796](https://github.com/pytorch/pytorch/pull/185796))
- Restore dense MKL-DNN pointwise convolution speed by keeping the `forward_inference` prop kind only for channels-last/MKLDNN-layout, fixing a ~2x dense-contiguous slowdown ([#185997](https://github.com/pytorch/pytorch/pull/185997))
- Pre-bucket FSDP collectives in the compile overlap scheduler, merging many per-parameter all-gathers into bandwidth-saturating buckets ([#179935](https://github.com/pytorch/pytorch/pull/179935))
- Decompose small dot-shaped batched matmuls (`bmm`) ([#183911](https://github.com/pytorch/pytorch/pull/183911))

## Ahead-Of-Time Inductor (AOTI)

- Parallelize tensor-to-bytes conversion for AOTI weight serialization ([#181280](https://github.com/pytorch/pytorch/pull/181280))
- Enable shared model loading from a directory to avoid redundant unzipping ([#172436](https://github.com/pytorch/pytorch/pull/172436))

## Composability

- Use `torch.var_mean` to fuse paired var/mean reductions ([#184843](https://github.com/pytorch/pytorch/pull/184843))
- Avoid a Triton sort compile-time cliff in `create_block_mask` ([#182745](https://github.com/pytorch/pytorch/pull/182745))

## C++ Frontend

- Fix reduced-precision `rsqrt()` double promotion ([#181232](https://github.com/pytorch/pytorch/pull/181232))

## Release Engineering

- Add an operator microbenchmark comparison workflow for PRs ([#179476](https://github.com/pytorch/pytorch/pull/179476))
- Add a batch-invariant accuracy mode for benchmark perf tests ([#180610](https://github.com/pytorch/pytorch/pull/180610))

## CUDA

- Fix CUDA version check gating warp merge sort ([#183527](https://github.com/pytorch/pytorch/pull/183527))
- Allow specifying `nbits` to radix sort in `embedding_dense_backward_cuda` (#183578) ([#183578](https://github.com/pytorch/pytorch/pull/183578))
- Vectorize `scatter_add` with TMA bulk reduce on sm_90+ (Hopper) ([#182675](https://github.com/pytorch/pytorch/pull/182675))

## CPU (x86)

- Speed up random number generation for `bfloat16` and `half` tensors on x86 (roughly 2x faster) by using AVX2/VSX vectorized instructions in the `normal_`/`randn` kernel ([#179834](https://github.com/pytorch/pytorch/pull/179834))

## CPU (AArch64)

- Improve `bfloat16` transpose performance on AArch64 by adding a dedicated SVE-vectorized `transpose_mxn` implementation ([#174097](https://github.com/pytorch/pytorch/pull/174097))
- Add SVE128 dispatch for Arm CPUs ([#176256](https://github.com/pytorch/pytorch/pull/176256))

## MPS

- Fully utilize Philox state in distribution kernels ([#182247](https://github.com/pytorch/pytorch/pull/182247))
- 2D dispatch for strided unary kernels ([#185291](https://github.com/pytorch/pytorch/pull/185291))
- Templatize Im2Col to regain performance when 32-bit indexing suffices ([#185860](https://github.com/pytorch/pytorch/pull/185860))
- Faster norms ([#186076](https://github.com/pytorch/pytorch/pull/186076))
- Flatten 5D tensors to 4D in `batch_norm` for performance ([#180335](https://github.com/pytorch/pytorch/pull/180335))

## ROCm

- Set `MIOPEN_FIND_MODE=FAST` in op benchmark CI to prevent cold-cache timeout ([#179795](https://github.com/pytorch/pytorch/pull/179795))
- Fix FlexAttention fp16 default `num_warps` (8 -> 4) on AMD GPUs ([#180720](https://github.com/pytorch/pytorch/pull/180720))
- Fix perf regression in `index_add` and `index_reduce` ([#182533](https://github.com/pytorch/pytorch/pull/182533))
- Add no-fence optimization to the JIT reduce template ([#176812](https://github.com/pytorch/pytorch/pull/176812))
- Add target-dependent FlexAttention default forward configs ([#181283](https://github.com/pytorch/pytorch/pull/181283))

## XPU

- Add oneDNN-backed `nn.LSTM` inference support on XPU, replacing the per-timestep fused-cell path with a sequence-level primitive ([#185531](https://github.com/pytorch/pytorch/pull/185531))

## Sparse Frontend

- Optimize the layernorm + sigmoid epilogue by providing an ideal input shape to layernorm after sparse matmul ([#183472](https://github.com/pytorch/pytorch/pull/183472))

# Documentation

## Python Frontend

- Fix `out_dtype` signatures for `bmm`, `mm`, `addmm`, `baddbmm` ([#179182](https://github.com/pytorch/pytorch/pull/179182))
- Add CUDA SDPA determinism section to `randomness.rst` ([#182551](https://github.com/pytorch/pytorch/pull/182551))
- Convert stub docs pages to MyST Markdown ([#183498](https://github.com/pytorch/pytorch/pull/183498))
- Expose `nonzero_static` docs ([#185674](https://github.com/pytorch/pytorch/pull/185674))
- Note `expand` materialization costs ([#185400](https://github.com/pytorch/pytorch/pull/185400))
- Fix `torch.trapz` documentation signature to match `torch.trapezoid` ([#180571](https://github.com/pytorch/pytorch/pull/180571))
- Clarify that `torch.normal` does not support integer dtypes ([#180580](https://github.com/pytorch/pytorch/pull/180580))
- Document actual keyword argument names for `tensor_split` ([#182075](https://github.com/pytorch/pytorch/pull/182075))

## Dataloader Frontend

- Document previously undocumented functions in the `torch.utils.data` documentation ([#182682](https://github.com/pytorch/pytorch/pull/182682))

## Optimizer

- Use `\gamma` consistently for `lr` in `Adafactor` math blocks ([#184773](https://github.com/pytorch/pytorch/pull/184773))
- Clarify `ReduceLROnPlateau` `threshold_mode` behavior ([#180638](https://github.com/pytorch/pytorch/pull/180638))

## Distributed

- Improve the wording of the `batch_isend_irecv` documentation ([#183022](https://github.com/pytorch/pytorch/pull/183022))
- Add documentation for 8 functions in `distributed.md` ([#182544](https://github.com/pytorch/pytorch/pull/182544))
- Add TorchComms backend documentation to `torch.distributed` ([#182711](https://github.com/pytorch/pytorch/pull/182711))
- Add a distributed training integration guide for out-of-tree accelerators ([#182308](https://github.com/pytorch/pytorch/pull/182308))

- Convert the torchelastic `elastic/quickstart.rst` from reStructuredText to MyST Markdown ([#182569](https://github.com/pytorch/pytorch/pull/182569))
- Convert the RPC `rpc/rref.rst` from reStructuredText to MyST Markdown ([#182877](https://github.com/pytorch/pytorch/pull/182877))
- Clarify that `--node-rank` is only used with static rendezvous ([#182374](https://github.com/pytorch/pytorch/pull/182374))
- Add API reference documentation for previously-undocumented functions in `torch.distributed.rpc` ([#183393](https://github.com/pytorch/pytorch/pull/183393))
- Add API reference documentation for previously-undocumented functional optimizer APIs in `torch.distributed.optim` ([#182871](https://github.com/pytorch/pytorch/pull/182871))

## Distributed Checkpointing

- Document previously undocumented functions in the `torch.distributed.checkpoint` API reference ([#182887](https://github.com/pytorch/pytorch/pull/182887))

## DTensor

- Clarify default dtype behavior in the `DTensor.redistribute` docstring ([#181671](https://github.com/pytorch/pytorch/pull/181671))
- Document undocumented functions in `distributed.tensor.parallel.md` ([#182876](https://github.com/pytorch/pytorch/pull/182876))

## Distributed FSDP2

- Document previously undocumented functions in `distributed.fsdp.fully_shard` ([#182866](https://github.com/pytorch/pytorch/pull/182866))

## Profiler

- Remove references to `_KinetoProfile` in public docs ([#180672](https://github.com/pytorch/pytorch/pull/180672))

## Export

- Fix typos in attention bias, activation, and dataloader docs ([#184244](https://github.com/pytorch/pytorch/pull/184244))

## ONNX

- Remove stale Caffe2 references from ONNX TorchScript exporter docs ([#180498](https://github.com/pytorch/pytorch/pull/180498))

## C++ Frontend

- Fix typos in export wrapper docstring and transformer module comment ([#181972](https://github.com/pytorch/pytorch/pull/181972))

# Security

# Developers

## Optimizer

- Add optimizer reparameterization helper for non-strict tracing ([#181643](https://github.com/pytorch/pytorch/pull/181643))

## Autograd

- Expose the PrivateUse1 backend name as an alias in `DeviceType` ([#184835](https://github.com/pytorch/pytorch/pull/184835))
- Show the forward op name instead of the backward node name in autograd anomaly/error messages ([#180383](https://github.com/pytorch/pytorch/pull/180383))

## Distributed

- Add a missing include to `GlooDeviceFactory.cpp` ([#182800](https://github.com/pytorch/pytorch/pull/182800))
- Fix a missing `#include <cuda.h>` in `CUDASymmetricMemoryTypes.hpp` ([#183704](https://github.com/pytorch/pytorch/pull/183704))

## FX

- Add a fast path in `GraphPickler.reducer_override` for primitive types ([#181602](https://github.com/pytorch/pytorch/pull/181602))

## Inductor

- Enable the Inductor SYCL-TLA standalone runner on XPU (developer benchmarking tooling) ([#174958](https://github.com/pytorch/pytorch/pull/174958))
- Add an optional Torch-Profiler-based Inductor autotuning benchmarker (off by default, env-gated) for more accurate timing of short-duration kernels ([#175097](https://github.com/pytorch/pytorch/pull/175097))
- Add a dedicated custom-pass class for `_pre_fusion_custom_pass` to match its scheduler-node signature ([#179050](https://github.com/pytorch/pytorch/pull/179050))
- Include `_post_fusion_custom_pass` in the FX graph cache hash ([#179051](https://github.com/pytorch/pytorch/pull/179051))
- Share storage for aliased inputs in the generated `benchmark_compiled_module` repro code to avoid OOM ([#181119](https://github.com/pytorch/pytorch/pull/181119))
- Enable frame pointers by default in AOTInductor shared libraries so profilers get accurate stacks ([#181358](https://github.com/pytorch/pytorch/pull/181358))
- Fix decomposition and lowering debug info (overload names) for the compiler bisector, including across subprocesses ([#181452](https://github.com/pytorch/pytorch/pull/181452))
- Add DOT graph dumps for Inductor debug traces ([#184039](https://github.com/pytorch/pytorch/pull/184039))
- Fix the Inductor `save_args` debug/repro tooling to serialize fake tensors and symbolic metadata so it works with dynamic shapes ([#184428](https://github.com/pytorch/pytorch/pull/184428))
- Fix the device argument in the generated combo-kernel benchmark script ([#184868](https://github.com/pytorch/pytorch/pull/184868))

## Ahead-Of-Time Inductor (AOTI)

- Add C-ABI-safe V2 interface for MinimalArrayref ([#179483](https://github.com/pytorch/pytorch/pull/179483))
- Add C-ABI-safe V2 interface for UpdateConstantsMap ([#180533](https://github.com/pytorch/pytorch/pull/180533))
- Add C-ABI-safe ExtractConstantsMapForEach ([#183030](https://github.com/pytorch/pytorch/pull/183030))
- Add C-ABI-safe UpdateConstantBufferPairs ([#183031](https://github.com/pytorch/pytorch/pull/183031))
- Add C-ABI-safe UpdateConstantBufferFromCpuPairs ([#183032](https://github.com/pytorch/pytorch/pull/183032))
- Add C-ABI-safe UpdateInactiveConstantBufferPairs ([#183033](https://github.com/pytorch/pytorch/pull/183033))
- Add C-ABI-safe AOTInductorModelCreateV2 ([#185729](https://github.com/pytorch/pytorch/pull/185729))

## Composability

- Change most HOPs to use `@register_fake` instead of `py_impl(FakeTensorMode)` ([#186247](https://github.com/pytorch/pytorch/pull/186247))
- Genericize graphsafe RNG in `aot_autograd` to support non-CUDA device backends ([#182391](https://github.com/pytorch/pytorch/pull/182391))
- Mark `graphsafe_run_with_rng_state` as cacheable for `FxGraphCache` ([#185562](https://github.com/pytorch/pytorch/pull/185562))

## Release Engineering

- Migrate the build to CMake / scikit-build-core: move NCCL checkout, source-file mirroring, header wrapping, `compile_commands` merging, and the `torch._C` extension/`version.py` build out of `setup.py` and into CMake ([#181450](https://github.com/pytorch/pytorch/pull/181450), [#177642](https://github.com/pytorch/pytorch/pull/177642), [#177643](https://github.com/pytorch/pytorch/pull/177643), [#177644](https://github.com/pytorch/pytorch/pull/177644), [#180243](https://github.com/pytorch/pytorch/pull/180243))
- Drop the setuptools `concat_license_files` hook and adopt PEP 639 `license-files`; replace deprecated `distutils` usage ([#180237](https://github.com/pytorch/pytorch/pull/180237), [#182120](https://github.com/pytorch/pytorch/pull/182120))
- Install `libaotriton_v2.so` via cmake install for wheel packaging ([#180242](https://github.com/pytorch/pytorch/pull/180242))
- Embed the macOS OpenMP runtime in `PostBuildSteps` ([#180239](https://github.com/pytorch/pytorch/pull/180239))

## XPU

- Respect `MKLROOT`, `CMPLR_ROOT`, and `ONEAPI_ROOT` from `setvars.sh` in `FindMKL.cmake` so custom oneAPI installs are detected correctly ([#183506](https://github.com/pytorch/pytorch/pull/183506))


## TorchScript

- Add `torch._C._jit_replace_submodule` to swap submodules in scripted modules while updating parent types and remapping referenced types across graphs ([#180296](https://github.com/pytorch/pytorch/pull/180296))
- Use `TORCH_CHECK` instead of `AT_ASSERT` for single input/output node helpers, producing clearer error messages ([#181282](https://github.com/pytorch/pytorch/pull/181282))
- Expose `overlapsWithUsedNodes` and `getVmap` from `SubgraphRewriter` ([#183333](https://github.com/pytorch/pytorch/pull/183333))
