
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
- Honor $XDG_CACHE_HOME in C++ code of DebugInfoWriter ([#168232](https://github.com/pytorch/pytorch/pull/168232))
### deprecation
### new features
- Differentiability Support for Functional Collectives ([#168140](https://github.com/pytorch/pytorch/pull/168140))
- Differentiability Support for Functional Collectives ([#168140](https://github.com/pytorch/pytorch/pull/168140))
- Add start_method option to torch.distributed.debug.start_debug_server to support spawn/forkserver ([#173196](https://github.com/pytorch/pytorch/pull/173196))
### improvements
### bug fixes
- Add half precision binding for MPI backend ([#170074](https://github.com/pytorch/pytorch/pull/170074))
### performance
### docs
### devs
### Untopiced
- [Fix] Fix incorrect boolean logic in std::string::find method ([#170057](https://github.com/pytorch/pytorch/pull/170057))
- [Gloo] Set thread name for gloo internal loop ([#169979](https://github.com/pytorch/pytorch/pull/169979))
- [DTensor] Refactor _select_min_cost_strategy as a util ([#170197](https://github.com/pytorch/pytorch/pull/170197))
- [DTensor][BE] remove is_backward from redistribute_local_tensor ([#170147](https://github.com/pytorch/pytorch/pull/170147))
- [c10d] Fix _set_pg_timeout not working for Gloo backend ([#167052](https://github.com/pytorch/pytorch/pull/167052))
- [DeviceMesh] Fix a corner case for coalesce in cute layout and mesh slicing ([#169454](https://github.com/pytorch/pytorch/pull/169454))
- fix input mutation handling for subclasses that perform intermediate compute during copy_ (DTensor) ([#170467](https://github.com/pytorch/pytorch/pull/170467))
- [DTensor] Add OpSchema.args_meta, kwargs_meta helpers ([#170358](https://github.com/pytorch/pytorch/pull/170358))
- [CP] Make context_parallel_shard more general ([#170200](https://github.com/pytorch/pytorch/pull/170200))
- [CP] Fix the flex_input_fn argument unwrapping issue ([#170201](https://github.com/pytorch/pytorch/pull/170201))
- [Symmetric memory] Polish NCCL symm mem code ([#170582](https://github.com/pytorch/pytorch/pull/170582))
- [FSDP] Fix _unshard() passing Stream instead of Event ([#170525](https://github.com/pytorch/pytorch/pull/170525))
- [SymmMem] NCCL device comm manager ([#170544](https://github.com/pytorch/pytorch/pull/170544))
- [SymmMem] Improve header dependency re nccl_device support ([#170634](https://github.com/pytorch/pytorch/pull/170634))
- use fusion regions in overlapping ([#170560](https://github.com/pytorch/pytorch/pull/170560))
- Reapply "[DTensor] Refactor strategy/rule registration into dedicated module (#168221)" (a695f3cbd3c)
- Ensure that threadblock size to be larger or equal to the world size in CUDA Symmetric Memory barrier ([#170785](https://github.com/pytorch/pytorch/pull/170785))
- [DTensor] ensure op_info is never None in _dispatch_get_local_results_slow_path ([#170584](https://github.com/pytorch/pytorch/pull/170584))
- [DTensor] Fix OpInfo.schema type and add asserts ([#170790](https://github.com/pytorch/pytorch/pull/170790))
- [2/N] Remove outdated CUDA code ([#170357](https://github.com/pytorch/pytorch/pull/170357))
- ProcessGroupGloo: fix CUDA tensor stream handling with futures ([#170812](https://github.com/pytorch/pytorch/pull/170812))
- [DTensor] Optimize strfmt for ExplicitRedistributionContext ([#170405](https://github.com/pytorch/pytorch/pull/170405))
- [DTensor] Hook up output tensor_meta to expand util ([#170827](https://github.com/pytorch/pytorch/pull/170827))
- [BE] Simplify _ComputationType ([#170799](https://github.com/pytorch/pytorch/pull/170799))
- c10d/ProcessGroupNCCL: reduce_scatter world_size=1 work around ([#170922](https://github.com/pytorch/pytorch/pull/170922))
- Fix env variable to retrieve HCA list for NVSHMEM from ([#170891](https://github.com/pytorch/pytorch/pull/170891))
- [Distributed] Optimize checkpoint resharding with sweep-line algorithm ([#169115](https://github.com/pytorch/pytorch/pull/169115))
- [DTensor] single-dim foreach strategy ([#170631](https://github.com/pytorch/pytorch/pull/170631))
- [PP] refactor ([#170804](https://github.com/pytorch/pytorch/pull/170804))
- Apply various ruff fixes ([#170968](https://github.com/pytorch/pytorch/pull/170968))
- [small] fix assert double negatives ([#171142](https://github.com/pytorch/pytorch/pull/171142))
- [ncclx] Set group desc before creating nccl comm so that desc gets propagated ([#171159](https://github.com/pytorch/pytorch/pull/171159))
- ensure meta impls for nonfunctional collectives are registered on import torch; support nonfunctional collectives with FakeTensor ([#162119](https://github.com/pytorch/pytorch/pull/162119))
- [fsdp2] fix split_with_sizes_copy() missing argument: 'dim' ([#169173](https://github.com/pytorch/pytorch/pull/169173))
- Remove old CUDA conditions ([#171235](https://github.com/pytorch/pytorch/pull/171235))
- Cleanup unused ignores 2 ([#171639](https://github.com/pytorch/pytorch/pull/171639))
- [CUDA][Mempool] Sort mempool registrations via allocation-time counter ([#167662](https://github.com/pytorch/pytorch/pull/167662))
- module load fix ([#171750](https://github.com/pytorch/pytorch/pull/171750))
- [c10d] Fix USE_NCCL=0 build failure in nccl_dev_cap.hpp ([#171694](https://github.com/pytorch/pytorch/pull/171694))
- Use enum.member starting in version 3.11 ([#169301](https://github.com/pytorch/pytorch/pull/169301))
- Improve NUMA binding docs ([#171543](https://github.com/pytorch/pytorch/pull/171543))
- [SymmMem] Expose window ([#170740](https://github.com/pytorch/pytorch/pull/170740))
- torch.distrubuted: lazy import pdb only when user calls breakpoint() ([#171818](https://github.com/pytorch/pytorch/pull/171818))
- Fix TypedStorage deprecation warning in distributed checkpoint async_â€¦ ([#170759](https://github.com/pytorch/pytorch/pull/170759))
- [DTensor] LRU cachable OpStrategy ([#171223](https://github.com/pytorch/pytorch/pull/171223))
- [c10d] Fix cross-thread work registry lookup in wait_tensor ([#171614](https://github.com/pytorch/pytorch/pull/171614))
- deprecate check_is_size and guard_size_oblivious (#167198) ([#169400](https://github.com/pytorch/pytorch/pull/169400))
- [DTensor] fix _StridedShard(sf=) bug in single dim strategy ([#171942](https://github.com/pytorch/pytorch/pull/171942))
- Fix typo in variable name from 'statetful_sd' to 'stateful_sd' ([#171292](https://github.com/pytorch/pytorch/pull/171292))
- Make copy_ work with more Partial placements ([#170704](https://github.com/pytorch/pytorch/pull/170704))
- [SymmMem] Add MemPool support for NCCL backend ([#171727](https://github.com/pytorch/pytorch/pull/171727))
- [SymmMem][BE] Fold make_peer_info into NCCLPeerAllocInfo ctor ([#171955](https://github.com/pytorch/pytorch/pull/171955))
- [SymmMem] Implement get_offset ([#172044](https://github.com/pytorch/pytorch/pull/172044))
- [DTensor] Ban redistribute from one partial type to another ([#172041](https://github.com/pytorch/pytorch/pull/172041))
- [DTensor] Make redistribution cost for different partials infinite ([#172042](https://github.com/pytorch/pytorch/pull/172042))
- [BE]: Add typing utils to copy signatures from methods or signatures ([#163418](https://github.com/pytorch/pytorch/pull/163418))
- [SymmMem] Deprecate enable_symm_mem_for_group ([#172163](https://github.com/pytorch/pytorch/pull/172163))
- [DTensor] Handle out= ops in single-dim expander ([#172276](https://github.com/pytorch/pytorch/pull/172276))
- [DTensor] Fix for incorrect Tensor Meta Population in `expand_to_full_mesh_op_strategy` ([#172304](https://github.com/pytorch/pytorch/pull/172304))
- [DTensor] insert Replicate at the begining for matmul single dim ([#172150](https://github.com/pytorch/pytorch/pull/172150))
- [SymmMem] Use initializer for devComm requirement ([#172400](https://github.com/pytorch/pytorch/pull/172400))
- [LocalTensor] support misc sym ops ([#172268](https://github.com/pytorch/pytorch/pull/172268))
- Remove MB < PP check for Gpipe ([#171462](https://github.com/pytorch/pytorch/pull/171462))
- [DTensor] single_dim fix symint + _create_expanded_strategy ([#172421](https://github.com/pytorch/pytorch/pull/172421))
- [Fix] fix fully_shard arg typehint inconsistency ([#171574](https://github.com/pytorch/pytorch/pull/171574))
- [dcp][hf] Write metadata file for Consolidate hf safetensors file on every rank method ([#171885](https://github.com/pytorch/pytorch/pull/171885))
- DTensor Ops: Made aten.div.* linearity similar to aten.mul.* ([#172514](https://github.com/pytorch/pytorch/pull/172514))
- DTensor Ops: Add linearity support for neg operation ([#172563](https://github.com/pytorch/pytorch/pull/172563))
- [SymmMem] Extend barrier to both LSA and GIN ([#172701](https://github.com/pytorch/pytorch/pull/172701))
- [coor-slicing] Add SymInt support for DTensor mesh coordinate computation in PT2 ([#169552](https://github.com/pytorch/pytorch/pull/169552))
- [DTensor] make expand_to_full_mesh_op_strategy filter incompatible out= strategies ([#172420](https://github.com/pytorch/pytorch/pull/172420))
- [DTensor] single dim fix inplace op expansion ([#172477](https://github.com/pytorch/pytorch/pull/172477))
- [DebugMode] log DTensor output placements ([#172688](https://github.com/pytorch/pytorch/pull/172688))
- [DTensor] enable single-dim strategy for addmm and baddbmm ([#172387](https://github.com/pytorch/pytorch/pull/172387))
- [DTensor] Support uneven _StridedShard redistribution with device order through Replicate ([#172266](https://github.com/pytorch/pytorch/pull/172266))
- Pass ddp buck cap size list additionally ([#169026](https://github.com/pytorch/pytorch/pull/169026))
- [DTensor] Fix single-dim output_meta validation to handle null-return op ([#172293](https://github.com/pytorch/pytorch/pull/172293))
- [DTensor][BE] redistribute to replicate in from_local backward for partial target type ([#173153](https://github.com/pytorch/pytorch/pull/173153))
- [DTensor] no-op redistribution shouldn't create _TransformInfo ([#172924](https://github.com/pytorch/pytorch/pull/172924))
- [DTensor] single-dim strategy validation infra ([#172990](https://github.com/pytorch/pytorch/pull/172990))
- Implement NCCL 2.29 one-sided APIs for symmetric memory ([#172425](https://github.com/pytorch/pytorch/pull/172425))
- Don't repeatedly log environment variables ([#170399](https://github.com/pytorch/pytorch/pull/170399))
- [DTensor] fix redistribute cost crashing on non-participating ranks ([#172478](https://github.com/pytorch/pytorch/pull/172478))
- [DTensor] S->P(sum) strategy for _powsum, remove reduce_op from NormPartial ([#172604](https://github.com/pytorch/pytorch/pull/172604))
- [DTensor] Make RedistributionPlanner handle all partials ([#172479](https://github.com/pytorch/pytorch/pull/172479))
- Add XCCL to use ProcessGroupWrapper ([#171920](https://github.com/pytorch/pytorch/pull/171920))
- [DTensor] single-dim expander raises clear inplace error ([#173572](https://github.com/pytorch/pytorch/pull/173572))
- [Replicate][FSDP2] share more code betwen replicate and fully_shard ([#173580](https://github.com/pytorch/pytorch/pull/173580))
- [DTensor] Update TP api to support single-dim strategies ([#173567](https://github.com/pytorch/pytorch/pull/173567))
- ProcessGroupNCCL: use lowest rank as split color ([#173687](https://github.com/pytorch/pytorch/pull/173687))
- [FSDP2] Fix mixed DTensor error with nested FSDP and activation checkâ€¦ ([#171779](https://github.com/pytorch/pytorch/pull/171779))
- Fix Flight Recorder default buffer size inconsistency  ([#172843](https://github.com/pytorch/pytorch/pull/172843))
- [DTensor] Fix t() sharding strategy for 1D tensors ([#173964](https://github.com/pytorch/pytorch/pull/173964))
- Removed mixed dtype rejection for clip_grad_norm to bring it inline with the documentation ([#173641](https://github.com/pytorch/pytorch/pull/173641))
- Fix all-reduce strides in compile ([#171616](https://github.com/pytorch/pytorch/pull/171616))
- [c10d] Fix ProcessGroupWrapper missing method forwarding ([#173599](https://github.com/pytorch/pytorch/pull/173599))
- [FSDP2] consolidate shard_mesh and shard_mesh_from_root ([#174107](https://github.com/pytorch/pytorch/pull/174107))
- [DTensor] initial support for decomps + sharding prop ([#171652](https://github.com/pytorch/pytorch/pull/171652))
- [DTensor] Fix unsupported op error ([#170889](https://github.com/pytorch/pytorch/pull/170889))
- [coor-targets] Enable ProcessGroup round-trip through JIT via CapsuleType ([#172794](https://github.com/pytorch/pytorch/pull/172794))
- [DTensor] add shard prop cache logging ([#173775](https://github.com/pytorch/pytorch/pull/173775))
- [DTensor RNG][BC Breaking] Change DTensor Philox seed and offset from int to tensor ([#173876](https://github.com/pytorch/pytorch/pull/173876))
- [DTensor] infer RuntimeSchemaInfo for decomposition ops ([#174422](https://github.com/pytorch/pytorch/pull/174422))
- fix([DTensor]): honor single-dim RuntimeSchemaInfo in C++/Python dispatch  ([#174312](https://github.com/pytorch/pytorch/pull/174312))
- Bind SymmetricMemory as torch class for use in op definition ([#174019](https://github.com/pytorch/pytorch/pull/174019))
- [DTensor] Fix device_mesh extraction from kwargs and add eye.m_out  ([#173489](https://github.com/pytorch/pytorch/pull/173489))
- [DTensor] Optimize redistribute comms using flattened meshes ([#174630](https://github.com/pytorch/pytorch/pull/174630))
- [FSDP2] improve _get_param_to_fqns from O(N^2) to O(N) ([#174675](https://github.com/pytorch/pytorch/pull/174675))
- [DTensor] set static args for decomp OpSchema ([#174616](https://github.com/pytorch/pytorch/pull/174616))
- [DTensor] Fix StridedShard usage conflict with shard order ([#174831](https://github.com/pytorch/pytorch/pull/174831))
- [Torchcomms + DeviceMesh] Enables torchcomms _BackendWrapper shim layer in c10d ([#174202](https://github.com/pytorch/pytorch/pull/174202))
- [DTensor] Fix bucketize with Partial inputs ([#173937](https://github.com/pytorch/pytorch/pull/173937))
- torch.distributed.debug: add support for periodic dumping ([#174808](https://github.com/pytorch/pytorch/pull/174808))
- [DTensor] Strategy Validation (1/3): placement utilities and data structures ([#174798](https://github.com/pytorch/pytorch/pull/174798))
- [DTensor] Fix embedding_dense_backward cache key missing num_weights ([#174727](https://github.com/pytorch/pytorch/pull/174727))
- [DTensor] skip decomposition for CIA ops ([#174918](https://github.com/pytorch/pytorch/pull/174918))
### not user facing
- Enable skipped ROCm NCCL tests ([#169698](https://github.com/pytorch/pytorch/pull/169698))
- [ROCm][CI] Fix failure for test NcclErrorDumpTest::test_nccl_errors_dump ([#169683](https://github.com/pytorch/pytorch/pull/169683))
- [ROCm][CI] Fix failure for test ProcessGroupNCCLGroupTest::test_nan_assert ([#169990](https://github.com/pytorch/pytorch/pull/169990))
- [dtensor][partial] preventing redistribution when linearity is 0 ([#170025](https://github.com/pytorch/pytorch/pull/170025))
- [Test][elastic]fix test_etcd_server_with_rendezvous ([#165431](https://github.com/pytorch/pytorch/pull/165431))
- Fix typing in public torch API ([#168002](https://github.com/pytorch/pytorch/pull/168002))
- [distributed] Replace 89 assert statements in pipelining directory ([#165255](https://github.com/pytorch/pytorch/pull/165255))
- Don't call str when in redistribute hotpath ([#170366](https://github.com/pytorch/pytorch/pull/170366))
- [DTensor] Fix DTensor shardable with StridedShard ([#170364](https://github.com/pytorch/pytorch/pull/170364))
- [CPU][Flex attn] Add a readable error message for the backward path ([#169646](https://github.com/pytorch/pytorch/pull/169646))
- [BE] Restore a unified cache clear for both C++ and Python caches ([#168301](https://github.com/pytorch/pytorch/pull/168301))
- Beef up Partial docs, including note about numerics ([#170434](https://github.com/pytorch/pytorch/pull/170434))
- [CI] fix test_pointwise_ops.py test_mul_div_scalar_partial ([#170510](https://github.com/pytorch/pytorch/pull/170510))
- Optimize bs=1 case for allgather on dim 1 to not split/cat ([#169404](https://github.com/pytorch/pytorch/pull/169404))
- [BE] Rename MaskPartial back to _MaskPartial ([#170423](https://github.com/pytorch/pytorch/pull/170423))
- [DTensor] Use infinite cost for StridedShard temporarily ([#170728](https://github.com/pytorch/pytorch/pull/170728))
- Address LocalTensor test flakines ([#170815](https://github.com/pytorch/pytorch/pull/170815))
- Fix Wdeprecated-copy-with-dtor warnings ([#170734](https://github.com/pytorch/pytorch/pull/170734))
- Part 1: LocalTensor raise ValueError for empty tensor. ([#170577](https://github.com/pytorch/pytorch/pull/170577))
- Fix flaky compile tests for differentiable collectives ([#170779](https://github.com/pytorch/pytorch/pull/170779))
- [DTensor] single-dim pointwise strategy ([#168115](https://github.com/pytorch/pytorch/pull/168115))
- [DebugMode] node.meta["stack_trace"] from DebugInterpreter ([#170126](https://github.com/pytorch/pytorch/pull/170126))
- [DTensor] Fix split_strategy to handle symint split_size ([#170504](https://github.com/pytorch/pytorch/pull/170504))
- localtensor tp ([#169748](https://github.com/pytorch/pytorch/pull/169748))
- fix test_multiple_embeddings_rowwise ([#171330](https://github.com/pytorch/pytorch/pull/171330))
- [DTensor] Add pointwise ops strategy for aten.fmin, aten.fmax, aten.hâ€¦ ([#167973](https://github.com/pytorch/pytorch/pull/167973))
- [DTensor] Fix torch.equal with scalar DTensor inputs ([#169364](https://github.com/pytorch/pytorch/pull/169364))
- Delete copy and move operations for NVSHMEMAllocation to prevent  ([#171456](https://github.com/pytorch/pytorch/pull/171456))
- Gloo PG expand tests for different reduce ops ([#171458](https://github.com/pytorch/pytorch/pull/171458))
- [Enhance] remove CheckpointImpl.REENTRANT future warning ([#171701](https://github.com/pytorch/pytorch/pull/171701))
- [Distributed] Enable support for reduce_scatter_base backward for XCCL backend ([#168213](https://github.com/pytorch/pytorch/pull/168213))
- Add LocalTensor tutorial with verifiable by CI examples ([#171840](https://github.com/pytorch/pytorch/pull/171840))
- Propagate exception from LocalRunnerMode threads to avoid ignored exception failure ([#171947](https://github.com/pytorch/pytorch/pull/171947))
- [DTensor] Add complete OpSpec metadata to create_like_strategy ([#169890](https://github.com/pytorch/pytorch/pull/169890))
- [coor-slicing] DeviceMesh.is_current_rank_part_of_mesh ([#169548](https://github.com/pytorch/pytorch/pull/169548))
- [CUDA] Prevent custom allocator from dying until all allocated blocks die. ([#171962](https://github.com/pytorch/pytorch/pull/171962))
- Unskipped test_ddp_apply_optim_in_backward* for ROCm ([#171889](https://github.com/pytorch/pytorch/pull/171889))
- [DTensor] Correct tensor_meta in _dtensor_init_helper ([#171949](https://github.com/pytorch/pytorch/pull/171949))
- Skip device mesh device setup when using fake backend ([#171830](https://github.com/pytorch/pytorch/pull/171830))
- Part 2: LocalTensor test flatten and unflatten roundtrip. ([#170675](https://github.com/pytorch/pytorch/pull/170675))
- [DTensor] reduce test size due to timeout ([#172255](https://github.com/pytorch/pytorch/pull/172255))
- Adds support for complex parameter model in DataParallel ([#170185](https://github.com/pytorch/pytorch/pull/170185))
- Remove stale @skipIfTorchDynamo for closed issue #115653 ([#171937](https://github.com/pytorch/pytorch/pull/171937))
- Part 3: Split LocalTensor rank and world tests. ([#170814](https://github.com/pytorch/pytorch/pull/170814))
- Skip SAC ILP tests when pulp package is not installed ([#171975](https://github.com/pytorch/pytorch/pull/171975))
- [DTensor] reduce test size due to timeout  ([#172486](https://github.com/pytorch/pytorch/pull/172486))
- [debug mode] Support dispatching into subgraphs in DebugMode for InvokeSubgraph ([#170512](https://github.com/pytorch/pytorch/pull/170512))
- Fix `TestGradCollectives.test_all_reduce` ([#172555](https://github.com/pytorch/pytorch/pull/172555))
- Add force_compile_during_fx_trace config and invoke_subgraph backend ([#171819](https://github.com/pytorch/pytorch/pull/171819))
- [DTensor] tenor -> tensor ([#172723](https://github.com/pytorch/pytorch/pull/172723))
- [ROCm] Enable and fix test_debug_mode_backward ([#172426](https://github.com/pytorch/pytorch/pull/172426))
- [ROCm] Enable test_nccl_errors_nonblocking for ROCm ([#172704](https://github.com/pytorch/pytorch/pull/172704))
- only align mms estimations ([#172778](https://github.com/pytorch/pytorch/pull/172778))
- Add AOTAutograd over Dynamo tests with requires_grad inputs ([#172643](https://github.com/pytorch/pytorch/pull/172643))
- [DTensor] clear shard_prop cache between test_ops tests ([#172504](https://github.com/pytorch/pytorch/pull/172504))
- [bucketing] Fix reordering in manual bucketing pass ([#172699](https://github.com/pytorch/pytorch/pull/172699))
- Make TraceEntry and related structs shareable across backends ([#171089](https://github.com/pytorch/pytorch/pull/171089))
- Add Backend.FAKE ([#172241](https://github.com/pytorch/pytorch/pull/172241))
- Add Backend.FAKE ([#172241](https://github.com/pytorch/pytorch/pull/172241))
- [ROCm][CI] Test skips and fixes for gfx950 ([#173590](https://github.com/pytorch/pytorch/pull/173590))
- Add foreach_groups optimization to _pre_bucket_all_gather ([#173653](https://github.com/pytorch/pytorch/pull/173653))
- [BE] Add explicit copy construction to `c10::Backend::Options` ([#173764](https://github.com/pytorch/pytorch/pull/173764))
- [Test] Fix test_hash_empty_tensor typing ([#173524](https://github.com/pytorch/pytorch/pull/173524))
- Remove more asserts in testing ([#173931](https://github.com/pytorch/pytorch/pull/173931))
- [DTensor][dynamic shapes] OpInfo suite for DTensor + unbacked ops ([#172583](https://github.com/pytorch/pytorch/pull/172583))
- Update FSDP1 tests to use MultiProcContinuousTest ([#173689](https://github.com/pytorch/pytorch/pull/173689))
- Update FSDP tests to use DTensorContinuousTestBase ([#173728](https://github.com/pytorch/pytorch/pull/173728))
- [bc-breaking] Add process group registry to DeviceMesh ([#172272](https://github.com/pytorch/pytorch/pull/172272))
- More benchmark assert removal ([#174214](https://github.com/pytorch/pytorch/pull/174214))
- Add unittest test_nccl_cudagraph_multisegment ([#174225](https://github.com/pytorch/pytorch/pull/174225))
- [distributed][LocalTensor] add view ops test for LocalTensor ([#174077](https://github.com/pytorch/pytorch/pull/174077))
- [dynamic shapes] fix linalg op DDEs ([#173399](https://github.com/pytorch/pytorch/pull/173399))
- Update FSDP1 tests to use MultiProcContinuousTest ([#173689](https://github.com/pytorch/pytorch/pull/173689))
- Remove misleading TODO in _expand_group for DeviceMesh ([#172305](https://github.com/pytorch/pytorch/pull/172305))
- Update FSDP tests to use DTensorContinuousTestBase ([#173728](https://github.com/pytorch/pytorch/pull/173728))
- Update replicate tests to use continuous variants ([#173842](https://github.com/pytorch/pytorch/pull/173842))
- [LocalTensor] Cache DeviceMesh.get_coordinate results in LocalTensorMode ([#173836](https://github.com/pytorch/pytorch/pull/173836))
- [c10] Add cuMemRetainAllocationHandle and cuMemGetAllocationPropertiesFromHandle to DriverAPI ([#173766](https://github.com/pytorch/pytorch/pull/173766))
- Preserves requires_grad state in distribute_module and tensor_parallel ([#171709](https://github.com/pytorch/pytorch/pull/171709))
- Fix DDE in view_as_complex to unblock GoogleFnet hf model with unbacked [HF torchbench] ([#173984](https://github.com/pytorch/pytorch/pull/173984))
- Start test/distributed assert removl ([#174261](https://github.com/pytorch/pytorch/pull/174261))
- Enable DDPOptimizer for composable replicate with torch.compile ([#174307](https://github.com/pytorch/pytorch/pull/174307))
- [ROCm] Check for re-initialization of the process group ([#174586](https://github.com/pytorch/pytorch/pull/174586))
- Check availability of accelerator in test_schedule ([#174760](https://github.com/pytorch/pytorch/pull/174760))
- [LocalTensor] Guard data_ptr() access on wrapper subclass ([#174772](https://github.com/pytorch/pytorch/pull/174772))
- Fix test_replicate_with_fsdp.py ([#174737](https://github.com/pytorch/pytorch/pull/174737))
- [c10d] Document higher-precision reduction ([#174690](https://github.com/pytorch/pytorch/pull/174690))
- [DTensor] set device index only for existing devices ([#174845](https://github.com/pytorch/pytorch/pull/174845))
### security
