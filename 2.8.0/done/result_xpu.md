
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
- Support Intel distributed backend (XCCL) in PyTorch ([#141856](https://github.com/pytorch/pytorch/pull/141856))
- Support int4 WOQ GEMM on Intel GPU ([#137566](https://github.com/pytorch/pytorch/pull/137566))
- Support SYCL kernels through CPP Extension([#132945](https://github.com/pytorch/pytorch/pull/132945))
- Support safe softmax for SDPA on Intel GPU ([#151999](https://github.com/pytorch/pytorch/pull/151999))
- Support GQA and different head_dim of value for SDPA on Intel GPU([#150992](https://github.com/pytorch/pytorch/pull/150992))

### improvements
- Add memory reporting to Memory Profiler for Intel GPU ([#152842](https://github.com/pytorch/pytorch/pull/152842))
- Support Intel GPU profiler toggle functionality ([#155135](https://github.com/pytorch/pytorch/pull/155135))
- Support distributed memory tracker integration for Intel GPU ([#150703](https://github.com/pytorch/pytorch/pull/150703))
- Improve scalar tensor case handling in addmm, baddmm on Intel GPU ([#153051](https://github.com/pytorch/pytorch/pull/153051))
- Support f32 intermediate dtype, headdim <= 576, and f32 causal mask for SDPA ([#152091](https://github.com/pytorch/pytorch/pull/152091))
- Add Intel GPU device support for nested_layer_norm ([#148593](https://github.com/pytorch/pytorch/pull/148593))
- Refine oneDNN context manager API on Intel GPU ([#147349](https://github.com/pytorch/pytorch/pull/147349))
- Improve error handling and reporting in Intel GPU CMake files ([#149353](https://github.com/pytorch/pytorch/pull/149353))
- Support multi_arch_kernel_binary option in AOTInductor for Intel GPU ([#154514](https://github.com/pytorch/pytorch/pull/154514))
- Embed SPIR-V files into .so for Intel GPU ([#153924](https://github.com/pytorch/pytorch/pull/153924))
- Add generic and Intel GPU specific Stream & Event in UserDefineClass ([#155787](https://github.com/pytorch/pytorch/pull/155787))

### bug fixes
- Fix matmul accuracy when offset > 0 ([#154495](https://github.com/pytorch/pytorch/pull/154495))
- Correct torch.xpu.is_bf16_supported to return False if no Intel GPU detected ([#152317](https://github.com/pytorch/pytorch/pull/152317))
- Fix AOT compilation in SYCL C++ extension ([#156364](https://github.com/pytorch/pytorch/pull/156364))
- Fix compilation issue when TORCH_Intel GPU_ARCH_LIST is empty ([#153604](https://github.com/pytorch/pytorch/pull/153604))
- Add device guard for multi-device conv ([#153067](https://github.com/pytorch/pytorch/pull/153067))

### performance
- Enable post-op fusion for mkldnn Conv on Intel GPU ([#150287](https://github.com/pytorch/pytorch/pull/150287))
- Skip CUDA API calls in AMP to save Intel GPU host overhead ([#151111](https://github.com/pytorch/pytorch/pull/151111))
- Add OneDNN primitive cache support for Int4 WOQ GEMM on Intel GPU ([#147693](https://github.com/pytorch/pytorch/pull/147693))


### docs
- Improve "Getting Started on Intel GPU" hardware requirements and notes ([#151886](https://github.com/pytorch/pytorch/pull/151886))

### devs
### Untopiced
### not user facing
### security
