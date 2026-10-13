
# Release Notes worksheet optim

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

## optim
### bc breaking
### deprecation
- Passing a bare `set` of parameters to an optimizer is deprecated and now emits a `FutureWarning`; it will become an error in a future release ([#198710](https://github.com/pytorch/pytorch/pull/198710))

  Optimizer state is matched to parameters by position, and iteration order over a `set` can change between runs, so `torch.optim.Adam(set(model.parameters()))` could silently mismatch state when it is reloaded. A set inside a param group was already rejected; a bare set was silently accepted. It now warns: `optimizer parameters need to be organized in ordered collections, but the ordering of tensors in sets will change between runs. Please use a list instead. This will be an error in a future release.` Pass a list (or another ordered iterable) instead.

  Version 2.14:
  ```python
  opt = torch.optim.Adam(set(model.parameters()))  # silently accepted
  ```

  Version 2.15:
  ```python
  opt = torch.optim.Adam(set(model.parameters()))  # FutureWarning
  opt = torch.optim.Adam(list(model.parameters()))  # recommended
  ```

### new features
- Add `torch.optim.functional`, a public module with functional optimizer APIs (`adadelta`, `adafactor`, `adagrad`, `adam`, `adamax`, `adamw`, `asgd`, `muon`, `nadam`, `radam`, `rmsprop`, `rprop`, `sgd`, `sparse_adam`) for callers that want to manage parameters, gradients and optimizer state themselves ([#194986](https://github.com/pytorch/pytorch/pull/194986))

  These functions run the same implementations as the optimizer classes and update parameters and state tensors in place; the caller creates, keeps and checkpoints the state. The `torch.optim` docs now include examples, such as keeping AdamW moment buffers in BF16 to save memory.

  ```python
  import torch
  from torch.optim.functional import adamw

  model = torch.nn.Linear(16, 4, device="cuda")
  params = list(model.parameters())
  exp_avgs = [torch.zeros_like(p, dtype=torch.bfloat16) for p in params]
  exp_avg_sqs = [torch.zeros_like(p, dtype=torch.bfloat16) for p in params]
  steps = [torch.zeros((), device=p.device) for p in params]

  with torch.no_grad():
      adamw(
          params=params,
          grads=[p.grad for p in params],
          exp_avgs=exp_avgs,
          exp_avg_sqs=exp_avg_sqs,
          max_exp_avg_sqs=[],
          state_steps=steps,
          fused=True,  # CUDA fused path supports FP32 params with BF16 moments
          amsgrad=False,
          beta1=0.9,
          beta2=0.999,
          lr=1e-3,
          weight_decay=1e-2,
          eps=1e-8,
          maximize=False,
      )
  ```

### improvements
- Validate `lambd` and `alpha` in `torch.optim.ASGD`; negative values now raise `ValueError` at construction instead of causing a `ZeroDivisionError` or a wrong learning-rate schedule during training ([#193303](https://github.com/pytorch/pytorch/pull/193303))
- Run the optimizer graph-capture health check (including the `capturable=True` performance warning) on all accelerators, not only CUDA and XPU ([#194362](https://github.com/pytorch/pytorch/pull/194362))
### bug fixes
- Fix `Muon` normalizing the momentum buffer in place during Newton-Schulz orthogonalization when gradients are already `bfloat16` ([#194664](https://github.com/pytorch/pytorch/pull/194664))
### performance
### docs
### devs
### Untopiced
### not user facing
- Deduplicate the `ADAM_MODE` enum and share one launcher across the fused Adam/AdamW CUDA implementations; the only visible change is that the unsupported-dtype error from the fused `amsgrad=True` kernels now names `fused_adam_amsgrad_kernel_cuda`/`fused_adamw_amsgrad_kernel_cuda` instead of `fused_adam_kernel_cuda`/`fused_adamw_kernel_cuda` ([#190774](https://github.com/pytorch/pytorch/pull/190774))
### security
