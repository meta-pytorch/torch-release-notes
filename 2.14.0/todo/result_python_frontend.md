
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
- [CUDA] Add post-facto memory annotation API for memory snapshots ([#190575](https://github.com/pytorch/pytorch/pull/190575))
- Add decorator/curried calling convention for torch.utils.checkpoint.checkpoint (eager) ([#189411](https://github.com/pytorch/pytorch/pull/189411))
### improvements
- Fix arange int64 fractional truncation ([#185812](https://github.com/pytorch/pytorch/pull/185812))
- Expose c10::utils::{get,set}_env to Python ([#191015](https://github.com/pytorch/pytorch/pull/191015))
- Avoid closure cycles in `cuda/memory.py` + copypasta ([#191441](https://github.com/pytorch/pytorch/pull/191441))
### bug fixes
- Raise user error for dense mkldnn device tensors ([#185711](https://github.com/pytorch/pytorch/pull/185711))
- [Sobol] Validate input arguments ([#191198](https://github.com/pytorch/pytorch/pull/191198))
- [Sobol] Validate input arguments ([#191198](https://github.com/pytorch/pytorch/pull/191198))
- Make SAC-saved tensors optionally respect user saved_tensors_hooks ([#190581](https://github.com/pytorch/pytorch/pull/190581))
- Add type check to THPStream_richcompare instead of casting arbitrary objects ([#192523](https://github.com/pytorch/pytorch/pull/192523))
### performance
- PyObject Dispatch ([#187949](https://github.com/pytorch/pytorch/pull/187949))
- Fix extra clone in torch.compile for stateless RNG APIs ([#188495](https://github.com/pytorch/pytorch/pull/188495))
- PyObject Dispatch ([#187949](https://github.com/pytorch/pytorch/pull/187949))
- PyObject Dispatch ([#187949](https://github.com/pytorch/pytorch/pull/187949))
- Speed up CPU quantile/nanquantile with partial selection ([#188394](https://github.com/pytorch/pytorch/pull/188394))
### docs
- Clarify set_default_device device arguments ([#187240](https://github.com/pytorch/pytorch/pull/187240))
- Document factory kwargs for torch.normal(mean, std, size) ([#187820](https://github.com/pytorch/pytorch/pull/187820))
- Fix index_reduce_ docstring: index indexes into self, not source ([#189008](https://github.com/pytorch/pytorch/pull/189008))
### devs
### Untopiced
- Optimize mutable custom op version bump dispatch ([#186175](https://github.com/pytorch/pytorch/pull/186175))
- skip xpu cow histogramdd ([#174670](https://github.com/pytorch/pytorch/pull/174670))
- Introduce initial_seed/get_rng_state/get_rng_state_all to torch.accelerator ([#186597](https://github.com/pytorch/pytorch/pull/186597))
- Support large float32 tensors in quantile by computing ranks in float64 ([#187574](https://github.com/pytorch/pytorch/pull/187574))
- [dlpack] Add read-only DLPack export and ReadOnlyTensorWrapper ([#188554](https://github.com/pytorch/pytorch/pull/188554))
- Clarify undefined behavior for unsorted searchsorted inputs ([#184888](https://github.com/pytorch/pytorch/pull/184888))
- Skip conv_transpose3d redispatch test on Windows CI - flaky test ([#188828](https://github.com/pytorch/pytorch/pull/188828))
- Expose Philox RNG state reservation to Python as Generator.philox_state ([#191019](https://github.com/pytorch/pytorch/pull/191019))
- Fix uint64 setitem overflow for values above INT64_MAX ([#191604](https://github.com/pytorch/pytorch/pull/191604))
- [xpu] Increase tolerance for tests that fail due to non-deterministic operators behavior. ([#177069](https://github.com/pytorch/pytorch/pull/177069))
### not user facing
- [CUDA][CuteDSL] Use unique values for cutedsl topk in `common_methods_invocations.py` ([#188838](https://github.com/pytorch/pytorch/pull/188838))
- Fix torch.arange dtype note: stop should be step ([#188943](https://github.com/pytorch/pytorch/pull/188943))
- Add docstrings to in-place functions with an out-of-place equivalent ([#189571](https://github.com/pytorch/pytorch/pull/189571))
- Increase precision for golden solution in transformer tests. ([#169694](https://github.com/pytorch/pytorch/pull/169694))
- [OpInfo] Fix randint samples for bool ([#192347](https://github.com/pytorch/pytorch/pull/192347))
### security
