
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
- Upgrade to DLPack 1.0. ([#145000](https://github.com/pytorch/pytorch/pull/145000))
- [BE] Raise ValueError from `torch.cat` meta func ([#158249](https://github.com/pytorch/pytorch/pull/158249))
### deprecation
### new features
- Add utility to get computed kernel in torch.library ([#158393](https://github.com/pytorch/pytorch/pull/158393))
- Detect torch function in lists as well ([#160256](https://github.com/pytorch/pytorch/pull/160256))
### improvements
- Reduce random reads for offset metadata when calling torch.load under FakeTensorMode ([#157931](https://github.com/pytorch/pytorch/pull/157931))
- Add unsigned support to `IValue` ([#160102](https://github.com/pytorch/pytorch/pull/160102))
- added class or module info for functions blocked by weight-only load ([#159935](https://github.com/pytorch/pytorch/pull/159935))
- [BE] Cleanup stale comments/copy from `gemm`  ([#162001](https://github.com/pytorch/pytorch/pull/162001))
- [BE] Cleanup stale comments/copy from `gemm`  ([#162001](https://github.com/pytorch/pytorch/pull/162001))
### bug fixes
- load inline user overridable gencode ([#156850](https://github.com/pytorch/pytorch/pull/156850))
- More fixes to `MakeTensor::computeStorageSize()` ([#158813](https://github.com/pytorch/pytorch/pull/158813))
- Fix max_width computation in _tensor_str._Formatter ([#126859](https://github.com/pytorch/pytorch/pull/126859))
- Fix max_width computation in _tensor_str._Formatter ([#126859](https://github.com/pytorch/pytorch/pull/126859))
- Improve pin_memory error message on CPU-only systems ([#159994](https://github.com/pytorch/pytorch/pull/159994))
### performance
### docs
- Improve documentation for torch.lobpcg ([#156139](https://github.com/pytorch/pytorch/pull/156139))
- Delete sections referencing torchscript in serialization docs ([#156648](https://github.com/pytorch/pytorch/pull/156648))
- Documentation update torch.clone #156644 ([#157007](https://github.com/pytorch/pytorch/pull/157007))
- Fix typo in torch.set_float32_matmul_precision docs ([#158191](https://github.com/pytorch/pytorch/pull/158191))
- Update RuntimeError message in is_nonzero(input) method from bool to Boolean ([#159712](https://github.com/pytorch/pytorch/pull/159712))
- DOC: Clarify documentation for torch.matmul and fix a typo ([#161424](https://github.com/pytorch/pytorch/pull/161424))
### devs
### Untopiced
- Optimize dim description in torch.max ([#156153](https://github.com/pytorch/pytorch/pull/156153))
- [BE] Accelerator agnostic timer.py ([#157131](https://github.com/pytorch/pytorch/pull/157131))
- Documentation Fix: Torch gather broadcasting  ([#157920](https://github.com/pytorch/pytorch/pull/157920))
- Documentation Fix: torch.tensor.scatter_ docs ([#157929](https://github.com/pytorch/pytorch/pull/157929))
- Documentation Fix: torch.empty_like memory preservation ([#158050](https://github.com/pytorch/pytorch/pull/158050))
- [DLPack] Add support for missing keyword-arguments. ([#150218](https://github.com/pytorch/pytorch/pull/150218))
- Raise `BufferError` for DLPack buffer-related errors. ([#150691](https://github.com/pytorch/pytorch/pull/150691))
- Fix `torch.randint`, `torch.mul` param missing description ([#158731](https://github.com/pytorch/pytorch/pull/158731))
- Fix docstring for clip_grads_with_norm_ to reflect clamping behavior ([#158200](https://github.com/pytorch/pytorch/pull/158200))
- [OpInfo][BE] Better inputs for addmm ([#160234](https://github.com/pytorch/pytorch/pull/160234))
- Fix the Doc issue on the description of edge_order in torch.gradient() ([#159130](https://github.com/pytorch/pytorch/pull/159130))
- Optimize `min`, `max` gradient behavior description ([#160312](https://github.com/pytorch/pytorch/pull/160312))
- Fix sort doc error ([#161539](https://github.com/pytorch/pytorch/pull/161539))
- Update optional tag for `interpolation` in `torch.quantile()` ([#161706](https://github.com/pytorch/pytorch/pull/161706))
- Argsort doc stable kwargs ([#161986](https://github.com/pytorch/pytorch/pull/161986))
- Adding missing example of torch.full_like Issue#161899 ([#162051](https://github.com/pytorch/pytorch/pull/162051))
- Modified the docs to add example for torch.is_floating_point and torc… ([#161951](https://github.com/pytorch/pytorch/pull/161951))
### not user facing
- Add `torch.segment_reduce` docs ([#154352](https://github.com/pytorch/pytorch/pull/154352))
- Fix incorrect bin edge description in histogramdd docs ([#158275](https://github.com/pytorch/pytorch/pull/158275))
- Update the signature and test of torch.hamming_window() ([#152682](https://github.com/pytorch/pytorch/pull/152682))
- Relax tolerance for test_quick_baddbmm_cpu_complex64 ([#152424](https://github.com/pytorch/pytorch/pull/152424))
### security
- Don't store flamegraph to tmp folder ([#157374](https://github.com/pytorch/pytorch/pull/157374))
