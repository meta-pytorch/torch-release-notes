
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

- Add a migration flag to route `new_group` through `split_group`, warning of the upcoming change ([#185416](https://github.com/pytorch/pytorch/pull/185416))

  To unblock migrating callers from `new_group` to `split_group`, a new opt-in flag `torch.distributed.config.new_group_use_split_group` (env var `TORCH_DIST_NEW_GROUP_USE_SPLIT_GROUP`, default `False`) routes `new_group` through `split_group` on the default process group. The legacy path remains the default and a warning is emitted about the upcoming change.

  ```python
  import torch.distributed as dist
  dist.config.new_group_use_split_group = True  # opt in to split_group-backed new_group
  pg = dist.new_group(ranks=[0, 1])
  ```

### new features
- Add a registration API for symmetric memory arguments (`lib.register_symm_mem_args()`), letting operators (including out-of-tree ops) declare which arguments require symmetric-memory allocation ([#173513](https://github.com/pytorch/pytorch/pull/173513))
- Remove `NCCLSymmetricMemory`'s explicit dependency on `ProcessGroupNCCL`, enabling symmetric memory to work with out-of-tree backends such as torchcomms ([#184260](https://github.com/pytorch/pytorch/pull/184260))
- [FSDP2] Add `FSDPModule.set_separate_reduce_scatter_group` to give reduce-scatter its own communicator for opt-in all-gather / reduce-scatter overlap ([#186335](https://github.com/pytorch/pytorch/pull/186335))
- [FSDP2] Add `set_reduce_scatter_max_input_buffers` to keep multiple reduce-scatter input buffers in flight and mitigate reduce-scatter blocking backward compute ([#186000](https://github.com/pytorch/pytorch/pull/186000))
- `c10d`: return a typed Python exception from `Work.exception()` ([#184697](https://github.com/pytorch/pytorch/pull/184697))
- `c10d`/`ReduceOp`: support accessing the `PREMUL_SUM` factor from Python when implementing process group backends in Python ([#185863](https://github.com/pytorch/pytorch/pull/185863))
- Expose new NCCL v2.30 `maxP2pPeers` config bindings ([#181686](https://github.com/pytorch/pytorch/pull/181686))
- Delegate `dist.new_group` to custom process group subclasses ([#184262](https://github.com/pytorch/pytorch/pull/184262))
- Add `linear_cross_entropy` with chunking along the batch dimension ([#185852](https://github.com/pytorch/pytorch/pull/185852))
- [DCP] Forward the FSDP process group to optimizer state-dict APIs ([#181261](https://github.com/pytorch/pytorch/pull/181261))
- Add a health check to the debug server ([#179326](https://github.com/pytorch/pytorch/pull/179326))
- Support all backends in Flight Recorder ([#179753](https://github.com/pytorch/pytorch/pull/179753))
- [PP] Support extra `loss_fn` kwargs in pipeline schedules ([#181057](https://github.com/pytorch/pytorch/pull/181057))
- [DTensor] Add sharding support for the `scatter` op ([#186149](https://github.com/pytorch/pytorch/pull/186149))

### improvements
- [DTensor] Migrate embedding ops to single-dim strategies ([#180281](https://github.com/pytorch/pytorch/pull/180281))
- [DTensor] Migrate random ops to single-dim strategies and increase op coverage ([#180503](https://github.com/pytorch/pytorch/pull/180503))
- [DTensor] Add single-dim strategy auto-infrastructure ([#185386](https://github.com/pytorch/pytorch/pull/185386))
- [DTensor] Register sharding strategies for upsample/interpolation backward ops ([#180311](https://github.com/pytorch/pytorch/pull/180311))
- [DTensor] Add sharding strategies for anti-aliased upsample ops ([#184626](https://github.com/pytorch/pytorch/pull/184626))
- [DTensor] Add a sharding strategy for batch norm backward ([#182743](https://github.com/pytorch/pytorch/pull/182743))
- [DTensor] Register a sharding strategy for `aten.detach_.default` ([#181876](https://github.com/pytorch/pytorch/pull/181876))
- [DTensor] Prevent `squeeze` from redistributing with `strict_view` ([#175798](https://github.com/pytorch/pytorch/pull/175798))
- [DTensor] Make local tensor contiguous after an uneven Shard->Replicate redistribute ([#184443](https://github.com/pytorch/pytorch/pull/184443))
- [DTensor] Don't trace shard propagation into `make_fx` graphs ([#185865](https://github.com/pytorch/pytorch/pull/185865))
- [Context Parallel] Handle short-sequence load balancing ([#183968](https://github.com/pytorch/pytorch/pull/183968))
- [FSDP2] Support partial forward of `[norm, head]` for chunked loss ([#180428](https://github.com/pytorch/pytorch/pull/180428))
- [FSDP2] Support input JVP through `replicate` ([#182732](https://github.com/pytorch/pytorch/pull/182732))
- [FSDP2] Warn when a forward output is a view tensor ([#181850](https://github.com/pytorch/pytorch/pull/181850))
- [FSDP] Flatten multi-dim DP shard axes in the sharding spec ([#183629](https://github.com/pytorch/pytorch/pull/183629))
- [FSDP] Cast forward inputs during activation-checkpoint recompute ([#182580](https://github.com/pytorch/pytorch/pull/182580))
- [Full DTensor][FSDP] Use `_StridedShard` when TP exists ([#186126](https://github.com/pytorch/pytorch/pull/186126))
- [c10d] Use `multiGet` and a store barrier in `StoreExchange` ([#182132](https://github.com/pytorch/pytorch/pull/182132))
- [c10d] Surface started-work metadata in NCCL watchdog timeouts ([#183656](https://github.com/pytorch/pytorch/pull/183656))
- [c10d] Clean up duplicated process-group setup code ([#184374](https://github.com/pytorch/pytorch/pull/184374))
- [c10d] Don't call `split_group` for the fake backend ([#186172](https://github.com/pytorch/pytorch/pull/186172))
- [c10d][symm_mem] Coalesce the NCCL buffer and signal pad into a single allocation ([#183344](https://github.com/pytorch/pytorch/pull/183344))
- Require NCCL >= 2.23 and drop version gates for older NCCL ([#186292](https://github.com/pytorch/pytorch/pull/186292))
- Tag `_c10d_functional` `all_gather_tensor_out`/`reduce_scatter_tensor_out` as out variants ([#183597](https://github.com/pytorch/pytorch/pull/183597))
- Remove custom `_c10d_functional_autograd` implementations in favor of redirects ([#172792](https://github.com/pytorch/pytorch/pull/172792))
- Fix the `split_group` API to align with torchcomms ([#182057](https://github.com/pytorch/pytorch/pull/182057))
- [torchelastic] Start the health check server before `remote_pre_launch` in the APF executor ([#180543](https://github.com/pytorch/pytorch/pull/180543))
- [torchelastic] Handle d-state processes ([#185414](https://github.com/pytorch/pytorch/pull/185414))
- [DeviceMesh] Enforce 2-level layouts ([#181223](https://github.com/pytorch/pytorch/pull/181223))
- Defer pipeline RECV ops with rank-parity deadlock avoidance ([#178815](https://github.com/pytorch/pytorch/pull/178815))
- Validate rank/size in the `FakeProcessGroup` constructor ([#182363](https://github.com/pytorch/pytorch/pull/182363))
- [DCP] Fixes `DefaultStager` crash when reused ([#183424](https://github.com/pytorch/pytorch/pull/183424))

### bug fixes
- [FSDP2] Fix `post_accumulate_grad_hook` staleness under `CPUOffloadPolicy` ([#180666](https://github.com/pytorch/pytorch/pull/180666))
- [FSDP2] Fix unused DTensor param reduce-scatter ([#183040](https://github.com/pytorch/pytorch/pull/183040))
- [FSDP2] Fix no-input forward handling ([#183943](https://github.com/pytorch/pytorch/pull/183943))
- [FSDP] Remove redundant stream waits ([#183983](https://github.com/pytorch/pytorch/pull/183983))
- [FSDP][composability] Fix TP + FSDP + mixed precision bug ([#183805](https://github.com/pytorch/pytorch/pull/183805))
- [DTensor] Fix `Partial` placement lost during the autograd layout invariant ([#180511](https://github.com/pytorch/pytorch/pull/180511))
- [DTensor] Fix `OpSpec.mesh` crash when specs contain `None` entries ([#181541](https://github.com/pytorch/pytorch/pull/181541))
- [DTensor] Fix `redistribute(backward_dtype=...)` ignoring the backward dtype ([#182032](https://github.com/pytorch/pytorch/pull/182032))
- [DTensor] Fix `_StridedShard` flag conflict during gradient accumulation ([#183517](https://github.com/pytorch/pytorch/pull/183517))
- [DTensor] Fix reduction strategy linearity ([#183794](https://github.com/pytorch/pytorch/pull/183794))
- [DTensor] Fix the cache key hashing for fake meshes ([#184001](https://github.com/pytorch/pytorch/pull/184001))
- [DTensor] Fix `FakeTensor` device hint in sharding propagation ([#183970](https://github.com/pytorch/pytorch/pull/183970))
- [DTensor] Fix `group_norm` scalar adjuster crash when `weight=None` ([#184819](https://github.com/pytorch/pytorch/pull/184819))
- [DTensor] `to_local()` no longer drops the `_is_param` marker that `nn.Parameter` sets on custom tensors ([#184422](https://github.com/pytorch/pytorch/pull/184422))
- Fix `pad_tensor`/`unpad_tensor` creating unnecessary guards on symbolic pad sizes during tracing ([#180887](https://github.com/pytorch/pytorch/pull/180887))
- Fix `NCCLComm::abort()` to use the correct deregister API for window-registered handles ([#181626](https://github.com/pytorch/pytorch/pull/181626))
- Fix `FakeProcessGroup` allgather on tensors that require grad ([#181790](https://github.com/pytorch/pytorch/pull/181790))
- Fix gather/allgather_coalesced on `FakeProcessGroup` to copy input to output ([#182364](https://github.com/pytorch/pytorch/pull/182364))
- Fix scatter/reduce_scatter family on `FakeProcessGroup` to copy input to output ([#182365](https://github.com/pytorch/pytorch/pull/182365))
- Fix alltoall on `FakeProcessGroup`, validate splits, and clean up DTensor xfails ([#182366](https://github.com/pytorch/pytorch/pull/182366))
- Fix the torchcomms-backed device mesh tests ([#181747](https://github.com/pytorch/pytorch/pull/181747))
- dist/c10d: Add TorchComms backend c10d tests and fix gather on non-dst ranks ([#178533](https://github.com/pytorch/pytorch/pull/178533))
- Fix conflict between `broadcast_buffers` and `init_sync` (DDP) ([#178054](https://github.com/pytorch/pytorch/pull/178054))
- [c10d] Fix TCPStore compilation with Clang 20 ([#185785](https://github.com/pytorch/pytorch/pull/185785))
- [distributed] Fix `AssertionError` in elastic c10d rendezvous when rank changes ([#182375](https://github.com/pytorch/pytorch/pull/182375))
- Reland: fix the c10d issue from #178362 ([#183489](https://github.com/pytorch/pytorch/pull/183489))
- Fix the symbol lookup issue with symmetric memory `__init__` ([#186416](https://github.com/pytorch/pytorch/pull/186416))
- [ROCm] Add a version guard to the ROCm workaround for watchdog polling during graph capture ([#179780](https://github.com/pytorch/pytorch/pull/179780))

### performance
### docs
- [Docathon] Convert `elastic/quickstart.rst` from rST to MyST Markdown ([#182569](https://github.com/pytorch/pytorch/pull/182569))
- [Docathon] Convert `rpc/rref.rst` from rST to MyST Markdown ([#182877](https://github.com/pytorch/pytorch/pull/182877))
- Clarify default dtype behavior in the `DTensor.redistribute` docstring ([#181671](https://github.com/pytorch/pytorch/pull/181671))
- [distributed] Clarify that `--node-rank` is only used with static rendezvous ([#182374](https://github.com/pytorch/pytorch/pull/182374))
- Improve the wording of the `batch_isend_irecv` docs ([#183022](https://github.com/pytorch/pytorch/pull/183022))
- Document undocumented functions in `distributed.fsdp.fully_shard.md` ([#182866](https://github.com/pytorch/pytorch/pull/182866))
- [Docathon] Document undocumented functions in `distributed.checkpoint.md` ([#182887](https://github.com/pytorch/pytorch/pull/182887))

### devs
- [ROCm] Use CMake native HIP language support (`enable_language(HIP)`) ([#180485](https://github.com/pytorch/pytorch/pull/180485))
- Add a missing include to `GlooDeviceFactory.cpp` ([#182800](https://github.com/pytorch/pytorch/pull/182800))
- [SymmMem] Fix a missing `#include <cuda.h>` in `CUDASymmetricMemoryTypes.hpp` ([#183704](https://github.com/pytorch/pytorch/pull/183704))

### not user facing
- [pytorch] Address warning of unreachable-code-return after `TORCH_INTERNAL_ASSERT_DEBUG_ONLY` ([#180279](https://github.com/pytorch/pytorch/pull/180279))
- Remove unused noqa directives in `torch/`, batch 1 ([#180134](https://github.com/pytorch/pytorch/pull/180134))
- Remove unused noqa directives in `torch/`, batch 4 ([#180138](https://github.com/pytorch/pytorch/pull/180138))
- [claude][skill] distributed triaging sub-skill ([#180401](https://github.com/pytorch/pytorch/pull/180401))
- [claude][skill] getting rid of redundant ptd-bot-triaged label ([#185537](https://github.com/pytorch/pytorch/pull/185537))
- [claude][skill] fixing missing sub-oncall when distributed module has already been added ([#181927](https://github.com/pytorch/pytorch/pull/181927))
- Fix "fist" -> "first" typo in comments ([#181931](https://github.com/pytorch/pytorch/pull/181931))
- Fix typos in comments, docstrings, and error messages ([#181990](https://github.com/pytorch/pytorch/pull/181990))
- Fix possessive "its" and "other than" typos in comments and docstrings ([#181986](https://github.com/pytorch/pytorch/pull/181986))
- Fix article typos: "an" before consonant sounds -> "a" ([#182302](https://github.com/pytorch/pytorch/pull/182302))
- Fix typo "constrains" -> "constraints" in FlightRecorder.hpp ([#182686](https://github.com/pytorch/pytorch/pull/182686))
- Fix typos across autograd, distributed, and export modules ([#182771](https://github.com/pytorch/pytorch/pull/182771))
- Fix typos in distributed and data loading modules ([#183326](https://github.com/pytorch/pytorch/pull/183326))
- Fix "its" to "it's" contractions in comments and docstrings ([#185720](https://github.com/pytorch/pytorch/pull/185720))
- Fix typos in sharded embedding op docstrings ([#181985](https://github.com/pytorch/pytorch/pull/181985))
- [docs] fixing docs misspellings ([#179801](https://github.com/pytorch/pytorch/pull/179801))
- [xpu][fix] Fix hard code UT failed on XPU ([#180647](https://github.com/pytorch/pytorch/pull/180647))
- [reland][xpu][test] Port distributed checkpoint test cases on Intel GPU ([#182425](https://github.com/pytorch/pytorch/pull/182425))
- [xpu][test] Port distributed _shard tests cases on Intel GPUs ([#180881](https://github.com/pytorch/pytorch/pull/180881))
- [XPU][Test] Migrate 6 UT test suites for Intel GPU ([#174370](https://github.com/pytorch/pytorch/pull/174370))
- [PGNCCL][Symmetric Memory][IntraNodeComm] Add parameterization to `test_intra_node_comm_all_reduce` ([#181331](https://github.com/pytorch/pytorch/pull/181331))
- [overlap] pre-bucketing of fsdp collectives ([#179935](https://github.com/pytorch/pytorch/pull/179935))
- align all estimations across ranks ([#181105](https://github.com/pytorch/pytorch/pull/181105))
- [DeviceMesh] Use hashed PG names for fake backend when torchcomms is enabled ([#181929](https://github.com/pytorch/pytorch/pull/181929))
- [DTensor][BugFix] Fix DTensor + AC + compile crash: unbound inner symbol at root tracer ([#181797](https://github.com/pytorch/pytorch/pull/181797))
- [CUDA] Fix CUDA IPC deserialization mismatch with `expandable_segments` on `FABRIC_HANDLE` ([#179618](https://github.com/pytorch/pytorch/pull/179618))
- [BE]: Simplify WorkerServer with nlohmann json ([#177460](https://github.com/pytorch/pytorch/pull/177460))
- [DTensor] Make DTensor OpStrategy stringification handle missing mesh ([#182371](https://github.com/pytorch/pytorch/pull/182371))
- [docs] Add documentation for 8 functions in distributed.md ([#182544](https://github.com/pytorch/pytorch/pull/182544))
- [distributed] Fix flaky TestFunctionalAutograd by switching to LocalTensorMode ([#182665](https://github.com/pytorch/pytorch/pull/182665))
- Fix import of _debug_handlers in test_debug.py ([#182442](https://github.com/pytorch/pytorch/pull/182442))
- [DTensor]: add backward gradient verification to test_single_dim_strategy ([#182558](https://github.com/pytorch/pytorch/pull/182558))
- Add TorchComms backend docs to torch.distributed ([#182711](https://github.com/pytorch/pytorch/pull/182711))
- Convert rpc/distributed_autograd.rst from rST to MyST Markdown ([#182926](https://github.com/pytorch/pytorch/pull/182926))
- Skip ROCm MI300 mixed precision norm tests ([#182773](https://github.com/pytorch/pytorch/pull/182773))
- [FSDP] Fix CUDA memory leak check failure in test_fsdp_apply ([#182774](https://github.com/pytorch/pytorch/pull/182774))
- NCCL Symm mem tests ([#182445](https://github.com/pytorch/pytorch/pull/182445))
- Allow Dynamo to trace _maybe_view_chunk_cat and restore skipIfHpu on test_functional_api ([#182435](https://github.com/pytorch/pytorch/pull/182435))
- adds missing vector header in Handlers.hpp ([#183058](https://github.com/pytorch/pytorch/pull/183058))
- [BE][Ez]: Add missing typing vars for decorators. Prevent type erasure ([#183116](https://github.com/pytorch/pytorch/pull/183116))
- [BE][Ez]: Fix type erasure due to missing Callable annotation for decorator ([#182990](https://github.com/pytorch/pytorch/pull/182990))
- [OpenReg][distributed] Refactor OCCL backend registration ([#183257](https://github.com/pytorch/pytorch/pull/183257))
- documented undocumented functions in distributed.optim.md ([#182871](https://github.com/pytorch/pytorch/pull/182871))
- Fix pipelining crash when split_module interleaves get_attr with placeholder ([#182644](https://github.com/pytorch/pytorch/pull/182644))
- [Docathon] Document undocumented functions in distributed.tensor.parallel.md ([#182876](https://github.com/pytorch/pytorch/pull/182876))
- [ROCm] Refactor TestSACILP.test_sac_ilp_case1 to be hardware independent ([#182670](https://github.com/pytorch/pytorch/pull/182670))
- [Docathon] Document undocumented functions in rpc.md ([#183393](https://github.com/pytorch/pytorch/pull/183393))
- Add distributed training integration doc for OOT accelerators ([#182308](https://github.com/pytorch/pytorch/pull/182308))
- [Test] Consolidate and streamline skip and xfail functionality in tests ([#183541](https://github.com/pytorch/pytorch/pull/183541))
- Guard pipeline schedule adjacency ([#179293](https://github.com/pytorch/pytorch/pull/179293))
- [NCCL][Symmetric Memory] Add test with CUDA Graph ([#184527](https://github.com/pytorch/pytorch/pull/184527))
- Fix shared-weight gradient double-counting in zero-bubble pipeline schedules ([#181365](https://github.com/pytorch/pytorch/pull/181365))
- Fix check for `aiohttp` in tests ([#184544](https://github.com/pytorch/pytorch/pull/184544))
- Use extern op metadata for runtime benchmarks ([#184138](https://github.com/pytorch/pytorch/pull/184138))
- [ROCm] Fix skipIfRocm erroring instead of skipping on continuous tests ([#185275](https://github.com/pytorch/pytorch/pull/185275))
- Narrow OpInfo skips from #185013 to per-op entries ([#185307](https://github.com/pytorch/pytorch/pull/185307))
- [Test] Remove useless `gpus_for_rank()` ([#185194](https://github.com/pytorch/pytorch/pull/185194))
- [ROCm] Skip test_compile_multiple_random_ops on ROCm ([#185522](https://github.com/pytorch/pytorch/pull/185522))
- [reland][compile] fix diagonal_scatter backward ([#185146](https://github.com/pytorch/pytorch/pull/185146))
- [DDE] Fix data-dependent errors in pixel_shuffle, pdist, and padding ops ([#183814](https://github.com/pytorch/pytorch/pull/183814))
- Split linear_cross_entropy OpInfo into unchunked and chunked variants ([#184596](https://github.com/pytorch/pytorch/pull/184596))
- Fix call to fork_rng by specifying device type ([#180512](https://github.com/pytorch/pytorch/pull/180512))
- Fix missing stride() call in test_redistribute TensorMeta ([#186170](https://github.com/pytorch/pytorch/pull/186170))
- Normalize device_type in distributed reordering/logger tests ([#186169](https://github.com/pytorch/pytorch/pull/186169))
- [Overlap Scheduling] Fix SymInt crash in collective/compute node benchmarking ([#186065](https://github.com/pytorch/pytorch/pull/186065))
- UCC/test: Undo migration to reduce_scatter_single ([#186666](https://github.com/pytorch/pytorch/pull/186666))
- [pipelining] Fix None gradient handling in backward send/recv ([#182182](https://github.com/pytorch/pytorch/pull/182182))
- [ROCm] Guard NCCL device reduce-copy support on symmetric-memory device APIs ([#186794](https://github.com/pytorch/pytorch/pull/186794))
- [pipelining] Add guards for non-float tensors when building pipeline ([#183582](https://github.com/pytorch/pytorch/pull/183582))
- Inline DISABLED-test skips from the auto-disabler JSON into source ([#185013](https://github.com/pytorch/pytorch/pull/185013))
- Drop dead CUDA/ROCm version gates from tests and helpers ([#184879](https://github.com/pytorch/pytorch/pull/184879))
- Clean up unused variables, redundant casts and namespaces in CUDA kernels ([#185040](https://github.com/pytorch/pytorch/pull/185040))
- Modernize some CUDA kernels ([#184393](https://github.com/pytorch/pytorch/pull/184393))
- [tcomms-shim] Tests for torchcomms backed cuda symm mem ([#184523](https://github.com/pytorch/pytorch/pull/184523))
- Make `LocalTensorMode` work with compile_on_one_rank functional collectives and runtime mesh coordinates ([#184782](https://github.com/pytorch/pytorch/pull/184782))

### security
