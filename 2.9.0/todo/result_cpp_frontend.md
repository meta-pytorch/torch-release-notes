
# Release Notes worksheet cpp_frontend

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

## cpp_frontend
### bc breaking
### deprecation
### new features
### improvements
- Introduce AcceleratorAllocatorConfig as the common class ([#149601](https://github.com/pytorch/pytorch/pull/149601))
- Introduce AcceleratorAllocatorConfig as the common class ([#149601](https://github.com/pytorch/pytorch/pull/149601))
- Introduce AcceleratorAllocatorConfig as the common class ([#149601](https://github.com/pytorch/pytorch/pull/149601))
- [C10] Add `Scalar::isUnsigned()` method ([#159877](https://github.com/pytorch/pytorch/pull/159877))
### bug fixes
- Fix torch.utils.cpp_extension parser for clang version 20.1.7+libcxx ([#157666](https://github.com/pytorch/pytorch/pull/157666))
- Fix `MakeTensor::computeStorageSize()` ([#158690](https://github.com/pytorch/pytorch/pull/158690))
- Fix AllocatorConfig potential SIO issue ([#159629](https://github.com/pytorch/pytorch/pull/159629))
### performance
### docs
### devs
### Untopiced
- Improve error message for torch.binomial enforcing float inputs ([#157658](https://github.com/pytorch/pytorch/pull/157658))
- Detach tensor before clone in SGD optimiser and other code ([#159204](https://github.com/pytorch/pytorch/pull/159204))
- Feature: Implement support for `cudnn_batch_norm_out` kernel to replace the autogen approach. ([#123020](https://github.com/pytorch/pytorch/pull/123020))
- [nativert] Expose ModelRunner to public through pmpl type ModelRunnerHandle. ([#159989](https://github.com/pytorch/pytorch/pull/159989))
### not user facing
- Refactor CUDAAllocatorConfig to reuse AcceleratorAllocatorConfig ([#150312](https://github.com/pytorch/pytorch/pull/150312))
- Remove unsafe PyTorchError constructor ([#154961](https://github.com/pytorch/pytorch/pull/154961))
- Refactor CUDAAllocatorConfig to reuse AcceleratorAllocatorConfig ([#150312](https://github.com/pytorch/pytorch/pull/150312))
- Refactor CUDAAllocatorConfig to reuse AcceleratorAllocatorConfig ([#150312](https://github.com/pytorch/pytorch/pull/150312))
- Refactor CUDAAllocatorConfig to reuse AcceleratorAllocatorConfig ([#150312](https://github.com/pytorch/pytorch/pull/150312))
- [codemod] Fix unreachable-break issue in caffe2/c10/cuda/CUDAFunctions.cpp +2 ([#160257](https://github.com/pytorch/pytorch/pull/160257))
### security
