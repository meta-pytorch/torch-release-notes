
# Release Notes worksheet fx

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.
* Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

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

## fx
### bc breaking
### deprecation
### new features
### improvements
- enable torch.compile for torch._scaled_mm nvfp4 recipe ([#150462](https://github.com/pytorch/pytorch/pull/150462))
### bug fixes
### performance
### docs
### devs
### Untopiced
- Remove warnings on non-buffer tensor constants ([#148483](https://github.com/pytorch/pytorch/pull/148483))
- [Sigmoid] Remove magic method in CapabilityBasedPartitioner ([#149400](https://github.com/pytorch/pytorch/pull/149400))
- [export] Beef up guard_added logs ([#149465](https://github.com/pytorch/pytorch/pull/149465))
- [export] Support python assertion with symints. ([#149444](https://github.com/pytorch/pytorch/pull/149444))
- Fix is_nonzero for more than one elem tensors ([#149637](https://github.com/pytorch/pytorch/pull/149637))
- Demote logger of runtime_asserts_frozen to be fired only on debug mode ([#149832](https://github.com/pytorch/pytorch/pull/149832))
- Improve error handling when checking CUDA version in case nvcc is not found ([#148671](https://github.com/pytorch/pytorch/pull/148671))
- [dynamic shapes] C++ bindings for guard_or_false/true ([#150148](https://github.com/pytorch/pytorch/pull/150148))
- Suppress more warnings ([#149833](https://github.com/pytorch/pytorch/pull/149833))
- Remove unused rand call if not fallback to eager for rand ([#147790](https://github.com/pytorch/pytorch/pull/147790))
- [dynamic shapes] allow duck typing for 0/1 ([#150222](https://github.com/pytorch/pytorch/pull/150222))
- Fix codegen, change str comparison opeator to == for proper equality … ([#150611](https://github.com/pytorch/pytorch/pull/150611))
- [MTIA] Map names to operand indices when folding submodules ([#150692](https://github.com/pytorch/pytorch/pull/150692))
- support backed_size_oblivious in guard_or_false/guard_or_true ([#150231](https://github.com/pytorch/pytorch/pull/150231))
- Fix issue in optimized_add issue: make_optimized should be called on non args only  ([#150955](https://github.com/pytorch/pytorch/pull/150955))
- [dynamic shapes] add sym_and, sym_or ([#150456](https://github.com/pytorch/pytorch/pull/150456))
- [Export] fix automatically convert instances of _check(u>=0) to check_is_size() ([#148844](https://github.com/pytorch/pytorch/pull/148844))
- Fix has_free_symbols ([#151492](https://github.com/pytorch/pytorch/pull/151492))
- Support C++ statically_known_true ([#151346](https://github.com/pytorch/pytorch/pull/151346))
- Don't specialize min/max ([#151347](https://github.com/pytorch/pytorch/pull/151347))
- Do not do proper const fold during tensorify_python_scalars ([#151494](https://github.com/pytorch/pytorch/pull/151494))
- [fx] Filter stacktrace ([#151029](https://github.com/pytorch/pytorch/pull/151029))
- [torch][fx] Add support for EXIR dialect overload ops in normalize_function ([#143689](https://github.com/pytorch/pytorch/pull/143689))
- [dynamic shapes] bound_sympy for size-oblivious min/max reasoning ([#151242](https://github.com/pytorch/pytorch/pull/151242))
- [dynamic shapes] be less aggressive with runtime assert CSE for bounds ([#151590](https://github.com/pytorch/pytorch/pull/151590))
- Adding fbgemm to whitelist ([#152079](https://github.com/pytorch/pytorch/pull/152079))
- [Typing] Enable torch.types.IntLikeType / FloatLikeType / BoolLikeType ([#152157](https://github.com/pytorch/pytorch/pull/152157))
- [ez][export] suggest torch._checks only for booleans ([#152499](https://github.com/pytorch/pytorch/pull/152499))
- [export][function schema] support exporting hop with function schema argument ([#152073](https://github.com/pytorch/pytorch/pull/152073))
- [Minimizer] Fix the path naming ([#153130](https://github.com/pytorch/pytorch/pull/153130))
- [dynamic shapes] guard_or_false for infer_size ([#152146](https://github.com/pytorch/pytorch/pull/152146))
- [2/n][Optimus][Auto-AC] Support activation quantization with scaling ([#151770](https://github.com/pytorch/pytorch/pull/151770))
- [export] Flatten frame local logs ([#153627](https://github.com/pytorch/pytorch/pull/153627))
- [dynamic shapes] simplify int(x / y) pattern ([#153477](https://github.com/pytorch/pytorch/pull/153477))
- add graph_code_verbose_log artifact for fx passes ([#153775](https://github.com/pytorch/pytorch/pull/153775))
- [Minimizer] Gracefully exit when there is no discrepancy in block mode ([#154076](https://github.com/pytorch/pytorch/pull/154076))
- change guard_or impl for better perf and simplicity ([#153674](https://github.com/pytorch/pytorch/pull/153674))
- [draft export] skip when no LOC found ([#154190](https://github.com/pytorch/pytorch/pull/154190))
- [EASY] remove guard_size_oblivious from is_nonzero proxy call check ([#154164](https://github.com/pytorch/pytorch/pull/154164))
- [ez] Add docblock for resolve_unbacked_bindings ([#154374](https://github.com/pytorch/pytorch/pull/154374))
- [ez] add docblock for is_accessor_node ([#154375](https://github.com/pytorch/pytorch/pull/154375))
- [ez] add docblock for _sympy_from_args ([#154376](https://github.com/pytorch/pytorch/pull/154376))
- [ez] remove unused function _constrain_symbol_range ([#154386](https://github.com/pytorch/pytorch/pull/154386))
- [ez] add docblock for RuntimeAssert ([#154401](https://github.com/pytorch/pytorch/pull/154401))
- [ez] add docblock for _suggest_torch_checks ([#154404](https://github.com/pytorch/pytorch/pull/154404))
- [ez] add docblock for _remove_effect_token_unbacked_bindings ([#154405](https://github.com/pytorch/pytorch/pull/154405))
- [ez] add docblock for _iterate_exprs ([#154377](https://github.com/pytorch/pytorch/pull/154377))
- [ez] add docblock for free_symbols ([#154378](https://github.com/pytorch/pytorch/pull/154378))
- [ez] add docblock for free_unbacked_symbols ([#154379](https://github.com/pytorch/pytorch/pull/154379))
- [ez] add docblock to is_symbol_binding_fx_node ([#154380](https://github.com/pytorch/pytorch/pull/154380))
- [ez] add docblock for find_symbol_binding_fx_nodes ([#154381](https://github.com/pytorch/pytorch/pull/154381))
- [ez] add docblock for _free_unbacked_symbols_with_path ([#154383](https://github.com/pytorch/pytorch/pull/154383))
- [ez] add docblock for _guard_or ([#154384](https://github.com/pytorch/pytorch/pull/154384))
- [ez] add docblock for guard_scalar ([#154385](https://github.com/pytorch/pytorch/pull/154385))
- [ez] add docblock for _ShapeGuardPrinter ([#154402](https://github.com/pytorch/pytorch/pull/154402))
- [ez] add docblock for ShapeGuardPythonPrinter ([#154403](https://github.com/pytorch/pytorch/pull/154403))
- [ez] add docblock to cast_symbool_to_symint_guardless ([#154400](https://github.com/pytorch/pytorch/pull/154400))
- add docblock for _fast_expand ([#154398](https://github.com/pytorch/pytorch/pull/154398))
- Add docblock for TrackedFake ([#154396](https://github.com/pytorch/pytorch/pull/154396))
- [ez] add docblock for _eval_is_non_overlapping_and_dense ([#154399](https://github.com/pytorch/pytorch/pull/154399))
- [ez] add docblock for _expandsums ([#154397](https://github.com/pytorch/pytorch/pull/154397))
- Add __main__ guards to fx tests ([#154715](https://github.com/pytorch/pytorch/pull/154715))
- [typo] Fix 'intialize' -> 'initialize' in proxy_tensor.py ([#155301](https://github.com/pytorch/pytorch/pull/155301))
- [reland] Add stack_trace on make_fx ([#155486](https://github.com/pytorch/pytorch/pull/155486))
- [export] Allow user frame to be None when symbolic shape tries to get stacktrace. ([#155744](https://github.com/pytorch/pytorch/pull/155744))
- [export] Add meta[val] to getattr nodes ([#154934](https://github.com/pytorch/pytorch/pull/154934))
- fix error message on specialization with Dim.DYNAMIC ([#155738](https://github.com/pytorch/pytorch/pull/155738))
### not user facing
- [Partitioner] Reduce time consuming of partitions merger ([#146582](https://github.com/pytorch/pytorch/pull/146582))
- [Partitioner] Remove unnecessary upstream nodes in dependency viewer ([#146580](https://github.com/pytorch/pytorch/pull/146580))
- Refactor layout constraint selection logic ([#148104](https://github.com/pytorch/pytorch/pull/148104))
- [ez] Make relaxed constraint error message more user friendly ([#151407](https://github.com/pytorch/pytorch/pull/151407))
- [ez] Make relaxed constraint error message more user friendly ([#151407](https://github.com/pytorch/pytorch/pull/151407))
- Do not log exception when recording is disabled or already recording ([#151038](https://github.com/pytorch/pytorch/pull/151038))
- Log information about suppressed data dependent errors ([#151041](https://github.com/pytorch/pytorch/pull/151041))
- Do not log exception when recording is disabled or already recording ([#151038](https://github.com/pytorch/pytorch/pull/151038))
- Log information about suppressed data dependent errors ([#151041](https://github.com/pytorch/pytorch/pull/151041))
- [ez] Make relaxed constraint error message more user friendly ([#151407](https://github.com/pytorch/pytorch/pull/151407))
- [ez] fix grammar mistakes in StatefulSymbolicContext comment ([#152598](https://github.com/pytorch/pytorch/pull/152598))
- Refactor layout constraint selection logic ([#148104](https://github.com/pytorch/pytorch/pull/148104))
- [fx] Recursive DCE on subgraphs ([#152772](https://github.com/pytorch/pytorch/pull/152772))
- [invoke_subgraph] Run missing graph passes recursively ([#152675](https://github.com/pytorch/pytorch/pull/152675))
- Improve cache key graph printing performance ([#151928](https://github.com/pytorch/pytorch/pull/151928))
- Thread through options so GraphPickler can allow all ops ([#152801](https://github.com/pytorch/pytorch/pull/152801))
- Fix evaluate_expr to include suppress_guards_tls in cache key ([#152661](https://github.com/pytorch/pytorch/pull/152661))
- include user stacks with constraint violation error message ([#152924](https://github.com/pytorch/pytorch/pull/152924))
- Introduce statically_known_false ([#154291](https://github.com/pytorch/pytorch/pull/154291))
- check fallback_value first.  ([#154493](https://github.com/pytorch/pytorch/pull/154493))
- [BE][Ez]: Optimize unnecessary lambda with operator ([#154722](https://github.com/pytorch/pytorch/pull/154722))
- Include c++ stack traces when we hit constraint violation ([#155603](https://github.com/pytorch/pytorch/pull/155603))
- Migrate from lru_cache to cache ([#155613](https://github.com/pytorch/pytorch/pull/155613))
- Fix provenance unit test ([#155747](https://github.com/pytorch/pytorch/pull/155747))
- Fix logging of failed tensorified ops ([#155982](https://github.com/pytorch/pytorch/pull/155982))
- [BE][PYFMT] migrate PYFMT for `torch/[e-n]*/` to `ruff format` ([#144553](https://github.com/pytorch/pytorch/pull/144553))
- remove allow-untyped-defs from torch/fx/passes/utils/fuser_utils.py ([#156538](https://github.com/pytorch/pytorch/pull/156538))
- [aotd] Support mutations of the same input in fw and bw ([#155354](https://github.com/pytorch/pytorch/pull/155354))
### security
