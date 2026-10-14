
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
- Add `torch.compiler.config.static_sources` (`TORCH_COMPILE_STATIC_SOURCES`), the inverse of `dynamic_sources`, listing sources that stay static even under automatic dynamic shapes, PGO, or `dynamic=True`, but not explicit `mark_dynamic` ([#193626](https://github.com/pytorch/pytorch/pull/193626))
- Let custom backends define a `_dynamo_backend_init` callable that runs when `torch.compile()` resolves the backend, so out-of-tree backends can load native libraries or set up devices and fail fast ([#192345](https://github.com/pytorch/pytorch/pull/192345))
### improvements
- Support more Python in compiled regions: `bytearray`, `types.SimpleNamespace`, `bytes()`, calling `classmethod`/`staticmethod`, list subclasses overriding `__new__`, `del` of captured variables, and more of `math`, `cmath`, `operator` and `heapq` ([#192205](https://github.com/pytorch/pytorch/pull/192205), [#199252](https://github.com/pytorch/pytorch/pull/199252), [#193719](https://github.com/pytorch/pytorch/pull/193719), [#196103](https://github.com/pytorch/pytorch/pull/196103), [#197499](https://github.com/pytorch/pytorch/pull/197499), [#197781](https://github.com/pytorch/pytorch/pull/197781), [#191512](https://github.com/pytorch/pytorch/pull/191512), [#189216](https://github.com/pytorch/pytorch/pull/189216), [#196867](https://github.com/pytorch/pytorch/pull/196867), [#197498](https://github.com/pytorch/pytorch/pull/197498), [#197222](https://github.com/pytorch/pytorch/pull/197222), [#198685](https://github.com/pytorch/pytorch/pull/198685), [#195999](https://github.com/pytorch/pytorch/pull/195999), [#192942](https://github.com/pytorch/pytorch/pull/192942), [#192834](https://github.com/pytorch/pytorch/pull/192834), [#195765](https://github.com/pytorch/pytorch/pull/195765))
- Improve exception and object-model support: exception identity checks, `delattr` and `super().__init__(msg)` on exceptions, non-string `assert` messages, `property` attributes, `types.DynamicClassAttribute`, and closure-cell comparison ([#191404](https://github.com/pytorch/pytorch/pull/191404), [#196722](https://github.com/pytorch/pytorch/pull/196722), [#196051](https://github.com/pytorch/pytorch/pull/196051), [#197798](https://github.com/pytorch/pytorch/pull/197798), [#194642](https://github.com/pytorch/pytorch/pull/194642), [#199260](https://github.com/pytorch/pytorch/pull/199260), [#197189](https://github.com/pytorch/pytorch/pull/197189))
- Raise the real Python exception (e.g. `TypeError`) for user errors detected while tracing instead of graph breaking ([#196432](https://github.com/pytorch/pytorch/pull/196432))
- Trace more without graph breaks: setting `requires_grad = True` on in-region tensors, `Tensor.storage_offset()` on inputs, `Tensor.is_pinned()`, builtin function `__name__`, `hasattr`/`getattr` on opaque objects such as `ProcessGroup`, attribute reads on `autograd.Function` subclasses, `setattr` on `torch.split` outputs, and torchvision `roi_align` ([#191129](https://github.com/pytorch/pytorch/pull/191129), [#197224](https://github.com/pytorch/pytorch/pull/197224), [#186494](https://github.com/pytorch/pytorch/pull/186494), [#196049](https://github.com/pytorch/pytorch/pull/196049), [#196050](https://github.com/pytorch/pytorch/pull/196050), [#185316](https://github.com/pytorch/pytorch/pull/185316), [#198514](https://github.com/pytorch/pytorch/pull/198514), [#185528](https://github.com/pytorch/pytorch/pull/185528))
- With `allow_rnn` disabled, graph break at the `nn.RNN`/`nn.GRU`/`nn.LSTM` call so the rest of the frame compiles ([#186614](https://github.com/pytorch/pytorch/pull/186614))
- Avoid recompiles when ops on constant inputs produce unused results ([#191143](https://github.com/pytorch/pytorch/pull/191143), [#191144](https://github.com/pytorch/pytorch/pull/191144), [#191145](https://github.com/pytorch/pytorch/pull/191145))
- Improve out-of-tree accelerator support: `DeviceInterface` streams and events, renamed PrivateUse1 tensor classes, cross-stream deallocation safety, and `torch.mtia` streams ([#194343](https://github.com/pytorch/pytorch/pull/194343), [#195432](https://github.com/pytorch/pytorch/pull/195432), [#197187](https://github.com/pytorch/pytorch/pull/197187), [#195649](https://github.com/pytorch/pytorch/pull/195649))
- Forward `torch.compile(..., name=...)` to custom backends as `kwargs["name"]` ([#196229](https://github.com/pytorch/pytorch/pull/196229))
- Improve diagnostics: less warning spam on backend fallbacks, carets in graph-break stacks, and clearer recompile reasons and error hints ([#185155](https://github.com/pytorch/pytorch/pull/185155), [#186249](https://github.com/pytorch/pytorch/pull/186249), [#185466](https://github.com/pytorch/pytorch/pull/185466), [#185419](https://github.com/pytorch/pytorch/pull/185419), [#197464](https://github.com/pytorch/pytorch/pull/197464), [#197450](https://github.com/pytorch/pytorch/pull/197450), [#186082](https://github.com/pytorch/pytorch/pull/186082), [#195691](https://github.com/pytorch/pytorch/pull/195691))
- `aot_compile` serializes more functions (`functools.wraps` helpers, `types.MethodType`, closure cells) and prunes unpicklable values no guard reads ([#196472](https://github.com/pytorch/pytorch/pull/196472), [#196473](https://github.com/pytorch/pytorch/pull/196473), [#196474](https://github.com/pytorch/pytorch/pull/196474), [#196476](https://github.com/pytorch/pytorch/pull/196476), [#196478](https://github.com/pytorch/pytorch/pull/196478), [#196479](https://github.com/pytorch/pytorch/pull/196479), [#196481](https://github.com/pytorch/pytorch/pull/196481), [#196684](https://github.com/pytorch/pytorch/pull/196684), [#196685](https://github.com/pytorch/pytorch/pull/196685), [#196686](https://github.com/pytorch/pytorch/pull/196686), [#196687](https://github.com/pytorch/pytorch/pull/196687), [#196691](https://github.com/pytorch/pytorch/pull/196691), [#196692](https://github.com/pytorch/pytorch/pull/196692), [#197750](https://github.com/pytorch/pytorch/pull/197750), [#197752](https://github.com/pytorch/pytorch/pull/197752), [#197754](https://github.com/pytorch/pytorch/pull/197754), [#197755](https://github.com/pytorch/pytorch/pull/197755), [#197833](https://github.com/pytorch/pytorch/pull/197833), [#197762](https://github.com/pytorch/pytorch/pull/197762))
- `load_compiled_function(..., f_globals=...)` and loaded `aot_compile` modules resolve guarded globals against the live scope and re-read them on each call; a guarded global missing from `f_globals` fails with `KeyError on G['NAME']` ([#196815](https://github.com/pytorch/pytorch/pull/196815), [#196817](https://github.com/pytorch/pytorch/pull/196817), [#196818](https://github.com/pytorch/pytorch/pull/196818), [#196908](https://github.com/pytorch/pytorch/pull/196908), [#196897](https://github.com/pytorch/pytorch/pull/196897), [#197218](https://github.com/pytorch/pytorch/pull/197218), [#196904](https://github.com/pytorch/pytorch/pull/196904))
- Make `aot_compile` module dispatch more robust and improve its error messages for guard mismatches, missing globals, unpicklable values and incompatible artifacts ([#197055](https://github.com/pytorch/pytorch/pull/197055), [#196826](https://github.com/pytorch/pytorch/pull/196826), [#197047](https://github.com/pytorch/pytorch/pull/197047), [#196823](https://github.com/pytorch/pytorch/pull/196823), [#197149](https://github.com/pytorch/pytorch/pull/197149), [#197048](https://github.com/pytorch/pytorch/pull/197048), [#197220](https://github.com/pytorch/pytorch/pull/197220), [#197050](https://github.com/pytorch/pytorch/pull/197050), [#197257](https://github.com/pytorch/pytorch/pull/197257), [#197319](https://github.com/pytorch/pytorch/pull/197319), [#196816](https://github.com/pytorch/pytorch/pull/196816), [#196693](https://github.com/pytorch/pytorch/pull/196693), [#196819](https://github.com/pytorch/pytorch/pull/196819), [#197391](https://github.com/pytorch/pytorch/pull/197391), [#198061](https://github.com/pytorch/pytorch/pull/198061), [#196470](https://github.com/pytorch/pytorch/pull/196470), [#197756](https://github.com/pytorch/pytorch/pull/197756))
- `maybe_mark_dynamic` accepts `min`/`max` for an initial value range, and passing only one of them to `mark_dynamic` no longer crashes ([#194625](https://github.com/pytorch/pytorch/pull/194625))
- Keep the device index of `torch.cuda.synchronize()` unresolved under the experimental `torch.distributed.config.compile_on_one_rank` mode, so the artifact is not rank-specific ([#196937](https://github.com/pytorch/pytorch/pull/196937))
### bug fixes
- Fix guards treating `-0.0` and `0.0` as equal and rejecting `NaN` constants, which reused graphs with the wrong float ([#192604](https://github.com/pytorch/pytorch/pull/192604), [#192608](https://github.com/pytorch/pytorch/pull/192608))
- Fix relational guards being skipped by the dict-version shortcut ([#185911](https://github.com/pytorch/pytorch/pull/185911))
- Guard autocast objects by value, fixing spurious recompiles and stale graphs ([#194754](https://github.com/pytorch/pytorch/pull/194754))
- Fix silently wrong results from `isinstance` with `@runtime_checkable` Protocols, zero-argument `super()` in classmethods, user descriptors, and closure-list mutations in local classes ([#196124](https://github.com/pytorch/pytorch/pull/196124), [#198435](https://github.com/pytorch/pytorch/pull/198435), [#198410](https://github.com/pytorch/pytorch/pull/198410), [#197830](https://github.com/pytorch/pytorch/pull/197830))
- Fix `random` module draws returning stale values on cache hits, ignoring `random.seed()`, or using float32 ([#196921](https://github.com/pytorch/pytorch/pull/196921), [#197221](https://github.com/pytorch/pytorch/pull/197221), [#199075](https://github.com/pytorch/pytorch/pull/199075))
- Fix `torch.Tensor(torch.Size([...]))` selecting the wrong overload ([#196717](https://github.com/pytorch/pytorch/pull/196717))
- Fix wrong or missing gradients with custom `autograd.Function`s under `torch.func`, graph breaks at `torch.autograd.grad`, and shape-changing `Parameter.data` assignments ([#193724](https://github.com/pytorch/pytorch/pull/193724), [#185829](https://github.com/pytorch/pytorch/pull/185829), [#186512](https://github.com/pytorch/pytorch/pull/186512), [#184704](https://github.com/pytorch/pytorch/pull/184704))
- Reject input mutation or aliasing in higher-order op bodies that do not support it, such as `flex_attention` `mask_mod` ([#185738](https://github.com/pytorch/pytorch/pull/185738))
- Fix `out=` variants of `torch.max`, `torch.min` and `torch.topk` recompiling on every new shape ([#187952](https://github.com/pytorch/pytorch/pull/187952))
- Fix memory leaks keeping CUDA tensors, Python stacks, and higher-order op inputs alive after compilation ([#193015](https://github.com/pytorch/pytorch/pull/193015), [#197567](https://github.com/pytorch/pytorch/pull/197567), [#195954](https://github.com/pytorch/pytorch/pull/195954))
- Fix crashes, internal errors and guard edge cases, including `list.pop()` with a shape-derived index, in-place ops on `__torch_function__` subclasses, activation checkpointing with dynamic shapes, `torch._C._infer_size`, nested `torch.compile` calls, and `torch.random.fork_rng` ([#196590](https://github.com/pytorch/pytorch/pull/196590), [#193969](https://github.com/pytorch/pytorch/pull/193969), [#193254](https://github.com/pytorch/pytorch/pull/193254), [#185471](https://github.com/pytorch/pytorch/pull/185471), [#185742](https://github.com/pytorch/pytorch/pull/185742), [#184793](https://github.com/pytorch/pytorch/pull/184793), [#195413](https://github.com/pytorch/pytorch/pull/195413), [#191977](https://github.com/pytorch/pytorch/pull/191977), [#184977](https://github.com/pytorch/pytorch/pull/184977), [#185373](https://github.com/pytorch/pytorch/pull/185373), [#185462](https://github.com/pytorch/pytorch/pull/185462), [#186168](https://github.com/pytorch/pytorch/pull/186168), [#196865](https://github.com/pytorch/pytorch/pull/196865), [#198330](https://github.com/pytorch/pytorch/pull/198330), [#197191](https://github.com/pytorch/pytorch/pull/197191), [#197745](https://github.com/pytorch/pytorch/pull/197745), [#198153](https://github.com/pytorch/pytorch/pull/198153), [#194749](https://github.com/pytorch/pytorch/pull/194749), [#197049](https://github.com/pytorch/pytorch/pull/197049), [#197585](https://github.com/pytorch/pytorch/pull/197585), [#185300](https://github.com/pytorch/pytorch/pull/185300), [#198060](https://github.com/pytorch/pytorch/pull/198060))
- Fix stable Triton TMA descriptors, value-opaque object methods, and nanobind-bound C++ methods under `torch.compile` ([#185469](https://github.com/pytorch/pytorch/pull/185469), [#188799](https://github.com/pytorch/pytorch/pull/188799), [#188632](https://github.com/pytorch/pytorch/pull/188632), [#194556](https://github.com/pytorch/pytorch/pull/194556))
- Fix a graph-breaking debug f-string (`f"{x=}"`) abandoning the whole frame ([#186500](https://github.com/pytorch/pytorch/pull/186500))
- Fix thread-safety issues on Python 3.14 and free-threaded builds, and eval-frame state such as `set_stance(skip_guard_eval_unsafe=True)` leaking between threads ([#191281](https://github.com/pytorch/pytorch/pull/191281), [#199210](https://github.com/pytorch/pytorch/pull/199210), [#196637](https://github.com/pytorch/pytorch/pull/196637))
- Match CPython behavior for builtin container subclasses, `dict_keys` views, `frozenset`, `deque` edge cases, `range.index`, `operator.length_hint`, and unbound numeric dunders ([#193679](https://github.com/pytorch/pytorch/pull/193679), [#193649](https://github.com/pytorch/pytorch/pull/193649), [#193580](https://github.com/pytorch/pytorch/pull/193580), [#197454](https://github.com/pytorch/pytorch/pull/197454), [#195010](https://github.com/pytorch/pytorch/pull/195010), [#195029](https://github.com/pytorch/pytorch/pull/195029), [#195030](https://github.com/pytorch/pytorch/pull/195030), [#196711](https://github.com/pytorch/pytorch/pull/196711), [#196901](https://github.com/pytorch/pytorch/pull/196901), [#198482](https://github.com/pytorch/pytorch/pull/198482), [#198604](https://github.com/pytorch/pytorch/pull/198604), [#198726](https://github.com/pytorch/pytorch/pull/198726))
- Match CPython exception types and messages for constant-folded ops, `except X as e` scoping, `getattr()` argument checks, `.index()`, and attribute errors ([#198590](https://github.com/pytorch/pytorch/pull/198590), [#198380](https://github.com/pytorch/pytorch/pull/198380), [#196526](https://github.com/pytorch/pytorch/pull/196526), [#197443](https://github.com/pytorch/pytorch/pull/197443), [#198476](https://github.com/pytorch/pytorch/pull/198476), [#198512](https://github.com/pytorch/pytorch/pull/198512), [#192509](https://github.com/pytorch/pytorch/pull/192509), [#196080](https://github.com/pytorch/pytorch/pull/196080), [#195496](https://github.com/pytorch/pytorch/pull/195496))
- Fix minifier repros for non-UTF-8 output, symbolic shapes, FP64 softmax and `is_inference`, and keep the original backend failure ([#186546](https://github.com/pytorch/pytorch/pull/186546), [#196620](https://github.com/pytorch/pytorch/pull/196620), [#194827](https://github.com/pytorch/pytorch/pull/194827), [#194595](https://github.com/pytorch/pytorch/pull/194595), [#193565](https://github.com/pytorch/pytorch/pull/193565))
- Fix precompile and `aot_compile` artifacts: pruned interned values such as `torch.float32` failing on load (`argument 'dtype' must be torch.dtype, not _Missing`), one unserializable compile discarding others, and global-name collisions ([#197749](https://github.com/pytorch/pytorch/pull/197749), [#196505](https://github.com/pytorch/pytorch/pull/196505), [#196756](https://github.com/pytorch/pytorch/pull/196756), [#196895](https://github.com/pytorch/pytorch/pull/196895), [#196822](https://github.com/pytorch/pytorch/pull/196822), [#196814](https://github.com/pytorch/pytorch/pull/196814))
### performance
- Reduce per-call overhead of compiled code and helpers like `assert_size_stride` ([#190623](https://github.com/pytorch/pytorch/pull/190623), [#195951](https://github.com/pytorch/pytorch/pull/195951), [#198019](https://github.com/pytorch/pytorch/pull/198019), [#196771](https://github.com/pytorch/pytorch/pull/196771), [#197451](https://github.com/pytorch/pytorch/pull/197451), [#197733](https://github.com/pytorch/pytorch/pull/197733))
- Reduce compile time: defer gen-2 GC while compiling (4.2s on one model; see `gc_gen2_threshold_during_compile`), skip empty graphs, and speed up large functions ([#193289](https://github.com/pytorch/pytorch/pull/193289), [#193157](https://github.com/pytorch/pytorch/pull/193157), [#195622](https://github.com/pytorch/pytorch/pull/195622), [#193416](https://github.com/pytorch/pytorch/pull/193416))
### docs
- Remove references to the obsolete `dynamic_shapes` config ([#198707](https://github.com/pytorch/pytorch/pull/198707))
- Fix the PGO config example in the dynamic shapes docs ([#191027](https://github.com/pytorch/pytorch/pull/191027))
- Document more `torch._logging.set_logs` options ([#188138](https://github.com/pytorch/pytorch/pull/188138))
### devs
### not user facing
- [dynamo] Migrate list-family VariableTrackers to tp_methods ([#189429](https://github.com/pytorch/pytorch/pull/189429))
- [dynamo] Migrate dict-family VariableTrackers to tp_methods ([#189431](https://github.com/pytorch/pytorch/pull/189431))
- [dynamo] Split TupleIteratorVariable off ListIteratorVariable to match CPython ([#193717](https://github.com/pytorch/pytorch/pull/193717))
- [dynamo] Split DequeReverseIteratorVariable off DequeIteratorVariable to match CPython ([#194348](https://github.com/pytorch/pytorch/pull/194348))
- Model readonly members by making `setter`a required arg in `Member` ([#193983](https://github.com/pytorch/pytorch/pull/193983))
- Introduce DescriptorVariable ([#194107](https://github.com/pytorch/pytorch/pull/194107))
- [dynamo] Add composite mutation type for builtin-container subclasses ([#193420](https://github.com/pytorch/pytorch/pull/193420))
- Enable `__hash__` in slotdefs ([#195762](https://github.com/pytorch/pytorch/pull/195762))
- Introduce `tp_descr_set_impl` to VariableTracker ([#194108](https://github.com/pytorch/pytorch/pull/194108))
- add tp_descr_get_impl fallback ([#194410](https://github.com/pytorch/pytorch/pull/194410))
- Expose getset `__class__` in UserDefinedObjectVariable tp_getset ([#195856](https://github.com/pytorch/pytorch/pull/195856))
- Use `istype` in `unpack_iterable` / `lazily_unpack` ([#193672](https://github.com/pytorch/pytorch/pull/193672))
- [dynamo][Ez] Unify `raise_observed_exception(TypeError, ...)` to `raise_type_error` ([#197082](https://github.com/pytorch/pytorch/pull/197082))
- [Testcase Refactoring] Add hw_classification to cpython test files ([#191832](https://github.com/pytorch/pytorch/pull/191832))
- [dynamo] Type the opaque `.value` a VariableTracker wraps as object instead of Any ([#192873](https://github.com/pytorch/pytorch/pull/192873))
- [dynamo] Type opaque global and FunctionType values as object ([#193425](https://github.com/pytorch/pytorch/pull/193425))
- [dynamo] Restore tp_getset/tp_members migration in variables/misc.py ([#193587](https://github.com/pytorch/pytorch/pull/193587))
- [dynamo] Split DequeIteratorVariable off ListIteratorVariable to match CPython ([#193261](https://github.com/pytorch/pytorch/pull/193261))
- [dynamo] Type bytecode-constant tuples as tuple[object, ...] ([#193828](https://github.com/pytorch/pytorch/pull/193828))
- Implement mp_subscript / sq_concat / bool_impl for ConstantVariable ([#192825](https://github.com/pytorch/pytorch/pull/192825))
- Route MethodWrapperVariable.call_function to `slotdef.__call__` ([#192826](https://github.com/pytorch/pytorch/pull/192826))
- [Dynamo] Model __class__ in base tp_getset ([#191540](https://github.com/pytorch/pytorch/pull/191540))
- [dynamo] Replace three Any annotations in compiled_autograd/decorators ([#194086](https://github.com/pytorch/pytorch/pull/194086))
- [dynamo] Add offline sync check for test/cpython/v3_13 *.diff files (… ([#191767](https://github.com/pytorch/pytorch/pull/191767))
- [dynamo] Migrate DictBuiltinVariable.fromkeys to tp_methods ([#195181](https://github.com/pytorch/pytorch/pull/195181))
- [dynamo] Migrate AutogradEngineVariable methods ([#195175](https://github.com/pytorch/pytorch/pull/195175))
- [dynamo] Migrate OptimizerVariable methods to tp_methods ([#195173](https://github.com/pytorch/pytorch/pull/195173))
- [dynamo] Migrate AutogradFunctionContextVariable methods ([#195179](https://github.com/pytorch/pytorch/pull/195179))
- [dynamo] Migrate AutogradFunctionVariable methods ([#195180](https://github.com/pytorch/pytorch/pull/195180))
- [dynamo] Migrate ContextVarVariable methods to tp_methods ([#195167](https://github.com/pytorch/pytorch/pull/195167))
- [dynamo] Migrate FuncTorchInterpreterVariable methods to tp_methods ([#195171](https://github.com/pytorch/pytorch/pull/195171))
- [dynamo] Fix skipped compiled model is Dynamo benchmarks ([#195703](https://github.com/pytorch/pytorch/pull/195703))
- [dynamo] Migrate DispatchKeySetVariable methods to tp_methods ([#195168](https://github.com/pytorch/pytorch/pull/195168))
- [dynamo] Migrate NNModuleVariable methods to tp_methods ([#195193](https://github.com/pytorch/pytorch/pull/195193))
- [dynamo] Fix Dynamo Benchmarks: Stabilization iters counted in latency ([#196060](https://github.com/pytorch/pytorch/pull/196060))
- [dynamo] Type replay registries as object ([#196054](https://github.com/pytorch/pytorch/pull/196054))
- [dynamo][inductor] Type diagnostic payloads as object ([#196135](https://github.com/pytorch/pytorch/pull/196135))
- [dynamo] Type runtime predicate inputs as object ([#196175](https://github.com/pytorch/pytorch/pull/196175))
- [dynamo] Type value-builder ingress as object ([#196176](https://github.com/pytorch/pytorch/pull/196176))
- [Dynamo] Port CPython 3.13 dict view tests ([#196246](https://github.com/pytorch/pytorch/pull/196246))
- [Dynamo] Port CPython 3.13 test_pow to Dynamo test suite ([#196259](https://github.com/pytorch/pytorch/pull/196259))
- [Dynamo] Port CPython 3.13 test_hash to Dynamo test suite ([#196283](https://github.com/pytorch/pytorch/pull/196283))
- [dynamo] Port CPython 3.13 test_userstring tests ([#196306](https://github.com/pytorch/pytorch/pull/196306))
- [dynamo] Port CPython 3.13 test_compare to Dynamo ([#196304](https://github.com/pytorch/pytorch/pull/196304))
- [dynamo] Port CPython 3.13 test_positional_only_arg to Dynamo ([#196316](https://github.com/pytorch/pytorch/pull/196316))
- [dynamo] Port CPython 3.13 test_string to Dynamo ([#196317](https://github.com/pytorch/pytorch/pull/196317))
- [typing] Tighten Triton HOP value annotations ([#196328](https://github.com/pytorch/pytorch/pull/196328))
- [dynamo] Fix Dynamo Benchmark: Eager Deepcopy Inflating Memory Compression ([#196178](https://github.com/pytorch/pytorch/pull/196178))
- [dynamo] Port CPython 3.13 test_genericclass to Dynamo ([#196329](https://github.com/pytorch/pytorch/pull/196329))
- [Dynamo] Port CPython 3.13 test_bisect to Dynamo test suite ([#196294](https://github.com/pytorch/pytorch/pull/196294))
- [dynamo] Type source keys and region hashes as object ([#196370](https://github.com/pytorch/pytorch/pull/196370))
- [dynamo] Port CPython 3.13 test_long to Dynamo test suite ([#196436](https://github.com/pytorch/pytorch/pull/196436))
- [dynamo] Port CPython 3.13 test_yield_from to Dynamo test suite ([#196408](https://github.com/pytorch/pytorch/pull/196408))
- [dynamo] Type metrics storage as object ([#196458](https://github.com/pytorch/pytorch/pull/196458))
- [Dynamo] Port CPython 3.13 test_copy to Dynamo test suite ([#196456](https://github.com/pytorch/pytorch/pull/196456))
- [dynamo] Port CPython 3.13 test_abc to Dynamo ([#196373](https://github.com/pytorch/pytorch/pull/196373))
- [Dynamo] Port CPython 3.13 test_grammar to Dynamo test suite ([#196482](https://github.com/pytorch/pytorch/pull/196482))
- [dynamo][benchmarks] Add synthetic DiT compile-time benchmark for nested compile regions ([#196380](https://github.com/pytorch/pytorch/pull/196380))
- [dynamo][benchmarks] Fix FSDP policy imports and clean up diffusion benchmarks ([#195909](https://github.com/pytorch/pytorch/pull/195909))
- [dynamo] Port CPython 3.13 test_unary to Dynamo test suite ([#196240](https://github.com/pytorch/pytorch/pull/196240))
- [dynamo] Port CPython 3.13 test_listcomps to Dynamo test suite ([#196518](https://github.com/pytorch/pytorch/pull/196518))
- [dynamo] Explicitly enable input normalization in cache test ([#196540](https://github.com/pytorch/pytorch/pull/196540))
- [dynamo] Extract FunctionPicklerBase from GuardsStatePickler ([#196471](https://github.com/pytorch/pytorch/pull/196471))
- [dynamo] Share the by-reference resolution test as FunctionPicklerBase._fqn_resolves ([#196683](https://github.com/pytorch/pytorch/pull/196683))
- [dynamo] Probe a bound method's function name inside the reducer's try, pin the dict-served case ([#196764](https://github.com/pytorch/pytorch/pull/196764))
- [dynamo] Prebuild pybind enum fixture in fbcode (#196545) ([#196545](https://github.com/pytorch/pytorch/pull/196545))
- [dynamo] Decide the verbatim tuple on its recording, keep builtins out of snapshots, guard the 3.14 annotation read ([#196767](https://github.com/pytorch/pytorch/pull/196767))
- [dynamo] Migrate SymNodeVariable methods to tp_methods ([#195189](https://github.com/pytorch/pytorch/pull/195189))
- [dynamo] Port CPython test_enumerate ([#196587](https://github.com/pytorch/pytorch/pull/196587))
- [dynamo] Port CPython 3.13 test_call to Dynamo test suite ([#196564](https://github.com/pytorch/pytorch/pull/196564))
- [aot_compile] Decide a module dispatch call's shared binding at the second scanned result ([#197133](https://github.com/pytorch/pytorch/pull/197133))
- [dynamo] Restore autocast state between tests in TestCase ([#195662](https://github.com/pytorch/pytorch/pull/195662))
- [Dynamo] Port CPython 3.13 test_str to Dynamo test suite ([#196498](https://github.com/pytorch/pytorch/pull/196498))
- flex_gemm: raise on compiled backward, guard kernel_options keys ([#196320](https://github.com/pytorch/pytorch/pull/196320))
- [dynamo] Split UserMethodVariable off UserFunctionVariable to match CPython ([#193593](https://github.com/pytorch/pytorch/pull/193593))
- Include epilogue guards in Dynamo code_parts ([#186222](https://github.com/pytorch/pytorch/pull/186222))
- [dynamo] Split OrderedSetVariable off SetVariable to match CPython ([#196167](https://github.com/pytorch/pytorch/pull/196167))
- [dynamo] Port CPython 3.13 test_fractions to Dynamo test suite ([#197379](https://github.com/pytorch/pytorch/pull/197379))
- [dynamo] Port CPython 3.13 test_fstring to Dynamo test suite ([#196566](https://github.com/pytorch/pytorch/pull/196566))
- [aot_compile] Bind the certified globals at load on every live-scope path, drop bytecode_reads_guard_scope ([#196909](https://github.com/pytorch/pytorch/pull/196909))
- [precompile] Start torch/_dynamo/precompile_package.py with the default guard filter ([#197261](https://github.com/pytorch/pytorch/pull/197261))
- [dynamo] Read guards-state bytes through load_guards_state in the serialization tests ([#197748](https://github.com/pytorch/pytorch/pull/197748))
- [dynamo] Move the _Missing sentinel from guards.py to package.py ([#197751](https://github.com/pytorch/pytorch/pull/197751))
- [dynamo] Memoize import_source per translator with an explicit dict ([#197746](https://github.com/pytorch/pytorch/pull/197746))
- [dynamo] Load guards state through an unpickler that maps the pruned persistent id to _Missing ([#197817](https://github.com/pytorch/pytorch/pull/197817))
- [dynamo] Pin that persistent_id pruning leaves a loaded nn.Module's bookkeeping alone ([#197819](https://github.com/pytorch/pytorch/pull/197819))
- [precompile] Locate the stdlib, install and torch roots for the module-ownership lint (#197262) ([#197961](https://github.com/pytorch/pytorch/pull/197961))
- [precompile] Name the guard bindings that cannot be repointed by configuration (#197263) ([#197962](https://github.com/pytorch/pytorch/pull/197962))
- [precompile] Classify a module file as stdlib, install-dir or torch by its resolved path (#197428) ([#197963](https://github.com/pytorch/pytorch/pull/197963))
- [precompile] Decide library ownership by where a module resolves, not by its name (#197264) ([#197965](https://github.com/pytorch/pytorch/pull/197965))
- [precompile] Recognise the trusted module namespaces an attribute guard hangs off (#197265) ([#197967](https://github.com/pytorch/pytorch/pull/197967))
- [precompile] Classify the guard types that are never dropped and never compared (#197267) ([#197968](https://github.com/pytorch/pytorch/pull/197968))
- [precompile] Complete the guard-type classification and pin it with a totality test (#197268) ([#197969](https://github.com/pytorch/pytorch/pull/197969))
- [precompile] Normalize addresses and per-process counters out of rendered guard code (#197269) ([#197970](https://github.com/pytorch/pytorch/pull/197970))
- [precompile] Fingerprint code objects and callables by content for the guard report (#197270) ([#197971](https://github.com/pytorch/pytorch/pull/197971))
- [precompile] Add _is_risky_drop, the lint over identity guards serialization dropped (#197266) ([#197972](https://github.com/pytorch/pytorch/pull/197972))
- [precompile] Fingerprint what a guard checks when its rendered code does not say (#197271) ([#197973](https://github.com/pytorch/pytorch/pull/197973))
- [precompile] Report the value-pinned sources no captured variant will generalize (#197272) ([#197974](https://github.com/pytorch/pytorch/pull/197974))
- [precompile] Add _varying_guard_slots and the PrecompileSummary builder (#197273) ([#197975](https://github.com/pytorch/pytorch/pull/197975))
- [precompile] Add _capture_config, the compiler configuration a capture runs under (#197274) ([#197976](https://github.com/pytorch/pytorch/pull/197976))
- [precompile] Add the frame converter that compiles package frames with allow_empty_graphs (#197275) ([#197977](https://github.com/pytorch/pytorch/pull/197977))
- [precompile] Refuse a DDPOptimizer frame by name when the package's converter is asked to clone (#197721) ([#197978](https://github.com/pytorch/pytorch/pull/197978))
- [dynamo, 3.15] Update some error messages ([#198018](https://github.com/pytorch/pytorch/pull/198018))
- [dynamo] Cut 22% off the runtime of the three slowest dynamo test files ([#198030](https://github.com/pytorch/pytorch/pull/198030))
- Fix two log messages that print a literal %s ([#198244](https://github.com/pytorch/pytorch/pull/198244))
- [Dynamo] Port CPython 3.13 test_fnmatch ([#197389](https://github.com/pytorch/pytorch/pull/197389))
- Increase small tensor tolerance for functorch_dp_cifar10 ([#198210](https://github.com/pytorch/pytorch/pull/198210))
- [Dynamo] Clean up global state leaks in test/dynamo ([#191931](https://github.com/pytorch/pytorch/pull/191931))
- [dynamo] Lower the backward eagerly under the multi-graph capture config ([#198215](https://github.com/pytorch/pytorch/pull/198215))
- [dynamo] Fix deque.remove raising deque.pop() TypeError under compile ([#198716](https://github.com/pytorch/pytorch/pull/198716))
- [Dynamo][Benchmarks] Add Qwen3.5-0.8B to Hugging Face benchmarks ([#198261](https://github.com/pytorch/pytorch/pull/198261))
- [dynamo] Add PrecompileSession, the caller-driven multi-graph capture ([#198137](https://github.com/pytorch/pytorch/pull/198137))
- [dynamo] Migrate AutogradFunctionVariable.apply attribute access to t… ([#197828](https://github.com/pytorch/pytorch/pull/197828))
- [dynamo] Fix flaky CPython test_fnmatch FilterTestCase tests ([#199193](https://github.com/pytorch/pytorch/pull/199193))
- [dynamo] Speed up test_tp_richcompare.py ([#199238](https://github.com/pytorch/pytorch/pull/199238))
- [dynamo][python3.14] Skip the two C-pickler-overflow aot_compile tests on fbcode 3.14 (#199531) ([#199531](https://github.com/pytorch/pytorch/pull/199531))
- [dynamo] Port CPython 3.13 test_graphlib to Dynamo ([#197253](https://github.com/pytorch/pytorch/pull/197253))
- Bind arguments once per call in `aot_compile` module dispatch when compiled results bind alike ([#197071](https://github.com/pytorch/pytorch/pull/197071)) (cut for length)
### security
