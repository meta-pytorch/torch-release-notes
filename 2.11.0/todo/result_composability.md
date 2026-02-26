
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
- Multiple optimizations to symbolic shape reasoning, including faster symbol sorting, reduced redundant hint computations, and optimized construction of relational expressions ([#174615](https://github.com/pytorch/pytorch/pull/174615), [#174655](https://github.com/pytorch/pytorch/pull/174655), [#174664](https://github.com/pytorch/pytorch/pull/174664), [#174652](https://github.com/pytorch/pytorch/pull/174652), [#174665](https://github.com/pytorch/pytorch/pull/174665), [#174662](https://github.com/pytorch/pytorch/pull/174662))
### docs
### devs
### Untopiced
- Fix-bucketize-export-crash ([#170751](https://github.com/pytorch/pytorch/pull/170751))
- Remove unused type ignores ([#171800](https://github.com/pytorch/pytorch/pull/171800))
- Remove unused ignores of pyrefly ([#171839](https://github.com/pytorch/pytorch/pull/171839))
- remove assert in library/cuda/ao ([#170803](https://github.com/pytorch/pytorch/pull/170803))
- Fix torch.isin compile shape for scalar test_elements ([#172531](https://github.com/pytorch/pytorch/pull/172531))
- [custom ops] Add check for out variant ([#174473](https://github.com/pytorch/pytorch/pull/174473))
### not user facing
- More decomp assert removal ([#170080](https://github.com/pytorch/pytorch/pull/170080))
- Updating the strides to be F-continuous for nonzero_static. ([#164120](https://github.com/pytorch/pytorch/pull/164120))
- [export] Fix isin decomposition ([#170362](https://github.com/pytorch/pytorch/pull/170362))
- [xpu][test] Enable int4 and int8 test on Intel GPU ([#166504](https://github.com/pytorch/pytorch/pull/166504))
- Remove assert meta/prims/refs ([#170776](https://github.com/pytorch/pytorch/pull/170776))
- Fix convolution_backward meta kernel stride predictions ([#171623](https://github.com/pytorch/pytorch/pull/171623))
- Fix conv shape check to be device-aware for zero-sized outputs ([#171888](https://github.com/pytorch/pytorch/pull/171888))
- Fix `MaxUnpool` crash ([#169359](https://github.com/pytorch/pytorch/pull/169359))
- Fix: Make are_strides_like_channels_last python match c++ ([#173038](https://github.com/pytorch/pytorch/pull/173038))
- Fix dde in _exec_fft ([#172717](https://github.com/pytorch/pytorch/pull/172717))
- [dynamic shapes] fix diagonal op DDEs ([#173408](https://github.com/pytorch/pytorch/pull/173408))
- [BugFix][Display]:  type(alpha) not type(beta) ([#173655](https://github.com/pytorch/pytorch/pull/173655))
- Add single-level NVFP4 to scaled_mm_v2 tracing ([#173806](https://github.com/pytorch/pytorch/pull/173806))
- add meta impl for foreach_norm ([#174342](https://github.com/pytorch/pytorch/pull/174342))
### security
