# PyTorch 2.14.0 Release Notes

- [Highlights](#highlights)
- [Backwards Incompatible Changes](#backwards-incompatible-changes)
- [Deprecations](#deprecations)
- [New Features](#new-features)
- [Improvements](#improvements)
- [Bug fixes](#bug-fixes)
- [Performance](#performance)
- [Documentation](#documentation)
- [Security](#security)
- [Developers](#developers)

# Highlights

<table>
  <tr><td><strong>NVGEMM</strong> brings CuTeDSL-generated CUTLASS kernels to Inductor, with epilogue fusion, scaled and NVFP4 GEMM, and grouped-reduction epilogues autotuned alongside Triton and ATen</td></tr>
  <tr><td><strong><code>torch.switch</code></strong> generalizes <code>torch.cond</code> to multi-way branching, and <code>torch.while_loop</code> can now be captured in a CUDA graph</td></tr>
  <tr><td><strong>Declarative dynamic shapes via <code>@dynamic_spec</code></strong>, shared across <code>torch.compile</code>, <code>torch.export</code> and <code>make_fx</code></td></tr>
  <tr><td><strong>Experimental <code>torch.compile</code> support for complex-valued tensors</strong>: Opt-in support decomposes supported complex operations into real and imaginary computations, enabling compiler backends to optimize more complex-number workloads.</td></tr>
  <tr><td><strong>A new <code>nccl2</code> backend for PyTorch Distributed</strong>, ported from torchcomms, implementing the full collective contract with nonblocking communicators and eager communicator splitting</td></tr>
  <tr><td><strong>Fault tolerance becomes a first-class <code>c10d</code> concept</strong>, with in-place process-group reconfiguration, one-sided RMA windows, and a Flight Recorder that works for any backend rather than only NCCL</td></tr>
  <tr><td><strong>Apple Silicon gains native linear algebra</strong>, including Jacobi-kernel SVD, <code>eigh</code>, QR and Cholesky, alongside a five-part reduction rewrite and a further MPSGraph to Metal kernel migration</td></tr>
  <tr><td><strong>Broader platform support</strong>: ROCm 7.14 wheels are produced from the TheRock pip SDK, Intel XPU adds native graph capture, and Inductor targets Rubin (<code>sm_107</code>)</td></tr>
</table>

For more details about these highlighted features, you can look at the release blogpost. Below are the full release notes for this release.

# Backwards Incompatible Changes

## torch.nn

- `torch.nn.LinearCrossEntropyOptions` no longer accepts `acc_policy="balanced"`; use `"compact"` instead (#188283)

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

- Clamp and min/max boundary subgradients now follow the selected dispatcher schema's input space (#191142)

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

- Custom Python process groups that implement `new_group()` must now accept a `backend` keyword argument (#188489)

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

- NCCL symmetric-memory pools no longer automatically upgrade segments allocated after `register_mem_pool(..., symm=True)` to symmetric windows (#192112)

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

- Nonmember ranks now receive `GroupMember.NON_GROUP_MEMBER` instead of `None` from experimental `torch.distributed.split_group()` (#190725)

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

- Remove the deprecated `torch.cholesky()` and `Tensor.cholesky()` APIs (#186817)

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

- Remove the deprecated `torch.qr()` and `Tensor.qr()` APIs (#186815)

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

- The deprecated `use_cuda` argument has been removed from `torch.profiler.profile` and `torch.autograd.profiler.profile` (#192543)

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

- The `tvm` backend now uses TVM's relax frontend exclusively; the relay path has been removed (#190766, #189639)

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

- Remove the deprecated zero-argument C++ overloads `c10::Scalar::isIntegral()` and `c10::isIntegralType(ScalarType)` (#187115)

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

- `setup.py` is now a deprecation shim; build PyTorch through pip or `python -m build` (#180248)

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

## MPS

- The C++ MPS macOS-version helper and its enum members have been renamed (#188645)

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

## Complex Frontend

- Complex type promotion for `bfloat16` now uses the new `torch.bcomplex32` shell dtype instead of `torch.complex64` (#186928)

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

- Selective activation checkpointing will change to honor surrounding `saved_tensors_hooks` by default; use the new `respect_saved_tensors_hooks` argument to choose the behavior explicitly (#190581)

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

- Use `torch.compiler.config.compile_on_one_rank` instead of `torch.distributed.config.compile_on_one_rank` (#187869)

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

## Profiler

- The experimental `profiler_metrics` and `profiler_measure_per_kernel` options no longer enable CUPTI range profiling and now emit a `FutureWarning` when set to a non-default value (#187204)

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

- The `with_modules` profiler option is deprecated and now emits a `FutureWarning` (#192808)

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

- `torch._dynamo.config.enable_faithful_generator_behavior` is deprecated and is now a no-op (#189894)

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

- Deprecate `CUDAGraph.register_generator_state()`; CUDA graphs now register generator state lazily on first RNG use during capture (#176753)

  The method is now a no-op and emits a deprecation warning. Remove explicit registration calls; the graph automatically retains the required state when the generator is used during capture.

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

- Deprecate `GreenContext.set_context()` and `GreenContext.pop_context()`; use custom streams to activate a green context instead (#188419)

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

- TorchScript APIs now emit visible `FutureWarning`s instead of normally hidden `DeprecationWarning`s (#189914)

  Calls such as `torch.jit.script`, `torch.jit.trace`, `torch.jit.save`, and `torch.jit.load` now visibly direct users toward `torch.compile` or `torch.export`. Imports of `torch.utils.mkldnn`, `torch.fx.experimental.optimization`, and `torch.distributed.optim` also avoid eagerly compiling TorchScript when those modules are merely imported.

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

- Add `torch.accelerator.initial_seed()`, `torch.accelerator.get_rng_state()`, and `torch.accelerator.get_rng_state_all()` for backend-agnostic accelerator RNG inspection (#186597)
- Add read-only DLPack export through `Tensor.__dlpack__(read_only=True)` and `torch.utils.dlpack.ReadOnlyTensorWrapper`, including copy-on-write-preserving exchange with compatible consumers (#188554)
- Add `torch.Generator.philox_state()` so Python-authored kernels can reserve Philox counter ranges that remain correct across CUDA Graph capture and replay (#191019)

## Autograd

- `torch.utils.checkpoint.checkpoint()` can now be called without a function to create an eager-mode decorator with checkpoint configuration separated from the wrapped function's arguments (#189411)

  ```python
  checkpointed_function = torch.utils.checkpoint.checkpoint(
      use_reentrant=False
  )(function)
  output = checkpointed_function(*args, **kwargs)
  ```

  The curried form is initially supported in eager mode; existing direct calls remain the compatible form under `torch.compile`.

- Add `torch.autograd.graph.node_creation_hook`, a thread-local context manager whose callback receives every fully populated autograd graph node created within its scope. The callback can inspect nodes, store metadata, or register backward pre-hooks and post-hooks, including for nodes created during higher-order differentiation and checkpoint recomputation (#189284)

- Add `ctx.set_output_grad_dtype(*dtypes)` for custom `torch.autograd.Function` implementations. Called once from `forward` or `setup_context`, it declares the gradient dtype expected for each output independently of the output's storage dtype; a concrete dtype converts incoming gradients, while `None` leaves their dtype unchanged (#189634)

- Add second-order gradient support for `torch.cdist` and `torch.nn.functional.pdist`, so grad-grad computations no longer fail because `_cdist_backward` or `_pdist_backward` lacks a derivative (#188901)

## Distributed

- Add portable JSON serialization through `DebugMode.save_logs()` and `DebugMode.load_logs()` so distributed execution logs can be compared across separate processes or model configurations (#185010)
- Add the public `torch.distributed.set_timeout()` API; the private `_set_pg_timeout()` alias remains available with a deprecation warning (#187387)
- Add `torch.distributed.tensor.logspace` for constructing distributed logarithmically spaced tensors (#186398)
- Add experimental `torch.distributed.get_backend_impl()` and `ProcessGroup.get_backend()` accessors for custom backend development (#187494)
- Add `torch.distributed.tensor.linspace` for constructing distributed linearly spaced tensors (#187933)
- Add fault-tolerant reconfiguration and one-sided window operations to the experimental `nccl2` backend (#189359, #189360)
- Add the experimental `nccl-lazy` backend, which creates per-peer NCCL point-to-point communicators on demand (#189362)
- Add the `CheckpointableTensor` protocol so distributed checkpointing can save and load `torch.Tensor` objects exposing `global_shape`, `global_offsets`, `local_offsets`, and `local_sizes` metadata (#189492)
- Add an explicit `nccl-legacy` backend and the `TORCH_DIST_USE_NCCL2=1` opt-in for selecting the experimental replacement behind the `nccl` name (#191272)
- Allow `ProcessGroupNCCL.Options.config.comm_name` to assign readable communicator names for NCCL logs and profiler tools (#191001)
- Add `torchrun --log-line-prefix-template` and a `${hostname}` template variable for identifying the host that emitted each worker log line (#191265)
- Allow pipeline schedules to consume explicitly pre-split positional inputs, keyword inputs, and targets through `arg_mbs`, `kwarg_mbs`, and `target_mbs` (#188500)
- Add optional shell-completion generation to `torchrun` through `--print-completion` and the `shtab` package (#191289)

## Symmetric Memory

- Add XPU support for symmetric-memory operations used by asynchronous tensor parallelism, enabling communication/computation overlap on Intel GPUs (#185102)

## Linear Algebra Frontend

- Add `torch.linalg.polar()` for computing `A = U @ H` for matrices with at least as many rows as columns, using a portable SVD implementation and cuSOLVER QDWH acceleration for eligible CUDA inputs (#185837)
- Add `torch.linalg.matrix_sqrth` for computing the principal square root of symmetric or Hermitian positive-definite matrices, with support for batched inputs, autograd, `vmap`, and `torch.compile` (#187987)
- Add CUDA cuBLASLt support to TunableOp, including controls for the number of heuristic candidates through `torch.cuda.tunable.set_cublaslt_requested_algo_count()` and `PYTORCH_TUNABLEOP_CUBLASLT_REQUESTED_ALGO_COUNT` (#186270)

## Profiler

- Memory snapshots can now include CPU pinned-memory allocations by passing `record_pinned_host_memory=True` to `torch.cuda.memory._record_memory_history()` (#182407)

  Pinned-memory allocator state and history are available in the snapshot's `host_segments` and `host_traces` fields. Pass `record_cuda=False` to record only pinned host memory; the web memory visualizer does not yet display host-memory data.

- Profiler events now expose Kineto metadata as typed values through `FunctionEvent.metadata` when `expose_kineto_event_metadata=True` is enabled (#191756)

  The new dictionary avoids reparsing JSON strings and automatically includes metadata fields supported by the active profiler backend.

## Dynamo

- Add `torch.compiler.nonstrict_trace` as a public API (#187737)
- Add the prototype `switch` higher-order op, which selects between N branches by index and mirrors `jax.lax.switch`. It is available as `from torch._higher_order_ops.switch import switch` and lowers to `torch.ops.higher_order.switch`; autograd is not yet supported (#182902, #188374, #189028)
- Declare dynamic shapes explicitly with `ShapesSpec` / `ParamsSpec`, now accepted by strict and non-strict `torch.export.export`, `make_fx(tracing_mode="fake")`, and `torch.compile` through a shared `dynamic_shapes=` keyword (#185982, #186751, #187602, #187010)
- Support Dynamo and AOTAutograd tracing of permitted input mutations in the prototype `scan`, `map`, and `switch` higher-order ops when gradients are disabled; Inductor lowering for these mutations is not yet supported (#186474, #187568, #188903)
- Support `torch.cuda.use_mem_pool` inside a compiled region, so allocations in the context - including fallback and extern kernels - are routed to the pool (#185057)
- Support calls to `logging.Logger` methods that are explicitly registered in `torch._dynamo.config.reorderable_logging_functions`, so supported positional-argument logging calls run after the compiled region instead of causing graph breaks (#190840)

## Inductor

- Add NVGEMM epilogue fusion so supported pointwise operations and output casts can be fused into autotuned matrix multiplications (#186183)
- Add NVGEMM autotuning support for `torch.addmm`, including fused bias and supported pointwise epilogues (#189774)
- Support FlexAttention FLASH-backend backward graphs that differentiate through the returned log-sum-exp output (#189784)
- Add an opt-in `torch._inductor.config.reorder_for_locality_in_training` setting for applying locality-based graph reordering to training graphs (#186643)
- Add opt-in CUDA Graph Trees generation cloning through `torch._inductor.config.triton.cudagraph_trees_generation_cloning = "user_visible"`, preserving live user-visible outputs across generations (#188078)
- Add `bfloat16` support to `torch.fft` operations and `torch.stft` on CUDA and add `float16`/`bfloat16` support on XPU. Native CUDA `bfloat16` cuFFT execution requires SM80 or newer and power-of-two transform sizes; unsupported CUDA and XPU cases promote to `float32`. CPU FFT continues to reject these low-precision dtypes (#180766)
- Add the opt-in `autotuning_inputs` log artifact, enabled with `TORCH_LOGS=autotuning_inputs`, to report Triton autotuning input shapes, dtypes, strides, and scalar values (#184399)
- Add Inductor support for the prototype `switch` control-flow operator on CPU and GPU, including dynamic shapes, multiple outputs, and AOTInductor; CUDA graphs remain unsupported for graphs containing `switch` (#188976)
- Add dynamic-shape support to `torch.compiler.precompile` for dimensions marked with `torch._dynamo.decorators.mark_unbacked`, allowing one artifact to serve multiple runtime sizes without guarding on the marked dimension (#189165)
- Add `torch.compiler.cudagraph_mark_warmup_incomplete()` so code can request another CUDA Graph Trees warmup iteration (#191386)

## Ahead-Of-Time Inductor (AOTI)

- Add `AOTInductorModelContainerCreateWithExternalConstants`, allowing callers to construct an AOTInductor model container from caller-owned weight tensors for zero-copy sharing such as CUDA IPC (#188643)

  The new C API skips loading constants from the package and leaves ownership with the caller. Existing model-container creation and constant-loading paths are unchanged unless external constants are explicitly provided.

- Support explicit user-defined streams in the AOTInductor C++ wrapper. A compiled region that selects a stream with `torch.cuda.stream(...)` now emits stream-guard code so its kernels run on the requested stream, instead of always running on the default stream (#182971)

## Export

- Add the `torch.fx.experimental.dynamic_spec.dynamic_spec` decorator for attaching a dynamic-shape specification to a function or `nn.Module.forward`. `torch.compile`, `torch.export.export`, and `make_fx` automatically use the attached specification; passing a conflicting call-site specification raises an error (#187639)

## Composability

- Add a `length` argument to the prototype `torch._higher_order_ops.scan`, allowing a scan to run for a fixed number of steps when `xs=None`, matching the corresponding `jax.lax.scan` usage pattern (#188349)
- Add grouped-query attention to the CUDA memory-efficient backend for `torch.nn.functional.scaled_dot_product_attention`, including native grouped key/value heads, implicit multi-query attention broadcasting, and backward support under `vmap` (#191085)

## C++ Frontend

- Add `torch::stable::tensor_from_pyobject` and `torch::stable::tensor_to_pyobject` for converting between Python `torch.Tensor` objects and `torch::stable::Tensor` (#183323)
- Move the `c10/util/complex_utils.h` helpers and the `ATen/NumericUtils.h` `_isinf` and `_isnan` implementations into the header-only ABI (#192552, #192557)
- Add stable-ABI `torch::stable::permute` and the dtype overload of `torch::stable::view` (#192083)
- Add stable-ABI `torch::stable::Tensor` overloads for `bitwise_and`, `bitwise_or`, `bitwise_left_shift`, `bitwise_right_shift`, `index_select`, `floor_divide`, and `is_pinned` (#191973, #192097)
- Add `torch::stable::Tensor::has_storage()` (#189877)

## Release Engineering

- Expand Python 3.15 and free-threaded (no-GIL) Python 3.15t binary coverage to Windows and macOS, completing support across the PyTorch release matrix (#189722, #190360, #190361, #186033)

  PyTorch 2.14 publishes Python 3.15 and 3.15t wheels for Linux on x86-64 and aarch64, Windows x86-64, and macOS on Apple silicon, covering the applicable CPU, CUDA, ROCm, and XPU builds. `torchvision` 0.29.0 publishes matching Python 3.15 and 3.15t wheels for the same supported platform and accelerator combinations. This is binary and eager-runtime support; `torch.compile` remains unsupported on Python 3.15 in this release.

## CUDA

- Add a cuBLASLt backend for grouped GEMM on Hopper and Blackwell GPUs with CUDA 13.3 or newer (#177037, #190372)

  The backend supports `float16` and `bfloat16`, works with `torch.compile` and CUDA Graphs, and is selected by default for eligible `float16` workloads. Set `torch.backends.cuda.matmul.prefer_cublaslt_grouped_gemm = True` to opt into it for `bfloat16`. Matrices and leading dimensions must be 16-byte aligned, so some shapes may require padding and slicing.

- Add `torch.cuda.memory._annotate_tensor()` for attaching metadata to a live CUDA tensor allocation after it is created (#190575)

  Each annotation is recorded as a timestamped memory-history event, multiple annotations accumulate without replacing allocation-time metadata, and memory snapshot tools display the annotations alongside the affected allocation. Memory history must be enabled with `torch.cuda.memory._record_memory_history()` for annotations to be observable. Only the native CUDA caching allocator supports annotations.

- Add the public `torch.cuda.graph_annotations` module (#189417)

- Annotate backward kernels in `mark_kernels` via `node_creation_hook` (#191563)

- Allow multiple memory pools in a single `CUDAGraph` (#187929)

- Add CUDA graph support for `torch.while_loop` (#186055)

- Add destroy callbacks and object retention to `torch.cuda.CUDAGraph` (#190582)

- Add replay start/end hooks to `torch.cuda.CUDAGraph` (#190602)

- Add global CUDA graph capture-start/end and replay-start/end hooks, plus `torch.cuda.CUDAGraph.register_capture_start_hook()` (#192162)

## cuDNN

- Add cuDNN SDPA support for head dimension 256 on SM90 and SM10.x GPUs with cuDNN newer than 9.22 and cuDNN Frontend 1.24 or newer; backward currently supports only `(d_qk, d_v) = (256, 256)` (#185553)

## MPS

- Add native MPS support for binomial sampling (#187078)
- Add MPS forward and backward support for `torch.nn.functional.ctc_loss` (#187716, #188187)
- Add MPS support for `torch.linalg.matrix_exp`, including complex inputs, on macOS 15 or newer (#188954)
- Add native MPS Poisson sampling, eliminating its CPU fallback (#173319)
- Add native `float32` and `complex64` MPS implementations of `torch.linalg.svd`, `svdvals`, `eigh`, `eigvalsh`, and `lstsq`, while retaining CPU fallbacks for small matrices and matrices that exceed threadgroup memory (#185954)

## ROCm

- Add initial, technology-preview support for AMD `gfx1250`; CK SDPA/GEMM, FP8 grouped GEMM, and int4 matrix multiplication remain unsupported (#187548, #188597, #188612)
- Enable hipFile on Linux with ROCm 7.14 or newer (#191069, #192803)

## XPU

- Add FP8 blockwise scaling support for MXFP8/MXFP4/NVFP4 recipes to `torch._scaled_mm` and `torch._scaled_mm_v2` on XPU (#181726, #181727, #187315)
- Add XPU Graph native recording mode on non-PVC devices when PyTorch is built with oneAPI 2026.1 or newer (#188874)
- Add `torch.xpu.list_gpu_processes` to query per-process GPU memory usage on XPU (#185192)

# Improvements

## Python Frontend

- Allow `torch.quantile` and `torch.nanquantile` to process `float32` and `float64` inputs larger than `2**24` elements on devices with `float64` support by computing ranks in `float64` (#187574)

## torch.nn

- Allow the chunked path of `torch.nn.functional.linear_cross_entropy` to handle probability targets for `reduction="mean"` and `reduction="sum"` when the target dtype matches the input and the target does not require gradients (#187053)
- Improve static typing for `torch.nn.Sequential` indexing so integer keys resolve to `Module` and slices resolve to `Sequential` (#187758)
- Add the documented `memory_format` overload to `torch.nn.Module.to()` so static type checkers accept calls such as `module.to(memory_format=torch.channels_last)` (#185117)

## Optimizer

- Add the `"spectral_unclamped"` scaling option to the `adjust_lr_fn` parameter of `torch.optim.Muon` (#187402)
- Add a `maximize` parameter to `torch.optim.LBFGS` (#187309)
- Make `torch.optim.LBFGS.step()` a no-op for an empty parameter group (#191666)

## Distributed

- Expand `DTensor` sharding strategies for matrix, attention, sorting, scanning, softmax, and related operations (#186667, #179068)
- Allow custom Python `ProcessGroup` implementations to use `batch_isend_irecv` and the coalescing manager (#186964)
- Improve the Flight Recorder diagnostic emitted when a `TCPStore` check fails (#187191)
- Allow pipeline parallel stages to use separate forward and backward point-to-point communicators, reducing cross-batch ordering hazards (#186173)
- Add fault-tolerant reconfiguration support to Gloo process groups (#187381)
- Make compile-on-one-rank graphs portable across ranks by replacing baked accelerator device indices with a runtime current-device operation (#186892)
- Expand active `DTensor` single-dimension strategies for tensor operations (#186754)
- Auto-qualify bare backend names and pass process-group options through custom TorchComms backend creation (#187856)
- Add complete collective coverage to custom Python process groups, including single-tensor gather/scatter and the remaining point-to-point and collective operations (#188548, #188570)
- Make TorchElastic NUMA binding and `ShardedTensor` device transfers work with accelerator backends beyond CUDA (#185266, #187939)
- Use generic collective coalescing when aborting process groups so third-party backends can avoid multi-communicator teardown deadlocks (#189770)
- Mark CUDA symmetric-memory allocations as GPUDirect RDMA capable on supported systems (#189941)
- Add communicator memory suspend/resume support to the experimental `nccl2` backend (#189361)
- Allow unknown device-qualified TorchComms backend names to register as custom backends without requiring manual changes to internal backend maps (#191034)
- Add eager `split_group` support, complete `Work` semantics, nonblocking communicators, and uneven list collectives to the experimental `nccl2` backend (#190943, #191517, #191528, #191542)
- Include `nccl-lazy` pair communicators in error reporting, suspend/resume operations, and memory statistics, and expand its shared backend coverage (#191553, #191556)
- Add memory-pool registration and deregistration support to the experimental `nccl2` backend (#192108)
- Add per-process-group collective sequence numbers and accurate split-group membership metadata to `nccl2` profiler traces (#192114, #192115)
- Support non-overlapping final-spatial-dimension `DTensor` sharding for `Conv1d`, `Conv2d`, and `Conv3d` forward and backward (#192147)
- Pass process-group descriptions and names to NCCL's `commName` field while preserving user-specified communicator names (#192487)
- Support `DTensor` redistribution from final-dimension sharding to `Partial("sum")` (#191828)

## Distributed (c10d)

- Upgrade NCCL to 2.30.7 for CUDA 13.0 and CUDA 13.2 builds (#187528)
- Enable Inductor's `simple_overlap` scheduler pass by default for compiled distributed workloads, moving collective starts earlier and waits later without reordering collectives or increasing peak memory (#184235, #184240)

## Linear Algebra Frontend

- Add backward support for `torch.linalg.polar` on CPU, CUDA, and MPS (#189732)
- Enable `torch.linalg.eig` on ROCm 7.14 or newer through hipSOLVER's generic `Xgeev` API, and update generated linear-algebra tests to recognize hipSOLVER implementations that do not require MAGMA (#188720)
- Allow `torch.backends.cuda.preferred_blas_library("ck")` to select the CK GEMM backend on ROCm `gfx90a` devices by separating GEMM support from CK attention support (#187267)
- Expand ROCm backend coverage for `torch.linalg.eig`, `torch.linalg.ldl_solve`, `torch.linalg.solve`, and `torch.linalg.solve_triangular` through hipSOLVER and hipBLAS paths (#185557)

## Profiler

- Record XPU profiler overhead as `OVERHEAD` activities, making collection costs visible on a dedicated track in exported traces (#187835)

## FX

- Allow `split_const_subgraphs()` callers to supply an `is_impure_node` callback so destination-passing operations and other side-effecting nodes are preserved during dead-code elimination (#190716)
- Make `get_source_partitions()` return input nodes, output nodes, and parameters in deterministic graph order (#188965)

## Dynamo

- Extend `torch.compiler.nested_compile_region` reuse to source-backed objects, symbolic shapes, dataclasses, and namedtuples (#192003, #191806, #191817)
- Expand compilation support for `staticmethod`, built-in leaf modules, cross-device `tensor.data` swaps, raw unbacked `SymInt` inputs, zero-length scans, and methods reached through `super()` (#190673, #185722, #185980, #187273, #188348, #183850)
- Trace accelerator probes, channels-last `out=` tensors, sourceless `DistributedDataParallel`, `dist.reduce_scatter`, `SDPAParams`, and `torch.linalg.polar` (#185277, #185089, #187210, #190429, #190839, #188537)
- Recognize out-of-tree Triton devices and accept module functions or constants as `torch._check` messages (#190324, #188576)
- Match more Python built-ins and operators, including `min`/`max`, integer bases and formatting, `range`/slice coercion, object and container subclasses, mutable string splits, rich comparisons, item mutation, and `callable()` (#191401, #191402, #191408, #187129, #186976, #189021, #187588, #185999, #188306, #191406, #190259, #186971)
- Expand iterator support for `itertools`, dict/set views, and range iterators (#188080, #189022, #186937, #187080, #186240, #188081, #188221, #189575)
- Improve `deque`, dict, set, dict-view, `__dict__`, and list initialization fidelity (#187128, #188220, #191403, #189052, #191405, #186759, #186760, #186669, #186761, #186763, #188908, #187586, #187587, #187583, #187584)
- Improve object representation and copying, exception attributes, and subgenerator closure behavior (#187775, #188909, #189053, #189576, #188105, #189024, #188825, #188834)
- Trace module-level random calls, text-file encoding operations, and additional numeric operator slots (#188235, #188083, #189984, #186296, #189585, #185641)
- Improve graph-break, guard-mismatch, in-place-view, backend-name, and exception diagnostics (#185763, #185083, #185903, #189333, #182972, #185508)
- Support TVM's Relax frontend and pipeline-based tuning (#189010, #189638)

## Inductor

- Make missing CUDA and ROCm warp-size metadata explicit so Inductor skips heuristics that require it instead of silently assuming a warp size of 32. Raise when a code path requires a concrete warp size but the metadata is unavailable (#183014)
- Make autotuning subprocesses honor `ZE_AFFINITY_MASK` on XPU while preserving `CUDA_VISIBLE_DEVICES` behavior on CUDA (#183436)
- Add a dedicated `XPUCompileError` for SYCL compilation failures and clear loaded XPU libraries when the code cache is reset (#183530)
- Make partitioned-scatter selection memory- and contention-aware, enable it by default on ROCm, and replace the removed `partitioned_scatter_memory_budget` setting with memory-headroom controls; set `partitioned_scatter_enabled = False` to opt out (#184365)
- Support ROCm Composable Kernel GEMM templates when compiling with the JIT C++ wrapper (#185505)
- Fuse decomposed SiLU activations into CUTLASS GEMM epilogues and improve XPU GEMM template compatibility (#186197, #186198)
- Accept multiword compiler commands such as `CXX="zig c++"` when building Inductor-generated C++ code on POSIX systems (#186336)
- Add Intel Arc B580 and Arc Pro B70 specifications to Inductor's device-performance metadata (#187308)
- Lower `uniform_` and `aten.uniform` through a native decomposition instead of always falling back to eager execution (#187887)
- Enable Triton indirect-indexing assertions on ROCm with Triton 3.7 or newer, improving diagnostics for out-of-bounds accesses (#188075)
- Allow XPU's static launcher to accept host and shared USM pointers recognized by the driver instead of requiring device memory (#188240)
- Extend manual communication-overlap scheduling to bucket and defer waits for DDP and HSDP `all_reduce` operations (#188472)
- Support grouped and FP8-scaled grouped GEMM Triton lowering on compatible ROCm hardware (#188600, #188742)
- Apply per-region Inductor configuration patches throughout nested-region compilation and allow separate forward and backward patches (#189320, #190068)
- Decompose semi-structured sparse CUTLASS matrix multiplication so Inductor can lower and autotune the underlying operation (#189366)
- Report stuck compile workers and their current phase in structured `tlparse` traces through the configurable compile-worker watchdog (#189485, #189486)
- Prefer device datasheet bandwidth for Inductor's bandwidth-driven heuristics and add Intel Data Center GPU Max 1100 metadata (#189819)
- Lower `torch.float8_e8m0fnu` conversions directly on CPU and CUDA instead of relying on fallback conversion code (#190593)
- Expand NVGEMM epilogue fusion to pointwise operations, multiple outputs, and grouped reductions, including scaled and centered outputs (#190643, #190808, #190809, #190810, #190813, #190817, #190823)
- Suppress empty generated-code dumps from `TORCH_LOGS=output_code` during autotuning (#191381)

## Ahead-Of-Time Inductor (AOTI)

- Support `int[]`, `SymInt[]`, and optional integer-list arguments in AOTI eager cache keys, enabling cached compilation for operators such as `new_zeros`, `mean.dim`, and `count_nonzero.dim_IntList` (#187360)
- Support lazy autotuning when compiling with the AOTInductor dual-wrapper, so Triton autotuning is deferred to a first JIT pass rather than being done during ahead-of-time compilation (#184735)
- Support `torch.cond` and `torch.while_loop` when compiling with the AOTInductor dual-wrapper (#184736)
- Add an `AOTI_LOG_LOADING` environment variable. When it is set, AOTInductor prints timing and diagnostic messages for each stage of constant loading, prefixed with `[AOTI_LOAD]`, without requiring a rebuild (#186309)
- Check the error codes returned by the generated `scatter`, `index_put`, `clone`, and tensor-handle shim calls, so a failure inside one of these fallbacks raises an error instead of being silently ignored (#190909, #190910)

## Export

- Support serializing nested integer and floating-point list arguments, including empty nested lists, for custom operators in exported programs (#189424)
- Support `ObjectSpec`, `SeqSpec`, and `DictSpec` container types when using shape specifications with strict export (#186167)

## Composability

- Add `torch.linalg.vector_norm` to the core ATen decomposition table used by `ExportedProgram.run_decompositions()`, including correct `dim=()` handling (#185735)
- Allow out-of-tree backends to define additional `out_dtype` combinations for `torch.mm`, `torch.bmm`, and `torch.baddbmm` under fake/meta tracing; CUDA and XPU restrictions remain unchanged (#187096)
- Provide a targeted dynamic-shape error when a data-dependent expression conflicts with a `dynamic_spec` constraint (#187143)

## Foreach

- Use the nvmath `_foreach_mm` path only when the loaded cuBLASLt version supports grouped GEMM (#189757)

## ONNX

- Preserve constants introduced during export decompositions so `ExportedProgram` remains valid when ONNX symbolic operations are inserted during retracing (#185090)

## C++ Frontend

- Enable stable-ABI error-message retrieval dynamically when the required runtime shim is available (#183823)
- Treat `-Wdeprecated-declarations` diagnostics as warnings rather than errors in `c10`, ATen, and LibTorch builds (#189948)
- Reject negative CUDA storage-resize requests instead of wrapping them to huge `size_t` allocation requests (#190652)

## Release Engineering

- Enable ROCm 7.14 nightly manywheel builds through TheRock wheels (#190276) and add `libatomic` to the manywheel builder image (#192254)
- Update the bundled Triton to 3.8.0 (#188251, #190349)
- Add full CUDA 13.2 CI coverage for stable-version configurations (#190641), Inductor, H100, B200, and `DTensor` (#190948), plus B200 smoke tests (#191705)
- Upgrade the XPU support package to 2026.1 (#189593)
- Update OpenBLAS to v0.3.34 (#190314)
- Update the Arm Compute Library (ACL) version used by aarch64 builds (#191316)
- Relax the `nvidia-nvjitlink-cu12` runtime dependency of CUDA 12 wheels so it no longer forces an exact version (#186958)

## CUDA

- Add CUDA compute capability 10.7 (`sm_107`) awareness for NVIDIA Rubin GPUs with CUDA 13.4 or newer in extension builds and Inductor code generation (#190654)
- Update CUDA compatibility checks for Jetson devices using SBSA binaries with CUDA 13.2 or newer (#186285)
- Move green contexts to cuda-python bindings (#185527)
- Unify the `CUDAGraph` debug flag, move `debug_dump` to Python, and add capture hooks (#187749)
- Trim the `cudaMallocAsync` pool and retry once before raising an out-of-memory error (#188110)
- Improve CUDA errors by including excerpts from CUDA logs (#191334)
- Add `torch.float16` and `torch.bfloat16` support to `torch.angle` on CUDA (#191301)

## cuDNN

- Upgrade the CUDA 12.8, 12.9, and 13.x wheels to cuDNN 9.24 and re-enable convolution engine 5 after its nondeterminism issue was fixed (#187091, #189483)

## CPU (x86)

- Add `Half` support to the eager `torch.polar` kernel (#192311)
- Allow `xeon/run_cpu.py` to accept multiple values for `--ncores-per-instance` (#169916)

## MPS

- Support `return_aux(max_scores=True)` in MPS `flex_attention` forward (#188362)
- Support `SymInt` captures in MPS `flex_attention` score and mask functions, including dynamically shaped compiled graphs (#188403)
- Add MPS support for `torch.linalg.polar` (#189701)
- Support MPS `torch.nonzero` on tensors containing more than `2**32` elements (#188816)
- Add complex MPS support for Cholesky factorization (#191836)
- Support key/value batch broadcasting and returning log-sum-exp values from MPS `flex_attention` (#187722, #187768)
- Add MPS backward support for antialiased bilinear and bicubic 2D upsampling (#188819)
- Add complex MPS support to `torch.nan_to_num` and correctly resize empty `out=` tensors (#189489)
- Add MPS `torch.geqrf` support and align the MPS `torch.linalg.qr` implementation with other backends (#189192)

## ROCm

- Add `torch.utils.hipify` mappings for the `cublasMath_t` type, its enum values, and `CUBLAS_COMPUTE_16F`, so HIP-ported extensions that call `cublasGemmEx` with `CUBLAS_COMPUTE_16F` or set a cuBLAS math mode hipify cleanly without per-project aliases (#187752)
- Migrate from `rocm_smi` to `amd_smi` (#190014)
- Preload TheRock ROCm dependencies so wheels are self-contained (#188454)
- Enable Inductor lowering for FMA on ROCm (#187165)

## XPU

- Add device-wide synchronization support on XPU (#191900)
- Add IPC memory handle sharing support to `XPUCachingAllocator` on XPU (#188789)
- Support head dimensions 32 and 256 for XPU FlashAttention (#180646)
- Enable TF32 `fpmath` mode for XPU deconvolution, matching the existing convolution behavior (#185606)
- Fix XPU graph-capture hangs by deferring memory-pool block handling until capture ends (#187931)
- Refine `clock_rate` and `power_draw` device property queries through `pyzes` 0.1.2 (#188248, #188256)
- Add experimental C++ XPU device properties for Xe topology, including `xe_stack_count`, `xe_regions_per_stack`, `xe_clusters_per_region`, and `xe_cores_per_cluster` (#191477)
- Support BMG-G31 architecture compilation for the SYCL-TLA CUTLASS backend on XPU (#187040)
- Enable the XPU scope profiler to gather hardware metrics through the Kineto plugin (#165766)
- Make Inductor use XPU's device-specific TF32 setting so compiled matrix multiplication matches eager behavior (#187948)
- Enable SYCL native fast-math approximations for `exp`, `log`, `log1p`, and `tan` on XPU (#176262)

## Sparse Frontend

- Add CUDA `float16` and `bfloat16` support to `torch.sparse.sampled_addmm`, including supported sparse-CSR backward paths (#187681)
- Add sparse COO dispatch for `torch.linalg.vector_norm`, allowing it to replace deprecated `torch.norm` calls on sparse COO tensors (#185309)

## torch.func

- Allow `torch.vmap` to handle the scalar overload of `torch.searchsorted` (#188974)
- Expand `torch.vmap` coverage for copy-view operations by routing them through existing batching rules (#187256)
- Add a batching rule for `torch.repeat_interleave` when `repeats` is batched; callers must provide a common `output_size` because per-example output lengths are data-dependent (#187702)
- Add a native batching rule for in-place `Tensor.masked_fill_()`, avoiding the slow fallback and its performance warning under `torch.vmap` (#175513)
- Expand scalar fill and comparison support under `torch.vmap`, including accelerator placement for scalar operands (#189176)

# Bug Fixes

## Python Frontend

- Fix `torch.arange` computing the wrong length for fractional arguments with an integer output dtype because it truncates those arguments too early (#185812)
- Raise a clear unsupported-operation error for dense tensor factories targeting `device="mkldnn"` instead of triggering an internal assertion (#185711)

## Dataloader Frontend

- Release CUDA IPC-backed dataset storage when `DataLoader` workers exit, preventing producer-side IPC references and allocations from being retained indefinitely (#190485)

## torch.nn

- Enable eligible fused scaled dot-product attention backends for dense rank-3 inputs on CPU, CUDA/ROCm, and XPU instead of always falling back to the math implementation (#192271)

  Rank-3 inputs are normalized to rank 4 with a singleton batch dimension before backend selection. This fixes fused execution for rank-3 and vmapped inputs, but automatic backend selection can change floating-point numerics, dropout RNG consumption, whether the result is a view, and higher-order-gradient support. Fused CUDA backends do not support the second derivatives provided by the math backend; code that depends on those semantics should explicitly select the math backend.

  ```python
  from torch.nn.attention import SDPBackend, sdpa_kernel

  with sdpa_kernel(backends=[SDPBackend.MATH]):
      output = torch.nn.functional.scaled_dot_product_attention(
          query, key, value
      )
  ```

- Reject `norm_type=0` in functional and module Lp pooling APIs with a descriptive `ValueError` instead of a deferred `ZeroDivisionError` (#187861)

- Fix failures in memory-efficient scaled dot-product attention backward after `torch.autograd.graph.save_on_cpu()` changes an attention mask's aligned strides (#188246)

- Fix a CUDA illegal memory access in memory-efficient scaled dot-product attention backward when only the floating-point attention mask requires gradients (#188302)

- Make the cuDNN CTC loss backend correctly zero infinite losses and their gradients when `zero_infinity=True` (#176911)

- Validate each output dimension for `replication_pad2d` and `replication_pad3d` so excessive negative padding raises a clear error instead of attempting to create a negative-sized tensor (#184254)

- Fix silently incorrect CUDA gradients from channels-last `avg_pool2d` when padding is nonzero (#188345)

- Make CPU eager and decomposed `torch.nn.functional.softshrink` cast scalar `lambd` values consistently for reduced-precision inputs (#186358)

- Prevent CUDA `avg_pool3d` backward from corrupting gradients when an overlapping-window input contains more than `2**31` elements (#188229)

- Reject non-positive `kernel_size` values in raw `fractional_max_pool2d` and `fractional_max_pool3d` operations instead of returning `-inf` outputs with invalid indices (#190480)

- Support 64-bit indexing for channels-last CUDA bilinear upsampling so outputs with at least `2**31` elements no longer fail with `CUDA error: invalid configuration argument` (#185788)

- Fall back to the ATen CUDA implementation when the fused RMSNorm override's normalized dimension exceeds the device's shared-memory capacity, avoiding compiler hangs or crashes (#186941)

- Reject invalid `dim` types when constructing `torch.nn.Softmax` or `torch.nn.LogSoftmax` instead of failing later during the forward pass with a confusing overload error (#185055)

- Handle misaligned input and weight storage in the fused RMSNorm override instead of raising `Misaligned Tensor data on argument #0` (#186235)

- Make CUDA `float16` softmax with `dtype=torch.float32` use the same persistent-kernel range as the `float16` output path, fixing rounding inconsistencies for dimensions between 1025 and 2048 (#188247)

## Optimizer

- Fix skipped updates and incorrect `float16`/`bfloat16` casts in fused CPU `torch.optim.SGD` and `torch.optim.Adagrad` (#192545)

## Autograd

- Reject unsupported third-order derivatives for training-mode batch normalization instead of silently returning an invalid result; second-order derivatives and evaluation mode are unchanged (#186779)
- Fix `torch.pow` backward when the base is a Boolean scalar by promoting the scalar before computing its logarithm, avoiding an internal assertion failure (#182564)
- Fix `torch.pow` backward under `torch.compile(dynamic=True)` when a Python integer exponent becomes symbolic, avoiding the `NYI SymInt equality` crash without specializing on the exponent (#185851)
- Make `native_group_norm` and `native_group_norm_backward` safely handle non-contiguous tensors, fixing `vmap` failures and possible out-of-bounds memory accesses (#186414)
- Fix the `torch.ldexp` gradient for negative integer exponents so it returns `2.0 ** exponent` instead of zero (#186566)
- Fix `DeviceContext` mode leaks during checkpoint recomputation and default-device restoration (#189286)
- Fix end-of-backward leaf-stream synchronization across CUDA graph capture boundaries, avoiding opaque `cudaErrorStreamCaptureIsolation` failures and providing an actionable error when the crossing cannot be safely skipped (#189591)
- Fix precision errors in the CUDA `native_group_norm_backward` kernel and its decomposition by applying the missing upcasts (#190245)
- Stop `register_full_backward_pre_hook`-only modules from emitting a warning intended for `register_full_backward_hook` when their forward inputs do not require gradients (#190685)
- Fix max-pooling double backward under `vmap` for channels-last inputs, which previously raised `NYI: querying is_contiguous inside of vmap` (#191678)
- Preserve dynamic type names and argument indices in custom `torch.autograd.Function` validation error messages (#191748)
- Improve `log2` and `log10` backward accuracy by using named mathematical constants, including a correctly rounded double-precision `log(10)` constant (#192613)

## Distributed

- Fix construction of Python `ProcessGroup` subclasses through the `(store, rank, size)` constructor and ensure their virtual overrides are dispatched correctly (#186853)
- Select registered custom communication backends instead of incorrectly falling back to NCCL or Gloo when the backend is unspecified (#179901)
- Fix compiled DTensor backward paths producing data-dependent guards for valid symbolic local layouts (#187026)
- Preserve local Philox seed and offset outputs when expanding DTensor scaled dot-product attention strategies across multidimensional meshes (#187199)
- Respect nonzero `root` arguments in `torch.cuda.nccl.broadcast` instead of always broadcasting from the first tensor (#187216)
- Fix ring-attention backward using mismatched maximum sequence lengths when context-parallel load balancing is enabled (#185493)
- Fix DTensor backward strategies emitting placements for outputs disabled by `output_mask` (#187383)
- Preserve the configured FSDP2 gradient-reduction dtype when parameters are frozen during the first forward and later unfrozen (#187376)
- Make `torch.distributed.set_timeout()` a no-op for fake process groups and warn rather than fail for backends that cannot configure timeouts (#187693)
- Prevent `LocalDeviceMesh` from returning stale coordinates after a temporary submesh is destroyed and its object ID is reused (#187052)
- Fix asynchronous coalesced collectives failing CUDA graph capture under `torch.compile(mode="reduce-overhead")` because tensors were retained by the wrong work object (#187433)
- Implement `barrier()` for the NCCL symmetric-memory backend instead of raising a not-implemented error (#188051)
- Flush distributed-checkpoint streams before `fsync()` so buffered writes are persisted correctly on remote filesystems such as GCS (#183877)
- Fix repeated `hipMemMap` calls causing symmetric-memory failures on ROCm (#188673)
- Fix custom backend registration with a string `devices` argument incorrectly registering each character as a device type (#187960)
- Fix FSDP `summon_full_params(offload_to_cpu=True)` accessing freed storage when the flattened parameter is already on CPU (#188990)
- Include the local device in compiled DTensor cache keys so ranks cannot reuse kernels compiled for another device (#188401)
- Prevent stale symmetric-memory signal data when virtual addresses are reused by placing and clearing the signal pad at the front of each allocation (#189088)
- Fix collective validation, sequence tracking, complex tensors, barriers, and work cleanup in the experimental `nccl2` backend (#190138)
- Preserve container object identity when FSDP recursively moves values but their elements do not change (#171617)
- Make compile-on-one-rank graphs resolve process groups from their device mesh at runtime instead of serializing rank-specific process-group objects (#188215)
- Fix `torch.distributed.nn.functional.broadcast` producing a zero source gradient for subgroups whose local and global source ranks differ (#190583)
- Create TorchComms subgroups on the calling rank's actual device, including under launchers that do not set TorchComms rank variables (#189072)
- Fix work-object and expandable-segment allocator lifetimes in the experimental `nccl2` backend (#190370)
- Return `GroupMember.NON_GROUP_MEMBER` consistently from locally synchronized `new_group` calls on nonmember ranks (#190588)
- Support the linear `avg` reduction in functional `all_reduce` backward instead of rejecting it after a successful forward pass (#190224)
- Prevent subgroup creation hangs and duplicate-finalization crashes by making subgroup-name salts rank-consistent and finalizing each communicator once (#189073, #189074)
- Fix single-operation point-to-point completion ordering and synchronous barrier semantics in the experimental `nccl2` backend (#190622, #190682)
- Allow NCCL symmetric memory to use communicators created by the experimental `nccl2` backend (#191109)
- Normalize `new_group` ranks through Python's integer protocol so tensor integer ranks work and non-integral values fail clearly (#191377)
- Fix simulated `all_to_all_single` with uneven split sizes in `LocalTensorMode` and raise a clear error for inconsistent splits (#190311)
- Accept device-qualified Gloo backends in `monitored_barrier` when TorchComms is enabled (#189070)
- Prevent `CommDebugMode` hooks from leaking or double-running when a module executes more than once (#191452)
- Warn when symmetric-memory collectives are launched concurrently on multiple streams, which can otherwise deadlock (#191482)
- Choose a process group's default backend only from backend types that were actually registered (#189193)
- Report the correct group-local rank and process-group identifier in NCCL work timeout and error logs (#191440)
- Preserve the caller's current CUDA device in the experimental `nccl2` backend and validate full device identities (#191510)
- Validate all-to-all split sizes consistently across Gloo, NCCL, and `nccl2` (#191511)
- Prevent destroying one TorchComms subgroup from inadvertently destroying every live group (#191637)
- Propagate `device_id` through `ProcessGroupWrapper` so debug wrappers do not hang with heterogeneous rank-to-GPU mappings (#182273)
- Forward group identifiers through `nccl-lazy` so NCCL symmetric-memory rendezvous can find the primary communicator (#191544)
- Reject unsupported reconfigurable mode for `nccl-lazy` instead of advertising incomplete membership-change support (#191549)
- Disable NCCL NVLS in `nccl2` when deterministic algorithms are enabled, matching the legacy NCCL backend (#192104)
- Prevent `nccl2` watchdog errors, timeouts, explicit aborts, and normal teardown from unconditionally terminating the process (#192105)
- Fix Gloo and NCCL `split_group` crashes when the world process group was not the first backend instance created in the process (#192106, #192109)
- Fix device-bound `nccl2` process-group initialization failing before the CUDA caching allocator has been initialized (#192107)
- Give split and merged process groups independent backend options so child creation cannot corrupt parent metadata or share mutable options (#192110)
- Fix `split_group(backend=...)` filtering for parent groups created with a bare backend name (#192111)
- Prevent private `TCPStore` rendezvous under `torchrun` from hanging by using the agent store only for the agent's own address (#192113)
- Fix `bfloat16` NCCL `PREMUL_SUM` factors being interpreted as zero and silently producing zero gradients (#190747)
- Fix a use-after-free race while concurrently dumping Flight Recorder entries (#192232)
- Run symmetric-memory allocation and rendezvous device work on the caller's current CUDA stream (#192308)
- Recognize libuv's lowercase `address already in use` message when TorchElastic retries `TCPStore` creation (#191561)
- Add missing collective-fingerprint checks for `allgather_into_tensor_coalesced` under `ProcessGroupWrapper` (#185123)
- Fix DTensor AOT compilation misclassifying overload names containing `out` as output-variant operators (#187466)
- Fix compiled functional point-to-point collectives that pass global peer ranks to subgroup operations requiring group-local ranks (#187924)
- Preserve pipeline-stage module buffers while dynamic metadata inference runs representative forward and backward passes (#188558)
- Fix DTensor backward support for `cumprod`, `cummax`, and `cummin` (#185228)
- Make pipeline schedules select static metadata locally when a fake process group cannot perform cross-rank metadata inference, and report incomplete stage metadata clearly (#191538)
- Restore the caller's cyclic garbage collector state after Flight Recorder `read_dir()` calls, including when loading fails (#191607)

## Distributed (c10d)

- Fix `destroy_process_group()` hanging after collectives run on partially split process groups by keeping group names consistent across ranks (#190431)

## DTensor

- Fix compiled functions failing when they return DTensor permutation views such as `transpose`, `permute`, or `movedim` (#191784)
- Fix deferred `local_map` export failing inside nested compile regions (#186647)

## Linear Algebra Frontend

- Fix `torch.linalg.cond()` reporting a misleading overflow error for a complex norm order; invalid orders now raise `ValueError` with a clear message (#188591)
- Fix `torch.lu_unpack` segfaulting when `LU_pivots` has a shape inconsistent with `LU_data`; invalid shapes now raise a clear error (#187660)
- Fix `torch.linalg.lstsq(driver="gelsy")` returning an incorrect rank on CPU when stale pivot values leaked between batched LAPACK calls (#187436)
- Fix `torch.compile(dynamic=True)` failing on `torch.linalg.cond` with `p="fro"` or `p="nuc"` because symbolic tensor sizes were queried as concrete values (#187614)
- Fix offline `TunableOp` tuning silently using the wrong GEMM shape when a padded leading dimension matches another matrix dimension (#189355)
- Fix `CUBLAS_STATUS_NOT_SUPPORTED` failures in matrix multiplication on CUDA compute capability 11.0 by increasing the default cuBLAS workspace to 32 MiB (#189312)

## Indexing

- Reject nonempty `torch.unravel_index()` inputs whose `shape` contains a zero-sized dimension with a clear `ValueError` instead of an uncaught division-by-zero `RuntimeError`; empty indices remain supported (#191092)
- Fix assigning Python integers greater than `INT64_MAX` into `torch.uint64` tensors, which previously raised `Overflow when unpacking long long` (#191604)
- Fix an illegal CUDA memory access in `torch.nn.functional.adaptive_avg_pool2d` backward for very large contiguous tensors whose element offsets exceed 32-bit indexing limits (#189082)

## Profiler

- Exclude individual Python function events from `key_averages()` by default so frames such as `threading.py: wait` do not obscure operator-level hotspots; pass `include_python_functions=True` to retain the previous view (#188631)
- Clamp incomplete Python function events to their parent event's end time so exported traces retain correct nesting instead of placing overrunning events on unrelated tracks (#190950)
- Avoid importing the experimental CUPTI monitor during ordinary `record_function` profiling, preventing repeated warnings and tracebacks on systems with incompatible `cupti-python` versions (#187874)
- Fix reference leaks when reading the `layout` and `dtype` properties of profiler tensor metadata (#187068)

## FX

- Respect deferred runtime-assert bounds when deriving optimization hints for unbacked symbolic sizes, preventing negative storage sizes and downstream CUDA indexing failures (#190589)
- Make selected Dynamo, Inductor, and FX tracing state thread-local to prevent race conditions when `torch.compile` is invoked concurrently from multiple threads (#168999)
- Fix FX `GraphModule` serialization when generated code contains string type annotations (#185051)
- Fix scripting FX-generated modules with nested `Optional[Dict[...]]` annotations on Python 3.14 (#190580)
- Skip constant folding for `get_attr` nodes whose targets cannot be resolved or refer to modules (#191939)
- Preserve non-persistent buffer registration when an FX `GraphModule` copies attributes, keeping those buffers out of `state_dict()` (#191708)
- Fix Z3 translation validation for graphs containing symbolic boolean negation through `torch.sym_not` (#185147)
- Fix FX-generated code raising `NameError` for complex constants whose imaginary component is `nan` or `inf` (#188596)
- Preserve signed zero when FX code generation emits complex constants with a zero real or imaginary component (#185550)
- Apply `skip_folding_node_fn` recursively to `call_module` subgraphs so FX constant folding does not evaluate skipped or symbolic nodes inside them (#189487)
- Return valid `tuple[...]` annotations from `get_signature_for_torch_op` for operators that return multiple tensors (#189142)
- Avoid a `linecache` loader warning when executing generated FX `GraphModule` code on Python 3.15 (#187221)

## Dynamo

- Match CPython errors for invalid `next`, `set`, and `frozenset` calls (#190624, #189051)
- Fix `torch.compiler.nested_compile_region` graph reuse, eager autograd, graph capture, and transposed captured buffers (#192006, #184700, #186137, #191785)
- Fix nested graph breaks involving generators, hooks, context managers, custom operators, comprehensions, f-strings, and `DeviceMesh` submeshes (#188622, #191388, #187088, #191264, #191523, #189601, #187005, #187701, #188861)
- Fix `eager_then_compile` for higher-rank inputs (#184689)
- Fix precompile caches, package globals, and guard serialization for tensor subclasses, `torch.func`, and autocast (#191128, #191418, #190576, #191428, #184850, #187736, #184562)
- Fix tensor-subclass metadata guards, fake-mode re-entry, metadata replay, and stale metadata after in-place mutation (#184684, #176977, #185732, #187057, #187890)
- Fix compiled class definitions, scalar-tensor indexing, non-module globals, and conditional hook handles (#185998, #184625, #184653, #184712)
- Graph-break on forward-AD dual tensors instead of silently dropping tangents; `fullgraph=True` now errors (#189644)
- Preserve `ctx.needs_input_grad`, autocast state, overlapping-view storage, `vmap` gradients, and captured FlexAttention gradients (#191492, #186530, #187111, #186362, #188869)
- Fix compiled-method attribute reads, `TorchDispatchMode` skip state, symbolic lazy modules, and stale tracing weak references (#190185, #190287, #188595, #190951)
- Preserve dynamic f-string formatting and Python-side mutation order across graph breaks (#189830, #182638)
- Match Python semantics for `vars`, pybind enums, pytree equality, call errors, numeric conversion, descriptors, custom `isinstance`, deque reinitialization, sequence/set operators, subclass types, slice errors, and attribute probing (#185128, #188605, #190649, #190797, #190257, #190776, #186491, #188171, #189554, #189274, #189145, #187777, #190970)
- Fix Python 3.12 exception tables and free-threaded/Python 3.15 list-comprehension bytecode (#185731, #187086, #187103)
- Fix TorchScript backends, CUDA repro probing, and backend device/dtype classification while preserving third-party minifier configuration (#188875, #185843, #190425, #190426, #187855)
- Fix self-referential backward-compiler state when AOTAutograd compiles a second graph (#189325)

## Inductor

- Fix handling of `torch.combinations`, indexed `randperm`, dynamic-output custom ops, tensor-subclass standalone compilation, `torch.cond` constants, duplicate kernel registrations, generic `associative_scan`, dynamic combo reductions, empty scatters, autograd `expand`, tuple graph outputs, aliased FX outputs, and fused positional arguments (#189305, #184066, #185601, #185638, #185838, #186262, #186633, #187275, #188466, #188758, #189887, #190255, #190976)
- Match eager arithmetic, validation, dtype, NaN/infinity, signed-zero, and overflow semantics across `addmm`, remainder, min/max, low-precision scalar math, unsigned `abs`, CELU, Bessel functions, multiply-by-zero folding, `signbit`, floor division, `cummax`/`cummin`, `cumsum`, adaptive pooling, index propagation, and CPU integer arithmetic (#183511, #185168, #185970, #186818, #186933, #187024, #187321, #187354, #187580, #187941, #188049, #188361, #188556, #188862, #190328, #190427, #190531, #190566, #191132)
- Fix wrong or unstable results in CPU outer-loop and Halide fusion, nested/split/TMA reductions, MPS special functions, scheduler-recomputed gradients, CPU `expm1`, small transposed GEMMs, and noncontiguous `uniform_` (#185855, #186121, #188771, #189291, #189896, #185873, #190533, #191127, #191709, #192344)
- Fix CPU code generation for vectorized atomics and boolean `index_put_`, including an out-of-bounds atomic that could produce wrong results; fix max-autotune failures with reused GEMM inputs or outputs and zero-hinted symbolic rows (#185325, #185767, #186523, #191502, #191861, #192553)
- Fix `_scaled_mm` scale-shape compilation; fall back safely for `_scaled_mm_v2` with swizzled MXFP8/NVFP4 scales; and fix complex signatures, `float8` storage, dtype bitcasts, and CUTLASS INT8 target filtering (#183964, #185501, #186384, #188209, #189561, #189584, #192414)
- Fix convolution and attention pattern selection or fallback correctness for dynamic bias, transposed or dilated convolution, CUDA convolution backward, `ConvTranspose2d`, and unsupported 3D SDPA key permutations (#184132, #186067, #187372, #189660, #191260)
- Fix dynamic-shape and symbolic-expression failures in split ranges, adaptive pooling, AOTI autotuning, regional wrappers, TMA `addmm`, `torch.cond`, fused epilogues, stride guards, tiling, and FX wrappers (#184566, #185369, #185778, #185890, #187371, #189529, #189890, #190965, #191605, #191811)
- Prevent index-expression overflow, unsound loop-index inversion, and negative modular-term miscompilations (#186060, #189108, #190401, #190966)
- Fix FlexAttention errors and wrong results involving large or sliced buffers, invalid `score_mod`, kernel options, sparse masks, and mixed or 64-bit captured indices (#185264, #185991, #186876, #187886, #187904, #188484, #188876)
- Fix ordering and races in multi-stream event/control-dependency graphs, aligned input copies, bidirectional synchronization, replacement-created intermediates, captured events, and cross-warp reductions; honor `torch.use_deterministic_algorithms()` for compiled scans (#183803, #183804, #186022, #186023, #186025, #187224, #188533, #189095, #189096, #190519, #191714)
- Fix premature reuse, leaks, and races in memory planning, cached launchers, failed autotuning, dynamic reduction caching, mutation dependencies, fallback storage reuse, and saved compiler-cache loading (#187678, #188607, #188907, #189124, #189288, #189735, #192526)
- Reject incompatible custom-Triton epilogue fusion, fall back when descriptor alignment or template tiling is unsupported, and serialize custom-kernel `Enum` metadata correctly (#184248, #186922, #186932, #187209, #189494)
- Fix CUTLASS and NVGEMM compilation, worker initialization, XPU wrapper selection, reshaped epilogues, newer CuTeDSL compatibility, target filtering, cache reentrancy, and CUDA Graph outputs (#186385, #186791, #187404, #188865, #189775, #189780, #189781)
- Gate TF32 warnings, use an NVML clock-rate fallback, report CUDA Graph skip reasons, fix CUDA Graph capture for `torch.linalg.eigh`, and suppress internal `TypedStorage` warnings (#185541, #187427, #188384, #188641, #191383)
- Fix imports, compiler probes, workers, template decoding, and generated builds across vendored `typing_extensions`, localized MSVC output, initialized CUDA, Windows path limits, Python 3.11/3.12, UTF-8 templates, dead workers, and library paths containing spaces (#185708, #185972, #187408, #187641, #187700, #189196, #189290, #191010)
- Fix AOTInductor floor division by captured tensor constants, CUDA architecture packaging, and constant-graph code generation with lazy autotuning (#186242, #187888, #190073)
- Fix duplicate MPS Metal kernel names and XPU compiled RNG or quantized tensor-subclass handling (#187894, #189310, #189509)
- Fix manual collective-bucketing graph order and register DTensor shard-all-to-all autograd while adding an opt-in functional decomposition (#187341, #188137)
- Restrict ROCm Origami GEMM selection to static shapes to avoid dynamic-shape `NoValidChoicesError` (#190024)

## Ahead-Of-Time Inductor (AOTI)

- Fix compilation and dispatch failures for C++ wrapper fallback operators with `Any` arguments, including distributed operators such as `all_gather_into_tensor` (#188124)
- Route custom operators with `SymInt`, `SymBool`, or `SymFloat` arguments through boxed C++ wrapper dispatch, avoiding runtime `API call failed` errors (#188154)
- Box `None` passed to non-optional tensor arguments as an undefined tensor in C++ wrappers, matching eager custom-operator behavior (#188485)
- Prevent C++ wrappers from dereferencing a null tensor handle when a Python fallback operator returns a one-element `Tensor[]` (#190551)
- Emit portable `std::array::data()` pointers in generated CPU wrappers instead of relying on iterator-to-pointer conversion (#191240)
- Package AOTInductor CUDA multi-architecture kernels for the requested deployment architecture instead of the physical compilation GPU (#185328)
- Fix AOTInductor C++ wrappers recovering integer symbols from composed dynamic sizes through floating-point division, which could truncate valid runtime dimensions (#185841)
- Fail fast with a clear error when loading a CUDA AOTInductor package in a process without CUDA or ROCm available (#186943)
- Fix C++ wrapper fallback output indexing for mutable custom operators and remove invalid 16-byte alignment assumptions for misaligned tensor views (#187331)
- Preserve C++ wrapper input slots when graphs contain Python-only custom-class inputs (#188030)
- Pass the device the model was actually loaded on to custom operator fallbacks, instead of the device recorded when the model was compiled. Previously a model compiled for one GPU and then loaded on another would hand the wrong device to its custom ops (#184741)
- Synchronize the default stream after copying model constants on AMD GPUs, fixing a race in which inference could read constants before the copy had completed (#186963)
- Fix a 32-bit integer overflow when computing the SYCL global launch range in the AOTInductor runtime, which produced incorrect launch dimensions for large grids on XPU (#187307)
- Release AOTInductor input tensor handles when runtime input validation fails, preventing a GPU memory leak (#189503)
- Release untransferred AOTInductor constants when runtime constant folding fails, preventing a memory leak on the error path (#189505)
- Prevent an AOTInductor constant-folding segmentation fault on XPU when no stream is provided (#189517)
- Make the C++ wrapper's debug synchronization device-aware, fixing a regression on ROCm (#190071)
- Fix a missing CUDA header in the generated constant graph when compiling with the dual-wrapper, which made the generated code fail to compile (#191050)
- Skip CUDA stream event code generation in the AOTInductor C++ wrapper on XPU, where those APIs do not apply (#190637)

## Export

- Fix `torch.export` dynamic-shape specifications for functions with `**kwargs`, accepting both call-like keys and specs nested under the variadic parameter while reporting ambiguous name collisions as `UserError` (#185730)
- Prevent `ExportedProgram.module()` from raising `RecursionError` while generating guard messages for deeply nested symbolic-shape expressions (#186993)
- Fix `torch.export.unflatten` failing to restore parameters, buffers, and constants for non-contiguously numbered repeated module calls (#188185)
- Fix strict export of parameters from modules stored in unregistered Python containers by treating the traced-only parameters as constants instead of attempting to restore them from the eager module's state (#185728)
- Fix non-strict export of tensor indexing under `vmap` when the index is a batched scalar tensor (#186894)

## AOTDispatcher

- Resolve nested `AsyncCollectiveTensor` inputs before AOTAutograd tracing so compiled forward execution waits for in-flight data and backward metadata expects the correct local-tensor cotangents (#186442)
- Prevent activation-memory-budget partitioning from crashing with `expected all tensors_saved_with_vc_check to be Tensors, got [Tensor, tuple]` when a required multi-output node is marked `MUST_SAVE` (#188014)
- Prevent AOTAutograd common-subexpression elimination from merging forward-only values with nodes required by backward, preserving correct partitioning and reduction fusion (#184044)
- Fix backward graphs missing symbolic-integer bindings by preserving both raw symbols and their ShapeEnv replacement targets, preventing unbound guard expressions and `FxGraphCache` lookup failures (#185473, #189783)
- Fix incorrect alias-output slicing when Inductor clones a misaligned input (#191002)
- Move `invoke_subgraph` inference-mode input mutations to the AOT epilogue so they are applied correctly (#191672)
- Fix `control_deps` handling in the partitioner during forward/backward extraction (#187695)
- Support mutable (`Tensor!`) custom ops in input-mutating `invoke_subgraph` regions by routing them through Python functionalization (#189543)
- Fix common subexpression elimination (CSE) to correctly deduplicate NaN constant tensors by normalizing float/complex hashing and comparison (#191173)

## Composability

- Raise `NotImplementedError` for unsupported Boolean operations and distinguish unsupported FFT dtypes from invalid real/complex domains with `NotImplementedError` and `TypeError` (#192348, #192349)
- Preserve eager identity semantics for no-op dropout decompositions, preventing `torch.compile` and `torch.export` from replacing a `Parameter` with a cloned fake tensor when dropout is disabled (#185335)
- Fix compiled `torch.nn.functional.multilabel_margin_loss` values and gradients when targets use `-1` padding (#189552)
- Fix `torch.nansum` meta output shapes when `dim=()` should reduce all dimensions (#191530)
- Make the `constant_pad_nd` reference decomposition fully functional so `torch.onnx.export(dynamo=True)` no longer fails functionalization for models using `torch.nn.functional.pad` (#185636)
- Keep `torch.istft` length clamping and padding symbolic under dynamic shapes, avoiding recompilation and data-dependent guard failures when the requested length crosses the signal length (#186490)
- Make compiled and fake/meta `torch.aminmax(..., out=...)` enforce the same exact output-dtype requirements as eager execution (#186227)
- Make compiled `torch.nn.functional.celu` reject `alpha=0` with the same error as eager execution (#179375)
- Avoid data-dependent guard failures in fake/meta tracing of native multi-head attention with unbacked symbolic sizes (#187144)
- Avoid data-dependent guards in `torch.nn.utils.rnn.pad_sequence` decompositions when sequence lengths are symbolic (#187145)
- Make the CUDA `native_layer_norm` decomposition reject mixed affine-parameter dtypes in the same cases as eager execution (#185693)
- Fix incorrect compiled output and gradients for overlapping-input `torch.diagonal_scatter` operations (#182292)
- Match compiled `max_unpool2d` output strides and channels-last memory format to eager CPU execution (#186602, #187195)
- Route meta `view` operations through the symbolic-shape-aware kernel, avoiding `SymIntArrayRef expected to contain only concrete integers` failures (#189447)
- Avoid data-dependent guard failures in the transformer encoder layer meta kernel when the input size is an unbacked symbol (#187860)
- Prevent fake/meta decompositions of in-place operations from silently resizing their destination when operands cannot broadcast to its shape; compiled execution now raises the same shape error as eager execution (#191373)
- Preserve symbolic tensor, scalar, and unbacked-binding metadata across `ProxyTensor` and `make_fx` tracing (#187231)
- Preserve loop-local value ranges and use known ranges when simplifying symbolic `Min` and `Max` expressions, avoiding `vr must not be None` and spurious data-dependent guard failures (#187350, #186248)
- Fix symbolic proxy tracing and repeated lowering edge cases involving natural powers, `torch.cond` contiguous-stride expressions, and equivalent rebound unbacked symbols (#188278, #189525, #190083)
- Fix silently incorrect second-order gradients from post-dispatch `make_fx` tracing by decomposing `detach` by default; callers that provide an explicit decomposition table retain the previous behavior (#186845)

## Quantization

- Fix a divide-by-zero crash (`SIGFPE`) in `torch.quantize_per_channel` on the per-channel `float_qparams` path for the `qint32` dtype; whole-byte quantized types now pack correctly instead of underflowing the packing factor to zero (#186767)
- Add the missing overflow check to the FBGEMM build of the ARM `quantize_val` path, fixing incorrect quantized values that showed up as quantization test failures on some hardware (#187481)
- Fix a GPU memory access fault that aborted quantized `embedding_bag` byte and 4-bit rowwise lookups on ROCm, caused by a bitwise-AND typo in the bit-field extraction primitive (#192571)

## Foreach

- Prevent out-of-bounds metadata writes in CUDA foreach operations with complex scalar lists by respecting their reduced per-launch tensor capacity (#189915)

## ONNX

- Fix signed right-shift export in the TorchScript exporter so negative values round toward negative infinity as they do in PyTorch (#191226)
- Fix quantized `gather` export by unpacking quantized tensor inputs before lowering (#188272)

## C++ Frontend

- Fix a memory leak when converting `StableIValue` to `std::string` (#190493)
- Remove `noexcept` from `TensorMaker::computeStorageSize()` (#188062)
- Fix uninitialized return in Chebyshev polynomial helpers for NaN inputs (#187767)
- Guard the `Scalar(long long)` constructor on NetBSD and other LP64 BSDs (#188941)
- Replace `FileBaton` with `filelock` to prevent stale-lock deadlocks in `CppExtension` (#190543)
- Fix floating-point-to-integer range checks at wide-integer boundaries in `c10/util/overflows.h` (#190651)

## Build Frontend

- Fix source-build linker failures on systems where CMake reordered static and shared libraries by linking `libcpuinfo` through the `c10` shared library instead of linking it separately into both `c10` and `torch_cpu` (#167328)
- Fix Windows ARM64 builds failing to register a CPU quantized backend by recognizing the uppercase `ARM64` CMake processor name and enabling oneDNN (#189346)

## Release Engineering

- Fix invalid ZIP64 archives for ROCm wheels larger than 4 GB by repackaging them with `auditwheel` (#189903)
- Prevent an intermittent deadlock during `import torch` with ROCm wheels by shipping a bare `.so` alias (#189114)
- Fix missing CUDA dependencies when extracting LibTorch from a wheel, which previously left the extracted tree with unresolved RPATHs (#184336)

## CUDA

- Fix CUDA graph kernel-annotation remapping across sequentially captured graphs and with `keep_graph=True` (#186638, #187741)
- Fix a heap overflow in `CachingHostAllocator` when rounding is disabled (#192722)
- Preserve signed zero in `relu` and `clamp` (#185354)
- Fix `int32` overflow in `embedding_bag(mode="max")` backward (#188661)
- Include CUDA graph memory pools in `memory_reserved()` (#186809)
- Use 64-bit sample offsets in `NLLLoss2d` backward (#190144)
- Fix remap extents, causal key bounds, and 32-bit dropout offsets in memory-efficient attention (#192138)

## cuDNN

- Fix cuDNN variable-length SDPA (#172108)
- Disable cuDNN convolution engines 58 and 63 on `sm120` to prevent illegal memory accesses (#190112)
- Declare the attention-mask dtype to cuDNN instead of inheriting the graph I/O dtype (#191612)
- Update the cuDNN errata filter for `sm120` (#191701)

## CPU (x86)

- Fix incorrect results from CPU flash SDPA when the innermost dimension of the inputs is not contiguous (#187506)
- Prevent the Laguerre and Legendre polynomial kernels from returning uninitialized memory (#188027)

## CPU (AArch64)

- Fix an integer overflow in the `bfloat16`/`float16` GEMM staging-buffer size calculation, which could corrupt results or crash on large matrix multiplications (#191096)
- Fix CPU `embedding_bag` using the wrong index count for `scale_grad_by_freq`, producing incorrect gradients (#190264)

## MPS

- Fix compiled MPS operations such as `torch.eye(256)` failing with `KeyError` when Inductor generates unsigned 16-, 32-, or 64-bit index expressions (#192020)
- Preserve the MPS dispatch key through `torch.func` transforms so MPS autocast and autograd work under transforms such as `vmap` and `grad` (#187282)
- Reject complex MPS average-pooling inputs with `NotImplementedError` instead of an internal MPSGraph error (#187671)
- Propagate NaNs correctly through MPS scaled dot-product attention kernels (#188147)
- Raise a clear error when MPS batch normalization receives an unsupported dtype (#188265)
- Fix corrupted MPS prefill-attention output on macOS 26 by selecting the correct Metal cooperative-tensor ABI (#191794)
- Fix Metal argument alignment that could make MPS kernels fail validation or crash under the Metal debug layer (#191640)
- Fix `torch.hypot` producing incorrect results for extreme values (#192541)
- Handle empty indices in MPS `index_add` and empty dimensions in threshold, `baddbmm`, and `addbmm` operations (#186990, #187719, #188808, #187879)
- Fix `mm` and `addmm` with strided output tensors on macOS 14 and 15 (#187255)
- Respect `storage_offset` when an MPS binary operation consumes a zero-dimensional CPU tensor view (#187229)
- Make MPS `baddbmm` follow its documented behavior by not propagating NaN or infinity from the input when `beta=0` (#187522)
- Fix MPS linear backward for inputs with more than four dimensions and prevent complex high-rank linear operations from aborting on macOS 27 (#187379, #190352)
- Prevent `BatchNorm` backward from crashing for channels-last MPS tensors (#188371)
- Fix incorrect MPS Conv2d output when a kernel spatial dimension is at least 256 (#188359)
- Match CPU and CUDA nonfinite-value semantics for MPS `torch.div(..., rounding_mode="floor")` (#189252)
- Make MPS-backed pinned memory correctly appear as a CPU tensor while retaining its shared Metal buffer (#181720)
- Prevent dtype-converting MPS-to-CPU copies from overwriting their source and correctly copy non-dense views with matching strides (#189572, #189966)
- Compute integer absolute values exactly instead of rounding through `float32` (#190053)
- Handle zero `in_features` in MPS linear forward and backward without aborting (#190051)
- Fix `torch.nextafter` returning its input unchanged for MPS `bfloat16` tensors (#190481)
- Preserve exact integer values in MPS `torch.linspace` for large ranges (#189630)
- Fix `int64` minimum and maximum reductions returning zero when a partial SIMD group contains only negative or positive values (#191104)
- Fix adaptive max pooling for input sizes that are not divisible by the output size (#189659)
- Fix large matrix multiplications producing incorrect results on M1 and M2 GPUs (#183535)
- Keep MPS exponential samples strictly positive so `torch.multinomial(..., 1)` cannot select a zero-probability entry (#192621)
- Make CPU and MPS `torch.logit` agree with other backends when `eps > 0.5` (#181297)
- Fix MPS FFT operations when a transformed dimension is not among the tensor's final four dimensions (#186967)
- Fix `torch.nn.functional.linear` dropping its bias for vector-shaped inputs on macOS 26 (#188619)
- Raise clear unsupported-dtype errors for complex MPS inputs to `cummax`, `cummin`, and `logaddexp2` (#188038, #188800)
- Fix MPS ternary-kernel dispatch for large tensors and mixed-dtype `out=` tensors, including `torch.clamp` (#189624)
- Apply inter-layer dropout correctly in MPS LSTM backward and avoid NaNs when `dropout=1` (#190059)
- Improve MPS layer-normalization correctness for small-variance rows and add 64-bit indexing support (#190492)
- Fix biased MPS linear operations corrupting rows when a batch dimension exceeds 2^16 (#189496)
- Validate MPS `EmbeddingBag` offsets consistently with CPU and CUDA instead of silently returning incorrect results (#187572)
- Support `float32` affine parameters with `float16` or `bfloat16` MPS layer normalization in forward and backward (#190055)
- Match CPU and CUDA RMSNorm precision by performing the fused affine multiplication in float32 (#189617)
- Fix Conv2d forward and backward with non-contiguous MPS weights (#192303)
- Raise clear unsupported-dtype errors for complex `igamma`/`igammac` and boolean `torch.linalg.cross` inputs on MPS (#188134, #187274)
- Prevent intermittent crashes when stopping a Metal capture by draining work from all active MPS streams first (#191362)

## ROCm

- Fix `torch.nn.functional.interpolate` with `mode="nearest"` failing on large channels-last inputs with `torch.AcceleratorError: HIP error: invalid configuration argument`. The channels-last `upsample_nearest2d` forward kernel launched a grid whose total thread count exceeded HIP's `UINT32_MAX` limit once the output approached 2^32 elements; this was a regression from 2.9 that showed up in diffusion VAE decode at large batch sizes (#180310)
- Fix incorrect `torch.nn.LayerNorm` results for tensors with a very large number of rows when the normalized size is not a multiple of 4. The non-vectorized fallback exceeded HIP's launch limit; it now uses a grid-stride loop over rows (#186956)
- Fix `torch.cuda.make_graphed_callables` failing to capture, or hanging, on ROCm when the callable uses hipBLASLt. Warmup and capture now run on the same stream so the hipBLASLt handle is created and cached before capture instead of being lazily created mid-capture (#187745)
- Fix graph-capture error handling on ROCm 7.14 and later by using HIP's native capture errors instead of the compatibility precheck required by older ROCm versions (#187110)
- Fix transposed convolution failing with `miopenStatusBadParm` when the computed spatial output is zero-sized. MIOpen rejects zero-length tensor descriptors, so these cases now short-circuit to an empty output (and zero gradients in backward), matching cuDNN and CPU behavior (#187431)
- Fix a meta-kernel shape mismatch for memory-efficient scaled dot product attention on ROCm. The meta registration padded the log-sum-exp dimension to a 32-element alignment as CUDA does, while the ROCm backends return a compact log-sum-exp, breaking nested tensor SDPA backward and `torch.compile` (#190723)
- Fix the memory-wait instructions used by the atomic-store commit path on `gfx10`, `gfx11`, and `gfx12` GPUs. These architectures have separate load and store counters, and `gfx12` renames the wait instructions, so the wrong instruction was previously emitted (#188067)
- Fix failures when building HIP C++ extensions on Windows with `Don't know how to compile <file>.hip`. `.hip` sources produced by hipify are now registered with the MSVC compiler so they are dispatched to `hipcc` (#187665)
- Fix out-of-bounds accesses in CK SDPA for tile-unaligned shapes by padding sequence-length allocations (#187152)

## XPU

- Fix compiled `torch.signbit` for `float64` inputs on XPU by avoiding an incorrect Triton XPU signature (#188818)
- Fix compiled `multi_margin_loss` with weights on XPU by using one-dimensional indexing in its decomposition (#188770)
- Handle empty tensor inputs correctly in XPU `addmv` (#174193)
- Fix oneDNN SDPA with GQA and a broadcasted mask on XPU (#190503)
- Fix `max_unpool2d` channels-last stride mismatch on XPU (#190189)
- Fix `bmm_outer_product` Triton override to support XPU tensors (#188783)
- Raise `RuntimeError` instead of crashing when XPU cannot allocate a pinned host-memory buffer (#189681)
- Route `GPU_USER_ANNOTATION` Kineto profiler events to `DeviceType::XPU` (#191841)

## Functorch

- Fix a crash in `torch.func.vmap` when `out_dims=-1` and the mapped function returns an output that is independent of its vmapped input (#178495)

## JIT

- Make TorchScript reject bare `list` and `tuple` value annotations consistently with `Attempted to use list without a contained type` or the equivalent tuple error; specify an element type such as `list[int]` instead (#188779)
- Fix runtime compilation of JIT fuser kernels on ROCm 7 when HIPRTC's `bfloat16` conversion symbols collide with PyTorch's embedded definitions (#185656)
- Fix `torch.jit.script` failing with `Cannot re-assign modules in a ScriptModule with non-scripted module` when a wrapper contains an already-scripted child with a `__jit_ignored_attributes__` submodule (#187863)

## Sparse Frontend

- Create cuSPARSELt handles per device so sparse operations remain valid when a thread switches between CUDA devices (#189048)
- Make grouped-matrix, batch-normalization, and sparse-matrix operations on ROCm Windows raise clear unsupported-operation errors instead of crashing with access violation `0xC0000005` when optional libraries are unavailable (#191680)

# Performance

## Python Frontend

- Reduce Python custom-op dispatch overhead and speed up CPU quantiles with partial selection (#187949, #186175, #188394)

## torch.nn

- Reduce `linear_cross_entropy` memory and chunking costs, and avoid materializing RMSNorm copy-on-write tensors (#187219, #187838, #189202)

## Autograd

- Reduce `autograd.Function.apply` overhead and constant-fold more generated backward formulas (#189582, #189788, #189800, #189577, #192611)

## Distributed

- Balance packed-document context-parallel attention across ranks (#189902)

## Symmetric Memory

- Improve symmetric-memory all-gather, peer-copy overlap, and large-scale rendezvous (#185359, #192530, #192623)

## Linear Algebra Frontend

- Speed up CUDA `addmm`, batched LU factorization, and viewable batched `matmul` (#191706, #181998, #186178)

## FX

- Speed up unused-submodule deletion and reduce boxed-call peak memory (#178320, #187186)

## Dynamo

- Reduce compiled-call and TVM overhead and speed up native `itertools` tracing (#190390, #190571, #190392, #186973, #186974, #189012)
- Avoid unnecessary guards, recompiles, and FlexAttention cache misses (#187782, #189482, #185739, #188177)

## Inductor

- Reduce RNG clones, tune RDNA3 FlexAttention and ROCm reductions, enable XPU linear fusion, and enable Origami for ROCm max-autotuning by default (`TORCHINDUCTOR_ORIGAMI=0` opts out) (#188495, #177840, #181854, #183364, #186644)
- Reduce combo-kernel, guard, NVGEMM-cache, and CPU expression overhead (#184323, #184752, #185966, #185967, #187013, #186356)
- Improve combo and persistent reductions, XPU fallbacks, and optional `cat_linear` fusion (#186668, #186957, #187147, #187880, #187940, #188179, #188180)
- Improve NVGEMM isolation and decode tuning, Blackwell split reductions, and host-side TMA launches (#188303, #188579, #188646, #188822)
- Optimize FlexAttention predicates, broadcast-bias `baddbmm`, small GEMMs, softmax, and Triton 3.8 defaults (#188929, #189127, #189149, #189162, #189187)
- Improve NVGEMM small-M and block-scaled kernels, compilation, launching, and caching; profile ten configurations by default (`TORCHINDUCTOR_NVGEMM_MAX_PROFILING_CONFIGS=5` restores five) (#189771, #189777, #189805, #189773, #189778, #189779, #189806, #189841, #189807)
- Optimize Triton min/max with relaxed signed-zero ties (`torch._inductor.config.strict_signed_zero=True` preserves eager ties), combo-kernel register use, fusion locality, FlexAttention code generation, and peak-memory scheduling (#190404, #190689, #191349, #192247, #192449)
- Reduce fusion-analysis, repro-generation, and symbolic-comparison overhead (#192675, #192818, #192819)

## Ahead-Of-Time Inductor (AOTI)

- Add opt-in pinned asynchronous AOTInductor constant loading through `AOTI_COPY_USE_PINNED_ASYNC=1` (#186258)

## Export

- Make large-graph export decomposition scale linearly (#177927)

## AOTDispatcher

- Avoid an unnecessary `Tensor.detach()` in AOTAutograd backward (#189759)

## Composability

- Reduce dynamic-shape tracing and wide-symbol substitution costs (#192677, #185884)
- Optimize `reciprocal(sqrt(x))` and BatchNorm inference with `rsqrt` (#190206)

## Quantization

- Speed up bias addition in dynamically quantized `float16` CPU linear layers (#189943)

## CUDA

- Avoid synchronization and redundant initialization in CUDA kernels, optimize FFT fill, and tune Rubin elementwise kernels (#186508, #190269, #190953, #190546)

## cuDNN

- Reduce cuDNN convolution cold-start overhead (#187212)

## MPS

- Move interpolation, logical, indexing, Mish, median, and range operations to faster native Metal kernels (#186989, #187324, #187109, #187906, #187060, #188905, #188921, #191060)
- Speed up Cholesky, LU factorization and solves, GEMV, and sequence-length-one linear decoding (#187022, #187038, #189200, #186927, #189855)
- Optimize full, strided, batched, variance, normalization, and arg/min/max reductions (#187313, #188412, #191101, #191097, #191098, #191099, #191100)
- Reduce allocator fragmentation, decoding memory, and synchronization overhead (#187441, #190438, #190115)
- Optimize FlexAttention, 3D convolution, GLU, sigmoid, and log-sigmoid; accelerate attention prefill on supported macOS versions and GPUs (#188663, #188802, #192229, #187833, #187151, #187228, #182256)
- Speed up concatenation and sliced-view copies, including pinned transfers (#188200, #188483, #188613, #189512)
- Fix incorrect large-`int64` results while optimizing flat `torch.unique`, and reduce `torch.nonzero` memory use (#184780, #191274)

## ROCm

- Prefer hipBLASLt on additional ROCm architectures (#185375)

## XPU

- Fuse low-precision upcasts into XPU softmax and reduction kernels (#189999)

## JIT

- Reduce JIT startup and compilation overhead (#181118, #188121, #183813)

# Documentation

## Python Frontend

- Document all accepted device-like arguments for `torch.set_default_device`, including integer accelerator indices and `None` (#187240)
- Document the tensor-factory keyword arguments accepted by the `torch.normal(mean, std, size)` overload (#187820)
- Clarify that the `index` argument to `Tensor.index_reduce_()` selects positions in `self` to accumulate into, rather than positions in `source` (#189008)
- Document that `torch.searchsorted` does not validate sorting and has undefined behavior for unsorted input when no `sorter` is provided (#184888)
- Correct the `torch.arange` dtype-inference note to refer to the `step` argument instead of the nonexistent `stop` argument (#188943)
- Add docstrings for top-level in-place functions that have out-of-place equivalents (#189571)

## torch.nn

- Clarify that `torch.nn.functional.gaussian_nll_loss` uses `eps` to clamp `var` to a minimum rather than adding it to `var` (#190058)
- Add deterministic example output to the `torch.nn.Tanh` documentation (#189390)
- Correct the documented `mat_b` shape for `torch.nn.functional.grouped_mm` and explain how to pass grouped linear weights (#191610)
- Correct the `ceil_mode=True` output-size formula in the `torch.nn.MaxPool1d` documentation (#188735)
- Document that repeated calls to `torch.nn.Module.parameters()` return parameters in a deterministic order when the module is unchanged (#189990)

## Optimizer

- Fix incorrect learning-rate curves in the `torch.optim.lr_scheduler.ChainedScheduler` and `torch.optim.lr_scheduler.SequentialLR` documentation (#186468)

## Distributed

- Correct typos in distributed memory-analysis documentation and related distributed and utility docstrings (#187079, #189357, #190827)
- Document the callback signatures, return values, keyword-argument behavior, and usage of `distribute_module` (#188071)
- Correct PyTorch brand name capitalization in distributed checkpoint and other documentation (#189248)
- Document the experimental process-group reconfiguration APIs and provide an end-to-end usage example (#191384)
- Document how to enable and verify NCCL symmetric-memory kernels through registered memory pools or symmetric-memory rendezvous (#192515)

## Linear Algebra Frontend

- Clarify `torch.linalg.norm`, `torch.linalg.matrix_norm`, and `torch.linalg.vector_norm` behavior for complex inputs, and correct the documented `ord` values accepted by `torch.linalg.vector_norm` (#190381, #188204)

## Dynamo

- Link the guard-overhead page to the developer blog post and document a profiler-based way to measure guard overhead (#191387)

## ONNX

- Clarify that `output_names` labels outputs but does not reorder them (#175796)

## XPU

- Update the XPU documentation with newly supported operating-system versions and simplified installation instructions (#187923, #190992)

# Security

## Python Frontend

- Validate tensor shapes and sequence bounds in `torch.quasirandom.SobolEngine` before native kernels index direction-number tables (#191198)
- Make stream comparisons with non-stream objects safe and Python-consistent: equality returns `False`, `stream != None` now returns `True` instead of `False`, and ordering comparisons raise `TypeError` instead of returning `False` (#192523)

## torch.nn

- Validate `grad_output` shapes in 2D and 3D `grid_sample` backward operations before CPU, CUDA, or MPS kernels can read out of bounds (#191915)
- Validate channel counts in `replication_pad1d` and `replication_pad2d` backward operations to prevent out-of-bounds reads and segmentation faults (#189463)
- Validate `mean`, `invstd`, and `counts` shapes before CUDA batch-normalization statistics gathering to prevent out-of-bounds reads (#190005)

## Distributed

- Add an opt-in `weights_only=True` mode to distributed object collectives for restricted deserialization; the default remains unchanged for compatibility (#189353)
- Validate symmetric-memory signal channels and peer ranks to prevent out-of-bounds device-memory access and adjacent-allocation corruption (#191596, #191842)
- Parse Flight Recorder rank expressions with `ast.literal_eval()` instead of executing them with `eval()` (#191490)

## Mobile

- Reject malformed mobile FlatBuffer modules whose function class-type index is out of range, preventing an out-of-bounds access and crash during loading (#186672)

## Sparse Frontend

- Always validate sparse-tensor invariants when loading with `torch.load(..., weights_only=True)` so malformed checkpoints cannot create tensors whose indices cause out-of-bounds reads (#184750)

  Validation is an O(nnz) scan and applies regardless of the global `torch.sparse.check_sparse_tensor_invariants` setting. Fix or regenerate malformed sparse checkpoints that now raise errors such as `RuntimeError: size is inconsistent with indices`. Do not use `weights_only=False` as a workaround for untrusted files.


# Developers

## torch.nn

- Integrate Helion with the native-DSL registry and add reusable kernel instrumentation (#190636)

## Distributed

- Extend process groups for reconfiguration, one-sided windows, lifecycle hooks, backend-routed rank/size, and safe ROCm builds (#186888, #186298, #186299, #186300, #187467)
- Modernize RPC and backend extension APIs with atomic shared pointers, canonical `_single` collectives, custom-op `ProcessGroup` inputs, and Python entry points (#185633, #187140, #187459, #187388)
- Support optional NCCL expert parallelism and keep experimental `nccl2` builds portable (#187366, #187385, #189938, #189958)
- Add TorchElastic error enrichment, update sequence-number and `FakeStore` interfaces, and expose a backend-agnostic Flight Recorder hook (#187098, #188611, #189259, #189363)

## Distributed (c10d)

- Add fake-backend `split_group` support and correct c10d type stubs (#186290, #191633)

## Symmetric Memory

- Add the `USE_NCCL_EP` source-build option (#177437)

## Profiler

- Add CUDA graph lifecycle hooks for the experimental CUPTI monitor (#191299)

## FX

- Add source-stack provenance to compiler profiler timelines and preserve device indices in minifier repros (#186230, #186547)

## Dynamo

- Make generated graphs and repros deterministic and robust for higher-order operators, symbolic storage sizes, and non-UTF-8 diagnostics (#181775, #186804, #190838, #190696)

## Inductor

- Improve compiler provenance, custom-pattern matching, wrapper timing, and repro serialization (#183952, #184419, #187936, #190728)
- Add optional external TLX backend integration (#189094)

## Ahead-Of-Time Inductor (AOTI)

- Add optional kernel-context metadata for generated C++ wrappers (#184513)

## Export

- Improve raw Triton export errors and draft-export report readability (#185827, #186070)

## C++ Frontend

- Add portable lifetime annotations across borrowed C++ APIs (#190076, #190077, #190075, #190074, #189912)
- Enforce C++20 headers and add safer integer conversions and borrowed-range support (#178150, #190092, #186635)

## Developer Experience

- Add the contributor-facing `spin docs` wrapper (#182814)

## Build Frontend

- Limit concurrent FlashAttention compilation and update `clang-tidy` (#192305, #191111)

## Release Engineering

- Migrate builds from `setuptools` to `scikit-build-core` (#180247)

## MPS

- Regenerate bundled Metal headers when sources change and clean up newer-SDK compiler warnings (#189179, #187087, #186822, #187753, #188416, #188910, #191636, #191970)

## ROCm

- Support ROCm ASAN builds and derive hipCUB's CCCL version automatically (#188242, #188072)
- Update CK/AITER for `gfx1033` and residual-NaN fixes, and fix a `libdrm` installer overflow (#183965, #187799)

## XPU

- Consolidate XPU operator generation and align internals with oneAPI 2026 (#181233, #191470)
- Move the XPU C++ memory-pool API to ATen (#192032)

## Caffe2

- Fix source builds with `fmt` 12.2 and Windows Clang 17 (#190691, #192376, #190929)

## JIT

- Restore `TensorExpr` builds with LLVM 24 (#192381)
