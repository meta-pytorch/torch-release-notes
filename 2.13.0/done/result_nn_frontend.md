
# Release Notes worksheet nn_frontend

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

## nn_frontend
### bc breaking
### deprecation
### new features
- Add `nn.LinearCrossEntropyLoss`, a fused linear-projection plus cross-entropy loss module that avoids materializing the full logits tensor ([#181573](https://github.com/pytorch/pytorch/pull/181573), [#185852](https://github.com/pytorch/pytorch/pull/185852))
### improvements
- Expose `num_splits` in FlashAttention-2 and bump the flash-attention submodule ([#179760](https://github.com/pytorch/pytorch/pull/179760))
- Support `linear_bias` in `linear_cross_entropy` on the reference and chunked paths ([#185129](https://github.com/pytorch/pytorch/pull/185129), [#185276](https://github.com/pytorch/pytorch/pull/185276))
### bug fixes
- Validate `stride`/`padding`/`kernel_size` length in `slow_conv3d` ([#181063](https://github.com/pytorch/pytorch/pull/181063))
- Validate inputs in `math_channel_shuffle` ([#181029](https://github.com/pytorch/pytorch/pull/181029))
- Validate `delta` type in `nn.HuberLoss` constructor ([#184012](https://github.com/pytorch/pytorch/pull/184012))
- Lowercase the environment variable in `torch/serialization.py` so it matches the true values ([#180959](https://github.com/pytorch/pytorch/pull/180959))
- Fix int32 overflow in `layer_norm` on CUDA for tensors with more than 2^32 elements ([#181600](https://github.com/pytorch/pytorch/pull/181600))
- Reject `NestedTensor` inputs in `flex_attention` with a clear error instead of an unclear backend failure ([#183516](https://github.com/pytorch/pytorch/pull/183516))
- Fix SDPA incorrect early return on 0 head dim qk with valid v ([#184914](https://github.com/pytorch/pytorch/pull/184914))
- Fix `reflection_pad1d` backward CUDA launch for large batches ([#185024](https://github.com/pytorch/pytorch/pull/185024))
- Fix `lp_pool` infinity norm handling ([#183997](https://github.com/pytorch/pytorch/pull/183997))
### performance
### docs
### devs
### Untopiced
### not user facing
- Fix typo in Transformer._reset_parameters docstring ([#182243](https://github.com/pytorch/pytorch/pull/182243))
- Fix RuntimeError formatting in AdaptiveLogSoftmaxWithLoss ([#182325](https://github.com/pytorch/pytorch/pull/182325))
- docs: clarify interpolate align_corners default ([#182589](https://github.com/pytorch/pytorch/pull/182589))
- Fix grammar in FractionalMaxPool3d error message (#182346) ([#182346](https://github.com/pytorch/pytorch/pull/182346))
- [Docathon]: converted cudnn_rnn_determinism to markdown ([#184080](https://github.com/pytorch/pytorch/pull/184080))
- Drop obsolete fp16/bfloat16 CPU skips in tests ([#184640](https://github.com/pytorch/pytorch/pull/184640))
- Audit @skipIfMPS decorators: drop obsolete, refine with @dtypesIfMPS ([#184655](https://github.com/pytorch/pytorch/pull/184655))
- Fix typos in torch.nn.modules docstrings ([#185603](https://github.com/pytorch/pytorch/pull/185603))
### security
