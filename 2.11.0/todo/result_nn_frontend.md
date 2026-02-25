
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
- add sliding window to varlen ([#172238](https://github.com/pytorch/pytorch/pull/172238))
- remove is_causal flag ([#172245](https://github.com/pytorch/pytorch/pull/172245))
### deprecation
### new features
### improvements
### bug fixes
- Fix AdaptiveMaxPool index error ([#159936](https://github.com/pytorch/pytorch/pull/159936))
- [NATIVE][ReplicationPadding] Fix wrong gradOutput (width is only in the next case, but in this oneâ€¦ ([#172948](https://github.com/pytorch/pytorch/pull/172948))
### performance
### docs
- Add examples to loss function docstrings ([#166296](https://github.com/pytorch/pytorch/pull/166296))
- [Doc] Fix documentation for varlen attention ([#171461](https://github.com/pytorch/pytorch/pull/171461))
- [docs] Clarify that F.embedding weight must be 2-D tensor ([#173093](https://github.com/pytorch/pytorch/pull/173093))
### devs
### Untopiced
- Add type validation for RNN module parameters ([#166980](https://github.com/pytorch/pytorch/pull/166980))
- Updated binary_cross_entropy_with_logits and BCEWithLogitsLoss documeâ€¦ ([#164767](https://github.com/pytorch/pytorch/pull/164767))
- add mechanism to restore default flash attn impl after override ([#169866](https://github.com/pytorch/pytorch/pull/169866))
- Add input_size validation for RNN modules with clear error messages ([#166302](https://github.com/pytorch/pytorch/pull/166302))
- Fix segmentation fault caused by invalid gate weight size in lstm_cell ([#168348](https://github.com/pytorch/pytorch/pull/168348))
- Remove outdated Python code ([#170928](https://github.com/pytorch/pytorch/pull/170928))
- add softmax scaling to varlen attn ([#171199](https://github.com/pytorch/pytorch/pull/171199))
- Improve RNN dtype mismatch error message ([#166946](https://github.com/pytorch/pytorch/pull/166946))
- Added torch.autocast DispatchKey to FlexAttention HOP ([#171160](https://github.com/pytorch/pytorch/pull/171160))
- Fix CPU/CUDA inconsistency in cosine_similarity for large eps ([#169047](https://github.com/pytorch/pytorch/pull/169047))
- Updating CPU code to match CUDA for torch.nn.InstanceNorm2d: Issue#139140 ([#164069](https://github.com/pytorch/pytorch/pull/164069))
- Add weight dtype validation to CUDA nll_loss ([#172018](https://github.com/pytorch/pytorch/pull/172018))
- [FA3] pass max_q and max_k for varlen attn ([#173681](https://github.com/pytorch/pytorch/pull/173681))
- fix IMA bug in FA2 ([#174114](https://github.com/pytorch/pytorch/pull/174114))
- Add remove_duplicate parameter to Module.modules() function ([#174383](https://github.com/pytorch/pytorch/pull/174383))
- [Docs][Typing] Fix parameter type in functional.pyi.in ([#172710](https://github.com/pytorch/pytorch/pull/172710))
- Fix integer overflow in avg_pool with large parameters ([#171710](https://github.com/pytorch/pytorch/pull/171710))
### not user facing
- Remove asserts in nn ([#170327](https://github.com/pytorch/pytorch/pull/170327))
- [Docs] Clarify boolean mask polarity in SDPA (Fixes #170400) ([#170415](https://github.com/pytorch/pytorch/pull/170415))
- [flex_attention] adds support for low precision K/V inputs in compiled mode with GPU ([#170486](https://github.com/pytorch/pytorch/pull/170486))
- [ROCm] Enabled test cases for ROCm ([#171414](https://github.com/pytorch/pytorch/pull/171414))
- [ROCm] Enable MIOpen backend for CTC Loss ([#170749](https://github.com/pytorch/pytorch/pull/170749))
- Do not hardcode `cuda` in `test_warp_softmax_64bit_indexing` ([#172821](https://github.com/pytorch/pytorch/pull/172821))
- Fix incorrect default value for align_corners in interpolate docs ([#172761](https://github.com/pytorch/pytorch/pull/172761))
- [pytorch] Fix RMSNorm eps documentation to match opmath behavior ([#173039](https://github.com/pytorch/pytorch/pull/173039))
- Added test file for FA3 implementation of SDPA ([#172671](https://github.com/pytorch/pytorch/pull/172671))
- Fix test_partial_flat_weights flakiness with relaxed tolerances ([#172201](https://github.com/pytorch/pytorch/pull/172201))
- [docs] Remove misleading GLU activation image ([#173617](https://github.com/pytorch/pytorch/pull/173617))
- [ROCm] forward fix #174087 ([#174300](https://github.com/pytorch/pytorch/pull/174300))
- [ROCm] forward fix #174087, take 2 ([#174388](https://github.com/pytorch/pytorch/pull/174388))
### security
