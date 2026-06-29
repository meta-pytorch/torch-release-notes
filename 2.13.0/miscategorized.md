# Miscategorized PRs

PRs that ended up in the wrong worksheet, organized by which area they belong to.

## cuda
- Expose torch.cuda.current_solver_handle for cuSOLVER handle sharing ([#176705](https://github.com/pytorch/pytorch/pull/176705)) (from dynamo; labeled `release notes: cuda`)

## export
- Make functorch JVP operator torch.exportable ([#179686](https://github.com/pytorch/pytorch/pull/179686)) (from dynamo; labeled `release notes: export`)

- Fix typos in inductor and export comments ([#181971](https://github.com/pytorch/pytorch/pull/181971)) (from inductor; labeled `release notes: export`)
- [AOTI] Add UpdateConstantBufferFromCpu for host to device copy ([#181637](https://github.com/pytorch/pytorch/pull/181637)) (from inductor; labeled `release notes: export`)

## autograd
- Add torch.autograd.graph.region_activation_memory_budget ([#185979](https://github.com/pytorch/pytorch/pull/185979)) (from dynamo; labeled `release notes: autograd`)

## mps
(from inductor (aoti) — these are pure MPS kernel changes that also carried a `release notes: inductor (aoti)` label)
- [MPS] grid_sampler_3d backward pass ([#179388](https://github.com/pytorch/pytorch/pull/179388))
- [MPS] Flatten 5D tensors to 4D in batch_norm for performance ([#180335](https://github.com/pytorch/pytorch/pull/180335))

## quantization
- Remove unused noqa directives in torch/, batch 2 ([#180136](https://github.com/pytorch/pytorch/pull/180136)) (from inductor; labeled `release notes: quantization`)

## inductor (aoti)
- Fix inductor AOTI codegen for float('inf')/float('-inf') kernel args (#180297) ([#180297](https://github.com/pytorch/pytorch/pull/180297)) (from inductor; labeled `release notes: inductor (aoti)`)
- [5/11][aoti] Add C-ABI-safe V2 interface for MinimalArrayref (#179483) ([#179483](https://github.com/pytorch/pytorch/pull/179483)) (from inductor; labeled `release notes: inductor (aoti)`)
- [inductor] Fix MSVC path append in kernel context stack compression ([#179857](https://github.com/pytorch/pytorch/pull/179857)) (from inductor; labeled `release notes: inductor (aoti)`)
- [aoti] Fix cond subgraph arrayref dispatch with generic lambda ([#180558](https://github.com/pytorch/pytorch/pull/180558)) (from inductor; labeled `release notes: inductor (aoti)`)
- [inductor] Fix MSVC const pointer emission in cpp wrapper temporary arrays ([#179846](https://github.com/pytorch/pytorch/pull/179846)) (from inductor; labeled `release notes: inductor (aoti)`)
- Preserve AOTI proxy_executor error messages (#180884) ([#180884](https://github.com/pytorch/pytorch/pull/180884)) (from inductor; labeled `release notes: inductor (aoti)`)
- [inductor][cpu] Enable Triton kernels in AOTI C++ wrapper on CPU (#181068) ([#181068](https://github.com/pytorch/pytorch/pull/181068)) (from inductor; labeled `release notes: inductor (aoti)`)
- [inductor] Remove del statement to fix RUFF F821 lint in combo kernel benchmark cleanup ([#182321](https://github.com/pytorch/pytorch/pull/182321)) (from inductor; labeled `release notes: inductor (aoti)`)
- [Inductor] Add explicit headers for CPP wrapper to fix MSVC compilation ([#180120](https://github.com/pytorch/pytorch/pull/180120)) (from inductor; labeled `release notes: inductor (aoti)`)
- [7A/11][aoti] Add C-ABI-safe V2 interface for UpdateConstantsMap ([#180533](https://github.com/pytorch/pytorch/pull/180533)) (from inductor; labeled `release notes: inductor (aoti)`)
- [aoti] Fix arrayref proxy executor tensor args ([#182751](https://github.com/pytorch/pytorch/pull/182751)) (from inductor; labeled `release notes: inductor (aoti)`)
- [inductor][cpp_wrapper] Defer Triton compile kickoff out of static init (#182824) ([#182824](https://github.com/pytorch/pytorch/pull/182824)) (from inductor; labeled `release notes: inductor (aoti)`)
- [inductor] Expose torchbind constants from AOTIModelPackageLoader ([#182149](https://github.com/pytorch/pytorch/pull/182149)) (from inductor; labeled `release notes: inductor (aoti)`)
- [ROCm] Fix maybe_hipify_code_wrapper for bare-token inputs ([#183725](https://github.com/pytorch/pytorch/pull/183725)) (from inductor; labeled `release notes: inductor (aoti)`)
- [Inductor] Skip CPU vec ISA setup for device-only cpp_wrapper ([#182089](https://github.com/pytorch/pytorch/pull/182089)) (from inductor; labeled `release notes: inductor (aoti)`)
- [inductor][refactor] Extract lazy scratch allocation as a util function ([#184731](https://github.com/pytorch/pytorch/pull/184731)) (from inductor; labeled `release notes: inductor (aoti)`)
- [inductor][refactor] Introduce AssertDivByZeroLine WrapperLine ([#184732](https://github.com/pytorch/pytorch/pull/184732)) (from inductor; labeled `release notes: inductor (aoti)`)
- [8.1A/11][aoti] Add C-ABI-safe ExtractConstantsMapForEach (#183030) ([#183030](https://github.com/pytorch/pytorch/pull/183030)) (from inductor; labeled `release notes: inductor (aoti)`)
- [8.2A/11][aoti] Add C-ABI-safe UpdateConstantBufferPairs (#183031) ([#183031](https://github.com/pytorch/pytorch/pull/183031)) (from inductor; labeled `release notes: inductor (aoti)`)
- [8.3A/11][aoti] Add C-ABI-safe UpdateConstantBufferFromCpuPairs (#183032) ([#183032](https://github.com/pytorch/pytorch/pull/183032)) (from inductor; labeled `release notes: inductor (aoti)`)
- [8.4A/11][aoti] Add C-ABI-safe UpdateInactiveConstantBufferPairs (#183033) ([#183033](https://github.com/pytorch/pytorch/pull/183033)) (from inductor; labeled `release notes: inductor (aoti)`)
- Fix cpp wrapper while loop carried mutations ([#183657](https://github.com/pytorch/pytorch/pull/183657)) (from inductor; labeled `release notes: inductor (aoti)`)
- Reapply [8.5A/11][aoti] Add C-ABI-safe AOTInductorModelCreateV2 ([#185729](https://github.com/pytorch/pytorch/pull/185729)) (from inductor; labeled `release notes: inductor (aoti)`)
- [inductor] Resolve relative TORCHINDUCTOR_CACHE_DIR ([#185723](https://github.com/pytorch/pytorch/pull/185723)) (from inductor; labeled `release notes: inductor (aoti)`)
- Improve AOTI error for Python custom ops ([#186305](https://github.com/pytorch/pytorch/pull/186305)) (from inductor; labeled `release notes: inductor (aoti)`)
- Fix AOTI CUDA device copy allocation ([#185634](https://github.com/pytorch/pytorch/pull/185634)) (from inductor; labeled `release notes: inductor (aoti)`)

## dynamo
- [Optimus] Add another batch linear anchor node ([#180477](https://github.com/pytorch/pytorch/pull/180477)) (from inductor; labeled `release notes: dynamo`)
- [Optimus] Support detach method call (#180513) ([#180513](https://github.com/pytorch/pytorch/pull/180513)) (from inductor; labeled `release notes: dynamo`)
- Fix FxGraphCache pickling of opaque types with cyclic references ([#180422](https://github.com/pytorch/pytorch/pull/180422)) (from inductor; labeled `release notes: dynamo`)
- Handle missing Windows C++ compiler in shape guard fallback ([#185447](https://github.com/pytorch/pytorch/pull/185447)) (from inductor; labeled `release notes: dynamo`)

## releng
- [Inductor] Add batch-invariant accuracy mode for benchmark perf tests ([#180610](https://github.com/pytorch/pytorch/pull/180610)) (from inductor; labeled `release notes: releng`)

## composability
- [inductor] Fix mix_order_reduction over-fusion via load count check ([#179494](https://github.com/pytorch/pytorch/pull/179494)) (from inductor; labeled `release notes: composability`)
- Formalize out= operators and custom operators definition ([#180851](https://github.com/pytorch/pytorch/pull/180851)) (from inductor; labeled `release notes: composability`)
- Support out-tagged custom operators in torch.compile ([#180852](https://github.com/pytorch/pytorch/pull/180852)) (from inductor; labeled `release notes: composability`)
- Enable Armv9-A target support for torch.compile on AArch64 ([#184555](https://github.com/pytorch/pytorch/pull/184555)) (from inductor; labeled `release notes: composability`)

## fx
- [pyrefly] Add type annotations to torch/fx graph and graph_module  ([#180994](https://github.com/pytorch/pytorch/pull/180994)) (from inductor; labeled `release notes: fx`)
- Fix typos in comments and docstrings ([#181967](https://github.com/pytorch/pytorch/pull/181967)) (from inductor; labeled `release notes: fx`)
- Fix indefinite article typos: "a" → "an" before vowels ([#184216](https://github.com/pytorch/pytorch/pull/184216)) (from inductor; labeled `release notes: fx`)
- [Inductor] Fix stale backed-symbol references in AOTI deferred runtime asserts (#184624) ([#184624](https://github.com/pytorch/pytorch/pull/184624)) (from inductor; labeled `release notes: fx`)
- Preserve FX graph cache guard provenance ([#184193](https://github.com/pytorch/pytorch/pull/184193)) (from inductor; labeled `release notes: fx`)
- Fix `torch.cat` axis handling in Inductor pre-grad fusion ([#183995](https://github.com/pytorch/pytorch/pull/183995)) (from inductor; labeled `release notes: fx`)
- Avoid a Triton sort compile-time cliff in `create_block_mask` ([#182745](https://github.com/pytorch/pytorch/pull/182745)) (from inductor; labeled `release notes: fx`)
- [Inductor] Support dynamic shapes in sort lowering and symbolic floor/ceil in FX wrapper ([#182786](https://github.com/pytorch/pytorch/pull/182786)) (from inductor; labeled `release notes: fx`)
- Fix AOT FXIR parallel Triton kernel reload that failed with `AttributeError` when the worker returned a pickled, stripped `JITFunction` ([#185134](https://github.com/pytorch/pytorch/pull/185134)) (from inductor; labeled `release notes: fx`)

## jit
- Fix duplicated article "the the" typos in comments ([#181672](https://github.com/pytorch/pytorch/pull/181672)) (from inductor; labeled `release notes: jit`)
- Fix typos across torch codebase ([#181813](https://github.com/pytorch/pytorch/pull/181813)) (from inductor; labeled `release notes: jit`)
- Fix duplicate-word typos and a misspelling in comments and docs ([#181934](https://github.com/pytorch/pytorch/pull/181934)) (from inductor; labeled `release notes: jit`)
- Fix typos in comments and docstrings across torch ([#181978](https://github.com/pytorch/pytorch/pull/181978)) (from inductor; labeled `release notes: jit`)
- Fix typos in comments, docstrings, and documentation ([#181966](https://github.com/pytorch/pytorch/pull/181966)) (from inductor; labeled `release notes: jit`)
- Fix typos in comments and documentation ([#185241](https://github.com/pytorch/pytorch/pull/185241)) (from inductor; labeled `release notes: jit`)

## distributed (torchelastic)
- Fix typos in comments and docstrings ([#182246](https://github.com/pytorch/pytorch/pull/182246)) (from inductor; labeled `release notes: distributed (torchelastic)`)

## distributed (c10d)
- Fix grammar typos in comments and error messages ([#182806](https://github.com/pytorch/pytorch/pull/182806)) (from inductor; labeled `release notes: distributed (c10d)`)

## foreach_frontend
- [easy][compile] fix _foreach_sub ([#184421](https://github.com/pytorch/pytorch/pull/184421)) (from inductor; labeled `release notes: foreach_frontend`)
- [Inductor] Make per_subkernel_blocks an explicit ForeachKernelSchedulerNode attribute ([#182901](https://github.com/pytorch/pytorch/pull/182901)) (from inductor; labeled `release notes: foreach_frontend`)

## linalg_frontend
- [Inductor][Bucketing] Make collective bucketing tolerate hinted unbacked SymInts ([#183544](https://github.com/pytorch/pytorch/pull/183544)) (from inductor; labeled `release notes: linalg_frontend`)

## cpp
- Fix typos in comments and docstrings ([#186234](https://github.com/pytorch/pytorch/pull/186234)) (from inductor; labeled `release notes: cpp`)

## distributed (pipeline)
- [Inductor][TP] Fuse slice-cat TP collective patterns ([#184911](https://github.com/pytorch/pytorch/pull/184911)) (from inductor; labeled `release notes: distributed (pipeline)`)

## distributed (dtensor)
- [Inductor][CK][ROCm] Update CK pin and build wheel alongside PyTorch ([#178181](https://github.com/pytorch/pytorch/pull/178181)) (from inductor; labeled `release notes: distributed (dtensor)`)
