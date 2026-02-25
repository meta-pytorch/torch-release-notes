
# Release Notes worksheet caffe2

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

## caffe2
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- Rm platform args xplat/caffe2/aten/src/ATen/native/quantized/cpu/qnnpack/buckbuild.bzl ([#169130](https://github.com/pytorch/pytorch/pull/169130))
- [reland][ROCm] remove caffe2 from hipify ([#172796](https://github.com/pytorch/pytorch/pull/172796))
- [pytorch][PR] [reland][ROCm] remove caffe2 from hipify ([#173372](https://github.com/pytorch/pytorch/pull/173372))
- [reland][ROCm] remove caffe2 from hipify ([#174087](https://github.com/pytorch/pytorch/pull/174087))
### not user facing
- [pytorch] redirect `fbcode//caffe2/c10:c10` to the OSS/conda version ([#169004](https://github.com/pytorch/pytorch/pull/169004))
- Rm platform compiler flags from xplat/caffe2/third_party/xnnpack.buck.bzl ([#169808](https://github.com/pytorch/pytorch/pull/169808))
- [aarch64][caffe2] Fix FBGEMM detection on aarch64 ([#169379](https://github.com/pytorch/pytorch/pull/169379))
- [codemod] Fix deprecated-literal-operator in caffe2/aten/src/ATen/native/cudnn/Conv_v7.cpp +4 ([#170329](https://github.com/pytorch/pytorch/pull/170329))
- [folly][caffe2] Remove use of `folly:molly` target ([#171711](https://github.com/pytorch/pytorch/pull/171711))
- Fix caffe2 genrules for root based genrules rollout ([#170574](https://github.com/pytorch/pytorch/pull/170574))
- [caffe2] Skip subprocess test in fbcode for D91862702 ([#174117](https://github.com/pytorch/pytorch/pull/174117))
- [caffe2] Fix signal handler deleting siginfo_t in resulting Coredump ([#174247](https://github.com/pytorch/pytorch/pull/174247))
- [caffe2][cudnn] Fix incorrect TORCH_CHECK usage in MHA.cpp ([#174885](https://github.com/pytorch/pytorch/pull/174885))
- [pytorch][caffe2] fix conditional-uninitialized warnings in Math.h ([#174904](https://github.com/pytorch/pytorch/pull/174904))
### security
