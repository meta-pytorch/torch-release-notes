
# Release Notes worksheet rocm

You should:

1. ensure commit categorization is correct
2. write up major features, bc-breaking changes, deprecations in detail
3. summarize the other sections

## 1. Ensure commit categorization is correct

* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.

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

## 2. Major features, BC-breaking changes, deprecations

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.

## 3. Summarize the other sections

For the other sections (improvements, bug fixes, performance, documentation, developers, not user facing) - use your
judgement to summarize the key PRs. You do not need to make every commit description perfect
(changed in v2.10 to simplify the process).

Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

Feel free to use https://github.com/pytorch/pytorch/releases/tag/v2.10.0 as an example.

## rocm
### bc breaking
### deprecation
### new features
- Enable expandable segments ([#173330](https://github.com/pytorch/pytorch/pull/173330), [#179930](https://github.com/pytorch/pytorch/pull/179930), [#179781](https://github.com/pytorch/pytorch/pull/179781))
- hipSPARSELt
  - Enable for ROCm >= 7.12 ([#170852](https://github.com/pytorch/pytorch/pull/170852), [#178285](https://github.com/pytorch/pytorch/pull/178285))
  - Enable FP8 semi-structured sparsity ([#179310](https://github.com/pytorch/pytorch/pull/179310))
- amdgcnspirv is now a supported offload target, not enabled by default ([#172559](https://github.com/pytorch/pytorch/pull/172559))
### improvements
- CPP extensions only compile for user's detected arch ([#168998](https://github.com/pytorch/pytorch/pull/168998))
- Remove obsolete HIP NaN handling workarounds; remove technical debt ([#171104](https://github.com/pytorch/pytorch/pull/171104))
### bug fixes
- Fix build due to void pointer arithmetic in CUDACachingAllocator ([c67b40befbb](https://github.com/pytorch/pytorch/commit/c67b40befbb9f12a3ca6ffadd94832a59eaab2d8))
- Fix SDPA build error when USE_FLASH_ATTENTION=0 USE_MEM_EFF_ATTENTION=1 ([#177552](https://github.com/pytorch/pytorch/pull/177552))
- Fix `_get_amdsmi_device_index` to return devices in correct order ([#178398](https://github.com/pytorch/pytorch/pull/178398))
- Fix scaled_mm incorrectly validating unsupported swizzle ([#178688](https://github.com/pytorch/pytorch/pull/178688))
- Move rocblas.h include out of anonymous namespace ([#178767](https://github.com/pytorch/pytorch/pull/178767))
- Don't crash for MHA backward with head dim > 192, fall back to CK tile (#178946) ([#178946](https://github.com/pytorch/pytorch/pull/178946))
- Don't fail torch.cuda.device_count() if pynvml is installed ([#175077](https://github.com/pytorch/pytorch/pull/175077))
- Fix hipblaslt GEMMs executing concurrently on multiple HIP streams ([#179053](https://github.com/pytorch/pytorch/pull/179053))
- Windows
  - Fix linker failure caused by missing DLL export directives via native headers ([#179138](https://github.com/pytorch/pytorch/pull/179138))
  - Fix int4mm std::memcpy build error ([#175410](https://github.com/pytorch/pytorch/pull/175410))
  - Fix Windows access violation in MIOpen CTC loss dispatch ([#178284](https://github.com/pytorch/pytorch/pull/178284))
  - Fix Windows DLL linkage for batch norm (`-Winconsistent-dllimport`) ([#179706](https://github.com/pytorch/pytorch/pull/179706))
- TunableOp supports FP64 on hipBLASLt ([#178195](https://github.com/pytorch/pytorch/pull/178195))
- Workaround hipGraph event query errors in NCCL watchdog ([#175377](https://github.com/pytorch/pytorch/pull/175377))
- Fix linker error for aotriton when USE_MEM_EFF_ATTENTION=ON but USE_FLASH_ATTENTION=OFF ([#175079](https://github.com/pytorch/pytorch/pull/175079))
- Fix build_amd.py (hipify) failure when MSLK submodule is missing ([#175180](https://github.com/pytorch/pytorch/pull/175180))
### performance
- Directly access GPU scalars if largeBar is enabled, avoiding D2H copy ([#177023](https://github.com/pytorch/pytorch/pull/177023))
- TopK operator performance improvement via RadixSelect prefetching ([#174897](https://github.com/pytorch/pytorch/pull/174897), [#177149](https://github.com/pytorch/pytorch/pull/177149), [#178188](https://github.com/pytorch/pytorch/pull/178188), [#174837](https://github.com/pytorch/pytorch/pull/174837))
- Improved kernel loop unrolling by leveraging compiler ([#177697](https://github.com/pytorch/pytorch/pull/177697))
- Remove need for expensive fence in normalization kernel ([#175286](https://github.com/pytorch/pytorch/pull/175286))
- Avoid double casting in ReduceLogicKernel ([#176132](https://github.com/pytorch/pytorch/pull/176132))
- In group_gemm, use new kernel for all K equal cases ([#173502](https://github.com/pytorch/pytorch/pull/173502))
- Use BFloat16 native hardware type casting ([#178814](https://github.com/pytorch/pytorch/pull/178814))
- Use optimized tiled kernel for LayerNorm gamma beta backward ([#179019](https://github.com/pytorch/pytorch/pull/179019))
### docs
### devs
### Untopiced
### not user facing
- CI
  - Enable unit tests with theRock nightly ([#176306](https://github.com/pytorch/pytorch/pull/176306), [#175443](https://github.com/pytorch/pytorch/pull/175443), [#175784](https://github.com/pytorch/pytorch/pull/175784), [#179009](https://github.com/pytorch/pytorch/pull/179009), [#179585](https://github.com/pytorch/pytorch/pull/179585), [#174478](https://github.com/pytorch/pytorch/pull/174478))
  - MI200 improvements ([#174116](https://github.com/pytorch/pytorch/pull/174116), [#175179](https://github.com/pytorch/pytorch/pull/175179), [#172977](https://github.com/pytorch/pytorch/pull/172977))
  - Upgrade GCC version to version 13 ([#174451](https://github.com/pytorch/pytorch/pull/174451), [#179504](https://github.com/pytorch/pytorch/pull/179504), [#179841](https://github.com/pytorch/pytorch/pull/179841))
  - Check if rocm_env.sh exists before sourcing ([#175071](https://github.com/pytorch/pytorch/pull/175071))
  - Run reduced test set for Navi31 runners ([#175770](https://github.com/pytorch/pytorch/pull/175770))
  - Hardening, update docker GPU_FLAG to remove network option ([#176612](https://github.com/pytorch/pytorch/pull/176612))
  - Clarify docker and workflow names, add GPU-specific suffix ([#176445](https://github.com/pytorch/pytorch/pull/176445))
  - Upgrade CI image and wheels to ROCm 7.2.1 patch release ([#178407](https://github.com/pytorch/pytorch/pull/178407), [#178402](https://github.com/pytorch/pytorch/pull/178402))
  - Install libtbb-dev in CI image for benchmark workflows ([#179517](https://github.com/pytorch/pytorch/pull/179517))
  - Fix batch_norm decomp test, it was using a negative running_var ([#177665](https://github.com/pytorch/pytorch/pull/177665))
  - TunableOp test fixes ([#178448](https://github.com/pytorch/pytorch/pull/178448), [#177125](https://github.com/pytorch/pytorch/pull/177125))
  - Skip linalg tests when MAGMA is not available ([#177559](https://github.com/pytorch/pytorch/pull/177559), [#178229](https://github.com/pytorch/pytorch/pull/178229))
- CD
  - Missing libraries in wheel bundle ([#178508](https://github.com/pytorch/pytorch/pull/178508), [#179353](https://github.com/pytorch/pytorch/pull/179353))
  - Increase build time for nightly manywheel workflows to 420 (which is standard) ([#179596](https://github.com/pytorch/pytorch/pull/179596))
- OSDC
  - Fix permissions for workflows for OSDC build-osdc job ([#178772](https://github.com/pytorch/pytorch/pull/178772))
  - Fix permissions for workflows for OSDC build-osdc job for Navi31 - 2/N  ([#179040](https://github.com/pytorch/pytorch/pull/179040))
  - Enable ROCm and XPU build on OSDC pull ([#179932](https://github.com/pytorch/pytorch/pull/179932))
### security

