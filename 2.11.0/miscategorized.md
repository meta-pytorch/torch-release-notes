# Miscategorized PRs

PRs moved from the main `distributed` worksheet to the appropriate area.

## From distributed -> distributed (checkpoint)
- [Distributed] Optimize checkpoint resharding with sweep-line algorithm ([#169115](https://github.com/pytorch/pytorch/pull/169115))
- Cleanup unused ignores 2 ([#171639](https://github.com/pytorch/pytorch/pull/171639))
- Fix TypedStorage deprecation warning in distributed checkpoint async_â€¦ ([#170759](https://github.com/pytorch/pytorch/pull/170759))
- Fix typo in variable name from 'statetful_sd' to 'stateful_sd' ([#171292](https://github.com/pytorch/pytorch/pull/171292))
- [dcp][hf] Write metadata file for Consolidate hf safetensors file on every rank method ([#171885](https://github.com/pytorch/pytorch/pull/171885))

## From distributed -> distributed (dtensor)
- [DTensor] Refactor _select_min_cost_strategy as a util ([#170197](https://github.com/pytorch/pytorch/pull/170197))
- [DTensor][BE] remove is_backward from redistribute_local_tensor ([#170147](https://github.com/pytorch/pytorch/pull/170147))
- [DTensor] Add OpSchema.args_meta, kwargs_meta helpers ([#170358](https://github.com/pytorch/pytorch/pull/170358))
- Reapply "[DTensor] Refactor strategy/rule registration into dedicated module (#168221)" (a695f3cbd3c)
- [DTensor] ensure op_info is never None in _dispatch_get_local_results_slow_path ([#170584](https://github.com/pytorch/pytorch/pull/170584))
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
- [DTensor] Fix for incorrect Tensor Meta Population in `expand_to_full_mesh_op_strategy` ([#172304](https://github.com/pytorch/pytorch/pull/172304))
- [DTensor] insert Replicate at the begining for matmul single dim ([#172150](https://github.com/pytorch/pytorch/pull/172150))
- [LocalTensor] support misc sym ops ([#172268](https://github.com/pytorch/pytorch/pull/172268))
- [DTensor] single_dim fix symint + _create_expanded_strategy ([#172421](https://github.com/pytorch/pytorch/pull/172421))
- DTensor Ops: Made aten.div.* linearity similar to aten.mul.* ([#172514](https://github.com/pytorch/pytorch/pull/172514))
- DTensor Ops: Add linearity support for neg operation ([#172563](https://github.com/pytorch/pytorch/pull/172563))
- [coor-slicing] Add SymInt support for DTensor mesh coordinate computation in PT2 ([#169552](https://github.com/pytorch/pytorch/pull/169552))
- [DTensor] make expand_to_full_mesh_op_strategy filter incompatible out= strategies ([#172420](https://github.com/pytorch/pytorch/pull/172420))
- [DTensor] single dim fix inplace op expansion ([#172477](https://github.com/pytorch/pytorch/pull/172477))
- [DebugMode] log DTensor output placements ([#172688](https://github.com/pytorch/pytorch/pull/172688))
- [DTensor] enable single-dim strategy for addmm and baddbmm ([#172387](https://github.com/pytorch/pytorch/pull/172387))
- [DTensor] Support uneven _StridedShard redistribution with device order through Replicate ([#172266](https://github.com/pytorch/pytorch/pull/172266))
- [DTensor] Fix single-dim output_meta validation to handle null-return op ([#172293](https://github.com/pytorch/pytorch/pull/172293))
- [DTensor][BE] redistribute to replicate in from_local backward for partial target type ([#173153](https://github.com/pytorch/pytorch/pull/173153))
- [DTensor] no-op redistribution shouldn't create _TransformInfo ([#172924](https://github.com/pytorch/pytorch/pull/172924))
- [DTensor] single-dim strategy validation infra ([#172990](https://github.com/pytorch/pytorch/pull/172990))
- [DTensor] fix redistribute cost crashing on non-participating ranks ([#172478](https://github.com/pytorch/pytorch/pull/172478))
- [DTensor] S->P(sum) strategy for _powsum, remove reduce_op from NormPartial ([#172604](https://github.com/pytorch/pytorch/pull/172604))
- [DTensor] Make RedistributionPlanner handle all partials ([#172479](https://github.com/pytorch/pytorch/pull/172479))
- [DTensor] single-dim expander raises clear inplace error ([#173572](https://github.com/pytorch/pytorch/pull/173572))
- [DTensor] Update TP api to support single-dim strategies ([#173567](https://github.com/pytorch/pytorch/pull/173567))
- [DTensor] Fix t() sharding strategy for 1D tensors ([#173964](https://github.com/pytorch/pytorch/pull/173964))
- [DTensor] initial support for decomps + sharding prop ([#171652](https://github.com/pytorch/pytorch/pull/171652))
- [DTensor] Fix unsupported op error ([#170889](https://github.com/pytorch/pytorch/pull/170889))
- [DTensor] add shard prop cache logging ([#173775](https://github.com/pytorch/pytorch/pull/173775))
- [DTensor RNG][BC Breaking] Change DTensor Philox seed and offset from int to tensor ([#173876](https://github.com/pytorch/pytorch/pull/173876))
- [DTensor] infer RuntimeSchemaInfo for decomposition ops ([#174422](https://github.com/pytorch/pytorch/pull/174422))
- fix([DTensor]): honor single-dim RuntimeSchemaInfo in C++/Python dispatch  ([#174312](https://github.com/pytorch/pytorch/pull/174312))
- [DTensor] Fix device_mesh extraction from kwargs and add eye.m_out  ([#173489](https://github.com/pytorch/pytorch/pull/173489))
- [DTensor] Optimize redistribute comms using flattened meshes ([#174630](https://github.com/pytorch/pytorch/pull/174630))
- [DTensor] set static args for decomp OpSchema ([#174616](https://github.com/pytorch/pytorch/pull/174616))
- [DTensor] Fix StridedShard usage conflict with shard order ([#174831](https://github.com/pytorch/pytorch/pull/174831))
- [DTensor] Fix bucketize with Partial inputs ([#173937](https://github.com/pytorch/pytorch/pull/173937))
- [DTensor] Strategy Validation (1/3): placement utilities and data structures ([#174798](https://github.com/pytorch/pytorch/pull/174798))
- [DTensor] Fix embedding_dense_backward cache key missing num_weights ([#174727](https://github.com/pytorch/pytorch/pull/174727))
- [DTensor] skip decomposition for CIA ops ([#174918](https://github.com/pytorch/pytorch/pull/174918))

## From distributed -> distributed (fsdp2)
- [Replicate][FSDP2] share more code betwen replicate and fully_shard ([#173580](https://github.com/pytorch/pytorch/pull/173580))
- [FSDP2] Fix mixed DTensor error with nested FSDP and activation checkâ€¦ ([#171779](https://github.com/pytorch/pytorch/pull/171779))
- [FSDP2] consolidate shard_mesh and shard_mesh_from_root ([#174107](https://github.com/pytorch/pytorch/pull/174107))

## From distributed -> distributed (symm_mem)
- [Symmetric memory] Polish NCCL symm mem code ([#170582](https://github.com/pytorch/pytorch/pull/170582))
- [SymmMem] NCCL device comm manager ([#170544](https://github.com/pytorch/pytorch/pull/170544))
- [SymmMem] Improve header dependency re nccl_device support ([#170634](https://github.com/pytorch/pytorch/pull/170634))
- [SymmMem] Add MemPool support for NCCL backend ([#171727](https://github.com/pytorch/pytorch/pull/171727))
- [SymmMem][BE] Fold make_peer_info into NCCLPeerAllocInfo ctor ([#171955](https://github.com/pytorch/pytorch/pull/171955))
- [SymmMem] Deprecate enable_symm_mem_for_group ([#172163](https://github.com/pytorch/pytorch/pull/172163))
- Implement NCCL 2.29 one-sided APIs for symmetric memory ([#172425](https://github.com/pytorch/pytorch/pull/172425))
- Bind SymmetricMemory as torch class for use in op definition ([#174019](https://github.com/pytorch/pytorch/pull/174019))

## From distributed -> distributed (torchelastic)
- Improve NUMA binding docs ([#171543](https://github.com/pytorch/pytorch/pull/171543))

## From distributed -> fx
- fix input mutation handling for subclasses that perform intermediate compute during copy_ (DTensor) ([#170467](https://github.com/pytorch/pytorch/pull/170467))
- use fusion regions in overlapping ([#170560](https://github.com/pytorch/pytorch/pull/170560))
- deprecate check_is_size and guard_size_oblivious (#167198) ([#169400](https://github.com/pytorch/pytorch/pull/169400))

## From distributed -> jit
- [coor-targets] Enable ProcessGroup round-trip through JIT via CapsuleType ([#172794](https://github.com/pytorch/pytorch/pull/172794))

## From distributed -> nn
- [2/N] Remove outdated CUDA code ([#170357](https://github.com/pytorch/pytorch/pull/170357))

## From distributed -> python_frontend
- [BE]: Add typing utils to copy signatures from methods or signatures ([#163418](https://github.com/pytorch/pytorch/pull/163418))

## From distributed -> quantization
- Apply various ruff fixes ([#170968](https://github.com/pytorch/pytorch/pull/170968))

## From distributed -> cpu
- [CPU][Flex attn] Add a readable error message for the backward path ([#169646](https://github.com/pytorch/pytorch/pull/169646))

## From distributed -> linalg_frontend
- [dynamic shapes] fix linalg op DDEs ([#173399](https://github.com/pytorch/pytorch/pull/173399))
- Fix DDE in view_as_complex to unblock GoogleFnet hf model with unbacked [HF torchbench] ([#173984](https://github.com/pytorch/pytorch/pull/173984))
