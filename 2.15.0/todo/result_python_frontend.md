
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
- Remove NJT (nested jagged tensor) from weights_only safe globals ([#194380](https://github.com/pytorch/pytorch/pull/194380))
- Reject re-running `import torch` after a failed import ([#194654](https://github.com/pytorch/pytorch/pull/194654))
### deprecation
### new features
### improvements
- [BE] Saturate out-of-range integer scalar `clamp` bounds ([#193169](https://github.com/pytorch/pytorch/pull/193169))
- [BE] Saturate out-of-range integer scalar `clamp` bounds ([#193169](https://github.com/pytorch/pytorch/pull/193169))
- Add handling for empty batch dimensions in FFT operations ([#190483](https://github.com/pytorch/pytorch/pull/190483))
- [BE] Saturate out-of-range integer scalar `clamp` bounds ([#193169](https://github.com/pytorch/pytorch/pull/193169))
### bug fixes
- Make emptyHostCache() a no-op when the backend has no host allocator ([#197593](https://github.com/pytorch/pytorch/pull/197593))
- Compute Multinomial.entropy() in the distribution dtype and keep _binomial in expand() ([#198006](https://github.com/pytorch/pytorch/pull/198006))
- Reject overlapping out= tensors in aminmax ([#195342](https://github.com/pytorch/pytorch/pull/195342))
### performance
### docs
- [docs] Document undefined behavior of non-0/1 bytes in bool tensors ([#199012](https://github.com/pytorch/pytorch/pull/199012))
### devs
### Untopiced
- Enable eager tests for inductor-unittest - define xfails for xpu in op_db for test_ops.py using device_type list in DecorateInfo ([#179549](https://github.com/pytorch/pytorch/pull/179549))
- Preserve storage sharing when loading checkpoints on meta/fake devices ([#193566](https://github.com/pytorch/pytorch/pull/193566))
- [PyTorch] Fix OpInfo rand_like in common_methods_invocations ([#193975](https://github.com/pytorch/pytorch/pull/193975))
- Enable eager tests for inductor-unittest - - Enabel more tests in test_ops.py on Intel GPU ([#178849](https://github.com/pytorch/pytorch/pull/178849))
- Fix nn.functional.threshold OpInfo reference for strict NumPy uint8 casting ([#189273](https://github.com/pytorch/pytorch/pull/189273))
- Fix stale test-class name in the conv_transpose3d redispatch skip ([#196608](https://github.com/pytorch/pytorch/pull/196608))
- Widen fp16 redispatch tolerance for linear_cross_entropy OpInfos ([#197565](https://github.com/pytorch/pytorch/pull/197565))
- Fix `torch.asarray` for buffer-protocol objects with no dtype ([#188784](https://github.com/pytorch/pytorch/pull/188784))
- Support optional Tensor list schemas ([#187012](https://github.com/pytorch/pytorch/pull/187012))
- [FlopCounter] Add skip_unsupported parameter for graceful handling of unsupported HOPs ([#167224](https://github.com/pytorch/pytorch/pull/167224))
- Fix Float8_e5m2fnuz numeric_limits epsilon and round_error ([#198855](https://github.com/pytorch/pytorch/pull/198855))
### not user facing
- [ROCm] Skip conv_transpose1d complex32 reference test on MI200 ([#198025](https://github.com/pytorch/pytorch/pull/198025))
### security
