
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
- `DebugInfoWriter` now honors `$XDG_CACHE_HOME` in C++ code ([#168232](https://github.com/pytorch/pytorch/pull/168232))

  Previously, the C++ `DebugInfoWriter` always wrote to `~/.cache/torch` regardless of the `$XDG_CACHE_HOME` environment variable. This change aligns C++ behavior with existing Python code, which already uses `$XDG_CACHE_HOME/torch` when that variable is set.

  Users who have `$XDG_CACHE_HOME` set will now see DebugInfoWriter output in `$XDG_CACHE_HOME/torch` instead of `~/.cache/torch`. This also fixes cases where `$HOME` is not set or not writable.

  Version 2.10:
  ```python
  # C++ DebugInfoWriter always wrote to ~/.cache/torch,
  # even when $XDG_CACHE_HOME was set
  ```

  Version 2.11:
  ```python
  # C++ DebugInfoWriter now uses $XDG_CACHE_HOME/torch when set,
  # falling back to ~/.cache/torch otherwise
  ```

- `DeviceMesh` now stores its process group registry directly, which may break a rare workflow involving `torch.compile` ([#172272](https://github.com/pytorch/pytorch/pull/172272))

  `DeviceMesh` now stores process groups on a `_pg_registry` attribute, enabling `torch.compile` to trace through `DeviceMesh.get_group()`. This is BC breaking for users who: (1) skip `init_process_group`, (2) load a saved DTensor (which constructs a DeviceMesh with no PGs attached), (3) create PGs later, and then (4) use `torch.compile` with this mesh. In this scenario, the compiled runtime will fail to find the PG.

  To fix this, ensure `init_process_group` is called before constructing DeviceMesh objects that will be used with `torch.compile`.

  Version 2.10:
  ```python
  # PGs resolved through C++ _resolve_process_group at runtime
  mesh = DeviceMesh(...)
  # ... later create PGs ...
  torch.compile(fn)(mesh)  # worked
  ```

  Version 2.11:
  ```python
  # PGs must exist when DeviceMesh is constructed
  dist.init_process_group(...)  # must be done first
  mesh = DeviceMesh(...)
  torch.compile(fn)(mesh)  # works
  ```

### deprecation
### new features
- Functional collectives (`all_reduce`, `all_gather`, etc.) now support autograd differentiability ([#168140](https://github.com/pytorch/pytorch/pull/168140))
- Added `start_method` option to `torch.distributed.debug.start_debug_server` to support `spawn`/`forkserver` multiprocessing start methods, enabling CUDA-safe server startup ([#173196](https://github.com/pytorch/pytorch/pull/173196))
- `torch.distributed.debug` now supports periodic dumping of debug handlers via `dump_dir` and `dump_interval` parameters in `start_debug_server` ([#174808](https://github.com/pytorch/pytorch/pull/174808))
- Non-functional collectives (e.g. `torch.distributed.all_gather`) now automatically work with `FakeTensorMode` without requiring a separate import ([#162119](https://github.com/pytorch/pytorch/pull/162119))
- Added opt-in TorchComms backend wrapper integration for DeviceMesh and process groups via `TORCH_DISTRIBUTED_USE_TORCHCOMMS=1` ([#174202](https://github.com/pytorch/pytorch/pull/174202))
### improvements
- Context Parallel: `context_parallel_shard` now supports batch dimensions created through `expand()` or `view()` operations ([#170200](https://github.com/pytorch/pytorch/pull/170200))
- DDP: Added `ddp_bucket_cap_mb_list` parameter for fine-grained control over per-bucket all-reduce sizes, improving comm/compute overlap ([#169026](https://github.com/pytorch/pytorch/pull/169026))
- Reduced log noise by only logging environment variables once for the first process group ([#170399](https://github.com/pytorch/pytorch/pull/170399))
- Added XCCL backend support for `ProcessGroupWrapper` ([#171920](https://github.com/pytorch/pytorch/pull/171920))
- Pipeline Parallel: Removed `microbatches < pipeline_stages` check for Gpipe schedule, allowing more flexible configurations ([#171462](https://github.com/pytorch/pytorch/pull/171462))
- `torch.distributed` now lazily imports `pdb` only when `breakpoint()` is called, reducing import overhead ([#171818](https://github.com/pytorch/pytorch/pull/171818))
- Removed `CheckpointImpl.REENTRANT` future warning since the default has already switched to `NO_REENTRANT` ([#171701](https://github.com/pytorch/pytorch/pull/171701))
- Added `reduce_scatter_base` backward support for XCCL backend ([#168213](https://github.com/pytorch/pytorch/pull/168213))
- Added `DeviceMesh.is_current_rank_part_of_mesh()` and `sym_get_coordinate()` convenience methods ([#169548](https://github.com/pytorch/pytorch/pull/169548))
- Enabled `DDPOptimizer` for composable `replicate()` with `torch.compile`, fixing missing comm/compute overlap ([#174307](https://github.com/pytorch/pytorch/pull/174307))
- `DataParallel` now supports models with complex-valued parameters ([#170185](https://github.com/pytorch/pytorch/pull/170185))
- Symmetric Memory: Extended barrier to support both LSA and GIN modes ([#172701](https://github.com/pytorch/pytorch/pull/172701))
### bug fixes
- Added half precision binding for MPI backend ([#170074](https://github.com/pytorch/pytorch/pull/170074))
- Fixed `_set_pg_timeout` not working for Gloo backend ([#167052](https://github.com/pytorch/pytorch/pull/167052))
- Fixed DeviceMesh corner case for coalesce in cute layout and mesh slicing ([#169454](https://github.com/pytorch/pytorch/pull/169454))
- Fixed Context Parallel `flex_input_fn` argument unwrapping issue ([#170201](https://github.com/pytorch/pytorch/pull/170201))
- Fixed FSDP `_unshard()` passing `Stream` instead of `Event` ([#170525](https://github.com/pytorch/pytorch/pull/170525))
- Fixed CUDA Symmetric Memory barrier when threadblock size was smaller than world size ([#170785](https://github.com/pytorch/pytorch/pull/170785))
- Fixed `ProcessGroupGloo` CUDA tensor stream handling with futures ([#170812](https://github.com/pytorch/pytorch/pull/170812))
- Fixed `reduce_scatter` crash with `world_size=1` in `ProcessGroupNCCL` ([#170922](https://github.com/pytorch/pytorch/pull/170922))
- Fixed environment variable retrieval for NVSHMEM HCA list ([#170891](https://github.com/pytorch/pytorch/pull/170891))
- Fixed `split_with_sizes_copy()` missing `dim` argument in FSDP2 ([#169173](https://github.com/pytorch/pytorch/pull/169173))
- Fixed module load failure caused by missing `.py` extension in `_StringLoader.get_filename()` ([#171750](https://github.com/pytorch/pytorch/pull/171750))
- Fixed cross-thread work registry lookup in `wait_tensor` ([#171614](https://github.com/pytorch/pytorch/pull/171614))
- Fixed Flight Recorder default buffer size inconsistency ([#172843](https://github.com/pytorch/pytorch/pull/172843))
- Fixed mixed dtype rejection for `clip_grad_norm` in FSDP to match documentation ([#173641](https://github.com/pytorch/pytorch/pull/173641))
- Fixed all-reduce strides in compiled mode ([#171616](https://github.com/pytorch/pytorch/pull/171616))
- Fixed `ProcessGroupWrapper` missing method forwarding ([#173599](https://github.com/pytorch/pytorch/pull/173599))
- Fixed incorrect boolean logic in `std::string::find` usage in c10d ([#170057](https://github.com/pytorch/pytorch/pull/170057))
- Fixed `requires_grad` state being lost when converting parameters to distributed tensors in `distribute_module` and tensor parallel APIs ([#171709](https://github.com/pytorch/pytorch/pull/171709))
- Fixed `torch.equal` with scalar DTensor inputs failing due to shard strategy applied to 0D tensors ([#169364](https://github.com/pytorch/pytorch/pull/169364))
- Fixed reduce-scatter node reordering in manual bucketing pass ([#172699](https://github.com/pytorch/pytorch/pull/172699))
### performance
- Improved FSDP2 `_get_param_to_fqns` from O(N^2) to O(N) ([#174675](https://github.com/pytorch/pytorch/pull/174675))
- Optimized `bs=1` case for allgather on dim 1 to avoid unnecessary split/cat operations ([#169404](https://github.com/pytorch/pytorch/pull/169404))
- Removed string formatting overhead in redistribute hot path ([#170366](https://github.com/pytorch/pytorch/pull/170366))
- Added `foreach_groups` optimization to `_pre_bucket_all_gather` ([#173653](https://github.com/pytorch/pytorch/pull/173653))
- Cached `DeviceMesh.get_coordinate` results in `LocalTensorMode` ([#173836](https://github.com/pytorch/pytorch/pull/173836))
### docs
- Improved `Partial` placement documentation with notes about numerical behavior ([#170434](https://github.com/pytorch/pytorch/pull/170434))
- Documented higher-precision reduction behavior in c10d ([#174690](https://github.com/pytorch/pytorch/pull/174690))
### devs
- NCCL group desc is now set before creating the communicator so that the description is propagated ([#171159](https://github.com/pytorch/pytorch/pull/171159))
- `DebugMode` now populates `node.meta["stack_trace"]` from `DebugInterpreter` ([#170126](https://github.com/pytorch/pytorch/pull/170126))
- `DebugMode` now supports dispatching into subgraphs for `InvokeSubgraph` ([#170512](https://github.com/pytorch/pytorch/pull/170512))
- Added `force_compile_during_fx_trace` config and `invoke_subgraph` backend ([#171819](https://github.com/pytorch/pytorch/pull/171819))
- Made `TraceEntry` and related structs shareable across backends ([#171089](https://github.com/pytorch/pytorch/pull/171089))
- Added `Backend.FAKE` for testing with fake backends ([#172241](https://github.com/pytorch/pytorch/pull/172241))
- Added explicit copy construction to `c10::Backend::Options` ([#173764](https://github.com/pytorch/pytorch/pull/173764))
- Added `cuMemRetainAllocationHandle` and `cuMemGetAllocationPropertiesFromHandle` to DriverAPI ([#173766](https://github.com/pytorch/pytorch/pull/173766))
- Fixed typing annotations in public `torch.distributed` API ([#168002](https://github.com/pytorch/pytorch/pull/168002))
- Skip device mesh device setup when using fake backend ([#171830](https://github.com/pytorch/pytorch/pull/171830))
- Fixed `USE_NCCL=0` build failure in `nccl_dev_cap.hpp` ([#171694](https://github.com/pytorch/pytorch/pull/171694))
- Fixed `fully_shard` arg typehint inconsistency ([#171574](https://github.com/pytorch/pytorch/pull/171574))
- Exposed `window` method in `NCCLSymmetricMemory.hpp` for C++ developers ([#170740](https://github.com/pytorch/pytorch/pull/170740))
- Implemented `get_offset` for Symmetric Memory ([#172044](https://github.com/pytorch/pytorch/pull/172044))
- Sorted mempool registrations via allocation-time counter ([#167662](https://github.com/pytorch/pytorch/pull/167662))
### not user facing
- Enable skipped ROCm NCCL tests ([#169698](https://github.com/pytorch/pytorch/pull/169698))
- [ROCm][CI] Fix failure for test NcclErrorDumpTest::test_nccl_errors_dump ([#169683](https://github.com/pytorch/pytorch/pull/169683))
- [ROCm][CI] Fix failure for test ProcessGroupNCCLGroupTest::test_nan_assert ([#169990](https://github.com/pytorch/pytorch/pull/169990))
- Prevent DTensor redistribution when linearity is 0 ([#170025](https://github.com/pytorch/pytorch/pull/170025))
- Fix test_etcd_server_with_rendezvous ([#165431](https://github.com/pytorch/pytorch/pull/165431))
- Replace 89 assert statements in pipelining directory ([#165255](https://github.com/pytorch/pytorch/pull/165255))
- [BE] Restore a unified cache clear for both C++ and Python caches ([#168301](https://github.com/pytorch/pytorch/pull/168301))
- [CI] Fix test_pointwise_ops.py test_mul_div_scalar_partial ([#170510](https://github.com/pytorch/pytorch/pull/170510))
- Rename MaskPartial back to _MaskPartial ([#170423](https://github.com/pytorch/pytorch/pull/170423))
- Use infinite cost for StridedShard temporarily in DTensor ([#170728](https://github.com/pytorch/pytorch/pull/170728))
- Address LocalTensor test flakiness ([#170815](https://github.com/pytorch/pytorch/pull/170815))
- Fix Wdeprecated-copy-with-dtor warnings ([#170734](https://github.com/pytorch/pytorch/pull/170734))
- LocalTensor raise ValueError for empty tensor ([#170577](https://github.com/pytorch/pytorch/pull/170577))
- Fix flaky compile tests for differentiable collectives ([#170779](https://github.com/pytorch/pytorch/pull/170779))
- DTensor single-dim pointwise strategy ([#168115](https://github.com/pytorch/pytorch/pull/168115))
- DTensor fix split_strategy to handle symint split_size ([#170504](https://github.com/pytorch/pytorch/pull/170504))
- LocalTensor TP support ([#169748](https://github.com/pytorch/pytorch/pull/169748))
- Fix test_multiple_embeddings_rowwise ([#171330](https://github.com/pytorch/pytorch/pull/171330))
- DTensor: add pointwise ops strategy for aten.fmin, aten.fmax, aten.heaviside ([#167973](https://github.com/pytorch/pytorch/pull/167973))
- Delete copy and move operations for NVSHMEMAllocation ([#171456](https://github.com/pytorch/pytorch/pull/171456))
- Gloo PG expand tests for different reduce ops ([#171458](https://github.com/pytorch/pytorch/pull/171458))
- Add LocalTensor tutorial with CI-verifiable examples ([#171840](https://github.com/pytorch/pytorch/pull/171840))
- Propagate exception from LocalRunnerMode threads ([#171947](https://github.com/pytorch/pytorch/pull/171947))
- DTensor: add complete OpSpec metadata to create_like_strategy ([#169890](https://github.com/pytorch/pytorch/pull/169890))
- Prevent custom CUDA allocator from dying until all allocated blocks die ([#171962](https://github.com/pytorch/pytorch/pull/171962))
- Unskipped test_ddp_apply_optim_in_backward* for ROCm ([#171889](https://github.com/pytorch/pytorch/pull/171889))
- DTensor: correct tensor_meta in _dtensor_init_helper ([#171949](https://github.com/pytorch/pytorch/pull/171949))
- LocalTensor test flatten and unflatten roundtrip ([#170675](https://github.com/pytorch/pytorch/pull/170675))
- DTensor reduce test size due to timeout ([#172255](https://github.com/pytorch/pytorch/pull/172255)), ([#172486](https://github.com/pytorch/pytorch/pull/172486))
- Remove stale @skipIfTorchDynamo for closed issue ([#171937](https://github.com/pytorch/pytorch/pull/171937))
- Split LocalTensor rank and world tests ([#170814](https://github.com/pytorch/pytorch/pull/170814))
- Skip SAC ILP tests when pulp package is not installed ([#171975](https://github.com/pytorch/pytorch/pull/171975))
- Fix TestGradCollectives.test_all_reduce ([#172555](https://github.com/pytorch/pytorch/pull/172555))
- DTensor: fix typo "tenor" -> "tensor" ([#172723](https://github.com/pytorch/pytorch/pull/172723))
- [ROCm] Enable and fix test_debug_mode_backward ([#172426](https://github.com/pytorch/pytorch/pull/172426))
- [ROCm] Enable test_nccl_errors_nonblocking for ROCm ([#172704](https://github.com/pytorch/pytorch/pull/172704))
- Only align mm estimations ([#172778](https://github.com/pytorch/pytorch/pull/172778))
- Add AOTAutograd over Dynamo tests with requires_grad inputs ([#172643](https://github.com/pytorch/pytorch/pull/172643))
- DTensor: clear shard_prop cache between test_ops tests ([#172504](https://github.com/pytorch/pytorch/pull/172504))
- [ROCm][CI] Test skips and fixes for gfx950 ([#173590](https://github.com/pytorch/pytorch/pull/173590))
- Fix test_hash_empty_tensor typing ([#173524](https://github.com/pytorch/pytorch/pull/173524))
- Remove more asserts in testing ([#173931](https://github.com/pytorch/pytorch/pull/173931))
- DTensor dynamic shapes OpInfo suite for unbacked ops ([#172583](https://github.com/pytorch/pytorch/pull/172583))
- Update FSDP1 tests to use MultiProcContinuousTest ([#173689](https://github.com/pytorch/pytorch/pull/173689))
- Update FSDP tests to use DTensorContinuousTestBase ([#173728](https://github.com/pytorch/pytorch/pull/173728))
- More benchmark assert removal ([#174214](https://github.com/pytorch/pytorch/pull/174214))
- Add unittest test_nccl_cudagraph_multisegment ([#174225](https://github.com/pytorch/pytorch/pull/174225))
- Add view ops test for LocalTensor ([#174077](https://github.com/pytorch/pytorch/pull/174077))
- Remove misleading TODO in _expand_group for DeviceMesh ([#172305](https://github.com/pytorch/pytorch/pull/172305))
- Update replicate tests to use continuous variants ([#173842](https://github.com/pytorch/pytorch/pull/173842))
- Start test/distributed assert removal ([#174261](https://github.com/pytorch/pytorch/pull/174261))
- [ROCm] Check for re-initialization of the process group ([#174586](https://github.com/pytorch/pytorch/pull/174586))
- Check availability of accelerator in test_schedule ([#174760](https://github.com/pytorch/pytorch/pull/174760))
- Guard data_ptr() access on wrapper subclass in LocalTensor ([#174772](https://github.com/pytorch/pytorch/pull/174772))
- Fix test_replicate_with_fsdp.py ([#174737](https://github.com/pytorch/pytorch/pull/174737))
- DTensor: set device index only for existing devices ([#174845](https://github.com/pytorch/pytorch/pull/174845))
- Simplify _ComputationType for pipeline parallel ([#170799](https://github.com/pytorch/pytorch/pull/170799))
- Pipeline parallel refactor ([#170804](https://github.com/pytorch/pytorch/pull/170804))
- Fix assert double negatives ([#171142](https://github.com/pytorch/pytorch/pull/171142))
- Remove old CUDA conditions ([#171235](https://github.com/pytorch/pytorch/pull/171235))
- Use enum.member starting in version 3.11 ([#169301](https://github.com/pytorch/pytorch/pull/169301))
- ProcessGroupNCCL: use lowest rank as split color ([#173687](https://github.com/pytorch/pytorch/pull/173687))
- SymmMem: use initializer for devComm requirement ([#172400](https://github.com/pytorch/pytorch/pull/172400))
- [Gloo] Set thread name for gloo internal loop ([#169979](https://github.com/pytorch/pytorch/pull/169979))
- DTensor: fix DTensor shardable with StridedShard ([#170364](https://github.com/pytorch/pytorch/pull/170364))
### Untopiced
### security
