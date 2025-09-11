
# Release Notes worksheet nn_frontend

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

## nn_frontend
### bc breaking
### deprecation
### new features
### improvements
- Allow register_buffer with Tensor-like object ([#159455](https://github.com/pytorch/pytorch/pull/159455))
### bug fixes
- [CUDA] Fix missing `__syncthreads` in MultiMarginLoss backward ([#158994](https://github.com/pytorch/pytorch/pull/158994))
### performance
### docs
- [BE] Make torch.nn.modules.* satisfy the docs coverage test ([#158491](https://github.com/pytorch/pytorch/pull/158491))
- [BE] More torch.nn docs coverage test (except for torch.nn.parallel) ([#158654](https://github.com/pytorch/pytorch/pull/158654))
- Fix the Doc of `padding` in `avg_poolnd` ([#159142](https://github.com/pytorch/pytorch/pull/159142))
### devs
### Untopiced
- Support deterministic upsample trilinear backward ([#154239](https://github.com/pytorch/pytorch/pull/154239))
- Add device check in `mse_loss` ([#155089](https://github.com/pytorch/pytorch/pull/155089))
- Fused RMSNorm Housekeeping ([#159317](https://github.com/pytorch/pytorch/pull/159317))
- [ROCm] revamp miopen integration ([#161687](https://github.com/pytorch/pytorch/pull/161687))
- NLLLoss: validate target is 0D when input is 1D ([#161412](https://github.com/pytorch/pytorch/pull/161412))
### not user facing
- add test_batchnorn_2D and 3D tests ([#156498](https://github.com/pytorch/pytorch/pull/156498))
- layernorm tests: Tweak test thresholds for comparing tensors ([#156699](https://github.com/pytorch/pytorch/pull/156699))
- fix type hints for interpolation functions ([#157202](https://github.com/pytorch/pytorch/pull/157202))
- [BE][Ez]: Auto add return type annotations for methods in torch/nn/module ([#157925](https://github.com/pytorch/pytorch/pull/157925))
- FractionalMaxPool3d add kernel_size check ([#155549](https://github.com/pytorch/pytorch/pull/155549))
- [nn]: updated type alias for padddingmode in module/conv.py ([#158843](https://github.com/pytorch/pytorch/pull/158843))
- typo ([#156560](https://github.com/pytorch/pytorch/pull/156560))
- [Testing] Add MPS to NATIVE_DEVICES ([#153835](https://github.com/pytorch/pytorch/pull/153835))
- DOC: update CrossEntropyLoss with note and example of incorrect target specification ([#155649](https://github.com/pytorch/pytorch/pull/155649))
- Removed redundant dtype conversion in scaled_dot_product_attention docstring example ([#161613](https://github.com/pytorch/pytorch/pull/161613))
- Improve error message for unsupported padding config ([#160866](https://github.com/pytorch/pytorch/pull/160866))
### security
