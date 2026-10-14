
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
- `torch.distributed.config.pipeline_per_direction_p2p` is renamed to `pipeline_per_edge_p2p` and now uses one communicator per directed rank-to-rank edge ([#196666](https://github.com/pytorch/pytorch/pull/196666))

  The old names were removed with no alias: setting the attribute raises `AttributeError: torch.distributed.config.pipeline_per_direction_p2p does not exist`, and `TORCH_DISTRIBUTED_PIPELINE_PER_DIRECTION_P2P` is silently ignored.

  Version 2.14:
  ```python
  dist_config.pipeline_per_direction_p2p = True
  ```

  Version 2.15:
  ```python
  dist_config.pipeline_per_edge_p2p = True  # or TORCH_DISTRIBUTED_PIPELINE_PER_EDGE_P2P=1
  ```
### deprecation
### new features
- Add `finalize_gradients` to pipeline schedule `step()` for gradient accumulation across several schedule runs with FSDP stages ([#196641](https://github.com/pytorch/pytorch/pull/196641))
- Add `PipelineStage.register_forward_context(factory)` to wrap each stage forward in a context manager that receives the stage and microbatch indices ([#196462](https://github.com/pytorch/pytorch/pull/196462))
- Add `torch.distributed.pipelining.analyze_pipeline_activation_liveness`, which computes activation lifetimes and reusable storage slots from a schedule ([#196464](https://github.com/pytorch/pytorch/pull/196464))
### improvements
- `is_symm_mem_enabled_for_group()` no longer requires the deprecated `enable_symm_mem_for_group()` call ([#193115](https://github.com/pytorch/pytorch/pull/193115))
- Add `WAIT_SEND_F`/`WAIT_SEND_B` schedule actions and an optional `max_outstanding_sends` limit on pending sends ([#196726](https://github.com/pytorch/pytorch/pull/196726), [#196727](https://github.com/pytorch/pytorch/pull/196727))
- Add a `max_active_stages` argument to multi-stage schedules to control how many FSDP stages stay unsharded at once ([#193972](https://github.com/pytorch/pytorch/pull/193972))
- Label pipeline schedule actions in CUDA graph traces captured with `enable_annotations=True` ([#195072](https://github.com/pytorch/pytorch/pull/195072))
- Initialize pipeline communicators with one setup sequence for manual and traced stages ([#197488](https://github.com/pytorch/pytorch/pull/197488))
### bug fixes
### performance
- Lower peak memory and improve overlap via lazy receive buffers and new `defer_reduce_grad_wait`/`unshard_lookahead` options ([#196463](https://github.com/pytorch/pytorch/pull/196463), [#196963](https://github.com/pytorch/pytorch/pull/196963), [#196725](https://github.com/pytorch/pytorch/pull/196725), [#196706](https://github.com/pytorch/pytorch/pull/196706))
### docs
### devs
### Untopiced
### not user facing
### security
