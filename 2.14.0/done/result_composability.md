
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
### deprecation
### new features
- Add a `length` argument to `torch.scan`, allowing a scan to run for a fixed number of steps when `xs=None`, matching the corresponding `jax.lax.scan` usage pattern ([#188349](https://github.com/pytorch/pytorch/pull/188349))
- Add grouped-query attention to the CUDA memory-efficient backend for `torch.nn.functional.scaled_dot_product_attention`, including native grouped key/value heads, implicit multi-query attention broadcasting, and backward support under `vmap` ([#191085](https://github.com/pytorch/pytorch/pull/191085))
### improvements
- Add `torch.linalg.vector_norm` to the core ATen decomposition table used by `ExportedProgram.run_decompositions()`, including correct `dim=()` handling ([#185735](https://github.com/pytorch/pytorch/pull/185735))
- Allow out-of-tree backends to define additional `out_dtype` combinations for `torch.mm`, `torch.bmm`, and `torch.baddbmm` under fake/meta tracing; CUDA and XPU restrictions remain unchanged ([#187096](https://github.com/pytorch/pytorch/pull/187096))
- Provide a targeted dynamic-shape error when a data-dependent expression conflicts with a `dynamic_spec` constraint ([#187143](https://github.com/pytorch/pytorch/pull/187143))
### bug fixes
- Raise `NotImplementedError` for unsupported Boolean operations and distinguish unsupported FFT dtypes from invalid real/complex domains with `NotImplementedError` and `TypeError` ([#192348](https://github.com/pytorch/pytorch/pull/192348), [#192349](https://github.com/pytorch/pytorch/pull/192349))
- Preserve eager identity semantics for no-op dropout decompositions, preventing `torch.compile` and `torch.export` from replacing a `Parameter` with a cloned fake tensor when dropout is disabled ([#185335](https://github.com/pytorch/pytorch/pull/185335))
- Fix compiled `torch.nn.functional.multilabel_margin_loss` values and gradients when targets use `-1` padding ([#189552](https://github.com/pytorch/pytorch/pull/189552))
- Fix `torch.nansum` meta output shapes when `dim=()` should reduce all dimensions ([#191530](https://github.com/pytorch/pytorch/pull/191530))
- Make the `constant_pad_nd` reference decomposition fully functional so `torch.onnx.export(dynamo=True)` no longer fails functionalization for models using `torch.nn.functional.pad` ([#185636](https://github.com/pytorch/pytorch/pull/185636))
- Keep `torch.istft` length clamping and padding symbolic under dynamic shapes, avoiding recompilation and data-dependent guard failures when the requested length crosses the signal length ([#186490](https://github.com/pytorch/pytorch/pull/186490))
- Make compiled and fake/meta `torch.aminmax(..., out=...)` enforce the same exact output-dtype requirements as eager execution ([#186227](https://github.com/pytorch/pytorch/pull/186227))
- Make compiled `torch.nn.functional.celu` reject `alpha=0` with the same error as eager execution ([#179375](https://github.com/pytorch/pytorch/pull/179375))
- Avoid data-dependent guard failures in fake/meta tracing of native multi-head attention with unbacked symbolic sizes ([#187144](https://github.com/pytorch/pytorch/pull/187144))
- Avoid data-dependent guards in `torch.nn.utils.rnn.pad_sequence` decompositions when sequence lengths are symbolic ([#187145](https://github.com/pytorch/pytorch/pull/187145))
- Make the CUDA `native_layer_norm` decomposition reject mixed affine-parameter dtypes in the same cases as eager execution ([#185693](https://github.com/pytorch/pytorch/pull/185693))
- Fix incorrect compiled output and gradients for overlapping-input `torch.diagonal_scatter` operations ([#182292](https://github.com/pytorch/pytorch/pull/182292))
- Match compiled `max_unpool2d` output strides and channels-last memory format to eager CPU execution ([#186602](https://github.com/pytorch/pytorch/pull/186602), [#187195](https://github.com/pytorch/pytorch/pull/187195))
- Route meta `view` operations through the symbolic-shape-aware kernel, avoiding `SymIntArrayRef expected to contain only concrete integers` failures ([#189447](https://github.com/pytorch/pytorch/pull/189447))
- Avoid data-dependent guard failures in the transformer encoder layer meta kernel when the input size is an unbacked symbol ([#187860](https://github.com/pytorch/pytorch/pull/187860))
- Prevent fake/meta decompositions of in-place operations from silently resizing their destination when operands cannot broadcast to its shape; compiled execution now raises the same shape error as eager execution ([#191373](https://github.com/pytorch/pytorch/pull/191373))
- Preserve symbolic tensor, scalar, and unbacked-binding metadata across ProxyTensor and `make_fx` tracing ([#187231](https://github.com/pytorch/pytorch/pull/187231))
- Preserve loop-local value ranges and use known ranges when simplifying symbolic `Min` and `Max` expressions, avoiding `vr must not be None` and spurious data-dependent guard failures ([#187350](https://github.com/pytorch/pytorch/pull/187350), [#186248](https://github.com/pytorch/pytorch/pull/186248))
- Fix symbolic proxy tracing and repeated lowering edge cases involving natural powers, `torch.cond` contiguous-stride expressions, and equivalent rebound unbacked symbols ([#188278](https://github.com/pytorch/pytorch/pull/188278), [#189525](https://github.com/pytorch/pytorch/pull/189525), [#190083](https://github.com/pytorch/pytorch/pull/190083))
- Fix silently incorrect second-order gradients from post-dispatch `make_fx` tracing by decomposing `detach` by default; callers that provide an explicit decomposition table retain the previous behavior ([#186845](https://github.com/pytorch/pytorch/pull/186845))
### performance
- Reduce dynamic-shape tracing overhead by avoiding repeated symbolic-number checks and unnecessary memory-format computation, cutting reported AOTAutograd joint-tracing time by approximately 4–5% on a dynamic-shape model ([#192677](https://github.com/pytorch/pytorch/pull/192677))
- Bound the cost of applying wide unbacked-symbol substitution maps in `optimization_hint`, reducing a synthetic case with 300 replacements from 7.36 seconds to 22 milliseconds ([#185884](https://github.com/pytorch/pytorch/pull/185884))
- Canonicalize `reciprocal(sqrt(x))` to `rsqrt(x)` and update the BatchNorm inference decomposition, improving affected kernels by 85–94% and reported model end-to-end performance by 2.11 percentage points ([#190206](https://github.com/pytorch/pytorch/pull/190206))
### docs
### devs
### not user facing
- Add hinted symbolic storage-size metadata to internal `FakeTensor` trace serialization without changing runtime shape semantics ([#183839](https://github.com/pytorch/pytorch/pull/183839))
- Rename private custom-class bases, registration helpers, type names, and predicates while retaining deprecated compatibility aliases ([#188455](https://github.com/pytorch/pytorch/pull/188455), [#188456](https://github.com/pytorch/pytorch/pull/188456), [#188458](https://github.com/pytorch/pytorch/pull/188458), [#188461](https://github.com/pytorch/pytorch/pull/188461))
- Fix spelling and grammar in comments, docstrings, and user-facing strings across PyTorch without changing behavior ([#187076](https://github.com/pytorch/pytorch/pull/187076), [#187730](https://github.com/pytorch/pytorch/pull/187730), [#188977](https://github.com/pytorch/pytorch/pull/188977), [#190249](https://github.com/pytorch/pytorch/pull/190249))
- Rename the private opaque-custom-class type value from `reference` to `symbolic`, while continuing to accept the old value with a warning ([#188457](https://github.com/pytorch/pytorch/pull/188457))
- Centralize private `_scaled_mm_v2` recipe validation in C++ while preserving symbolic shape inference in the Python meta path ([#185273](https://github.com/pytorch/pytorch/pull/185273))
- Add C++ FakeTensor dispatch tables for decompositions, operator implementations, and primitives ([#188699](https://github.com/pytorch/pytorch/pull/188699))
- Convert private `_scaled_grouped_mm_v2` to a structured operator and centralize its validation ([#187357](https://github.com/pytorch/pytorch/pull/187357))
### security
