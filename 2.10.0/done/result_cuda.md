
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
- Make `torch.cuda.rng_set_state` and `torch.cuda.rng_get_state` work in CUDA graph capture. ([#162505](https://github.com/pytorch/pytorch/pull/162505))
- `torch.cuda._compile_kernel`
  - Enable templated kernels ([#162875](https://github.com/pytorch/pytorch/pull/162875))
  - Enable pre-compiled kernels ([#162972](https://github.com/pytorch/pytorch/pull/162972))
  - Add CUDA headers automatically ([#162634](https://github.com/pytorch/pytorch/pull/162634))
  - Remove outdated `header_code` argument ([#163165](https://github.com/pytorch/pytorch/pull/163165))
- Prevent copies of std::vector in CUDA ForeachOps ([#163416](https://github.com/pytorch/pytorch/pull/163416))
- Implement cuda-python CUDA stream protocol ([#163614](https://github.com/pytorch/pytorch/pull/163614))
- Remove outdated checks and docs for cuBLAS determinism ([#161749](https://github.com/pytorch/pytorch/pull/161749))
- Cleanup old workaround code in `launch_logcumsumexp_cuda_kernel` ([#164567](https://github.com/pytorch/pytorch/pull/164567))
- Add a compile-time flag to trigger verbose logging for device-side asserts ([#166171](https://github.com/pytorch/pytorch/pull/166171))
- Support SM 10.3 in custom CUTLASS matmuls ([#162956](https://github.com/pytorch/pytorch/pull/162956))
- Enable CUTLASS matmuls on Thor ([#164836](https://github.com/pytorch/pytorch/pull/164836))
- Add `per_process_memory_fraction` option to `PYTORCH_CUDA_ALLOC_CONF` ([#161035](https://github.com/pytorch/pytorch/pull/161035))
- Support nested memory pools ([#168382](https://github.com/pytorch/pytorch/pull/168382))
### bug fixes
- `torch._compile_kernel`
  - Handle python floats as double in CUDA C++ ([#162626](https://github.com/pytorch/pytorch/pull/162626))
  - Use libnvrtc.so path based on CUDA version used by torch ([#163642](https://github.com/pytorch/pytorch/pull/163642))
- Fix `torch.nonzero_static` crash on CUDA when the input is a empty tensor ([#162578](https://github.com/pytorch/pytorch/pull/162578))
- Fix caller source location in `C10_CUDA_CHECK` error messages ([#162808](https://github.com/pytorch/pytorch/pull/162808))
- Fix channels-last dimension mapping in CUDA `parallel_cat` ([#165023](https://github.com/pytorch/pytorch/pull/165023))
- 64-bit indexing on CUDA:
  - Fix a large tensor indexding crash ([#164049](https://github.com/pytorch/pytorch/pull/164049))
  - Handle 64-bit outer dimension in `cumsum` ([#167326](https://github.com/pytorch/pytorch/pull/167326))
  - Fix crash in `embedding_dense_backward` ([#165095](https://github.com/pytorch/pytorch/pull/165095))
  - Fix chunk-size for 64-bit indexing in fused adagrad ([#165971](https://github.com/pytorch/pytorch/pull/165971))
- Remove erroneous `const_cast` in CUDA `memcpy` call ([#168165](https://github.com/pytorch/pytorch/pull/168165))
- Handle large shared memory in `torch.cuda._compile_kernel` ([#162647](https://github.com/pytorch/pytorch/pull/162647))
- Fix `torch.unique_consecutive` crash on CUDA ([#162950](https://github.com/pytorch/pytorch/pull/162950))
- Fix correctness of `parallel_cat` ([#165446](https://github.com/pytorch/pytorch/pull/165446))
- Fix race condition and make `torch.kthvalue` deterministic on CUDA ([#165762](https://github.com/pytorch/pytorch/pull/165762))
- Fix shared memory race in `reduce_kernel` ([#162995](https://github.com/pytorch/pytorch/pull/162995))
- Fix `Tensor.__dlpack__(stream=None)` support during CUDA Graph capture ([#163242](https://github.com/pytorch/pytorch/pull/163242))
- Remove explicit casting of complex nansum during accumulation to avoid precision loss ([#165494](https://github.com/pytorch/pytorch/pull/165494))
- Disable jiterator for complex tan and tanh due to numerical issues ([#165250](https://github.com/pytorch/pytorch/pull/165250))
- Fix a few issues with `out_dtype` overload for addmm/baddbmm ([#167931](https://github.com/pytorch/pytorch/pull/167931))
- Fix safety issues when calling cuBLAS from multiple threads ([#167248](https://github.com/pytorch/pytorch/pull/167248))
### performance
- Integrate NVIDIA cuSolver backend into ATen/Linalg (initial implementation for eig/eigval) ([#166715](https://github.com/pytorch/pytorch/pull/166715))
- Reduce register pressure in `radix_sort_pairs` to improve torch.sort performance ([#167094](https://github.com/pytorch/pytorch/pull/167094))
- Add Flash Attention 4 to sdpa ([#167348](https://github.com/pytorch/pytorch/pull/167348))
- Vectorize stores in cat for all dtypes on CUDA ([#162440](https://github.com/pytorch/pytorch/pull/162440))
- Expose `pinned_reserve_segment_size_mb` to speed up pinned memory allocation ([#164501](https://github.com/pytorch/pytorch/pull/164501))
- torch.topk: refactor global histogram/cumsum into a dedicated kernel to improve performance on CUDA ([#164459](https://github.com/pytorch/pytorch/pull/164459))
- Vectorize 8 elements on 16=bit data types for sum/mean to improve performance ([#165055](https://github.com/pytorch/pytorch/pull/165055))
- Switch order of blocked reduce when vectorize loads to improve performance ([#165178](https://github.com/pytorch/pytorch/pull/165178))
- Reduce register pressure to improve `torch.EmbeddingBag` performance ([#167834](https://github.com/pytorch/pytorch/pull/167834))
- Make clamp kernel branchless to improve performance ([#167889](https://github.com/pytorch/pytorch/pull/167889))
### docs
- Add Documentation for Device APIs ([#162834](https://github.com/pytorch/pytorch/pull/162834))
- Adding aliases for CUDA and XPU API documentation ([#162984](https://github.com/pytorch/pytorch/pull/162984))
- Clarify safety of CUDA graph memory pool sharing across graphs in documentation ([#166975](https://github.com/pytorch/pytorch/pull/166975))
### devs
### Untopiced
### not user facing
- Add Metadata Field to Memory Snapshots ([#165490](https://github.com/pytorch/pytorch/pull/165490))
- Update `at::native::offset_t` for compatibility with CCCL 3.1 ([#164570](https://github.com/pytorch/pytorch/pull/164570))
- Remove outdated CUB macros ([#164656](https://github.com/pytorch/pytorch/pull/164656))
- Move `CUDAEvent` to c10 ([#158219](https://github.com/pytorch/pytorch/pull/158219))
- Add env variable to enable IPC for expandable segments ([#169487](https://github.com/pytorch/pytorch/pull/169487))
- Fix `_preload_cuda_deps` throw condition (40b84d665a4)
- Replace thrust::tie with structure binding ([#168943](https://github.com/pytorch/pytorch/pull/168943))
### security
