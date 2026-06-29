
# Release Notes worksheet rocm

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

## rocm
### bc breaking
### deprecation
### new features
- Enable external events in CUDA graphs ([#178264](https://github.com/pytorch/pytorch/pull/178264))
- Enable GPU Address Sanitizer build ([#183792](https://github.com/pytorch/pytorch/pull/183792), [#176461](https://github.com/pytorch/pytorch/pull/176461))
- Improve inductor GEMM search space performance using Origami project ([#172512](https://github.com/pytorch/pytorch/pull/172512))
- Use CMake native HIP language support, enable_language(HIP) ([#180485](https://github.com/pytorch/pytorch/pull/180485))
- New Inductor benchmarker based on Torch Profiler ([#175097](https://github.com/pytorch/pytorch/pull/175097))
### improvements
- Additional cub::DeviceHistogram hipify mappings ([#180433](https://github.com/pytorch/pytorch/pull/180433))
- SDPA improvements via AOTriton 0.12b: head_dim != head_dim_v, use_deterministic_algorithims, gfx1100 and gfx1151 promoted out of experimental, partial FAv3 support on gfx950 ([#184288](https://github.com/pytorch/pytorch/pull/184288))
### bug fixes
- Support TheRock wheel distribution in _find_rocm_home ([#180723](https://github.com/pytorch/pytorch/pull/180723))
- Fix warpMergeSortTopK padding sentinel for integer dtypes ([#182212](https://github.com/pytorch/pytorch/pull/182212))
- Guard ck_group_gemm on USE_ROCM_CK_GEMM ([#182615](https://github.com/pytorch/pytorch/pull/182615))
- Fix large arange launch ([#182657](https://github.com/pytorch/pytorch/pull/182657))
- Fix triu/tril for 64-bit indexing for large matrices ([#179717](https://github.com/pytorch/pytorch/pull/179717))
- Drop dead CUDA/ROCm version gates from tests and helpers ([#184879](https://github.com/pytorch/pytorch/pull/184879))
- Fix LayerNorm backward kernel for AMD Strix Halo GPUs ([#183864](https://github.com/pytorch/pytorch/pull/183864))
- Decline CuteDSL scatter_add on ROCm ([#185678](https://github.com/pytorch/pytorch/pull/185678))
- For HSTU, fix CK flash-attn GQA seqlen_q==1 garbage output (#186434) ([#186434](https://github.com/pytorch/pytorch/pull/186434))
- Inductor fixes:
  - Add config flag to disable pointer_range_32 optimization (#179604) ([#179604](https://github.com/pytorch/pytorch/pull/179604))
  - Fix maybe_hipify_code_wrapper for bare-token inputs ([#183725](https://github.com/pytorch/pytorch/pull/183725))
  - Work around file handle limits in StaticCudaLauncher ([#183926](https://github.com/pytorch/pytorch/pull/183926))
  - Preserve combo kernel HIP compile options ([#180277](https://github.com/pytorch/pytorch/pull/180277))
  - lookup_device_info is now case-insensitive ([#182284](https://github.com/pytorch/pytorch/pull/182284))
- Windows
  - Fix MIOpen CTC loss crash on Windows ([#179264](https://github.com/pytorch/pytorch/pull/179264))
  - Apply per-config HIP optimization flags via CMAKE_HIP_FLAGS ([#183856](https://github.com/pytorch/pytorch/pull/183856))
  - Fix inconsistent dllimport ([#183690](https://github.com/pytorch/pytorch/pull/183690), [#183324](https://github.com/pytorch/pytorch/pull/183324), [#183282](https://github.com/pytorch/pytorch/pull/183282), [#183694](https://github.com/pytorch/pytorch/pull/183694))
  - Remove redundant cuSPARSE/hipSPARSE error-string forward declarations ([#180327](https://github.com/pytorch/pytorch/pull/180327))
  - Remove MSVC flags from CMAKE_HIP_FLAGS ([#183365](https://github.com/pytorch/pytorch/pull/183365))
  - Don't set USE_ROCM_CK_SDPA on Windows ([#183962](https://github.com/pytorch/pytorch/pull/183962))
### performance
- Set MIOPEN_FIND_MODE=FAST in op benchmark CI to prevent cold-cache timeout ([#179795](https://github.com/pytorch/pytorch/pull/179795))
- Fix FlexAttention fp16 default num_warps (8 -> 4) on AMD GPUs ([#180720](https://github.com/pytorch/pytorch/pull/180720))
- Fix perf regression in index_add and index_reduce ([#182533](https://github.com/pytorch/pytorch/pull/182533))
- No fence optimization to jit reduce template. ([#176812](https://github.com/pytorch/pytorch/pull/176812))
- Add target-dependent FlexAttention default forward configs ([#181283](https://github.com/pytorch/pytorch/pull/181283))
### docs
### devs
### Untopiced
### not user facing
- Add version guard to ROCm workaround for watchdog polling during graph capture ([#179780](https://github.com/pytorch/pytorch/pull/179780))
- Stop setting CUDA_VISIBLE_DEVICES on ROCm for CI ([#183622](https://github.com/pytorch/pytorch/pull/183622))
- Skip ROCm MI300 mixed precision norm tests ([#182773](https://github.com/pytorch/pytorch/pull/182773))
- [ROCm] Refactor TestSACILP.test_sac_ilp_case1 to be hardware independent ([#182670](https://github.com/pytorch/pytorch/pull/182670))
- [ROCm] Fix skipIfRocm erroring instead of skipping on continuous tests ([#185275](https://github.com/pytorch/pytorch/pull/185275))
- [ROCm] Skip test_compile_multiple_random_ops on ROCm ([#185522](https://github.com/pytorch/pytorch/pull/185522))
- [ROCm] Guard NCCL device reduce-copy support on symmetric-memory device APIs ([#186794](https://github.com/pytorch/pytorch/pull/186794))
- [Inductor] Skip test_template_epilogue_fusion_static_analysis on ROCm ([#180950](https://github.com/pytorch/pytorch/pull/180950))
- [ROCm][CI][inductor] Stabilize test_conv_with_as_strided on ROCm ([#183573](https://github.com/pytorch/pytorch/pull/183573))
- [inductor][ROCm] Fix sys.modules eviction in origami fallback test ([#184480](https://github.com/pytorch/pytorch/pull/184480))
- [ROCm][Inductor] Remove skipIfRocm from test_mm_dropout; expand autotuner VERIFY tolerance for fp16 GEMM on ROCm ([#186009](https://github.com/pytorch/pytorch/pull/186009))
- [ROCm][inductor][UT] Enable 3layer split reduction test ([#186288](https://github.com/pytorch/pytorch/pull/186288))
- [ATen][ROCm] Set reduction numerics to match between oss and internal ([#182668](https://github.com/pytorch/pytorch/pull/182668))
- [ROCm][CI] Skip tests which consume excessive run time in CI ([#182763](https://github.com/pytorch/pytorch/pull/182763))
- [ROCm] fix issue #168635; remove dead quantization code from test_mkldnn_pattern_matcher.py ([#181279](https://github.com/pytorch/pytorch/pull/181279))
- [ROCm] Fix AutoHeuristic test device capability assertion ([#181415](https://github.com/pytorch/pytorch/pull/181415))
- [ROCm] Relax foreach custom error assertion ([#181697](https://github.com/pytorch/pytorch/pull/181697))
- [ROCm] Remove ROCm-specific skip for test_python_ref, add OpInfo-level skips for ihfftn/ihfft2 float16 ([#181468](https://github.com/pytorch/pytorch/pull/181468))
- [ROCm] Unskip matmul accuracy tests for hipblas/hipblaslt ([#175868](https://github.com/pytorch/pytorch/pull/175868))
- [ROCm] Enable TestCudaMallocAsync.test_clock_speed on ROCm MI300 ([#171374](https://github.com/pytorch/pytorch/pull/171374))
- [ROCm][Distributed] Replace MI300-only ROCm gating with platform capability checks ([#174252](https://github.com/pytorch/pytorch/pull/174252))
- [ROCm] Skip TestCachingAutotunerPlugin pending Triton MLIR fix ([#182254](https://github.com/pytorch/pytorch/pull/182254))
- Make skipIfRocm work on test classes ([#182288](https://github.com/pytorch/pytorch/pull/182288))
- Skip on rocm ([#182678](https://github.com/pytorch/pytorch/pull/182678))
- [ROCm] Exclude arch ck ([#182733](https://github.com/pytorch/pytorch/pull/182733))
- [ROCm] Whitelist MI3xx arch CK builds only ([#182969](https://github.com/pytorch/pytorch/pull/182969))
- [ROCm] - Prevent ck and mslk from building on unsupported HW ([#183348](https://github.com/pytorch/pytorch/pull/183348))
- [ROCm] Ensure sdpa backend gets set to default after tests ([#182852](https://github.com/pytorch/pytorch/pull/182852))
- [ROCm] Fix xfail for Navi ([#183448](https://github.com/pytorch/pytorch/pull/183448))
- [ROCm][CI] Unskip TestMatmulCuda.test_cublas_deterministic ([#183350](https://github.com/pytorch/pytorch/pull/183350))
- [ROCm][CI] add gfx950 CDNA2OrLater() in common_cuda.py ([#183599](https://github.com/pytorch/pytorch/pull/183599))
- [ROCm] remove warning in CK for unknown warnings ([#183618](https://github.com/pytorch/pytorch/pull/183618))
- [ROCm] Fix test_origami import after template_heuristics rename ([#183665](https://github.com/pytorch/pytorch/pull/183665))
- [ROCm] Remove redundant ROCm scale-mode branch in CUDABlas ([#183633](https://github.com/pytorch/pytorch/pull/183633))
- Mark ROCm fp16 log10 numerics xfail ([#183824](https://github.com/pytorch/pytorch/pull/183824))
- [ROCm] Fix conv stride constraint layout expectation ([#183876](https://github.com/pytorch/pytorch/pull/183876))
- Xfail ROCm log10 strict numerics test ([#183788](https://github.com/pytorch/pytorch/pull/183788))
- Fix ROCm combo kernel profiler grid checks ([#183832](https://github.com/pytorch/pytorch/pull/183832))
- [ROCm] Fix test_origami autotune comparison after PR #181617 cap ([#184389](https://github.com/pytorch/pytorch/pull/184389))
- [ROCm] Remove stale skips in test_native_multihead_self_attention ([#184802](https://github.com/pytorch/pytorch/pull/184802))
- [ROCm] - Link ck_sdpa ONLY if it exists ([#185250](https://github.com/pytorch/pytorch/pull/185250))
- [ROCm][CI] Unskipping linalg_householder_product_cuda tests  ([#183963](https://github.com/pytorch/pytorch/pull/183963))
- [torch._native] Skip CuTeDSL op registration on ROCm/HIP builds ([#185303](https://github.com/pytorch/pytorch/pull/185303))
- [ROCm] Skip matmul dtype overload accuracy tests on MI200 (gfx90a) ([#186098](https://github.com/pytorch/pytorch/pull/186098))
- [ROCm] Skip cuda graph utils tests on ROCm ([#186383](https://github.com/pytorch/pytorch/pull/186383))
- [ROCm] Remove test_upsamplingNearest2d_launch_rocm test as ROCm reduces max grid size ([#186257](https://github.com/pytorch/pytorch/pull/186257))
- [ROCm] Bump conv3d test_grad tolerance for MIOpen Wrw atomic flake ([#182908](https://github.com/pytorch/pytorch/pull/182908))
- [ROCm][CI] Remove skip decorator because the tests seem to be fixed ([#184266](https://github.com/pytorch/pytorch/pull/184266))
### security
