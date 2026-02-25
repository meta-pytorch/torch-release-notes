
# Release Notes worksheet onnx

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

## onnx
### bc breaking
- [ONNX] Remove the fallback option ([#173189](https://github.com/pytorch/pytorch/pull/173189))
- [ONNX] Remove overload matching logic from dispatcher ([#165083](https://github.com/pytorch/pytorch/pull/165083))
### deprecation
### new features
- [ONNX] Exportable module ([#170810](https://github.com/pytorch/pytorch/pull/170810))
- [ONNX] InputObserver to guess the dynamic shapes for export ([#172838](https://github.com/pytorch/pytorch/pull/172838))
- [ONNX] Add a parameter to force the first dimension to be dynamic in InputObserver.infer_dynamic_shapes ([#173533](https://github.com/pytorch/pytorch/pull/173533))
- [ONNX] Implement while_loop ([#162645](https://github.com/pytorch/pytorch/pull/162645))
- [ONNX] Implement while_loop ([#162645](https://github.com/pytorch/pytorch/pull/162645))
- [ONNX] Add invoke_subgraph HOP export support ([#174283](https://github.com/pytorch/pytorch/pull/174283))
- Fix InputObserver.infer_arguments with empty caches ([#174205](https://github.com/pytorch/pytorch/pull/174205))
- [ONNX] Expose ONNXProgram.rename_axes for renaming dims ([#172032](https://github.com/pytorch/pytorch/pull/172032))
### improvements
- [ONNX] Implement torch.sym_sum and torch.sym_ite ([#170263](https://github.com/pytorch/pytorch/pull/170263))
- [ONNX] Raise an error if there are duplicated input/output names ([#173077](https://github.com/pytorch/pytorch/pull/173077))
- [ONNX] Refactor optimize and version conversion logic ([#173185](https://github.com/pytorch/pytorch/pull/173185))
### bug fixes
- [ONNX] Handle complex initializers ([#170231](https://github.com/pytorch/pytorch/pull/170231))
- [ONNX] Fix export of torch.cdist with dynamic axes ([#172758](https://github.com/pytorch/pytorch/pull/172758))
### performance
### docs
- [ONNX] Change warning to debug log for missing annotations ([#172247](https://github.com/pytorch/pytorch/pull/172247))
### devs
### Untopiced
- [Misc][BE] Type more of `torch/_subclasses` ([#171950](https://github.com/pytorch/pytorch/pull/171950))
### not user facing
- [ONNX] Remove unused expecttest files ([#170824](https://github.com/pytorch/pytorch/pull/170824))
- Fix GELU docstring parameter type annotation in ONNX exporter ([#171055](https://github.com/pytorch/pytorch/pull/171055))
- Fix missing closing bracket in ONNX attention docstring ([#171056](https://github.com/pytorch/pytorch/pull/171056))
- Better error handling in torch/csrc/jit/passes by replacing std::runtime_error with TORCH_CHECK in passes [part 2] ([#165736](https://github.com/pytorch/pytorch/pull/165736))
- Submodule upgrade flash-attn version to 2.8.3 ([#170703](https://github.com/pytorch/pytorch/pull/170703))
- [ONNX] Remove outdated comment in ExportedProgram conversion ([#171740](https://github.com/pytorch/pytorch/pull/171740))
- [ONNX][ez] Change import of onnxscript.ir to onnx_ir ([#172036](https://github.com/pytorch/pytorch/pull/172036))
- [ONNX] Update onnx-ir version and imports ([#173078](https://github.com/pytorch/pytorch/pull/173078))
- [ONNX] Update onnx-ir version and imports ([#173078](https://github.com/pytorch/pytorch/pull/173078))
- [ONNX] Update onnx-ir version and imports ([#173078](https://github.com/pytorch/pytorch/pull/173078))
- Remove assert in functorch and start onnx ([#173928](https://github.com/pytorch/pytorch/pull/173928))
- Finish onnx and start testing ([#173929](https://github.com/pytorch/pytorch/pull/173929))
- [ONNX] Clean up type utils ([#174393](https://github.com/pytorch/pytorch/pull/174393))
### security
