
# Release Notes worksheet composability

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.
* Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

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

## composability
### bc breaking
### deprecation
### new features
* Support autograd in torch.cond ([#165908](https://github.com/pytorch/pytorch/pull/165908))
### improvements

- If you are using the `torch.compile(backend="aot_eager")` backend, it should now give bitwise equivalent results in eager. Previously it sometimes would not due to extra compile-only decompositions running ([#165910](https://github.com/pytorch/pytorch/pull/165910))
- Some dynamic shape errors were changed to recommend using `torch._check` over `torch._check_is_size` ([#164889](https://github.com/pytorch/pytorch/pull/164889),
- Some unbacked (dynamic shape) improvements ([#162652](https://github.com/pytorch/pytorch/pull/162652), [#169612](https://github.com/pytorch/pytorch/pull/169612))
- Some bugfixes for symbolic float handling in compile ([#166573](https://github.com/pytorch/pytorch/pull/166573), [#162788](https://github.com/pytorch/pytorch/pull/162788))

*Decompositions, FakeTensor and meta tensors*

Several operator decomps + meta implementations received improvements/bugfixes:
- bugfixes for few decompositions (torch.convolution [#160408](https://github.com/pytorch/pytorch/pull/160408), torch.linalg.eig [#162484](https://github.com/pytorch/pytorch/pull/162484), torch.eye [#163386](https://github.com/pytorch/pytorch/pull/163386), aten.index_select [#168922](https://github.com/pytorch/pytorch/pull/168922), torch._scaled_grouped_mm [#162765](https://github.com/pytorch/pytorch/pull/162765), rms_norm [#165437](https://github.com/pytorch/pytorch/pull/165437))
- new fake / meta implementations for some ops: _native_multi_head_attention ([#163700](https://github.com/pytorch/pytorch/pull/163700)), scaled_mm_v2 ([#167653](https://github.com/pytorch/pytorch/pull/167653)), aten.clone ([#163017](https://github.com/pytorch/pytorch/pull/163017))
- improved unbacked symint (dynamic shape) support for some decompositions ([#161414](https://github.com/pytorch/pytorch/pull/161414), [#167689](https://github.com/pytorch/pytorch/pull/167689), [#164225](https://github.com/pytorch/pytorch/pull/164225), [#165043](https://github.com/pytorch/pytorch/pull/165043), [#164622](https://github.com/pytorch/pytorch/pull/164622), [#164781](https://github.com/pytorch/pytorch/pull/164781), [#162254](https://github.com/pytorch/pytorch/pull/162254), [#162216](https://github.com/pytorch/pytorch/pull/162216), [#163867](https://github.com/pytorch/pytorch/pull/163867))

### bug fixes
### performance
### docs
### devs
- Removed guard_size_oblivious from internal code, replacing most usages with guard_if_{false|true}. Both APIs are used in framework code that gets traced through to make it more friendly to unbacked symints, but the new APIs are more intuitive ([#164664](https://github.com/pytorch/pytorch/pull/164664), [#164665](https://github.com/pytorch/pytorch/pull/164665), [#167232](https://github.com/pytorch/pytorch/pull/167232))
### Untopiced
### not user facing
- [4/N] Apply ruff UP035 rule to python code ([#164206](https://github.com/pytorch/pytorch/pull/164206))
- [5/N] Apply ruff UP035 rule ([#164423](https://github.com/pytorch/pytorch/pull/164423))
- Add pyrefly suppressions (3/n) ([#164588](https://github.com/pytorch/pytorch/pull/164588))
- Pyrefly suppressions 4/n ([#164615](https://github.com/pytorch/pytorch/pull/164615))
- Add pyrefly suppressions ([#164748](https://github.com/pytorch/pytorch/pull/164748))
- Pyrefly suppressions 6/n ([#164877](https://github.com/pytorch/pytorch/pull/164877))
- Fix flake8 B028 warnings ([#166224](https://github.com/pytorch/pytorch/pull/166224))
- Fix pyrefly ignore syntax ([#166438](https://github.com/pytorch/pytorch/pull/166438))
- Fix pyrefly error syntax (2/n) ([#166448](https://github.com/pytorch/pytorch/pull/166448))
- [3/N] Use key in dict for existence checks ([#167214](https://github.com/pytorch/pytorch/pull/167214))
- remove gso from collapse_view_helper ([#162212](https://github.com/pytorch/pytorch/pull/162212))
- are_strides_like_channels_last_or_false ([#162354](https://github.com/pytorch/pytorch/pull/162354))
- [cuDNN][SDPA][submodule] Roll-back cuDNN frontend upgrade, update Meta registration ([#163104](https://github.com/pytorch/pytorch/pull/163104))
- Remove export of slice_in_dim ([#164117](https://github.com/pytorch/pytorch/pull/164117))
- Fix cdist export compute mode validation ([#161724](https://github.com/pytorch/pytorch/pull/161724))
- Add paths to exclude shape guards ([#162684](https://github.com/pytorch/pytorch/pull/162684))
- Fix phantom symbol for derived dims ([#162416](https://github.com/pytorch/pytorch/pull/162416))
- Adjust mark_unbacked logs. ([#164131](https://github.com/pytorch/pytorch/pull/164131))
- ProxyTorchDispatchMode: Decomposing missing sympy.SymExpr should handle constant literals ([#167585](https://github.com/pytorch/pytorch/pull/167585))
- Make unbacked_sym[int/float]_counter integers ([#163920](https://github.com/pytorch/pytorch/pull/163920))
- remove allocation of new unbacked symbols during mod eval ([#167123](https://github.com/pytorch/pytorch/pull/167123))
- Teach ProxyTorchDispatchMode how to decompose sympy.Expr into known inputs ([#164717](https://github.com/pytorch/pytorch/pull/164717))
- [hoo] Fix unlift of effects with invoke_subgraph ([#167363](https://github.com/pytorch/pytorch/pull/167363))
- [Fix] Adding missing `f` prefixes to formatted strings [1/N] ([#164065](https://github.com/pytorch/pytorch/pull/164065))
- [BE][Easy]: Add prims common TypeGuard ([#164263](https://github.com/pytorch/pytorch/pull/164263))
- Fix typo in torch._refs ([#167310](https://github.com/pytorch/pytorch/pull/167310))
- [16/N]Use Python 3.10 typing ([#169917](https://github.com/pytorch/pytorch/pull/169917))
- [symbolic shapes] remove maybe_guard_rel warning ([#166553](https://github.com/pytorch/pytorch/pull/166553))
- Don't register wrong overload to prim decomp ([#163138](https://github.com/pytorch/pytorch/pull/163138))
### security
