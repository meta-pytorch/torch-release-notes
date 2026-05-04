
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
### bug fixes
### performance
### docs
### devs
### Untopiced
- Delete `size_vars` `size_hint` API ([#175365](https://github.com/pytorch/pytorch/pull/175365)) _(from fx worksheet)_
- Add partition merging for regions connected by data dependencies in regional inductor ([#178690](https://github.com/pytorch/pytorch/pull/178690)) _(from fx worksheet)_
- Revert to CapabilityBasedPartitioner with per-region partitioning in regional inductor ([#179209](https://github.com/pytorch/pytorch/pull/179209)) _(from fx worksheet)_
- Use FloorDiv and Mod instead of // and % on sympy exprs ([#177051](https://github.com/pytorch/pytorch/pull/177051)) _(from fx worksheet)_
- Reduce threshold for calling `sympy.factor` to 50, avoiding expensive symbolic simplification on large expressions ([#177779](https://github.com/pytorch/pytorch/pull/177779)) _(from fx worksheet)_
- Improve tracing speed via the `aggressive_guard_free_semantics` config flag ([#174654](https://github.com/pytorch/pytorch/pull/174654)) _(from fx worksheet)_
- Add `DynamicInt` `__pow__` and `__rpow__` methods ([#179868](https://github.com/pytorch/pytorch/pull/179868)) _(from fx worksheet)_
- Fix `_build_proxy_for_sym_expr` for n-ary `sympy.Add` by mapping to `torch.sym_sum` ([#175398](https://github.com/pytorch/pytorch/pull/175398)) _(from fx worksheet)_
- Fix `SYMPY_INTERP` calling convention for `IsNonOverlappingAndDenseIndicator` ([#179031](https://github.com/pytorch/pytorch/pull/179031)) _(from fx worksheet)_
- Fix wrong bool to int conversion ([#177178](https://github.com/pytorch/pytorch/pull/177178)) _(from fx worksheet)_
- Add per-SymNode expression cache keyed on `_replacements_version_counter`, reducing redundant symbolic computation ([#175353](https://github.com/pytorch/pytorch/pull/175353)) _(from fx worksheet)_
- Decompose `mm`/`addmm` to pointwise multiply when K==1, yielding up to 1.55x speedup for outer-product-like matrix multiplications ([#175825](https://github.com/pytorch/pytorch/pull/175825)) _(from fx worksheet)_
- Preserve scalar item() semantics for size-1 tensors ([#177270](https://github.com/pytorch/pytorch/pull/177270)) _(from fx worksheet)_
- Handle div by 0 in optimization hint when fallback is 0 ([#177709](https://github.com/pytorch/pytorch/pull/177709)) _(from fx worksheet)_
- Tag backward nodes via `_patch_autograd_grad` and update remat pass ([#179105](https://github.com/pytorch/pytorch/pull/179105)) _(from fx worksheet)_
- Support `fast_bind` used in `normalize_function` for FakeTensor ([#175740](https://github.com/pytorch/pytorch/pull/175740)) _(from fx worksheet)_
- Fix stride handling in FFT meta registrations ([#175731](https://github.com/pytorch/pytorch/pull/175731))
- Fix exception messages displaying as tuples instead of formatted strings ([#175957](https://github.com/pytorch/pytorch/pull/175957))
- [Bugfix] Fix onehot runtime error ([#177160](https://github.com/pytorch/pytorch/pull/177160))
- Add scaled_mm_v2 cpu implementation ([#176266](https://github.com/pytorch/pytorch/pull/176266))
### not user facing
- Fix clamp(None, nan) to propagate scalar NaNs ([#172200](https://github.com/pytorch/pytorch/pull/172200))
- Fix DDE in meta_copy ([#175582](https://github.com/pytorch/pytorch/pull/175582))
- [meta_registrations] Add bmm out variant support ([#175619](https://github.com/pytorch/pytorch/pull/175619))
- index_select decomposition preserve memory format ([#175638](https://github.com/pytorch/pytorch/pull/175638))
- Use TORCH_SYM_CHECK in nll_loss_nd_symint for symbolic size comparison to avoid DDE  ([#175956](https://github.com/pytorch/pytorch/pull/175956))
- [MXFP4] Fix E8M0 blockwise scale size validation for packed FP4 in _scaled_mm ([#176357](https://github.com/pytorch/pytorch/pull/176357))
- [Bugfix] Fix nll bug via decomposition handling ([#177189](https://github.com/pytorch/pytorch/pull/177189))
- Fix staged CUDA FFT meta strides ([#177323](https://github.com/pytorch/pytorch/pull/177323))
- Fix export for unary torch.where ([#177493](https://github.com/pytorch/pytorch/pull/177493))
- [BE][Ez]: Fused some empty as_strided calls ([#177545](https://github.com/pytorch/pytorch/pull/177545))
- Fix scalar-only add/sub alpha out refs in torch.compile ([#177677](https://github.com/pytorch/pytorch/pull/177677))
- Inductor Decomposition-Fix Return Value Type Mismatch On binary_cross_entropy_with_logits ([#176844](https://github.com/pytorch/pytorch/pull/176844))
- [Bugfix] Fix meta conv backwards strides ([#177175](https://github.com/pytorch/pytorch/pull/177175))
- Support half precision FFT on XPU backend ([#171231](https://github.com/pytorch/pytorch/pull/171231))
- [PyTorch] Add meta kernel for _scaled_dot_product_fused_attention_overrideable_backward (#178494) ([#178494](https://github.com/pytorch/pytorch/pull/178494))
- decomp:add decomposition for aten.hann_window ([#177946](https://github.com/pytorch/pytorch/pull/177946))
- [easy] fix rng decomposition typo ([#174308](https://github.com/pytorch/pytorch/pull/174308))
- Fix _make_dep_token meta to return 0-dim tensor ([#179354](https://github.com/pytorch/pytorch/pull/179354))
- Fix rrelu_with_noise_backward decomposition to match C++ ([#179355](https://github.com/pytorch/pytorch/pull/179355))
- Dynamo bug fix: Missing meta kernel for aten::quantize_per_tensor.tensor_qparams ([#169697](https://github.com/pytorch/pytorch/pull/169697))
- fix: aten.quantize_per_tensor isn't a MKLDNN-specific operator ([#180218](https://github.com/pytorch/pytorch/pull/180218))
- Fix slice_scatter meta overlap handling ([#180166](https://github.com/pytorch/pytorch/pull/180166))
### security
