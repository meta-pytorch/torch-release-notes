
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
- Add `torch.compiler.config.static_sources` (environment variable `TORCH_COMPILE_STATIC_SOURCES`), the inverse of `dynamic_sources`: it lists sources (exact names, regexes, or `:N` per-dim suffixes) that should stay static. Listed sources override automatic dynamic shapes, PGO, `dynamic=True`, `dynamic_sources`, and `unbacked_sources`, but not an explicit `torch._dynamo.mark_dynamic`. Use it when automatic dynamism produces a worse kernel or unwanted guards, e.g. `with torch.compiler.config.patch(static_sources="L['x']"): ...` ([#193626](https://github.com/pytorch/pytorch/pull/193626))
- Custom backends can define a `_dynamo_backend_init` no-argument callable that runs when `torch.compile()` resolves the backend, before the first graph is captured. Out-of-tree backends can use it to load native libraries or set up device contexts so that `torch.compile()` fails fast on a broken environment, without monkeypatching Dynamo. It works for backends passed directly, registered with `register_backend`, or forced via `torch.compiler.set_stance(force_backend=...)` ([#192345](https://github.com/pytorch/pytorch/pull/192345))
### improvements
- Support `bytearray` inside compiled regions: construction, read-only operations, `hex()`, and `decode()` ([#192205](https://github.com/pytorch/pytorch/pull/192205), [#199252](https://github.com/pytorch/pytorch/pull/199252))
- Support `types.SimpleNamespace` ([#193719](https://github.com/pytorch/pytorch/pull/193719))
- Support `bytes()` with no arguments and constant-fold `bytes(...)` with constant arguments ([#196103](https://github.com/pytorch/pytorch/pull/196103), [#197499](https://github.com/pytorch/pytorch/pull/197499))
- Support calling `classmethod(...)` and `staticmethod(...)`, list subclasses that override `__new__`, and `del` of a variable captured by a nested function ([#197781](https://github.com/pytorch/pytorch/pull/197781), [#191512](https://github.com/pytorch/pytorch/pull/191512), [#189216](https://github.com/pytorch/pytorch/pull/189216))
- Extend `math` coverage: `ceil`/`floor`/`trunc`, `atan2`/`copysign`/`remainder`, and `gcd`/`lcm` on user-defined numeric objects, `sumprod` with non-constant arguments, and more `math`/`cmath` C functions captured in graph ([#196867](https://github.com/pytorch/pytorch/pull/196867), [#197498](https://github.com/pytorch/pytorch/pull/197498), [#197222](https://github.com/pytorch/pytorch/pull/197222), [#198685](https://github.com/pytorch/pytorch/pull/198685), [#195999](https://github.com/pytorch/pytorch/pull/195999))
- Add polyfills for more of the `operator` module, `heapq` (so `collections.Counter.most_common` traces), and constant-fold `float.from_number` / `int.from_number`; bad `collections.deque()` arguments and instantiating non-instantiable types now raise a catchable `TypeError` ([#192942](https://github.com/pytorch/pytorch/pull/192942), [#192834](https://github.com/pytorch/pytorch/pull/192834), [#195765](https://github.com/pytorch/pytorch/pull/195765))
- Improve exception support: `is`/`is not` between exception objects, `delattr` on exception attributes, user exception classes whose `__init__` calls `super().__init__(msg)`, and non-string `assert` messages such as `assert cond, (3,)` ([#191404](https://github.com/pytorch/pytorch/pull/191404), [#196722](https://github.com/pytorch/pytorch/pull/196722), [#196051](https://github.com/pytorch/pytorch/pull/196051), [#197798](https://github.com/pytorch/pytorch/pull/197798))
- Improve descriptor and object-model fidelity: `property` attributes (`fget`, `fset`, `fdel`, `__doc__`, `__name__`), `types.DynamicClassAttribute` created inside a compiled class body, and rich comparison of closure cells ([#194642](https://github.com/pytorch/pytorch/pull/194642), [#199260](https://github.com/pytorch/pytorch/pull/199260), [#197189](https://github.com/pytorch/pytorch/pull/197189))
- Raise the real Python exception (e.g. `TypeError`) for user errors detected while tracing instead of graph breaking ([#196432](https://github.com/pytorch/pytorch/pull/196432))
- Support setting `tensor.requires_grad = True` on tensors created inside the compiled region ([#191129](https://github.com/pytorch/pytorch/pull/191129))
- `Tensor.storage_offset()` on an input tensor now returns a guarded Python `int` under `fullgraph=True` instead of failing ([#197224](https://github.com/pytorch/pytorch/pull/197224))
- Constant-fold `Tensor.is_pinned()` on non-CPU tensors, and the `__name__`, `__qualname__`, `__module__`, and `__doc__` of torch builtin functions (e.g. inside `__torch_function__`), instead of graph breaking ([#186494](https://github.com/pytorch/pytorch/pull/186494), [#196049](https://github.com/pytorch/pytorch/pull/196049))
- `hasattr(obj, name)` and `getattr(obj, name, default)` on opaque objects such as `ProcessGroup` now trace, raising `AttributeError` for missing members as in eager ([#196050](https://github.com/pytorch/pytorch/pull/196050))
- Resolve attribute reads on `torch.autograd.Function` subclasses (e.g. inspecting `setup_context`) instead of graph breaking ([#185316](https://github.com/pytorch/pytorch/pull/185316))
- Support `setattr` on tensors returned inside tuples/lists, e.g. the outputs of `torch.split` ([#198514](https://github.com/pytorch/pytorch/pull/198514))
- Trace `torch._dynamo.utils.is_compile_supported`, removing graph breaks in newer torchvision `roi_align` ([#185528](https://github.com/pytorch/pytorch/pull/185528))
- When `allow_rnn` is disabled, the graph break for `nn.RNN`/`nn.GRU`/`nn.LSTM` now happens at the module call, so the rest of the frame keeps compiling ([#186614](https://github.com/pytorch/pytorch/pull/186614))
- Avoid recompiles when bitwise, comparison, unary, or builtin (`len`, `str`, `bool`, `min`, `max`) operations are applied to constant inputs whose result is unused ([#191143](https://github.com/pytorch/pytorch/pull/191143), [#191144](https://github.com/pytorch/pytorch/pull/191144), [#191145](https://github.com/pytorch/pytorch/pull/191145))
- Better out-of-tree accelerator support: Stream/Event classes from registered `DeviceInterface`s and legacy tensor classes of a renamed PrivateUse1 module are captured in graph, cross-stream deallocation safety applies to every accelerator, and `torch.mtia` stream APIs are supported ([#194343](https://github.com/pytorch/pytorch/pull/194343), [#195432](https://github.com/pytorch/pytorch/pull/195432), [#197187](https://github.com/pytorch/pytorch/pull/197187), [#195649](https://github.com/pytorch/pytorch/pull/195649))
- `torch.compile(..., name=...)` is now forwarded to custom backends as `kwargs["name"]` (it was previously only passed to Inductor) ([#196229](https://github.com/pytorch/pytorch/pull/196229))
- Improve diagnostics: no `WARNING` spam for backend exceptions that fall back to eager, no misleading unsupported-builtin warning for `time` module clocks, carets in graph-break user stacks, a clearer `TORCHDYNAMO_VERBOSE=1` hint for backend failures, clearer recompile reasons for `SET_CONTAINS`/`DICT_CONTAINS` guard failures, the offending index and dynamic-shape guidance in `SymIntArrayRef` concrete-int errors, and an actionable error for legacy collectives called with `async_op=True` ([#185155](https://github.com/pytorch/pytorch/pull/185155), [#186249](https://github.com/pytorch/pytorch/pull/186249), [#185466](https://github.com/pytorch/pytorch/pull/185466), [#185419](https://github.com/pytorch/pytorch/pull/185419), [#197464](https://github.com/pytorch/pytorch/pull/197464), [#197450](https://github.com/pytorch/pytorch/pull/197450), [#186082](https://github.com/pytorch/pytorch/pull/186082), [#195691](https://github.com/pytorch/pytorch/pull/195691))
- `aot_compile` serialization handles more functions: helpers wrapped with `functools.wraps`, bound methods built with `types.MethodType`, closure cells, and nested helpers' `__dict__`, `__doc__`, annotations, and type parameters; unpicklable values that no guard reads are pruned instead of failing the save ([#196472](https://github.com/pytorch/pytorch/pull/196472), [#196473](https://github.com/pytorch/pytorch/pull/196473), [#196474](https://github.com/pytorch/pytorch/pull/196474), [#196476](https://github.com/pytorch/pytorch/pull/196476), [#196478](https://github.com/pytorch/pytorch/pull/196478), [#196479](https://github.com/pytorch/pytorch/pull/196479), [#196481](https://github.com/pytorch/pytorch/pull/196481), [#196684](https://github.com/pytorch/pytorch/pull/196684), [#196685](https://github.com/pytorch/pytorch/pull/196685), [#196686](https://github.com/pytorch/pytorch/pull/196686), [#196687](https://github.com/pytorch/pytorch/pull/196687), [#196691](https://github.com/pytorch/pytorch/pull/196691), [#196692](https://github.com/pytorch/pytorch/pull/196692), [#197750](https://github.com/pytorch/pytorch/pull/197750), [#197752](https://github.com/pytorch/pytorch/pull/197752), [#197754](https://github.com/pytorch/pytorch/pull/197754), [#197755](https://github.com/pytorch/pytorch/pull/197755), [#197833](https://github.com/pytorch/pytorch/pull/197833), [#197762](https://github.com/pytorch/pytorch/pull/197762))
- `torch.compiler.load_compiled_function(..., f_globals=...)` and loaded `aot_compile` modules now resolve kept global guards against the live scope (for modules, the scope of `model.forward`, including when it is wrapped by `torch.compile` or `torch._dynamo.disable`), and re-read a guarded global before every call instead of serving the load-time value. A kept guard on a global missing from `f_globals` now fails with `KeyError on G['NAME']` until the name is bound ([#196815](https://github.com/pytorch/pytorch/pull/196815), [#196817](https://github.com/pytorch/pytorch/pull/196817), [#196818](https://github.com/pytorch/pytorch/pull/196818), [#196908](https://github.com/pytorch/pytorch/pull/196908), [#196897](https://github.com/pytorch/pytorch/pull/196897), [#197218](https://github.com/pytorch/pytorch/pull/197218), [#196904](https://github.com/pytorch/pytorch/pull/196904))
- `aot_compile` module dispatch checks every compiled result before refusing a call, tolerates a guard tree that raises, and honors `disable_guard_check()` on any result ([#197055](https://github.com/pytorch/pytorch/pull/197055), [#196826](https://github.com/pytorch/pytorch/pull/196826), [#197047](https://github.com/pytorch/pytorch/pull/197047))
- Improve `aot_compile` diagnostics: when no compiled graph matches, raise a report naming every compiled input and why it was rejected; name the scope a missing guarded global was looked up in; suggest `external_data` when `serialize()` cannot pickle a value; warn when hooks registered on the model are dropped by module compilation, and when dispatch serves a graph while another result's guards raised; check the artifact format before unpickling so incompatible artifacts fail with a clear message; raise `PackageError` instead of internal errors for unpicklable guarded values ([#196823](https://github.com/pytorch/pytorch/pull/196823), [#197149](https://github.com/pytorch/pytorch/pull/197149), [#197048](https://github.com/pytorch/pytorch/pull/197048), [#197220](https://github.com/pytorch/pytorch/pull/197220), [#197050](https://github.com/pytorch/pytorch/pull/197050), [#197257](https://github.com/pytorch/pytorch/pull/197257), [#197319](https://github.com/pytorch/pytorch/pull/197319), [#196816](https://github.com/pytorch/pytorch/pull/196816), [#196693](https://github.com/pytorch/pytorch/pull/196693), [#196819](https://github.com/pytorch/pytorch/pull/196819), [#197391](https://github.com/pytorch/pytorch/pull/197391), [#198061](https://github.com/pytorch/pytorch/pull/198061), [#196470](https://github.com/pytorch/pytorch/pull/196470), [#197756](https://github.com/pytorch/pytorch/pull/197756))
- `torch._dynamo.maybe_mark_dynamic(t, dim, min=..., max=...)` now accepts an initial value range for the dimension. Unlike `mark_dynamic`, guards may still narrow the range and the dimension may still specialize. Passing only one of `min`/`max` to `mark_dynamic` or `maybe_mark_dynamic` no longer crashes with `AssertionError: not simple sympy type NoneType` ([#194625](https://github.com/pytorch/pytorch/pull/194625))
### bug fixes
- Fix guards treating `-0.0` and `0.0` as equal and rejecting `NaN` constants, which reused graphs with the wrong float baked in (wrong results for e.g. `copysign`, `atan2`, `1/x`) and blocked `nested_compile_region` reuse ([#192604](https://github.com/pytorch/pytorch/pull/192604), [#192608](https://github.com/pytorch/pytorch/pull/192608))
- Fix relational guards being skipped by the dict-version shortcut, which could let a real guard failure pass ([#185911](https://github.com/pytorch/pytorch/pull/185911))
- Guard autocast objects by value instead of identity, fixing unnecessary recompiles for an equivalent object and stale graphs when the same object is mutated ([#194754](https://github.com/pytorch/pytorch/pull/194754))
- Fix `isinstance(obj, A | B)` / `isinstance(obj, (A, B))` with `@runtime_checkable` Protocols silently returning `False` ([#196124](https://github.com/pytorch/pytorch/pull/196124))
- Fix silently wrong results from zero-argument `super()` in a classmethod resolving to a plain function, from user descriptors stored in a class's own `__dict__` (whose `__get__` ran repeatedly), and from closure-list mutations made by methods of locally defined classes; also support `contextlib.closing` ([#198435](https://github.com/pytorch/pytorch/pull/198435), [#198410](https://github.com/pytorch/pytorch/pull/198410), [#197830](https://github.com/pytorch/pytorch/pull/197830))
- Fix `random` module handling: draws from a `random.Random` input or module attribute returned stale values on cache hits, `random.seed()` did not affect scalar draws on the first compile, and float draws were traced as float32 instead of float64 (wrong values with Inductor on CPU) ([#196921](https://github.com/pytorch/pytorch/pull/196921), [#197221](https://github.com/pytorch/pytorch/pull/197221), [#199075](https://github.com/pytorch/pytorch/pull/199075))
- Fix `torch.Tensor(torch.Size([...]))` selecting the data overload instead of the size overload under `torch.compile` ([#196717](https://github.com/pytorch/pytorch/pull/196717))
- Fix autograd correctness: a custom `torch.autograd.Function` backward was dropped under `torch.func` transforms, a graph break at `torch.autograd.grad` could produce `None` or wrong gradients, shape-changing `Parameter.data` assignments (e.g. DeepSpeed ZeRO-3 hooks) now graph break instead of producing a wrong backward, and an optimizer's `capturable` flag is restored after tracing ([#193724](https://github.com/pytorch/pytorch/pull/193724), [#185829](https://github.com/pytorch/pytorch/pull/185829), [#186512](https://github.com/pytorch/pytorch/pull/186512), [#184704](https://github.com/pytorch/pytorch/pull/184704))
- Higher-order op bodies no longer allow input mutation or aliasing unless the op supports it. `flex_attention` `mask_mod` functions that mutate inputs or return aliases of captured tensors are now rejected (an error under `fullgraph=True`, otherwise a graph break with eager fallback), and `register_post_accumulate_grad_hook` on an intermediate tensor graph breaks without compiled autograd instead of miscompiling ([#185738](https://github.com/pytorch/pytorch/pull/185738))
- Fix `out=` variants of `torch.max`, `torch.min`, and `torch.topk` recompiling on every new input shape ([#187952](https://github.com/pytorch/pytorch/pull/187952))
- Fix memory leaks: tracked fake tensors kept CUDA tensors alive after compilation, observed exceptions pinned the Python stack until the next GC, and frames with higher-order ops (e.g. `flex_attention`, `torch.cond`) that read `__dict__` kept their inputs alive until `gc.collect()` (this also fixes a dropped attribute mutation) ([#193015](https://github.com/pytorch/pytorch/pull/193015), [#197567](https://github.com/pytorch/pytorch/pull/197567), [#195954](https://github.com/pytorch/pytorch/pull/195954))
- Fix crashes and internal errors: `list.pop()` with a shape-derived index under `dynamic=True`; in-place ops on `__torch_function__` tensor subclasses (missing `__subclass_Tensor_...` global); activation checkpointing with dynamic shapes and unspecialized floats such as `nn.RMSNorm.eps`; `torch._C._infer_size` (`expected a torch.Size as argument 1`, e.g. KL divergence of `MultivariateNormal`); `nonstrict_trace` with `None` leaves; recompile-reason reporting when a container of tensors becomes `None`; grad-mode-decorated methods on objects created in the region (`Unexpected type in sourceless builder`); `caching_precompile=True` with a decorated class; nested calls to `torch.compile`-decorated methods; `assume_constant_result` tensors across graph breaks; NumPy operators under a default-device context; `torch.random.fork_rng` with a set of devices; `setattr` on untracked user objects; `getattr` on builtin types with a missing attribute; `torch.compile` on an `nn.Module` from compiled autograd; a non-module `sys.modules` entry; exceptions whose args are not strings ([#196590](https://github.com/pytorch/pytorch/pull/196590), [#193969](https://github.com/pytorch/pytorch/pull/193969), [#193254](https://github.com/pytorch/pytorch/pull/193254), [#185471](https://github.com/pytorch/pytorch/pull/185471), [#185742](https://github.com/pytorch/pytorch/pull/185742), [#184793](https://github.com/pytorch/pytorch/pull/184793), [#195413](https://github.com/pytorch/pytorch/pull/195413), [#191977](https://github.com/pytorch/pytorch/pull/191977), [#184977](https://github.com/pytorch/pytorch/pull/184977), [#185373](https://github.com/pytorch/pytorch/pull/185373), [#185462](https://github.com/pytorch/pytorch/pull/185462), [#186168](https://github.com/pytorch/pytorch/pull/186168), [#196865](https://github.com/pytorch/pytorch/pull/196865), [#198330](https://github.com/pytorch/pytorch/pull/198330), [#197191](https://github.com/pytorch/pytorch/pull/197191), [#197745](https://github.com/pytorch/pytorch/pull/197745), [#198153](https://github.com/pytorch/pytorch/pull/198153))
- Fix a crash in an unrelated later compile after reading a tensor's `.grad` or `requires_grad`, and TorchFunction handling being left disabled on the calling thread after a guard raised (e.g. `TENSOR_MATCH` on a strided nested tensor) ([#194749](https://github.com/pytorch/pytorch/pull/194749), [#197049](https://github.com/pytorch/pytorch/pull/197049))
- Fix stable Triton TMA descriptor creation falling back to eager, method access on callable value-opaque objects, `@staticmethod` guards on value-opaque objects, and C++ methods bound with nanobind (e.g. upcoming Triton releases) failing under `torch.compile` ([#185469](https://github.com/pytorch/pytorch/pull/185469), [#188799](https://github.com/pytorch/pytorch/pull/188799), [#188632](https://github.com/pytorch/pytorch/pull/188632), [#194556](https://github.com/pytorch/pytorch/pull/194556))
- Fix a debug f-string such as `f"{x=}"` that graph breaks abandoning the whole frame instead of resuming after it ([#186500](https://github.com/pytorch/pytorch/pull/186500))
- Fix thread-safety issues: a dict-mutation race when a dataclass is defined in a compiled region on Python 3.14, cache-entry reordering on free-threaded builds causing spurious recompiles, and per-region eval-frame state leaking between threads running compiled functions (for example `set_stance(skip_guard_eval_unsafe=True)` in one thread turning off guard evaluation in others) ([#191281](https://github.com/pytorch/pytorch/pull/191281), [#199210](https://github.com/pytorch/pytorch/pull/199210), [#196637](https://github.com/pytorch/pytorch/pull/196637))
- Fix guards on `property` descriptors evaluating the getter, `make_fx` `_AttrProxy` module reuse, and a later frame-skip decision being ignored for code with a recorded per-region strategy ([#197585](https://github.com/pytorch/pytorch/pull/197585), [#185300](https://github.com/pytorch/pytorch/pull/185300), [#198060](https://github.com/pytorch/pytorch/pull/198060))
- Match CPython for builtin types and containers: subclasses of `list`, `dict`, `set`, `frozenset`, `tuple`, and `deque` (e.g. `copy()` identity on a `frozenset` subclass); `dict_keys` views passed into a compiled region; mutating methods on `frozenset` (`AttributeError` instead of an internal assertion); `list_reverseiterator` inputs; `collections.deque` `popleft()`/`pop()` on an empty deque, `maxlen=0`, `maxlen` with `*`, and `del d[i]`; `range.index` with custom equality; `operator.length_hint`; unbound `int`/`float`/`complex` dunders such as `float.__rsub__`; `__init__` returning a non-`None` value now raises `TypeError`; `property.__isabstractmethod__` raising in user code ([#193679](https://github.com/pytorch/pytorch/pull/193679), [#193649](https://github.com/pytorch/pytorch/pull/193649), [#193580](https://github.com/pytorch/pytorch/pull/193580), [#197454](https://github.com/pytorch/pytorch/pull/197454), [#195010](https://github.com/pytorch/pytorch/pull/195010), [#195029](https://github.com/pytorch/pytorch/pull/195029), [#195030](https://github.com/pytorch/pytorch/pull/195030), [#196711](https://github.com/pytorch/pytorch/pull/196711), [#196901](https://github.com/pytorch/pytorch/pull/196901), [#198482](https://github.com/pytorch/pytorch/pull/198482), [#198604](https://github.com/pytorch/pytorch/pull/198604), [#198726](https://github.com/pytorch/pytorch/pull/198726))
- Match CPython exception behavior and messages: exceptions raised by constant-folded operations keep their message (e.g. `"abc".index("z")`); reading an `except X as e` variable after the block raises `UnboundLocalError`; `getattr()` validates its arguments; `str(KeyError("k"))`, `repr()` of self-referential sets, `UserList`, and `UserDict`, `.index()` `ValueError`s on lists/tuples/deques, property `AttributeError`s, and read-only attribute errors now match eager ([#198590](https://github.com/pytorch/pytorch/pull/198590), [#198380](https://github.com/pytorch/pytorch/pull/198380), [#196526](https://github.com/pytorch/pytorch/pull/196526), [#197443](https://github.com/pytorch/pytorch/pull/197443), [#198476](https://github.com/pytorch/pytorch/pull/198476), [#198512](https://github.com/pytorch/pytorch/pull/198512), [#192509](https://github.com/pytorch/pytorch/pull/192509), [#196080](https://github.com/pytorch/pytorch/pull/196080), [#195496](https://github.com/pytorch/pytorch/pull/195496))
- Fix minifier repros: non-UTF-8 subprocess output crashing minification, symbolic shapes written as sympy instead of Python, FP64 softmax arguments, after-AOT repros dropping `is_inference`, and the minifier's own sanity-check error replacing the original backend failure ([#186546](https://github.com/pytorch/pytorch/pull/186546), [#196620](https://github.com/pytorch/pytorch/pull/196620), [#194827](https://github.com/pytorch/pytorch/pull/194827), [#194595](https://github.com/pytorch/pytorch/pull/194595), [#193565](https://github.com/pytorch/pytorch/pull/193565))
- Fix precompile and `aot_compile` artifacts: an interned value such as `torch.float32` being pruned (`empty_strided(): argument 'dtype' must be torch.dtype, not _Missing` on load); one unserializable compile discarding every other compile of the same code; bypassed cache entries growing on reload; uninstalling a package deleting globals it had only overwritten; global-name collisions with names seeded by a loaded package; and incorrect device-type detection for a graph ([#197749](https://github.com/pytorch/pytorch/pull/197749), [#196505](https://github.com/pytorch/pytorch/pull/196505), [#196756](https://github.com/pytorch/pytorch/pull/196756), [#196895](https://github.com/pytorch/pytorch/pull/196895), [#196822](https://github.com/pytorch/pytorch/pull/196822), [#196814](https://github.com/pytorch/pytorch/pull/196814))
### performance
- Reduce per-call overhead of compiled functions: emit the "Pregraph bytecode" profiler marker only when a profiler is active (about 10% of a trivial compiled call), get the current stream in C++, and trim the warm-cache path ([#190623](https://github.com/pytorch/pytorch/pull/190623), [#195951](https://github.com/pytorch/pytorch/pull/195951), [#198019](https://github.com/pytorch/pytorch/pull/198019), [#196771](https://github.com/pytorch/pytorch/pull/196771))
- Defer full (generation 2) garbage collections while compiling, which cut 4.2s of GC from one model's cold compile. This sets the process-wide gen2 threshold during compilation; tune or disable it with `torch._dynamo.config.gc_gen2_threshold_during_compile` / `TORCH_DYNAMO_GC_GEN2_THRESHOLD_DURING_COMPILE` (default 1000, `0` or `None` to disable; off on free-threaded builds) ([#193289](https://github.com/pytorch/pytorch/pull/193289))
- Reduce compile time: skip the backend for graphs that compute nothing, remove quadratic constant lookup when assembling bytecode for large functions, and avoid recomputing storage sizes for functional tensors ([#193157](https://github.com/pytorch/pytorch/pull/193157), [#195622](https://github.com/pytorch/pytorch/pull/195622), [#193416](https://github.com/pytorch/pytorch/pull/193416))
- Bind arguments once per call in `aot_compile` module dispatch when compiled results bind alike ([#197071](https://github.com/pytorch/pytorch/pull/197071))
- Speed up the C++ helpers that Inductor-generated code and guards call at runtime (such as `assert_size_stride`, `assert_alignment` and `_reinterpret_tensor`) by about 50%, and make Dynamo's `GenerationTracker` slightly faster ([#197451](https://github.com/pytorch/pytorch/pull/197451), [#197733](https://github.com/pytorch/pytorch/pull/197733))
### docs
- Remove references to the obsolete `dynamic_shapes` config option from docstrings ([#198707](https://github.com/pytorch/pytorch/pull/198707))
- Fix the profile-guided optimization (PGO) config example in the dynamic shapes docs, which crashed because `0`/`1` values are converted to booleans ([#191027](https://github.com/pytorch/pytorch/pull/191027))
- Document the `cudagraphs`, `compiled_autograd`, `compiled_autograd_verbose` and `compute_dependencies` options of `torch._logging.set_logs` ([#188138](https://github.com/pytorch/pytorch/pull/188138))
### devs
### not user facing
- Keep the device index of `torch.cuda.synchronize()` unresolved under the in-progress compile-on-one-rank mode, so the artifact is not rank-specific ([#196937](https://github.com/pytorch/pytorch/pull/196937))
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
### security
