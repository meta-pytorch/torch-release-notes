
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
- Custom Op handle 1-element tuples ([#155447](https://github.com/pytorch/pytorch/pull/155447))
### performance
### docs
### devs
### Untopiced
- Avoid overflow in vector_norm for scalar input ([#144073](https://github.com/pytorch/pytorch/pull/144073))
- [custom ops] Override fake registration ([#150806](https://github.com/pytorch/pytorch/pull/150806))
- Generate meta kernel with operator profiles ([#150807](https://github.com/pytorch/pytorch/pull/150807))
- [dynamic shapes] rewrite expand with guard_or_false ([#150236](https://github.com/pytorch/pytorch/pull/150236))
- Save/load op profiles ([#151817](https://github.com/pytorch/pytorch/pull/151817))
- [dynamic shapes] aten.constant_pad_nd meta impl ([#152129](https://github.com/pytorch/pytorch/pull/152129))
- [dynamic shapes] use try-catch instead of guard_or_true for reshape_view_helper ([#152638](https://github.com/pytorch/pytorch/pull/152638))
- error out on negative offs or on K=0 in group gemm ([#153226](https://github.com/pytorch/pytorch/pull/153226))
- Data dependent free reshape. ([#153198](https://github.com/pytorch/pytorch/pull/153198))
- [dynamic shapes] unbacked safe unsqueeze ([#154087](https://github.com/pytorch/pytorch/pull/154087))
- [dynamic shapes] guard_or_false for cat, repeat ([#155290](https://github.com/pytorch/pytorch/pull/155290))
- [dynamic shapes] skip fused linear path if not definitely contiguous ([#155051](https://github.com/pytorch/pytorch/pull/155051))
- Align meta deducing for fft_r2c with fft_r2c_mkl on XPU ([#156048](https://github.com/pytorch/pytorch/pull/156048))
### not user facing
- fix cuDNN SDPA meta registration ([#148921](https://github.com/pytorch/pytorch/pull/148921))
- Add meta function for out variants of ones,zeros,empty ([#149098](https://github.com/pytorch/pytorch/pull/149098))
- [export] fix stft decomp and making it consistent with cpp impl. ([#149232](https://github.com/pytorch/pytorch/pull/149232))
- Remove aten.elu core ATen decomp because it is now core ATen ([#149780](https://github.com/pytorch/pytorch/pull/149780))
- Fix torch.matmul related out dtype check ([#148174](https://github.com/pytorch/pytorch/pull/148174))
- Fix addbmm & addmv & baddbmm out dtype check ([#148176](https://github.com/pytorch/pytorch/pull/148176))
- Make torch._chunk_cat support non-contiguous inputs ([#151263](https://github.com/pytorch/pytorch/pull/151263))
- [MPSInductor] Fix masked_fill decomp ([#152268](https://github.com/pytorch/pytorch/pull/152268))
- Fix GuardOnDataDependentSymNode in the normalize operator ([#152039](https://github.com/pytorch/pytorch/pull/152039))
- Support using SymInt shapes for torch.baddbmm no-broadcast case ([#153112](https://github.com/pytorch/pytorch/pull/153112))
- Fix `torch.isin` decomposition for scalar inputs ([#153216](https://github.com/pytorch/pytorch/pull/153216))
- Add skip_dtype_check_in_meta_registrations config to torch/fx/experimental/_config ([#153513](https://github.com/pytorch/pytorch/pull/153513))
- Treat dim=[] same as dim=None ([#153570](https://github.com/pytorch/pytorch/pull/153570))
- use definitely_contiguous for _prim_elementwise_meta short circuit ([#153441](https://github.com/pytorch/pytorch/pull/153441))
- Fix clamp type promotion in inductor decomposition ([#154471](https://github.com/pytorch/pytorch/pull/154471))
- avoid sym_max on nested int in is_contiguous.  ([#154633](https://github.com/pytorch/pytorch/pull/154633))
- Symintify baddbmm ([#154656](https://github.com/pytorch/pytorch/pull/154656))
- [refactor] is_known_channels_last_contiguous* -> definitely_channels_last_contiguous* ([#155499](https://github.com/pytorch/pytorch/pull/155499))
- [export] support linear & layer_norm unbacked ([#155260](https://github.com/pytorch/pytorch/pull/155260))
- fix slice w/ dynamic shapes ([#153131](https://github.com/pytorch/pytorch/pull/153131))
- remove allow-untyped-defs from context.py ([#155622](https://github.com/pytorch/pytorch/pull/155622))
- remove gso from vector_norm ([#156530](https://github.com/pytorch/pytorch/pull/156530))
### security
