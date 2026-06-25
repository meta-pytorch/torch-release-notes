
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
- `StorageImpl`'s built-in copy-on-write (COW) materialization is replaced by a pluggable materializer hook ([#179063](https://github.com/pytorch/pytorch/pull/179063))

  `StorageImpl` no longer knows about COW directly. Its internal COW entry points
  `StorageImpl::is_cow()`, `StorageImpl::maybe_materialize_cow()`, and the friend
  `cow::materialize_cow_storage()` have been removed in favor of a single pluggable
  `MaterializeFn` hook (`void(*)(StorageImpl*)`) that a backend registers to run once,
  on the first mutable data-pointer access. COW is now just one consumer of this hook
  (`c10::impl::cow::materialize_cow`), and all COW behavior (lazy clone, refcounted
  shared data, copy-on-write) is unchanged. This also gives accelerator backends and
  eager-mode graph compilers a zero-fast-path-cost place to commit deferred allocations
  or materialize symbolic buffers on first mutation.

  This is a C++-only change. It affects out-of-tree backends/extensions that called the
  removed `StorageImpl` COW symbols directly; they will fail to compile against 2.13
  with errors such as `no member named 'is_cow' in 'c10::StorageImpl'`. Migrate to the
  new hook API (`set_materializer()` / `has_materializer()` / `clear_materializer()`).

  Version 2.12:
  ```cpp
  // Detect a COW storage and force it to materialize.
  if (storage.is_cow()) {
    storage.maybe_materialize_cow();
  }
  ```

  Version 2.13:
  ```cpp
  // Register a one-shot materializer; it runs on the next mutable-data access
  // and then clears itself. COW registers c10::impl::cow::materialize_cow this way.
  storage.set_materializer(&my_backend_materialize);  // void(StorageImpl*)

  // `has_materializer()` replaces `is_cow()` for "is a deferred materialization pending?"
  if (storage.has_materializer()) { /* ... */ }
  ```
