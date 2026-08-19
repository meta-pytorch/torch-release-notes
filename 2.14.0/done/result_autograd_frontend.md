
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
- Training-mode batch normalization now raises an error when a third-order derivative is requested ([#186779](https://github.com/pytorch/pytorch/pull/186779))

  Second-order derivatives remain supported. Previously, differentiating a training-mode batch-normalization backward pass again silently treated the saved batch statistics as constants and returned an invalid third-order derivative. In PyTorch 2.14, this case raises `RuntimeError: batch_norm does not support 3rd+ order derivatives.` Evaluation-mode batch normalization is unchanged. There is no equivalent workaround that preserves correct training-mode third derivatives; avoid requesting them, use evaluation mode when its running-statistics semantics are appropriate, or provide a custom differentiable implementation.

  Version 2.13:
  ```python
  import torch
  import torch.nn.functional as F

  x = torch.randn(8, 3, requires_grad=True)
  y = F.batch_norm(x, None, None, training=True)
  (grad1,) = torch.autograd.grad(y.sum(), x, create_graph=True)
  (grad2,) = torch.autograd.grad(grad1.sum(), x, create_graph=True)
  (grad3,) = torch.autograd.grad(grad2.sum(), x)
  # Returns a tensor, but the result is not a valid third-order derivative.
  ```

  Version 2.14:
  ```python
  import torch
  import torch.nn.functional as F

  x = torch.randn(8, 3, requires_grad=True)
  y = F.batch_norm(x, None, None, training=True)
  (grad1,) = torch.autograd.grad(y.sum(), x, create_graph=True)
  (grad2,) = torch.autograd.grad(grad1.sum(), x, create_graph=True)
  torch.autograd.grad(grad2.sum(), x)
  # RuntimeError: batch_norm does not support 3rd+ order derivatives.
  ```

- Clamp and min/max boundary subgradients now follow the selected dispatcher schema's input space ([#191142](https://github.com/pytorch/pytorch/pull/191142))

  This affects gradients exactly at nondifferentiable bounds or ties. A scalar clamp bound is a fixed parameter, so the input gradient at equality changes from `1` to the minimum-norm subgradient `0`. A Tensor bound is part of the differentiable input space, so `clamp`, `clamp_min`, and `clamp_max` now split the gradient evenly between the input and bound at an ordinary tie instead of assigning it entirely to the input. `fmin` and `fmax` use the same even tie split, and forward-mode AD for the min/max family is aligned with these rules. Code that intentionally depends on the old tie-breaking behavior can express it explicitly with `torch.where`, such as `torch.where(value >= bound, value, bound)`.

  Version 2.13:
  ```python
  import torch

  x = torch.tensor(0.0, requires_grad=True)
  torch.clamp_min(x, 0.0).backward()
  print(x.grad)  # tensor(1.)

  value = torch.tensor(0.0, requires_grad=True)
  bound = torch.tensor(0.0, requires_grad=True)
  torch.clamp_min(value, bound).backward()
  print(value.grad, bound.grad)  # tensor(1.) tensor(0.)
  ```

  Version 2.14:
  ```python
  import torch

  x = torch.tensor(0.0, requires_grad=True)
  torch.clamp_min(x, 0.0).backward()
  print(x.grad)  # tensor(0.)

  value = torch.tensor(0.0, requires_grad=True)
  bound = torch.tensor(0.0, requires_grad=True)
  torch.clamp_min(value, bound).backward()
  print(value.grad, bound.grad)  # tensor(0.5000) tensor(0.5000)
  ```

### deprecation
### new features
- Add `torch.autograd.graph.node_creation_hook`, a thread-local context manager whose callback receives every fully populated autograd graph node created within its scope. The callback can inspect nodes, store metadata, or register backward pre-hooks and post-hooks, including for nodes created during higher-order differentiation and checkpoint recomputation ([#189284](https://github.com/pytorch/pytorch/pull/189284))
- Add `ctx.set_output_grad_dtype(*dtypes)` for custom `torch.autograd.Function` implementations. Called once from `forward` or `setup_context`, it declares the gradient dtype expected for each output independently of the output's storage dtype; a concrete dtype converts incoming gradients, while `None` leaves their dtype unchanged ([#189634](https://github.com/pytorch/pytorch/pull/189634))
- Add second-order gradient support for `torch.cdist` and `torch.nn.functional.pdist`, so grad-grad computations no longer fail because `_cdist_backward` or `_pdist_backward` lacks a derivative ([#188901](https://github.com/pytorch/pytorch/pull/188901))
### improvements
### bug fixes
- Fix `torch.pow` backward when the base is a Boolean scalar by promoting the scalar before computing its logarithm, avoiding an internal assertion failure ([#182564](https://github.com/pytorch/pytorch/pull/182564))
- Fix `torch.pow` backward under `torch.compile(dynamic=True)` when a Python integer exponent becomes symbolic, avoiding the `NYI SymInt equality` crash without specializing on the exponent ([#185851](https://github.com/pytorch/pytorch/pull/185851))
- Make `native_group_norm` and `native_group_norm_backward` safely handle non-contiguous tensors, fixing `vmap` failures and possible out-of-bounds memory accesses ([#186414](https://github.com/pytorch/pytorch/pull/186414))
- Fix the `torch.ldexp` gradient for negative integer exponents so it returns `2.0 ** exponent` instead of zero ([#186566](https://github.com/pytorch/pytorch/pull/186566))
- Fix `DeviceContext` mode leaks during checkpoint recomputation and default-device restoration ([#189286](https://github.com/pytorch/pytorch/pull/189286))
- Fix end-of-backward leaf-stream synchronization across CUDA graph capture boundaries, avoiding opaque `cudaErrorStreamCaptureIsolation` failures and providing an actionable error when the crossing cannot be safely skipped ([#189591](https://github.com/pytorch/pytorch/pull/189591))
- Fix precision errors in the CUDA `native_group_norm_backward` kernel and its decomposition by applying the missing upcasts ([#190245](https://github.com/pytorch/pytorch/pull/190245))
- Stop `register_full_backward_pre_hook`-only modules from emitting a warning intended for `register_full_backward_hook` when their forward inputs do not require gradients ([#190685](https://github.com/pytorch/pytorch/pull/190685))
- Fix max-pooling double backward under `vmap` for channels-last inputs, which previously raised `NYI: querying is_contiguous inside of vmap` ([#191678](https://github.com/pytorch/pytorch/pull/191678))
- Preserve dynamic type names and argument indices in custom `torch.autograd.Function` validation error messages ([#191748](https://github.com/pytorch/pytorch/pull/191748))
- Improve `log2` and `log10` backward accuracy by using named mathematical constants, including a correctly rounded double-precision `log(10)` constant ([#192613](https://github.com/pytorch/pytorch/pull/192613))
### performance
- Reduce `torch.autograd.Function.apply` overhead by avoiding unused profiler input copies, borrowed-input `Tensor` refcount churn, and output copies. The profiler change alone saves approximately 0.3–0.4 microseconds in the reported custom-function benchmark ([#189582](https://github.com/pytorch/pytorch/pull/189582), [#189788](https://github.com/pytorch/pytorch/pull/189788), [#189800](https://github.com/pytorch/pytorch/pull/189800))
- Enable the compiler to constant-fold more floating-point constants in generated backward formulas, reducing runtime computation while keeping the simplified constants within one ULP of the originals ([#192611](https://github.com/pytorch/pytorch/pull/192611))
### docs
### devs
### not user facing
- Expose the private `_wrapped_node` property on `CopySlices` for internal autograd graph tooling ([#190806](https://github.com/pytorch/pytorch/pull/190806))
- Release unexpected objects returned from custom `torch.autograd.Function.setup_context` instead of leaking the underlying Python reference ([#191966](https://github.com/pytorch/pytorch/pull/191966))
### security
