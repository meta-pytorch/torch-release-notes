
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
### improvements
- [BE] Don't print 12 `triton not found` on import ([#172614](https://github.com/pytorch/pytorch/pull/172614))
### bug fixes
- Preserve original stack trace when rethrowing exception ([#170198](https://github.com/pytorch/pytorch/pull/170198))
### performance
### docs
### devs
- Fix typo in log environment variable name (d2305bd68fe)
### Untopiced
- [dynamo] Add option to disable decomps which can affect numerics vs eager ([#170131](https://github.com/pytorch/pytorch/pull/170131))
- [dynamo] polyfill group_tensors_by_device_and_dtype ([#170152](https://github.com/pytorch/pytorch/pull/170152))
- [18/N] Use Python 3.10 typing ([#170280](https://github.com/pytorch/pytorch/pull/170280))
- [Dynamo] Fix overguarding on OrderedSet w/ AC ([#169535](https://github.com/pytorch/pytorch/pull/169535))
- [Dynamo] Fix overguarding on set/frozenset with AC ([#170291](https://github.com/pytorch/pytorch/pull/170291))
- [dynamo] Add ignore_fresh_unbacked_symbols for foreach ops with scalar values ([#170288](https://github.com/pytorch/pytorch/pull/170288))
- [19/N] Use Python 3.10 typing ([#170368](https://github.com/pytorch/pytorch/pull/170368))
- torch.compile: build graph for top-level TorchInGraph functions ([#169844](https://github.com/pytorch/pytorch/pull/169844))
- move dynamo MetricsContext into TLS ([#170605](https://github.com/pytorch/pytorch/pull/170605))
- [dynamo] Clear weakrefs held by memos and guards ([#165367](https://github.com/pytorch/pytorch/pull/165367))
- Fix syntax for suppression comments. ([#167088](https://github.com/pytorch/pytorch/pull/167088))
- [BE][Typing][Dynamo] Type torch/_dynamo/variables/builder.py ([#171328](https://github.com/pytorch/pytorch/pull/171328))
- Fix share_memory_ compile ([#171162](https://github.com/pytorch/pytorch/pull/171162))
- Cleanup pyrefly ignores 3 ([#171640](https://github.com/pytorch/pytorch/pull/171640))
- Support contextlib.ExitStack ([#146506](https://github.com/pytorch/pytorch/pull/146506))
- Support `contextlib.suppress` ([#147990](https://github.com/pytorch/pytorch/pull/147990))
- [dynamo] add side_effects logging artifact ([#171469](https://github.com/pytorch/pytorch/pull/171469))
- AOTAutograd: at runtime, specialcase saved-for-bw tensors whos version counters werent checked in eager ([#171353](https://github.com/pytorch/pytorch/pull/171353))
- hint_int -> size_hint, support size_hint in user code. ([#171944](https://github.com/pytorch/pytorch/pull/171944))
- [BE][Ez]: Add slots to treespec dataclasses ([#172172](https://github.com/pytorch/pytorch/pull/172172))
- [BE][Ez]: Modernize symbolic shape dataclasses ([#172115](https://github.com/pytorch/pytorch/pull/172115))
- [dynamo] use closure cell name in recompilation reasons ([#172403](https://github.com/pytorch/pytorch/pull/172403))
- [user-streams] Assign streams to epilogue copies ([#168368](https://github.com/pytorch/pytorch/pull/168368))
- env variable for disabling dynamic shapes ([#172334](https://github.com/pytorch/pytorch/pull/172334))
- [Dynamo] Clearer compile error messages for sparse tensors ([#172256](https://github.com/pytorch/pytorch/pull/172256))
- [dynamo] Add per-graph backend override for debugging/bisecting ([#172411](https://github.com/pytorch/pytorch/pull/172411))
- [opaque obj] Invoke subgraph support ([#172101](https://github.com/pytorch/pytorch/pull/172101))
- [ao] Enable ao with the default partitioner ([#172702](https://github.com/pytorch/pytorch/pull/172702))
- [ao] Add additional offloading fields to checkpoint policy ([#172705](https://github.com/pytorch/pytorch/pull/172705))
- [Dynamo] Update nn module hook handling to work with kwargs=True ([#172519](https://github.com/pytorch/pytorch/pull/172519))
- use shape_id to inform inputs that must have matching sizes  in support in mark_unbacked.  ([#172716](https://github.com/pytorch/pytorch/pull/172716))
- [dynamo] New `UserDefinedEnumVariable` and Support __contains__ method for Enum and constants ([#173223](https://github.com/pytorch/pytorch/pull/173223))
- [dynamo][autogradable leaf module] adding initial support ([#170471](https://github.com/pytorch/pytorch/pull/170471))
- [dynamo] disable dynamo recursively on compiled code if fullgraph=True using eval frame overrides ([#173080](https://github.com/pytorch/pytorch/pull/173080))
- [annotation][export] Add metadata hook for all nodes created in runtime_assert pass ([#173970](https://github.com/pytorch/pytorch/pull/173970))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through variable builders in lists.py ([#173458](https://github.com/pytorch/pytorch/pull/173458))
- [DYNAMO] Change trigger to trigger.name ([#173676](https://github.com/pytorch/pytorch/pull/173676))
- Hoistable opaque value type objects ([#174430](https://github.com/pytorch/pytorch/pull/174430))
- Fix assigning fn.__annotations__ in `SET_FUNCTION_ATTRIBUTE` ([#174568](https://github.com/pytorch/pytorch/pull/174568))
- [dynamo] Add per-graph inductor config override for debugging/bisecting ([#174228](https://github.com/pytorch/pytorch/pull/174228))
- [dynamo] Refactor GraphBackendRouter and GraphConfigRouter to share common logic ([#174229](https://github.com/pytorch/pytorch/pull/174229))
- [leaf_function] Add None output support ([#174434](https://github.com/pytorch/pytorch/pull/174434))
### not user facing
- Adding string names of  type  as hint when guarding input types ([#167717](https://github.com/pytorch/pytorch/pull/167717))
- Add support for ignore_logging_functions in Dynamo to skip arbitrary logging callables during tracing ([#168913](https://github.com/pytorch/pytorch/pull/168913))
- [dynamo] Support UserDefinedObjectVariable.call_tree_map ([#170004](https://github.com/pytorch/pytorch/pull/170004))
- [dynamo] Fix benchmarks/dynamo/common.py error ([#170009](https://github.com/pytorch/pytorch/pull/170009))
- [dynamo, hops] refactor HOP graph breaks to always include HOP names ([#169742](https://github.com/pytorch/pytorch/pull/169742))
- Removed dynamo skip decorator to allow cpython tests to run ([#169405](https://github.com/pytorch/pytorch/pull/169405))
- Log global state ([#170070](https://github.com/pytorch/pytorch/pull/170070))
- [dynamo][user_defined] Reduce var_getattr trace time by caching ([#170100](https://github.com/pytorch/pytorch/pull/170100))
- Support BlockMask pytree registration ([#170088](https://github.com/pytorch/pytorch/pull/170088))
- [RFC] Enable caching for some more HOPs ([#169959](https://github.com/pytorch/pytorch/pull/169959))
- [dynamo] fix missing gb website link on jump graph breaks ([#170031](https://github.com/pytorch/pytorch/pull/170031))
- [dynamo][hops] Ignore side effects for _reparameterize_module ([#170251](https://github.com/pytorch/pytorch/pull/170251))
- [dynamo] Fix failure in test/dynamo/test_activation_checkpointing.py ([#170118](https://github.com/pytorch/pytorch/pull/170118))
- [dynamo] Fix test state leakage in test_aot_compile.py ([#170144](https://github.com/pytorch/pytorch/pull/170144))
- Don't run torch.compile under non-strict export.  ([#165322](https://github.com/pytorch/pytorch/pull/165322))
- [invoke_subgraph] Add backend_options to nested_compile_region to be used by regional_inductor ([#167599](https://github.com/pytorch/pytorch/pull/167599))
- [Dynamo][Guards]Add e2e user stack to guard debug info and ++ leaf guard ([#169999](https://github.com/pytorch/pytorch/pull/169999))
- Delete deprecated Dynamo enrich_profiler_metadata config ([#169831](https://github.com/pytorch/pytorch/pull/169831))
- [dynamo] remove special handling for fsdp wrapping ([#170413](https://github.com/pytorch/pytorch/pull/170413))
- [BE][Typing][Dynamo] Type torch/_dynamo/variables/higher_order_ops.py ([#170011](https://github.com/pytorch/pytorch/pull/170011))
- We should still codegen new objects when replay_side_effects=False ([#169608](https://github.com/pytorch/pytorch/pull/169608))
- [precompile][ez] Use a separate config flag for autograd key bypassing. ([#170443](https://github.com/pytorch/pytorch/pull/170443))
- fix typo in aot_compile error message: `enable_aot_config` -> `enable_aot_compile` ([#170441](https://github.com/pytorch/pytorch/pull/170441))
- [dynamo] fix missing step_unsupported graph break message ([#170115](https://github.com/pytorch/pytorch/pull/170115))
- Revert "[ROCm][CUDA] add unit test utility busy_wait_for_flag (#166218)" ([#170462](https://github.com/pytorch/pytorch/pull/170462))
- Support for pytree in nonstrict_traceable output ([#168934](https://github.com/pytorch/pytorch/pull/168934))
- Fix typo: "compmilation" -> "compilation" ([#170522](https://github.com/pytorch/pytorch/pull/170522))
- [precompile] Support nested named tuple type in guard serialization. ([#170081](https://github.com/pytorch/pytorch/pull/170081))
- [precompile] Add an option to keep tensor, shape and global state guards. ([#170082](https://github.com/pytorch/pytorch/pull/170082))
- Support calling torch.compile inside torch_dispatch ([#166417](https://github.com/pytorch/pytorch/pull/166417))
- Support closure variables in nested functiuon defs ([#170705](https://github.com/pytorch/pytorch/pull/170705))
- Fix crash when indexing torch.Size with tensor ([#170435](https://github.com/pytorch/pytorch/pull/170435))
- Fix bool trace dynamo ([#171050](https://github.com/pytorch/pytorch/pull/171050))
- fix-dynamo-subclass ([#170871](https://github.com/pytorch/pytorch/pull/170871))
- Update graph break message to include `enable_rnn=True` hint ([#171266](https://github.com/pytorch/pytorch/pull/171266))
- [BE][Typing][Dynamo] Type torch/_dynamo/variables/misc.py ([#171112](https://github.com/pytorch/pytorch/pull/171112))
- [dynamo] refactor frame skips and error messages in dynamo ([#170587](https://github.com/pytorch/pytorch/pull/170587))
- [Dynamo][Triton] handle wrap_triton as a no-op in Dynamo tracing ([#171289](https://github.com/pytorch/pytorch/pull/171289))
- [dynamo] Remove SkipCodeRecursiveException and RecompileLimitExceeded, add frame_exec_strategy attribute ([#171358](https://github.com/pytorch/pytorch/pull/171358))
- [dynamo] remove most Unsupported subclasses ([#171486](https://github.com/pytorch/pytorch/pull/171486))
- [dynamo] remove most InstructionTranslator.current_tx() callsites ([#170234](https://github.com/pytorch/pytorch/pull/170234))
- Include one level of stack trace in the `lru_cache` warning msg ([#171496](https://github.com/pytorch/pytorch/pull/171496))
- [logging][dynamo_compile] Populate hit/miss cache counts for both FXGraph and AOTAutograd caches ([#171743](https://github.com/pytorch/pytorch/pull/171743))
- [dynamo] Fix the bench profiler ([#171691](https://github.com/pytorch/pytorch/pull/171691))
- Opt in more test files to Pyrefly type checking ([#171833](https://github.com/pytorch/pytorch/pull/171833))
- [precompile] Support serializing nested function in the context of guard preservation. ([#171156](https://github.com/pytorch/pytorch/pull/171156))
- fix error message missing spaces ([#171915](https://github.com/pytorch/pytorch/pull/171915))
- [BE] Don't search for NVCC on ROCM environment ([#171914](https://github.com/pytorch/pytorch/pull/171914))
- Support `object` in dynamo ([#171457](https://github.com/pytorch/pytorch/pull/171457))
- Fix flaky CUDA memory leak in test_aot_cudagraphs_cuda ([#171879](https://github.com/pytorch/pytorch/pull/171879))
- [BE][Ez]: Add more dataclass slots kwarg to various dynamo internals ([#171906](https://github.com/pytorch/pytorch/pull/171906))
- [xpu][test] Enable more Inductor UT for XPU ([#171773](https://github.com/pytorch/pytorch/pull/171773))
- [opaque_obj] Allow member accesses on reference types ([#171483](https://github.com/pytorch/pytorch/pull/171483))
- [opaque obj] Support nested opaque objs ([#171484](https://github.com/pytorch/pytorch/pull/171484))
- [opaque obj] Minor refactor for method support on value-types ([#172092](https://github.com/pytorch/pytorch/pull/172092))
- [opaque obj] Allow tensor subclass attr accesses ([#172099](https://github.com/pytorch/pytorch/pull/172099))
- Fix converting tensor subclass sequence ([#172103](https://github.com/pytorch/pytorch/pull/172103))
- Small doc suggestion for intermediate hooks ([#172023](https://github.com/pytorch/pytorch/pull/172023))
- Fix for test/distributed/test_device_mesh.py::TestDeviceMeshGetItem::test_flatten_mesh_4d ([#172189](https://github.com/pytorch/pytorch/pull/172189))
- [dynamo] Add LazyConstantVariable ([#169282](https://github.com/pytorch/pytorch/pull/169282))
- opaque objects - handle class attributes ([#172413](https://github.com/pytorch/pytorch/pull/172413))
- [opaque obj] Fix call_method on tensor subclasses ([#172265](https://github.com/pytorch/pytorch/pull/172265))
- Print the source when assert fails ([#172489](https://github.com/pytorch/pytorch/pull/172489))
- [dynamo, nested graph breaks] fix nested WithExitFunctionVariable codegen issue in step graph breaks; remove partial_convert ([#171646](https://github.com/pytorch/pytorch/pull/171646))
- [dynamo, nested graph breaks] fix nested graph breaks with error_on_graph_break ([#170135](https://github.com/pytorch/pytorch/pull/170135))
- [dynamo, nested graph breaks] ensure upper ctx managers are active in the unsupported instruction ([#171823](https://github.com/pytorch/pytorch/pull/171823))
- [dynamo, nested graph breaks] fix codegen error in nested step graph break ([#171824](https://github.com/pytorch/pytorch/pull/171824))
- [dynamo, nested graph breaks] restore upper contexts for nested step graph break skipped code ([#171825](https://github.com/pytorch/pytorch/pull/171825))
- Fix UserDefinedTupleVariable equality fallback behavior  ([#172667](https://github.com/pytorch/pytorch/pull/172667))
- Update graph break message `enable_rnn` -> `allow_rnn` ([#172771](https://github.com/pytorch/pytorch/pull/172771))
- Support hooks on intermediate tensors in dynamo ([#172126](https://github.com/pytorch/pytorch/pull/172126))
- Fix CPython 3.13 test failures reported in dynamo-unittest job ([#172448](https://github.com/pytorch/pytorch/pull/172448))
- [opaque obj] Support getitem ([#172908](https://github.com/pytorch/pytorch/pull/172908))
- [dynamo, BE] Improve type annotations around BaseUserFunctionVariable ([#172916](https://github.com/pytorch/pytorch/pull/172916))
- [dynamo, type checking] Improve type hints for InliningInstructionTranslator ([#173217](https://github.com/pytorch/pytorch/pull/173217))
- [dynamo] Save source helper functions ([#173394](https://github.com/pytorch/pytorch/pull/173394))
- Revert "[dynamo] Support type inspection on unrealized LazyConstantVariables (#169513)" ([#173496](https://github.com/pytorch/pytorch/pull/173496))
- Don't capture TypeError when binding args ([#173536](https://github.com/pytorch/pytorch/pull/173536))
- [dynamo] fix frozenset reconstruction ([#173557](https://github.com/pytorch/pytorch/pull/173557))
- [dynamo] Speedup GET_ITER on tuples ([#173582](https://github.com/pytorch/pytorch/pull/173582))
- Support default kwargs in new export ([#173613](https://github.com/pytorch/pytorch/pull/173613))
- [dynamo][index] Speedup index method for constant data structures ([#173612](https://github.com/pytorch/pytorch/pull/173612))
- [dynamo] Speedup iter on DictItemsVaraible ([#173645](https://github.com/pytorch/pytorch/pull/173645))
- [precompile] Serialize triton kernel side table for bundled AOT artifacts ([#173556](https://github.com/pytorch/pytorch/pull/173556))
- [Flex] Support scalar learnable bias ([#173490](https://github.com/pytorch/pytorch/pull/173490))
- [ez] refactor _serialize_triton_kernel ([#173667](https://github.com/pytorch/pytorch/pull/173667))
- [dynamo][refactor] Use ImportSource to generalize TorchSource and CollectionsSource ([#173745](https://github.com/pytorch/pytorch/pull/173745))
- [dynamo]  Support sourceless MappingProxyObjects ([#173749](https://github.com/pytorch/pytorch/pull/173749))
- [dynamo] Support sourceless inspect.Parameter objects ([#173750](https://github.com/pytorch/pytorch/pull/173750))
- Fix `MATCH_MAPPING` ([#173085](https://github.com/pytorch/pytorch/pull/173085))
- Fix `MATCH_KEYS` opcode ([#173086](https://github.com/pytorch/pytorch/pull/173086))
- Fix `MATCH_SEQUENCE` ([#173087](https://github.com/pytorch/pytorch/pull/173087))
- [dynamo] Improve graph_id_filter ([#173880](https://github.com/pytorch/pytorch/pull/173880))
- [dynamo] Remove code dependency on deprecated `dead_code_elimination` ([#169621](https://github.com/pytorch/pytorch/pull/169621))
- [dynamo][claude] Dynamo profiler ([#173942](https://github.com/pytorch/pytorch/pull/173942))
- [dynamo][compile time][claude-assist] Cache constant attrs of InlineInstructionTranslator ([#174141](https://github.com/pytorch/pytorch/pull/174141))
- [dynamo] Cache the attr source construction ([#174020](https://github.com/pytorch/pytorch/pull/174020))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through variable builders in builtin.py ([#173439](https://github.com/pytorch/pytorch/pull/173439))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through SourcelessBuilder in dicts.py ([#173441](https://github.com/pytorch/pytorch/pull/173441))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through builders in higher_order_ops.py ([#173442](https://github.com/pytorch/pytorch/pull/173442))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through variable builders in exc.py, utils.py, nn_module.py ([#173451](https://github.com/pytorch/pytorch/pull/173451))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through variable builders in torch.py ([#173449](https://github.com/pytorch/pytorch/pull/173449))
- [dynamo][claude-assisted] Consolidate VariableTracker construction through variable builders in user_defined.py ([#173450](https://github.com/pytorch/pytorch/pull/173450))
- [dynamo] add USER_ERROR graph break hint to some dynamic shapes errors, chain underlying exceptions ([#172694](https://github.com/pytorch/pytorch/pull/172694))
- [dynamo][dtensor] Support custom placements in DTensor.grad_placements ([#173787](https://github.com/pytorch/pytorch/pull/173787))
- Added proper dict repr utilized across several tests ([#169468](https://github.com/pytorch/pytorch/pull/169468))
- [dynamo] fix innermost_fn bug on bound and unbound functions ([#174243](https://github.com/pytorch/pytorch/pull/174243))
- Fixed default dict default factory and union functionality in dynamo. ([#168028](https://github.com/pytorch/pytorch/pull/168028))
- support unbacked-batch-only in torchbench ([#172719](https://github.com/pytorch/pytorch/pull/172719))
- [dynamo][claude-assisted] Support namedtuple fast path for tree_map ([#174130](https://github.com/pytorch/pytorch/pull/174130))
- Resolved range variable index method correctness ([#174210](https://github.com/pytorch/pytorch/pull/174210))
- Handle List/Dict Comprehension Graph Breaks for Python3.12+ ([#173558](https://github.com/pytorch/pytorch/pull/173558))
- [dynamo] Simplify VT cache, extent to LazyVTs ([#174242](https://github.com/pytorch/pytorch/pull/174242))
- [TorchRec] mark `torch._utils_internal.justknobs_check` as constant in dynamo ([#174149](https://github.com/pytorch/pytorch/pull/174149))
- [bugfix][dynamo] Fix named children in `wrap_values` for NNModuleVarible ([#174399](https://github.com/pytorch/pytorch/pull/174399))
- [dynamo] Fix Tensor Metadata Propagation for In-Place Ops ([#167583](https://github.com/pytorch/pytorch/pull/167583))
- [precompile] Support eager backend. ([#174226](https://github.com/pytorch/pytorch/pull/174226))
- [Dynamo] Clear weak references from FakeTensorMode after Compile ([#171209](https://github.com/pytorch/pytorch/pull/171209))
- [dynamo] Cache inspect.signature trace results ([#174437](https://github.com/pytorch/pytorch/pull/174437))
- [dynamo] Fast path for bind_args for simpler functions ([#174438](https://github.com/pytorch/pytorch/pull/174438))
- [dynamo][profiler] Ensure generator frames are also recorded ([#174440](https://github.com/pytorch/pytorch/pull/174440))
- Don't try to print repro on failure for CPython test cases ([#174571](https://github.com/pytorch/pytorch/pull/174571))
- [dynamo] Miscellaneous compile time fixes ([#174598](https://github.com/pytorch/pytorch/pull/174598))
- [dynamo][compile time] Add chromium events for dynamo compile time debugging ([#174641](https://github.com/pytorch/pytorch/pull/174641))
- [dynamo] Add cpython enum tests ([#174458](https://github.com/pytorch/pytorch/pull/174458))
- [dynamo] Make compilation events visible in profiler ([#174191](https://github.com/pytorch/pytorch/pull/174191))
- Support FlexAttention blockmask taking arbitrary callable ([#174610](https://github.com/pytorch/pytorch/pull/174610))
- [Dynamo] Graph Break on __class__ assignment ([#174761](https://github.com/pytorch/pytorch/pull/174761))
- Fix CUDA memory usage for CPU only compile ([#163841](https://github.com/pytorch/pytorch/pull/163841))
- [dynamo] Fix property setter on MutableMapping subclasses ([#173184](https://github.com/pytorch/pytorch/pull/173184))
- Correctly pass is_inference in the cudagraphs torch.compile backend. ([#174713](https://github.com/pytorch/pytorch/pull/174713))
- Add `TypingVariable.__eq__` ([#174569](https://github.com/pytorch/pytorch/pull/174569))
- [Dynamo] Include var_to_hint_override in FxGraphCache key ([#174805](https://github.com/pytorch/pytorch/pull/174805))
- [dynamo][profiler] Fix corner case while generating prof svg file ([#174909](https://github.com/pytorch/pytorch/pull/174909))
- [dynamo] Add variable builder time in tlparse ([#174908](https://github.com/pytorch/pytorch/pull/174908))
- [dynamo] support self-referentiable lists and dicts ([#173672](https://github.com/pytorch/pytorch/pull/173672))
- [dynamo] don't unconditionally reconstruct list/dict as a potentially self-referential object ([#174498](https://github.com/pytorch/pytorch/pull/174498))
- Cpython test refactor fixes ([#174415](https://github.com/pytorch/pytorch/pull/174415))
- [dynamo] add id check to innermost_fn ([#174335](https://github.com/pytorch/pytorch/pull/174335))
- Nested Comprehension Graph Breaks ([#174413](https://github.com/pytorch/pytorch/pull/174413))
- [dynamo] Skip LazyVT for VTs that anyways realize ([#174901](https://github.com/pytorch/pytorch/pull/174901))
- Refactor Comprehension Graph Break Handling  ([#174694](https://github.com/pytorch/pytorch/pull/174694))
- [dynamo][claude-assisted][BE] Introduce CONSTANT_VARIABLE_NONE singleton for ConstantVariable(None) ([#174728](https://github.com/pytorch/pytorch/pull/174728))
- Disable einops 0.8.2 check on PyTorch ([#175351](https://github.com/pytorch/pytorch/pull/175351))
### security
