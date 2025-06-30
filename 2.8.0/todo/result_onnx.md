
# Release Notes worksheet onnx

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

## onnx
### bc breaking
- [ONNX] Clean up legacy dynamo export code ([#149745](https://github.com/pytorch/pytorch/pull/149745))
- [ONNX] Update default opset to 18 ([#156023](https://github.com/pytorch/pytorch/pull/156023))
### deprecation
### new features
- [ONNX] Create onnx_symbolic ([#148905](https://github.com/pytorch/pytorch/pull/148905))
- [ONNX] Add draft_export as a strategy ([#147529](https://github.com/pytorch/pytorch/pull/147529))
- [ONNX] Set is_in_onnx_export for dynamo=True ([#149678](https://github.com/pytorch/pytorch/pull/149678))
- [ONNX] Supporting different opset versions for torchlib registry ([#149901](https://github.com/pytorch/pytorch/pull/149901))
- [ONNX] Support float4 ([#151069](https://github.com/pytorch/pytorch/pull/151069))
- [ONNX] Create support for rotary embeddings ([#154745](https://github.com/pytorch/pytorch/pull/154745))
- [ONNX] Support 0/1 on dynamic dimension ([#155717](https://github.com/pytorch/pytorch/pull/155717))
- [ONNX] Implements converter for higher order ops scan ([#154513](https://github.com/pytorch/pytorch/pull/154513))
- Fix num_heads inference in ONNX Attention-23 exporter ([#156367](https://github.com/pytorch/pytorch/pull/156367))
- [ONNX] Implement Attention-23 ([#156431](https://github.com/pytorch/pytorch/pull/156431))
### improvements
- [ONNX] Annotate None inputs in symbolic ops ([#150038](https://github.com/pytorch/pytorch/pull/150038))
- [ONNX] Add asdict method to VerificationInfo class ([#151024](https://github.com/pytorch/pytorch/pull/151024))
- [ONNX] Support running bfloat16 models with ONNX Runtime ([#149646](https://github.com/pytorch/pytorch/pull/149646))
- [ONNX][Eazy] Update onnx program doc formatting and improve robustness ([#151623](https://github.com/pytorch/pytorch/pull/151623))
- [ONNX] Add group_norm support from opset 21 ([#152138](https://github.com/pytorch/pytorch/pull/152138))
- [ONNX] Implement sym_not ([#152111](https://github.com/pytorch/pytorch/pull/152111))
- [ONNX] add converters for sym_min, sym_max ([#152196](https://github.com/pytorch/pytorch/pull/152196))
- [ONNX] dynamic_shapes uses DYNAMIC ([#153065](https://github.com/pytorch/pytorch/pull/153065))
- [ONNX] Allow exporter to export SDPA to Attention onnx operator ([#154596](https://github.com/pytorch/pytorch/pull/154596))
- [ONNX] Set the name of the producing node using the value name ([#155413](https://github.com/pytorch/pytorch/pull/155413))
- [ONNX] Fix how shapes are computed for float4 ([#156353](https://github.com/pytorch/pytorch/pull/156353))
### bug fixes
- [ONNX] Fix bfloat16 support in onnx_program callable ([#151121](https://github.com/pytorch/pytorch/pull/151121))
- [ONNX] Produce correct dtypes for bf16/f8 in IR TorchTensor ([#151259](https://github.com/pytorch/pytorch/pull/151259))
### performance
### docs
- [ONNX] Update types in VerificationInfo ([#149377](https://github.com/pytorch/pytorch/pull/149377))
- [ONNX] Improve docstring of onnx symbolic ops ([#149668](https://github.com/pytorch/pytorch/pull/149668))
- [ONNX] Note on attention op symbolic function ([#156441](https://github.com/pytorch/pytorch/pull/156441))
### devs
### Untopiced
- [export] refactor DimHints for type errors ([#149424](https://github.com/pytorch/pytorch/pull/149424))
- [export] refactor _Dim into Dim ([#149891](https://github.com/pytorch/pytorch/pull/149891))
- [ONNX] Add a comment for handling bf16/fp8 tensor to numpy conversion ([#151371](https://github.com/pytorch/pytorch/pull/151371))
- [ONNX] Delete JitTraceConvertStrategy ([#152556](https://github.com/pytorch/pytorch/pull/152556))
- [ONNX] Suggest users setting dynamo=True when exporting ([#152478](https://github.com/pytorch/pytorch/pull/152478))
- [ONNX] Support sym_float ([#153200](https://github.com/pytorch/pytorch/pull/153200))
- [submodule] Update ONNX to 1.18 ([#152200](https://github.com/pytorch/pytorch/pull/152200))
- Convert to markdown onnx rst ([#155228](https://github.com/pytorch/pytorch/pull/155228))
- [ONNX] Change deprecation message from 2.8 to 2.9 ([#155580](https://github.com/pytorch/pytorch/pull/155580))
- Typo fixes for "overridden" in comments and function names ([#155944](https://github.com/pytorch/pytorch/pull/155944))
- [ONNX] Preserve all legacy exporter params in fallback ([#156659](https://github.com/pytorch/pytorch/pull/156659))
### not user facing
- [ONNX] Clean up the diagnostics module ([#149864](https://github.com/pytorch/pytorch/pull/149864))
- [ONNX] Clean up the diagnostics module ([#149864](https://github.com/pytorch/pytorch/pull/149864))
- [ONNX] Add test for decomp_table update ([#153671](https://github.com/pytorch/pytorch/pull/153671))
- Add __main__ guards to tests ([#154716](https://github.com/pytorch/pytorch/pull/154716))
- Convert to .md: onnx_verification.rst, onnx.rst, package.rst, ([#155556](https://github.com/pytorch/pytorch/pull/155556))
- Delete tools/onnx/update_default_opset_version.py ([#156055](https://github.com/pytorch/pytorch/pull/156055))
- Add ONNX dynamo metadata documentation ([#155816](https://github.com/pytorch/pytorch/pull/155816))
- [BE] fix typos in docs/ ([#156080](https://github.com/pytorch/pytorch/pull/156080))
### security
