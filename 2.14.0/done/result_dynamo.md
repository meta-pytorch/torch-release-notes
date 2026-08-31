
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
- The `tvm` backend now uses TVM's relax frontend exclusively; the relay path has been removed ([#190766](https://github.com/pytorch/pytorch/pull/190766), [#189639](https://github.com/pytorch/pytorch/pull/189639))

  Relay was removed in TVM 0.20, so the backend now requires a TVM providing `tvm.relax.frontend.torch`. Two things are gone with it: the relay-only `scheduler` / `trials` options, replaced by a TVM pipeline passed as `options={"pipeline": ...}`; and the `tvm_meta_schedule` / `tvm_auto_scheduler` backend entry points, which no longer exist in `torch._dynamo.backends.tvm`. With an older TVM installed, `torch.compile(..., backend="tvm")` now raises `ImportError: Please install apache-tvm to use the tvm backend.`

  Version 2.13:
  ```python
  opt = torch.compile(model, backend="tvm", options={"scheduler": "meta_schedule", "trials": 20000})

  # or through the relay-only entry points
  from torch._dynamo.backends.tvm import tvm_meta_schedule, tvm_auto_scheduler
  ```

  Version 2.14:
  ```python
  import tvm

  pipeline = tvm.relax.get_pipeline("static_shape_tuning", target="llvm", total_trials=2000)
  opt = torch.compile(model, backend="tvm", options={"pipeline": pipeline})

  # tvm_meta_schedule / tvm_auto_scheduler no longer exist:
  # ImportError: cannot import name 'tvm_meta_schedule'
  ```
