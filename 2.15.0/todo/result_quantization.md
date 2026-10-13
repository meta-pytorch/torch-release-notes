
# Release Notes worksheet quantization

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

## quantization
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [qnnpack] Add 1..4x8 dynamic-quant aarch64 q8gemm microkernel for small batch (#193595) ([#193595](https://github.com/pytorch/pytorch/pull/193595))
- Fix typos and grammar in comments and docstrings ([#193963](https://github.com/pytorch/pytorch/pull/193963))
- Cleanup/cuda indexing stale remnants ([#189338](https://github.com/pytorch/pytorch/pull/189338))
- [CUDA][ROCm] Support pruned lookups in quantized embedding_bag_byte_rowwise_offsets (#192573) ([#192573](https://github.com/pytorch/pytorch/pull/192573))
- Fix typos in comments and docstrings ([#194627](https://github.com/pytorch/pytorch/pull/194627))
- Fix grammatical errors in comments and docstrings ([#194565](https://github.com/pytorch/pytorch/pull/194565))
- [CUDA][ROCm] Support pruned lookups in quantized embedding_bag_byte_rowwise_offsets (#192573) ([#192573](https://github.com/pytorch/pytorch/pull/192573))
- [CUDA][ROCm] Support pruned lookups in quantized embedding_bag_byte_rowwise_offsets ([#194934](https://github.com/pytorch/pytorch/pull/194934))
- [BE][Ez]: Add missing std::moves in aten and torch/csrc ([#195032](https://github.com/pytorch/pytorch/pull/195032))
- [BE][Ez]: Use cuda::std::midpoint for clarity, safety and perf ([#196356](https://github.com/pytorch/pytorch/pull/196356))
- [fc_quantization] Fix the problematic weights deletion (#194292) ([#194292](https://github.com/pytorch/pytorch/pull/194292))
### not user facing
- Modernize map usage in ATen ([#179397](https://github.com/pytorch/pytorch/pull/179397))
- [2/N][Test] Refactor `TestFPGMPruner` in `torch_ao_sparsity.py` ([#191200](https://github.com/pytorch/pytorch/pull/191200))
- Use C++20 <bit> instead of c10::llvm bit helpers in c10 ([#187002](https://github.com/pytorch/pytorch/pull/187002))
- [3/N][Test] Enable `torch_ao_sparsity.py` for XPU ([#191202](https://github.com/pytorch/pytorch/pull/191202))
- Use C++20 <bit> instead of c10::llvm bit helpers in c10 ([#187002](https://github.com/pytorch/pytorch/pull/187002))
- [Test] Make sigmoid_add extension test device-agnostic in test_cpp_extensions_aot.py ([#185648](https://github.com/pytorch/pytorch/pull/185648))
- [Testcase Refactoring] [quantization] Annotate TestFakeQuantize with hw_classification = GENERIC ([#193013](https://github.com/pytorch/pytorch/pull/193013))
- [Testcase Refactoring][quantization][eager] Add GENERIC hw_classification to test_equalize_eager.py ([#193650](https://github.com/pytorch/pytorch/pull/193650))
- [Testcase Refactoring] Annotate TestActivationSparsifier with HardwareClassification.GENERIC ([#192479](https://github.com/pytorch/pytorch/pull/192479))
- [Testcase Refactoring][ao][sparsity] Add GENERIC hw_classification to test_scheduler.py ([#193588](https://github.com/pytorch/pytorch/pull/193588))
- [Testcase Refactoring] Decouple TestBaseDataScheduler for out-of-tree backends ([#193848](https://github.com/pytorch/pytorch/pull/193848))
- [Testcase Refactoring] Classify sparse qlinear packed params tests as generic ([#193177](https://github.com/pytorch/pytorch/pull/193177))
- [Testcase Refactoring] Add hardware classification to nonuniform observer tests ([#192965](https://github.com/pytorch/pytorch/pull/192965))
- [Testcase Refactoring] Add hardware classification to APoT quantizer tests ([#193000](https://github.com/pytorch/pytorch/pull/193000))
- [Testcase Refactoring] Add hardware classification to sparsity utility tests ([#192964](https://github.com/pytorch/pytorch/pull/192964))
- [Testcase Refactoring][Quantization] Add hw_classification to test_top_level_apis.py ([#194500](https://github.com/pytorch/pytorch/pull/194500))
- [Testcase Refactoring] Add hardware classification to quantization utility tests ([#193001](https://github.com/pytorch/pytorch/pull/193001))
- [Testcase Refactoring] [quantization] Annotate TestModelNumericsEager with hw_classification = GENERIC ([#193014](https://github.com/pytorch/pytorch/pull/193014))
- [Testcase Refactoring][quantization][eager] Add GENERIC hw_classification to test_quantize_eager_ptq.py ([#195998](https://github.com/pytorch/pytorch/pull/195998))
- [Testcase Refactoring] Classify sparsity parametrization tests by hardware ([#195965](https://github.com/pytorch/pytorch/pull/195965))
- [Testcase Refactoring][ao][sparsity] Add CPU hw_classification to spa… ([#194925](https://github.com/pytorch/pytorch/pull/194925))
- Use COMPILE_OPTIONS property instead of COMPILE_FLAGS ([#197814](https://github.com/pytorch/pytorch/pull/197814))
- [Testcase Refactoring] Decouple TestDeprecatedJitQuantized for out-of-tree backends ([#194192](https://github.com/pytorch/pytorch/pull/194192))
- [Testcase Refactoring] Make data sparsifier tests device agnostic ([#195433](https://github.com/pytorch/pytorch/pull/195433))
- [Testcase Refactoring][quantization][eager] Add CPU hw_classification to test_bias_correction_eager.py ([#195989](https://github.com/pytorch/pytorch/pull/195989))
- [Testcase Refactoring][quantization][jit] Add CPU hw_classification to test_fusion_passes.py ([#194440](https://github.com/pytorch/pytorch/pull/194440))
- cmake: Use dedicated functions for defining macros ([#198957](https://github.com/pytorch/pytorch/pull/198957))
- [Testcase Refactoring] Add HardwareClassification GENERIC to test_backward_compatibility.py ([#197794](https://github.com/pytorch/pytorch/pull/197794))
- [Testcase Refactoring] Add HardwareClassification GENERIC to test_quantization_fx.py ([#197791](https://github.com/pytorch/pytorch/pull/197791))
- [Test][XPU] Enable `test_bits.py` and `test_floatx.py` quantization tests for XPU and remove XPU skip from `test_memory_profiler.py` ([#190889](https://github.com/pytorch/pytorch/pull/190889))
- [Testcase Refactoring] Add hardware classification to APoT linear tests ([#192636](https://github.com/pytorch/pytorch/pull/192636))
- [fbgemm] Add embedding-bag byte cache re-key regression test ([#199060](https://github.com/pytorch/pytorch/pull/199060))
- Upgrade submodule oneDNN to v3.13 ([#196712](https://github.com/pytorch/pytorch/pull/196712))
- Reland AArch64 quantized engine gating and guard FBGEMM dispatch ([#199121](https://github.com/pytorch/pytorch/pull/199121))
### security
