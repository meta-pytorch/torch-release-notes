
# Release Notes worksheet python_frontend

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

## python_frontend
### bc breaking
### deprecation
### new features
- Add `torch.accelerator.initial_seed()`, `torch.accelerator.get_rng_state()`, and `torch.accelerator.get_rng_state_all()` for backend-agnostic accelerator RNG inspection ([#186597](https://github.com/pytorch/pytorch/pull/186597))
- Add read-only DLPack export through `Tensor.__dlpack__(read_only=True)` and `torch.utils.dlpack.ReadOnlyTensorWrapper`, including copy-on-write-preserving exchange with compatible consumers ([#188554](https://github.com/pytorch/pytorch/pull/188554))
- Add `torch.Generator.philox_state()` so Python-authored kernels can reserve Philox counter ranges that remain correct across CUDA Graph capture and replay ([#191019](https://github.com/pytorch/pytorch/pull/191019))
### improvements
- Allow `torch.quantile` and `torch.nanquantile` to process `float32` and `float64` inputs larger than `2**24` elements on devices with `float64` support by computing ranks in `float64` ([#187574](https://github.com/pytorch/pytorch/pull/187574))
### bug fixes
- Fix `torch.arange` with an integer output dtype and fractional arguments computing the wrong length by truncating those arguments too early ([#185812](https://github.com/pytorch/pytorch/pull/185812))
- Raise a clear unsupported-operation error for dense tensor factories targeting `device="mkldnn"` instead of triggering an internal assertion ([#185711](https://github.com/pytorch/pytorch/pull/185711))
### performance
- Add a Python-object dispatch fast path for Python-implemented custom operators, reducing no-op dispatch overhead when all relevant kernels are registered in Python ([#187949](https://github.com/pytorch/pytorch/pull/187949))
- Speed up CPU `torch.quantile` and `torch.nanquantile` by using partial selection instead of fully sorting when only a small number of quantiles is requested ([#188394](https://github.com/pytorch/pytorch/pull/188394))
- Reduce mutable `torch.library.custom_op` dispatch overhead by bumping version counters only for mutated arguments actually supplied by the caller ([#186175](https://github.com/pytorch/pytorch/pull/186175))
### docs
- Document all accepted device-like arguments for `torch.set_default_device`, including integer accelerator indices and `None` ([#187240](https://github.com/pytorch/pytorch/pull/187240))
- Document the tensor-factory keyword arguments accepted by the `torch.normal(mean, std, size)` overload ([#187820](https://github.com/pytorch/pytorch/pull/187820))
- Clarify that the `index` argument to `Tensor.index_reduce_()` selects positions in `self` to accumulate into, rather than positions in `source` ([#189008](https://github.com/pytorch/pytorch/pull/189008))
- Document that `torch.searchsorted` does not validate sorting and has undefined behavior for unsorted input when no `sorter` is provided ([#184888](https://github.com/pytorch/pytorch/pull/184888))
- Correct the `torch.arange` dtype-inference note to refer to the `step` argument instead of the nonexistent `stop` argument ([#188943](https://github.com/pytorch/pytorch/pull/188943))
- Add docstrings for top-level in-place functions that have out-of-place equivalents ([#189571](https://github.com/pytorch/pytorch/pull/189571))
### devs
### not user facing
- Restore ROCm OpInfo test coverage for reverse power and interpolation without changing Python API behavior ([#191534](https://github.com/pytorch/pytorch/pull/191534))
- Expose private, mutex-protected environment-variable helpers to Python for internal native/Python coordination ([#191015](https://github.com/pytorch/pytorch/pull/191015))
- Refactor accelerator memory-statistics traversal helpers to avoid temporary Python closure cycles ([#191441](https://github.com/pytorch/pytorch/pull/191441))
- Skip a flaky `conv_transpose3d` redispatch test on Windows CI ([#188828](https://github.com/pytorch/pytorch/pull/188828))
- Increase the precision of reference results in transformer tests to avoid TF32-related false failures ([#169694](https://github.com/pytorch/pytorch/pull/169694))
- Correct boolean `randint` sample generation in OpInfo tests ([#192347](https://github.com/pytorch/pytorch/pull/192347))
### security
- Validate native Sobol-engine tensor shapes and sequence bounds before indexing direction-number tables ([#191198](https://github.com/pytorch/pytorch/pull/191198))
- Type-check operands in stream comparisons instead of interpreting arbitrary Python objects as stream instances ([#192523](https://github.com/pytorch/pytorch/pull/192523))
