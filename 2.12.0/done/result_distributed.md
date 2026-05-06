
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
- `torch.distributed.nn.functional` ops now raise `RuntimeError` under `torch.compile` ([#177342](https://github.com/pytorch/pytorch/pull/177342))

  All ops in `torch.distributed.nn.functional` (e.g., `broadcast`, `all_reduce`, `all_gather`, `reduce_scatter`, `all_to_all_single`) now raise `RuntimeError` when called inside `torch.compile`. Users should migrate to the functional collectives API in `torch.distributed._functional_collectives`.

  Version 2.11:
  ```python
  @torch.compile
  def my_func(x):
      return torch.distributed.nn.functional.all_reduce(x, op=ReduceOp.SUM)
  ```

  Version 2.12:
  ```python
  @torch.compile
  def my_func(x):
      return torch.distributed._functional_collectives.all_reduce(x, reduceOp="sum", group=group)
  ```

### deprecation
- Compiling through FSDP2 hooks without graph breaks is no longer supported ([#174906](https://github.com/pytorch/pytorch/pull/174906)). If you use compiled autograd with FSDP2, update your code to allow graph breaks around FSDP2 hooks or disable compiled autograd for the FSDP2 training step.

  Version 2.11:
  ```python
  with torch._dynamo.config.patch(compiled_autograd=True):
      compiled_model = torch.compile(fsdp_model, fullgraph=True)
      loss = compiled_model(input).sum()
      loss.backward()
  ```

  Version 2.12:
  ```python
  # Either run FSDP2 backward without fullgraph.
  compiled_model = torch.compile(fsdp_model, fullgraph=False)
  loss = compiled_model(input).sum()
  loss.backward()

  # Or apply compile before applying FSDP
  compiled_model_pre_fsdp = torch.compile(model, fullgraph=True)
  compiled_model = fully_shard(compiled_model_pre_fsdp, ...)
  loss = compiled_model(input).sum()
  loss.backward()
  ```

### new features
- Add `Store::barrier` API and TCPStore client `BARRIER` support, reducing synchronization round trips compared to the existing `ADD`+`WAIT` pattern ([#174920](https://github.com/pytorch/pytorch/pull/174920))
- Add NCCL communicator `suspend()`, `resume()`, and `memory_stats()` APIs for managing communicator memory lifecycle ([#176300](https://github.com/pytorch/pytorch/pull/176300))
- Add `all_to_all` support in the Gloo backend ([#165435](https://github.com/pytorch/pytorch/pull/165435))
- Add `reduce_scatter_offset` to symmetric memory, supporting variable-sized block reductions with NVLink multicast or LSA fallback ([#177791](https://github.com/pytorch/pytorch/pull/177791))
- Enable `batch_isend_irecv` to work under `torch.compile` ([#161213](https://github.com/pytorch/pytorch/pull/161213))
- Add `torch.distributed.symmetric_memory.is_symm_mem_tensor()` API to check if a tensor is a symmetric memory tensor ([#178947](https://github.com/pytorch/pytorch/pull/178947))
- Convert `NanCheck` to a standalone op (`torch.ops.c10d.check_for_nan`) usable outside of `ProcessGroupNCCL` ([#174990](https://github.com/pytorch/pytorch/pull/174990))

### improvements
- Add configurable worker timeout and partial data support to the distributed debug server ([#176058](https://github.com/pytorch/pytorch/pull/176058))
- Add `timeout` parameter to `torch.distributed.barrier()` ([#174974](https://github.com/pytorch/pytorch/pull/174974))
- Add `reduce_scatter_tensor_coalesced` support to `ProcessGroupWrapper` ([#168961](https://github.com/pytorch/pytorch/pull/168961))
- Functional collectives API now automatically handles non-contiguous inputs instead of asserting ([#177965](https://github.com/pytorch/pytorch/pull/177965))
- FSDP2: Allow `ModuleList`/`ModuleDict` subclasses that implement `forward()` ([#175033](https://github.com/pytorch/pytorch/pull/175033))
- FSDP2: Support dataclass args/kwargs output without memory leakage ([#174692](https://github.com/pytorch/pytorch/pull/174692))
- DDP: Add `batched_grad_copy` option to reduce per-parameter kernel launches to 2 kernels per bucket ([#176638](https://github.com/pytorch/pytorch/pull/176638))
- DDP: Refactor bucket capacity config into `BucketCapacityConfig` dataclass ([#175217](https://github.com/pytorch/pytorch/pull/175217))
- Add signal name to `ChildFailedError` exitcode output for better debugging ([#175254](https://github.com/pytorch/pytorch/pull/175254))
- Add CUDA-aware detection for Cray MPICH ([#178323](https://github.com/pytorch/pytorch/pull/178323))
- Support `dist.broadcast` for FP8 tensors on GPUs older than SM90 ([#175884](https://github.com/pytorch/pytorch/pull/175884))
- Add `__torch_function__` handlers for distributed functions ([#176376](https://github.com/pytorch/pytorch/pull/176376))
- Enable `split_group` API for TorchComms on XPU ([#178236](https://github.com/pytorch/pytorch/pull/178236))
- Make py-spy dumps nonblocking by default ([#178312](https://github.com/pytorch/pytorch/pull/178312))
- Add `ncclx` and `gloo` to FlightRecorder trace analyzer backend allowlist ([#180268](https://github.com/pytorch/pytorch/pull/180268))
- Improve error message on symmetric memory handle exchange ([#178989](https://github.com/pytorch/pytorch/pull/178989))
- SymmMem: Add thread safety to NCCL and NVSHMEM backends ([#176551](https://github.com/pytorch/pytorch/pull/176551))
- Check NCCL terminate signal more frequently when exiting from heartbeat monitor ([#170000](https://github.com/pytorch/pytorch/pull/170000))
- `Implement missing methods in ProcessGroupWrapper` ([#178779](https://github.com/pytorch/pytorch/pull/178779))
- Add compute_estimator option for overlap scheduling ([#175204](https://github.com/pytorch/pytorch/pull/175204))
- [local_tensor] Add standalone rank_map/tensor_map functions ([#174795](https://github.com/pytorch/pytorch/pull/174795))

### bug fixes
- Fix `_CoalescingManager` not passing `Opts` to `allgather_into_tensor_coalesced()` ([#175379](https://github.com/pytorch/pytorch/pull/175379))
- Fix `_CoalescingManager` to raise exception when ops in the coalesced list are not the same type ([#175573](https://github.com/pytorch/pytorch/pull/175573))
- Fix `getenv`/`setenv` race condition causing segfault during NCCL initialization with heartbeat thread ([#167523](https://github.com/pytorch/pytorch/pull/167523))
- Fix HSDP `sync_module_states` broadcast order for buffers with meta-device initialization ([#178569](https://github.com/pytorch/pytorch/pull/178569))
- Fix `AsyncCollectiveTensor` inputs leaking into compiled regions, causing `RuntimeError` or silent data corruption in TP + compile workflows ([#179849](https://github.com/pytorch/pytorch/pull/179849))
- Fix potential infinite loop in FlightRecorder when multiple ProcessGroups run into barrier ([#179449](https://github.com/pytorch/pytorch/pull/179449))
- Fix activation checkpointing crash when passing `BlockMask` as argument ([#179215](https://github.com/pytorch/pytorch/pull/179215))
- Fix two forward passes of DDP-wrapped BatchNorm raising error ([#175851](https://github.com/pytorch/pytorch/pull/175851))
- Fix `USE_RCOM` typo to `USE_ROCM` in `intra_node_comm.cpp` ([#175078](https://github.com/pytorch/pytorch/pull/175078))
- Fix HPU backend mapping issue ([#174764](https://github.com/pytorch/pytorch/pull/174764))
- Fix NCCL symmetric memory mismatch by using allocation-time counter for Block ordering ([#178362](https://github.com/pytorch/pytorch/pull/178362))
- Fix `NCCLPeerAllocInfo` destructor to properly deregister windows and free resources ([#177459](https://github.com/pytorch/pytorch/pull/177459))
- Fix nested DDP causing _active_ddp_module cleared by inner _inside_ddp_module() ([#178364](https://github.com/pytorch/pytorch/pull/178364))
- Fix extra deps mapping and cycles after bucketing ([#177688](https://github.com/pytorch/pytorch/pull/177688))
- Add proper skips for FP8 on sm < 89 ([#170528](https://github.com/pytorch/pytorch/pull/170528))
- Fix cross type bucketing ([#175150](https://github.com/pytorch/pytorch/pull/175150))

### performance
- Improve `AsyncMM.cu` performance by avoiding redundant IO/compute via `ElementC` void type ([#178653](https://github.com/pytorch/pytorch/pull/178653))
- Improve Context Parallel head-tail load balancer indices creation performance (up to 1555x speedup for 1M sequence length) ([#178199](https://github.com/pytorch/pytorch/pull/178199))
- Improve tensor-to-allocation lookup in NCCL Symmetric Memory ([#176744](https://github.com/pytorch/pytorch/pull/176744))
- Avoid two probes when inserting handle into SymmMem cache ([#177463](https://github.com/pytorch/pytorch/pull/177463))

### docs
- Document FSDP2 communication grouping and scheduling semantics ([#176318](https://github.com/pytorch/pytorch/pull/176318))

### devs
- Add profiling name to NCCL collectives ([#173837](https://github.com/pytorch/pytorch/pull/173837))
- Add NCCL collective sequence number (`seq_num`) to Kineto profiler traces ([#177148](https://github.com/pytorch/pytorch/pull/177148))
- Add `RECORD_PARAM_COMMS` to symmetric memory CUDA ops for ProcessGroup metadata in profiler traces ([#178571](https://github.com/pytorch/pytorch/pull/178571))
- Capture async flag of collectives in PyTorch execution trace ([#169416](https://github.com/pytorch/pytorch/pull/169416))
- TorchComms: Flight Recorder debug server integration and hook support ([#175270](https://github.com/pytorch/pytorch/pull/175270), [#175561](https://github.com/pytorch/pytorch/pull/175561), [#178359](https://github.com/pytorch/pytorch/pull/178359))
- Refactor `NCCLDevCommManager` API design ([#177380](https://github.com/pytorch/pytorch/pull/177380))
- ROCm: Use `amdsmi` instead of `rocmsmi` for intra-node communication ([#176506](https://github.com/pytorch/pytorch/pull/176506))
- SymmMem: Improve CUDA hygiene ([#175616](https://github.com/pytorch/pytorch/pull/175616))
- SymmMem: Use host API to get NCCL peer pointer ([#176570](https://github.com/pytorch/pytorch/pull/176570))
- Split `_BackendWrapper` import to `torchcomms._backend_wrapper` module ([#177157](https://github.com/pytorch/pytorch/pull/177157), [#178352](https://github.com/pytorch/pytorch/pull/178352))
- ROCm: Enable cpp/c10d unit tests ([#169063](https://github.com/pytorch/pytorch/pull/169063))
- Fix FR script for coalesced collective not scheduled ([#177076](https://github.com/pytorch/pytorch/pull/177076))

### Untopiced

### not user facing
- test_matrix_ops.py: Add skip_if_lt_x_gpu(4) for test_mm_with_strided_input ([#175105](https://github.com/pytorch/pytorch/pull/175105))
- patch .comms attribute for ThreadLocalWorld warnings ([#175099](https://github.com/pytorch/pytorch/pull/175099))
- [Dist][CI] fix distributed timeout ([#175030](https://github.com/pytorch/pytorch/pull/175030))
- Apply PEP 604 type annotations to torch/testing ([#175925](https://github.com/pytorch/pytorch/pull/175925))
- Fix flaky test_extra_collectives by disabling shape padding ([#176137](https://github.com/pytorch/pytorch/pull/176137))
- Use correct head dim for XPU SDPA tests ([#175540](https://github.com/pytorch/pytorch/pull/175540))
- Apply up007 and up045 to torch/backends through torch/futures ([#176311](https://github.com/pytorch/pytorch/pull/176311))
- Fix MultiProcContinuousTest completion queue desync ([#176259](https://github.com/pytorch/pytorch/pull/176259))
- Apply up007 and up045 to test ([#176462](https://github.com/pytorch/pytorch/pull/176462))
- ROCm: Check for at least one compilation for each rank ([#175849](https://github.com/pytorch/pytorch/pull/175849))
- Fix failing test from annotation failure ([#176887](https://github.com/pytorch/pytorch/pull/176887))
- Skip 4-GPU distributed tests on 2-GPU runners ([#176924](https://github.com/pytorch/pytorch/pull/176924))
- Fix the BucketMode ([#175886](https://github.com/pytorch/pytorch/pull/175886))
- Extract runtime_estimations from OverlapScheduler ([#175174](https://github.com/pytorch/pytorch/pull/175174))
- Add OCCL ProcessGroup stub validation + distributed smoke tests ([#171250](https://github.com/pytorch/pytorch/pull/171250))
- Remove redundant inline_inbuilt_nn_modules=True patches from tests ([#177971](https://github.com/pytorch/pytorch/pull/177971))
- Delete tests that explicitly set inline_inbuilt_nn_modules=False ([#177979](https://github.com/pytorch/pytorch/pull/177979))
- ROCm: Remove ROCm skips after upstream Triton 3.7 pin update ([#178450](https://github.com/pytorch/pytorch/pull/178450))
- Use torch._utils.cpu_count ([#178743](https://github.com/pytorch/pytorch/pull/178743))
- Avoid multiprocess tests hanging forever ([#171972](https://github.com/pytorch/pytorch/pull/171972))
- Update pull test cases to support OSDC k8s migration ([#178738](https://github.com/pytorch/pytorch/pull/178738))
- Remove static from barrier tensor variable ([#178896](https://github.com/pytorch/pytorch/pull/178896))
- Slicing with backed should produce backed output when possible ([#178899](https://github.com/pytorch/pytorch/pull/178899))
- Replace erase idiom for map/set with erase_if ([#179373](https://github.com/pytorch/pytorch/pull/179373))
- Fix env var leak in NCCLTraceTestBase causing named pipe errors ([#179557](https://github.com/pytorch/pytorch/pull/179557))
- Extract bucket_mode from all passes to inductor config ([#175877](https://github.com/pytorch/pytorch/pull/175877))
- Add "coalesced" bucket_mode for zero-copy reduce_scatter bucketing ([#177132](https://github.com/pytorch/pytorch/pull/177132))
- Remove unused suppressions in torch/distributed ([#175257](https://github.com/pytorch/pytorch/pull/175257))
- Use () for tuple() for slightly improved performance ([#175492](https://github.com/pytorch/pytorch/pull/175492))
- Unify symmetric memory key and map types across backends ([#179903](https://github.com/pytorch/pytorch/pull/179903))
- Fix race condition in RPC test_tensor_view_as_return_value ([#175529](https://github.com/pytorch/pytorch/pull/175529))
- Address violations of warning unreachable-code-return ([#179518](https://github.com/pytorch/pytorch/pull/179518))

### security
