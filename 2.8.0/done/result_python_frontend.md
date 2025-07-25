
# Release Notes worksheet python_frontend

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

## python_frontend
### bc breaking
- **Calling an op with an input dtype that is unsupported now raise `NotImplementedError` instead of `RuntimeError`. Please update exception handling logic to reflect this.** ([#155470](https://github.com/pytorch/pytorch/pull/155470))

  In 2.7.0
  ```
  try:
      torch.nn.Hardshrink()(torch.randint(0, 5, (10,)))
  except RuntimeError:
      ...
  ```

  In 2.8.0
  ```
  try:
      torch.nn.Hardshrink()(torch.randint(0, 5, (10,)))
  except NotImplementedError:
      ...
  ```
### deprecation
### new features
- Add Generalized Pareto Distribution (GPD) ([#135968](https://github.com/pytorch/pytorch/pull/135968))
### improvements
- Add a warning when a tensor with `requires_grad=True` is converted to a scalar ([#143261](https://github.com/pytorch/pytorch/pull/143261))
- Move warning from item to specific number conversions ([#152709](https://github.com/pytorch/pytorch/pull/152709))
- Avoid triggering ignored `requires_grad` warning during tensor string formatting ([#152686](https://github.com/pytorch/pytorch/pull/152686))
- Introduce `torch.AcceleratorError` ([#152023](https://github.com/pytorch/pytorch/pull/152023))
- Implement `Size.__radd__` ([#152554](https://github.com/pytorch/pytorch/pull/152554))
- Update `get_default_device()` to also respect `torch.device` context manager ([#148621](https://github.com/pytorch/pytorch/pull/148621))
- Delegate `torch.accelerator.device_count` to `torch.xxx.device_count` for multi-process usage ([#149924](https://github.com/pytorch/pytorch/pull/149924))
### bug fixes
- Gracefully handle missing pip installation in `collect_env.py` ([#151607](https://github.com/pytorch/pytorch/pull/151607))
- Fix segfault during NumPy string tensor conversion ([#155364](https://github.com/pytorch/pytorch/pull/155364))
- Add checks for empty tensor list ([#155383](https://github.com/pytorch/pytorch/pull/155383))
- Fix sample validation for `MixtureSameFamily` distribution ([#151317](https://github.com/pytorch/pytorch/pull/151317))
- Fix bug where creating a second `Wishart` or `Uniform` distribution modifies constraints on the first ([#154361](https://github.com/pytorch/pytorch/pull/154361))
- Fix to properly export `torch::utils::tensor_to_numpy` symbol ([#154178](https://github.com/pytorch/pytorch/pull/154178))
- Fix `torch.[con]cat[enate]` to raise `ValueError` instead of crashing on empty inputs ([#155460](https://github.com/pytorch/pytorch/pull/155460))
### performance
- Optimize SVE embedding performance ([#150176](https://github.com/pytorch/pytorch/pull/150176))
- `torch.tensordot`: performance improvements when contracting to a scalar. ([#145936](https://github.com/pytorch/pytorch/pull/145936))
### docs
- Make `torch.Library`'s `kind` have no default value to be consistent with the code ([#149390](https://github.com/pytorch/pytorch/pull/149390))
- Add 32-bit complex to the list of dtypes ([#144590](https://github.com/pytorch/pytorch/pull/144590))
- Clarify behavior when integer dtype is used with requires_grad=True in `tensor.to()` ([#150913](https://github.com/pytorch/pytorch/pull/150913))
- Optimize `cdist` param description ([#151178](https://github.com/pytorch/pytorch/pull/151178))
- Update serialization docs ([#153631](https://github.com/pytorch/pytorch/pull/153631))
- Render `Example:` and not `Example::` in docs ([#153978](https://github.com/pytorch/pytorch/pull/153978))
- Add docstring indicating undefined behavior for converting inf to int ([#154781](https://github.com/pytorch/pytorch/pull/154781))
- Update `as_strided()` docs ([#149146](https://github.com/pytorch/pytorch/pull/149146))
- Fix `keepdim` param optional description ([#151197](https://github.com/pytorch/pytorch/pull/151197))
- Clarify that x and dx are mutually exclusive in `torch.trapezoid` docs ([#151190](https://github.com/pytorch/pytorch/pull/151190))
- Document `out_dtype` arg for torch GEMM operations ([#151704](https://github.com/pytorch/pytorch/pull/151704))
- Fix the basic description of `torch.min()`, `torch.max()`, `torch.all()`, and `torch.any()` ([#152658](https://github.com/pytorch/pytorch/pull/152658))
- Add `torch.triu_indices`, `torch.tril_indices` dtype description ([#150749](https://github.com/pytorch/pytorch/pull/150749))
- Optimize `torch.equal` description ([#149618](https://github.com/pytorch/pytorch/pull/149618))
### devs
### Untopiced
### not user facing
- Add `Any` return annotation to `__getattr__` methods that return a union of types. ([#150204](https://github.com/pytorch/pytorch/pull/150204))
- Use variadic length tuple for `torch.masked.DimOrDims` ([#149870](https://github.com/pytorch/pytorch/pull/149870))
- Type hints for distributions/utils ([#154712](https://github.com/pytorch/pytorch/pull/154712))
- typing: allow integer in bitwise operations ([#155704](https://github.com/pytorch/pytorch/pull/155704))
- [typing] Add type hints to `__init__` methods in `torch.distributions`. ([#144197](https://github.com/pytorch/pytorch/pull/144197))
- [Testing] Add copysign from scalar regression test ([#152997](https://github.com/pytorch/pytorch/pull/152997))
- Migrate dtype_abbrs into one location ([#152229](https://github.com/pytorch/pytorch/pull/152229))
- Add `__all__` for `torch.utils.dlpack` ([#149026](https://github.com/pytorch/pytorch/pull/149026))
- [CUDA][cuBLAS] Aten GEMM overload for FP32 output from FP16/BF16 inputs ([#150812](https://github.com/pytorch/pytorch/pull/150812))
- Support fp8 dtypes in assert_close ([#150002](https://github.com/pytorch/pytorch/pull/150002))
- Add torch.accelerator.device_index as accelerator's device switch context ([#148864](https://github.com/pytorch/pytorch/pull/148864))
- [CUDA][conv3d] bump tolerances for `test_variant_consistency_eager` `conv3d` `complex64` ([#152203](https://github.com/pytorch/pytorch/pull/152203))
- [Torch] Fix crash when comparing fp8 tensors that have more than 1 dimension ([#153508](https://github.com/pytorch/pytorch/pull/153508))
- [Torch] Fix error message formatting in fp8 comparison logic ([#153647](https://github.com/pytorch/pytorch/pull/153647))
- remove allow-untyped-defs from torch/nn/utils/_expanded_weights/conv_expanded_weights.py ([#154623](https://github.com/pytorch/pytorch/pull/154623))
- [BE] Use vendored packaging for testing ([#154946](https://github.com/pytorch/pytorch/pull/154946))
### security
