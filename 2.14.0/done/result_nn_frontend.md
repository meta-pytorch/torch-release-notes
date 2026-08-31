
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
- `torch.nn.LinearCrossEntropyOptions` no longer accepts `acc_policy="balanced"`; use `"compact"` instead ([#188283](https://github.com/pytorch/pytorch/pull/188283))

  The `"balanced"` policy was removed because `"compact"` provides the same weight-gradient accumulation precision with lower memory use on CUDA, already uses the equivalent scratch layout for mixed-precision inputs on other devices, and was never selected by `"auto"`. Constructing the options with `acc_policy="balanced"` now raises `ValueError: invalid acc_policy: 'balanced'; expected one of 'auto', 'accurate', 'compact'`.

  Before:

  ```python
  options = torch.nn.LinearCrossEntropyOptions(acc_policy="balanced")
  loss = torch.nn.functional.linear_cross_entropy(
      input, linear_weight, target, options=options
  )
  ```

  After:

  ```python
  options = torch.nn.LinearCrossEntropyOptions(acc_policy="compact")
  loss = torch.nn.functional.linear_cross_entropy(
      input, linear_weight, target, options=options
  )
  ```
- Dense rank-3 scaled dot-product attention can now select a fused backend instead of always using the math backend ([#192271](https://github.com/pytorch/pytorch/pull/192271))

  Eligible CPU, CUDA/ROCm, and XPU calls are normalized to rank 4 with a singleton batch dimension before backend selection. This can change floating-point numerics, dropout RNG consumption, whether the result is a view, and higher-order-gradient support; fused CUDA backends do not support the second derivatives that the math backend provides. Code that depends on the previous behavior should explicitly select the math backend.

  Version 2.13:

  ```python
  # Rank-3 inputs selected the math backend automatically.
  output = torch.nn.functional.scaled_dot_product_attention(query, key, value)
  ```

  Version 2.14:

  ```python
  from torch.nn.attention import SDPBackend, sdpa_kernel

  with sdpa_kernel(backends=[SDPBackend.MATH]):
      output = torch.nn.functional.scaled_dot_product_attention(
          query, key, value
      )
  ```
- Lp pooling with `norm_type=0` now raises `ValueError`, and module forms validate it during construction ([#187861](https://github.com/pytorch/pytorch/pull/187861))

  `torch.nn.functional.lp_pool1d`, `lp_pool2d`, and `lp_pool3d` previously failed later with `ZeroDivisionError`. `torch.nn.LPPool1d`, `LPPool2d`, and `LPPool3d` also accepted the invalid value at construction and failed only during `forward()`. Use a nonzero norm type; exception-handling code that supports both releases can catch `(ZeroDivisionError, ValueError)` during migration.

  Version 2.13:

  ```python
  try:
      torch.nn.functional.lp_pool2d(x, norm_type=0, kernel_size=2)
  except ZeroDivisionError:
      handle_invalid_norm_type()
  ```

  Version 2.14:

  ```python
  try:
      torch.nn.functional.lp_pool2d(x, norm_type=0, kernel_size=2)
  except ValueError:
      handle_invalid_norm_type()
  ```
### deprecation
### new features
### improvements
- Allow the chunked path of `torch.nn.functional.linear_cross_entropy` to handle probability targets for `reduction="mean"` and `reduction="sum"` when the target dtype matches the input and the target does not require gradients ([#187053](https://github.com/pytorch/pytorch/pull/187053))
- Improve static typing for `torch.nn.Sequential` indexing so integer keys resolve to `Module` and slices resolve to `Sequential` ([#187758](https://github.com/pytorch/pytorch/pull/187758))
- Add the documented `memory_format` overload to `torch.nn.Module.to()` so static type checkers accept calls such as `module.to(memory_format=torch.channels_last)` ([#185117](https://github.com/pytorch/pytorch/pull/185117))
### bug fixes
- Fix memory-efficient scaled dot-product attention backward failing after `torch.autograd.graph.save_on_cpu()` changes an attention mask's aligned strides ([#188246](https://github.com/pytorch/pytorch/pull/188246))
- Fix a CUDA illegal memory access in memory-efficient scaled dot-product attention backward when only the floating-point attention mask requires gradients ([#188302](https://github.com/pytorch/pytorch/pull/188302))
- Make the cuDNN CTC loss backend correctly zero infinite losses and their gradients when `zero_infinity=True` ([#176911](https://github.com/pytorch/pytorch/pull/176911))
- Validate each output dimension for `replication_pad2d` and `replication_pad3d` so excessive negative padding raises a clear error instead of attempting to create a negative-sized tensor ([#184254](https://github.com/pytorch/pytorch/pull/184254))
- Fix silently incorrect CUDA gradients from channels-last `avg_pool2d` when padding is nonzero ([#188345](https://github.com/pytorch/pytorch/pull/188345))
- Make CPU eager and decomposed `torch.nn.functional.softshrink` cast scalar `lambd` values consistently for reduced-precision inputs ([#186358](https://github.com/pytorch/pytorch/pull/186358))
- Prevent CUDA `avg_pool3d` backward from corrupting gradients when an overlapping-window input contains more than `2**31` elements ([#188229](https://github.com/pytorch/pytorch/pull/188229))
- Reject non-positive `kernel_size` values in raw `fractional_max_pool2d` and `fractional_max_pool3d` operations instead of returning `-inf` outputs with invalid indices ([#190480](https://github.com/pytorch/pytorch/pull/190480))
- Support 64-bit indexing for channels-last CUDA bilinear upsampling so outputs with at least `2**31` elements no longer fail with `CUDA error: invalid configuration argument` ([#185788](https://github.com/pytorch/pytorch/pull/185788))
- Fall back to the ATen CUDA implementation when the fused RMSNorm override's normalized dimension exceeds the device's shared-memory capacity, avoiding compiler hangs or crashes ([#186941](https://github.com/pytorch/pytorch/pull/186941))
- Reject invalid `dim` types when constructing `torch.nn.Softmax` or `torch.nn.LogSoftmax` instead of failing later during the forward pass with a confusing overload error ([#185055](https://github.com/pytorch/pytorch/pull/185055))
- Handle misaligned input and weight storage in the fused RMSNorm override instead of raising `Misaligned Tensor data on argument #0` ([#186235](https://github.com/pytorch/pytorch/pull/186235))
- Make CUDA fp16 softmax with `dtype=torch.float32` use the same persistent-kernel range as the fp16-output path, fixing rounding inconsistencies for dimensions between 1025 and 2048 ([#188247](https://github.com/pytorch/pytorch/pull/188247))
### performance
- Avoid materializing zero-filled gradients for unused outputs of chunked `linear_cross_entropy`, substantially reducing backward peak memory ([#187219](https://github.com/pytorch/pytorch/pull/187219))
- Use faster factor-one automatic chunking for `linear_cross_entropy` while capping chunk size so peak memory stays at or below the unchunked implementation ([#187838](https://github.com/pytorch/pytorch/pull/187838))
- Avoid materializing copy-on-write tensors while the fused RMSNorm override checks input and weight alignment ([#189202](https://github.com/pytorch/pytorch/pull/189202))
### docs
- Clarify that `torch.nn.functional.gaussian_nll_loss` uses `eps` to clamp `var` to a minimum rather than adding it to `var` ([#190058](https://github.com/pytorch/pytorch/pull/190058))
- Add deterministic example output to the `torch.nn.Tanh` documentation ([#189390](https://github.com/pytorch/pytorch/pull/189390))
- Correct the documented `mat_b` shape for `torch.nn.functional.grouped_mm` and explain how to pass grouped linear weights ([#191610](https://github.com/pytorch/pytorch/pull/191610))
- Correct the `ceil_mode=True` output-size formula in the `torch.nn.MaxPool1d` documentation ([#188735](https://github.com/pytorch/pytorch/pull/188735))
- Document that repeated calls to `torch.nn.Module.parameters()` return parameters in a deterministic order when the module is unchanged ([#189990](https://github.com/pytorch/pytorch/pull/189990))
### devs
- Integrate Helion with the native-DSL backend registry behind lazy availability and version checks, and add reusable kernel instrumentation for backend development ([#190636](https://github.com/pytorch/pytorch/pull/190636))
### not user facing
- Make `linear_cross_entropy` numerical-tolerance tests device-independent without changing runtime behavior ([#187217](https://github.com/pytorch/pytorch/pull/187217))
- Update the expected ROCm error signature for an out-of-bounds cross-entropy test ([#187613](https://github.com/pytorch/pytorch/pull/187613))
- Refactor `test_nn.py` coverage to run through device-agnostic test infrastructure ([#186200](https://github.com/pytorch/pytorch/pull/186200), [#186204](https://github.com/pytorch/pytorch/pull/186204), [#186219](https://github.com/pytorch/pytorch/pull/186219), [#186228](https://github.com/pytorch/pytorch/pull/186228), [#189534](https://github.com/pytorch/pytorch/pull/189534), [#189535](https://github.com/pytorch/pytorch/pull/189535))
- Relax a borderline BatchNorm gradient tolerance in an AArch64-only test ([#189180](https://github.com/pytorch/pytorch/pull/189180))
- Account for TF32 numerical differences in `linear_cross_entropy` tests ([#190952](https://github.com/pytorch/pytorch/pull/190952))
### security
- Validate `grad_output` shapes in 2D and 3D `grid_sample` backward operations before CPU, CUDA, or MPS kernels can read out of bounds ([#191915](https://github.com/pytorch/pytorch/pull/191915))
- Validate channel counts in `replication_pad1d` and `replication_pad2d` backward operations to prevent out-of-bounds reads and segmentation faults ([#189463](https://github.com/pytorch/pytorch/pull/189463))
- Validate `mean`, `invstd`, and `counts` shapes before CUDA batch-normalization statistics gathering to prevent out-of-bounds reads ([#190005](https://github.com/pytorch/pytorch/pull/190005))
