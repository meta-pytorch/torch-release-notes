# PyTorch 2.14.0 Release Notes

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

## torch.nn

- `torch.nn.LinearCrossEntropyOptions` no longer accepts `acc_policy="balanced"`; use `"compact"` instead ([#188283](https://github.com/pytorch/pytorch/pull/188283))

  The `"balanced"` policy was removed because `"compact"` provides the same weight-gradient accumulation precision with lower memory use on CUDA, already uses the equivalent scratch layout for mixed-precision inputs on other devices, and was never selected by `"auto"`. Constructing the options with `acc_policy="balanced"` now raises `ValueError: invalid acc_policy: 'balanced'; expected one of 'auto', 'accurate', 'compact'`.

  Before:

  ```python
  options = torch.nn.LinearCrossEntropyOptions(acc_policy="balanced")
  loss = torch.nn.functional.linear_cross_entropy(
      input, linear_weight, target, options=options
  )
  ```

  After:

  ```python
  options = torch.nn.LinearCrossEntropyOptions(acc_policy="compact")
  loss = torch.nn.functional.linear_cross_entropy(
      input, linear_weight, target, options=options
  )
  ```

## Autograd

- Clamp and min/max boundary subgradients now follow the selected dispatcher schema's input space ([#191142](https://github.com/pytorch/pytorch/pull/191142))

  This affects gradients exactly at nondifferentiable bounds or ties. A scalar clamp bound is a fixed parameter, so the input gradient at equality changes from `1` to the minimum-norm subgradient `0`. A Tensor bound is part of the differentiable input space, so `clamp`, `clamp_min`, and `clamp_max` now split the gradient evenly between the input and bound at an ordinary tie instead of assigning it entirely to the input. `fmin` and `fmax` use the same even tie split, and forward-mode AD for the min/max family is aligned with these rules. Code that intentionally depends on the old tie-breaking behavior can express it explicitly with `torch.where`, such as `torch.where(value >= bound, value, bound)`.

  Version 2.13:
  ```python
  import torch

  x = torch.tensor(0.0, requires_grad=True)
  torch.clamp_min(x, 0.0).backward()
  print(x.grad)  # tensor(1.)

  value = torch.tensor(0.0, requires_grad=True)
  bound = torch.tensor(0.0, requires_grad=True)
  torch.clamp_min(value, bound).backward()
  print(value.grad, bound.grad)  # tensor(1.) tensor(0.)
  ```

  Version 2.14:
  ```python
  import torch

  x = torch.tensor(0.0, requires_grad=True)
  torch.clamp_min(x, 0.0).backward()
  print(x.grad)  # tensor(0.)

  value = torch.tensor(0.0, requires_grad=True)
  bound = torch.tensor(0.0, requires_grad=True)
  torch.clamp_min(value, bound).backward()
  print(value.grad, bound.grad)  # tensor(0.5000) tensor(0.5000)
  ```

## Distributed

- Custom Python process groups that implement `new_group()` must now accept a `backend` keyword argument ([#188489](https://github.com/pytorch/pytorch/pull/188489))

  This applies when the default process group supplies its own `new_group()` method and `torch.distributed.new_group()` delegates subgroup creation to it. PyTorch now forwards the resolved backend so custom implementations can construct the requested subgroup correctly. Existing implementations without this parameter will raise `TypeError: ... got an unexpected keyword argument 'backend'`. Accept and use the argument, or accept and ignore it when the implementation has only one backend.

  Before:

  ```python
  class MyProcessGroup(...):
      def new_group(
          self, ranks, *, timeout=None, pg_options=None,
          group_name=None, group_desc=None
      ):
          ...
  ```

  After:

  ```python
  class MyProcessGroup(...):
      def new_group(
          self, ranks, *, timeout=None, backend=None, pg_options=None,
          group_name=None, group_desc=None
      ):
          ...
  ```

- NCCL symmetric-memory pools no longer automatically upgrade segments allocated after `register_mem_pool(..., symm=True)` to symmetric windows ([#192112](https://github.com/pytorch/pytorch/pull/192112))

  Registering those late segments from the CUDA allocator callback could invoke a collective NCCL operation on only some ranks while holding the allocator lock, causing an unrecoverable hang. Late segments now remain ordinary registered NCCL buffers. Applications that need newly allocated segments to use symmetric-window algorithms must collectively deregister and register the pool again after those allocations are created.

  Before:

  ```python
  backend.register_mem_pool(pool, symm=True)
  with torch.cuda.use_mem_pool(pool):
      tensor = torch.empty(size, device="cuda")
  # Newly allocated segments were automatically upgraded, but this could hang.
  ```

  After:

  ```python
  backend.register_mem_pool(pool, symm=True)
  with torch.cuda.use_mem_pool(pool):
      tensor = torch.empty(size, device="cuda")

  # Collectively refresh registration after the pool grows.
  backend.deregister_mem_pool(pool)
  backend.register_mem_pool(pool, symm=True)
  ```

- Nonmember ranks now receive `GroupMember.NON_GROUP_MEMBER` instead of `None` from experimental `torch.distributed.split_group()` ([#190725](https://github.com/pytorch/pytorch/pull/190725))

  When the calling rank is absent from every requested split, `split_group()` now returns the same nonmember sentinel as `new_group()`. Code that identifies nonmembers with `is None` must compare against `torch.distributed.GroupMember.NON_GROUP_MEMBER` instead.

  Before:

  ```python
  group = torch.distributed.split_group(
      split_ranks=[[0, 1], [2, 3]]
  )
  if group is None:
      return
  ```

  After:

  ```python
  group = torch.distributed.split_group(
      split_ranks=[[0, 1], [2, 3]]
  )
  if group == torch.distributed.GroupMember.NON_GROUP_MEMBER:
      return
  ```

## Linear Algebra Frontend

- Remove the deprecated `torch.cholesky()` and `Tensor.cholesky()` APIs ([#186817](https://github.com/pytorch/pytorch/pull/186817))

  Calls now raise a `RuntimeError` directing users to `torch.linalg.cholesky()`. The replacement returns a lower-triangular factor; callers that previously requested `upper=True` should take the conjugate transpose with `.mH`.

  Version 2.13:

  ```python
  lower = torch.cholesky(a)
  upper = torch.cholesky(a, upper=True)
  ```

  Version 2.14:

  ```python
  lower = torch.linalg.cholesky(a)
  upper = torch.linalg.cholesky(a).mH
  ```

- Remove the deprecated `torch.qr()` and `Tensor.qr()` APIs ([#186815](https://github.com/pytorch/pytorch/pull/186815))

  Calls now raise a `RuntimeError` directing users to `torch.linalg.qr()`. Replace the Boolean `some` argument with `mode="reduced"` or `mode="complete"`.

  Version 2.13:

  ```python
  q, r = torch.qr(a)
  q_full, r_full = torch.qr(a, some=False)
  ```

  Version 2.14:

  ```python
  q, r = torch.linalg.qr(a, mode="reduced")
  q_full, r_full = torch.linalg.qr(a, mode="complete")
  ```

## Profiler

- The deprecated `use_cuda` argument has been removed from `torch.profiler.profile` and `torch.autograd.profiler.profile` ([#192543](https://github.com/pytorch/pytorch/pull/192543))

  Passing `use_cuda` to either profiler now raises `TypeError: profile.__init__() got an unexpected keyword argument 'use_cuda'`. Select CUDA explicitly through `activities` when using `torch.profiler.profile`, or use `use_device="cuda"` with `torch.autograd.profiler.profile`.

  Version 2.13:

  ```python
  with torch.profiler.profile(use_cuda=True) as prof:
      run_workload()

  with torch.autograd.profiler.profile(use_cuda=True) as prof:
      run_workload()
  ```

  Version 2.14:

  ```python
  with torch.profiler.profile(
      activities=[
          torch.profiler.ProfilerActivity.CPU,
          torch.profiler.ProfilerActivity.CUDA,
      ]
  ) as prof:
      run_workload()

  with torch.autograd.profiler.profile(use_device="cuda") as prof:
      run_workload()
  ```

## Dynamo

- The `tvm` backend now uses TVM's relax frontend exclusively; the relay path has been removed ([#190766](https://github.com/pytorch/pytorch/pull/190766), [#189639](https://github.com/pytorch/pytorch/pull/189639))

  Relay was removed in TVM 0.20, so the backend now requires a TVM providing `tvm.relax.frontend.torch`. Two things are gone with it: the relay-only `scheduler` / `trials` options, replaced by a TVM pipeline passed as `options={"pipeline": ...}`; and the `tvm_meta_schedule` / `tvm_auto_scheduler` backend entry points, which no longer exist in `torch._dynamo.backends.tvm`. With an older TVM installed, `torch.compile(..., backend="tvm")` now raises `ImportError: Please install apache-tvm to use the tvm backend.`

  Version 2.13:
  ```python
  opt = torch.compile(model, backend="tvm", options={"scheduler": "meta_schedule", "trials": 20000})

  # or through the relay-only entry points
  from torch._dynamo.backends.tvm import tvm_meta_schedule, tvm_auto_scheduler
  ```

  Version 2.14:
  ```python
  import tvm

  pipeline = tvm.relax.get_pipeline("static_shape_tuning", target="llvm", total_trials=2000)
  opt = torch.compile(model, backend="tvm", options={"pipeline": pipeline})

  # tvm_meta_schedule / tvm_auto_scheduler no longer exist:
  # ImportError: cannot import name 'tvm_meta_schedule'
  ```

## C++ Frontend

- C++ extensions and LibTorch applications must now compile as C++20 or newer ([#178150](https://github.com/pytorch/pytorch/pull/178150))

  PyTorch's public ATen and C++ frontend headers now reject pre-C++20 language modes. On non-MSVC compilers, including `<ATen/ATen.h>` or `<torch/torch.h>` with C++17 produces `C++20 or later compatible compiler is required to use ATen.` or the equivalent PyTorch message. Update the consuming build to request C++20.

  Version 2.13:

  ```cmake
  set(CMAKE_CXX_STANDARD 17)
  find_package(Torch REQUIRED)
  ```

  Version 2.14:

  ```cmake
  set(CMAKE_CXX_STANDARD 20)
  find_package(Torch REQUIRED)
  ```

- Remove the deprecated C++ method `at::Tensor::is_variable()` ([#187136](https://github.com/pytorch/pytorch/pull/187136))

  All tensors have used Variable semantics for several releases, so callers should remove checks of `tensor.is_variable()`. Code that was specifically checking whether Variable dispatch had already been excluded can query `at::impl::variable_excluded_from_dispatch()` instead.

  Version 2.13:

  ```cpp
  if (tensor.is_variable()) {
    use_tensor(tensor);
  }
  ```

  Version 2.14:

  ```cpp
  // Every Tensor has Variable semantics.
  use_tensor(tensor);
  ```

- Remove the `c10/util/Array.h` header and `c10::array_of()` helper ([#186790](https://github.com/pytorch/pytorch/pull/186790))

  C++ extensions that include this header or call `c10::array_of()` will no longer compile. Since PyTorch now requires C++20, use the standard `<array>` header and `std::to_array()` instead.

  Version 2.13:

  ```cpp
  #include <c10/util/Array.h>

  constexpr auto values = c10::array_of<int>(1, 2, 3);
  ```

  Version 2.14:

  ```cpp
  #include <array>

  constexpr auto values = std::to_array<int>({1, 2, 3});
  ```

- Remove the deprecated zero-argument C++ overloads `c10::Scalar::isIntegral()` and `c10::isIntegralType(ScalarType)` ([#187115](https://github.com/pytorch/pytorch/pull/187115))

  Code that calls either overload without specifying whether Boolean values count as integral will no longer compile. Pass `includeBool` explicitly; use `false` to preserve the removed overloads' behavior.

  Version 2.13:

  ```cpp
  bool scalar_is_integer = scalar.isIntegral();
  bool dtype_is_integer = c10::isIntegralType(dtype);
  ```

  Version 2.14:

  ```cpp
  bool scalar_is_integer = scalar.isIntegral(/*includeBool=*/false);
  bool dtype_is_integer =
      c10::isIntegralType(dtype, /*includeBool=*/false);
  ```

## Release Engineering

- Source builds with CUDA now require CUDA 12.6 or newer ([#192257](https://github.com/pytorch/pytorch/pull/192257))

  The minimum supported CUDA toolkit for building PyTorch has increased from 12.1 to 12.6. Configuring a source build with CUDA 12.1 through 12.5 now fails with `PyTorch requires CUDA 12.6 or above.` Upgrade the selected toolkit, or build without CUDA.

  Version 2.13:

  ```bash
  CUDA_HOME=/usr/local/cuda-12.1 python -m pip install . --no-build-isolation
  ```

  Version 2.14:

  ```bash
  CUDA_HOME=/usr/local/cuda-12.6 python -m pip install . --no-build-isolation
  ```

- Prebuilt Windows LibTorch debug binaries are no longer published ([#187352](https://github.com/pytorch/pytorch/pull/187352))

  The separately built Debug archives for Windows x86-64 and Windows Arm64 have been discontinued. Windows wheels and release-mode LibTorch binaries remain available. Projects that require a Debug LibTorch build must build it from a PyTorch source checkout.

  Version 2.13:

  ```powershell
  # A prebuilt Windows LibTorch Debug archive was available.
  ```

  Version 2.14:

  ```powershell
  $env:DEBUG = "1"
  python tools/build_libtorch.py
  ```

- `setup.py` is now a deprecation shim; build PyTorch through pip or `python -m build` ([#180248](https://github.com/pytorch/pytorch/pull/180248))

  `setup.py` is now a thin shim. `install` and `develop` still forward to pip, but
  `build`, `bdist_wheel`, `clean`, `sdist` and the rest print the replacement
  command instead of falling through to setuptools. Builds that already go through
  a PEP 517 frontend are unaffected, since pip and `python -m build` never ran
  `setup.py`. The shim prints the schedule: `install`/`develop` keep forwarding
  through 2.15, every command stops working in 2.16, and `setup.py` is removed
  in 2.18.

  Version 2.13:
  ```bash
  python setup.py bdist_wheel
  ```

  Version 2.14:
  ```bash
  python -m build --wheel --no-isolation
  ```

## CUDA

- CUDA Green Contexts now require the `cuda-bindings` package, and the C++ `at::cuda::GreenContext` API has been removed ([#185527](https://github.com/pytorch/pytorch/pull/185527))

  The experimental Python `torch.cuda.green_contexts.GreenContext` API is now implemented with CUDA Python. Constructing or querying a green context without `cuda-bindings` raises `RuntimeError: GreenContext requires the cuda.bindings package`. Install that package before using the Python API; the existing `GreenContext.create()` factory remains available as a compatibility wrapper. C++ code that included `<ATen/cuda/CUDAGreenContext.h>` must instead use the CUDA Driver API directly; there is no replacement LibTorch class.

  Version 2.13:

  ```python
  ctx = torch.cuda.green_contexts.GreenContext.create(num_sms=8)
  ```

  Version 2.14:

  ```bash
  python -m pip install cuda-bindings
  ```

  ```python
  ctx = torch.cuda.green_contexts.GreenContext.create(num_sms=8)
  ```

- `CUDAGraph` debug mode is now per instance, defers instantiation, and requires `cuda-bindings` for `debug_dump()` ([#187749](https://github.com/pytorch/pytorch/pull/187749))

  Calling `enable_debug_mode()` now retains only that graph's capture template, like constructing it with `keep_graph=True`; it no longer sets a process-wide flag. Because retained graphs are not instantiated at `capture_end()`, call `instantiate()` before accessing `raw_cuda_graph_exec()` if replay has not already instantiated the graph. Direct users of the split capture API must also call `instantiate()` before `capture_end_post()` when `keep_graph=False`, because `capture_end_post()` is now destroy-only. The Python `debug_dump()` implementation now uses `cuda-bindings`, and the C++ `CUDAGraph::debug_dump` method has been removed. For a one-time dump without retaining the template, register `torch.cuda.export_dot(path)` with `register_capture_end_hook()` before capture.

  Version 2.13:

  ```python
  graph = torch.cuda.CUDAGraph()
  graph.enable_debug_mode()
  with torch.cuda.graph(graph):
      captured_work()
  exec_handle = graph.raw_cuda_graph_exec()
  graph.debug_dump("graph.dot")
  ```

  Version 2.14:

  ```python
  # Requires: python -m pip install cuda-bindings
  graph = torch.cuda.CUDAGraph(keep_graph=True)
  with torch.cuda.graph(graph):
      captured_work()
  graph.debug_dump("graph.dot")
  graph.instantiate()
  exec_handle = graph.raw_cuda_graph_exec()
  ```

- Deprecate Python `CUDAGraph.register_generator_state()` and remove its C++ overload; CUDA graphs now register generator state lazily on first RNG use during capture ([#176753](https://github.com/pytorch/pytorch/pull/176753))

  The Python method is now a no-op and emits a deprecation warning. The C++ `at::cuda::CUDAGraph::register_generator_state(const at::Generator&)` overload has been removed. Remove explicit registration calls in both languages; the graph automatically retains the required state when the generator is first used during capture.

  Before:

  ```python
  graph = torch.cuda.CUDAGraph()
  state = generator.graphsafe_get_state()
  graph.register_generator_state(state)

  with torch.cuda.graph(graph):
      generator.graphsafe_set_state(state)
      output = torch.rand(16, device="cuda", generator=generator)
  ```

  After:

  ```python
  graph = torch.cuda.CUDAGraph()
  state = generator.graphsafe_get_state()

  with torch.cuda.graph(graph):
      generator.graphsafe_set_state(state)
      output = torch.rand(16, device="cuda", generator=generator)
  ```

## MPS

- The C++ MPS macOS-version helper and its enum members have been renamed ([#188645](https://github.com/pytorch/pytorch/pull/188645))

  Downstream C++ code that includes `<ATen/mps/MPSDevice.h>` must replace the exported `at::mps::is_macos_13_or_newer()` function with `at::mps::is_macos_at_least()`. The associated `MacOSVersion` members also drop the `VER` and `PLUS` portions of their names. No compatibility aliases are provided, so code using the old names will no longer compile.

  Version 2.13:

  ```cpp
  const bool supported = at::mps::is_macos_13_or_newer(
      at::mps::MacOSVersion::MACOS_VER_15_0_PLUS);
  ```

  Version 2.14:

  ```cpp
  const bool supported = at::mps::is_macos_at_least(
      at::mps::MacOSVersion::MACOS_15_0);
  ```

## XPU

- The XPU C++ memory-pool class has moved from `c10::xpu::MemPool` to `at::xpu::MemPool` ([#192032](https://github.com/pytorch/pytorch/pull/192032))

  C++ code that constructs an XPU memory pool must include its new ATen header and use the new namespace. The Python `torch.xpu.MemPool` API is unchanged.

  Version 2.13:

  ```cpp
  #include <c10/xpu/XPUCachingAllocator.h>
  c10::xpu::MemPool pool;
  ```

  Version 2.14:

  ```cpp
  #include <ATen/xpu/MemPool.h>
  at::xpu::MemPool pool;
  ```

- XPU source builds no longer support pre-2026 SYCL compilers ([#191470](https://github.com/pytorch/pytorch/pull/191470))

  PyTorch now uses 2026 SYCL APIs such as `sycl::aspect::ext_oneapi_is_integrated_gpu` without the older compiler fallback. A source build using a 2025.x or earlier oneAPI compiler may therefore fail to compile. Activate a oneAPI 2026.x or newer toolchain before configuring the build; PyTorch's packaged XPU stack uses oneAPI 2026.1.

  Version 2.13 source build:

  ```bash
  icpx --version  # A pre-2026 compiler could still use fallback code.
  python -m pip install . --no-build-isolation
  ```

  Version 2.14 source build:

  ```bash
  icpx --version  # Must report a 2026.x or newer compiler.
  python -m pip install . --no-build-isolation
  ```

## Complex Frontend

- Complex type promotion for `bfloat16` now uses the new `torch.bcomplex32` shell dtype instead of `torch.complex64` ([#186928](https://github.com/pytorch/pytorch/pull/186928))

  `torch.bcomplex32` stores real and imaginary components as `bfloat16`. Operations that combine a `bfloat16` tensor with a complex scalar or otherwise request its corresponding complex type can therefore produce `bcomplex32` instead of `complex64`. Because `bcomplex32` is a shell dtype with limited operator support, an operation that previously ran in `complex64` may now raise a not-implemented error. Explicitly cast to `complex64` when the previous precision or operator coverage is required.

  Version 2.13:

  ```python
  x = torch.ones(4, dtype=torch.bfloat16)
  assert torch.result_type(x, 1j) == torch.complex64
  ```

  Version 2.14:

  ```python
  x = torch.ones(4, dtype=torch.bfloat16)
  assert torch.result_type(x, 1j) == torch.bcomplex32

  # Preserve the previous complex64 behavior explicitly.
  y = x.to(torch.complex64) + 1j
  ```

# Deprecations

## Autograd

- Selective activation checkpointing will change to honor surrounding `saved_tensors_hooks` by default; use the new `respect_saved_tensors_hooks` argument to choose the behavior explicitly ([#190581](https://github.com/pytorch/pytorch/pull/190581))

  The current default, `None`, preserves the legacy behavior in which tensors retained by selective activation checkpointing bypass user hooks, but now emits a `FutureWarning` when hooks are active. Pass `True` to opt into the future behavior or `False` to preserve the legacy behavior without a warning. This option requires `use_reentrant=False`.

  Before:

  ```python
  with torch.autograd.graph.saved_tensors_hooks(pack, unpack):
      output = torch.utils.checkpoint.checkpoint(
          function,
          input,
          use_reentrant=False,
          context_fn=sac_context_fn,
      )
  ```

  After:

  ```python
  with torch.autograd.graph.saved_tensors_hooks(pack, unpack):
      output = torch.utils.checkpoint.checkpoint(
          function,
          input,
          use_reentrant=False,
          context_fn=sac_context_fn,
          respect_saved_tensors_hooks=True,
      )
  ```

## Distributed

- Use `torch.compiler.config.compile_on_one_rank` instead of `torch.distributed.config.compile_on_one_rank` ([#187869](https://github.com/pytorch/pytorch/pull/187869))

  The distributed spelling remains as a forwarding alias but now emits a `FutureWarning`. The preferred environment variable is also `TORCH_COMPILE_ON_ONE_RANK`; the older `TORCH_DISTRIBUTED_COMPILE_ON_ONE_RANK` remains supported for compatibility.

  Before:

  ```python
  import torch.distributed.config
  torch.distributed.config.compile_on_one_rank = True
  ```

  After:

  ```python
  import torch.compiler.config
  torch.compiler.config.compile_on_one_rank = True
  ```

## Distributed (c10d)

- Use `torch.distributed.gather_single()` instead of `torch.distributed.gather_into_tensor()` ([#191073](https://github.com/pytorch/pytorch/pull/191073))

  `gather_into_tensor()` remains as a forwarding alias with the same arguments, but now emits a `FutureWarning`. The corresponding C++ `Backend` and `ProcessGroup` collective is also named `gather_single`; custom backends should implement the new name.

  Before:

  ```python
  torch.distributed.gather_into_tensor(
      input_tensor, output_tensor, dst=0
  )
  ```

  After:

  ```python
  torch.distributed.gather_single(
      input_tensor, output_tensor, dst=0
  )
  ```

## Profiler

- The experimental `profiler_metrics` and `profiler_measure_per_kernel` options no longer enable CUPTI range profiling and now emit a `FutureWarning` when set to a non-default value ([#187204](https://github.com/pytorch/pytorch/pull/187204))

  Kineto no longer supports this range-profiler path on PyTorch's supported CUDA versions. The arguments remain accepted temporarily for compatibility, but they are ignored and have no direct replacement.

  Before:

  ```python
  config = torch.profiler._ExperimentalConfig(
      profiler_metrics=["sm__cycles_elapsed.avg"],
      profiler_measure_per_kernel=True,
  )
  ```

  After:

  ```python
  config = torch.profiler._ExperimentalConfig()
  ```

- The `with_modules` profiler option is deprecated and now emits a `FutureWarning` ([#192808](https://github.com/pytorch/pytorch/pull/192808))

  `with_modules=True` only collected module hierarchy for TorchScript models and did nothing in eager mode. For eager models, use `with_stack=True` to record `nn.Module` events.

  Before:

  ```python
  with torch.profiler.profile(with_modules=True) as prof:
      run_workload()
  ```

  After:

  ```python
  with torch.profiler.profile(with_stack=True) as prof:
      run_workload()
  ```

## Dynamo

- `torch._dynamo.config.enable_faithful_generator_behavior` is deprecated and is now a no-op ([#189894](https://github.com/pytorch/pytorch/pull/189894))

  Faithful (lazy) generator tracing has been the default and is the only supported behavior, so the dead eager-exhaustion path was removed. The config is kept as a deprecated setting that always behaves as `True`, so setting it does not error but no longer changes anything.

  Version 2.13:
  ```python
  # generators were eagerly exhausted on first execution
  with torch._dynamo.config.patch(enable_faithful_generator_behavior=False):
      torch.compile(fn)(x)
  ```

  Version 2.14:
  ```python
  # the flag is ignored; generators are always traced lazily
  torch.compile(fn)(x)
  ```

## CUDA

- Deprecate `GreenContext.set_context()` and `GreenContext.pop_context()`; use custom streams to activate a green context instead ([#188419](https://github.com/pytorch/pytorch/pull/188419))

  These methods now emit a `FutureWarning`. Create a stream from the green context and use it with `torch.cuda.stream()` instead. Synchronization with streams outside the green context remains the caller's responsibility and should use CUDA events when needed.

  Before:

  ```python
  ctx = torch.cuda.green_contexts.GreenContext(num_sms=1)
  ctx.set_context()
  try:
      output = model(input)
  finally:
      ctx.pop_context()
  ```

  After:

  ```python
  ctx = torch.cuda.green_contexts.GreenContext(num_sms=1)
  stream = ctx.Stream()
  with torch.cuda.stream(stream):
      output = model(input)
  ```

## JIT

- TorchScript APIs now emit visible `FutureWarning`s instead of normally hidden `DeprecationWarning`s ([#189914](https://github.com/pytorch/pytorch/pull/189914))

  Calls such as `torch.jit.script`, `torch.jit.trace`, `torch.jit.save`, and `torch.jit.load` now visibly direct users toward `torch.compile` or `torch.export`. Imports of `torch.utils.mkldnn` and `torch.distributed.optim` also avoid eagerly compiling TorchScript when those modules are merely imported.

  Before:

  ```python
  scripted = torch.jit.script(model)
  torch.jit.save(scripted, "model.pt")
  ```

  After:

  ```python
  exported = torch.export.export(model, example_inputs)
  torch.export.save(exported, "model.pt2")
  ```

# New Features

## Python Frontend

- Add `torch.accelerator.initial_seed()`, `torch.accelerator.get_rng_state()`, and `torch.accelerator.get_rng_state_all()` for backend-agnostic accelerator RNG inspection ([#186597](https://github.com/pytorch/pytorch/pull/186597))
- Add read-only DLPack export through `Tensor.__dlpack__(read_only=True)` and `torch.utils.dlpack.ReadOnlyTensorWrapper`, including copy-on-write-preserving exchange with compatible consumers ([#188554](https://github.com/pytorch/pytorch/pull/188554))
- Add `torch.Generator.philox_state()` so Python-authored kernels can reserve Philox counter ranges that remain correct across CUDA Graph capture and replay ([#191019](https://github.com/pytorch/pytorch/pull/191019))

## Autograd

- `torch.utils.checkpoint.checkpoint()` can now be called without a function to create an eager-mode decorator with checkpoint configuration separated from the wrapped function's arguments ([#189411](https://github.com/pytorch/pytorch/pull/189411))

  ```python
  checkpointed_function = torch.utils.checkpoint.checkpoint(
      use_reentrant=False
  )(function)
  output = checkpointed_function(*args, **kwargs)
  ```

  The curried form is initially supported in eager mode; existing direct calls remain the compatible form under `torch.compile`.

- Add `torch.autograd.graph.node_creation_hook`, a thread-local context manager whose callback receives every fully populated autograd graph node created within its scope. The callback can inspect nodes, store metadata, or register backward pre-hooks and post-hooks, including for nodes created during higher-order differentiation and checkpoint recomputation ([#189284](https://github.com/pytorch/pytorch/pull/189284))

- Add `ctx.set_output_grad_dtype(*dtypes)` for custom `torch.autograd.Function` implementations. Called once from `forward` or `setup_context`, it declares the gradient dtype expected for each output independently of the output's storage dtype; a concrete dtype converts incoming gradients, while `None` leaves their dtype unchanged ([#189634](https://github.com/pytorch/pytorch/pull/189634))

- Add second-order gradient support for `torch.cdist` and `torch.nn.functional.pdist`, so grad-grad computations no longer fail because `_cdist_backward` or `_pdist_backward` lacks a derivative ([#188901](https://github.com/pytorch/pytorch/pull/188901))

## Distributed

- Add portable JSON serialization through `DebugMode.save_logs()` and `DebugMode.load_logs()` so distributed execution logs can be compared across separate processes or model configurations ([#185010](https://github.com/pytorch/pytorch/pull/185010))
- Add the public `torch.distributed.set_timeout()` API; the private `_set_pg_timeout()` alias remains available with a deprecation warning ([#187387](https://github.com/pytorch/pytorch/pull/187387))
- Add `torch.distributed.tensor.logspace` for constructing distributed logarithmically spaced tensors ([#186398](https://github.com/pytorch/pytorch/pull/186398))
- Add experimental `torch.distributed.get_backend_impl()` and `ProcessGroup.get_backend()` accessors for custom backend development ([#187494](https://github.com/pytorch/pytorch/pull/187494))
- Add `torch.distributed.tensor.linspace` for constructing distributed linearly spaced tensors ([#187933](https://github.com/pytorch/pytorch/pull/187933))
- Add fault-tolerant reconfiguration and one-sided window operations to the experimental `nccl2` backend ([#189359](https://github.com/pytorch/pytorch/pull/189359), [#189360](https://github.com/pytorch/pytorch/pull/189360))
- Add the experimental `nccl-lazy` backend, which creates per-peer NCCL point-to-point communicators on demand ([#189362](https://github.com/pytorch/pytorch/pull/189362))
- Add the `CheckpointableTensor` protocol so distributed checkpointing can save and load `torch.Tensor` objects exposing `global_shape`, `global_offsets`, `local_offsets`, and `local_sizes` metadata ([#189492](https://github.com/pytorch/pytorch/pull/189492))
- Add an explicit `nccl-legacy` backend and the `TORCH_DIST_USE_NCCL2=1` opt-in for selecting the experimental replacement behind the `nccl` name ([#191272](https://github.com/pytorch/pytorch/pull/191272))
- Allow `ProcessGroupNCCL.Options.config.comm_name` to assign readable communicator names for NCCL logs and profiler tools ([#191001](https://github.com/pytorch/pytorch/pull/191001))
- Add `torchrun --log-line-prefix-template` and a `${hostname}` template variable for identifying the host that emitted each worker log line ([#191265](https://github.com/pytorch/pytorch/pull/191265))
- Allow pipeline schedules to consume explicitly pre-split positional inputs, keyword inputs, and targets through `arg_mbs`, `kwarg_mbs`, and `target_mbs` ([#188500](https://github.com/pytorch/pytorch/pull/188500))
- Add optional shell-completion generation to `torchrun` through `--print-completion` and the `shtab` package ([#191289](https://github.com/pytorch/pytorch/pull/191289))

## Symmetric Memory

- Add XPU support for symmetric-memory operations used by asynchronous tensor parallelism, enabling communication/computation overlap on Intel GPUs ([#185102](https://github.com/pytorch/pytorch/pull/185102))

## Linear Algebra Frontend

- Add `torch.linalg.polar()` for computing `A = U @ H` for matrices with at least as many rows as columns, using a portable SVD implementation and cuSOLVER QDWH acceleration for eligible CUDA inputs ([#185837](https://github.com/pytorch/pytorch/pull/185837))
- Add `torch.linalg.matrix_sqrth` for computing the principal square root of symmetric or Hermitian positive-definite matrices, with support for batched inputs, autograd, `vmap`, and `torch.compile` ([#187987](https://github.com/pytorch/pytorch/pull/187987))
- Add CUDA cuBLASLt support to TunableOp, including controls for the number of heuristic candidates through `torch.cuda.tunable.set_cublaslt_requested_algo_count()` and `PYTORCH_TUNABLEOP_CUBLASLT_REQUESTED_ALGO_COUNT` ([#186270](https://github.com/pytorch/pytorch/pull/186270))

## Profiler

- Memory snapshots can now include CPU pinned-memory allocations by passing `record_pinned_host_memory=True` to `torch.cuda.memory._record_memory_history()` ([#182407](https://github.com/pytorch/pytorch/pull/182407))

  Pinned-memory allocator state and history are available in the snapshot's `host_segments` and `host_traces` fields. Pass `record_cuda=False` to record only pinned host memory; the web memory visualizer does not yet display host-memory data.

- Profiler events now expose Kineto metadata as typed values through `FunctionEvent.metadata` when `expose_kineto_event_metadata=True` is enabled ([#191756](https://github.com/pytorch/pytorch/pull/191756))

  The new dictionary avoids reparsing JSON strings and automatically includes metadata fields supported by the active profiler backend.

## Dynamo

- Add `torch.compiler.nonstrict_trace` as a public API ([#187737](https://github.com/pytorch/pytorch/pull/187737))
- Add the prototype `switch` higher-order op, which selects between N branches by index and mirrors `jax.lax.switch`. It is available as `from torch._higher_order_ops.switch import switch` and lowers to `torch.ops.higher_order.switch`; autograd is not yet supported ([#182902](https://github.com/pytorch/pytorch/pull/182902), [#188374](https://github.com/pytorch/pytorch/pull/188374), [#189028](https://github.com/pytorch/pytorch/pull/189028))
- Declare dynamic shapes explicitly with `ShapesSpec` / `ParamsSpec`, now accepted by strict and non-strict `torch.export.export`, `make_fx(tracing_mode="fake")`, and `torch.compile` through a shared `dynamic_shapes=` keyword ([#185982](https://github.com/pytorch/pytorch/pull/185982), [#186751](https://github.com/pytorch/pytorch/pull/186751), [#187602](https://github.com/pytorch/pytorch/pull/187602), [#187010](https://github.com/pytorch/pytorch/pull/187010))
- Support Dynamo and AOTAutograd tracing of permitted input mutations in the prototype `scan`, `map`, and `switch` higher-order ops when gradients are disabled; Inductor lowering for these mutations is not yet supported ([#186474](https://github.com/pytorch/pytorch/pull/186474), [#187568](https://github.com/pytorch/pytorch/pull/187568), [#188903](https://github.com/pytorch/pytorch/pull/188903))
- Support `torch.cuda.use_mem_pool` inside a compiled region, so allocations in the context - including fallback and extern kernels - are routed to the pool ([#185057](https://github.com/pytorch/pytorch/pull/185057))
- Support calls to `logging.Logger` methods that are explicitly registered in `torch._dynamo.config.reorderable_logging_functions`, so supported positional-argument logging calls run after the compiled region instead of causing graph breaks ([#190840](https://github.com/pytorch/pytorch/pull/190840))

## Inductor

- Add NVGEMM epilogue fusion so supported pointwise operations and output casts can be fused into autotuned matrix multiplications ([#186183](https://github.com/pytorch/pytorch/pull/186183))
- Add NVGEMM autotuning support for `torch.addmm`, including fused bias and supported pointwise epilogues ([#189774](https://github.com/pytorch/pytorch/pull/189774))
- Support FlexAttention FLASH-backend backward graphs that differentiate through the returned log-sum-exp output ([#189784](https://github.com/pytorch/pytorch/pull/189784))
- Add an opt-in `torch._inductor.config.reorder_for_locality_in_training` setting for applying locality-based graph reordering to training graphs ([#186643](https://github.com/pytorch/pytorch/pull/186643))
- Add opt-in CUDA Graph Trees generation cloning through `torch._inductor.config.triton.cudagraph_trees_generation_cloning = "user_visible"`, preserving live user-visible outputs across generations ([#188078](https://github.com/pytorch/pytorch/pull/188078))
- Add `bfloat16` support to `torch.fft` operations and `torch.stft` on CUDA and add `float16`/`bfloat16` support on XPU. Native CUDA `bfloat16` cuFFT execution requires SM80 or newer and power-of-two transform sizes; unsupported CUDA and XPU cases promote to `float32`. CPU FFT continues to reject these low-precision dtypes ([#180766](https://github.com/pytorch/pytorch/pull/180766))
- Add the opt-in `autotuning_inputs` log artifact, enabled with `TORCH_LOGS=autotuning_inputs`, to report Triton autotuning input shapes, dtypes, strides, and scalar values ([#184399](https://github.com/pytorch/pytorch/pull/184399))
- Add Inductor support for the prototype `switch` control-flow operator on CPU and GPU, including dynamic shapes, multiple outputs, and AOTInductor; CUDA graphs remain unsupported for graphs containing `switch` ([#188976](https://github.com/pytorch/pytorch/pull/188976))
- Add dynamic-shape support to `torch.compiler.precompile` for dimensions marked with `torch._dynamo.decorators.mark_unbacked`, allowing one artifact to serve multiple runtime sizes without guarding on the marked dimension ([#189165](https://github.com/pytorch/pytorch/pull/189165))
- Add `torch.compiler.cudagraph_mark_warmup_incomplete()` so code can request another CUDA Graph Trees warmup iteration ([#191386](https://github.com/pytorch/pytorch/pull/191386))

## Ahead-Of-Time Inductor (AOTI)

- Add `AOTInductorModelContainerCreateWithExternalConstants`, allowing callers to construct an AOTInductor model container from caller-owned weight tensors for zero-copy sharing such as CUDA IPC ([#188643](https://github.com/pytorch/pytorch/pull/188643))

  The new C API skips loading constants from the package and leaves ownership with the caller. Existing model-container creation and constant-loading paths are unchanged unless external constants are explicitly provided.

- Support explicit user-defined streams in the AOTInductor C++ wrapper. A compiled region that selects a stream with `torch.cuda.stream(...)` now emits stream-guard code so its kernels run on the requested stream, instead of always running on the default stream ([#182971](https://github.com/pytorch/pytorch/pull/182971))

## Export

- Add the `torch.fx.experimental.dynamic_spec.dynamic_spec` decorator for attaching a dynamic-shape specification to a function or `nn.Module.forward`. `torch.compile`, `torch.export.export`, and `make_fx` automatically use the attached specification; passing a conflicting call-site specification raises an error ([#187639](https://github.com/pytorch/pytorch/pull/187639))

## Composability

- Add a `length` argument to the prototype `torch._higher_order_ops.scan`, allowing a scan to run for a fixed number of steps when `xs=None`, matching the corresponding `jax.lax.scan` usage pattern ([#188349](https://github.com/pytorch/pytorch/pull/188349))
- Add grouped-query attention to the CUDA memory-efficient backend for `torch.nn.functional.scaled_dot_product_attention`, including native grouped key/value heads, implicit multi-query attention broadcasting, and backward support under `vmap` ([#191085](https://github.com/pytorch/pytorch/pull/191085))

## C++ Frontend

- Add `torch::stable::tensor_from_pyobject` and `torch::stable::tensor_to_pyobject` for converting between Python `torch.Tensor` objects and `torch::stable::Tensor` ([#183323](https://github.com/pytorch/pytorch/pull/183323))
- Move the `c10/util/complex_utils.h` helpers and the `ATen/NumericUtils.h` `_isinf` and `_isnan` implementations into the header-only ABI ([#192552](https://github.com/pytorch/pytorch/pull/192552), [#192557](https://github.com/pytorch/pytorch/pull/192557))
- Add stable-ABI `torch::stable::permute` and the dtype overload of `torch::stable::view` ([#192083](https://github.com/pytorch/pytorch/pull/192083))
- Add stable-ABI `torch::stable::Tensor` overloads for `bitwise_and`, `bitwise_or`, `bitwise_left_shift`, `bitwise_right_shift`, `index_select`, `floor_divide`, and `is_pinned` ([#191973](https://github.com/pytorch/pytorch/pull/191973), [#192097](https://github.com/pytorch/pytorch/pull/192097))
- Add `torch::stable::Tensor::has_storage()` ([#189877](https://github.com/pytorch/pytorch/pull/189877))

## Release Engineering

- Python 3.15 and 3.15t (free-threaded) enablement: nightly wheels on Windows ([#190360](https://github.com/pytorch/pytorch/pull/190360)) and macOS arm64 ([#190361](https://github.com/pytorch/pytorch/pull/190361)), ROCm manywheel builds ([#189722](https://github.com/pytorch/pytorch/pull/189722)), and Triton XPU Windows wheels ([#186033](https://github.com/pytorch/pytorch/pull/186033))

## CUDA

- Add a cuBLASLt backend for grouped GEMM on Hopper and Blackwell GPUs with CUDA 13.3 or newer ([#177037](https://github.com/pytorch/pytorch/pull/177037), [#190372](https://github.com/pytorch/pytorch/pull/190372))

  The backend supports `float16` and `bfloat16`, works with `torch.compile` and CUDA Graphs, and is selected by default for eligible `float16` workloads. Set `torch.backends.cuda.matmul.prefer_cublaslt_grouped_gemm = True` to opt into it for `bfloat16`. Matrices and leading dimensions must be 16-byte aligned, so some shapes may require padding and slicing.

- Add `torch.cuda.memory._annotate_tensor()` for attaching metadata to a live CUDA tensor allocation after it is created ([#190575](https://github.com/pytorch/pytorch/pull/190575))

  Each annotation is recorded as a timestamped memory-history event, multiple annotations accumulate without replacing allocation-time metadata, and memory snapshot tools display the annotations alongside the affected allocation. Memory history must be enabled with `torch.cuda.memory._record_memory_history()` for annotations to be observable. Only the native CUDA caching allocator supports annotations.

- Add the public `torch.cuda.graph_annotations` module ([#189417](https://github.com/pytorch/pytorch/pull/189417))

- Annotate backward kernels in `mark_kernels` via `node_creation_hook` ([#191563](https://github.com/pytorch/pytorch/pull/191563))

- Allow multiple memory pools in a single `CUDAGraph` ([#187929](https://github.com/pytorch/pytorch/pull/187929))

- Add CUDA graph support for `torch.while_loop` ([#186055](https://github.com/pytorch/pytorch/pull/186055))

- Add destroy callbacks and object retention to `torch.cuda.CUDAGraph` ([#190582](https://github.com/pytorch/pytorch/pull/190582))

- Add replay start/end hooks to `torch.cuda.CUDAGraph` ([#190602](https://github.com/pytorch/pytorch/pull/190602))

- Add global CUDA graph capture-start/end and replay-start/end hooks, plus `torch.cuda.CUDAGraph.register_capture_start_hook()` ([#192162](https://github.com/pytorch/pytorch/pull/192162))

## cuDNN

- Add cuDNN SDPA support for head dimension 256 on SM90 and SM10.x GPUs with cuDNN newer than 9.22 and cuDNN Frontend 1.24 or newer; backward currently supports only `(d_qk, d_v) = (256, 256)` ([#185553](https://github.com/pytorch/pytorch/pull/185553))

## MPS

- Add native MPS support for binomial sampling ([#187078](https://github.com/pytorch/pytorch/pull/187078))
- Add MPS forward and backward support for `torch.nn.functional.ctc_loss` ([#187716](https://github.com/pytorch/pytorch/pull/187716), [#188187](https://github.com/pytorch/pytorch/pull/188187))
- Add MPS support for `torch.linalg.matrix_exp`, including complex inputs, on macOS 15 or newer ([#188954](https://github.com/pytorch/pytorch/pull/188954))
- Add native MPS Poisson sampling, eliminating its CPU fallback ([#173319](https://github.com/pytorch/pytorch/pull/173319))
- Add native `float32` and `complex64` MPS implementations of `torch.linalg.svd`, `svdvals`, `eigh`, `eigvalsh`, and `lstsq`, while retaining CPU fallbacks for small matrices and matrices that exceed threadgroup memory ([#185954](https://github.com/pytorch/pytorch/pull/185954))

## ROCm

- Add initial, technology-preview support for AMD `gfx1250`; CK SDPA/GEMM, FP8 grouped GEMM, and int4 matrix multiplication remain unsupported ([#187548](https://github.com/pytorch/pytorch/pull/187548), [#188597](https://github.com/pytorch/pytorch/pull/188597), [#188612](https://github.com/pytorch/pytorch/pull/188612))
- Enable hipFile on Linux with ROCm 7.14 or newer ([#191069](https://github.com/pytorch/pytorch/pull/191069), [#192803](https://github.com/pytorch/pytorch/pull/192803))

## XPU

- Add FP8 blockwise scaling support for MXFP8/MXFP4/NVFP4 recipes to `torch._scaled_mm` and `torch._scaled_mm_v2` on XPU ([#181726](https://github.com/pytorch/pytorch/pull/181726), [#181727](https://github.com/pytorch/pytorch/pull/181727), [#187315](https://github.com/pytorch/pytorch/pull/187315))
- Add XPU Graph native recording mode on non-PVC devices when PyTorch is built with oneAPI 2026.1 or newer ([#188874](https://github.com/pytorch/pytorch/pull/188874))
- Add `torch.xpu.list_gpu_processes` to query per-process GPU memory usage on XPU ([#185192](https://github.com/pytorch/pytorch/pull/185192))

# Improvements

## Python Frontend

- Allow `torch.quantile` and `torch.nanquantile` to process `float32` and `float64` inputs larger than `2**24` elements on devices with `float64` support by computing ranks in `float64` ([#187574](https://github.com/pytorch/pytorch/pull/187574))

## torch.nn

- Allow the chunked path of `torch.nn.functional.linear_cross_entropy` to handle probability targets for `reduction="mean"` and `reduction="sum"` when the target dtype matches the input and the target does not require gradients ([#187053](https://github.com/pytorch/pytorch/pull/187053))
- Improve static typing for `torch.nn.Sequential` indexing so integer keys resolve to `Module` and slices resolve to `Sequential` ([#187758](https://github.com/pytorch/pytorch/pull/187758))
- Add the documented `memory_format` overload to `torch.nn.Module.to()` so static type checkers accept calls such as `module.to(memory_format=torch.channels_last)` ([#185117](https://github.com/pytorch/pytorch/pull/185117))

## Optimizer

- Add the `"spectral_unclamped"` scaling option to the `adjust_lr_fn` parameter of `torch.optim.Muon` ([#187402](https://github.com/pytorch/pytorch/pull/187402))
- Add a `maximize` parameter to `torch.optim.LBFGS` ([#187309](https://github.com/pytorch/pytorch/pull/187309))
- Make `torch.optim.LBFGS.step()` a no-op for an empty parameter group ([#191666](https://github.com/pytorch/pytorch/pull/191666))

## Distributed

- Expand `DTensor` sharding strategies for matrix, attention, sorting, scanning, softmax, and related operations ([#186667](https://github.com/pytorch/pytorch/pull/186667), [#179068](https://github.com/pytorch/pytorch/pull/179068))
- Allow custom Python `ProcessGroup` implementations to use `batch_isend_irecv` and the coalescing manager ([#186964](https://github.com/pytorch/pytorch/pull/186964))
- Improve the Flight Recorder diagnostic emitted when a `TCPStore` check fails ([#187191](https://github.com/pytorch/pytorch/pull/187191))
- Allow pipeline parallel stages to use separate forward and backward point-to-point communicators, reducing cross-batch ordering hazards ([#186173](https://github.com/pytorch/pytorch/pull/186173))
- Add fault-tolerant reconfiguration support to Gloo process groups ([#187381](https://github.com/pytorch/pytorch/pull/187381))
- Make compile-on-one-rank graphs portable across ranks by replacing baked accelerator device indices with a runtime current-device operation ([#186892](https://github.com/pytorch/pytorch/pull/186892))
- Expand active `DTensor` single-dimension strategies for tensor operations ([#186754](https://github.com/pytorch/pytorch/pull/186754))
- Auto-qualify bare backend names and pass process-group options through custom TorchComms backend creation ([#187856](https://github.com/pytorch/pytorch/pull/187856))
- Add complete collective coverage to custom Python process groups, including single-tensor gather/scatter and the remaining point-to-point and collective operations ([#188548](https://github.com/pytorch/pytorch/pull/188548), [#188570](https://github.com/pytorch/pytorch/pull/188570))
- Make TorchElastic NUMA binding and `ShardedTensor` device transfers work with accelerator backends beyond CUDA ([#185266](https://github.com/pytorch/pytorch/pull/185266), [#187939](https://github.com/pytorch/pytorch/pull/187939))
- Use generic collective coalescing when aborting process groups so third-party backends can avoid multi-communicator teardown deadlocks ([#189770](https://github.com/pytorch/pytorch/pull/189770))
- Mark CUDA symmetric-memory allocations as GPUDirect RDMA capable on supported systems ([#189941](https://github.com/pytorch/pytorch/pull/189941))
- Add communicator memory suspend/resume support to the experimental `nccl2` backend ([#189361](https://github.com/pytorch/pytorch/pull/189361))
- Allow unknown device-qualified TorchComms backend names to register as custom backends without requiring manual changes to internal backend maps ([#191034](https://github.com/pytorch/pytorch/pull/191034))
- Add eager `split_group` support, complete `Work` semantics, nonblocking communicators, and uneven list collectives to the experimental `nccl2` backend ([#190943](https://github.com/pytorch/pytorch/pull/190943), [#191517](https://github.com/pytorch/pytorch/pull/191517), [#191528](https://github.com/pytorch/pytorch/pull/191528), [#191542](https://github.com/pytorch/pytorch/pull/191542))
- Include `nccl-lazy` pair communicators in error reporting, suspend/resume operations, and memory statistics, and expand its shared backend coverage ([#191553](https://github.com/pytorch/pytorch/pull/191553), [#191556](https://github.com/pytorch/pytorch/pull/191556))
- Add memory-pool registration and deregistration support to the experimental `nccl2` backend ([#192108](https://github.com/pytorch/pytorch/pull/192108))
- Add per-process-group collective sequence numbers and accurate split-group membership metadata to `nccl2` profiler traces ([#192114](https://github.com/pytorch/pytorch/pull/192114), [#192115](https://github.com/pytorch/pytorch/pull/192115))
- Support non-overlapping final-spatial-dimension `DTensor` sharding for `Conv1d`, `Conv2d`, and `Conv3d` forward and backward ([#192147](https://github.com/pytorch/pytorch/pull/192147))
- Pass process-group descriptions and names to NCCL's `commName` field while preserving user-specified communicator names ([#192487](https://github.com/pytorch/pytorch/pull/192487))
- Support `DTensor` redistribution from final-dimension sharding to `Partial("sum")` ([#191828](https://github.com/pytorch/pytorch/pull/191828))

## Distributed (c10d)

- Upgrade NCCL to 2.30.7 for CUDA 13.0 and CUDA 13.2 builds ([#187528](https://github.com/pytorch/pytorch/pull/187528))
- Enable Inductor's `simple_overlap` scheduler pass by default for compiled distributed workloads, moving collective starts earlier and waits later without reordering collectives or increasing peak memory ([#184235](https://github.com/pytorch/pytorch/pull/184235), [#184240](https://github.com/pytorch/pytorch/pull/184240))

## Linear Algebra Frontend

- Add backward support for `torch.linalg.polar` on CPU, CUDA, and MPS ([#189732](https://github.com/pytorch/pytorch/pull/189732))
- Enable `torch.linalg.eig` on ROCm 7.14 or newer through hipSOLVER's generic `Xgeev` API, and update generated linear-algebra tests to recognize hipSOLVER implementations that do not require MAGMA ([#188720](https://github.com/pytorch/pytorch/pull/188720))
- Allow `torch.backends.cuda.preferred_blas_library("ck")` to select the CK GEMM backend on ROCm `gfx90a` devices by separating GEMM support from CK attention support ([#187267](https://github.com/pytorch/pytorch/pull/187267))
- Expand ROCm backend coverage for `torch.linalg.eig`, `torch.linalg.ldl_solve`, `torch.linalg.solve`, and `torch.linalg.solve_triangular` through hipSOLVER and hipBLAS paths ([#185557](https://github.com/pytorch/pytorch/pull/185557))

## Profiler

- Record XPU profiler overhead as `OVERHEAD` activities, making collection costs visible on a dedicated track in exported traces ([#187835](https://github.com/pytorch/pytorch/pull/187835))

## FX

- Allow `split_const_subgraphs()` callers to supply an `is_impure_node` callback so destination-passing operations and other side-effecting nodes are preserved during dead-code elimination ([#190716](https://github.com/pytorch/pytorch/pull/190716))
- Make `get_source_partitions()` return input nodes, output nodes, and parameters in deterministic graph order ([#188965](https://github.com/pytorch/pytorch/pull/188965))

## Dynamo

- Reuse a traced region in `torch.compiler.nested_compile_region` when its arguments contain source-backed user-defined objects, and accept only source-backed `nn.Module` arguments (previously, sourceless modules were reused without checks) ([#192003](https://github.com/pytorch/pytorch/pull/192003))
- Extend `torch.compiler.nested_compile_region` reuse to regions with symbolic-shape inputs and pytree arguments such as dataclasses and namedtuples, which previously retraced the region on every call ([#191806](https://github.com/pytorch/pytorch/pull/191806), [#191817](https://github.com/pytorch/pytorch/pull/191817))
- Support `torch.compile` applied directly to a `staticmethod` ([#190673](https://github.com/pytorch/pytorch/pull/190673))
- Make `Module.compile()` compile built-in leaf modules such as `Conv2d`, which previously produced no capturable frame ([#185722](https://github.com/pytorch/pytorch/pull/185722))
- Support cross-device `tensor.data = tensor.data.to(device)` under `torch.compile`, matching eager's metadata swap ([#185980](https://github.com/pytorch/pytorch/pull/185980))
- Trace raw unbacked `SymInt` inputs in non-strict tracing, preserving symbol provenance from an outer fake-tensor trace ([#187273](https://github.com/pytorch/pytorch/pull/187273))
- Support a scan dimension of length zero in `scan` and `associative_scan` ([#188348](https://github.com/pytorch/pytorch/pull/188348))
- Trace `Tensor` methods reached through `super()`, for example `super().unflatten(...)` ([#183850](https://github.com/pytorch/pytorch/pull/183850))
- Constant-fold the MPS and MTIA availability predicates and add trace rules for `torch.mps.is_available` / `torch.mtia.is_available`, so backend probes no longer graph break ([#185277](https://github.com/pytorch/pytorch/pull/185277))
- Accept `out=` tensors in `channels_last` and `channels_last_3d` layouts instead of graph breaking ([#185089](https://github.com/pytorch/pytorch/pull/185089))
- Allow `torch.compile` to handle `DistributedDataParallel` objects when source information is unavailable ([#187210](https://github.com/pytorch/pytorch/pull/187210))
- Trace `dist.reduce_scatter` ([#190429](https://github.com/pytorch/pytorch/pull/190429))
- Support constructing `torch.backends.cuda.SDPAParams` under `fullgraph=True` ([#190839](https://github.com/pytorch/pytorch/pull/190839))
- Add a trace rule for `torch.linalg.polar` (and its Inductor lowering) so it can be captured ([#188537](https://github.com/pytorch/pytorch/pull/188537))
- Make `has_triton()` query registered device interfaces so out-of-tree accelerator backends are recognized without monkeypatching ([#190324](https://github.com/pytorch/pytorch/pull/190324))
- Allow `torch._check` to accept a module-level function or any constant as its message, matching eager behavior ([#188576](https://github.com/pytorch/pytorch/pull/188576))
- Support `key=` and `default=` in `min()`/`max()`, the `base` argument of `int()`, and `oct()`/`hex()`/`bin()` on objects implementing `__index__` ([#191401](https://github.com/pytorch/pytorch/pull/191401), [#191402](https://github.com/pytorch/pytorch/pull/191402), [#191408](https://github.com/pytorch/pytorch/pull/191408))
- Apply `__index__` coercion to `range()` arguments and slice members, matching CPython ([#187129](https://github.com/pytorch/pytorch/pull/187129))
- Support constructing `object()`, empty `tuple` subclasses (`MyTuple()`), and `collections.deque` subclasses inside a compiled region ([#186976](https://github.com/pytorch/pytorch/pull/186976), [#189021](https://github.com/pytorch/pytorch/pull/189021), [#187588](https://github.com/pytorch/pytorch/pull/187588))
- Trace `list.sort` with non-constant key comparisons and `functools.cmp_to_key` ([#185999](https://github.com/pytorch/pytorch/pull/185999))
- Return mutable lists from `str.split`, `str.rsplit`, and `str.splitlines`, so the result can be sorted or appended to inside a compiled region ([#188306](https://github.com/pytorch/pytorch/pull/188306))
- Support unbound rich-comparison dunders on built-in types, for example `complex.__eq__(1 + 1j, 2)` ([#191406](https://github.com/pytorch/pytorch/pull/191406))
- Support `operator.setitem` and `operator.delitem` on lists, dicts, tensors, and NumPy arrays ([#190259](https://github.com/pytorch/pytorch/pull/190259))
- Make `callable()` follow the type's `tp_call` slot, and make calls to non-callable objects raise `TypeError: 'X' object is not callable` instead of an internal error ([#186971](https://github.com/pytorch/pytorch/pull/186971))
- Extend `itertools` coverage: bounded `repeat`, `count(start=, step=)` and its `repr`, and support for `permutations`, `combinations`, `combinations_with_replacement`, and `batched` ([#188080](https://github.com/pytorch/pytorch/pull/188080), [#189022](https://github.com/pytorch/pytorch/pull/189022), [#186937](https://github.com/pytorch/pytorch/pull/186937), [#187080](https://github.com/pytorch/pytorch/pull/187080), [#186240](https://github.com/pytorch/pytorch/pull/186240))
- Support `__length_hint__` on set and dict-view iterators ([#188081](https://github.com/pytorch/pytorch/pull/188081))
- Improve `collections.deque` fidelity: re-initialization through `__init__`, `copy()` / `copy.copy()` preserving `maxlen`, `rotate()`, iterators that detect mutation during iteration, and `AttributeError` on attribute writes ([#187128](https://github.com/pytorch/pytorch/pull/187128), [#188220](https://github.com/pytorch/pytorch/pull/188220), [#191403](https://github.com/pytorch/pytorch/pull/191403), [#189052](https://github.com/pytorch/pytorch/pull/189052), [#191405](https://github.com/pytorch/pytorch/pull/191405))
- Support `range_iterator.__setstate__` / `__length_hint__`, and fall back to `==` comparison for non-integer operands of `x in range(...)` ([#188221](https://github.com/pytorch/pytorch/pull/188221), [#189575](https://github.com/pytorch/pytorch/pull/189575))
- Improve dict and set fidelity: do not re-hash keys when building from an existing dict/set, use per-element rich comparison for sequence membership, run a user-defined `__eq__` for dict/set key comparison, normalize `set.remove`/`set.discard` keys, read set subclasses through the base `set` APIs, and report the concrete set type from `hasattr` ([#186759](https://github.com/pytorch/pytorch/pull/186759), [#186760](https://github.com/pytorch/pytorch/pull/186760), [#186669](https://github.com/pytorch/pytorch/pull/186669), [#186761](https://github.com/pytorch/pytorch/pull/186761), [#186763](https://github.com/pytorch/pytorch/pull/186763), [#188908](https://github.com/pytorch/pytorch/pull/188908))
- Support the dict-view `.mapping` attribute, non-`str` keys assigned through an instance `__dict__`, CPython's clear-then-extend `list.__init__`, and CPython's `__dict__` re-insertion order after a `pop` ([#187586](https://github.com/pytorch/pytorch/pull/187586), [#187587](https://github.com/pytorch/pytorch/pull/187587), [#187583](https://github.com/pytorch/pytorch/pull/187583), [#187584](https://github.com/pytorch/pytorch/pull/187584))
- Make `str()` and `repr()` follow CPython's `tp_str`/`tp_repr` fallbacks, including `repr()` and integer arithmetic on the `id()`/`hash()` values of an object created inside the compiled region ([#187775](https://github.com/pytorch/pytorch/pull/187775), [#188909](https://github.com/pytorch/pytorch/pull/188909), [#189053](https://github.com/pytorch/pytorch/pull/189053))
- Make the `object.__reduce_ex__` polyfill faithful for objects with `__slots__` or `__getnewargs__`, so `copy.copy`/`copy.deepcopy` of a namedtuple no longer graph breaks ([#189576](https://github.com/pytorch/pytorch/pull/189576))
- Support custom attributes on exceptions and exception-specific attributes such as `StopIteration.value`, `AttributeError.name`/`.obj`, and `NameError.name` ([#188105](https://github.com/pytorch/pytorch/pull/188105), [#189024](https://github.com/pytorch/pytorch/pull/189024))
- Support subgenerator `.throw()` / `.close()` and track generator attribute mutations for correct closure handling ([#188825](https://github.com/pytorch/pytorch/pull/188825), [#188834](https://github.com/pytorch/pytorch/pull/188834))
- Route module-level `random.random` and `random.seed` calls through the traced RNG instead of graph breaking ([#188235](https://github.com/pytorch/pytorch/pull/188235), [#188083](https://github.com/pytorch/pytorch/pull/188083))
- Add text-encoding support so `open()`, `pathlib.Path.read_text()`/`write_text()`, and `tempfile.NamedTemporaryFile` no longer graph break under `fullgraph=True` ([#189984](https://github.com/pytorch/pytorch/pull/189984))
- Add the `**` / `**=`, `@` / `@=`, and `~` operator slots ([#186296](https://github.com/pytorch/pytorch/pull/186296), [#189585](https://github.com/pytorch/pytorch/pull/189585), [#185641](https://github.com/pytorch/pytorch/pull/185641))
- Improve diagnostics: dedicated graph-break messages for direct `torch._dynamo.disable`/`torch.compiler.disable` calls, clearer `Parameter`-vs-`Tensor` guard mismatch text in recompilation logs, an actionable hint for in-place views on graph inputs, closest-match suggestions for a mistyped backend name, graph breaks on exceptions based on whether user code would catch them, and observed-exception stacks preserved across a bare `raise` ([#185763](https://github.com/pytorch/pytorch/pull/185763), [#185083](https://github.com/pytorch/pytorch/pull/185083), [#185903](https://github.com/pytorch/pytorch/pull/185903), [#189333](https://github.com/pytorch/pytorch/pull/189333), [#182972](https://github.com/pytorch/pytorch/pull/182972), [#185508](https://github.com/pytorch/pytorch/pull/185508))
- Support TVM's relax frontend in the `tvm` backend, with tuning selected via `options={"pipeline": ...}` ([#189010](https://github.com/pytorch/pytorch/pull/189010), [#189638](https://github.com/pytorch/pytorch/pull/189638))

## Inductor

- Make missing CUDA and ROCm warp-size metadata explicit so Inductor skips heuristics that require it instead of silently assuming a warp size of 32. Raise when a code path requires a concrete warp size but the metadata is unavailable ([#183014](https://github.com/pytorch/pytorch/pull/183014))
- Make autotuning subprocesses honor `ZE_AFFINITY_MASK` on XPU while preserving `CUDA_VISIBLE_DEVICES` behavior on CUDA ([#183436](https://github.com/pytorch/pytorch/pull/183436))
- Add a dedicated `XPUCompileError` for SYCL compilation failures and clear loaded XPU libraries when the code cache is reset ([#183530](https://github.com/pytorch/pytorch/pull/183530))
- Make partitioned-scatter selection memory- and contention-aware, enable it by default on ROCm, and replace the removed `partitioned_scatter_memory_budget` setting with memory-headroom controls; set `partitioned_scatter_enabled = False` to opt out ([#184365](https://github.com/pytorch/pytorch/pull/184365))
- Support ROCm Composable Kernel GEMM templates when compiling with the JIT C++ wrapper ([#185505](https://github.com/pytorch/pytorch/pull/185505))
- Fuse decomposed SiLU activations into CUTLASS GEMM epilogues and improve XPU GEMM template compatibility ([#186197](https://github.com/pytorch/pytorch/pull/186197), [#186198](https://github.com/pytorch/pytorch/pull/186198))
- Accept multiword compiler commands such as `CXX="zig c++"` when building Inductor-generated C++ code on POSIX systems ([#186336](https://github.com/pytorch/pytorch/pull/186336))
- Add Intel Arc B580 and Arc Pro B70 specifications to Inductor's device-performance metadata ([#187308](https://github.com/pytorch/pytorch/pull/187308))
- Lower `uniform_` and `aten.uniform` through a native decomposition instead of always falling back to eager execution ([#187887](https://github.com/pytorch/pytorch/pull/187887))
- Enable Triton indirect-indexing assertions on ROCm with Triton 3.7 or newer, improving diagnostics for out-of-bounds accesses ([#188075](https://github.com/pytorch/pytorch/pull/188075))
- Allow XPU's static launcher to accept host and shared USM pointers recognized by the driver instead of requiring device memory ([#188240](https://github.com/pytorch/pytorch/pull/188240))
- Extend manual communication-overlap scheduling to bucket and defer waits for DDP and HSDP `all_reduce` operations ([#188472](https://github.com/pytorch/pytorch/pull/188472))
- Support grouped and FP8-scaled grouped GEMM Triton lowering on compatible ROCm hardware ([#188600](https://github.com/pytorch/pytorch/pull/188600), [#188742](https://github.com/pytorch/pytorch/pull/188742))
- Apply per-region Inductor configuration patches throughout nested-region compilation and allow separate forward and backward patches ([#189320](https://github.com/pytorch/pytorch/pull/189320), [#190068](https://github.com/pytorch/pytorch/pull/190068))
- Decompose semi-structured sparse CUTLASS matrix multiplication so Inductor can lower and autotune the underlying operation ([#189366](https://github.com/pytorch/pytorch/pull/189366))
- Report stuck compile workers and their current phase in structured `tlparse` traces through the configurable compile-worker watchdog ([#189485](https://github.com/pytorch/pytorch/pull/189485), [#189486](https://github.com/pytorch/pytorch/pull/189486))
- Prefer device datasheet bandwidth for Inductor's bandwidth-driven heuristics and add Intel Data Center GPU Max 1100 metadata ([#189819](https://github.com/pytorch/pytorch/pull/189819))
- Lower `torch.float8_e8m0fnu` conversions directly on CPU and CUDA instead of relying on fallback conversion code ([#190593](https://github.com/pytorch/pytorch/pull/190593))
- Expand NVGEMM epilogue fusion to pointwise operations, multiple outputs, and grouped reductions, including scaled and centered outputs ([#190643](https://github.com/pytorch/pytorch/pull/190643), [#190808](https://github.com/pytorch/pytorch/pull/190808), [#190809](https://github.com/pytorch/pytorch/pull/190809), [#190810](https://github.com/pytorch/pytorch/pull/190810), [#190813](https://github.com/pytorch/pytorch/pull/190813), [#190817](https://github.com/pytorch/pytorch/pull/190817), [#190823](https://github.com/pytorch/pytorch/pull/190823))
- Suppress empty generated-code dumps from `TORCH_LOGS=output_code` during autotuning ([#191381](https://github.com/pytorch/pytorch/pull/191381))

## Ahead-Of-Time Inductor (AOTI)

- Support `int[]`, `SymInt[]`, and optional integer-list arguments in AOTI eager cache keys, enabling cached compilation for operators such as `new_zeros`, `mean.dim`, and `count_nonzero.dim_IntList` ([#187360](https://github.com/pytorch/pytorch/pull/187360))
- Support lazy autotuning when compiling with the AOTInductor dual-wrapper, so Triton autotuning is deferred to a first JIT pass rather than being done during ahead-of-time compilation ([#184735](https://github.com/pytorch/pytorch/pull/184735))
- Support `torch.cond` and `torch.while_loop` when compiling with the AOTInductor dual-wrapper ([#184736](https://github.com/pytorch/pytorch/pull/184736))
- Add an `AOTI_LOG_LOADING` environment variable. When it is set, AOTInductor prints timing and diagnostic messages for each stage of constant loading, prefixed with `[AOTI_LOAD]`, without requiring a rebuild ([#186309](https://github.com/pytorch/pytorch/pull/186309))
- Check the error codes returned by the generated `scatter`, `index_put`, `clone`, and tensor-handle shim calls, so a failure inside one of these fallbacks raises an error instead of being silently ignored ([#190909](https://github.com/pytorch/pytorch/pull/190909), [#190910](https://github.com/pytorch/pytorch/pull/190910))

## Export

- Support serializing nested integer and floating-point list arguments, including empty nested lists, for custom operators in exported programs ([#189424](https://github.com/pytorch/pytorch/pull/189424))
- Support `ObjectSpec`, `SeqSpec`, and `DictSpec` container types when using shape specifications with strict export ([#186167](https://github.com/pytorch/pytorch/pull/186167))

## Composability

- Add `torch.linalg.vector_norm` to the core ATen decomposition table used by `ExportedProgram.run_decompositions()`, including correct `dim=()` handling ([#185735](https://github.com/pytorch/pytorch/pull/185735))
- Allow out-of-tree backends to define additional `out_dtype` combinations for `torch.mm`, `torch.bmm`, and `torch.baddbmm` under fake/meta tracing; CUDA and XPU restrictions remain unchanged ([#187096](https://github.com/pytorch/pytorch/pull/187096))
- Provide a targeted dynamic-shape error when a data-dependent expression conflicts with a `dynamic_spec` constraint ([#187143](https://github.com/pytorch/pytorch/pull/187143))

## Foreach

- Use the nvmath `_foreach_mm` path only when the loaded cuBLASLt version supports grouped GEMM ([#189757](https://github.com/pytorch/pytorch/pull/189757))

## ONNX

- Preserve constants introduced during export decompositions so `ExportedProgram` remains valid when ONNX symbolic operations are inserted during retracing ([#185090](https://github.com/pytorch/pytorch/pull/185090))

## C++ Frontend

- Enable stable-ABI error-message retrieval dynamically when the required runtime shim is available ([#183823](https://github.com/pytorch/pytorch/pull/183823))
- Treat `-Wdeprecated-declarations` diagnostics as warnings rather than errors in `c10`, ATen, and LibTorch builds ([#189948](https://github.com/pytorch/pytorch/pull/189948))
- Reject negative CUDA storage-resize requests instead of wrapping them to huge `size_t` allocation requests ([#190652](https://github.com/pytorch/pytorch/pull/190652))

## Release Engineering

- Enable ROCm 7.14 nightly manywheel builds through TheRock wheels ([#190276](https://github.com/pytorch/pytorch/pull/190276)) and add `libatomic` to the manywheel builder image ([#192254](https://github.com/pytorch/pytorch/pull/192254))
- Update the bundled Triton to 3.8.0 ([#188251](https://github.com/pytorch/pytorch/pull/188251), [#190349](https://github.com/pytorch/pytorch/pull/190349))
- Add full CUDA 13.2 CI coverage for stable-version configurations ([#190641](https://github.com/pytorch/pytorch/pull/190641)), Inductor, H100, B200, and `DTensor` ([#190948](https://github.com/pytorch/pytorch/pull/190948)), plus B200 smoke tests ([#191705](https://github.com/pytorch/pytorch/pull/191705))
- Upgrade the XPU support package to 2026.1 ([#189593](https://github.com/pytorch/pytorch/pull/189593))
- Update OpenBLAS to v0.3.34 ([#190314](https://github.com/pytorch/pytorch/pull/190314))
- Update the Arm Compute Library (ACL) version used by aarch64 builds ([#191316](https://github.com/pytorch/pytorch/pull/191316))
- Relax the `nvidia-nvjitlink-cu12` runtime dependency of CUDA 12 wheels so it no longer forces an exact version ([#186958](https://github.com/pytorch/pytorch/pull/186958))

## CUDA

- Add CUDA compute capability 10.7 (`sm_107`) awareness for NVIDIA Rubin GPUs with CUDA 13.4 or newer in extension builds and Inductor code generation ([#190654](https://github.com/pytorch/pytorch/pull/190654))
- Update CUDA compatibility checks for Jetson devices using SBSA binaries with CUDA 13.2 or newer ([#186285](https://github.com/pytorch/pytorch/pull/186285))
- Trim the `cudaMallocAsync` pool and retry once before raising an out-of-memory error ([#188110](https://github.com/pytorch/pytorch/pull/188110))
- Improve CUDA errors by including excerpts from CUDA logs ([#191334](https://github.com/pytorch/pytorch/pull/191334))
- Add `torch.float16` and `torch.bfloat16` support to `torch.angle` on CUDA ([#191301](https://github.com/pytorch/pytorch/pull/191301))

## cuDNN

- Upgrade the CUDA 12.8, 12.9, and 13.x wheels to cuDNN 9.24 and re-enable convolution engine 5 after its nondeterminism issue was fixed ([#187091](https://github.com/pytorch/pytorch/pull/187091), [#189483](https://github.com/pytorch/pytorch/pull/189483))

## CPU (x86)

- Add `Half` support to the eager `torch.polar` kernel ([#192311](https://github.com/pytorch/pytorch/pull/192311))
- Allow `xeon/run_cpu.py` to accept multiple values for `--ncores-per-instance` ([#169916](https://github.com/pytorch/pytorch/pull/169916))

## MPS

- Support `return_aux(max_scores=True)` in MPS `flex_attention` forward ([#188362](https://github.com/pytorch/pytorch/pull/188362))
- Support `SymInt` captures in MPS `flex_attention` score and mask functions, including dynamically shaped compiled graphs ([#188403](https://github.com/pytorch/pytorch/pull/188403))
- Add MPS support for `torch.linalg.polar` ([#189701](https://github.com/pytorch/pytorch/pull/189701))
- Support MPS `torch.nonzero` on tensors containing more than `2**32` elements ([#188816](https://github.com/pytorch/pytorch/pull/188816))
- Add complex MPS support for Cholesky factorization ([#191836](https://github.com/pytorch/pytorch/pull/191836))
- Support key/value batch broadcasting and returning log-sum-exp values from MPS `flex_attention` ([#187722](https://github.com/pytorch/pytorch/pull/187722), [#187768](https://github.com/pytorch/pytorch/pull/187768))
- Add MPS backward support for antialiased bilinear and bicubic 2D upsampling ([#188819](https://github.com/pytorch/pytorch/pull/188819))
- Add complex MPS support to `torch.nan_to_num` and correctly resize empty `out=` tensors ([#189489](https://github.com/pytorch/pytorch/pull/189489))
- Add MPS `torch.geqrf` support and align the MPS `torch.linalg.qr` implementation with other backends ([#189192](https://github.com/pytorch/pytorch/pull/189192))

## ROCm

- Add `torch.utils.hipify` mappings for the `cublasMath_t` type, its enum values, and `CUBLAS_COMPUTE_16F`, so HIP-ported extensions that call `cublasGemmEx` with `CUBLAS_COMPUTE_16F` or set a cuBLAS math mode hipify cleanly without per-project aliases ([#187752](https://github.com/pytorch/pytorch/pull/187752))
- Migrate from `rocm_smi` to `amd_smi` ([#190014](https://github.com/pytorch/pytorch/pull/190014))
- Preload TheRock ROCm dependencies so wheels are self-contained ([#188454](https://github.com/pytorch/pytorch/pull/188454))
- Enable Inductor lowering for FMA on ROCm ([#187165](https://github.com/pytorch/pytorch/pull/187165))

## XPU

- Add device-wide synchronization support on XPU ([#191900](https://github.com/pytorch/pytorch/pull/191900))
- Add IPC memory handle sharing support to `XPUCachingAllocator` on XPU ([#188789](https://github.com/pytorch/pytorch/pull/188789))
- Support head dimensions 32 and 256 for XPU FlashAttention ([#180646](https://github.com/pytorch/pytorch/pull/180646))
- Enable TF32 `fpmath` mode for XPU deconvolution, matching the existing convolution behavior ([#185606](https://github.com/pytorch/pytorch/pull/185606))
- Fix XPU graph-capture hangs by deferring memory-pool block handling until capture ends ([#187931](https://github.com/pytorch/pytorch/pull/187931))
- Refine `clock_rate` and `power_draw` device property queries through `pyzes` 0.1.2 ([#188248](https://github.com/pytorch/pytorch/pull/188248), [#188256](https://github.com/pytorch/pytorch/pull/188256))
- Add experimental C++ XPU device properties for Xe topology, including `xe_stack_count`, `xe_regions_per_stack`, `xe_clusters_per_region`, and `xe_cores_per_cluster` ([#191477](https://github.com/pytorch/pytorch/pull/191477))
- Support BMG-G31 architecture compilation for the SYCL-TLA CUTLASS backend on XPU ([#187040](https://github.com/pytorch/pytorch/pull/187040))
- Enable the XPU scope profiler to gather hardware metrics through the Kineto plugin ([#165766](https://github.com/pytorch/pytorch/pull/165766))
- Make Inductor use XPU's device-specific TF32 setting so compiled matrix multiplication matches eager behavior ([#187948](https://github.com/pytorch/pytorch/pull/187948))
- Enable SYCL native fast-math approximations for `exp`, `log`, `log1p`, and `tan` on XPU ([#176262](https://github.com/pytorch/pytorch/pull/176262))

## Sparse Frontend

- Add CUDA `float16` and `bfloat16` support to `torch.sparse.sampled_addmm`, including supported sparse-CSR backward paths ([#187681](https://github.com/pytorch/pytorch/pull/187681))
- Add sparse COO dispatch for `torch.linalg.vector_norm`, allowing it to replace deprecated `torch.norm` calls on sparse COO tensors ([#185309](https://github.com/pytorch/pytorch/pull/185309))

## torch.func

- Allow `torch.vmap` to handle the scalar overload of `torch.searchsorted` ([#188974](https://github.com/pytorch/pytorch/pull/188974))
- Expand `torch.vmap` coverage for copy-view operations by routing them through existing batching rules ([#187256](https://github.com/pytorch/pytorch/pull/187256))
- Add a batching rule for `torch.repeat_interleave` when `repeats` is batched; callers must provide a common `output_size` because per-example output lengths are data-dependent ([#187702](https://github.com/pytorch/pytorch/pull/187702))
- Add a native batching rule for in-place `Tensor.masked_fill_()`, avoiding the slow fallback and its performance warning under `torch.vmap` ([#175513](https://github.com/pytorch/pytorch/pull/175513))
- Expand scalar fill and comparison support under `torch.vmap`, including accelerator placement for scalar operands ([#189176](https://github.com/pytorch/pytorch/pull/189176))

# Bug Fixes

## Python Frontend

- Fix `torch.arange` computing the wrong length for fractional arguments with an integer output dtype because it truncates those arguments too early ([#185812](https://github.com/pytorch/pytorch/pull/185812))
- Raise a clear unsupported-operation error for dense tensor factories targeting `device="mkldnn"` instead of triggering an internal assertion ([#185711](https://github.com/pytorch/pytorch/pull/185711))

## Dataloader Frontend

- Release CUDA IPC-backed dataset storage when `DataLoader` workers exit, preventing producer-side IPC references and allocations from being retained indefinitely ([#190485](https://github.com/pytorch/pytorch/pull/190485))

## torch.nn

- Enable eligible fused scaled dot-product attention backends for dense rank-3 inputs on CPU, CUDA/ROCm, and XPU instead of always falling back to the math implementation ([#192271](https://github.com/pytorch/pytorch/pull/192271))

  Rank-3 inputs are normalized to rank 4 with a singleton batch dimension before backend selection. This fixes fused execution for rank-3 and vmapped inputs, but automatic backend selection can change floating-point numerics, dropout RNG consumption, whether the result is a view, and higher-order-gradient support. Fused CUDA backends do not support the second derivatives provided by the math backend; code that depends on those semantics should explicitly select the math backend.

  ```python
  from torch.nn.attention import SDPBackend, sdpa_kernel

  with sdpa_kernel(backends=[SDPBackend.MATH]):
      output = torch.nn.functional.scaled_dot_product_attention(
          query, key, value
      )
  ```

- Reject `norm_type=0` in functional and module Lp pooling APIs with a descriptive `ValueError` instead of a deferred `ZeroDivisionError` ([#187861](https://github.com/pytorch/pytorch/pull/187861))

- Fix failures in memory-efficient scaled dot-product attention backward after `torch.autograd.graph.save_on_cpu()` changes an attention mask's aligned strides ([#188246](https://github.com/pytorch/pytorch/pull/188246))

- Fix a CUDA illegal memory access in memory-efficient scaled dot-product attention backward when only the floating-point attention mask requires gradients ([#188302](https://github.com/pytorch/pytorch/pull/188302))

- Make the cuDNN CTC loss backend correctly zero infinite losses and their gradients when `zero_infinity=True` ([#176911](https://github.com/pytorch/pytorch/pull/176911))

- Validate each output dimension for `replication_pad2d` and `replication_pad3d` so excessive negative padding raises a clear error instead of attempting to create a negative-sized tensor ([#184254](https://github.com/pytorch/pytorch/pull/184254))

- Fix silently incorrect CUDA gradients from channels-last `avg_pool2d` when padding is nonzero ([#188345](https://github.com/pytorch/pytorch/pull/188345))

- Make CPU eager and decomposed `torch.nn.functional.softshrink` cast scalar `lambd` values consistently for reduced-precision inputs ([#186358](https://github.com/pytorch/pytorch/pull/186358))

- Prevent CUDA `avg_pool3d` backward from corrupting gradients when an overlapping-window input contains more than `2**31` elements ([#188229](https://github.com/pytorch/pytorch/pull/188229))

- Reject non-positive `kernel_size` values in raw `fractional_max_pool2d` and `fractional_max_pool3d` operations instead of returning `-inf` outputs with invalid indices ([#190480](https://github.com/pytorch/pytorch/pull/190480))

- Support 64-bit indexing for channels-last CUDA bilinear upsampling so outputs with at least `2**31` elements no longer fail with `CUDA error: invalid configuration argument` ([#185788](https://github.com/pytorch/pytorch/pull/185788))

- Fall back to the ATen CUDA implementation when the fused RMSNorm override's normalized dimension exceeds the device's shared-memory capacity, avoiding compiler hangs or crashes ([#186941](https://github.com/pytorch/pytorch/pull/186941))

- Reject invalid `dim` types when constructing `torch.nn.Softmax` or `torch.nn.LogSoftmax` instead of failing later during the forward pass with a confusing overload error ([#185055](https://github.com/pytorch/pytorch/pull/185055))

- Handle misaligned input and weight storage in the fused RMSNorm override instead of raising `Misaligned Tensor data on argument #0` ([#186235](https://github.com/pytorch/pytorch/pull/186235))

- Make CUDA `float16` softmax with `dtype=torch.float32` use the same persistent-kernel range as the `float16` output path, fixing rounding inconsistencies for dimensions between 1025 and 2048 ([#188247](https://github.com/pytorch/pytorch/pull/188247))

## Optimizer

- Fix skipped updates and incorrect `float16`/`bfloat16` casts in fused CPU `torch.optim.SGD` and `torch.optim.Adagrad` ([#192545](https://github.com/pytorch/pytorch/pull/192545))

## Autograd

- Reject unsupported third-order derivatives for training-mode batch normalization instead of silently returning an invalid result; second-order derivatives and evaluation mode are unchanged ([#186779](https://github.com/pytorch/pytorch/pull/186779))
- Fix `torch.pow` backward when the base is a Boolean scalar by promoting the scalar before computing its logarithm, avoiding an internal assertion failure ([#182564](https://github.com/pytorch/pytorch/pull/182564))
- Fix `torch.pow` backward under `torch.compile(dynamic=True)` when a Python integer exponent becomes symbolic, avoiding the `NYI SymInt equality` crash without specializing on the exponent ([#185851](https://github.com/pytorch/pytorch/pull/185851))
- Make `native_group_norm` and `native_group_norm_backward` safely handle non-contiguous tensors, fixing `vmap` failures and possible out-of-bounds memory accesses ([#186414](https://github.com/pytorch/pytorch/pull/186414))
- Fix the `torch.ldexp` gradient for negative integer exponents so it returns `2.0 ** exponent` instead of zero ([#186566](https://github.com/pytorch/pytorch/pull/186566))
- Fix `DeviceContext` mode leaks during checkpoint recomputation and default-device restoration ([#189286](https://github.com/pytorch/pytorch/pull/189286))
- Fix end-of-backward leaf-stream synchronization across CUDA graph capture boundaries, avoiding opaque `cudaErrorStreamCaptureIsolation` failures and providing an actionable error when the crossing cannot be safely skipped ([#189591](https://github.com/pytorch/pytorch/pull/189591))
- Fix precision errors in the CUDA `native_group_norm_backward` kernel and its decomposition by applying the missing upcasts ([#190245](https://github.com/pytorch/pytorch/pull/190245))
- Stop `register_full_backward_pre_hook`-only modules from emitting a warning intended for `register_full_backward_hook` when their forward inputs do not require gradients ([#190685](https://github.com/pytorch/pytorch/pull/190685))
- Fix max-pooling double backward under `vmap` for channels-last inputs, which previously raised `NYI: querying is_contiguous inside of vmap` ([#191678](https://github.com/pytorch/pytorch/pull/191678))
- Preserve dynamic type names and argument indices in custom `torch.autograd.Function` validation error messages ([#191748](https://github.com/pytorch/pytorch/pull/191748))
- Improve `log2` and `log10` backward accuracy by using named mathematical constants, including a correctly rounded double-precision `log(10)` constant ([#192613](https://github.com/pytorch/pytorch/pull/192613))

## Distributed

- Fix construction of Python `ProcessGroup` subclasses through the `(store, rank, size)` constructor and ensure their virtual overrides are dispatched correctly ([#186853](https://github.com/pytorch/pytorch/pull/186853))
- Select registered custom communication backends instead of incorrectly falling back to NCCL or Gloo when the backend is unspecified ([#179901](https://github.com/pytorch/pytorch/pull/179901))
- Fix compiled DTensor backward paths producing data-dependent guards for valid symbolic local layouts ([#187026](https://github.com/pytorch/pytorch/pull/187026))
- Preserve local Philox seed and offset outputs when expanding DTensor scaled dot-product attention strategies across multidimensional meshes ([#187199](https://github.com/pytorch/pytorch/pull/187199))
- Respect nonzero `root` arguments in `torch.cuda.nccl.broadcast` instead of always broadcasting from the first tensor ([#187216](https://github.com/pytorch/pytorch/pull/187216))
- Fix ring-attention backward using mismatched maximum sequence lengths when context-parallel load balancing is enabled ([#185493](https://github.com/pytorch/pytorch/pull/185493))
- Fix DTensor backward strategies emitting placements for outputs disabled by `output_mask` ([#187383](https://github.com/pytorch/pytorch/pull/187383))
- Preserve the configured FSDP2 gradient-reduction dtype when parameters are frozen during the first forward and later unfrozen ([#187376](https://github.com/pytorch/pytorch/pull/187376))
- Make `torch.distributed.set_timeout()` a no-op for fake process groups and warn rather than fail for backends that cannot configure timeouts ([#187693](https://github.com/pytorch/pytorch/pull/187693))
- Prevent `LocalDeviceMesh` from returning stale coordinates after a temporary submesh is destroyed and its object ID is reused ([#187052](https://github.com/pytorch/pytorch/pull/187052))
- Fix asynchronous coalesced collectives failing CUDA graph capture under `torch.compile(mode="reduce-overhead")` because tensors were retained by the wrong work object ([#187433](https://github.com/pytorch/pytorch/pull/187433))
- Implement `barrier()` for the NCCL symmetric-memory backend instead of raising a not-implemented error ([#188051](https://github.com/pytorch/pytorch/pull/188051))
- Flush distributed-checkpoint streams before `fsync()` so buffered writes are persisted correctly on remote filesystems such as GCS ([#183877](https://github.com/pytorch/pytorch/pull/183877))
- Fix repeated `hipMemMap` calls causing symmetric-memory failures on ROCm ([#188673](https://github.com/pytorch/pytorch/pull/188673))
- Fix custom backend registration with a string `devices` argument incorrectly registering each character as a device type ([#187960](https://github.com/pytorch/pytorch/pull/187960))
- Fix FSDP `summon_full_params(offload_to_cpu=True)` accessing freed storage when the flattened parameter is already on CPU ([#188990](https://github.com/pytorch/pytorch/pull/188990))
- Include the local device in compiled DTensor cache keys so ranks cannot reuse kernels compiled for another device ([#188401](https://github.com/pytorch/pytorch/pull/188401))
- Prevent stale symmetric-memory signal data when virtual addresses are reused by placing and clearing the signal pad at the front of each allocation ([#189088](https://github.com/pytorch/pytorch/pull/189088))
- Fix collective validation, sequence tracking, complex tensors, barriers, and work cleanup in the experimental `nccl2` backend ([#190138](https://github.com/pytorch/pytorch/pull/190138))
- Preserve container object identity when FSDP recursively moves values but their elements do not change ([#171617](https://github.com/pytorch/pytorch/pull/171617))
- Make compile-on-one-rank graphs resolve process groups from their device mesh at runtime instead of serializing rank-specific process-group objects ([#188215](https://github.com/pytorch/pytorch/pull/188215))
- Fix `torch.distributed.nn.functional.broadcast` producing a zero source gradient for subgroups whose local and global source ranks differ ([#190583](https://github.com/pytorch/pytorch/pull/190583))
- Create TorchComms subgroups on the calling rank's actual device, including under launchers that do not set TorchComms rank variables ([#189072](https://github.com/pytorch/pytorch/pull/189072))
- Fix work-object and expandable-segment allocator lifetimes in the experimental `nccl2` backend ([#190370](https://github.com/pytorch/pytorch/pull/190370))
- Return `GroupMember.NON_GROUP_MEMBER` consistently from locally synchronized `new_group` calls on nonmember ranks ([#190588](https://github.com/pytorch/pytorch/pull/190588))
- Support the linear `avg` reduction in functional `all_reduce` backward instead of rejecting it after a successful forward pass ([#190224](https://github.com/pytorch/pytorch/pull/190224))
- Prevent subgroup creation hangs and duplicate-finalization crashes by making subgroup-name salts rank-consistent and finalizing each communicator once ([#189073](https://github.com/pytorch/pytorch/pull/189073), [#189074](https://github.com/pytorch/pytorch/pull/189074))
- Fix single-operation point-to-point completion ordering and synchronous barrier semantics in the experimental `nccl2` backend ([#190622](https://github.com/pytorch/pytorch/pull/190622), [#190682](https://github.com/pytorch/pytorch/pull/190682))
- Allow NCCL symmetric memory to use communicators created by the experimental `nccl2` backend ([#191109](https://github.com/pytorch/pytorch/pull/191109))
- Normalize `new_group` ranks through Python's integer protocol so tensor integer ranks work and non-integral values fail clearly ([#191377](https://github.com/pytorch/pytorch/pull/191377))
- Fix simulated `all_to_all_single` with uneven split sizes in `LocalTensorMode` and raise a clear error for inconsistent splits ([#190311](https://github.com/pytorch/pytorch/pull/190311))
- Accept device-qualified Gloo backends in `monitored_barrier` when TorchComms is enabled ([#189070](https://github.com/pytorch/pytorch/pull/189070))
- Prevent `CommDebugMode` hooks from leaking or double-running when a module executes more than once ([#191452](https://github.com/pytorch/pytorch/pull/191452))
- Warn when symmetric-memory collectives are launched concurrently on multiple streams, which can otherwise deadlock ([#191482](https://github.com/pytorch/pytorch/pull/191482))
- Choose a process group's default backend only from backend types that were actually registered ([#189193](https://github.com/pytorch/pytorch/pull/189193))
- Report the correct group-local rank and process-group identifier in NCCL work timeout and error logs ([#191440](https://github.com/pytorch/pytorch/pull/191440))
- Preserve the caller's current CUDA device in the experimental `nccl2` backend and validate full device identities ([#191510](https://github.com/pytorch/pytorch/pull/191510))
- Validate all-to-all split sizes consistently across Gloo, NCCL, and `nccl2` ([#191511](https://github.com/pytorch/pytorch/pull/191511))
- Prevent destroying one TorchComms subgroup from inadvertently destroying every live group ([#191637](https://github.com/pytorch/pytorch/pull/191637))
- Propagate `device_id` through `ProcessGroupWrapper` so debug wrappers do not hang with heterogeneous rank-to-GPU mappings ([#182273](https://github.com/pytorch/pytorch/pull/182273))
- Forward group identifiers through `nccl-lazy` so NCCL symmetric-memory rendezvous can find the primary communicator ([#191544](https://github.com/pytorch/pytorch/pull/191544))
- Reject unsupported reconfigurable mode for `nccl-lazy` instead of advertising incomplete membership-change support ([#191549](https://github.com/pytorch/pytorch/pull/191549))
- Disable NCCL NVLS in `nccl2` when deterministic algorithms are enabled, matching the legacy NCCL backend ([#192104](https://github.com/pytorch/pytorch/pull/192104))
- Prevent `nccl2` watchdog errors, timeouts, explicit aborts, and normal teardown from unconditionally terminating the process ([#192105](https://github.com/pytorch/pytorch/pull/192105))
- Fix Gloo and NCCL `split_group` crashes when the world process group was not the first backend instance created in the process ([#192106](https://github.com/pytorch/pytorch/pull/192106), [#192109](https://github.com/pytorch/pytorch/pull/192109))
- Fix device-bound `nccl2` process-group initialization failing before the CUDA caching allocator has been initialized ([#192107](https://github.com/pytorch/pytorch/pull/192107))
- Give split and merged process groups independent backend options so child creation cannot corrupt parent metadata or share mutable options ([#192110](https://github.com/pytorch/pytorch/pull/192110))
- Fix `split_group(backend=...)` filtering for parent groups created with a bare backend name ([#192111](https://github.com/pytorch/pytorch/pull/192111))
- Prevent private `TCPStore` rendezvous under `torchrun` from hanging by using the agent store only for the agent's own address ([#192113](https://github.com/pytorch/pytorch/pull/192113))
- Fix `bfloat16` NCCL `PREMUL_SUM` factors being interpreted as zero and silently producing zero gradients ([#190747](https://github.com/pytorch/pytorch/pull/190747))
- Fix a use-after-free race while concurrently dumping Flight Recorder entries ([#192232](https://github.com/pytorch/pytorch/pull/192232))
- Run symmetric-memory allocation and rendezvous device work on the caller's current CUDA stream ([#192308](https://github.com/pytorch/pytorch/pull/192308))
- Recognize libuv's lowercase `address already in use` message when TorchElastic retries `TCPStore` creation ([#191561](https://github.com/pytorch/pytorch/pull/191561))
- Add missing collective-fingerprint checks for `allgather_into_tensor_coalesced` under `ProcessGroupWrapper` ([#185123](https://github.com/pytorch/pytorch/pull/185123))
- Fix DTensor AOT compilation misclassifying overload names containing `out` as output-variant operators ([#187466](https://github.com/pytorch/pytorch/pull/187466))
- Fix compiled functional point-to-point collectives that pass global peer ranks to subgroup operations requiring group-local ranks ([#187924](https://github.com/pytorch/pytorch/pull/187924))
- Preserve pipeline-stage module buffers while dynamic metadata inference runs representative forward and backward passes ([#188558](https://github.com/pytorch/pytorch/pull/188558))
- Fix DTensor backward support for `cumprod`, `cummax`, and `cummin` ([#185228](https://github.com/pytorch/pytorch/pull/185228))
- Make pipeline schedules select static metadata locally when a fake process group cannot perform cross-rank metadata inference, and report incomplete stage metadata clearly ([#191538](https://github.com/pytorch/pytorch/pull/191538))
- Restore the caller's cyclic garbage collector state after Flight Recorder `read_dir()` calls, including when loading fails ([#191607](https://github.com/pytorch/pytorch/pull/191607))

## Distributed (c10d)

- Fix `destroy_process_group()` hanging after collectives run on partially split process groups by keeping group names consistent across ranks ([#190431](https://github.com/pytorch/pytorch/pull/190431))

## DTensor

- Fix compiled functions failing when they return DTensor permutation views such as `transpose`, `permute`, or `movedim` ([#191784](https://github.com/pytorch/pytorch/pull/191784))
- Fix deferred `local_map` export failing inside nested compile regions ([#186647](https://github.com/pytorch/pytorch/pull/186647))

## Linear Algebra Frontend

- Fix `torch.linalg.cond()` reporting a misleading overflow error for a complex norm order; invalid orders now raise `ValueError` with a clear message ([#188591](https://github.com/pytorch/pytorch/pull/188591))
- Fix `torch.lu_unpack` segfaulting when `LU_pivots` has a shape inconsistent with `LU_data`; invalid shapes now raise a clear error ([#187660](https://github.com/pytorch/pytorch/pull/187660))
- Fix `torch.linalg.lstsq(driver="gelsy")` returning an incorrect rank on CPU when stale pivot values leaked between batched LAPACK calls ([#187436](https://github.com/pytorch/pytorch/pull/187436))
- Fix `torch.compile(dynamic=True)` failing on `torch.linalg.cond` with `p="fro"` or `p="nuc"` because symbolic tensor sizes were queried as concrete values ([#187614](https://github.com/pytorch/pytorch/pull/187614))
- Fix offline `TunableOp` tuning silently using the wrong GEMM shape when a padded leading dimension matches another matrix dimension ([#189355](https://github.com/pytorch/pytorch/pull/189355))
- Fix `CUBLAS_STATUS_NOT_SUPPORTED` failures in matrix multiplication on CUDA compute capability 11.0 by increasing the default cuBLAS workspace to 32 MiB ([#189312](https://github.com/pytorch/pytorch/pull/189312))

## Indexing

- Reject nonempty `torch.unravel_index()` inputs whose `shape` contains a zero-sized dimension with a clear `ValueError` instead of an uncaught division-by-zero `RuntimeError`; empty indices remain supported ([#191092](https://github.com/pytorch/pytorch/pull/191092))
- Fix assigning Python integers greater than `INT64_MAX` into `torch.uint64` tensors, which previously raised `Overflow when unpacking long long` ([#191604](https://github.com/pytorch/pytorch/pull/191604))
- Fix an illegal CUDA memory access in `torch.nn.functional.adaptive_avg_pool2d` backward for very large contiguous tensors whose element offsets exceed 32-bit indexing limits ([#189082](https://github.com/pytorch/pytorch/pull/189082))

## Profiler

- Exclude individual Python function events from `key_averages()` by default so frames such as `threading.py: wait` do not obscure operator-level hotspots; pass `include_python_functions=True` to retain the previous view ([#188631](https://github.com/pytorch/pytorch/pull/188631))
- Clamp incomplete Python function events to their parent event's end time so exported traces retain correct nesting instead of placing overrunning events on unrelated tracks ([#190950](https://github.com/pytorch/pytorch/pull/190950))
- Avoid importing the experimental CUPTI monitor during ordinary `record_function` profiling, preventing repeated warnings and tracebacks on systems with incompatible `cupti-python` versions ([#187874](https://github.com/pytorch/pytorch/pull/187874))
- Fix reference leaks when reading the `layout` and `dtype` properties of profiler tensor metadata ([#187068](https://github.com/pytorch/pytorch/pull/187068))

## FX

- Respect deferred runtime-assert bounds when deriving optimization hints for unbacked symbolic sizes, preventing negative storage sizes and downstream CUDA indexing failures ([#190589](https://github.com/pytorch/pytorch/pull/190589))
- Make selected Dynamo, Inductor, and FX tracing state thread-local to prevent race conditions when `torch.compile` is invoked concurrently from multiple threads ([#168999](https://github.com/pytorch/pytorch/pull/168999))
- Fix FX `GraphModule` serialization when generated code contains string type annotations ([#185051](https://github.com/pytorch/pytorch/pull/185051))
- Fix scripting FX-generated modules with nested `Optional[Dict[...]]` annotations on Python 3.14 ([#190580](https://github.com/pytorch/pytorch/pull/190580))
- Skip constant folding for `get_attr` nodes whose targets cannot be resolved or refer to modules ([#191939](https://github.com/pytorch/pytorch/pull/191939))
- Preserve non-persistent buffer registration when an FX `GraphModule` copies attributes, keeping those buffers out of `state_dict()` ([#191708](https://github.com/pytorch/pytorch/pull/191708))
- Fix Z3 translation validation for graphs containing symbolic boolean negation through `torch.sym_not` ([#185147](https://github.com/pytorch/pytorch/pull/185147))
- Fix FX-generated code raising `NameError` for complex constants whose imaginary component is `nan` or `inf` ([#188596](https://github.com/pytorch/pytorch/pull/188596))
- Preserve signed zero when FX code generation emits complex constants with a zero real or imaginary component ([#185550](https://github.com/pytorch/pytorch/pull/185550))
- Apply `skip_folding_node_fn` recursively to `call_module` subgraphs so FX constant folding does not evaluate skipped or symbolic nodes inside them ([#189487](https://github.com/pytorch/pytorch/pull/189487))
- Return valid `tuple[...]` annotations from `get_signature_for_torch_op` for operators that return multiple tensors ([#189142](https://github.com/pytorch/pytorch/pull/189142))
- Avoid a `linecache` loader warning when executing generated FX `GraphModule` code on Python 3.15 ([#187221](https://github.com/pytorch/pytorch/pull/187221))

## Dynamo

- Make compiled `next()` reject non-iterators with the same `TypeError` as CPython instead of silently returning the first element ([#190624](https://github.com/pytorch/pytorch/pull/190624))
- Make compiled `set()` and `frozenset()` reject keyword arguments instead of silently constructing an empty set, matching CPython ([#189051](https://github.com/pytorch/pytorch/pull/189051))
- Preserve registered third-party backend configuration and extra Triton imports in generated minifier reproductions ([#187855](https://github.com/pytorch/pytorch/pull/187855))
- Fix `torch.compiler.nested_compile_region` reuse across regions that read a global rebound between calls, which reused a stale graph ([#192006](https://github.com/pytorch/pytorch/pull/192006))
- Fix autograd through a `torch.compiler.nested_compile_region` executed in eager mode, which entered the fake-tensor AOTAutograd backward path instead of recording through the region ([#184700](https://github.com/pytorch/pytorch/pull/184700))
- Emit a `torch.compiler.nested_compile_region` call as a single graph node instead of graph breaking, as its documentation states ([#186137](https://github.com/pytorch/pytorch/pull/186137))
- Fix `torch.compiler.nested_compile_region` on transposed views of captured buffers (`x @ self.w.T`), which failed with `Freevar has no source` ([#191785](https://github.com/pytorch/pytorch/pull/191785))
- Fix nested graph break handling: reconstruction of exhausted generators and of empty `nn.Module` hook dictionaries, a crash in `mark_static_input` for non-tensor variables, a graph break inside a context manager's `__init__` causing the whole frame to fall back to eager, a custom operator defined and registered with `register_fake` inside the traced function, a graph-break naming error in list comprehensions on Python < 3.12, a `compile_subgraph` failure swallowed while formatting an f-string, and nested graph breaks during `DeviceMesh` submesh creation ([#188622](https://github.com/pytorch/pytorch/pull/188622), [#191388](https://github.com/pytorch/pytorch/pull/191388), [#187088](https://github.com/pytorch/pytorch/pull/187088), [#191264](https://github.com/pytorch/pytorch/pull/191264), [#191523](https://github.com/pytorch/pytorch/pull/191523), [#189601](https://github.com/pytorch/pytorch/pull/189601), [#187005](https://github.com/pytorch/pytorch/pull/187005), [#187701](https://github.com/pytorch/pytorch/pull/187701), [#188861](https://github.com/pytorch/pytorch/pull/188861))
- Reject `Tensor` values in tensor subclass metadata before installing the default metadata guard, avoiding an ambiguous Boolean-value error ([#184684](https://github.com/pytorch/pytorch/pull/184684))
- Fix `eager_then_compile` when a later compile sees a higher-rank input ([#184689](https://github.com/pytorch/pytorch/pull/184689))
- Fix a flaky `NameError: name '__compiled_fn_N_...' is not defined` when `CompilePackage.install()` reuses a global name after `torch._dynamo.reset()` ([#191128](https://github.com/pytorch/pytorch/pull/191128))
- Fix `torch._dynamo.reset()` leaving the process-global fake tensor dispatch cache populated, which could make a compile that failed cold pass on an in-process retry ([#191418](https://github.com/pytorch/pytorch/pull/191418))
- Fix precompile guard serialization for transparent tensor subclasses such as `AsyncCollectiveTensor` ([#190576](https://github.com/pytorch/pytorch/pull/190576))
- Fix AOT guard serialization for functions using `torch.func` transforms (`vmap`/`grad`/`jvp`) ([#191428](https://github.com/pytorch/pytorch/pull/191428))
- Preserve the guard-building thread-local dispatch state so a precompile artifact loaded outside autocast does not force a recompile when the compiled function runs under autocast ([#184850](https://github.com/pytorch/pytorch/pull/184850))
- Fix precompile guard-state load at decoration time, which raised `TracingContext.get() must be called within an ongoing trace` ([#187736](https://github.com/pytorch/pytorch/pull/187736))
- Reinstall the compiled-function globals required by guarded bytecode on a warm precompile package load ([#184562](https://github.com/pytorch/pytorch/pull/184562))
- Skip storage memo for wrapper subclasses in `MetaConverter`, fixing `RuntimeError: Attempted to set the storage of a tensor on device "cuda:0" to a storage on different device "meta"` when a `_make_wrapper_subclass` tensor is a non-batched `torch.vmap` input inside `torch.compile` ([#176977](https://github.com/pytorch/pytorch/pull/176977))
- Fix class definitions inside a compiled region that close over a non-constant object, which raised `Invalid call to __build_class__` ([#185998](https://github.com/pytorch/pytorch/pull/185998))
- Use symbolic scalar extraction for zero-dimensional integral tensor indices, so indexing a tensor with a scalar tensor stays on the `select` path under `torch.export` ([#184625](https://github.com/pytorch/pytorch/pull/184625))
- Fix modeling of globals for functions whose globals dictionary is not owned by a registered module ([#184653](https://github.com/pytorch/pytorch/pull/184653))
- Fix `hasattr` on user objects so tracing does not materialize an existing `RemovableHandle` stored by conditional hook registration ([#184712](https://github.com/pytorch/pytorch/pull/184712))
- Run `torch.compile` wrappers eagerly when re-entered from compiler-internal fake or functional tracing, fixing fake-mode mismatch and fake tensor data pointer errors from tensor subclass hooks ([#185732](https://github.com/pytorch/pytorch/pull/185732))
- Insert a graph break instead of silently dropping the tangent when a forward-AD dual tensor is passed into a compiled function; `fullgraph=True` now raises a clear error ([#189644](https://github.com/pytorch/pytorch/pull/189644))
- Fix `InternalTorchDynamoError` when traced code reads an attribute from `torch.compile(obj.meth)` ([#190185](https://github.com/pytorch/pytorch/pull/190185))
- Prevent an active `TorchDispatchMode` from permanently marking a code object as skipped ([#190287](https://github.com/pytorch/pytorch/pull/190287))
- Fix lazy module initialization when the fake inputs carry symbolic shapes, e.g. in a resume function after a graph break ([#188595](https://github.com/pytorch/pytorch/pull/188595))
- Clear weak references left by discarded tracing attempts so `torch.utils.swap_tensors` works on a live compiled module's parameters ([#190951](https://github.com/pytorch/pytorch/pull/190951))
- Fix compiled tensor subclasses replaying placeholder objects instead of the original metadata values when those values are also used by Python side effects ([#187057](https://github.com/pytorch/pytorch/pull/187057))
- Refresh cached tensor metadata after any in-place mutation proven by fake execution, fixing stale `size()`/`stride()` reads after `as_strided_` ([#187890](https://github.com/pytorch/pytorch/pull/187890))
- Fix `TypeError: sequence item N: expected str instance, int found` for an f-string over a dynamic `SymInt` that spans a graph break ([#189830](https://github.com/pytorch/pytorch/pull/189830))
- Fix f-string mutation ordering so Python-side object and container formatting is evaluated at the original bytecode point ([#182638](https://github.com/pytorch/pytorch/pull/182638))
- Route `ctx.needs_input_grad` through side-effect mutation tracking, so a traced store is no longer silently dropped ([#191492](https://github.com/pytorch/pytorch/pull/191492))
- Restore the process autocast dtype after a trace-time `torch.set_autocast_dtype`, fixing `Global autocast state changed while dynamo tracing` ([#186530](https://github.com/pytorch/pytorch/pull/186530))
- Correctly detect shared storage for overlapping `unsqueeze` views when tracing mutations ([#187111](https://github.com/pytorch/pytorch/pull/187111))
- Raise an observed `TypeError` instead of an internal `AssertionError` for bad `vars()` arity ([#185128](https://github.com/pytorch/pytorch/pull/185128))
- Fix `torch.vmap` over an `autograd.Function` that uses `generate_vmap_rule=True` ([#186362](https://github.com/pytorch/pytorch/pull/186362))
- Fix infinite recursion when calling `int()`/`float()` on or indexing a pybind11 enum in a compiled function ([#188605](https://github.com/pytorch/pytorch/pull/188605))
- Fix the C++ pytree polyfill's `PyTreeSpec.__eq__`/`__hash__` so it matches eager `optree` semantics ([#190649](https://github.com/pytorch/pytorch/pull/190649))
- Propagate Python `TypeError` exceptions from function-signature mismatches instead of converting them into graph breaks ([#190797](https://github.com/pytorch/pytorch/pull/190797))
- Check that a traced `__int__`/`__float__` actually returns an `int`/`float` ([#190257](https://github.com/pytorch/pytorch/pull/190257))
- Validate the bound object's type in the `__get__` of C descriptors, which could otherwise bind a descriptor to an incompatible object and produce wrong control flow ([#190776](https://github.com/pytorch/pytorch/pull/190776))
- Graph break on `isinstance` checks of a tensor against a `classinfo` argument with a custom `__instancecheck__` (for example, `jaxtyping` annotations) instead of compiling the wrong branch ([#186491](https://github.com/pytorch/pytorch/pull/186491))
- Fix `deque.__init__` truncating items against the pre-init `maxlen` when re-initializing ([#188171](https://github.com/pytorch/pytorch/pull/188171))
- Route `list`/`tuple` `__add__` through the sequence-concat slot, and let explicit set / dict-view `__and__`, `__xor__`, `__sub__` calls return `NotImplemented` for an unsupported operand as CPython does ([#189554](https://github.com/pytorch/pytorch/pull/189554), [#189274](https://github.com/pytorch/pytorch/pull/189274))
- Return the actual subclass from `type()` on a `torch.Event` subclass ([#189145](https://github.com/pytorch/pytorch/pull/189145))
- Fix the error message for non-iterable slice assignment on affected older CPython patch releases ([#187777](https://github.com/pytorch/pytorch/pull/187777))
- Clear stale exception-table entries on copied prefix instructions, fixing a `KeyError` when compiling Python 3.12 coroutine bytecode ([#185731](https://github.com/pytorch/pytorch/pull/185731))
- Stop generating `LIST_APPEND` bytecode, which assumes single ownership and tripped assertions on free-threaded builds ([#187086](https://github.com/pytorch/pytorch/pull/187086))
- Always create a real iterator instead of imitating CPython's virtual iterators, fixing segfaults when restoring from a graph break inside a list comprehension on Python 3.15 ([#187103](https://github.com/pytorch/pytorch/pull/187103))
- Probe internal attributes with `object.__getattribute__` instead of running a user-defined `__getattr__` ([#190970](https://github.com/pytorch/pytorch/pull/190970))
- Fix the `ts` and `aot_ts` backends, which failed on every function because `torch.jit.script` cannot script the `_LazyGraphModule` handed to backends ([#188875](https://github.com/pytorch/pytorch/pull/188875))
- Handle `OSError` (e.g. `PermissionError`) from the `nvcc` probe when collecting CUDA info for a repro, which could crash `torch.compile` with an `InductorError` ([#185843](https://github.com/pytorch/pytorch/pull/185843))
- Do not graft a self-referential `bw_compiler` when an `aot_autograd` backend compiles a second graph ([#189325](https://github.com/pytorch/pytorch/pull/189325))
- Ignore non-tensor `.device` and `.dtype` attributes when inferring a compiled graph's input device and dtype ([#190425](https://github.com/pytorch/pytorch/pull/190425))
- Avoid misclassifying custom backend objects as registered backends merely because they expose a matching `compiler_name` attribute ([#190426](https://github.com/pytorch/pytorch/pull/190426))
- Fix gradients for a directly captured zero-dimensional `score_mod` tensor in FlexAttention ([#188869](https://github.com/pytorch/pytorch/pull/188869))

## Inductor

- Fix `torch.compile` support for `torch.combinations` by removing a CUDA synchronization from argument validation ([#189305](https://github.com/pytorch/pytorch/pull/189305))
- Match eager CUDA behavior for `torch.addmm(..., beta=0)` by ignoring a non-broadcastable bias while retaining dtype and device validation ([#183511](https://github.com/pytorch/pytorch/pull/183511))
- Fix ordering, dependency, and stream-state races in compiled multi-stream graphs that use events or the `control_deps` operator ([#183803](https://github.com/pytorch/pytorch/pull/183803), [#183804](https://github.com/pytorch/pytorch/pull/183804), [#186022](https://github.com/pytorch/pytorch/pull/186022), [#186023](https://github.com/pytorch/pytorch/pull/186023), [#186025](https://github.com/pytorch/pytorch/pull/186025))
- Fix `_scaled_mm` compilation when tensorwise scales mix scalar and singleton two-dimensional shapes ([#183964](https://github.com/pytorch/pytorch/pull/183964))
- Fix Inductor pattern-matching failures when `torch.randperm` is followed by advanced or sliced indexing ([#184066](https://github.com/pytorch/pytorch/pull/184066))
- Prevent incorrect convolution binary folding when the convolution bias is a dynamic graph input ([#184132](https://github.com/pytorch/pytorch/pull/184132))
- Prevent incorrect results when fusing user-defined Triton kernels with epilogues whose read and write layouts differ by rejecting the incompatible fusion ([#184248](https://github.com/pytorch/pytorch/pull/184248))
- Fix `CantSplit` compilation errors when split iteration ranges contain equivalent symbolic floor-division expressions ([#184566](https://github.com/pytorch/pytorch/pull/184566))
- Fix `torch.remainder` returning results that differ from eager mode when a `float16` or `bfloat16` tensor is combined with a Python or zero-dimensional scalar divisor ([#185168](https://github.com/pytorch/pytorch/pull/185168))
- Fix FlexAttention illegal-memory-access failures on very large key/value buffers by using 64-bit pointer offsets when required ([#185264](https://github.com/pytorch/pytorch/pull/185264))
- Fix CPU C++ code generation for vectorized atomic addition with scalar destination indices ([#185325](https://github.com/pytorch/pytorch/pull/185325))
- Fix `"cannot determine truth value of Relational"` failures for dynamic-shape adaptive average pooling and `Upsample(mode="area")` ([#185369](https://github.com/pytorch/pytorch/pull/185369))
- Fix `KeyError: 'complex64'` during Triton signature generation when compiled graphs require exact-stride copies of complex tensors ([#185501](https://github.com/pytorch/pytorch/pull/185501))
- Stop successful CUDA compilation from emitting TF32 `UserWarning` messages while retaining the advisory under `TORCH_LOGS=perf_hints` ([#185541](https://github.com/pytorch/pytorch/pull/185541))
- Fix assertion failures when lowering custom operators with out variants and dynamic output shapes ([#185601](https://github.com/pytorch/pytorch/pull/185601))
- Preserve the graph's fake-tensor mode when `standalone_compile` receives tensor-subclass outputs ([#185638](https://github.com/pytorch/pytorch/pull/185638))
- Fix an import-time `TypeError` in `torch._inductor` when another vendored `typing_extensions` copy has modified `typing` internals ([#185708](https://github.com/pytorch/pytorch/pull/185708))
- Fix CPU max-autotune `IndexError` failures when a GEMM and its epilogue reuse the same input tensor ([#185767](https://github.com/pytorch/pytorch/pull/185767))
- Prevent `RecursionError: maximum recursion depth exceeded` during AOTInductor autotuning when very wide symbolic size expressions are emitted into Triton source ([#185778](https://github.com/pytorch/pytorch/pull/185778))
- Fix `torch.cond` compilation when a branch uses a tensor constant that was not registered in the root graph ([#185838](https://github.com/pytorch/pytorch/pull/185838))
- Fix silently incorrect CPU results when outer-loop fusion reuses local buffers across tiled iterations ([#185855](https://github.com/pytorch/pytorch/pull/185855))
- Fix generated regional-compilation wrappers referencing undefined symbols when an input dimension is a symbolic expression ([#185890](https://github.com/pytorch/pytorch/pull/185890))
- Fix compiled `torch.min` and `torch.max` returning incorrect indices for boolean tensors on CPU and other non-Triton backends ([#185970](https://github.com/pytorch/pytorch/pull/185970))
- Prevent `UnicodeDecodeError` while probing MSVC when `cl.exe /help` emits malformed or locale-specific bytes ([#185972](https://github.com/pytorch/pytorch/pull/185972))
- Raise a clear error when FlexAttention backward receives a `score_mod` whose output does not depend on `score`, instead of failing inside Inductor lowering ([#185991](https://github.com/pytorch/pytorch/pull/185991))
- Prevent fused kernels with large constant address offsets from overflowing 32-bit indices and raising out-of-range errors ([#186060](https://github.com/pytorch/pytorch/pull/186060))
- Prevent `NoValidChoicesError` for Triton-only transposed or dilated convolution autotuning by supporting `ConvTranspose2d` and falling back safely when needed ([#186067](https://github.com/pytorch/pytorch/pull/186067))
- Fix wrong results from Halide fusion when a producer reads a buffer that an in-place mutation also writes ([#186121](https://github.com/pytorch/pytorch/pull/186121))
- Fix AOTInductor integer floor division by captured tensor constants, including correct rounding for negative values ([#186242](https://github.com/pytorch/pytorch/pull/186242))
- Prevent duplicate equivalent template or external-kernel registrations from crashing imports with an assertion ([#186262](https://github.com/pytorch/pytorch/pull/186262))
- Fall back to eager execution instead of failing compilation for `_scaled_mm_v2` with swizzled scale layouts such as blockwise MXFP8 and NVFP4 ([#186384](https://github.com/pytorch/pytorch/pull/186384))
- Prevent NVGEMM precompilation from initializing CUDA inside an incompatible forked compile worker ([#186385](https://github.com/pytorch/pytorch/pull/186385))
- Fix CPU code generation for `index_put_(accumulate=True)` with boolean values ([#186523](https://github.com/pytorch/pytorch/pull/186523))
- Allow eager pointwise `associative_scan` to use its generic fallback on devices without scan code generation, and report unsupported compiled devices during Inductor lowering with an actionable error suggesting `combine_mode="generic"` ([#186633](https://github.com/pytorch/pytorch/pull/186633))
- Fix CUTLASS kernel compilation through the C++ wrapper on XPU by using the XPU compiler and code cache ([#186791](https://github.com/pytorch/pytorch/pull/186791))
- Match eager CPU and MPS semantics for `float16` and `bfloat16` addition and subtraction with Python scalar operands ([#186818](https://github.com/pytorch/pytorch/pull/186818))
- Honor user-supplied FlexAttention kernel options and report incompatible sparse-block and tile sizes with actionable errors ([#186876](https://github.com/pytorch/pytorch/pull/186876))
- Fall back to regular loads and stores when tensor descriptors cannot satisfy Triton's 16-byte transfer requirement, including `XBLOCK=1` and small persistent-reduction cases ([#186922](https://github.com/pytorch/pytorch/pull/186922), [#186932](https://github.com/pytorch/pytorch/pull/186932))
- Preserve eager signed-zero and NaN behavior for compiled `torch.minimum` and `torch.maximum` on Triton backends ([#186933](https://github.com/pytorch/pytorch/pull/186933))
- Fix incorrect CPU results for `abs()` on unsigned integer tensors under `torch.compile` ([#187024](https://github.com/pytorch/pytorch/pull/187024))
- Fall back to an unfused epilogue instead of raising `AssertionError: failed to set ranges` when a template's tiling cannot represent its iteration domain ([#187209](https://github.com/pytorch/pytorch/pull/187209))
- Fix a race when an input requiring alignment correction is consumed on multiple CUDA streams by emitting one copy per stream ([#187224](https://github.com/pytorch/pytorch/pull/187224))
- Fix combo-kernel compilation for persistent reductions with dynamic reduction dimensions ([#187275](https://github.com/pytorch/pytorch/pull/187275))
- Make compiled `torch.celu` and `torch.celu_` reject `alpha=0` with the same error as eager execution ([#187321](https://github.com/pytorch/pytorch/pull/187321))
- Prevent manual collective bucketing from producing a non-topological FX graph when packing order differs from graph order ([#187341](https://github.com/pytorch/pytorch/pull/187341))
- Match eager CUDA behavior by returning `NaN` for infinite inputs to compiled modified-Bessel I0 and I1 operations ([#187354](https://github.com/pytorch/pytorch/pull/187354))
- Fix `Unregistered range symbol` failures for persistent-TMA `addmm` kernels with fused epilogues ([#187371](https://github.com/pytorch/pytorch/pull/187371))
- Avoid CUDA convolution-backward illegal memory accesses by falling back from Triton to the ATen implementation ([#187372](https://github.com/pytorch/pytorch/pull/187372))
- Fix CUTLASS GEMM epilogue-fusion crashes when reshaped external inputs have incompatible dimensions ([#187404](https://github.com/pytorch/pytorch/pull/187404))
- Fix `RuntimeError: 0 active drivers` in asynchronous Triton compile workers after CUDA has already been initialized ([#187408](https://github.com/pytorch/pytorch/pull/187408))
- Fall back to NVML for GPU clock-rate queries when `nvidia-smi` is unavailable ([#187427](https://github.com/pytorch/pytorch/pull/187427))
- Preserve NaN and infinity semantics by not folding floating-point or complex multiplication by zero into a constant zero ([#187580](https://github.com/pytorch/pytorch/pull/187580))
- Prevent generated Triton cache paths from exceeding Windows path-length limits by truncating long fused-kernel names while retaining a uniqueness hash ([#187641](https://github.com/pytorch/pytorch/pull/187641))
- Prevent memory planning from destroying an allocation pool too early when a graph output aliases a reused buffer ([#187678](https://github.com/pytorch/pytorch/pull/187678))
- Fix `torch._inductor` import failures on Python 3.11 and 3.12 caused by supplying too few generic parameters to `CSE` ([#187700](https://github.com/pytorch/pytorch/pull/187700))
- Fix sliced FlexAttention `BlockMask` objects retaining the original query sequence length instead of the sliced length ([#187886](https://github.com/pytorch/pytorch/pull/187886))
- Preserve architecture suffixes such as `sm_100a` when packaging AOTInductor CUDA kernels, avoiding `ptxas fatal: PTX with .target 'sm_100a' cannot be compiled for architecture 'sm_100'` ([#187888](https://github.com/pytorch/pytorch/pull/187888))
- Prevent duplicate Metal kernel names when a compiled graph contains multiple MPS scheduling instances ([#187894](https://github.com/pytorch/pytorch/pull/187894))
- Fix FlexAttention illegal memory accesses when `score_mod` or `mask_mod` captures tensors requiring 64-bit indexing ([#187904](https://github.com/pytorch/pytorch/pull/187904))
- Preserve the sign of `float64` negative zero in compiled CUDA `torch.signbit` ([#187941](https://github.com/pytorch/pytorch/pull/187941))
- Match eager results for floating-point floor division with infinite operands and signed-zero quotients ([#188049](https://github.com/pytorch/pytorch/pull/188049))
- Add an opt-in decomposition of DTensor shard-dimension all-to-all operations into traceable functional collectives through `TORCHINDUCTOR_DECOMPOSE_SHARD_DIM_ALLTOALL=1`. The same change always registers an autograd formula for `_dtensor::shard_dim_alltoall`, preventing compiled backward graphs from silently dropping its gradient even when the decomposition is disabled ([#188137](https://github.com/pytorch/pytorch/pull/188137))
- Prevent the CUTLASS backend from generating unsupported INT8 matrix-multiplication kernels on SM 10.3 GPUs ([#188209](https://github.com/pytorch/pytorch/pull/188209))
- Make eager and compiled `torch.cummax` and `torch.cummin` validate invalid dimensions consistently for zero-element tensors instead of silently returning empty results ([#188361](https://github.com/pytorch/pytorch/pull/188361))
- Report CUDA Graph skip reasons on supported non-CUDA GPU backends instead of silently recording only a counter ([#188384](https://github.com/pytorch/pytorch/pull/188384))
- Fix `LoweringException: AssertionError` when compiling scatter operations with empty index tensors ([#188466](https://github.com/pytorch/pytorch/pull/188466))
- Fix FlexAttention's FLASH backend ignoring sparse `BlockMask` metadata when `mask_mod` is trivial ([#188484](https://github.com/pytorch/pytorch/pull/188484))
- Fix wrong results in compiled programs that use bidirectional custom-stream synchronization ([#188533](https://github.com/pytorch/pytorch/pull/188533))
- Match eager CUDA behavior by returning `NaN` for infinite inputs to compiled Bessel J0, J1, Y0, and Y1 operations ([#188556](https://github.com/pytorch/pytorch/pull/188556))
- Fix CUDA `misaligned address` failures when a cached fast launcher outlives its autotuned kernel module ([#188607](https://github.com/pytorch/pytorch/pull/188607))
- Fix `cudaErrorStreamCaptureUnsupported` when `torch.linalg.eigh` is compiled with CUDA Graphs enabled ([#188641](https://github.com/pytorch/pytorch/pull/188641))
- Fix backward compilation failures caused by autograd-generated `aten.expand` calls carrying the schema's `implicit` keyword ([#188758](https://github.com/pytorch/pytorch/pull/188758))
- Fix severely incorrect nested reduction results by rewinding block pointers across outer loops ([#188771](https://github.com/pytorch/pytorch/pull/188771))
- Fix `ValueError: The argument 'False' is not comparable` when compiling boolean `torch.minimum` or `torch.maximum` ([#188862](https://github.com/pytorch/pytorch/pull/188862))
- Fix NVGEMM compilation against newer CuTeDSL releases that removed the enum-based `fence_proxy` API ([#188865](https://github.com/pytorch/pytorch/pull/188865))
- Fix FlexAttention FLASH-backend compilation and incorrect gathers caused by mixed 32-bit and 64-bit captured-buffer indices ([#188876](https://github.com/pytorch/pytorch/pull/188876))
- Release benchmark buffers retained by failed Triton autotuning configurations, preventing large transient GPU-memory leaks ([#188907](https://github.com/pytorch/pytorch/pull/188907))
- Preserve user stream assignments when compiler pattern replacements introduce intermediate operations ([#189095](https://github.com/pytorch/pytorch/pull/189095))
- Preserve eager ordering for captured CUDA event recording, waits, and CPU-blocking stream synchronization ([#189096](https://github.com/pytorch/pytorch/pull/189096))
- Fix silent miscompiles and illegal memory accesses when exact index expressions overflow 32-bit addressing ([#189108](https://github.com/pytorch/pytorch/pull/189108))
- Cache dynamically expanded reduction configurations so later processes do not retune near-tied kernels and select inconsistent performance or numerics ([#189124](https://github.com/pytorch/pytorch/pull/189124))
- Read kernel templates as UTF-8 to prevent locale-dependent `UnicodeDecodeError` compilation failures ([#189196](https://github.com/pytorch/pytorch/pull/189196))
- Fix scheduler `KeyError` failures when mutation propagation creates a self-referential buffer dependency ([#189288](https://github.com/pytorch/pytorch/pull/189288))
- Prevent `torch.compile` from hanging indefinitely when an Inductor compile-worker subprocess dies or shuts down unexpectedly ([#189290](https://github.com/pytorch/pytorch/pull/189290))
- Fix severe `torch.erfc` and `torch.special.gammaincc` tail inaccuracies on MPS in eager and compiled execution ([#189291](https://github.com/pytorch/pytorch/pull/189291))
- Fix compiled RNG-consuming fallback operators on XPU by using accelerator-neutral default-generator handling ([#189310](https://github.com/pytorch/pytorch/pull/189310))
- Fix invalid generated Python for user-defined Triton kernels whose metadata contains `Enum` values by serializing each enum's underlying value ([#189494](https://github.com/pytorch/pytorch/pull/189494))
- Fix XPU compilation of quantized tensor-subclass weights by skipping shared-input linear fusion only when `torch.cat` is unsupported ([#189509](https://github.com/pytorch/pytorch/pull/189509))
- Fix `NameError: name 'u0' is not defined` when compiling `torch.cond` branches whose outputs differ in an inner dimension ([#189529](https://github.com/pytorch/pytorch/pull/189529))
- Fix lowering of `float8_e4m3fn` inputs that use byte-backed Triton storage on CUDA devices older than SM 8.9 ([#189561](https://github.com/pytorch/pytorch/pull/189561))
- Fix `NotImplementedError: make_reindexer NYI on DtypeView(...)` when compiling dtype-bitcast workloads such as MXFP8 scaling ([#189584](https://github.com/pytorch/pytorch/pull/189584))
- Avoid wrong results and illegal memory accesses from compiled CUDA `ConvTranspose2d` by using the ATen implementation ([#189660](https://github.com/pytorch/pytorch/pull/189660))
- Prevent result corruption when memory planning reuses storage returned by mutating fallback operators ([#189735](https://github.com/pytorch/pytorch/pull/189735))
- Prevent NVGEMM compilation failures by rejecting kernels that do not support the exact target GPU architecture ([#189775](https://github.com/pytorch/pytorch/pull/189775))
- Fix a compilation hang caused by reentrant NVGEMM epilogue-kernel cache lookup ([#189780](https://github.com/pytorch/pytorch/pull/189780))
- Fix CUDA Graph capture failures for NVGEMM `addmm` epilogues whose outputs are intermediate tensors ([#189781](https://github.com/pytorch/pytorch/pull/189781))
- Fix `RuntimeError: Graph output must be a ()` when Inductor rewrites a non-tuple FX graph output into a tuple ([#189887](https://github.com/pytorch/pytorch/pull/189887))
- Fix `Unregistered range symbol` failures after fused Triton epilogues rename their iteration index ([#189890](https://github.com/pytorch/pytorch/pull/189890))
- Fix silently wrong results when a padded tensor is fused into a split reduction and its masked load is served from the common-subexpression store cache ([#189896](https://github.com/pytorch/pytorch/pull/189896))
- Fix silently incorrect gradients in compiled convolution, pooling, and `torch.where` graphs when scheduler recomputation loses mutation dependencies ([#185873](https://github.com/pytorch/pytorch/pull/185873))
- Fix `NoValidChoicesError` for dynamic-shape ROCm matrix multiplication by using ROCm's `origami` GEMM performance model only when dimensions are statically known ([#190024](https://github.com/pytorch/pytorch/pull/190024))
- Fix AOTInductor constant-graph code generation when runtime constant folding and lazy autotuning are enabled together ([#190073](https://github.com/pytorch/pytorch/pull/190073))
- Fix FX-wrapper code generation for aliased fallback outputs that have no unbacked-symbol bindings ([#190255](https://github.com/pytorch/pytorch/pull/190255))
- Preserve an explicit `dtype=` when Inductor replaces constant `torch.cumsum` patterns ([#190328](https://github.com/pytorch/pytorch/pull/190328))
- Reject unsound loop-index inversions that could generate incorrect indexing expressions during fusion ([#190401](https://github.com/pytorch/pytorch/pull/190401))
- Fall back to backend code generation instead of raising `OverflowError` when index propagation casts `inf` or `NaN` to an integer dtype ([#190427](https://github.com/pytorch/pytorch/pull/190427))
- Fix cross-warp read-after-write races after stores inside reduction loops by inserting a barrier before reading the buffer ([#190519](https://github.com/pytorch/pytorch/pull/190519))
- Match eager behavior for `AdaptiveAvgPool2d(0)` with `int64` inputs by returning an empty output instead of rejecting the dtype ([#190531](https://github.com/pytorch/pytorch/pull/190531))
- Fix severe precision loss for small values of CPU-vectorized `torch.expm1` by using the vectorized `expm1` intrinsic instead of computing `exp(x) - 1` ([#190533](https://github.com/pytorch/pytorch/pull/190533))
- Fix `LoweringException: 'float' object has no attribute 'get_dtype'` for floating-point floor division with a Python-scalar dividend ([#190566](https://github.com/pytorch/pytorch/pull/190566))
- Fix dynamic-shape compilation failures caused by reciprocal powers in symbolic stride guards ([#190965](https://github.com/pytorch/pytorch/pull/190965))
- Fix incorrect or nondeterministic results for indexing expressions whose surviving modular-index terms may be negative ([#190966](https://github.com/pytorch/pytorch/pull/190966))
- Preserve positional arguments to operations such as `torch.clamp` during pre-gradient batch-math fusion ([#190976](https://github.com/pytorch/pytorch/pull/190976))
- Fix C++ compilation failures when Python library search paths contain spaces ([#191010](https://github.com/pytorch/pytorch/pull/191010))
- Fix incorrect results from compiled small matrix multiplications with transposed operands ([#191127](https://github.com/pytorch/pytorch/pull/191127))
- Fix compiled `int32` and `int64` addition, subtraction, and multiplication on CPU to preserve PyTorch wrapping semantics on overflow ([#191132](https://github.com/pytorch/pytorch/pull/191132))
- Fix compile failures when a fused scaled-dot-product-attention pattern incorrectly matches unsupported 3D key permutations ([#191260](https://github.com/pytorch/pytorch/pull/191260))
- Stop repeated `TypedStorage is deprecated` warnings while Inductor sizes autotuning outputs ([#191383](https://github.com/pytorch/pytorch/pull/191383))
- Fix CPU max-autotune batched-matmul compilation when a GEMM output is both returned and consumed by another operation ([#191502](https://github.com/pytorch/pytorch/pull/191502))
- Fall back from tiling analysis instead of raising `InductorError: AssertionError` for nested modular-indexing or floor-division expressions ([#191605](https://github.com/pytorch/pytorch/pull/191605))
- Fix `uniform_` on non-contiguous views producing NaNs or out-of-range values under `torch.compile` ([#191709](https://github.com/pytorch/pytorch/pull/191709))
- Honor `torch.use_deterministic_algorithms()` for compiled scans such as CUDA `cumsum` ([#191714](https://github.com/pytorch/pytorch/pull/191714))
- Fix failures in Inductor's FX wrapper backend when a `torch.cond` branch captures a compound symbolic integer such as `2*s0 + 1` ([#191811](https://github.com/pytorch/pytorch/pull/191811))
- Fix an out-of-bounds vectorized `atomic_add` in CPU code generation that could abort on x86 or silently produce wrong results on aarch64 ([#191861](https://github.com/pytorch/pytorch/pull/191861))
- Fix silently wrong results in TMA mix-order reductions where the x offset was not advanced between loop iterations ([#192344](https://github.com/pytorch/pytorch/pull/192344))
- Prevent the CUTLASS backend from generating unsupported INT8 UMMA kernels on SM 10.7 GPUs ([#192414](https://github.com/pytorch/pytorch/pull/192414))
- Fix out-of-bounds `IndexError` failures during `addmm` autotuning when a symbolic row count is hinted as zero ([#192553](https://github.com/pytorch/pytorch/pull/192553))
- Avoid races while loading saved compiler-cache artifacts by populating bundled Triton kernels on demand through the JIT path instead of eagerly; cold cache loads may compile kernels on first use ([#192526](https://github.com/pytorch/pytorch/pull/192526))

## Ahead-Of-Time Inductor (AOTI)

- Fix compilation and dispatch failures for C++ wrapper fallback operators with `Any` arguments, including distributed operators such as `all_gather_into_tensor` ([#188124](https://github.com/pytorch/pytorch/pull/188124))
- Route custom operators with `SymInt`, `SymBool`, or `SymFloat` arguments through boxed C++ wrapper dispatch, avoiding runtime `API call failed` errors ([#188154](https://github.com/pytorch/pytorch/pull/188154))
- Box `None` passed to non-optional tensor arguments as an undefined tensor in C++ wrappers, matching eager custom-operator behavior ([#188485](https://github.com/pytorch/pytorch/pull/188485))
- Prevent C++ wrappers from dereferencing a null tensor handle when a Python fallback operator returns a one-element `Tensor[]` ([#190551](https://github.com/pytorch/pytorch/pull/190551))
- Emit portable `std::array::data()` pointers in generated CPU wrappers instead of relying on iterator-to-pointer conversion ([#191240](https://github.com/pytorch/pytorch/pull/191240))
- Package AOTInductor CUDA multi-architecture kernels for the requested deployment architecture instead of the physical compilation GPU ([#185328](https://github.com/pytorch/pytorch/pull/185328))
- Fix AOTInductor C++ wrappers recovering integer symbols from composed dynamic sizes through floating-point division, which could truncate valid runtime dimensions ([#185841](https://github.com/pytorch/pytorch/pull/185841))
- Fail fast with a clear error when loading a CUDA AOTInductor package in a process without CUDA or ROCm available ([#186943](https://github.com/pytorch/pytorch/pull/186943))
- Fix C++ wrapper fallback output indexing for mutable custom operators and remove invalid 16-byte alignment assumptions for misaligned tensor views ([#187331](https://github.com/pytorch/pytorch/pull/187331))
- Preserve C++ wrapper input slots when graphs contain Python-only custom-class inputs ([#188030](https://github.com/pytorch/pytorch/pull/188030))
- Pass the device the model was actually loaded on to custom operator fallbacks, instead of the device recorded when the model was compiled. Previously a model compiled for one GPU and then loaded on another would hand the wrong device to its custom ops ([#184741](https://github.com/pytorch/pytorch/pull/184741))
- Synchronize the default stream after copying model constants on AMD GPUs, fixing a race in which inference could read constants before the copy had completed ([#186963](https://github.com/pytorch/pytorch/pull/186963))
- Fix a 32-bit integer overflow when computing the SYCL global launch range in the AOTInductor runtime, which produced incorrect launch dimensions for large grids on XPU ([#187307](https://github.com/pytorch/pytorch/pull/187307))
- Release AOTInductor input tensor handles when runtime input validation fails, preventing a GPU memory leak ([#189503](https://github.com/pytorch/pytorch/pull/189503))
- Release untransferred AOTInductor constants when runtime constant folding fails, preventing a memory leak on the error path ([#189505](https://github.com/pytorch/pytorch/pull/189505))
- Prevent an AOTInductor constant-folding segmentation fault on XPU when no stream is provided ([#189517](https://github.com/pytorch/pytorch/pull/189517))
- Make the C++ wrapper's debug synchronization device-aware, fixing a regression on ROCm ([#190071](https://github.com/pytorch/pytorch/pull/190071))
- Fix a missing CUDA header in the generated constant graph when compiling with the dual-wrapper, which made the generated code fail to compile ([#191050](https://github.com/pytorch/pytorch/pull/191050))
- Skip CUDA stream event code generation in the AOTInductor C++ wrapper on XPU, where those APIs do not apply ([#190637](https://github.com/pytorch/pytorch/pull/190637))

## Export

- Fix `torch.export` dynamic-shape specifications for functions with `**kwargs`, accepting both call-like keys and specs nested under the variadic parameter while reporting ambiguous name collisions as `UserError` ([#185730](https://github.com/pytorch/pytorch/pull/185730))
- Prevent `ExportedProgram.module()` from raising `RecursionError` while generating guard messages for deeply nested symbolic-shape expressions ([#186993](https://github.com/pytorch/pytorch/pull/186993))
- Fix `torch.export.unflatten` failing to restore parameters, buffers, and constants for non-contiguously numbered repeated module calls ([#188185](https://github.com/pytorch/pytorch/pull/188185))
- Fix strict export of parameters from modules stored in unregistered Python containers by treating the traced-only parameters as constants instead of attempting to restore them from the eager module's state ([#185728](https://github.com/pytorch/pytorch/pull/185728))
- Fix non-strict export of tensor indexing under `vmap` when the index is a batched scalar tensor ([#186894](https://github.com/pytorch/pytorch/pull/186894))

## AOTDispatcher

- Resolve nested `AsyncCollectiveTensor` inputs before AOTAutograd tracing so compiled forward execution waits for in-flight data and backward metadata expects the correct local-tensor cotangents ([#186442](https://github.com/pytorch/pytorch/pull/186442))
- Prevent activation-memory-budget partitioning from crashing with `expected all tensors_saved_with_vc_check to be Tensors, got [Tensor, tuple]` when a required multi-output node is marked `MUST_SAVE` ([#188014](https://github.com/pytorch/pytorch/pull/188014))
- Prevent AOTAutograd common-subexpression elimination from merging forward-only values with nodes required by backward, preserving correct partitioning and reduction fusion ([#184044](https://github.com/pytorch/pytorch/pull/184044))
- Fix backward graphs missing symbolic-integer bindings by preserving both raw symbols and their ShapeEnv replacement targets, preventing unbound guard expressions and `FxGraphCache` lookup failures ([#185473](https://github.com/pytorch/pytorch/pull/185473), [#189783](https://github.com/pytorch/pytorch/pull/189783))
- Fix incorrect alias-output slicing when Inductor clones a misaligned input ([#191002](https://github.com/pytorch/pytorch/pull/191002))
- Move `invoke_subgraph` inference-mode input mutations to the AOT epilogue so they are applied correctly ([#191672](https://github.com/pytorch/pytorch/pull/191672))
- Fix `control_deps` handling in the partitioner during forward/backward extraction ([#187695](https://github.com/pytorch/pytorch/pull/187695))
- Support mutable (`Tensor!`) custom ops in input-mutating `invoke_subgraph` regions by routing them through Python functionalization ([#189543](https://github.com/pytorch/pytorch/pull/189543))
- Fix common subexpression elimination (CSE) to correctly deduplicate NaN constant tensors by normalizing float/complex hashing and comparison ([#191173](https://github.com/pytorch/pytorch/pull/191173))

## Composability

- Raise `NotImplementedError` for unsupported Boolean operations and distinguish unsupported FFT dtypes from invalid real/complex domains with `NotImplementedError` and `TypeError` ([#192348](https://github.com/pytorch/pytorch/pull/192348), [#192349](https://github.com/pytorch/pytorch/pull/192349))
- Preserve eager identity semantics for no-op dropout decompositions, preventing `torch.compile` and `torch.export` from replacing a `Parameter` with a cloned fake tensor when dropout is disabled ([#185335](https://github.com/pytorch/pytorch/pull/185335))
- Fix compiled `torch.nn.functional.multilabel_margin_loss` values and gradients when targets use `-1` padding ([#189552](https://github.com/pytorch/pytorch/pull/189552))
- Fix `torch.nansum` meta output shapes when `dim=()` should reduce all dimensions ([#191530](https://github.com/pytorch/pytorch/pull/191530))
- Make the `constant_pad_nd` reference decomposition fully functional so `torch.onnx.export(dynamo=True)` no longer fails functionalization for models using `torch.nn.functional.pad` ([#185636](https://github.com/pytorch/pytorch/pull/185636))
- Keep `torch.istft` length clamping and padding symbolic under dynamic shapes, avoiding recompilation and data-dependent guard failures when the requested length crosses the signal length ([#186490](https://github.com/pytorch/pytorch/pull/186490))
- Make compiled and fake/meta `torch.aminmax(..., out=...)` enforce the same exact output-dtype requirements as eager execution ([#186227](https://github.com/pytorch/pytorch/pull/186227))
- Make compiled `torch.nn.functional.celu` reject `alpha=0` with the same error as eager execution ([#179375](https://github.com/pytorch/pytorch/pull/179375))
- Avoid data-dependent guard failures in fake/meta tracing of native multi-head attention with unbacked symbolic sizes ([#187144](https://github.com/pytorch/pytorch/pull/187144))
- Avoid data-dependent guards in `torch.nn.utils.rnn.pad_sequence` decompositions when sequence lengths are symbolic ([#187145](https://github.com/pytorch/pytorch/pull/187145))
- Make the CUDA `native_layer_norm` decomposition reject mixed affine-parameter dtypes in the same cases as eager execution ([#185693](https://github.com/pytorch/pytorch/pull/185693))
- Fix incorrect compiled output and gradients for overlapping-input `torch.diagonal_scatter` operations ([#182292](https://github.com/pytorch/pytorch/pull/182292))
- Match compiled `max_unpool2d` output strides and channels-last memory format to eager CPU execution ([#186602](https://github.com/pytorch/pytorch/pull/186602), [#187195](https://github.com/pytorch/pytorch/pull/187195))
- Route meta `view` operations through the symbolic-shape-aware kernel, avoiding `SymIntArrayRef expected to contain only concrete integers` failures ([#189447](https://github.com/pytorch/pytorch/pull/189447))
- Avoid data-dependent guard failures in the transformer encoder layer meta kernel when the input size is an unbacked symbol ([#187860](https://github.com/pytorch/pytorch/pull/187860))
- Prevent fake/meta decompositions of in-place operations from silently resizing their destination when operands cannot broadcast to its shape; compiled execution now raises the same shape error as eager execution ([#191373](https://github.com/pytorch/pytorch/pull/191373))
- Preserve symbolic tensor, scalar, and unbacked-binding metadata across `ProxyTensor` and `make_fx` tracing ([#187231](https://github.com/pytorch/pytorch/pull/187231))
- Preserve loop-local value ranges and use known ranges when simplifying symbolic `Min` and `Max` expressions, avoiding `vr must not be None` and spurious data-dependent guard failures ([#187350](https://github.com/pytorch/pytorch/pull/187350), [#186248](https://github.com/pytorch/pytorch/pull/186248))
- Fix symbolic proxy tracing and repeated lowering edge cases involving natural powers, `torch.cond` contiguous-stride expressions, and equivalent rebound unbacked symbols ([#188278](https://github.com/pytorch/pytorch/pull/188278), [#189525](https://github.com/pytorch/pytorch/pull/189525), [#190083](https://github.com/pytorch/pytorch/pull/190083))
- Fix silently incorrect second-order gradients from post-dispatch `make_fx` tracing by decomposing `detach` by default; callers that provide an explicit decomposition table retain the previous behavior ([#186845](https://github.com/pytorch/pytorch/pull/186845))

## Quantization

- Fix a divide-by-zero crash (`SIGFPE`) in `torch.quantize_per_channel` on the per-channel `float_qparams` path for the `qint32` dtype; whole-byte quantized types now pack correctly instead of underflowing the packing factor to zero ([#186767](https://github.com/pytorch/pytorch/pull/186767))
- Add the missing overflow check to the FBGEMM build of the ARM `quantize_val` path, fixing incorrect quantized values that showed up as quantization test failures on some hardware ([#187481](https://github.com/pytorch/pytorch/pull/187481))
- Fix a GPU memory access fault that aborted quantized `embedding_bag` byte and 4-bit rowwise lookups on ROCm, caused by a bitwise-AND typo in the bit-field extraction primitive ([#192571](https://github.com/pytorch/pytorch/pull/192571))

## Foreach

- Prevent out-of-bounds metadata writes in CUDA foreach operations with complex scalar lists by respecting their reduced per-launch tensor capacity ([#189915](https://github.com/pytorch/pytorch/pull/189915))

## ONNX

- Fix signed right-shift export in the TorchScript exporter so negative values round toward negative infinity as they do in PyTorch ([#191226](https://github.com/pytorch/pytorch/pull/191226))
- Fix quantized `gather` export by unpacking quantized tensor inputs before lowering ([#188272](https://github.com/pytorch/pytorch/pull/188272))

## C++ Frontend

- Fix a memory leak when converting `StableIValue` to `std::string` ([#190493](https://github.com/pytorch/pytorch/pull/190493))
- Remove `noexcept` from `TensorMaker::computeStorageSize()` ([#188062](https://github.com/pytorch/pytorch/pull/188062))
- Fix uninitialized return in Chebyshev polynomial helpers for NaN inputs ([#187767](https://github.com/pytorch/pytorch/pull/187767))
- Guard the `Scalar(long long)` constructor on NetBSD and other LP64 BSDs ([#188941](https://github.com/pytorch/pytorch/pull/188941))
- Replace `FileBaton` with `filelock` to prevent stale-lock deadlocks in `CppExtension` ([#190543](https://github.com/pytorch/pytorch/pull/190543))
- Fix floating-point-to-integer range checks at wide-integer boundaries in `c10/util/overflows.h` ([#190651](https://github.com/pytorch/pytorch/pull/190651))

## Build Frontend

- Fix source-build linker failures on systems where CMake reordered static and shared libraries by linking `libcpuinfo` through the `c10` shared library instead of linking it separately into both `c10` and `torch_cpu` ([#167328](https://github.com/pytorch/pytorch/pull/167328))
- Fix Windows ARM64 builds failing to register a CPU quantized backend by recognizing the uppercase `ARM64` CMake processor name and enabling oneDNN ([#189346](https://github.com/pytorch/pytorch/pull/189346))

## Release Engineering

- Fix invalid ZIP64 archives for ROCm wheels larger than 4 GB by repackaging them with `auditwheel` ([#189903](https://github.com/pytorch/pytorch/pull/189903))
- Prevent an intermittent deadlock during `import torch` with ROCm wheels by shipping a bare `.so` alias ([#189114](https://github.com/pytorch/pytorch/pull/189114))
- Fix missing CUDA dependencies when extracting LibTorch from a wheel, which previously left the extracted tree with unresolved RPATHs ([#184336](https://github.com/pytorch/pytorch/pull/184336))

## CUDA

- Fix CUDA graph kernel-annotation remapping across sequentially captured graphs and with `keep_graph=True` ([#186638](https://github.com/pytorch/pytorch/pull/186638), [#187741](https://github.com/pytorch/pytorch/pull/187741))
- Fix a heap overflow in `CachingHostAllocator` when rounding is disabled ([#192722](https://github.com/pytorch/pytorch/pull/192722))
- Preserve signed zero in `relu` and `clamp` ([#185354](https://github.com/pytorch/pytorch/pull/185354))
- Fix `int32` overflow in `embedding_bag(mode="max")` backward ([#188661](https://github.com/pytorch/pytorch/pull/188661))
- Include CUDA graph memory pools in `memory_reserved()` ([#186809](https://github.com/pytorch/pytorch/pull/186809))
- Use 64-bit sample offsets in `NLLLoss2d` backward ([#190144](https://github.com/pytorch/pytorch/pull/190144))
- Fix remap extents, causal key bounds, and 32-bit dropout offsets in memory-efficient attention ([#192138](https://github.com/pytorch/pytorch/pull/192138))

## cuDNN

- Fix cuDNN variable-length SDPA ([#172108](https://github.com/pytorch/pytorch/pull/172108))
- Disable cuDNN convolution engines 58 and 63 on `sm120` to prevent illegal memory accesses ([#190112](https://github.com/pytorch/pytorch/pull/190112))
- Declare the attention-mask dtype to cuDNN instead of inheriting the graph I/O dtype ([#191612](https://github.com/pytorch/pytorch/pull/191612))
- Update the cuDNN errata filter for `sm120` ([#191701](https://github.com/pytorch/pytorch/pull/191701))

## CPU (x86)

- Fix incorrect results from CPU flash SDPA when the innermost dimension of the inputs is not contiguous ([#187506](https://github.com/pytorch/pytorch/pull/187506))
- Prevent the Laguerre and Legendre polynomial kernels from returning uninitialized memory ([#188027](https://github.com/pytorch/pytorch/pull/188027))

## CPU (AArch64)

- Fix an integer overflow in the `bfloat16`/`float16` GEMM staging-buffer size calculation, which could corrupt results or crash on large matrix multiplications ([#191096](https://github.com/pytorch/pytorch/pull/191096))
- Fix CPU `embedding_bag` using the wrong index count for `scale_grad_by_freq`, producing incorrect gradients ([#190264](https://github.com/pytorch/pytorch/pull/190264))

## MPS

- Fix compiled MPS operations such as `torch.eye(256)` failing with `KeyError` when Inductor generates unsigned 16-, 32-, or 64-bit index expressions ([#192020](https://github.com/pytorch/pytorch/pull/192020))
- Preserve the MPS dispatch key through `torch.func` transforms so MPS autocast and autograd work under transforms such as `vmap` and `grad` ([#187282](https://github.com/pytorch/pytorch/pull/187282))
- Reject complex MPS average-pooling inputs with `NotImplementedError` instead of an internal MPSGraph error ([#187671](https://github.com/pytorch/pytorch/pull/187671))
- Propagate NaNs correctly through MPS scaled dot-product attention kernels ([#188147](https://github.com/pytorch/pytorch/pull/188147))
- Raise a clear error when MPS batch normalization receives an unsupported dtype ([#188265](https://github.com/pytorch/pytorch/pull/188265))
- Fix corrupted MPS prefill-attention output on macOS 26 by selecting the correct Metal cooperative-tensor ABI ([#191794](https://github.com/pytorch/pytorch/pull/191794))
- Fix Metal argument alignment that could make MPS kernels fail validation or crash under the Metal debug layer ([#191640](https://github.com/pytorch/pytorch/pull/191640))
- Fix `torch.hypot` producing incorrect results for extreme values ([#192541](https://github.com/pytorch/pytorch/pull/192541))
- Handle empty indices in MPS `index_add` and empty dimensions in threshold, `baddbmm`, and `addbmm` operations ([#186990](https://github.com/pytorch/pytorch/pull/186990), [#187719](https://github.com/pytorch/pytorch/pull/187719), [#188808](https://github.com/pytorch/pytorch/pull/188808), [#187879](https://github.com/pytorch/pytorch/pull/187879))
- Fix `mm` and `addmm` with strided output tensors on macOS 14 and 15 ([#187255](https://github.com/pytorch/pytorch/pull/187255))
- Respect `storage_offset` when an MPS binary operation consumes a zero-dimensional CPU tensor view ([#187229](https://github.com/pytorch/pytorch/pull/187229))
- Make MPS `baddbmm` follow its documented behavior by not propagating NaN or infinity from the input when `beta=0` ([#187522](https://github.com/pytorch/pytorch/pull/187522))
- Fix MPS linear backward for inputs with more than four dimensions and prevent complex high-rank linear operations from aborting on macOS 27 ([#187379](https://github.com/pytorch/pytorch/pull/187379), [#190352](https://github.com/pytorch/pytorch/pull/190352))
- Prevent `BatchNorm` backward from crashing for channels-last MPS tensors ([#188371](https://github.com/pytorch/pytorch/pull/188371))
- Fix incorrect MPS Conv2d output when a kernel spatial dimension is at least 256 ([#188359](https://github.com/pytorch/pytorch/pull/188359))
- Match CPU and CUDA nonfinite-value semantics for MPS `torch.div(..., rounding_mode="floor")` ([#189252](https://github.com/pytorch/pytorch/pull/189252))
- Make MPS-backed pinned memory correctly appear as a CPU tensor while retaining its shared Metal buffer ([#181720](https://github.com/pytorch/pytorch/pull/181720))
- Prevent dtype-converting MPS-to-CPU copies from overwriting their source and correctly copy non-dense views with matching strides ([#189572](https://github.com/pytorch/pytorch/pull/189572), [#189966](https://github.com/pytorch/pytorch/pull/189966))
- Compute integer absolute values exactly instead of rounding through `float32` ([#190053](https://github.com/pytorch/pytorch/pull/190053))
- Handle zero `in_features` in MPS linear forward and backward without aborting ([#190051](https://github.com/pytorch/pytorch/pull/190051))
- Fix `torch.nextafter` returning its input unchanged for MPS `bfloat16` tensors ([#190481](https://github.com/pytorch/pytorch/pull/190481))
- Preserve exact integer values in MPS `torch.linspace` for large ranges ([#189630](https://github.com/pytorch/pytorch/pull/189630))
- Fix `int64` minimum and maximum reductions returning zero when a partial SIMD group contains only negative or positive values ([#191104](https://github.com/pytorch/pytorch/pull/191104))
- Fix adaptive max pooling for input sizes that are not divisible by the output size ([#189659](https://github.com/pytorch/pytorch/pull/189659))
- Fix large matrix multiplications producing incorrect results on M1 and M2 GPUs ([#183535](https://github.com/pytorch/pytorch/pull/183535))
- Keep MPS exponential samples strictly positive so `torch.multinomial(..., 1)` cannot select a zero-probability entry ([#192621](https://github.com/pytorch/pytorch/pull/192621))
- Make CPU and MPS `torch.logit` agree with other backends when `eps > 0.5` ([#181297](https://github.com/pytorch/pytorch/pull/181297))
- Fix MPS FFT operations when a transformed dimension is not among the tensor's final four dimensions ([#186967](https://github.com/pytorch/pytorch/pull/186967))
- Fix `torch.nn.functional.linear` dropping its bias for vector-shaped inputs on macOS 26 ([#188619](https://github.com/pytorch/pytorch/pull/188619))
- Raise clear unsupported-dtype errors for complex MPS inputs to `cummax`, `cummin`, and `logaddexp2` ([#188038](https://github.com/pytorch/pytorch/pull/188038), [#188800](https://github.com/pytorch/pytorch/pull/188800))
- Fix MPS ternary-kernel dispatch for large tensors and mixed-dtype `out=` tensors, including `torch.clamp` ([#189624](https://github.com/pytorch/pytorch/pull/189624))
- Apply inter-layer dropout correctly in MPS LSTM backward and avoid NaNs when `dropout=1` ([#190059](https://github.com/pytorch/pytorch/pull/190059))
- Improve MPS layer-normalization correctness for small-variance rows and add 64-bit indexing support ([#190492](https://github.com/pytorch/pytorch/pull/190492))
- Fix biased MPS linear operations corrupting rows when a batch dimension exceeds 2^16 ([#189496](https://github.com/pytorch/pytorch/pull/189496))
- Validate MPS `EmbeddingBag` offsets consistently with CPU and CUDA instead of silently returning incorrect results ([#187572](https://github.com/pytorch/pytorch/pull/187572))
- Support `float32` affine parameters with `float16` or `bfloat16` MPS layer normalization in forward and backward ([#190055](https://github.com/pytorch/pytorch/pull/190055))
- Match CPU and CUDA RMSNorm precision by performing the fused affine multiplication in float32 ([#189617](https://github.com/pytorch/pytorch/pull/189617))
- Fix Conv2d forward and backward with non-contiguous MPS weights ([#192303](https://github.com/pytorch/pytorch/pull/192303))
- Raise clear unsupported-dtype errors for complex `igamma`/`igammac` and boolean `torch.linalg.cross` inputs on MPS ([#188134](https://github.com/pytorch/pytorch/pull/188134), [#187274](https://github.com/pytorch/pytorch/pull/187274))
- Prevent intermittent crashes when stopping a Metal capture by draining work from all active MPS streams first ([#191362](https://github.com/pytorch/pytorch/pull/191362))

## ROCm

- Fix `torch.nn.functional.interpolate` with `mode="nearest"` failing on large channels-last inputs with `torch.AcceleratorError: HIP error: invalid configuration argument`. The channels-last `upsample_nearest2d` forward kernel launched a grid whose total thread count exceeded HIP's `UINT32_MAX` limit once the output approached 2^32 elements; this was a regression from 2.9 that showed up in diffusion VAE decode at large batch sizes ([#180310](https://github.com/pytorch/pytorch/pull/180310))
- Fix incorrect `torch.nn.LayerNorm` results for tensors with a very large number of rows when the normalized size is not a multiple of 4. The non-vectorized fallback exceeded HIP's launch limit; it now uses a grid-stride loop over rows ([#186956](https://github.com/pytorch/pytorch/pull/186956))
- Fix `torch.cuda.make_graphed_callables` failing to capture, or hanging, on ROCm when the callable uses hipBLASLt. Warmup and capture now run on the same stream so the hipBLASLt handle is created and cached before capture instead of being lazily created mid-capture ([#187745](https://github.com/pytorch/pytorch/pull/187745))
- Fix graph-capture error handling on ROCm 7.14 and later by using HIP's native capture errors instead of the compatibility precheck required by older ROCm versions ([#187110](https://github.com/pytorch/pytorch/pull/187110))
- Fix transposed convolution failing with `miopenStatusBadParm` when the computed spatial output is zero-sized. MIOpen rejects zero-length tensor descriptors, so these cases now short-circuit to an empty output (and zero gradients in backward), matching cuDNN and CPU behavior ([#187431](https://github.com/pytorch/pytorch/pull/187431))
- Fix a meta-kernel shape mismatch for memory-efficient scaled dot product attention on ROCm. The meta registration padded the log-sum-exp dimension to a 32-element alignment as CUDA does, while the ROCm backends return a compact log-sum-exp, breaking nested tensor SDPA backward and `torch.compile` ([#190723](https://github.com/pytorch/pytorch/pull/190723))
- Fix the memory-wait instructions used by the atomic-store commit path on `gfx10`, `gfx11`, and `gfx12` GPUs. These architectures have separate load and store counters, and `gfx12` renames the wait instructions, so the wrong instruction was previously emitted ([#188067](https://github.com/pytorch/pytorch/pull/188067))
- Fix failures when building HIP C++ extensions on Windows with `Don't know how to compile <file>.hip`. `.hip` sources produced by hipify are now registered with the MSVC compiler so they are dispatched to `hipcc` ([#187665](https://github.com/pytorch/pytorch/pull/187665))
- Fix out-of-bounds accesses in CK SDPA for tile-unaligned shapes by padding sequence-length allocations ([#187152](https://github.com/pytorch/pytorch/pull/187152))

## XPU

- Fix compiled `torch.signbit` for `float64` inputs on XPU by avoiding an incorrect Triton XPU signature ([#188818](https://github.com/pytorch/pytorch/pull/188818))
- Fix compiled `multi_margin_loss` with weights on XPU by using one-dimensional indexing in its decomposition ([#188770](https://github.com/pytorch/pytorch/pull/188770))
- Handle empty tensor inputs correctly in XPU `addmv` ([#174193](https://github.com/pytorch/pytorch/pull/174193))
- Fix oneDNN SDPA with GQA and a broadcasted mask on XPU ([#190503](https://github.com/pytorch/pytorch/pull/190503))
- Fix `max_unpool2d` channels-last stride mismatch on XPU ([#190189](https://github.com/pytorch/pytorch/pull/190189))
- Fix `bmm_outer_product` Triton override to support XPU tensors ([#188783](https://github.com/pytorch/pytorch/pull/188783))
- Raise `RuntimeError` instead of crashing when XPU cannot allocate a pinned host-memory buffer ([#189681](https://github.com/pytorch/pytorch/pull/189681))
- Route `GPU_USER_ANNOTATION` Kineto profiler events to `DeviceType::XPU` ([#191841](https://github.com/pytorch/pytorch/pull/191841))

## Functorch

- Fix a crash in `torch.func.vmap` when `out_dims=-1` and the mapped function returns an output that is independent of its vmapped input ([#178495](https://github.com/pytorch/pytorch/pull/178495))

## JIT

- Make TorchScript reject bare `list` and `tuple` value annotations consistently with `Attempted to use list without a contained type` or the equivalent tuple error; specify an element type such as `list[int]` instead ([#188779](https://github.com/pytorch/pytorch/pull/188779))
- Fix runtime compilation of JIT fuser kernels on ROCm 7 when HIPRTC's `bfloat16` conversion symbols collide with PyTorch's embedded definitions ([#185656](https://github.com/pytorch/pytorch/pull/185656))
- Fix `torch.jit.script` failing with `Cannot re-assign modules in a ScriptModule with non-scripted module` when a wrapper contains an already-scripted child with a `__jit_ignored_attributes__` submodule ([#187863](https://github.com/pytorch/pytorch/pull/187863))

## Sparse Frontend

- Create cuSPARSELt handles per device so sparse operations remain valid when a thread switches between CUDA devices ([#189048](https://github.com/pytorch/pytorch/pull/189048))
- Make grouped-matrix, batch-normalization, and sparse-matrix operations on ROCm Windows raise clear unsupported-operation errors instead of crashing with access violation `0xC0000005` when optional libraries are unavailable ([#191680](https://github.com/pytorch/pytorch/pull/191680))

# Performance

## Python Frontend

- Add a Python-object dispatch fast path for Python-implemented custom operators, reducing no-op dispatch overhead when all relevant kernels are registered in Python ([#187949](https://github.com/pytorch/pytorch/pull/187949))
- Speed up CPU `torch.quantile` and `torch.nanquantile` by using partial selection instead of fully sorting when only a small number of quantiles is requested ([#188394](https://github.com/pytorch/pytorch/pull/188394))
- Reduce mutable `torch.library.custom_op` dispatch overhead by bumping version counters only for mutated arguments actually supplied by the caller ([#186175](https://github.com/pytorch/pytorch/pull/186175))

## torch.nn

- Avoid materializing zero-filled gradients for unused outputs of chunked `linear_cross_entropy`, substantially reducing backward peak memory ([#187219](https://github.com/pytorch/pytorch/pull/187219))
- Use a faster automatic chunking strategy for `linear_cross_entropy` while capping chunk size so peak memory stays at or below the unchunked implementation ([#187838](https://github.com/pytorch/pytorch/pull/187838))
- Avoid materializing copy-on-write tensors while the fused RMSNorm override checks input and weight alignment ([#189202](https://github.com/pytorch/pytorch/pull/189202))

## Autograd

- Reduce `torch.autograd.Function.apply` overhead by avoiding unused profiler input copies, borrowed-input `Tensor` refcount churn, output copies, and unnecessary dead-wrapper processing. The profiler change alone saves approximately 0.3–0.4 microseconds in the reported custom-function benchmark ([#189582](https://github.com/pytorch/pytorch/pull/189582), [#189788](https://github.com/pytorch/pytorch/pull/189788), [#189800](https://github.com/pytorch/pytorch/pull/189800), [#189577](https://github.com/pytorch/pytorch/pull/189577))
- Enable the compiler to constant-fold more floating-point constants in generated backward formulas, reducing runtime computation while keeping the simplified constants within one ULP of the originals ([#192611](https://github.com/pytorch/pytorch/pull/192611))

## Distributed

- Balance context-parallel packed-document attention work across ranks with rank-major head-tail layout ([#189902](https://github.com/pytorch/pytorch/pull/189902))

## Symmetric Memory

- Add a copy-engine multicast implementation of low-contention symmetric-memory all-gather with improved bandwidth and compute overlap ([#185359](https://github.com/pytorch/pytorch/pull/185359))
- Let rank 0 use the peer-copy path for symmetric-memory multicast transfers so copies can overlap host transfers ([#192530](https://github.com/pytorch/pytorch/pull/192530))
- Reduce store pressure during large-scale symmetric-memory setup by routing multicast rendezvous through the process group when configured ([#192623](https://github.com/pytorch/pytorch/pull/192623))

## Linear Algebra Frontend

- Speed up CUDA `torch.addmm` when the addend and output are distinct row-major tensors by letting cuBLASLt consume both pointers directly instead of copying the addend into the output first ([#191706](https://github.com/pytorch/pytorch/pull/191706))
- Reduce allocator overhead for batched CUDA LU factorization by allocating the cuSOLVER GETRF workspace once per batch instead of once per matrix ([#181998](https://github.com/pytorch/pytorch/pull/181998))
- Speed up `torch.matmul` for viewable batched inputs with a size-one folded dimension by dispatching through the flattened `mm` path instead of `bmm` ([#186178](https://github.com/pytorch/pytorch/pull/186178))

## FX

- Speed up `GraphModule.delete_all_unused_submodules()` by using constant-time membership checks while determining submodule liveness ([#178320](https://github.com/pytorch/pytorch/pull/178320))
- Release inputs to boxed FX calls before dispatch when they have no other uses, reducing peak memory in compiled backward graphs ([#187186](https://github.com/pytorch/pytorch/pull/187186))

## Dynamo

- Trim the fixed per-call overhead of a compiled function: avoid per-call `DispatchKeySet` pybind churn in `compile_wrapper`, default the guard TLS attributes so `TracingContext.try_get()` avoids a `getattr` miss, and slim the `torch._dynamo.disable` prologue ([#190390](https://github.com/pytorch/pytorch/pull/190390), [#190571](https://github.com/pytorch/pytorch/pull/190571), [#190392](https://github.com/pytorch/pytorch/pull/190392))
- Model `itertools.chain`, `itertools.chain.from_iterable`, and `itertools.zip_longest` natively instead of tracing through a Python polyfill, cutting compile time for those constructs by roughly 4× ([#186973](https://github.com/pytorch/pytorch/pull/186973), [#186974](https://github.com/pytorch/pytorch/pull/186974))
- Skip guard creation for function inputs the compiled code never reads, avoiding spurious recompiles from pass-through arguments ([#187782](https://github.com/pytorch/pytorch/pull/187782))
- Avoid recompiles when a compiled region's input alternates between an `AsyncCollectiveTensor` and the resolved plain `Tensor` ([#189482](https://github.com/pytorch/pytorch/pull/189482))
- Avoid recompiles when Hugging Face Accelerate patches identical module `forward` methods with shared `functools.partial` objects ([#185739](https://github.com/pytorch/pytorch/pull/185739))
- Fix an AOTAutograd cache miss in FlexAttention caused by unpicklable local `torch._check` message closures ([#188177](https://github.com/pytorch/pytorch/pull/188177))
- Reduce per-call overhead for the TVM backend by querying the runtime module's input metadata once when building the executable instead of on every invocation ([#189012](https://github.com/pytorch/pytorch/pull/189012))

## Inductor

- Eliminate an extra clone from compiled stateless RNG operations by allowing Inductor to reinplace their functional variants ([#188495](https://github.com/pytorch/pytorch/pull/188495))
- Select FlexAttention tile sizes by query sequence length on RDNA3 GPUs ([#177840](https://github.com/pytorch/pytorch/pull/177840))
- Enable shared-input linear fusion by default for XPU inference, combining compatible linear layers into one wider GEMM ([#181854](https://github.com/pytorch/pytorch/pull/181854))
- Improve small ROCm reductions by adding a one-thread x-dimension candidate when the non-reduction dimension has at most 64 elements ([#183364](https://github.com/pytorch/pytorch/pull/183364))
- Enable Origami GEMM configuration selection by default for ROCm max-autotuning; set `TORCHINDUCTOR_ORIGAMI=0` to opt out ([#186644](https://github.com/pytorch/pytorch/pull/186644))
- Reduce Triton compilation time for foreach combo kernels by emitting one shared body for equivalent pointwise subkernels ([#184323](https://github.com/pytorch/pytorch/pull/184323))
- Group input size and stride checks that share a first-use point into one C++ guard call, avoiding repeated Python-to-C++ dispatch before the first compiled kernel launch ([#184752](https://github.com/pytorch/pytorch/pull/184752))
- Reduce NVGEMM choice-enumeration and cross-process compilation overhead by scanning the kernel cache once, preserving selected tile hints, and caching epilogue-fusion artifacts on disk ([#185966](https://github.com/pytorch/pytorch/pull/185966), [#185967](https://github.com/pytorch/pytorch/pull/185967), [#187013](https://github.com/pytorch/pytorch/pull/187013))
- Materialize heavily reused CPU pointwise expressions near the operation-count threshold instead of recomputing them for each consumer ([#186356](https://github.com/pytorch/pytorch/pull/186356))
- Keep very large reductions out of combo kernels and add occupancy-based reduction-block autotuning candidates for remaining combo reductions ([#186668](https://github.com/pytorch/pytorch/pull/186668), [#186957](https://github.com/pytorch/pytorch/pull/186957))
- Restore combo-kernel fusion for simple XPU pointwise workloads by using an XPU-compatible autotuning gate ([#187147](https://github.com/pytorch/pytorch/pull/187147))
- Add an opt-in `cat_linear` fusion that avoids materializing a large concatenation immediately consumed by narrow linear layers ([#187880](https://github.com/pytorch/pytorch/pull/187880))
- Restore the faster eager fallback for XPU `max_pool2d_with_indices_backward` instead of compiling its decomposition into Triton ([#187940](https://github.com/pytorch/pytorch/pull/187940))
- Improve persistent-reduction selection with tiling-aware hints and reuse equivalent loads across full-range splits ([#188179](https://github.com/pytorch/pytorch/pull/188179), [#188180](https://github.com/pytorch/pytorch/pull/188180))
- Isolate NVGEMM compilation in subprocesses and share compiled artifacts through the disk cache, avoiding thread-safety failures and duplicate compilation ([#188303](https://github.com/pytorch/pytorch/pull/188303))
- Tune split-reduction thresholds for Blackwell workloads to avoid regressions from the previous flat threshold ([#188579](https://github.com/pytorch/pytorch/pull/188579))
- Expand NVGEMM autotuning choices for tall-K decode workloads with additional tile and cluster configurations ([#188646](https://github.com/pytorch/pytorch/pull/188646))
- Launch host-side TMA kernels through the static Triton launcher instead of falling back to the dynamic launcher on every call ([#188822](https://github.com/pytorch/pytorch/pull/188822))
- Pack lane-uniform FlexAttention predicates such as sequence-length masks into interval masks instead of using slower per-lane evaluation ([#188929](https://github.com/pytorch/pytorch/pull/188929))
- Decompose broadcast-bias `baddbmm` into `bmm` plus a pointwise add so the bias can fuse with surrounding operations ([#189127](https://github.com/pytorch/pytorch/pull/189127))
- Use a fused pointwise multiply-and-reduce kernel for small GPU matrix multiplications with `M >= 64`, `K < 5`, and `N < 5` when max-autotune is disabled ([#189149](https://github.com/pytorch/pytorch/pull/189149))
- Speed up persistent softmax reductions by avoiding redundant NaN propagation in the internal maximum pass while preserving final output semantics ([#189162](https://github.com/pytorch/pytorch/pull/189162))
- Retune FlexAttention defaults for Triton 3.8 and skip unnecessary boundary checks when sparse block sizes divide sequence lengths ([#189187](https://github.com/pytorch/pytorch/pull/189187))
- Improve NVGEMM small-M and block-scaled workloads with operand swapping, fused runtime scaling, and expanded kernel choices ([#189771](https://github.com/pytorch/pytorch/pull/189771), [#189777](https://github.com/pytorch/pytorch/pull/189777), [#189805](https://github.com/pytorch/pytorch/pull/189805))
- Reduce NVGEMM compile and launch overhead through per-shape memoization, targeted manifest queries, earlier subprocess precompilation, cached launcher arguments, and scaled-GEMM subprocess support ([#189773](https://github.com/pytorch/pytorch/pull/189773), [#189778](https://github.com/pytorch/pytorch/pull/189778), [#189779](https://github.com/pytorch/pytorch/pull/189779), [#189806](https://github.com/pytorch/pytorch/pull/189806), [#189841](https://github.com/pytorch/pytorch/pull/189841))
- Increase the default number of profiled NVGEMM configurations from five to ten; set `TORCHINDUCTOR_NVGEMM_MAX_PROFILING_CONFIGS=5` to restore the previous limit ([#189807](https://github.com/pytorch/pytorch/pull/189807))
- Use native NaN-propagating Triton min/max reductions with a relaxed signed-zero tie policy for faster kernels; set `torch._inductor.config.strict_signed_zero = True` when exact signed-zero selection must match eager execution ([#190404](https://github.com/pytorch/pytorch/pull/190404))
- Emit per-subkernel-block combo-kernel bodies as non-inlined device functions to avoid register-pressure cliffs ([#190689](https://github.com/pytorch/pytorch/pull/190689))
- Reject loop-reindexing fusions that worsen memory coalescing, fixing severe convolution-model latency regressions ([#191349](https://github.com/pytorch/pytorch/pull/191349))
- Deduplicate repeated captured-tensor loads while generating CuTeDSL FlexAttention kernels, reducing first-compilation time ([#192247](https://github.com/pytorch/pytorch/pull/192247))
- Run peak-memory reordering before combo-kernel formation so combo kernels do not hide scheduling freedom from the memory planner ([#192449](https://github.com/pytorch/pytorch/pull/192449))
- Reduce compilation overhead by caching tiling analysis during fusion search, lazily building runnable-graph reproducers, and bypassing symbolic comparisons for identical size objects ([#192675](https://github.com/pytorch/pytorch/pull/192675), [#192818](https://github.com/pytorch/pytorch/pull/192818), [#192819](https://github.com/pytorch/pytorch/pull/192819))

## Ahead-Of-Time Inductor (AOTI)

- Add an opt-in pinned, asynchronous host-to-device path for AOTInductor constant loading through `AOTI_COPY_USE_PINNED_ASYNC=1`, avoiding the device-wide synchronization caused by pageable-memory copies ([#186258](https://github.com/pytorch/pytorch/pull/186258))

## Export

- Reduce decomposition-time complexity for large exported graphs from super-linear to linear growth by avoiding repeated scans of graph-signature and module metadata ([#177927](https://github.com/pytorch/pytorch/pull/177927))

## AOTDispatcher

- Avoid an expensive `Tensor.detach()` when saving graph-input views for backward at AOTAutograd runtime ([#189759](https://github.com/pytorch/pytorch/pull/189759))

## Composability

- Reduce dynamic-shape tracing overhead by avoiding repeated symbolic-number checks and unnecessary memory-format computation, cutting reported AOTAutograd joint-tracing time by approximately 4–5% on a dynamic-shape model ([#192677](https://github.com/pytorch/pytorch/pull/192677))
- Bound the cost of applying wide unbacked-symbol substitution maps in `optimization_hint`, reducing a synthetic case with 300 replacements from 7.36 seconds to 22 milliseconds ([#185884](https://github.com/pytorch/pytorch/pull/185884))
- Canonicalize `reciprocal(sqrt(x))` to `rsqrt(x)` and update the BatchNorm inference decomposition, improving affected kernels by 85–94% and reported model end-to-end performance by 2.11 percentage points ([#190206](https://github.com/pytorch/pytorch/pull/190206))

## Quantization

- Add a bias-add fast path for dynamically quantized CPU linear layers with `torch.float16` weights, speeding up the bias addition step by 10–49× on representative shapes (roughly a 5% overall CPU reduction) ([#189943](https://github.com/pytorch/pytorch/pull/189943))

## CUDA

- Avoid a CUDA synchronization when `torch.normal` validates tensor-valued standard deviations, improving `torch.compile` and CUDA Graph compatibility ([#186508](https://github.com/pytorch/pytorch/pull/186508))
- Add a 32-bit-indexed kernel for CUDA FFT conjugate-symmetry fill ([#190269](https://github.com/pytorch/pytorch/pull/190269))
- Remove redundant zero initialization of fully overwritten buffers in CUDA kernels ([#190953](https://github.com/pytorch/pytorch/pull/190953))
- Increase the number of elements processed per thread by CUDA vectorized elementwise kernels on NVIDIA Rubin GPUs ([#190546](https://github.com/pytorch/pytorch/pull/190546))

## cuDNN

- Reduce cuDNN convolution cold-start overhead by trying the top heuristic algorithm or engine configuration before enumerating all candidates ([#187212](https://github.com/pytorch/pytorch/pull/187212))

## MPS

- Reduce launch overhead and improve strided-input performance by moving 1D and 2D nearest-neighbor interpolation, `torch.logical_not`, `torch.index_add`, `torch.index_select`, and `torch.nn.functional.mish` to native Metal kernels ([#186989](https://github.com/pytorch/pytorch/pull/186989), [#187324](https://github.com/pytorch/pytorch/pull/187324), [#187109](https://github.com/pytorch/pytorch/pull/187109), [#187906](https://github.com/pytorch/pytorch/pull/187906))
- Speed up `median` and `nanmedian` and avoid large intermediate allocations by using native Metal kernels ([#187060](https://github.com/pytorch/pytorch/pull/187060))
- Speed up Cholesky factorization with panel factorization and matrix-multiplication trailing updates ([#187022](https://github.com/pytorch/pytorch/pull/187022))
- Speed up reductions on permuted contiguous inputs ([#187313](https://github.com/pytorch/pytorch/pull/187313))
- Reduce caching-allocator reserved memory during decoding by bucketing large allocations ([#187441](https://github.com/pytorch/pytorch/pull/187441))
- Speed up variance and normalization reductions in compiled MPS workloads with parallel Welford reduction ([#188412](https://github.com/pytorch/pytorch/pull/188412))
- Speed up `torch.linspace` and `torch.arange` by moving them to native Metal kernels ([#188905](https://github.com/pytorch/pytorch/pull/188905), [#188921](https://github.com/pytorch/pytorch/pull/188921))
- Speed up MPS `flex_attention` by using 32-bit symbolic captures when their values fit ([#188663](https://github.com/pytorch/pytorch/pull/188663))
- Speed up `torch.linalg.lu_factor` with native Metal kernels, especially for batched factorizations ([#187038](https://github.com/pytorch/pytorch/pull/187038))
- Reduce synchronization overhead in MPS `torch.bincount` ([#190115](https://github.com/pytorch/pytorch/pull/190115))
- Add optimized Metal GEMV paths for matrix-vector operations, including strided inputs and fused bias ([#186927](https://github.com/pytorch/pytorch/pull/186927))
- Eliminate a major half-precision `torch.nn.functional.linear` regression for three-dimensional sequence-length-one inputs used in batched decoding ([#189855](https://github.com/pytorch/pytorch/pull/189855))
- Speed up integral `torch.linspace` for small ranges by using the floating-point kernel where it remains sufficiently precise ([#191060](https://github.com/pytorch/pytorch/pull/191060))
- Speed up MPS reductions by avoiding input materialization and adding specialized vectorized, packed-row, strided, batched, narrow, and split-K kernels for full, inner, and non-final dimensions, including optimized `argmax`, `argmin`, `min`, and `max`, while fixing NaN index selection ([#191101](https://github.com/pytorch/pytorch/pull/191101), [#191097](https://github.com/pytorch/pytorch/pull/191097), [#191098](https://github.com/pytorch/pytorch/pull/191098), [#191099](https://github.com/pytorch/pytorch/pull/191099), [#191100](https://github.com/pytorch/pytorch/pull/191100))
- Reduce allocator fragmentation for dynamic-shape workloads by coalescing free ranges in placement heaps ([#190438](https://github.com/pytorch/pytorch/pull/190438))
- Speed up 3D convolution on MPS with native Metal and Metal Performance Primitives kernels, including convolutions without bias ([#188802](https://github.com/pytorch/pytorch/pull/188802), [#192229](https://github.com/pytorch/pytorch/pull/192229))
- Speed up contiguous, same-dtype `torch.cat` along any dimension with vectorized Metal copies ([#188200](https://github.com/pytorch/pytorch/pull/188200))
- Speed up GLU forward and backward with fused native Metal kernels ([#187833](https://github.com/pytorch/pytorch/pull/187833))
- Reduce dispatch overhead for sigmoid backward and log-sigmoid forward/backward by moving them to native Metal kernels ([#187151](https://github.com/pytorch/pytorch/pull/187151), [#187228](https://github.com/pytorch/pytorch/pull/187228))
- Speed up unary, binary, and copy operations on sliced or strided views whose innermost dimension is contiguous ([#188483](https://github.com/pytorch/pytorch/pull/188483))
- Speed up LU-based linear solves with native Metal kernels, particularly for batched systems and single right-hand sides ([#189200](https://github.com/pytorch/pytorch/pull/189200))
- Speed up contiguous, same-dtype MPS copies with compute kernels and transfer pinned CPU buffers directly without rewrapping them ([#188613](https://github.com/pytorch/pytorch/pull/188613), [#189512](https://github.com/pytorch/pytorch/pull/189512))
- Add an atomic-free fast path for flat `torch.unique`, fixing incorrect results for large `torch.int64` input values and dramatically accelerating inputs with long duplicate runs ([#184780](https://github.com/pytorch/pytorch/pull/184780))
- Speed up scaled dot-product attention prefill with Metal Performance Primitives on supported macOS versions and GPU generations ([#182256](https://github.com/pytorch/pytorch/pull/182256))
- Reduce `torch.nonzero` memory use for very large tensors by recomputing per-block prefixes during scatter ([#191274](https://github.com/pytorch/pytorch/pull/191274))

## ROCm

- Add `gfx1100`, `gfx1101`, and `gfx1151` to the preferred hipBLASLt architecture list for ROCm 7.13 and later ([#185375](https://github.com/pytorch/pytorch/pull/185375))

## XPU

- Fuse `torch.float16`-to-`torch.float32` upcasts into XPU softmax and reduction kernels, and `torch.bfloat16`-to-`torch.float32` upcasts into XPU reduction kernels ([#189999](https://github.com/pytorch/pytorch/pull/189999))

## JIT

- Reduce JIT startup and compilation overhead by replacing lexer static hash maps with switch-based lookups, preallocating dead-code-elimination memoization storage, and reserving tuple type-parser storage ([#181118](https://github.com/pytorch/pytorch/pull/181118), [#188121](https://github.com/pytorch/pytorch/pull/188121), [#183813](https://github.com/pytorch/pytorch/pull/183813))

# Documentation

## Python Frontend

- Document all accepted device-like arguments for `torch.set_default_device`, including integer accelerator indices and `None` ([#187240](https://github.com/pytorch/pytorch/pull/187240))
- Document the tensor-factory keyword arguments accepted by the `torch.normal(mean, std, size)` overload ([#187820](https://github.com/pytorch/pytorch/pull/187820))
- Clarify that the `index` argument to `Tensor.index_reduce_()` selects positions in `self` to accumulate into, rather than positions in `source` ([#189008](https://github.com/pytorch/pytorch/pull/189008))
- Document that `torch.searchsorted` does not validate sorting and has undefined behavior for unsorted input when no `sorter` is provided ([#184888](https://github.com/pytorch/pytorch/pull/184888))
- Correct the `torch.arange` dtype-inference note to refer to the `step` argument instead of the nonexistent `stop` argument ([#188943](https://github.com/pytorch/pytorch/pull/188943))
- Add docstrings for top-level in-place functions that have out-of-place equivalents ([#189571](https://github.com/pytorch/pytorch/pull/189571))

## torch.nn

- Clarify that `torch.nn.functional.gaussian_nll_loss` uses `eps` to clamp `var` to a minimum rather than adding it to `var` ([#190058](https://github.com/pytorch/pytorch/pull/190058))
- Add deterministic example output to the `torch.nn.Tanh` documentation ([#189390](https://github.com/pytorch/pytorch/pull/189390))
- Correct the documented `mat_b` shape for `torch.nn.functional.grouped_mm` and explain how to pass grouped linear weights ([#191610](https://github.com/pytorch/pytorch/pull/191610))
- Correct the `ceil_mode=True` output-size formula in the `torch.nn.MaxPool1d` documentation ([#188735](https://github.com/pytorch/pytorch/pull/188735))
- Document that repeated calls to `torch.nn.Module.parameters()` return parameters in a deterministic order when the module is unchanged ([#189990](https://github.com/pytorch/pytorch/pull/189990))

## Optimizer

- Fix incorrect learning-rate curves in the `torch.optim.lr_scheduler.ChainedScheduler` and `torch.optim.lr_scheduler.SequentialLR` documentation ([#186468](https://github.com/pytorch/pytorch/pull/186468))

## Distributed

- Correct typos in distributed memory-analysis documentation and related distributed and utility docstrings ([#187079](https://github.com/pytorch/pytorch/pull/187079), [#189357](https://github.com/pytorch/pytorch/pull/189357), [#190827](https://github.com/pytorch/pytorch/pull/190827))
- Document the callback signatures, return values, keyword-argument behavior, and usage of `distribute_module` ([#188071](https://github.com/pytorch/pytorch/pull/188071))
- Correct PyTorch brand name capitalization in distributed checkpoint and other documentation ([#189248](https://github.com/pytorch/pytorch/pull/189248))
- Document the experimental process-group reconfiguration APIs and provide an end-to-end usage example ([#191384](https://github.com/pytorch/pytorch/pull/191384))
- Document how to enable and verify NCCL symmetric-memory kernels through registered memory pools or symmetric-memory rendezvous ([#192515](https://github.com/pytorch/pytorch/pull/192515))

## Linear Algebra Frontend

- Clarify `torch.linalg.norm`, `torch.linalg.matrix_norm`, and `torch.linalg.vector_norm` behavior for complex inputs, and correct the documented `ord` values accepted by `torch.linalg.vector_norm` ([#190381](https://github.com/pytorch/pytorch/pull/190381), [#188204](https://github.com/pytorch/pytorch/pull/188204))

## Dynamo

- Link the guard-overhead page to the developer blog post and document a profiler-based way to measure guard overhead ([#191387](https://github.com/pytorch/pytorch/pull/191387))

## ONNX

- Clarify that `output_names` labels outputs but does not reorder them ([#175796](https://github.com/pytorch/pytorch/pull/175796))

## XPU

- Update the XPU documentation with newly supported operating-system versions and simplified installation instructions ([#187923](https://github.com/pytorch/pytorch/pull/187923), [#190992](https://github.com/pytorch/pytorch/pull/190992))

# Security

## Python Frontend

- Validate tensor shapes and sequence bounds in `torch.quasirandom.SobolEngine` before native kernels index direction-number tables ([#191198](https://github.com/pytorch/pytorch/pull/191198))
- Make stream comparisons with non-stream objects safe and Python-consistent: equality returns `False`, `stream != None` now returns `True` instead of `False`, and ordering comparisons raise `TypeError` instead of returning `False` ([#192523](https://github.com/pytorch/pytorch/pull/192523))

## torch.nn

- Validate `grad_output` shapes in 2D and 3D `grid_sample` backward operations before CPU, CUDA, or MPS kernels can read out of bounds ([#191915](https://github.com/pytorch/pytorch/pull/191915))
- Validate channel counts in `replication_pad1d` and `replication_pad2d` backward operations to prevent out-of-bounds reads and segmentation faults ([#189463](https://github.com/pytorch/pytorch/pull/189463))
- Validate `mean`, `invstd`, and `counts` shapes before CUDA batch-normalization statistics gathering to prevent out-of-bounds reads ([#190005](https://github.com/pytorch/pytorch/pull/190005))

## Distributed

- Add an opt-in `weights_only=True` mode to distributed object collectives for restricted deserialization; the default remains unchanged for compatibility ([#189353](https://github.com/pytorch/pytorch/pull/189353))
- Validate symmetric-memory signal channels and peer ranks to prevent out-of-bounds device-memory access and adjacent-allocation corruption ([#191596](https://github.com/pytorch/pytorch/pull/191596), [#191842](https://github.com/pytorch/pytorch/pull/191842))
- Parse Flight Recorder rank expressions with `ast.literal_eval()` instead of executing them with `eval()` ([#191490](https://github.com/pytorch/pytorch/pull/191490))

## Release Engineering


## Mobile

- Reject malformed mobile FlatBuffer modules whose function class-type index is out of range, preventing an out-of-bounds access and crash during loading ([#186672](https://github.com/pytorch/pytorch/pull/186672))

## Sparse Frontend

- Always validate sparse-tensor invariants when loading with `torch.load(..., weights_only=True)` so malformed checkpoints cannot create tensors whose indices cause out-of-bounds reads ([#184750](https://github.com/pytorch/pytorch/pull/184750))

  Validation is an O(nnz) scan and applies regardless of the global `torch.sparse.check_sparse_tensor_invariants` setting. Fix or regenerate malformed sparse checkpoints that now raise errors such as `RuntimeError: size is inconsistent with indices`. Do not use `weights_only=False` as a workaround for untrusted files.


# Developers

## torch.nn

- Integrate Helion with the native-DSL backend registry behind lazy availability and version checks, and add reusable kernel instrumentation for backend development ([#190636](https://github.com/pytorch/pytorch/pull/190636))

## Distributed

- Guard NCCL one-sided APIs correctly on ROCm so source builds do not reference unsupported device-side functionality ([#186888](https://github.com/pytorch/pytorch/pull/186888))
- Add process-group extension interfaces for fault-tolerant reconfiguration, one-sided communication windows, and abort and pre- and post-collective hooks ([#186298](https://github.com/pytorch/pytorch/pull/186298), [#186299](https://github.com/pytorch/pytorch/pull/186299), [#186300](https://github.com/pytorch/pytorch/pull/186300))
- Keep RPC source builds compatible with modern C++ standard libraries by using `std::atomic<std::shared_ptr>` where available ([#185633](https://github.com/pytorch/pytorch/pull/185633))
- Add canonical `_single` collective methods to the C++ `Backend` interface while preserving compatibility with existing backend overrides and callers ([#187140](https://github.com/pytorch/pytorch/pull/187140))
- Register `ProcessGroup` globally as a supported custom-operator input type ([#187459](https://github.com/pytorch/pytorch/pull/187459))
- Route process-group rank and size through backend implementations to support reconfigurable backends ([#187467](https://github.com/pytorch/pytorch/pull/187467))
- Support optional NCCL expert-parallelism extensions in source builds with bundled NCCL and wheels built against system NCCL ([#187366](https://github.com/pytorch/pytorch/pull/187366), [#187385](https://github.com/pytorch/pytorch/pull/187385))
- Allow distributed backends to register through Python package entry points ([#187388](https://github.com/pytorch/pytorch/pull/187388))
- Add a TorchElastic error-handler hook that downstream integrations can use to enrich signal-failure reports ([#187098](https://github.com/pytorch/pytorch/pull/187098))
- Deprecate the backend-level `_set_sequence_number_for_group()` no-op and remove its private `ProcessGroup` binding while preserving the sequence-number getter ([#188611](https://github.com/pytorch/pytorch/pull/188611))
- Add the missing `FakeStore` declaration to the `_distributed_c10d` type stub ([#189259](https://github.com/pytorch/pytorch/pull/189259))
- Keep the experimental `nccl2` backend buildable without NCCL and on ROCm versions before 7.0 ([#189938](https://github.com/pytorch/pytorch/pull/189938), [#189958](https://github.com/pytorch/pytorch/pull/189958))
- Add a backend-agnostic Flight Recorder hook for process-group extension authors ([#189363](https://github.com/pytorch/pytorch/pull/189363))

## Distributed (c10d)

- Add `split_group` support to the fake process-group backend used for distributed testing ([#186290](https://github.com/pytorch/pytorch/pull/186290))
- Correct `_distributed_c10d.pyi` type stubs for `_create_work_from_future` and the optional `ProcessGroupGloo` timeout argument ([#191633](https://github.com/pytorch/pytorch/pull/191633))

## Symmetric Memory

- Add the `USE_NCCL_EP` source-build option for compiling and statically linking NCCL's expert-parallelism library ([#177437](https://github.com/pytorch/pytorch/pull/177437))

## Profiler

- Add documented CUDA graph instantiate and destroy hooks for the experimental CUPTI monitor, allowing it to observe graph lifecycles without modifying graph execution code ([#191299](https://github.com/pytorch/pytorch/pull/191299))

## FX

- Allow exported profiler timelines to include source-stack provenance for Inductor-generated kernels when `TORCH_COMPILE_DEBUG_EXTEND=1` ([#186230](https://github.com/pytorch/pytorch/pull/186230))
- Preserve device indices such as `cuda:7` in functorch minifier repro inputs so generated repros run on the original device ([#186547](https://github.com/pytorch/pytorch/pull/186547))

## Dynamo

- Add `torch._dynamo.config.canonicalize_output_graph_node_order` to canonicalize node order and names in generated FX graphs, making captured graphs deterministic across runs ([#181775](https://github.com/pytorch/pytorch/pull/181775))
- Make generated `fx_graph_runnable` repros work for graphs containing higher-order-operator subgraphs (`torch.cond`, `torch.while_loop`), which previously emitted invalid Python ([#186804](https://github.com/pytorch/pytorch/pull/186804))
- Serialize symbolic storage sizes in generated repros as executable Python instead of `repr()` output such as `Max(1, s35)` ([#190838](https://github.com/pytorch/pytorch/pull/190838))
- Decode minifier subprocess output tolerantly so non-UTF-8 bytes in runtime diagnostics no longer abort the minifier harness ([#190696](https://github.com/pytorch/pytorch/pull/190696))

## Inductor

- Add semantic identity, shape, and dtype metadata for external kernels to `kernel_information.json` provenance output ([#183952](https://github.com/pytorch/pytorch/pull/183952))
- Allow custom Inductor patterns to match traced `get_attr` tensor constants by value and metadata ([#184419](https://github.com/pytorch/pytorch/pull/184419))
- Record host-side C++ wrapper compilation under a dedicated `cpp_wrapper_compile` timing event ([#187936](https://github.com/pytorch/pytorch/pull/187936))
- Add optional integration with an externally packaged TLX Inductor backend through `torch._inductor.config.triton.tlx_mode` ([#189094](https://github.com/pytorch/pytorch/pull/189094))
- Serialize top-level `functools.partial` configuration values into valid compiler-repro preambles ([#190728](https://github.com/pytorch/pytorch/pull/190728))

## Ahead-Of-Time Inductor (AOTI)

- Add `TORCHINDUCTOR_CPP_ENABLE_KERNEL_CONTEXT_GUARD` to opt into kernel-context metadata when profiling generated C++ wrappers ([#184513](https://github.com/pytorch/pytorch/pull/184513))

## Export

- Improve raw Triton kernel errors during non-strict export with guidance to define the kernel through `torch.library.triton_op` and launch it through `torch.library.wrap_triton` or `torch._library.capture_triton` ([#185827](https://github.com/pytorch/pytorch/pull/185827))
- Improve the readability of draft-export reports on light terminal backgrounds by using red for warning banners, green for success banners, and the terminal's default color for failure details ([#186070](https://github.com/pytorch/pytorch/pull/186070))

## C++ Frontend

- Add the compiler-portable `C10_LIFETIMEBOUND` annotation and apply it to borrowing constructors and accessors in `c10::OptionalArrayRef`, `c10::MaybeOwned`, `c10::TensorAccessor`, `at::TensorRef`, and `at::OptionalTensorRef`, allowing Clang to diagnose dangling references ([#190076](https://github.com/pytorch/pytorch/pull/190076), [#190077](https://github.com/pytorch/pytorch/pull/190077), [#190075](https://github.com/pytorch/pytorch/pull/190075), [#190074](https://github.com/pytorch/pytorch/pull/190074), [#189912](https://github.com/pytorch/pytorch/pull/189912))
- Add strict, integer-only `c10::safe_conv` and wrapping `c10::unsafe_wrapping_convert` ([#190092](https://github.com/pytorch/pytorch/pull/190092))
- Specialize `std::ranges::enable_borrowed_range` for `c10::ArrayRef` ([#186635](https://github.com/pytorch/pytorch/pull/186635))

## Developer Experience

- Add `spin docs` as a contributor-facing wrapper around the documentation Makefile, with `html` as the default target, pass-through support for other targets and options, and clearer dependency checks ([#182814](https://github.com/pytorch/pytorch/pull/182814))

## Build Frontend

- Limit concurrent compilation of vendored FlashAttention CUDA sources with a target-specific Ninja job pool, reducing compiler out-of-memory failures on smaller build machines ([#192305](https://github.com/pytorch/pytorch/pull/192305))
- Update `clang-tidy` to 21.1.0 and temporarily suppress checks newly enabled by that release ([#191111](https://github.com/pytorch/pytorch/pull/191111))

## Release Engineering

- Migrate the build system from `setuptools` to `scikit-build-core` ([#180247](https://github.com/pytorch/pytorch/pull/180247))

## MPS

- Regenerate bundled Metal library headers whenever their generator script or source `.metal` files change ([#189179](https://github.com/pytorch/pytorch/pull/189179), [#187087](https://github.com/pytorch/pytorch/pull/187087))
- Clean up Metal compiler warnings, including compatibility with Metal 3 and newer SDK diagnostics ([#186822](https://github.com/pytorch/pytorch/pull/186822), [#187753](https://github.com/pytorch/pytorch/pull/187753), [#188416](https://github.com/pytorch/pytorch/pull/188416), [#188910](https://github.com/pytorch/pytorch/pull/188910), [#191636](https://github.com/pytorch/pytorch/pull/191636), [#191970](https://github.com/pytorch/pytorch/pull/191970))

## ROCm

- Support source builds with `USE_ASAN=1` ([#188242](https://github.com/pytorch/pytorch/pull/188242))
- Derive hipCUB's compatible CCCL version from `HIPCUB_CCCL_VERSION` ([#188072](https://github.com/pytorch/pytorch/pull/188072))
- Update the bundled CK and AITER submodules to add `gfx1033` support and fix residual NaNs ([#183965](https://github.com/pytorch/pytorch/pull/183965))
- Prevent an out-of-bounds terminator write when the ROCm `libdrm` installer reads `/proc/self/exe` with `readlink()` ([#187799](https://github.com/pytorch/pytorch/pull/187799))

## XPU

- Migrate XPU ATen operator registrations into PyTorch's `native_functions.yaml`, consolidating code generation into a single build step ([#181233](https://github.com/pytorch/pytorch/pull/181233))
- Upgrade the bundled oneDNN submodule to v3.12.3, enabling SYCL graph record/replay support on Intel GPUs ([#188785](https://github.com/pytorch/pytorch/pull/188785))

## Caffe2

- Fix C10 and Python binding source builds with `fmt` 12.2 by including `<fmt/format.h>` directly where `fmt::format` is used ([#190691](https://github.com/pytorch/pytorch/pull/190691), [#192376](https://github.com/pytorch/pytorch/pull/192376))
- Fix Windows Clang 17 builds of the vendored miniz library when `WIN32_LEAN_AND_MEAN` is already defined by the compiler command line ([#190929](https://github.com/pytorch/pytorch/pull/190929))

## JIT

- Restore `TensorExpr` source-build compatibility with LLVM 24 after removal of legacy typed-pointer APIs ([#192381](https://github.com/pytorch/pytorch/pull/192381))
