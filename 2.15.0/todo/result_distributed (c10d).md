
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

  `backend="nccl"` (also the default CUDA backend of `init_process_group()`) now creates a `ProcessGroupNCCL2`. The previous implementation is available as `backend="nccl-legacy"`. Differences:

  - Communicators are created eagerly in `init_process_group()`/`new_group()`, allocating GPU memory even for unused groups (`nccl-lazy` creates them on demand).
  - Each group is bound to one CUDA device: `device_id`, else `LOCAL_RANK % torch.cuda.device_count()` (or the global rank modulo the device count); `torch.cuda.set_device()` is not used. Tensors on another GPU fail with `Expected tensor on cuda:X but found tensor on cuda:Y` or `ProcessGroupNCCL is bound to device cuda:X but an operation was issued on cuda:Y`. Pass `device_id` if needed; several GPUs per process requires `nccl-legacy`.
  - `dist.get_backend_impl(...)` returns a `ProcessGroupNCCL2`, so `isinstance(..., ProcessGroupNCCL)` is `False` and legacy-only methods such as `comm_split_count()` are missing.
  - An async `all_gather`'s `work.get_future()` value is the list of per-rank outputs, not a one-element list holding a stacked tensor.

  To restore the old behavior, set `TORCH_DIST_USE_NCCL2=0` on every rank or use `nccl-legacy`:

  Version 2.14:
  ```python
  dist.init_process_group("nccl")  # ProcessGroupNCCL
  ```

  Version 2.15:
  ```python
  dist.init_process_group("nccl", device_id=torch.device("cuda", local_rank))  # ProcessGroupNCCL2
  dist.init_process_group("nccl-legacy")  # previous behavior
  ```
