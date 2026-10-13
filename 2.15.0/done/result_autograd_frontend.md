
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

  Recomputing an operator with a side effect runs that side effect a second time during backward. In eager mode, when a `create_selective_checkpoint_contexts` policy returns `PREFER_RECOMPUTE`, `PREFER_CPU_OFFLOAD` or `MUST_CPU_OFFLOAD` for a non-aliasing operator with an ordered effect, `torch.utils.checkpoint` now saves its outputs as if the policy were `MUST_SAVE`. This applies to operators registered with an ordered effect through `torch.library` (e.g. `custom_op.register_effect(torch.library.EffectType.ORDERED)`) and to operators inferred to be effectful from TorchBind arguments; operators in the `c10d` namespace are excluded. Such operators now run once instead of twice, and their outputs stay alive until backward, which can increase activation memory. To keep replaying the operator in eager mode, return `CheckpointPolicy.MUST_RECOMPUTE` for it.

  Under `torch.compile`, effectful operators with `PREFER_RECOMPUTE` are now also saved, while `MUST_RECOMPUTE` on an effectful operator, which previously failed later inside the AOTAutograd runtime, now raises at compile time: `RuntimeError: AOTAutograd does not support MUST_RECOMPUTE for effectful operations because forward effects cannot join the backward effect-token chain.` Change the policy for that operator to a save policy when compiling.

  Version 2.14:
  ```python
  import torch
  from torch.utils.checkpoint import checkpoint, create_selective_checkpoint_contexts, CheckpointPolicy

  calls = 0

  @torch.library.custom_op("mylib::log_and_clone", mutates_args=())
  def log_and_clone(x: torch.Tensor) -> torch.Tensor:
      global calls
      calls += 1
      return x.clone()

  log_and_clone.register_autograd(lambda ctx, grad: grad)
  log_and_clone.register_effect(torch.library.EffectType.ORDERED)

  def context_fn():
      return create_selective_checkpoint_contexts(lambda ctx, op, *args, **kwargs: CheckpointPolicy.PREFER_RECOMPUTE)

  x = torch.randn(3, requires_grad=True)
  checkpoint(lambda t: log_and_clone(t).sin(), x, use_reentrant=False, context_fn=context_fn).sum().backward()
  print(calls)  # 2: the effectful op was replayed during backward
  ```

  Version 2.15:
  ```python
  # same code as above
  print(calls)  # 1: the effectful op's output is saved instead of recomputed

  # To keep the old eager replay, request it explicitly:
  def context_fn():
      return create_selective_checkpoint_contexts(lambda ctx, op, *args, **kwargs: CheckpointPolicy.MUST_RECOMPUTE)
  ```

### deprecation
### new features
- Add `ctx.input_grad_buffers` to custom `torch.autograd.Function` backward, which exposes the autograd engine's existing gradient accumulation buffers so a fused backward kernel can add its contribution in place and return `None` for that input ([#196491](https://github.com/pytorch/pytorch/pull/196491))

  When an input has several forward uses, the engine sums the gradient contributions in an internal buffer. `ctx.input_grad_buffers` is a tuple with one entry per `forward` argument: either the current partial-sum buffer for that input, or `None` when no earlier producer has contributed yet or the buffer cannot safely be updated in place. Because availability depends on backward execution order, a backward using it should keep an out-of-place fallback. Buffers are valid only during the current `backward` call and must be updated synchronously. The property is available during eager, first-order `Tensor.backward()`, `torch.autograd.backward()` and `torch.autograd.grad()` calls, and not with `create_graph=True`, anomaly detection, or post-hooks on the producing node.

  ```python
  class Matmul(torch.autograd.Function):
      @staticmethod
      def forward(ctx, x, weight):
          ctx.save_for_backward(x, weight)
          return x @ weight

      @staticmethod
      def backward(ctx, grad_output):
          x, weight = ctx.saved_tensors
          x_buffer, _ = ctx.input_grad_buffers
          if x_buffer is not None:
              x_buffer.addmm_(grad_output, weight.mT)  # accumulate in place
              grad_x = None
          else:
              grad_x = grad_output @ weight.mT
          return grad_x, x.mT @ grad_output
  ```

