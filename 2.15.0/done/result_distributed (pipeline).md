
# Release Notes worksheet distributed (pipeline)

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

## distributed (pipeline)
### bc breaking
- `torch.distributed.config.pipeline_per_direction_p2p` is renamed to `pipeline_per_edge_p2p` and now uses a separate communicator for each directed rank-to-rank pipeline edge ([#196666](https://github.com/pytorch/pytorch/pull/196666))

  In 2.14 this option split pipeline P2P traffic into one forward communicator and one backward communicator. When one physical rank hosts several logical stages, unrelated edges could still share a communicator, and skew between ranks in looped or V-shaped schedules could form ordering cycles. The option now creates one child communicator per directed physical-rank edge after the schedule has fixed its stage placement, and connects them during schedule initialization. The old config name and the `TORCH_DISTRIBUTED_PIPELINE_PER_DIRECTION_P2P` environment variable were removed with no alias. Setting the old attribute raises `AttributeError: torch.distributed.config.pipeline_per_direction_p2p does not exist`, and the old environment variable is silently ignored. Use the new names. As before, the behavior is enabled automatically when TorchComms is in use.

  Version 2.14:
  ```python
  import torch.distributed.config as dist_config

  dist_config.pipeline_per_direction_p2p = True
  # or: TORCH_DISTRIBUTED_PIPELINE_PER_DIRECTION_P2P=1
  ```

  Version 2.15:
  ```python
  import torch.distributed.config as dist_config

  dist_config.pipeline_per_edge_p2p = True
  # or: TORCH_DISTRIBUTED_PIPELINE_PER_EDGE_P2P=1
  ```
### deprecation
### new features
- Add `finalize_gradients` to pipeline schedule `step()` for gradient accumulation across several complete schedule runs with FSDP stages. Pass `finalize_gradients=False` to keep FSDP gradients unreduced and parameters unsharded between calls, then pass `True` on the last call to reduce gradients and reshard ([#196641](https://github.com/pytorch/pytorch/pull/196641))
- Add `PipelineStage.register_forward_context(factory)` and `torch.distributed.pipelining.PipelineStageInfo`. The registered factory wraps each stage forward in a context manager and receives the global logical stage index, the microbatch index, and whether the call is metadata inference, without changing the module's forward signature ([#196462](https://github.com/pytorch/pytorch/pull/196462))
- Add `torch.distributed.pipelining.analyze_pipeline_activation_liveness`. It computes, from a schedule, how long each activation stays live between forward and backward, and assigns reusable storage slots to `(stage, microbatch)` pairs for memory planning ([#196464](https://github.com/pytorch/pytorch/pull/196464))
### improvements
- `torch.distributed._symmetric_memory.is_symm_mem_enabled_for_group()` no longer requires the deprecated `enable_symm_mem_for_group()` call. Async tensor-parallel fusions, one-shot all-reduce selection, and the low-contention collectives pass now work without it ([#193115](https://github.com/pytorch/pytorch/pull/193115))
- Add explicit `WAIT_SEND_F` and `WAIT_SEND_B` schedule actions, so every pipeline send has a matching wait that defines when its buffers can be released ([#196726](https://github.com/pytorch/pytorch/pull/196726))
- Add an optional `max_outstanding_sends` limit to runtime pipeline schedules. Send waits are moved earlier to keep the number of pending sends per rank within the limit, and an error is raised if the limit cannot be met safely ([#196727](https://github.com/pytorch/pytorch/pull/196727))
- Initialize pipeline communicators with a single explicit setup sequence for both manual and traced stages, so communicator readiness no longer depends on the metadata mode ([#197488](https://github.com/pytorch/pytorch/pull/197488))
- Add a `max_active_stages` argument (default 3) to the multi-stage pipeline schedules (`ScheduleInterleaved1F1B`, `ScheduleLoopedBFS`, `ScheduleInterleavedZeroBubble`, `ScheduleZBVZeroBubble`, `ScheduleDualPipeV`) to control how many FSDP stages stay unsharded at once, for example to avoid repeated all-gathers with four virtual stages per rank ([#193972](https://github.com/pytorch/pytorch/pull/193972))
- Label each pipeline schedule action in CUDA graph traces captured with `enable_annotations=True`, so replayed kernels can be mapped back to their schedule action ([#195072](https://github.com/pytorch/pytorch/pull/195072))
### bug fixes
### performance
- Allocate pipeline receive buffers right before each receive instead of for every microbatch at setup, and release forward outputs once their sends complete, which lowers peak activation memory ([#196463](https://github.com/pytorch/pytorch/pull/196463), [#196963](https://github.com/pytorch/pytorch/pull/196963))
- Add `defer_reduce_grad_wait` to pipeline schedules. It splits FSDP gradient reduction into separate `REDUCE_GRAD` and `WAIT_REDUCE_GRAD` actions, so a stage's gradient reduction can overlap the next local stage's backward ([#196725](https://github.com/pytorch/pytorch/pull/196725))
- Add `unshard_lookahead` (`"full"`, `"auto"`, or a per-rank tuple) to control how far ahead FSDP unshards are issued, separately from `max_active_stages`. This avoids putting all-gather work ahead of the first forward computation ([#196706](https://github.com/pytorch/pytorch/pull/196706))
### docs
### devs
### Untopiced
### not user facing
### security
