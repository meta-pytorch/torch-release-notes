
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
- The `nccl` backend now uses the `nccl2` implementation by default ([#192281](https://github.com/pytorch/pytorch/pull/192281), [#192895](https://github.com/pytorch/pytorch/pull/192895), [#193237](https://github.com/pytorch/pytorch/pull/193237), [#193241](https://github.com/pytorch/pytorch/pull/193241))

  PyTorch 2.14 added `nccl2`, a new NCCL backend ported from torchcomms, as an experimental opt-in (`backend="nccl2"` or `TORCH_DIST_USE_NCCL2=1`). In PyTorch 2.15, `backend="nccl"` creates a `ProcessGroupNCCL2` by default. This also applies to the CUDA backend that `init_process_group()` picks when no backend is given. The previous implementation is still available as `backend="nccl-legacy"`. Training results are expected to be unchanged, but `nccl2` differs from the legacy backend in these ways:

  - NCCL communicators are created eagerly when `init_process_group()` or `new_group()` is called, not at the first collective. Each group's NCCL resources and GPU memory are allocated at creation time, even if the group is never used. `nccl-lazy` keeps creating per-peer communicators on demand. Pipeline-parallel stages that run on an eager NCCL group now log a one-time warning that suggests creating the group with `backend="nccl-lazy"`.
  - Each process group is bound to a single CUDA device when it is created. If `device_id` is not passed to `init_process_group()`, the device is `LOCAL_RANK % torch.cuda.device_count()` when `LOCAL_RANK` is set, and otherwise the global rank modulo the device count. The device selected with `torch.cuda.set_device()` is not used. A collective on a tensor that lives on another GPU fails with `Expected tensor on cuda:X but found tensor on cuda:Y` or `ProcessGroupNCCL is bound to device cuda:X but an operation was issued on cuda:Y`. If your ranks do not map to GPUs this way, pass `device_id` explicitly. Using several GPUs from one process requires `nccl-legacy`.
  - The backend object returned by `dist.get_backend_impl(device="cuda")` or `pg._get_backend(torch.device("cuda"))` is now a `ProcessGroupNCCL2`, not a `ProcessGroupNCCL`. As a result, `isinstance(..., ProcessGroupNCCL)` checks return `False`, and methods that only exist on the legacy class (for example `comm_split_count()` and `get_build_nccl_version()`) are missing. The `comm_ptr` property and `_comm_ptr()` method work on every NCCL backend.
  - For an asynchronous `all_gather`, the value of `work.get_future()` is the list of per-rank output tensors. The legacy backend returned a one-element list holding a stacked `[world_size, ...]` tensor. Code such as DDP communication hooks that indexes the future's value should read the output tensor list it passed to `all_gather` instead, which works with both backends.

  To restore the previous behavior, set `TORCH_DIST_USE_NCCL2=0` in the environment of every rank before the first process group is created, or request `nccl-legacy` explicitly:

  Version 2.14:
  ```python
  # "nccl" resolves to the legacy ProcessGroupNCCL; communicators are
  # created lazily on the device of the first collective's tensors.
  dist.init_process_group("nccl")
  type(dist.get_backend_impl(device="cuda"))  # ProcessGroupNCCL
  ```

  Version 2.15:
  ```python
  # "nccl" resolves to nccl2; the communicator is created during
  # init_process_group on device_id (or LOCAL_RANK % device_count).
  dist.init_process_group("nccl", device_id=torch.device("cuda", local_rank))
  type(dist.get_backend_impl(device="cuda"))  # ProcessGroupNCCL2

  # Keep the legacy implementation:
  dist.init_process_group("nccl-legacy")
  # or launch with: TORCH_DIST_USE_NCCL2=0 torchrun ...
  ```
### deprecation
### new features
- Add `torch.distributed._functional_collectives.wait_tensors` (backed by the new `torch.ops._c10d_functional.wait_tensors` op). It waits on all outputs of a multi-output functional collective at once and waits on each underlying `Work` only once. Under `torch.compile`, coalesced functional collectives and `batch_isend_irecv` now use one batched wait instead of a separate `wait_tensor` per output ([#193892](https://github.com/pytorch/pytorch/pull/193892))
- Add an `nccl4py` backend, a Python-only NCCL backend for `torch.distributed` built on the `nccl4py` bindings. Select it with `init_process_group(backend="nccl4py")` (requires the `nccl4py` package). It supports the core collectives, point-to-point operations, coalescing, communicator splitting and `PREMUL_SUM`, and is registered through the `torch.distributed.backends` entry point ([#191703](https://github.com/pytorch/pytorch/pull/191703), [#196331](https://github.com/pytorch/pytorch/pull/196331), [#198000](https://github.com/pytorch/pytorch/pull/198000), [#195766](https://github.com/pytorch/pytorch/pull/195766))
- Add an experimental one-sided transport API in `torch.distributed._transport`. It includes a backend registry, a NIXL backend, `new_transport_rank` for connecting transports through a `Store` without collectives, and `Transport.read_stream`/`write_stream` for transfers that are ordered on a CUDA stream and can be captured in CUDA graphs ([#195643](https://github.com/pytorch/pytorch/pull/195643), [#197032](https://github.com/pytorch/pytorch/pull/197032), [#198889](https://github.com/pytorch/pytorch/pull/198889), [#198918](https://github.com/pytorch/pytorch/pull/198918))
- Add an experimental pure-Python watchdog, `torch.distributed._watchdog` (`stream_timeout`, `cpu_timeout`, `shutdown`), that detects hung CPU and GPU operations in Python distributed backends and primitives. On timeout it dumps all thread stacks and aborts the process by default ([#192075](https://github.com/pytorch/pytorch/pull/192075))
- Expose NCCL Compute Fabric Transport (CFT) logical endpoints from NCCL symmetric memory through `get_peer_cft_handle(peer)` and `get_multimem_cft_handle()`, plus a `host_cft_mode` field on `ProcessGroupNCCL.NCCLConfig`. Custom kernels can use these to write into peer memory with CFT. Requires NCCL 2.31.2 or newer ([#191685](https://github.com/pytorch/pytorch/pull/191685))
### improvements
- Add more features to the `nccl2` backend: collective runtime estimation, used by compiler-driven communication scheduling ([#192854](https://github.com/pytorch/pytorch/pull/192854)); backend tensor allocation through the NCCL allocator for FSDP and Inductor ([#192855](https://github.com/pytorch/pytorch/pull/192855)); and an opt-in shrink/grow fast path for `reconfigure()`, enabled with `TORCH_NCCL2_RECONFIGURE_SHRINK_GROW=1` (requires NCCL 2.29 or newer) ([#199240](https://github.com/pytorch/pytorch/pull/199240))
- Match the legacy NCCL backend's argument validation, exception types and timeout messages in `nccl2` ([#194953](https://github.com/pytorch/pytorch/pull/194953))
- Enable `nccl2` one-sided windows and communicator reconfiguration on ROCm. Window memory must come from the backend's NCCL memory allocator ([#193282](https://github.com/pytorch/pytorch/pull/193282), [#194774](https://github.com/pytorch/pytorch/pull/194774))
- Add a documented `comm_ptr` property, plus a `_comm_ptr()` method for backward compatibility, that returns the underlying `ncclComm_t` as an opaque handle on the `nccl-legacy`, `nccl2` and `nccl-lazy` backends ([#197558](https://github.com/pytorch/pytorch/pull/197558), [#198865](https://github.com/pytorch/pytorch/pull/198865))
- Support `ReduceOp.PREMUL_SUM` in functional `all_reduce` and `all_reduce_coalesced`, and add backward support for `MIN` and `MAX` reductions ([#190942](https://github.com/pytorch/pytorch/pull/190942), [#193868](https://github.com/pytorch/pytorch/pull/193868))
- Stop emitting a `FutureWarning` from `all_gather_into_tensor`, `gather_into_tensor` and `reduce_scatter_tensor`. They remain supported aliases of `all_gather_single`, `gather_single` and `reduce_scatter_single` ([#193874](https://github.com/pytorch/pytorch/pull/193874))
- Allow a CPU `device_id` (for example `torch.device("cpu", 0)`) in `init_process_group`, so `device_id` can be used with Gloo ([#198340](https://github.com/pytorch/pytorch/pull/198340))
- Add the `TORCH_NCCL_TEARDOWN_ON_TIMEOUT` environment variable (default off). It makes the legacy NCCL backend terminate the process on a collective timeout even when `TORCH_NCCL_RETHROW_CUDA_ERRORS=0`, instead of hanging ([#196187](https://github.com/pytorch/pytorch/pull/196187))
- Support `ReduceOp.PREMUL_SUM` for collectives under `LocalTensorMode` ([#191947](https://github.com/pytorch/pytorch/pull/191947))
- Add an expert-major receive layout and zero-copy dispatch/combine from NCCL symmetric memory to the experimental token-switch MoE dispatch API ([#187784](https://github.com/pytorch/pytorch/pull/187784), [#187785](https://github.com/pytorch/pytorch/pull/187785))
- Pass timeout and `enable_reconfigure` through to dynamically created TorchComms communicators ([#199099](https://github.com/pytorch/pytorch/pull/199099))
- Record collectives in the flight recorder for backends that have no built-in flight recorder support, including `nccl2` (now the default `nccl` implementation), MPI, UCC and out-of-tree backends. Recording is enabled by the existing `TORCH_FR_BUFFER_SIZE`/`TORCH_NCCL_TRACE_BUFFER_SIZE` setting, and the trace is dumped to disk when a collective fails or times out, honoring `TORCH_FR_DUMP_ON_TIMEOUT`. The debug server's flight recorder pages take a `backend` query parameter to select the backend, and gain a `/fr_dump_file` page ([#192233](https://github.com/pytorch/pytorch/pull/192233))
- Publish `nccl2` watchdog health to the distributed debug server through a new `c10d_health_check` handler (enabled by default). When any rank reports an unhealthy backend, the debug server requests a flight recorder dump from every rank ([#199092](https://github.com/pytorch/pytorch/pull/199092))
- Support the implicit symmetric memory `MemPool` on XPU, so `symm_mem.empty()`, `get_mem_pool()` and Inductor's symmetric-memory communication buffers work on XPU devices ([#197065](https://github.com/pytorch/pytorch/pull/197065))
### bug fixes
- Fix a heap corruption or hang when an asynchronous `Work` from the `nccl2` backend is released after `destroy_process_group()` ([#195485](https://github.com/pytorch/pytorch/pull/195485))
- Fix `nccl2` keeping functional collective tensors alive after `wait_tensor`, which raised memory usage ([#193239](https://github.com/pytorch/pytorch/pull/193239))
- Fix the `nccl2` watchdog thread creating a CUDA context on GPU 0 (about 500 MiB per rank) for communicators on other GPUs ([#198339](https://github.com/pytorch/pytorch/pull/198339))
- Fix `nccl2` accepting a failed child communicator from a nonblocking split or shrink as ready ([#199263](https://github.com/pytorch/pytorch/pull/199263))
- Fix `CUDA error: operation not permitted` when destroying an `nccl2` process group whose collectives were captured in a CUDA graph ([#199226](https://github.com/pytorch/pytorch/pull/199226))
- Fix the flight recorder not being attached to process groups created with the default `nccl` name when it resolves to `nccl2`, and fix a completion race in the flight recorder ([#192858](https://github.com/pytorch/pytorch/pull/192858))
- Fix single-rank `reduce_scatter` on the legacy NCCL backend silently dropping the `PREMUL_SUM` scaling factor ([#198961](https://github.com/pytorch/pytorch/pull/198961))
- Fix all-zero gradients from coalesced functional collectives (for example `all_reduce_coalesced`) under `torch.compile` by registering autograd for `wait_tensors` ([#196077](https://github.com/pytorch/pytorch/pull/196077))
- Fix functional `all_gather_single` with a negative `gather_dim` raising `RuntimeError: shape '[...]' is invalid for input of size ...` ([#194865](https://github.com/pytorch/pytorch/pull/194865))
- Fix `split_group` rejecting a valid split when the parent group's backend is initialized but the lazily created default group is not ([#195758](https://github.com/pytorch/pytorch/pull/195758))
- Fix a possible hang or desynchronization when splitting a subgroup whose backend differs from the eagerly initialized default group's backend ([#197568](https://github.com/pytorch/pytorch/pull/197568))
- Fix a segfault when registering a second device for an already registered backend type without passing a backend ([#195536](https://github.com/pytorch/pytorch/pull/195536))
- Fix Python `ProcessGroup` subclasses whose `reconfigure`, `get_reconfigure_handle` and `supports_reconfigure` overrides were bypassed when called through the C++ bindings ([#198251](https://github.com/pytorch/pytorch/pull/198251))
- Fix collectives under `LocalTensorMode` on process groups whose ranks are not in sorted order ([#192777](https://github.com/pytorch/pytorch/pull/192777))
- Fix `NCCL host communicator for group ... not found` errors from separately linked extensions (such as NCCL expert parallelism) by sharing the NCCL device-communicator registry across shared libraries ([#193942](https://github.com/pytorch/pytorch/pull/193942))
- Fix NVSHMEM symmetric memory `barrier()`, `put_signal()` and `wait_signal()`, which were empty stubs that did not synchronize. Peers that are not reachable over P2P now raise a not-implemented error ([#192579](https://github.com/pytorch/pytorch/pull/192579))
- Fix several symmetric memory hangs and races: enforce stream ordering for signal-pad operations issued from different streams on CUDA and NCCL backends ([#195947](https://github.com/pytorch/pytorch/pull/195947)); a hang on a full-group rendezvous after a subgroup rendezvous ([#196350](https://github.com/pytorch/pytorch/pull/196350)); multicast setup reporting success before the mapping existed, or hanging when a rank failed to set it up ([#195596](https://github.com/pytorch/pytorch/pull/195596)); a race zeroing NVSHMEM signal pads ([#196546](https://github.com/pytorch/pytorch/pull/196546)); and an out-of-bounds shared-memory write in the NVSHMEM `all_to_all_v_2d` kernel ([#192300](https://github.com/pytorch/pytorch/pull/192300))
- Fix symmetric memory cleanup: synchronize the device before freeing CUDA, NCCL and NVSHMEM allocations so tensors are not unmapped while kernels still use them ([#198306](https://github.com/pytorch/pytorch/pull/198306)), and warn instead of calling `std::terminate` (which hid the original error) when cleanup fails in a broken CUDA context ([#196003](https://github.com/pytorch/pytorch/pull/196003))
### performance
- Use the NVLS multicast (multimem) barrier for CUDA symmetric memory when a multicast mapping is available ([#192861](https://github.com/pytorch/pytorch/pull/192861))
- Speed up `all_gather_object` by gathering into a single tensor with `all_gather_single`, removing extra device copies and concatenation ([#196185](https://github.com/pytorch/pytorch/pull/196185))
- Share the parent `Store` connection, under a unique key prefix, for communicators created by `split_group` instead of cloning a `Store` (and a TCP connection) per child group. This greatly reduces connections for pipeline schedules that create many groups ([#196665](https://github.com/pytorch/pytorch/pull/196665))
### docs
- Add a tutorial for the distributed debug server ([#178800](https://github.com/pytorch/pytorch/pull/178800))
- Document `Backend.Options` and fix docstrings that referred to a nonexistent `ProcessGroupOptions` type ([#196123](https://github.com/pytorch/pytorch/pull/196123))
- Fix the `group_src` description in the `irecv` docstring ([#189623](https://github.com/pytorch/pytorch/pull/189623))
- Remove leftover documentation of `TORCH_NCCL_AVOID_RECORD_STREAMS`, which has been ignored for over a year ([#194701](https://github.com/pytorch/pytorch/pull/194701))
### devs
- Fix a clang build error from an unescaped `%` in CUDA symmetric memory inline assembly ([#194104](https://github.com/pytorch/pytorch/pull/194104))
- Add `amd_smi` as a build-time dependency for ROCm 7.14 and newer ([#192520](https://github.com/pytorch/pytorch/pull/192520))
- Make the fake process group used for testing support `all_to_all_single` with any input and output sizes, filling unreceived output with zeros ([#193985](https://github.com/pytorch/pytorch/pull/193985))
- Add an opt-in `simulate_uniform_ranks` option to `FakeProcessGroup.Options`, which makes fake collectives apply the reduce op and produce output with the correct shape, as if every rank held the same input ([#194545](https://github.com/pytorch/pytorch/pull/194545))
### not user facing
- Prepare for the `nccl2` default switch: force `nccl-legacy` for internal builds, run legacy-only tests with `nccl-legacy`, and configure test timeouts through the `ProcessGroup` API ([#193221](https://github.com/pytorch/pytorch/pull/193221), [#193240](https://github.com/pytorch/pytorch/pull/193240), [#193238](https://github.com/pytorch/pytorch/pull/193238))
- Refactor `nccl2` `Work` completion state, completion hooks and input tensor ownership ahead of the lifetime fixes listed above ([#194830](https://github.com/pytorch/pytorch/pull/194830), [#194831](https://github.com/pytorch/pytorch/pull/194831), [#194832](https://github.com/pytorch/pytorch/pull/194832))
- Initialize the backend group UID in the `nccl2` constructor, fixing a symmetric-memory rendezvous regression caused by eager initialization (#192895) in this release ([#194935](https://github.com/pytorch/pytorch/pull/194935))
- Factor TorchComms backend creation into a reusable helper ([#197616](https://github.com/pytorch/pytorch/pull/197616))
- Replace raw C++ `throw`s with `TORCH_CHECK`-family macros in `torch/csrc/distributed` while keeping the same Python exception types ([#193612](https://github.com/pytorch/pytorch/pull/193612), [#195149](https://github.com/pytorch/pytorch/pull/195149), [#195763](https://github.com/pytorch/pytorch/pull/195763))
- Code cleanups: `fmap`/`filter` rvalue overloads, range-based for loops, and comment/docstring typo fixes ([#194929](https://github.com/pytorch/pytorch/pull/194929), [#196097](https://github.com/pytorch/pytorch/pull/196097), [#193967](https://github.com/pytorch/pytorch/pull/193967))
- Fix a threaded process group teardown crash in the test utilities ([#196786](https://github.com/pytorch/pytorch/pull/196786))
- Test fixes: hardcoded rendezvous ports, ROCm NaN-check tests, and the ROCm torchcomms test harness ([#195994](https://github.com/pytorch/pytorch/pull/195994), [#197885](https://github.com/pytorch/pytorch/pull/197885), [#196907](https://github.com/pytorch/pytorch/pull/196907))
### security
