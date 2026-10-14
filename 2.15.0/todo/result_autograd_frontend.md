
# Release Notes worksheet autograd_frontend

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

## autograd_frontend
### bc breaking
- Selective activation checkpointing now saves, rather than recomputes, the outputs of operators with an ordered effect unless the policy returns `CheckpointPolicy.MUST_RECOMPUTE` ([#196956](https://github.com/pytorch/pytorch/pull/196956))

  Recomputing an effectful operator reruns its side effect. In eager mode, when a `create_selective_checkpoint_contexts` policy returns `PREFER_RECOMPUTE`, `PREFER_CPU_OFFLOAD` or `MUST_CPU_OFFLOAD` for an operator with an ordered effect (e.g. via `register_effect(torch.library.EffectType.ORDERED)`), its outputs are now saved as with `MUST_SAVE`, which can increase activation memory. Operators in the `c10d` namespace are excluded. Under `torch.compile`, `MUST_RECOMPUTE` on an effectful operator now raises at compile time: `RuntimeError: AOTAutograd does not support MUST_RECOMPUTE for effectful operations because forward effects cannot join the backward effect-token chain.` Use a save policy instead.

  ```python
  policy = lambda ctx, op, *args, **kwargs: CheckpointPolicy.PREFER_RECOMPUTE
  checkpoint(fn, x, use_reentrant=False, context_fn=lambda: create_selective_checkpoint_contexts(policy))
  # 2.14: an effectful op in fn runs twice; 2.15: once (use MUST_RECOMPUTE to replay)
  ```

### deprecation
### new features
- Add `ctx.input_grad_buffers` to custom `torch.autograd.Function` backward, exposing the engine's gradient accumulation buffers (or `None` when unavailable) so a fused kernel can accumulate an input's gradient in place and return `None` for it. Availability depends on backward order, so keep an out-of-place fallback; buffers must be updated synchronously within the current `backward` call, and the property is unavailable with `create_graph=True`, anomaly detection, or post-hooks on the producing node ([#196491](https://github.com/pytorch/pytorch/pull/196491))
- Add `torch.autograd.graph.queue_callback(callback)`, a public API to run a callback when the current backward pass finishes ([#193958](https://github.com/pytorch/pytorch/pull/193958))
### improvements
- Add backward and forward-mode AD for the `torch.special` Bessel functions ([#189872](https://github.com/pytorch/pytorch/pull/189872))
- Add forward-mode AD for `F.grid_sample` ([#195280](https://github.com/pytorch/pytorch/pull/195280))
- Add `torch._functorch.config.activation_memory_budget_require_full_coverage` to let `region_activation_memory_budget` apply to a whole compiled graph ([#195932](https://github.com/pytorch/pytorch/pull/195932))
- Allow reading `Tensor.grad_dtype` on non-leaf tensors ([#190852](https://github.com/pytorch/pytorch/pull/190852))
### bug fixes
- Fix `torch.fmin`/`fmax` gradients when one input is NaN ([#193035](https://github.com/pytorch/pytorch/pull/193035))
- Fix hooks on a view after an in-place update of its base using a stale `grad_fn` ([#196514](https://github.com/pytorch/pytorch/pull/196514))
- Fix fast-mode `gradcheck` checking the wrong output or raising `IndexError` ([#194222](https://github.com/pytorch/pytorch/pull/194222), [#194991](https://github.com/pytorch/pytorch/pull/194991))
- Fix `region_activation_memory_budget` across graph breaks ([#194808](https://github.com/pytorch/pytorch/pull/194808))
- Fix a segfault accessing a saved tensor after a pack hook raised ([#189160](https://github.com/pytorch/pytorch/pull/189160))
### performance
### docs
- Document that custom `Function`/op backward gradients may have arbitrary strides and that `unpack_hook` order is unspecified ([#195210](https://github.com/pytorch/pytorch/pull/195210), [#198016](https://github.com/pytorch/pytorch/pull/198016))
- Point `torch.utils.checkpoint` docs to `torch_remat` and drop the stale `use_reentrant` "version 2.9" error notice ([#193998](https://github.com/pytorch/pytorch/pull/193998), [#193720](https://github.com/pytorch/pytorch/pull/193720))
- Fix math rendering on the autograd mechanics page ([#192562](https://github.com/pytorch/pytorch/pull/192562))
### devs
### Untopiced
### not user facing
- Replace raw C++ `throw`s in autograd and Python bindings with the standard error-check macros ([#193618](https://github.com/pytorch/pytorch/pull/193618), [#194245](https://github.com/pytorch/pytorch/pull/194245))
- Avoid refcount churn and an oversized vector in generated autograd code ([#194882](https://github.com/pytorch/pytorch/pull/194882), [#195857](https://github.com/pytorch/pytorch/pull/195857))
- Add a private `Tensor._has_grad_dtype_override` property reporting whether `grad_dtype` was set explicitly ([#197504](https://github.com/pytorch/pytorch/pull/197504))
### security
