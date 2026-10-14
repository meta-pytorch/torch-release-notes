
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
- `torch.histc(..., out=...)` on CUDA now raises an error when `out` does not have the same dtype as the input ([#196100](https://github.com/pytorch/pytorch/pull/196100))

  CUDA used to silently cast into any `out` dtype. It now matches CPU and MPS and rejects mismatches, even widening ones. Compute without `out` and cast instead.

  Version 2.14:
  ```python
  >>> torch.histc(x, bins=4, min=-2.0, max=2.0, out=int64_out)  # silently truncated
  ```

  Version 2.15:
  ```python
  RuntimeError: torch.histogram: input tensor and hist tensor should have the same dtype, but got input float and hist long int
  >>> int64_out.copy_(torch.histc(x, bins=4, min=-2.0, max=2.0))  # workaround
  ```
- On CUDA, cuBLAS and cuBLASLt workspaces are now allocated for each operation instead of being cached per handle and stream ([#194311](https://github.com/pytorch/pytorch/pull/194311))

  Graphs captured separately on one stream could share the cached workspace and fail on replay with `CUDA error: an illegal memory access was encountered`. Workspaces are now freed after each op, so `torch.cuda.memory_allocated()` excludes them and the handle from `torch.cuda.current_blas_handle()` has no ATen workspace attached. Set `TORCH_CUBLAS_WORKSPACE_CACHE=1` to restore caching (unsafe with multiple graphs on one stream). ROCm has a matching change ([#196920](https://github.com/pytorch/pytorch/pull/196920)).

  Version 2.14:
  ```python
  >>> torch.mm(a, a, out=out)
  >>> torch.cuda.memory_allocated() - before > 0  # workspace stays allocated
  True
  ```

  Version 2.15:
  ```python
  >>> torch.cuda.memory_allocated() - before  # freed after the op
  0
  ```
### deprecation
- `torch.cuda.graph_annotations.clear_kernel_annotations()` is deprecated and now emits a `FutureWarning` ([#195398](https://github.com/pytorch/pytorch/pull/195398))

  The CUDA graph kernel annotation registry now cleans up after itself: annotations are rekeyed to the executable graph when it is instantiated and dropped when that graph is destroyed. A global clear also discards annotations for graphs that are still live. Remove the call, and reset or delete a graph to drop its annotations.

  Version 2.14:
  ```python
  annotations = get_kernel_annotations()
  clear_kernel_annotations()
  ```

  Version 2.15:
  ```python
  annotations = get_kernel_annotations()
  # No clear needed; g's annotations are dropped when g is reset or destroyed.
  ```
### new features
- Add `GreenContext.split` and `torch.cuda.green_contexts.SMPartition` for creating green contexts with disjoint SM allocations, plus a `GreenContext.sm_count` property reporting the SMs actually allocated; requires a CUDA driver and `cuda.bindings` 13.1 or newer ([#198278](https://github.com/pytorch/pytorch/pull/198278))
- Add `locality_domain_ids` to `GreenContext.split` and `SMPartition.split`, together with `get_num_locality_domains()` and `is_localization_supported()`, to restrict SM partitions to hardware locality domains; requires a CUDA driver and `cuda.bindings` 13.4 or newer ([#198279](https://github.com/pytorch/pytorch/pull/198279))
- Add a `"bfx9"` mode for `torch.backends.cuda.matmul.fp32_precision` that keeps FP32 inputs and outputs but lets cuBLAS use its BF16x9 algorithm on compute capability 10.0 and 10.3 GPUs; requires a CUDA 12.9 or newer build ([#195301](https://github.com/pytorch/pytorch/pull/195301))
### improvements
- Support scalar `scatter` for float8 dtypes on CUDA ([#197199](https://github.com/pytorch/pytorch/pull/197199))
- Extend CUDA graph kernel annotations: an `annotation_config` argument to `torch.cuda.graph` with a CUPTI backend ([#191999](https://github.com/pytorch/pytorch/pull/191999)), `key_by="source"` and `"auto"` modes that can annotate kernels inside nested `torch.cond` / `torch.while_loop` bodies ([#196528](https://github.com/pytorch/pytorch/pull/196528), [#196530](https://github.com/pytorch/pytorch/pull/196530), [#197577](https://github.com/pytorch/pytorch/pull/197577)), and a `cuda_graph_annotations` argument to `export_chrome_trace` that writes them into the trace ([#194854](https://github.com/pytorch/pytorch/pull/194854))
- `CUDAGraph.get_graph_data()` now reports kernel grid and block dimensions, dynamic shared memory size, and programmatic dependency edges ([#196018](https://github.com/pytorch/pytorch/pull/196018), [#196527](https://github.com/pytorch/pytorch/pull/196527))
- Add `PYTORCH_CUDA_ALLOC_CONF` options `expandable_segments_reserve` and `expandable_segments_reserve_by_class` to shrink the virtual-address reservation of expandable segments ([#192269](https://github.com/pytorch/pytorch/pull/192269)), and explain these options when that reservation fails ([#193211](https://github.com/pytorch/pytorch/pull/193211))
- CUDA out-of-memory errors now say when a custom `MemPool` allocator returned a null pointer ([#199363](https://github.com/pytorch/pytorch/pull/199363))
- Add opt-in `TORCH_CUDA_CHECK_STRAY_CONTEXT=warn|error`, which makes `torch.cuda.set_device` warn or raise when another device already holds a CUDA primary context ([#191036](https://github.com/pytorch/pytorch/pull/191036))
### bug fixes
- Fix silently wrong results or illegal memory accesses from 32-bit index overflow on CUDA in `arange`, `range`, `linspace` and `logspace` ([#197713](https://github.com/pytorch/pytorch/pull/197713)), `cdist` backward ([#198452](https://github.com/pytorch/pytorch/pull/198452)), `bincount` ([#189685](https://github.com/pytorch/pytorch/pull/189685)), `embedding_bag` backward with `per_sample_weights` ([#193408](https://github.com/pytorch/pytorch/pull/193408)), and `bmm` ([#196431](https://github.com/pytorch/pytorch/pull/196431), [#197695](https://github.com/pytorch/pytorch/pull/197695))
- Fix nondeterministic NaNs in memory-efficient attention forward with head dimension 256 or larger on Ampere, Ada and consumer Blackwell GPUs ([#198922](https://github.com/pytorch/pytorch/pull/198922))
- Fix CUDA batch norm under AMP overflowing to `inf` ([#196125](https://github.com/pytorch/pytorch/pull/196125))
- Fix rare incorrect indices from `argmax`, `argmin`, `max` and `min` for large reductions on ROCm ([#193291](https://github.com/pytorch/pytorch/pull/193291))
- Fix a deadlock when a lazy-init callback such as `torch.cuda.manual_seed` re-enters CUDA lazy initialization ([#182948](https://github.com/pytorch/pytorch/pull/182948))
- Fix device-side assertions on CUDA 13 builds failing with `CUDA error: invalid argument` instead of reporting the assertion ([#195899](https://github.com/pytorch/pytorch/pull/195899))
- Fix CUDA graph annotation bugs: `mark_stream` mutating the caller's dict ([#194851](https://github.com/pytorch/pytorch/pull/194851)), leaked annotations ([#198418](https://github.com/pytorch/pytorch/pull/198418)), missing backward annotations with the CUPTI backend ([#194853](https://github.com/pytorch/pytorch/pull/194853)), and `get_graph_data()` failing on batch memory-operation nodes ([#193091](https://github.com/pytorch/pytorch/pull/193091))
- Fix `torch.cuda.make_graphed_callables` graphs being garbage-collected during an unrelated capture ([#195397](https://github.com/pytorch/pytorch/pull/195397))
- Fix `torch.cuda.empty_cache()` unmapping expandable segments on another device without synchronizing it ([#197159](https://github.com/pytorch/pytorch/pull/197159)), and expandable segments imported over IPC each reserving about 9/8 of device memory ([#198129](https://github.com/pytorch/pytorch/pull/198129))
- Fix several memory visualizer (MemoryViz) bugs, including wrong pool attribution and underreported peaks ([#199335](https://github.com/pytorch/pytorch/pull/199335), [#199415](https://github.com/pytorch/pytorch/pull/199415), [#193989](https://github.com/pytorch/pytorch/pull/193989))
- Recover from a corrupted or truncated JITerator kernel cache entry by recompiling the kernel ([#186346](https://github.com/pytorch/pytorch/pull/186346))
### performance
- Avoid CPU-GPU synchronization when assigning scalars through indexing on CUDA, e.g. `x[mask] = 1.0` ([#189303](https://github.com/pytorch/pytorch/pull/189303), [#188330](https://github.com/pytorch/pytorch/pull/188330), [#198811](https://github.com/pytorch/pytorch/pull/198811))
- Speed up CUDA `upsample_linear1d` by 5-25x for small outputs ([#180885](https://github.com/pytorch/pytorch/pull/180885)), pooling backward ([#191086](https://github.com/pytorch/pytorch/pull/191086), [#195119](https://github.com/pytorch/pytorch/pull/195119), [#196156](https://github.com/pytorch/pytorch/pull/196156)), dtype-conversion copies ([#195542](https://github.com/pytorch/pytorch/pull/195542), [#198723](https://github.com/pytorch/pytorch/pull/198723)), 2D transpose copies ([#194310](https://github.com/pytorch/pytorch/pull/194310)), and `zero_` ([#195303](https://github.com/pytorch/pytorch/pull/195303), [#198565](https://github.com/pytorch/pytorch/pull/198565))
- `torch.topk` on CUDA 13 Linux wheels uses ahead-of-time compiled radix-select kernels on Hopper and Blackwell (median 2.16x on H100) ([#190899](https://github.com/pytorch/pytorch/pull/190899))
### docs
### devs
- Update the bundled CUTLASS to v4.8.0 and CUTLASS-Operators to v0.3.0 ([#198179](https://github.com/pytorch/pytorch/pull/198179))
### Untopiced
### not user facing
- Re-enable expandable segments for CUDA graph private pools in internal (fbcode) builds; open-source builds already used them ([#194767](https://github.com/pytorch/pytorch/pull/194767))
- Move the caching allocator's active-capture counter into a new internal `CUDAGraphMemory` tracker, with no behavior change ([#195510](https://github.com/pytorch/pytorch/pull/195510))
- Simplify stateless RNG `split()` / `fold_in()` kernels ([#190036](https://github.com/pytorch/pytorch/pull/190036))
- Stop instantiating unreachable `cat` kernels and unused grouped FP8 GEMM variants, reducing binary size ([#194184](https://github.com/pytorch/pytorch/pull/194184), [#194189](https://github.com/pytorch/pytorch/pull/194189))
- Clean up `RowwiseScaledMM` CUTLASS arguments and warning suppressions ([#195396](https://github.com/pytorch/pytorch/pull/195396))
- Replace `qsort` with `std::sort` in CUDA index utilities ([#195470](https://github.com/pytorch/pytorch/pull/195470))
- Remove unused local tensors in batch norm statistics ([#199479](https://github.com/pytorch/pytorch/pull/199479))
- Log recoverable `cudaMalloc` failures in the CUDA caching allocator at INFO level instead of WARNING ([#193391](https://github.com/pytorch/pytorch/pull/193391)) (cut for length)
- Fix an out-of-bounds read in the cuDNN/MIOpen CTC loss eligibility check when `target_lengths` is longer than `input_lengths` ([#196084](https://github.com/pytorch/pytorch/pull/196084)) (cut for length)
- Fix lost updates in pinned host memory allocator statistics with concurrent memory pools ([#199144](https://github.com/pytorch/pytorch/pull/199144)) (cut for length)
- Fix a process abort when recording an event fails while freeing pinned host memory ([#198426](https://github.com/pytorch/pytorch/pull/198426)) (cut for length)
- Fix a reference counting bug in `torch.cuda.memory_snapshot` argument handling ([#199044](https://github.com/pytorch/pytorch/pull/199044)) (cut for length)
- Remove an input-sized copy from `torch.multinomial` on CUDA ([#194391](https://github.com/pytorch/pytorch/pull/194391)) (cut for length)
- Use fused `sincos` in the CUDA `torch.polar` kernel ([#193729](https://github.com/pytorch/pytorch/pull/193729)) (cut for length)
- Reduce the per-launch CPU overhead of the stray-context check in compiled CUDA code ([#197566](https://github.com/pytorch/pytorch/pull/197566)) (cut for length)
- Improve layer norm backward performance on ROCm by choosing between tiled and two-pass kernels per shape ([#189405](https://github.com/pytorch/pytorch/pull/189405)) (cut for length)
- Speed up 2D `scatter_reduce_` and `index_reduce_` with `amin`/`amax` along `dim=0` on CUDA ([#195537](https://github.com/pytorch/pytorch/pull/195537)) (cut for length)
- Fix a ROCm build failure with toolchains that declare `__builtin_amdgcn_flat_atomic_fadd_v2bf16` with a signed-short vector type ([#196538](https://github.com/pytorch/pytorch/pull/196538)) (cut for length)
### security
