
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
- Support Intel distributed backend (XCCL) ([#141856](https://github.com/pytorch/pytorch/pull/141856))
- Support int4 WOQ GEMM on Intel GPU ([#137566](https://github.com/pytorch/pytorch/pull/137566))
- Support SYCL kernels through CPP Extension([#132945](https://github.com/pytorch/pytorch/pull/132945))

### improvements
- Support safe softmax, GQA, fp32 causal mask for SDP and Increase maximum headdim from 256 to 576 on Intel GPU ([#151999](https://github.com/pytorch/pytorch/pull/151999), [#150992](https://github.com/pytorch/pytorch/pull/150992), [#152091](https://github.com/pytorch/pytorch/pull/152091))
- Add memory reporting to Memory Profiler for Intel GPU ([#152842](https://github.com/pytorch/pytorch/pull/152842))
- Support Intel GPU profiler toggle functionality ([#155135](https://github.com/pytorch/pytorch/pull/155135))
- Support distributed memory tracker integration for Intel GPU ([#150703](https://github.com/pytorch/pytorch/pull/150703))
- Improve error handling and reporting in Intel GPU CMake files ([#149353](https://github.com/pytorch/pytorch/pull/149353))
- Support `embed_cubin` and `multi_arch_kernel_binary` options in AOTInductor for Intel GPU ([#154514](https://github.com/pytorch/pytorch/pull/154514), [#153924](https://github.com/pytorch/pytorch/pull/153924))
- Add generic and Intel GPU specific Stream & Event in UserDefineClass ([#155787](https://github.com/pytorch/pytorch/pull/155787))

### bug fixes
- Fix matmul accuracy when offset > 0 ([#154495](https://github.com/pytorch/pytorch/pull/154495))
- Fix the issue that `torch.xpu.is_bf16_supported` always returns `True` even if Intel GPU is not available ([#152317](https://github.com/pytorch/pytorch/pull/152317))
- Fix AOT compilation in SYCL C++ extension ([#156364](https://github.com/pytorch/pytorch/pull/156364))
- Add device guard for Cov to handle the case that the input tensors reside on different devices([#153067](https://github.com/pytorch/pytorch/pull/153067))

### performance
- Enable post-op fusion for oneDNN Conv on Intel GPU ([#150287](https://github.com/pytorch/pytorch/pull/150287))
- Reduce host overhead for Intel GPU by eliminating meaningless API calls ([#151111](https://github.com/pytorch/pytorch/pull/151111))
- Improve INT4 WOQ GEMM for Intel GPU by introducing a cache mechanism to reduce the oneDNN integration overhead further. ([#147693](https://github.com/pytorch/pytorch/pull/147693))
- Improve scalar tensor case handling in addmm, baddmm to reduce oneDNN integration overhead on Intel GPU ([#153051](https://github.com/pytorch/pytorch/pull/153051))


### docs
- Improve "Getting Started on Intel GPU" hardware requirements and notes ([#151886](https://github.com/pytorch/pytorch/pull/151886))

### devs
### Untopiced
### not user facing
### security
