
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

  The experimental per-region Inductor config patches passed through `get_invoke_subgraph_compile_options(fw_inductor_config_patches=..., bw_inductor_config_patches=...)` used to accept any `torch._inductor.config` key, even though many options were silently ignored or changed compiler-wide state. Only `fallback_by_default` and `max_autotune` are now accepted; any other key raises `ValueError: Inductor config key '<key>' is not supported in forward nested compile-region options` (or `backward`). Patch dictionaries are snapshotted when the options are created, so mutating them afterwards has no effect, and the default no longer implicitly sets `triton.autotune_at_compile_time=True`. To keep using another option, apply it to the whole compiled graph instead.

  Version 2.14:
  ```python
  from torch._higher_order_ops.invoke_subgraph import get_invoke_subgraph_compile_options

  # passing options= requires this experimental flag in both versions
  torch._dynamo.config.enable_invoke_subgraph_regional_compile = True

  opts = get_invoke_subgraph_compile_options(
      fw_inductor_config_patches={"triton.multi_kernel": 1}
  )

  @torch.compiler.nested_compile_region(options=opts)
  def block(x):
      return torch.sin(x)
  ```

  Version 2.15:
  ```python
  # ValueError: Inductor config key 'triton.multi_kernel' is not supported in
  # forward nested compile-region options
  opts = get_invoke_subgraph_compile_options(
      fw_inductor_config_patches={"triton.multi_kernel": 1}
  )

  # Supported region-local keys:
  opts = get_invoke_subgraph_compile_options(
      fw_inductor_config_patches={"max_autotune": True},
      bw_inductor_config_patches={"fallback_by_default": True},
  )

  # Other options apply to the whole compiled function:
  compiled = torch.compile(fn, options={"triton.multi_kernel": 1})
  ```
