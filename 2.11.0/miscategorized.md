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

## distributed (dtensor) (from distributed)
- [DTensor] Refactor _select_min_cost_strategy as a util ([#170197](https://github.com/pytorch/pytorch/pull/170197))
- [DTensor][BE] remove is_backward from redistribute_local_tensor ([#170147](https://github.com/pytorch/pytorch/pull/170147))
- fix input mutation handling for subclasses (DTensor copy_) ([#170467](https://github.com/pytorch/pytorch/pull/170467))
- [DTensor] Add OpSchema.args_meta, kwargs_meta helpers ([#170358](https://github.com/pytorch/pytorch/pull/170358))
- [DTensor] ensure op_info is never None in slow path ([#170584](https://github.com/pytorch/pytorch/pull/170584))
- [DTensor] Fix OpInfo.schema type and add asserts ([#170790](https://github.com/pytorch/pytorch/pull/170790))
- [DTensor] Optimize strfmt for ExplicitRedistributionContext ([#170405](https://github.com/pytorch/pytorch/pull/170405))
- [DTensor] Hook up output tensor_meta to expand util ([#170827](https://github.com/pytorch/pytorch/pull/170827))
- [DTensor] single-dim foreach strategy ([#170631](https://github.com/pytorch/pytorch/pull/170631))
- [DTensor] LRU cachable OpStrategy ([#171223](https://github.com/pytorch/pytorch/pull/171223))
- [DTensor] fix _StridedShard(sf=) bug in single dim strategy ([#171942](https://github.com/pytorch/pytorch/pull/171942))
- Make copy_ work with more Partial placements ([#170704](https://github.com/pytorch/pytorch/pull/170704))
- [DTensor] Ban redistribute from one partial type to another ([#172041](https://github.com/pytorch/pytorch/pull/172041))
- [DTensor] Make redistribution cost for different partials infinite ([#172042](https://github.com/pytorch/pytorch/pull/172042))
- [DTensor] Handle out= ops in single-dim expander ([#172276](https://github.com/pytorch/pytorch/pull/172276))
- [DTensor] Fix incorrect Tensor Meta Population ([#172304](https://github.com/pytorch/pytorch/pull/172304))
- [DTensor] insert Replicate at beginning for matmul single dim ([#172150](https://github.com/pytorch/pytorch/pull/172150))
- [LocalTensor] support misc sym ops ([#172268](https://github.com/pytorch/pytorch/pull/172268))
- [DTensor] single_dim fix symint + _create_expanded_strategy ([#172421](https://github.com/pytorch/pytorch/pull/172421))
- DTensor Ops: Made aten.div.* linearity similar to aten.mul.* ([#172514](https://github.com/pytorch/pytorch/pull/172514))
- DTensor Ops: Add linearity support for neg operation ([#172563](https://github.com/pytorch/pytorch/pull/172563))
- Add SymInt support for DTensor mesh coordinate computation in PT2 ([#169552](https://github.com/pytorch/pytorch/pull/169552))
- [DTensor] make expand_to_full_mesh_op_strategy filter incompatible out= strategies ([#172420](https://github.com/pytorch/pytorch/pull/172420))
- [DTensor] single dim fix inplace op expansion ([#172477](https://github.com/pytorch/pytorch/pull/172477))
- [DebugMode] log DTensor output placements ([#172688](https://github.com/pytorch/pytorch/pull/172688))
- [DTensor] enable single-dim strategy for addmm and baddbmm ([#172387](https://github.com/pytorch/pytorch/pull/172387))
- [DTensor] Support uneven _StridedShard redistribution ([#172266](https://github.com/pytorch/pytorch/pull/172266))
- [DTensor] Fix single-dim output_meta validation ([#172293](https://github.com/pytorch/pytorch/pull/172293))
- [DTensor][BE] redistribute to replicate in from_local backward for partial ([#173153](https://github.com/pytorch/pytorch/pull/173153))
- [DTensor] no-op redistribution shouldn't create _TransformInfo ([#172924](https://github.com/pytorch/pytorch/pull/172924))
- [DTensor] single-dim strategy validation infra ([#172990](https://github.com/pytorch/pytorch/pull/172990))
- [DTensor] fix redistribute cost crashing on non-participating ranks ([#172478](https://github.com/pytorch/pytorch/pull/172478))
- [DTensor] S->P(sum) strategy for _powsum ([#172604](https://github.com/pytorch/pytorch/pull/172604))
- [DTensor] Make RedistributionPlanner handle all partials ([#172479](https://github.com/pytorch/pytorch/pull/172479))
- [DTensor] single-dim expander raises clear inplace error ([#173572](https://github.com/pytorch/pytorch/pull/173572))
- [DTensor] Update TP api to support single-dim strategies ([#173567](https://github.com/pytorch/pytorch/pull/173567))
- [DTensor] Fix t() sharding strategy for 1D tensors ([#173964](https://github.com/pytorch/pytorch/pull/173964))
- [DTensor] initial support for decomps + sharding prop ([#171652](https://github.com/pytorch/pytorch/pull/171652))
- [DTensor] Fix unsupported op error ([#170889](https://github.com/pytorch/pytorch/pull/170889))
- [DTensor] add shard prop cache logging ([#173775](https://github.com/pytorch/pytorch/pull/173775))
- [DTensor RNG][BC Breaking] Change DTensor Philox seed and offset from int to tensor ([#173876](https://github.com/pytorch/pytorch/pull/173876))
- [DTensor] infer RuntimeSchemaInfo for decomposition ops ([#174422](https://github.com/pytorch/pytorch/pull/174422))
- fix DTensor honor single-dim RuntimeSchemaInfo ([#174312](https://github.com/pytorch/pytorch/pull/174312))
- [DTensor] Fix device_mesh extraction from kwargs ([#173489](https://github.com/pytorch/pytorch/pull/173489))
- [DTensor] Optimize redistribute comms using flattened meshes ([#174630](https://github.com/pytorch/pytorch/pull/174630))
- [DTensor] set static args for decomp OpSchema ([#174616](https://github.com/pytorch/pytorch/pull/174616))
- [DTensor] Fix StridedShard usage conflict with shard order ([#174831](https://github.com/pytorch/pytorch/pull/174831))
- [DTensor] Fix bucketize with Partial inputs ([#173937](https://github.com/pytorch/pytorch/pull/173937))
- [DTensor] Strategy Validation: placement utilities and data structures ([#174798](https://github.com/pytorch/pytorch/pull/174798))
- [DTensor] Fix embedding_dense_backward cache key missing num_weights ([#174727](https://github.com/pytorch/pytorch/pull/174727))
- [DTensor] skip decomposition for CIA ops ([#174918](https://github.com/pytorch/pytorch/pull/174918))
- Reapply "[DTensor] Refactor strategy/rule registration into dedicated module (#168221)" (a695f3cbd3c)

## distributed (checkpoint) (from distributed)
- Optimize checkpoint resharding with sweep-line algorithm ([#169115](https://github.com/pytorch/pytorch/pull/169115))
- Cleanup unused ignores 2 ([#171639](https://github.com/pytorch/pytorch/pull/171639))
- Fix TypedStorage deprecation warning in distributed checkpoint ([#170759](https://github.com/pytorch/pytorch/pull/170759))
- Fix typo in variable name from 'statetful_sd' to 'stateful_sd' ([#171292](https://github.com/pytorch/pytorch/pull/171292))
- Write metadata file for Consolidate hf safetensors file on every rank ([#171885](https://github.com/pytorch/pytorch/pull/171885))

## distributed (symm_mem) (from distributed)
- NCCL device comm manager ([#170544](https://github.com/pytorch/pytorch/pull/170544))
- Improve header dependency re nccl_device support ([#170634](https://github.com/pytorch/pytorch/pull/170634))

## distributed (fsdp2) (from distributed)
- Share more code between replicate and fully_shard ([#173580](https://github.com/pytorch/pytorch/pull/173580))
- Fix mixed DTensor error with nested FSDP and activation checkpoint ([#171779](https://github.com/pytorch/pytorch/pull/171779))
- Consolidate shard_mesh and shard_mesh_from_root ([#174107](https://github.com/pytorch/pytorch/pull/174107))

## distributed (torchelastic) (from distributed)
- Improve NUMA binding docs ([#171543](https://github.com/pytorch/pytorch/pull/171543))

## nn (from distributed)
- Remove outdated CUDA code ([#170357](https://github.com/pytorch/pytorch/pull/170357))

## quantization (from distributed)
- Apply various ruff fixes ([#170968](https://github.com/pytorch/pytorch/pull/170968))

## python_frontend (from distributed)
- Add typing utils to copy signatures from methods or signatures ([#163418](https://github.com/pytorch/pytorch/pull/163418))