- Add `torch.autograd.graph.queue_callback(callback)`, a public API to run a callback when the current backward pass finishes, replacing the private `Variable._execution_engine.queue_callback` ([#193958](https://github.com/pytorch/pytorch/pull/193958))

  ```python
  def backward_hook(grad):
      # Runs `update_scales` once, after the whole backward pass has completed
      torch.autograd.graph.queue_callback(update_scales)
      return grad
  ```

### improvements
- Add backward and forward-mode AD support for `torch.special.bessel_j0`, `bessel_j1`, `bessel_y0`, `bessel_y1`, `modified_bessel_i0`, `modified_bessel_i1`, `modified_bessel_k0` and `modified_bessel_k1` ([#189872](https://github.com/pytorch/pytorch/pull/189872))
- Add forward-mode AD support for `torch.nn.functional.grid_sample` ([#195280](https://github.com/pytorch/pytorch/pull/195280))
- Add `torch._functorch.config.activation_memory_budget_require_full_coverage` (default `True`); set it to `False` to let `torch.autograd.graph.region_activation_memory_budget` apply its budget to a whole compiled graph that also contains forward ops outside the context, instead of raising an error ([#195932](https://github.com/pytorch/pytorch/pull/195932))
- `Tensor.grad_dtype` is now readable on non-leaf tensors, returning the gradient dtype recorded on the producing node (e.g. set by `ctx.set_output_grad_dtype` in a custom `torch.autograd.Function`); setting it is still restricted to leaf tensors ([#190852](https://github.com/pytorch/pytorch/pull/190852))
### bug fixes
- Fix `torch.fmin`/`torch.fmax` gradients when one input is NaN: the gradient now goes to the value the forward pass actually selected instead of to both inputs ([#193035](https://github.com/pytorch/pytorch/pull/193035))
- Fix hooks registered on a view after an in-place update of its base being attached to a stale `grad_fn` ([#196514](https://github.com/pytorch/pytorch/pull/196514))
- Fix fast-mode `torch.autograd.gradcheck` comparing against the wrong output when a non-differentiable output comes before a differentiable one ([#194222](https://github.com/pytorch/pytorch/pull/194222))
- Fix `torch.autograd.graph.region_activation_memory_budget` losing its budget in frames that `torch.compile` resumes after a graph break inside the region ([#194808](https://github.com/pytorch/pytorch/pull/194808))
- Fix `gradcheck(fast_mode=True, check_forward_ad=True)` raising `IndexError` instead of reporting which input/output failed ([#194991](https://github.com/pytorch/pytorch/pull/194991))
- Fix a segfault when accessing a saved tensor after a `torch.autograd.graph.saved_tensors_hooks` pack hook raised; it now raises a `RuntimeError` ([#189160](https://github.com/pytorch/pytorch/pull/189160))
### performance
### docs
- Point users to `torch_remat` for region-level selective activation checkpointing in the `torch.utils.checkpoint` documentation ([#193998](https://github.com/pytorch/pytorch/pull/193998))
- Document that the order of `unpack_hook` calls in `torch.autograd.graph.saved_tensors_hooks` is unspecified ([#198016](https://github.com/pytorch/pytorch/pull/198016))
- Fix inline math rendering on the autograd mechanics page ([#192562](https://github.com/pytorch/pytorch/pull/192562))
- Document that gradients passed to the backward of a custom `torch.autograd.Function` or custom op may have arbitrary strides, so kernels must not assume a contiguous layout ([#195210](https://github.com/pytorch/pytorch/pull/195210))
- Remove the stale promise in the `torch.utils.checkpoint` `use_reentrant` warnings and docs that omitting it would raise an error "in version 2.9" ([#193720](https://github.com/pytorch/pytorch/pull/193720))
### devs
### Untopiced
### not user facing
- Replace raw C++ `throw`s in autograd and Python bindings with the standard error-check macros ([#193618](https://github.com/pytorch/pytorch/pull/193618), [#194245](https://github.com/pytorch/pytorch/pull/194245))
- Avoid refcount churn and an oversized vector in generated autograd code ([#194882](https://github.com/pytorch/pytorch/pull/194882), [#195857](https://github.com/pytorch/pytorch/pull/195857))
- Add a private `Tensor._has_grad_dtype_override` property reporting whether `grad_dtype` was set explicitly ([#197504](https://github.com/pytorch/pytorch/pull/197504))
### security
