
# Release Notes worksheet distributed (fsdp)

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

## distributed (fsdp)
### bc breaking
### deprecation
### new features
- Add manual backward finalization to `fully_shard`. Call `FSDPModule.set_manual_backward_finalization(True)` on the root module, then call `FSDPModule.finalize_backward()` on the calling thread to finish pending gradient reduction and resharding. This lets you place gradient reduction at a point of your choosing, for example after several backward passes or inside a CUDA graph, instead of in the autograd final callback ([#196640](https://github.com/pytorch/pytorch/pull/196640))
- Add `finalize_backward(async_op=True)`, which returns a `torch.distributed.fsdp.GradientReductionHandle` instead of blocking. Call `handle.wait()` before reading gradients or starting more work on the module, so gradient reduction can overlap other compute ([#196724](https://github.com/pytorch/pytorch/pull/196724))
- Add `param_dtype_override_fn` to `MixedPrecisionPolicy` for per-parameter mixed precision in `fully_shard`. The callable runs once per parameter and returns `None`, `param_dtype`, or the parameter's original dtype, so selected parameters can stay in full precision while still using one all-gather per `fully_shard` group ([#196626](https://github.com/pytorch/pytorch/pull/196626))
- Add `FSDPModule.set_keep_unsharded_storage()`, which keeps the unsharded parameter storage allocated across `reshard()`, so storage addresses stay stable between unshard and reshard ([#198417](https://github.com/pytorch/pytorch/pull/198417))
- Allow tensor-subclass parameters that implement the FSDP extension hooks to free the raw all-gather buffers right after `fsdp_post_all_gather`. Implement `fsdp_should_release_all_gather_outputs_after_post_all_gather()` and return `True`; the transformed tensors are kept until the normal reshard ([#194114](https://github.com/pytorch/pytorch/pull/194114))
### improvements
### bug fixes
- Fix `AttributeError: 'FSDPParam' object has no attribute '_unsharded_param'` during gradient accumulation when `reduce_dtype` differs from the parameter dtype and some parameters were not used in forward ([#194058](https://github.com/pytorch/pytorch/pull/194058))
- Fix silently wrong gradients with `ShardingStrategy.NO_SHARD` and `CPUOffload(offload_params=True)`, which happened because a device buffer was freed and reused while still in use ([#194519](https://github.com/pytorch/pytorch/pull/194519))
- Fix wrap overrides leaking between modules through a shared mutable default dictionary when overriding module mixed precision ([#194895](https://github.com/pytorch/pytorch/pull/194895))
- Fix `fully_shard` keeping the last prefetched all-gather output alive through backward when part of the model runs outside the grouped forward ([#196460](https://github.com/pytorch/pytorch/pull/196460))
- Fix possible use-after-free of the reduce-scatter output on backends that free memory eagerly across streams, by recording the consumer stream on it ([#193686](https://github.com/pytorch/pytorch/pull/193686))
- Fix silently wrong gradients with `set_all_reduce_hook` when the hook runs on a separate stream: the next group's reduce-scatter could overwrite the output before the hook finished reading it ([#198804](https://github.com/pytorch/pytorch/pull/198804))
- Fix CUDA graph capture failing with `cudaErrorStreamCaptureUnjoined` when backward finalization cleans up a prefetched all-gather that was never used ([#199677](https://github.com/pytorch/pytorch/pull/199677))
- Fix the single-rank all-gather path converting values instead of copying bytes when an extension's `fsdp_pre_all_gather` returns a `uint8` view. This caused size-mismatch errors, or silently wrong values for one-byte dtypes such as float8 ([#199733](https://github.com/pytorch/pytorch/pull/199733))
### performance
### docs
- Document that modifying parameters between forward and backward is not supported with `fully_shard` ([#198826](https://github.com/pytorch/pytorch/pull/198826))
### devs
### Untopiced
### not user facing
- Widen type annotations for internal FSDP all-reduce streams from `torch.cuda.Stream` to `torch.Stream` ([#196563](https://github.com/pytorch/pytorch/pull/196563))
- Make FSDP test infrastructure device-agnostic for out-of-tree accelerators ([#187650](https://github.com/pytorch/pytorch/pull/187650))
### security
