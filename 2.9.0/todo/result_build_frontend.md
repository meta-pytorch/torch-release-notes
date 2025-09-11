
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
- Remove `/d2implyavx512upperregs-` flag ([#159431](https://github.com/pytorch/pytorch/pull/159431))
- Add ScalarType -> shim conversion, add stable::Tensor.scalar_type ([#160557](https://github.com/pytorch/pytorch/pull/160557))
### deprecation
### new features
- Add transpose to torch/csrc/stable ([#158160](https://github.com/pytorch/pytorch/pull/158160))
- Add zero_() and empty_like(t) to torch/csrc/stable/ops.h ([#158866](https://github.com/pytorch/pytorch/pull/158866))
### improvements
### bug fixes
- [BE] Fix dev warning in `Dependencies.cmake` ([#159702](https://github.com/pytorch/pytorch/pull/159702))
- gloo: fix building system gloo with CUDA/HIP ([#146637](https://github.com/pytorch/pytorch/pull/146637))
- [CD] Build libtorch without nvshmem ([#160910](https://github.com/pytorch/pytorch/pull/160910))
### performance
### docs
### devs
### Untopiced
- Check F2C BLAS for OpenBLAS and other vendors ([#143846](https://github.com/pytorch/pytorch/pull/143846))
- Add an ovrsource target for torch/headeronly ([#157912](https://github.com/pytorch/pytorch/pull/157912))
- Migrate c10/macros/cmake_macros.h.in to torch/headeronly ([#158035](https://github.com/pytorch/pytorch/pull/158035))
- Move c10/macros/Macros.h to headeronly ([#158365](https://github.com/pytorch/pytorch/pull/158365))
- Add STD_TORCH_CHECK to headeronly ([#158377](https://github.com/pytorch/pytorch/pull/158377))
- Migrate easy q(u)int/bits stuff to torch/headeronly ([#159302](https://github.com/pytorch/pytorch/pull/159302))
- Move Float4 to headeronly ([#159414](https://github.com/pytorch/pytorch/pull/159414))
- Move BFloat16.h to headeronly ([#159412](https://github.com/pytorch/pytorch/pull/159412))
- Move Float8 variations to headeronly ([#159415](https://github.com/pytorch/pytorch/pull/159415))
- Move complex to headeronly ([#159411](https://github.com/pytorch/pytorch/pull/159411))
- [Reland] Migrate ScalarType to headeronly ([#159911](https://github.com/pytorch/pytorch/pull/159911))
- Add stable Tensor get_device_index, use more stable DeviceIndex ([#160143](https://github.com/pytorch/pytorch/pull/160143))
- Add `is_cpu` method to stable tensor type ([#160212](https://github.com/pytorch/pytorch/pull/160212))
### not user facing
- [build] remove cmake cache and reconfigure again if it is invalid ([#156958](https://github.com/pytorch/pytorch/pull/156958))
- [build] remove `wheel` from build requirements ([#158027](https://github.com/pytorch/pytorch/pull/158027))
- Error when TORCH_STABLE_ONLY is defined in TensorBase.h ([#161658](https://github.com/pytorch/pytorch/pull/161658))
### security