- `torch.compiler.precompile` is now a module instead of a callable; capture with `torch.compiler.precompile.capture(...)` and reload with `torch.compiler.precompile.load(...)` ([#197993](https://github.com/pytorch/pytorch/pull/197993), [#198135](https://github.com/pytorch/pytorch/pull/198135), [#198213](https://github.com/pytorch/pytorch/pull/198213))

  In 2.14, `torch.compiler.precompile` was a callable object: `precompile(fn, *example_inputs, backend="inductor", tracer="make_fx", decompositions=None)` traced `fn` once on the given inputs and returned an in-memory `(python_code, cache)` pair, which `torch.compiler.precompile.load(python_code, cache)` turned back into a runnable. `torch.compiler.precompile` is now a module (still a prototype API) with two entry points. `capture(fn, *, artifact_path, cache_path, tracer=MakeFxTracer(), backend="inductor")` returns a context manager: inside the `with` block you call it the way you would call `fn` (a make_fx capture takes exactly one call), and the artifact pair is written to the two files when the block exits cleanly or when `cap.save()` is called. `load(artifact_path, cache_path)` reads those files and returns a `torch.compiler.precompile.PrecompiledRunnable`. Calling the old API now raises `TypeError: 'module' object is not callable`, and `load` takes file paths instead of the in-memory strings. The `decompositions=` argument is now set on the tracer with `torch.compiler.precompile.MakeFxTracer(decompositions=...)`. The module also exports the `Capture`, `MakeFxTracer`, `PrecompiledRunnable` and `PrecompileSummary` types, and `torch.compiler.PrecompileError` is unchanged.

  Version 2.14:
  ```python
  python_code, cache = torch.compiler.precompile(lambda m, x: m(x), model, x)
  f = torch.compiler.precompile.load(python_code, cache)
  out = f(model, x)  # pass the model again at runtime
  ```

  Version 2.15:
  ```python
  # torch.compiler.precompile(lambda m, x: m(x), model, x)
  # TypeError: 'module' object is not callable

  with torch.compiler.precompile.capture(
      lambda m, x: m(x), artifact_path="m.py", cache_path="m.cache"
  ) as cap:
      out = cap(model, x)

  f = torch.compiler.precompile.load("m.py", "m.cache")
  out = f(model, x)  # pass the model again at runtime

  # decompositions= now goes on the tracer:
  from torch.compiler.precompile import MakeFxTracer
  cap = torch.compiler.precompile.capture(
      fn, artifact_path="m.py", cache_path="m.cache",
      tracer=MakeFxTracer(decompositions=my_decomposition_table),
  )
  ```
### deprecation
- Deprecate `torch._inductor.config.triton.use_block_ptr` because Triton removed its block-pointer API ([#191007](https://github.com/pytorch/pytorch/pull/191007))

  Upstream Triton removed `tl.make_block_ptr`/`tl.advance` in favor of tensor descriptors. Inductor now checks whether the installed Triton still provides the block-pointer API. If it does, `use_block_ptr=True` behaves as before. If it does not, the flag is a no-op: Inductor falls back to its default masked-indexing path (or the tensor-descriptor path where eligible) and emits a one-time `FutureWarning`, instead of failing with `CompilationError: ... Block pointers have been removed in favor of the tensor descriptor API`. The flag will be removed in a future release ([#191012](https://github.com/pytorch/pytorch/issues/191012)); use tensor descriptors instead.

  Version 2.14:
  ```python
  torch._inductor.config.triton.use_block_ptr = True
  torch.compile(fn)(x)
  # With a Triton that removed block pointers:
  # CompilationError: ... Block pointers have been removed in favor of the tensor descriptor API
  ```

  Version 2.15:
  ```python
  torch._inductor.config.triton.use_block_ptr = True
  torch.compile(fn)(x)
  # FutureWarning: config.triton.use_block_ptr=True but the installed Triton no longer
  # provides the block-pointer frontend API ...; falling back to the default
  # masked-indexing path. This flag is deprecated and will be removed (#191012).

  # Use tensor descriptors instead:
  torch._inductor.config.triton.use_tensor_descriptor = True
  ```

- Deprecate the no-op `torch._inductor.config.use_mixed_mm` and `torch._inductor.config.mixed_mm_choice` settings ([#193721](https://github.com/pytorch/pytorch/pull/193721))

  The tuned `mixed_mm` path was removed in an earlier release and these settings have been ignored since. Reading or setting either one now emits a one-time `FutureWarning` such as `torch._inductor.config.use_mixed_mm is deprecated and does not do anything. It will be removed in a future version of PyTorch.` The unused `mixed_mm` AutoHeuristic support was removed at the same time: `"mixed_mm"` is no longer the default of `TORCHINDUCTOR_AUTOHEURISTIC_USE`, and `torch._inductor.config.autoheuristic_collect.mixed_mm` / `autoheuristic_use.mixed_mm` no longer exist. Remove these settings from your code; they have no effect.

  Version 2.14:
  ```python
  torch._inductor.config.use_mixed_mm = True  # silently ignored
  ```

  Version 2.15:
  ```python
  torch._inductor.config.use_mixed_mm = True
  # FutureWarning: torch._inductor.config.use_mixed_mm is deprecated and does not do
  # anything. It will be removed in a future version of PyTorch.
  # Fix: delete the line.
  ```

- Rename `torch._inductor.config.benchmark_epilogue_fusion` to `benchmark_template_fusion` and `max_epilogue_benchmarked_choices` to `max_template_fusion_benchmarked_choices` ([#198430](https://github.com/pytorch/pytorch/pull/198430))

  These settings control benchmarking of template choices with prologue as well as epilogue fusion, so the old names were misleading. The old names remain as deprecated aliases that forward to the new settings and emit a one-time `FutureWarning`. The environment variable is now `TORCHINDUCTOR_BENCHMARK_TEMPLATE_FUSION`; `TORCHINDUCTOR_BENCHMARK_EPILOGUE_FUSION` is still read as a fallback.

  Version 2.14:
  ```python
  torch._inductor.config.benchmark_epilogue_fusion = False
  torch._inductor.config.max_epilogue_benchmarked_choices = 3
  ```

  Version 2.15:
  ```python
  torch._inductor.config.benchmark_template_fusion = False
  torch._inductor.config.max_template_fusion_benchmarked_choices = 3
  ```
### new features
- Add thread-based Inductor compile workers for free-threaded (no-GIL) Python builds, selected with `TORCH_COMPILE_WORKER_MODE=thread` or `TORCH_COMPILE_WORKER_MODE=auto`, which avoids process-spawn and pickling overhead. The default remains `process` ([#179547](https://github.com/pytorch/pytorch/pull/179547), [#179548](https://github.com/pytorch/pytorch/pull/179548))
- Add an experimental FlyDSL GEMM autotuning backend for ROCm gfx950 GPUs. Add `FLYDSL` to `torch._inductor.config.max_autotune_gemm_backends` (for example `"ATEN,TRITON,FLYDSL"`) to let max-autotune consider FlyDSL kernels for FP16/BF16 `torch.mm` in all input layouts, `F.grouped_mm`, and MXFP4/MXFP8 `scaled_mm`. The optional FlyDSL package must be installed, and multi-configuration tuning is opt-in through `torch._inductor.config.flydsl_enable_autotuning` (`FLYDSL_ENABLE_AUTOTUNING=1`) ([#190903](https://github.com/pytorch/pytorch/pull/190903), [#192877](https://github.com/pytorch/pytorch/pull/192877), [#194032](https://github.com/pytorch/pytorch/pull/194032), [#194303](https://github.com/pytorch/pytorch/pull/194303), [#194981](https://github.com/pytorch/pytorch/pull/194981), [#196719](https://github.com/pytorch/pytorch/pull/196719))
- Extend the `torch._inductor.config.numerics` mode for matching eager numerics, selectable with `TORCHINDUCTOR_NUMERICS=strict` or `torch.compile(options={"numerics": "strict"})`. `"strict"` now applies eager's inner-tree reduction order to `prod` as well as `sum`, the new `"strict_pointwise"` and `"strict_reduction"` values are accepted, and `"strict"`/`"strict_pointwise"` turn on `eager_numerics.disable_ftz`, `eager_numerics.division_rounding` and `emulate_precision_casts`. Strict modes may reduce performance ([#192883](https://github.com/pytorch/pytorch/pull/192883), [#195640](https://github.com/pytorch/pytorch/pull/195640))
### improvements
- Stop printing verbose FX graph cache-key details to the `torch._inductor.codecache` debug log; they remain available in cache events and tlparse artifacts ([#186217](https://github.com/pytorch/pytorch/pull/186217))
- Enable runtime coordinate-descent tuning of per-subkernel block sizes for combo kernels selected by compile-time autotuning ([#189003](https://github.com/pytorch/pytorch/pull/189003))
- Support the ROCm 7.14+ CK-Tile universal GEMM API in Inductor's CK-Tile GEMM templates by probing the installed headers ([#189646](https://github.com/pytorch/pytorch/pull/189646))
- Add memory-timeline fusion guards, `torch._inductor.config.fusion_memory_timeline_peak_memory_increase_gb` and `fusion_memory_timeline_peak_memory_pct_threshold`, that reject fusions which increase the estimated peak memory beyond the given limit ([#190344](https://github.com/pytorch/pytorch/pull/190344))
- Enable nested (staged) reduction fusion by default through `torch._inductor.config.triton.nested_reduction` (set `TORCHINDUCTOR_NESTED_REDUCTION=0` to disable). This fuses block-quantization patterns such as RMSNorm followed by MXFP8/NVFP4 scale computation and packing into one kernel, now including interleaved packing epilogues, quantize tails that write into preallocated buffers, persistent and looped multi-kernel choices, and the AOTInductor C++ wrapper ([#190594](https://github.com/pytorch/pytorch/pull/190594), [#190595](https://github.com/pytorch/pytorch/pull/190595), [#191974](https://github.com/pytorch/pytorch/pull/191974), [#193598](https://github.com/pytorch/pytorch/pull/193598), [#196332](https://github.com/pytorch/pytorch/pull/196332), [#196333](https://github.com/pytorch/pytorch/pull/196333), [#196334](https://github.com/pytorch/pytorch/pull/196334))
- Extend NVGEMM epilogue fusion. Dense GEMM epilogues are now generated directly as CuTeDSL from Inductor's loop IR, with CUTLASS EVT as the fallback. Dense and block-scaled kernels share one reduction contract, grouped reduction epilogues support any associative reduction plus pointwise consumers, swapped-operand (`swap_ab`) configurations are supported, and validated reduction chains are kept together during scheduling ([#190820](https://github.com/pytorch/pytorch/pull/190820), [#190821](https://github.com/pytorch/pytorch/pull/190821), [#190822](https://github.com/pytorch/pytorch/pull/190822), [#191514](https://github.com/pytorch/pytorch/pull/191514), [#191515](https://github.com/pytorch/pytorch/pull/191515), [#192298](https://github.com/pytorch/pytorch/pull/192298), [#194792](https://github.com/pytorch/pytorch/pull/194792), [#194793](https://github.com/pytorch/pytorch/pull/194793), [#194873](https://github.com/pytorch/pytorch/pull/194873), [#195231](https://github.com/pytorch/pytorch/pull/195231), [#195538](https://github.com/pytorch/pytorch/pull/195538))
- Support Triton kernels that need global scratch memory (such as device-side TMA kernels) in the static Triton launcher, so they no longer require a compile-worker round trip on FX graph cache hits ([#191133](https://github.com/pytorch/pytorch/pull/191133))
- Copy CUDA Graph Trees managed inputs whose pointers keep changing into stable replay buffers instead of re-recording, controlled by `torch._inductor.config.triton.cudagraph_managed_input_rerecord_limit` and `cudagraph_managed_input_rerecord_action` ([#191369](https://github.com/pytorch/pytorch/pull/191369))
- Use schedule-first bounded-region search for combo-kernel memory gating, allowing independent nodes from different dependency layers to be combined ([#192622](https://github.com/pytorch/pytorch/pull/192622))
- Hold the GPU benchmark lock across all candidates of a runtime multi-kernel comparison so concurrent compile workers cannot interleave measurements ([#192876](https://github.com/pytorch/pytorch/pull/192876))
- Add an opt-in Triton `bmm` template for a batch-broadcast left operand (`[M, K] x [B, K, N]`), enabled with `torch._inductor.config.bmm_shared_a` or `TORCHINDUCTOR_BMM_SHARED_A_TEMPLATE_ENABLED=1` ([#193049](https://github.com/pytorch/pytorch/pull/193049))
- Extend host-side TMA descriptor support to the Blackwell persistent TMA GEMM template, resolve template descriptors and symbolic strides consistently, and make the static launcher tolerate Triton/CUDA version skew ([#193857](https://github.com/pytorch/pytorch/pull/193857), [#194126](https://github.com/pytorch/pytorch/pull/194126), [#196410](https://github.com/pytorch/pytorch/pull/196410), [#196998](https://github.com/pytorch/pytorch/pull/196998))
- Support `nvidia-cutlass-operators` 0.2.0 for NVGEMM, which renamed `common_efc` to `efc` ([#193940](https://github.com/pytorch/pytorch/pull/193940), [#196984](https://github.com/pytorch/pytorch/pull/196984))
- Honor `assume_32bit_indexing` when choosing the integer type of dynamic size arguments, instead of always widening them to `int64` ([#194127](https://github.com/pytorch/pytorch/pull/194127))
- Add NVIDIA B200 and GB300 to Inductor's device-specification table, recognize the device names reported by ROCm hosts (such as MI350X VF, MI300X HF, MI210, MI250X and Radeon Pro W7800), and make TFLOPS and DRAM-bandwidth estimates device-generic, so roofline-based heuristics such as `pad_mm` use datasheet values instead of fallback estimates ([#194297](https://github.com/pytorch/pytorch/pull/194297), [#196398](https://github.com/pytorch/pytorch/pull/196398), [#196506](https://github.com/pytorch/pytorch/pull/196506), [#196944](https://github.com/pytorch/pytorch/pull/196944), [#198220](https://github.com/pytorch/pytorch/pull/198220))
- Allow out-of-tree backend config values registered through `register_backend_for_device(device_custom_config=...)` to be passed as `"<device>.<key>"` in `torch.compile(options=...)`, AOTInductor and standalone compile ([#194998](https://github.com/pytorch/pytorch/pull/194998))
- Drop the forced-inlining `-amdgpu-early-inline-all`/`-amdgpu-function-calls` LLVM flags from Inductor's ROCm Composable Kernel compile commands, avoiding compile-time and memory blowups with newer ROCm compilers ([#195023](https://github.com/pytorch/pytorch/pull/195023))
- Normalize `torch.concatenate` like `torch.cat` in pre-grad passes so split/cat optimizations apply to it ([#195174](https://github.com/pytorch/pytorch/pull/195174))
- Name the offending operator and its schema in `Unsupported return type` errors for extern kernels ([#195868](https://github.com/pytorch/pytorch/pull/195868))
- Add `torch._inductor.config.triton.cudagraph_initial_mempool_allocation_gb` to reserve one large segment in the CUDA graph memory pool up front, reducing fragmentation ([#196378](https://github.com/pytorch/pytorch/pull/196378))
- Add `torch._inductor.config.autotune_cudagraph_benchmarking_iters` (`TORCHINDUCTOR_AUTOTUNE_CUDAGRAPH_BENCHMARKING_ITERS`) to amortize CUDA-graph autotune benchmarking over several captured calls, reducing noise for tiny kernels ([#196413](https://github.com/pytorch/pytorch/pull/196413))
- Add an opt-in `bmm_skip_dynamic_shape_dim_check` option to `post_grad_fusion_options["decompose_mm_pass"]` that decomposes CPU `bmm` with an unprovable batch dimension based on operand sizes ([#197016](https://github.com/pytorch/pytorch/pull/197016))
- Use recipe-aware layout constraints for `_scaled_mm_v2` in Inductor instead of requiring exact input strides ([#197029](https://github.com/pytorch/pytorch/pull/197029))
- Add `torch._inductor.config.triton.cudagraph_dynamic_shape_rerecord_limit` to stop recording new CUDA graphs after a given number of distinct dynamic shapes; further new shapes run eagerly ([#197433](https://github.com/pytorch/pytorch/pull/197433))
- Extend N-D reduction tiling from two to three reduction dimensions ([#197437](https://github.com/pytorch/pytorch/pull/197437))
- Add an `include_fallback` option to custom-op autotuning so the custom op itself can be excluded from the candidate choices ([#197446](https://github.com/pytorch/pytorch/pull/197446))
- Reuse the CUTLASS sm120 kernel generators on sm121 GPUs ([#197621](https://github.com/pytorch/pytorch/pull/197621))
- Log at debug level when a Triton config is retried without software pipelining after an out-of-resources launch failure ([#199416](https://github.com/pytorch/pytorch/pull/199416))
- Keep Triton FP fusion enabled for Inductor templates (unless `emulate_precision_casts` is on) to preserve numerics with Triton 3.9, which changes the default ([#199500](https://github.com/pytorch/pytorch/pull/199500))
- Warm up the async compile worker pool for every Triton-backed device, and skip it when the CUDA backend does not use Triton ([#199635](https://github.com/pytorch/pytorch/pull/199635))
- Add `torch._inductor.config.alignment_asserts_inputs` (`TORCHINDUCTOR_ALIGNMENT_ASSERTS_INPUTS=1`, off by default). Graph inputs that were compiled assuming they are aligned are then checked at runtime and raise an `AssertionError` when misaligned, instead of being silently cloned to realign them ([#196379](https://github.com/pytorch/pytorch/pull/196379))
### bug fixes
- Fix `float16` and `bfloat16` scalar arguments being passed with the wrong width to Triton kernels by the static launcher on CUDA, ROCm and XPU ([#184065](https://github.com/pytorch/pytorch/pull/184065))
- Fix C++ compile errors in CPU code generation for boolean vector mask casts, including vectorized boolean `ops.masked` bodies ([#184155](https://github.com/pytorch/pytorch/pull/184155), [#199560](https://github.com/pytorch/pytorch/pull/199560))
- Fix `torch.compile` inferring the wrong output channel count for mkldnn transposed-convolution pointwise fusions with regular (non-prepacked) weights ([#184950](https://github.com/pytorch/pytorch/pull/184950))
- Emit runtime asserts for backed `SymInt` input checks when `prefer_deferred_runtime_asserts_over_guards=True`; previously regular Inductor compilation silently dropped them ([#185588](https://github.com/pytorch/pytorch/pull/185588))
- Fix `cannot determine truth value of Relational` errors when sorting symbolic strides without an explicit `ShapeEnv` ([#185871](https://github.com/pytorch/pytorch/pull/185871))
- Fix version-counter errors in backward when a grad-requiring input mutated outside the compiled graph was saved for backward by the min-cut partitioner ([#185876](https://github.com/pytorch/pytorch/pull/185876))
- Fix `/usr/bin/ld: cannot find -lcuda` when building Inductor CUDA/CUTLASS kernels on systems that only provide `libcuda.so.1` ([#186538](https://github.com/pytorch/pytorch/pull/186538))
- Fix `TypeError: too many positional arguments` during autotuning when a cached `bmm` template kernel deduplicated aliased inputs (for example `einsum("...ab,...Ab->...aA", grad, grad)`) ([#188268](https://github.com/pytorch/pytorch/pull/188268))
- Raise the same `output_padding` and bias-shape errors as eager for transposed convolution on the meta device instead of silently returning a shape ([#188328](https://github.com/pytorch/pytorch/pull/188328))
- Fix silently incorrect results from the `mm_plus_mm` and `bmm`/`baddbmm` Triton templates on XPU by using ascending K loops ([#189516](https://github.com/pytorch/pytorch/pull/189516))
- Fix code generation for user-defined Triton kernels that pass non-builtin Python objects as `tl.constexpr` values ([#189692](https://github.com/pytorch/pytorch/pull/189692))
- Fix compilation failures when compile-time combo-kernel autotuning is used with Inductor deterministic mode ([#189724](https://github.com/pytorch/pytorch/pull/189724))
- Fix Inductor compilation, FlexAttention and ROCm CK failing with a mixed-API error after fp32 matmul precision was set through the per-backend `torch.backends.cuda.matmul.fp32_precision` API ([#189955](https://github.com/pytorch/pytorch/pull/189955), [#196860](https://github.com/pytorch/pytorch/pull/196860))
- Use Triton's own `fp32` signature for Python `float` literal arguments to user-defined Triton kernels instead of forcing `fp64` ([#190340](https://github.com/pytorch/pytorch/pull/190340))
- Fix `torch.compile` failing on `torch.nan_to_num` with complex inputs ([#190428](https://github.com/pytorch/pytorch/pull/190428))
- Partition extern and fallback kernels that read or produce tensors on more than one device out of CUDA graphs, fixing incorrect capture of cross-device custom ops and `index_put` with CPU indices ([#190555](https://github.com/pytorch/pytorch/pull/190555))
- Preserve the input dtype for integer `bmm`/`matmul` on CPU when Inductor decomposes it into multiply and sum, instead of returning `int64` ([#191324](https://github.com/pytorch/pytorch/pull/191324))
- Fix compiled `torch.special.log_ndtr` returning `0.0` instead of `-0.0` for large positive inputs ([#191339](https://github.com/pytorch/pytorch/pull/191339))
- Fix `RuntimeError: aten::scaled_dot_product_attention() Expected a value of type 'Optional[float]' for argument 'scale'` when attention is written with a 0-d tensor scale and matched by SDPA fusion ([#191496](https://github.com/pytorch/pytorch/pull/191496))
- Fix `torch.compile` silently returning wrong results when `resize_()` is called on a no-op view of a no-grad intermediate returned from a compiled graph ([#191844](https://github.com/pytorch/pytorch/pull/191844))
- Fix `requested allocation size (X) is different from the size of a previous allocation with the same alloc_id` errors for symmetric-memory communication buffers when the global `random` module was reseeded between compilations ([#192089](https://github.com/pytorch/pytorch/pull/192089))
- Fix silent out-of-bounds reads when a view with a non-zero storage offset is passed as a mutated argument to a user-defined Triton kernel ([#192227](https://github.com/pytorch/pytorch/pull/192227))
- Fix `CUDA driver error: misaligned address` in backward when a user input that is saved for backward but unused in forward is misaligned on a later call ([#192263](https://github.com/pytorch/pytorch/pull/192263))
- Fix unbounded recursion (stack overflow) when overlap scheduling handles collective waits ([#192268](https://github.com/pytorch/pytorch/pull/192268))
- Honor `max_autotune_gemm_search_space="EXHAUSTIVE"` in `tuned_mm`, which previously dropped the regular mm template whenever decompose-K applied ([#192285](https://github.com/pytorch/pytorch/pull/192285))
- Fail the compile instead of hanging forever when a compile-worker result callback dies or a result cannot be serialized ([#192301](https://github.com/pytorch/pytorch/pull/192301))
- Fix silent data corruption when a non-contiguous reshape view was created over a buffer whose layout was not yet frozen ([#192575](https://github.com/pytorch/pytorch/pull/192575))
- Fix `AttributeError: 'NoneType' object has no attribute 'schedule_node'` in overlap scheduling when both `max_memory_increase_gb` and `max_memory_increase_ratio` are `None` ([#192628](https://github.com/pytorch/pytorch/pull/192628))
- Fix crashes and wrong output from the Triton `grouped_mm` template on very large inputs caused by 32-bit index overflow ([#192649](https://github.com/pytorch/pytorch/pull/192649))
- Fix `IndexError: list index out of range` when lowering a `control_deps` subgraph whose placeholders are not contiguous in node order ([#192903](https://github.com/pytorch/pytorch/pull/192903))
- Fix a data-dependent guard error (`GuardOnDataDependentSymNode`) in the joint-graph no-op removal pass when shapes contain different unbacked symbols ([#193052](https://github.com/pytorch/pytorch/pull/193052))
- Fix `KeyError` during pipelined autotuning when a choice was rejected during precompilation ([#193094](https://github.com/pytorch/pytorch/pull/193094))
- Fix silently wrong gradients from mix-order reductions whose outputs are views into a shared buffer (for example chained AdaLN/modulated LayerNorms whose scale and shift are `chunk()`-ed from one parameter), a regression since 2.10 ([#193103](https://github.com/pytorch/pytorch/pull/193103))
- Fix compile failures in the constant `cumsum` pattern for scalar (0-d) inputs and for symbolic or unbacked fill values ([#193422](https://github.com/pytorch/pytorch/pull/193422), [#193959](https://github.com/pytorch/pytorch/pull/193959))
- Fix boolean `index_put(..., accumulate=True)` on GPU by using an atomic OR instead of an atomic add ([#193584](https://github.com/pytorch/pytorch/pull/193584))
- Fix argument-count mismatch crashes when joint-graph view cleanup erased an unused graph input placeholder ([#193708](https://github.com/pytorch/pytorch/pull/193708))
- Fix CK-Tile GEMM autotuning on ROCm silently dropping every `float16` kernel ([#193902](https://github.com/pytorch/pytorch/pull/193902))
- Fix corrupted gradients from a reused `nested_compile_region` whose subgraph inputs inherited the outer graph's donated-buffer indices ([#193960](https://github.com/pytorch/pytorch/pull/193960))
- Fix compiled `torch.randn` and `torch.randn_like` on CUDA returning uniform `[0, 1)` values when `torch._inductor.config.align_random_eager=True` ([#194118](https://github.com/pytorch/pytorch/pull/194118))
- Fix `Detected N tensor(s) in the cudagraph pool not tracked as outputs` errors and silent gradient corruption in CUDA Graph Trees when a forward's backward is still pending ([#194124](https://github.com/pytorch/pytorch/pull/194124))
- Honor `TORCHINDUCTOR_EMIT_POINTER_RANGE_32=0` and the atomics exclusion for `tt.pointer_range` annotations in template kernels such as FlexAttention ([#194136](https://github.com/pytorch/pytorch/pull/194136))
- Fix `RuntimeError: Argument X of Node X was used before it has been defined!` and broadcast handling in the partitioned scatter pass ([#194366](https://github.com/pytorch/pytorch/pull/194366))
- Fix `CppCompileError` for Inductor C++ compilation with ROCm on Windows by using the ROCm SDK's `clang-cl` instead of MSVC ([#194471](https://github.com/pytorch/pytorch/pull/194471))
- Fix FlexAttention max-autotune failures when captured score/mask buffers are produced by ops inlined into the Triton template ([#194555](https://github.com/pytorch/pytorch/pull/194555))
- Measure every autotuning candidate under the same CUDA graph launch policy across in-process, subprocess, extern, Triton and CUTLASS benchmarking ([#194649](https://github.com/pytorch/pytorch/pull/194649))
- Fix NVGEMM failing with `AttributeError: 'CUstream' object has no attribute 'device'` in block-scaled GEMMs, and with an `ImportError` while lowering ordinary matmuls when a broken optional `cutlass.operators` install is present (NVGEMM is now disabled instead) ([#194727](https://github.com/pytorch/pytorch/pull/194727), [#198292](https://github.com/pytorch/pytorch/pull/198292))
- Fix compiled `torch.frexp` returning a zero mantissa and wrong exponent for `float32` subnormal inputs on CUDA, and preserve the sign of `-0.0` ([#195041](https://github.com/pytorch/pytorch/pull/195041))
- Fix incorrect `argmax`/`argmin` indices when the contiguous-index shortcut conflicted with later layout changes or loop reordering ([#195178](https://github.com/pytorch/pytorch/pull/195178))
- Fix `torch.while_loop` silently producing wrong results when `cond_fn` mutates a captured tensor that was mutated before the loop ([#195393](https://github.com/pytorch/pytorch/pull/195393))
- Fix batched post-grad fusion of `aten.sub` silently dropping a non-default `alpha` argument ([#195463](https://github.com/pytorch/pytorch/pull/195463))
- Fix `ValueRangeError: Invalid ranges` when compiling `constant_pad_nd` with negative padding feeding a matmul ([#195465](https://github.com/pytorch/pytorch/pull/195465))
- Fix lowering failures when an operator that falls back to eager is wrapped in `control_deps` (for example by overlap scheduling) ([#195517](https://github.com/pytorch/pytorch/pull/195517))
- Make the `addmm`, `addmv` and `_addmm_activation` decompositions (used by meta, FakeTensor and Inductor) reject an `input` that would broadcast wider than the matmul result, matching eager instead of silently returning a differently shaped output ([#195594](https://github.com/pytorch/pytorch/pull/195594))
- Fix wrong results from the Triton FP8 blockwise `scaled_mm` template caused by incorrect scale layouts, indexing and dot precision ([#195751](https://github.com/pytorch/pytorch/pull/195751))
- Fix the bias device check that gates CPU weight packing for `addmm` under freezing, which checked the weight instead of the bias ([#195833](https://github.com/pytorch/pytorch/pull/195833))
- Fix compile failures for nested grouped-reduction epilogues (`R0_BLOCK != nested_R0_REDUCED_BLOCK`) and a SymPy assertion in `solve_for_zero` ([#195874](https://github.com/pytorch/pytorch/pull/195874))
- Fix `GuardOnDataDependentSymNode` aborting compilation when a tiling leftover extent is an unbacked symbol; the incompatible fusion is now skipped ([#196081](https://github.com/pytorch/pytorch/pull/196081))
- Fix `FileNotFoundError` from autotuning when a later compilation in the same process reused stale benchmark futures from an earlier one ([#196148](https://github.com/pytorch/pytorch/pull/196148))
- Treat a concurrently cleared local AOTAutograd/Inductor cache as a cache miss instead of raising `FileNotFoundError` ([#196189](https://github.com/pytorch/pytorch/pull/196189))
- Fix user-defined Triton kernels that reference aliased `triton`/`triton.language` module imports (for example `import triton.language as source_tl`) being reconstructed without those imports ([#196237](https://github.com/pytorch/pytorch/pull/196237))
- Fix Triton-based TFLOPS estimates being off by 1000x because the GPU clock rate was passed in MHz instead of kHz ([#196372](https://github.com/pytorch/pytorch/pull/196372))
- Fix `NoValidChoicesError` when decompose-K is selected for a shape that has no valid K split, by keeping the regular Triton mm template as a fallback ([#196453](https://github.com/pytorch/pytorch/pull/196453))
- Fix `NoValidChoicesError` for every Triton GEMM template on ROCm when `multi_kernel_hints` is set ([#196510](https://github.com/pytorch/pytorch/pull/196510))
- Fix silently wrong results from mix-order split column reductions when the row count is not a multiple of `XBLOCK` ([#196565](https://github.com/pytorch/pytorch/pull/196565))
- Fix compiled `torch.nextafter` being a no-op for `float16`/`bfloat16` and flushing `float32` subnormal steps on CUDA ([#196578](https://github.com/pytorch/pytorch/pull/196578))
- Fix `AttributeError: module 'torch._inductor.fx_passes' has no attribute 'reinplace'` when `FakeTensorUpdater` runs before the post-grad passes are imported ([#196946](https://github.com/pytorch/pytorch/pull/196946))
- Fix wrong results and validation for DeepSeek-style blockwise `scaled_mm` in Inductor's Triton template, which assumed row-major scales and mis-advanced scale indices ([#197028](https://github.com/pytorch/pytorch/pull/197028))
- Fix batched linear post-grad fusion combining `mm`/`addmm` calls with different dtypes into one `bmm` ([#197069](https://github.com/pytorch/pytorch/pull/197069))
- Fix compile crashes for floor division of `float16`/`bfloat16` values derived from `arange` ([#197132](https://github.com/pytorch/pytorch/pull/197132))
- Fix static pointwise kernels being partitioned out of CUDA graphs as "dynamic shape ops" when `cudagraph_skip_dynamic_graphs` is enabled ([#197139](https://github.com/pytorch/pytorch/pull/197139))
- Fix `IndexError` in `tuned_addmm` when the bias is a 0-d scalar tensor ([#197214](https://github.com/pytorch/pytorch/pull/197214))
- Remove duplicate waits on the same collective, which parametrizations such as SimpleFSDP could produce ([#197323](https://github.com/pytorch/pytorch/pull/197323))
- Fix CUDA Graph backward graphs treating activations produced by an uncaptured forward graph partition as static inputs ([#197438](https://github.com/pytorch/pytorch/pull/197438))
- Fix compilation failures for DeepSeek-style blockwise `scaled_mm` at `K=128` caused by re-inferring the scaling recipe in the TMA heuristic ([#197458](https://github.com/pytorch/pytorch/pull/197458))
- Fix Triton template kernels being compiled twice, with two jobs racing on the same cache file, when the compile worker pool is warm ([#197471](https://github.com/pytorch/pytorch/pull/197471))
- Fix the `CUDA_HOME` fallback for locating `nvcc` when compiling Inductor CUDA kernels, which could never succeed ([#197573](https://github.com/pytorch/pytorch/pull/197573))
- Fix `Not sure where to find device info` assertions for fallback kernels with no tensor inputs or dict outputs; tensorless fallbacks now default to CPU ([#197584](https://github.com/pytorch/pytorch/pull/197584))
- Fix compiled `max_pool2d`/`max_pool3d` with indices, `adaptive_max_pool2d` and `fractional_max_pool` silently returning transposed indices for inputs with non-contiguous spatial dimensions ([#197596](https://github.com/pytorch/pytorch/pull/197596))
- Fix pattern-matcher replacements that return a one-element tuple, which failed to compile in post-grad passes and silently produced wrong results in pre-grad passes (for example a `scan` that only returns a carry) ([#197832](https://github.com/pytorch/pytorch/pull/197832))
- Fix Triton `CompilationError` when compiling integer or bool to `float8_e4m3fnuz`/`float8_e5m2fnuz` casts on ROCm ([#197905](https://github.com/pytorch/pytorch/pull/197905))
- Fix races and wrong results when the reinplace pass turned a scatter into an in-place copy whose source is a view of the mutated storage (for example `x[1:] = x[:-1].clone()`) ([#198010](https://github.com/pytorch/pytorch/pull/198010))
- Fix `remove_noop_ops` replacing a copy of a graph input with the input itself when the input is mutated before the copy's user runs, which returned the mutated value ([#198132](https://github.com/pytorch/pytorch/pull/198132))
- Fix silently wrong results when a reader of a buffer was fused with a later in-place mutation after an earlier mutation of the same buffer (for example `x.index_put_(...); x.add_(x.flip(0))`) ([#198325](https://github.com/pytorch/pytorch/pull/198325))
- Fix FlexAttention decoding (query length < 128) silently reading the query at wrong offsets when the query is produced by a pointwise op such as `q * scale` ([#198543](https://github.com/pytorch/pytorch/pull/198543))
- Fix wrong values and scheduler `KeyError`s when an in-place mutation such as `index_put_` targets a buffer that was already referenced by views or extern kernels ([#198549](https://github.com/pytorch/pytorch/pull/198549))
- Fix wrong results (CPU) or overlap errors (CUDA) when the reinplace pass turned `index_put` into `index_put_` while its indices or values shared storage with the input, as in `torch.put(r, r, r, accumulate=True)` ([#198637](https://github.com/pytorch/pytorch/pull/198637))
- Fix crashes, wrong results and unintended aliasing from `merge_select_cat_aten` (with `select_cat_aten_pass` enabled) when `cat` inputs are not selects of one tensor in order ([#198638](https://github.com/pytorch/pytorch/pull/198638))
- Disable the 4x-vectorized Triton random number path by default, which produced correlated, incorrect CUDA dropout masks since 2.13 (opt back in with `TORCHINDUCTOR_USE_RAND4X=1`) ([#198680](https://github.com/pytorch/pytorch/pull/198680))
- Fix wrong results under `dynamic=True` when a symbolic dimension that is guarded equal to 1 is broadcast by an unrealized pointwise input (for example `F.interpolate` followed by `F.pad`) ([#198774](https://github.com/pytorch/pytorch/pull/198774))
- Match eager gradients for compiled `adaptive_max_pool3d` on channels-last 3D inputs ([#199068](https://github.com/pytorch/pytorch/pull/199068))
- Accumulate Triton scans (such as `cumsum`) on `float16`/`bfloat16` in `float32`, as reductions already do ([#199088](https://github.com/pytorch/pytorch/pull/199088))
- Fall back to flattened indexing instead of asserting when a reshape view involves unbacked symbols that cannot be grouped ([#199105](https://github.com/pytorch/pytorch/pull/199105))
- Count only successfully compiled choices toward `max_template_fusion_benchmarked_choices`, and skip instead of crashing on template-fusion choices that raise `CantSplit` (including under `multi_kernel_hints`) ([#199113](https://github.com/pytorch/pytorch/pull/199113))
- Fix FX graph cycles from manual collective bucketing when a dependency path leaves and re-enters a module scope ([#199227](https://github.com/pytorch/pytorch/pull/199227))
- Fix `graph.lint()` failures from the manual overlap scheduler moving collectives past a consumer that also takes an external input ([#199228](https://github.com/pytorch/pytorch/pull/199228))
- Fix a CPU buffer being passed to a CUDA kernel when a device copy of a view of a constant-only computation was incorrectly eliminated ([#199402](https://github.com/pytorch/pytorch/pull/199402))
- Fix `NameError: name 'buf1' is not defined` for complex indexed assignment under `mode="reduce-overhead"` with graph partitioning ([#199414](https://github.com/pytorch/pytorch/pull/199414))
- Fix silently incorrect results on MPS when two masked loads with the same mask were deduplicated into one by common-subexpression elimination ([#199673](https://github.com/pytorch/pytorch/pull/199673))
- Fix `torch.compile` crashing with `AttributeError: 'ExternKernelSchedulerNode' object has no attribute 'group'` on `torch._foreach_pow`/`torch._foreach_pow_` with integer tensors ([#198675](https://github.com/pytorch/pytorch/pull/198675))
- Fix `InductorError: KeyError: 'reinterpret_tensor(...)'` in the FX wrapper backend when a user-defined Triton kernel takes a view of another buffer, such as a slice of a matmul result ([#193820](https://github.com/pytorch/pytorch/pull/193820))
- Fix Inductor reordering consecutive ordered side-effectful ops (for example torchbind or effectful custom ops) when they lower to different kernel types, and stop the ordering edge from keeping the earlier op's output alive longer than needed ([#188301](https://github.com/pytorch/pytorch/pull/188301))
- Fix pre-grad batch math fusion failing with `TypeError: clamp() received an invalid combination of arguments` for `torch.clamp` with tensor bounds, and mutating a stacked copy instead of the original inputs for in-place dropout (`inplace=True`); equivalent positional and keyword calls are now grouped together ([#198285](https://github.com/pytorch/pytorch/pull/198285))
- Fix NVGEMM autotuning benchmarking on inputs whose storage aliasing, view offsets and alignment differ from the arguments the runtime kernel receives ([#199072](https://github.com/pytorch/pytorch/pull/199072))
- Fix a spurious `ZeroDivisionError` from integer `%` on the CPU backend when the inner size does not fill a whole vector (for example sizes 3, 5 or 7) ([#192025](https://github.com/pytorch/pytorch/pull/192025))
- Fix Inductor's SDPA pattern fusion silently producing wrong results, or crashing, for hand-written attention whose key reaches the score matmul through a permute other than `key.transpose(-2, -1)`. Pattern matches are now validated by re-tracing with the matched inputs ([#195383](https://github.com/pytorch/pytorch/pull/195383))
- Fix native DSL ops silently not registering when Triton is installed under another distribution name (for example `triton-rocm`), or when a stale distribution's metadata is left behind after switching Triton providers ([#195022](https://github.com/pytorch/pytorch/pull/195022))
### performance
- Add an opt-in pattern (`torch._inductor.config.var_std_reduction_dedup`) that shares the reduction when both `torch.var` and `torch.std` are computed on the same tensor ([#182945](https://github.com/pytorch/pytorch/pull/182945))
- Reduce compile time by caching `optimization_hint` results, dtype-propagation handler setup and formatted origin-node kernel comments, and by skipping full SymPy simplification in CPU vector index analysis ([#186319](https://github.com/pytorch/pytorch/pull/186319), [#192817](https://github.com/pytorch/pytorch/pull/192817), [#192820](https://github.com/pytorch/pytorch/pull/192820), [#194010](https://github.com/pytorch/pytorch/pull/194010))
- Allow mix-order reduction fusion for square shapes and remove the `nrow >= 2 * ncol` gate, speeding up kernels such as RMSNorm backward and paired row/column sums ([#186370](https://github.com/pytorch/pytorch/pull/186370), [#188660](https://github.com/pytorch/pytorch/pull/188660))
- Enable layout optimization for backward graphs that contain `convolution_backward` without a forward convolution ([#188236](https://github.com/pytorch/pytorch/pull/188236))
- Cache host-side TMA descriptors across launches in the static Triton launcher ([#188823](https://github.com/pytorch/pytorch/pull/188823))
- Keep large attention masks consumed by masked SDPA out of horizontal combo kernels, preserving producer-consumer locality and reducing peak memory ([#189002](https://github.com/pytorch/pytorch/pull/189002))
- Use per-row scalar accumulators in large non-persistent CUDA reduction loops that contain an online softmax, including the other reductions in those kernels (`torch._inductor.config.triton.scalar_accumulators`, on by default) ([#190692](https://github.com/pytorch/pytorch/pull/190692), [#196371](https://github.com/pytorch/pytorch/pull/196371))
- Fix the CPU loop-parallelization heuristic moving OpenMP parallelism onto an inner reduction loop when an outer vectorized loop is smaller than the vector width, which caused heavy fork overhead with freezing ([#190928](https://github.com/pytorch/pytorch/pull/190928))
- Add a `num_warps=16` candidate for inner reductions on XPU, recovering a performance regression from the reduction-hint change in 2.11 ([#190986](https://github.com/pytorch/pytorch/pull/190986))
- Overlap AMX matmul and AVX softmax in the CPU FlexAttention template, improving BF16 performance by 6-29% on some shapes ([#191780](https://github.com/pytorch/pytorch/pull/191780))
- Fix a performance regression where `select_scatter` recomputed an expensive `src` once per element of the scattered dimension ([#192136](https://github.com/pytorch/pytorch/pull/192136))
- Reduce the Python call overhead of C++-wrapper (`cpp_wrapper`) kernel bindings by 40-50% by using `METH_FASTCALL` ([#192287](https://github.com/pytorch/pytorch/pull/192287))
- Avoid redundant full-tile loads in masked reductions when the loaded value only depends on the output row ([#192410](https://github.com/pytorch/pytorch/pull/192410))
- Use larger reduction tiles on GB300 (sm_103) GPUs, which need more memory-level parallelism, roughly doubling HBM bandwidth utilization for memory-bound reduction kernels ([#193774](https://github.com/pytorch/pytorch/pull/193774))
- Reduce fusion-search compile time by caching per-node and per-buffer quantities instead of recomputing them for every candidate pair ([#194011](https://github.com/pytorch/pytorch/pull/194011))
- Add gfx950-specific FlexAttention backward default configs on ROCm (1.8-2.3x faster on measured shapes) ([#194151](https://github.com/pytorch/pytorch/pull/194151))
- Lower eligible large BF16 `X @ X.T` and batched `bmm(X, X.mT)` on SM100 GPUs to a symmetric CuTeDSL kernel that computes only one triangle ([#194177](https://github.com/pytorch/pytorch/pull/194177), [#194178](https://github.com/pytorch/pytorch/pull/194178))
- Improve NVGEMM NVFP4 decode performance on Blackwell with a bounded, shape-aware candidate set, fused output scaling for `_scaled_mm` linears that multiply by a dequantization scalar, and programmatic dependent launch into downstream Triton kernels, now on by default for measured shapes (`TORCHINDUCTOR_NVGEMM_PDL=auto`; set `0` to disable) ([#194651](https://github.com/pytorch/pytorch/pull/194651), [#194652](https://github.com/pytorch/pytorch/pull/194652), [#197485](https://github.com/pytorch/pytorch/pull/197485))
- Lower `index_add` with `bfloat16` through the Triton decomposition on SM90+ and ROCm so it can fuse instead of falling back to ATen ([#195192](https://github.com/pytorch/pytorch/pull/195192))
- Let recommended 2-CTA kernels and wider SM100 dense N tiles (160 to 256) enter NVGEMM autotuning when nvMatmulHeuristics selects them ([#195539](https://github.com/pytorch/pytorch/pull/195539), [#198293](https://github.com/pytorch/pytorch/pull/198293))
- Eliminate no-op `slice_scatter` chains that write an unchanged `split` view back to its source ([#195608](https://github.com/pytorch/pytorch/pull/195608))
- Make manual collective bucketing's wait-user repair linear, fixing apparent hangs on large sharded graphs ([#195616](https://github.com/pytorch/pytorch/pull/195616))
- Rewrite `slice_scatter` chains that fill an entire tensor (as produced by functionalized chunking) into `cat` or `copy_`, reducing peak memory ([#195631](https://github.com/pytorch/pytorch/pull/195631))
- Drop a compiler-proven all-zero attention bias from `aten._scaled_dot_product_efficient_attention` forward and backward calls ([#196068](https://github.com/pytorch/pytorch/pull/196068), [#196079](https://github.com/pytorch/pytorch/pull/196079))
- Reduce all-gather bucketing kernel launches by copying differently shaped inputs with one `foreach_copy` ([#196621](https://github.com/pytorch/pytorch/pull/196621))
- Apply the `index_add` unique-index rewrite when the index is a full `torch.randperm`, not only a sliced one ([#196873](https://github.com/pytorch/pytorch/pull/196873))
- Fix a compile-time and performance regression for BERT-family models under dynamic shapes with CUDA graphs caused by pattern-matcher re-validation of symbolic size lists ([#198320](https://github.com/pytorch/pytorch/pull/198320))
- Reuse base storage for views when generating example inputs for compile-time autotuning instead of re-allocating it ([#198660](https://github.com/pytorch/pytorch/pull/198660))
- Start hashing the torch and Triton sources for FX graph cache keys in the background when `torch.compile` is called, removing about 140 ms from the first compilation ([#198747](https://github.com/pytorch/pytorch/pull/198747))
- Compile combo-kernel benchmark candidates in the async-compile process pool instead of serially on the scheduler thread, reducing compile time ([#198881](https://github.com/pytorch/pytorch/pull/198881))
- Pad uneven reduce-scatter inputs (as with unevenly sharded FSDP) with a single `chunk_cat` when bucketing, instead of one padding copy per input, about 9x faster in eager and 3.4x faster with CUDA graphs on a 32-input benchmark ([#196647](https://github.com/pytorch/pytorch/pull/196647))
- Fuse the per-input copies of `torch.cat`/`torch.stack` into foreach kernels when the inputs have dynamic shapes, as was already done for static shapes ([#198294](https://github.com/pytorch/pytorch/pull/198294))
### docs
- Document the actual requirement of the FlexAttention `ROWS_GUARANTEED_SAFE` kernel option: each row needs an unmasked key in the first block scheduled for it ([#194154](https://github.com/pytorch/pytorch/pull/194154))
### devs
- Add extension points for out-of-tree accelerator backends: `DeviceInterface.is_gpu()` to be treated as a GPU without patching Inductor's device list, `DeviceInterface.get_cpp_device_options()` for C++ compile options, `DeviceInterface.get_cache_system_info()` to contribute to the code-cache key, `DeviceInterface.get_multi_processor_count()` to report the compute-unit count, `DeviceOpOverrides.uses_gpu_cpp_wrapper()` to opt into the GPU-style C++ wrapper path, and an optional lazy `_inductor_backend_init` hook on the registered PrivateUse1 device module ([#190326](https://github.com/pytorch/pytorch/pull/190326), [#190614](https://github.com/pytorch/pytorch/pull/190614), [#192896](https://github.com/pytorch/pytorch/pull/192896), [#193908](https://github.com/pytorch/pytorch/pull/193908), [#190615](https://github.com/pytorch/pytorch/pull/190615))
- Add a keyed registry so multiple integrations can each contribute `InductorChoices` overrides without replacing one another ([#194097](https://github.com/pytorch/pytorch/pull/194097))
- Allow out-of-tree Inductor backends to register FlexAttention backward template candidates ([#195786](https://github.com/pytorch/pytorch/pull/195786))
- Let out-of-tree backends that subclass `MetalKernel` override the launch device through a class attribute ([#195809](https://github.com/pytorch/pytorch/pull/195809))
- Add declarative `implies` support to `Config` in Inductor/Dynamo config modules so one config value can force other settings ([#196663](https://github.com/pytorch/pytorch/pull/196663))
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
### security
