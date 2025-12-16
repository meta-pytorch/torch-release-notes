
# Release Notes worksheet xpu

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

## xpu
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- Add a new API torch.xpu.can_device_access_peer for Intel GPU ([#162705](https://github.com/pytorch/pytorch/pull/162705))
- [1/N]Enable some tests in test_ops.TestCommon on Intel GPU ([#159944](https://github.com/pytorch/pytorch/pull/159944))
- Add a new API torch.xpu.is_tf32_supported for Intel GPU ([#163141](https://github.com/pytorch/pytorch/pull/163141))
- Give a friendly message for older Intel GPU ([#165622](https://github.com/pytorch/pytorch/pull/165622))
- Remove unused parameter when query extension attribute ([#165623](https://github.com/pytorch/pytorch/pull/165623))
- [xpu][feature] Introduce ExpandableSegment for XPU ([#166299](https://github.com/pytorch/pytorch/pull/166299))
- [xpu][feature] Support expandable segment feature for XPU ([#166292](https://github.com/pytorch/pytorch/pull/166292))
- [xpu][feature] Introduce PeerToPeerAccess API for XPU ([#166424](https://github.com/pytorch/pytorch/pull/166424))
- [xpu][fix] Fix XPU oneDNN memory query bug: pointer to array ([#166830](https://github.com/pytorch/pytorch/pull/166830))
- [xpu][fix] Fix conv1d precision error ([#162944](https://github.com/pytorch/pytorch/pull/162944))
- [xpu][test] Migrated two test files to XPU ([#166684](https://github.com/pytorch/pytorch/pull/166684))
- [xpu][fix] Fix empty cache on mempool ([#168074](https://github.com/pytorch/pytorch/pull/168074))
- [xpu][fix] Refine memory pool logic when expandable segement enabled ([#168956](https://github.com/pytorch/pytorch/pull/168956))
- [xpu][feature] enable Sycl CPP extension on Windows ([#162579](https://github.com/pytorch/pytorch/pull/162579))
- [xpu][fix] Support xpu custom raw_alloc/delete in caching allocator ([#168957](https://github.com/pytorch/pytorch/pull/168957))
- [xpu][feature] [1/2] Introduce XPUPluggableAllocator in cpp part ([#168966](https://github.com/pytorch/pytorch/pull/168966))
- [xpu][feature] [2/2] Introduce XPUPluggableAllocator in frontend part ([#169043](https://github.com/pytorch/pytorch/pull/169043))
### not user facing
- [XPU] Enhance XPUGeneratorImpl functionality to support XPUGraph ([#163332](https://github.com/pytorch/pytorch/pull/163332))
- [1/3][XPU][feature] The implementation of memory private pool in XPU device allocator ([#166831](https://github.com/pytorch/pytorch/pull/166831))
### security
