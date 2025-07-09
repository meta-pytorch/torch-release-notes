
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
- Add warning for module full backward hook when no input requires gradient ([#155339](https://github.com/pytorch/pytorch/pull/155339))
### bug fixes
### performance
- Add Half support for weight_norm on CPU ([#148878](https://github.com/pytorch/pytorch/pull/148878))
### docs
- Fix docs format error in `torch.nn` ([#150156](https://github.com/pytorch/pytorch/pull/150156))
- Optimize transformer encoder/decoder init suggestion ([#146882](https://github.com/pytorch/pytorch/pull/146882))
- Optimize `ConvTranspose2d` stride description ([#150819](https://github.com/pytorch/pytorch/pull/150819))
- [Easy] Add `output_size` in forward method of ConvTranspose2d ([#150609](https://github.com/pytorch/pytorch/pull/150609))
- Expand docs for `nn.functional`, and make the wording consistent ([#148436](https://github.com/pytorch/pytorch/pull/148436))
- [Easy] Optimize `clip_grad` param description ([#151532](https://github.com/pytorch/pytorch/pull/151532))
- Optimize `interpolate` saturate description ([#151304](https://github.com/pytorch/pytorch/pull/151304))
- Optimize `Sequential` methods description ([#147304](https://github.com/pytorch/pytorch/pull/147304))
- Fix nn.LazyModuleMixin examples ([#150596](https://github.com/pytorch/pytorch/pull/150596))
- Fix RMSNorm doc rendering ([#154205](https://github.com/pytorch/pytorch/pull/154205))
- Update documentation wording for transformer-related layers ([#155123](https://github.com/pytorch/pytorch/pull/155123))
- Address docs for clip_grad functions ([#155125](https://github.com/pytorch/pytorch/pull/155125))
### devs
### Untopiced
- Add `nn.Bilinear` param validation ([#149018](https://github.com/pytorch/pytorch/pull/149018))
- Fix broken LazyLinear init ([#149693](https://github.com/pytorch/pytorch/pull/149693))
- Add check for ctc_loss targets param ([#150981](https://github.com/pytorch/pytorch/pull/150981))
- Optimize register_full_backward_hook description when all input no grad ([#151785](https://github.com/pytorch/pytorch/pull/151785))
- Native channel shuffle floating point exception ([#144010](https://github.com/pytorch/pytorch/pull/144010))
- Add pad limit of avg_poolnd and AvgPoolnd ([#152680](https://github.com/pytorch/pytorch/pull/152680))
- [Pytorch] Add option to CPU Blas GEMM to avoid output downcast ([#154012](https://github.com/pytorch/pytorch/pull/154012))
- Don't call `sum()` on a tensor that is not summable in layer_norm ([#156600](https://github.com/pytorch/pytorch/pull/156600))
### not user facing
- Remove outdated skipCUDAIfCudnnVersionLessThan decoration ([#148940](https://github.com/pytorch/pytorch/pull/148940))
- Optimize `MaxPool1d` param `ceil_mode` description ([#148869](https://github.com/pytorch/pytorch/pull/148869))
- Fixed abnormal behavior of LazyLinear when using LayzLinear and load_state together ([#147599](https://github.com/pytorch/pytorch/pull/147599))
- [ROCm] skip test_RNN_dropout_state ([#149446](https://github.com/pytorch/pytorch/pull/149446))
- Move formulas on separate line in loss.py ([#150565](https://github.com/pytorch/pytorch/pull/150565))
- Add plot for `torch.nn.Threshold` and `torch.nn.GLU` ([#150171](https://github.com/pytorch/pytorch/pull/150171))
- docs: allow empty targets tensor in ctc_loss ([#151080](https://github.com/pytorch/pytorch/pull/151080))
- [Easy] Optimize container.py typing ([#151653](https://github.com/pytorch/pytorch/pull/151653))
- [BE][Easy]: Simplify ModuleList reversed method ([#151673](https://github.com/pytorch/pytorch/pull/151673))
- [CUDA][CPU] Bump system memory requirement for `test_cross_entropy_large_tensor` ([#151812](https://github.com/pytorch/pytorch/pull/151812))
- [TF32][CUDA] account for TF32 in `test_linear_autograd` ([#152216](https://github.com/pytorch/pytorch/pull/152216))
- [ROCm] Unskipped test_rnn_dropout_state for ROCm ([#152339](https://github.com/pytorch/pytorch/pull/152339))
- [CUDA][cuDNN] Fix handling of `CPU` side input and target length tensors in `CTCLoss` ([#152745](https://github.com/pytorch/pytorch/pull/152745))
- [BE] Update `.pyi` stub template to use Generic TypeAlias (PEP 585) and Union Type (PEP 604) ([#150728](https://github.com/pytorch/pytorch/pull/150728))
- [BE] Add `__all__` to `torch/nn/functional.pyi` and `torch/return_types.pyi` ([#150729](https://github.com/pytorch/pytorch/pull/150729))
- [BE][Ez]: Improve typing in torch/modules/container.py ([#153728](https://github.com/pytorch/pytorch/pull/153728))
- Update rnn.py, fix `torch.nn.RNN` document error ([#153620](https://github.com/pytorch/pytorch/pull/153620))
- docs: fix "should not to be" typo in `register_buffer` docstring ([#153817](https://github.com/pytorch/pytorch/pull/153817))
- Add hint message when parameters is empty in clip_grad_norm_ ([#151529](https://github.com/pytorch/pytorch/pull/151529))
- Fix load_state_dict description ([#154599](https://github.com/pytorch/pytorch/pull/154599))
- Fix avg_pool2d param kernel_size descripthon ([#154353](https://github.com/pytorch/pytorch/pull/154353))
- Fix weight tensor documentation #134896 ([#155093](https://github.com/pytorch/pytorch/pull/155093))
- [CUDA] Fix missing bounds check in `Softmax.cu` ([#154778](https://github.com/pytorch/pytorch/pull/154778))
- [BE][PYFMT] migrate PYFMT for `{torch,test}/{nn,optim}/**` to `ruff format` ([#144548](https://github.com/pytorch/pytorch/pull/144548))
- Document padding size limitations in nn.modules.padding (#134840) ([#155618](https://github.com/pytorch/pytorch/pull/155618))
- fix hack to check if register_buffer has been overridden ([#155963](https://github.com/pytorch/pytorch/pull/155963))
### security
