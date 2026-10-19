
# Release Notes worksheet xpu

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

## xpu
### bc breaking
- Remove the `allocator` property from `torch.xpu.MemPool`, aligning with other accelerators ([#192041](https://github.com/pytorch/pytorch/pull/192041))

  `torch.xpu.MemPool` no longer exposes the allocator it was constructed with, so `pool.allocator` now raises `AttributeError`. Keep your own reference to the allocator instead; passing one to the `MemPool` constructor is unchanged.

  Before:

  ```python
  pool = torch.xpu.MemPool(allocator.allocator())
  my_allocator = pool.allocator
  ```

  After:

  ```python
  my_allocator = allocator.allocator()
  pool = torch.xpu.MemPool(my_allocator)
  ```

### deprecation
### new features
- SYCL Kernel Programming Simplified: Add SYCL free-function kernel support to the XPU backend and migrate most existing SYCL kernels to it, so device code can be written as explicit free functions in a more intuitive style instead of verbose functors ([#196387](https://github.com/pytorch/pytorch/pull/196387), [#196932](https://github.com/pytorch/pytorch/pull/196932), [#198200](https://github.com/pytorch/pytorch/pull/198200), [#198720](https://github.com/pytorch/pytorch/pull/198720), [#200289](https://github.com/pytorch/pytorch/pull/200289))
- Enhanced XPU Runtime Capabilities: Support sharing `torch.xpu.Event` across processes, through `torch.multiprocessing` or `ipc_handle()` / `from_ipc_handle()` on an event created with `interprocess=True` ([#191182](https://github.com/pytorch/pytorch/pull/191182), [#192495](https://github.com/pytorch/pytorch/pull/192495), [#193399](https://github.com/pytorch/pytorch/pull/193399), [#192514](https://github.com/pytorch/pytorch/pull/192514))
- Improved XPU Profiling Experience: Add kernel-level visibility into XPU Graph replay, cross-rank correlation for XCCL collectives, and per-kernel hardware counter collection across all Intel GPUs in multi-GPU workloads to the XPU profiler ([#195128](https://github.com/pytorch/pytorch/pull/195128), [#198200](https://github.com/pytorch/pytorch/pull/198200))

### improvements
- Add `no_split` and `use_on_oom` support to `torch.xpu.MemPool` ([#192048](https://github.com/pytorch/pytorch/pull/192048), [#192033](https://github.com/pytorch/pytorch/pull/192033), [#192038](https://github.com/pytorch/pytorch/pull/192038))
- Support `torch.xpu.mem_get_info` and `torch.accelerator.get_memory_info` with a pluggable XPU allocator ([#197412](https://github.com/pytorch/pytorch/pull/197412))
- Add XPU support for `linalg.polar`, `linalg.qr` (out variant), `geqrf`, `linalg.householder_product`, `sparse.spsolve` and sparse `linalg.vector_norm`; `linalg.qr`, `geqrf` and `linalg.householder_product` now run natively instead of falling back to CPU ([#188253](https://github.com/pytorch/pytorch/pull/188253), [#187564](https://github.com/pytorch/pytorch/pull/187564), [#189372](https://github.com/pytorch/pytorch/pull/189372), [#194165](https://github.com/pytorch/pytorch/pull/194165), [#189238](https://github.com/pytorch/pytorch/pull/189238), [#193110](https://github.com/pytorch/pytorch/pull/193110))
- Use the XPU SDPA backend for multi-query attention even when `enable_gqa=True` is not passed, consistent with the CUDA and CPU checks ([#196731](https://github.com/pytorch/pytorch/pull/196731))
- Support unsigned integer dtypes in `where` and float8 in `scatter` fill on XPU ([#198720](https://github.com/pytorch/pytorch/pull/198720))
- Add mixed-precision support to the fused `Adam` and `AdamW` implementations on XPU ([#200289](https://github.com/pytorch/pytorch/pull/200289))
- Support large tensors in `upsample_bilinear2d` channels-last by using 64-bit indexing ([#200289](https://github.com/pytorch/pytorch/pull/200289))
- Support stateless Philox RNG operations `_philox_normal` and `_philox_uniform` on XPU ([#198200](https://github.com/pytorch/pytorch/pull/198200))
- Enable symmetric memory on XPU by registering a SymmetricMemory allocator for `torch.xpu.MemPool` ([#197065](https://github.com/pytorch/pytorch/pull/197065), [#198720](https://github.com/pytorch/pytorch/pull/198720))
- Support `Float4_e2m1fn_x2` and `Float8_e8m0fnu` in XCCL non-reduction collectives ([#198200](https://github.com/pytorch/pytorch/pull/198200))

### bug fixes
- Fix wrong `conv1d` backward results on XPU for some singleton-dimension layouts, caused by detecting the memory format before the 3D-to-4D view used by the oneDNN path ([#194328](https://github.com/pytorch/pytorch/pull/194328))
- Fix batch norm accuracy, `fft`/`ifft` on empty batches, `norm` global reductions, and half-precision `sampled_addmm` on XPU ([#193929](https://github.com/pytorch/pytorch/pull/193929))
- Fix precision loss in `addmm` and `baddbmm` for bf16/fp16 with non-trivial `alpha`/`beta` on XPU, which now accumulate in fp32 as CPU and CUDA do ([#174864](https://github.com/pytorch/pytorch/pull/174864))
- Fix `torch.xpu.mem_get_info` under-reporting free memory on Xe2 and later GPUs ([#195987](https://github.com/pytorch/pytorch/pull/195987))
- Fix XPU device indices not matching SYCL's order on platforms that enumerate an integrated GPU before the discrete ones ([#198336](https://github.com/pytorch/pytorch/pull/198336))
- Fix oneDNN SDPA with grouped-query attention and a mask broadcast in the head dimension ([#194973](https://github.com/pytorch/pytorch/pull/194973))
- Fix `torch.xpu.Event.record()` enqueueing two commands on first use, which could leave the event without profiling data and intermittently fail Inductor autotuning ([#194609](https://github.com/pytorch/pytorch/pull/194609))
- Fix "An event cannot be enqueued for signaling or waiting behind a command which is not enqueued in the backend" errors with oneCCL on Intel® Arc™ B-Series Graphics, by limiting reusable events to the IPC case ([#197396](https://github.com/pytorch/pytorch/pull/197396))
- Fix `_safe_softmax` incorrectly zeroing rows that contain NaN on XPU ([#195708](https://github.com/pytorch/pytorch/pull/195708))
- Fix incorrect `_weight_int4pack_mm` results on XPU ([#195708](https://github.com/pytorch/pytorch/pull/195708))
- Fix undefined behavior with NaN inputs in `topk`, a spurious `group_reduce` assert, and fused moving-average observer/fake-quantize dtype mismatches on XPU ([#194185](https://github.com/pytorch/pytorch/pull/194185))
- Fix an abort in the XPU flash attention backward with an empty batch, and return BSHD-contiguous input gradients from the XPU efficient attention backward ([#198200](https://github.com/pytorch/pytorch/pull/198200))
- Fix `weight_norm` running out of memory for 1-D inputs on XPU, and a host-to-device metadata race in nested `_transform_bias_rescale_qkv` ([#200289](https://github.com/pytorch/pytorch/pull/200289))
- Fix RNG stream reuse for large tensors on XPU ([#200289](https://github.com/pytorch/pytorch/pull/200289))

### performance
- Speed up SDPA training on XPU by aligning the oneDNN graph SDPA pattern with oneDNN v3.13 and integrating its GQA and dropout support ([#195419](https://github.com/pytorch/pytorch/pull/195419))
- Fuse the `GroupNorm` forward into a single kernel and speed up contiguous `cat` with vectorized stores on XPU ([#194842](https://github.com/pytorch/pytorch/pull/194842))
- Avoid register spilling in mixed fp32/bf16/fp16 elementwise kernels on XPU by adding vectorized type-casting loads ([#194185](https://github.com/pytorch/pytorch/pull/194185))
- Speed up `col2im` on XPU by replacing its hard-coded work-group size ([#198720](https://github.com/pytorch/pytorch/pull/198720))
- Reduce oneMKL LAPACK overhead on XPU by trimming scratchpad initialization, host synchronizations and re-allocation ([#193110](https://github.com/pytorch/pytorch/pull/193110))

### docs

### devs
- Build XPU with pure SYCL compilation and support Clang as the host compiler; expose `USE_SYCLTLA` and enable oneMKL sparse in the build system ([#194185](https://github.com/pytorch/pytorch/pull/194185), [#198720](https://github.com/pytorch/pytorch/pull/198720), [#196387](https://github.com/pytorch/pytorch/pull/196387), [#198200](https://github.com/pytorch/pytorch/pull/198200))
### Untopiced
### not user facing
### security
