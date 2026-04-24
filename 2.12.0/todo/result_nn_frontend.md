
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
### improvements
- Adding bias argument to NN normalization methods (Reopened PR #157198) ([#176573](https://github.com/pytorch/pytorch/pull/176573))
### bug fixes
- [BE] Add dtype check to loss_nll meta func ([#175151](https://github.com/pytorch/pytorch/pull/175151))
- trunc_normal_ low precision fix  ([#174997](https://github.com/pytorch/pytorch/pull/174997))
- trunc_normal_ low precision fix  ([#174997](https://github.com/pytorch/pytorch/pull/174997))
- trunc_normal_ low precision fix  ([#174997](https://github.com/pytorch/pytorch/pull/174997))
### performance
### docs
### devs
### Untopiced
- fix varlen doc string ([#175261](https://github.com/pytorch/pytorch/pull/175261))
- [nn] Improve MultiMarginLoss error message for inconsistent target size ([#174072](https://github.com/pytorch/pytorch/pull/174072))
- NEON implementation of `interpolate` for `{bilinear, bicubic} x {antialias=(True, False)}` on ChannelsLast RGB images ([#176217](https://github.com/pytorch/pytorch/pull/176217))
- Fix #110505 ([#176559](https://github.com/pytorch/pytorch/pull/176559))
- Fix numerical inconsistency in Conv3d.reset_parameters for channels_l… ([#175990](https://github.com/pytorch/pytorch/pull/175990))
- Fixes MSELoss failing to compute the gradients when inputs have different dtype ([#175743](https://github.com/pytorch/pytorch/pull/175743))
- [SDPA] Fix device mismatch in scaled_dot_product_attention docstring example ([#178684](https://github.com/pytorch/pytorch/pull/178684))
- add enable_gqa flag to varlen_attn ([#179468](https://github.com/pytorch/pytorch/pull/179468))
- Fix GroupNorm backward correctness bug on AMD wavefront-64 ([#178872](https://github.com/pytorch/pytorch/pull/178872))
- add flop registration to varlen ([#179500](https://github.com/pytorch/pytorch/pull/179500))
### not user facing
- [CUDA] Parallelize upsample_bicubic2d across batch/channel dimensions — 4-43x speedup for VLM pos embed resizing ([#174578](https://github.com/pytorch/pytorch/pull/174578))
- [nn] Allow eps=0 in batch_norm during eval mode ([#175508](https://github.com/pytorch/pytorch/pull/175508))
- [nn] Support meta device in trunc_normal_ init ([#176240](https://github.com/pytorch/pytorch/pull/176240))
- [pt2 bug bash] Fix nn.functional.pad compile crash with deterministic mode + replication padding ([#177166](https://github.com/pytorch/pytorch/pull/177166))
- [xpu][test][1/N] Enable tests of test_nn.py on Intel GPU - instantiate TestNN with instantiate_device_type_tests ([#166396](https://github.com/pytorch/pytorch/pull/166396))
- Fix incorrect attn_mask shape in scaled_dot_product_attention docs ([#177999](https://github.com/pytorch/pytorch/pull/177999))
- Free q, k, v early in multi_head_attention_forward  ([#178452](https://github.com/pytorch/pytorch/pull/178452))
- [docs] Clarify RMSNorm eps parameter default behavior ([#173887](https://github.com/pytorch/pytorch/pull/173887))
- Improve Conv2d docs: clarify math variable to parameter mapping and fix cross-correlation link ([#178965](https://github.com/pytorch/pytorch/pull/178965))
- [rnn] Update condition in test_rnn_check_device ([#178981](https://github.com/pytorch/pytorch/pull/178981))
- [Testing] Add guard-page test for uint8 interpolate overread ([#180219](https://github.com/pytorch/pytorch/pull/180219))
### security
