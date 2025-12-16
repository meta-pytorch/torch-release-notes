
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
- compile_kernel: Handle python floats as c double ([#162626](https://github.com/pytorch/pytorch/pull/162626))
- [BUG] Fix nonzero_static crash on CUDA when the input is a empty tensor ([#162578](https://github.com/pytorch/pytorch/pull/162578))
- [BE] Preserve caller source location in the error message ([#162808](https://github.com/pytorch/pytorch/pull/162808))
- [CUDA] fix indexing on large tensor causing nvalid configuration argument ([#164049](https://github.com/pytorch/pytorch/pull/164049))
- Fix channels-last dimension mapping in CUDA parallel_cat ([#165023](https://github.com/pytorch/pytorch/pull/165023))
- [CUDA][64-bit indexing] Handle 64-bit outer dim `cumsum` case ([#167326](https://github.com/pytorch/pytorch/pull/167326))
- [BE] Remove erroneous `const_cast` ([#168165](https://github.com/pytorch/pytorch/pull/168165))
### performance
- Integrate NVIDIA cuSolver backend into ATen/Linalg (initial implementation for eig/eigval) ([#166715](https://github.com/pytorch/pytorch/pull/166715))
- [ATEN][CUDA] Reduce register pressure in radix_sort_pairs to improve torch.sort performance ([#167094](https://github.com/pytorch/pytorch/pull/167094))
- Add FA4 to sdpa ([#167348](https://github.com/pytorch/pytorch/pull/167348))
- Add FA4 to sdpa ([#167348](https://github.com/pytorch/pytorch/pull/167348))
### docs
- [BE] Add Documentation for Device APIs ([#162834](https://github.com/pytorch/pytorch/pull/162834))
- [BE] Adding aliases for CUDA and XPU API documentation ([#162984](https://github.com/pytorch/pytorch/pull/162984))
- Clarify safety of CUDA graph memory pool sharing across graphs that are replayed in arbtirary order. ([#166975](https://github.com/pytorch/pytorch/pull/166975))
### devs
### Untopiced
- [ROCm] OffsetCalc Unroll Optimization ([#161700](https://github.com/pytorch/pytorch/pull/161700))
- Add cuda headers automatically for compile_kernel ([#162634](https://github.com/pytorch/pytorch/pull/162634))
- compile_kernel large shared memory fix ([#162647](https://github.com/pytorch/pytorch/pull/162647))
- [NVRTC] Enable compiling templated kernels ([#162875](https://github.com/pytorch/pytorch/pull/162875))
- compile_kernel enable pch ([#162972](https://github.com/pytorch/pytorch/pull/162972))
- Make torch.cuda.rng_set_state() and torch.cuda.rng_get_state() work during stream capture. ([#162505](https://github.com/pytorch/pytorch/pull/162505))
- compile_kernel remove header_code arg ([#163165](https://github.com/pytorch/pytorch/pull/163165))
- Reland #161649, vectorize stored in cat for all dtypes ([#162440](https://github.com/pytorch/pytorch/pull/162440))
- [CUDA] revert PR 130472 ([#162950](https://github.com/pytorch/pytorch/pull/162950))
- [BE][Ez]: Prevent copies of std::vector in CUDA ForeachOps ([#163416](https://github.com/pytorch/pytorch/pull/163416))
- [ROCm] Improve perf for elementwise broadcast with mixed dtype ([#163562](https://github.com/pytorch/pytorch/pull/163562))
- Implement CUDA stream protocol ([#163614](https://github.com/pytorch/pytorch/pull/163614))
- Use cuda nvrtc so file based on cuda version used by torch ([#163642](https://github.com/pytorch/pytorch/pull/163642))
- [ROCm] Implement float32 copy kernel ([#163869](https://github.com/pytorch/pytorch/pull/163869))
- [cuBLAS] update cuBLAS determinism docs, remove workspace requirement checks ([#161749](https://github.com/pytorch/pytorch/pull/161749))
- Remove old workaround in launch_logcumsumexp_cuda_kernel ([#164567](https://github.com/pytorch/pytorch/pull/164567))
- [PyTorch Pinned Allocator] Add support of reserved pinned memory segment to avoid slow paths ([#164501](https://github.com/pytorch/pytorch/pull/164501))
- torch.topk: refactor global histogram/cumsum into a dedicated kernel to eliminate redundant memory access ([#164459](https://github.com/pytorch/pytorch/pull/164459))
- [ROCm] Improve non stride-one backwards indexing for small index sets ([#164409](https://github.com/pytorch/pytorch/pull/164409))
- [ROCm] Adjust grid size for non-unit stride backwards indexing ([#165026](https://github.com/pytorch/pytorch/pull/165026))
- Fix int32 overflow in embedding_dense_backward ([#165095](https://github.com/pytorch/pytorch/pull/165095))
- Allow at::native::offset_t to be offset using `operator+=` ([#164570](https://github.com/pytorch/pytorch/pull/164570))
- Fix: nDims is mutated inside the loop in Shape.cu ([#165446](https://github.com/pytorch/pytorch/pull/165446))
- [ATen] Vectorize 8 elements on 16 bit data types for sum/mean ([#165055](https://github.com/pytorch/pytorch/pull/165055))
- [ATen] Switch order of blocked reduce when vectorize loads ([#165178](https://github.com/pytorch/pytorch/pull/165178))
- [BugFix] chunk_size should always be int64_t ([#165971](https://github.com/pytorch/pytorch/pull/165971))
- [ROCm] [Normalization] Update block size ([#165941](https://github.com/pytorch/pytorch/pull/165941))
- [ROCm] Deserialize loads in planer sum portion of reduce() of norm. ([#165927](https://github.com/pytorch/pytorch/pull/165927))
- [ROCm] deserialize loads in planer sum portion of stats() of norm ([#166021](https://github.com/pytorch/pytorch/pull/166021))
- Use std::min for #165927 ([#166199](https://github.com/pytorch/pytorch/pull/166199))
- Fix race condition and make CUDA kthvalue deterministic ([#165762](https://github.com/pytorch/pytorch/pull/165762))
- Use std::min for #166021 ([#166195](https://github.com/pytorch/pytorch/pull/166195))
- Add a compile-time flag to trigger verbose logging for device-side asserts ([#166171](https://github.com/pytorch/pytorch/pull/166171))
- [ROCm] Disable `__builtin_amdgcn_rcpf` for gfx90a ([#166454](https://github.com/pytorch/pytorch/pull/166454))
- Add per_process_memory_fraction to PYTORCH_CUDA_ALLOC_CONF ([#161035](https://github.com/pytorch/pytorch/pull/161035))
- [ROCm] Specialized binary elementwise broadcast kernel for mixed dtypes with float/bfloat16/half ([#167233](https://github.com/pytorch/pytorch/pull/167233))
- [ATEN][CUDA] Reduce register pressure introduced by CUDA_KERNEL_ASSERT to improve torch.EmbeddingBag performance ([#167834](https://github.com/pytorch/pytorch/pull/167834))
- fixes a few issues with out_dtype overload for addmm/baddbmm ([#167931](https://github.com/pytorch/pytorch/pull/167931))
- [CUDA][Thor] Enable CUTLASS matmuls on Thor ([#164836](https://github.com/pytorch/pytorch/pull/164836))
- [pytorch] Make clamp kernel branchless ([#167889](https://github.com/pytorch/pytorch/pull/167889))
- Replace thrust::tie with structure binding ([#168943](https://github.com/pytorch/pytorch/pull/168943))
- [ROCm] roll kernel as grid stride loop ([#169474](https://github.com/pytorch/pytorch/pull/169474))
### not user facing
- [CUDA] fix shared memory race in `reduce_kernel` ([#162995](https://github.com/pytorch/pytorch/pull/162995))
- [ATen][CUDA] CUTLASS matmuls: add sm_103a flag  ([#162956](https://github.com/pytorch/pytorch/pull/162956))
- Make `Tensor.__dlpack__(stream=None)` capture-safe during CUDA Graph capture ([#163242](https://github.com/pytorch/pytorch/pull/163242))
- [ATen] Remove explicit casting of complex nansum during accumulation ([#165494](https://github.com/pytorch/pytorch/pull/165494))
- [Mem Snapshot] Add Metadata Field ([#165490](https://github.com/pytorch/pytorch/pull/165490))
- [Mem Snapshot] Add Metadata Field ([#165490](https://github.com/pytorch/pytorch/pull/165490))
- Remove outdated CUB macros ([#164656](https://github.com/pytorch/pytorch/pull/164656))
- disable jiterator for complex tan and tanh ([#165250](https://github.com/pytorch/pytorch/pull/165250))
- Fix thread safety in getCurrentCUDABlasHandle and getCUDABlasLtWorkspace ([#167248](https://github.com/pytorch/pytorch/pull/167248))
- [BugFix] Fix incorrect usage of const_data_ptr in memcpy ([#168233](https://github.com/pytorch/pytorch/pull/168233))
- Move CUDAEvent to c10 ([#158219](https://github.com/pytorch/pytorch/pull/158219))
- The Nested Pool ([#168382](https://github.com/pytorch/pytorch/pull/168382))
- [pytorch] Add env variable to enable IPC for expandable segments ([#169487](https://github.com/pytorch/pytorch/pull/169487))
- Fix _preload_cuda_deps throw condition (40b84d665a4)
### security
