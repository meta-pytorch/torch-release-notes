
# Release Notes worksheet autograd_frontend

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

## autograd_frontend
### bc breaking
- Add missing in-place on view check to custom autograd.Function ([#153094](https://github.com/pytorch/pytorch/pull/153094))
### deprecation
### new features
### improvements
- Improve error message when view of intermediate is returned from autograd.Function and marked dirty ([#149543](https://github.com/pytorch/pytorch/pull/149543))
### bug fixes
### performance
### docs
- Update docs of saved_tensors_hooks to avoid ref cycle ([#153049](https://github.com/pytorch/pytorch/pull/153049))
- [BE] Mention debug=True in AC error messages ([#155593](https://github.com/pytorch/pytorch/pull/155593))
### devs
### Untopiced
- support multinomial for dynamic num_samples ([#149463](https://github.com/pytorch/pytorch/pull/149463))
- partitioner: ensure collectives saved by SAC that are actually unused in the bw are properly not saved ([#149652](https://github.com/pytorch/pytorch/pull/149652))
- Fix `torch.autograd.backward` `inputs` validation ([#150975](https://github.com/pytorch/pytorch/pull/150975))
- add min/max_seqlen to non_differentiable ([#151750](https://github.com/pytorch/pytorch/pull/151750))
- [dynamic shapes] support SymInt inputs for kthvalue ([#152151](https://github.com/pytorch/pytorch/pull/152151))
- SAC: fix recompute tag propagation for ops with list[tensor] inputs ([#152195](https://github.com/pytorch/pytorch/pull/152195))
- [3/N] Use internal linkage in C++ files  ([#151297](https://github.com/pytorch/pytorch/pull/151297))
- [autograd][docs] Add more details on why save_for_backward is important in extending autograd note ([#153005](https://github.com/pytorch/pytorch/pull/153005))
- Add missing attr access check for legacy autograd.Function ([#155055](https://github.com/pytorch/pytorch/pull/155055))
### not user facing
- bf16 grouped gemm ([#150374](https://github.com/pytorch/pytorch/pull/150374))
- Update gradient behavior note in torch.amin and torch.amax ([#155071](https://github.com/pytorch/pytorch/pull/155071))
- [BE] fix typos in tools/ ([#156082](https://github.com/pytorch/pytorch/pull/156082))
### security
