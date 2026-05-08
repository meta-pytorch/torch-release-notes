
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
- The `max_autotune` layout-constraint deferral introduced in 2.11 is now opt-in ([#175330](https://github.com/pytorch/pytorch/pull/175330))

  In 2.11, Inductor deferred layout freezing for `max_autotune` templates to expose more fusion opportunities. This caused a regional-inductor failure mode, so the default in 2.12 reverts to immediate layout freezing. Users who relied on the deferred behavior for fusion opportunities should opt in explicitly via `torch._inductor.config.max_autotune_defer_layout_freezing` or `TORCHINDUCTOR_MAX_AUTOTUNE_DEFER_LAYOUT_FREEZING=1`.

  Version 2.11:
  ```python
  # Deferred layout freezing was the default
  torch.compile(model, mode="max-autotune")
  ```

  Version 2.12:
  ```python
  import torch._inductor.config as cfg
  cfg.max_autotune_defer_layout_freezing = True
  # or set TORCHINDUCTOR_MAX_AUTOTUNE_DEFER_LAYOUT_FREEZING=1
  torch.compile(model, mode="max-autotune")
  ```

### deprecation
### new features
- Added user-defined stream support to `torch.compile`. Inductor now codegens stream context managers (enter/exit) and `record_stream` calls in the wrapper, enabling user streams to flow through compiled regions with proper synchronization, scheduler integration, and cross-stream dependency tracking ([#165390](https://github.com/pytorch/pytorch/pull/165390), [#165391](https://github.com/pytorch/pytorch/pull/165391), [#165504](https://github.com/pytorch/pytorch/pull/165504), [#165505](https://github.com/pytorch/pytorch/pull/165505), [#174223](https://github.com/pytorch/pytorch/pull/174223), [#176700](https://github.com/pytorch/pytorch/pull/176700), [#177694](https://github.com/pytorch/pytorch/pull/177694))
- Added `ao::offload`, `ao::reload`, and `ao::wait` ops for asynchronous activation offloading. These ops encapsulate async CPU offloading stream management following the same async 2-op pattern as c10d functional collectives, reducing IR size from 7 nodes (offload) and 5 nodes (reload) down to 2 nodes each ([#177621](https://github.com/pytorch/pytorch/pull/177621))
- Added user-defined Triton kernel unary epilogue fusion. Inductor can now fuse user Triton kernels with downstream pointwise epilogues (e.g. `relu()`), parsing the user kernel source via AST and inlining the epilogue into the `tl.store` expression ([#173662](https://github.com/pytorch/pytorch/pull/173662))
- Added out-variant discovery and lowering for custom ops. When a custom op registers both functional and `.out` overloads, Inductor automatically lowers single-output and multi-output functional ops to their `.out` variants as `ExternKernelOut`, enabling memory planner buffer reuse ([#175116](https://github.com/pytorch/pytorch/pull/175116), [#176117](https://github.com/pytorch/pytorch/pull/176117))
- `max_autotune` now extends to combo kernels. The autotuning pipeline generates and benchmarks per-sub-kernel block-size phase configs, with chained sequential autotuning and per-sub-kernel reduction hints ([#177715](https://github.com/pytorch/pytorch/pull/177715), [#178936](https://github.com/pytorch/pytorch/pull/178936), [#179317](https://github.com/pytorch/pytorch/pull/179317))
- Added non-TMA persistent Triton templates for `mm` and `addmm` for max-autotune, enabling persistent kernels on hardware without TMA ([#177781](https://github.com/pytorch/pytorch/pull/177781), [#179095](https://github.com/pytorch/pytorch/pull/179095))
- Added CUTLASS backend support for `torch.float8_e5m2` dtype, including registration for FP8 GEMM autotuning ([#171176](https://github.com/pytorch/pytorch/pull/171176))
- Added XPU CUTLASS GEMM kernel codegen and codecache to `max-autotune-gemm`, allowing CUTLASS-style GEMM templates to target Intel GPUs ([#161938](https://github.com/pytorch/pytorch/pull/161938), [#161939](https://github.com/pytorch/pytorch/pull/161939))
- Added MTIA Triton codegen for `sort`, `median`, and `mode` operations ([#178525](https://github.com/pytorch/pytorch/pull/178525))
- Added a Triton template for depthwise `conv1d` ([#175280](https://github.com/pytorch/pytorch/pull/175280))
- Added AVX10.2 fp32↔fp8 intrinsics in `at::vec::convert` for the Inductor C++ x86 backend ([#172309](https://github.com/pytorch/pytorch/pull/172309))
- Pallas backend: added scalar prefetch and indirect access support ([#177212](https://github.com/pytorch/pytorch/pull/177212))
- Added a `disable_welford_reduction` config flag to opt out of Welford reduction in codegen ([#175778](https://github.com/pytorch/pytorch/pull/175778))

### improvements
- Unified `OUT_DTYPE`, `ACC_TYPE`, and `INDEX_DTYPE` codegen flow in Triton templates ([#179453](https://github.com/pytorch/pytorch/pull/179453))
- Enabled cudagraph w/o partition for cpp-wrapper ([#179249](https://github.com/pytorch/pytorch/pull/179249))
- Added FMA-based `addcdiv` lowering for CUDA parity with eager and matching `_foreach_addcdiv` to `_foreach_addcmul` ([#174912](https://github.com/pytorch/pytorch/pull/174912), [#175309](https://github.com/pytorch/pytorch/pull/175309), [#175310](https://github.com/pytorch/pytorch/pull/175310), [#175839](https://github.com/pytorch/pytorch/pull/175839), [#176237](https://github.com/pytorch/pytorch/pull/176237))
- Added `lerp` decompositions for bitwise parity with eager ([#176804](https://github.com/pytorch/pytorch/pull/176804))
- Added outer-product decomposition ([#176552](https://github.com/pytorch/pytorch/pull/176552))
- Enabled padding fusion with `torch.cat` and avoided duplicate computation in `cat`/`pad` when inputs have multiple consumers ([#175729](https://github.com/pytorch/pytorch/pull/175729))
- Lowered functional symmetric memory ops to `ExternKernelOut` for output buffer reuse, and added `symm_mem` planning for graph inputs and fallback regions ([#174856](https://github.com/pytorch/pytorch/pull/174856), [#175449](https://github.com/pytorch/pytorch/pull/175449))
- Modified addmm template call to support hipblaslt bias-fused kernels on ROCm ([#177130](https://github.com/pytorch/pytorch/pull/177130))
- Newly trained PadMM AutoHeuristics for A100 and H200, plus support for `pad_mm` AutoHeuristics in deterministic mode ([#176186](https://github.com/pytorch/pytorch/pull/176186), [#179826](https://github.com/pytorch/pytorch/pull/179826))
- Propagate metadata in pattern matcher and add validation ([#179113](https://github.com/pytorch/pytorch/pull/179113))
- FlexAttention: raise a clear `NotImplementedError` when `return_aux=AuxRequest(max_scores=True)` is requested with `BACKEND='FLASH'` instead of failing later with an opaque error ([#177434](https://github.com/pytorch/pytorch/pull/177434))
- Migrated Inductor internals from legacy `allow_tf32` to `fp32_precision` to avoid divergence with the new TF32 API ([#176098](https://github.com/pytorch/pytorch/pull/176098))
- Pallas backend: enabled element-wise ops, native TPU OOB DMA masking via aligned block specs, and generalized N-D transpose permutation detection ([#174743](https://github.com/pytorch/pytorch/pull/174743), [#175458](https://github.com/pytorch/pytorch/pull/175458), [#176952](https://github.com/pytorch/pytorch/pull/176952))
- Registered lowerings for `prims.scalar_tensor` and `aten.arange.start_step` ([#179017](https://github.com/pytorch/pytorch/pull/179017), [#179028](https://github.com/pytorch/pytorch/pull/179028))
- Added SDPA pattern matching support for visformer ([#177826](https://github.com/pytorch/pytorch/pull/177826))
- Relaxed concat-linear fusion to support GQA QKV ([#178523](https://github.com/pytorch/pytorch/pull/178523))
- Allowed subgraphs to be benchmarked with async pipelined autotuning ([#175455](https://github.com/pytorch/pytorch/pull/175455))
- Added `convert_element_type` lowering to emulate PyTorch eager numerics ([#176781](https://github.com/pytorch/pytorch/pull/176781))
- Added GEMM configs to XPU autotuning heuristic ([#177647](https://github.com/pytorch/pytorch/pull/177647))
- Added `kpack` Triton compile options on ROCm ([#173179](https://github.com/pytorch/pytorch/pull/173179))
- ROCm: enabled exhaustive autotuning for FP8 ([#177797](https://github.com/pytorch/pytorch/pull/177797))
- Override decomposition for `aten.index_add` ([#179486](https://github.com/pytorch/pytorch/pull/179486))
- Drop `tile_k` from nvMatmulHeuristics matching ([#176845](https://github.com/pytorch/pytorch/pull/176845))

### bug fixes
- Fix horizontal fusion bug and add partition tests for regional inductor ([#178421](https://github.com/pytorch/pytorch/pull/178421))
- Fix `floordiv` Inductor lowering for mixed signedness (Triton workaround) ([#175168](https://github.com/pytorch/pytorch/pull/175168))
- Use `Sm100CollectiveEpilogue` on SM100 ([#175305](https://github.com/pytorch/pytorch/pull/175305))
- Fix `aten.resize` on overlapping-stride views ([#176651](https://github.com/pytorch/pytorch/pull/176651))
- Fix `ConstructorMoverPass` replacing CPU placeholder in graph output and creating mixed-device pointwise ops ([#176164](https://github.com/pytorch/pytorch/pull/176164), [#177646](https://github.com/pytorch/pytorch/pull/177646))
- Use `VecMask::from` for scalar masks in CPU codegen ([#178148](https://github.com/pytorch/pytorch/pull/178148))
- Fix `triton_main_loop_scaled_mm` template to use correct scale recipe ([#178005](https://github.com/pytorch/pytorch/pull/178005))
- Fix `cpp_wrapper` lazy compile stale state across `fresh_cache` resets ([#178162](https://github.com/pytorch/pytorch/pull/178162))
- Fix int64 indexing with >65k M/N size ([#172925](https://github.com/pytorch/pytorch/pull/172925))
- Fix BMM Triton template `grid_y` overflow for large batch dims and i32 overflow in template kernel signature for large storage offsets ([#178617](https://github.com/pytorch/pytorch/pull/178617), [#179333](https://github.com/pytorch/pytorch/pull/179333))
- Fix `remove_no_ops` incorrectly eliminating ops on mutated values ([#174938](https://github.com/pytorch/pytorch/pull/174938))
- Fix negative-zero constant codegen for the Triton backend ([#176035](https://github.com/pytorch/pytorch/pull/176035))
- Fix coordinate descent tuner incorrectly re-running on warm cache ([#173391](https://github.com/pytorch/pytorch/pull/173391))
- Fix BF16/FP16 scalar comparison to match eager ([#175807](https://github.com/pytorch/pytorch/pull/175807))
- Defensively check `name` is in `buffer_read_counts` before access ([#171245](https://github.com/pytorch/pytorch/pull/171245))
- Fix cpp-wrapper `SyntaxError` when Triton kernel has docstrings ([#176796](https://github.com/pytorch/pytorch/pull/176796))
- Fix `fallback_random` dropout stride mismatch ([#177077](https://github.com/pytorch/pytorch/pull/177077))
- Fix `AssertionError` in `ForeachKernelSchedulerNode` loop reordering after fusion ([#176849](https://github.com/pytorch/pytorch/pull/176849))
- Fix incorrect rounding of `floordiv` ([#177926](https://github.com/pytorch/pytorch/pull/177926))
- Fix issue in AMD `persistent_mm_template` selection ([#178178](https://github.com/pytorch/pytorch/pull/178178))
- Pointwise configs with `max_autotune` must include pointwise configs with `max_autotune_pointwise` ([#177995](https://github.com/pytorch/pytorch/pull/177995))
- Fix `num_warps` when max_autotune is enabled on HIP ([#178023](https://github.com/pytorch/pytorch/pull/178023))
- Fix `nn.Dropout` accuracy discrepancies between Triton and torch implementations ([#178843](https://github.com/pytorch/pytorch/pull/178843))
- Fix eager/compiled mismatch for integer `floor_divide` with zero divisor ([#178016](https://github.com/pytorch/pytorch/pull/178016))
- Accept 1D bias in addmm ATen heuristic on ROCm ([#179087](https://github.com/pytorch/pytorch/pull/179087))
- Fix `randn_like` inconsistency between eager and compile with `fallback_random=True` ([#177994](https://github.com/pytorch/pytorch/pull/177994))
- Fix `MetalScheduling` constructor in MPSInductor ([#179646](https://github.com/pytorch/pytorch/pull/179646))
- Prevent cross-stream inplace and memory-planning buffer reuse for user-streams ([#178548](https://github.com/pytorch/pytorch/pull/178548), [#178549](https://github.com/pytorch/pytorch/pull/178549))
- Fix `argmax`/`argmin` returning incorrect indices for boolean tensors on CUDA ([#174076](https://github.com/pytorch/pytorch/pull/174076))
- Fix block-pointer advancement for broadcasted tensors ([#175008](https://github.com/pytorch/pytorch/pull/175008))
- Fix masked vectorization for the Inductor C++ backend ([#174648](https://github.com/pytorch/pytorch/pull/174648))
- Fix bucketize NaN handling in Triton codegen and Pallas `sign` to match PyTorch NaN semantics ([#176579](https://github.com/pytorch/pytorch/pull/176579), [#176814](https://github.com/pytorch/pytorch/pull/176814))
- Fix `UnicodeDecodeError` in Triton depthwise conv template ([#176484](https://github.com/pytorch/pytorch/pull/176484))
- Handle 0-sized dimensions in Pallas codegen ([#176813](https://github.com/pytorch/pytorch/pull/176813))
- Fix `torch._check` divisibility propagation to Triton `tt.divisibility` ([#175755](https://github.com/pytorch/pytorch/pull/175755))
- Fix SIGSEGV on AMD RDNA (Wave32) from removed reduction masks in persistent kernels ([#176269](https://github.com/pytorch/pytorch/pull/176269))
- Pallas: fix non-stride-1 reductions and prevent incompatible reduction fusion ([#176489](https://github.com/pytorch/pytorch/pull/176489))
- Fix `block_ptr` store dtype for inplace-mutated buffers ([#177860](https://github.com/pytorch/pytorch/pull/177860))
- Fix constants handling for Triton `constexpr` ([#172354](https://github.com/pytorch/pytorch/pull/172354))
- Fix Inductor reinplace bool shadowing (`'bool' object not callable`) ([#176090](https://github.com/pytorch/pytorch/pull/176090))
- Fix Inductor `_split_iteration_ranges` silently dropping dimensions ([#177673](https://github.com/pytorch/pytorch/pull/177673))
- Fix `sym_sum` lowering to accept varargs ([#178661](https://github.com/pytorch/pytorch/pull/178661))
- Fix `bias_addmm` for AMD ([#178929](https://github.com/pytorch/pytorch/pull/178929))
- Define unbacked slice size symbol when bounds become provable after tracing ([#178897](https://github.com/pytorch/pytorch/pull/178897))
- Add `isinf()` to `Float8_e4m3fn` to fix `nan_asserts` crash with fp8 inputs ([#160641](https://github.com/pytorch/pytorch/pull/160641))
- Fix division by zero in the Triton kernel launcher when `Grid2DWithYZOverflow` ([#178878](https://github.com/pytorch/pytorch/pull/178878))
- Prevent user-kernel fusion with non-unary epilogues ([#179735](https://github.com/pytorch/pytorch/pull/179735))
- Preserve order of `torch.cond` ([#179457](https://github.com/pytorch/pytorch/pull/179457))
- Fix performance regression caused by user kernel epilogue fusion ([#176772](https://github.com/pytorch/pytorch/pull/176772))
- Fix `torch.compile` performance regression for `cumprod` backward ([#170388](https://github.com/pytorch/pytorch/pull/170388))

### performance
- Add `donate_graph_module` option to `standalone_compile` to avoid extra graph module copies ([#179910](https://github.com/pytorch/pytorch/pull/179910))
- Rewrite multi-consumer `F.pad` as `torch.cat` for zero-copy ([#177216](https://github.com/pytorch/pytorch/pull/177216))
- ROCm: enable pipelining for FlexAttention ([#176676](https://github.com/pytorch/pytorch/pull/176676))
- CPU: make `remove_identity` in-place for inference to align with `pre_grad_passes` ([#177805](https://github.com/pytorch/pytorch/pull/177805))
- CPU: fuse `round` and `to` in quant ([#171699](https://github.com/pytorch/pytorch/pull/171699))
- Fix hardcoded OMP thread counts in `torch.compile` ([#170585](https://github.com/pytorch/pytorch/pull/170585))

### docs
- Fix incorrect remediation instructions in cudagraph pending-backward warning ([#176865](https://github.com/pytorch/pytorch/pull/176865))

### devs
- Refactor `autotune_select_algorithm` to always return a `(node, choice)` tuple ([#177181](https://github.com/pytorch/pytorch/pull/177181))
- Add min/max input distance metric to scheduler nodes ([#175730](https://github.com/pytorch/pytorch/pull/175730))
- Refactor `autoheuristic_use`/`collect` to facilitate configuring/defaulting AH for different ops ([#180276](https://github.com/pytorch/pytorch/pull/180276))

### Untopiced
### not user facing
- select_algorithm.py produces json during mm, admm, etc. tuning. ([#173811](https://github.com/pytorch/pytorch/pull/173811))
- [Inductor] Fix benchmarking Inductor lowering with get_args ([#175111](https://github.com/pytorch/pytorch/pull/175111))
- [Inductor] Async Pipelined Autotuning better handling of benchmarking errors ([#174621](https://github.com/pytorch/pytorch/pull/174621))
- [pallas backend] scalar outputs ([#174836](https://github.com/pytorch/pytorch/pull/174836))
- [Inductor][CUDA][TEST] Allow registration of `_register_woq_lowerings` without `mkldnn` ([#174899](https://github.com/pytorch/pytorch/pull/174899))
- [pallas backend] tiling on tpu ([#175027](https://github.com/pytorch/pytorch/pull/175027))
- Save and load extra_options (compile_options) for MTIA backend ([#173821](https://github.com/pytorch/pytorch/pull/173821))
- [Helion + torch.compile] Allow multi-output template fusion logic override in TemplateBuffer ([#175186](https://github.com/pytorch/pytorch/pull/175186))
- [inductor] Respect use_compute_types in CuteDSLOpOverrides.to_dtype ([#175069](https://github.com/pytorch/pytorch/pull/175069))
- [inductor][BE] Fix test_triton_kernels's make_fx import error ([#175341](https://github.com/pytorch/pytorch/pull/175341))
- [inductor][BE] Fix test_triton_kernel_clone_wekdeps test pollution ([#175342](https://github.com/pytorch/pytorch/pull/175342))
- [inductor] Document `CUTEDSL` and `NVGEMM` in `max_autotune_gemm_backends` config ([#172541](https://github.com/pytorch/pytorch/pull/172541))
- [inductor] Fix shape display for extern/template/nop nodes in graph_diagram SVG ([#175335](https://github.com/pytorch/pytorch/pull/175335))
- [ROCm] Fix positional filtering for cache events ([#175405](https://github.com/pytorch/pytorch/pull/175405))
- [inductor][ez] change online softmax warning to dbg ([#175434](https://github.com/pytorch/pytorch/pull/175434))
- [inductor] Add CUDA graph benchmarking for ExternKernelCaller and min_speedup_threshold ([#175275](https://github.com/pytorch/pytorch/pull/175275))
- [Inductor] Do not freeze layouts on flexattention ([#175445](https://github.com/pytorch/pytorch/pull/175445))
- [inductor] Implement some missing ops for CuteDSLOpOverrides ([#175070](https://github.com/pytorch/pytorch/pull/175070))
- [inductor] Add config patches propagation for scoped autotuning ([#175277](https://github.com/pytorch/pytorch/pull/175277))
- migrate size_hints from 5 files ([#175216](https://github.com/pytorch/pytorch/pull/175216))
- All remianing size_hint deprecation ([#175219](https://github.com/pytorch/pytorch/pull/175219))
- [Inductor] Fix flaky test by changing empty to randn ([#175564](https://github.com/pytorch/pytorch/pull/175564))
- [pallas backend] Eliminate all copies on TPU backend ([#175606](https://github.com/pytorch/pytorch/pull/175606))
- [inductor] support is_inference flag for custom post grad pass ([#171049](https://github.com/pytorch/pytorch/pull/171049))
- [Inductor] Extend prefer_nd_tiling algorithm to tile reduction output dimensions ([#175308](https://github.com/pytorch/pytorch/pull/175308))
- [resubmit] rewrite all remaining size_hint usages in ir.py to support unbacked and use new APIs (#174937) ([#175595](https://github.com/pytorch/pytorch/pull/175595))
- [re-submit] More size-hinting cleanups (#174580) ([#175575](https://github.com/pytorch/pytorch/pull/175575))
- Normalize custom op autotuning fallback choice ([#175422](https://github.com/pytorch/pytorch/pull/175422))
- Add memory cleanup for CUDA graph benchmarking ([#175276](https://github.com/pytorch/pytorch/pull/175276))
- [wrap compiled regions] Fix supporting Nones in compiled outputs ([#175733](https://github.com/pytorch/pytorch/pull/175733))
- [Inductor] Only use bias_addmm if compatible ([#175653](https://github.com/pytorch/pytorch/pull/175653))
- [Pallas TPU] Pallas TPU Compilation Cache Collision ([#175597](https://github.com/pytorch/pytorch/pull/175597))
- [Inductor] Add initial DeviceInterface implementation for TPU ([#175586](https://github.com/pytorch/pytorch/pull/175586))
- [Inductor] Don't do broadcast check if there are unbacked symints ([#175772](https://github.com/pytorch/pytorch/pull/175772))
- [inductor] Fix select_one bitcast size mismatch for sub-32-bit dtypes ([#175430](https://github.com/pytorch/pytorch/pull/175430))
- Use optimization_hint for triton kernel size_hints to fix unbacked perf regression ([#175220](https://github.com/pytorch/pytorch/pull/175220))
- better get_dep_size_hint cost analysis for hinted unbacked ([#175221](https://github.com/pytorch/pytorch/pull/175221))
- [Inductor] Benchmark with layout constrained stride ([#175630](https://github.com/pytorch/pytorch/pull/175630))
- wrap_inductor_compiled keep original gm and retrace for dynamic shapes and aliasing ([#175794](https://github.com/pytorch/pytorch/pull/175794))
- [Inductor] MultiTemplate path even if autotune process pool is shut down ([#175864](https://github.com/pytorch/pytorch/pull/175864))
- [Inductor] Stricter heuristics for epilogue fusion to prevent unprofitable fusions ([#175773](https://github.com/pytorch/pytorch/pull/175773))
- Skip large-XBLOCK autotune configs for combo kernels with persistent sub-kernels on AMD HIP ([#175671](https://github.com/pytorch/pytorch/pull/175671))
- [Inductor][CUDA] Update CUDA arch flags in _nvcc_arch_as_compile_option() ([#175951](https://github.com/pytorch/pytorch/pull/175951))
- fix-cutedsl ([#176048](https://github.com/pytorch/pytorch/pull/176048))
- [Inductor][CUDA][test] Fix test_mm_plus_mm3_dynamic_shapes_gpu_wrapper on CUDA ([#175569](https://github.com/pytorch/pytorch/pull/175569))
- Use version check for XPU fallback registration in inductor ([#174679](https://github.com/pytorch/pytorch/pull/174679))
- [ROCm] Fix multi-arch AOT Inductor compilation with newer Triton LLVM ([#175021](https://github.com/pytorch/pytorch/pull/175021))
- [inductor] mix-order-reduction handle additive expression for num_splits ([#176008](https://github.com/pytorch/pytorch/pull/176008))
- [inductor] Add bitwise tests for compiled Adam/AdamW ([#174911](https://github.com/pytorch/pytorch/pull/174911))
- [inductor][UT] Fix test_pattern_matcher benchmark environment variable not properly set. ([#176046](https://github.com/pytorch/pytorch/pull/176046))
- [Inductor][CUTLASS] Skip CUTLASS backend in non-AOT cpp_wrapper mode ([#176336](https://github.com/pytorch/pytorch/pull/176336))
- Misc clean up + add vecsize sweeping for fwd ([#176055](https://github.com/pytorch/pytorch/pull/176055))
- [Inductor][CUTLASS] Restore addmm input reordering ([#176263](https://github.com/pytorch/pytorch/pull/176263))
- return float("inf")  if having invalid config for codegen triton kernel ([#175698](https://github.com/pytorch/pytorch/pull/175698))
- [Inductor] Fix choice_timings cache override in non benchmark epilogue path ([#176314](https://github.com/pytorch/pytorch/pull/176314))
- [inductor][auto-chunker] Add some elementwise ops to propagation rule ([#176330](https://github.com/pytorch/pytorch/pull/176330))
- [Inductor] Disable "jax_enable_x64" for TPU Pallas codegen. ([#176209](https://github.com/pytorch/pytorch/pull/176209))
- [inductor] handle additive rnumel for mixorder reduction ([#176483](https://github.com/pytorch/pytorch/pull/176483))
- Fix broken type checker with TypeAlias ([#176438](https://github.com/pytorch/pytorch/pull/176438))
- [Inductor] Shut down process pool based on warmup ([#176561](https://github.com/pytorch/pytorch/pull/176561))
- [inductor][CI] Fix cpp-wrapper CI failures ([#176745](https://github.com/pytorch/pytorch/pull/176745))
- [inductor] Add Adadelta to bitwise compiled optimizer tests ([#176758](https://github.com/pytorch/pytorch/pull/176758))
- [inductor] Add Adamax to bitwise compiled optimizer tests ([#176759](https://github.com/pytorch/pytorch/pull/176759))
- [inductor] Add ASGD to bitwise compiled optimizer tests ([#176760](https://github.com/pytorch/pytorch/pull/176760))
- [inductor] Add NAdam to bitwise compiled optimizer tests ([#176761](https://github.com/pytorch/pytorch/pull/176761))
- [inductor] Add RAdam to bitwise compiled optimizer tests ([#176762](https://github.com/pytorch/pytorch/pull/176762))
- [inductor] Add RMSprop to bitwise compiled optimizer tests ([#176763](https://github.com/pytorch/pytorch/pull/176763))
- [inductor] Add Rprop to bitwise compiled optimizer tests ([#176764](https://github.com/pytorch/pytorch/pull/176764))
- [inductor] Improve fusion scoring for split/cat patterns (#175376) ([#176685](https://github.com/pytorch/pytorch/pull/176685))
- [inductor] Cache SDPA constraint results to avoid duplicate buffer copies ([#175599](https://github.com/pytorch/pytorch/pull/175599))
- [Inductor] Prevent circular imports in triton_kernel_wrap ([#176836](https://github.com/pytorch/pytorch/pull/176836))
- [Inductor] Fallback to super().get_read_writes when epilogue_fusion_user_defined_triton_kernel is disabled ([#176832](https://github.com/pytorch/pytorch/pull/176832))
- [inductor][heuristics] Update total tiling score when it is zero ([#176423](https://github.com/pytorch/pytorch/pull/176423))
- [inductor] Drop autotune_at_compile_time config for test_profiler_mark_wrapper_call ([#176801](https://github.com/pytorch/pytorch/pull/176801))
- [inductor] Add singletensor capturable optimizers to bitwise tests ([#176807](https://github.com/pytorch/pytorch/pull/176807))
- [inductor] Add SGD to bitwise optimizer tests ([#176872](https://github.com/pytorch/pytorch/pull/176872))
- [inductor] Add tensor value/alpha samples to inductor opinfo tests ([#176874](https://github.com/pytorch/pytorch/pull/176874))
- Enable reduction splitting for explicitly hinted unbacked symbols ([#175835](https://github.com/pytorch/pytorch/pull/175835))
- Fix weak dep check if not all indices are used ([#175568](https://github.com/pytorch/pytorch/pull/175568))
- Convert fake tensors to detected fake mode in pattern matcher replace_by_example ([#176938](https://github.com/pytorch/pytorch/pull/176938))
- include extern lib hashes in the triton hash ([#175674](https://github.com/pytorch/pytorch/pull/175674))
- [inductor] Add kernel count verification to bitwise optimizer tests ([#177071](https://github.com/pytorch/pytorch/pull/177071))
- Allow slicing block mask data indepently ([#177092](https://github.com/pytorch/pytorch/pull/177092))
- [Inductor] Clear CUTLASSCodeCache.write lru_cache on cache_clear ([#177153](https://github.com/pytorch/pytorch/pull/177153))
- [Inductor] Allow `skip_if_tpu`, `skip_if_cpu`, and `skip_if_cuda` in test_pallas.py to take an optional string as reason. ([#176914](https://github.com/pytorch/pytorch/pull/176914))
- [Inductor] Add proper regression test for Voxtral compilation on MPS ([#177207](https://github.com/pytorch/pytorch/pull/177207))
- [inductor] Enable cpp_wrapper in fbcode ([#177137](https://github.com/pytorch/pytorch/pull/177137))
- [Helion + torch.compile] Fix MultiOutput write deps and extend fusion score matching ([#177302](https://github.com/pytorch/pytorch/pull/177302))
- [Re-land] [Helion + torch.compile] Refactor TemplateBuffer as extensible base class ([#177367](https://github.com/pytorch/pytorch/pull/177367))
- [inductor] Remove more skip_if_cpp_wrapper from test_torchinductor.py ([#177306](https://github.com/pytorch/pytorch/pull/177306))
- [Helion + torch.compile] Refactor template codegen pipeline for extensibility ([#177064](https://github.com/pytorch/pytorch/pull/177064))
- [inductor] Cast symbolic integer scalar exponents for Triton pow ([#177272](https://github.com/pytorch/pytorch/pull/177272))
- [Helion + torch.compile] Extend TemplateBuffer and scheduler for external backends ([#177491](https://github.com/pytorch/pytorch/pull/177491))
- [Helion + torch.compile] Add prologue/epilogue fusion to ExternalTritonTemplateKernel ([#177492](https://github.com/pytorch/pytorch/pull/177492))
- Use output stack traces on output node instead of intermediaries ([#176953](https://github.com/pytorch/pytorch/pull/176953))
- [inductor] Don't mark saved activations as static in backward when forward is partitioned ([#176620](https://github.com/pytorch/pytorch/pull/176620))
- [inductor] Fix shlex quoting in build_fbcode_re command splitting ([#177453](https://github.com/pytorch/pytorch/pull/177453))
- [Inductor] Gate addmm unfuse for half dtypes behind config flag ([#177579](https://github.com/pytorch/pytorch/pull/177579))
- [inductor] fix redundant buffer materialization across layers ([#176307](https://github.com/pytorch/pytorch/pull/176307))
- [Diode] Log epilogue_subtile in data collection workflow (#177420) ([#177420](https://github.com/pytorch/pytorch/pull/177420))
- [Helion + torch.compile] Fix prologue fusion dtype check for multi-output templates ([#177597](https://github.com/pytorch/pytorch/pull/177597))
- [inductor] Reject complex LayerNorm inputs during tracing ([#177527](https://github.com/pytorch/pytorch/pull/177527))
- [Inductor] Preserve float truncation when materializing scalar tensors ([#177494](https://github.com/pytorch/pytorch/pull/177494))
- [Inductor] Explicitly set `jax_enable_x64` to False in Pallas-TPU codegen to avoid interference between tests. ([#177586](https://github.com/pytorch/pytorch/pull/177586))
- [inductor] fix oom of mix-order-red in ci ([#177674](https://github.com/pytorch/pytorch/pull/177674))
- [inductor][nccl estimator] Resolve cuda backend correctly ([#175896](https://github.com/pytorch/pytorch/pull/175896))
- [inductor] fix sdpa pattern matcher issue when scale is not default  ([#174361](https://github.com/pytorch/pytorch/pull/174361))
- [Inductor]: Cast to long for max when calculating grid (#177395) ([#177395](https://github.com/pytorch/pytorch/pull/177395))
- [inductor] run small dce after pattern match so it does not insert dead code ([#177547](https://github.com/pytorch/pytorch/pull/177547))
- [torchTLX] Consolidate TLX knobs + TLXInductorChoices subclass (#177748) ([#177748](https://github.com/pytorch/pytorch/pull/177748))
- [Inductor] Fix MixOrderReduction split reduction group during codegen (#177419) ([#177419](https://github.com/pytorch/pytorch/pull/177419))
- Filter ALL reduction configs by max_persistent_rblock on AMD HIP (#177574) ([#177574](https://github.com/pytorch/pytorch/pull/177574))
- [ROCm][Inductor] Emit tt.pointer_range=32 for small tensor arguments ([#176675](https://github.com/pytorch/pytorch/pull/176675))
- [inductor][auto_chunker] Add support for amax backward ([#176505](https://github.com/pytorch/pytorch/pull/176505))
- [inductor] fix triton api change in nightly for is_active_gpu with a shim ([#177358](https://github.com/pytorch/pytorch/pull/177358))
- Issue 176712 triton user kernel ([#177033](https://github.com/pytorch/pytorch/pull/177033))
- [Inductor] MixOrderReduction account for keepdim (#177782) ([#177782](https://github.com/pytorch/pytorch/pull/177782))
- [Inductor][NVGEMM] Refactor tests ([#176847](https://github.com/pytorch/pytorch/pull/176847))
- [Inductor] Fix benchmark_example_value losing dtype on view unwrap ([#176859](https://github.com/pytorch/pytorch/pull/176859))
- [opaque obj] Filter out opaque objs from inductor handling ([#177991](https://github.com/pytorch/pytorch/pull/177991))
- Fix store_cache miss for TMA epilogue stores causing NameError ([#177990](https://github.com/pytorch/pytorch/pull/177990))
- [inductor] pre comm passes graph spmd check ([#177960](https://github.com/pytorch/pytorch/pull/177960))
- RFC: Increase Pattern Matcher Observability   ([#177032](https://github.com/pytorch/pytorch/pull/177032))
- [inductor] Make CUTLASS non-AOT cpp_wrapper warning only warn once ([#178159](https://github.com/pytorch/pytorch/pull/178159))
- [torchTLX] Rename fused TLX kernels with tlx prefix (#177590) ([#177590](https://github.com/pytorch/pytorch/pull/177590))
- [Inductor][Pallas] Support handling 0-D tensors ([#178193](https://github.com/pytorch/pytorch/pull/178193))
- Adding override_best_choice hook to InductorChoices ([#178212](https://github.com/pytorch/pytorch/pull/178212))
- [inductor][cutedsl] Fix ssa_to_indexable crash when loading 0-dim tensor in mask_mod ([#177813](https://github.com/pytorch/pytorch/pull/177813))
- [Inductor][Pallas] Add reason annotations for a few TPU tests skipped due to intrinsic Pallas limitations ([#178279](https://github.com/pytorch/pytorch/pull/178279))
- [Inductor][Pallas] Enable sign() TPU test, which already works fine ([#178281](https://github.com/pytorch/pytorch/pull/178281))
- [Inductor][Pallas] Unblock var_mean() TPU test which works fine via Inductor but fails in torch_tpu eager mode ([#178282](https://github.com/pytorch/pytorch/pull/178282))
- Add inductor output code test for record_stream ordering ([#178254](https://github.com/pytorch/pytorch/pull/178254))
- [inductor][auto_chunker] Add gather/scatter propagation and generaliz… ([#178017](https://github.com/pytorch/pytorch/pull/178017))
- Package Triton kernel metadata into Lowering output torch package (#177571) ([#177571](https://github.com/pytorch/pytorch/pull/177571))
- [opaque] Add OpaqueObjectState to support opaque objects as inductor graph inputs ([#178114](https://github.com/pytorch/pytorch/pull/178114))
- add option to avoid generating runtime assertions in inductor code ([#175871](https://github.com/pytorch/pytorch/pull/175871))
- [inductor] Add structural divisibility analysis to statically_known_multiple_of  ([#177214](https://github.com/pytorch/pytorch/pull/177214))
- [Helion + torch.compile] Support per-template prologue/epilogue fusion flags in scheduler ([#178555](https://github.com/pytorch/pytorch/pull/178555))
- [inductor] Fix test_triton_autotuning and test_triton_mutated_autotuning failures after Triton 3.7 pin update ([#178583](https://github.com/pytorch/pytorch/pull/178583))
- [inductor] Use -O1 for GPU cpp_wrapper C++ compilation ([#178166](https://github.com/pytorch/pytorch/pull/178166))
- [Inductor] Prefer smaller R0_BLOCK for Blackwell (#178512) ([#178512](https://github.com/pytorch/pytorch/pull/178512))
- [Inductor][Pallas] Use a _BufferIndexing dataclass to ecapsulate buffer indexing info  ([#178608](https://github.com/pytorch/pytorch/pull/178608))
- [Inductor][Pallas] Use a _BroadcastedIterVar dataclass to encapsulate info needed to codegen broadcasted iter vars ([#178609](https://github.com/pytorch/pytorch/pull/178609))
- [Inductor][Pallas] Small refactor in _codegen_iteration_vars() to factor out common logic ([#178610](https://github.com/pytorch/pytorch/pull/178610))
- [inductor] Bundle only winning autotuning configs in TritonBundler                                                                                                                                                                                          ([#178470](https://github.com/pytorch/pytorch/pull/178470))
- inductor: Fix invalid tiling for >=3D reductions w/max_tiles ([#177136](https://github.com/pytorch/pytorch/pull/177136))
- [coor] Don't pickle TorchBindObject graph inputs in benchmark codegen ([#178117](https://github.com/pytorch/pytorch/pull/178117))
- [Helion + torch.compile] Add codegen hooks for fusion-aware autotuning in external template backends ([#178556](https://github.com/pytorch/pytorch/pull/178556))
- [xpu][fix] Fix test_flash_attention_dynamic on XPU. ([#178369](https://github.com/pytorch/pytorch/pull/178369))
- [Inductor] Normalize example inputs in register replacement ([#176416](https://github.com/pytorch/pytorch/pull/176416))
- [opaque] Exclude OpaqueMultiOutput from tensor IR node check ([#178691](https://github.com/pytorch/pytorch/pull/178691))
- [inductor] Handle OpaqueObjectState in graph outputs and memory planner ([#178701](https://github.com/pytorch/pytorch/pull/178701))
- Add a ds hopper stamp out ([#178816](https://github.com/pytorch/pytorch/pull/178816))
- [xpu][test] Enable test/dynamo/test_aot_compile.py for XPU. ([#178385](https://github.com/pytorch/pytorch/pull/178385))
- [inductor] Make autotune_at_compile_time defaults to False for cpp_wrapper ([#177732](https://github.com/pytorch/pytorch/pull/177732))
- [Inductor] Remove dead code (#178629) ([#178629](https://github.com/pytorch/pytorch/pull/178629))
- [inductor] Cooperative reduction bugfixes ([#177883](https://github.com/pytorch/pytorch/pull/177883))
- WeakDeps preserved when recomputation of size and body during fusing in CPU ([#175623](https://github.com/pytorch/pytorch/pull/175623))
- [inductor] Enable precompiled headers in fbcode (#178870) ([#178870](https://github.com/pytorch/pytorch/pull/178870))
- [xpu][inductor] update Intel Triton commit pin ([#177516](https://github.com/pytorch/pytorch/pull/177516))
- [inductor] fix CantSplit raise error ([#178886](https://github.com/pytorch/pytorch/pull/178886))
- Make inductor_choices_class participate in cache key via uuid() ([#179055](https://github.com/pytorch/pytorch/pull/179055))
- [xpu][fix] Fix DeviceOpOverrides registered incorrectly ([#178959](https://github.com/pytorch/pytorch/pull/178959))
- [inductor] Fix `test_evt_codegen` on Blackwell (cluster_shape mock + SM100 inline expect) ([#177515](https://github.com/pytorch/pytorch/pull/177515))
- Fix WorkspaceArg autotuning allocation: count => bytes ([#179270](https://github.com/pytorch/pytorch/pull/179270))
- inductor: link c10 on Windows cpp wrapper builds ([#178976](https://github.com/pytorch/pytorch/pull/178976))
- [inductor] Fix combo kernel XBLOCK default in lazy triton compile ([#179329](https://github.com/pytorch/pytorch/pull/179329))
- [pytorch] enable frame pointers in aoti_inductor wrappers.so (#179240) ([#179240](https://github.com/pytorch/pytorch/pull/179240))
- Accept GraphModule in create_compiler_config_extra ([#177852](https://github.com/pytorch/pytorch/pull/177852))
- [Inductor] Remove ReinterpretView from all layout constraint considerations (#179283) ([#179283](https://github.com/pytorch/pytorch/pull/179283))
- Add _emit_post_kernel_code hook to TritonTemplateKernel ([#179275](https://github.com/pytorch/pytorch/pull/179275))
- [inductor] Remove fp8 special handling in triton_utils.py ([#178957](https://github.com/pytorch/pytorch/pull/178957))
- Add cache key equivalence mixin to AOTAutogradCacheTests ([#178873](https://github.com/pytorch/pytorch/pull/178873))
- Reject unsupported graph shapes in standalone autograd_cache_key ([#178874](https://github.com/pytorch/pytorch/pull/178874))
- Log when pre-grad pass lacks uuid and cache is bypassed ([#178526](https://github.com/pytorch/pytorch/pull/178526))
- [Bugfix][Ez]: Fix missing CPP20 updates to inductor ([#179474](https://github.com/pytorch/pytorch/pull/179474))
- [inductor] Use `is_dtype_supported` in scatter tests ([#179588](https://github.com/pytorch/pytorch/pull/179588))
- [Inductor] Avoid redundant cache entries in `identify_triton_stores` ([#177843](https://github.com/pytorch/pytorch/pull/177843))
- [pytorch][inductor] Add _print_NaN to sympy expression printers (#179708) ([#179708](https://github.com/pytorch/pytorch/pull/179708))
- [inductor] Add dimension-size guards to BMM template contiguity hints (#179267) ([#179267](https://github.com/pytorch/pytorch/pull/179267))
- [cudagraph] Accept opaque values (DeviceMesh, ProcessGroup) in cudagraph pipeline ([#179793](https://github.com/pytorch/pytorch/pull/179793))
- Extract shared context setup in standalone_compile ([#179915](https://github.com/pytorch/pytorch/pull/179915))
- [inductor] Include provenance_tracking_level in FxGraphCache key (#179728) ([#179728](https://github.com/pytorch/pytorch/pull/179728))
- [inductor] Add CUDAGraphPolicy for pluggable cudagraph wrapping in post_compile ([#180163](https://github.com/pytorch/pytorch/pull/180163))
- [Inductor] Refactor reinterpretview check to after realizing inputs (#180269) ([#180269](https://github.com/pytorch/pytorch/pull/180269))
- Simplify FloorDiv(ModularIndexing) and generalize remove_zero_terms ([#176345](https://github.com/pytorch/pytorch/pull/176345))
### security
