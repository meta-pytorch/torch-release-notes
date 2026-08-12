
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
### bug fixes
### performance
### docs
### devs
### Untopiced
- Route ProcessGroup Python constructors through the PyProcessGroup trampoline ([#186853](https://github.com/pytorch/pytorch/pull/186853))
- [ROCm] Guard NCCL one-sided API behind device support ([#186888](https://github.com/pytorch/pytorch/pull/186888))
- [spmd_types] Add no-typecheck scopes to FSDP hooks ([#186254](https://github.com/pytorch/pytorch/pull/186254))
- [dtensor] migrating matrix_ops to single dim strategies ([#186667](https://github.com/pytorch/pytorch/pull/186667))
- [bugfix] set default backend CUSTOM when backend is UNDEFINED with cu… ([#179901](https://github.com/pytorch/pytorch/pull/179901))
- [dtensor][math_ops]  Add single_dim_strategy functions for sort-like, scan and softmax ops ([#179068](https://github.com/pytorch/pytorch/pull/179068))
- [dtensor] Add single_dim_strategy functions for reduction-with-indices ops ([#179200](https://github.com/pytorch/pytorch/pull/179200))
- PyProcessGroup: support batch_isend_irecv and the coalescing manager ([#186964](https://github.com/pytorch/pytorch/pull/186964))
- c10d: add reconfigure fault-tolerance interfaces to Backend and ProcessGroup ([#186298](https://github.com/pytorch/pytorch/pull/186298))
- c10d: add one-sided window interfaces to Backend and ProcessGroup ([#186299](https://github.com/pytorch/pytorch/pull/186299))
- Use `atomic<shared_ptr>` for current RPC agent ([#185633](https://github.com/pytorch/pytorch/pull/185633))
- Move backend-specific c10d files into per-backend subfolders (#187083) ([#187083](https://github.com/pytorch/pytorch/pull/187083))
- [DTensor] Preserve symbolic local layouts without DDE guards ([#187026](https://github.com/pytorch/pytorch/pull/187026))
- Add nccl-ep bindings ([#178711](https://github.com/pytorch/pytorch/pull/178711))
- [c10d][Flight Recorder][ez] Update the logging message when TCPStore check failed ([#187191](https://github.com/pytorch/pytorch/pull/187191))
- [DTensor] preserve None SDPA philox output specs ([#187199](https://github.com/pytorch/pytorch/pull/187199))
- [CUDA][NCCL] Fix nccl.broadcast dropping the root argument ([#187216](https://github.com/pytorch/pytorch/pull/187216))
- [distributed] Fix max_seqlen mismatch in ring attention backward ([#185493](https://github.com/pytorch/pytorch/pull/185493))
- Add _single c10d::Backend methods and migrate backends to them (#187140) ([#187140](https://github.com/pytorch/pytorch/pull/187140))
- Add portable DebugMode log serialization ([#185010](https://github.com/pytorch/pytorch/pull/185010))
- Fix typos in comments and docstrings ([#187079](https://github.com/pytorch/pytorch/pull/187079))
- [dtensor] Add single_dim_strategy functions for reduction ops ([#179201](https://github.com/pytorch/pytorch/pull/179201))
- Add `torch.distributed._token_switch.TokenSwitch` ([#178712](https://github.com/pytorch/pytorch/pull/178712))
- Add autograd support to TokenSwitch dispatch and combine ([#181314](https://github.com/pytorch/pytorch/pull/181314))
- Move NCCL EP bindings into an optional extension ([#187366](https://github.com/pytorch/pytorch/pull/187366))
- [dtensor] Add single_dim_strategy functions for pooling, replicate-only, and histc ops ([#179202](https://github.com/pytorch/pytorch/pull/179202))
- [dtensor][math_ops] fixing math_ops single dim strategies to consider output_mask ([#187383](https://github.com/pytorch/pytorch/pull/187383))
- [fsdp2][mp] Fix FSDP2 mixed precision reduce dtype after unfreezing params ([#187376](https://github.com/pytorch/pytorch/pull/187376))
- [pipelining] Optional per-direction P2P communicators for PipelineStage ([#186173](https://github.com/pytorch/pytorch/pull/186173))
- Avoid AOT CSE across backward dependency boundary ([#184044](https://github.com/pytorch/pytorch/pull/184044))
- [c10d] Add public torch.distributed.set_timeout, deprecate _set_pg_timeout ([#187387](https://github.com/pytorch/pytorch/pull/187387))
- c10d: add abort hooks and wire pre/post collective hooks ([#186300](https://github.com/pytorch/pytorch/pull/186300))
- Register ProcessGroup opaque type globally ([#187459](https://github.com/pytorch/pytorch/pull/187459))
- c10d: route ProcessGroup rank and size through backends ([#187467](https://github.com/pytorch/pytorch/pull/187467))
- Dynamically link NCCL EP for USE_SYSTEM_NCCL=ON (wheel) builds ([#187385](https://github.com/pytorch/pytorch/pull/187385))
- [dtensor] add logspace ([#186398](https://github.com/pytorch/pytorch/pull/186398))
- Expose distributed backend implementation accessors ([#187494](https://github.com/pytorch/pytorch/pull/187494))
- Support set_timeout on FakeProcessGroup; warn instead of raising by default ([#187693](https://github.com/pytorch/pytorch/pull/187693))
- [c10d] Silence clang-tidy false positives in TraceUtils.h ([#187706](https://github.com/pytorch/pytorch/pull/187706))
- [c10d] Add Gloo process group fault tolerance support ([#187381](https://github.com/pytorch/pytorch/pull/187381))
- Add TorchElastic signal-failure enrichment hook (#187098) ([#187098](https://github.com/pytorch/pytorch/pull/187098))
- compile-on-one-rank: move the flag to torch.compiler.config (deprecate distributed alias) ([#187869](https://github.com/pytorch/pytorch/pull/187869))
- make_fx: parameterize baked device operands under compile-on-one-rank (CooR) ([#186892](https://github.com/pytorch/pytorch/pull/186892))
- [c10d] Keep tabulate private in flight_recorder builder ([#186648](https://github.com/pytorch/pytorch/pull/186648))
- [SymmetricMemory] Add `get` API to SymmetricMemory ([#182378](https://github.com/pytorch/pytorch/pull/182378))
- Support distributed backend registration through entrypoints (#187388) ([#187388](https://github.com/pytorch/pytorch/pull/187388))
- Fix coordinate cache in `LocalDeviceMesh` ([#187052](https://github.com/pytorch/pytorch/pull/187052))
- [spmd_types] fully_shard in DTensor and spmd_types save-restore ([#181519](https://github.com/pytorch/pytorch/pull/181519))
- [dtensor][math_ops] strategies for remaining ops ([#179203](https://github.com/pytorch/pytorch/pull/179203))
- Stash coalesced tensors on the endCoalescing Work, not the per-call Work ([#187433](https://github.com/pytorch/pytorch/pull/187433))
- [dtensor] migrating tensor ops to single dim strategies ([#186754](https://github.com/pytorch/pytorch/pull/186754))
- [SymmMem] Add barrier implementation for NCCL symmetric memory backend ([#188051](https://github.com/pytorch/pytorch/pull/188051))
- [dcp] Explicitly flush streams before os.fsync to support remote storage systems like GCS ([#183877](https://github.com/pytorch/pytorch/pull/183877))
- auto qualify backend strings for comms ([#187856](https://github.com/pytorch/pytorch/pull/187856))
- Forward backend through dist.new_group delegation to custom PGs ([#188489](https://github.com/pytorch/pytorch/pull/188489))
- Add all_gather_single and reduce_scatter_single to PyProcessGroup ([#188548](https://github.com/pytorch/pytorch/pull/188548))
- Add OpInfo for cpu flash sdpa ([#185651](https://github.com/pytorch/pytorch/pull/185651))
- Remove control collectives implementation ([#188617](https://github.com/pytorch/pytorch/pull/188617))
- [dtensor] add linspace ([#187933](https://github.com/pytorch/pytorch/pull/187933))
- [c10d] Deprecate setSequenceNumberForGroup as a no-op ([#188611](https://github.com/pytorch/pytorch/pull/188611))
- Support all remaining unsupported collectives in PyProcessGroup ([#188570](https://github.com/pytorch/pytorch/pull/188570))
- Improve distribute_module docstring ([#188071](https://github.com/pytorch/pytorch/pull/188071))
- [ROCm] Fixed memory errors in SymmetricMemory caused by repeated call of hipMemMap ([#188673](https://github.com/pytorch/pytorch/pull/188673))
- Rename OpaqueBase to CustomClassBase ([#188455](https://github.com/pytorch/pytorch/pull/188455))
- Rename register_opaque_type to register_custom_class ([#188456](https://github.com/pytorch/pytorch/pull/188456))
- Rename "value type" to "constant type" for custom classes ([#188458](https://github.com/pytorch/pytorch/pull/188458))
- [Test] Make NUMA binding device-generic via torch.accelerator for out-of-tree backends ([#185266](https://github.com/pytorch/pytorch/pull/185266))
- [ShardedTensor] Make ShardedTensor Device Transfer Methods Hardware-Agnostic ([#187939](https://github.com/pytorch/pytorch/pull/187939))
- [xpu][test] Add XCCL support in common distributed test code ([#183625](https://github.com/pytorch/pytorch/pull/183625))
- Add cublasLt as a backend for grouped GEMM (bf16/fp16 support) ([#177037](https://github.com/pytorch/pytorch/pull/177037))
- Add FakeStore type stub to _distributed_c10d.pyi ([#189259](https://github.com/pytorch/pytorch/pull/189259))
- Fix backend registration for string devices ([#187960](https://github.com/pytorch/pytorch/pull/187960))
- [c10d][nccl2] Port torchcomms NCCL backend foundation (utils, CUDA API, batch) ([#188582](https://github.com/pytorch/pytorch/pull/188582))
- [c10d][nccl2] Port the NcclApi abstraction ([#188583](https://github.com/pytorch/pytorch/pull/188583))
- [c10d][nccl2] Port the NCCL work object (on c10d::Work) and Store bootstrap ([#188584](https://github.com/pytorch/pytorch/pull/188584))
- [c10d][nccl2] Add ProcessGroupNCCL class declaration and engine helpers ([#188585](https://github.com/pytorch/pytorch/pull/188585))
- [c10d][nccl2] Add the ProcessGroupNCCL NCCL engine implementation ([#188586](https://github.com/pytorch/pytorch/pull/188586))
- [FSDP] Fix to_cpu when flat_param is already on CPU ([#188990](https://github.com/pytorch/pytorch/pull/188990))
- Add CE multicast low-contention all-gather ([#185359](https://github.com/pytorch/pytorch/pull/185359))
- [c10d] Add weights_only parameter to object collectives ([#189353](https://github.com/pytorch/pytorch/pull/189353))
- [c10d] Use _coalescing_manager for abort instead of hardcoded NCCL group calls ([#189770](https://github.com/pytorch/pytorch/pull/189770))
- [c10d][nccl2] Add fault tolerance (reconfigure) support with backend-agnostic tests ([#189359](https://github.com/pytorch/pytorch/pull/189359))
- [c10d][nccl2] Add one-sided window (RMA) APIs ([#189360](https://github.com/pytorch/pytorch/pull/189360))
- dtensor: include local tensor device in _stable_hash_for_caching ([#188401](https://github.com/pytorch/pytorch/pull/188401))
- Set gpuDirectRDMACapable alloc flag in CUDA symmetric memory ([#189941](https://github.com/pytorch/pytorch/pull/189941))
- Gate nccl2 backend behind USE_C10D_NCCL ([#189938](https://github.com/pytorch/pytorch/pull/189938))
- [CP] Balance per-document head-tail load balancer with rank-major layout ([#189902](https://github.com/pytorch/pytorch/pull/189902))
- Reapply "Remove CUDA sync in torch.combinations to improve `torch.compile` support (#186595)" ([#189305](https://github.com/pytorch/pytorch/pull/189305))
- [c10d][nccl2] Fix ROCm <7.0 build by guarding hipEventRecordWithFlags ([#189958](https://github.com/pytorch/pytorch/pull/189958))
- Keep TorchScript out of import paths and make its deprecation warnings visible ([#189914](https://github.com/pytorch/pytorch/pull/189914))
- [SymmMem] Place the signal pad at the front of symmetric memory allocations ([#189088](https://github.com/pytorch/pytorch/pull/189088))
- Fix typos in comments and docstrings across distributed and utils modules ([#189357](https://github.com/pytorch/pytorch/pull/189357))
- [c10d][nccl2] Add suspend/resume memory offload support ([#189361](https://github.com/pytorch/pytorch/pull/189361))
- [c10d][nccl2] Add nccl-lazy wrapper backend with per-peer P2P pair comms ([#189362](https://github.com/pytorch/pytorch/pull/189362))
- [c10d] Add FlightRecorderHook: FlightRecorder recording via ProcessGroup hooks for any backend ([#189363](https://github.com/pytorch/pytorch/pull/189363))
- [DCP] Add CheckpointableTensor protocol ([#189492](https://github.com/pytorch/pytorch/pull/189492))
- [c10d] Use PyTorch CUDA wrappers in NCCL2 ([#190084](https://github.com/pytorch/pytorch/pull/190084))
- [c10d][nccl2] Fix c10d backend contract gaps ([#190138](https://github.com/pytorch/pytorch/pull/190138))
- [FSDP] Preserve container object identity in _recursive_to function ([#171617](https://github.com/pytorch/pytorch/pull/171617))
- [dtensor] Resolve ProcessGroup from mesh in-graph under compile_on_one_rank ([#188215](https://github.com/pytorch/pytorch/pull/188215))
- [distributed] Fix broadcast subgroup gradient rank comparison ([#190583](https://github.com/pytorch/pytorch/pull/190583))
- Remove NCCL2 store creation/destruction logic ([#190592](https://github.com/pytorch/pytorch/pull/190592))
- Create TorchComms subgroups on the correct device ([#189072](https://github.com/pytorch/pytorch/pull/189072))
- [c10d][nccl2] Fix work and allocator lifetimes ([#190370](https://github.com/pytorch/pytorch/pull/190370))
- Remove new_group to split_group delegation on the TorchComms path ([#189071](https://github.com/pytorch/pytorch/pull/189071))
- [distributed] Return NON_GROUP_MEMBER from local new_group ([#190588](https://github.com/pytorch/pytorch/pull/190588))
- Fix: allow both linear reductions ("sum" and "avg") through the guard ([#190224](https://github.com/pytorch/pytorch/pull/190224))
- Make subgroup name hash salt collective-consistent ([#189073](https://github.com/pytorch/pytorch/pull/189073))
- Deduplicate comms when destroying a process group ([#189074](https://github.com/pytorch/pytorch/pull/189074))
- [c10d][nccl2] Wrap single-op P2P send/recv in ncclGroupStart/End ([#190622](https://github.com/pytorch/pytorch/pull/190622))
- [Test] Decouple hardcoded device types in distributed test infrastructure ([#190182](https://github.com/pytorch/pytorch/pull/190182))
- [nccl2] Cleanup naming for reconfigure and CCA hook ([#191023](https://github.com/pytorch/pytorch/pull/191023))
- [c10d][torchcomms] Add MCCL backend wrapper example (#190292) ([#191034](https://github.com/pytorch/pytorch/pull/191034))
- [c10d][nccl2] Host-block the synchronous barrier ([#190682](https://github.com/pytorch/pytorch/pull/190682))
- [nccl2] Publish host comm to symmetric memory via a registration hook ([#191109](https://github.com/pytorch/pytorch/pull/191109))
- [c10d] Add an explicit NCCL legacy backend ([#191272](https://github.com/pytorch/pytorch/pull/191272))
- Expose  NCCL commName in ncclConfig bindings to ProcessGroupNCCL.Options() ([#191001](https://github.com/pytorch/pytorch/pull/191001))
- Add ${hostname} macro to torchrun log line prefixes ([#191265](https://github.com/pytorch/pytorch/pull/191265))
- [distributed] Document reconfigure APIs ([#191384](https://github.com/pytorch/pytorch/pull/191384))
- [c10d] Normalize new_group ranks to Python integers ([#191377](https://github.com/pytorch/pytorch/pull/191377))
- Allow explicit pre-split pipeline microbatches ([#188500](https://github.com/pytorch/pytorch/pull/188500))
- Validate LocalTensor all_to_all_single split sizes ([#190311](https://github.com/pytorch/pytorch/pull/190311))
- [c10d][nccl2] Implement eager comm-split (split_group) support ([#190943](https://github.com/pytorch/pytorch/pull/190943))
- Add --print-completion to torchrun ([#191289](https://github.com/pytorch/pytorch/pull/191289))
- Accept device-qualified gloo backend in monitored_barrier ([#189070](https://github.com/pytorch/pytorch/pull/189070))
- [DTensor] Fix CommDebugMode hook leak when a module runs twice ([#191452](https://github.com/pytorch/pytorch/pull/191452))
- [Distributed] Remove unreachable return in functional collectives fallback ([#191444](https://github.com/pytorch/pytorch/pull/191444))
- [symm_mem] Warn on multi-stream use of collective ops ([#191482](https://github.com/pytorch/pytorch/pull/191482))
- [c10d] Pick default ProcessGroup BackendType from backends that are actually registered ([#189193](https://github.com/pytorch/pytorch/pull/189193))
- [c10d] Fix WorkNCCL::logPrefix() reporting stale rank across process groups ([#191440](https://github.com/pytorch/pytorch/pull/191440))
- [BugFix] Fix operator precedence bug in check_channel signal pad validation ([#191596](https://github.com/pytorch/pytorch/pull/191596))
- [c10d][nccl2] Preserve the caller CUDA device ([#191510](https://github.com/pytorch/pytorch/pull/191510))
- [c10d] Validate all-to-all split sizes ([#191511](https://github.com/pytorch/pytorch/pull/191511))
- Fix torchcomms bug of destroying one subgroup wipes every live group ([#191637](https://github.com/pytorch/pytorch/pull/191637))
- [c10d] Fix device_id not propagated through ProcessGroupWrapper ([#182273](https://github.com/pytorch/pytorch/pull/182273))
- [c10d][nccl2] Complete the WorkNCCL contract ([#191517](https://github.com/pytorch/pytorch/pull/191517))
- [c10d][nccl2] Support nonblocking NCCL communicators ([#191528](https://github.com/pytorch/pytorch/pull/191528))
- [c10d][nccl2] Support uneven list collectives ([#191542](https://github.com/pytorch/pytorch/pull/191542))
- [c10d][nccl-lazy] Forward group UID to primary backend ([#191544](https://github.com/pytorch/pytorch/pull/191544))
- [c10d][nccl-lazy] Reject reconfigurable mode ([#191549](https://github.com/pytorch/pytorch/pull/191549))
- [c10d][nccl-lazy] Include pair channels in lifecycle state ([#191553](https://github.com/pytorch/pytorch/pull/191553))
- [c10d][nccl-lazy] Add shared backend test coverage ([#191556](https://github.com/pytorch/pytorch/pull/191556))
- [ROCm] Add skipIfRocmVersionAtLeast([7, 14]) skips for ROCm 7.14 known failures ([#188593](https://github.com/pytorch/pytorch/pull/188593))
- [c10d][nccl2] Disable NVLS under torch deterministic mode ([#192104](https://github.com/pytorch/pytorch/pull/192104))
- [c10d][nccl2] Make process-abort on timeout/error configurable; stop abort() killing the process ([#192105](https://github.com/pytorch/pytorch/pull/192105))
- [c10d][gloo] Fix ProcessGroupGloo::split OOB when the world PG is not the first gloo PG ([#192106](https://github.com/pytorch/pytorch/pull/192106))
- [c10d][nccl2] Don't allocate from the CUDA caching allocator during eager init ([#192107](https://github.com/pytorch/pytorch/pull/192107))
- [c10d][nccl2] Implement register_mem_pool / deregister_mem_pool ([#192108](https://github.com/pytorch/pytorch/pull/192108))
- [c10d][nccl] Fix ProcessGroupNCCL::split OOB when the world PG is not the first NCCL PG ([#192109](https://github.com/pytorch/pytorch/pull/192109))
- [c10d] Give each backend its own Options when splitting or merging a process group ([#192110](https://github.com/pytorch/pytorch/pull/192110))
- [c10d] Fix split_group's backend filter for parents with a bare backend string ([#192111](https://github.com/pytorch/pytorch/pull/192111))
- [c10d][nccl2] Never issue collective NCCL calls from the caching-allocator trace hook ([#192112](https://github.com/pytorch/pytorch/pull/192112))
- [c10d] Only honor TORCHELASTIC_USE_AGENT_STORE at the agent's own address ([#192113](https://github.com/pytorch/pytorch/pull/192113))
- [c10d] Fix bfloat16 NCCL PREMUL_SUM factor being read as zero ([#190747](https://github.com/pytorch/pytorch/pull/190747))
- [c10d][nccl2] Give the profiler a per-group collective sequence number ([#192114](https://github.com/pytorch/pytorch/pull/192114))
- [c10d][nccl2] Record a split child's world ranks and stop it borrowing commName ([#192115](https://github.com/pytorch/pytorch/pull/192115))
- [DTensor] Support non-overlapping last-dimension sharding for convolution op ([#192147](https://github.com/pytorch/pytorch/pull/192147))
- [c10d] Fix use-after-free in FlightRecorder::dump_entries ([#192232](https://github.com/pytorch/pytorch/pull/192232))
- [symm_mem] Run alloc/rendezvous device ops on the current stream  ([#192308](https://github.com/pytorch/pytorch/pull/192308))
- [TorchElastic] handle EADDRINUSE message of libuv ([#191561](https://github.com/pytorch/pytorch/pull/191561))
- [docs] Document how to invoke NCCL's symmetric memory (SymK) kernels from process group ([#192515](https://github.com/pytorch/pytorch/pull/192515))
- Remove the deprecated use_cuda option from the profiler ([#192543](https://github.com/pytorch/pytorch/pull/192543))
- [symm_mem] Self-import the multicast handle on rank 0 ([#192530](https://github.com/pytorch/pytorch/pull/192530))
- Pass group_desc and group_name to NCCL via ncclConfig.commName ([#192487](https://github.com/pytorch/pytorch/pull/192487))
- final plain assertion removal ([#192517](https://github.com/pytorch/pytorch/pull/192517))
- [symm_mem] Route multicast setup through the PG when PG rendezvous is… ([#192623](https://github.com/pytorch/pytorch/pull/192623))
- [c10d] Add missing runCollectiveChecks for allgather_into_tensor_coalesced in ProcessGroupWrapper ([#185123](https://github.com/pytorch/pytorch/pull/185123))
- [symm_mem] Validate peer rank in put_signal/wait_signal, complete channel OOB tests ([#191842](https://github.com/pytorch/pytorch/pull/191842))
- Deprecate the profiler's with_modules option ([#192808](https://github.com/pytorch/pytorch/pull/192808))
- support DTensor S(1) -> Partial("sum") ([#191828](https://github.com/pytorch/pytorch/pull/191828))
### not user facing
- [ptd_triage_bot] preventing duplicated ptd triage bot comments ([#186966](https://github.com/pytorch/pytorch/pull/186966))
- cache _is_spmd_types_available ([#187071](https://github.com/pytorch/pytorch/pull/187071))
- Resolve nested ACT inputs before AOTAutograd tracing ([#186442](https://github.com/pytorch/pytorch/pull/186442))
- [dynamo, nested graph breaks] add NGB_SUPPRESS_INLINELIST to prevent NGB in torch.distributed ([#187220](https://github.com/pytorch/pytorch/pull/187220))
- Fix DTensor out variant detection ([#187466](https://github.com/pytorch/pytorch/pull/187466))
- [SymmMem] Skip test_get on ROCm ([#188021](https://github.com/pytorch/pytorch/pull/188021))
- Fix functional isend/irecv passing a global peer rank to sub-group P2P ops ([#187924](https://github.com/pytorch/pytorch/pull/187924))
- Remove experimental torch.distributed._dist2 API ([#188116](https://github.com/pytorch/pytorch/pull/188116))
- Replace std::lock+adopt_lock with std::scoped_lock ([#188142](https://github.com/pytorch/pytorch/pull/188142))
- Preserve pipeline buffers during dynamic metadata inference ([#188558](https://github.com/pytorch/pytorch/pull/188558))
- [DTensor] Fix backward support for cumprod, cummax, cummin ([#185228](https://github.com/pytorch/pytorch/pull/185228))
- Rename TorchScriptObjectVariable and OpaqueObjectClassVariable ([#188460](https://github.com/pytorch/pytorch/pull/188460))
- Rename is_opaque_type and is_opaque_value ([#188461](https://github.com/pytorch/pytorch/pull/188461))
- [dynamo, nested graph breaks] enable NGB on some tests that now work with NGB ([#186657](https://github.com/pytorch/pytorch/pull/186657))
- [Test][distributed] Update entries in `test_backends.py` ([#185202](https://github.com/pytorch/pytorch/pull/185202))
- docs: fix PyTorch brand name consistency ([#189248](https://github.com/pytorch/pytorch/pull/189248))
- Make test_sac_ilp hardware-independent by pinning device datasheet ([#189278](https://github.com/pytorch/pytorch/pull/189278))
- Add a debug log when we skip sync_decision_cross_ranks (#187699) ([#187699](https://github.com/pytorch/pytorch/pull/187699))
- [TEST] Actually check the required number of gpus in `test_dtensor_pp_integration` ([#189418](https://github.com/pytorch/pytorch/pull/189418))
- Skip test_p2p_ipc_expandable_segments (failing in CI, B200) ([#190096](https://github.com/pytorch/pytorch/pull/190096))
- Skip DTensor test_scaled_mm (failing on B200) ([#190097](https://github.com/pytorch/pytorch/pull/190097))
- Fix flaky xfail for test_dtensor_op_db_multinomial_cpu_float32 ([#190252](https://github.com/pytorch/pytorch/pull/190252))
- Fix distributed test main-guard AttributeError on GPU-less CUDA builds ([#190441](https://github.com/pytorch/pytorch/pull/190441))
- Fix test_nvshmem import crash on GPU-less CUDA builds ([#190442](https://github.com/pytorch/pytorch/pull/190442))
- Bump cublasLt grouped GEMM version requirement to 13.3 ([#190372](https://github.com/pytorch/pytorch/pull/190372))
- [Test] Refactor FSDP tests for hardware agnosticism ([#190309](https://github.com/pytorch/pytorch/pull/190309))
- [local_tensor] Patch dist.get_rank in LocalTensorMode ([#189408](https://github.com/pytorch/pytorch/pull/189408))
- Add symmetric memory + CUDAGraph tests ([#190786](https://github.com/pytorch/pytorch/pull/190786))
- Add another hook to triage skill ([#191042](https://github.com/pytorch/pytorch/pull/191042))
- Fix GPU requirements for 2D composability tests ([#191033](https://github.com/pytorch/pytorch/pull/191033))
- Fix PP composability skip decorator ordering ([#191039](https://github.com/pytorch/pytorch/pull/191039))
- [CI] Update clang-tidyto 21.1.0 ([#191111](https://github.com/pytorch/pytorch/pull/191111))
- [Testcase Refactoring]Add PrivateUse1 backend support to ShardedOptimizer tests ([#191174](https://github.com/pytorch/pytorch/pull/191174))
- [tests] Add coverage for fabric expandable segment cleanup ([#191343](https://github.com/pytorch/pytorch/pull/191343))
- [pipelining] Decide metadata mode locally when using a fake process group ([#191538](https://github.com/pytorch/pytorch/pull/191538))
- Use ast.literal_eval instead of eval for ranks ([#191490](https://github.com/pytorch/pytorch/pull/191490))
- [tests] #191343 followup - missing delete to trigger unmap ([#191639](https://github.com/pytorch/pytorch/pull/191639))
- Fix flaky test_redistribute_cost_latency via local RNG generator ([#191516](https://github.com/pytorch/pytorch/pull/191516))
- [BE] Fix B018 warnings in symmetric-memory Triton hooks ([#191831](https://github.com/pytorch/pytorch/pull/191831))
- Preserve GC state in flight recorder read_dir ([#191607](https://github.com/pytorch/pytorch/pull/191607))
- [symmetric_memory] Re-enable multicast tests ([#192539](https://github.com/pytorch/pytorch/pull/192539))
- [Testcase Refactoring] Enable PrivateUse1 tests and add hw-classification in test_transformer ([#189682](https://github.com/pytorch/pytorch/pull/189682))
### security
