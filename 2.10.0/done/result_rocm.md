
# Release Notes worksheet rocm

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

## rocm
### bc breaking
### deprecation
### new features
- Enable grouped GEMM via regular GEMM fallback ([#162419](https://github.com/pytorch/pytorch/pull/162419))
- Enable grouped GEMM via CK ([#166334](https://github.com/pytorch/pytorch/pull/166334), [#167403](https://github.com/pytorch/pytorch/pull/167403))
- Enable ATen GEMM overload for FP32 output from FP16/BF16 inputs ([#162600](https://github.com/pytorch/pytorch/pull/162600))
- Support torch.cuda._compile_kernel ([#162510](https://github.com/pytorch/pytorch/pull/162510))
- Enhanced Windows support
  - load_inline ([#162577](https://github.com/pytorch/pytorch/pull/162577))
  - Enable AOTriton runtime compile ([#165538](https://github.com/pytorch/pytorch/pull/165538))
  - AOTriton scaled_dot_product_attention ([#162330](https://github.com/pytorch/pytorch/pull/162330))
- Add gfx1150 gfx1151 to hipblaslt-supported GEMM lists ([#164744](https://github.com/pytorch/pytorch/pull/164744))
- Add scaled_mm v2 support. ([#165528](https://github.com/pytorch/pytorch/pull/165528))
- Add torch.version.rocm, distinct from torch.version.hip ([#168097](https://github.com/pytorch/pytorch/pull/168097))
### improvements
- Allow custom OpenBLAS library name for CMake build ([#166333](https://github.com/pytorch/pytorch/pull/166333))
- Add gfx1150 gfx1151 to binary build targets ([#164782](https://github.com/pytorch/pytorch/pull/164782), [#164854](https://github.com/pytorch/pytorch/pull/164854), [#164763](https://github.com/pytorch/pytorch/pull/164763))
- hipSPARSELt support - Update cuda_to_hip_mappings.py ([#167335](https://github.com/pytorch/pytorch/pull/167335))
- New implementation of upsample_bilinear2d_backward ([#164572](https://github.com/pytorch/pytorch/pull/164572))
- Remove env var HIPBLASLT_ALLOW_TF32 from codebase, TF32 always allowed ([#162998](https://github.com/pytorch/pytorch/pull/162998))
- Enable multi-arch compilation and unit tests for AOT Inductor ([#166357](https://github.com/pytorch/pytorch/pull/166357))
- Fix miopen batchnorm changing output format ([#162112](https://github.com/pytorch/pytorch/pull/162112))
### bug fixes
- Fix hardsigmoid op ([#162758](https://github.com/pytorch/pytorch/pull/162758))
- Fix GEMM carveout feature ([#164303](https://github.com/pytorch/pytorch/pull/164303))
- Disable `__builtin_amdgcn_rcpf` for gfx90a ([#166454](https://github.com/pytorch/pytorch/pull/166454))
- ROCm 7.0 BC-breaking preparations in JIT support ([#160587](https://github.com/pytorch/pytorch/pull/160587), [#166147](https://github.com/pytorch/pytorch/pull/166147))
### performance
- Use hipSolver instead of MAGMA for Cholesky ([#163977](https://github.com/pytorch/pytorch/pull/163977))
- Layer norm now uses __builtin_amdgcn_rcpf(x) instead of 1.f/x ([#165589](https://github.com/pytorch/pytorch/pull/165589))
- OffsetCalc Unroll Optimization ([#161700](https://github.com/pytorch/pytorch/pull/161700))
- Improve perf for elementwise broadcast with mixed dtype ([#163562](https://github.com/pytorch/pytorch/pull/163562))
- Implement float32 copy kernel ([#163869](https://github.com/pytorch/pytorch/pull/163869))
- Improve non stride-one backwards indexing for small index sets ([#164409](https://github.com/pytorch/pytorch/pull/164409))
- Adjust grid size for non-unit stride backwards indexing ([#165026](https://github.com/pytorch/pytorch/pull/165026))
- Normalization update to block size ([#165941](https://github.com/pytorch/pytorch/pull/165941))
- Deserialize loads in planer sum portion of reduce() of norm. ([#165927](https://github.com/pytorch/pytorch/pull/165927))
- Deserialize loads in planer sum portion of stats() of norm ([#166021](https://github.com/pytorch/pytorch/pull/166021))
- Specialized binary elementwise broadcast kernel for mixed dtypes with float/bfloat16/half ([#167233](https://github.com/pytorch/pytorch/pull/167233))
- Roll kernel as grid stride loop ([#169474](https://github.com/pytorch/pytorch/pull/169474))
- Inductor performance improvements via configs, heurstics, and/or codegen ([#163908](https://github.com/pytorch/pytorch/pull/163908), [#161280](https://github.com/pytorch/pytorch/pull/161280), [#166470](https://github.com/pytorch/pytorch/pull/166470), [#162052](https://github.com/pytorch/pytorch/pull/162052), [#163197](https://github.com/pytorch/pytorch/pull/163197))
### docs
### devs
- Add Rocm to Operator Microbenchmark CI ([#164173](https://github.com/pytorch/pytorch/pull/164173))
- Enable TD for all ROCm default and distributed config workflows ([#168225](https://github.com/pytorch/pytorch/pull/168225))
- Expand trunk.yml coverage for ROCm ([#168162](https://github.com/pytorch/pytorch/pull/168162))
- cudagraph trees ut fixes ([#163592](https://github.com/pytorch/pytorch/pull/163592))
- test_convolution.py uses miopen immediate mode ([#164598](https://github.com/pytorch/pytorch/pull/164598))
- Keep amdgpu-coerce-illegal-types flag if rocm version is less than 7.2 ([#165789](https://github.com/pytorch/pytorch/pull/165789))
- Use a ROCm version string without hash. ([#166336](https://github.com/pytorch/pytorch/pull/166336))
- Dynamo benchmarks: remove outdated flaky models and enable deterministic algorithms ([#169024](https://github.com/pytorch/pytorch/pull/169024))
### Untopiced
### not user facing
- ROCm 7.1 CI and binary upgrades ([#166743](https://github.com/pytorch/pytorch/pull/166743), [#166693](https://github.com/pytorch/pytorch/pull/166693), [#166730](https://github.com/pytorch/pytorch/pull/166730), [#167390](https://github.com/pytorch/pytorch/pull/167390), [#166665](https://github.com/pytorch/pytorch/pull/166665))
- ROCm 7.0 CI and binary upgrades ([#163937](https://github.com/pytorch/pytorch/pull/163937), [#163140](https://github.com/pytorch/pytorch/pull/163140), [#165756](https://github.com/pytorch/pytorch/pull/165756), [#163860](https://github.com/pytorch/pytorch/pull/163860), [#163883](https://github.com/pytorch/pytorch/pull/163883), [#164244](https://github.com/pytorch/pytorch/pull/164244))
- Move trunk wheel builds to python 3.10 ([#163339](https://github.com/pytorch/pytorch/pull/163339))
- Increase binary build timeout to 5 hours (300 minutes) ([#163776](https://github.com/pytorch/pytorch/pull/163776))
- Remove amdgpu from install_rocm.sh ([#166575](https://github.com/pytorch/pytorch/pull/166575))
- Manylinux docker images use devtoolset-13 ([#166764](https://github.com/pytorch/pytorch/pull/166764))
- Enable latest fbgemm build for CI ([#162385](https://github.com/pytorch/pytorch/pull/162385), [#162649](https://github.com/pytorch/pytorch/pull/162649))
- Fix skip condition for PLATFORM_SUPPORTS_SYMM_MEM ([#163205](https://github.com/pytorch/pytorch/pull/163205))
- Skip AsyncTP test class as AsyncTP is not supported on ROCm ([#166316](https://github.com/pytorch/pytorch/pull/166316))
- Enable ZerO Optimizer UTs ([#169077](https://github.com/pytorch/pytorch/pull/169077))
### security
