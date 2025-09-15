
# Release Notes worksheet rocm

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

## rocm
### bc breaking
### deprecation
### new features
- OCP Micro-scaling Format (mx-fp8/mx-fp4) Support ([#151360](https://github.com/pytorch/pytorch/pull/151360))
- Support experimental CU carveout torch._C._set_sm_carveout_experimental() ([#149466](https://github.com/pytorch/pytorch/pull/149466))
- Add FP8 rowwise support to _scaled_grouped_mm ([#159075](https://github.com/pytorch/pytorch/pull/159075))
### improvements
- Additional hipify mappings ([#158056](https://github.com/pytorch/pytorch/pull/158056), [#158352](https://github.com/pytorch/pytorch/pull/158352), [#161992](https://github.com/pytorch/pytorch/pull/161992))
- composable_kernel (CK) backend user interface refactored to improve user experience ([#152951](https://github.com/pytorch/pytorch/pull/152951))
- Allow use of rocSOLVER for Cholesky inversion. ([#157154](https://github.com/pytorch/pytorch/pull/157154))
- AOT Inductor enable gfx950 for max autotune using CK ([#159195](https://github.com/pytorch/pytorch/pull/159195))
- Add flag torch.backends.miopen.immediate to toggle MIOpen Immediate Mode instead of relying on deterministic=True + benchmark=False ([#158951](https://github.com/pytorch/pytorch/pull/158951))
- MIOpen convolutions no longer call reshape_ or unexpectedly change memory formats ([#161687](https://github.com/pytorch/pytorch/pull/161687))
### bug fixes
- inductor with cudagraph trees hip:0 device error is resolved ([#161221](https://github.com/pytorch/pytorch/pull/161221))
- ROCm 7.0 BC-breaking change to amdclang compiler `warpSize` no longer constexpr ([#156979](https://github.com/pytorch/pytorch/pull/156979))
- ROCm 7.0 BC-breaking change to hiprtc needed fix resource_strings.h and jit_utils.cpp ([#159292](https://github.com/pytorch/pytorch/pull/159292), [#159996](https://github.com/pytorch/pytorch/pull/159996))
- On Windows fix some build failures and support some BLAS calls ([#161981](https://github.com/pytorch/pytorch/pull/161981))
- On Windows fix undefined symbol linker error after exposing MIOpen symbols ([#156479](https://github.com/pytorch/pytorch/pull/156479))
- On Windows fix finding ROCm/HIP version ([#156486](https://github.com/pytorch/pytorch/pull/156486))
- On Windows fix LoadHIP handling of environment variable paths on Windows. ([#159080](https://github.com/pytorch/pytorch/pull/159080))
- On Windows add hipcc compatibility flags to cpp_extension.py. ([#159790](https://github.com/pytorch/pytorch/pull/159790))
- Symmetric memory set handle type for ROCm ([#161741](https://github.com/pytorch/pytorch/pull/161741))
- In SDPA via AOTriton, logsumexp needs scaling back to natural base. ([#156903](https://github.com/pytorch/pytorch/pull/156903))
- Check stream graph capture status in memcpy_and_sync inline function ([#158165](https://github.com/pytorch/pytorch/pull/158165))
### performance
- SDPA now uses AOTriton to 0.11b ([#161754](https://github.com/pytorch/pytorch/pull/161754))
- hipblaslt is used by default on gfx908 for ROCm >= 6.3 ([#159092](https://github.com/pytorch/pytorch/pull/159092))
- Enable miopen channels last 3d for conv and batchnorm ([#160529](https://github.com/pytorch/pytorch/pull/160529))
- Remove extra transposes in NHWC convolutions on MIOpen ([#160435](https://github.com/pytorch/pytorch/pull/160435))
- Remove extra sync in tensor.item() ([#158486](https://github.com/pytorch/pytorch/pull/158486))
- Elementwise and reduction kernel perf improvements ([#159430](https://github.com/pytorch/pytorch/pull/159430), [#159652](https://github.com/pytorch/pytorch/pull/159652), [#160444](https://github.com/pytorch/pytorch/pull/160444), [#160466](https://github.com/pytorch/pytorch/pull/160466), [#161054](https://github.com/pytorch/pytorch/pull/161054), [#161180](https://github.com/pytorch/pytorch/pull/161180), [#161181](https://github.com/pytorch/pytorch/pull/161181))
- Symmetric Memory Performance improvements for two-shot allreduce ([#156746](https://github.com/pytorch/pytorch/pull/156746))
- Enable build of fbgemm_gpu genai sources for grouped gemm support. ([#160676](https://github.com/pytorch/pytorch/pull/160676))
### docs
### devs
### Untopiced
### not user facing
### security
