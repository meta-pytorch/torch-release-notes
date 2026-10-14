
# Release Notes worksheet inductor

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

## inductor
### bc breaking
- `torch.compiler.nested_compile_region(options=...)` now accepts only an allowlist of Inductor config patches ([#195864](https://github.com/pytorch/pytorch/pull/195864), [#195865](https://github.com/pytorch/pytorch/pull/195865))

  Patches passed through `get_invoke_subgraph_compile_options(fw_inductor_config_patches=..., bw_inductor_config_patches=...)` used to accept any `torch._inductor.config` key, though many were silently ignored. Only `fallback_by_default` and `max_autotune` are now accepted; other keys raise `ValueError: Inductor config key '<key>' is not supported in forward nested compile-region options` (or `backward`). Apply other options to the whole compiled function. Patch dictionaries are now snapshotted when the options are created, so later mutation has no effect, and the default no longer implicitly sets `triton.autotune_at_compile_time=True`.

  Version 2.14:
  ```python
  opts = get_invoke_subgraph_compile_options(fw_inductor_config_patches={"triton.multi_kernel": 1})
  ```

  Version 2.15:
  ```python
  opts = get_invoke_subgraph_compile_options(fw_inductor_config_patches={"max_autotune": True})
  compiled = torch.compile(fn, options={"triton.multi_kernel": 1})
  ```
- `torch.compiler.precompile` is now a module instead of a callable; capture with `torch.compiler.precompile.capture(...)` and reload with `torch.compiler.precompile.load(...)` ([#197993](https://github.com/pytorch/pytorch/pull/197993), [#198135](https://github.com/pytorch/pytorch/pull/198135), [#198213](https://github.com/pytorch/pytorch/pull/198213))

  Calling `torch.compiler.precompile(fn, *example_inputs)` now raises `TypeError: 'module' object is not callable`. `capture(fn, *, artifact_path, cache_path)` returns a context manager that you call once inside the `with` block; it writes both files on exit, and `load` now takes those paths. `decompositions=` moves to `tracer=MakeFxTracer(decompositions=...)`.

  Version 2.14:
  ```python
  python_code, cache = torch.compiler.precompile(lambda m, x: m(x), model, x)
  f = torch.compiler.precompile.load(python_code, cache)
  ```

  Version 2.15:
  ```python
  with torch.compiler.precompile.capture(lambda m, x: m(x), artifact_path="m.py", cache_path="m.cache") as cap:
      cap(model, x)
  f = torch.compiler.precompile.load("m.py", "m.cache")
  ```
### deprecation
- Deprecate `torch._inductor.config.triton.use_block_ptr` because Triton removed its block-pointer API ([#191007](https://github.com/pytorch/pytorch/pull/191007))

  With a Triton that no longer provides block pointers, `use_block_ptr=True` is now a no-op that falls back to the default indexing path with a one-time `FutureWarning: config.triton.use_block_ptr=True but the installed Triton no longer provides the block-pointer frontend API`, instead of failing with `CompilationError: ... Block pointers have been removed in favor of the tensor descriptor API`. Use tensor descriptors instead.

  Version 2.14:
  ```python
  torch._inductor.config.triton.use_block_ptr = True
  ```

  Version 2.15:
  ```python
  torch._inductor.config.triton.use_tensor_descriptor = True
  ```

- Deprecate the no-op `torch._inductor.config.use_mixed_mm` and `torch._inductor.config.mixed_mm_choice` settings ([#193721](https://github.com/pytorch/pytorch/pull/193721))

  These settings have been ignored since the tuned `mixed_mm` path was removed. Reading or setting either now emits a one-time `FutureWarning` such as `torch._inductor.config.use_mixed_mm is deprecated and does not do anything`. The `mixed_mm` AutoHeuristic options were removed. Delete these settings from your code.

  Version 2.14:
  ```python
  torch._inductor.config.use_mixed_mm = True  # silently ignored
  ```

  Version 2.15:
  ```python
  # FutureWarning; delete the line
  ```

- Rename `torch._inductor.config.benchmark_epilogue_fusion` to `benchmark_template_fusion` and `max_epilogue_benchmarked_choices` to `max_template_fusion_benchmarked_choices` ([#198430](https://github.com/pytorch/pytorch/pull/198430))

  The settings also cover prologue fusion, so the old names were misleading. The old names remain as deprecated aliases that emit a one-time `FutureWarning`. The environment variable is now `TORCHINDUCTOR_BENCHMARK_TEMPLATE_FUSION`; `TORCHINDUCTOR_BENCHMARK_EPILOGUE_FUSION` is still read as a fallback.

  Version 2.14:
  ```python
  torch._inductor.config.benchmark_epilogue_fusion = False
  ```

  Version 2.15:
  ```python
  torch._inductor.config.benchmark_template_fusion = False
  ```
### new features
- Add thread-based Inductor compile workers for free-threaded Python, selected with `TORCH_COMPILE_WORKER_MODE=thread` or `auto` to avoid process-spawn and pickling overhead ([#179547](https://github.com/pytorch/pytorch/pull/179547), [#179548](https://github.com/pytorch/pytorch/pull/179548))
- Add an experimental FlyDSL GEMM autotuning backend for ROCm gfx950, covering FP16/BF16 `mm`, `grouped_mm` and MXFP4/MXFP8 `scaled_mm`, enabled by adding `FLYDSL` to `torch._inductor.config.max_autotune_gemm_backends` ([#190903](https://github.com/pytorch/pytorch/pull/190903), [#192877](https://github.com/pytorch/pytorch/pull/192877), [#194032](https://github.com/pytorch/pytorch/pull/194032), [#194303](https://github.com/pytorch/pytorch/pull/194303), [#194981](https://github.com/pytorch/pytorch/pull/194981), [#196719](https://github.com/pytorch/pytorch/pull/196719))
- Add `"strict_pointwise"` and `"strict_reduction"` values to `torch._inductor.config.numerics` and make `"strict"` match eager numerics more closely ([#192883](https://github.com/pytorch/pytorch/pull/192883), [#195640](https://github.com/pytorch/pytorch/pull/195640))
### improvements
- Enable nested reduction fusion by default (`TORCHINDUCTOR_NESTED_REDUCTION=0` disables it), fusing patterns such as RMSNorm followed by MXFP8/NVFP4 quantization into one kernel ([#190594](https://github.com/pytorch/pytorch/pull/190594), [#190595](https://github.com/pytorch/pytorch/pull/190595), [#191974](https://github.com/pytorch/pytorch/pull/191974), [#193598](https://github.com/pytorch/pytorch/pull/193598), [#196332](https://github.com/pytorch/pytorch/pull/196332), [#196333](https://github.com/pytorch/pytorch/pull/196333), [#196334](https://github.com/pytorch/pytorch/pull/196334))
- Extend NVGEMM epilogue fusion (CuTeDSL-generated dense epilogues, grouped reduction epilogues, `swap_ab` configs) and support `nvidia-cutlass-operators` 0.2.0 ([#190820](https://github.com/pytorch/pytorch/pull/190820), [#190821](https://github.com/pytorch/pytorch/pull/190821), [#190822](https://github.com/pytorch/pytorch/pull/190822), [#191514](https://github.com/pytorch/pytorch/pull/191514), [#191515](https://github.com/pytorch/pytorch/pull/191515), [#192298](https://github.com/pytorch/pytorch/pull/192298), [#194792](https://github.com/pytorch/pytorch/pull/194792), [#194793](https://github.com/pytorch/pytorch/pull/194793), [#194873](https://github.com/pytorch/pytorch/pull/194873), [#195231](https://github.com/pytorch/pytorch/pull/195231), [#195538](https://github.com/pytorch/pytorch/pull/195538), [#193940](https://github.com/pytorch/pytorch/pull/193940), [#196984](https://github.com/pytorch/pytorch/pull/196984))
- Extend host-side TMA descriptors to the Blackwell persistent TMA GEMM template, and support Triton kernels that need global scratch memory in the static launcher ([#191133](https://github.com/pytorch/pytorch/pull/191133), [#193857](https://github.com/pytorch/pytorch/pull/193857), [#194126](https://github.com/pytorch/pytorch/pull/194126), [#196410](https://github.com/pytorch/pytorch/pull/196410), [#196998](https://github.com/pytorch/pytorch/pull/196998))
- Add CUDA Graph Trees options `triton.cudagraph_managed_input_rerecord_limit`, `triton.cudagraph_initial_mempool_allocation_gb` and `triton.cudagraph_dynamic_shape_rerecord_limit` to limit re-recording and memory-pool fragmentation ([#191369](https://github.com/pytorch/pytorch/pull/191369), [#196378](https://github.com/pytorch/pytorch/pull/196378), [#197433](https://github.com/pytorch/pytorch/pull/197433))
- Add `autotune_cudagraph_benchmarking_iters` and hold the benchmark lock across multi-kernel comparisons to reduce autotuning noise ([#196413](https://github.com/pytorch/pytorch/pull/196413), [#192876](https://github.com/pytorch/pytorch/pull/192876))
- Add B200, GB300 and more ROCm GPUs to Inductor's device table so roofline heuristics such as `pad_mm` use datasheet values ([#194297](https://github.com/pytorch/pytorch/pull/194297), [#196398](https://github.com/pytorch/pytorch/pull/196398), [#196506](https://github.com/pytorch/pytorch/pull/196506), [#196944](https://github.com/pytorch/pytorch/pull/196944), [#198220](https://github.com/pytorch/pytorch/pull/198220))
- Improve combo kernels with runtime per-subkernel block-size tuning and grouping across dependency layers ([#189003](https://github.com/pytorch/pytorch/pull/189003), [#192622](https://github.com/pytorch/pytorch/pull/192622))
- Support the ROCm 7.14+ CK-Tile GEMM API and avoid compile-time blowups in ROCm Composable Kernel builds ([#189646](https://github.com/pytorch/pytorch/pull/189646), [#195023](https://github.com/pytorch/pytorch/pull/195023))
- Add `fusion_memory_timeline_peak_memory_increase_gb` and `fusion_memory_timeline_peak_memory_pct_threshold` to reject fusions that raise peak memory ([#190344](https://github.com/pytorch/pytorch/pull/190344))
- Add an opt-in Triton `bmm` template for a batch-broadcast left operand (`bmm_shared_a`) ([#193049](https://github.com/pytorch/pytorch/pull/193049))
- Add `alignment_asserts_inputs` to assert, rather than silently clone, misaligned graph inputs ([#196379](https://github.com/pytorch/pytorch/pull/196379))
- Accept out-of-tree backend config values as `"<device>.<key>"` in `torch.compile(options=...)` ([#194998](https://github.com/pytorch/pytorch/pull/194998))
- Honor `assume_32bit_indexing` for dynamic size arguments ([#194127](https://github.com/pytorch/pytorch/pull/194127))
- Use recipe-aware layout constraints for `_scaled_mm_v2` ([#197029](https://github.com/pytorch/pytorch/pull/197029))
- Support three reduction dimensions in N-D reduction tiling ([#197437](https://github.com/pytorch/pytorch/pull/197437))
- Add `include_fallback` to custom-op autotuning ([#197446](https://github.com/pytorch/pytorch/pull/197446))
- Keep Triton FP fusion on for templates to preserve numerics with Triton 3.9 ([#199500](https://github.com/pytorch/pytorch/pull/199500))
- Apply split/cat optimizations to `torch.concatenate` ([#195174](https://github.com/pytorch/pytorch/pull/195174))
- Reuse the CUTLASS sm120 kernel generators on sm121 GPUs ([#197621](https://github.com/pytorch/pytorch/pull/197621))
- Add an opt-in `bmm_skip_dynamic_shape_dim_check` to decompose CPU `bmm` whose batch size cannot be proven ([#197016](https://github.com/pytorch/pytorch/pull/197016))
### bug fixes
- Disable the 4x-vectorized Triton RNG path, which produced correlated CUDA dropout masks since 2.13 (`TORCHINDUCTOR_USE_RAND4X=1` restores it) ([#198680](https://github.com/pytorch/pytorch/pull/198680))
- Fix silently wrong results from in-place mutations: reinplaced scatters and `index_put` whose sources alias the input, `remove_noop_ops` on copies of mutated inputs, fusions across repeated mutations of one buffer, and mutations of buffers already referenced by views ([#198010](https://github.com/pytorch/pytorch/pull/198010), [#198132](https://github.com/pytorch/pytorch/pull/198132), [#198325](https://github.com/pytorch/pytorch/pull/198325), [#198549](https://github.com/pytorch/pytorch/pull/198549), [#198637](https://github.com/pytorch/pytorch/pull/198637))
- Fix silently wrong results for `resize_()` on a no-op view of a returned intermediate, non-contiguous reshape views, and `torch.while_loop` whose `cond_fn` mutates a captured tensor ([#191844](https://github.com/pytorch/pytorch/pull/191844), [#192575](https://github.com/pytorch/pytorch/pull/192575), [#195393](https://github.com/pytorch/pytorch/pull/195393))
- Fix silently wrong gradients and results from mix-order reductions with views into a shared buffer (a regression since 2.10) or row counts not divisible by `XBLOCK` ([#193103](https://github.com/pytorch/pytorch/pull/193103), [#196565](https://github.com/pytorch/pytorch/pull/196565))
- Fix corrupted gradients from a reused `nested_compile_region` that inherited donated-buffer indices ([#193960](https://github.com/pytorch/pytorch/pull/193960))
- Fix wrong results from the Triton FP8 blockwise `scaled_mm` template, including DeepSeek-style scales ([#195751](https://github.com/pytorch/pytorch/pull/195751), [#197028](https://github.com/pytorch/pytorch/pull/197028), [#197458](https://github.com/pytorch/pytorch/pull/197458))
- Fix wrong results from SDPA pattern fusion when the key is permuted other than `key.transpose(-2, -1)`, and failures with a 0-d tensor scale ([#195383](https://github.com/pytorch/pytorch/pull/195383), [#191496](https://github.com/pytorch/pytorch/pull/191496))
- Fix wrong results in pre-/post-grad fusion passes: batched `aten.sub` dropping `alpha`, batched linear mixing dtypes, one-element tuple replacements, `merge_select_cat_aten`, and batch math fusion of `torch.clamp` and in-place dropout ([#195463](https://github.com/pytorch/pytorch/pull/195463), [#197069](https://github.com/pytorch/pytorch/pull/197069), [#197832](https://github.com/pytorch/pytorch/pull/197832), [#198638](https://github.com/pytorch/pytorch/pull/198638), [#198285](https://github.com/pytorch/pytorch/pull/198285))
- Fix compile failures in the partitioned scatter, joint-graph no-op removal and view cleanup passes and the constant `cumsum` pattern ([#194366](https://github.com/pytorch/pytorch/pull/194366), [#193052](https://github.com/pytorch/pytorch/pull/193052), [#193708](https://github.com/pytorch/pytorch/pull/193708), [#193422](https://github.com/pytorch/pytorch/pull/193422), [#193959](https://github.com/pytorch/pytorch/pull/193959))
- Fix compiled `torch.special.log_ndtr`, `torch.frexp` and `torch.nextafter` edge cases (signed zeros, subnormals, `float16`/`bfloat16`), `torch.randn` with `align_random_eager=True`, and `torch.nan_to_num` on complex inputs ([#191339](https://github.com/pytorch/pytorch/pull/191339), [#195041](https://github.com/pytorch/pytorch/pull/195041), [#196578](https://github.com/pytorch/pytorch/pull/196578), [#194118](https://github.com/pytorch/pytorch/pull/194118), [#190428](https://github.com/pytorch/pytorch/pull/190428))
- Accumulate `float16`/`bfloat16` Triton scans such as `cumsum` in `float32` ([#199088](https://github.com/pytorch/pytorch/pull/199088))
- Fix boolean `index_put(..., accumulate=True)` on GPU ([#193584](https://github.com/pytorch/pytorch/pull/193584))
- Fix compiled max pooling with indices returning transposed indices for non-contiguous inputs, and `adaptive_max_pool3d` gradients on channels-last inputs ([#197596](https://github.com/pytorch/pytorch/pull/197596), [#199068](https://github.com/pytorch/pytorch/pull/199068))
- Fix wrong `argmax`/`argmin` indices after layout changes or loop reordering ([#195178](https://github.com/pytorch/pytorch/pull/195178))
- Fix wrong results under `dynamic=True` when a dimension guarded equal to 1 is broadcast ([#198774](https://github.com/pytorch/pytorch/pull/198774))
- Fix dynamic-shape compile errors (`cannot determine truth value of Relational`, `GuardOnDataDependentSymNode`, `ValueRangeError`) with symbolic strides, unbacked tiling and reshapes, and negative `constant_pad_nd` padding ([#185871](https://github.com/pytorch/pytorch/pull/185871), [#196081](https://github.com/pytorch/pytorch/pull/196081), [#199105](https://github.com/pytorch/pytorch/pull/199105), [#195465](https://github.com/pytorch/pytorch/pull/195465))
- Fix wrong results on XPU from the `mm_plus_mm` and `bmm`/`baddbmm` Triton templates ([#189516](https://github.com/pytorch/pytorch/pull/189516))
- Fix crashes and wrong output from the Triton `grouped_mm` template on very large inputs ([#192649](https://github.com/pytorch/pytorch/pull/192649))
- Fix static-launcher `float16`/`bfloat16` scalar arguments being passed with the wrong width ([#184065](https://github.com/pytorch/pytorch/pull/184065))
- Fix CUDA Graph Trees capturing cross-device extern kernels, `Detected N tensor(s) in the cudagraph pool not tracked as outputs` errors with pending backwards, static kernels partitioned out under `cudagraph_skip_dynamic_graphs`, and backward graphs treating activations as static inputs ([#190555](https://github.com/pytorch/pytorch/pull/190555), [#194124](https://github.com/pytorch/pytorch/pull/194124), [#197139](https://github.com/pytorch/pytorch/pull/197139), [#197438](https://github.com/pytorch/pytorch/pull/197438))
- Fix `NameError` for complex indexed assignment with `mode="reduce-overhead"` and graph partitioning ([#199414](https://github.com/pytorch/pytorch/pull/199414))
- Fix `CUDA driver error: misaligned address` in backward for misaligned saved inputs ([#192263](https://github.com/pytorch/pytorch/pull/192263))
- Fix version-counter errors in backward for inputs mutated outside the compiled graph ([#185876](https://github.com/pytorch/pytorch/pull/185876))
- Emit runtime asserts for backed `SymInt` inputs when `prefer_deferred_runtime_asserts_over_guards=True` ([#185588](https://github.com/pytorch/pytorch/pull/185588))
- Fix reordering of consecutive side-effectful ops that lower to different kernel types ([#188301](https://github.com/pytorch/pytorch/pull/188301))
- Fix a CPU buffer being passed to a CUDA kernel after an incorrect device-copy elimination ([#199402](https://github.com/pytorch/pytorch/pull/199402))
- Fix wrong results on MPS when masked loads were deduplicated ([#199673](https://github.com/pytorch/pytorch/pull/199673))
- Fix user-defined Triton kernels with mutated offset views (out-of-bounds reads), non-builtin `tl.constexpr` values, aliased `triton.language` imports, `float` literals, and buffer views in the FX wrapper backend ([#192227](https://github.com/pytorch/pytorch/pull/192227), [#189692](https://github.com/pytorch/pytorch/pull/189692), [#196237](https://github.com/pytorch/pytorch/pull/196237), [#190340](https://github.com/pytorch/pytorch/pull/190340), [#193820](https://github.com/pytorch/pytorch/pull/193820))
- Fix autotuning errors with deduplicated `bmm` inputs, pipelined autotuning, stale benchmark futures, decompose-K or ROCm `multi_kernel_hints` (`NoValidChoicesError`), 0-d `addmm` biases, `CantSplit` template-fusion choices, and deterministic combo kernels ([#188268](https://github.com/pytorch/pytorch/pull/188268), [#193094](https://github.com/pytorch/pytorch/pull/193094), [#196148](https://github.com/pytorch/pytorch/pull/196148), [#196453](https://github.com/pytorch/pytorch/pull/196453), [#196510](https://github.com/pytorch/pytorch/pull/196510), [#197214](https://github.com/pytorch/pytorch/pull/197214), [#199113](https://github.com/pytorch/pytorch/pull/199113), [#189724](https://github.com/pytorch/pytorch/pull/189724))
- Honor `max_autotune_gemm_search_space="EXHAUSTIVE"` with decompose-K and benchmark all candidates under the same CUDA graph policy ([#192285](https://github.com/pytorch/pytorch/pull/192285), [#194649](https://github.com/pytorch/pytorch/pull/194649))
- Fix crashes, stack overflows and graph cycles in overlap scheduling, `control_deps` lowering and manual collective bucketing, and remove duplicate waits on one collective ([#192268](https://github.com/pytorch/pytorch/pull/192268), [#192628](https://github.com/pytorch/pytorch/pull/192628), [#192903](https://github.com/pytorch/pytorch/pull/192903), [#195517](https://github.com/pytorch/pytorch/pull/195517), [#197323](https://github.com/pytorch/pytorch/pull/197323), [#199227](https://github.com/pytorch/pytorch/pull/199227), [#199228](https://github.com/pytorch/pytorch/pull/199228))
- Fix FlexAttention decoding reading the query at wrong offsets after a pointwise op, max-autotune failures with inlined captured buffers, and `TORCHINDUCTOR_EMIT_POINTER_RANGE_32=0` being ignored ([#198543](https://github.com/pytorch/pytorch/pull/198543), [#194555](https://github.com/pytorch/pytorch/pull/194555), [#194136](https://github.com/pytorch/pytorch/pull/194136))
- Fix NVGEMM errors in block-scaled GEMMs, with a broken optional `cutlass.operators` install, and when benchmarking aliased inputs ([#194727](https://github.com/pytorch/pytorch/pull/194727), [#198292](https://github.com/pytorch/pytorch/pull/198292), [#199072](https://github.com/pytorch/pytorch/pull/199072))
- Fix CPU backend compile errors for boolean vector masks, a spurious `ZeroDivisionError` from integer `%`, wrong mkldnn transposed-convolution channels, and integer `bmm` returning `int64` ([#184155](https://github.com/pytorch/pytorch/pull/184155), [#199560](https://github.com/pytorch/pytorch/pull/199560), [#192025](https://github.com/pytorch/pytorch/pull/192025), [#184950](https://github.com/pytorch/pytorch/pull/184950), [#191324](https://github.com/pytorch/pytorch/pull/191324))
- Fix ROCm CK-Tile GEMM autotuning dropping all `float16` kernels and `float8_e4m3fnuz`/`float8_e5m2fnuz` cast errors ([#193902](https://github.com/pytorch/pytorch/pull/193902), [#197905](https://github.com/pytorch/pytorch/pull/197905))
- Fix failures after fp32 matmul precision was set through `torch.backends.cuda.matmul.fp32_precision` ([#189955](https://github.com/pytorch/pytorch/pull/189955), [#196860](https://github.com/pytorch/pytorch/pull/196860))
- Fix kernel builds with only `libcuda.so.1`, the `CUDA_HOME` fallback for `nvcc`, ROCm on Windows, and DSL ops with `triton-rocm` ([#186538](https://github.com/pytorch/pytorch/pull/186538), [#197573](https://github.com/pytorch/pytorch/pull/197573), [#194471](https://github.com/pytorch/pytorch/pull/194471), [#195022](https://github.com/pytorch/pytorch/pull/195022))
- Match eager shape errors for meta transposed convolution and over-broadcast `addmm`/`addmv` inputs ([#188328](https://github.com/pytorch/pytorch/pull/188328), [#195594](https://github.com/pytorch/pytorch/pull/195594))
- Fail instead of hanging when a compile worker dies, and treat a cleared local cache as a miss ([#192301](https://github.com/pytorch/pytorch/pull/192301), [#196189](https://github.com/pytorch/pytorch/pull/196189))
- Fix `AttributeError` with `torch._foreach_pow` on integer tensors ([#198675](https://github.com/pytorch/pytorch/pull/198675))
- Fix compile crashes for `float16`/`bfloat16` floor division of `arange` values, nested grouped-reduction epilogues, fallback kernels without tensor inputs, and an early `FakeTensorUpdater` ([#197132](https://github.com/pytorch/pytorch/pull/197132), [#195874](https://github.com/pytorch/pytorch/pull/195874), [#197584](https://github.com/pytorch/pytorch/pull/197584), [#196946](https://github.com/pytorch/pytorch/pull/196946))
- Fix symmetric-memory `alloc_id` size-mismatch errors after reseeding `random` between compilations ([#192089](https://github.com/pytorch/pytorch/pull/192089))
- Fix Triton-based TFLOPS estimates being off by 1000x ([#196372](https://github.com/pytorch/pytorch/pull/196372))
- Fix Triton template kernels being compiled twice when the worker pool is warm ([#197471](https://github.com/pytorch/pytorch/pull/197471))
### performance
- Reduce compile time by caching in fusion search and codegen, hashing sources in the background, and compiling combo-kernel benchmarks in parallel ([#186319](https://github.com/pytorch/pytorch/pull/186319), [#192817](https://github.com/pytorch/pytorch/pull/192817), [#192820](https://github.com/pytorch/pytorch/pull/192820), [#194010](https://github.com/pytorch/pytorch/pull/194010), [#194011](https://github.com/pytorch/pytorch/pull/194011), [#198747](https://github.com/pytorch/pytorch/pull/198747), [#198881](https://github.com/pytorch/pytorch/pull/198881), [#198320](https://github.com/pytorch/pytorch/pull/198320))
- Allow mix-order reduction fusion for more shapes, speeding up RMSNorm backward ([#186370](https://github.com/pytorch/pytorch/pull/186370), [#188660](https://github.com/pytorch/pytorch/pull/188660))
- Reduce `cpp_wrapper` kernel call overhead by 40-50% ([#192287](https://github.com/pytorch/pytorch/pull/192287))
- Improve CPU FlexAttention BF16 performance by 6-29% ([#191780](https://github.com/pytorch/pytorch/pull/191780))
- Use larger reduction tiles on GB300, roughly doubling HBM bandwidth use ([#193774](https://github.com/pytorch/pytorch/pull/193774))
- Add gfx950 FlexAttention backward configs (1.8-2.3x faster) ([#194151](https://github.com/pytorch/pytorch/pull/194151))
- Improve NVGEMM NVFP4 decode performance on Blackwell and widen its autotuning candidates ([#194651](https://github.com/pytorch/pytorch/pull/194651), [#194652](https://github.com/pytorch/pytorch/pull/194652), [#197485](https://github.com/pytorch/pytorch/pull/197485), [#195539](https://github.com/pytorch/pytorch/pull/195539), [#198293](https://github.com/pytorch/pytorch/pull/198293))
- Compute only one triangle for large BF16 `X @ X.T` on SM100 ([#194177](https://github.com/pytorch/pytorch/pull/194177), [#194178](https://github.com/pytorch/pytorch/pull/194178))
- Speed up collective bucketing, including up to 9x faster uneven reduce-scatter padding ([#196647](https://github.com/pytorch/pytorch/pull/196647), [#196621](https://github.com/pytorch/pytorch/pull/196621), [#195616](https://github.com/pytorch/pytorch/pull/195616))
- Simplify `slice_scatter` chains to reduce recomputation and peak memory ([#192136](https://github.com/pytorch/pytorch/pull/192136), [#195608](https://github.com/pytorch/pytorch/pull/195608), [#195631](https://github.com/pytorch/pytorch/pull/195631))
- Fix CPU OpenMP parallelization moving onto inner reduction loops under freezing, and recover an XPU inner-reduction regression ([#190928](https://github.com/pytorch/pytorch/pull/190928), [#190986](https://github.com/pytorch/pytorch/pull/190986))
- Fuse `torch.cat`/`torch.stack` copies into foreach kernels for dynamic shapes ([#198294](https://github.com/pytorch/pytorch/pull/198294))
### docs
- Document the FlexAttention `ROWS_GUARANTEED_SAFE` requirement ([#194154](https://github.com/pytorch/pytorch/pull/194154))
### devs
- Add `DeviceInterface` and `DeviceOpOverrides` extension points for out-of-tree accelerator backends ([#190326](https://github.com/pytorch/pytorch/pull/190326), [#190614](https://github.com/pytorch/pytorch/pull/190614), [#192896](https://github.com/pytorch/pytorch/pull/192896), [#193908](https://github.com/pytorch/pytorch/pull/193908), [#190615](https://github.com/pytorch/pytorch/pull/190615))
- Add a keyed registry for `InductorChoices` overrides ([#194097](https://github.com/pytorch/pytorch/pull/194097))
- Let out-of-tree backends register FlexAttention backward templates and override the `MetalKernel` launch device ([#195786](https://github.com/pytorch/pytorch/pull/195786), [#195809](https://github.com/pytorch/pytorch/pull/195809))
- Add declarative `implies` support to Inductor/Dynamo `Config` ([#196663](https://github.com/pytorch/pytorch/pull/196663))
### Untopiced
### not user facing
- Unskip test_bmm_large_batch_dynamic on ROCm ([#184531](https://github.com/pytorch/pytorch/pull/184531))
- Fix test_comprehensive_addbmm_cpu_float16 precision mismatch ([#187171](https://github.com/pytorch/pytorch/pull/187171))
- Add private stateless RNG `randint`/`bits` APIs in `torch.func._random` ([#190253](https://github.com/pytorch/pytorch/pull/190253))
- Fix typos in comments and docstrings ([#190565](https://github.com/pytorch/pytorch/pull/190565))
- Enable 2-CTA kernels for Blackwell max-autotune GEMM with Meta's warp-specialization Triton fork ([#190769](https://github.com/pytorch/pytorch/pull/190769))
- Support swap_ab local reductions in the private FlexGEMM backend ([#190793](https://github.com/pytorch/pytorch/pull/190793))
- Add NVGEMM grouped epilogue parity tests ([#190825](https://github.com/pytorch/pytorch/pull/190825))
- Support blocked local-reduce output layouts in the private FlexGEMM backend ([#191026](https://github.com/pytorch/pytorch/pull/191026))
- Keep `.item()` (`aten._local_scalar_dense`) on its dedicated lowering in lite mode (`fallback_by_default`) ([#191254](https://github.com/pytorch/pytorch/pull/191254))
- Support bool main outputs in the private FlexGEMM backend ([#191271](https://github.com/pytorch/pytorch/pull/191271))
- Keep `aten.sym_size.int` on its dedicated lowering in lite mode ([#191295](https://github.com/pytorch/pytorch/pull/191295))
- Materialize Python scalars passed as Tensor arguments for proxy-executor fallback kernels in AOTInductor lite mode ([#191380](https://github.com/pytorch/pytorch/pull/191380))
- Use dtype-aware tolerances in OpInfo property tests ([#191557](https://github.com/pytorch/pytorch/pull/191557))
- Skip mm padding when the matmul is lowered as pointwise ops ([#192072](https://github.com/pytorch/pytorch/pull/192072))
- Remove a dead frame walk in `_find_names` ([#192123](https://github.com/pytorch/pytorch/pull/192123))
- Test dynamic-shape TunableOp wildcard dispatch ([#192144](https://github.com/pytorch/pytorch/pull/192144))
- Add TunableOp layout/scaled coverage tests ([#192148](https://github.com/pytorch/pytorch/pull/192148))
- Drop dead num_stages axis from ROCm exhaustive mm configs ([#192286](https://github.com/pytorch/pytorch/pull/192286))
- Enable multi-GPU FlexAttention tests on XPU ([#192494](https://github.com/pytorch/pytorch/pull/192494))
- Support contiguous transposed reduction outputs in the private FlexGEMM backend ([#192661](https://github.com/pytorch/pytorch/pull/192661))
- Add autoWS max-autotune config set for Meta's Triton fork ([#192830](https://github.com/pytorch/pytorch/pull/192830))
- Support block-scaled GEMMs in the private FlexGEMM backend ([#192839](https://github.com/pytorch/pytorch/pull/192839))
- Move the CuTeDSL inner-tree sum override into a shared reductions module ([#192881](https://github.com/pytorch/pytorch/pull/192881))
- Skip NVGEMM operator API tests internally ([#192928](https://github.com/pytorch/pytorch/pull/192928))
- Rename internal strict_sum identifiers to strict_reduction ([#192995](https://github.com/pytorch/pytorch/pull/192995))
- Use public CUTLASS DSL `min`/`max` APIs in the private FlexGEMM backend for compatibility with older CUTLASS DSL releases ([#193032](https://github.com/pytorch/pytorch/pull/193032))
- Keep `aten.sym_size.int` lowered by Inductor in lite mode (`fallback_by_default`) ([#193243](https://github.com/pytorch/pytorch/pull/193243))
- Support multiple outputs in the private `inline_asm_elementwise` operator ([#193434](https://github.com/pytorch/pytorch/pull/193434))
- Support the private `inline_asm_elementwise` operator inside FlexAttention `score_mod`/`mask_mod` ([#193459](https://github.com/pytorch/pytorch/pull/193459))
- Add opt-in private libc++ build support for AOTInductor model libraries ([#193846](https://github.com/pytorch/pytorch/pull/193846))
- Guard mutation tests that require Triton block pointers ([#194090](https://github.com/pytorch/pytorch/pull/194090))
- Remove manual XPU Triton module unloading in fresh_cache, fixing access violations in Windows XPU tests ([#194217](https://github.com/pytorch/pytorch/pull/194217))
- Support user-defined Triton kernels in AOTInductor lite mode ([#194255](https://github.com/pytorch/pytorch/pull/194255))
- Typing cleanup ([#194275](https://github.com/pytorch/pytorch/pull/194275))
- Typing cleanup ([#194461](https://github.com/pytorch/pytorch/pull/194461))
- Typing cleanup ([#194482](https://github.com/pytorch/pytorch/pull/194482))
- Fix FlexAttention FLASH captured-float test expectation ([#194483](https://github.com/pytorch/pytorch/pull/194483))
- Typing cleanup ([#194540](https://github.com/pytorch/pytorch/pull/194540))
- Loosen fp16 grad tolerance for special.i1/i1e on XPU ([#194566](https://github.com/pytorch/pytorch/pull/194566))
- Update dynamic vision_maskrcnn graph-break baselines ([#194630](https://github.com/pytorch/pytorch/pull/194630))
- Add subgraph memory planning tests ([#194820](https://github.com/pytorch/pytorch/pull/194820))
- Eagerly load codegen heuristic modules ([#194822](https://github.com/pytorch/pytorch/pull/194822))
- Typing cleanup ([#194825](https://github.com/pytorch/pytorch/pull/194825))
- Enable MXFP8 nested-reduction test on XPU ([#194864](https://github.com/pytorch/pytorch/pull/194864))
- Remove remaining `mixed_mm` leftovers from the autoheuristic fuzzer and docs ([#195104](https://github.com/pytorch/pytorch/pull/195104))
- Rename CompilerConfigExtra fields ([#195156](https://github.com/pytorch/pytorch/pull/195156))
- Pass CompilerConfigExtra to fw_compiler_freezing ([#195157](https://github.com/pytorch/pytorch/pull/195157))
- Add direct scheduler unit tests ([#195336](https://github.com/pytorch/pytorch/pull/195336))
- Fix no-op config restriction in TestTemplateConfigPruning ([#195461](https://github.com/pytorch/pytorch/pull/195461))
- Trace deallocation of MTIA tensors in Dynamo for cross-stream safety ([#195524](https://github.com/pytorch/pytorch/pull/195524))
- Fix grid size in a graph-partition test ([#195546](https://github.com/pytorch/pytorch/pull/195546))
- Typing cleanup ([#195938](https://github.com/pytorch/pytorch/pull/195938))
- Typing cleanup ([#196021](https://github.com/pytorch/pytorch/pull/196021))
- Let Inductor own QuACK autotuning in the private FlexGEMM backend ([#196174](https://github.com/pytorch/pytorch/pull/196174))
- Accept 1-D captured tensors in the private FlexGEMM backend ([#196183](https://github.com/pytorch/pytorch/pull/196183))
- Support `F.grouped_mm` in the private FlexGEMM backend ([#196318](https://github.com/pytorch/pytorch/pull/196318))
- Keep fp32 GEMMs off QuACK in the private FlexGEMM backend unless TF32 is allowed ([#196319](https://github.com/pytorch/pytorch/pull/196319))
- Support grouped-main SwiGLU on the grouped_mm path in the private FlexGEMM backend ([#196321](https://github.com/pytorch/pytorch/pull/196321))
- Typing cleanup ([#196364](https://github.com/pytorch/pytorch/pull/196364))
- Typing cleanup ([#196513](https://github.com/pytorch/pytorch/pull/196513))
- Guard triton CPU test ([#196515](https://github.com/pytorch/pytorch/pull/196515))
- Test configuration fix ([#196541](https://github.com/pytorch/pytorch/pull/196541))
- Test configuration fix ([#196542](https://github.com/pytorch/pytorch/pull/196542))
- Xfail unsupported 4D flex indexing test on H100 ([#196543](https://github.com/pytorch/pytorch/pull/196543))
- Remove stale GELU xfail ([#196544](https://github.com/pytorch/pytorch/pull/196544))
- Let custom CUDAGraph policies override the supported device types ([#196625](https://github.com/pytorch/pytorch/pull/196625))
- Gate CUDA TMA tests on CUDA devices ([#196636](https://github.com/pytorch/pytorch/pull/196636))
- Skip internal CPU tests pending Triton upgrade ([#196655](https://github.com/pytorch/pytorch/pull/196655))
- Internal tlx_mode knob ([#196718](https://github.com/pytorch/pytorch/pull/196718))
- Test megacache loading during kernel finalization ([#196763](https://github.com/pytorch/pytorch/pull/196763))
- Make local AOTI arrayref tests host-independent ([#196917](https://github.com/pytorch/pytorch/pull/196917))
- Gate remaining CUDA TMA tests on CUDA devices ([#197141](https://github.com/pytorch/pytorch/pull/197141))
- Relax __rpow__ OpInfo gradient tolerance on ROCm ([#197185](https://github.com/pytorch/pytorch/pull/197185))
- Fix TMA fast-launcher fallback test ([#197414](https://github.com/pytorch/pytorch/pull/197414))
- Fix SIGABRT in ROCm AOTI standalone binary tests ([#197421](https://github.com/pytorch/pytorch/pull/197421))
- Share a compile-recording harness in graph-partition tests ([#197899](https://github.com/pytorch/pytorch/pull/197899))
- Enable ROCm FP8 scaled_mm tests ([#198291](https://github.com/pytorch/pytorch/pull/198291))
- Refactor FlexGEMM layout recognition ([#198421](https://github.com/pytorch/pytorch/pull/198421))
- Enable ROCm FP8 scaled_mm v2 tests ([#198588](https://github.com/pytorch/pytorch/pull/198588))
- Enable ROCm FP8 scaled_mm swizzle tests ([#198600](https://github.com/pytorch/pytorch/pull/198600))
- Internal AOTI libstdc++ link fix ([#198944](https://github.com/pytorch/pytorch/pull/198944))
- Call super().setUp() in test_dynamic_tunable_ops ([#198979](https://github.com/pytorch/pytorch/pull/198979))
- Disable loop flattening for Blackwell WS templates when Meta's WS Triton knob is on ([#199061](https://github.com/pytorch/pytorch/pull/199061))
- Isolate combo kernel grid tests from caches ([#199095](https://github.com/pytorch/pytorch/pull/199095))
- Fix stale precision key in a CUTLASS test ([#199248](https://github.com/pytorch/pytorch/pull/199248))
- Lazily load the TLX registry ([#199427](https://github.com/pytorch/pytorch/pull/199427))
- xfail AOTI arrayref tests under lite mode ([#199434](https://github.com/pytorch/pytorch/pull/199434))
- Fix view loaders evaluated without an active graph (follow-up to #199402) ([#199608](https://github.com/pytorch/pytorch/pull/199608))
- Require SM90 for an AOTI CUTLASS test ([#199660](https://github.com/pytorch/pytorch/pull/199660))
- Don't reinplace all_reduce that may lower as one-shot symmetric memory (fixes a regression from #198549 within this release) ([#199661](https://github.com/pytorch/pytorch/pull/199661))
- Loosen a test tolerance ([#199663](https://github.com/pytorch/pytorch/pull/199663))
- Stop printing verbose FX graph cache-key details to the `torch._inductor.codecache` debug log; they remain available in cache events and tlparse artifacts ([#186217](https://github.com/pytorch/pytorch/pull/186217)) (cut for length)
- Name the offending operator and its schema in `Unsupported return type` errors for extern kernels ([#195868](https://github.com/pytorch/pytorch/pull/195868)) (cut for length)
- Log at debug level when a Triton config is retried without software pipelining after an out-of-resources launch failure ([#199416](https://github.com/pytorch/pytorch/pull/199416)) (cut for length)
- Warm up the async compile worker pool for every Triton-backed device, and skip it when the CUDA backend does not use Triton ([#199635](https://github.com/pytorch/pytorch/pull/199635)) (cut for length)
- Fix the bias device check that gates CPU weight packing for `addmm` under freezing, which checked the weight instead of the bias ([#195833](https://github.com/pytorch/pytorch/pull/195833)) (cut for length)
- Add an opt-in pattern (`torch._inductor.config.var_std_reduction_dedup`) that shares the reduction when both `torch.var` and `torch.std` are computed on the same tensor ([#182945](https://github.com/pytorch/pytorch/pull/182945)) (cut for length)
- Enable layout optimization for backward graphs that contain `convolution_backward` without a forward convolution ([#188236](https://github.com/pytorch/pytorch/pull/188236)) (cut for length)
- Cache host-side TMA descriptors across launches in the static Triton launcher ([#188823](https://github.com/pytorch/pytorch/pull/188823)) (cut for length)
- Keep large attention masks consumed by masked SDPA out of horizontal combo kernels, preserving producer-consumer locality and reducing peak memory ([#189002](https://github.com/pytorch/pytorch/pull/189002)) (cut for length)
- Use per-row scalar accumulators in large non-persistent CUDA reduction loops that contain an online softmax, including the other reductions in those kernels (`torch._inductor.config.triton.scalar_accumulators`, on by default) ([#190692](https://github.com/pytorch/pytorch/pull/190692), [#196371](https://github.com/pytorch/pytorch/pull/196371)) (cut for length)
- Avoid redundant full-tile loads in masked reductions when the loaded value only depends on the output row ([#192410](https://github.com/pytorch/pytorch/pull/192410)) (cut for length)
- Lower `index_add` with `bfloat16` through the Triton decomposition on SM90+ and ROCm so it can fuse instead of falling back to ATen ([#195192](https://github.com/pytorch/pytorch/pull/195192)) (cut for length)
- Drop a compiler-proven all-zero attention bias from `aten._scaled_dot_product_efficient_attention` forward and backward calls ([#196068](https://github.com/pytorch/pytorch/pull/196068), [#196079](https://github.com/pytorch/pytorch/pull/196079)) (cut for length)
- Apply the `index_add` unique-index rewrite when the index is a full `torch.randperm`, not only a sliced one ([#196873](https://github.com/pytorch/pytorch/pull/196873)) (cut for length)
- Reuse base storage for views when generating example inputs for compile-time autotuning instead of re-allocating it ([#198660](https://github.com/pytorch/pytorch/pull/198660)) (cut for length)
### security
