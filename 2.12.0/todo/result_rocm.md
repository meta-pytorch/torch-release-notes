
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
### improvements
### bug fixes
- [ROCm] Fix void pointer arithmetic in CUDACachingAllocator for HIP build (c67b40befbb)
- [ROCm] Fix SDPA build error when USE_FLASH_ATTENTION=0 USE_MEM_EFF_ATTENTION=1 ([#177552](https://github.com/pytorch/pytorch/pull/177552))
### performance
### docs
### devs
### Untopiced
- [ROCm] Detect and compile for user architecture only ([#168998](https://github.com/pytorch/pytorch/pull/168998))
- [ROCm] Enable hipSPARSELt for ROCm >= 7.12 ([#170852](https://github.com/pytorch/pytorch/pull/170852))
- [ROCm] Enable hipSPARSELt UTs ([#178285](https://github.com/pytorch/pytorch/pull/178285))
- [ROCm] Fix _get_amdsmi_device_index#160468 ([#178398](https://github.com/pytorch/pytorch/pull/178398))
- [ROCm] Directly access scalars if largeBar is enabled ([#177023](https://github.com/pytorch/pytorch/pull/177023))
- [ROCm] Fix wrong ROCM code execution in in `ScaledBlas.cpp` at `check_swizzle_lengths()` ([#178688](https://github.com/pytorch/pytorch/pull/178688))
- [ROCm] Move rocblas.h include out of anonymous namespace ([#178767](https://github.com/pytorch/pytorch/pull/178767))
- [MHA Backward] Disable ASM v3 backward for head dim > 192 to fall back to CK tile (#178946) ([#178946](https://github.com/pytorch/pytorch/pull/178946))
- [ROCm] Add separate _HAS_AMDSMI flag for amdsmi availability check ([#175077](https://github.com/pytorch/pytorch/pull/175077))
- [ROCm] Use per-stream hipblaslt handles ([#179053](https://github.com/pytorch/pytorch/pull/179053))
### not user facing
- [ROCm] add multiarch path to CMAKE_MODULE_PATH ([#175349](https://github.com/pytorch/pytorch/pull/175349))
- [Windows][ROCm] Fix missing native header includes causing DLL export… ([#179138](https://github.com/pytorch/pytorch/pull/179138))
### security
