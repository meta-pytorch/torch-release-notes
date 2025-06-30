
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
- Refine XPU oneDNN context manager API ([#147349](https://github.com/pytorch/pytorch/pull/147349))
### bug fixes
### performance
### docs
### devs
### Untopiced
- xpu: improve error handling and reporting in XPU cmake files ([#149353](https://github.com/pytorch/pytorch/pull/149353))
- Add default XPU toolkit path to CMake ([#149270](https://github.com/pytorch/pytorch/pull/149270))
- [Intel gpu] always set deterministic for xpu accuracy test ([#149028](https://github.com/pytorch/pytorch/pull/149028))
- [XPU] Add an implict conversion from XPUStream to sycl::queue* ([#148646](https://github.com/pytorch/pytorch/pull/148646))
- Correct torch.xpu.is_bf16_supported return False if no XPU detected ([#152317](https://github.com/pytorch/pytorch/pull/152317))
- xpu: rely on sycl/sycl.hpp to include bfloat16.hpp ([#152562](https://github.com/pytorch/pytorch/pull/152562))
- [Intel GPU] undo broadcast on zero stride tensor for SDPA ([#151976](https://github.com/pytorch/pytorch/pull/151976))
- Define USE_C10D_XCCL and USE_XCCL in pytorch ([#147593](https://github.com/pytorch/pytorch/pull/147593))
- Add memory reporting for XPU to Memory Profiler ([#152842](https://github.com/pytorch/pytorch/pull/152842))
- Update USE_XCCL option if USE_XPU is OFF ([#153936](https://github.com/pytorch/pytorch/pull/153936))
- Keep XPU compatible with toolchain 2025.2 ([#154359](https://github.com/pytorch/pytorch/pull/154359))
- [Intel GPU] Support f32 intermediate dtype, headdim size <=576 and f32 causal mask for SDPA ([#152091](https://github.com/pytorch/pytorch/pull/152091))
- [Intel GPU] Enable safe softmax for XPU SDPA ([#151999](https://github.com/pytorch/pytorch/pull/151999))
- xpu: fix AOT compilation in sycl cpp extension ([#156364](https://github.com/pytorch/pytorch/pull/156364))
- Add toggle functionality for XPU profiler ([#155135](https://github.com/pytorch/pytorch/pull/155135))
### not user facing
- Add XPU device to nested_layer_norm ([#148593](https://github.com/pytorch/pytorch/pull/148593))
- xpu: update filter out of dg2 AOT target ([#148677](https://github.com/pytorch/pytorch/pull/148677))
- Add "xpu" to __all__ for torch/version.py ([#149695](https://github.com/pytorch/pytorch/pull/149695))
- xpu: get xpu arch flags at runtime in cpp_extensions ([#152192](https://github.com/pytorch/pytorch/pull/152192))
- [Kineto] Upgrade the kineto commit to fb36cce ([#152007](https://github.com/pytorch/pytorch/pull/152007))
- [Intel GPU] add tf32 support for matmul on XPU ([#144240](https://github.com/pytorch/pytorch/pull/144240))
- [Intel GPU][Inductor] Fallback embedding_dense_backward on XPU ([#151637](https://github.com/pytorch/pytorch/pull/151637))
- Record the XPU and XCCL build settings in the compiled binary ([#147161](https://github.com/pytorch/pytorch/pull/147161))
- Add C10_NODEPRECATED check for xpu ([#153935](https://github.com/pytorch/pytorch/pull/153935))
- Fix platform detection in MKLDNN CMake file ([#142067](https://github.com/pytorch/pytorch/pull/142067))
- [Intel GPU] OneDNN primitive cache support for Int4 WOQ gemm on XPU ([#147693](https://github.com/pytorch/pytorch/pull/147693))
- [Intel GPU] fix matmul accuracy when offset > 0 ([#154495](https://github.com/pytorch/pytorch/pull/154495))
- XPU enable XCCL by default ([#154963](https://github.com/pytorch/pytorch/pull/154963))
### security
