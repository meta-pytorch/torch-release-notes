
# Release Notes worksheet distributed (c10d)

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

## distributed (c10d)
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- c10d/symm_mem: use multimem in CUDA barrier ([#192861](https://github.com/pytorch/pytorch/pull/192861))
- [c10d] Fix flight recorder attach for the default nccl name, and a completion race ([#192858](https://github.com/pytorch/pytorch/pull/192858))
- c10d: support collective time estimation in nccl2 ([#192854](https://github.com/pytorch/pytorch/pull/192854))
- c10d: support tensor allocation in nccl2 ([#192855](https://github.com/pytorch/pytorch/pull/192855))
- [symm_mem] Implement NVSHMEM signaling APIs ([#192579](https://github.com/pytorch/pytorch/pull/192579))
- c10d: initialize nccl2 communicators eagerly ([#192895](https://github.com/pytorch/pytorch/pull/192895))
- Add a Pure-Python c10d watchdog ([#192075](https://github.com/pytorch/pytorch/pull/192075))
- [c10d][CFT] Expose NCCL CFT logical endpoints from symmetric memory ([#191685](https://github.com/pytorch/pytorch/pull/191685))
- [torch.distributed] force nccl-legacy for internal users ([#193221](https://github.com/pytorch/pytorch/pull/193221))
- Add more ops support for functional all_reduce ([#190942](https://github.com/pytorch/pytorch/pull/190942))
- c10d: stop noisy warning on the renamed public collective aliases ([#193874](https://github.com/pytorch/pytorch/pull/193874))
- Fix compiler error due to invalid % escape in CUDA inline assembly ([#194104](https://github.com/pytorch/pytorch/pull/194104))
- Fix "a"/"an" article errors and typos in comments and docstrings ([#193967](https://github.com/pytorch/pytorch/pull/193967))
- Introduce batched `wait_tensors` api for coalescing multi-output functional collectives ([#193892](https://github.com/pytorch/pytorch/pull/193892))
- [SymmMem] Fix out-of-bounds shared memory write in NVSHMEM allToAllV_2d ([#192300](https://github.com/pytorch/pytorch/pull/192300))
- [fake_pg] handle varied buffer shapes and sizes in all_to_all_single ([#193985](https://github.com/pytorch/pytorch/pull/193985))
- Share `NCCLDevCommManager` singleton across DSOs ([#193942](https://github.com/pytorch/pytorch/pull/193942))
- [c10d] Bind local rank before eager NCCL2 initialization ([#193237](https://github.com/pytorch/pytorch/pull/193237))
- [distributed] Run legacy-only NCCL tests with nccl-legacy ([#193240](https://github.com/pytorch/pytorch/pull/193240))
- Clean up stale TORCH_NCCL_AVOID_RECORD_STREAMS and avoidRecordStreams_ ([#194701](https://github.com/pytorch/pytorch/pull/194701))
- Fix _maybe_view_chunk_cat view shape for negative gather_dim ([#194865](https://github.com/pytorch/pytorch/pull/194865))
- [c10d] Decouple completion hooks from Work lifetime ([#194830](https://github.com/pytorch/pytorch/pull/194830))
- [c10d] Move NCCL2 completion data into shared state ([#194831](https://github.com/pytorch/pytorch/pull/194831))
- [c10d] Share NCCL2 input tensor ownership ([#194832](https://github.com/pytorch/pytorch/pull/194832))
- [c10d] Release unused functional Work results ([#193239](https://github.com/pytorch/pytorch/pull/193239))
- [TokenSwitch] Add expert-major dispatch layout ([#187784](https://github.com/pytorch/pytorch/pull/187784))
- [c10d] Match NCCL2 collective validation with NCCL ([#194953](https://github.com/pytorch/pytorch/pull/194953))
- [c10d] Make nccl2 the default NCCL backend ([#192281](https://github.com/pytorch/pytorch/pull/192281))
- [distributed] Warn pipeline users about eager NCCL communicators ([#193241](https://github.com/pytorch/pytorch/pull/193241))
- Add parameter-contiguous all-gather (symm_mem.all_gather_offset) ([#187642](https://github.com/pytorch/pytorch/pull/187642))
- [TokenSwitch] Add symmetric-memory zero-copy dispatch/combine ([#187785](https://github.com/pytorch/pytorch/pull/187785))
- [c10d] Make NCCL2 Work teardown lifetime-safe ([#195485](https://github.com/pytorch/pytorch/pull/195485))
- [c10d] Make nccl2 the default NCCL backend ([#192281](https://github.com/pytorch/pytorch/pull/192281))
- [distributed] Warn pipeline users about eager NCCL communicators ([#193241](https://github.com/pytorch/pytorch/pull/193241))
- [Distributed][NCCL] Initialize Backend group UID in constructor ([#194935](https://github.com/pytorch/pytorch/pull/194935))
- Add nccl4py c10d backend ([#191703](https://github.com/pytorch/pytorch/pull/191703))
- [RAWTHROW][8] torch/csrc/distributed: everything except nccl2 ([#195149](https://github.com/pytorch/pytorch/pull/195149))
- [ROCm][c10d] Enable NCCL2 windows and enforce allocator provenance ([#193282](https://github.com/pytorch/pytorch/pull/193282))
- [c10d] [PyBackend] Fix nccl4py backend binding subgroup communicators to the wrong GPU ([#195766](https://github.com/pytorch/pytorch/pull/195766))
- [RAWTHROW][9] torch/csrc/distributed/c10d/nccl2: 43 conversions ([#195763](https://github.com/pytorch/pytorch/pull/195763))
- Do not dereference the absent backend when reusing one in setBackend ([#195536](https://github.com/pytorch/pytorch/pull/195536))
- [LocalTensor] Support ReduceOp.PREMUL_SUM for collectives under LocalTensorMode ([#191947](https://github.com/pytorch/pytorch/pull/191947))
- [symm_mem] Fix multicast rendezvous cleanup  ([#195596](https://github.com/pytorch/pytorch/pull/195596))
- Add more ops support for functional all_reduce_coalesced ([#193868](https://github.com/pytorch/pytorch/pull/193868))
- [distributed] Validate the parent backend before split_group ([#195758](https://github.com/pytorch/pytorch/pull/195758))
- [symm_mem] Don't throw from AllocationRef destructor ([#196003](https://github.com/pytorch/pytorch/pull/196003))
- [c10d] Tear down on a NCCL timeout regardless of RETHROW_CUDA_ERRORS, under a flag (#196187) ([#196187](https://github.com/pytorch/pytorch/pull/196187))
- [distributed][docs] Fix group_src docstring in irecv ([#189623](https://github.com/pytorch/pytorch/pull/189623))
- Fix hardcoded rendezvous ports in distributed tests ([#195994](https://github.com/pytorch/pytorch/pull/195994))
- [SymmMem] Fix signal pad zeroing race in NVSHMEM allocator ([#196546](https://github.com/pytorch/pytorch/pull/196546))
- replace all_gather with all_gather_single to implement all_gather_object ([#196185](https://github.com/pytorch/pytorch/pull/196185))
- [elastic] Close leaked mkstemp fd in _create_file_store ([#191425](https://github.com/pytorch/pytorch/pull/191425))
- [c10d] [PyBackend] NCCL4Py backend refactor and requested changes ([#196331](https://github.com/pytorch/pytorch/pull/196331))
- [c10d][nccl2] Expose comm ptr in nccl2 backend ([#197558](https://github.com/pytorch/pytorch/pull/197558))
- Register autograd for wait_tensors to fix zeroed coalesced collective grads ([#196077](https://github.com/pytorch/pytorch/pull/196077))
- [symm_mem]: Add per-PG stream serialization for ops ([#195947](https://github.com/pytorch/pytorch/pull/195947))
- symm_mem: Scope the StoreExchange sequence counter to the process group ([#196350](https://github.com/pytorch/pytorch/pull/196350))
- [c10d] Split only from compatible parent backends (#197568) ([#197568](https://github.com/pytorch/pytorch/pull/197568))
- [c10d] Let backends own split Store isolation ([#196665](https://github.com/pytorch/pytorch/pull/196665))
- [LocalTensor] Support permuted process group ranks in collectives ([#192777](https://github.com/pytorch/pytorch/pull/192777))
- [c10d][torchcomms] Factor TorchComms backend creation (#197616) ([#197616](https://github.com/pytorch/pytorch/pull/197616))
- Forward PyProcessGroup reconfiguration through Python overrides ([#198251](https://github.com/pytorch/pytorch/pull/198251))
- [symm_mem] Synchronize CUDA cleanup across backends ([#198306](https://github.com/pytorch/pytorch/pull/198306))
- Fix stale ProcessGroupOptions docstring references, document Backend.Options ([#196123](https://github.com/pytorch/pytorch/pull/196123))
- [c10d] [NCCL4PyBackend] Migrate NCCL4PyBackend to extended backend ([#198000](https://github.com/pytorch/pytorch/pull/198000))
- [ROCm] Fix the NaN-check tests on boxes with core dumps enabled ([#197885](https://github.com/pytorch/pytorch/pull/197885))
- [c10d][nccl2] Bind the watchdog thread to its communicator device ([#198339](https://github.com/pytorch/pytorch/pull/198339))
- Add NIXL distributed transport ([#197032](https://github.com/pytorch/pytorch/pull/197032))
- [c10d] Allow CPU device_id in init_process_group ([#198340](https://github.com/pytorch/pytorch/pull/198340))
- [ROCm] Fix torchcomms test harness to probe RCCL instead of NCCL ([#196907](https://github.com/pytorch/pytorch/pull/196907))
- [c10d][nccl2] Add comm_ptr and _comm_ptr to all NCCL backends ([#198865](https://github.com/pytorch/pytorch/pull/198865))
- Relanding #198571 ([#198961](https://github.com/pytorch/pytorch/pull/198961))
- [symm_mem]: Add per-PG stream serialization for ops ([#195947](https://github.com/pytorch/pytorch/pull/195947))
- replace all_gather with all_gather_single to implement all_gather_object ([#196185](https://github.com/pytorch/pytorch/pull/196185))
- Bootstrap transports from a Store and rank ([#198889](https://github.com/pytorch/pytorch/pull/198889))
- Add CUDA stream transport operations ([#198918](https://github.com/pytorch/pytorch/pull/198918))
- [c10d][nccl2] Wait for nonblocking split/shrink child initialization ([#199263](https://github.com/pytorch/pytorch/pull/199263))
- [ROCm][c10d] Enable NCCL2 reconfigure on ROCm ([#194774](https://github.com/pytorch/pytorch/pull/194774))
- [elastic] Guard rendezvous shutdown in launch_agent to avoid masking ChildFailedError ([#195316](https://github.com/pytorch/pytorch/pull/195316))
- [c10d][torchcomms] Propagate dynamic options (#199099) ([#199099](https://github.com/pytorch/pytorch/pull/199099))
- [c10d][nccl2] Port torchcomms shrink/grow reconfigure fast path ([#199240](https://github.com/pytorch/pytorch/pull/199240))
### not user facing
- [RAWTHROW][1b] TORCH_CHECK_PYTHON; delete four exclude patterns ([#193612](https://github.com/pytorch/pytorch/pull/193612))
- debug server tutorial ([#178800](https://github.com/pytorch/pytorch/pull/178800))
- [distributed] Configure collective timeouts through ProcessGroup ([#193238](https://github.com/pytorch/pytorch/pull/193238))
- [c10d] Add an opt-in uniform-rank simulation contract to FakeProcessGroup ([#194545](https://github.com/pytorch/pytorch/pull/194545))
- [BE][Ez]: Optimize aten::{fmap,filter} with rvalue overload ([#194929](https://github.com/pytorch/pytorch/pull/194929))
- Replace irange-and-subscript loops with range-based for ([#196097](https://github.com/pytorch/pytorch/pull/196097))
- [PyTorch][DDP] Add caller-controlled backward finalization ([#196651](https://github.com/pytorch/pytorch/pull/196651))
- [c10d] Fix threaded-PG teardown crash on pg_flight_recorder_hooks ([#196786](https://github.com/pytorch/pytorch/pull/196786))
- [ROCm] Add amd_smi as a build time dependency on ROCm 7.14 and after ([#192520](https://github.com/pytorch/pytorch/pull/192520))
- [distributed] Preserve PreMulSum in single-rank reduce-scatter ([#198571](https://github.com/pytorch/pytorch/pull/198571))
- Lazy-import torchcomms so default-shard doctests do not load it ([#198681](https://github.com/pytorch/pytorch/pull/198681))
- Lazy-import torchcomms so default-shard doctests do not load it ([#198681](https://github.com/pytorch/pytorch/pull/198681))
- [detailed][DDP] Lazy allocate reducer buckets in backward (#199110) ([#199110](https://github.com/pytorch/pytorch/pull/199110))
### security
