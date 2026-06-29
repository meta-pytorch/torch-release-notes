
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
- [FSDP] Fix alias annotation for fsdp::all_gather_copy_in ([#177170](https://github.com/pytorch/pytorch/pull/177170))
- Add pluggable MaterializeFn hook to StorageImpl ([#179063](https://github.com/pytorch/pytorch/pull/179063))
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
- [Docathon] Convert elastic/quickstart.rst from rST to MyST Markdown ([#182569](https://github.com/pytorch/pytorch/pull/182569))
- [Docathon] Convert rpc/rref.rst from rST to MyST Markdown #182504 ([#182877](https://github.com/pytorch/pytorch/pull/182877))
### devs
### Untopiced
- [dtensor][resubmit] migrating embedding ops to single dim strategies ([#180281](https://github.com/pytorch/pytorch/pull/180281))
- [pytorch] Address warning of unreachable-code-return after TORCH_INTERNAL_ASSERT_DEBUG_ONLY (#180279) ([#180279](https://github.com/pytorch/pytorch/pull/180279))
- Remove unused noqa directives in torch/, batch 1 ([#180134](https://github.com/pytorch/pytorch/pull/180134))
- Remove unused noqa directives in torch/, batch 4 ([#180138](https://github.com/pytorch/pytorch/pull/180138))
- Fix DTensor Partial placement lost during autograd layout invariant (issue #180486) ([#180511](https://github.com/pytorch/pytorch/pull/180511))
- [torchelastic] Start health check server before remote_pre_launch in APF executor (#180543) ([#180543](https://github.com/pytorch/pytorch/pull/180543))
- [DTensor] Register sharding strategies for upsample/interpolation backward ops ([#180311](https://github.com/pytorch/pytorch/pull/180311))
- [FSDP2] Fix post_accumulate_grad_hook staleness under CPUOffloadPolicy ([#180666](https://github.com/pytorch/pytorch/pull/180666))
- [DTensor] Prevent squeeze from redistributing with strict_view ([#175798](https://github.com/pytorch/pytorch/pull/175798))
- Fix pad_tensor/unpad_tensor creating unnecessary guards on symbolic pad sizes during tracing ([#180887](https://github.com/pytorch/pytorch/pull/180887))
- [DeviceMesh] Enforce 2-level Layouts ([#181223](https://github.com/pytorch/pytorch/pull/181223))
- [dtensor][resubmit] migrating random_ops to single dim strategies and increasing op coverage ([#180503](https://github.com/pytorch/pytorch/pull/180503))
- [PP] Support extra loss_fn kwargs in pipeline schedules ([#181057](https://github.com/pytorch/pytorch/pull/181057))
- [FSDP2] Support partial forward of [norm, head] for chunked loss ([#180428](https://github.com/pytorch/pytorch/pull/180428))
- Fixes NCCLComm::abort() to use correct deregister API for window-registered handles ([#181626](https://github.com/pytorch/pytorch/pull/181626))
- [DTensor] Fix OpSpec.mesh crash when specs contain None entries ([#181541](https://github.com/pytorch/pytorch/pull/181541))
- Fix FakeProcessGroup allgather on tensors that require grad ([#181790](https://github.com/pytorch/pytorch/pull/181790))
- [claude][skill] distribute triaging sub-skill ([#180401](https://github.com/pytorch/pytorch/pull/180401))
- Clarify default dtype behavior in DTensor.redistribute docstring ([#181671](https://github.com/pytorch/pytorch/pull/181671))
- [dtensor] Register sharding strategy for aten.detach_.default ([#181876](https://github.com/pytorch/pytorch/pull/181876))
- Defer pipeline RECV ops with rank-parity deadlock avoidance (#172668) ([#178815](https://github.com/pytorch/pytorch/pull/178815))
- Fix the torchcomms backed device mesh tests ([#181747](https://github.com/pytorch/pytorch/pull/181747))
- Fix "fist" -> "first" typo in comments ([#181931](https://github.com/pytorch/pytorch/pull/181931))
- Fix the split_group API to align with torchcomms ([#182057](https://github.com/pytorch/pytorch/pull/182057))
- Fix typos in comments, docstrings, and error messages ([#181990](https://github.com/pytorch/pytorch/pull/181990))
- Fix possessive "its" and "other than" typos in comments and docstrings ([#181986](https://github.com/pytorch/pytorch/pull/181986))
- [c10d] Use multiGet and store barrier in StoreExchange ([#182132](https://github.com/pytorch/pytorch/pull/182132))
- [dtensor] Fix redistribute(backward_dtype=...) ignoring the backward dtype ([#182032](https://github.com/pytorch/pytorch/pull/182032))
- [distributed] Clarify that --node-rank is only used with static rendezvous ([#182374](https://github.com/pytorch/pytorch/pull/182374))
- [distributed] Fix AssertionError in elastic c10d rendezvous when rank changes ([#182375](https://github.com/pytorch/pytorch/pull/182375))
- Expose new NCCL v2.30 maxP2pPeers nccl config bindings ([#181686](https://github.com/pytorch/pytorch/pull/181686))
- dist/c10d: Add TorchComms backend c10d tests and fix gather on non-dst ranks ([#178533](https://github.com/pytorch/pytorch/pull/178533))
- Functionalize inplace c10d collectives in standalone compile ([#181836](https://github.com/pytorch/pytorch/pull/181836))
- [FSDP2] warn when forward output is a view tensor ([#181850](https://github.com/pytorch/pytorch/pull/181850))
- Fixes conflict between broadcast_buffers and init_sync ([#178054](https://github.com/pytorch/pytorch/pull/178054))
- Plumb ProcessGroup through standalone_compile ([#181964](https://github.com/pytorch/pytorch/pull/181964))
- Fix article typos: "an" before consonant sounds → "a" ([#182302](https://github.com/pytorch/pytorch/pull/182302))
- Fix typo "constrains" → "constraints" in FlightRecorder.hpp ([#182686](https://github.com/pytorch/pytorch/pull/182686))
- [DTensor] add DTensor sharding strategy for batch norm backward ([#182743](https://github.com/pytorch/pytorch/pull/182743))
- Add missing include to `GlooDeviceFactory.cpp` ([#182800](https://github.com/pytorch/pytorch/pull/182800))
- [FSDP] Cast forward inputs during AC recompute ([#182580](https://github.com/pytorch/pytorch/pull/182580))
- [library] Add registration API for symmetric memory arguments ([#173513](https://github.com/pytorch/pytorch/pull/173513))
- [FSDP2] Support input JVP through replicate ([#182732](https://github.com/pytorch/pytorch/pull/182732))
- [BE][Ez]: Fix type erasure due to missing Callable annotation for decorator ([#182990](https://github.com/pytorch/pytorch/pull/182990))
- Fix typos across autograd, distributed, and export modules ([#182771](https://github.com/pytorch/pytorch/pull/182771))
- improve wording of batch_isend_irecv docs ([#183022](https://github.com/pytorch/pytorch/pull/183022))
- [FSDP2] Fix unused DTensor param reduce-scatter ([#183040](https://github.com/pytorch/pytorch/pull/183040))
- Document undocumented functions in distributed.fsdp.fully_shard.md ([#182866](https://github.com/pytorch/pytorch/pull/182866))
- [reland][xpu][test] Port distributed checkpoint test cases on Intel GPU ([#182425](https://github.com/pytorch/pytorch/pull/182425))
- [Docathon] Document undocumented functions in distributed.checkpoint.md (7 functions) ([#182887](https://github.com/pytorch/pytorch/pull/182887))
- Reland #178362 ([#183489](https://github.com/pytorch/pytorch/pull/183489))
- Validate rank/size in FakeProcessGroup constructor ([#182363](https://github.com/pytorch/pytorch/pull/182363))
- Fix gather/allgather_coalesced on FakeProcessGroup to copy input to output ([#182364](https://github.com/pytorch/pytorch/pull/182364))
- Fix scatter/reduce_scatter family on FakeProcessGroup to copy input to output ([#182365](https://github.com/pytorch/pytorch/pull/182365))
- Fix alltoall on FakeProcessGroup, validate splits, clean up dtensor xfails ([#182366](https://github.com/pytorch/pytorch/pull/182366))
- Tag _c10d_functional {all_gather,reduce_scatter}_tensor_out as out variants ([#183597](https://github.com/pytorch/pytorch/pull/183597))
- [DTensor] Fix _StridedShard flag conflict during gradient accumulation ([#183517](https://github.com/pytorch/pytorch/pull/183517))
- Fix typos in distributed and data loading modules ([#183326](https://github.com/pytorch/pytorch/pull/183326))
- [fsdp][composability] fixing tp + fsdp + mixed precision bug ([#183805](https://github.com/pytorch/pytorch/pull/183805))
- [c10d] Surface started-work metadata in NCCL watchdog timeouts ([#183656](https://github.com/pytorch/pytorch/pull/183656))
- Fix DTensor reduction strategy linearity ([#183794](https://github.com/pytorch/pytorch/pull/183794))
- [FSDP] Flatten multi-dim DP shard axes in sharding spec ([#183629](https://github.com/pytorch/pytorch/pull/183629))
- [c10d][symm_mem] Coalesce NCCL buffer + signal pad into a single allocation ([#183344](https://github.com/pytorch/pytorch/pull/183344))
- Fix DTensor cache key hashing for fake meshes ([#184001](https://github.com/pytorch/pytorch/pull/184001))
- [Context Parallel] Handle short sequence load balancing ([#183968](https://github.com/pytorch/pytorch/pull/183968))
- [pytorch] Delegate `dist.new_group` to custom PG subclasses (#184262) ([#184262](https://github.com/pytorch/pytorch/pull/184262))
- [c10d] Cleanup duplicated pg setup code ([#184374](https://github.com/pytorch/pytorch/pull/184374))
- [fsdp] Remove redundant stream waits ([#183983](https://github.com/pytorch/pytorch/pull/183983))
- Fix FakeTensor device hint in DTensor sharding propagation ([#183970](https://github.com/pytorch/pytorch/pull/183970))
- [SymmMem] Fix missing #include <cuda.h> in CUDASymmetricMemoryTypes.hpp (#183704) ([#183704](https://github.com/pytorch/pytorch/pull/183704))
- [fsdp] Fix FSDP2 no-input forward handling ([#183943](https://github.com/pytorch/pytorch/pull/183943))
- [DTensor]: add sharding strategies for anti-aliased upsample ops ([#184626](https://github.com/pytorch/pytorch/pull/184626))
- c10d: return typed Python exception from Work.exception() ([#184697](https://github.com/pytorch/pytorch/pull/184697))
- Modernize some CUDA kernels ([#184393](https://github.com/pytorch/pytorch/pull/184393))
- Make DTensor local tensor contiguous after uneven Shard->Replicate redistribute ([#184443](https://github.com/pytorch/pytorch/pull/184443))
- Make LocalTensorMode work with compile_on_one_rank functional collectives and runtime mesh coordinates ([#184782](https://github.com/pytorch/pytorch/pull/184782))
- Inline DISABLED-test skips from the auto-disabler JSON into source ([#185013](https://github.com/pytorch/pytorch/pull/185013))
- Clean up unused variables, redundant casts and namespaces in CUDA kernels ([#185040](https://github.com/pytorch/pytorch/pull/185040))
- [tcomms-shim] Tests for torchcomms backed cuda symm mem ([#184523](https://github.com/pytorch/pytorch/pull/184523))
- Preserve linalg error checks in AOT graphs ([#184111](https://github.com/pytorch/pytorch/pull/184111))
- c10d/ReduceOp: support accessing PREMUL_SUM factor from Python ([#185863](https://github.com/pytorch/pytorch/pull/185863))
- Add linear_cross_entropy implementation with chunking along batch dimension (3) ([#185852](https://github.com/pytorch/pytorch/pull/185852))
- Fixes DefaultStager crash when reused ([#183424](https://github.com/pytorch/pytorch/pull/183424))
- [DCP] Forward FSDP process group to optimizer state-dict APIs ([#181261](https://github.com/pytorch/pytorch/pull/181261))
- [DTensor] Don't trace shard propagation into make_fx graphs ([#185865](https://github.com/pytorch/pytorch/pull/185865))
- add health check to debug server ([#179326](https://github.com/pytorch/pytorch/pull/179326))
- [c10d] Fix TCPStore compilation with Clang 20 ([#185785](https://github.com/pytorch/pytorch/pull/185785))
- support all the back ends in FR ([#179753](https://github.com/pytorch/pytorch/pull/179753))
- [torchelastic] handle d-state process (#185414) ([#185414](https://github.com/pytorch/pytorch/pull/185414))
- Make new_group delegate to split_group behind a migration flag ([#185416](https://github.com/pytorch/pytorch/pull/185416))
- Allow generator placeholders through control deps ([#183863](https://github.com/pytorch/pytorch/pull/183863))
- [Symmetric Memory] Remove NCCL symmetric memory explicit dependency on process group ([#184260](https://github.com/pytorch/pytorch/pull/184260))
- Rename distributed collective ops to _single naming scheme ([#186123](https://github.com/pytorch/pytorch/pull/186123))
- Migrate internal usages to all_gather_single / reduce_scatter_single ([#186124](https://github.com/pytorch/pytorch/pull/186124))
- [dtensor] add sharding support for scatter op ([#186149](https://github.com/pytorch/pytorch/pull/186149))
- DTensor.to_local() drops the _is_param marker that nn.Parameter sets on custom-tensor i... ([#184422](https://github.com/pytorch/pytorch/pull/184422))
- [claude][skill] getting rid of redundant ptd-bot-triaged label ([#185537](https://github.com/pytorch/pytorch/pull/185537))
- [Full DTensor][FSDP] Use _StridedShard when TP exist ([#186126](https://github.com/pytorch/pytorch/pull/186126))
- [dtensor] single dim strategies auto infra ([#185386](https://github.com/pytorch/pytorch/pull/185386))
- Require NCCL >= 2.23 and drop version gates for older NCCL (#186163) ([#186292](https://github.com/pytorch/pytorch/pull/186292))
- Fix the symbol lookup issue with symmetric memory __init__ ([#186416](https://github.com/pytorch/pytorch/pull/186416))
- Remove custom _c10d_functional_autograd implementations, use redirects ([#172792](https://github.com/pytorch/pytorch/pull/172792))
- [FSDP2] Add set_reduce_scatter_max_input_buffers to mitigate reduce-scatter blocking backward compute ([#186000](https://github.com/pytorch/pytorch/pull/186000))
- [c10d] don't call split_group for fake backend ([#186172](https://github.com/pytorch/pytorch/pull/186172))
- Preserve user runtime asserts in FX pass ([#184608](https://github.com/pytorch/pytorch/pull/184608))
- [DTensor] Fix group_norm scalar adjuster crash when weight=None ([#184819](https://github.com/pytorch/pytorch/pull/184819))
- [FSDP2] Add set_separate_reduce_scatter_group (opt-in AG/RS overlap) ([#186335](https://github.com/pytorch/pytorch/pull/186335))
### not user facing
- [xpu][fix] Fix hard code UT failed on XPU ([#180647](https://github.com/pytorch/pytorch/pull/180647))
- [docs] fixing docs misspellings ([#179801](https://github.com/pytorch/pytorch/pull/179801))
- [PGNCCL][Symmetric Memory][IntraNodeComm] Add parameterization to `test_intra_node_comm_all_reduce` ([#181331](https://github.com/pytorch/pytorch/pull/181331))
- [overlap] pre-bucketing of fsdp collectives ([#179935](https://github.com/pytorch/pytorch/pull/179935))
- align all estimations across ranks ([#181105](https://github.com/pytorch/pytorch/pull/181105))
- [DeviceMesh] Use hashed PG names for fake backend when torchcomms is enabled ([#181929](https://github.com/pytorch/pytorch/pull/181929))
- [DTensor][BugFix] Fix DTensor + AC + compile crash: unbound inner symbol at root tracer   ([#181797](https://github.com/pytorch/pytorch/pull/181797))
- [CUDA] Fix CUDA IPC deserialization mismatch with `expandable_segments` on `FABRIC_HANDLE` ([#179618](https://github.com/pytorch/pytorch/pull/179618))
- Fix typos in sharded embedding op docstrings ([#181985](https://github.com/pytorch/pytorch/pull/181985))
- [claude][skill] fixing missing sub-oncall when distributed module has already been added ([#181927](https://github.com/pytorch/pytorch/pull/181927))
- [BE]: Simplify WorkerServer with nholmann json ([#177460](https://github.com/pytorch/pytorch/pull/177460))
- [DTensor] Make DTensor OpStrategy stringification handle missing mesh ([#182371](https://github.com/pytorch/pytorch/pull/182371))
- [docs] Add documentation for 8 functions in distributed.md ([#182544](https://github.com/pytorch/pytorch/pull/182544))
- [distributed] Fix flaky TestFunctionalAutograd by switching to LocalTensorMode ([#182665](https://github.com/pytorch/pytorch/pull/182665))
- Fix import of _debug_handlers in test_debug.py ([#182442](https://github.com/pytorch/pytorch/pull/182442))
- [DTensor]: add backward gradient verification to test_single_dim_strategy ([#182558](https://github.com/pytorch/pytorch/pull/182558))
- Add TorchComms backend docs to torch.distributed ([#182711](https://github.com/pytorch/pytorch/pull/182711))
- Convert rpc/distributed_autograd.rst from rST to MyST Markdown ([#182926](https://github.com/pytorch/pytorch/pull/182926))
- [FSDP] Fix CUDA memory leak check failure in test_fsdp_apply ([#182774](https://github.com/pytorch/pytorch/pull/182774))
- NCCL Symm mem tests ([#182445](https://github.com/pytorch/pytorch/pull/182445))
- Allow Dynamo to trace _maybe_view_chunk_cat and restore skipIfHpu on test_functional_api ([#182435](https://github.com/pytorch/pytorch/pull/182435))
- adds missing vector header in Handlers.hpp ([#183058](https://github.com/pytorch/pytorch/pull/183058))
- [BE][Ez]: Add missing typing vars for decorators. Prevent type erasure ([#183116](https://github.com/pytorch/pytorch/pull/183116))
- [OpenReg][distributed] Refactor OCCL backend registration ([#183257](https://github.com/pytorch/pytorch/pull/183257))
- documented undocumented functions in distributed.optim.md ([#182871](https://github.com/pytorch/pytorch/pull/182871))
- Fix pipelining crash when split_module interleaves get_attr with placeholder ([#182644](https://github.com/pytorch/pytorch/pull/182644))
- [Docathon] Document undocumented functions in distributed.tensor.parallel.md (3 functions)  ([#182876](https://github.com/pytorch/pytorch/pull/182876))
- [xpu][test] Port distributed _shard tests cases on Intel GPUs ([#180881](https://github.com/pytorch/pytorch/pull/180881))
- [Docathon] Document undocumented functions in rpc.md (#182830) ([#183393](https://github.com/pytorch/pytorch/pull/183393))
- Add distributed training integration doc for OOT accelerators ([#182308](https://github.com/pytorch/pytorch/pull/182308))
- [Test] Consolidate and streamline skip and xfail functionality in tests ([#183541](https://github.com/pytorch/pytorch/pull/183541))
- Guard pipeline schedule adjacency ([#179293](https://github.com/pytorch/pytorch/pull/179293))
- [NCCL][Symmetric Memory] Add test with CUDA Graph ([#184527](https://github.com/pytorch/pytorch/pull/184527))
- Fix shared-weight gradient double-counting in zero-bubble pipeline schedules ([#181365](https://github.com/pytorch/pytorch/pull/181365))
- Fix check for `aiohttp` in tests ([#184544](https://github.com/pytorch/pytorch/pull/184544))
- Use extern op metadata for runtime benchmarks ([#184138](https://github.com/pytorch/pytorch/pull/184138))
- Narrow OpInfo skips from #185013 to per-op entries ([#185307](https://github.com/pytorch/pytorch/pull/185307))
- [Test] Remove useless `gpus_for_rank()` ([#185194](https://github.com/pytorch/pytorch/pull/185194))
- [reland][compile] fix diagonal_scatter backward ([#185146](https://github.com/pytorch/pytorch/pull/185146))
- [DDE] Fix data-dependent errors in pixel_shuffle, pdist, and padding ops ([#183814](https://github.com/pytorch/pytorch/pull/183814))
- Split linear_cross_entropy OpInfo into unchunked and chunked variants ([#184596](https://github.com/pytorch/pytorch/pull/184596))
- Fix call to fork_rng by by specifying device type ([#180512](https://github.com/pytorch/pytorch/pull/180512))
- Fix "its" to "it's" contractions in comments and docstrings ([#185720](https://github.com/pytorch/pytorch/pull/185720))
- Fix missing stride() call in test_redistribute TensorMeta ([#186170](https://github.com/pytorch/pytorch/pull/186170))
- Normalize device_type in distributed reordering/logger tests ([#186169](https://github.com/pytorch/pytorch/pull/186169))
- [Overlap Scheduling] Fix SymInt crash in collective/compute node benchmarking ([#186065](https://github.com/pytorch/pytorch/pull/186065))
- [XPU][Test] Migrate 6 UT test suites for Intel GPU ([#174370](https://github.com/pytorch/pytorch/pull/174370))
- UCC/test: Undo migration to reduce_scatter_single ([#186666](https://github.com/pytorch/pytorch/pull/186666))
- [pipelining] Fix None gradient handling in backward send/recv ([#182182](https://github.com/pytorch/pytorch/pull/182182))
- [pipelining] Add guards for non-float tensors when building pipeline ([#183582](https://github.com/pytorch/pytorch/pull/183582))
### security
