
# Release Notes worksheet composability

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

## composability
### bc breaking
- Under functionalization, a regenerated output of `split`, `split_with_sizes` or `unbind` is now rebuilt as a single `slice` or `select` of its base, so its `grad_fn` is `SliceBackward0`/`SelectBackward0` instead of `SplitBackward0`/`SplitWithSizesBackward0`/`UnbindBackward0` ([#194037](https://github.com/pytorch/pytorch/pull/194037))

  This greatly reduces compile time for code that mutates many `split()` views (for example 32s to 15s with 128 views). Gradients are unchanged, but the in-place error now names the new op with output index 0: `RuntimeError: Output 0 of Select is a view and is being modified inplace.` Code that inspects `grad_fn` names, matches the old error text, or pattern-matches `split`/`unbind` nodes in functionalized graphs needs updating. There is no option to restore the previous behavior.

  Version 2.14:
  ```python
  >>> out = torch.func.functionalize(f)(x)  # f returns base.unbind(0)[1] after base.add_(1)
  >>> out.grad_fn
  <UnbindBackward0 object at 0x...>
  ```

  Version 2.15:
  ```python
  >>> out = torch.func.functionalize(f)(x)
  >>> out.grad_fn
  <SelectBackward0 object at 0x...>
  ```
### deprecation
### new features
### improvements
- Add meta implementations for `torch.histogramdd` helper ops, enabling fake-tensor tracing ([#198897](https://github.com/pytorch/pytorch/pull/198897))
- Validate `attn_bias` and key/value shapes in the overrideable fused SDPA fake kernel ([#194271](https://github.com/pytorch/pytorch/pull/194271), [#198303](https://github.com/pytorch/pytorch/pull/198303))
- Raise `NotImplementedError` instead of `RuntimeError` for unsupported dtypes in linalg and norm ops ([#192352](https://github.com/pytorch/pytorch/pull/192352))
- Keep backed dimensions with hint 1 symbolic in `expand` and broadcasting ([#198258](https://github.com/pytorch/pytorch/pull/198258))
### bug fixes
- Fix wrong values and `nan` gradients when compiling `weight_norm` on 1-D parameters ([#198772](https://github.com/pytorch/pytorch/pull/198772))
- Fix compiled `torch.normal(mean, std)` output dtype with mixed float dtypes ([#194557](https://github.com/pytorch/pytorch/pull/194557))
- Fix fake/meta kernels: eager-matching `out=` dtype checks for many ops, symbolic `out=` bitwise shifts, and data-dependent `linalg.cross` ([#192383](https://github.com/pytorch/pytorch/pull/192383), [#193050](https://github.com/pytorch/pytorch/pull/193050), [#193555](https://github.com/pytorch/pytorch/pull/193555), [#194375](https://github.com/pytorch/pytorch/pull/194375), [#195767](https://github.com/pytorch/pytorch/pull/195767))
- Add fused GRU cell meta kernels so CUDA `nn.GRUCell` can be compiled ([#191156](https://github.com/pytorch/pytorch/pull/191156))
- Match eager in decompositions and refs on XPU (`native_layer_norm`), MPS (FFT strides, `logspace`) and MTIA (`masked_fill`) ([#198647](https://github.com/pytorch/pytorch/pull/198647), [#199030](https://github.com/pytorch/pytorch/pull/199030), [#195611](https://github.com/pytorch/pytorch/pull/195611))
- Fix `torch.cond` branch metadata mismatches from `math.trunc(s / 1)` on a `SymInt` ([#186194](https://github.com/pytorch/pytorch/pull/186194))
- Fix `torch.tensor(..., device="meta")` under `FakeTensorMode` not returning a `FakeTensor` ([#186188](https://github.com/pytorch/pytorch/pull/186188))
- Fix spurious `Tensor device mismatch` errors from the FakeTensor dispatch cache ([#197583](https://github.com/pytorch/pytorch/pull/197583))
### performance
- Speed up FakeTensor view cache hits ([#192821](https://github.com/pytorch/pytorch/pull/192821))
### docs
### devs
### Untopiced
### not user facing
- Add a C++ meta kernel for `arange`, skip the Python meta implementation for operators that now have symbolic C++ meta kernels, and preserve fake-tensor metadata through `as_strided` views for the in-progress C++ FakeTensor ([#197581](https://github.com/pytorch/pytorch/pull/197581), [#198888](https://github.com/pytorch/pytorch/pull/198888), [#194744](https://github.com/pytorch/pytorch/pull/194744))
### security
