
# Release Notes worksheet fx

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

## fx
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
- [fx] Memoize the result expression of symbolic binary arithmetic ([#193219](https://github.com/pytorch/pytorch/pull/193219))
### docs
### devs
### Untopiced
- Lower symbolic bool not to torch.sym_not ([#186043](https://github.com/pytorch/pytorch/pull/186043))
- Fix IndexError in produce_guards for jagged NestedTensor batch dim (#193059) ([#193059](https://github.com/pytorch/pytorch/pull/193059))
- [fx] Skip the record_shapeenv_event prologue when nothing is recorded ([#193161](https://github.com/pytorch/pytorch/pull/193161))
- Fix SymBool equality handling in symbolic shapes ([#186461](https://github.com/pytorch/pytorch/pull/186461))
- [fx] Shallow-copy `from_node` provenance in `NodeSource` instead of deepcopy (#193051) ([#193051](https://github.com/pytorch/pytorch/pull/193051))
- [mtia][inductor] resolve view args of user-defined Triton kernels in FX wrapper (#193820) ([#193820](https://github.com/pytorch/pytorch/pull/193820))
- Fix AOT export GraphModule serialization ([#186418](https://github.com/pytorch/pytorch/pull/186418))
- [fx] Clear fake_mode on a view's base in GraphPickler (#194771) ([#194771](https://github.com/pytorch/pytorch/pull/194771))
- Fix stale float specialization in tensorify_python_scalars (#194976) ([#195040](https://github.com/pytorch/pytorch/pull/195040))
- Improve FX CodeGen process_inputs typing ([#188287](https://github.com/pytorch/pytorch/pull/188287))
- [fx] Fix autowrap_modules type annotation to tuple[ModuleType, ...] ([#195467](https://github.com/pytorch/pytorch/pull/195467))
- [symbolic shapes] Reuse expression symbols during axiom matching ([#195623](https://github.com/pytorch/pytorch/pull/195623))
- Keep saved-activation strides symbolic under dynamic shapes ([#194420](https://github.com/pytorch/pytorch/pull/194420))
- [dynamo] Preserve activation memory budgets across graph breaks ([#194808](https://github.com/pytorch/pytorch/pull/194808))
- [dynamo] Fix canonicalize_output_graph_node_order dropping inference_mode ([#195518](https://github.com/pytorch/pytorch/pull/195518))
- Fix printing an FX graph whose meta carries a BSR or BSC tensor ([#195253](https://github.com/pytorch/pytorch/pull/195253))
- Add scaled addmm functional and in-place APIs ([#195409](https://github.com/pytorch/pytorch/pull/195409))
- [dynamo] Allow partial regional memory budget coverage ([#195932](https://github.com/pytorch/pytorch/pull/195932))
- [FakeTensor] Support sparse compressed tensor ctors ([#192091](https://github.com/pytorch/pytorch/pull/192091))
- [model_extractor][recompile_fix] Repair int32 repeat inputs ([#197035](https://github.com/pytorch/pytorch/pull/197035))
- Fix FX subgraph rewrite of adjacent aggregate matches ([#185365](https://github.com/pytorch/pytorch/pull/185365))
- [FX] Skip fusion discovery for fully supported graphs (#198519) ([#198519](https://github.com/pytorch/pytorch/pull/198519))
- [fx] make update_deps_for_fusions linear in fusion group size (#198654) ([#198654](https://github.com/pytorch/pytorch/pull/198654))
- [symbolic shapes] Restore exact FloorDiv cancellation ([#198575](https://github.com/pytorch/pytorch/pull/198575))
- [Lowering Memory] Don't retain the traced graph in the export leak-detection map (#198295) ([#198295](https://github.com/pytorch/pytorch/pull/198295))
- Fix _sympy_mod crash on plain int operands (#198395) ([#198395](https://github.com/pytorch/pytorch/pull/198395))
- Fix SingletonInt static guard evaluation ([#184628](https://github.com/pytorch/pytorch/pull/184628))
- [inductor] Keep unbacked runtime asserts through selective_decompose ([#199294](https://github.com/pytorch/pytorch/pull/199294))
- [reland][symbolic shapes] Restore exact FloorDiv cancellation (#198575) (#198808) ([#198808](https://github.com/pytorch/pytorch/pull/198808))
- [fx] Don't keep caller frames alive from torch.fx.wrap (#198561) ([#198561](https://github.com/pytorch/pytorch/pull/198561))
- [inductor] Keep unbacked runtime asserts through selective_decompose ([#199294](https://github.com/pytorch/pytorch/pull/199294))
- Prune unused view ops from proxy tensor traces ([#198515](https://github.com/pytorch/pytorch/pull/198515))
### not user facing
- [fx] Skip replace() for a SymNode holding a boolean constant ([#193159](https://github.com/pytorch/pytorch/pull/193159))
- [Testcase Refactoring] Add hw_classification in test/fx/test_fx_const_fold.py ([#192455](https://github.com/pytorch/pytorch/pull/192455))
- [Testcase Refactoring] Add hw_classification in test/test_fx_reinplace_pass.py ([#192470](https://github.com/pytorch/pytorch/pull/192470))
- [Testcase Refactoring] Add hw_classification in test/test_fx_passes.py ([#192450](https://github.com/pytorch/pytorch/pull/192450))
- [Testcase Refactoring] Add hw_classification in test/test_fx_gragh_print.py ([#192451](https://github.com/pytorch/pytorch/pull/192451))
- [Testcase Refactoring] Add hw_classification in test/fx/test_fx_split.py ([#193274](https://github.com/pytorch/pytorch/pull/193274))
- [Testcase Refactoring] Classify pre-grad FX pass tests by hardware ([#192929](https://github.com/pytorch/pytorch/pull/192929))
- [Testcase Refactoring] Add hw_classification in test/fx/test_fx_traceback.py ([#194857](https://github.com/pytorch/pytorch/pull/194857))
- [Testcase Refactoring] Add hw_classification in test/fx/test_fx_xform_observer.py ([#194879](https://github.com/pytorch/pytorch/pull/194879))
- Make tensor device observations rank-portable under compile_on_one_rank ([#196151](https://github.com/pytorch/pytorch/pull/196151))
- [FX splitter] Make fusion discovery deterministic (#198684) ([#198684](https://github.com/pytorch/pytorch/pull/198684))
- Fix shape inference symbol key mismatch with ShapeEnv global symbol names ([#197491](https://github.com/pytorch/pytorch/pull/197491))
- [Testcase Refactoring] Add hw_classification in test/test_fx.py ([#192742](https://github.com/pytorch/pytorch/pull/192742))
### security
