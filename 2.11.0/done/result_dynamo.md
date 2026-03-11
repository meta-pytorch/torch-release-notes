
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
* We place a lot of emphasis on the "BC-breaking" and "deprecation" sections. Those should be where the most effort goes in. The "improvements" and "bug fixes" for Python API should be nice as well.

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
- `torch.compile` now supports tracing through `contextlib.ExitStack` and `contextlib.suppress` context managers, allowing code that uses these patterns to be compiled without graph breaks ([#146506](https://github.com/pytorch/pytorch/pull/146506), [#147990](https://github.com/pytorch/pytorch/pull/147990))
- Added `torch._dynamo.config.ignore_logging_functions` config to skip arbitrary logging callables during tracing without causing graph breaks. Add functions to this set to have Dynamo treat them as no-ops during compilation ([#168913](https://github.com/pytorch/pytorch/pull/168913))
- Added `TORCH_DYNAMO_AUTOMATIC_DYNAMIC_SHAPES=0` environment variable to globally disable automatic dynamic shapes without modifying Python code ([#172334](https://github.com/pytorch/pytorch/pull/172334))
- Added `TORCH_COMPILE_GRAPH_BACKENDS` environment variable for per-graph backend override, enabling binary search to find problematic compiled graphs. Supports filter syntax like `">10:eager"` or `"0-5:aot_eager;6-10:inductor"` ([#172411](https://github.com/pytorch/pytorch/pull/172411))
- Added initial support for `torch._dynamo.leaf_function`, which allows annotating functions as leaf operations that Dynamo and AOTAutograd will not trace into ([#170471](https://github.com/pytorch/pytorch/pull/170471))
- Added support for tracing backward hooks on intermediate tensors, fixing cases where `register_hook` on non-leaf tensors would fail under `torch.compile` ([#172126](https://github.com/pytorch/pytorch/pull/172126))
### improvements
- Suppressed repeated "triton not found" messages during import — previously 12 identical warnings were printed ([#172614](https://github.com/pytorch/pytorch/pull/172614))
- `fullgraph=True` now recursively disables dynamo on compiled code to prevent unintentional re-invocation of `torch.compile` ([#173080](https://github.com/pytorch/pytorch/pull/173080))
- Miscellaneous smaller tracing support additions:
  - Support for `Enum.__contains__` and constants ([#173223](https://github.com/pytorch/pytorch/pull/173223))
  - Updated nn module hook handling to work with `kwargs=True` ([#172519](https://github.com/pytorch/pytorch/pull/172519))
  - Support `object` type in dynamo tracing ([#171457](https://github.com/pytorch/pytorch/pull/171457))
### bug fixes
- Fixed memory leaks: cleared weakrefs from memos/guards after compilation ([#165367](https://github.com/pytorch/pytorch/pull/165367)), cleared weak references from `FakeTensorMode` after compile ([#171209](https://github.com/pytorch/pytorch/pull/171209)), fixed CUDA memory usage for CPU-only compile ([#163841](https://github.com/pytorch/pytorch/pull/163841))
- Fixed overguarding on `OrderedSet`, `set`, and `frozenset` with activation checkpointing ([#169535](https://github.com/pytorch/pytorch/pull/169535), [#170291](https://github.com/pytorch/pytorch/pull/170291))
- Fixed `MATCH_MAPPING`, `MATCH_KEYS`, and `MATCH_SEQUENCE` opcodes for Python pattern matching (`match`/`case`) support ([#173085](https://github.com/pytorch/pytorch/pull/173085), [#173086](https://github.com/pytorch/pytorch/pull/173086), [#173087](https://github.com/pytorch/pytorch/pull/173087))
- Handle List/Dict comprehension graph breaks for Python 3.12+, including nested comprehensions ([#173558](https://github.com/pytorch/pytorch/pull/173558), [#174413](https://github.com/pytorch/pytorch/pull/174413))
- Fixed support for self-referential lists and dicts ([#173672](https://github.com/pytorch/pytorch/pull/173672), [#174498](https://github.com/pytorch/pytorch/pull/174498))
- Fixed `share_memory_` compile failure ([#171162](https://github.com/pytorch/pytorch/pull/171162))
- Fixed `defaultdict` default factory and union functionality ([#168028](https://github.com/pytorch/pytorch/pull/168028))
- Fixed property setter on `MutableMapping` subclasses ([#173184](https://github.com/pytorch/pytorch/pull/173184))
- Various tensor subclass fixes: subclass handling ([#170871](https://github.com/pytorch/pytorch/pull/170871)), sequence conversion ([#172103](https://github.com/pytorch/pytorch/pull/172103)), metadata propagation for in-place ops ([#167583](https://github.com/pytorch/pytorch/pull/167583))
- Correctly pass `is_inference` in the cudagraphs `torch.compile` backend ([#174713](https://github.com/pytorch/pytorch/pull/174713))
### performance
- Various compile time improvements: caching for `inspect.signature`, `var_getattr`, attr source construction, and higher-order ops; fast paths for `bind_args`, `GET_ITER` on tuples, and `tree_map` on namedtuples; lazy variable tracker optimizations ([#170100](https://github.com/pytorch/pytorch/pull/170100), [#169959](https://github.com/pytorch/pytorch/pull/169959), [#173582](https://github.com/pytorch/pytorch/pull/173582), [#174437](https://github.com/pytorch/pytorch/pull/174437), [#174438](https://github.com/pytorch/pytorch/pull/174438), [#174141](https://github.com/pytorch/pytorch/pull/174141), [#174020](https://github.com/pytorch/pytorch/pull/174020), [#174130](https://github.com/pytorch/pytorch/pull/174130), [#174901](https://github.com/pytorch/pytorch/pull/174901), [#174598](https://github.com/pytorch/pytorch/pull/174598))
### docs
### devs
### Untopiced
### not user facing
- Added `torch._dynamo.config.disable_numerics_affecting_decomps` option to disable decompositions that can affect numerics vs eager mode ([#170131](https://github.com/pytorch/pytorch/pull/170131))
- Added support for calling `torch.compile` inside `torch_dispatch` mode ([#166417](https://github.com/pytorch/pytorch/pull/166417))
- Enabled activation offloading (ao) with the default partitioner ([#172702](https://github.com/pytorch/pytorch/pull/172702))
- Added additional offloading fields to checkpoint policy for activation offloading ([#172705](https://github.com/pytorch/pytorch/pull/172705))
- `torch.compile` now builds graphs for top-level `TorchInGraph` functions ([#169844](https://github.com/pytorch/pytorch/pull/169844))
- Added polyfill for `group_tensors_by_device_and_dtype` ([#170152](https://github.com/pytorch/pytorch/pull/170152))
- Improved recompilation reason messages to use closure cell names ([#172403](https://github.com/pytorch/pytorch/pull/172403))
- Clearer compile error messages for sparse tensors ([#172256](https://github.com/pytorch/pytorch/pull/172256))
- Added `leaf_function` support for `None` output ([#174434](https://github.com/pytorch/pytorch/pull/174434))
- Improved graph break error messages with `USER_ERROR` hints for dynamic shape errors ([#172694](https://github.com/pytorch/pytorch/pull/172694))
- Added support for custom placements in `DTensor.grad_placements` under dynamo ([#173787](https://github.com/pytorch/pytorch/pull/173787))
- Support for `UserDefinedObjectVariable.call_tree_map` ([#170004](https://github.com/pytorch/pytorch/pull/170004))
- HOP graph break messages now always include the HOP name ([#169742](https://github.com/pytorch/pytorch/pull/169742))
- Updated graph break message to include `allow_rnn=True` hint ([#171266](https://github.com/pytorch/pytorch/pull/171266))
- Include one level of stack trace in the `lru_cache` warning message ([#171496](https://github.com/pytorch/pytorch/pull/171496))
- Print the source location when internal assert fails ([#172489](https://github.com/pytorch/pytorch/pull/172489))
- Support for pytree in `nonstrict_traceable` output ([#168934](https://github.com/pytorch/pytorch/pull/168934))
- Adding string names of type as hint when guarding input types ([#167717](https://github.com/pytorch/pytorch/pull/167717))
- Support BlockMask pytree registration for FlexAttention ([#170088](https://github.com/pytorch/pytorch/pull/170088))
- Support FlexAttention blockmask taking arbitrary callable ([#174610](https://github.com/pytorch/pytorch/pull/174610))
- Preserve original stack trace when rethrowing exception ([#170198](https://github.com/pytorch/pytorch/pull/170198))
- Fixed `TORCH_LOGS` environment variable name in log messages (d2305bd68fe)
- Fixed assigning `fn.__annotations__` in `SET_FUNCTION_ATTRIBUTE` ([#174568](https://github.com/pytorch/pytorch/pull/174568))
- Fixed codegen for new objects when `replay_side_effects=False` ([#169608](https://github.com/pytorch/pytorch/pull/169608))
- Fixed typo in `aot_compile` error message ([#170441](https://github.com/pytorch/pytorch/pull/170441))
- Fixed missing `step_unsupported` graph break message ([#170115](https://github.com/pytorch/pytorch/pull/170115))
- Fixed missing graph break website link ([#170031](https://github.com/pytorch/pytorch/pull/170031))
- Fixed typo: "compmilation" → "compilation" ([#170522](https://github.com/pytorch/pytorch/pull/170522))
- Fixed closure variables in nested function definitions ([#170705](https://github.com/pytorch/pytorch/pull/170705))
- Fixed crash when indexing `torch.Size` with tensor ([#170435](https://github.com/pytorch/pytorch/pull/170435))
- Fixed `bool` trace in dynamo ([#171050](https://github.com/pytorch/pytorch/pull/171050))
- Fixed error message missing spaces ([#171915](https://github.com/pytorch/pytorch/pull/171915))
- Multiple fixes for nested graph breaks ([#171646](https://github.com/pytorch/pytorch/pull/171646), [#170135](https://github.com/pytorch/pytorch/pull/170135), [#171823](https://github.com/pytorch/pytorch/pull/171823), [#171824](https://github.com/pytorch/pytorch/pull/171824), [#171825](https://github.com/pytorch/pytorch/pull/171825))
- Fixed `UserDefinedTupleVariable` equality fallback behavior ([#172667](https://github.com/pytorch/pytorch/pull/172667))
- Updated graph break message `enable_rnn` → `allow_rnn` ([#172771](https://github.com/pytorch/pytorch/pull/172771))
- Fixed `TypeError` being incorrectly captured when binding args ([#173536](https://github.com/pytorch/pytorch/pull/173536))
- Fixed `frozenset` reconstruction ([#173557](https://github.com/pytorch/pytorch/pull/173557))
- Fixed `innermost_fn` bug on bound and unbound functions ([#174243](https://github.com/pytorch/pytorch/pull/174243))
- Fixed `range` variable `index` method correctness ([#174210](https://github.com/pytorch/pytorch/pull/174210))
- Fixed named children in `wrap_values` for `NNModuleVariable` ([#174399](https://github.com/pytorch/pytorch/pull/174399))
- Include `var_to_hint_override` in `FxGraphCache` key ([#174805](https://github.com/pytorch/pytorch/pull/174805))
- Fixed profiler SVG generation corner case ([#174909](https://github.com/pytorch/pytorch/pull/174909))
- Speedup `index` method for constant data structures ([#173612](https://github.com/pytorch/pytorch/pull/173612))
- Speedup `iter` on `DictItemsVariable` ([#173645](https://github.com/pytorch/pytorch/pull/173645))
- Simplify VT cache and extend to lazy VTs ([#174242](https://github.com/pytorch/pytorch/pull/174242))
- `CONSTANT_VARIABLE_NONE` singleton for `ConstantVariable(None)` ([#174728](https://github.com/pytorch/pytorch/pull/174728))
- Small doc suggestion for intermediate hooks ([#172023](https://github.com/pytorch/pytorch/pull/172023))
- Added side effects logging artifact for debugging ([#171469](https://github.com/pytorch/pytorch/pull/171469))
- Added e2e user stack to guard debug info ([#169999](https://github.com/pytorch/pytorch/pull/169999))
- Added option to keep tensor, shape, and global state guards in precompile ([#170082](https://github.com/pytorch/pytorch/pull/170082))
- Added Dynamo profiler for compile time analysis ([#173942](https://github.com/pytorch/pytorch/pull/173942))
- Improved `graph_id_filter` for debugging ([#173880](https://github.com/pytorch/pytorch/pull/173880))
- Added chromium events for dynamo compile time debugging ([#174641](https://github.com/pytorch/pytorch/pull/174641))
- Made compilation events visible in profiler ([#174191](https://github.com/pytorch/pytorch/pull/174191))
- Added variable builder time in tlparse ([#174908](https://github.com/pytorch/pytorch/pull/174908))
- Ensured generator frames are recorded in profiler ([#174440](https://github.com/pytorch/pytorch/pull/174440))
- [dynamo] Add ignore_fresh_unbacked_symbols for foreach ops with scalar values ([#170288](https://github.com/pytorch/pytorch/pull/170288))
- move dynamo MetricsContext into TLS ([#170605](https://github.com/pytorch/pytorch/pull/170605))
- [BE][Typing][Dynamo] Type torch/_dynamo/variables/builder.py ([#171328](https://github.com/pytorch/pytorch/pull/171328))
- [dynamo] Fix benchmarks/dynamo/common.py error ([#170009](https://github.com/pytorch/pytorch/pull/170009))
- Removed dynamo skip decorator to allow cpython tests to run ([#169405](https://github.com/pytorch/pytorch/pull/169405))
- Log global state ([#170070](https://github.com/pytorch/pytorch/pull/170070))
- [dynamo][hops] Ignore side effects for _reparameterize_module ([#170251](https://github.com/pytorch/pytorch/pull/170251))
- [dynamo] Fix failure in test/dynamo/test_activation_checkpointing.py ([#170118](https://github.com/pytorch/pytorch/pull/170118))
- [dynamo] Fix test state leakage in test/dynamo/test_aot_compile.py ([#170144](https://github.com/pytorch/pytorch/pull/170144))
- Don't run torch.compile under non-strict export ([#165322](https://github.com/pytorch/pytorch/pull/165322))
- [invoke_subgraph] Add backend_options to nested_compile_region to be used by regional_inductor ([#167599](https://github.com/pytorch/pytorch/pull/167599))
- Delete deprecated Dynamo enrich_profiler_metadata config ([#169831](https://github.com/pytorch/pytorch/pull/169831))
- [dynamo] remove special handling for fsdp wrapping ([#170413](https://github.com/pytorch/pytorch/pull/170413))
- [BE][Typing][Dynamo] Type torch/_dynamo/variables/higher_order_ops.py ([#170011](https://github.com/pytorch/pytorch/pull/170011))
- [precompile][ez] Use a separate config flag for autograd key bypassing ([#170443](https://github.com/pytorch/pytorch/pull/170443))
- [precompile] Support serializing nested function in the context of guard preservation ([#170081](https://github.com/pytorch/pytorch/pull/170081))
- [BE][Typing][Dynamo] Type torch/_dynamo/variables/misc.py ([#171112](https://github.com/pytorch/pytorch/pull/171112))
- [dynamo] refactor frame skips and error messages in dynamo ([#170587](https://github.com/pytorch/pytorch/pull/170587))
- [Dynamo][Triton] handle wrap_triton as a no-op in Dynamo tracing ([#171289](https://github.com/pytorch/pytorch/pull/171289))
- [dynamo] Remove SkipCodeRecursiveException and RecompileLimitExceeded, add frame_exec_strategy attribute ([#171358](https://github.com/pytorch/pytorch/pull/171358))
- [dynamo] remove most Unsupported subclasses ([#171486](https://github.com/pytorch/pytorch/pull/171486))
- [dynamo] remove most InstructionTranslator.current_tx() callsites ([#170234](https://github.com/pytorch/pytorch/pull/170234))
- [logging][dynamo_compile] Populate hit/miss cache counts for both FXGraph and AOTAutograd caches ([#171743](https://github.com/pytorch/pytorch/pull/171743))
- [dynamo] Fix the bench profiler ([#171691](https://github.com/pytorch/pytorch/pull/171691))
- Opt in more test files to Pyrefly type checking ([#171833](https://github.com/pytorch/pytorch/pull/171833))
- [precompile] Support serializing nested function in the context of guard preservation ([#171156](https://github.com/pytorch/pytorch/pull/171156))
- [BE] Don't search for NVCC on ROCM environment ([#171914](https://github.com/pytorch/pytorch/pull/171914))
- Fix flaky CUDA memory leak in test_aot_cudagraphs_cuda ([#171879](https://github.com/pytorch/pytorch/pull/171879))
- [BE][Ez]: Add more dataclass slots kwarg to various dynamo internals ([#171906](https://github.com/pytorch/pytorch/pull/171906))
- [opaque_obj] Allow member accesses on reference types ([#171483](https://github.com/pytorch/pytorch/pull/171483))
- [opaque obj] Support nested opaque objs ([#171484](https://github.com/pytorch/pytorch/pull/171484))
- [opaque obj] Minor refactor for method support on value-types ([#172092](https://github.com/pytorch/pytorch/pull/172092))
- [opaque obj] Allow tensor subclass attr accesses ([#172099](https://github.com/pytorch/pytorch/pull/172099))
- [dynamo] Add LazyConstantVariable ([#169282](https://github.com/pytorch/pytorch/pull/169282))
- opaque objects - handle class attributes ([#172413](https://github.com/pytorch/pytorch/pull/172413))
- [opaque obj] Fix call_method on tensor subclasses ([#172265](https://github.com/pytorch/pytorch/pull/172265))
- Fix CPython 3.13 test failures reported in dynamo-unittest job ([#172448](https://github.com/pytorch/pytorch/pull/172448))
- [opaque obj] Support getitem ([#172908](https://github.com/pytorch/pytorch/pull/172908))
- [dynamo, BE] Improve type annotations around BaseUserFunctionVariable ([#172916](https://github.com/pytorch/pytorch/pull/172916))
- [dynamo, type checking] Improve type hints for InliningInstructionTranslator ([#173217](https://github.com/pytorch/pytorch/pull/173217))
- [dynamo] Save source helper functions ([#173394](https://github.com/pytorch/pytorch/pull/173394))
- Revert "[dynamo] Support type inspection on unrealized LazyConstantVariables (#169513)" ([#173496](https://github.com/pytorch/pytorch/pull/173496))
- [precompile] Serialize triton kernel side table for bundled AOT artifacts ([#173556](https://github.com/pytorch/pytorch/pull/173556))
- [Flex] Support scalar learnable bias ([#173490](https://github.com/pytorch/pytorch/pull/173490))
- [ez] refactor _serialize_triton_kernel ([#173667](https://github.com/pytorch/pytorch/pull/173667))
- [dynamo][refactor] Use ImportSource to generalize TorchSource and CollectionsSource ([#173745](https://github.com/pytorch/pytorch/pull/173745))
- [dynamo] Support sourceless MappingProxyObjects ([#173749](https://github.com/pytorch/pytorch/pull/173749))
- [dynamo] Support sourceless inspect.Parameter objects ([#173750](https://github.com/pytorch/pytorch/pull/173750))
- [dynamo] Remove code dependency on deprecated `dead_code_elimination` ([#169621](https://github.com/pytorch/pytorch/pull/169621))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through variable builders in lists.py ([#173458](https://github.com/pytorch/pytorch/pull/173458))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through variable builders in builtin.py ([#173439](https://github.com/pytorch/pytorch/pull/173439))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through SourcelessBuilder in dicts.py ([#173441](https://github.com/pytorch/pytorch/pull/173441))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through builders in higher_order_ops.py ([#173442](https://github.com/pytorch/pytorch/pull/173442))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through variable builders in exc.py, utils.py, nn_module.py ([#173451](https://github.com/pytorch/pytorch/pull/173451))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through variable builders in torch.py ([#173449](https://github.com/pytorch/pytorch/pull/173449))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through variable builders in user_defined.py ([#173450](https://github.com/pytorch/pytorch/pull/173450))
- Added proper dict repr utilized across several tests ([#169468](https://github.com/pytorch/pytorch/pull/169468))
- support unbacked-batch-only in torchbench ([#172719](https://github.com/pytorch/pytorch/pull/172719))
- [TorchRec] mark `torch._utils_internal.justknobs_check` as constant in dynamo ([#174149](https://github.com/pytorch/pytorch/pull/174149))
- [precompile] Support eager backend ([#174226](https://github.com/pytorch/pytorch/pull/174226))
- Don't try to print repro on failure for CPython test cases ([#174571](https://github.com/pytorch/pytorch/pull/174571))
- [dynamo] Add cpython enum tests ([#174458](https://github.com/pytorch/pytorch/pull/174458))
- [Dynamo] Graph Break on __class__ assignment ([#174761](https://github.com/pytorch/pytorch/pull/174761))
- Add `TypingVariable.__eq__` ([#174569](https://github.com/pytorch/pytorch/pull/174569))
- [dynamo] add id check to innermost_fn ([#174335](https://github.com/pytorch/pytorch/pull/174335))
- Cpython test refactor fixes ([#174415](https://github.com/pytorch/pytorch/pull/174415))
- Refactor Comprehension Graph Break Handling ([#174694](https://github.com/pytorch/pytorch/pull/174694))
- [DYNAMO] Change trigger to trigger.name ([#173676](https://github.com/pytorch/pytorch/pull/173676))
- Hoistable opaque value type objects ([#174430](https://github.com/pytorch/pytorch/pull/174430))
- [dynamo] Refactor GraphBackendRouter and GraphConfigRouter to share common logic ([#174229](https://github.com/pytorch/pytorch/pull/174229))
- [opaque obj] Invoke subgraph support ([#172101](https://github.com/pytorch/pytorch/pull/172101))
- use shape_id to inform inputs that must have matching sizes in support in mark_unbacked ([#172716](https://github.com/pytorch/pytorch/pull/172716))
- [user-streams] Assign streams to epilogue copies ([#168368](https://github.com/pytorch/pytorch/pull/168368))
- Disable einops 0.8.2 check on PyTorch ([#175351](https://github.com/pytorch/pytorch/pull/175351))
### security