- The minimum supported NCCL version is now 2.23 ([#186292](https://github.com/pytorch/pytorch/pull/186292))

  PyTorch now requires NCCL >= 2.23 at compile time, and the preprocessor/runtime gates that guarded NCCL features introduced in 2.23 or earlier have been removed. Users who build PyTorch from source against a system NCCL older than 2.23 will hit compile errors against the dropped gates. Upgrade the NCCL installation to >= 2.23 to build. The prebuilt PyTorch wheels already bundle a compatible NCCL, so pip/conda users are unaffected.
### deprecation
- Rename distributed collective ops to the `_single` naming scheme and deprecate the old names ([#186123](https://github.com/pytorch/pytorch/pull/186123), [#186124](https://github.com/pytorch/pytorch/pull/186124))

  To align the public `torch.distributed` collective APIs with the naming used by torchcomms' `TorchCommBackend`, `all_gather_into_tensor` is renamed to `all_gather_single` and `reduce_scatter_tensor` to `reduce_scatter_single`. The previous names continue to work as thin wrappers that delegate to the new functions, but now emit a `FutureWarning`.

  Version 2.12:
  ```python
  dist.all_gather_into_tensor(output, input)
  dist.reduce_scatter_tensor(output, input)
  ```

  Version 2.13:
  ```python
  dist.all_gather_single(output, input)
  dist.reduce_scatter_single(output, input)
  ```
### new features
- Add a registration API for symmetric memory arguments (`lib.register_symm_mem_args()`), letting operators (including out-of-tree ops) declare which arguments require symmetric-memory allocation ([#173513](https://github.com/pytorch/pytorch/pull/173513))
- Remove `NCCLSymmetricMemory`'s explicit dependency on `ProcessGroupNCCL`, enabling symmetric memory to work with out-of-tree backends such as torchcomms ([#184260](https://github.com/pytorch/pytorch/pull/184260))
- Support accessing the `ReduceOp.PREMUL_SUM` factor from Python when implementing process group backends in Python ([#185863](https://github.com/pytorch/pytorch/pull/185863))
- Expose the NCCL 2.30 `maxP2pPeers` config binding ([#181686](https://github.com/pytorch/pytorch/pull/181686))
### improvements
- When TorchComms is enabled, route `new_group` through `split_group` for subgroup creation, raising `NotImplementedError` for arguments `split_group` cannot honor (e.g. `use_local_synchronization=True`, `sort_ranks=False`) instead of silently falling back ([#185416](https://github.com/pytorch/pytorch/pull/185416))
- Delegate `dist.new_group` to custom process group subclasses ([#184262](https://github.com/pytorch/pytorch/pull/184262))
- Surface started-work metadata in NCCL watchdog timeouts ([#183656](https://github.com/pytorch/pytorch/pull/183656))
- Add a health check endpoint to the distributed debug server ([#179326](https://github.com/pytorch/pytorch/pull/179326))
### bug fixes
- Fix `NCCLComm::abort()` to use the correct deregister API for window-registered handles ([#181626](https://github.com/pytorch/pytorch/pull/181626))
- Fix `FakeProcessGroup` all_gather on tensors that require grad ([#181790](https://github.com/pytorch/pytorch/pull/181790))
- Fix gather and allgather_coalesced on `FakeProcessGroup` to copy input to output ([#182364](https://github.com/pytorch/pytorch/pull/182364))
- Fix the scatter and reduce_scatter family on `FakeProcessGroup` to copy input to output ([#182365](https://github.com/pytorch/pytorch/pull/182365))
- Fix all_to_all on `FakeProcessGroup` and validate splits ([#182366](https://github.com/pytorch/pytorch/pull/182366))
- Fix conflict between `broadcast_buffers` and `init_sync` in DDP ([#178054](https://github.com/pytorch/pytorch/pull/178054))
- Fix gather on non-destination ranks for the TorchComms backend ([#178533](https://github.com/pytorch/pytorch/pull/178533))
- Fix TCPStore compilation with Clang 20 ([#185785](https://github.com/pytorch/pytorch/pull/185785))
- Fix NCCL symmetric memory mismatch by using an allocation-time counter instead of address for block ordering ([#183489](https://github.com/pytorch/pytorch/pull/183489))
- Fix a symbol lookup issue with the symmetric memory `__init__` ([#186416](https://github.com/pytorch/pytorch/pull/186416))
- Fix the value returned by `Work.exception()` so the exception can be inspected from Python instead of being unusable ([#184697](https://github.com/pytorch/pytorch/pull/184697))
- Fix false assertion errors in the flight recorder when using the `ncclx`, `gloo`, `rccl`, `rcclx`, `mccl`, or `hccl` backends ([#179753](https://github.com/pytorch/pytorch/pull/179753))
- Fix a failure when creating a subgroup on a fake backend via `new_group`, which has no underlying communicator to split ([#186172](https://github.com/pytorch/pytorch/pull/186172))
- Fix `torch.compile` of the `_c10d_functional` `all_gather_tensor_out` and `reduce_scatter_tensor_out` ops, which previously failed functionalization with "Found a custom (non-ATen) operator whose output has alias annotations" ([#183597](https://github.com/pytorch/pytorch/pull/183597))
- Fix `split_group` on multi-backend process groups (e.g. `init_process_group(backend="cpu:gloo,cuda:nccl")`) to split only the relevant backend instead of every backend, avoiding spurious warnings, extra rendezvous overhead, and inconsistent process-group shapes ([#182057](https://github.com/pytorch/pytorch/pull/182057))
- Fix `FakeProcessGroup` to reject `rank >= world_size` at construction time, which previously failed silently and only surfaced later when collectives indexed past `world_size` ([#182363](https://github.com/pytorch/pytorch/pull/182363))
### performance
- Speed up store-based metadata exchange on `TCPStore` by using `multiGet` and a server-side `barrier`, reducing network round trips from `2*(world_size-1)` to `1` ([#182132](https://github.com/pytorch/pytorch/pull/182132))
- Coalesce the NCCL buffer and signal pad into a single symmetric-memory allocation so window registration runs only once ([#183344](https://github.com/pytorch/pytorch/pull/183344))
### docs
- Improve the wording of the `batch_isend_irecv` documentation ([#183022](https://github.com/pytorch/pytorch/pull/183022))
- Add documentation for 8 functions in `distributed.md` ([#182544](https://github.com/pytorch/pytorch/pull/182544))
- Add TorchComms backend documentation to `torch.distributed` ([#182711](https://github.com/pytorch/pytorch/pull/182711))
- Add a distributed training integration guide for out-of-tree accelerators ([#182308](https://github.com/pytorch/pytorch/pull/182308))
### devs
- Add a missing include to `GlooDeviceFactory.cpp` ([#182800](https://github.com/pytorch/pytorch/pull/182800))
- Fix a missing `#include <cuda.h>` in `CUDASymmetricMemoryTypes.hpp` ([#183704](https://github.com/pytorch/pytorch/pull/183704))
### not user facing
- Enforce 2-level layouts in `DeviceMesh` by refactoring the internal layout representation into the private `_FlatLayout`/`_ListOfFlatLayouts` helpers (no public API or behavior change) ([#181223](https://github.com/pytorch/pytorch/pull/181223))
- Remove custom `_c10d_functional_autograd` implementations in favor of redirects to the standard functional collectives (backward-compatible, no user-visible change) ([#172792](https://github.com/pytorch/pytorch/pull/172792))
- Clean up duplicated process-group setup code ([#184374](https://github.com/pytorch/pytorch/pull/184374))
- Address warning of unreachable-code-return after `TORCH_INTERNAL_ASSERT_DEBUG_ONLY` ([#180279](https://github.com/pytorch/pytorch/pull/180279))
- Fix missing sub-oncall when distributed module has already been added ([#181927](https://github.com/pytorch/pytorch/pull/181927))
- Fix "fist" -> "first" typo in comments ([#181931](https://github.com/pytorch/pytorch/pull/181931))
- Fix possessive "its" and "other than" typos in comments and docstrings ([#181986](https://github.com/pytorch/pytorch/pull/181986))
- Fix typo "constrains" -> "constraints" in FlightRecorder.hpp ([#182686](https://github.com/pytorch/pytorch/pull/182686))
- Fix typos across autograd, distributed, and export modules ([#182771](https://github.com/pytorch/pytorch/pull/182771))
- Fix "its" to "it's" contractions in comments and docstrings ([#185720](https://github.com/pytorch/pytorch/pull/185720))
- Fix typos in sharded embedding op docstrings ([#181985](https://github.com/pytorch/pytorch/pull/181985))
- [docs] fixing docs misspellings ([#179801](https://github.com/pytorch/pytorch/pull/179801))
- [xpu][fix] Fix hard code UT failed on XPU ([#180647](https://github.com/pytorch/pytorch/pull/180647))
- [XPU][Test] Migrate 6 UT test suites for Intel GPU ([#174370](https://github.com/pytorch/pytorch/pull/174370))
- [PGNCCL][Symmetric Memory][IntraNodeComm] Add parameterization to `test_intra_node_comm_all_reduce` ([#181331](https://github.com/pytorch/pytorch/pull/181331))
- align all estimations across ranks ([#181105](https://github.com/pytorch/pytorch/pull/181105))
- [DeviceMesh] Use hashed PG names for fake backend when torchcomms is enabled ([#181929](https://github.com/pytorch/pytorch/pull/181929))
- [CUDA] Fix CUDA IPC deserialization mismatch with `expandable_segments` on `FABRIC_HANDLE` ([#179618](https://github.com/pytorch/pytorch/pull/179618))
- Simplify WorkerServer with nlohmann json ([#177460](https://github.com/pytorch/pytorch/pull/177460))
- Fix flaky TestFunctionalAutograd by switching to LocalTensorMode ([#182665](https://github.com/pytorch/pytorch/pull/182665))
- Fix import of _debug_handlers in test_debug.py ([#182442](https://github.com/pytorch/pytorch/pull/182442))
- NCCL Symm mem tests ([#182445](https://github.com/pytorch/pytorch/pull/182445))
- Allow Dynamo to trace _maybe_view_chunk_cat and restore skipIfHpu on test_functional_api ([#182435](https://github.com/pytorch/pytorch/pull/182435))
- adds missing vector header in Handlers.hpp ([#183058](https://github.com/pytorch/pytorch/pull/183058))
- [OpenReg][distributed] Refactor OCCL backend registration ([#183257](https://github.com/pytorch/pytorch/pull/183257))
- Consolidate and streamline skip and xfail functionality in tests ([#183541](https://github.com/pytorch/pytorch/pull/183541))
- [NCCL][Symmetric Memory] Add test with CUDA Graph ([#184527](https://github.com/pytorch/pytorch/pull/184527))
- Fix check for `aiohttp` in tests ([#184544](https://github.com/pytorch/pytorch/pull/184544))
- Use extern op metadata for runtime benchmarks ([#184138](https://github.com/pytorch/pytorch/pull/184138))
- Narrow OpInfo skips from #185013 to per-op entries ([#185307](https://github.com/pytorch/pytorch/pull/185307))
- Remove useless `gpus_for_rank()` ([#185194](https://github.com/pytorch/pytorch/pull/185194))
- Split linear_cross_entropy OpInfo into unchunked and chunked variants ([#184596](https://github.com/pytorch/pytorch/pull/184596))
- Fix call to fork_rng by specifying device type ([#180512](https://github.com/pytorch/pytorch/pull/180512))
- Normalize device_type in distributed reordering/logger tests ([#186169](https://github.com/pytorch/pytorch/pull/186169))
- Undo the reduce_scatter_single migration in UCC tests ([#186666](https://github.com/pytorch/pytorch/pull/186666))
- Modernize some CUDA kernels ([#184393](https://github.com/pytorch/pytorch/pull/184393))
- [tcomms-shim] Tests for torchcomms backed cuda symm mem ([#184523](https://github.com/pytorch/pytorch/pull/184523))
- Make `LocalTensorMode` work with compile_on_one_rank functional collectives and runtime mesh coordinates ([#184782](https://github.com/pytorch/pytorch/pull/184782))
### security
