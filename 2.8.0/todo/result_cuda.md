
# Release Notes worksheet cuda

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

## cuda
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- Fix deterministic indexing with broadcast ([#154296](https://github.com/pytorch/pytorch/pull/154296))
### performance
- [aten] 8 bytes aligned vector loads for bf16 and fp16 dtypes in torch.cat ([#150233](https://github.com/pytorch/pytorch/pull/150233))
- [aten] Enable vectorized 8byte copy for fp16/bf16 for index select kernel ([#152380](https://github.com/pytorch/pytorch/pull/152380))
### docs
- Fix deprecated amp APIs in docs ([#154553](https://github.com/pytorch/pytorch/pull/154553))
- [BE] Document device memory apis in correct module ([#155126](https://github.com/pytorch/pytorch/pull/155126))
### devs
### Untopiced
- [ROCm] Improve softmax performance ([#149076](https://github.com/pytorch/pytorch/pull/149076))
- [GPU Snapshot] Add Clear History Flag ([#149352](https://github.com/pytorch/pytorch/pull/149352))
- fix missing field initializer warning ([#149597](https://github.com/pytorch/pytorch/pull/149597))
- [ROCm] NLLLoss (torch.nll_loss) Performance Tuning by Dynamically Selecting # of GPU threads ([#149548](https://github.com/pytorch/pytorch/pull/149548))
- [ROCm] Extend vectorized elementwise kernel to more heterogenous tensor types. ([#149738](https://github.com/pytorch/pytorch/pull/149738))
- Removed ROCM ifdef that governs thread count + smem parallel reduction. ([#149779](https://github.com/pytorch/pytorch/pull/149779))
- [ROCM] Fix in-place aten sum with specialized templated kernels. ([#151230](https://github.com/pytorch/pytorch/pull/151230))
- [Easy][Building] Fix the warning of int4mm.cu when building ([#151427](https://github.com/pytorch/pytorch/pull/151427))
- Document non-pytorch CUDA memory allocation and how to query it ([#150880](https://github.com/pytorch/pytorch/pull/150880))
- Add torch.cuda._compile_kernel() ([#151484](https://github.com/pytorch/pytorch/pull/151484))
- use cutlass native BroadcastPtrArray in scaled group gemm ([#152404](https://github.com/pytorch/pytorch/pull/152404))
- [BE]: Update cutlass submodule to 3.9.2 ([#152779](https://github.com/pytorch/pytorch/pull/152779))
- [ROCm] opportunistic fastatomics - fix build error with newer compilers ([#152841](https://github.com/pytorch/pytorch/pull/152841))
- Use gather in index_select ([#151715](https://github.com/pytorch/pytorch/pull/151715))
- Fix TORCH_CHECK error message in FusedSgdKernel ([#153074](https://github.com/pytorch/pytorch/pull/153074))
- [CUDA][cuBLASLt] Fix scale setting for `allowFP16AccumulationCuBLAS` `true` case ([#153083](https://github.com/pytorch/pytorch/pull/153083))
- make use_mem_pool threadlocal ([#153356](https://github.com/pytorch/pytorch/pull/153356))
- [ROCm] Maxpool backward NHWC Perf Improvement targeting Resnet scenarios ([#152267](https://github.com/pytorch/pytorch/pull/152267))
- Fix AsyncMM not compiled with SM90a issue ([#153519](https://github.com/pytorch/pytorch/pull/153519))
- [ROCm] Improvements to non-vectorized elementwise kernels ([#153184](https://github.com/pytorch/pytorch/pull/153184))
- [Memory Snapshot] Fix RecordFunction Callback Handling ([#153839](https://github.com/pytorch/pytorch/pull/153839))
- SDPA fix memory efficient attention for large batch dim ([#154029](https://github.com/pytorch/pytorch/pull/154029))
- use 4 elements per thread in no-cast elementwise kernel ([#154558](https://github.com/pytorch/pytorch/pull/154558))
- [ROCm] Fix 3D tensor perf degradation with NHWC format ([#154522](https://github.com/pytorch/pytorch/pull/154522))
- [ROCm] Update maxpool launch config ([#154619](https://github.com/pytorch/pytorch/pull/154619))
- [CUDA] Fixes for backwards in memefficient attn for large tensors ([#154663](https://github.com/pytorch/pytorch/pull/154663))
- Enable FP8 row-wise scaled-mm for sm12x ([#155991](https://github.com/pytorch/pytorch/pull/155991))
- Support stream capture of event record and wait nodes in cuda graphs ([#155372](https://github.com/pytorch/pytorch/pull/155372))
- support CUBLASLT_MATMUL_MATRIX_SCALE_OUTER_VEC_32F ([#154680](https://github.com/pytorch/pytorch/pull/154680))
- [ROCm] Enable more parallelism for multi-dimensional reductions ([#155806](https://github.com/pytorch/pytorch/pull/155806))
- [CUDA] fix illegal memory access in attention ([#155397](https://github.com/pytorch/pytorch/pull/155397))
### not user facing
- [ROCm] missing AT_CUDA_CHECK for cub and SoftMax ([#149883](https://github.com/pytorch/pytorch/pull/149883))
- [ROCm] AtomicAdd specialization on AMD for fp64. ([#151724](https://github.com/pytorch/pytorch/pull/151724))
- [ATen][CUDA][SDPA] Enable SDPA on sm_121 ([#152314](https://github.com/pytorch/pytorch/pull/152314))
- [C10][CUDA] Eagerly create context on torch.cuda.set_device(device) call ([#155900](https://github.com/pytorch/pytorch/pull/155900))
- [C10][CUDA] Eagerly create context on torch.cuda.set_device(device) call ([#155900](https://github.com/pytorch/pytorch/pull/155900))
### security
