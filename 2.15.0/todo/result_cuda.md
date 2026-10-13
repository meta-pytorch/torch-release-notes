
# Release Notes worksheet cuda

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

## cuda
### bc breaking
### deprecation
### new features
### improvements
- [CUDA] Support float8 scalar scatter ([#197199](https://github.com/pytorch/pytorch/pull/197199))
### bug fixes
- Don't mutate the caller's annotation dict in mark_stream ([#194851](https://github.com/pytorch/pytorch/pull/194851))
- Only warn on the final failed cudaMalloc attempt in alloc_block ([#193391](https://github.com/pytorch/pytorch/pull/193391))
### performance
### docs
### devs
### Untopiced
- Reapply "Dispatch index_put_ to fill_ for scalar values (#188267 / #189105)" ([#189303](https://github.com/pytorch/pytorch/pull/189303))
- Attribute CUDA-graph nodes from CUPTI node-creation callbacks ([#191999](https://github.com/pytorch/pytorch/pull/191999))
- [ROCm] Optimize AMD normalization backward kernel by using tiled and two pass implementations where they are most efficient. ([#189405](https://github.com/pytorch/pytorch/pull/189405))
- [BE][Ez]: Update c10::complex kernels to use sincos ([#193729](https://github.com/pytorch/pytorch/pull/193729))
- [BE][Ez]: Update c10::complex kernels to use sincos ([#193729](https://github.com/pytorch/pytorch/pull/193729))
- [ROCm] Fix incorrect results in cross-CTA reductions (argmax/max) ([#193291](https://github.com/pytorch/pytorch/pull/193291))
- [CUDA] Fix reentrant deadlock in torch.cuda._lazy_call ([#182948](https://github.com/pytorch/pytorch/pull/182948))
- Drop the unused BiasType parameter from the grouped FP8 GEMM ([#194189](https://github.com/pytorch/pytorch/pull/194189))
- [CUDA] Remove unused multinomial probability copy ([#194391](https://github.com/pytorch/pytorch/pull/194391))
- Reapply "Dispatch index_put_ to fill_ for scalar values (#188267 / #189105)" ([#189303](https://github.com/pytorch/pytorch/pull/189303))
- Handle invalid CUDA JITerator cache entries ([#186346](https://github.com/pytorch/pytorch/pull/186346))
- [CUDA] Add non-overlapping fast path for avg_pool2d backward ([#191086](https://github.com/pytorch/pytorch/pull/191086))
- [CUDA] Hoist uniform divisor in avg_pool3d backward ([#195119](https://github.com/pytorch/pytorch/pull/195119))
- Name RowwiseScaledMM's EVT arguments, drop dead warning suppression ([#195396](https://github.com/pytorch/pytorch/pull/195396))
- Dispatch `index_put_` to `masked_fill_.Scalar` when possible ([#188330](https://github.com/pytorch/pytorch/pull/188330))
- Add opt-in TORCH_CUDA_CHECK_STRAY_CONTEXT guard to torch.cuda.set_device ([#191036](https://github.com/pytorch/pytorch/pull/191036))
- [BE][Ez]: Use inlined std::sort in CUDA maybeOverlappingIndices ([#195470](https://github.com/pytorch/pytorch/pull/195470))
- Add BF16x9 precision mode for CUDA FP32 matmul ([#195301](https://github.com/pytorch/pytorch/pull/195301))
- Bake CUDA graph annotations into the chrome trace, retiring the offline joiner ([#194854](https://github.com/pytorch/pytorch/pull/194854))
- [CUDA] Introduce CUDA graph memory management ([#195510](https://github.com/pytorch/pytorch/pull/195510))
- Use fastAtomicAdd for the max-pool backward scatters ([#196156](https://github.com/pytorch/pytorch/pull/196156))
- Stop the CTC cuDNN check reading past the input lengths ([#196084](https://github.com/pytorch/pytorch/pull/196084))
- [ROCm] Enforce signed short for __builtin_amdgcn_flat_atomic_fadd_v2bf16 ([#196538](https://github.com/pytorch/pytorch/pull/196538))
- Widen Float2 constructor to accscalar_t in batch norm reduction ([#196125](https://github.com/pytorch/pytorch/pull/196125))
- Add annotation_config["key_by"], and annotate nested graph bodies with it ([#196528](https://github.com/pytorch/pytorch/pull/196528))
- CUDA: unrolled kernels for upsample_linear1d forward/backward when grid is small ([#180885](https://github.com/pytorch/pytorch/pull/180885))
- [CUDA] Fix arange overflow for N >= 2**32 ([#197713](https://github.com/pytorch/pytorch/pull/197713))
- [cuda] Improve speed of _check_stray_context ([#197566](https://github.com/pytorch/pytorch/pull/197566))
- Fix histc(out=) dtype validation mismatch between CPU and CUDA ([#196100](https://github.com/pytorch/pytorch/pull/196100))
- CUDA: unrolled kernels for upsample_linear1d forward/backward when grid is small ([#180885](https://github.com/pytorch/pytorch/pull/180885))
- [ATen][ROCm] zero_: keep the memset fast path outside graph capture on ROCm 7.0.x ([#198565](https://github.com/pytorch/pytorch/pull/198565))
- Fix int32 overflow in cdist CUDA backward kernel ([#198452](https://github.com/pytorch/pytorch/pull/198452))
- [cuda] Improve speed of _check_stray_context ([#197566](https://github.com/pytorch/pytorch/pull/197566))
- [CUDA] Expose SM partitions and disjoint green-context splitting ([#198278](https://github.com/pytorch/pytorch/pull/198278))
- Stop instantiating unreachable cat kernels ([#194184](https://github.com/pytorch/pytorch/pull/194184))
- [CUDA] Add locality constraints to SM partitioning ([#198279](https://github.com/pytorch/pytorch/pull/198279))
- Fix int32 overflow in CUDA bincount/histogram bin index ([#189685](https://github.com/pytorch/pytorch/pull/189685))
- [CD] [Windows] Update to CUDA 13.2.2 for build ([#198843](https://github.com/pytorch/pytorch/pull/198843))
- Fix missing cp.async drain in memory-efficient attention forward kernel ([#198922](https://github.com/pytorch/pytorch/pull/198922))
- Avoid CUDA sync for scalar tensor indices in scalar assignment ([#198811](https://github.com/pytorch/pytorch/pull/198811))
- [CachingHostAllocator] Don't share bucket stats between pools ([#199144](https://github.com/pytorch/pytorch/pull/199144))
### not user facing
- Simplify stateless RNG split() / fold_in() kernels with no grid-stride loop ([#190036](https://github.com/pytorch/pytorch/pull/190036))
- [ATen][CUDA][CUTLASS][SUBMODULE] Update CUTLASS to v4.8.0 and CUTLASS-Operators to v0.3.0 ([#198179](https://github.com/pytorch/pytorch/pull/198179))
- [ATen][CUDA][CUTLASS][SUBMODULE] Update CUTLASS to v4.8.0 and CUTLASS-Operators to v0.3.0 ([#198179](https://github.com/pytorch/pytorch/pull/198179))
- Remove unused dummy_mean_/dummy_var_ in Normalization.cuh ([#199479](https://github.com/pytorch/pytorch/pull/199479))
### security
