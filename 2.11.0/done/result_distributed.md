
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
- `DebugInfoWriter` now honors `$XDG_CACHE_HOME` for its cache directory in C++ code, consistent with the Python side. Previously it always used `~/.cache/torch`. ([#168232](https://github.com/pytorch/pytorch/pull/168232))

  This avoids issues where `$HOME` is not set or not writable. Users who relied on `~/.cache/torch` being used regardless of `$XDG_CACHE_HOME` may see debug info written to a different location.

  Version 2.10:
  ```python
  # C++ DebugInfoWriter always wrote to ~/.cache/torch
  ```

  Version 2.11:
  ```python
  # C++ DebugInfoWriter now respects $XDG_CACHE_HOME/torch (same as Python code)
  # Falls back to ~/.cache/torch if $XDG_CACHE_HOME is not set
  ```

- `DeviceMesh` now stores a process group registry (`_pg_registry`) directly, enabling `torch.compile` to trace through `get_group()`. ([#172272](https://github.com/pytorch/pytorch/pull/172272))

  This may break code that skips `init_process_group`, loads a saved DTensor (constructing a DeviceMesh with no PGs), and later creates PGs separately — during `torch.compile` runtime the PG lookup will fail. Users should ensure process groups are initialized before constructing the DeviceMesh.

  Version 2.10:
  ```python
  # PGs resolved via global _resolve_process_group at runtime
  mesh = DeviceMesh(...)  # PGs could be created later
  ```

  Version 2.11:
  ```python
  # PGs now stored on DeviceMesh._pg_registry; must exist at mesh creation
  dist.init_process_group(...)  # Must be called before creating mesh
  mesh = DeviceMesh(...)
  ```

### deprecation
- `torch.distributed.symmetric_memory.enable_symm_mem_for_group` is deprecated. The store can be retrieved directly via `ProcessGroup.getStore()` in C++, making this call unnecessary. ([#172163](https://github.com/pytorch/pytorch/pull/172163))

  Version 2.10:
  ```python
  from torch.distributed.symmetric_memory import enable_symm_mem_for_group
  enable_symm_mem_for_group(group)
  ```

  Version 2.11:
  ```python
  # No longer needed — store is accessed directly from the ProcessGroup
  ```

### new features
- Add `start_method` option to `torch.distributed.debug.start_debug_server` to select the multiprocessing start method (`fork`, `spawn`, or `forkserver`), enabling CUDA-safe server startup ([#173196](https://github.com/pytorch/pytorch/pull/173196))
- Add support for periodic dumping in `torch.distributed.debug` ([#174808](https://github.com/pytorch/pytorch/pull/174808))
- Non-functional collectives (e.g. `torch.distributed.all_gather`) now automatically work with `FakeTensorMode` — meta implementations are registered at `import torch` time ([#162119](https://github.com/pytorch/pytorch/pull/162119))
- Implement NCCL 2.29 one-sided APIs for symmetric memory ([#172425](https://github.com/pytorch/pytorch/pull/172425))
- Bind `SymmetricMemory` as a torch class for use in op definitions ([#174019](https://github.com/pytorch/pytorch/pull/174019))
- Enable `torchcomms` `_BackendWrapper` shim layer in c10d ([#174202](https://github.com/pytorch/pytorch/pull/174202))
- Expose SymmetricMemory window API ([#170740](https://github.com/pytorch/pytorch/pull/170740))
### improvements
- Set thread name for Gloo internal loop for easier debugging ([#169979](https://github.com/pytorch/pytorch/pull/169979))
- Make `context_parallel_shard` more general ([#170200](https://github.com/pytorch/pytorch/pull/170200))
- Polish NCCL symmetric memory code ([#170582](https://github.com/pytorch/pytorch/pull/170582))
- Add MemPool support for NCCL symmetric memory backend ([#171727](https://github.com/pytorch/pytorch/pull/171727))
- Extend symmetric memory barrier to both LSA and GIN ([#172701](https://github.com/pytorch/pytorch/pull/172701))
- Implement `get_offset` for symmetric memory ([#172044](https://github.com/pytorch/pytorch/pull/172044))
- `ProcessGroupNCCL`: work around for `reduce_scatter` with `world_size=1` ([#170922](https://github.com/pytorch/pytorch/pull/170922))
- Add XCCL backend support for `ProcessGroupWrapper` ([#171920](https://github.com/pytorch/pytorch/pull/171920))
- Lazy import `pdb` only when user calls `breakpoint()` in `torch.distributed` ([#171818](https://github.com/pytorch/pytorch/pull/171818))
- Remove MB < PP check for GPipe pipeline schedule ([#171462](https://github.com/pytorch/pytorch/pull/171462))
- Pass DDP bucket cap size list for finer-grained control ([#169026](https://github.com/pytorch/pytorch/pull/169026))
- Enable ProcessGroup round-trip through JIT via CapsuleType ([#172794](https://github.com/pytorch/pytorch/pull/172794))
- Don't repeatedly log environment variables ([#170399](https://github.com/pytorch/pytorch/pull/170399))
- Set NCCL group desc before creating comm so it propagates ([#171159](https://github.com/pytorch/pytorch/pull/171159))
- `ProcessGroupNCCL`: use lowest rank as split color ([#173687](https://github.com/pytorch/pytorch/pull/173687))
### bug fixes
- Add half precision binding for MPI backend ([#170074](https://github.com/pytorch/pytorch/pull/170074))
- Fix incorrect boolean logic in `std::string::find` method in c10d ([#170057](https://github.com/pytorch/pytorch/pull/170057))
- Fix `_set_pg_timeout` not working for Gloo backend ([#167052](https://github.com/pytorch/pytorch/pull/167052))
- Fix DeviceMesh corner case for coalesce in cute layout and mesh slicing ([#169454](https://github.com/pytorch/pytorch/pull/169454))
- Fix Context Parallel `flex_input_fn` argument unwrapping issue ([#170201](https://github.com/pytorch/pytorch/pull/170201))
- Fix FSDP `_unshard()` passing `Stream` instead of `Event` ([#170525](https://github.com/pytorch/pytorch/pull/170525))
- Ensure threadblock size >= world size in CUDA symmetric memory barrier ([#170785](https://github.com/pytorch/pytorch/pull/170785))
- Fix `ProcessGroupGloo` CUDA tensor stream handling with futures ([#170812](https://github.com/pytorch/pytorch/pull/170812))
- Fix env variable to retrieve HCA list for NVSHMEM ([#170891](https://github.com/pytorch/pytorch/pull/170891))
- Fix FSDP `split_with_sizes_copy()` missing `dim` argument ([#169173](https://github.com/pytorch/pytorch/pull/169173))
- Fix cross-thread work registry lookup in `wait_tensor` ([#171614](https://github.com/pytorch/pytorch/pull/171614))
- Fix `fully_shard` arg typehint inconsistency ([#171574](https://github.com/pytorch/pytorch/pull/171574))
- Fix Flight Recorder default buffer size inconsistency ([#172843](https://github.com/pytorch/pytorch/pull/172843))
- Remove mixed dtype rejection for `clip_grad_norm` to align with documentation (FSDP) ([#173641](https://github.com/pytorch/pytorch/pull/173641))
- Fix all-reduce strides in compiled code ([#171616](https://github.com/pytorch/pytorch/pull/171616))
- Fix `ProcessGroupWrapper` missing method forwarding ([#173599](https://github.com/pytorch/pytorch/pull/173599))
### performance
- Sort mempool registrations via allocation-time counter for CUDA mempools ([#167662](https://github.com/pytorch/pytorch/pull/167662))
- Improve `_get_param_to_fqns` from O(N^2) to O(N) in FSDP ([#174675](https://github.com/pytorch/pytorch/pull/174675))
### docs
### devs
- Fix `USE_NCCL=0` build failure in `nccl_dev_cap.hpp` ([#171694](https://github.com/pytorch/pytorch/pull/171694))
### Untopiced
### not user facing
- Use fusion regions in overlapping ([#170560](https://github.com/pytorch/pytorch/pull/170560))
- Simplify `_ComputationType` (pipeline) ([#170799](https://github.com/pytorch/pytorch/pull/170799))
- Pipeline parallel refactor ([#170804](https://github.com/pytorch/pytorch/pull/170804))
- Fix assert double negatives (pipeline) ([#171142](https://github.com/pytorch/pytorch/pull/171142))
- Remove old CUDA conditions ([#171235](https://github.com/pytorch/pytorch/pull/171235))
- Module load fix ([#171750](https://github.com/pytorch/pytorch/pull/171750))
- Use `enum.member` starting in Python 3.11 ([#169301](https://github.com/pytorch/pytorch/pull/169301))
- Deprecate `check_is_size` and `guard_size_oblivious` ([#169400](https://github.com/pytorch/pytorch/pull/169400))
- Fold `make_peer_info` into `NCCLPeerAllocInfo` ctor (SymmMem) ([#171955](https://github.com/pytorch/pytorch/pull/171955))
- Use initializer for devComm requirement (SymmMem) ([#172400](https://github.com/pytorch/pytorch/pull/172400))
- Preventing redistribution when linearity is 0 (dtensor/partial) ([#170025](https://github.com/pytorch/pytorch/pull/170025))
- Fix test_etcd_server_with_rendezvous ([#165431](https://github.com/pytorch/pytorch/pull/165431))
- Fix typing in public torch API ([#168002](https://github.com/pytorch/pytorch/pull/168002))
- Replace 89 assert statements in pipelining directory ([#165255](https://github.com/pytorch/pytorch/pull/165255))
- Don't call str when in redistribute hotpath ([#170366](https://github.com/pytorch/pytorch/pull/170366))
- Fix DTensor shardable with StridedShard ([#170364](https://github.com/pytorch/pytorch/pull/170364))
- Add a readable error message for flex attn backward on CPU ([#169646](https://github.com/pytorch/pytorch/pull/169646))
- Restore a unified cache clear for both C++ and Python caches ([#168301](https://github.com/pytorch/pytorch/pull/168301))
- Beef up Partial docs, including note about numerics ([#170434](https://github.com/pytorch/pytorch/pull/170434))
- Fix test_pointwise_ops.py test_mul_div_scalar_partial ([#170510](https://github.com/pytorch/pytorch/pull/170510))
- Optimize bs=1 case for allgather on dim 1 ([#169404](https://github.com/pytorch/pytorch/pull/169404))
- Rename MaskPartial back to _MaskPartial ([#170423](https://github.com/pytorch/pytorch/pull/170423))
- Use infinite cost for StridedShard temporarily ([#170728](https://github.com/pytorch/pytorch/pull/170728))
- Address LocalTensor test flakiness ([#170815](https://github.com/pytorch/pytorch/pull/170815))
- Fix Wdeprecated-copy-with-dtor warnings ([#170734](https://github.com/pytorch/pytorch/pull/170734))
- LocalTensor raise ValueError for empty tensor ([#170577](https://github.com/pytorch/pytorch/pull/170577))
- Fix flaky compile tests for differentiable collectives ([#170779](https://github.com/pytorch/pytorch/pull/170779))
- DTensor single-dim pointwise strategy ([#168115](https://github.com/pytorch/pytorch/pull/168115))
- DebugMode: node.meta stack_trace from DebugInterpreter ([#170126](https://github.com/pytorch/pytorch/pull/170126))
- Fix split_strategy to handle symint split_size ([#170504](https://github.com/pytorch/pytorch/pull/170504))
- LocalTensor TP support ([#169748](https://github.com/pytorch/pytorch/pull/169748))
- Fix test_multiple_embeddings_rowwise ([#171330](https://github.com/pytorch/pytorch/pull/171330))
- Add pointwise ops strategy for aten.fmin, aten.fmax ([#167973](https://github.com/pytorch/pytorch/pull/167973))
- Fix torch.equal with scalar DTensor inputs ([#169364](https://github.com/pytorch/pytorch/pull/169364))
- Delete copy/move operations for NVSHMEMAllocation ([#171456](https://github.com/pytorch/pytorch/pull/171456))
- Gloo PG expand tests for different reduce ops ([#171458](https://github.com/pytorch/pytorch/pull/171458))
- Remove CheckpointImpl.REENTRANT future warning ([#171701](https://github.com/pytorch/pytorch/pull/171701))
- Enable support for reduce_scatter_base backward for XCCL backend ([#168213](https://github.com/pytorch/pytorch/pull/168213))
- Add LocalTensor tutorial with CI examples ([#171840](https://github.com/pytorch/pytorch/pull/171840))
- Propagate exception from LocalRunnerMode threads ([#171947](https://github.com/pytorch/pytorch/pull/171947))
- Add complete OpSpec metadata to create_like_strategy ([#169890](https://github.com/pytorch/pytorch/pull/169890))
- DeviceMesh.is_current_rank_part_of_mesh ([#169548](https://github.com/pytorch/pytorch/pull/169548))
- Prevent custom CUDA allocator from dying until all blocks die ([#171962](https://github.com/pytorch/pytorch/pull/171962))
- Correct tensor_meta in _dtensor_init_helper ([#171949](https://github.com/pytorch/pytorch/pull/171949))
- Skip device mesh device setup when using fake backend ([#171830](https://github.com/pytorch/pytorch/pull/171830))
- LocalTensor test flatten and unflatten roundtrip ([#170675](https://github.com/pytorch/pytorch/pull/170675))
- Reduce DTensor test size due to timeout ([#172255](https://github.com/pytorch/pytorch/pull/172255))
- Add support for complex parameter model in DataParallel ([#170185](https://github.com/pytorch/pytorch/pull/170185))
- Remove stale @skipIfTorchDynamo ([#171937](https://github.com/pytorch/pytorch/pull/171937))
- Split LocalTensor rank and world tests ([#170814](https://github.com/pytorch/pytorch/pull/170814))
- Skip SAC ILP tests when pulp package is not installed ([#171975](https://github.com/pytorch/pytorch/pull/171975))
- Reduce DTensor test size due to timeout ([#172486](https://github.com/pytorch/pytorch/pull/172486))
- Support dispatching into subgraphs in DebugMode for InvokeSubgraph ([#170512](https://github.com/pytorch/pytorch/pull/170512))
- Fix TestGradCollectives.test_all_reduce ([#172555](https://github.com/pytorch/pytorch/pull/172555))
- Add force_compile_during_fx_trace config and invoke_subgraph backend ([#171819](https://github.com/pytorch/pytorch/pull/171819))
- DTensor: fix typo (tenor → tensor) ([#172723](https://github.com/pytorch/pytorch/pull/172723))
- Only align mms estimations ([#172778](https://github.com/pytorch/pytorch/pull/172778))
- Add AOTAutograd over Dynamo tests with requires_grad inputs ([#172643](https://github.com/pytorch/pytorch/pull/172643))
- Clear shard_prop cache between test_ops tests ([#172504](https://github.com/pytorch/pytorch/pull/172504))
- Fix reordering in manual bucketing pass ([#172699](https://github.com/pytorch/pytorch/pull/172699))
- Make TraceEntry and related structs shareable across backends ([#171089](https://github.com/pytorch/pytorch/pull/171089))
- Add foreach_groups optimization to _pre_bucket_all_gather ([#173653](https://github.com/pytorch/pytorch/pull/173653))
- Add explicit copy construction to c10::Backend::Options ([#173764](https://github.com/pytorch/pytorch/pull/173764))
- Fix test_hash_empty_tensor typing ([#173524](https://github.com/pytorch/pytorch/pull/173524))
- Remove more asserts in testing ([#173931](https://github.com/pytorch/pytorch/pull/173931))
- DTensor dynamic shapes OpInfo suite ([#172583](https://github.com/pytorch/pytorch/pull/172583))
- More benchmark assert removal ([#174214](https://github.com/pytorch/pytorch/pull/174214))
- Add unittest test_nccl_cudagraph_multisegment ([#174225](https://github.com/pytorch/pytorch/pull/174225))
- Add view ops test for LocalTensor ([#174077](https://github.com/pytorch/pytorch/pull/174077))
- Fix linalg op DDEs (dynamic shapes) ([#173399](https://github.com/pytorch/pytorch/pull/173399))
- Remove misleading TODO in _expand_group for DeviceMesh ([#172305](https://github.com/pytorch/pytorch/pull/172305))
- Update replicate tests to use continuous variants ([#173842](https://github.com/pytorch/pytorch/pull/173842))
- Cache DeviceMesh.get_coordinate results in LocalTensorMode ([#173836](https://github.com/pytorch/pytorch/pull/173836))
- Add cuMemRetainAllocationHandle and cuMemGetAllocationPropertiesFromHandle to DriverAPI ([#173766](https://github.com/pytorch/pytorch/pull/173766))
- Preserve requires_grad state in distribute_module and tensor_parallel ([#171709](https://github.com/pytorch/pytorch/pull/171709))
- Fix DDE in view_as_complex for dynamic shapes ([#173984](https://github.com/pytorch/pytorch/pull/173984))
- Start test/distributed assert removal ([#174261](https://github.com/pytorch/pytorch/pull/174261))
- Enable DDPOptimizer for composable replicate with torch.compile ([#174307](https://github.com/pytorch/pytorch/pull/174307))
- Check availability of accelerator in test_schedule ([#174760](https://github.com/pytorch/pytorch/pull/174760))
- Guard data_ptr() access on wrapper subclass (LocalTensor) ([#174772](https://github.com/pytorch/pytorch/pull/174772))
- Fix test_replicate_with_fsdp.py ([#174737](https://github.com/pytorch/pytorch/pull/174737))
- Document higher-precision reduction (c10d) ([#174690](https://github.com/pytorch/pytorch/pull/174690))
- Set device index only for existing devices (DTensor) ([#174845](https://github.com/pytorch/pytorch/pull/174845))
### security
