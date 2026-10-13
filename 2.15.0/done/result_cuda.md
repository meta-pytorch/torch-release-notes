
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

  Previously the CUDA implementation computed the histogram in the input dtype and then silently cast it into `out`, so any `out` dtype was accepted (for example, a float histogram was truncated into an `int64` tensor). The CPU and MPS implementations already required the dtypes to match. CUDA now performs the same check and raises the same error as CPU, and the meta implementation used by `torch.compile` enforces it too. Even a widening `out` dtype, such as a `float64` `out` for `float32` input, is rejected. To keep the previous behavior, compute the histogram without `out` and cast the result yourself.

  Version 2.14:
  ```python
  >>> x = torch.randn(8, device="cuda")
  >>> out = torch.empty(4, dtype=torch.int64, device="cuda")
  >>> torch.histc(x, bins=4, min=-2.0, max=2.0, out=out)  # silently truncated into int64
  tensor([1, 3, 3, 1], device='cuda:0')
  ```

  Version 2.15:
  ```python
  >>> torch.histc(x, bins=4, min=-2.0, max=2.0, out=out)
  RuntimeError: torch.histogram: input tensor and hist tensor should have the same dtype, but got input float and hist long int
  >>> # Workaround: compute in the input dtype, then cast
  >>> out.copy_(torch.histc(x, bins=4, min=-2.0, max=2.0))
  ```
