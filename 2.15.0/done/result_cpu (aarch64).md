
# Release Notes worksheet cpu (aarch64)

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

## cpu (aarch64)
### bc breaking
- Float32 `torch.sin` and `torch.cos` on Arm CPUs (NEON and SVE) now use SLEEF's 3.5-ULP kernels instead of the 1.0-ULP kernels, matching the accuracy of the x86 AVX2 implementation and running 1.7x-2.4x faster on Neoverse V1/V2 ([#196315](https://github.com/pytorch/pytorch/pull/196315))

  Float32 `sin` and `cos` results on Arm can now differ from earlier releases in the last bits. Bit-for-bit comparisons against stored golden outputs, `torch.equal`, or `torch.testing.assert_close` with `rtol=0, atol=0` may fail; default `assert_close` tolerances are unaffected. There is no switch to restore the previous kernels; if you need tighter accuracy, compute in float64 and cast back.

  Version 2.14:
  ```python
  >>> x.cos()  # float32 on Arm: within 1 ULP
  ```

  Version 2.15:
  ```python
  >>> x.cos()  # float32 on Arm: within 3.5 ULP
  >>> x.double().cos().float()  # workaround: compute in higher precision
  ```
### deprecation
### new features
### improvements
- Make float32 `sum` and `norm` on NEON use the same accumulation order as AVX2 and SVE256, so results are bitwise identical across these CPU types; NEON results can differ from earlier releases in the last bits ([#197037](https://github.com/pytorch/pytorch/pull/197037), [#197252](https://github.com/pytorch/pytorch/pull/197252))
### bug fixes
- Fix contiguous float32, float16 and bfloat16 to `uint8` conversions of out-of-range values (for example `Tensor.byte()` on `-1`) on Arm CPUs saturating to `0` instead of wrapping around to `255` as on x86 and for strided inputs ([#196646](https://github.com/pytorch/pytorch/pull/196646), [#198744](https://github.com/pytorch/pytorch/pull/198744))
- Fix `torch.compile` of 4-bit dynamically quantized matmul on Arm CPUs without the dot-product extension ([#197518](https://github.com/pytorch/pytorch/pull/197518))
### performance
- Optimize `libtorch` code layout with LLVM BOLT, using profiles shipped in the repository. The new `USE_LLVM_BOLT` build option is on by default for Linux aarch64 CUDA builds when `llvm-bolt` 21 or newer is found and `USE_PRIORITIZED_TEXT_FOR_LD` is enabled, giving up to 30% faster workloads in some cases and up to 3% slower in others; set `USE_LLVM_BOLT=0` to opt out in source builds ([#186245](https://github.com/pytorch/pytorch/pull/186245))
- Use the native GEMV path for single-column (`n == 1`) BF16 GEMMs on Arm Neoverse CPUs built with oneDNN ACL, for about 5x faster single-thread GPT-2 BF16 decode on Graviton 4 and 5 (1.4x-2.7x with 8-64 threads on Graviton 5) ([#198411](https://github.com/pytorch/pytorch/pull/198411))
- Dispatch non-contiguous FP16 matmuls to oneDNN ACL GEMM kernels instead of the reference implementation on AArch64 ([#198498](https://github.com/pytorch/pytorch/pull/198498))
### docs
### devs
- Add the `AT_VEC_CUSTOM_MATH` compile definition, which hides the built-in vectorized math functions on AVX2, AVX512, NEON and SVE256 builds so that a vectorized math library other than SLEEF can be plugged in ([#197419](https://github.com/pytorch/pytorch/pull/197419))
### not user facing
- Stop oneDNN/ACL matmuls on aarch64 from materializing copy-on-write inputs ([#198625](https://github.com/pytorch/pytorch/pull/198625))
- Use NEON `vreinterpretq` intrinsics for casts between `Vectorized<T>` types on Arm ([#196776](https://github.com/pytorch/pytorch/pull/196776))
- Add NEON implementations of float <-> double vectorized conversion and of `Vectorized<float>::reduce_max` ([#197153](https://github.com/pytorch/pytorch/pull/197153), [#196716](https://github.com/pytorch/pytorch/pull/196716))
### security
