
# Release Notes worksheet distributed

You should:

1. ensure commit categorization is correct
2. write up major features, bc-breaking changes, deprecations in detail
3. summarize the other sections

## 1. Ensure commit categorization is correct

* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.

The categories below are as follows:

* BC breaking: All commits that are BC-breaking. These are the most important commits. If any pre-sorted commit is actually BC-breaking, do move it to this section. Each commit should contain a paragraph explaining the rational behind the change as well as an example for how to update user code [BC-Guidelines](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit#heading=h.a9htwgvvec1m).
* Deprecations: All commits introducing deprecation. Each commit should include a small example explaining what should be done to update user code.
* new_features: All commits introducing a new feature (new functions, new submodule, new supported platform etc)
* improvements: All commits providing improvements to existing feature should be here (new backend for a function, new argument, better numerical stability)
* bug fixes: All commits that fix bugs and behaviors that do not match the documentation
* performance: All commits that are added mainly for performance (we separate this from improvements above to make it easier for users to look for it)
* documentation: All commits that add/update documentation
* Developers: All commits that are not end-user facing but still impact people that compile from source, develop into pytorch, extend pytorch, etc
* not user facing: All commits that are not public end-user facing and hence should be dropped from the release notes

## 2. Major features, BC-breaking changes, deprecations

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.

## 3. Summarize the other sections

For the other sections (improvements, bug fixes, performance, documentation, developers, not user facing) - use your
judgement to summarize the key PRs. You do not need to make every commit description perfect
(changed in v2.10 to simplify the process).

Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

Feel free to use https://github.com/pytorch/pytorch/releases/tag/v2.10.0 as an example.

## distributed
### bc breaking
### deprecation
### new features
### improvements
- [c10d] [PERFORMANCE] Improve performance for `AsyncMM.cu` by avoiding redundant IO/compute via indicating that indicating that `ElementC` type is void ([#178653](https://github.com/pytorch/pytorch/pull/178653))
### bug fixes
- [fix] coalescing_manager not passing Opts to allgather_into_tensor_coalesced() ([#175379](https://github.com/pytorch/pytorch/pull/175379))
- [fix] raise exception from _CoalescingManager when the ops in list are not the same ([#175573](https://github.com/pytorch/pytorch/pull/175573))
- Implement missing methods in `ProcessGroupWrapper` ([#178779](https://github.com/pytorch/pytorch/pull/178779))
### performance
### docs
### devs
- [c10d] add profiling name to NCCL collective ([#173837](https://github.com/pytorch/pytorch/pull/173837))
- [c10d] add profiling name to NCCL collective ([#173837](https://github.com/pytorch/pytorch/pull/173837))
- [c10d] add profiling name to NCCL collective ([#173837](https://github.com/pytorch/pytorch/pull/173837))
### Untopiced
- [DTensor] prims ops sharding strategies ([#174442](https://github.com/pytorch/pytorch/pull/174442))
- [DTensor] fix stack dim normalization ([#174640](https://github.com/pytorch/pytorch/pull/174640))
- [DTensor] Strategy Validation (3/3): strategy querying, orchestrator, and CLI ([#174800](https://github.com/pytorch/pytorch/pull/174800))
- Fix USE_RCOM typo to USE_ROCM in intra_node_comm.cpp ([#175078](https://github.com/pytorch/pytorch/pull/175078))
- [DTensor] single dim bucketize rule supporting sharded buckets ([#174830](https://github.com/pytorch/pytorch/pull/174830))
- move getenv to main thread, to avoid getenv,setenv race + segfault ([#167523](https://github.com/pytorch/pytorch/pull/167523))
- [DTensor] Strategy Validation (4/4): Multi-output ops ([#174995](https://github.com/pytorch/pytorch/pull/174995))
- Fix hpu backend mapping issue - alternate ([#174764](https://github.com/pytorch/pytorch/pull/174764))
- [reland] c10d: convert NanCheck to an op + tests (#174736) ([#174990](https://github.com/pytorch/pytorch/pull/174990))
- Add Store::barrier API and TCPStore client BARRIER support to reduce sync round trips ([#174920](https://github.com/pytorch/pytorch/pull/174920))
- [DTensor] expand_to_full_mesh_op_strategy filters mixed partials ([#173614](https://github.com/pytorch/pytorch/pull/173614))
- [DTensor] Fix view_as_complex with P(max)/P(min) placements ([#173935](https://github.com/pytorch/pytorch/pull/173935))
- Remove unused suppressions in torch/distributed ([#175257](https://github.com/pytorch/pytorch/pull/175257))
- [DTensor] cache DecompStrategy and fake mesh ([#175205](https://github.com/pytorch/pytorch/pull/175205))
- Fix DTensor get_mesh_from_args when first arg is not a tensor ([#169265](https://github.com/pytorch/pytorch/pull/169265))
- [TorchDistributed] Add signal name to ChildFailedError exitcode output ([#175254](https://github.com/pytorch/pytorch/pull/175254))
- [DTensor] lenient handling of view redistributes in decomposition flow ([#175194](https://github.com/pytorch/pytorch/pull/175194))
- torchcomms fr debug server integration ([#175270](https://github.com/pytorch/pytorch/pull/175270))
- [FSDP2] allow ModuleList/ModuleDict subclasses that implement forward() ([#175033](https://github.com/pytorch/pytorch/pull/175033))
- [HOP][print]Add Dtensor support ([#175222](https://github.com/pytorch/pytorch/pull/175222))
- Capture async flag of collectives in PyTorch execution trace ([#169416](https://github.com/pytorch/pytorch/pull/169416))
- [DDP] Refactor bucket capacity config into BucketCapacityConfig dataclass ([#175217](https://github.com/pytorch/pytorch/pull/175217))
- add fr hook on torchcomm ([#175561](https://github.com/pytorch/pytorch/pull/175561))
- [PGNCCL] check terminate signal more frequently when exiting from heartbeat monitor ([#170000](https://github.com/pytorch/pytorch/pull/170000))
- [distributed][rpc][cuda] Fix race condition in test_tensor_view_as_return_value ([#175529](https://github.com/pytorch/pytorch/pull/175529))
- [BE]SymMem: Better CUDA hygiene ([#175616](https://github.com/pytorch/pytorch/pull/175616))
- document public APIs using a Claude Skill ([#175578](https://github.com/pytorch/pytorch/pull/175578))
- [DTensor] Improve strategy validator denoising for Partial inputs ([#175265](https://github.com/pytorch/pytorch/pull/175265))
- [DTensor] Replace prop_index_put with single_dim_strategy ([#172894](https://github.com/pytorch/pytorch/pull/172894))
- [torchrun] Default to free port for single-node training ([#175699](https://github.com/pytorch/pytorch/pull/175699))
- fix: stage_backward_weight with multi-output intermediate ([#175705](https://github.com/pytorch/pytorch/pull/175705))
- [DTensor] layernorm output meta ([#175652](https://github.com/pytorch/pytorch/pull/175652))
- Add reduce_scatter_tensor_coalesced support to ProcessGroupWrapper ([#168961](https://github.com/pytorch/pytorch/pull/168961))
- [DTensor] Add _PreparedSingleDimStrategy ([#175462](https://github.com/pytorch/pytorch/pull/175462))
- [DTensor] roll/fft sharding strategies ([#175463](https://github.com/pytorch/pytorch/pull/175463))
- [DTensor] strategy_validation report if no dtensor support exists ([#175589](https://github.com/pytorch/pytorch/pull/175589))
- Optimize DCP consolidation I/O for remote mounts ([#175762](https://github.com/pytorch/pytorch/pull/175762))
- [DTensor] Report strategy_validation results per aten op variant ([#175892](https://github.com/pytorch/pytorch/pull/175892))
- [DTensor] Add grad_placement to from_local ([#175867](https://github.com/pytorch/pytorch/pull/175867))
- [DTensor] Strategy Validation fix for non-tensor args ([#175821](https://github.com/pytorch/pytorch/pull/175821))
- fix to two forward pass of ddp wrapped batch norm raising error ([#175851](https://github.com/pytorch/pytorch/pull/175851))
- [DISTRIBUTED] Use () for tuple() for slightly improved performance ([#175492](https://github.com/pytorch/pytorch/pull/175492))
- [DTensor] Extract monotonic increasing unary ops from pointwise_ops ([#175685](https://github.com/pytorch/pytorch/pull/175685))
- [DTensor] Extract monotonic decreasing unary ops from pointwise_ops ([#175686](https://github.com/pytorch/pytorch/pull/175686))
- Fix flaky DTensor sharding prop cache logging test ([#176119](https://github.com/pytorch/pytorch/pull/176119))
- [FSDP2]: remove compiled autograd since we are not tracing into hooks ([#174906](https://github.com/pytorch/pytorch/pull/174906))
- Improving DTensor performance for torch.cat ([#174879](https://github.com/pytorch/pytorch/pull/174879))
- [DTensor] Extract monotonic binary ops and non_decreasing_linear_unary ops from pointwise_ops ([#175687](https://github.com/pytorch/pytorch/pull/175687))
- [DTensor] add linearity rule to gen_single_dim_einsum_strategies ([#176150](https://github.com/pytorch/pytorch/pull/176150))
- [DTensor] index_select single-dim strategy ([#176037](https://github.com/pytorch/pytorch/pull/176037))
- [FSDP2] support dataclass args/kwargs output without memory leakage ([#174692](https://github.com/pytorch/pytorch/pull/174692))
- Improving DTensor performance for pytree ops ([#174879](https://github.com/pytorch/pytorch/pull/174879))
- [DTensor] report registered ops ([#176034](https://github.com/pytorch/pytorch/pull/176034))
- [DTensor] Auto-append output placement for .out variant ops ([#175960](https://github.com/pytorch/pytorch/pull/175960))
- [DTensor] constant_pad_nd non-replicate strategy ([#175656](https://github.com/pytorch/pytorch/pull/175656))
- Fix: Makes worker shutdown timeout configurable in torchrun ([#172596](https://github.com/pytorch/pytorch/pull/172596))
- [Pipeline Parallel] Dispatch homogeneous P2P ops individually to avoid stream serialization ([#175712](https://github.com/pytorch/pytorch/pull/175712))
- dist.broadcast for fp8 on <sm90 ([#175884](https://github.com/pytorch/pytorch/pull/175884))
- [dcp] Fix save plan caching bug during validation failures ([#176289](https://github.com/pytorch/pytorch/pull/176289))
- [SymmMem] Use host API to get NCCL peer pointer ([#176570](https://github.com/pytorch/pytorch/pull/176570))
- [DTensor] unbacked-safe view_groups ([#174629](https://github.com/pytorch/pytorch/pull/174629))
- [dtensor] Fix tp_conv rejecting batch-dim-only sharding for valid configs ([#176448](https://github.com/pytorch/pytorch/pull/176448))
- [DTensor] skip zero-numel outputs for strategy validator ([#176020](https://github.com/pytorch/pytorch/pull/176020))
- [DTensor] Add Dijkstra-based single-dim strategy search ([#169438](https://github.com/pytorch/pytorch/pull/169438))
- [SymmMem] Add thread safety to NCCL and NVSHMEM backends ([#176551](https://github.com/pytorch/pytorch/pull/176551))
- [aps]Start the TW health check thrift server before rendezvous ([#176576](https://github.com/pytorch/pytorch/pull/176576))
- [SymmMem] Improve tensor-to-allocation lookup in NCCL Symmetric Memory ([#176744](https://github.com/pytorch/pytorch/pull/176744))
- Add torch function handlers for distributed functions ([#176376](https://github.com/pytorch/pytorch/pull/176376))
- Split _BackendWrapper import to torchcomms._backend_wrapper module ([#177157](https://github.com/pytorch/pytorch/pull/177157))
- [dcp] Update save plan validation error messaging ([#176728](https://github.com/pytorch/pytorch/pull/176728))
- [DTensor] Fix Dijkstra sharding search: shardability checks and graceful fallback ([#177167](https://github.com/pytorch/pytorch/pull/177167))
- [DTensor] Validate Dijkstra match feasibility with redistribute_cost ([#177168](https://github.com/pytorch/pytorch/pull/177168))
- [DTensor] Fix compute_local_stride for unevenly-sharded tensors ([#177174](https://github.com/pytorch/pytorch/pull/177174))
- [PT2 Bug Bash] Hard error and deprecate torch.distributed.nn.functional under torch.compile ([#177342](https://github.com/pytorch/pytorch/pull/177342))
- [DTensor] fix scaled_mm sharding strategy ([#177234](https://github.com/pytorch/pytorch/pull/177234))
- Add NCCL collective sequence number (seq_num) to Kineto profiler traces ([#177148](https://github.com/pytorch/pytorch/pull/177148))
- [DTensor] handle is_pinned() ([#177235](https://github.com/pytorch/pytorch/pull/177235))
- [dynamo ] Enabling batch_isend_irecv to compile ([#161213](https://github.com/pytorch/pytorch/pull/161213))
- [distributed] Add configurable worker timeout and partial data support to debug server ([#176058](https://github.com/pytorch/pytorch/pull/176058))
- [SymmMem] Fix NCCLPeerAllocInfo destructor: deregister windows and free resources ([#177459](https://github.com/pytorch/pytorch/pull/177459))
- [SymmMem] Avoid two probes when inserting handle into cache ([#177463](https://github.com/pytorch/pytorch/pull/177463))
- Refactor `NCCLDevCommManager`: Improve API design; do not create devComm by default ([#177380](https://github.com/pytorch/pytorch/pull/177380))
- [ROCm] intra_node_comm: use amdsmi instead of rocmsmi ([#176506](https://github.com/pytorch/pytorch/pull/176506))
- [DTensor] Skip unnecessary all-reduce of total_weight in DTensor nll_loss_backward for reduction='sum' ([#177233](https://github.com/pytorch/pytorch/pull/177233))
- [ROCm] Enable cpp/c10d UTs ([#169063](https://github.com/pytorch/pytorch/pull/169063))
- [shard prop] linalg ops strategies ([#176955](https://github.com/pytorch/pytorch/pull/176955))
- Add NCCL comm suspend, resume and memory stats ([#176300](https://github.com/pytorch/pytorch/pull/176300))
- [DDP] Add batched grad-to-bucket copy optimization (#176638) ([#176638](https://github.com/pytorch/pytorch/pull/176638))
- [DTensor] index single-dim strategy ([#176038](https://github.com/pytorch/pytorch/pull/176038))
- [fully_shard][DTensor] Support fully_shard with DTensor on full SPMD mesh ([#176334](https://github.com/pytorch/pytorch/pull/176334))
- [DCP] Fix unpicklable FrameSummary._code on Python 3.13+ (#177754) ([#177754](https://github.com/pytorch/pytorch/pull/177754))
- [dtensor-compile] Emit zero paddings for uneven shardings to get SPMD ([#177758](https://github.com/pytorch/pytorch/pull/177758))
- Make run_dtensor_rng_op compatible with compile_on_one_rank ([#177447](https://github.com/pytorch/pytorch/pull/177447))
- [ROCm] Reland: Enable expandable segments (#173330) ([#177974](https://github.com/pytorch/pytorch/pull/177974))
- [dcp][oss] Fix Metadata.storage_meta regression from dataclasses.replace() (#178001) ([#178001](https://github.com/pytorch/pytorch/pull/178001))
- [DTensor] Add sharding strategy for aten.squeeze.dims ([#173563](https://github.com/pytorch/pytorch/pull/173563))
- [dtensor] Add single_dim_strategy infrastructure for foreach/fused ops ([#177186](https://github.com/pytorch/pytorch/pull/177186))
- [dtensor] Register foreach and fused ops via single_dim_strategy ([#177187](https://github.com/pytorch/pytorch/pull/177187))
- [DCP] Preserve original exception in metadata read failure for better debuggability (#177739) ([#177739](https://github.com/pytorch/pytorch/pull/177739))
- [CP] Improve head tail load balancer indices creation performance ([#178199](https://github.com/pytorch/pytorch/pull/178199))
- [torchelastic] Keep health check alive during exit barrier ([#178197](https://github.com/pytorch/pytorch/pull/178197))
- [c10d] Remove contiguous assertions from functional collectives API ([#177965](https://github.com/pytorch/pytorch/pull/177965))
- [DTensor] Fix double-shard validation in propagate_shape_and_sharding  ([#177973](https://github.com/pytorch/pytorch/pull/177973))
- [DTensor] support DTensor view (flatten/unflatten) with _StridedSharding ([#166483](https://github.com/pytorch/pytorch/pull/166483))
- Enable split_group API when TorchComms is used as a backend for TorchTitan on XPU ([#178236](https://github.com/pytorch/pytorch/pull/178236))
- make pyspy dumps nonblocking by default ([#178312](https://github.com/pytorch/pytorch/pull/178312))
- torchcomms: use either import path for _BackendWrapper ([#178352](https://github.com/pytorch/pytorch/pull/178352))
- [fix] put strided shard in safe globals ([#178560](https://github.com/pytorch/pytorch/pull/178560))
- Fix HSDP sync_module_states broadcast order for buffers ([#178569](https://github.com/pytorch/pytorch/pull/178569))
- [SymmetricMemory] Add RECORD_PARAM_COMMS to symmetric memory CUDA ops for PG metadata in profiler traces (#178571) ([#178571](https://github.com/pytorch/pytorch/pull/178571))
- [coor] Add _dtensor::mesh_get_process_group custom op ([#178116](https://github.com/pytorch/pytorch/pull/178116))
- [shard prop] default sharding validator to 1-1 OpInfo-aten entries ([#177595](https://github.com/pytorch/pytorch/pull/177595))
- [torch] add timeout to distributed barrier (#174974) ([#174974](https://github.com/pytorch/pytorch/pull/174974))
- allow torchcomms operations in flight recorder ([#178359](https://github.com/pytorch/pytorch/pull/178359))
- [SymmMem] add `reduce_scatter_offset` ([#177791](https://github.com/pytorch/pytorch/pull/177791))
- Add CUDA-aware detection for Cray MPICH ([#178323](https://github.com/pytorch/pytorch/pull/178323))
- [DTensor] Add InputDim.__eq__ type guard to prevent int comparison bugs ([#178599](https://github.com/pytorch/pytorch/pull/178599))
- [Distributed] 88245 Add all to all support in Gloo backend ([#165435](https://github.com/pytorch/pytorch/pull/165435))
- Add custom op for flattened submesh lookup during compile_on_one_rank tracing ([#178889](https://github.com/pytorch/pytorch/pull/178889))
- Add reconstruct_fn to opaque type registration for make_fx tracing ([#178970](https://github.com/pytorch/pytorch/pull/178970))
- Fix DTensor backward for value-selecting reductions (topk, sort, min,… ([#178668](https://github.com/pytorch/pytorch/pull/178668))
- add API to check if a tensor is symm-mem-tensor ([#178947](https://github.com/pytorch/pytorch/pull/178947))
- [DTensor] redistribute from/to _StridedShard through Replicate ([#179059](https://github.com/pytorch/pytorch/pull/179059))
- [dtensor][pointwise_ops] removing dead code ([#178975](https://github.com/pytorch/pytorch/pull/178975))
- Fix Potential Infinite Loop in FlightRecorder When Multiple PGs are Running into Barrier ([#179449](https://github.com/pytorch/pytorch/pull/179449))
- Fix AC crash when passing BlockMask as argument ([#179215](https://github.com/pytorch/pytorch/pull/179215))
- [DTensor] Fix precision loss in NestedRedistribute backward dtype handling ([#179495](https://github.com/pytorch/pytorch/pull/179495))
- [dtensor][index_ops] adding index_fill and index_reduce strategies ([#178456](https://github.com/pytorch/pytorch/pull/178456))
- [symm_mem] Improve error message on symmetric memory handle exchange ([#178989](https://github.com/pytorch/pytorch/pull/178989))
- [torchelastic] Start health check server before MAST rendezvous in launch_agent (#179560) ([#179560](https://github.com/pytorch/pytorch/pull/179560))
- [DTensor] Raise error for unsupported Split(Flatten) sharding propagation ([#179632](https://github.com/pytorch/pytorch/pull/179632))
- [shard prop] interpolate ([#176991](https://github.com/pytorch/pytorch/pull/176991))
- [DTensor] Fix index_put sharding strategy for None indices ([#179217](https://github.com/pytorch/pytorch/pull/179217))
- [shard prop] single-dim rules for LayerNorm, RMSNorm FW/BW ([#179173](https://github.com/pytorch/pytorch/pull/179173))
- [FSDP2] Cache shard_mesh to avoid repeated _create_sub_mesh calls (#179655) ([#179655](https://github.com/pytorch/pytorch/pull/179655))
- [PP][1/3] DTensor metadata foundation for Pipeline Parallelism ([#177727](https://github.com/pytorch/pytorch/pull/177727))
- [PP][2/3] DTensor-aware stage and schedule refactoring ([#177728](https://github.com/pytorch/pytorch/pull/177728))
- [SymmMem] Unify symmetric memory key and map types across backends ([#179903](https://github.com/pytorch/pytorch/pull/179903))
- Unwrap AsyncCollectiveTensor inputs before AOT autograd tracing and at runtime ([#179849](https://github.com/pytorch/pytorch/pull/179849))
- [CUDA][Mempool] use allocation-time counter instead of address for Block ordering to fix NCCL symmetric memory mismatch ([#178362](https://github.com/pytorch/pytorch/pull/178362))
- [FR] Add ncclx and gloo to FlightRecorder trace analyzer backend allowlist (#180268) ([#180268](https://github.com/pytorch/pytorch/pull/180268))
- [pytorch] address violations of warning unreachable-code-return (v2) (#179518) ([#179518](https://github.com/pytorch/pytorch/pull/179518))
### not user facing
- test_matrix_ops.py: Add skip_if_lt_x_gpu(4) for test_mm_with_strided_input ([#175105](https://github.com/pytorch/pytorch/pull/175105))
- patch .comms attribute for ThreadLocalWorld warnings ([#175099](https://github.com/pytorch/pytorch/pull/175099))
- [Dist][CI] fix distributed timeout ([#175030](https://github.com/pytorch/pytorch/pull/175030))
- [TEST][FP8] Add proper skips for FP8 on sm < 89 ([#170528](https://github.com/pytorch/pytorch/pull/170528))
- [bucketing] Fix cross type bucketing ([#175150](https://github.com/pytorch/pytorch/pull/175150))
- [DTensor] organize OpInfo xfails ([#175234](https://github.com/pytorch/pytorch/pull/175234))
- Add compute_estimator option for overlap scheduling ([#175204](https://github.com/pytorch/pytorch/pull/175204))
- [DTensor] End to end test for strategy validator ([#175588](https://github.com/pytorch/pytorch/pull/175588))
- [BE] Apply PEP 604 type annotations to torch/testing ([#175925](https://github.com/pytorch/pytorch/pull/175925))
- Additionally disable proxy tensor in DeviceMesh.__getitem__ ([#176007](https://github.com/pytorch/pytorch/pull/176007))
- Fix flaky test_extra_collectives by disabling shape padding ([#176137](https://github.com/pytorch/pytorch/pull/176137))
- Use correct head dim for XPU SDPA tests ([#175540](https://github.com/pytorch/pytorch/pull/175540))
- [opaque obj] Fix sourceless tracing issue ([#176236](https://github.com/pytorch/pytorch/pull/176236))
- Fix test interaction: clean up DTensorSpec pytree registration ([#176128](https://github.com/pytorch/pytorch/pull/176128))
- [BE] Apply up007 and up045 to torch/backends through torch/futures ([#176311](https://github.com/pytorch/pytorch/pull/176311))
- Revert #169867 ([#176485](https://github.com/pytorch/pytorch/pull/176485))
- [Test Infra] Fix MultiProcContinuousTest completion queue desync ([#176259](https://github.com/pytorch/pytorch/pull/176259))
- [BE] Apply up007 and up045 to test ([#176462](https://github.com/pytorch/pytorch/pull/176462))
- [FSDP2][docs] Document communication grouping and scheduling semantics ([#176318](https://github.com/pytorch/pytorch/pull/176318))
- [ROCm] Check for atleast one compilation for each rank ([#175849](https://github.com/pytorch/pytorch/pull/175849))
- [device_mesh] Fix inverted condition in `_unflatten` string dim validation ([#176563](https://github.com/pytorch/pytorch/pull/176563))
- [Bugfix] Fix failing test from annotation failure ([#176887](https://github.com/pytorch/pytorch/pull/176887))
- Reland "Make DeviceMesh Opaque" ([#176661](https://github.com/pytorch/pytorch/pull/176661))
- Skip 4-GPU distributed tests on 2-GPU runners ([#176924](https://github.com/pytorch/pytorch/pull/176924))
- Fix the BucketMode (#175886) ([#175886](https://github.com/pytorch/pytorch/pull/175886))
- [overlap] extract runtime_estimations from OverlapScheduler ([#175174](https://github.com/pytorch/pytorch/pull/175174))
- [OpenReg][distributed] Add OCCL ProcessGroup stub validation + distributed smoke tests ([#171250](https://github.com/pytorch/pytorch/pull/171250))
- [ROCm] Skip elastic multiprocessing test_function_raise ([#177742](https://github.com/pytorch/pytorch/pull/177742))
- [DTensor] Fix test_comm_mode_with_dtensor for Dijkstra sharding propagation ([#177798](https://github.com/pytorch/pytorch/pull/177798))
- Remove redundant inline_inbuilt_nn_modules=True patches from tests ([#177971](https://github.com/pytorch/pytorch/pull/177971))
- Delete tests that explicitly set inline_inbuilt_nn_modules=False ([#177979](https://github.com/pytorch/pytorch/pull/177979))
- [FR script] Fixed bug which caused FR script to fail in the case of a coalsced collective not scheduled (#177076) ([#177076](https://github.com/pytorch/pytorch/pull/177076))
- [coor] Fix DeviceMesh _sym_get_coordinate crash and register __ne__ for opaque types ([#178110](https://github.com/pytorch/pytorch/pull/178110))
- [DTensor] Add unflatten tests for multi-mesh sharding in view ops ([#176151](https://github.com/pytorch/pytorch/pull/176151))
- [DTensor] Fix None IValue == DTensorSpec, cache key collision, and move op_strategy_context ([#178442](https://github.com/pytorch/pytorch/pull/178442))
- [overlap] fix extra deps mapping and cycles after bucketing ([#177688](https://github.com/pytorch/pytorch/pull/177688))
- Fix nested DDP causing _active_ddp_module cleared by inner _inside_ddp_module() (#178364) ([#178364](https://github.com/pytorch/pytorch/pull/178364))
- [ROCm][UT] Remove ROCm skips after upstream Triton 3.7 pin update ([#178450](https://github.com/pytorch/pytorch/pull/178450))
- [2/N] Use torch._utils.cpu_count ([#178743](https://github.com/pytorch/pytorch/pull/178743))
- Avoid multiprocess tests hanging forever. ([#171972](https://github.com/pytorch/pytorch/pull/171972))
- [OSDC][1/n] Update pull test cases to support OSDC k8s migration ([#178738](https://github.com/pytorch/pytorch/pull/178738))
- [c10d] Remove static from barrier tensor variable ([#178896](https://github.com/pytorch/pytorch/pull/178896))
- [reland] Slicing with backed should produce backed output when possible (#178899) ([#178899](https://github.com/pytorch/pytorch/pull/178899))
- Replace erase idiom for map/set with erase_if ([#179373](https://github.com/pytorch/pytorch/pull/179373))
- [test] Fix env var leak in NCCLTraceTestBase causing named pipe errors ([#179557](https://github.com/pytorch/pytorch/pull/179557))
- [bucketing] Extract bucket_mode from all passes to inductor config ([#175877](https://github.com/pytorch/pytorch/pull/175877))
- [bucketing] Add "coalesced" bucket_mode for zero-copy reduce_scatter bucketing ([#177132](https://github.com/pytorch/pytorch/pull/177132))
### security
