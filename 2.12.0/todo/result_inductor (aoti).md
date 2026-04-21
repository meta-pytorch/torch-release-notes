
# Release Notes worksheet inductor (aoti)

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

## inductor (aoti)
### bc breaking
### deprecation
### new features
### improvements
- [inductor] Batch cubin-to-obj conversion using .incbin assembly ([#177864](https://github.com/pytorch/pytorch/pull/177864))
- [inductor] Batch cubin-to-obj conversion using .incbin assembly ([#177864](https://github.com/pytorch/pytorch/pull/177864))
- [inductor] Parallelize PTX-to-fatbin compilation ([#177904](https://github.com/pytorch/pytorch/pull/177904))
- [MPS] Add nonzero_static implementation ([#179589](https://github.com/pytorch/pytorch/pull/179589))
### bug fixes
- Fix AOTI incorrect loads from bool tensor pointers in user-defined Triton kernels ([#176353](https://github.com/pytorch/pytorch/pull/176353))
- [inductor] Make lazy compile kernel state per-module instead of global ([#178163](https://github.com/pytorch/pytorch/pull/178163))
- [inductor] Fix expression-nesting limit in cpp-wrapper when combo kernel gets too large ([#180217](https://github.com/pytorch/pytorch/pull/180217))
### performance
### docs
### devs
### Untopiced
- [AOTI]: Fix const folding in run_single_threaded ([#174998](https://github.com/pytorch/pytorch/pull/174998))
- [AOTI] Add MXFP4 dtype support to AOTInductor C shim ([#176496](https://github.com/pytorch/pytorch/pull/176496))
- export: add float8_e8m0fnu serde support ([#176270](https://github.com/pytorch/pytorch/pull/176270))
- [AOTI Eager] Fix caching AFG ([#176017](https://github.com/pytorch/pytorch/pull/176017))
- [pytorch] fix parsing of compressed aoti stacks for fused kernels ([#177026](https://github.com/pytorch/pytorch/pull/177026))
- [AOTI Eager] Add dynamic shapes support to AOTIPythonKernelHolder ([#176018](https://github.com/pytorch/pytorch/pull/176018))
- [AOTI Eager] Support multi-return ops in AOTIPythonKernelHolder ([#176019](https://github.com/pytorch/pytorch/pull/176019))
- [4/11][aoti] Add MinimalArrayref V2 descriptor ABI (#179482) ([#179482](https://github.com/pytorch/pytorch/pull/179482))
- Support `torch.uint{32,64}` in `torch.export.save` ([#179434](https://github.com/pytorch/pytorch/pull/179434))
### not user facing
- [inductor] Add _grouped_mm to AOTI fallback ops ([#177307](https://github.com/pytorch/pytorch/pull/177307))
- [inductor] Support cpp-wrapper lazy compile in fbcode (#177502) ([#177502](https://github.com/pytorch/pytorch/pull/177502))
- Use `STD_TORCH_CHECK_MSG` instead of `TORCH_CHECK_MSG` in `torch/csrc/inductor/aoti_torch/c/shim.h` ([#177594](https://github.com/pytorch/pytorch/pull/177594))
- [inductor] Move lazy compile helper to a precompilable C++ header ([#178164](https://github.com/pytorch/pytorch/pull/178164))
- [inductor] Mark lazy compile wrapper functions as noniline ([#178165](https://github.com/pytorch/pytorch/pull/178165))
- [AOTI][XPU] Support lazy Triton kernel compilation for cpp-wrapper on XPU ([#179239](https://github.com/pytorch/pytorch/pull/179239))
### security
