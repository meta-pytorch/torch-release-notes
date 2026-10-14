
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
### deprecation
### new features
### improvements
### bug fixes
- Fix `torch.onnx.export(dynamo=True)` hardcoding LSTM/GRU output length under dynamic shapes ([#193192](https://github.com/pytorch/pytorch/pull/193192))
### performance
### docs
### devs
### Untopiced
### not user facing
- [RAWTHROW][11] torch/csrc/jit passes and runtime: 48 conversions ([#195858](https://github.com/pytorch/pytorch/pull/195858))
- [Testcase Refactoring] Add proper hw_classification to test_core ([#193528](https://github.com/pytorch/pytorch/pull/193528))
- [Testcase Refactoring] Add proper hw_classification to test_dynamic_shapes.py. ([#193529](https://github.com/pytorch/pytorch/pull/193529))
- [Testcase Refactoring] Add proper hw_classification to test_registration ([#194330](https://github.com/pytorch/pytorch/pull/194330))
- [Testcase Refactoring] Add proper hw_classification to test_capture_strategies ([#193526](https://github.com/pytorch/pytorch/pull/193526))
- [Testcase Refactoring] Add proper hw_classification to test_onnxscript_runtime ([#194342](https://github.com/pytorch/pytorch/pull/194342))
- [Testcase Refactoring] Add proper hw_classification to test_building ([#193521](https://github.com/pytorch/pytorch/pull/193521))
- [Testcase Refactoring] Add proper hw_classification to test_hf_models_e2e ([#193532](https://github.com/pytorch/pytorch/pull/193532))
- [Testcase Refactoring] Add proper hw_classification to test_pytorch_onnx_onnxruntime ([#195118](https://github.com/pytorch/pytorch/pull/195118))
- [Testcase Refactoring] Add proper hw_classification to test_ops ([#193309](https://github.com/pytorch/pytorch/pull/193309))
- [Testcase Refactoring] Add proper hw_classification to test_api ([#193253](https://github.com/pytorch/pytorch/pull/193253))
- [Testcase Refactoring] Add proper hw_classification to test_symbolic_helper. ([#195122](https://github.com/pytorch/pytorch/pull/195122))
- [Testcase Refactoring] Add proper hw_classification to test_ir_passes ([#193541](https://github.com/pytorch/pytorch/pull/193541))
- [Testcase Refactoring] Add proper hw_classification to test_small_models_e2e ([#193543](https://github.com/pytorch/pytorch/pull/193543))
- [Testcase Refactoring] Add proper hw_classification to test_pytorch_onnx_shape_inference. ([#195120](https://github.com/pytorch/pytorch/pull/195120))
- [Testcase Refactoring] Add proper hw_classification to test_models_quantized_onnxruntime ([#194339](https://github.com/pytorch/pytorch/pull/194339))
- [Testcase Refactoring] Add proper hw_classification to test_lazy_import ([#194337](https://github.com/pytorch/pytorch/pull/194337))
- [Testcase Refactoring] Add proper hw_classification to test_verification ([#193547](https://github.com/pytorch/pytorch/pull/193547))
- [Testcase Refactoring] Add proper hw_classification to test_tensors ([#193544](https://github.com/pytorch/pytorch/pull/193544))
- [Testcase Refactoring] Add proper hw_classification to test_autograd_funs ([#194333](https://github.com/pytorch/pytorch/pull/194333))
- [Testcase Refactoring] Add proper hw_classification to test_fx_type__promotion ([#193552](https://github.com/pytorch/pytorch/pull/193552))
- [Testcase Refactoring] Add proper hw_classification to test_exportable_module.py. ([#193530](https://github.com/pytorch/pytorch/pull/193530))
- [Testcase Refactoring] Add proper hw_classification to test_custom_ops ([#194336](https://github.com/pytorch/pytorch/pull/194336))
- [Testcase Refactoring] Add proper hw_classification to test_input_observer ([#193538](https://github.com/pytorch/pytorch/pull/193538))
- [Testcase Refactoring] Add proper hw_classification to test_models_onnxruntime ([#194338](https://github.com/pytorch/pytorch/pull/194338))
- [Testcase Refactoring] Add proper hw_classification to test_onnxscript_no_runtime ([#194341](https://github.com/pytorch/pytorch/pull/194341))
- [Testcase Refactoring] Add proper hw_classification to test_onnx_opset ([#194340](https://github.com/pytorch/pytorch/pull/194340))
- [Testcase Refactoring] Add proper hw_classification to test_onnx_program.py ([#193542](https://github.com/pytorch/pytorch/pull/193542))
### security