- On CUDA, cuBLAS and cuBLASLt workspaces are now allocated for each operation instead of being cached per handle and stream ([#194311](https://github.com/pytorch/pytorch/pull/194311))

  Previously ATen kept one persistent workspace for each cuBLAS(Lt) handle and CUDA stream until `torch._C._cuda_clearCublasWorkspaces()` was called. Separately captured CUDA graphs on the same stream could share that workspace, and replaying them could fail with `CUDA error: an illegal memory access was encountered`. ATen now allocates the workspace from the CUDA caching allocator for each operation and frees it when the operation returns. You may notice this change if:

  - Your code or tests check memory after a matmul: `torch.cuda.memory_allocated()` no longer includes a persistent cuBLAS workspace. The workspace now only shows up in peak statistics such as `torch.cuda.max_memory_allocated()`.
  - Your extension calls cuBLAS directly with the handle from `torch.cuda.current_blas_handle()` (or `at::cuda::getCurrentCUDABlasHandle()` / `torch_get_current_cuda_blas_handle`): the handle no longer has an ATen workspace attached, so cuBLAS uses its default workspace.
  - You set `TORCH_CUBLASLT_UNIFIED_WORKSPACE`: it now only takes effect when workspace caching is enabled.
  - You are sensitive to small-GEMM CPU overhead: the PR's benchmarks measured roughly 0.1-0.8 us more per GEMM.

  Set `TORCH_CUBLAS_WORKSPACE_CACHE=1` to restore the previous caching. Do not use cached workspaces if you capture multiple CUDA graphs on the same stream. This PR leaves ROCm caching workspaces by default; the ROCm notes cover the matching hipBLAS/hipBLASLt change ([#196920](https://github.com/pytorch/pytorch/pull/196920)).

  Version 2.14:
  ```python
  >>> a = torch.randn(1024, 1024, device="cuda")
  >>> out = torch.empty_like(a)
  >>> before = torch.cuda.memory_allocated()
  >>> torch.mm(a, a, out=out)
  >>> torch.cuda.memory_allocated() - before > 0  # workspace stays allocated
  True
  ```

  Version 2.15:
  ```python
  >>> torch.mm(a, a, out=out)
  >>> torch.cuda.memory_allocated() - before  # workspace was freed after the op
  0
  >>> # To keep the old caching, launch with TORCH_CUBLAS_WORKSPACE_CACHE=1
  ```
### deprecation
- `torch.cuda.graph_annotations.clear_kernel_annotations()` is deprecated and now emits a `FutureWarning` ([#195398](https://github.com/pytorch/pytorch/pull/195398))

  The CUDA graph kernel annotation registry now cleans up after itself. Annotations are rekeyed to the executable graph when it is instantiated and dropped when that graph is destroyed, so you no longer need to clear the registry after consuming annotations. In a long-running job that replays its graphs for the whole run, a global clear also discards annotations for graphs that are still live. The function still clears the registry, but it does not stop backward hooks that `mark_kernels` already attached to live autograd nodes from recording; the earlier documentation said it did. Remove the call, and reset or delete a graph to drop its annotations. The same PR also fixes annotations leaking when a capture fails in `capture_end`.

  Version 2.14:
  ```python
  from torch.cuda.graph_annotations import clear_kernel_annotations, get_kernel_annotations

  g = torch.cuda.CUDAGraph()
  with torch.cuda.graph(g, enable_annotations=True):
      ...
  annotations = get_kernel_annotations()
  clear_kernel_annotations()  # previously recommended once annotations were consumed
  ```

  Version 2.15:
  ```python
  from torch.cuda.graph_annotations import get_kernel_annotations

  g = torch.cuda.CUDAGraph()
  with torch.cuda.graph(g, enable_annotations=True):
      ...
  annotations = get_kernel_annotations()
  # No clear needed; g's annotations are dropped when g is reset or destroyed.
  ```
### new features
- Add `GreenContext.split` and `torch.cuda.green_contexts.SMPartition` for creating green contexts with disjoint SM allocations ([#198278](https://github.com/pytorch/pytorch/pull/198278))

  Green contexts created by separate `GreenContext(num_sms=...)` calls are not guaranteed to use disjoint SMs. `GreenContext.split` creates several contexts in one call, and their SM allocations do not overlap. `SMPartition.from_device(...).split(...)` does the same but also returns the remaining SMs, and a partition can be further subdivided by creating a context from it and splitting its `sm_partition`. Split options such as `num_sms` and `coscheduled_sm_count` accept a scalar or a sequence, and `num_sms=0` discovers the largest group that satisfies the constraints. The new `GreenContext.sm_count` property reports the number of SMs actually allocated, including for contexts created with the existing constructor. This requires a CUDA driver and `cuda.bindings` 13.1 or newer.

  ```python
  from torch.cuda.green_contexts import GreenContext

  a, b = GreenContext.split(num_sms=(24, 40), coscheduled_sm_count=(8, 4), device_id=0)
  print(a.sm_count, b.sm_count)
  ```
- Add locality-domain constraints to SM partitioning for green contexts ([#198279](https://github.com/pytorch/pytorch/pull/198279))

  `GreenContext.split` and `SMPartition.split` accept `locality_domain_ids` to restrict each group to a hardware locality domain, for example to create one context per domain. The new `torch.cuda.green_contexts.get_num_locality_domains()` and `is_localization_supported()` query the device topology (the latter without initializing CUDA when possible), and partitions and contexts expose a `locality_domain_id` property. Splitting with locality constraints requires a CUDA driver and `cuda.bindings` 13.4 or newer.

  ```python
  from torch.cuda.green_contexts import GreenContext, get_num_locality_domains

  n = get_num_locality_domains(device_id=0)
  contexts = GreenContext.split(
      locality_domain_ids=tuple(range(n)), coscheduled_sm_count=2, device_id=0
  )
  ```
- Add a `"bfx9"` FP32 matmul precision mode that uses cuBLAS's BF16x9 algorithm ([#195301](https://github.com/pytorch/pytorch/pull/195301))

  Setting `torch.backends.cuda.matmul.fp32_precision = "bfx9"` keeps FP32 inputs and outputs while allowing cuBLAS to split each input into three BF16 values and accumulate the nine BF16 products in FP32. The algorithm runs on GPUs with compute capability 10.0 or 10.3; on other NVIDIA GPUs cuBLAS accepts the setting but uses native FP32. The mode requires a PyTorch build with CUDA 12.9 or newer and is valid only for `torch.backends.cuda.matmul.fp32_precision`; it raises an error on older CUDA builds, on ROCm, and for other precision settings. Under `torch.compile`, FP32 matmuls stay as cuBLAS calls in this mode, and fused Triton kernels that cannot honor it (such as FP32 FlexAttention) warn once and fall back to IEEE precision.
### improvements
- Support scalar `scatter` for float8 dtypes on CUDA ([#197199](https://github.com/pytorch/pytorch/pull/197199))
- Add a `cuda_graph_annotations` argument to `export_chrome_trace` that writes CUDA graph kernel annotations from `torch.cuda.graph_annotations` directly into the exported Chrome trace, replacing the previous offline post-processing step ([#194854](https://github.com/pytorch/pytorch/pull/194854))
- Add an `annotation_config` argument to `torch.cuda.graph` for CUDA graph kernel annotations. `annotation_config={"backend": "cupti"}` attributes graph nodes from CUPTI node-creation callbacks, which also annotates scopes entered before the current stream starts capturing and scales better with deep nesting; the default `"auto"` uses CUPTI when available ([#191999](https://github.com/pytorch/pytorch/pull/191999))
- Add `annotation_config={"key_by": "source"}`, which keys CUDA graph kernel annotations by the captured graph node and makes it possible to annotate kernels inside nested `torch.cond` / `torch.while_loop` graph bodies; requires a CUDA 13.4 driver ([#196528](https://github.com/pytorch/pytorch/pull/196528)). Under source keying, peer-to-peer copy and host nodes, which CUPTI reports without a source node id, keep their annotations through an executable-graph alias ([#196530](https://github.com/pytorch/pytorch/pull/196530)). The new `annotation_config={"key_by": "auto"}` uses source keying when the driver supports it and executable-graph keying otherwise, instead of raising; `"exec"` remains the default ([#197577](https://github.com/pytorch/pytorch/pull/197577))
- `CUDAGraph.get_graph_data()` now reports each kernel node's `grid_dim`, `block_dim` and dynamic shared memory size, plus programmatic dependency edge data ([#196018](https://github.com/pytorch/pytorch/pull/196018), [#196527](https://github.com/pytorch/pytorch/pull/196527))
- Add opt-in `PYTORCH_CUDA_ALLOC_CONF` options `expandable_segments_reserve` and `expandable_segments_reserve_by_class` that shrink the virtual-address reservation of expandable segments (by default 9/8 of device memory) to a fraction of device memory or an absolute size, with per-stream classes selected from C++ ([#192269](https://github.com/pytorch/pytorch/pull/192269))
- When creating an expandable segment fails because virtual address space ran out, the allocator now logs the requested reservation, the live segment count and bytes, and the options that reduce the reservation; out-of-memory messages with expandable segments enabled also point at these options. C++ gauges for reserved bytes and segment count are added ([#193211](https://github.com/pytorch/pytorch/pull/193211))
- CUDA out-of-memory errors now say when a custom `MemPool` allocator returned a null pointer, so the failure is not mistaken for device-wide memory exhaustion ([#199363](https://github.com/pytorch/pytorch/pull/199363))
- Add an opt-in `TORCH_CUDA_CHECK_STRAY_CONTEXT=warn|error` environment variable that makes `torch.cuda.set_device` warn or raise when another device already holds a CUDA primary context, which helps find code that accidentally creates a context on GPU 0 before each rank selects its device ([#191036](https://github.com/pytorch/pytorch/pull/191036))
### bug fixes
- Fix silently wrong results from `arange`, `range`, `linspace` and `logspace` on CUDA when the output has 2^32 or more elements ([#197713](https://github.com/pytorch/pytorch/pull/197713))
- Fix illegal memory accesses from 32-bit index overflow in `torch.cdist` backward ([#198452](https://github.com/pytorch/pytorch/pull/198452)) and in `torch.bincount` with values above `INT_MAX` ([#189685](https://github.com/pytorch/pytorch/pull/189685)) on CUDA
- Fix a race condition in the memory-efficient attention forward kernel that produced nondeterministic NaNs with head dimension 256 or larger on Ampere, Ada and consumer Blackwell GPUs ([#198922](https://github.com/pytorch/pytorch/pull/198922))
- Fix CUDA batch norm reductions under AMP rounding fp32 partial sums through half precision, which could overflow to `inf` ([#196125](https://github.com/pytorch/pytorch/pull/196125))
- Fix rare incorrect indices from `argmax`, `argmin`, `max` and `min` on ROCm for large reductions that span multiple thread blocks ([#193291](https://github.com/pytorch/pytorch/pull/193291))
- Fix a deadlock when a callback queued through CUDA lazy initialization, such as `torch.cuda.manual_seed` or `torch.cuda.set_rng_state`, re-enters lazy initialization ([#182948](https://github.com/pytorch/pytorch/pull/182948))
- Recover from a corrupted or truncated JITerator kernel cache entry by recompiling the kernel, instead of failing with a CUDA driver "invalid argument" error ([#186346](https://github.com/pytorch/pytorch/pull/186346))
- Stop the CUDA caching allocator from logging a warning on every recoverable `cudaMalloc` failure; the message is now logged at INFO level and can be shown with `TORCH_CPP_LOG_LEVEL=INFO` ([#193391](https://github.com/pytorch/pytorch/pull/193391))
- Fix an out-of-bounds read in the cuDNN/MIOpen CTC loss eligibility check when `target_lengths` is longer than `input_lengths` ([#196084](https://github.com/pytorch/pytorch/pull/196084))
- Fix lost updates and contention in pinned host memory allocator statistics when several memory pools are used concurrently ([#199144](https://github.com/pytorch/pytorch/pull/199144))
- Fix `torch.cuda.graph_annotations` `mark_stream` modifying the caller's annotation dict, which made regions marked with a reused dict all render on the same lane ([#194851](https://github.com/pytorch/pytorch/pull/194851))
- Fix CUDA graph kernel annotations leaking for graphs captured without an active profiler and for graphs that are never instantiated; each graph now drops its annotations when it is destroyed ([#198418](https://github.com/pytorch/pytorch/pull/198418))
- Fix CUDA graph annotations with `annotation_config={"backend": "cupti"}` silently not annotating backward kernels when `backward=True` ([#194853](https://github.com/pytorch/pytorch/pull/194853))
- Fix `CUDAGraph.get_graph_data()` failing on driver-created batch memory-operation nodes, which are now reported as `batch_mem_op` ([#193091](https://github.com/pytorch/pytorch/pull/193091))
- Fix `torch.cuda.make_graphed_callables` leaving its CUDA graphs in reference cycles, so the cyclic garbage collector could destroy one in the middle of an unrelated capture, invalidating it with "operation not permitted when stream is capturing" ([#195397](https://github.com/pytorch/pytorch/pull/195397))
- Fix an illegal memory access in CUDA `embedding_bag` backward with `per_sample_weights` when an index is out of range or a large `int64` index was truncated to 32 bits ([#193408](https://github.com/pytorch/pytorch/pull/193408))
- Fix device-side assertions on CUDA 13 builds failing with `CUDA error: invalid argument` instead of reporting the assertion ([#195899](https://github.com/pytorch/pytorch/pull/195899))
- Fix out-of-bounds writes or illegal memory accesses from `torch.bmm` on CUDA when the contraction dimension is 1 and `(batch - 1) * M * N` exceeds `INT32_MAX` ([#196431](https://github.com/pytorch/pytorch/pull/196431)), and fall back to the ATen kernel for this case when the Triton driver cannot initialize instead of failing ([#197695](https://github.com/pytorch/pytorch/pull/197695))
- Fix `torch.cuda.empty_cache()` unmapping expandable segments on another device without synchronizing that device first ([#197159](https://github.com/pytorch/pytorch/pull/197159))
- Fix importing an expandable segment over IPC reserving about 9/8 of device memory in virtual address space per import, which could exhaust the address space; only the shared extent is reserved now ([#198129](https://github.com/pytorch/pytorch/pull/198129))
- Fix a process abort when recording an event fails while freeing pinned host memory in the caching host allocator ([#198426](https://github.com/pytorch/pytorch/pull/198426))
- Fix a reference counting bug in `torch.cuda.memory_snapshot` argument handling that could free objects still in use by the caller ([#199044](https://github.com/pytorch/pytorch/pull/199044))
- Fix several memory visualizer (MemoryViz) bugs: historical events attributed to the wrong memory pool, underreported peaks and misplaced summarized allocations at lower detail levels, and rendering problems in Safari ([#199335](https://github.com/pytorch/pytorch/pull/199335), [#199415](https://github.com/pytorch/pytorch/pull/199415), [#193989](https://github.com/pytorch/pytorch/pull/193989))
### performance
- Avoid CPU-GPU synchronization and extra CPU tensors when assigning scalars through indexing on CUDA tensors, e.g. `x[idx] = 1.0`, `x[mask] = 1.0` and assignment with a scalar GPU tensor index ([#189303](https://github.com/pytorch/pytorch/pull/189303), [#188330](https://github.com/pytorch/pytorch/pull/188330), [#198811](https://github.com/pytorch/pytorch/pull/198811))
- Speed up `upsample_linear1d` forward and backward on CUDA by 5-25x when the output width is small ([#180885](https://github.com/pytorch/pytorch/pull/180885))
- Speed up pooling backward kernels on CUDA: a fast path for non-overlapping `avg_pool2d` (about 1.4x), a hoisted divisor in `avg_pool3d`, and packed half/bfloat16 atomics in `adaptive_max_pool2d`, `adaptive_max_pool3d` and `max_pool3d` ([#191086](https://github.com/pytorch/pytorch/pull/191086), [#195119](https://github.com/pytorch/pytorch/pull/195119), [#196156](https://github.com/pytorch/pytorch/pull/196156))
- Remove an input-sized copy from `torch.multinomial` on CUDA, reducing memory use and runtime ([#194391](https://github.com/pytorch/pytorch/pull/194391))
- Use fused `sincos` in the CUDA `torch.polar` kernel ([#193729](https://github.com/pytorch/pytorch/pull/193729))
- Reduce the per-launch CPU overhead added by the stray-context check in compiled CUDA code ([#197566](https://github.com/pytorch/pytorch/pull/197566))
- Improve layer norm backward performance on ROCm by choosing between tiled and two-pass kernels per shape ([#189405](https://github.com/pytorch/pytorch/pull/189405))
- `zero_` on CUDA now uses `cudaMemsetAsync` instead of a fill kernel, saving about 2 us of host time per call and running faster on small buffers. On ROCm 7.0.x the fill kernel is still used during CUDA graph capture. This also lets `zero_` work on dense `bits*` and `float4_e2m1fn_x2` tensors, which used to raise an error ([#195303](https://github.com/pytorch/pytorch/pull/195303), [#198565](https://github.com/pytorch/pytorch/pull/198565))
- Speed up CUDA dtype conversion copies with vectorized bf16/fp16 -> fp32 kernels (up to about 1.3x) and specialized int32/bool -> int64 and bool -> float64 kernels ([#195542](https://github.com/pytorch/pytorch/pull/195542), [#198723](https://github.com/pytorch/pytorch/pull/198723))
- Speed up 2D `scatter_reduce_` and `index_reduce_` with `amin`/`amax` along `dim=0` on CUDA ([#195537](https://github.com/pytorch/pytorch/pull/195537))
- Add a tiled CUDA kernel for copies that reduce to a dense 2D transpose, such as `x.t().contiguous()`, reaching close to plain-copy bandwidth for large transposes ([#194310](https://github.com/pytorch/pytorch/pull/194310))
- `torch.topk` on CUDA can use ahead-of-time compiled radix-select kernels shipped in the Linux CUDA 13 wheels for float32 and bfloat16 inputs on Hopper and Blackwell (last dimension, `largest=True`, `sorted=True`, row lengths 2048-16384, `k` of 64, 128 or 256), with a median 2.16x speedup over the previous kernel on H100 ([#190899](https://github.com/pytorch/pytorch/pull/190899))
### docs
### devs
- Update the bundled CUTLASS to v4.8.0 and CUTLASS-Operators to v0.3.0 ([#198179](https://github.com/pytorch/pytorch/pull/198179))
- Fix a ROCm build failure with toolchains that declare `__builtin_amdgcn_flat_atomic_fadd_v2bf16` with a signed-short vector type ([#196538](https://github.com/pytorch/pytorch/pull/196538))
### Untopiced
### not user facing
- Re-enable expandable segments for CUDA graph private pools in internal (fbcode) builds; open-source builds already used them ([#194767](https://github.com/pytorch/pytorch/pull/194767))
- Move the caching allocator's active-capture counter into a new internal `CUDAGraphMemory` tracker, with no behavior change ([#195510](https://github.com/pytorch/pytorch/pull/195510))
- Simplify stateless RNG `split()` / `fold_in()` kernels ([#190036](https://github.com/pytorch/pytorch/pull/190036))
- Stop instantiating unreachable `cat` kernels and unused grouped FP8 GEMM variants, reducing binary size ([#194184](https://github.com/pytorch/pytorch/pull/194184), [#194189](https://github.com/pytorch/pytorch/pull/194189))
- Clean up `RowwiseScaledMM` CUTLASS arguments and warning suppressions ([#195396](https://github.com/pytorch/pytorch/pull/195396))
- Replace `qsort` with `std::sort` in CUDA index utilities ([#195470](https://github.com/pytorch/pytorch/pull/195470))
- Remove unused local tensors in batch norm statistics ([#199479](https://github.com/pytorch/pytorch/pull/199479))
### security
