
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
### bug fixes
- save_on_cpu memeff_bias ([#188246](https://github.com/pytorch/pytorch/pull/188246))
- Allow grads for attn_bias only ([#188302](https://github.com/pytorch/pytorch/pull/188302))
- Fix behavor of CTC loss cuDNN backend when `zero_infinity=True` ([#176911](https://github.com/pytorch/pytorch/pull/176911))
- Fix `replication_pad{2d,3d}` meta accepting negative output dims ([#184254](https://github.com/pytorch/pytorch/pull/184254))
- fix(grid_sampler): Validate grad_output shape in 2D/3D backward ([#191915](https://github.com/pytorch/pytorch/pull/191915))
### performance
### docs
- Fix gaussian_nll_loss eps docstring: it clamps var, not adds ([#190058](https://github.com/pytorch/pytorch/pull/190058))
### devs
### Untopiced
- linear_cross_entropy: support probability targets on the chunked path ([#187053](https://github.com/pytorch/pytorch/pull/187053))
- linear_cross_entropy: remove the `balanced` acc_policy ([#188283](https://github.com/pytorch/pytorch/pull/188283))
- Fix avg_pool2d CUDA backward for channels_last inputs with padding ([#188345](https://github.com/pytorch/pytorch/pull/188345))
- Fix output mismtach for F.softshrink with bfloat16 and float scalar ([#186358](https://github.com/pytorch/pytorch/pull/186358))
- Fix segfault in replication_pad{1d,2d}_backward on channel mismatch ([#189463](https://github.com/pytorch/pytorch/pull/189463))
- Show example output in nn.Tanh docstring ([#189390](https://github.com/pytorch/pytorch/pull/189390))
- Fix 64-bit indexing in avg_pool3d backward atomic kernel ([#188229](https://github.com/pytorch/pytorch/pull/188229))
- [ATen] Reject non-positive kernel_size in fractional_max_pool ([#190480](https://github.com/pytorch/pytorch/pull/190480))
- [native dsl] Add Helion backend integration ([#190636](https://github.com/pytorch/pytorch/pull/190636))
- Fix OOB read in batch_norm_gather_stats with inconsistent invstd ([#190005](https://github.com/pytorch/pytorch/pull/190005))
- Fix grouped_mm docs: mat_b shape is (num_groups, K, N) ([#191610](https://github.com/pytorch/pytorch/pull/191610))
- Support 64-bit indexing in channels_last bilinear upsampling ([#185788](https://github.com/pytorch/pytorch/pull/185788))
- [SDPA] Enable fused CUDA backends for rank-3 inputs ([#192271](https://github.com/pytorch/pytorch/pull/192271))
### not user facing
- Fall back to aten in the RMSNorm override when N exceeds the smem budget ([#186941](https://github.com/pytorch/pytorch/pull/186941))
- [BE] Make linear_cross_entropy compact gradient ULP caps device-independent ([#187217](https://github.com/pytorch/pytorch/pull/187217))
- linear_cross_entropy: do not materialize gradients for unused chunked-op outputs ([#187219](https://github.com/pytorch/pytorch/pull/187219))
- Validate dim type in Softmax and LogSoftmax constructors ([#185055](https://github.com/pytorch/pytorch/pull/185055))
- [ROCM] Fix test_cross_entropy_loss_2d_out_of_bounds_class ([#187613](https://github.com/pytorch/pytorch/pull/187613))
- [Native DSL] Fix RMSNorm override on misaligned base pointers, add regression tests ([#186235](https://github.com/pytorch/pytorch/pull/186235))
- Add Sequential.__getitem__ overloads for precise int/slice typing ([#187758](https://github.com/pytorch/pytorch/pull/187758))
- [nn] Raise ValueError for norm_type=0 in lp_pool{1,2,3}d and LPPoolNd ([#187861](https://github.com/pytorch/pytorch/pull/187861))
- linear_cross_entropy: factor-1 chunking with an N*V/4D memory cap; simplified auto resolution ([#187838](https://github.com/pytorch/pytorch/pull/187838))
- Align softmax path for half_to_float ([#188247](https://github.com/pytorch/pytorch/pull/188247))
- [dynamo, nested graph breaks] fix empty nn.Module hook dict reconstruction ([#187088](https://github.com/pytorch/pytorch/pull/187088))
- [Test] Refactor test/test_nn.py to be device-agnostic [1/N] ([#186200](https://github.com/pytorch/pytorch/pull/186200))
- [Test] Refactor test/test_nn.py to be device-agnostic [2/N] ([#186204](https://github.com/pytorch/pytorch/pull/186204))
- [dynamo, nested graph breaks] fix empty nn.Module hook dict reconstruction ([#187088](https://github.com/pytorch/pytorch/pull/187088))
- [DOC] Fix math formula for `nn.MaxPool1d` output size calculation ([#188735](https://github.com/pytorch/pytorch/pull/188735))
- [Test] Refactor test/test_nn.py to be device-agnostic [3/N] ([#186219](https://github.com/pytorch/pytorch/pull/186219))
- [Test] Refactor test/test_nn.py to be device-agnostic [4/N] ([#186228](https://github.com/pytorch/pytorch/pull/186228))
- Relax bias.grad tolerance in test_batchnorm_nhwc_cpu (aarch64 flake) ([#189180](https://github.com/pytorch/pytorch/pull/189180))
- [Test] Refactor test/test_nn.py to be device-agnostic [5/N] ([#189534](https://github.com/pytorch/pytorch/pull/189534))
- Add keepdim parameter to cosine_similarity ([#189654](https://github.com/pytorch/pytorch/pull/189654))
- Docs: Clarify deterministic ordering of module.parameters() to Fixes #188389 ([#189990](https://github.com/pytorch/pytorch/pull/189990))
- [Test] Refactor test/test_nn.py to be device-agnostic [6/N] ([#189535](https://github.com/pytorch/pytorch/pull/189535))
- [TF32] Account for TF32 in `linear_cross_entropy` tests ([#190952](https://github.com/pytorch/pytorch/pull/190952))
- [CuteDSL][RMSNorm] use const_data_ptr for alignment check ([#189202](https://github.com/pytorch/pytorch/pull/189202))
- nn: add missing memory_format overload to Module.to() ([#185117](https://github.com/pytorch/pytorch/pull/185117))
### security
