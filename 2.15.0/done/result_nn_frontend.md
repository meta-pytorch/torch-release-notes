
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
- Add `torch.nn.functional.scaled_addmm` and its in-place variant `scaled_addmm_`, the `addmm` analogue of `torch.nn.functional.scaled_mm` ([#195409](https://github.com/pytorch/pytorch/pull/195409))
- Support `torch.nn.functional.scaled_addmm` and `scaled_addmm_` under `torch.compile`, lowered through Inductor's extern-kernel fallback with reinplacing of the functional form ([#195410](https://github.com/pytorch/pytorch/pull/195410)) (may belong in nn_frontend, next to #195409)

  `scaled_addmm(input, mat1, mat2, scale_a, scale_recipe_a, scale_b, scale_recipe_b, ..., *, beta=1.0, alpha=1.0)` computes `beta * input + alpha * scaled_mm(mat1, mat2)` in a single cuBLASLt GEMM on CUDA. The scaling recipes and swizzles have the same meaning as in `scaled_mm` (tensorwise and rowwise FP8, DeepSeek-style block scaling on SM90, MXFP8 and NVFP4), and the result has the dtype of `input` (`float16`, `bfloat16` or `float32`). `scaled_addmm_` accumulates into `input` in place, which suits accumulating weight gradients over microbatches. ROCm is not supported.

  ```python
  import torch.nn.functional as F
  from torch.nn.functional import ScalingType

  a, sa, b, sb = chunks[0]
  wgrad = F.scaled_mm(a, b.t(), sa, ScalingType.TensorWise, sb, ScalingType.TensorWise, output_dtype=torch.float32)
  for a, sa, b, sb in chunks[1:]:
      F.scaled_addmm_(wgrad, a, b.t(), sa, ScalingType.TensorWise, sb, ScalingType.TensorWise)  # wgrad += a @ b.t()
  ```

### improvements
- Support probability (soft-label) targets with `reduction="none"` on the chunked path of `torch.nn.functional.linear_cross_entropy`, which previously fell back to the unchunked reference implementation ([#188296](https://github.com/pytorch/pytorch/pull/188296))
- Allow `scaled_dot_product_attention` to use FlashAttention-4 with different query/key and value head dimensions (e.g. DeepSeek-style Q/K=192, V=128), and size the output by the value head dimension ([#193039](https://github.com/pytorch/pytorch/pull/193039))
- Support `F.interpolate(..., mode="bicubic")` backward under `torch.use_deterministic_algorithms(True)` by using a deterministic decomposition ([#193707](https://github.com/pytorch/pytorch/pull/193707))
- Support `mode="bicubic"` with 5-D (volumetric) input in `torch.nn.functional.grid_sample` on CPU and CUDA, including backward and double backward ([#194787](https://github.com/pytorch/pytorch/pull/194787))
- Add the missing `weight` argument to the `torch.nn.functional.mse_loss` type stub ([#196126](https://github.com/pytorch/pytorch/pull/196126))
- Allow `torch.nn.attention.varlen.varlen_attn` to dispatch causal attention to cuDNN, using the same bottom-right causal alignment as the Flash backend ([#193630](https://github.com/pytorch/pytorch/pull/193630))
### bug fixes
- Fix `LSTMCell`, `GRUCell` and `RNNCell` segfaulting when the input and hidden state have different numbers of dimensions; they now raise an error ([#191232](https://github.com/pytorch/pytorch/pull/191232))
- Fix `torch.ops.aten.native_batch_norm` segfaulting on CPU in eval mode when `running_mean`/`running_var` are `None`; it now raises `running_mean must be defined in evaluation mode` ([#194031](https://github.com/pytorch/pytorch/pull/194031))
- Fix `weight_norm` on CPU producing a `nan` gradient for `g` (and reading through a null pointer) for empty inputs such as `nn.Linear(0, 1)` ([#192179](https://github.com/pytorch/pytorch/pull/192179))
- Fix `rms_norm` failing when a C++ caller passes an engaged optional holding an undefined weight; it is now treated as no weight, matching `layer_norm` ([#195574](https://github.com/pytorch/pytorch/pull/195574))
- Fix the meta and reference implementations of `pixel_shuffle`/`pixel_unshuffle` raising `ZeroDivisionError` or an unclear assertion for a non-positive factor; they now raise the same error as eager ([#195224](https://github.com/pytorch/pytorch/pull/195224))
- Fix `Module.to()` on a `meta`-device module dropping the "use `Module.to_empty()`" guidance from the error when `TORCH_SHOW_CPP_STACKTRACES=1` ([#191151](https://github.com/pytorch/pytorch/pull/191151))
- Fix `grid_sample` returning zeros when the AVX512 CPU kernel is used ([#197635](https://github.com/pytorch/pytorch/pull/197635))
- Fix wrong CUDA gradients from `softmax`/`log_softmax` over a non-last dimension on tensors large enough to need 64-bit indexing ([#188031](https://github.com/pytorch/pytorch/pull/188031))
- Fix an out-of-bounds write and invalid gradients in CUDA `layer_norm` backward for very large batch sizes with a multi-dimensional `normalized_shape` or no weight ([#193016](https://github.com/pytorch/pytorch/pull/193016))
- Fix ROCm `layer_norm` normalizing the wrong rows (and leaving trailing rows unwritten) for very large inputs due to a 32-bit offset overflow ([#199438](https://github.com/pytorch/pytorch/pull/199438))
- Fix the CUDA memory-efficient `scaled_dot_product_attention` kernels failing when batch size or number of heads exceeds the CUDA grid limit ([#199594](https://github.com/pytorch/pytorch/pull/199594))
- Fix cuDNN and MIOpen RNN backward silently producing wrong gradients when the saved forward output is not laid out as `(T, B, H)`-contiguous (e.g. under compiled autograd) ([#198773](https://github.com/pytorch/pytorch/pull/198773))
- Fix ROCm (MIOpen) multi-layer `nn.RNN`/`nn.LSTM`/`nn.GRU` with `dropout > 0` reusing the same dropout mask on every step, which stalled training ([#189285](https://github.com/pytorch/pytorch/pull/189285))
- Fix FlashAttention-4 variable-length attention defaulting to one split instead of automatic split selection ([#198872](https://github.com/pytorch/pytorch/pull/198872))
- Fix `torch.max_pool1d` segfaulting on out-of-range integer `kernel_size`/`stride`/`dilation` values due to integer overflow in the output-shape checks; these now raise an error, and the same overflow fix makes `slow_conv_dilated2d` and `F.unfold` reject such sizes instead of returning empty results or failing later ([#194112](https://github.com/pytorch/pytorch/pull/194112))
- Fix `varlen_attn` ignoring the active `torch.nn.attention.sdpa_kernel` backend selection (e.g. running cuDNN when Flash was forced) and possibly choosing a different backend for backward than for forward ([#193631](https://github.com/pytorch/pytorch/pull/193631))
- Fix CUDA memory-efficient `scaled_dot_product_attention` with bottom-right causal masking (`torch.nn.attention.bias.causal_lower_right`) when the query is longer than the key, where masking was disabled for some query blocks and fully masked rows were left uninitialized ([#193632](https://github.com/pytorch/pytorch/pull/193632))
- Fix several defects in the cuDNN backend of `varlen_attn`, including silently wrong results or faults for misaligned inputs and a crash in backward with padded `grad_out` ([#194818](https://github.com/pytorch/pytorch/pull/194818))
- Fix packed RNNs dereferencing device memory on the host when falling back from cuDNN/MIOpen to the native implementation, by validating `batch_sizes` before backend dispatch ([#197560](https://github.com/pytorch/pytorch/pull/197560))
### performance
- Speed up `nn.Module.__call__` by about 15% by checking whether JIT tracing is active with a cheaper call ([#196236](https://github.com/pytorch/pytorch/pull/196236))
- Avoid an extra copy in backward when the output of an N-D `F.linear` is modified in place ([#194077](https://github.com/pytorch/pytorch/pull/194077))
- Add a channels-last (NHWC) CUDA `GroupNorm` kernel so channels-last inputs no longer produce contiguous outputs ([#191945](https://github.com/pytorch/pytorch/pull/191945))
- Use the CuTeDSL (Quack) fused RMSNorm kernels on sm12x GPUs, with up to about 2x faster backward ([#192400](https://github.com/pytorch/pytorch/pull/192400))
- Speed up the cuDNN path of `varlen_attn` by reusing shared query/key sequence metadata and, with cuDNN 9.24+, passing cumulative sequence lengths to cuDNN directly instead of launching conversion kernels ([#194834](https://github.com/pytorch/pytorch/pull/194834), [#194906](https://github.com/pytorch/pytorch/pull/194906))
- Reduce per-chunk overhead in the CuTeDSL implementation of chunked `torch.nn.functional.linear_cross_entropy` (about 6% faster on H100 and 10% on B200) ([#196134](https://github.com/pytorch/pytorch/pull/196134))
### docs
- Fix the `linear_cross_entropy` reference implementation snippet in its docstring and document that bias is supported with probability targets ([#198941](https://github.com/pytorch/pytorch/pull/198941), [#188433](https://github.com/pytorch/pytorch/pull/188433))
- Fix the `nn.RNN` documentation example so that it supports a backward pass ([#173888](https://github.com/pytorch/pytorch/pull/173888))
### devs
### Untopiced
### not user facing
- Refactor `test/test_nn.py` to be device-agnostic and add hardware classification ([#189536](https://github.com/pytorch/pytorch/pull/189536), [#189538](https://github.com/pytorch/pytorch/pull/189538), [#194038](https://github.com/pytorch/pytorch/pull/194038), [#194045](https://github.com/pytorch/pytorch/pull/194045), [#194191](https://github.com/pytorch/pytorch/pull/194191), [#194863](https://github.com/pytorch/pytorch/pull/194863), [#198467](https://github.com/pytorch/pytorch/pull/198467), [#198848](https://github.com/pytorch/pytorch/pull/198848), [#198859](https://github.com/pytorch/pytorch/pull/198859))
- Fix test tolerances, skips and expected failures on ROCm MI200, GB200 and MPS ([#192993](https://github.com/pytorch/pytorch/pull/192993), [#193949](https://github.com/pytorch/pytorch/pull/193949), [#194726](https://github.com/pytorch/pytorch/pull/194726), [#197904](https://github.com/pytorch/pytorch/pull/197904), [#198689](https://github.com/pytorch/pytorch/pull/198689), [#199006](https://github.com/pytorch/pytorch/pull/199006))
- Consolidate device-side assert stderr checks into a shared test helper ([#193613](https://github.com/pytorch/pytorch/pull/193613))
- Don't use blank targets in cuDNN `CTCLoss` tests ([#195620](https://github.com/pytorch/pytorch/pull/195620))
- Clear the `ModuleTest`/`CriterionTest` argument cache at every entry point so test variants are reproducible ([#196609](https://github.com/pytorch/pytorch/pull/196609))
- Extract `linear_cross_entropy` input checks so backend overrides can reuse them ([#195331](https://github.com/pytorch/pytorch/pull/195331))
### security
