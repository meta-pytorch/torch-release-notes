
# Release Notes worksheet quantization

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

## quantization
### bc breaking
### deprecation
### new features
- Add `_scaled_mm_v2` API ([#164141](https://github.com/pytorch/pytorch/pull/164141))
- Add `scaled_grouped_mm_v2` and python API ([#165154](https://github.com/pytorch/pytorch/pull/165154))
- Add `embedding_bag_byte_prepack_with_rowwise_min_max` and `embedding_bag_{2/4}bit_prepack_with_rowwise_min_max` ([#162924](https://github.com/pytorch/pytorch/pull/162924))
- Add `MXFP4` support for `_scaled_grouped_mm_v2` via. FBGEMM kernels ([#166530](https://github.com/pytorch/pytorch/pull/166530))

### improvements
- `half` and `bf16` support for `fused_moving_avg_obs_fake_quant` ([#162620](https://github.com/pytorch/pytorch/pull/162620), [#164175](https://github.com/pytorch/pytorch/pull/164175))
- `bf16` support for `fake_quantize_learnable_per_channel_affine` ([#165098](https://github.com/pytorch/pytorch/pull/165098))
- `bf16` support for backward of `torch._fake_quantize_learnable_per_tensor_affine` ([#165362](https://github.com/pytorch/pytorch/pull/165362))
- Add `NVFP4` two-level scaling to `scaled_mm` ([#165774](https://github.com/pytorch/pytorch/pull/165774))
- Add support for `fp8_input`/`fp8_weight`/`bf16_bias` and `bf16_output` for fp8 qconv in CPU ([#167611](https://github.com/pytorch/pytorch/pull/167611))
- Make the `torch.float4_e2m1fn_x2` dtype support equality comparisons ([#169575](https://github.com/pytorch/pytorch/pull/169575))
- add `copy_` support for `torch.float4_e2m1fn_x2` dtype ([#169595](https://github.com/pytorch/pytorch/pull/169595))

### bug fixes
### performance
- Make prepare and convert faster by caching ([#162550](https://github.com/pytorch/pytorch/pull/162550))
- Add onednn context cache for CPU qlinear to improve performance ([#168150](https://github.com/pytorch/pytorch/pull/168150))

### docs
- Document some quantization public apis ([#165160](https://github.com/pytorch/pytorch/pull/165160))
- Add missing method docstrings for pytorch quantization classes ([#165199](https://github.com/pytorch/pytorch/pull/165199))

### devs
### Untopiced

### not user facing
### security
