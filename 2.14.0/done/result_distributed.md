
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
- Nonmember ranks now receive `GroupMember.NON_GROUP_MEMBER` instead of `None` from locally synchronized subgroup creation ([#190588](https://github.com/pytorch/pytorch/pull/190588), [#190725](https://github.com/pytorch/pytorch/pull/190725))

  When `torch.distributed.new_group(..., use_local_synchronization=True)` excludes the calling rank, it now returns the same nonmember sentinel as other `new_group` paths. The experimental `torch.distributed.split_group()` likewise returns the sentinel when the calling rank is absent from every requested split. Code that identifies nonmembers with `is None` must compare against `torch.distributed.GroupMember.NON_GROUP_MEMBER` instead.

  Before:

  ```python
  group = torch.distributed.new_group(
      ranks=[0, 1], use_local_synchronization=True
  )
  if group is None:
      return
  ```

  After:

  ```python
  group = torch.distributed.new_group(
      ranks=[0, 1], use_local_synchronization=True
  )
  if group == torch.distributed.GroupMember.NON_GROUP_MEMBER:
      return
  ```
### deprecation
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
- Use `torch.distributed.set_timeout()` instead of the private `_set_pg_timeout()` helper ([#187387](https://github.com/pytorch/pytorch/pull/187387))

  `_set_pg_timeout()` remains as a forwarding alias but now emits a `FutureWarning`. The public replacement has the same `timeout, group=None` signature and updates every backend registered with the process group.

  Before:

  ```python
  from datetime import timedelta
  from torch.distributed.distributed_c10d import _set_pg_timeout

  _set_pg_timeout(timedelta(seconds=30), group)
  ```

  After:

  ```python
  from datetime import timedelta
  import torch.distributed as dist

  dist.set_timeout(timedelta(seconds=30), group)
  ```
### new features
- Add portable JSON serialization through `DebugMode.save_logs()` and `DebugMode.load_logs()` so distributed execution logs can be compared across separate processes or model configurations ([#185010](https://github.com/pytorch/pytorch/pull/185010))
- Add `torch.distributed.tensor.logspace` for constructing distributed logarithmically spaced tensors ([#186398](https://github.com/pytorch/pytorch/pull/186398))
- Add experimental `torch.distributed.get_backend_impl()` and `ProcessGroup.get_backend()` accessors for custom backend development ([#187494](https://github.com/pytorch/pytorch/pull/187494))
- Add `torch.distributed.tensor.linspace` for constructing distributed linearly spaced tensors ([#187933](https://github.com/pytorch/pytorch/pull/187933))
- Add fault-tolerant reconfiguration and one-sided window operations to the experimental `nccl2` backend ([#189359](https://github.com/pytorch/pytorch/pull/189359), [#189360](https://github.com/pytorch/pytorch/pull/189360))
- Add the experimental `nccl-lazy` backend, which creates per-peer NCCL point-to-point communicators on demand ([#189362](https://github.com/pytorch/pytorch/pull/189362))
- Add the `CheckpointableTensor` protocol so distributed checkpointing can save and load tensor-like objects that expose global and local shard metadata ([#189492](https://github.com/pytorch/pytorch/pull/189492))
- Add an explicit `nccl-legacy` backend and the `TORCH_DIST_USE_NCCL2=1` opt-in for selecting the experimental replacement behind the `nccl` name ([#191272](https://github.com/pytorch/pytorch/pull/191272))
- Allow `ProcessGroupNCCL.Options.config.comm_name` to assign readable communicator names for NCCL logs and profiler tools ([#191001](https://github.com/pytorch/pytorch/pull/191001))
- Add `torchrun --log-line-prefix-template` and a `${hostname}` template variable for identifying the host that emitted each worker log line ([#191265](https://github.com/pytorch/pytorch/pull/191265))
- Allow pipeline schedules to consume explicitly pre-split positional inputs, keyword inputs, and targets through `arg_mbs`, `kwarg_mbs`, and `target_mbs` ([#188500](https://github.com/pytorch/pytorch/pull/188500))
- Add optional shell-completion generation to `torchrun` through `--print-completion` and the `shtab` package ([#191289](https://github.com/pytorch/pytorch/pull/191289))
### improvements
- Expand DTensor sharding strategies for matrix, attention, sorting, scanning, softmax, and related operations ([#186667](https://github.com/pytorch/pytorch/pull/186667), [#179068](https://github.com/pytorch/pytorch/pull/179068))
- Allow custom Python `ProcessGroup` implementations to use `batch_isend_irecv` and the coalescing manager ([#186964](https://github.com/pytorch/pytorch/pull/186964))
- Improve the Flight Recorder diagnostic emitted when a TCPStore check fails ([#187191](https://github.com/pytorch/pytorch/pull/187191))
- Allow pipeline parallel stages to use separate forward and backward point-to-point communicators, reducing cross-batch ordering hazards ([#186173](https://github.com/pytorch/pytorch/pull/186173))
- Add fault-tolerant reconfiguration support to Gloo process groups ([#187381](https://github.com/pytorch/pytorch/pull/187381))
- Make compile-on-one-rank graphs portable across ranks by replacing baked accelerator device indices with a runtime current-device operation ([#186892](https://github.com/pytorch/pytorch/pull/186892))
- Expand active DTensor single-dimension strategies for tensor operations ([#186754](https://github.com/pytorch/pytorch/pull/186754))
- Auto-qualify bare backend names and pass process-group options through custom TorchComms backend creation ([#187856](https://github.com/pytorch/pytorch/pull/187856))
- Add complete collective coverage to custom Python process groups, including single-tensor gather/scatter and the remaining point-to-point and collective operations ([#188548](https://github.com/pytorch/pytorch/pull/188548), [#188570](https://github.com/pytorch/pytorch/pull/188570))
- Make TorchElastic NUMA binding and ShardedTensor device transfers work with accelerator backends beyond CUDA ([#185266](https://github.com/pytorch/pytorch/pull/185266), [#187939](https://github.com/pytorch/pytorch/pull/187939))
- Use generic collective coalescing when aborting process groups so third-party backends can avoid multi-communicator teardown deadlocks ([#189770](https://github.com/pytorch/pytorch/pull/189770))
- Mark CUDA symmetric-memory allocations as GPUDirect RDMA capable on supported systems ([#189941](https://github.com/pytorch/pytorch/pull/189941))
- Add communicator memory suspend/resume support to the experimental `nccl2` backend ([#189361](https://github.com/pytorch/pytorch/pull/189361))
- Allow unknown device-qualified TorchComms backend names to register as custom backends without users mutating c10d's backend maps ([#191034](https://github.com/pytorch/pytorch/pull/191034))
- Add eager `split_group` support, complete `Work` semantics, nonblocking communicators, and uneven list collectives to the experimental `nccl2` backend ([#190943](https://github.com/pytorch/pytorch/pull/190943), [#191517](https://github.com/pytorch/pytorch/pull/191517), [#191528](https://github.com/pytorch/pytorch/pull/191528), [#191542](https://github.com/pytorch/pytorch/pull/191542))
- Include `nccl-lazy` pair communicators in error reporting, suspend/resume operations, and memory statistics, and expand its shared backend coverage ([#191553](https://github.com/pytorch/pytorch/pull/191553), [#191556](https://github.com/pytorch/pytorch/pull/191556))
- Add memory-pool registration and deregistration support to the experimental `nccl2` backend ([#192108](https://github.com/pytorch/pytorch/pull/192108))
- Add per-process-group collective sequence numbers and accurate split-group membership metadata to `nccl2` profiler traces ([#192114](https://github.com/pytorch/pytorch/pull/192114), [#192115](https://github.com/pytorch/pytorch/pull/192115))
- Support non-overlapping final-spatial-dimension DTensor sharding for Conv1d, Conv2d, and Conv3d forward and backward ([#192147](https://github.com/pytorch/pytorch/pull/192147))
- Pass process-group descriptions and names to NCCL's `commName` field while preserving user-specified communicator names ([#192487](https://github.com/pytorch/pytorch/pull/192487))
- Support DTensor redistribution from final-dimension sharding to `Partial("sum")` ([#191828](https://github.com/pytorch/pytorch/pull/191828))
### bug fixes
- Fix Python `ProcessGroup` subclasses failing construction through the `(store, rank, size)` constructor and ensure their virtual overrides are dispatched correctly ([#186853](https://github.com/pytorch/pytorch/pull/186853))
- Select registered custom communication backends instead of incorrectly falling back to NCCL or Gloo when the backend is unspecified ([#179901](https://github.com/pytorch/pytorch/pull/179901))
- Fix compiled DTensor backward paths producing data-dependent guards for valid symbolic local layouts ([#187026](https://github.com/pytorch/pytorch/pull/187026))
- Preserve local Philox seed and offset outputs when expanding DTensor scaled dot-product attention strategies across multidimensional meshes ([#187199](https://github.com/pytorch/pytorch/pull/187199))
- Respect nonzero `root` arguments in `torch.cuda.nccl.broadcast` instead of always broadcasting from the first tensor ([#187216](https://github.com/pytorch/pytorch/pull/187216))
- Fix ring-attention backward using mismatched maximum sequence lengths when context-parallel load balancing is enabled ([#185493](https://github.com/pytorch/pytorch/pull/185493))
- Fix DTensor backward strategies emitting placements for outputs disabled by `output_mask` ([#187383](https://github.com/pytorch/pytorch/pull/187383))
- Preserve the configured FSDP2 gradient-reduction dtype when parameters are frozen during the first forward and later unfrozen ([#187376](https://github.com/pytorch/pytorch/pull/187376))
- Make `torch.distributed.set_timeout()` a no-op for fake process groups and warn rather than fail for backends that cannot configure timeouts ([#187693](https://github.com/pytorch/pytorch/pull/187693))
- Fix `LocalDeviceMesh` returning stale coordinates after a temporary submesh is destroyed and its object ID is reused ([#187052](https://github.com/pytorch/pytorch/pull/187052))
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
- Fix destroying one TorchComms subgroup inadvertently destroying every live group ([#191637](https://github.com/pytorch/pytorch/pull/191637))
- Propagate `device_id` through `ProcessGroupWrapper` so debug wrappers do not hang with heterogeneous rank-to-GPU mappings ([#182273](https://github.com/pytorch/pytorch/pull/182273))
- Forward group identifiers through `nccl-lazy` so NCCL symmetric-memory rendezvous can find the primary communicator ([#191544](https://github.com/pytorch/pytorch/pull/191544))
- Reject unsupported reconfigurable mode for `nccl-lazy` instead of advertising incomplete membership-change support ([#191549](https://github.com/pytorch/pytorch/pull/191549))
- Disable NCCL NVLS in `nccl2` when deterministic algorithms are enabled, matching the legacy NCCL backend ([#192104](https://github.com/pytorch/pytorch/pull/192104))
- Prevent `nccl2` watchdog errors, timeouts, explicit aborts, and normal teardown from unconditionally terminating the process ([#192105](https://github.com/pytorch/pytorch/pull/192105))
- Fix Gloo and NCCL `split_group` crashes when the world process group was not the first backend instance created in the process ([#192106](https://github.com/pytorch/pytorch/pull/192106), [#192109](https://github.com/pytorch/pytorch/pull/192109))
- Fix device-bound `nccl2` process-group initialization failing before the CUDA caching allocator has been initialized ([#192107](https://github.com/pytorch/pytorch/pull/192107))
- Give split and merged process groups independent backend options so child creation cannot corrupt parent metadata or share mutable options ([#192110](https://github.com/pytorch/pytorch/pull/192110))
- Fix `split_group(backend=...)` filtering for parent groups created with a bare backend name ([#192111](https://github.com/pytorch/pytorch/pull/192111))
- Prevent private TCPStore rendezvous under `torchrun` from hanging by using the agent store only for the agent's own address ([#192113](https://github.com/pytorch/pytorch/pull/192113))
- Fix bfloat16 NCCL `PREMUL_SUM` factors being interpreted as zero and silently producing zero gradients ([#190747](https://github.com/pytorch/pytorch/pull/190747))
- Fix a use-after-free race while concurrently dumping Flight Recorder entries ([#192232](https://github.com/pytorch/pytorch/pull/192232))
- Run symmetric-memory allocation and rendezvous device work on the caller's current CUDA stream ([#192308](https://github.com/pytorch/pytorch/pull/192308))
- Recognize libuv's lowercase `address already in use` message when TorchElastic retries TCPStore creation ([#191561](https://github.com/pytorch/pytorch/pull/191561))
- Add missing collective-fingerprint checks for `allgather_into_tensor_coalesced` under `ProcessGroupWrapper` ([#185123](https://github.com/pytorch/pytorch/pull/185123))
- Fix DTensor AOT compilation misclassifying overload names containing `out` as output-variant operators ([#187466](https://github.com/pytorch/pytorch/pull/187466))
- Fix compiled functional point-to-point collectives passing global peer ranks to subgroup operations that require group-local ranks ([#187924](https://github.com/pytorch/pytorch/pull/187924))
- Preserve pipeline-stage module buffers while dynamic metadata inference runs representative forward and backward passes ([#188558](https://github.com/pytorch/pytorch/pull/188558))
- Fix DTensor backward support for `cumprod`, `cummax`, and `cummin` ([#185228](https://github.com/pytorch/pytorch/pull/185228))
- Make pipeline schedules select static metadata locally when a fake process group cannot perform cross-rank metadata inference, and report incomplete stage metadata clearly ([#191538](https://github.com/pytorch/pytorch/pull/191538))
- Restore the caller's cyclic-garbage-collector state after Flight Recorder `read_dir()` calls, including when loading fails ([#191607](https://github.com/pytorch/pytorch/pull/191607))
### performance
- Add a copy-engine multicast implementation of low-contention symmetric-memory all-gather with improved bandwidth and compute overlap ([#185359](https://github.com/pytorch/pytorch/pull/185359))
- Balance context-parallel packed-document attention work across ranks with rank-major head-tail layout ([#189902](https://github.com/pytorch/pytorch/pull/189902))
- Let rank 0 use the peer-copy path for symmetric-memory multicast transfers so copies can overlap host transfers ([#192530](https://github.com/pytorch/pytorch/pull/192530))
- Reduce store pressure during large-scale symmetric-memory setup by routing multicast rendezvous through the process group when configured ([#192623](https://github.com/pytorch/pytorch/pull/192623))
### docs
- Correct typos in distributed memory-analysis documentation and related docstrings ([#187079](https://github.com/pytorch/pytorch/pull/187079))
- Document the callback signatures, return values, keyword-argument behavior, and usage of `distribute_module` ([#188071](https://github.com/pytorch/pytorch/pull/188071))
- Correct typos in distributed and utility comments and docstrings ([#189357](https://github.com/pytorch/pytorch/pull/189357), [#190827](https://github.com/pytorch/pytorch/pull/190827))
- Correct PyTorch brand name capitalization in distributed checkpoint and other documentation ([#189248](https://github.com/pytorch/pytorch/pull/189248))
- Document the experimental process-group reconfiguration APIs and provide an end-to-end usage example ([#191384](https://github.com/pytorch/pytorch/pull/191384))
- Document how to enable and verify NCCL symmetric-memory kernels through registered memory pools or symmetric-memory rendezvous ([#192515](https://github.com/pytorch/pytorch/pull/192515))
### devs
- Guard NCCL one-sided APIs correctly on ROCm so source builds do not reference unsupported device-side functionality ([#186888](https://github.com/pytorch/pytorch/pull/186888))
- Add process-group extension interfaces for fault-tolerant reconfiguration and one-sided communication windows ([#186298](https://github.com/pytorch/pytorch/pull/186298), [#186299](https://github.com/pytorch/pytorch/pull/186299))
- Keep RPC source builds compatible with modern C++ standard libraries by using `std::atomic<std::shared_ptr>` where available ([#185633](https://github.com/pytorch/pytorch/pull/185633))
- Add canonical `_single` collective methods to the C++ `Backend` interface while preserving compatibility with existing backend overrides and callers ([#187140](https://github.com/pytorch/pytorch/pull/187140))
- Add abort and pre/post-collective hooks to the c10d backend and process-group extension interfaces ([#186300](https://github.com/pytorch/pytorch/pull/186300))
- Register `ProcessGroup` globally as a supported custom-operator input type ([#187459](https://github.com/pytorch/pytorch/pull/187459))
- Route process-group rank and size through backend implementations to support reconfigurable backends ([#187467](https://github.com/pytorch/pytorch/pull/187467))
- Support optional NCCL expert-parallelism extensions in both bundled-NCCL source builds and system-NCCL wheel builds ([#187366](https://github.com/pytorch/pytorch/pull/187366), [#187385](https://github.com/pytorch/pytorch/pull/187385))
- Silence false-positive clang-tidy diagnostics in c10d Flight Recorder utilities ([#187706](https://github.com/pytorch/pytorch/pull/187706))
- Allow distributed backends to register through Python package entry points ([#187388](https://github.com/pytorch/pytorch/pull/187388))
- Add a TorchElastic error-handler hook that downstream integrations can use to enrich signal-failure reports ([#187098](https://github.com/pytorch/pytorch/pull/187098))
- Deprecate the backend-level `_set_sequence_number_for_group()` no-op and remove its private `ProcessGroup` binding while preserving the sequence-number getter ([#188611](https://github.com/pytorch/pytorch/pull/188611))
- Add XCCL-aware common distributed test infrastructure for Intel GPUs ([#183625](https://github.com/pytorch/pytorch/pull/183625))
- Add the missing `FakeStore` declaration to the `_distributed_c10d` type stub ([#189259](https://github.com/pytorch/pytorch/pull/189259))
- Keep the experimental `nccl2` backend buildable without NCCL and on ROCm versions before 7.0 ([#189938](https://github.com/pytorch/pytorch/pull/189938), [#189958](https://github.com/pytorch/pytorch/pull/189958))
- Add a backend-agnostic Flight Recorder hook for process-group extension authors ([#189363](https://github.com/pytorch/pytorch/pull/189363))
### not user facing
- Add no-typecheck scopes around internal FSDP hooks in preparation for type migration ([#186254](https://github.com/pytorch/pytorch/pull/186254))
- Refactor DTensor reduction-with-indices strategies without changing registered operator coverage ([#179200](https://github.com/pytorch/pytorch/pull/179200))
- Reorganize private c10d backend implementation files into backend-specific directories ([#187083](https://github.com/pytorch/pytorch/pull/187083))
- Add private NCCL expert-parallelism bindings used by higher-level distributed features ([#178711](https://github.com/pytorch/pytorch/pull/178711))
- Add internal single-dimension DTensor strategy implementations for reductions, pooling, replicate-only operations, and histograms without changing active registrations ([#179201](https://github.com/pytorch/pytorch/pull/179201), [#179202](https://github.com/pytorch/pytorch/pull/179202))
- Add the private experimental NCCL-backed `TokenSwitch` implementation and autograd support ([#178712](https://github.com/pytorch/pytorch/pull/178712), [#181314](https://github.com/pytorch/pytorch/pull/181314))
- Keep the optional Flight Recorder table-formatting dependency private ([#186648](https://github.com/pytorch/pytorch/pull/186648))
- Add the private symmetric-memory `get` primitive used by experimental one-sided DTensor work ([#182378](https://github.com/pytorch/pytorch/pull/182378))
- Add internal FSDP support for preserving and restoring experimental SPMD type annotations ([#181519](https://github.com/pytorch/pytorch/pull/181519))
- Add inactive single-dimension DTensor strategy implementations for remaining math operations ([#179203](https://github.com/pytorch/pytorch/pull/179203))
- Add CPU flash-attention operator metadata and test coverage ([#185651](https://github.com/pytorch/pytorch/pull/185651))
- Remove unused private store-based control-collective APIs ([#188617](https://github.com/pytorch/pytorch/pull/188617))
- Add source-only components of the experimental in-tree `nccl2` process-group backend before its activation ([#188582](https://github.com/pytorch/pytorch/pull/188582), [#188583](https://github.com/pytorch/pytorch/pull/188583), [#188584](https://github.com/pytorch/pytorch/pull/188584), [#188585](https://github.com/pytorch/pytorch/pull/188585), [#188586](https://github.com/pytorch/pytorch/pull/188586))
- Replace the experimental `nccl2` backend's private CUDA abstraction with PyTorch's standard CUDA wrappers ([#190084](https://github.com/pytorch/pytorch/pull/190084))
- Simplify experimental NCCL2 and TorchComms subgroup internals without changing public behavior ([#190592](https://github.com/pytorch/pytorch/pull/190592), [#189071](https://github.com/pytorch/pytorch/pull/189071), [#191023](https://github.com/pytorch/pytorch/pull/191023))
- Generalize distributed test infrastructure for additional accelerator backends ([#190182](https://github.com/pytorch/pytorch/pull/190182))
- Remove unreachable code from the functional-collectives fallback ([#191444](https://github.com/pytorch/pytorch/pull/191444))
- Temporarily skip known ROCm 7.14 test failures while the new CI configuration is stabilized ([#188593](https://github.com/pytorch/pytorch/pull/188593))
- Prevent duplicate comments from the distributed triage bot ([#186966](https://github.com/pytorch/pytorch/pull/186966))
- Cache the internal SPMD-types availability probe ([#187071](https://github.com/pytorch/pytorch/pull/187071))
- Skip the unsupported symmetric-memory `get` test on ROCm ([#188021](https://github.com/pytorch/pytorch/pull/188021))
- Remove the unused private experimental `torch.distributed._dist2` module ([#188116](https://github.com/pytorch/pytorch/pull/188116))
- Modernize internal locking and replace plain assertions across distributed and compiler code ([#188142](https://github.com/pytorch/pytorch/pull/188142), [#192517](https://github.com/pytorch/pytorch/pull/192517))
- Update distributed backend tests for the current XPU and MPS backend maps ([#185202](https://github.com/pytorch/pytorch/pull/185202))
- Make selective-activation-checkpointing estimator tests deterministic across GPU models by pinning device specifications ([#189278](https://github.com/pytorch/pytorch/pull/189278))
- Correct distributed test accelerator requirements, hardware guards, and CI skips ([#189418](https://github.com/pytorch/pytorch/pull/189418), [#190096](https://github.com/pytorch/pytorch/pull/190096), [#190097](https://github.com/pytorch/pytorch/pull/190097), [#190252](https://github.com/pytorch/pytorch/pull/190252), [#190441](https://github.com/pytorch/pytorch/pull/190441), [#190442](https://github.com/pytorch/pytorch/pull/190442), [#190309](https://github.com/pytorch/pytorch/pull/190309), [#191033](https://github.com/pytorch/pytorch/pull/191033), [#191039](https://github.com/pytorch/pytorch/pull/191039))
- Patch `torch.distributed.get_rank()` inside the private `LocalTensorMode` test utility ([#189408](https://github.com/pytorch/pytorch/pull/189408))
- Add symmetric-memory CUDA Graph test coverage ([#190786](https://github.com/pytorch/pytorch/pull/190786))
- Extend internal distributed issue-triage automation ([#191042](https://github.com/pytorch/pytorch/pull/191042))
- Extend ShardedOptimizer and pipeline-transformer tests to PrivateUse1 accelerators ([#191174](https://github.com/pytorch/pytorch/pull/191174), [#189682](https://github.com/pytorch/pytorch/pull/189682))
- Add regression coverage for CUDA fabric expandable-segment cleanup ([#191343](https://github.com/pytorch/pytorch/pull/191343), [#191639](https://github.com/pytorch/pytorch/pull/191639))
- Stabilize the DTensor redistribution cost-model test with a per-rank local random-number generator ([#191516](https://github.com/pytorch/pytorch/pull/191516))
- Resolve linter warnings in symmetric-memory Triton hooks without changing behavior ([#191831](https://github.com/pytorch/pytorch/pull/191831))
- Re-enable symmetric-memory multicast test coverage on supported hardware ([#192539](https://github.com/pytorch/pytorch/pull/192539))
### security
- Add an opt-in `weights_only=True` mode to distributed object collectives for restricted deserialization; the default remains unchanged for compatibility ([#189353](https://github.com/pytorch/pytorch/pull/189353))
- Validate symmetric-memory signal channels against the actual signal-pad bounds to prevent illegal memory access or adjacent-allocation corruption ([#191596](https://github.com/pytorch/pytorch/pull/191596))
- Validate peer ranks in symmetric-memory signaling APIs to prevent out-of-bounds device-memory access and silent corruption ([#191842](https://github.com/pytorch/pytorch/pull/191842))
- Parse Flight Recorder rank expressions with `ast.literal_eval()` instead of executing them with `eval()` ([#191490](https://github.com/pytorch/pytorch/pull/191490))
