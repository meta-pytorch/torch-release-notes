
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

- `fallback=False` is now the default in `torch.onnx.export` ([#162726](https://github.com/pytorch/pytorch/pull/162726))
    - The exporter now uses the `dynamo=True` option without fallback. This is the recommended way to use the ONNX exporter. To preserve 2.9 behavior, manually set `fallback=True` in the `torch.onnx.export` call.
### deprecation

- The `dynamic_axes` option in `torch.onnx.export` is deprecated ([#165769](https://github.com/pytorch/pytorch/pull/165769))
    - Users should supply the `dynamic_shapes` argument instead. See https://docs.pytorch.org/docs/stable/export.html#expressing-dynamism for more documentation.

### new features

- A new testing module `torch.onnx.testing` with a testing utility `assert_onnx_program` ([#162495](https://github.com/pytorch/pytorch/pull/162495))

### improvements

- Improved graph capture logic to preserve dynamic shapes and improve conversion success rate
    - Cover all FX passes into backed size oblivious ([#166151](https://github.com/pytorch/pytorch/pull/166151))
    - Set prefer_deferred_runtime_asserts_over_guards to True ([#165820](https://github.com/pytorch/pytorch/pull/165820))
- Various warning and error messages improvements ([#162819](https://github.com/pytorch/pytorch/pull/162819), [#163074](https://github.com/pytorch/pytorch/pull/163074), [#166412](https://github.com/pytorch/pytorch/pull/166412), [#166558](https://github.com/pytorch/pytorch/pull/166558), [#166692](https://github.com/pytorch/pytorch/pull/166692))
- Improved operator translation logic
    - Update weight tensor initialization in RMSNormalization ([#166550](https://github.com/pytorch/pytorch/pull/166550))
    - Support enable_gqa when dropout is non-zero ([#162771](https://github.com/pytorch/pytorch/pull/162771))
- Implement `tofile()` in ONNX IR tensors for more efficient ONNX model serialization ([#165195](https://github.com/pytorch/pytorch/pull/165195))

### bug fixes

- Native ONNX ops (`torch.onnx.ops`)
    - Fix rotary_embedding_23 implementation ([#162865](https://github.com/pytorch/pytorch/pull/162865))
    - Create fake implementations for onnx ops; fix boolean mask in attention ([#165780](https://github.com/pytorch/pytorch/pull/165780))
- Fix onnx export on big endian machines ([#167816](https://github.com/pytorch/pytorch/pull/167816))
### performance
### docs
- Update export docstring ([#162622](https://github.com/pytorch/pytorch/pull/162622))
- Fix incorrect attention example in ONNX exporter docstring ([#167646](https://github.com/pytorch/pytorch/pull/167646))
### devs
### Untopiced
### not user facing
- fix typo: summit -> submit ([#162587](https://github.com/pytorch/pytorch/pull/162587))
- remove allow-untyped-defs from ./torch/onnx/_internal/torchscript_exporter/_globals.py ([#163472](https://github.com/pytorch/pytorch/pull/163472))
- Add a test to backed_size_oblivious patch in onnx ([#166196](https://github.com/pytorch/pytorch/pull/166196))
- Add some import ignores to onnx ([#163133](https://github.com/pytorch/pytorch/pull/163133))
- Ignore pyrefly errors in torchlib ([#166588](https://github.com/pytorch/pytorch/pull/166588))
### security
