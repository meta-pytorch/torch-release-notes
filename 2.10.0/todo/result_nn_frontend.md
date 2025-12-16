
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
- [BC Breaking] Remove flex + njt code paths ([#161734](https://github.com/pytorch/pytorch/pull/161734))
### deprecation
### new features
- Add public grouped_mm ([#168298](https://github.com/pytorch/pytorch/pull/168298))
### improvements
- support batch size=0 for flash attention ([#166318](https://github.com/pytorch/pytorch/pull/166318))
- GroupNorm: include offending values in error message; add test ([#167925](https://github.com/pytorch/pytorch/pull/167925))
### bug fixes
- [Flex] Fix silent correctness w/ backpropping grads ([#163677](https://github.com/pytorch/pytorch/pull/163677))
- Avoid fast path mask left-align check in compiled TransformerEncoder ([#163773](https://github.com/pytorch/pytorch/pull/163773))
- [CUDA] Large tensor maxpool crash fix ([#165374](https://github.com/pytorch/pytorch/pull/165374))
- [CUDA] fix reflection padding for large batch size ([#165942](https://github.com/pytorch/pytorch/pull/165942))
- Added Validation for batch_norm eps value ([#166756](https://github.com/pytorch/pytorch/pull/166756))
- Raise error for 1D (size > 1) -> 0D parameter loads ([#166335](https://github.com/pytorch/pytorch/pull/166335))
- Add empty tensor check for `_pad_packed_sequence` ([#167521](https://github.com/pytorch/pytorch/pull/167521))
- Fix strides for fa4 integration ([#169714](https://github.com/pytorch/pytorch/pull/169714))
- Fix strides for fa4 integration ([#169714](https://github.com/pytorch/pytorch/pull/169714))
### performance
### docs
- Update ctc loss docs float32 input required for CuDNN ([#162042](https://github.com/pytorch/pytorch/pull/162042))
- Update LPPool docs to clarify ceil_mode padding semantics when ceil_mode=True ([#163186](https://github.com/pytorch/pytorch/pull/163186))
- [docs] Add usage examples to ConvTranspose1d docstring ([#165618](https://github.com/pytorch/pytorch/pull/165618))
### devs
### Untopiced
- [ROCm] fix miopen batchnorm changing output format ([#162112](https://github.com/pytorch/pytorch/pull/162112))
- enable sync batchnorm for HPU device ([#163047](https://github.com/pytorch/pytorch/pull/163047))
- [Flex attention] Fix flex attention head broadcast ([#163426](https://github.com/pytorch/pytorch/pull/163426))
- Fix warn message ([#163578](https://github.com/pytorch/pytorch/pull/163578))
- [2/N] Apply ruff UP035 check in torch files ([#164054](https://github.com/pytorch/pytorch/pull/164054))
- Add scaled_mm python API, test ([#164142](https://github.com/pytorch/pytorch/pull/164142))
- [flex_attention] replace sliced BlockMask noop with helpful error ([#164702](https://github.com/pytorch/pytorch/pull/164702))
- Fixes floating point exception in torch.nn.PixelShuffle ([#163154](https://github.com/pytorch/pytorch/pull/163154))
- Fix error suppression syntax in utils and nn ([#166242](https://github.com/pytorch/pytorch/pull/166242))
- bwd pass ([#164504](https://github.com/pytorch/pytorch/pull/164504))
- [Conv1d] Check overflow before we compute padding size. ([#162363](https://github.com/pytorch/pytorch/pull/162363))
- bwd pass ([#164504](https://github.com/pytorch/pytorch/pull/164504))
- [1/N] Add return types of Python functions ([#167162](https://github.com/pytorch/pytorch/pull/167162))
- Update torch.var documentation to use modern API ([#167209](https://github.com/pytorch/pytorch/pull/167209))
- [CUDA] Large max pool fix ([#167427](https://github.com/pytorch/pytorch/pull/167427))
- Fix softshrink overflow when lambda exceeds dtype max ([#166162](https://github.com/pytorch/pytorch/pull/166162))
### not user facing
- [Bilinear] move check to reset_parameters ([#160952](https://github.com/pytorch/pytorch/pull/160952))
- [Bug] Add more boundary check for FractionalMaxPool3d ([#161876](https://github.com/pytorch/pytorch/pull/161876))
- Handling overflow for long int overflow for the product of kernel_hei… ([#155989](https://github.com/pytorch/pytorch/pull/155989))
- Add explicit typing to nn.Module.__init__() parameters ([#157389](https://github.com/pytorch/pytorch/pull/157389))
- [2/n] Support module.to("cuda:0") in FakeTensorMode on cuda-less machine ([#163433](https://github.com/pytorch/pytorch/pull/163433))
- [ROCm] Transformer/SDPA unit test parity ([#163745](https://github.com/pytorch/pytorch/pull/163745))
- better error handling for rrelu when lower or upper range is infinite ([#160965](https://github.com/pytorch/pytorch/pull/160965))
- Fix the shape check inside gnll loss ([#147522](https://github.com/pytorch/pytorch/pull/147522))
- Update disabling fast-path for strict-export inside MultiheadAttention ([#164544](https://github.com/pytorch/pytorch/pull/164544))
- Fix error, remove file from pyrefly checking ([#165094](https://github.com/pytorch/pytorch/pull/165094))
- [cuda] fix nll_loss2d backward bounds check with reduction=none ([#165247](https://github.com/pytorch/pytorch/pull/165247))
- [6/N] Use Python 3.10 typing ([#167649](https://github.com/pytorch/pytorch/pull/167649))
- Remove useless super() delegation ([#167791](https://github.com/pytorch/pytorch/pull/167791))
- [MTIA] Support bfloat16 in half_to_float ([#168938](https://github.com/pytorch/pytorch/pull/168938))
- [xpu] Enable TransformerEncoderLayer Fast Path for XPU Device ([#168234](https://github.com/pytorch/pytorch/pull/168234))
- Preserves shape when 0 dim tensors are replicated ([#167976](https://github.com/pytorch/pytorch/pull/167976))
### security
