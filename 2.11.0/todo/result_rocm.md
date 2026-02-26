
# Release Notes worksheet rocm

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

## rocm
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [ROCm] fix and unskip tests on rocm ([#169827](https://github.com/pytorch/pytorch/pull/169827))
- [ROCm] Enable device properties for ROCm >= 6.4 ([#170572](https://github.com/pytorch/pytorch/pull/170572))
- [ROCm] revert miopen channels last back to opt in ([#170780](https://github.com/pytorch/pytorch/pull/170780))
- [ROCm] remove gfx940 gfx941 ([#172369](https://github.com/pytorch/pytorch/pull/172369))
- [ROCm] support device-side assertions ([#172679](https://github.com/pytorch/pytorch/pull/172679))
- [ROCm] Bump AOTriton to 0.11.2b ([#174105](https://github.com/pytorch/pytorch/pull/174105))
- [ROCm] Add partitioned buffer approach for scatter add op ([#168073](https://github.com/pytorch/pytorch/pull/168073))
- [ROCm] assert HIP events in profiler stack trace ([#174366](https://github.com/pytorch/pytorch/pull/174366))
- [ROCm] Enabled and validated correct HIP events ([#171384](https://github.com/pytorch/pytorch/pull/171384))
### not user facing
- [ROCm] Enable scaled group mm on gfx950  ([#173737](https://github.com/pytorch/pytorch/pull/173737))
### security
