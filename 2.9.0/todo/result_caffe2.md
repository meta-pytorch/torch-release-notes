
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
- Name threads in caffe2/torch/distributed/checkpoint AsyncCheckpointExecutor ([#158612](https://github.com/pytorch/pytorch/pull/158612))
- [caffe2]  Fix Missing override in get_buffer of NCCLSymmetricMemory ([#158597](https://github.com/pytorch/pytorch/pull/158597))
### not user facing
- [caffe2] Allow the elimination of implicit calls to strlen when using the RECORD_FUNCTION macros ([#153567](https://github.com/pytorch/pytorch/pull/153567))
- [TSAN][live speech translation] Fix A data race in caffe2 ([#156378](https://github.com/pytorch/pytorch/pull/156378))
- [gtest][listing] Enable gtest json listing for the fbcode/caffe2 project ([#156816](https://github.com/pytorch/pytorch/pull/156816))
- [caffe2] Enable auto vectorization ([#157984](https://github.com/pytorch/pytorch/pull/157984))
- Cleanup old caffe2 scripts ([#158475](https://github.com/pytorch/pytorch/pull/158475))
- [gtest][listing] fixing caffe2:verify_api_visibility - main ([#158229](https://github.com/pytorch/pytorch/pull/158229))
- Cleanup old caffe2 scripts ([#158475](https://github.com/pytorch/pytorch/pull/158475))
- [codemod] Fix unused-local-typedef issue in caffe2/aten/src/ATen/native/cuda/CUDALoops.cuh +2 ([#160944](https://github.com/pytorch/pytorch/pull/160944))
### security
