
# Release Notes worksheet quantization

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

## quantization
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- [Quantization] Fix incorrect dilation check in MaxPool3d (avoid negative values) ([#171790](https://github.com/pytorch/pytorch/pull/171790))
- [Fix] Fix incorrect values displayed in error messages and log strings ([#171868](https://github.com/pytorch/pytorch/pull/171868))
- Add validation for out_channels in quantized ConvTranspose modules ([#171628](https://github.com/pytorch/pytorch/pull/171628))
### performance
### docs
### devs
### Untopiced
- Apply more clang-tidy fixes ([#169794](https://github.com/pytorch/pytorch/pull/169794))
- Update tensor_attributes.rst with additional float4 information ([#170448](https://github.com/pytorch/pytorch/pull/170448))
- [HN] amend regression triggering unnecessary string creations ([#169465](https://github.com/pytorch/pytorch/pull/169465))
- Delete pt2e flow from pytorch/pytorch since it's migrated to torchao ([#169151](https://github.com/pytorch/pytorch/pull/169151))
- Fix local lint error ([#170945](https://github.com/pytorch/pytorch/pull/170945))
- emscripten support ([#171464](https://github.com/pytorch/pytorch/pull/171464))
- Cleanup pyrefly ignores 1 ([#171632](https://github.com/pytorch/pytorch/pull/171632))
- Fix typos in comments and variable names ([#171872](https://github.com/pytorch/pytorch/pull/171872))
- Remove assert in ao/pruning and testing internal ([#172096](https://github.com/pytorch/pytorch/pull/172096))
- Add _disable_torch_fn_metadata_mode option to make_fx and aot_export_joint_with_descriptors ([#172087](https://github.com/pytorch/pytorch/pull/172087))
- fixes crash for empty dims in quantized tensors ([#163487](https://github.com/pytorch/pytorch/pull/163487))
- Use expm1 for computing ELU ([#173968](https://github.com/pytorch/pytorch/pull/173968))
- make data_ptrs const or mutable in some native functions ([#174127](https://github.com/pytorch/pytorch/pull/174127))
### not user facing
- Fix clang-tidy warnings on c10/xpu files ([#169231](https://github.com/pytorch/pytorch/pull/169231))
- Checking if the input is finite before calculation in lowering of pow func ([#167723](https://github.com/pytorch/pytorch/pull/167723))
- hub/package/profiler/quant assert removal ([#170225](https://github.com/pytorch/pytorch/pull/170225))
- more ao and nn assert removal ([#170576](https://github.com/pytorch/pytorch/pull/170576))
- Remove unused test conditions ([#170767](https://github.com/pytorch/pytorch/pull/170767))
- Skip CUDA device in test_qat_embeddingbag_linear quantization test ([#170917](https://github.com/pytorch/pytorch/pull/170917))
- [ROCm] Enable tests that now pass on MI300X ([#171569](https://github.com/pytorch/pytorch/pull/171569))
- Return FakeTensorMode from AOTState as well. ([#171882](https://github.com/pytorch/pytorch/pull/171882))
- [BE][Ez]: Fix TypeAliasType backports with typing_extensions ([#171899](https://github.com/pytorch/pytorch/pull/171899))
- Upgrade usort ([#172262](https://github.com/pytorch/pytorch/pull/172262))
- [ROCm] Enable 3 stale-skipped tests ([#171033](https://github.com/pytorch/pytorch/pull/171033))
- [Quant][X86] Use onednn primitive for fp8 qconv ([#172551](https://github.com/pytorch/pytorch/pull/172551))
- [Quant][CPU] Fix context cache for fp8 qlinear ([#172553](https://github.com/pytorch/pytorch/pull/172553))
- Set disable_functionalization in prepare_aot_module_simplified ([#173118](https://github.com/pytorch/pytorch/pull/173118))
- Finish benchmark and start tests ([#174215](https://github.com/pytorch/pytorch/pull/174215))
- More test migration ([#174216](https://github.com/pytorch/pytorch/pull/174216))
- More test assert migration ([#174218](https://github.com/pytorch/pytorch/pull/174218))
- Continue removing assert in test and flip config to allowlist ([#174235](https://github.com/pytorch/pytorch/pull/174235))
- finish test numpy assert removal ([#174254](https://github.com/pytorch/pytorch/pull/174254))
### security
