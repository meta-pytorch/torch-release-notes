
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
- Extend torch function support to ALL arguments, not just scalar type (but not insides of list) ([#145089](https://github.com/pytorch/pytorch/pull/145089))
### improvements
### bug fixes
- [CUDA-13] Implement workaround for cudaErrorNotSupported ([#162412](https://github.com/pytorch/pytorch/pull/162412))
### performance
### docs
### devs
### Untopiced
- Consolidate stack trace in Tracer ([#156257](https://github.com/pytorch/pytorch/pull/156257))
- fix 'register_foward_pre_hook not supported on ScriptModule' error ([#156904](https://github.com/pytorch/pytorch/pull/156904))
- Fix UnbackedSymint rebinding - check unbacked before renaming ([#156911](https://github.com/pytorch/pytorch/pull/156911))
- [export] Remove stack trace from input/output ([#157302](https://github.com/pytorch/pytorch/pull/157302))
- Back out "Include c++ stack traces when we hit constraint violation (#155603)" ([#157406](https://github.com/pytorch/pytorch/pull/157406))
- [BE][14/16] fix typos in torch/ (torch/fx/) ([#156604](https://github.com/pytorch/pytorch/pull/156604))
- [FP8] FP8 for SwishLayerNorm ([#157574](https://github.com/pytorch/pytorch/pull/157574))
- [dynamic shapes] avoid unnecessary slices ([#157528](https://github.com/pytorch/pytorch/pull/157528))
- Fix DCE eliminating random operations by improving is_impure() (#151524) ([#157981](https://github.com/pytorch/pytorch/pull/157981))
- add eq function to NodeSource ([#158170](https://github.com/pytorch/pytorch/pull/158170))
- make node source hashable ([#158322](https://github.com/pytorch/pytorch/pull/158322))
- cache dict and string rep for better perf ([#158372](https://github.com/pytorch/pytorch/pull/158372))
- [Easy] Fix the format ([#158450](https://github.com/pytorch/pytorch/pull/158450))
- recovering node source from dict (#158373) ([#158473](https://github.com/pytorch/pytorch/pull/158473))
- Shunt fx_interpreter graphmodule print on error into tlparse ([#158469](https://github.com/pytorch/pytorch/pull/158469))
- [dynamic shapes] fix _maybe_evaluate_static axioms bug ([#158672](https://github.com/pytorch/pytorch/pull/158672))
- Extract a method that filters frames in the captured stack trace ([#158266](https://github.com/pytorch/pytorch/pull/158266))
- Add expanded_def option for FX printing, render descriptor, update tests ([#158708](https://github.com/pytorch/pytorch/pull/158708))
- FXConverter handling of generic output in inductor fallback kernel (#159002) ([#159297](https://github.com/pytorch/pytorch/pull/159297))
- remove co_lnotab in favor of co_linetable ([#159227](https://github.com/pytorch/pytorch/pull/159227))
- Fix launch grid calculation ([#159497](https://github.com/pytorch/pytorch/pull/159497))
- remove print ([#159917](https://github.com/pytorch/pytorch/pull/159917))
- [fx][pass] Support converting a float32 tensor to a scalar in FX trace. ([#158216](https://github.com/pytorch/pytorch/pull/158216))
- Correctly copy self.module_stack in ModuleStackTracer ([#159956](https://github.com/pytorch/pytorch/pull/159956))
- [fx] fix split_module with symint ([#160093](https://github.com/pytorch/pytorch/pull/160093))
- Separate provenance tracking to different levels ([#160383](https://github.com/pytorch/pytorch/pull/160383))
- [aoti-fx] Initial AOTInductor FX ([#160765](https://github.com/pytorch/pytorch/pull/160765))
- [aoti-fx] Dynamic shapes support ([#160766](https://github.com/pytorch/pytorch/pull/160766))
- [aoti-fx] Add meta["val"] metadata ([#161019](https://github.com/pytorch/pytorch/pull/161019))
- [tgif] fix getattr_recursive with ModuleList ([#161204](https://github.com/pytorch/pytorch/pull/161204))
- [Inductor-FX] Support custom triton kernels ([#161474](https://github.com/pytorch/pytorch/pull/161474))
- [hop] move insert_deferred_runtime_asserts under subtracer ([#161416](https://github.com/pytorch/pytorch/pull/161416))
- Skip const folding with symbolic expression ([#161437](https://github.com/pytorch/pytorch/pull/161437))
- [fx] Add lru_cache to warning ([#161721](https://github.com/pytorch/pytorch/pull/161721))
- removed duplicate imports ([#161685](https://github.com/pytorch/pytorch/pull/161685))
- Reland "[Fix XPU CI][Inductor UT] Fix test cases broken by community. (#161142)" ([#161949](https://github.com/pytorch/pytorch/pull/161949))
- Support generic dynamic shape with padding ([#160997](https://github.com/pytorch/pytorch/pull/160997))
- stop suggesting using guard_size_oblivious on data dependent errors ([#160510](https://github.com/pytorch/pytorch/pull/160510))
- Prototype for building non-strict leak detector ([#160456](https://github.com/pytorch/pytorch/pull/160456))
- fixed typo error ([#162055](https://github.com/pytorch/pytorch/pull/162055))
- [fx] fix qualified name for methods of torch.Tensor ([#162224](https://github.com/pytorch/pytorch/pull/162224))
- Graph split event tracker ([#159795](https://github.com/pytorch/pytorch/pull/159795))
### not user facing
- python definitely_contiguous-> is_contiguous_or_false ([#156515](https://github.com/pytorch/pytorch/pull/156515))
- [aotd] Support mutations of the same input in fw and bw ([#155354](https://github.com/pytorch/pytorch/pull/155354))
- simplify max(1,x) to x when x known >=1 ([#157189](https://github.com/pytorch/pytorch/pull/157189))
- python definitely_contiguous-> is_contiguous_or_false ([#156515](https://github.com/pytorch/pytorch/pull/156515))
- remove allow-untyped-defs from torch/fx/experimental/migrate_gradual_types/util.py ([#157236](https://github.com/pytorch/pytorch/pull/157236))
- Refactor Provenance Tracking ([#158399](https://github.com/pytorch/pytorch/pull/158399))
- Change from import trace to import config ([#158796](https://github.com/pytorch/pytorch/pull/158796))
- Fix duplicated sources in inductor provenance tracking ([#159484](https://github.com/pytorch/pytorch/pull/159484))
- Output tensor meta data for FX graph node ([#159311](https://github.com/pytorch/pytorch/pull/159311))
- [Dynamo][Better Engineering] Type annotation for `torch/_dynamo/output_graph.py` ([#159602](https://github.com/pytorch/pytorch/pull/159602))
- [Dynamo][Better Engineering] Typing `torch/_dynamo/guards.py` ([#159315](https://github.com/pytorch/pytorch/pull/159315))
- typing debugging.py ([#160364](https://github.com/pytorch/pytorch/pull/160364))
- [Inductor-FX] Support Tensorbox outputs ([#161245](https://github.com/pytorch/pytorch/pull/161245))
- [aoti-fx] Output OpOverload fallbacks ([#161195](https://github.com/pytorch/pytorch/pull/161195))
- [AOTI-FX] Enhance launch grid FloorDiv replacement using sympy.together.  ([#161582](https://github.com/pytorch/pytorch/pull/161582))
- [AOTI-FX] Support registering custom FX backends ([#162317](https://github.com/pytorch/pytorch/pull/162317))
- [fx] fix qualified name for methods of torch.Tensor ([#162407](https://github.com/pytorch/pytorch/pull/162407))
### security
