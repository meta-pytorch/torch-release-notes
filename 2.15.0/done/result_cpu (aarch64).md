
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
- Float32 `torch.sin` and `torch.cos` on Arm CPUs now use SLEEF's 3.5-ULP kernels instead of the 1.0-ULP kernels ([#196315](https://github.com/pytorch/pytorch/pull/196315))

  The vectorized float32 `sin` and `cos` kernels for the NEON (128-bit) and SVE code paths now call
  SLEEF's `u35` variants (maximum error 3.5 ULP) instead of the `u10` variants (maximum error 1.0 ULP).
  This puts Arm in the same accuracy class as the x86 AVX2 kernels and makes these ops 1.7x-2.4x
  faster on Neoverse V1/V2. In the PR's measurements, results stayed within 1 ULP of the correctly
  rounded value on NEON/SVE128 and within 2 ULP on SVE256. float16 and bfloat16 results were
  unchanged after rounding to the output dtype.

  You may see this change if you compare float32 `sin`/`cos` results on Arm bit-for-bit against values
  recorded with an earlier release (golden files, `torch.equal`, or `assert_close` with `rtol=0, atol=0`).
  Comparisons that use the default float32 tolerances of `torch.testing.assert_close` are not affected.
  There is no switch to restore the `u10` kernels. If you need tighter accuracy, compute in float64
  and cast back.

  Version 2.14 (SVE256, SLEEF u10):
  ```python
  >>> x = torch.full((256,), float.fromhex("0x1.0c1524p-1"))  # float32 pi/6
  >>> x.cos()[0].item().hex()  # correctly rounded result
  '0x1.bb67ae0000000p-1'
  ```

  Version 2.15 (SVE256, SLEEF u35):
  ```python
  >>> x.cos()[0].item().hex()  # 1 ULP away
  '0x1.bb67b00000000p-1'
  >>> x.double().cos().float()[0].item().hex()  # compute in float64 for a correctly rounded result
  '0x1.bb67ae0000000p-1'
  ```
### deprecation
### new features
### improvements
- Make float32 `sum` and `norm` on NEON use the same number of accumulators as AVX2 and SVE256, so they give bitwise-identical results across these CPUs. Results on NEON may differ from 2.14 in the last bits ([#197037](https://github.com/pytorch/pytorch/pull/197037), [#197252](https://github.com/pytorch/pytorch/pull/197252))
### bug fixes
- Fix out-of-range float32, float16 and bfloat16 to `uint8` conversions on Arm giving different results from x86 and from strided copies. Contiguous `x.byte()` used a saturating conversion (`-1 -> 0`), while other paths wrap through int64 (`-1 -> 255`) ([#196646](https://github.com/pytorch/pytorch/pull/196646), [#198744](https://github.com/pytorch/pytorch/pull/198744))
- Fix `linspace` on CPU (and `linspace`/`logspace` on CUDA) losing precision for float16 and bfloat16 by computing the step in the higher-precision accumulate type ([#198415](https://github.com/pytorch/pytorch/pull/198415))
- Fix the meta function of `torch.ops.aten._dyn_quant_pack_4bit_weight` disagreeing with the eager kernel on Arm CPUs without the dot-product extension, which broke `torch.compile` of 4-bit dynamically quantized matmul ([#197518](https://github.com/pytorch/pytorch/pull/197518))
- Fix matmuls that go through the oneDNN/ACL path on aarch64 (for example `addmm`, `__rmatmul__`, `cholesky_inverse` and `cholesky_solve`) materializing copy-on-write (lazily cloned) inputs ([#198625](https://github.com/pytorch/pytorch/pull/198625))
### performance
- Linux aarch64 CUDA builds are now optimized with LLVM BOLT by default ([#186245](https://github.com/pytorch/pytorch/pull/186245))

  BOLT is a post-link optimizer that reorders the code in the PyTorch shared libraries based on
  execution profiles. Profiles collected on a curated set of workloads are checked into the repository
  (`cmake/bolt_profiles/`). The new `USE_LLVM_BOLT` build option defaults to ON for Linux + aarch64 +
  CUDA builds when `llvm-bolt` 21 or newer is found and `USE_PRIORITIZED_TEXT_FOR_LD` is enabled (the
  default on Linux aarch64); otherwise it defaults to OFF.
  The PR reports up to 30% faster end-to-end workloads, with a few workloads up to 3%
  slower. The gains will shrink as the code drifts away from the committed profiles until the profiles
  are refreshed. When building from source, the unoptimized libraries are kept in a `prebolt/`
  subdirectory of the build tree. Set `USE_LLVM_BOLT=0` to opt out.
- Use NEON `vreinterpretq` intrinsics for casts between `Vectorized<T>` types on Arm instead of going through memory ([#196776](https://github.com/pytorch/pytorch/pull/196776))
- Use the native GEMV path instead of oneDNN/ACL for single-column (`n == 1`) BF16 GEMMs on Arm Neoverse. This shape is common in single-token decode; the PR reports about 5x faster GPT-2 BF16 decode on Graviton 4 and 5 ([#198411](https://github.com/pytorch/pytorch/pull/198411))
- Dispatch non-contiguous FP16 matmuls to the oneDNN ACL GEMM kernels instead of the reference implementation on AArch64 ([#198498](https://github.com/pytorch/pytorch/pull/198498))
- Add NEON implementations of float <-> double vectorized conversion and of `Vectorized<float>::reduce_max` ([#197153](https://github.com/pytorch/pytorch/pull/197153), [#196716](https://github.com/pytorch/pytorch/pull/196716))
### docs
### devs
- Add the `AT_VEC_CUSTOM_MATH` build flag, which leaves the vectorized math functions on AVX2, AVX512, NEON and SVE256 declared but not defined (instead of using SLEEF), so that other math libraries can be plugged in ([#197419](https://github.com/pytorch/pytorch/pull/197419))
### not user facing
### security
