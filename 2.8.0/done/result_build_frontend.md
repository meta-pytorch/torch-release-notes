
# Release Notes worksheet build_frontend

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

## build_frontend
### bc breaking
**DLPack has been upgraded to 1.0, with some of the DLDeviceType enum values renamed. Please switch
to the new names.** ([#145000](https://github.com/pytorch/pytorch/pull/145000))

In 2.7.0
```
from torch.utils.dlpack import DLDeviceType

d1 = DLDeviceType.kDLGPU
d2 = DLDeviceType.kDLCPUPinned
...
```

In 2.8.0
```
from torch.utils.dlpack import DLDeviceType

d1 = DLDeviceType.kDLCUDA  # formerly kDLGPU
d2 = DLDeviceType.kDLCUDAHost  # formerly kDLCPUPinned
...
```

**NVTX3 code has been moved from `cmake/public/cuda.cmake` to `cmake/Dependencies.cmake` ([#151583](https://github.com/pytorch/pytorch/pull/151583))**

This is a BC-breaking change for the build system interface. Downstream projects that previously got NVTX3 through `cmake/public/cuda.cmake`
(i.e.. calling `find_package(TORCH REQUIRED)`) will now need to explicitly configure NVTX3 support in the library itself (i.e. use `USE_SYSTEM_NVTX=1`).
The change is to fix the broken behavior where downstream projects couldn't find NVTX3 anyway due to the `PROJECT_SOURCE_DIR` mismatch.

`2.7.0`: A downstream project using `-DUSE_SYSTEM_NVTX` would be able to find NVTX3 and `torch::nvtx3` via PyTorch's `cmake/public/cuda.cmake` logic.
`2.8.0`: A downstream project using `-DUSE_SYSTEM_NVTX` will not be able to find NVTX3 or `torch::nvtx3` via PyTorch's `cmake/public/cuda.cmake`.
The downstream project now needs to explicitly find NVTX3 and torch::nvtx3 by implementing the same logic in PyTorch's `cmake/Dependences.cmake`.

`2.7.0`: A downstream project NOT using `-DUSE_SYSTEM_NVTX` would encounter build errors with CUDA 12.8 or above.
`2.8.0`: A downstream project NOT using `-DUSE_SYSTEM_NVTX` will proceed building without NVTX unless another part of the build process re-enables NVTX.
### deprecation
### new features
### improvements
- Remove outdated warning about `TORCH_CUDA_ARCH_LIST` ([#152715](https://github.com/pytorch/pytorch/pull/152715), ([#155314](https://github.com/pytorch/pytorch/pull/155314)))
- Use `torch_compile_options` for c10 libraries ([#147821](https://github.com/pytorch/pytorch/pull/147821))
- Remove pre-CXX11 ABI logic from build script ([#149888](https://github.com/pytorch/pytorch/pull/149888))
- Make Eigen an optional build dependency ([#155955](https://github.com/pytorch/pytorch/pull/155955))
### bug fixes
- Make PyTorch buildable by `CMake-4.x` ([#150203](https://github.com/pytorch/pytorch/pull/150203))
- Fix `fbgemm` build with `gcc-12+` ([#150847](https://github.com/pytorch/pytorch/pull/150847))
- Force build to conform to C++ standard on Windows by adding `/permissive-` flag ([#149035](https://github.com/pytorch/pytorch/pull/149035))
### performance
### docs
### devs
### Untopiced
### not user facing
- Fix broken build within xplat/caffe2 ([#149403](https://github.com/pytorch/pytorch/pull/149403))
- Unbreak //c10/util:base ([#156216](https://github.com/pytorch/pytorch/pull/156216))
- [BE]: No include left behind - recursive glob setuptools support ([#148258](https://github.com/pytorch/pytorch/pull/148258))
- [bazel] Build flatbuffers within bazel ([#151364](https://github.com/pytorch/pytorch/pull/151364))
- Fix compilation warning with gcc14 ([#155934](https://github.com/pytorch/pytorch/pull/155934))
### security
