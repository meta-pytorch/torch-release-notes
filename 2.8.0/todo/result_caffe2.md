
# Release Notes worksheet caffe2

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
- Address the ignored warnings for `-Wmissing-field-initializers `in the file fbcode/caffe2/aten/src/ATen/native/cuda/RowwiseScaledMM.cu ([#153958](https://github.com/pytorch/pytorch/pull/153958))
### not user facing
- [caffe2] Do not use --no-as-needed on macOS ([#149421](https://github.com/pytorch/pytorch/pull/149421))
- [fbcode]Removing `@NoIntBaseDeprecated` annotation in `caffe2.thrift` file (#149742) ([#149744](https://github.com/pytorch/pytorch/pull/149744))
- caffe2: Fix lint errors in native/xnnpack/Linear.cpp ([#150508](https://github.com/pytorch/pytorch/pull/150508))
- [Codemod][AddExplicitStrictExportForTrainingInferenceArg] caffe2/test/export ([#150884](https://github.com/pytorch/pytorch/pull/150884))
- [modefile free][long tail] selectify fbcode/caffe2/defs.bzl ([#148925](https://github.com/pytorch/pytorch/pull/148925))
- [caffe2/c10/util/TypeIndex] Add '__CUDA_ARCH_LIST__' check ([#152030](https://github.com/pytorch/pytorch/pull/152030))
- [caffe2] Support building for armv8.1 ([#152766](https://github.com/pytorch/pytorch/pull/152766))
- [caffe2] Make c10::str works with scoped enum (#152705) ([#152705](https://github.com/pytorch/pytorch/pull/152705))
- [libc++ readiness][caffe2] No reason to check for "ext/stdio_filebuf.h" ([#154080](https://github.com/pytorch/pytorch/pull/154080))
### security
