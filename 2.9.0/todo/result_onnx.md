
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
- [ONNX] Delete symbolic caffe2 ([#157102](https://github.com/pytorch/pytorch/pull/157102))
- [ONNX] Delete torch.onnx.dynamo_export ([#158130](https://github.com/pytorch/pytorch/pull/158130))
- [ONNX] Remove legacy Dort ([#158258](https://github.com/pytorch/pytorch/pull/158258))
- [ONNX] Set default opset to 20 ([#158802](https://github.com/pytorch/pytorch/pull/158802))
- [ONNX] Default to dynamo export ([#159646](https://github.com/pytorch/pytorch/pull/159646))
- [ONNX] Drop draft_export in exporter API ([#161454](https://github.com/pytorch/pytorch/pull/161454))
- [ONNX] Refactor torchscript based exporter ([#161323](https://github.com/pytorch/pytorch/pull/161323))
- [ONNX] Default to dynamo export ([#159646](https://github.com/pytorch/pytorch/pull/159646))
- [ONNX] Hide draft export under a flag ([#162225](https://github.com/pytorch/pytorch/pull/162225))
### deprecation
### new features
### improvements
- Fix torch.tensor warning in ONNX symbolic_opset10 export  ([#158835](https://github.com/pytorch/pytorch/pull/158835))
- [ONNX] RMS Norm ([#159377](https://github.com/pytorch/pytorch/pull/159377))
### bug fixes
- [ONNX] Support symbolic arguments in onnx exporter ([#157734](https://github.com/pytorch/pytorch/pull/157734))
- Make onnx export SDPA match aten behavior ([#159973](https://github.com/pytorch/pytorch/pull/159973))
- [ONNX] Fix the export of the model having none as output ([#160200](https://github.com/pytorch/pytorch/pull/160200))
- [ONNX] Fix lower opset version support in dynamo=True ([#161056](https://github.com/pytorch/pytorch/pull/161056))
### performance
### docs
- [ONNX] Delete deprecated tutorial page link ([#157310](https://github.com/pytorch/pytorch/pull/157310))
- [ONNX] Filter out torchscript sentences ([#158850](https://github.com/pytorch/pytorch/pull/158850))
- [ONNX] Fix doc typo for symbolic_multi_out ([#160702](https://github.com/pytorch/pytorch/pull/160702))
- [ONNX] Remove enable_fake_mode and exporter_legacy ([#161222](https://github.com/pytorch/pytorch/pull/161222))
### devs
### Untopiced
- Tidy  torch/csrc/jit/passes/onnx  code ([#160262](https://github.com/pytorch/pytorch/pull/160262))
- [ONNX] Remove unused _onnx_supported_ops ([#161322](https://github.com/pytorch/pytorch/pull/161322))
- [ONNX] Fix index_put_ usage ([#161263](https://github.com/pytorch/pytorch/pull/161263))
### not user facing
- [ONNX] Remove legacy io_adapter ([#158255](https://github.com/pytorch/pytorch/pull/158255))
- [ONNX] Remove legacy graph passes ([#158256](https://github.com/pytorch/pytorch/pull/158256))
- [ONNX] Remove legacy modularization ([#158257](https://github.com/pytorch/pytorch/pull/158257))
- [ONNX] Remove legacy Dort tests ([#158294](https://github.com/pytorch/pytorch/pull/158294))
- [ONNX] Remove legacy dynamo graph extractor ([#158262](https://github.com/pytorch/pytorch/pull/158262))
- [ONNX] Remove fx_onnx_interpreter.py ([#158282](https://github.com/pytorch/pytorch/pull/158282))
- [ONNX] Remove legacy registration and dispatcher ([#158283](https://github.com/pytorch/pytorch/pull/158283))
- Dont't GC as often when collecting cudagraphs ([#158193](https://github.com/pytorch/pytorch/pull/158193))
- Remove numpy dependency from onnx ([#159177](https://github.com/pytorch/pytorch/pull/159177))
- [ONNX] onnx.md to simplify deprecated entities ([#159312](https://github.com/pytorch/pytorch/pull/159312))
- typing inductor and placeholder backends ([#160366](https://github.com/pytorch/pytorch/pull/160366))
- [ONNX] Remove unused logic from internal verification module ([#161449](https://github.com/pytorch/pytorch/pull/161449))
- [ONNX] Remove private members from torch.onnx ([#161546](https://github.com/pytorch/pytorch/pull/161546))
- Improve typing of ONNX decorators with ParamSpec ([#162332](https://github.com/pytorch/pytorch/pull/162332))
### security
