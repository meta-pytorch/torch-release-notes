
# Release Notes worksheet nn_frontend

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

## nn_frontend
### bc breaking
- Remove `is_causal` flag from `varlen_attn` ([#172245](https://github.com/pytorch/pytorch/pull/172245))

The `is_causal` parameter has been removed from `torch.nn.attention.varlen_attn`. Causal attention is now expressed through the `window_size` parameter: use `window_size=(-1, 0)` for causal masking, or `window_size=(W, 0)` for causal attention with a sliding window of size `W`. The default `window_size=(-1, -1)` corresponds to full (non-causal) attention.

```python
# Before (2.10)
output = varlen_attn(query, key, value, cu_seq_q, cu_seq_k, max_q, max_k, is_causal=True)

# After (2.11) — use window_size instead
output = varlen_attn(query, key, value, cu_seq_q, cu_seq_k, max_q, max_k, window_size=(-1, 0))
```

- Add `sliding_window` support to `varlen_attn`, making optional arguments keyword-only ([#172238](https://github.com/pytorch/pytorch/pull/172238))

The signature of `torch.nn.attention.varlen_attn` has changed: a `*` (keyword-only separator) has been inserted before the optional arguments. Previously, optional arguments like `is_causal`, `return_aux`, and `scale` could be passed positionally; they must now be passed as keyword arguments. A new `window_size` keyword argument has also been added.

```python
# Before (2.10)
output = varlen_attn(query, key, value, cu_seq_q, cu_seq_k, max_q, max_k, True, None, 1.0)

# After (2.11) — pass as keyword argument
output = varlen_attn(query, key, value, cu_seq_q, cu_seq_k, max_q, max_k, is_causal=True, return_aux=None, scale=1.0)
```


### deprecation
### new features
- Add mechanism to restore default flash attn impl after `activate_flash_attention_impl` ([#169866](https://github.com/pytorch/pytorch/pull/169866))
- Add `scale` for softmax to varlen attn ([#171199](https://github.com/pytorch/pytorch/pull/171199))
### improvements
- Add `remove_duplicate` parameter to `nn.Module.modules()` function ([#174383](https://github.com/pytorch/pytorch/pull/174383))
### bug fixes
- Fix Illegal Memory Access in FlashAttention 2 by syncing with upstream ([#174114](https://github.com/pytorch/pytorch/pull/174114))
- Propagate `max_q` and `max_k` for `varlen_attn` ([#173681](https://github.com/pytorch/pytorch/pull/173681))


### performance
### docs

### devs
### Untopiced


### not user facing
### security
