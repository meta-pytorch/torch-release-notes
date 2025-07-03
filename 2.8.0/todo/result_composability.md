
# Release Notes worksheet composability

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

## composability
### bc breaking
### deprecation
### new features
### improvements
- Allow duck typing for 0/1 ([#150222](https://github.com/pytorch/pytorch/pull/150222))
### bug fixes
- Custom Op handle 1-element tuples ([#155447](https://github.com/pytorch/pytorch/pull/155447))
### performance
### docs
- Add docblock for resolve_unbacked_bindings ([#154374](https://github.com/pytorch/pytorch/pull/154374))
- Add docblock for is_accessor_node ([#154375](https://github.com/pytorch/pytorch/pull/154375))
- Add docblock for _sympy_from_args ([#154376](https://github.com/pytorch/pytorch/pull/154376))
- Remove _constrain_symbol_range ([#154386](https://github.com/pytorch/pytorch/pull/154386))
- Add docblock for RuntimeAssert ([#154401](https://github.com/pytorch/pytorch/pull/154401))
- Add docblock for _suggest_torch_checks ([#154404](https://github.com/pytorch/pytorch/pull/154404))
- Add docblock for _remove_effect_token_unbacked_bindings ([#154405](https://github.com/pytorch/pytorch/pull/154405))
- Add docblock for _iterate_exprs ([#154377](https://github.com/pytorch/pytorch/pull/154377))
- Add docblock for free_symbols ([#154378](https://github.com/pytorch/pytorch/pull/154378))
- Add docblock for free_unbacked_symbols ([#154379](https://github.com/pytorch/pytorch/pull/154379))
- Add docblock to is_symbol_binding_fx_node ([#154380](https://github.com/pytorch/pytorch/pull/154380))
- Add docblock for find_symbol_binding_fx_nodes ([#154381](https://github.com/pytorch/pytorch/pull/154381))
- Add docblock for _free_unbacked_symbols_with_path ([#154383](https://github.com/pytorch/pytorch/pull/154383))
- Add docblock for _guard_or ([#154384](https://github.com/pytorch/pytorch/pull/154384))
- Add docblock for guard_scalar ([#154385](https://github.com/pytorch/pytorch/pull/154385))
- Add docblock for _ShapeGuardPrinter ([#154402](https://github.com/pytorch/pytorch/pull/154402))
- Add docblock for ShapeGuardPythonPrinter ([#154403](https://github.com/pytorch/pytorch/pull/154403))
- Add docblock to cast_symbool_to_symint_guardless ([#154400](https://github.com/pytorch/pytorch/pull/154400))
- add docblock for _fast_expand ([#154398](https://github.com/pytorch/pytorch/pull/154398))
- Add docblock for TrackedFake ([#154396](https://github.com/pytorch/pytorch/pull/154396))
- Add docblock for _eval_is_non_overlapping_and_dense ([#154399](https://github.com/pytorch/pytorch/pull/154399))
- Add docblock for _expandsums ([#154397](https://github.com/pytorch/pytorch/pull/154397))
- Enable torch.types.IntLikeType / FloatLikeType / BoolLikeType ([#152157](https://github.com/pytorch/pytorch/pull/152157))
- Fix grammar mistakes in StatefulSymbolicContext comment ([#152598](https://github.com/pytorch/pytorch/pull/152598))

### devs
- Introduce sym_and, sym_or ([#150456](https://github.com/pytorch/pytorch/pull/150456))
- Support statically_known_true in C++ ([#151346](https://github.com/pytorch/pytorch/pull/151346))
- Add C++ bindings for guard_or_false/true ([#150148](https://github.com/pytorch/pytorch/pull/150148))
- Introduce statically_known_false ([#154291](https://github.com/pytorch/pytorch/pull/154291))
- Don't log exception when recording is disabled or already recording ([#151038](https://github.com/pytorch/pytorch/pull/151038))
- Log suppressed data dependent errors ([#151041](https://github.com/pytorch/pytorch/pull/151041))
- Demote runtime_asserts_frozen logger to debug mode ([#149832](https://github.com/pytorch/pytorch/pull/149832))
- Demote constant registration warnings to debug ([#149833](https://github.com/pytorch/pytorch/pull/149833))

### Untopiced
- Avoid overflow in vector_norm for scalar input ([#144073](https://github.com/pytorch/pytorch/pull/144073))
- [custom ops] Override fake registration ([#150806](https://github.com/pytorch/pytorch/pull/150806))
- Generate meta kernel with operator profiles ([#150807](https://github.com/pytorch/pytorch/pull/150807))
- [dynamic shapes] rewrite expand with guard_or_false ([#150236](https://github.com/pytorch/pytorch/pull/150236))
- Save/load op profiles ([#151817](https://github.com/pytorch/pytorch/pull/151817))
- [dynamic shapes] aten.constant_pad_nd meta impl ([#152129](https://github.com/pytorch/pytorch/pull/152129))
- [dynamic shapes] use try-catch instead of guard_or_true for reshape_view_helper ([#152638](https://github.com/pytorch/pytorch/pull/152638))
- error out on negative offs or on K=0 in group gemm ([#153226](https://github.com/pytorch/pytorch/pull/153226))
- Data dependent free reshape. ([#153198](https://github.com/pytorch/pytorch/pull/153198))
- [dynamic shapes] unbacked safe unsqueeze ([#154087](https://github.com/pytorch/pytorch/pull/154087))
- [dynamic shapes] guard_or_false for cat, repeat ([#155290](https://github.com/pytorch/pytorch/pull/155290))
- [dynamic shapes] skip fused linear path if not definitely contiguous ([#155051](https://github.com/pytorch/pytorch/pull/155051))
- Align meta deducing for fft_r2c with fft_r2c_mkl on XPU ([#156048](https://github.com/pytorch/pytorch/pull/156048))

### not user facing
- fix cuDNN SDPA meta registration ([#148921](https://github.com/pytorch/pytorch/pull/148921))
- Add meta function for out variants of ones,zeros,empty ([#149098](https://github.com/pytorch/pytorch/pull/149098))
- [export] fix stft decomp and making it consistent with cpp impl. ([#149232](https://github.com/pytorch/pytorch/pull/149232))
- Remove aten.elu core ATen decomp because it is now core ATen ([#149780](https://github.com/pytorch/pytorch/pull/149780))
- Fix torch.matmul related out dtype check ([#148174](https://github.com/pytorch/pytorch/pull/148174))
- Fix addbmm & addmv & baddbmm out dtype check ([#148176](https://github.com/pytorch/pytorch/pull/148176))
- Make torch._chunk_cat support non-contiguous inputs ([#151263](https://github.com/pytorch/pytorch/pull/151263))
- [MPSInductor] Fix masked_fill decomp ([#152268](https://github.com/pytorch/pytorch/pull/152268))
- Fix GuardOnDataDependentSymNode in the normalize operator ([#152039](https://github.com/pytorch/pytorch/pull/152039))
- Support using SymInt shapes for torch.baddbmm no-broadcast case ([#153112](https://github.com/pytorch/pytorch/pull/153112))
- Fix `torch.isin` decomposition for scalar inputs ([#153216](https://github.com/pytorch/pytorch/pull/153216))
- Add skip_dtype_check_in_meta_registrations config to torch/fx/experimental/_config ([#153513](https://github.com/pytorch/pytorch/pull/153513))
- Treat dim=[] same as dim=None ([#153570](https://github.com/pytorch/pytorch/pull/153570))
- use definitely_contiguous for _prim_elementwise_meta short circuit ([#153441](https://github.com/pytorch/pytorch/pull/153441))
- Fix clamp type promotion in inductor decomposition ([#154471](https://github.com/pytorch/pytorch/pull/154471))
- avoid sym_max on nested int in is_contiguous.  ([#154633](https://github.com/pytorch/pytorch/pull/154633))
- Symintify baddbmm ([#154656](https://github.com/pytorch/pytorch/pull/154656))
- [refactor] is_known_channels_last_contiguous* -> definitely_channels_last_contiguous* ([#155499](https://github.com/pytorch/pytorch/pull/155499))
- [export] support linear & layer_norm unbacked ([#155260](https://github.com/pytorch/pytorch/pull/155260))
- fix slice w/ dynamic shapes ([#153131](https://github.com/pytorch/pytorch/pull/153131))
- remove allow-untyped-defs from context.py ([#155622](https://github.com/pytorch/pytorch/pull/155622))
- remove gso from vector_norm ([#156530](https://github.com/pytorch/pytorch/pull/156530))


- Update meta kernel for torch._scaled_mm nvfp4 recipe ([#150462](https://github.com/pytorch/pytorch/pull/150462))
- Support backed_size_oblivious in guard_or_false/guard_or_true ([#150231](https://github.com/pytorch/pytorch/pull/150231))
- Fix optimized_add to call make_optimized on non args only  ([#150955](https://github.com/pytorch/pytorch/pull/150955))
- Fix has_free_symbols on sympy.S.true ([#151492](https://github.com/pytorch/pytorch/pull/151492))
- Automatically convert instances of _check(u>=0) to check_is_size() ([#148844](https://github.com/pytorch/pytorch/pull/148844))
- Don't specialize min/max ([#151347](https://github.com/pytorch/pytorch/pull/151347))
- Do not const fold for nodes with no float symbols ([#151494](https://github.com/pytorch/pytorch/pull/151494))
- Use bound_sympy for size-oblivious min/max reasoning ([#151242](https://github.com/pytorch/pytorch/pull/151242))
- Be less aggressive in CSE on bound expressions ([#151590](https://github.com/pytorch/pytorch/pull/151590))
- Suggest torch._checks only for booleans ([#152499](https://github.com/pytorch/pytorch/pull/152499))
- Use guard_or_false for infer_size ([#152146](https://github.com/pytorch/pytorch/pull/152146))
- Simplify int(x / y) pattern ([#153477](https://github.com/pytorch/pytorch/pull/153477))
- Fix guard_or implementation for better perf and simplicity ([#153674](https://github.com/pytorch/pytorch/pull/153674))
- Remove guard_size_oblivious from is_nonzero proxy call check ([#154164](https://github.com/pytorch/pytorch/pull/154164))
- Fix evaluate_expr to include suppress_guards_tls in cache key ([#152661](https://github.com/pytorch/pytorch/pull/152661))
- [aotd] Support mutations of the same input in fw and bw ([#155354](https://github.com/pytorch/pytorch/pull/155354))
- [multigraph] use specializations in compile_and_call_fx_graph ([#153449](https://github.com/pytorch/pytorch/pull/153449))
- Add guard_or_false for computeStorageNbytes ([#150483](https://github.com/pytorch/pytorch/pull/150483))

### security
