
# Release Notes worksheet distributed (fsdp2)

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

## distributed (fsdp2)
### bc breaking
- With `MixedPrecisionPolicy(reduce_dtype=None)`, `fully_shard` now accumulates and reduces gradients in the parameter's `grad_dtype` (its original dtype by default) instead of in `param_dtype` ([#194434](https://github.com/pytorch/pytorch/pull/194434))

  Before, `reduce_dtype=None` meant "reduce in `param_dtype`", and FSDP2 ignored any `grad_dtype` set on the parameters. Now `reduce_dtype=None` follows each parameter's `grad_dtype`, as configured before lazy initialization (the first forward or `FSDPModule.unshard()`). If `grad_dtype` is unset, the parameter's original dtype is used. If it is explicitly `None`, any incoming gradient dtype is accepted. This decision no longer depends on `param_dtype`. In the common setup of fp32 parameters with `param_dtype=torch.bfloat16`, gradients now accumulate and reduce-scatter in fp32 instead of bf16. That is more accurate but sends twice as many bytes per reduce-scatter. In the rare reverse setup (bf16 parameters with `param_dtype=torch.float32`), gradients now reduce in bf16 instead of fp32. `replicate()` behaves the same way because it uses the same `MixedPrecisionPolicy`. FSDP1 still reduces in `param_dtype`. To keep the old behavior, set `reduce_dtype` explicitly.

  This PR also changes gradient accumulation without reduction (`set_requires_gradient_sync(False)`): the unsharded parameter's `.grad` now always holds the accumulated gradient. Before, it was `None` when `reduce_dtype` differed from `param_dtype`, because FSDP kept the sum in a hidden buffer.

  Version 2.14:
  ```python
  # fp32 parameters
  mp_policy = MixedPrecisionPolicy(param_dtype=torch.bfloat16)
  fully_shard(model, mp_policy=mp_policy)
  # gradients accumulate and reduce-scatter in bf16
  ```

  Version 2.15:
  ```python
  # fp32 parameters
  mp_policy = MixedPrecisionPolicy(param_dtype=torch.bfloat16)
  fully_shard(model, mp_policy=mp_policy)
  # gradients accumulate and reduce-scatter in fp32

  # to keep the 2.14 behavior, set reduce_dtype explicitly
  mp_policy = MixedPrecisionPolicy(param_dtype=torch.bfloat16, reduce_dtype=torch.bfloat16)
  fully_shard(model, mp_policy=mp_policy)
  ```
### deprecation
### new features
### improvements
### bug fixes
- Fix `RuntimeError: Inference tensors do not track version counter` when unsharding FSDP2 modules under `torch.inference_mode()` ([#197327](https://github.com/pytorch/pytorch/pull/197327))
### performance
- Avoid an extra full-size gradient allocation in reduce-scatter when the shard group has size 1 (e.g. HSDP with a sharding degree of 1). This allocation could cause out-of-memory errors ([#196348](https://github.com/pytorch/pytorch/pull/196348))
- Upcast low-precision gradients during the reduce-scatter copy-in instead of once per parameter in autograd. This avoids extra cast kernels and higher-precision gradient memory when gradients reduce in a higher precision than the compute dtype ([#198668](https://github.com/pytorch/pytorch/pull/198668))
### docs
### devs
### Untopiced
### not user facing
- Extract all-gather and reduce-scatter copy preparation into helpers ([#197372](https://github.com/pytorch/pytorch/pull/197372))
### security
