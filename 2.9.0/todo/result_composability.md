
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
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [export] set enable_gqa in export flash->math decomp ([#158604](https://github.com/pytorch/pytorch/pull/158604))
- [ROCm] Add FP8 rowwise support to _scaled_grouped_mm + Submodule update ([#159075](https://github.com/pytorch/pytorch/pull/159075))
- Get tensor subclasses and torch.library.triton_op to dispatch correctly ([#160341](https://github.com/pytorch/pytorch/pull/160341))
- Add dtype checks in meta dispatch for various ordering ops ([#159556](https://github.com/pytorch/pytorch/pull/159556))
- [dynamic shapes] prims_common non_overlapping_and_dense ([#160462](https://github.com/pytorch/pytorch/pull/160462))
- Fix meta function for aten.complex ([#160894](https://github.com/pytorch/pytorch/pull/160894))
### not user facing
- remove guard_size_oblivious from unbind. ([#148815](https://github.com/pytorch/pytorch/pull/148815))
- address remaining straight forward gso in meta_registrations ([#156902](https://github.com/pytorch/pytorch/pull/156902))
- _broadcast_shapes gso generalizations ([#157008](https://github.com/pytorch/pytorch/pull/157008))
- Update test after CUTLASS upgrade ([#157903](https://github.com/pytorch/pytorch/pull/157903))
- [CPU] Support GQA for flash attention ([#157893](https://github.com/pytorch/pytorch/pull/157893))
- move view_meta to fake impl ([#158406](https://github.com/pytorch/pytorch/pull/158406))
- (is_non_overlapping_and_dense) gso to guard_or_false in when checking length 1 ([#158894](https://github.com/pytorch/pytorch/pull/158894))
- (should_fold) gso to guard_or_false when checking folding whether to 3d bmm into 2d mm ([#159184](https://github.com/pytorch/pytorch/pull/159184))
- improve shape checks for grouped_mm ([#159666](https://github.com/pytorch/pytorch/pull/159666))
- Add meta kernel for sdpa_math_for_mps ([#159695](https://github.com/pytorch/pytorch/pull/159695))
- [dde] use sym_or when checking normalized shape in layer_norm ([#160683](https://github.com/pytorch/pytorch/pull/160683))
- migrate more simple gso checks ([#160253](https://github.com/pytorch/pytorch/pull/160253))
- unify broadcast_shapes functions and avoid duplicates ([#160251](https://github.com/pytorch/pytorch/pull/160251))
- Add meta for add.Scalar ([#161332](https://github.com/pytorch/pytorch/pull/161332))
- use sym_or instead of any to avoid dde in calc_conv_nd_return_shape ([#162084](https://github.com/pytorch/pytorch/pull/162084))
- Fixes #154982: add missing to_result_dtype in vector_norm ([#155111](https://github.com/pytorch/pytorch/pull/155111))
- export: add explicit decomposition for aten.expand_copy and unit test ([#161688](https://github.com/pytorch/pytorch/pull/161688))
- make should_swap more dde friendly ([#162099](https://github.com/pytorch/pytorch/pull/162099))
- rewrite __maybe_broadcast should_expand check for unbacked ([#162109](https://github.com/pytorch/pytorch/pull/162109))
### security
