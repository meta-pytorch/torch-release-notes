
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
- [BE] Eliminate TODO for 2022 ([#149557](https://github.com/pytorch/pytorch/pull/149557))
### deprecation
### new features
### improvements
- Refine host caching allocator ([#151403](https://github.com/pytorch/pytorch/pull/151403))
### bug fixes
### performance
### docs
### devs
### Untopiced
- Fix AOTI update_constant_buffer issue. ([#149243](https://github.com/pytorch/pytorch/pull/149243))
- load_inline no_implicit_headers mode ([#149480](https://github.com/pytorch/pytorch/pull/149480))
- Set requires grad in TensorMaker::make_tensor()  ([#148255](https://github.com/pytorch/pytorch/pull/148255))
- Make at::vec::Vectorized ops work with scalars ([#150380](https://github.com/pytorch/pytorch/pull/150380))
- Overload unary - operator on at::vec::Vectorized to call neg() ([#150568](https://github.com/pytorch/pytorch/pull/150568))
- Add HostAllocator as the unified parent class ([#151431](https://github.com/pytorch/pytorch/pull/151431))
- Expose bicubic mode for torch::nn::functional::grid_sample in LibTorch ([#150817](https://github.com/pytorch/pytorch/pull/150817))
- Remove `reinterpret_cast`s with undefined behavior from stable/library.h ([#151595](https://github.com/pytorch/pytorch/pull/151595))
- Remove std::is_arithmetic specialization from c10/util/strong_type.h ([#153424](https://github.com/pytorch/pytorch/pull/153424))
- add is_vec_specialized_for ([#152365](https://github.com/pytorch/pytorch/pull/152365))
- vec::map: directly process reduced-precision floats when reasonable ([#152366](https://github.com/pytorch/pytorch/pull/152366))
- Add vec_reduce_all specialization for std::plus on AArch64 ([#152388](https://github.com/pytorch/pytorch/pull/152388))
- add #pragma once to stable/library.h ([#154920](https://github.com/pytorch/pytorch/pull/154920))
- torch::stable::Tensor beginnings, mainly mem mgmt ([#155367](https://github.com/pytorch/pytorch/pull/155367))
- Extract CPU log_softmax kernels to header ([#156243](https://github.com/pytorch/pytorch/pull/156243))
### not user facing
- [codemod][lowrisk] Fix deprecated use of 0/NULL in caffe2/aten/src/ATen/native/quantized/cpu/qnnpack/src/fc-unpack.cc + 1 ([#148996](https://github.com/pytorch/pytorch/pull/148996))
- [codemod][lowrisk] Remove unused exception parameter from caffe2/aten/src/ATen/cuda/CUDABlas.cpp ([#149328](https://github.com/pytorch/pytorch/pull/149328))
- Extract reusable portions of elu_kernel into header ([#149673](https://github.com/pytorch/pytorch/pull/149673))
- [codemod] Fix `-Wambiguous-reversed-operator` in aten/src/ATen/cuda/tunable/Tunable.h ([#150744](https://github.com/pytorch/pytorch/pull/150744))
- Add tests to check pretty print when padding is a string in C++ API ([#153126](https://github.com/pytorch/pytorch/pull/153126))
- [submodule] Update gtest to v1.17.0 ([#153618](https://github.com/pytorch/pytorch/pull/153618))
- Fix some CMake issues ([#153686](https://github.com/pytorch/pytorch/pull/153686))
- Document how to use stack-based APIs with StableIValue ([#155984](https://github.com/pytorch/pytorch/pull/155984))
- [2/N] Fix cppcoreguidelines-init-variables suppression ([#146237](https://github.com/pytorch/pytorch/pull/146237))
- [BE][9/16] fix typos in torch/ (torch/csrc/) ([#156319](https://github.com/pytorch/pytorch/pull/156319))
- [BE][9/16] fix typos in torch/ (torch/csrc/) ([#156319](https://github.com/pytorch/pytorch/pull/156319))
### security
