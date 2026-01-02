
# Release Notes worksheet sparse_frontend

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

## sparse_frontend
### bc breaking
### deprecation
### new features
### improvements
- Add MPS support sparse_mask backward and sparse sum backward ([#166260](https://github.com/pytorch/pytorch/pull/166260), [#169240](https://github.com/pytorch/pytorch/pull/169240))
- Add exp support for COO on CPU, CUDA and MPS ([#166801](https://github.com/pytorch/pytorch/pull/166801))
- Remove old CUDA 11 sparse code ([#166048](https://github.com/pytorch/pytorch/pull/166048), [#164531](https://github.com/pytorch/pytorch/pull/164531), [#164199](https://github.com/pytorch/pytorch/pull/164199))
### bug fixes
- Fix mul(COO, COO) on MPS for hybrid COO variants ([#166164](https://github.com/pytorch/pytorch/pull/166164))
- Update torch.sparse_coo_tensor error message to include more information about input tensor properties ([#161900](https://github.com/pytorch/pytorch/pull/161900))
- Fix GradTrackingTensor sparse layout propagation ([#165765](https://github.com/pytorch/pytorch/pull/165765))
### performance
### docs
### devs
### Untopiced
### not user facing
- Remove unused thrust inclusion ([#169051](https://github.com/pytorch/pytorch/pull/169051))
- [BE] C++20 template instantiation adjustments ([#168132](https://github.com/pytorch/pytorch/pull/168132))
- [5/N] Use Python 3.10 typing ([#167449](https://github.com/pytorch/pytorch/pull/167449))
- Remove old ROCm version checks and branches ([#166111](https://github.com/pytorch/pytorch/pull/166111))
- Don't return values in void functions ([#164809](https://github.com/pytorch/pytorch/pull/164809))
- [Caffe2] Add float batch box cox SVE128 implementation ([#159778](https://github.com/pytorch/pytorch/pull/159778))
- Use computed buffer sizes of torch for cusparseLt metadata ([#163125](https://github.com/pytorch/pytorch/pull/163125))
- [NFC] fixed mistake in comment ([#163697](https://github.com/pytorch/pytorch/pull/163697))
- [NFC] fixed typo in sparse semi structured filename ([#163904](https://github.com/pytorch/pytorch/pull/163904))
- [BE] Remove unused 'rows' parameter from spmm_bmm_coo_rows_grouped ([#166041](https://github.com/pytorch/pytorch/pull/166041))
- include `thrust/distance.h` explicitly in cuda sparse softmax ([#167436](https://github.com/pytorch/pytorch/pull/167436))
- Fix missing thrust includes ([#167450](https://github.com/pytorch/pytorch/pull/167450))
- Remove unnecessary uses of thrust::pair ([#168941](https://github.com/pytorch/pytorch/pull/168941))
### security