- `next()` on a non-iterator now raises `TypeError` instead of silently returning the first element ([#190624](https://github.com/pytorch/pytorch/pull/190624))

  Dynamo's `next()` handling skipped CPython's iterator check and, for a list, returned its first item rather than raising. Compiled code that relied on this now sees the same `TypeError: 'list' object is not an iterator` that eager Python raises. Wrap the argument in `iter()` to keep the old result.

  Version 2.13:
  ```python
  >>> @torch.compile(fullgraph=True)
  ... def f(xs):
  ...     return next(xs)
  >>> f([1, 2, 3])
  1
  ```

  Version 2.14:
  ```python
  >>> f([1, 2, 3])
  TypeError: 'list' object is not an iterator

  >>> # workaround: match eager semantics explicitly
  >>> @torch.compile(fullgraph=True)
  ... def f(xs):
  ...     return next(iter(xs))
  >>> f([1, 2, 3])
  1
  ```
- `set()` and `frozenset()` now reject keyword arguments ([#189051](https://github.com/pytorch/pytorch/pull/189051))

  `set(a=1)` and `set().__init__(a=1)` silently produced an empty set inside a compiled region, because the keyword check ran only after a zero-positional-argument early return. Dynamo now raises `TypeError: set() takes no keyword arguments` (and the `frozenset()` equivalent), matching CPython. Such calls were already an error in eager, so drop the keyword arguments.

  Version 2.13:
  ```python
  >>> @torch.compile(fullgraph=True)
  ... def f():
  ...     return set(a=1)
  >>> f()
  set()
  ```

  Version 2.14:
  ```python
  >>> f()
  TypeError: set() takes no keyword arguments
  ```
### deprecation
- `torch._dynamo.config.enable_faithful_generator_behavior` is deprecated and is now a no-op ([#189894](https://github.com/pytorch/pytorch/pull/189894))

  Faithful (lazy) generator tracing has been the default and is the only supported behavior, so the dead eager-exhaustion path was removed. The config is kept as a deprecated setting that always behaves as `True`, so setting it does not error but no longer changes anything.

  Version 2.13:
  ```python
  # generators were eagerly exhausted on first execution
  with torch._dynamo.config.patch(enable_faithful_generator_behavior=False):
      torch.compile(fn)(x)
  ```

  Version 2.14:
  ```python
  # the flag is ignored; generators are always traced lazily
  torch.compile(fn)(x)
  ```
### new features
- Add `torch.compiler.nonstrict_trace` as a public API ([#187737](https://github.com/pytorch/pytorch/pull/187737))
- Add `switch`, a higher-order op that selects between N branches by index, mirroring `jax.lax.switch`. It is available as `from torch._higher_order_ops.switch import switch` and lowers to `torch.ops.higher_order.switch` ([#182902](https://github.com/pytorch/pytorch/pull/182902), [#188374](https://github.com/pytorch/pytorch/pull/188374), [#189028](https://github.com/pytorch/pytorch/pull/189028))
- Declare dynamic shapes explicitly with `ShapesSpec` / `ParamsSpec`, now accepted by strict and non-strict `torch.export.export`, `make_fx(tracing_mode="fake")`, and `torch.compile` through a shared `dynamic_shapes=` keyword ([#185982](https://github.com/pytorch/pytorch/pull/185982), [#186751](https://github.com/pytorch/pytorch/pull/186751), [#187602](https://github.com/pytorch/pytorch/pull/187602), [#187010](https://github.com/pytorch/pytorch/pull/187010))
- Support input mutation inside the `scan`, `map`, and `switch` higher-order ops ([#186474](https://github.com/pytorch/pytorch/pull/186474), [#187568](https://github.com/pytorch/pytorch/pull/187568), [#188903](https://github.com/pytorch/pytorch/pull/188903))
- Support `torch.cuda.use_mem_pool` inside a compiled region, so allocations in the context - including fallback and extern kernels - are routed to the pool ([#185057](https://github.com/pytorch/pytorch/pull/185057))
- Support `logging.Logger` methods as reorderable logging functions, so logging inside a compiled region runs after the compiled region instead of graph breaking ([#190840](https://github.com/pytorch/pytorch/pull/190840))
### improvements
- `torch.compiler.nested_compile_region` now reuses a traced region when its arguments contain source-backed user-defined objects, and only source-backed `nn.Module` arguments are accepted (previously sourceless modules were reused with no checking) ([#192003](https://github.com/pytorch/pytorch/pull/192003))
- `torch.compiler.nested_compile_region` reuse now applies to regions taking symbolic-shape inputs and to pytree arguments such as dataclasses and namedtuples, which previously retraced the region on every call ([#191806](https://github.com/pytorch/pytorch/pull/191806), [#191817](https://github.com/pytorch/pytorch/pull/191817))
- Support `torch.compile` applied directly to a `staticmethod` ([#190673](https://github.com/pytorch/pytorch/pull/190673))
- `Module.compile()` now compiles builtin leaf modules such as `Conv2d`, which previously produced no capturable frame ([#185722](https://github.com/pytorch/pytorch/pull/185722))
- Support cross-device `tensor.data = tensor.data.to(device)` under `torch.compile`, matching eager's metadata swap ([#185980](https://github.com/pytorch/pytorch/pull/185980))
- Trace raw unbacked `SymInt` inputs in non-strict tracing, preserving symbol provenance from an outer fake-tensor trace ([#187273](https://github.com/pytorch/pytorch/pull/187273))
- Support a scan dimension of length zero in `scan` and `associative_scan` ([#188348](https://github.com/pytorch/pytorch/pull/188348))
- Trace `torch._C.TensorBase` methods reached through `super()`, e.g. `super().unflatten(...)` ([#183850](https://github.com/pytorch/pytorch/pull/183850))
- Constant-fold the MPS and MTIA availability predicates and add trace rules for `torch.mps.is_available` / `torch.mtia.is_available`, so backend probes no longer graph break ([#185277](https://github.com/pytorch/pytorch/pull/185277))
- Return `[]` for `torch.utils._python_dispatch._get_current_dispatch_mode_stack()` instead of graph breaking ([#186574](https://github.com/pytorch/pytorch/pull/186574))
- Accept `out=` tensors in `channels_last` and `channels_last_3d` layouts instead of graph breaking ([#185089](https://github.com/pytorch/pytorch/pull/185089))
- Handle `DistributedDataParallel` in `SourcelessBuilder` ([#187210](https://github.com/pytorch/pytorch/pull/187210))
- Trace `dist.reduce_scatter` ([#190429](https://github.com/pytorch/pytorch/pull/190429))
- Support constructing `torch.backends.cuda.SDPAParams` under `fullgraph=True` ([#190839](https://github.com/pytorch/pytorch/pull/190839))
- Add a trace rule for `torch.linalg.polar` (and its Inductor lowering) so it can be captured ([#188537](https://github.com/pytorch/pytorch/pull/188537))
- `has_triton()` now queries the registered device interfaces, so out-of-tree accelerator backends are recognized without monkeypatching ([#190324](https://github.com/pytorch/pytorch/pull/190324))
- `torch._check` now accepts a module-level function or any constant as its message, matching eager ([#188576](https://github.com/pytorch/pytorch/pull/188576))
- Support `key=` and `default=` in `min()`/`max()`, the `base` argument of `int()`, and `oct()`/`hex()`/`bin()` on objects implementing `__index__` ([#191401](https://github.com/pytorch/pytorch/pull/191401), [#191402](https://github.com/pytorch/pytorch/pull/191402), [#191408](https://github.com/pytorch/pytorch/pull/191408))
- Apply `__index__` coercion to `range()` arguments and slice members, matching CPython ([#187129](https://github.com/pytorch/pytorch/pull/187129))
- Support constructing `object()`, empty `tuple` subclasses (`MyTuple()`), and `collections.deque` subclasses inside a compiled region ([#186976](https://github.com/pytorch/pytorch/pull/186976), [#189021](https://github.com/pytorch/pytorch/pull/189021), [#187588](https://github.com/pytorch/pytorch/pull/187588))
- Trace `list.sort` with non-constant key comparisons and `functools.cmp_to_key` ([#185999](https://github.com/pytorch/pytorch/pull/185999))
- `str.split`, `str.rsplit`, and `str.splitlines` now return a mutable list, so the result can be sorted or appended to inside a compiled region ([#188306](https://github.com/pytorch/pytorch/pull/188306))
- Support unbound rich-comparison dunders on builtin types, e.g. `complex.__eq__(1 + 1j, 2)` ([#191406](https://github.com/pytorch/pytorch/pull/191406))
- Support `operator.setitem` and `operator.delitem` on lists, dicts, tensors, and numpy arrays ([#190259](https://github.com/pytorch/pytorch/pull/190259))
- `callable()` now follows the type's `tp_call` slot, and calling a non-callable object raises `TypeError: 'X' object is not callable` instead of an internal error ([#186971](https://github.com/pytorch/pytorch/pull/186971))
- Extend `itertools` coverage: bounded `repeat`, `count(start=, step=)` and its `repr`, and support for `permutations`, `combinations`, `combinations_with_replacement`, and `batched` ([#188080](https://github.com/pytorch/pytorch/pull/188080), [#189022](https://github.com/pytorch/pytorch/pull/189022), [#186937](https://github.com/pytorch/pytorch/pull/186937), [#187080](https://github.com/pytorch/pytorch/pull/187080), [#186240](https://github.com/pytorch/pytorch/pull/186240))
- Support `__length_hint__` on set and dict-view iterators ([#188081](https://github.com/pytorch/pytorch/pull/188081))
- Improve `collections.deque` fidelity: re-initialization through `__init__`, `copy()` / `copy.copy()` preserving `maxlen`, `rotate()`, iterators that detect mutation during iteration, and `AttributeError` on attribute writes ([#187128](https://github.com/pytorch/pytorch/pull/187128), [#188220](https://github.com/pytorch/pytorch/pull/188220), [#191403](https://github.com/pytorch/pytorch/pull/191403), [#189052](https://github.com/pytorch/pytorch/pull/189052), [#191405](https://github.com/pytorch/pytorch/pull/191405))
- Support `range_iterator.__setstate__` / `__length_hint__`, and fall back to `==` comparison for non-integer operands of `x in range(...)` ([#188221](https://github.com/pytorch/pytorch/pull/188221), [#189575](https://github.com/pytorch/pytorch/pull/189575))
- Improve dict and set fidelity: do not re-hash keys when building from an existing dict/set, use per-element rich comparison for sequence membership, run a user-defined `__eq__` for dict/set key comparison, normalize `set.remove`/`set.discard` keys, read set subclasses through the base `set` APIs, and report the concrete set type from `hasattr` ([#186759](https://github.com/pytorch/pytorch/pull/186759), [#186760](https://github.com/pytorch/pytorch/pull/186760), [#186669](https://github.com/pytorch/pytorch/pull/186669), [#186761](https://github.com/pytorch/pytorch/pull/186761), [#186763](https://github.com/pytorch/pytorch/pull/186763), [#188908](https://github.com/pytorch/pytorch/pull/188908))
- Support the dict-view `.mapping` attribute, non-`str` keys assigned through an instance `__dict__`, CPython's clear-then-extend `list.__init__`, and CPython's `__dict__` re-insertion order after a `pop` ([#187586](https://github.com/pytorch/pytorch/pull/187586), [#187587](https://github.com/pytorch/pytorch/pull/187587), [#187583](https://github.com/pytorch/pytorch/pull/187583), [#187584](https://github.com/pytorch/pytorch/pull/187584))
- `str()` and `repr()` now follow CPython's `tp_str`/`tp_repr` fallbacks, including `repr()` of and integer arithmetic on the `id()`/`hash()` of an object created inside the compiled region ([#187775](https://github.com/pytorch/pytorch/pull/187775), [#188909](https://github.com/pytorch/pytorch/pull/188909), [#189053](https://github.com/pytorch/pytorch/pull/189053))
- Make the `object.__reduce_ex__` polyfill faithful for objects with `__slots__` or `__getnewargs__`, so `copy.copy`/`copy.deepcopy` of a namedtuple no longer graph breaks ([#189576](https://github.com/pytorch/pytorch/pull/189576))
- Support custom attributes on exceptions and exception-specific attributes such as `StopIteration.value`, `AttributeError.name`/`.obj`, and `NameError.name` ([#188105](https://github.com/pytorch/pytorch/pull/188105), [#189024](https://github.com/pytorch/pytorch/pull/189024))
- Support subgenerator `.throw()` / `.close()` and track generator attribute mutations for correct closure handling ([#188825](https://github.com/pytorch/pytorch/pull/188825), [#188834](https://github.com/pytorch/pytorch/pull/188834))
- Model the module-level `random.random` and `random.seed` through the traced RNG instead of graph breaking ([#188235](https://github.com/pytorch/pytorch/pull/188235), [#188083](https://github.com/pytorch/pytorch/pull/188083))
- Add a polyfill for `_io.text_encoding` so `open()`, `pathlib.Path.read_text()`/`write_text()`, and `tempfile.NamedTemporaryFile` no longer graph break under `fullgraph=True` ([#189984](https://github.com/pytorch/pytorch/pull/189984))
- Add the `**` / `**=`, `@` / `@=`, and `~` operator slots ([#186296](https://github.com/pytorch/pytorch/pull/186296), [#189585](https://github.com/pytorch/pytorch/pull/189585), [#185641](https://github.com/pytorch/pytorch/pull/185641))
- Improve diagnostics: dedicated graph-break messages for direct `torch._dynamo.disable`/`torch.compiler.disable` calls, clearer `Parameter`-vs-`Tensor` guard mismatch text in recompilation logs, an actionable hint for in-place views on graph inputs, closest-match suggestions for a mistyped backend name, graph breaks on exceptions based on whether user code would catch them, and observed-exception stacks preserved across a bare `raise` ([#185763](https://github.com/pytorch/pytorch/pull/185763), [#185083](https://github.com/pytorch/pytorch/pull/185083), [#185903](https://github.com/pytorch/pytorch/pull/185903), [#189333](https://github.com/pytorch/pytorch/pull/189333), [#182972](https://github.com/pytorch/pytorch/pull/182972), [#185508](https://github.com/pytorch/pytorch/pull/185508))
- Support TVM's relax frontend in the `tvm` backend, with tuning selected via `options={"pipeline": ...}` ([#189010](https://github.com/pytorch/pytorch/pull/189010), [#189638](https://github.com/pytorch/pytorch/pull/189638))
### bug fixes
- Ensure `torch._dynamo.reset()` clears stale precompiled package entries by registering installed `target_code` with the package input tracker ([#189206](https://github.com/pytorch/pytorch/pull/189206))
- Preserve registered third-party backend configuration and extra Triton imports in generated minifier reproductions ([#187855](https://github.com/pytorch/pytorch/pull/187855))
- Fix `torch.compiler.nested_compile_region` reuse across regions that read a global rebound between calls, which reused a stale graph ([#192006](https://github.com/pytorch/pytorch/pull/192006))
- Fix autograd through a `torch.compiler.nested_compile_region` executed in eager mode, which entered the fake-tensor AOTAutograd backward path instead of recording through the region ([#184700](https://github.com/pytorch/pytorch/pull/184700))
- Emit a `torch.compiler.nested_compile_region` call as a single graph node instead of graph breaking, as its documentation states ([#186137](https://github.com/pytorch/pytorch/pull/186137))
- Fix `torch.compiler.nested_compile_region` on transposed views of captured buffers (`x @ self.w.T`), which failed with `Freevar has no source` ([#191785](https://github.com/pytorch/pytorch/pull/191785))
- Fix nested graph break handling: reconstruction of exhausted generators and of empty `nn.Module` hook dictionaries, a crash in `mark_static_input` for non-tensor variables, a graph break inside a context manager's `__init__` falling the whole frame back to eager, a custom op defined and `register_fake`'d inside the traced function, a graph-break naming error in list comprehensions on Python < 3.12, and a `compile_subgraph` failure swallowed while formatting an f-string ([#188622](https://github.com/pytorch/pytorch/pull/188622), [#191388](https://github.com/pytorch/pytorch/pull/191388), [#187088](https://github.com/pytorch/pytorch/pull/187088), [#191264](https://github.com/pytorch/pytorch/pull/191264), [#191523](https://github.com/pytorch/pytorch/pull/191523), [#189601](https://github.com/pytorch/pytorch/pull/189601), [#187005](https://github.com/pytorch/pytorch/pull/187005), [#187701](https://github.com/pytorch/pytorch/pull/187701), [#188861](https://github.com/pytorch/pytorch/pull/188861))
- Reject `Tensor` values in tensor subclass metadata before installing the default metadata guard, avoiding an ambiguous-bool failure ([#184684](https://github.com/pytorch/pytorch/pull/184684))
- Fix `eager_then_compile` when a later compile sees a higher-rank input ([#184689](https://github.com/pytorch/pytorch/pull/184689))
- Fix a flaky `NameError: name '__compiled_fn_N_...' is not defined` when `CompilePackage.install()` reuses a global name after `torch._dynamo.reset()` ([#191128](https://github.com/pytorch/pytorch/pull/191128))
- Fix `torch._dynamo.reset()` leaving the process-global fake tensor dispatch cache populated, which could make a compile that failed cold pass on an in-process retry ([#191418](https://github.com/pytorch/pytorch/pull/191418))
- Fix precompile guard serialization for transparent tensor subclasses such as `AsyncCollectiveTensor` ([#190576](https://github.com/pytorch/pytorch/pull/190576))
- Fix AOT guard serialization for functions using `torch.func` transforms (`vmap`/`grad`/`jvp`) ([#191428](https://github.com/pytorch/pytorch/pull/191428))
- Serialize the guard-build dispatch TLS state so a precompile artifact loaded outside autocast does not force a recompile when the compiled function runs under autocast ([#184850](https://github.com/pytorch/pytorch/pull/184850))
- Fix precompile guard-state load at decoration time, which raised `TracingContext.get() must be called within an ongoing trace` ([#187736](https://github.com/pytorch/pytorch/pull/187736))
- Reinstall the compiled-function globals required by guarded bytecode on a warm precompile package load ([#184562](https://github.com/pytorch/pytorch/pull/184562))
- Skip storage memo for wrapper subclasses in `MetaConverter`, fixing `RuntimeError: Attempted to set the storage of a tensor on device "cuda:0" to a storage on different device "meta"` when a `_make_wrapper_subclass` tensor is a non-batched `torch.vmap` input inside `torch.compile` ([#176977](https://github.com/pytorch/pytorch/pull/176977))
- Fix class definitions inside a compiled region that close over a non-constant object, which raised `Invalid call to __build_class__` ([#185998](https://github.com/pytorch/pytorch/pull/185998))
- Use symbolic scalar extraction for 0-d integral tensor indices, so indexing a tensor with a scalar tensor stays on the `select` path under `torch.export` ([#184625](https://github.com/pytorch/pytorch/pull/184625))
- Fix globals modeling for functions whose globals dict is not owned by a registered module ([#184653](https://github.com/pytorch/pytorch/pull/184653))
- Fix `hasattr` on user objects so tracing does not materialize an existing `RemovableHandle` stored by conditional hook registration ([#184712](https://github.com/pytorch/pytorch/pull/184712))
- Run `torch.compile` wrappers eagerly when re-entered from compiler-internal fake or functional tracing, fixing fake-mode mismatch and fake tensor data pointer errors from tensor subclass hooks ([#185732](https://github.com/pytorch/pytorch/pull/185732))
- Graph break instead of silently dropping the tangent when a forward-AD dual tensor is passed into a compiled function; `fullgraph=True` now raises a clear error ([#189644](https://github.com/pytorch/pytorch/pull/189644))
- Fix `InternalTorchDynamoError` when traced code reads an attribute off `torch.compile(obj.meth)` ([#190185](https://github.com/pytorch/pytorch/pull/190185))
- Frame skips caused by an active `TorchDispatchMode` are no longer permanent for that code object ([#190287](https://github.com/pytorch/pytorch/pull/190287))
- Propagate the `override_cudagraphs` annotation to callees compiled as separate frames ([#188610](https://github.com/pytorch/pytorch/pull/188610))
- Fix lazy module initialization when the fake inputs carry symbolic shapes, e.g. in a resume function after a graph break ([#188595](https://github.com/pytorch/pytorch/pull/188595))
- Clear the weakrefs left by discarded tracing attempts so `torch.utils.swap_tensors` works on a live compiled module's parameters ([#190951](https://github.com/pytorch/pytorch/pull/190951))
- Fix graph-output replay of value-opaque objects that are also used as tensor subclass metadata ([#187057](https://github.com/pytorch/pytorch/pull/187057))
- Refresh cached tensor metadata after any in-place mutation proven by fake execution, fixing stale `size()`/`stride()` reads after `as_strided_` ([#187890](https://github.com/pytorch/pytorch/pull/187890))
- Fix `TypeError: sequence item N: expected str instance, int found` for an f-string over a dynamic `SymInt` that spans a graph break ([#189830](https://github.com/pytorch/pytorch/pull/189830))
- Fix f-string mutation ordering so Python-side object and container formatting is evaluated at the original bytecode point ([#182638](https://github.com/pytorch/pytorch/pull/182638))
- Route `ctx.needs_input_grad` through side-effect mutation tracking, so a traced store is no longer silently dropped ([#191492](https://github.com/pytorch/pytorch/pull/191492))
- Restore the process autocast dtype after a trace-time `torch.set_autocast_dtype`, fixing `Global autocast state changed while dynamo tracing` ([#186530](https://github.com/pytorch/pytorch/pull/186530))
- Fix synthetic base detection for overlapping `unsqueeze` views with mutation ([#187111](https://github.com/pytorch/pytorch/pull/187111))
- Raise an observed `TypeError` instead of an internal `AssertionError` for bad `vars()` arity ([#185128](https://github.com/pytorch/pytorch/pull/185128))
- Fix `torch.vmap` over an `autograd.Function` that uses `generate_vmap_rule=True` ([#186362](https://github.com/pytorch/pytorch/pull/186362))
- Stop instantiating the deprecated `torch.autograd.Function` constructor when creating a `FunctionCtx` placeholder ([#186421](https://github.com/pytorch/pytorch/pull/186421))
- Fix infinite recursion when calling `int()`/`float()` on or indexing a pybind11 enum in a compiled function ([#188605](https://github.com/pytorch/pytorch/pull/188605))
- Fix the C++ pytree polyfill's `PyTreeSpec.__eq__`/`__hash__` so it matches eager `optree` semantics ([#190649](https://github.com/pytorch/pytorch/pull/190649))
- Propagate signature mismatch errors up correctly ([#190797](https://github.com/pytorch/pytorch/pull/190797))
- Check that a traced `__int__`/`__float__` actually returns an `int`/`float` ([#190257](https://github.com/pytorch/pytorch/pull/190257))
- Validate the bound object's type in the `__get__` of C descriptors, which could otherwise bind a descriptor to an incompatible object and produce wrong control flow ([#190776](https://github.com/pytorch/pytorch/pull/190776))
- Graph break on `isinstance` checks of a tensor against a classinfo with a custom `__instancecheck__` (e.g. jaxtyping annotations) instead of compiling the wrong branch ([#186491](https://github.com/pytorch/pytorch/pull/186491))
- Fix `deque.__init__` truncating items against the pre-init `maxlen` when re-initializing ([#188171](https://github.com/pytorch/pytorch/pull/188171))
- Route `list`/`tuple` `__add__` through the sequence-concat slot, and let explicit set / dict-view `__and__`, `__xor__`, `__sub__` calls return `NotImplemented` for an unsupported operand as CPython does ([#189554](https://github.com/pytorch/pytorch/pull/189554), [#189274](https://github.com/pytorch/pytorch/pull/189274))
- Return the actual subclass from `type()` on a `torch.Event` subclass ([#189145](https://github.com/pytorch/pytorch/pull/189145))
- Fix the error message for non-iterable slice assignment on CPython patch versions predating gh-120384 ([#187777](https://github.com/pytorch/pytorch/pull/187777))
- Specialize symbolic range bounds in `RangeVariable` ([#187605](https://github.com/pytorch/pytorch/pull/187605))
- Clear stale exception-table entries on copied prefix instructions, fixing a `KeyError` when compiling Python 3.12 coroutine bytecode ([#185731](https://github.com/pytorch/pytorch/pull/185731))
- Stop generating `LIST_APPEND` bytecode, which assumes single ownership and tripped assertions on free-threaded builds ([#187086](https://github.com/pytorch/pytorch/pull/187086))
- Always create a real iterator instead of imitating CPython's virtual iterators, fixing segfaults when restoring from a graph break inside a list comprehension on Python 3.15 ([#187103](https://github.com/pytorch/pytorch/pull/187103))
- Probe internal attributes with `object.__getattribute__` instead of running a user-defined `__getattr__` ([#190970](https://github.com/pytorch/pytorch/pull/190970))
- Fix the `ts` and `aot_ts` backends, which failed on every function because `torch.jit.script` cannot script the `_LazyGraphModule` handed to backends ([#188875](https://github.com/pytorch/pytorch/pull/188875))
- Handle `OSError` (e.g. `PermissionError`) from the `nvcc` probe when collecting CUDA info for a repro, which could crash `torch.compile` with an `InductorError` ([#185843](https://github.com/pytorch/pytorch/pull/185843))
- Do not graft a self-referential `bw_compiler` when an `aot_autograd` backend compiles a second graph ([#189325](https://github.com/pytorch/pytorch/pull/189325))
- Add meta kernels for `torch._grid_sampler_2d_cpu_fallback` and its backward so the op can be captured instead of hard-erroring on unallocated storage ([#191664](https://github.com/pytorch/pytorch/pull/191664))
- Infer a graph's input device and dtype only from tensors, and classify registered backends with `isinstance` checks instead of attribute probing ([#190425](https://github.com/pytorch/pytorch/pull/190425), [#190426](https://github.com/pytorch/pytorch/pull/190426))
- Fix gradients for a directly-captured 0-D score-mod tensor in FlexAttention ([#188869](https://github.com/pytorch/pytorch/pull/188869))
### performance
- Trim the fixed per-call overhead of a compiled function: avoid per-call `DispatchKeySet` pybind churn in `compile_wrapper`, default the guard TLS attributes so `TracingContext.try_get()` avoids a `getattr` miss, and slim the `torch._dynamo.disable` prologue ([#190390](https://github.com/pytorch/pytorch/pull/190390), [#190571](https://github.com/pytorch/pytorch/pull/190571), [#190392](https://github.com/pytorch/pytorch/pull/190392))
- Speed up `unwrap_dead_wrappers` on the `autograd.Function.apply` fast path ([#189577](https://github.com/pytorch/pytorch/pull/189577))
- Model `itertools.chain` / `chain.from_iterable` and `itertools.zip_longest` natively instead of tracing through a Python polyfill, cutting compile time for those constructs by roughly 4x ([#186973](https://github.com/pytorch/pytorch/pull/186973), [#186974](https://github.com/pytorch/pytorch/pull/186974))
- Skip guard creation for function inputs the compiled code never reads, avoiding spurious recompiles from pass-through arguments ([#187782](https://github.com/pytorch/pytorch/pull/187782))
- Avoid recompiles when a compiled region's input alternates between an `AsyncCollectiveTensor` and the resolved plain `Tensor`, and when Accelerate-style `functools.partial` patched module forwards are shared across identical layers ([#189482](https://github.com/pytorch/pytorch/pull/189482), [#185739](https://github.com/pytorch/pytorch/pull/185739))
- Fix an AOTAutograd cache miss in FlexAttention caused by unpicklable local `torch._check` message closures ([#188177](https://github.com/pytorch/pytorch/pull/188177))
- Query the TVM runtime module's input info once when building `exec_tvm` instead of on every call ([#189012](https://github.com/pytorch/pytorch/pull/189012))
### docs
- Link the guard-overhead page to the developer blog post and document a profiler-based way to measure guard overhead ([#191387](https://github.com/pytorch/pytorch/pull/191387))
- Document exception tracing behavior and the observed-exception model in the `torch/_dynamo/exc.py` module docstring ([#184923](https://github.com/pytorch/pytorch/pull/184923))
### devs
- Add a config flag to canonicalize the order of nodes in the generated FX graph, making captured graphs deterministic across runs ([#181775](https://github.com/pytorch/pytorch/pull/181775))
- Make generated `fx_graph_runnable` repros work for graphs containing higher-order-op subgraphs (`torch.cond`, `torch.while_loop`), which previously emitted invalid Python ([#186804](https://github.com/pytorch/pytorch/pull/186804))
- Serialize symbolic storage sizes in generated repros as executable Python instead of `repr()` output such as `Max(1, s35)` ([#190838](https://github.com/pytorch/pytorch/pull/190838))
- Decode minifier subprocess output tolerantly so non-UTF-8 bytes in runtime diagnostics no longer abort the minifier harness ([#190696](https://github.com/pytorch/pytorch/pull/190696))
### not user facing
- Add an internal suppression list for nested graph breaks in distributed code ([#187220](https://github.com/pytorch/pytorch/pull/187220))
- Rename internal Dynamo variable trackers for custom-class objects ([#188460](https://github.com/pytorch/pytorch/pull/188460))
- Enable nested graph breaks in additional Dynamo tests ([#186657](https://github.com/pytorch/pytorch/pull/186657))
- Route attribute access, method dispatch, and the object protocol through CPython-style type slots: a `getattro` slot plus `GenericGetAttr` infrastructure, `BoundMethodVariable`, `object_generic_getattr` as the base default, `hasattr` unified with it, UDOV hook extraction, generic attribute mutation for non-UDOV variables, `__dict__` view hoisting, dispatch through the `tp_as_*` sub-structs, and CPython-aligned helper names ([#186013](https://github.com/pytorch/pytorch/pull/186013), [#187113](https://github.com/pytorch/pytorch/pull/187113), [#187196](https://github.com/pytorch/pytorch/pull/187196), [#187200](https://github.com/pytorch/pytorch/pull/187200), [#187226](https://github.com/pytorch/pytorch/pull/187226), [#187469](https://github.com/pytorch/pytorch/pull/187469), [#187531](https://github.com/pytorch/pytorch/pull/187531), [#188181](https://github.com/pytorch/pytorch/pull/188181), [#190415](https://github.com/pytorch/pytorch/pull/190415), [#190790](https://github.com/pytorch/pytorch/pull/190790), [#191011](https://github.com/pytorch/pytorch/pull/191011), [#189081](https://github.com/pytorch/pytorch/pull/189081), [#187377](https://github.com/pytorch/pytorch/pull/187377))
- Introduce declarative `tp_methods` dispatch and migrate variable trackers onto it, deriving arity from CPython's `ml_flags` and adding CPython-mirroring positional-argument helpers ([#189428](https://github.com/pytorch/pytorch/pull/189428), [#189430](https://github.com/pytorch/pytorch/pull/189430), [#189433](https://github.com/pytorch/pytorch/pull/189433), [#189434](https://github.com/pytorch/pytorch/pull/189434), [#189435](https://github.com/pytorch/pytorch/pull/189435), [#189909](https://github.com/pytorch/pytorch/pull/189909), [#190971](https://github.com/pytorch/pytorch/pull/190971), [#191361](https://github.com/pytorch/pytorch/pull/191361))
- Represent `ConstDictVariable` as plain `dict` only and split `OrderedDict` storage into its own variable tracker ([#189549](https://github.com/pytorch/pytorch/pull/189549))
- Refactor side-effect replay into a registry dispatcher, validate `target_values`, and extract spec-binding helpers into shared FX modules ([#188395](https://github.com/pytorch/pytorch/pull/188395), [#186968](https://github.com/pytorch/pytorch/pull/186968), [#187160](https://github.com/pytorch/pytorch/pull/187160))
- Hoist `IndentedBuffer` into `torch/utils` so the AOTAutograd source builder can subclass it ([#189356](https://github.com/pytorch/pytorch/pull/189356))
- Rename the opaque-object type predicates, keeping deprecated aliases ([#188459](https://github.com/pytorch/pytorch/pull/188459))
- Typing sweeps across Dynamo: translator parameters, compiler config accessors, `Literal` vocabularies, `TypedDict` payloads, protocols for fixed-interface objects, repro CLI options, and `object` instead of `Any` on opaque surfaces ([#184800](https://github.com/pytorch/pytorch/pull/184800), [#185278](https://github.com/pytorch/pytorch/pull/185278), [#188486](https://github.com/pytorch/pytorch/pull/188486), [#188527](https://github.com/pytorch/pytorch/pull/188527), [#188574](https://github.com/pytorch/pytorch/pull/188574), [#188737](https://github.com/pytorch/pytorch/pull/188737), [#188749](https://github.com/pytorch/pytorch/pull/188749), [#190599](https://github.com/pytorch/pytorch/pull/190599), [#192142](https://github.com/pytorch/pytorch/pull/192142), [#192567](https://github.com/pytorch/pytorch/pull/192567), [#186318](https://github.com/pytorch/pytorch/pull/186318))
- Clean up the backends: store backend tags in the registry, check TVM availability with `find_spec`, and remove dead code in the `tvm` and common backends ([#189251](https://github.com/pytorch/pytorch/pull/189251), [#189013](https://github.com/pytorch/pytorch/pull/189013), [#189249](https://github.com/pytorch/pytorch/pull/189249))
- Fixes to the TVM relay path that were superseded by its removal in the same release: passing the scheduler through `options` in the `tvm_meta_schedule` / `tvm_auto_scheduler` partials, binding rank-0 tensor inputs, and raising an actionable error for `dynamic=True` ([#188811](https://github.com/pytorch/pytorch/pull/188811), [#189699](https://github.com/pytorch/pytorch/pull/189699), [#189125](https://github.com/pytorch/pytorch/pull/189125))
- Reverted changes that landed and were backed out within this release ([#185280](https://github.com/pytorch/pytorch/pull/185280), [#191024](https://github.com/pytorch/pytorch/pull/191024), [#192868](https://github.com/pytorch/pytorch/pull/192868))
- Internal configuration changes: turn `capture_sparse_compute` on by default internally and flip the default of `use_lambda_guard_for_object_aliasing` ([#190617](https://github.com/pytorch/pytorch/pull/190617), [#191043](https://github.com/pytorch/pytorch/pull/191043))
- Always reset Dynamo in tests when it has been imported ([#184568](https://github.com/pytorch/pytorch/pull/184568))
- Make the fbcode custom-op preload in `fx_graph_runnable` repros best-effort ([#189656](https://github.com/pytorch/pytorch/pull/189656))
- Update error messages for Python 3.15 ([#191814](https://github.com/pytorch/pytorch/pull/191814))
- Test-only changes: enable graph-node-order canonicalization for the Dynamo, functorch/HOP, and distributed suites and fix the affected `test_perf.py` tests, strengthen and extend the `isolate_recompiles` suite, make the compiled-autograd trace tests rerun-safe and unflake `test_compiled_autograd_id`, filter the `torch_version` structured-trace artifact, use the eager backend where Inductor is not needed, add regression coverage for unregistered module globals, prepended forward pre-hooks, and package reset with Inductor, mirror CPython iterator-protocol edge cases in the polyfills, drop stale expected-failure sentinels and redundant config patches, fix the `assertExpectedInline` skip count, make `test_tvm` run against a real TVM install, migrate Dynamo tests for XPU, and propagate the bool-mask IoU comparison through the Detectron2 benchmark comparator ([#181776](https://github.com/pytorch/pytorch/pull/181776), [#181778](https://github.com/pytorch/pytorch/pull/181778), [#181779](https://github.com/pytorch/pytorch/pull/181779), [#188176](https://github.com/pytorch/pytorch/pull/188176), [#182080](https://github.com/pytorch/pytorch/pull/182080), [#187884](https://github.com/pytorch/pytorch/pull/187884), [#187885](https://github.com/pytorch/pytorch/pull/187885), [#190510](https://github.com/pytorch/pytorch/pull/190510), [#190559](https://github.com/pytorch/pytorch/pull/190559), [#189883](https://github.com/pytorch/pytorch/pull/189883), [#188068](https://github.com/pytorch/pytorch/pull/188068), [#186884](https://github.com/pytorch/pytorch/pull/186884), [#185336](https://github.com/pytorch/pytorch/pull/185336), [#190870](https://github.com/pytorch/pytorch/pull/190870), [#188474](https://github.com/pytorch/pytorch/pull/188474), [#188436](https://github.com/pytorch/pytorch/pull/188436), [#188475](https://github.com/pytorch/pytorch/pull/188475), [#191028](https://github.com/pytorch/pytorch/pull/191028), [#187100](https://github.com/pytorch/pytorch/pull/187100), [#189643](https://github.com/pytorch/pytorch/pull/189643), [#169241](https://github.com/pytorch/pytorch/pull/169241), [#186441](https://github.com/pytorch/pytorch/pull/186441))
- Typo and comment-only fixes, and broken-URL cleanup ([#187234](https://github.com/pytorch/pytorch/pull/187234), [#187370](https://github.com/pytorch/pytorch/pull/187370), [#187575](https://github.com/pytorch/pytorch/pull/187575), [#187063](https://github.com/pytorch/pytorch/pull/187063), [#190477](https://github.com/pytorch/pytorch/pull/190477), [#190573](https://github.com/pytorch/pytorch/pull/190573), [#190750](https://github.com/pytorch/pytorch/pull/190750), [#189063](https://github.com/pytorch/pytorch/pull/189063))
### security
