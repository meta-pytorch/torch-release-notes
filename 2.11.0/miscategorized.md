## foreach_frontend (from linalg_frontend)
- linalg._powsum and _foreach_powsum ops ([#172685](https://github.com/pytorch/pytorch/pull/172685)) (from: linalg_frontend, labeled `release notes: foreach_frontend`)

## CPU / Linear algebra
- Added support for FP16 half-precision GEMM via OpenBLAS on CPU, enabling faster FP16 inference ([#169042](https://github.com/pytorch/pytorch/pull/169042)) (from: optimizer_frontend, labeled `release notes: optimizer` but is a CPU/BLAS change)

## Linear algebra
- Avoid differing results in `linalg.(tensor_)solve` when vmapped ([#154983](https://github.com/pytorch/pytorch/pull/154983))

## not user facing
- Rm platform args xplat/caffe2/aten/src/ATen/native/quantized/cpu/qnnpack/buckbuild.bzl ([#169130](https://github.com/pytorch/pytorch/pull/169130))
- [reland][ROCm] remove caffe2 from hipify ([#172796](https://github.com/pytorch/pytorch/pull/172796))
- [pytorch][PR] [reland][ROCm] remove caffe2 from hipify ([#173372](https://github.com/pytorch/pytorch/pull/173372))
- [reland][ROCm] remove caffe2 from hipify ([#174087](https://github.com/pytorch/pytorch/pull/174087))
- [pytorch] redirect `fbcode//caffe2/c10:c10` to the OSS/conda version ([#169004](https://github.com/pytorch/pytorch/pull/169004))
- Rm platform compiler flags from xplat/caffe2/third_party/xnnpack.buck.bzl ([#169808](https://github.com/pytorch/pytorch/pull/169808))
- [aarch64][caffe2] Fix FBGEMM detection on aarch64 ([#169379](https://github.com/pytorch/pytorch/pull/169379))
- [codemod] Fix deprecated-literal-operator in caffe2/aten/src/ATen/native/cudnn/Conv_v7.cpp +4 ([#170329](https://github.com/pytorch/pytorch/pull/170329))
- [folly][caffe2] Remove use of `folly:molly` target ([#171711](https://github.com/pytorch/pytorch/pull/171711))
- Fix caffe2 genrules for root based genrules rollout ([#170574](https://github.com/pytorch/pytorch/pull/170574))
- [caffe2] Skip subprocess test in fbcode for D91862702 ([#174117](https://github.com/pytorch/pytorch/pull/174117))
- [caffe2] Fix signal handler deleting siginfo_t in resulting Coredump ([#174247](https://github.com/pytorch/pytorch/pull/174247))
- [caffe2][cudnn] Fix incorrect TORCH_CHECK usage in MHA.cpp ([#174885](https://github.com/pytorch/pytorch/pull/174885))
- [pytorch][caffe2] fix conditional-uninitialized warnings in Math.h ([#174904](https://github.com/pytorch/pytorch/pull/174904))
- [jit] Raise ValueError for invalid fusion strategy and add test ([#171573](https://github.com/pytorch/pytorch/pull/171573))
- [BE] remove redudant items in unordered_set/unodered_map ([#170055](https://github.com/pytorch/pytorch/pull/170055))
- [BE]: Mark more hash impls as noexcept for efficiency ([#171388](https://github.com/pytorch/pytorch/pull/171388))
- Fix typos ([#171042](https://github.com/pytorch/pytorch/pull/171042))
- [oapque obj] Clean up classes properly ([#172503](https://github.com/pytorch/pytorch/pull/172503))
- [Refactor] Remove unused code ([#172599](https://github.com/pytorch/pytorch/pull/172599))
- Better error handling in torch/csrc/jit/passes by replacing std::runtime_error with TORCH_CHECK in passes ([#165620](https://github.com/pytorch/pytorch/pull/165620))
- Remove outdated jit files ([#173015](https://github.com/pytorch/pytorch/pull/173015))
- Assert removal finish in testing and start jit ([#173959](https://github.com/pytorch/pytorch/pull/173959))

## From dynamo worksheet

### distributed (c10d)
- Fix syntax for suppression comments. ([#167088](https://github.com/pytorch/pytorch/pull/167088)) (from: dynamo, labeled `release notes: distributed (c10d)`)

### distributed (fsdp/checkpoint)
- [18/N] Use Python 3.10 typing ([#170280](https://github.com/pytorch/pytorch/pull/170280)) (from: dynamo, labeled `release notes: distributed (fsdp)`, `release notes: distributed (checkpoint)`)
- [19/N] Use Python 3.10 typing ([#170368](https://github.com/pytorch/pytorch/pull/170368)) (from: dynamo, labeled `release notes: distributed (c10d)`, `release notes: distributed (checkpoint)`)

### fx
- AOTAutograd: at runtime, specialcase saved-for-bw tensors whos version counters werent checked in eager ([#171353](https://github.com/pytorch/pytorch/pull/171353)) (from: dynamo, labeled `release notes: fx`)
- Cleanup pyrefly ignores 3 ([#171640](https://github.com/pytorch/pytorch/pull/171640)) (from: dynamo, labeled `release notes: fx`)
- hint_int -> size_hint, support size_hint in user code. ([#171944](https://github.com/pytorch/pytorch/pull/171944)) (from: dynamo, labeled `release notes: fx`)
- [BE][Ez]: Modernize symbolic shape dataclasses ([#172115](https://github.com/pytorch/pytorch/pull/172115)) (from: dynamo, labeled `release notes: fx`)
- [annotation][export] Add metadata hook for all nodes created in runtime_assert pass ([#173970](https://github.com/pytorch/pytorch/pull/173970)) (from: dynamo, labeled `release notes: fx`)

### python_frontend
- [BE][Ez]: Add slots to treespec dataclasses ([#172172](https://github.com/pytorch/pytorch/pull/172172)) (from: dynamo, labeled `release notes: python_frontend`)

### inductor
- [dynamo] Add per-graph inductor config override for debugging/bisecting ([#174228](https://github.com/pytorch/pytorch/pull/174228)) (from: dynamo, labeled `release notes: inductor`)

### export
- Support default kwargs in new export ([#173613](https://github.com/pytorch/pytorch/pull/173613)) (from: dynamo, appears to belong to export)

### xpu
- [xpu][test] Enable more Inductor UT for XPU ([#171773](https://github.com/pytorch/pytorch/pull/171773)) (from: dynamo, XPU/inductor test)

### distributed
- Fix for test/distributed/test_device_mesh.py::TestDeviceMeshGetItem::test_flatten_mesh_4d ([#172189](https://github.com/pytorch/pytorch/pull/172189)) (from: dynamo, distributed test)

### cuda/rocm
- Revert "[ROCm][CUDA] add unit test utility busy_wait_for_flag (#166218)" ([#170462](https://github.com/pytorch/pytorch/pull/170462)) (from: dynamo, CUDA/ROCm revert)

## fx (from quantization)
- Add _disable_torch_fn_metadata_mode option to make_fx and aot_export_joint_with_descriptors ([#172087](https://github.com/pytorch/pytorch/pull/172087))

## quantization (from composability)
- Remove assert in library/cuda/ao ([#170803](https://github.com/pytorch/pytorch/pull/170803))

## aotdispatcher (from functorch)
- [functorch] Add cache-friendly custom estimator/solver support ([#171601](https://github.com/pytorch/pytorch/pull/171601))
- [functorch] force save with_effects outputs in partitioner ([#172889](https://github.com/pytorch/pytorch/pull/172889))
- [functorch] support with_effects flowing through FunctionalTensorMode ([#172887](https://github.com/pytorch/pytorch/pull/172887))


## fx (from inductor)
- [opaque_obj] Add nested value-type opaque obj support ([#169845](https://github.com/pytorch/pytorch/pull/169845))

## inductor (aoti) (from inductor)
- [AOTI] Support mixed-device constants ([#169504](https://github.com/pytorch/pytorch/pull/169504))
- [hop][print]Add args print support to hop print ([#170880](https://github.com/pytorch/pytorch/pull/170880))
- [cpp_wrapper] De-duplicate some unnecessary code duplication ([#170963](https://github.com/pytorch/pytorch/pull/170963))
- [xpu][feature] Support aot_inductor.emit_multi_arch_kernel for XPU. ([#171432](https://github.com/pytorch/pytorch/pull/171432))
- [inductor] Change cpp_kernel_name to public API to match AOTI shim gen; add mm_type_out to AOTI fallback kernel  ([#174489](https://github.com/pytorch/pytorch/pull/174489))
