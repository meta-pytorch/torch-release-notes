# PyTorch 2.9.0 Release Notes
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
   <td><strong>Unstable (API-Unstable)</strong></td>
  </tr>
  <tr>
   <td>Updates to the stable libtorch ABI for third-party C++/CUDA extensions</td>
  </tr>
  <tr>
   <td>Symmetric memory that enables easy programming of multi-GPU kernels</td>
  </tr>
  <tr>
   <td>The ability to arbitrarily toggle error or resume on graph breaks in torch.compile</td>
  </tr>
  <tr>
   <td>Expanded wheel variant support  to include ROCm,  XPU and CUDA 13</td>
  </tr>
  <tr>
   <td>FlexAttention enablement on Intel GPUs</td>
  </tr>
  <tr>
   <td>Flash decoding optimization based on FlexAttention on X86 CPU</td>
  </tr>
  <tr>
   <td>ARM Platform improvements and optimizations</td>
  </tr>
  <tr>
    <td>Enablement of Linux aarch64 binary wheel builds across all supported CUDA versions</td>
  </tr>
</table>

For more details about these highlighted features, you can look at the [release blogpost](https://pytorch.org/blog/pytorch2-9/). Below are the full release notes for this release.


# Backwards Incompatible Changes

## Min supported Python version is now 3.10 (#162310)

The minimum version of Python required for PyTorch 2.9.0 is 3.10. We also have 3.14 and 3.14t available as preview with this release.

## Undefined behavior when an output of a custom operator shares storage with an input

This is a reminder that outputs of PyTorch custom operators (that are registered using the `torch.library` or `TORCH_LIBRARY` APIs) are not allowed to return Tensors that share storage with input tensors. The violation of this condition leads to undefined behavior: sometimes the result will be correct, sometimes it will be garbage.

After [#163227](https://github.com/pytorch/pytorch/pull/163227), custom operators that violated this condition that previously returned correct results under `torch.compile` may now return silently incorrect results under `torch.compile`. Because this is changing the behavior of undefined behavior, we do not consider this to be a bug, but we are still documenting it in this section as a "potentially unexpected behavior change".

This is one of the conditions checked for by [`torch.library.opcheck`](https://docs.pytorch.org/docs/stable/library.html#testing-custom-ops) and is mentioned in [The Custom Operators Manual](https://docs.google.com/document/d/1_W62p8WJOQQUzPsJYa7s701JXt0qf2OfLub2sbkHOaU/edit?tab=t.0#bookmark=id.4c0um7xkba6e)

### More details

Outputs of PyTorch custom operators are not allowed to return Tensors that share storage with input tensors

For example, the following two custom operators are not valid custom operators:

```py
@torch.library.custom_op("mylib::foo", mutates_args=())
def foo(x: torch.Tensor) -> torch.Tensor:
    # the result of `foo` must not directly be an input to foo.
    return x

@torch.library.custom_op("mylib::bar", mutates_args=())
def bar(x: torch.Tensor) -> torch.Tensor:
    # the result of bar must not be a view of an input of bar
    return x.view(-1)
```
The easiest workaround is to add an extra `.clone()` to the outputs:
```py
@torch.library.custom_op("mylib::foo", mutates_args=())
def foo(x: torch.Tensor) -> torch.Tensor:
    return x.clone()

@torch.library.custom_op("mylib::bar", mutates_args=())
def bar(x: torch.Tensor) -> torch.Tensor:
    return x.view(-1).clone()
```

A common way to get into this situation is for a user to want to create a custom operator that sometimes mutates the input in-place and sometimes returns a new Tensor, like in the following example.

```py
@torch.library.custom_op("mylib::baz", mutates_args=["x"])
def baz(x: torch.Tensor) -> torch.Tensor:
    if inplace:
        x.sin_()
        return x
    else:
        return x.sin()
```
This dynamism is not supported and leads to undefined behavior. The workaround is to split the custom operator into two custom operators, one that always mutates the input in-place, and another that always returns a new Tensor.
```py
@torch.library.custom_op("mylib::baz_outplace", mutates_args=())
def baz_outplace(x: torch.Tensor) -> torch.Tensor:
    return x.sin()

@torch.library.custom_op("mylib::baz_inplace", mutates_args=["x"])
def baz_inplace(x: torch.Tensor) -> torch.Tensor:
    x.sin_()

def baz(x):
    if inplace:
        baz_inplace(x)
        return x
    else:
        return baz_outplace(x)
```

## Build metal kernels of MacOS-14+ and remove all pre-MacOS-14 specific logic, requires MacOS-14+ going forward (#159733, #159912)

PyTorch MPS is only supported on MacOS-14 or later. If you need to use MPS on MacOS Ventura, please avoid updating to Python-3.9 or above

## Upgrade to DLPack 1.0 (#145000)

This upgrade is doing the same BC-breaking changes as the DLPack release. Objects in `torch.utils.dlpack` have been updated to reflect these changes, such as `DLDeviceType`.

See the PR for details on the exact changes and how to update your code.

## Raise appropriate errors in `torch.cat` (#158249)

`torch.cat` now raises `ValueError`, `IndexError` or `TypeError` where appropriate instead of the generic `RuntimeError`. If you code was catching these errors, you can update to catch the new error type.


## Default to `dynamo=True` for ONNX exporter (#159646, #162726)

Previously `torch.onnx.export(...)` used the legacy TorchScript exporter if no arguments were provied. The ONNX exporter now uses the newer `torch.export.export` pipeline by default (`dynamo=True`). This change improves graph fidelity and future-proofs exports, but may surface graph capture errors that were previously masked or handled differently.

Previously in torch 2.8.0:

```python
# API calls the legacy exporter with dynamo=False
torch.onnx.export(...)
```

Now in torch 2.9.0:

```python
# To preserve the original behavior
torch.onnx.export(..., dynamo=False)

# Export onnx model through torch.export.export
torch.onnx.export(...)
```

Recommendation: first try the new default; only fall back if you hit blocking issues and report them upstream.
Long term solution: fix the root cause instead of relying on fallback or TorchScript exporter.

## Switch off runtime asserts by default in Export in favor of a shape guards function (#160111, #161178, #161794)


To enable runtime asserts, use `export(..., prefer_deferred_runtime_asserts_over_guards=True)`. Also kills the `allow_complex_guards_as_runtime_asserts` flag, merging it into the former option.


Additionally, `exported_program.module()` will generate a call to a `_guards_fn` submodule that will run additional checks on inputs. Users who do not want this behavior can either remove this call in the graph, or do `exported_program.module(check_guards=False)` to avoid the generation.

## Set default opset to 20 in ONNX (#158802)

Opset 20 enables newer operator definitions. If your tooling or downstream runtime only supports opset 18, pin it explicitly. For the latest ONNX operators, you can experiment with opset 23.

Previously in torch 2.8.0:

```python
# opset_version=18
torch.onnx.export(...)
```

Now in torch 2.9.0:

```python
# To preserve the original behavior
torch.onnx.export(..., opset_version=18)

# New: opset_version=20
torch.onnx.export(...)

# Use the latest supported opset: opset_version=23
torch.onnx.export(..., opset_version=23)
```

## Drop `draft_export` in exporter API (#161454, #162225)

Remove implicit draft tracing from the default exporter path, achieving clearer behaviour and faster failures.
The expensive `torch.export.draft_export` diagnostic path is no longer auto-invoked (which could take hours on large models). You can still opt in for deep diagnostics:

Previously in torch 2.8.0:

```bash
# If both torch.export.export(..., strict=False) and
# torch.export.export(..., strict=True) fail to capture
# the model graph, torch.export.draft_export(...) will be triggered,
# and uses real tensor to trace/export the model.
#
# Inside export_to_onnx.py:
#  ... torch.onnx.export(..., dynamo=True)
python export_to_onnx.py
```

Now in torch 2.9.0:

```bash
# To trigger torch.export.draft_export once
# torch.export.export strict=False/True both
# fail:

TORCH_ONNX_ENABLE_DRAFT_EXPORT=True python export_to_onnx.py
```

## Remove `torch.onnx.dynamo_export` and the `onnxrt` torch compile backend (#158130, #158258)

`torch.onnx.dynamo_export` is removed. Please use `torch.onnx.export` instead.
The experimental ONNX Runtime compile backend (`torch.compile(backend="onnxrt")`) is no longer supported.

## Remove `torch.onnx.enable_fake_mode` (#161222)

The `dynamo=True` mode uses `FakeTensor`s by default which is memory efficient.

## Some public facing ONNX utility APIs for the TorchScript based exporter are now private (#161323)

Deprecated members in `torch.onnx.verification` are removed. Previously private `torch.onnx.symbolic_opsets*` functions will no longer be accessible. Consider making a copy of the source code if you need to access any private functions for compatibility with the TorchScript based exporter.

## Remove `torch.onnx.symbolic_caffe2` (#157102)

Support for `caffe2` in the ONNX exporter has ended and is removed.

## Remove `/d2implyavx512upperregs` flag that slows build (#159431)

Re-introduced AVX512 optimizations for Windows VS2022 builds, may cause issues with specific versions of VS2022, see #145702

## Add `ScalarType` to shim conversion and `stable::Tensor.scalar_type` (#160557)

Before, user extensions could only in abstract pass around obfuscated dtypes appearing as `int32_ts`. Now, users can confidently use `torch::headeronly::ScalarType` in their extensions for major scalar types. This PR enables ABI stability by adding a translation layer through the shim, so that even if the `ScalarType` enum values change in the future, user extensions need not fear.

This change adds ScalarType support for user extensions and is only narrowly BC breaking for unpopular dtypes: `quint*`s, `qint*`s, `Bits*`, `dummy_uint*`s, `dummy_int*`s, `Float8_e8m0fnu`, and `Float4_e2m1fn_x2` in the use case where an extension retrieves a Tensor dtype of the above and passes it into `aoti_torch_call_dispatcher`.

# Deprecations
## Deprecate `pin_memory_device` param in `torch.utils.data.DataLoader` (#158323)

We move enabling `pin_memory` back inside `BaseDataLoaderIter`. This is required for `StatefulDataloader` which leveraged `BaseDataLoaderIter` direclty rather than the `Dataloader` class init

## Deprecate `torch.export.export_for_training` API in favor of equivalent `torch.export.export` API (#158203)

`torch.export.export_for_training` exists because we couldn't migrate internal usages of export to the final IR. Now that we have completed the migration, we deprecated and deleted this API.

# New Features
## Python Frontend
- Add utility to get the kernel currently registered on the dispatcher (#158393)
- Extend `__torch_function__` handler to be triggered by elements within a list (#160256)
- Add `torch.hash_tensor` reduction function (#154149)

## FX
- Extend torch function support to ALL arguments instead of just scalar type (but not inside of list, #145089)
- Add `is_fx_symbolic_tracing` flag (#161385)

## Dynamo
- Experimental API for ahead-of-time compiling models in fullgraph mode (#161383)
- Add a hook for recompilations (#157961)
- DynamicInts prototype (#162194)

Introduces an API for annotating dynamic integer inputs & attributes for `torch.compile`, by wrapping plain ints with `DynamicInt()`.
DynamicInt objects also work in eager mode, acting as their underlying values when passed as scalar inputs.

```python
a = DynamicInt(4)
y = a + 2  # DynamicInt(6)
z = torch.ones(a)  # torch.ones(4)

fn = torch.compile(torch.ones)
fn(a)  # compiled fn takes a dynamic integer input
fn(2)  # returns torch.ones(2) without recompiling
```


## Optimizer
- Introduce Muon optimizer to PyTorch (#160213)

## Profiler
- Add GC Events to Python Stack Tracer (#161209)
- Add a custom profiler configuration option (#151656)

## Inductor
- Allow user to pass in custom partitioner function (#157580)

## Export
- Add support for param mutation under inference mode (#159661)

## AOTDispatcher
- Add AOTDispatcher config to set backward autocast behavior (#156356)

## Quantization
- Enable cpu fp8 qlinear and cpu fp8 qconv (#155678, #157076)

## ONNX
- RMS Norm support in opset 23 (#159377)

## C++ Extensions
- Build out a stable set of ATen ops in `torch/csrc/stable/ops.h`:  `amax`, `narrow`, `new_empty` + `new_zeros` dtype variant, `pad`, (#159328, #158974, #159508, #161597, #160214)
- Add `torch::stable::Tensor()` default constructor,  `is_cpu`, and `get_device_index`(#159507, #160212, #160143)
- Add beginnings of `torch::stable::accelerator` with support for DeviceGuard and Stream (#159679, #160453)
- Start building out `torch/headeronly`: c10 Macros, STD_TORCH_CHECK, ScalarTypes (like BFloat16 and Half, #158035, #158365, #157912, #158377, #159302, #159414, #159412, #159415, #159411, #159911)
- Remove cmake cache and reconfigure again if it is invalid (#156958)
- Cut a version of `TORCH_ERROR_CODE_CHECK` in `headeronly` from AOTI (#159604)
- Remove `wheel` from build requirements (#158027)
- Error when `TORCH_STABLE_ONLY` is defined in `TensorBase.h` (#161658)

## Build Frontend
- Add transpose to `torch/csrc/stable` (#158160)
- Add `zero_()` and `empty_like(t)` to `torch/csrc/stable/ops.h` (#158866)

## Release Engineering
- Add support for CUDA 13.0 in CI/CD builds. Enable CUDA compression mode for binary size reduction for CUDA 13.0 builds (#160956, #161073, #161257, #161663, #161316, #160201, #160770, #161013, #161916, #162268, #162322, #162383, #161833)

- Enable CUDA 12.6, 12.8 and 13.0 support for Linux ARM64 CD builds (#162364, #160720, #159481)

- Add support for Python 3.14 in CI/CD builds (#156889, #157559, #159261, #159869, #160593, #160788, #161255, #159725)

- Enable NVSHMEM integration (#151261, #153010, #154538, #155506, #156685, #158938, #161321, #160778, #159907, #160465)

## CUDA
- Add getter for CUDA graph exec to allow mutation of captured kernel params (#161294)
- Implement support for `cudnn_batch_norm_out` kernel to replace the autogen approach (#123020)

## CPU
- Support GQA for flash attention (#157893)

## MPS
- Partial sparse support for MPS backend (#159729, #160254, #160223, #161846, #162007, #157238)
- Add `avg_pool3d`, `max_unpool1d/2d/3d`, `max_pool3d`, `max_pool3d` bwd pass, and `avg_pool3d` bwd pass for MPS (#158877,#159789, #156467, #157498, #159089)

## ROCm
- OCP Micro-scaling Format (mx-fp8/mx-fp4) Support (#151360)

## XPU
- Enable `FlexAttention` on Intel GPU (#143553)

# Improvements
## Python Frontend
- Speed up `torch.load` under `FakeTensorMode` by reducing random reads (#157931)
- Make `torch.utils.benchmark.utils.timer` accelerator agnostic (#157131)
- Improve error message for weight-only load errors (#159935)

## torch.nn
- Allow `register_buffer` with `Tensor`-like objects (#159455)
- Improve error message for unsupported padding configurations (#160866)
- Validate target is 0D when input is 1D in `NLLLoss` (#161412)

## Optimizer
- Resolve warning in LBFGS when converting a tensor with `requires_grad=True` to a scalar (#160389)
- Resolve `SequentialLR` deprecation warning about invoking `step(epoch)` (#149392)

## Autograd
- Support deterministic `torch.nn.Upsample` `mode="trilinear"` backward (#154239)

## Distributed
### c10d
  - Add improvements to eager init of `ProcessGroupNCCL` (#156748)
  - Simplify unique hash management of `ProcessGroupNCCL` (#156790)
  - Support per operation timeouts in `ProcessGroupGloo` (#158128)
  - Allow ping to be retried in `TCPStore` (#159165)
  - Support scalar tensor for functional `all_gather` (#149913)
  - Expos `unsafe_get_ptr` for dist.ProcessGroupNCCL.NCCLConfig (#161136)
  - Add batch option for `send/recv_object_list` (#160342)
  - Make FakeStore optional to be passed into fake backend (#162164)
  - Enable complex datatype support in `ProcessGroupGloo` (#156633)
  - Move thread-local capture mode guard to include `work.isStarted` (#160398)
### DistributedDataParallel (DDP)
  - Support ddp zero hook XCCL path (#159240)
### DTensor
  - Relax `device_mesh` argument constraint in `local_map` (#157049)
  - Support complex numbers in DTensor redistribute (#157329)
  - Rework partial propagation in point-wise op and support mul (#157340)
  - Allow dynamic shapes for `DTensor` slice (#157953)
  - Implement `histc` op (#158298)
  - Made dispatch to sharding prop over decomps (#159324)
  - Support user-supplied Generator for random ops (#159933)
  - Add `propagate_tensor_meta` function that skips cache if `_are_we_tracing` (#161334)
  - Support `local_map` as a decorator (#161353)
### Device Mesh
  - Enable the use of user set backend and pg option even for the global mesh (#157501)
  - Enable slicing a submesh with warnings (#158899)
  - Allow controlling PG backend and options via `init_device_mesh` (#159371)
### FullyShardedDataParallel2 (FSDP2)
  - Support custom `all_gather` and `reduce_scatter` comms (#155189)
  - Made it fail `set_allocate_memory_from_process_group` if used together with custom comm hooks (#157487)
  - Use `reduceOpSum` when world size is 1 (#157529)
  - Skipp `allgather` when world size is 1 (#160135)
  - Use `post_reduce_stream.record_event()` on hsdp+cpuoffload (#160481)
### Tensor Parallel (TP)
  - Improve `parallelize_module` API to support more cases (#157182)
### TensorPipe
  - Update TensorPipe pinned dependency version (#159834)
### TorchElastic
  - Enable NUMA binding integration with elastic agent and `torchrun` (#149334)
  - Support NUMA Binding for Callable Entrypoints (#160163, #161183)
### Pipeline Parallelism (PP)
  - Add `eval()` API to schedule (#157795)
  - Allow intermediate nodes in zero bubble to have multiple grads (#159084)
  - Support `OVERLAP_F_B` computation type (#158978)
  - Initializ P2P communicators on first step (#160210)
  - Add `DualPipeV` schedule (#159591)

## Linear Algebra Frontend
- Use rocSOLVER for Cholesky inversion on AMD. (#157154)
- Add option for using TF32 as fp32 internal precision for matmul/linear/conv on MKLDNN (#157520)
- Make einsum produce contiguous outputs in more cases (#161755)

## Profiler
- Add more CUDA API for kernel launcher (#156016)
- Allow Custom Time Unit When Printing Profiler Table (#157913)
- Update CUDA runtime kernel identification logic (#157890)

## FX
- Fix DCE eliminating random operations by improving `is_impure()` (#151524, #157981)
- Support converting a float32 tensor to a scalar in FX trace. (#158216)
- Correctly copy `self.module_stack` in ModuleStackTracer (#159956)
- Add tool to track events in graph split (#159795)
- Add `node_name_match` to subgraph rewriter (#157574)

## Dynamo
- Improve tracing support for various Python builtin data structures/modules:
  - `list`s (e.g. #153969)
  - `set`s (e.g. #153150)
  - `dict`s (e.g. #154794)
  - `iter` (e.g. #156371)
  - `itertools` (e.g. #159693)
  - `collections` (e.g. #159365)
  - `collections.NamedTuple` (#159367)
  - frozen `dataclasses.dataclass` (#159529)
- Graph break error messages link to a website with more information (#159011)
- Add option for `TorchDispatchMode` to ignore `torch.compile` internals (#161648)

## Inductor
- Add Inductor support for MTIA backend (#159211)
- Share default device context when all graph partitions and cudagraph-unsafe ops are on the same device(#162873)

## Ahead-Of-Time Inductor (AOTI)
- Enable AOTI for CPU on Windows (#158915)
- Re-enable TMA templates w/ AOTI (#157819)
- Don't allow int32 indices if `{non-inf, > int32_max}` upper bound is provided (#159433)
- Add RecordFunction to C shim so that profiling works with AOTI (#159842)
- Add AOTI C shim functions for collective ops (#154492)
- Add missing ops to set of C-shim ops which can have nullptr returns (#158073)

## Export
- Handle `None` & ellipsis slicing/select in non-strict (#157821)
- Extend FP8 types in serialization (#158430)
- Improve error messages for deserialization (#159881)
- Support serialization for `triton_kernel_wrapper_functional` HOP (#161314)
- Support serialization for complex constants (#161517)
- Add runtime asserts to `while_loop` HOP subgraphs (#158467)
- Warn on side-effectful code in strict mode (#160060)
- Support for vmap in pre-dispatch export (#154650)
- Support vmap and custom autograd function/improve DTensor constructor inefficiency (#162240)

## AOTDispatcher
- Skip logging in fp8 activation quantization if there are no nodes to be quantized (#158129)
- Add `aot_export_joint_with_descriptors` and `aot_compile_joint_with_descriptors` (#158715)
- Extract out `prepare_aot_module_simplified` for use in next PR (#158319)
- Rename modules in AOTAutograd (#158449)
- Track descriptors for all inputs/outputs of AOTAutograd traced graph (#158624)
- Improve graph output alias with subclass error message (#159619)
- Pass fw/bw compilers to `aot_export_joint_with_descriptors` (#159814)

## Composability
- Meta implementation for `aten.add.Scalar` (#161332)
- `aten.expand_copy` decomp (#161688)
- Fix result dtype cast in decomp for `aten.linalg_vector_norm` (#155111)
- Add dtype checks in meta implementation for several ordering ops (#159556)
- Fix meta function for `aten.complex` (#160894)
- Improve unbacked symint (dynamic shape) support for several decompositions (#148815, #156902, #157008, #158894, #159184, #160683, #160253, #162084, #162099, #162109, #160462)

## Quantization
- Avoid getting model device once per node for pt2e quantization flow (#159901)
- Fixes bug in implementation of `HistogramObserver` (#156457)
- Support `bias=None` for `fbgemm_linear_fp16_weight` CPU op (#158535)
- Add Static Dispatch Kernel for `wrapped_fbgemm_linear_fp16_weight` for Sigmoid (#160451)

## Nested Tensor (NJT)
- Added initial `log_softmax()` support (#159662)

## Foreach
- Invoke `vector.reserve()` consistently for non-inplace foreach operations (#161128)
- Faster and safer lambda expression capture in `has_integral_tensor()` (#161042)

## ONNX
- Support symbolic arguments in ONNX exporter (#157734)
- Fix `torch.tensor` warning in ONNX `symbolic_opset10` export  (#158835)

## C++ Frontend
- Generalized `AllocatorConfig` to be device-agnostic via new `AcceleratorAllocatorConfig` (#149601, #150312)
- Added `Scalar::isUnsigned()` method (#159877)
- Exposed `ModelRunner` from nativert as public (#159989)
- Improve error message for `torch.binomial` enforcing float inputs (#157658)

## Build Frontend
- Fix dev warning in `Dependencies.cmake` (#159702)
- Fix building system gloo with CUDA/HIP (#146637)
- Build `libtorch` without NVSHMEM (#160910)
- Improve BLAS feature detection (#143846)

## Release Engineering
- Enable vLLM testing workflow (#160583, #161565, #162292, #162000, #161797)
- Enable Windows ARM64 CI testing (#148753, #161504)
- Enable PyTorch ROCm CI for MI355X testing. (#158889)

## CUDA
- Make cublaslt/hipblaslt workspaces persistent (#156495)
- Remove unnecessary warnings during the ATen compilation process (#157703)
- Slightly improve error message from `repeat_interleave` kernel (#157996)
- Add framework for explanations for common CUDA errors (#158395)
- Upgrade KernelLauncher `kernelLaunchCheck` to print help string (#158896)
- Prep for cutlass upgrade by ignoring `Wunused-but-set-variable` (#159276)
- Workaround ATen SFINAE under `libc++` (#161101)
- Implement changes to CCCL (CUB/Thrust/LibCUDACXX) usage in ATen (#153373)
- Add maybe unused flag to remove warning (#157655)
- Use new CCCL API in v2.8 (#160554)
- Improve cupy device placement when device is provided with explicit index (#158529)

## CPU (AArch64)
- Made PyTorch compilable with gcc-14 on ARM (#157867)

## MPS
- Add `shifted_chebyshev_polynomial_[tuvw]`, `igamma/igammac,grid_sampler_3d, native_dropout`/`native_dropout_backward`  (#157488, #161927, #160541, #162108)
- Extend atomic operations to all int types (#158179)
- Extend `index_put` to complex types (#160159)
- Extend `addmm` to integral types (#160270)
- Add support for unsigned types (#159094)
- Add API to query GPU core count (#160414)
- Add `kthvalue` (#161817)
- Type-promote tensor-iterator common dtype (#160334)
- Implement `logcumsumexp` metal kernel (#156858)
- Enable `dlpack` integration (#158888)
- Dynamic reductions (#159355)
- Update `avg_pool2d` to use Metal kernel when `ceil_mode=True` (#161011)

## ROCm
- Additional hipify mappings (#158056, #158352, #161992)
- Refactor `composable_kernel` (CK) backend user interface to improve user experience (#152951)
- Allow use of `rocSOLVER` for Cholesky inversion. (#157154)
- AOT Inductor enable gfx950 for max autotune using CK (#159195)
- Add flag `torch.backends.miopen.immediate` to toggle MIOpen Immediate Mode instead of relying on `deterministic=True` and `benchmark=False` (#158951)
- MIOpen convolutions no longer call `reshape_` or unexpectedly change memory formats (#161687)

## XPU
- Support Intel GPU quantization ops in AOTInductor (#156572)
- Add `device_id` to Intel GPU properties to distinguish iGPUs with identical names (#156481)

# Bug Fixes
## Python Frontend
- Add option in `torch.utils.cpp_extension.load_inline` to override gencode (#156850)
- Fix `max_width` computation in Tensor printing (#126859)
- Improve `pin_memory` error message on CPU-only systems (#159994)
- Making batching rule for `F.embedding` DTensor-aware (#162117)

## Autograd
- Fix `torch.autograd.Function` memory leak due to `torch.utils.checkpiont` early stopping (#161171)
- Fix `torch.autograd.graph.GradientEdge` for `torch.autograd.Function` (#160098)
- Match 0-dim gradients device type regardless of subclass-ness (#160165)

## Distributed
### c10d
  - Fix slow init due to repeated dns resolution failure in socket (#159596)
  - Fix `setGroupName` and `setGroupDesc` in `group_split` and `merge_remote_group` (#159429)
  - Fix a bug of distributed 'gather' with noncontiguous tensors on the Gloo backend (#158903)
  - Fix a bug of distributed 'gather' with noncontiguous tensors on the NCCL backend (#159549)
  - Fix data inconsistencies when using `batch_isend_irecv` with 2D tensor views by making P2P tensors dense (#163719)
  - Handle discontiguous `allgather`/`reducescatter` inputs (#163712)
### Device Mesh
  - Fix the not incorrectly chained each of the strings as iterables (#160709)
### DistributedDataParallel (DDP)
  - Fix incorrect interaction between `DDPOptimizer` and donated buffers (#160745)
### DTensor
  - Fix DTensor handling of conjugate bit (#158030)
  - Fix `OpSchema` equality check (#161231)
  - Fix `grouped_mm` strategy for invalid stride cases (#158245)
  - Fix `F.one_hot` in DTensor (#162307)
  - Always disabled `ShardingPropagation` cache if compiling (#156868)
### FullyShardedDataParallel (FSDP)
  - Fix the bug in FSDP offload `pin_memory` (#157147)
  - Fix to ensure writeback handles `NO_SHARD` correctly by flattening tensors before copying (#154369)
### FullyShardedDataParallel2 (FSDP2)
  - Fix error message for `fsdp_pre_all_gather` (#160817)
  - Fix the issue with `set_reduce_scatter_divide_factor` errors and `MixedPrecisionPolicy`  (#155964)
### Pipeline Parallelism (PP)
  - Fix eval step under `no_grad()` (#159293)
  - Fix zero bubble schedules for `eval()` (#159475)
### TensorPipe
  - Fix `import torch` if compiled without `TensorPipe` (#159461)
### TorchElastic
  - Fix wrong log file name in the docs of `torch.distributed.elastic.multiprocessing.start_processes()` (#160396)

## Linear Algebra Frontend
- Avoid downcasts for fp16 matmul on the BLAS backend (#161999)

## Profiler
- Fix Linter for Global Annotations flag in Snapshot (#157858)

## FX
- Fix `split_module` with symint (#160093)
- Fix `getattr_recursive` with ModuleList (#161204)
- Skip const folding with symbolic expression (#161437)
- Fix qualified name for methods of `torch.Tensor` (#162224)

## Dynamo
- Fix segfault due to interaction between Dynamo backends and `torch.compiler.reset()` (#156527)
- Fix crash due to bad interaction with recompilations and with blocks in Python 3.11+ (#162318)

## torch.nn
- Fix silent correctness w/ backpropping grads for `FlexAttention` (#163677)
- Fix `return_lse` warning message in `FlexAttention` (#163578)
- Fix `FlexAttention` head broadcast (#163426)

## Inductor
- Fix wrong meta function for `constant_pad_nd` (#159878)
- Fix learnable bias assertion error in Inductor (#161170)
- Fix int64 from `MutationOutput` Buffer (#162020)
- Fix Inductor CUDA sort `NaN` behavior (#159308)
- Fix layout for local buf in outer loop fusion (#160857)
- Fix slice scatter `dtype` consistency (#160851)
- Fix 3d tiled online softmax (#162341)
- Fix unsafe collective reorder past wait in Inductor (#157489)
- Fix `FallbackKernel` alias function to avoid incorrect aliasing for custom ops (#163227)

## Ahead-Of-Time Inductor (AOTI)
- Fix a bug from `load_constants` (#161887)
- Fix wrong propagation of fallback_ops_dict in `gen_aoti_c_shim` (#159904)
- Fix unbacked symint and memory leak in Inductor memory planning (#159839)
- Fix memory leak in AOTI when calling `aoti_torch_as_strided` (#162118)
- Explicitly delete `wait_tensor` returned tensor (#159502)
- Fix memory leak from `all_reduce` (#159818)

## Composability
- Make functionalization ViewMeta serializable with pickle (#163769)

## Export
- Fix bug in constants lifting pass (#157719)
- Fix `from_node` provenance in unlift pass (#157943)
- Fix `NaN` serialization (#155359)
- Fix deserialization for unbacked symbol ranges (#158681)
- Fix runtime assert handling in deserialization (#159060)
- Fix for FQN handling in unflattener (#159418)
- Fix `nn_module_stack` for `assert_tensor_metadata` nodes (#159625)
- Fix usage for `move_to_device_pass` (#159992, #160528, #162301)
- Avoid name overwrites for aliased exported module parameters (#160600)
- Avoid inling `dynamo.disables` in unflattening (#161306)
- Fix deserialization issue for storage offset (#162172)
- Remove `.contiguous()` when saving weights to raw bytes to preserve original storage size of tensor (#163587)

## Quantization
- Avoid `NaN` in fp8 output of CPU `qlinear` and `qconv` ops (#160957)
- Fix segmentation fault when `choose_qparams_optimized` (#161966)

## Foreach
- `chunk_size` should always be `int64_t` for Foreach functors (#156872)

## ONNX
- Make onnx export SDPA match ATen behavior (#159973)
- Fix `rotary_embedding_23` implementation (#162865)
- Fix export behavior when model has `None` as output (#160200)
- Fix lower opset version support in `dynamo=True` (#161056)
- Fix `index_put_` usage (#161263)

## C++ Extensions
- Fix CPP extension distributed warning for `TORCH_CUDA_ARCH_LIST` to only log when running on non-distributed or on rank 0 (#162764)

## C++ Frontend
- Fix `torch.utils.cpp_extension` parser for clang version 20.1.7+libcxx (#157666)
- Fix `MakeTensor::computeStorageSize()` calculation (#158690)
- Fix static initialization order issue with `AllocatorConfig` (#159629)

## Build Frontend
- Turn on `BUILD_BUNDLEPTXAS=1` to allow compile on newer GPUs(#163988)

## CUDA
- Handle uninitialized `torch.backends.cuda.matmul.fp32_precision` (#161102)
- Fix nansum in non-JIT build (#158633)
- Decrease launch bounds of CTCLoss backward for blackwell to avoid crash (#159522)
- Implement workaround for `cudaErrorNotSupported` (#162412)
- Fix missing `__syncthreads` in MultiMarginLoss backward (#158994)
- Roll-back cuDNN frontend upgrade and update Meta registration due to compile issues (#163104)
- Disable cuDNN for 3D convolutions with `kernel size != 1` for cuDNN 9.8+ (#163581)

## CPU
- Add check so non-aarch64 platforms can hit `MKLDNN` path (#162168)

## MPS
- Fix batch norm incorrect gradient (#156867)
- Do not crash if `tensor dim > INT_MAX` (#158824)
- Avoid outputing zeros from `exponential_` for MPS (#159386)
- Fix MPS autocast for `ConvTranspose3d` (#160345)
- Fix MPS `conv3d` autocast bias dtype mismatch (#160423)
- Fix error check for `torch.var` on scalar (#160889)
- Fix `index_add` for complex + int64, int64 input + zerodim index (#160926, #161511)
- Fix `constant_pad_nd_mps` bug when pad is empty (#161149)
- Fix `index_select` for `scalar_types` (#161206)
- Fix `index_copy` for scalars and `index_copy` for strided indices (#161267, #161333)
- Ensure that tensors are contiguous before using MPS linear kernel (#161641)
- Address `NaN`s if SDPA is called with all values masked from query (#157727)
- Fix invalid formatting (#158436)
- Fix empty input in posneg functions (#161824)
- Migrate round unary op to Metal (#161712)
- Type-promote tensor-iterator common dtype (#160334)
- Fix regression in 2.8.0 for `scaled_dot_product_attention` using MPS (#163598)
- Chunk `fillBuffer` into 4Gb slices to avoid regression on MacOS 26 (#164108)
- Fix latent bug that can result in segfault in CPP extensions (#164093)

## ROCm
- Fix Inductor with cudagraph trees `hip:0` device error (#161221)
- Fix some build failures and support some BLAS calls on Windows (#161981)
- Fix undefined symbol linker error after exposing MIOpen symbols on Windows (#156479)
- Fix finding ROCm/HIP version on Windows (#156486)
- Fix LoadHIP handling of environment variable paths on Windows (#159080)
- Add hipcc compatibility flags to `cpp_extension.py` on Windows (#159790)
- In SDPA via AOTriton, `logsumexp` needs scaling back to natural base (#156903)
- Check stream graph capture status in `memcpy_and_sync` inline function (#158165)

## XPU
- Fix `cpp_extension` compatibility with `intel-deep-learning-essentials-2025.2` (#161012)

## JIT
- Make `ErrorReport::CallStack` thread-safe (#160386)
- Fix `RemoveProfileNodesAndSpecializeTypes` handling for `Tensor?` that is resolved to `None` (#161538)

# Performance
## Optimizer
- Use `addmm` to improve Newton–Schulz orthogonalization in Muon (#161379)
- Avoid stream sync in SWA `AveragedModel.update_parameters()` (#157705)

## Autograd
- Fix SVD forward-mode AD multiplication priority (#161027)

## Dynamo
- Recursive `dict` tag optimization for faster guard evaluation (#159183)

## Inductor
- Improve performance of A16W4 and A16W8 `GEMM` template (#159127, #161148)
- More aggressive persistent reduction (#161055)
- Add a few outer dimension reduction cases for LOAF (#162028)
- Fuse two RoPE kernels into a single kernel and improving runtime efficiency (#161420)

## Export
- Caching optimizations for placeholder naming pass (#158594)
- Add Static Dispatch Kernel for `fmod.Scalar` and `scale_gradient` (#160654, #160454)

## CUDA
- Use a nonblocking copy to avoid stream synchronization for GPU tensor indexing with CPU mask (#156384)
- Disable cudagraph GCs by default to improve capture performance (#158649)

## Release Engineering
- Upgrade to ROCm 6.4.1 and 6.4.2 patch releases (#156636, #158887, #158886, #158651, #159001)
- Migrate RPyTorch ROCm CI to MI325 capacity (#159059, #159649, #161184)
- Enable B200 PyTorch benchmark testing (#158011, #157341)

## MPS
- Optimize cummin/cummax metal kernels (#156794)
- Speedup `torch.full` for 1-byte types (#158874)
- Speedup `argmax`/`argmin` (#159524)
- Improve performance of `max_pool3d` (#157875)
- Avoid calling tensor ops in `max_pool3d` impl (#157874)
- Move `max_pool2d` to Metal for `stride != 1` (#157876)

## ROCm
- SDPA now uses AOTriton to 0.11b (#161754)
- `hipblaslt` is used by default on gfx908 for ROCm >= 6.3 (#159092)
- Enable miopen channels last 3d for conv and batchnorm (#160529)
- Remove extra transposes in NHWC convolutions on MIOpen (#160435)
- Remove extra sync in `tensor.item()` (#158486)
- Elementwise and reduction kernel perf improvements (#159430, #159652, #160444, #160466, #161054, #161180, #161181)
- Enable build of `fbgemm_gpu genai` sources for grouped GEMM support (#160676)

## XPU
- Enable tensor memory descriptor Triton template for Intel GPU (#161600)

# Documentation
## Python Frontend
- Improve documentation for `torch.lobpcg`, `torch.clone`, `torch.matmul`, `torch.max`, `torch.gather`, `torch.Tensor.scatter_`, `torch.empty_like`, `torch.randint`, `torch.mul`, `torch.min`, `torch.max`. `torch.sort`, `torch.full_like`, `torch.histogramdd`, `torch.hamming_window` (#156139, #157007, #161424, #156153, #157929, #157920, #158050, #158731, #160312, #161539, #162051, #158275, #152682)
- Remove torchscript related sections in serialization docs (#156648)
- Fix typo in `torch.set_float32_matmul_precision` docs (#158191)
- Fix docstring for `torch.nn.utils.clip_grads_with_norm_` to reflect clamping behavior (#158200)
- Fix the Doc issue on the description of edge_order in `torch.gradient` (#159130)
- Add `torch.segment_reduce` docs (#154352)
- Add examples to `torch.is_floating_point` and `torch.is_complex` docs (#161951)
## torch.nn
- Improve description of `padding` for `avg_poolnd` (#159142)
- Improve `CrossEntropyLoss` docs with example of incorrect target specification (#155649)
- Remove redundant dtype conversion in `scaled_dot_product_attention` example (#161613)

## Optimizer
- Document specific optimizer modules APIs e.g., `torch.optim.adam.Adam`, properly (#158483, #158669, #160194)
- Add note for clarity in Adafactor doc #154862 (#155248)
- Minorly improve `zero_grad` description (#161239)

## Autograd
- Improve `torch.inference_mode` docs and error message (#161164)

## Distributed
### c10d
  - Documented barrier collective's interaction with `device_id` (#159389)
  - Fix comment to match logic in `distributed_c10d.py` (#162158)
### DTensor
  - Rewrote doc of `TupleStrategy` (#158132)
  - Documented `redistribute_costs` (#158495)
### FullyShardedDataParallel (FSDP)
  - Removed FSDP1 developer note (#158991)

## Profiler
- Update PT2 Profiler Torch-Compiled Region Image (#158066)
- Fix Experimental Config Documentatation(#156586)
- Update README (#159816)

## FX
- Fix typos in `torch/` (`torch/fx/`, #156604)
- Add typing (#158450)
- Fix typo in FX interpreter class docs (#162055)
- Remove allow-untyped-defs from `torch/fx/experimental/migrate_gradual_types/util.py` (#157236)

## Inductor
- Add documentation for CUDAGraph partition (#159450)

## Export
- Update docs around draft export, dynamism, and PT2 Archive (#157750)

## ONNX
- Update export docstring (#162622)
- Delete deprecated tutorial page link (#157310)
- Filter out torchscript sentences (#158850)
- Fix doc typo for `symbolic_multi_out` (#160702)
- `onnx.md` to simplify deprecated entities (#159312)
- Update export docstring and set `fallback=False` by default (#162622, #162726)
- Fix typo in error message: summit -> submit (#162587)

## Release Engineering
- Add decorator to create deprecation warnings (#155127)
- Add runnable code examples to export documentation (#158506)
- Add developer notes for integrating new backends into PyTorch (#158644)

## XPU
- Update supported OS to Windows 11 & Ubuntu 24.04/25.04 for Intel client GPU (#161699)

# Security
## Python Frontend
- Don't store flamegraph to tmp folder (#157374)

# Developers
## Python Frontend
- Better sample inputs for addmm OpInfo (#160234)

## Distributed
### c10d
  - Add `waitcounter` for watchdog and heartbeat monitoring thread (#157480)
  - Made `torch.distributed.breakpoint` set a long timeout (#158481)
  - Add `check_rng_sync` util (#160283)
  - Add `FlightRecorder` support for `ProcessGroupXCCL` (#158568)
  - Add `early_stop` kwarg to `torch.utils.checkpoint` (#160781)
### DTensor
  - Wrap sharding prop error with contextual exception (#161574)
  - Add check if tracing for sharding propagation to handle un-hashable keys in DTensor (#160798)
### Device Mesh
  - Add error when users try to slice non contiguous flattened dim submesh (#157523)
  - Make the repr shorter when debug ENV not set (#158822)
### ShardedTensor
  - Make error message descriptive in ShardedTensor creation (#150627, #159423)
### Pipeline Parallelism (PP)
  - Add profiling to schedule execution (#160753)

## FX
- Consolidate stack trace in Tracer (#156257, #157302, #158266)
- Separate provenance tracking to different levels (#160383, #158399, #158796, #159484)
- Fix `register_foward_pre_hook not supported on ScriptModule` error (#156904)
- Add `__eq__` function to NodeSource (#158170)
- Add `__hash__` function to NodeSource (#158322)
- Cache dict and string rep for better perf in NodeSource (#158372)
- Recover node source from dict (#158373, #158473)
- Include error stacktrace and graph module in `tlparse` error (#158469)
- Add `expanded_def` option for FX printing, render descriptor, update tests (#158708)
- Remove `co_lnotab` in favor of `co_linetable` (#159227)
- Remove duplicate imports (#161685)
- Include Output tensor metadata for `CompiledFxGraph` (#159311)

## Inductor
- Deprecate `allow_tf32` in `tl.dot(..., allow_tf32=...)`, use `tl.dot(..., input_precision=...)` (#160711)
- Log autotune choices and benchmark result to scuba/chrome trace (#159496)
- Add TLParse artifact for logging runtime of collective and compute ops (#159730)
- Call `jit_post_compile_hook` within Inductor Triton Kernel compile path (#161443)
- Prune configs that require more shared memory than the hardware limit (#161996)
- Runtime estimations using nccl estimator on mm only benchmark mode (#161405)
- Don't use `torch.backends.cuda.matmul.allow_tf32` in Inductor cache key (#159480)

## Ahead-Of-Time Inductor (AOTI)
- Better error message when no .so/cpp files are found (#156863)
- Clean up old APIs in AOTI c shim (#158400)
- Add Inductor provenance mapping for cpp extern kernel (#161656, #162069)
- Print out error msg when nvcc compiler fails (#157203)
- Add kernel information JSON generation for AOTI packages (#160540)

## Composability
- Stop suggesting to use `guard_size_oblivious` on data dependent errors (#160510)
- Avoid unnecessary slices resulting in data-dependent errors (#157528)

## Quantization
- Revamp dtype documentation (#156087)
- Use new type statement to fix public API of types (#158487)

## Dataloader Frontend
- Add `torch.utils.data` samplers benchmark script (#156974)
- Add `torch.utils.data.Dataloader` benchmark script (#159432)

## Release Engineering
- Replace `setup.py develop` with `pip install -e` for development builds (#155998, #156027, #156710)  (#156709)

## XPU
- Upgrade Intel GPU software stack package to intel-deep-learning-essentials-2025.2 (#158733)
