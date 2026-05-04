
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
- `torch.compile(fullgraph=True)` now warns when a call runs no compiled code; will error in 2.13 ([#181940](https://github.com/pytorch/pytorch/pull/181940))

  Previously `fullgraph=True` was only validated once Dynamo actually compiled and ran the function. If Dynamo was bypassed at call time (e.g. under a user-defined `TorchDispatchMode`), the annotation silently had no effect. 2.12 emits a warning; **2.13 will raise.** For graph-break errors without `fullgraph`'s stronger guarantees, use `torch._dynamo.error_on_graph_break`.

  Version 2.12:
  ```python
  from torch.utils._python_dispatch import TorchDispatchMode

  class LoggingMode(TorchDispatchMode):
      def __torch_dispatch__(self, func, types, args=(), kwargs=None):
          return func(*args, **(kwargs or {}))

  @torch.compile(fullgraph=True)
  def model(x):
      return x.sin() + 1

  # A user-defined TorchDispatchMode is active, so Dynamo skips the frame
  # and no compiled code runs — emits a warning in 2.12, will raise in 2.13.
  with LoggingMode(): # Remove this to fix warning
      model(torch.randn(3, 4))

  ```

- The `inline_inbuilt_nn_modules` Dynamo config is deprecated ([#177489](https://github.com/pytorch/pytorch/pull/177489), [#178205](https://github.com/pytorch/pytorch/pull/178205))

  Inlining of in-built `nn.Module` instances is now the default; setting the flag emits a deprecation warning and it will be removed in a future release.

  Version 2.11:
  ```python
  import torch._dynamo.config as cfg
  cfg.inline_inbuilt_nn_modules = True  # was a tunable knob
  ```

  Version 2.12:
  ```python
  # No action needed — inlining is on by default.
  # Remove any explicit references to torch._dynamo.config.inline_inbuilt_nn_modules.
  ```

- Added a deprecation framework to the `torch.compile` config module so individual options can be marked deprecated ([#169837](https://github.com/pytorch/pytorch/pull/169837))

### new features
- Made `torch._dynamo.aot_compile` public, with `aot_eager` and `inductor` backend support and docs ([#179917](https://github.com/pytorch/pytorch/pull/179917), [#180008](https://github.com/pytorch/pytorch/pull/180008))
- Added a `recompile_limit` keyword argument to `torch.compile` to override the per-function recompile cap without touching global config ([#177936](https://github.com/pytorch/pytorch/pull/177936))
- Added min/max bounds to `torch._dynamo.mark_unbacked` for communicating value ranges to the symbolic shape system ([#176313](https://github.com/pytorch/pytorch/pull/176313))
- Added `bdb`, a `pdb`-style debugger for stepping through nested frames during Dynamo tracing (`n`, `u`, `d`, `r`, `bt`), plus a user-callable `breakpoint()` that auto-starts it ([#174626](https://github.com/pytorch/pytorch/pull/174626), [#174746](https://github.com/pytorch/pytorch/pull/174746), [#175200](https://github.com/pytorch/pytorch/pull/175200))

### improvements
- Broader Python tracing: `enum.Enum` iteration, `nn.Module.__getattribute__`, `_enter_autocast`/`_exit_autocast` and other context managers, `next()` on `itertools.count`, `itertools.takewhile`, `bool(OrderedDict)`, `NamedTuple.__eq__(tuple)`, numpy `ndarray.flat`, and `locals()`/`vars()` ([#175176](https://github.com/pytorch/pytorch/pull/175176), [#175527](https://github.com/pytorch/pytorch/pull/175527), [#173877](https://github.com/pytorch/pytorch/pull/173877), [#176521](https://github.com/pytorch/pytorch/pull/176521), [#178818](https://github.com/pytorch/pytorch/pull/178818), [#177876](https://github.com/pytorch/pytorch/pull/177876), [#175394](https://github.com/pytorch/pytorch/pull/175394), [#176729](https://github.com/pytorch/pytorch/pull/176729), [#175787](https://github.com/pytorch/pytorch/pull/175787), [#179595](https://github.com/pytorch/pytorch/pull/179595))
- CPython `nb_index`/`nb_bool`/`nb_float` slots so Dynamo can trace `operator.index(tensor)`, `bool(...)`, and `float(...)`; graph-break on `torch.Generator` methods ([#178921](https://github.com/pytorch/pytorch/pull/178921), [#178931](https://github.com/pytorch/pytorch/pull/178931), [#179114](https://github.com/pytorch/pytorch/pull/179114), [#180198](https://github.com/pytorch/pytorch/pull/180198), [#178519](https://github.com/pytorch/pytorch/pull/178519))
- Higher-order ops & subgraphs: `cond` supports aliases and mutations under `no_grad`, autogradable leaf modules support pytree outputs, `nonstrict_trace` accepts `nn.Module` inputs, and `invoke_subgraph` supports subgraph reuse ([#172836](https://github.com/pytorch/pytorch/pull/172836), [#172152](https://github.com/pytorch/pytorch/pull/172152), [#175010](https://github.com/pytorch/pytorch/pull/175010), [#172372](https://github.com/pytorch/pytorch/pull/172372), [#176644](https://github.com/pytorch/pytorch/pull/176644))
- Streams & Triton: current-stream handling via `torch.cuda.stream`, sync barriers via a dependency HOP, `triton.set_allocator` inside `torch.compile`, and reuse of tracked objects for Triton `prune_configs_by` ([#177610](https://github.com/pytorch/pytorch/pull/177610), [#168894](https://github.com/pytorch/pytorch/pull/168894), [#177470](https://github.com/pytorch/pytorch/pull/177470), [#177874](https://github.com/pytorch/pytorch/pull/177874))

### bug fixes
- Guard correctness: missing source annotation on float guard after recompile, missing guards on class attribute access for literals/enums, guard on constant function `__defaults__`, guard tensor-method fallthrough against unknown methods, and closure-hash in `CodeId` so factory functions don't reuse stale graphs ([#177103](https://github.com/pytorch/pytorch/pull/177103), [#177191](https://github.com/pytorch/pytorch/pull/177191), [#178420](https://github.com/pytorch/pytorch/pull/178420), [#177737](https://github.com/pytorch/pytorch/pull/177737), [#173512](https://github.com/pytorch/pytorch/pull/173512))
- Tracing: `@property` setters bypassed by `torch.compile`, `AttributeError` swallowed by `try`/`except` on tensor attributes, `torch.Size` dict lookups with tensor-backed keys, graph break on enum members with class values, `detach_` autograd metadata, `allow_in_graph` crash inside compiled functions, preserve original exception in `GuardOnDataDependentSymNode`, and `einops` 0.6.1 backwards patch ([#176624](https://github.com/pytorch/pytorch/pull/176624), [#175611](https://github.com/pytorch/pytorch/pull/175611), [#177313](https://github.com/pytorch/pytorch/pull/177313), [#177439](https://github.com/pytorch/pytorch/pull/177439), [#177875](https://github.com/pytorch/pytorch/pull/177875), [#178524](https://github.com/pytorch/pytorch/pull/178524), [#176016](https://github.com/pytorch/pytorch/pull/176016), [#177165](https://github.com/pytorch/pytorch/pull/177165))
- Nested graph breaks: global-scope bug in nested closures, decorators in the compiled region, graph break in `contextlib.contextmanager` init, and parent-stack corruption in `step_graph_break` ([#176906](https://github.com/pytorch/pytorch/pull/176906), [#177090](https://github.com/pytorch/pytorch/pull/177090), [#177195](https://github.com/pytorch/pytorch/pull/177195), [#177408](https://github.com/pytorch/pytorch/pull/177408))
- Compile-state & integration: `torch.compiler.is_exporting()` returning `True` during `torch.compile`, activation-checkpoint metadata loss through custom `autograd.Function`, mixed-dtype `bmm`/`matmul`, `vjp_fn` under `torch.compile`, `_extract_distributed_info` crash on FX-`Node` `group_name`, `nested_compile_region` cache keyed on `fn.__code__`, and reverting `allow_in_graph` deprecation warn-spam ([#176499](https://github.com/pytorch/pytorch/pull/176499), [#177396](https://github.com/pytorch/pytorch/pull/177396), [#177696](https://github.com/pytorch/pytorch/pull/177696), [#173883](https://github.com/pytorch/pytorch/pull/173883), [#178108](https://github.com/pytorch/pytorch/pull/178108), [#179148](https://github.com/pytorch/pytorch/pull/179148), [#178340](https://github.com/pytorch/pytorch/pull/178340))

### performance
- Faster guards: `GUARD_VALUE_DISPATCH` dispatch table, fast-path `requires_grad`, `DICT_NOT_CONTAINS`/`SET_NOT_CONTAINS`, `PyType_GetDict` on Python ≥3.12, thread-safe dict-version tracking, no recompiles on hoistable opaque objects, and a general guard-optimization pass ([#176033](https://github.com/pytorch/pytorch/pull/176033), [#177158](https://github.com/pytorch/pytorch/pull/177158), [#176053](https://github.com/pytorch/pytorch/pull/176053), [#179170](https://github.com/pytorch/pytorch/pull/179170), [#178703](https://github.com/pytorch/pytorch/pull/178703), [#176643](https://github.com/pytorch/pytorch/pull/176643), [#175006](https://github.com/pytorch/pytorch/pull/175006))
- Faster tracing: `tree_map_with_path`, constant-folding `elementwise_dtypes`, `inline_invoke_subgraph` post-tracing pass, emit subgraph output intermediates only on observed side effects, drop unnecessary `realize_all` in `speculate_subgraph`, skip `SymInt` copies in `TENSOR_SUBCLASS_METADATA_MATCH`, and avoid closure refcycle in `_empty_create_subclass` ([#174146](https://github.com/pytorch/pytorch/pull/174146), [#177743](https://github.com/pytorch/pytorch/pull/177743), [#176082](https://github.com/pytorch/pytorch/pull/176082), [#177368](https://github.com/pytorch/pytorch/pull/177368), [#176742](https://github.com/pytorch/pytorch/pull/176742), [#175596](https://github.com/pytorch/pytorch/pull/175596), [#175660](https://github.com/pytorch/pytorch/pull/175660))

### docs
- Improve `nonstrict_trace` documentation ([#172395](https://github.com/pytorch/pytorch/pull/172395))

### devs
- Repro/debug: `after_aot` repro generator in `fx_graph_runnable`, dumping resumption-frame bytecode in `tlparse`, and running the early pre-grad pass before `prepare_aot_module_simplified` ([#179657](https://github.com/pytorch/pytorch/pull/179657), [#166940](https://github.com/pytorch/pytorch/pull/166940), [#178394](https://github.com/pytorch/pytorch/pull/178394))
- Export plumbing: drop an unneeded flag from `dynamo_graph_capture_for_export` and support `torch._ops.Overload` ([#175646](https://github.com/pytorch/pytorch/pull/175646), [#175647](https://github.com/pytorch/pytorch/pull/175647))

### not user facing
- VariableTracker / Source refactors and infrastructure: `CONSTANT_VARIABLE_TRUE`/`FALSE` singletons, consolidating VariableTracker construction through variable builders, refactoring `UserDefinedObjectVariable.var_getattr`, `clone` method on `Source`, `resolve_source_value` on `OutputGraph`, `HASATTR` keyword-arg refactor, source-to-guards index on `GuardsSet`, side-effect stack/tracking on `SubgraphTracer`/`SideEffects`, consolidating `__dict__` handling, extracting comprehension graph-break logic, requiring `VariableTracker` args for `raise_observed_exception`, replacing raw `None` with `ConstantVariable` on the stack, tracking input tensors for attribute mutation, iterative DFS cycle detection, extracting `vt_identity_compare`, `_cpython_type` attribute on `VariableTracker`, `SetVariable` inheriting from `VT`, `ListBuiltinVariable` refactor, `python_type()` on ~35 `VariableTracker`s, `py_type` on `GetAttrVariable` creation sites, automatic `CONSTANT_VARIABLE_*` in `ConstantVariable.create`, `mp_subscript_impl` for unified `__getitem__`, `get_type_slots`, `VariableTracker.visit` walking side-effect attr mutations, code-motion for hierarchical compile, reduce special casing for `namedtuple`/`FrozenDataClass`/`enum.Enum`, list append/clear over-specialization (later reverted), more `istype` overloads, dropping a copy of exception args in `UserDefinedExceptionVariable`, and enabling nested-graph-breaks on dynamo tests ([#174758](https://github.com/pytorch/pytorch/pull/174758), [#174759](https://github.com/pytorch/pytorch/pull/174759), [#174849](https://github.com/pytorch/pytorch/pull/174849), [#175514](https://github.com/pytorch/pytorch/pull/175514), [#171772](https://github.com/pytorch/pytorch/pull/171772), [#176026](https://github.com/pytorch/pytorch/pull/176026), [#176032](https://github.com/pytorch/pytorch/pull/176032), [#176081](https://github.com/pytorch/pytorch/pull/176081), [#176124](https://github.com/pytorch/pytorch/pull/176124), [#176453](https://github.com/pytorch/pytorch/pull/176453), [#176459](https://github.com/pytorch/pytorch/pull/176459), [#176477](https://github.com/pytorch/pytorch/pull/176477), [#174941](https://github.com/pytorch/pytorch/pull/174941), [#175885](https://github.com/pytorch/pytorch/pull/175885), [#176647](https://github.com/pytorch/pytorch/pull/176647), [#169325](https://github.com/pytorch/pytorch/pull/169325), [#177467](https://github.com/pytorch/pytorch/pull/177467), [#172313](https://github.com/pytorch/pytorch/pull/172313), [#178118](https://github.com/pytorch/pytorch/pull/178118), [#179432](https://github.com/pytorch/pytorch/pull/179432), [#179192](https://github.com/pytorch/pytorch/pull/179192), [#179032](https://github.com/pytorch/pytorch/pull/179032), [#179796](https://github.com/pytorch/pytorch/pull/179796), [#179974](https://github.com/pytorch/pytorch/pull/179974), [#179161](https://github.com/pytorch/pytorch/pull/179161), [#179088](https://github.com/pytorch/pytorch/pull/179088), [#179107](https://github.com/pytorch/pytorch/pull/179107), [#179477](https://github.com/pytorch/pytorch/pull/179477), [#176086](https://github.com/pytorch/pytorch/pull/176086), [#179381](https://github.com/pytorch/pytorch/pull/179381), [#179426](https://github.com/pytorch/pytorch/pull/179426), [#179029](https://github.com/pytorch/pytorch/pull/179029), [#178426](https://github.com/pytorch/pytorch/pull/178426), [#179429](https://github.com/pytorch/pytorch/pull/179429), [#175980](https://github.com/pytorch/pytorch/pull/175980), [#177668](https://github.com/pytorch/pytorch/pull/177668), [#167695](https://github.com/pytorch/pytorch/pull/167695))
- Test scaffolding and CI: itertools dropwhile/starmap CPython tests, expected failures for Dynamo + metaclass tests, `tearDown` log.debug cleanup, fixing `itertools` islice tests, AC cache-entries error test cases, moving multi-GPU tests to distributed so they run in CI, detecting CPython skips (with revert), more invoke_subgraph subgraph-reuse tests, opaque-object tests, CPython `test_types.py`, pytree typing/docstring housekeeping, and `test_tree_map.py` refactor ([#175535](https://github.com/pytorch/pytorch/pull/175535), [#175970](https://github.com/pytorch/pytorch/pull/175970), [#175290](https://github.com/pytorch/pytorch/pull/175290), [#175404](https://github.com/pytorch/pytorch/pull/175404), [#176309](https://github.com/pytorch/pytorch/pull/176309), [#177391](https://github.com/pytorch/pytorch/pull/177391), [#177569](https://github.com/pytorch/pytorch/pull/177569), [#176795](https://github.com/pytorch/pytorch/pull/176795), [#178015](https://github.com/pytorch/pytorch/pull/178015), [#177989](https://github.com/pytorch/pytorch/pull/177989), [#179866](https://github.com/pytorch/pytorch/pull/179866), [#179336](https://github.com/pytorch/pytorch/pull/179336), [#177987](https://github.com/pytorch/pytorch/pull/177987), [#178050](https://github.com/pytorch/pytorch/pull/178050))
- Misc cleanup, reverts, and removed paths: legacy code removal, moving `fn.annotations` to `__dict__`, lint fix for `THROW`, revert of symbolic-shapes `guarding_hint_or_throw`/`optimization_hint`, telemetry using `.shape` instead of `.size()`, removing `inductor:mode` from `GraphBackendRouter` and aggregating rules in `GraphConfigRouter`, and an `allow_in_graph` deprecation notice that was later undone ([#175012](https://github.com/pytorch/pytorch/pull/175012), [#174714](https://github.com/pytorch/pytorch/pull/174714), [#179073](https://github.com/pytorch/pytorch/pull/179073), [#177113](https://github.com/pytorch/pytorch/pull/177113), [#177151](https://github.com/pytorch/pytorch/pull/177151), [#176363](https://github.com/pytorch/pytorch/pull/176363), [#176364](https://github.com/pytorch/pytorch/pull/176364), [#177096](https://github.com/pytorch/pytorch/pull/177096))

### security
