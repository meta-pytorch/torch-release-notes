
# Release Notes worksheet dynamo

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

## dynamo
### bc breaking
### deprecation
### new features
- Add `torch.compiler.set_default_backend` to override the default `torch.compile` backend globally, so out-of-tree backend authors don't need to pass `backend=` at every call site (following the pattern of `torch.set_default_dtype`/`torch.set_default_device`). Explicit `backend=` arguments still take precedence ([#178944](https://github.com/pytorch/pytorch/pull/178944))
- Add `torch.compile(f, isolate_recompiles=True)` to give each `torch.compile` call its own isolated cache bucket, preventing cross-compile interference in cache lookups and recompile-limit checks when multiple `torch.compile` calls target the same function ([#178351](https://github.com/pytorch/pytorch/pull/178351))
- Add `register_multi_grad_hook` support to `@leaf_function`, allowing a backward hook to fire once per backward pass when all `requires_grad` inputs have their gradients computed ([#179609](https://github.com/pytorch/pytorch/pull/179609))
### improvements
- Implement additional Python operators in Dynamo: bitwise and ([#184788](https://github.com/pytorch/pytorch/pull/184788)), bitwise xor ([#184789](https://github.com/pytorch/pytorch/pull/184789)), left/right shift ([#183462](https://github.com/pytorch/pytorch/pull/183462)), floor division ([#185652](https://github.com/pytorch/pytorch/pull/185652)), true division ([#185653](https://github.com/pytorch/pytorch/pull/185653)), remainder ([#185654](https://github.com/pytorch/pytorch/pull/185654)), and divmod ([#185655](https://github.com/pytorch/pytorch/pull/185655))
- Support tracing more constructs in Dynamo: einops 0.8.2 ([#185619](https://github.com/pytorch/pytorch/pull/185619)), `record_function` as a decorator ([#184703](https://github.com/pytorch/pytorch/pull/184703)), `inference_mode` retracing helpers ([#185066](https://github.com/pytorch/pytorch/pull/185066)), `mark_dirty` in the autograd Function HOP ([#184267](https://github.com/pytorch/pytorch/pull/184267)), `warn_only` deterministic toggles ([#180373](https://github.com/pytorch/pytorch/pull/180373)), and the `_maybe_view_chunk_cat` functional collective ([#180389](https://github.com/pytorch/pytorch/pull/180389))
- Support item assignment and deletion (`__setitem__`/`__delitem__`) on more container types in Dynamo via `sq_ass_item`/`mp_ass_subscript` slots ([#182862](https://github.com/pytorch/pytorch/pull/182862), [#182996](https://github.com/pytorch/pytorch/pull/182996))
- Support `torch.accelerator.device_index` and `torch.xpu.device` in the device context manager ([#181846](https://github.com/pytorch/pytorch/pull/181846), [#181847](https://github.com/pytorch/pytorch/pull/181847))
- Improve Triton support under `torch.compile`: accept `tl.constexpr` values as kernel arguments ([#181783](https://github.com/pytorch/pytorch/pull/181783)) and handle `capture_triton` as a no-op during tracing ([#183555](https://github.com/pytorch/pytorch/pull/183555))
- Improve dynamic shape specification: reduce verbosity in shape specs for the common case ([#184271](https://github.com/pytorch/pytorch/pull/184271)), add `SeqSpec` for list/tuple specs with better walk-spec errors ([#185327](https://github.com/pytorch/pytorch/pull/185327)), add `ObjectSpec` ([#182764](https://github.com/pytorch/pytorch/pull/182764)), pipe dynamic spec through `torch.compile` ([#184501](https://github.com/pytorch/pytorch/pull/184501)), and revisit guarding in `mark_dynamic` APIs ([#181469](https://github.com/pytorch/pytorch/pull/181469))
- Improve `torch.compile` device mismatch errors with a dedicated `FakeTensorDeviceMismatchError` and actionable guidance to place inputs, parameters, and buffers on the same device ([#185412](https://github.com/pytorch/pytorch/pull/185412))
- Improve error messages and diagnostics: clearer data-dependent errors for `.any()`/`.all()` ([#180406](https://github.com/pytorch/pytorch/pull/180406)), clearer `torch._check` tensor predicate errors ([#185777](https://github.com/pytorch/pytorch/pull/185777)), user-friendly reasons for skipped frames ([#183596](https://github.com/pytorch/pytorch/pull/183596)), carets in stack traces ([#182393](https://github.com/pytorch/pytorch/pull/182393)), and reporting why a symbol was created dynamically in `symbolic_shapes` logs ([#168331](https://github.com/pytorch/pytorch/pull/168331))
- Make Dynamo exceptions pickleable ([#185725](https://github.com/pytorch/pytorch/pull/185725))
- Inline decomposed quantization helpers in Dynamo ([#185628](https://github.com/pytorch/pytorch/pull/185628))
- Make Dynamo debug/repro utilities device-agnostic ([#184851](https://github.com/pytorch/pytorch/pull/184851))
### bug fixes
- Fix Python container and operator semantics in Dynamo to match CPython: list ([#185425](https://github.com/pytorch/pytorch/pull/185425)) and tuple ([#185427](https://github.com/pytorch/pytorch/pull/185427)) constructors, dict update ([#185428](https://github.com/pytorch/pytorch/pull/185428)), defaultdict inplace union ([#185429](https://github.com/pytorch/pytorch/pull/185429)), frozenset copy identity ([#185430](https://github.com/pytorch/pytorch/pull/185430)), sequence search ([#185431](https://github.com/pytorch/pytorch/pull/185431)), `iand` on bool constants ([#184503](https://github.com/pytorch/pytorch/pull/184503)), `sequence * SymNode` spurious graph break ([#185260](https://github.com/pytorch/pytorch/pull/185260)), and `torch.Size` tensor shape handling ([#184613](https://github.com/pytorch/pytorch/pull/184613))
- Fix symbolic shape / fake tensor handling: `float`/`bool` + `SymNode` ([#183362](https://github.com/pytorch/pytorch/pull/183362)), `PendingUnbackedSymbolNotFound` for 0-d tensor Scalar args ([#182660](https://github.com/pytorch/pytorch/pull/182660)), `GuardOnDataDependentSymNode` on sparse tensors ([#179616](https://github.com/pytorch/pytorch/pull/179616)), and creating symbolic tensors from foreign fake tensors ([#181794](https://github.com/pytorch/pytorch/pull/181794))
- Fix use-after-free issues in `CUDAStream`/`Event` `tp_dealloc` overrides ([#183403](https://github.com/pytorch/pytorch/pull/183403)) and Dynamo dict guard cleanup ([#183753](https://github.com/pytorch/pytorch/pull/183753))
- Fix Dynamo crash when `DeviceMesh` is constructed inside `torch.compile` ([#177201](https://github.com/pytorch/pytorch/pull/177201))
- Fix `torch.compile` crash when an unsupported type is passed to a tensor method inside try/except ([#182106](https://github.com/pytorch/pytorch/pull/182106))
- Skip `wrap_inline` for exec'd Python functions ([#181531](https://github.com/pytorch/pytorch/pull/181531))
- Fix tensor subclass construction under `torch.compile` ([#183337](https://github.com/pytorch/pytorch/pull/183337))
- Preserve eager `torch.full` validation for `nn.Parameter` fill values in Dynamo ([#183915](https://github.com/pytorch/pytorch/pull/183915))
- Prevent accuracy minifier repro recursion ([#184077](https://github.com/pytorch/pytorch/pull/184077))
- Fix AOT export with flex attention `BlockMask` placeholders ([#184611](https://github.com/pytorch/pytorch/pull/184611))
- Accept extra kwargs in `CudagraphsBackend.__call__` ([#182989](https://github.com/pytorch/pytorch/pull/182989))
- Avoid `def forward(self, ..., self, ...)` SyntaxError in `dynamo_graph_capture_for_export` ([#185314](https://github.com/pytorch/pytorch/pull/185314))
- Fix scoped Chromium event reset ([#184973](https://github.com/pytorch/pytorch/pull/184973))
- Fix Dynamo binding of overridden function defaults ([#184852](https://github.com/pytorch/pytorch/pull/184852))
- Fix SAC `context_fn` clobbered by DDPOptimizer's `propagate_metadata` ([#179496](https://github.com/pytorch/pytorch/pull/179496))
- Clear retained fake tensor CUDA constants ([#184445](https://github.com/pytorch/pytorch/pull/184445))
- Fix Dynamo `.grad` reads for new in-graph parameters ([#184972](https://github.com/pytorch/pytorch/pull/184972))
- Graph break on CUDA `manual_seed` in Dynamo so compiled random calls stay reproducible ([#185761](https://github.com/pytorch/pytorch/pull/185761))
- Fix functional tensor `to_dense` no-op ([#184586](https://github.com/pytorch/pytorch/pull/184586))
- Preserve original tensor strides across activation offload/reload ([#186396](https://github.com/pytorch/pytorch/pull/186396))
- Graph break on duplicate autograd Function inputs ([#184281](https://github.com/pytorch/pytorch/pull/184281))
- Raise `IndexError` in compile mode matching eager mode ([#184856](https://github.com/pytorch/pytorch/pull/184856))
- Don't error on a skipped frame when `fullgraph=True` and a non-default stance is set ([#183623](https://github.com/pytorch/pytorch/pull/183623))
- Set the `is_compiling` flag for the whole `torch.compile` session ([#184614](https://github.com/pytorch/pytorch/pull/184614))
- Fix FxGraphCache pickling of opaque types with cyclic references ([#180422](https://github.com/pytorch/pytorch/pull/180422))
- Handle missing Windows C++ compiler in shape guard fallback ([#185447](https://github.com/pytorch/pytorch/pull/185447))
### performance
- Fast path guardless cache hits ([#184683](https://github.com/pytorch/pytorch/pull/184683))
- Optimize jagged NestedTensor compile guards ([#184053](https://github.com/pytorch/pytorch/pull/184053))
- Skip Dynamo graph break for scalar-only binary ops when tensorify is enabled ([#183584](https://github.com/pytorch/pytorch/pull/183584))
- Avoid `repr` in Dynamo `ID_MATCH` guard text ([#184796](https://github.com/pytorch/pytorch/pull/184796))
- Add a pinned memory pool for activation-offloading `ao::offload` ops to avoid per-tensor `cudaHostAlloc` overhead (gated by the `pinned_memory_pool()` context manager) ([#186162](https://github.com/pytorch/pytorch/pull/186162))
### docs
### devs
### not user facing
- Remove plain asserts across the `torch/_dynamo/` codebase in favor of proper error types ([#182150](https://github.com/pytorch/pytorch/pull/182150), [#182151](https://github.com/pytorch/pytorch/pull/182151), [#182161](https://github.com/pytorch/pytorch/pull/182161), [#182162](https://github.com/pytorch/pytorch/pull/182162), [#182163](https://github.com/pytorch/pytorch/pull/182163), [#182164](https://github.com/pytorch/pytorch/pull/182164), [#182165](https://github.com/pytorch/pytorch/pull/182165), [#182166](https://github.com/pytorch/pytorch/pull/182166), [#182167](https://github.com/pytorch/pytorch/pull/182167), [#182168](https://github.com/pytorch/pytorch/pull/182168), [#182169](https://github.com/pytorch/pytorch/pull/182169), [#182170](https://github.com/pytorch/pytorch/pull/182170), [#182171](https://github.com/pytorch/pytorch/pull/182171), [#182172](https://github.com/pytorch/pytorch/pull/182172), [#182173](https://github.com/pytorch/pytorch/pull/182173), [#182177](https://github.com/pytorch/pytorch/pull/182177))
- Migrate away from `unpack_var_sequence` to `unpack_iterable` across Dynamo ([#181914](https://github.com/pytorch/pytorch/pull/181914), [#183477](https://github.com/pytorch/pytorch/pull/183477), [#183478](https://github.com/pytorch/pytorch/pull/183478), [#183480](https://github.com/pytorch/pytorch/pull/183480), [#183481](https://github.com/pytorch/pytorch/pull/183481), [#183574](https://github.com/pytorch/pytorch/pull/183574), [#185152](https://github.com/pytorch/pytorch/pull/185152), [#185153](https://github.com/pytorch/pytorch/pull/185153))
- Remove `error_on_graph_break` from CPython tests ([#182351](https://github.com/pytorch/pytorch/pull/182351), [#182352](https://github.com/pytorch/pytorch/pull/182352), [#182353](https://github.com/pytorch/pytorch/pull/182353), [#182354](https://github.com/pytorch/pytorch/pull/182354), [#182355](https://github.com/pytorch/pytorch/pull/182355), [#182356](https://github.com/pytorch/pytorch/pull/182356), [#182357](https://github.com/pytorch/pytorch/pull/182357), [#182368](https://github.com/pytorch/pytorch/pull/182368))
- Implement additional CPython type slots and generic protocols in Dynamo (`nb_negative`, `nb_positive`, `nb_absolute`, `nb_multiply`/`sq_repeat`, `tp_repr`, `tp_str`, `tp_hash`, `tp_iter`, `tp_richcompare`, `generic_iternext`, `generic_bool`, `sq_item`, and binary `nb_*` slots) ([#181657](https://github.com/pytorch/pytorch/pull/181657), [#182578](https://github.com/pytorch/pytorch/pull/182578), [#182880](https://github.com/pytorch/pytorch/pull/182880), [#182916](https://github.com/pytorch/pytorch/pull/182916), [#182332](https://github.com/pytorch/pytorch/pull/182332), [#180494](https://github.com/pytorch/pytorch/pull/180494), [#181328](https://github.com/pytorch/pytorch/pull/181328), [#178561](https://github.com/pytorch/pytorch/pull/178561), [#181884](https://github.com/pytorch/pytorch/pull/181884), [#179251](https://github.com/pytorch/pytorch/pull/179251), [#184633](https://github.com/pytorch/pytorch/pull/184633), [#181771](https://github.com/pytorch/pytorch/pull/181771), [#184836](https://github.com/pytorch/pytorch/pull/184836), [#184606](https://github.com/pytorch/pytorch/pull/184606), [#181104](https://github.com/pytorch/pytorch/pull/181104))
- Add descriptor-protocol variable trackers (`tp_descr_get_impl` infrastructure, non-data and data descriptor VTs, `StaticMethodVariable`/`ClassMethodVariable`, `member_descriptor`, and metaclass descriptors) ([#182213](https://github.com/pytorch/pytorch/pull/182213), [#182740](https://github.com/pytorch/pytorch/pull/182740), [#182741](https://github.com/pytorch/pytorch/pull/182741), [#182742](https://github.com/pytorch/pytorch/pull/182742), [#182961](https://github.com/pytorch/pytorch/pull/182961), [#182962](https://github.com/pytorch/pytorch/pull/182962))
- Improve Python 3.11+/3.15 compatibility (iterator reconstruction, common constants, `struct.pack`/`functools.reduce` polyfills, generator calling, virtual iterators, and `IMPORT_NAME` generation) ([#183491](https://github.com/pytorch/pytorch/pull/183491), [#184828](https://github.com/pytorch/pytorch/pull/184828), [#185403](https://github.com/pytorch/pytorch/pull/185403), [#185566](https://github.com/pytorch/pytorch/pull/185566), [#185682](https://github.com/pytorch/pytorch/pull/185682), [#185675](https://github.com/pytorch/pytorch/pull/185675), [#186402](https://github.com/pytorch/pytorch/pull/186402))
- Add and refactor Dynamo and CPython tests (`test_binop`, `test_deque`, `test_instancecheck`, `test_slice`, `test_isinstance`, tracing user-defined classes in CPython tests, pytest 9 compatibility, nested graph break tests, transformers v5 test updates, and test runner/structure cleanups) ([#181255](https://github.com/pytorch/pytorch/pull/181255), [#181896](https://github.com/pytorch/pytorch/pull/181896), [#182191](https://github.com/pytorch/pytorch/pull/182191), [#183012](https://github.com/pytorch/pytorch/pull/183012), [#184609](https://github.com/pytorch/pytorch/pull/184609), [#181244](https://github.com/pytorch/pytorch/pull/181244), [#182104](https://github.com/pytorch/pytorch/pull/182104), [#182044](https://github.com/pytorch/pytorch/pull/182044), [#182532](https://github.com/pytorch/pytorch/pull/182532), [#185238](https://github.com/pytorch/pytorch/pull/185238), [#181445](https://github.com/pytorch/pytorch/pull/181445), [#163335](https://github.com/pytorch/pytorch/pull/163335), [#180210](https://github.com/pytorch/pytorch/pull/180210), [#181677](https://github.com/pytorch/pytorch/pull/181677), [#181040](https://github.com/pytorch/pytorch/pull/181040))
- Internal dynamic shape specification infrastructure (`IntSpec`, `TensorSpec`, auto naming, doc fixes, and per-dim marking) ([#180525](https://github.com/pytorch/pytorch/pull/180525), [#180923](https://github.com/pytorch/pytorch/pull/180923), [#181844](https://github.com/pytorch/pytorch/pull/181844), [#181922](https://github.com/pytorch/pytorch/pull/181922), [#182534](https://github.com/pytorch/pytorch/pull/182534), [#184120](https://github.com/pytorch/pytorch/pull/184120))
- Refactor and clean up Dynamo variable trackers and builtins (`GetAttr`/`SetAttr`/`HasAttr` builtins, `object.__getattribute__` fallback, `id()` handling, `UserDefinedExceptionVariable`, `DefaultDictVariable`, `_tuplegetter`, removal of legacy method wrapper VTs and `TorchVersionVariable`, and source requirement removal) ([#179033](https://github.com/pytorch/pytorch/pull/179033), [#180585](https://github.com/pytorch/pytorch/pull/180585), [#180622](https://github.com/pytorch/pytorch/pull/180622), [#180630](https://github.com/pytorch/pytorch/pull/180630), [#181327](https://github.com/pytorch/pytorch/pull/181327), [#181329](https://github.com/pytorch/pytorch/pull/181329), [#180174](https://github.com/pytorch/pytorch/pull/180174), [#183347](https://github.com/pytorch/pytorch/pull/183347), [#186001](https://github.com/pytorch/pytorch/pull/186001), [#182359](https://github.com/pytorch/pytorch/pull/182359), [#181687](https://github.com/pytorch/pytorch/pull/181687))
- Clean up `InstructionTranslator` typing and `current_tx()` usage ([#183577](https://github.com/pytorch/pytorch/pull/183577), [#183800](https://github.com/pytorch/pytorch/pull/183800), [#183500](https://github.com/pytorch/pytorch/pull/183500))
- Constant-fold more builtins and modules (`hex`/`oct`/`bin`/`ascii`/`format`, `re` module functions) ([#180627](https://github.com/pytorch/pytorch/pull/180627), [#182186](https://github.com/pytorch/pytorch/pull/182186))
- Add bytecode source attribution to variable trackers ([#179350](https://github.com/pytorch/pytorch/pull/179350), [#180697](https://github.com/pytorch/pytorch/pull/180697))
- Device context manager internals: register API and `torch.xpu.Stream` current-stream handling ([#181848](https://github.com/pytorch/pytorch/pull/181848), [#182792](https://github.com/pytorch/pytorch/pull/182792))
- [dynamo] Forward compiler configs through DDPOptimizer ([#179623](https://github.com/pytorch/pytorch/pull/179623))
- [dynamo] call weakref cleanup on all paths ([#180566](https://github.com/pytorch/pytorch/pull/180566))
- [Dynamo]Add python_type() to TritonKernelVariable ([#180882](https://github.com/pytorch/pytorch/pull/180882))
- [dynamo] Lint Fx graph before sending to backend ([#180922](https://github.com/pytorch/pytorch/pull/180922))
- Add torch._dynamo.override_optimization_hint API for unbacked symbols ([#178544](https://github.com/pytorch/pytorch/pull/178544))
- Fix undefined symbolic variable in fx_graph_runnable repro scripts ([#180298](https://github.com/pytorch/pytorch/pull/180298))
- [dynamo] Taint filtered aliased intermediates with clear error message ([#180929](https://github.com/pytorch/pytorch/pull/180929))
- [dynamo] Support pybind enums ([#180631](https://github.com/pytorch/pytorch/pull/180631))
- [Dynamo] Handle data_ptr equality on detach aliases ([#179347](https://github.com/pytorch/pytorch/pull/179347))
- [dynamo] Defer side-effect checks for nullified mutations in HOP subgraphs ([#180939](https://github.com/pytorch/pytorch/pull/180939))
- [while_loop] support input mutation with auto_functionalize when inference ([#175972](https://github.com/pytorch/pytorch/pull/175972))
- [dynamo] restore Python dispatch TLS across graph breaks ([#180636](https://github.com/pytorch/pytorch/pull/180636))
- Consolidate cache artifact recording ([#180802](https://github.com/pytorch/pytorch/pull/180802))
- Add dynamo handlers for all torch._check* variants ([#181552](https://github.com/pytorch/pytorch/pull/181552))
- [dynamo] Add more info in BACKEND_MATCH recompile ([#178003](https://github.com/pytorch/pytorch/pull/178003))
- [dynamo] Refactor small updates to cleanup set migration. Note on migrating internal re… ([#181388](https://github.com/pytorch/pytorch/pull/181388))
- [dynamo] Fix FakeScriptObject leaking into TYPE_MATCH guards ([#179047](https://github.com/pytorch/pytorch/pull/179047))
- [dynamo] Pass source through WorldMetaClassVariable.var_getattr ([#181928](https://github.com/pytorch/pytorch/pull/181928))
- [dynamo] Add polyfills for operator.concat and operator.iconcat ([#175213](https://github.com/pytorch/pytorch/pull/175213))
- Codegen _backward_epilogue_functional ([#182539](https://github.com/pytorch/pytorch/pull/182539))
- Add `torch._scaled_mm_v2` to the trace rules set ([#180668](https://github.com/pytorch/pytorch/pull/180668))
- [dynamo] Use automatic_with_forced_inputs for local_map subgraph lifting ([#180863](https://github.com/pytorch/pytorch/pull/180863))
- [dynamo] Python codegen for simple fullgraph case POC. [1/n] ([#182090](https://github.com/pytorch/pytorch/pull/182090))
- [dynamo] Get Dynamo CI green again ([#182884](https://github.com/pytorch/pytorch/pull/182884))
- [Dynamo]: Make super().__new__(cls, tensor) traceable in Tensor subclasses ([#182241](https://github.com/pytorch/pytorch/pull/182241))
- [dynamo_compile] Log functorch_config to Scuba per compile region ([#182762](https://github.com/pytorch/pytorch/pull/182762))
- Support constant eval in Dynamo ([#183979](https://github.com/pytorch/pytorch/pull/183979))
- [dynamo] Fix TorchFunctionMode leak on graph break ([#183069](https://github.com/pytorch/pytorch/pull/183069))
- [dynamo] avoid redundant error_on_graph_break toggles ([#184073](https://github.com/pytorch/pytorch/pull/184073))
- Improve Dynamo output graph metadata typing ([#184369](https://github.com/pytorch/pytorch/pull/184369))
- [dynamo] Better handling of issubclass ([#184450](https://github.com/pytorch/pytorch/pull/184450))
- Fix functional accumulate_grad state modeling ([#184082](https://github.com/pytorch/pytorch/pull/184082))
- Fix after_aot repro_run graph mutation ([#184768](https://github.com/pytorch/pytorch/pull/184768))
- Fix Dynamo reconstruction for graph-created Events ([#185594](https://github.com/pytorch/pytorch/pull/185594))
- [dynamo/tvm] Handle ImportError for TVM backend ([#185893](https://github.com/pytorch/pytorch/pull/185893))
- [dynamo, nested graph breaks] disable nested graph breaks on inline_user_function_return by default ([#179844](https://github.com/pytorch/pytorch/pull/179844))
- [dynamo] Add dynamic_values config to mark int sources / tensor dims dynamic by value ([#185292](https://github.com/pytorch/pytorch/pull/185292))
- [FSDP2] remove dead code for dynamo tracable fsdp2 comm hooks ([#179817](https://github.com/pytorch/pytorch/pull/179817))
- Fix various typo and grammar errors across comments, docstrings, and error messages ([#181284](https://github.com/pytorch/pytorch/pull/181284), [#181350](https://github.com/pytorch/pytorch/pull/181350), [#181656](https://github.com/pytorch/pytorch/pull/181656), [#181698](https://github.com/pytorch/pytorch/pull/181698), [#181968](https://github.com/pytorch/pytorch/pull/181968), [#181969](https://github.com/pytorch/pytorch/pull/181969), [#181989](https://github.com/pytorch/pytorch/pull/181989), [#184215](https://github.com/pytorch/pytorch/pull/184215), [#185714](https://github.com/pytorch/pytorch/pull/185714), [#185719](https://github.com/pytorch/pytorch/pull/185719), [#185721](https://github.com/pytorch/pytorch/pull/185721), [#180609](https://github.com/pytorch/pytorch/pull/180609), [#181345](https://github.com/pytorch/pytorch/pull/181345), [#181472](https://github.com/pytorch/pytorch/pull/181472), [#181911](https://github.com/pytorch/pytorch/pull/181911), [#181981](https://github.com/pytorch/pytorch/pull/181981), [#184214](https://github.com/pytorch/pytorch/pull/184214), [#185342](https://github.com/pytorch/pytorch/pull/185342))
### security