### deprecation
### new features
- Add an `nccl4py` backend (`init_process_group(backend="nccl4py")`), a Python-only NCCL backend built on the `nccl4py` bindings ([#191703](https://github.com/pytorch/pytorch/pull/191703), [#196331](https://github.com/pytorch/pytorch/pull/196331), [#198000](https://github.com/pytorch/pytorch/pull/198000), [#195766](https://github.com/pytorch/pytorch/pull/195766))
- Add an experimental one-sided transport API, `torch.distributed._transport`, with a NIXL backend and CUDA-graph-capturable stream-ordered transfers ([#195643](https://github.com/pytorch/pytorch/pull/195643), [#197032](https://github.com/pytorch/pytorch/pull/197032), [#198889](https://github.com/pytorch/pytorch/pull/198889), [#198918](https://github.com/pytorch/pytorch/pull/198918))
- Add an experimental pure-Python watchdog, `torch.distributed._watchdog`, that detects hung CPU and GPU operations in Python distributed backends and dumps thread stacks on timeout ([#192075](https://github.com/pytorch/pytorch/pull/192075))
- Add `get_peer_cft_handle(peer)` and `get_multimem_cft_handle()` to NCCL symmetric memory for NCCL Compute Fabric Transport ([#191685](https://github.com/pytorch/pytorch/pull/191685))
### improvements
- Extend `nccl2`: collective runtime estimation, the NCCL allocator for backend tensors, an opt-in shrink/grow `reconfigure()` path, legacy-matching errors, and windows and reconfiguration on ROCm ([#192854](https://github.com/pytorch/pytorch/pull/192854), [#192855](https://github.com/pytorch/pytorch/pull/192855), [#199240](https://github.com/pytorch/pytorch/pull/199240), [#194953](https://github.com/pytorch/pytorch/pull/194953), [#193282](https://github.com/pytorch/pytorch/pull/193282), [#194774](https://github.com/pytorch/pytorch/pull/194774))
- Add a `comm_ptr` property returning the `ncclComm_t` on all NCCL backends ([#197558](https://github.com/pytorch/pytorch/pull/197558), [#198865](https://github.com/pytorch/pytorch/pull/198865))
- Support `ReduceOp.PREMUL_SUM` in functional `all_reduce` and under `LocalTensorMode`, and backward for `MIN`/`MAX` ([#190942](https://github.com/pytorch/pytorch/pull/190942), [#193868](https://github.com/pytorch/pytorch/pull/193868), [#191947](https://github.com/pytorch/pytorch/pull/191947))
- Stop emitting a `FutureWarning` from `all_gather_into_tensor` and `reduce_scatter_tensor` ([#193874](https://github.com/pytorch/pytorch/pull/193874))
- Allow a CPU `device_id` in `init_process_group` ([#198340](https://github.com/pytorch/pytorch/pull/198340))
- Add `TORCH_NCCL_TEARDOWN_ON_TIMEOUT` to terminate on a legacy NCCL timeout instead of hanging ([#196187](https://github.com/pytorch/pytorch/pull/196187))
- Record the flight recorder for backends without built-in support (`nccl2`, MPI, UCC) and dump it on `nccl2` health-check failures ([#192233](https://github.com/pytorch/pytorch/pull/192233), [#199092](https://github.com/pytorch/pytorch/pull/199092))
- Support the symmetric memory `MemPool` on XPU ([#197065](https://github.com/pytorch/pytorch/pull/197065))
- Add an expert-major receive layout and zero-copy dispatch/combine to the experimental token-switch MoE dispatch API ([#187784](https://github.com/pytorch/pytorch/pull/187784), [#187785](https://github.com/pytorch/pytorch/pull/187785))
- Pass timeout and `enable_reconfigure` to dynamically created TorchComms communicators ([#199099](https://github.com/pytorch/pytorch/pull/199099))
### bug fixes
- Fix `nccl2` lifetime bugs: a crash or hang when `Work` outlives `destroy_process_group()`, tensors kept alive after `wait_tensor`, a stray CUDA context on GPU 0, failed nonblocking splits treated as ready, and errors destroying a group used in CUDA graphs ([#195485](https://github.com/pytorch/pytorch/pull/195485), [#193239](https://github.com/pytorch/pytorch/pull/193239), [#198339](https://github.com/pytorch/pytorch/pull/198339), [#199263](https://github.com/pytorch/pytorch/pull/199263), [#199226](https://github.com/pytorch/pytorch/pull/199226))
- Fix the flight recorder not attaching to `nccl` groups that use `nccl2` ([#192858](https://github.com/pytorch/pytorch/pull/192858))
- Fix single-rank legacy NCCL `reduce_scatter` dropping the `PREMUL_SUM` factor ([#198961](https://github.com/pytorch/pytorch/pull/198961))
- Fix all-zero gradients from coalesced functional collectives under `torch.compile` ([#196077](https://github.com/pytorch/pytorch/pull/196077))
- Fix functional `all_gather_single` with a negative `gather_dim` ([#194865](https://github.com/pytorch/pytorch/pull/194865))
- Fix `split_group` rejecting valid splits or hanging when backends differ from the default group ([#195758](https://github.com/pytorch/pytorch/pull/195758), [#197568](https://github.com/pytorch/pytorch/pull/197568))
- Fix a segfault when registering a second device for a backend type without passing a backend ([#195536](https://github.com/pytorch/pytorch/pull/195536))
- Fix Python `ProcessGroup` subclasses' `reconfigure` overrides being bypassed from C++ ([#198251](https://github.com/pytorch/pytorch/pull/198251))
- Fix `LocalTensorMode` collectives on groups with unsorted ranks ([#192777](https://github.com/pytorch/pytorch/pull/192777))
- Fix `NCCL host communicator for group ... not found` errors from separately linked extensions ([#193942](https://github.com/pytorch/pytorch/pull/193942))
- Fix symmetric memory synchronization: no-op NVSHMEM `barrier()`/`put_signal()`/`wait_signal()`, stream ordering, rendezvous and multicast hangs, signal-pad races, and freeing memory still in use ([#192579](https://github.com/pytorch/pytorch/pull/192579), [#195947](https://github.com/pytorch/pytorch/pull/195947), [#196350](https://github.com/pytorch/pytorch/pull/196350), [#195596](https://github.com/pytorch/pytorch/pull/195596), [#196546](https://github.com/pytorch/pytorch/pull/196546), [#192300](https://github.com/pytorch/pytorch/pull/192300), [#198306](https://github.com/pytorch/pytorch/pull/198306), [#196003](https://github.com/pytorch/pytorch/pull/196003))
### performance
- Speed up `all_gather_object` ([#196185](https://github.com/pytorch/pytorch/pull/196185))
- Share the parent `Store` connection across `split_group` child groups ([#196665](https://github.com/pytorch/pytorch/pull/196665))
### docs
- Add a tutorial for the distributed debug server ([#178800](https://github.com/pytorch/pytorch/pull/178800))
- Document `Backend.Options` and fix `irecv` and NCCL env var docs ([#196123](https://github.com/pytorch/pytorch/pull/196123), [#189623](https://github.com/pytorch/pytorch/pull/189623), [#194701](https://github.com/pytorch/pytorch/pull/194701))
### devs
- Make `FakeProcessGroup` support `all_to_all_single` with any sizes and add a `simulate_uniform_ranks` option ([#193985](https://github.com/pytorch/pytorch/pull/193985), [#194545](https://github.com/pytorch/pytorch/pull/194545))
- Fix a clang build error and add `amd_smi` as a ROCm 7.14+ build dependency ([#194104](https://github.com/pytorch/pytorch/pull/194104), [#192520](https://github.com/pytorch/pytorch/pull/192520))
- Add the private `torch.distributed._functional_collectives.wait_tensors`, which waits on all outputs of a multi-output functional collective at once; `torch.compile` uses it for coalesced collectives and `batch_isend_irecv` ([#193892](https://github.com/pytorch/pytorch/pull/193892))
### not user facing
- Prepare for the `nccl2` default switch: force `nccl-legacy` for internal builds, run legacy-only tests with `nccl-legacy`, and configure test timeouts through the `ProcessGroup` API ([#193221](https://github.com/pytorch/pytorch/pull/193221), [#193240](https://github.com/pytorch/pytorch/pull/193240), [#193238](https://github.com/pytorch/pytorch/pull/193238))
- Refactor `nccl2` `Work` completion state, completion hooks and input tensor ownership ahead of the lifetime fixes listed above ([#194830](https://github.com/pytorch/pytorch/pull/194830), [#194831](https://github.com/pytorch/pytorch/pull/194831), [#194832](https://github.com/pytorch/pytorch/pull/194832))
- Initialize the backend group UID in the `nccl2` constructor, fixing a symmetric-memory rendezvous regression caused by eager initialization (#192895) in this release ([#194935](https://github.com/pytorch/pytorch/pull/194935))
- Factor TorchComms backend creation into a reusable helper ([#197616](https://github.com/pytorch/pytorch/pull/197616))
- Replace raw C++ `throw`s with `TORCH_CHECK`-family macros in `torch/csrc/distributed` while keeping the same Python exception types ([#193612](https://github.com/pytorch/pytorch/pull/193612), [#195149](https://github.com/pytorch/pytorch/pull/195149), [#195763](https://github.com/pytorch/pytorch/pull/195763))
- Code cleanups: `fmap`/`filter` rvalue overloads, range-based for loops, and comment/docstring typo fixes ([#194929](https://github.com/pytorch/pytorch/pull/194929), [#196097](https://github.com/pytorch/pytorch/pull/196097), [#193967](https://github.com/pytorch/pytorch/pull/193967))
- Fix a threaded process group teardown crash in the test utilities ([#196786](https://github.com/pytorch/pytorch/pull/196786))
- Test fixes: hardcoded rendezvous ports, ROCm NaN-check tests, and the ROCm torchcomms test harness ([#195994](https://github.com/pytorch/pytorch/pull/195994), [#197885](https://github.com/pytorch/pytorch/pull/197885), [#196907](https://github.com/pytorch/pytorch/pull/196907))
- Use the NVLS multicast (multimem) barrier for CUDA symmetric memory when a multicast mapping is available ([#192861](https://github.com/pytorch/pytorch/pull/192861)) (cut for length)
### security
