
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
- [distributed] Reduce convolution input size in the DDP join test ([#197633](https://github.com/pytorch/pytorch/pull/197633))
- Add Python distributed transport registry ([#195643](https://github.com/pytorch/pytorch/pull/195643))
- [distributed] Preserve PreMulSum in single-rank reduce-scatter (d4f9eff15024)
- forward fix for rs with ws=1 (f565b1282aa4)
- Comment NIXL transport lifecycle states ([#198890](https://github.com/pytorch/pytorch/pull/198890))
### not user facing
- [c10d] Tests for the flight recorder hook ([#192837](https://github.com/pytorch/pytorch/pull/192837))
- [Testcase Refactoring] Enable PrivateUse1 and add hw-classification in test_backward ([#191719](https://github.com/pytorch/pytorch/pull/191719))
- [Testcase Refactoring] Add hw-classification in test_pipe ([#191818](https://github.com/pytorch/pytorch/pull/191818))
- [Testcase Refactoring] Enable PrivateUse1 tests and add hw-classification in test_unflatten ([#191728](https://github.com/pytorch/pytorch/pull/191728))
- [ROCm] Remove obsolete ROCm 7.14 test skips ([#192674](https://github.com/pytorch/pytorch/pull/192674))
- [B200] remove some symmetric memory test xfails ([#192568](https://github.com/pytorch/pytorch/pull/192568))
- [c10d] Skip NCCL2 reconfiguration tests on ROCm ([#193744](https://github.com/pytorch/pytorch/pull/193744))
- Fix test_gather_object assertion for Python 3.14 PicklingError ([#192811](https://github.com/pytorch/pytorch/pull/192811))
- Make PP max_active_stages configuable ([#193972](https://github.com/pytorch/pytorch/pull/193972))
- [Test] Support `DistMatrixOpsTest.test_grouped_mm` with world size 2 ([#194264](https://github.com/pytorch/pytorch/pull/194264))
- [Test][distributed] Refactor some distributed test helpers to be device-agnostic ([#185184](https://github.com/pytorch/pytorch/pull/185184))
- Restore MemoryTracker operation count on load ([#191453](https://github.com/pytorch/pytorch/pull/191453))
- [Testcase Refactoring] Add hw_classification to test_store ([#192036](https://github.com/pytorch/pytorch/pull/192036))
- [Testcase Refactoring] Use is_backend_available for MultiProcContinuousTest backend check ([#192186](https://github.com/pytorch/pytorch/pull/192186))
- [Testcase Refactoring] Enable PrivateUse1 tests and add hw-classification in test_microbatch ([#190422](https://github.com/pytorch/pytorch/pull/190422))
- Add sync_cache_decision_cross_ranks (#193043) ([#193043](https://github.com/pytorch/pytorch/pull/193043))
- [c10d] Gate NCCL CFT tests on CFT-capable GPU/driver/CUDA stacks ([#194299](https://github.com/pytorch/pytorch/pull/194299))
- Fix issue triage GitHub MCP startup ([#194930](https://github.com/pytorch/pytorch/pull/194930))
- [Testcase Refactoring] Add hw_classification to test/distributed/elastic/metrics/api_test.py  ([#192491](https://github.com/pytorch/pytorch/pull/192491))
- Fix post-local SGD checkpoint reload race ([#194614](https://github.com/pytorch/pytorch/pull/194614))
- Fix duplicated word in DefaultStager.stage docstring ([#195233](https://github.com/pytorch/pytorch/pull/195233))
- [distributed] Stabilize NCCL timeout tests ([#194954](https://github.com/pytorch/pytorch/pull/194954))
- [c10d] Set local rank in backend test workers ([#195103](https://github.com/pytorch/pytorch/pull/195103))
- [pipelining] Annotate schedule actions with mark_kernels for CUDA graph traces ([#195072](https://github.com/pytorch/pytorch/pull/195072))
- [Testcase Refactoring][Test] Add hw_classification to elastic multiprocessing api_test.py ([#190974](https://github.com/pytorch/pytorch/pull/190974))
- [Testcase Refactoring] Add hardware classification for test_cupy_as_tensor.py ([#193127](https://github.com/pytorch/pytorch/pull/193127))
- Fix missing stream synchronization in the threaded process group ([#195281](https://github.com/pytorch/pytorch/pull/195281))
- [ROCm] Unskip distributed CUDA graph and symmetric memory tests ([#196409](https://github.com/pytorch/pytorch/pull/196409))
- [Testcase Refactoring] Add HardwareClassification for test_c10d_hooks ([#192587](https://github.com/pytorch/pytorch/pull/192587))
- [Testcase Refactoring] Add hw-classification in launcher_test_api ([#193891](https://github.com/pytorch/pytorch/pull/193891))
- [Testcase Refactoring] Add hw-classification in launcher_api_test ([#193930](https://github.com/pytorch/pytorch/pull/193930))
- [Testcase Refactoring] Add hw-classification in launcher_launch_test ([#194580](https://github.com/pytorch/pytorch/pull/194580))
- [Testcase Refactoring]Add hw_classification to elastic multiprocessing errors api_test.py ([#192201](https://github.com/pytorch/pytorch/pull/192201))
- [Testcase Refactoring] Add hw_classification to test_processgroup_jit ([#192028](https://github.com/pytorch/pytorch/pull/192028))
- [Testcase Refactoring] Add hw-classification in distributed_test_run ([#193906](https://github.com/pytorch/pytorch/pull/193906))
- [TokenSwitch] Hold `topk_idx` in `torch.int64` ([#195985](https://github.com/pytorch/pytorch/pull/195985))
- [Testcase Refactoring] Add hw-classification in test_launcher ([#193948](https://github.com/pytorch/pytorch/pull/193948))
- [Testcase Refactoring] Add hardware classification for argparse_util_test.py ([#193135](https://github.com/pytorch/pytorch/pull/193135))
- [Testcase Refactoring] Add hardware classification for test_local_tensor_tutorial_examples.py ([#193278](https://github.com/pytorch/pytorch/pull/193278))
- [Testcase Refactoring] Add HardwareClassification to cycling_iterator_test.py ([#193570](https://github.com/pytorch/pytorch/pull/193570))
- [Testcase Refactoring] Add hardware classification for test_typing.py ([#193256](https://github.com/pytorch/pytorch/pull/193256))
- [Testcase Refactoring] Add hw-classification and split device-exercising tests in test_schedule ([#191889](https://github.com/pytorch/pytorch/pull/191889))
- [Testcase Refactoring] Add hw-classification in util_test ([#193879](https://github.com/pytorch/pytorch/pull/193879))
- [Testcase Refactoring] Add hw_classification label to test_mod_tracker.py ([#193114](https://github.com/pytorch/pytorch/pull/193114))
- [Testcase Refactoring] Add hardware classification for test_right_inverse.py ([#193267](https://github.com/pytorch/pytorch/pull/193267))
- [Testcase Refactoring] Add hardware classification for test_coalesce.py ([#193270](https://github.com/pytorch/pytorch/pull/193270))
- [Testcase Refactoring] Enable hw-classification for api_test ([#193081](https://github.com/pytorch/pytorch/pull/193081))
- [Testcase Refactoring] Add hw-classification in logging_test ([#193799](https://github.com/pytorch/pytorch/pull/193799))
- [ROCm] Fix data race in test_triton_signal_wait_until ([#195761](https://github.com/pytorch/pytorch/pull/195761))
- [Testcase Refactoring] Demote test_fsdp_fx to Strategy 1 / GENERIC ([#192698](https://github.com/pytorch/pytorch/pull/192698))
- [ROCm] Unskip symmetric memory UTs on rocm 10.1+ ([#193980](https://github.com/pytorch/pytorch/pull/193980))
- [ROCm] Clear MI200 test gates after root-causing each one ([#196674](https://github.com/pytorch/pytorch/pull/196674))
- [Testcase Refactoring]Add hw_classification label to test_composition.py ([#193323](https://github.com/pytorch/pytorch/pull/193323))
- [Testcase Refactoring] Label test_distributed_checkpoint and decouple from hard-coded device list ([#191320](https://github.com/pytorch/pytorch/pull/191320))
- [Testcase Refactoring] Enable hw-classification for local_elastic_agent_test ([#193093](https://github.com/pytorch/pytorch/pull/193093))
- [Testcase Refactoring] Add hardware classification labels to test_fully_shard_state ([#193665](https://github.com/pytorch/pytorch/pull/193665))
- [Testcase Refactoring] Add hw_classification labels to optimizer test classes ([#194190](https://github.com/pytorch/pytorch/pull/194190))
- [Testcase Refactoring] Add hardware classification labels to test_contract ([#193653](https://github.com/pytorch/pytorch/pull/193653))
- [Testcase Refactoring]Add hw_classification to elastic rendezvous api_test.py ([#193075](https://github.com/pytorch/pytorch/pull/193075))
- [Testcase Refactoring] Add hw_classification to elastic multiprocessing tail_log_test.py ([#193072](https://github.com/pytorch/pytorch/pull/193072))
- [Testcase Refactoring]Add hw_classification=GENERIC to ShardingSpecLoggerTest ([#192766](https://github.com/pytorch/pytorch/pull/192766))
- [Testcase Refactoring] Add hw_classification=GENERIC to TestComplement ([#193310](https://github.com/pytorch/pytorch/pull/193310))
- [Testcase Refactoring] Add HardwareClassification to local_timer_test.py ([#194221](https://github.com/pytorch/pytorch/pull/194221))
- [Testcase Refactoring] Add HardwareClassification to file_based_local_timer_test.py ([#194219](https://github.com/pytorch/pytorch/pull/194219))
- [Testcase Refactoring] Add HardwareClassification to api_test.py ([#193568](https://github.com/pytorch/pytorch/pull/193568))
- [Testcase Refactoring] Add HardwareClassification to distributed_test.py ([#194216](https://github.com/pytorch/pytorch/pull/194216))
- [Testcase Refactoring] Add HardwareClassification for test_fake_backend_new_group ([#192586](https://github.com/pytorch/pytorch/pull/192586))
- [Testcase Refactoring]Add hw_classification to elastic multiprocessing test_api.py ([#193073](https://github.com/pytorch/pytorch/pull/193073))
- [Testcase Refactoring]Add hw_classification=GENERIC to TestLeftInverse ([#193335](https://github.com/pytorch/pytorch/pull/193335))
- [Testcase Refactoring]Add hw_classification to elastic multiprocessing redirects_test.py ([#192329](https://github.com/pytorch/pytorch/pull/192329))
- [ROCm] Unskip assorted GPU tests and fix two ROCm arch skips ([#197340](https://github.com/pytorch/pytorch/pull/197340))
- [ROCm] Drop the MI350 gates on three dynamo_distributed inductor tests ([#197472](https://github.com/pytorch/pytorch/pull/197472))
- [Testcase Refactoring] Classify fake distributed tests by hardware ([#192914](https://github.com/pytorch/pytorch/pull/192914))
- [DTensor] Remove exhaustive 3D Dijkstra test cases ([#197478](https://github.com/pytorch/pytorch/pull/197478))
- [DTensor] Bound the 4D Dijkstra strategy test ([#197479](https://github.com/pytorch/pytorch/pull/197479))
- Improve the CP test performance ([#197513](https://github.com/pytorch/pytorch/pull/197513))
- [FSDP2] Restore reduce-scatter numerical test coverage ([#197459](https://github.com/pytorch/pytorch/pull/197459))
- [distributed] Synchronize peers in NCCL2 timeout tests ([#197587](https://github.com/pytorch/pytorch/pull/197587))
- [distributed] Release flight recorder peers after checking the trace ([#197588](https://github.com/pytorch/pytorch/pull/197588))
- [3.15] Use public typing API in flight_recorder ([#197320](https://github.com/pytorch/pytorch/pull/197320))
- [distributed] Run independent store barrier timeout cases concurrently ([#197629](https://github.com/pytorch/pytorch/pull/197629))
- [distributed] Shorten explicitly failing store waits ([#197630](https://github.com/pytorch/pytorch/pull/197630))
- [distributed] Shorten deleted-key store timeout ([#197631](https://github.com/pytorch/pytorch/pull/197631))
- [distributed] Avoid duplicate AOTI compilation in the all-reduce test ([#197632](https://github.com/pytorch/pytorch/pull/197632))
- [distributed] Wait for completion instead of sleeping in work tests ([#197634](https://github.com/pytorch/pytorch/pull/197634))
- [distributed] Shrink all-gather layout test tensors ([#197639](https://github.com/pytorch/pytorch/pull/197639))
- [distributed] Join elastic test processes instead of sleeping ([#197640](https://github.com/pytorch/pytorch/pull/197640))
- [distributed] Wait for NCCL trace retirement instead of sleeping ([#197624](https://github.com/pytorch/pytorch/pull/197624))
- [distributed] Fail the stuck NCCL error propagation test promptly ([#197625](https://github.com/pytorch/pytorch/pull/197625))
- [distributed] Shorten deliberate NCCL2 collective timeouts ([#197626](https://github.com/pytorch/pytorch/pull/197626))
- [distributed] Skip diagnostic grace delay in NCCL error propagation test ([#197627](https://github.com/pytorch/pytorch/pull/197627))
- [distributed] Synchronize CUDA context checks with CPU store barriers ([#197628](https://github.com/pytorch/pytorch/pull/197628))
- Fix TF32 test helpers leaking the legacy matmul precision enum ([#197369](https://github.com/pytorch/pytorch/pull/197369))
- [distributed] Reuse workers for DTensor embedding tests ([#197648](https://github.com/pytorch/pytorch/pull/197648))
- Reuse workers for eager DTensor convolution tests ([#197692](https://github.com/pytorch/pytorch/pull/197692))
- [distributed] Reuse workers across FSDP communication hook tests ([#197643](https://github.com/pytorch/pytorch/pull/197643))
- [distributed] Reuse workers for isolated FSDP core tests ([#197644](https://github.com/pytorch/pytorch/pull/197644))
- [distributed] Reuse workers for FSDP freezing-weight tests ([#197645](https://github.com/pytorch/pytorch/pull/197645))
- [distributed] Reuse workers for FSDP2 autograd tests ([#197646](https://github.com/pytorch/pytorch/pull/197646))
- [distributed] Reuse workers for DTensor subclass tests ([#197655](https://github.com/pytorch/pytorch/pull/197655))
- [distributed] Reuse workers for core DTensor tests ([#197656](https://github.com/pytorch/pytorch/pull/197656))
- [distributed] Reuse tensor parallel transformation workers ([#197703](https://github.com/pytorch/pytorch/pull/197703))
- [distributed] Reuse context parallel argument test workers ([#197705](https://github.com/pytorch/pytorch/pull/197705))
- Reuse workers for distributed window tests ([#197698](https://github.com/pytorch/pytorch/pull/197698))
- [distributed] Reuse workers across LocalMap tests ([#197675](https://github.com/pytorch/pytorch/pull/197675))
- [distributed] Reuse replicate gradient accumulation workers ([#197676](https://github.com/pytorch/pytorch/pull/197676))
- [distributed] Reuse workers for FSDP original-parameter tests ([#197650](https://github.com/pytorch/pytorch/pull/197650))
- [distributed] Reuse workers for FSDP submodule precision tests ([#197651](https://github.com/pytorch/pytorch/pull/197651))
- [distributed] Reuse nccl4py collective test workers ([#197706](https://github.com/pytorch/pytorch/pull/197706))
- [distributed] Reuse workers for FSDP no_sync tests ([#197707](https://github.com/pytorch/pytorch/pull/197707))
- Reuse workers across DTensor experimental-op tests ([#197687](https://github.com/pytorch/pytorch/pull/197687))
- Reuse workers for uneven DTensor allocation tests ([#197690](https://github.com/pytorch/pytorch/pull/197690))
- [distributed] Reuse workers for single-rank FSDP reduction tests ([#197662](https://github.com/pytorch/pytorch/pull/197662))
- [distributed] Reuse workers for DTensor shape utility tests ([#197664](https://github.com/pytorch/pytorch/pull/197664))
- [distributed] Reuse workers for DTensor decomposition tests ([#197652](https://github.com/pytorch/pytorch/pull/197652))
- [distributed] Reuse workers for DTensor initialization tests ([#197653](https://github.com/pytorch/pytorch/pull/197653))
- [distributed] Reuse workers for DTensor API tests ([#197649](https://github.com/pytorch/pytorch/pull/197649))
- Reuse workers for tensor parallel style tests ([#197691](https://github.com/pytorch/pytorch/pull/197691))
- [Testcase Refactoring] Add hw_classification to test/distributed/elastic/events/lib_test.py ([#192921](https://github.com/pytorch/pytorch/pull/192921))
- Wait on coalesced all_gather outputs in the dynamo trace test ([#197823](https://github.com/pytorch/pytorch/pull/197823))
- Order all-gather streams after post-forward reshard in FSDP comm test ([#197827](https://github.com/pytorch/pytorch/pull/197827))
- [Testcase Refactoring] Generalize requires_world_size to be hardware-agnostic ([#192694](https://github.com/pytorch/pytorch/pull/192694))
- Reuse workers for sharded optimizer tests ([#197696](https://github.com/pytorch/pytorch/pull/197696))
- Reuse workers for sharded embedding tests ([#197697](https://github.com/pytorch/pytorch/pull/197697))
- Reuse workers in process-group hook tests ([#197686](https://github.com/pytorch/pytorch/pull/197686))
- Replace add_definitions with add_compile_definitions ([#197812](https://github.com/pytorch/pytorch/pull/197812))
- [distributed] Reuse workers for tensor-parallel API tests ([#197658](https://github.com/pytorch/pytorch/pull/197658))
- [distributed] Reuse workers for strided DTensor tests ([#197674](https://github.com/pytorch/pytorch/pull/197674))
- [distributed] Reuse mixed precision training workers ([#197678](https://github.com/pytorch/pytorch/pull/197678))
- [ROCm] Give the gloo CUDA skips their root-cause reason ([#197902](https://github.com/pytorch/pytorch/pull/197902))
- [distributed] Reuse workers for FSDP2 state-dict tests ([#197660](https://github.com/pytorch/pytorch/pull/197660))
- [distributed] Reuse quantization test workers ([#197702](https://github.com/pytorch/pytorch/pull/197702))
- [distributed] Reuse workers for FSDP optimizer state tests ([#197685](https://github.com/pytorch/pytorch/pull/197685))
- [distributed] Reuse workers for FSDP communication tests ([#197671](https://github.com/pytorch/pytorch/pull/197671))
- [distributed] Reuse workers for single-rank ZeRO tests ([#197672](https://github.com/pytorch/pytorch/pull/197672))
- [distributed] Reuse workers for DDP communication-hook tests ([#197669](https://github.com/pytorch/pytorch/pull/197669))
- [distributed] Reuse FSDP checkpoint workers ([#197679](https://github.com/pytorch/pytorch/pull/197679))
- [distributed] Reuse shared parameter test workers ([#197681](https://github.com/pytorch/pytorch/pull/197681))
- [distributed] Reuse FSDP gradient accumulation workers ([#197682](https://github.com/pytorch/pytorch/pull/197682))
- Fix test_ddp_zero_overlap parity check on 4 or more ranks ([#197890](https://github.com/pytorch/pytorch/pull/197890))
- [distributed] Reuse workers for DTensor strategy registration tests ([#197661](https://github.com/pytorch/pytorch/pull/197661))
- [ROCm] Unskip test_ring_attention_sdpa and widen its tolerances ([#197208](https://github.com/pytorch/pytorch/pull/197208))
- Add CUDA graph capture test for the NVSHMEM symm mem backend ([#197700](https://github.com/pytorch/pytorch/pull/197700))
- [TEST][NCCL] Avoid specifying `NCCL_ALGO=NVLS` for NCCL 2.31 ([#197038](https://github.com/pytorch/pytorch/pull/197038))
- Skip nccl4py backend tests on ROCm ([#198288](https://github.com/pytorch/pytorch/pull/198288))
- [Testcase Refactoring]Support multiple accelerator backends in test_overlap_bucketing_unit.py ([#190866](https://github.com/pytorch/pytorch/pull/190866))
- [distributed] Tear down NCCL timeout tests explicitly ([#198334](https://github.com/pytorch/pytorch/pull/198334))
- [ROCm] Fix dirty memory comparison in test_foreach_groups_correctness ([#198408](https://github.com/pytorch/pytorch/pull/198408))
- Guard tensors against the current device index under compile_on_one_rank ([#196150](https://github.com/pytorch/pytorch/pull/196150))
- Make the aten.polar ref functional so it can be used as a decomposition (#198300) ([#198300](https://github.com/pytorch/pytorch/pull/198300))
- Skip `TestFullyShardSymmMem` for NCCL < 2.28 ([#184536](https://github.com/pytorch/pytorch/pull/184536))
- Preserve rank-relative devices in Dynamo device contexts ([#196938](https://github.com/pytorch/pytorch/pull/196938))
- Construct streams on the runtime CooR device ([#196939](https://github.com/pytorch/pytorch/pull/196939))
- [ROCm][c10d] Unskip nccl2 expandable all-gather ([#195900](https://github.com/pytorch/pytorch/pull/195900))
- [c10d][nccl2] Make ranks 1/2 abort in test_work_reports_communicator_error ([#198318](https://github.com/pytorch/pytorch/pull/198318))
- [ROCm][test] Reuse process groups across FSDP hybrid-shard subtests ([#198302](https://github.com/pytorch/pytorch/pull/198302))
- [ROCm][test]Reuse device meshes across ComposabilityTest cases ([#198299](https://github.com/pytorch/pytorch/pull/198299))
- [ROCm][test] Reuse device meshes across FSDP2 ND-mesh subtests ([#198301](https://github.com/pytorch/pytorch/pull/198301))
- [ROCm] Make test_ddp_apply_optim_in_backward deterministic for BLAS ([#198643](https://github.com/pytorch/pytorch/pull/198643))
- [Testcase Refactoring] Add hw_classification to elastic rendezvous c10d_rendezvous_backend_test.py ([#193078](https://github.com/pytorch/pytorch/pull/193078))
- Fix teardown race in _test_rank_membership ([#199026](https://github.com/pytorch/pytorch/pull/199026))
- [Testcase Refactoring]Add hw_classification to elastic multiprocessing error_handler_test.py ([#192203](https://github.com/pytorch/pytorch/pull/192203))
- [CooR] Make stream observations rank-portable under compile_on_one_rank ([#196940](https://github.com/pytorch/pytorch/pull/196940))
- [distributed] Add scoped agent development guidance ([#199168](https://github.com/pytorch/pytorch/pull/199168))
- [C10d][NCCL2] Fix NCCL2 CUDA graph cleanup ([#199226](https://github.com/pytorch/pytorch/pull/199226))
- [distributed][tools] Fix MemoryTracker.load not restoring the operation count ([#192476](https://github.com/pytorch/pytorch/pull/192476))
- [FSDP] Skip unsupported FSDP state-dict configurations at collection ([#198082](https://github.com/pytorch/pytorch/pull/198082))
- [distributed] Avoid inherited duplicate compiler overlap tests ([#198158](https://github.com/pytorch/pytorch/pull/198158))
- [c10d] Reuse workers for backend process-group tests ([#198156](https://github.com/pytorch/pytorch/pull/198156))
- Skip test_manual_backward_finalization_pickle_compatibility for pypg process-group-wrapping DDP tests ([#199109](https://github.com/pytorch/pytorch/pull/199109))
- [RFC] [Testcase Refactoring]Make DDP comm hooks tests use torch.accelerator instead of torch.cuda for runtime check ([#191087](https://github.com/pytorch/pytorch/pull/191087))
- [Testcase Refactoring] Add hw-classification in launcher_test_run ([#194060](https://github.com/pytorch/pytorch/pull/194060))
- [ROCm] Enable test_grouped_mm on ROCm ([#199048](https://github.com/pytorch/pytorch/pull/199048))
- [FSDP] Reuse workers for FSDP1 state_dict and mixed precision tests ([#199534](https://github.com/pytorch/pytorch/pull/199534))
### security
