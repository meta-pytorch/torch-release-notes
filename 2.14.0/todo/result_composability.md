
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
### improvements
- Add a `length` argument to `torch.scan`, allowing scans without an `xs` input in the same style as `jax.lax.scan`. ([#188349](https://github.com/pytorch/pytorch/pull/188349))
### bug fixes
### performance
- Reduce dynamic-shape tracing overhead by avoiding repeated symbolic-number checks and unnecessary memory-format computation. ([#192677](https://github.com/pytorch/pytorch/pull/192677))
- Bound the cost of applying wide unbacked-symbol substitution maps in `optimization_hint`, reducing synthetic cases with 300 replacements from several seconds to tens of milliseconds. ([#185884](https://github.com/pytorch/pytorch/pull/185884))
### docs
### devs
### Untopiced
- Fix typos in comments, docstrings, and strings across torch ([#187076](https://github.com/pytorch/pytorch/pull/187076))
- Preserve no-op dropout identity in decomposition ([#185335](https://github.com/pytorch/pytorch/pull/185335))
- These are all trivial typo fixes in comments and docstrings. ([#187730](https://github.com/pytorch/pytorch/pull/187730))
- Rename "reference type" to "symbolic type" for custom classes ([#188457](https://github.com/pytorch/pytorch/pull/188457))
- Fix typos in docstrings and comments across torch modules ([#188977](https://github.com/pytorch/pytorch/pull/188977))
- Fix multilabel_margin_loss decomposition for -1 padded targets ([#189552](https://github.com/pytorch/pytorch/pull/189552))
- Fix typos in comments and docstrings across torch ([#190249](https://github.com/pytorch/pytorch/pull/190249))
- fix nansum meta kernel ([#191530](https://github.com/pytorch/pytorch/pull/191530))
### not user facing
- Make constant_pad_nd ref decomposition fully functional ([#185636](https://github.com/pytorch/pytorch/pull/185636))
- Fix torch.istft _refs length handling under dynamic shapes (symbolic clamp/pad) ([#186490](https://github.com/pytorch/pytorch/pull/186490))
- Port _scaled_mm_v2 per-recipe validation from Python meta to C++ ([#185273](https://github.com/pytorch/pytorch/pull/185273))
- Validate aminmax.out dtype in meta paths ([#186227](https://github.com/pytorch/pytorch/pull/186227))
- fix(compile): add celu decomposition with alpha=0 validation ([#179375](https://github.com/pytorch/pytorch/pull/179375))
- fix DDE in native_multi_head_attention_fake ([#187144](https://github.com/pytorch/pytorch/pull/187144))
- Fix DDE in pad_sequence ([#187145](https://github.com/pytorch/pytorch/pull/187145))
- Add CUDA dtype check to native_layer_norm decomposition ([#185693](https://github.com/pytorch/pytorch/pull/185693))
- Fix torch.compile produce wrong output due to problem in decomposition ([#182292](https://github.com/pytorch/pytorch/pull/182292))
- Fix inconsistent stride for max_unpool2d in compiled v eager ([#186602](https://github.com/pytorch/pytorch/pull/186602))
- Add linalg_vector_norm to core decompositions ([#185735](https://github.com/pytorch/pytorch/pull/185735))
- [Decomp] Fix multi_margin_loss to use 1D indexing for weight ([#188770](https://github.com/pytorch/pytorch/pull/188770))
- Make mm out_dtype restriction backend-dependent in meta ([#187096](https://github.com/pytorch/pytorch/pull/187096))
- Preserve CPU memory format in max_unpool2d decomposition ([#187195](https://github.com/pytorch/pytorch/pull/187195))
- [C++ Fake] fake dispatch tables for decomps/op_impl/prim ([#188699](https://github.com/pytorch/pytorch/pull/188699))
- use symint-supported view kernel for meta ([#189447](https://github.com/pytorch/pytorch/pull/189447))
- fix DDE in meta__transformer_encoder_layer_fwd ([#187860](https://github.com/pytorch/pytorch/pull/187860))
- Canonicalize reciprocal(sqrt(x)) to rsqrt(x), Update Batchnorm decomp ([#190206](https://github.com/pytorch/pytorch/pull/190206))
- [ROCm] Fix efficient attention LSE metadata ([#190723](https://github.com/pytorch/pytorch/pull/190723))
- [SDPA] Add memory-efficient GQA and vmap backward support ([#191085](https://github.com/pytorch/pytorch/pull/191085))
- Fix silent fake tensor resize in _make_inplace decompositions ([#191373](https://github.com/pytorch/pytorch/pull/191373))
- Convert _scaled_grouped_mm_v2 to a structured operator ([#187357](https://github.com/pytorch/pytorch/pull/187357))
- Fix max_unpool2d channels-last stride mismatch on XPU ([#190189](https://github.com/pytorch/pytorch/pull/190189))
- BE: Raise NotImplementedError for unsupported bool ops ([#192348](https://github.com/pytorch/pytorch/pull/192348))
- BE: Use NotImplementedError/TypeError for unsupported FFT dtypes ([#192349](https://github.com/pytorch/pytorch/pull/192349))
- Provide a targeted dynamic-shape error message when a data-dependent expression conflicts with a `dynamic_spec` specification. ([#187143](https://github.com/pytorch/pytorch/pull/187143))
- Preserve symbolic tensor and scalar metadata across ProxyTensor and `make_fx` tracing so downstream compilation can consume the traced graphs correctly. ([#187231](https://github.com/pytorch/pytorch/pull/187231))
- Fix symbolic simplification failures that reported `vr must not be None` by preserving loop-local value ranges through recursive simplification. ([#187350](https://github.com/pytorch/pytorch/pull/187350))
- Fix proxy tracing failures for symbolic expressions containing natural powers such as `s1**2`. ([#188278](https://github.com/pytorch/pytorch/pull/188278))
- Use known value ranges to simplify symbolic `Min` and `Max` expressions, avoiding spurious data-dependent guard failures. ([#186248](https://github.com/pytorch/pytorch/pull/186248))
- Fix `torch.cond` branch-output merging raising an internal error for symbolic contiguous strides of the form `stride * max(size, 1)`. ([#189525](https://github.com/pytorch/pytorch/pull/189525))
- Fix repeated tracing or lowering of data-dependent operations raising an assertion when equivalent unbacked symbolic values are rebound. ([#190083](https://github.com/pytorch/pytorch/pull/190083))
- Decompose `detach` by default during post-dispatch `make_fx` tracing, preventing silently incorrect higher-order gradients. Callers that pass an explicit decomposition table retain the previous behavior. ([#186845](https://github.com/pytorch/pytorch/pull/186845))
### security
