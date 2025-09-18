
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
- Default to `dynamo=True` ([#159646](https://github.com/pytorch/pytorch/pull/159646), [#162726](https://github.com/pytorch/pytorch/pull/162726))

  The ONNX exporter now uses the newer `torch.export.export` pipeline by default (`dynamo=True`). Previously, calling `torch.onnx.export(...)` without arguments used the legacy TorchScript exporter. This change improves graph fidelity and future-proofs exports, but may surface graph capture errors that were previously masked or handled differently.
  
  Version 2.8
  
  ```python
  # API calls the legacy exporter with dynamo=False
  torch.onnx.export(...)
  ```
  
  Version 2.9
  
  ```python
  # To preserve the original behavior
  torch.onnx.export(..., dynamo=False)
  
  # Export onnx model through torch.export.export
  torch.onnx.export(...)
  ```
  
  Recommendation: first try the new default; only fall back if you hit blocking issues and report them upstream. Long term, fix the root cause instead of relying on fallback or TorchScript exporter.

- Set default opset to 20 ([#158802](https://github.com/pytorch/pytorch/pull/158802))

  Opset 20 enables newer operator definitions. If your tooling or downstream runtime only supports opset 18, pin it explicitly. For the latest ONNX operators, you can experiment with opset 23.

  Version 2.8
  
  ```py
  # opset_version=18
  torch.onnx.export(...)
  ```
  
  Version 2.9
  
  ```py
  # To preserve the original behavior
  torch.onnx.export(..., opset_version=18)
  
  # New: opset_version=20
  torch.onnx.export(...)

  # Use the latest supported opset: opset_version=23
  torch.onnx.export(..., opset_version=23)
  ```

- Drop draft_export in exporter API ([#161454](https://github.com/pytorch/pytorch/pull/161454), [#162225](https://github.com/pytorch/pytorch/pull/162225))

  Clearer behavior and faster failures by removing implicit draft tracing from the default exporter path,
  The expensive `torch.export.draft_export` diagnostic path is no longer auto-invoked (which could take hours on large models). You can still opt in for deep diagnostics:
  
  Version 2.8,
  
  ```bash
  # If both torch.export.export(..., strict=False) and 
  # torch.export.export(..., strict=True) fail to capture
  # the model graph, torch.export.draft_export(...) will be triggered,
  # and uses real tensor to trace/export the model.
  # 
  # Inside export_to_onnx.py:
  #  ... torch.onnx.export(..., dynamo=True)
  python export_to_onnx.py
  ```
  
  Version 2.9,
  
  ```bash
  # To trigger torch.export.draft_export once
  # torch.export.export strict=False/True both
  # fail:
  
  TORCH_ONNX_ENABLE_DRAFT_EXPORT=True python export_to_onnx.py
  ```

- `torch.onnx.dynamo_export` and the `onnxrt` torch compile backend are removed ([#158130](https://github.com/pytorch/pytorch/pull/158130), [#158258](https://github.com/pytorch/pytorch/pull/158258))

  `torch.onnx.dynamo_export` is removed. Please use `torch.onnx.export` instead. 
  The experimental ONNX Runtime compile backend (`torch.compile(backend="onnxrt")`) is no longer supported.  

- `torch.onnx.enable_fake_mode` is removed ([#161222](https://github.com/pytorch/pytorch/pull/161222))

  The `dynamo=True` mode uses `FakeTensor`s by default, which is memory efficient.

- Some public facing utility APIs for the TorchScript based exporter is now private ([#161323](https://github.com/pytorch/pytorch/pull/161323))
- `torch.onnx.symbolic_caffe2` is removed ([#157102](https://github.com/pytorch/pytorch/pull/157102))

### deprecation
### new features
- RMS Norm support in opset 23 ([#159377](https://github.com/pytorch/pytorch/pull/159377))
### improvements
- Support symbolic arguments in onnx exporter ([#157734](https://github.com/pytorch/pytorch/pull/157734))
- Fix torch.tensor warning in ONNX symbolic_opset10 export  ([#158835](https://github.com/pytorch/pytorch/pull/158835))
### bug fixes
- Make onnx export SDPA match aten behavior ([#159973](https://github.com/pytorch/pytorch/pull/159973))
- Fix rotary_embedding_23 implementation ([#162865](https://github.com/pytorch/pytorch/pull/162865))
- Fix export behavior when model has None as output ([#160200](https://github.com/pytorch/pytorch/pull/160200))
- Fix lower opset version support in dynamo=True ([#161056](https://github.com/pytorch/pytorch/pull/161056))
- Fix index_put_ usage ([#161263](https://github.com/pytorch/pytorch/pull/161263))
### performance
### docs
- Update export docstring ([#162622](https://github.com/pytorch/pytorch/pull/162622))
- Delete deprecated tutorial page link ([#157310](https://github.com/pytorch/pytorch/pull/157310))
- Filter out torchscript sentences ([#158850](https://github.com/pytorch/pytorch/pull/158850))
- Fix doc typo for symbolic_multi_out ([#160702](https://github.com/pytorch/pytorch/pull/160702))
- onnx.md to simplify deprecated entities ([#159312](https://github.com/pytorch/pytorch/pull/159312))
### devs
### Untopiced
### not user facing
- Remove legacy io_adapter ([#158255](https://github.com/pytorch/pytorch/pull/158255))
- Remove legacy graph passes ([#158256](https://github.com/pytorch/pytorch/pull/158256))
- Remove legacy modularization ([#158257](https://github.com/pytorch/pytorch/pull/158257))
- Remove legacy Dort tests ([#158294](https://github.com/pytorch/pytorch/pull/158294))
- Remove legacy dynamo graph extractor ([#158262](https://github.com/pytorch/pytorch/pull/158262))
- Remove fx_onnx_interpreter.py ([#158282](https://github.com/pytorch/pytorch/pull/158282))
- Remove legacy registration and dispatcher ([#158283](https://github.com/pytorch/pytorch/pull/158283))
- Remove numpy dependency from onnx ([#159177](https://github.com/pytorch/pytorch/pull/159177))
- Remove unused logic from internal verification module ([#161449](https://github.com/pytorch/pytorch/pull/161449))
- Remove private members from torch.onnx ([#161546](https://github.com/pytorch/pytorch/pull/161546))
- Improve typing of ONNX decorators with ParamSpec ([#162332](https://github.com/pytorch/pytorch/pull/162332))
- Tidy torch/csrc/jit/passes/onnx code ([#160262](https://github.com/pytorch/pytorch/pull/160262))
- Remove unused _onnx_supported_ops ([#161322](https://github.com/pytorch/pytorch/pull/161322))

### security
