
# Release Notes worksheet quantization

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

## quantization
### bc breaking
### deprecation
### new features
- Add scaled_grouped_mm_v2 and python API ([#165154](https://github.com/pytorch/pytorch/pull/165154))
### improvements
### bug fixes
### performance
### docs
- [BE] document some quantization public apis ([#165160](https://github.com/pytorch/pytorch/pull/165160))
### devs
### Untopiced
- [torchao][pt2e] Make prepare and convert faster by caching ([#162550](https://github.com/pytorch/pytorch/pull/162550))
- bf16 support for fused_moving_avg_obs_fake_quant() op ([#162620](https://github.com/pytorch/pytorch/pull/162620))
- remove allow-untyped-defs from ./torch/ao/quantization/pt2e/duplicate_dq_pass.py ([#163470](https://github.com/pytorch/pytorch/pull/163470))
- [6/n] Quantization with min & max bounds support - using fbgemm changes in ATen ([#162924](https://github.com/pytorch/pytorch/pull/162924))
- [Fix] Adding missing `f` prefixes to formatted strings [2/N] ([#164066](https://github.com/pytorch/pytorch/pull/164066))
- half support for fused_moving_avg_obs_fake_quant() op ([#164175](https://github.com/pytorch/pytorch/pull/164175))
- [1/N] Simplify "in" operation for containers of a single item ([#164224](https://github.com/pytorch/pytorch/pull/164224))
- [1/N] Fix clang-tidy readability checks ([#164561](https://github.com/pytorch/pytorch/pull/164561))
- Add _scaled_mm_v2 API ([#164141](https://github.com/pytorch/pytorch/pull/164141))
- [7/N] Apply ruff UP035 rule  ([#164653](https://github.com/pytorch/pytorch/pull/164653))
- bf16 support for fake_quantize_learnable_per_channel_affine ([#165098](https://github.com/pytorch/pytorch/pull/165098))
- Remove unnecessary "static" for definitions in anonymous namespace ([#165035](https://github.com/pytorch/pytorch/pull/165035))
- bf16 support for per_channel bwd ([#165325](https://github.com/pytorch/pytorch/pull/165325))
- add the option to disable functionalization in AOTDispatcher ([#164577](https://github.com/pytorch/pytorch/pull/164577))
- bf16 support for per tensor backward ([#165362](https://github.com/pytorch/pytorch/pull/165362))
- Enable PLC1802 on ruff ([#165813](https://github.com/pytorch/pytorch/pull/165813))
- Add NVFP4 two-level scaling to scaled_mm ([#165774](https://github.com/pytorch/pytorch/pull/165774))
- [Code Clean]Replace assert statements with explicit if/raise patterns ([#165735](https://github.com/pytorch/pytorch/pull/165735))
- Enable PLC0414 on ruff ([#165828](https://github.com/pytorch/pytorch/pull/165828))
- Fix pyrelfy ignore syntax in distributions and ao ([#166248](https://github.com/pytorch/pytorch/pull/166248))
- Fix existing pyrefly errors on main ([#166312](https://github.com/pytorch/pytorch/pull/166312))
- Remove clang-tidy type conversion suppressions ([#166398](https://github.com/pytorch/pytorch/pull/166398))
- [ao][pruning] Replace assert statements with AssertionError exceptions ([#164926](https://github.com/pytorch/pytorch/pull/164926))
- Add MXFP4 grouped gemm support via. FBGEMM kernels ([#166530](https://github.com/pytorch/pytorch/pull/166530))
- [5/N] Use key in dict for existence checks ([#167311](https://github.com/pytorch/pytorch/pull/167311))
- [3/N] Use Python 3.10 typing ([#167431](https://github.com/pytorch/pytorch/pull/167431))
- Replace 2**31 with explicit int ([#168046](https://github.com/pytorch/pytorch/pull/168046))
- [1/N] Use TYPE_CHECKING  ([#165852](https://github.com/pytorch/pytorch/pull/165852))
- [CPU] add onednn context cache for qlinear to improve performance ([#168150](https://github.com/pytorch/pytorch/pull/168150))
- [Quant][CPU] fix fp8 qconv ([#167611](https://github.com/pytorch/pytorch/pull/167611))
- [BE] Add missing method docstrings for pytorch quantization classes ([#165199](https://github.com/pytorch/pytorch/pull/165199))
- [4/N] Use context managers ([#169169](https://github.com/pytorch/pytorch/pull/169169))
- make the float4 dtype support equality comparisons ([#169575](https://github.com/pytorch/pytorch/pull/169575))
- add copy_ support for float4 dtype ([#169595](https://github.com/pytorch/pytorch/pull/169595))
### not user facing
- [Precompile] [RFC] Implement aot_compile_module ([#162171](https://github.com/pytorch/pytorch/pull/162171))
- [BE] Make PyObjectSlot use a global PyInterpreter ([#162659](https://github.com/pytorch/pytorch/pull/162659))
- Allow aot_module_simplified to return a serializable output ([#162527](https://github.com/pytorch/pytorch/pull/162527))
- [BE] Make PyObjectSlot use a global PyInterpreter ([#162659](https://github.com/pytorch/pytorch/pull/162659))
- [testing] Add test owner labels for some ao sparse tests ([#163203](https://github.com/pytorch/pytorch/pull/163203))
- remove allow-untyped-defs from ./torch/ao/quantization/quantizer/utils.py ([#163471](https://github.com/pytorch/pytorch/pull/163471))
- [BE] Make PyObjectSlot use a global PyInterpreter ([#162659](https://github.com/pytorch/pytorch/pull/162659))
- Fix overflow in slow_conv3d when kernel size is too large. ([#162718](https://github.com/pytorch/pytorch/pull/162718))
- [1/N] Apply UP035 rule in tests ([#163947](https://github.com/pytorch/pytorch/pull/163947))
- [Fix] Adding missing `f` prefixes to formatted strings [4/N] ([#164068](https://github.com/pytorch/pytorch/pull/164068))
- [dynamo, 3.14] support some bytecodes, fix CALL_FUNCTION_EX ([#163009](https://github.com/pytorch/pytorch/pull/163009))
- Split scaled-mm tests into separate file ([#164266](https://github.com/pytorch/pytorch/pull/164266))
- Use torch.testing.test_close instead of torch.testing.test_allclose ([#164539](https://github.com/pytorch/pytorch/pull/164539))
- move fw|bw compiler args in aot joint with descriptors ([#164584](https://github.com/pytorch/pytorch/pull/164584))
- move partition and compiler fns from stage 1 to stage 2 ([#164765](https://github.com/pytorch/pytorch/pull/164765))
- Update round size with 1 division behavior ([#162203](https://github.com/pytorch/pytorch/pull/162203))
- Mark unused parameters in C++ code ([#164912](https://github.com/pytorch/pytorch/pull/164912))
- Refactor _scaled_grouped_mm_cuda dispatch ([#165060](https://github.com/pytorch/pytorch/pull/165060))
- [test] Skip testing of source_fn_stack in light of export changes ([#165176](https://github.com/pytorch/pytorch/pull/165176))
- [RFC] Add pyrefly to lintrunner ([#165179](https://github.com/pytorch/pytorch/pull/165179))
- [Code Clean] Clean asserts in torch/ao/quantization (root, quantizer, backend_config) ([#165433](https://github.com/pytorch/pytorch/pull/165433))
- [Code Clean] Clean asserts in torch/ao/quantization/experimental/* and torch/ao/quantization/pt2e/* ([#165317](https://github.com/pytorch/pytorch/pull/165317))
- [2/N][Fix] Fix typo in test folder  ([#166374](https://github.com/pytorch/pytorch/pull/166374))
- [Code Clean] Clean asserts in torch/ao/quantization/fx/* ([#165420](https://github.com/pytorch/pytorch/pull/165420))
- [4/N] Remove unused loop variables in tests ([#166690](https://github.com/pytorch/pytorch/pull/166690))
- [5/N] Remove unused loop variables in tests  ([#166716](https://github.com/pytorch/pytorch/pull/166716))
- Correctly use test parameters ([#166726](https://github.com/pytorch/pytorch/pull/166726))
- [3/N] Use 'is' in callable comparisons ([#166780](https://github.com/pytorch/pytorch/pull/166780))
- [export] Fix static_input_indices for aot_export_joint ([#166761](https://github.com/pytorch/pytorch/pull/166761))
- [6/N] Remove unused loop variables in tests ([#166785](https://github.com/pytorch/pytorch/pull/166785))
- [Code Clean] Clean asserts in torch/ao/quantization (root, quantizer, backend_config) ([#165433](https://github.com/pytorch/pytorch/pull/165433))
- [7/N] Fix unused loop variables in tests ([#167043](https://github.com/pytorch/pytorch/pull/167043))
- [8/N] Fix unused loop variables in tests ([#166921](https://github.com/pytorch/pytorch/pull/166921))
- [opaque obj] Allow non-effectful scriptobjs ([#163714](https://github.com/pytorch/pytorch/pull/163714))
- Add Pylint checks to linterrunner ([#167421](https://github.com/pytorch/pytorch/pull/167421))
- [Code Clean] Better error handling in  aten/src/ATen/native/* and aten/src/ATen/mkl/Exceptions.h ([#165290](https://github.com/pytorch/pytorch/pull/165290))
- [BE][1/6] fix typos in test/ ([#157635](https://github.com/pytorch/pytorch/pull/157635))
- Re-enable torch.compile tests for Python 3.12 and Windows ([#169387](https://github.com/pytorch/pytorch/pull/169387))
- Re-enable torch.compile tests for Python 3.12 and Windows ([#169387](https://github.com/pytorch/pytorch/pull/169387))
- Fix remaining Pylint W0143 warnings ([#167421](https://github.com/pytorch/pytorch/pull/167421))
### security
