
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

  **This is BC-breaking**: `mp_policy.reduce_dtype=None` no longer defaults to `mp_policy.param_dtype`.
  * [popular case] fp32 params, `MixedPrecisionPolicy(param_dtype=bf16)`
    * before: grad accumulation and reduce happen in bf16
    * after: grad accumulation and reduce happen in fp32 (2x reduce-scatter bytes)
  * [rare case] bf16 params, `MixedPrecisionPolicy(param_dtype=fp32)`
    * before: grad accumulation and reduce happen in fp32
    * after: grad accumulation and reduce happen in bf16

  How to deal with BC: explicitly set `mp_policy.reduce_dtype`.

  In grad accumulation (no reduce-scatter), the unsharded param's `.grad` always holds the accumulated value, visible via `model.parameters()` while unsharded. Before this change, `.grad` was `None` when `reduce_dtype` was set and differed from `param_dtype` (FSDP kept the sum in a hidden `reduce_dtype` buffer).

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
- Fix FSDP2 unshard under `torch.inference_mode()` ([#197327](https://github.com/pytorch/pytorch/pull/197327))
### performance
- Reduce reduce-scatter gradient memory for size-1 shard groups and low-precision gradients ([#196348](https://github.com/pytorch/pytorch/pull/196348), [#198668](https://github.com/pytorch/pytorch/pull/198668))
### docs
### devs
### Untopiced
### not user facing
- Extract all-gather and reduce-scatter copy preparation into helpers ([#197372](https://github.com/pytorch/pytorch/pull/197372))
### security
