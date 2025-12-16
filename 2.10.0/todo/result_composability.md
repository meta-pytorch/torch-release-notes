
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
- [FakeTensor] Supplement the relevant logic for converting conv1d to conv2d in meta_conv ([#160408](https://github.com/pytorch/pytorch/pull/160408))
- [dynamic shapes] unbacked-safe slicing ([#161414](https://github.com/pytorch/pytorch/pull/161414))
- [4/N] Apply ruff UP035 rule to python code ([#164206](https://github.com/pytorch/pytorch/pull/164206))
- [5/N] Apply ruff UP035 rule ([#164423](https://github.com/pytorch/pytorch/pull/164423))
- Add pyrefly suppressions (3/n) ([#164588](https://github.com/pytorch/pytorch/pull/164588))
- Pyrefly suppressions 4/n ([#164615](https://github.com/pytorch/pytorch/pull/164615))
- Add pyrefly suppressions ([#164748](https://github.com/pytorch/pytorch/pull/164748))
- Pyrefly suppressions 6/n ([#164877](https://github.com/pytorch/pytorch/pull/164877))
- more sizelike deprecation ([#164889](https://github.com/pytorch/pytorch/pull/164889))
- Back out "Do not decompose in functionalization/proxy tensor if autograd wouldn't have decomposed (#164939)" ([#165910](https://github.com/pytorch/pytorch/pull/165910))
- Fix flake8 B028 warnings ([#166224](https://github.com/pytorch/pytorch/pull/166224))
- Fix pyrefly ignore syntax ([#166438](https://github.com/pytorch/pytorch/pull/166438))
- Fix pyrefly error syntax (2/n) ([#166448](https://github.com/pytorch/pytorch/pull/166448))
- Reapply "Back out "Do not decompose in functionalization/proxy tensor if autograd wouldn't have decomposed (#164939)" (#165910)" (061fa73c97d)
- Fix torch.linalg.eig inductor stride mismatch ([#162484](https://github.com/pytorch/pytorch/pull/162484))
- [3/N] Use key in dict for existence checks ([#167214](https://github.com/pytorch/pytorch/pull/167214))
- harden backed_size_oblivious and broadcast_shapes ([#167232](https://github.com/pytorch/pytorch/pull/167232))
- backed size oblivious checks for expand() ([#167689](https://github.com/pytorch/pytorch/pull/167689))
- Fix take_along_dim negative index handling (#146211) ([#152161](https://github.com/pytorch/pytorch/pull/152161))
### not user facing
- remove gso from collapse_view_helper ([#162212](https://github.com/pytorch/pytorch/pull/162212))
- [mxfp8 torch._scaled_grouped_mm] fix meta registration for 3d tensor ([#162765](https://github.com/pytorch/pytorch/pull/162765))
- are_strides_like_channels_last_or_false ([#162354](https://github.com/pytorch/pytorch/pull/162354))
- [cuDNN][SDPA][submodule] Roll-back cuDNN frontend upgrade, update Meta registration ([#163104](https://github.com/pytorch/pytorch/pull/163104))
- support unbacked softmax / logsoftmax ([#162216](https://github.com/pytorch/pytorch/pull/162216))
- Don't register wrong overload to prim decomp ([#163138](https://github.com/pytorch/pytorch/pull/163138))
- [Bugfix] Match eager stride semantics for cloned tensors with preserve_format in compile ([#163017](https://github.com/pytorch/pytorch/pull/163017))
- Better decomp for torch.eye ([#163386](https://github.com/pytorch/pytorch/pull/163386))
- Add fake_impl for _native_multi_head_attention ([#163700](https://github.com/pytorch/pytorch/pull/163700))
- [Fix] Adding missing `f` prefixes to formatted strings [1/N] ([#164065](https://github.com/pytorch/pytorch/pull/164065))
- Remove export of slice_in_dim ([#164117](https://github.com/pytorch/pytorch/pull/164117))
- Fix cdist export compute mode validation ([#161724](https://github.com/pytorch/pytorch/pull/161724))
- Missing lambda in torch._check ([#164225](https://github.com/pytorch/pytorch/pull/164225))
- [BE][Easy]: Add prims common TypeGuard ([#164263](https://github.com/pytorch/pytorch/pull/164263))
- [export] support unbacked stack ([#163867](https://github.com/pytorch/pytorch/pull/163867))
- remove guard_size_oblivious from is_contiguous python eager eval path. ([#164622](https://github.com/pytorch/pytorch/pull/164622))
- Use sym_eq and sym_and on symbolic shapes in common_meta_baddbmm_bmm ([#164781](https://github.com/pytorch/pytorch/pull/164781))
- [Fix] missing lambda in torch._check ([#165043](https://github.com/pytorch/pytorch/pull/165043))
- Ensure rms_norm decomp generates add.Scalar for pattern match BC ([#165437](https://github.com/pytorch/pytorch/pull/165437))
- Fix typo in torch._refs ([#167310](https://github.com/pytorch/pytorch/pull/167310))
- Add meta registration for scaled_mm_v2 and test ([#167653](https://github.com/pytorch/pytorch/pull/167653))
- Fix: Remove incorrect non-negative validation for correction parameter in torch.var during export ([#162254](https://github.com/pytorch/pytorch/pull/162254))
- [hoo] Fix unlift of effects with invoke_subgraph ([#167363](https://github.com/pytorch/pytorch/pull/167363))
- Fix-index-select-contiguous-compile ([#168922](https://github.com/pytorch/pytorch/pull/168922))
- [16/N]Use Python 3.10 typing ([#169917](https://github.com/pytorch/pytorch/pull/169917))
### security
