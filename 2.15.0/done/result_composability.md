
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

  Functionalization (used by `torch.compile`, `torch.func.functionalize` and `torch.export`) records how to rebuild every view after its base is mutated. Previously one output of a multi-output view was rebuilt by replaying the whole operation and indexing the result, so regenerating all N outputs of one base built N*N tensors and left a redundant `split`/`unbind` node in the graph for each regeneration. Each output is now built directly as a `slice` (for `split`/`split_with_sizes`) or `select` (for `unbind`). This greatly reduces compile time for code that mutates many `split()` views (for example 32s to 15s with 128 views), and functionalized graphs now contain one `slice`/`select` per regenerated view instead of a `split`/`unbind` plus `getitem` nodes.

  Gradients are unchanged, and autograd still rejects in-place modification of these outputs. However, a regenerated output (for example one returned from a functionalized function, or an output of a compiled function that aliases an input) now reports the `select`/`slice` node, and the in-place error names that op (`Select`/`Slice`) with output index 0 instead of the original multi-output op and output index: `RuntimeError: Output 0 of Select is a view and is being modified inplace. This view is the output of a function that returns multiple views. Such functions do not allow the output views to be modified inplace.` Code that inspects `grad_fn` names, matches the old error text, or pattern-matches `split`/`unbind` nodes in functionalized graphs needs updating. There is no option to restore the previous behavior.

  Version 2.14:
  ```python
  >>> def f(x):
  ...     base = x.clone()
  ...     out = base.unbind(0)[1]
  ...     base.add_(1)
  ...     return out
  >>> out = torch.func.functionalize(f)(torch.ones(2, 3, requires_grad=True))
  >>> out.grad_fn
  <UnbindBackward0 object at 0x...>
  >>> out.mul_(2)
  RuntimeError: Output 1 of Unbind is a view and is being modified inplace. This view is the output of a function that returns multiple views. ...
  ```

  Version 2.15:
  ```python
  >>> out = torch.func.functionalize(f)(torch.ones(2, 3, requires_grad=True))
  >>> out.grad_fn
  <SelectBackward0 object at 0x...>
  >>> out.mul_(2)
  RuntimeError: Output 0 of Select is a view and is being modified inplace. This view is the output of a function that returns multiple views. ...
  ```
### deprecation
### new features
### improvements
- Add meta implementations for the `histogramdd` helper operators so `torch.histogramdd` can be traced with fake tensors and dynamic shapes, for example under `torch.export` ([#198897](https://github.com/pytorch/pytorch/pull/198897))
- Validate `attn_bias` and key/value sequence-length shapes in the fake/meta kernel of the overrideable fused SDPA backend, surfacing invalid shapes at trace time ([#194271](https://github.com/pytorch/pytorch/pull/194271), [#198303](https://github.com/pytorch/pytorch/pull/198303))
- Raise `NotImplementedError` instead of a plain `RuntimeError` when linear algebra and norm operations (including `torch.norm` and `torch.linalg.vander`) receive integer, Boolean, or unsupported half-precision inputs; existing `except RuntimeError` handlers still catch it ([#192352](https://github.com/pytorch/pytorch/pull/192352))
- Avoid installing guards from size hints in the symbolic fast paths of `expand` and broadcasting, so backed dimensions whose hint is 1 stay symbolic instead of being specialized ([#198258](https://github.com/pytorch/pytorch/pull/198258))
### bug fixes
- Fix silently wrong forward values and `inf`/`nan` gradients when compiling `torch.nn.utils.parametrizations.weight_norm` on a 1-D parameter (such as a bias) with Inductor, and match eager's norm dtype for half-precision inputs ([#198772](https://github.com/pytorch/pytorch/pull/198772))
- Fix compiled `torch.normal(mean, std)` returning the promoted dtype instead of `mean`'s dtype when `mean` and `std` have different floating dtypes ([#194557](https://github.com/pytorch/pytorch/pull/194557))
- Make fake/meta `out=` variants enforce the same output-dtype rules as eager for `torch.all`, `torch.any`, `torch.amax`, `torch.amin`, `torch.conj_physical`, `torch.frexp`, `torch.index_add`, `torch.index_copy`, `torch.index_select`, `torch.nan_to_num`, `torch.tril`, and `torch.triu` ([#192383](https://github.com/pytorch/pytorch/pull/192383), [#193050](https://github.com/pytorch/pytorch/pull/193050), [#193555](https://github.com/pytorch/pytorch/pull/193555))
- Add meta kernels for the fused GRU cell forward and backward operators so CUDA `torch.nn.GRUCell` can be traced with fake tensors and compiled, including inside `scan` ([#191156](https://github.com/pytorch/pytorch/pull/191156))
- Fix symbolic fake-tensor propagation for the `out=` overloads of the bitwise shift operators ([#194375](https://github.com/pytorch/pytorch/pull/194375))
- Fix `GuardOnDataDependentSymNode` errors from the `torch.linalg.cross` meta kernel when the cross dimension is data-dependent ([#195767](https://github.com/pytorch/pytorch/pull/195767))
- Make the `native_layer_norm` decomposition reject mixed weight/bias dtypes on XPU as eager does, matching the existing CUDA check ([#198647](https://github.com/pytorch/pytorch/pull/198647))
- Fix meta output strides for FFT operators on MPS and the `torch.logspace` reference on devices without float64 (such as MPS), so compiled code matches eager ([#199030](https://github.com/pytorch/pytorch/pull/199030))
- Allow a CPU scalar `value` tensor in the `masked_fill` reference on MTIA, matching eager ([#195611](https://github.com/pytorch/pytorch/pull/195611))
- Fix `torch.cond` branch metadata mismatches caused by `math.trunc(s / 1)` on a `SymInt` not simplifying back to `s` ([#186194](https://github.com/pytorch/pytorch/pull/186194))
- Fix `torch.tensor(..., device="meta")` under `FakeTensorMode` returning a plain meta tensor instead of a `FakeTensor` ([#186188](https://github.com/pytorch/pytorch/pull/186188))
- Fix spurious `Tensor device mismatch` errors when the FakeTensor dispatch cache reused a result for an index-less device argument (such as `device="cuda"`) traced under a different current device ([#197583](https://github.com/pytorch/pytorch/pull/197583))
### performance
- Speed up FakeTensor dispatch cache hits for view operations by not computing the symbolic size and stride twice, which reduces compile time with dynamic shapes ([#192821](https://github.com/pytorch/pytorch/pull/192821))
### docs
### devs
### Untopiced
### not user facing
- Add a C++ meta kernel for `arange`, skip the Python meta implementation for operators that now have symbolic C++ meta kernels, and preserve fake-tensor metadata through `as_strided` views for the in-progress C++ FakeTensor ([#197581](https://github.com/pytorch/pytorch/pull/197581), [#198888](https://github.com/pytorch/pytorch/pull/198888), [#194744](https://github.com/pytorch/pytorch/pull/194744))
### security
