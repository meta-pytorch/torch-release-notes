
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
- Add is_fx_symbolic_tracing flag ([#161385](https://github.com/pytorch/pytorch/pull/161385))
### improvements
- Fix DCE eliminating random operations by improving is_impure() (#151524) ([#157981](https://github.com/pytorch/pytorch/pull/157981))
- Support converting a float32 tensor to a scalar in FX trace. ([#158216](https://github.com/pytorch/pytorch/pull/158216))
- Correctly copy self.module_stack in ModuleStackTracer ([#159956](https://github.com/pytorch/pytorch/pull/159956))
- Add tool to track events in graph split ([#159795](https://github.com/pytorch/pytorch/pull/159795))
### bug fixes
- Fix split_module with symint ([#160093](https://github.com/pytorch/pytorch/pull/160093))
- Fix `getattr_recursive` with ModuleList ([#161204](https://github.com/pytorch/pytorch/pull/161204))
- Skip const folding with symbolic expression ([#161437](https://github.com/pytorch/pytorch/pull/161437))
- Fix qualified name for methods of torch.Tensor ([#162224](https://github.com/pytorch/pytorch/pull/162224))
### performance
### docs
- Fix typos in torch/ (torch/fx/) ([#156604](https://github.com/pytorch/pytorch/pull/156604))
- Add typing ([#158450](https://github.com/pytorch/pytorch/pull/158450))
- Fix typo ([#162055](https://github.com/pytorch/pytorch/pull/162055))
- Remove allow-untyped-defs from torch/fx/experimental/migrate_gradual_types/util.py ([#157236](https://github.com/pytorch/pytorch/pull/157236))
### devs
- Consolidate stack trace in Tracer ([#156257](https://github.com/pytorch/pytorch/pull/156257), [#157302](https://github.com/pytorch/pytorch/pull/157302), [#158266](https://github.com/pytorch/pytorch/pull/158266))
- Separate provenance tracking to different levels ([#160383](https://github.com/pytorch/pytorch/pull/160383), [#158399](https://github.com/pytorch/pytorch/pull/158399), [#158796](https://github.com/pytorch/pytorch/pull/158796), [#159484](https://github.com/pytorch/pytorch/pull/159484))
- Fix `register_foward_pre_hook not supported on ScriptModule` error ([#156904](https://github.com/pytorch/pytorch/pull/156904))
- Add `__eq__` function to NodeSource ([#158170](https://github.com/pytorch/pytorch/pull/158170))
- Add `__hash__` function to NodeSource ([#158322](https://github.com/pytorch/pytorch/pull/158322))
- Cache dict and string rep for better perf in NodeSource ([#158372](https://github.com/pytorch/pytorch/pull/158372))
- Recover node source from dict (#158373) ([#158473](https://github.com/pytorch/pytorch/pull/158473))
- Include error stacktrace and graph module in tlparse error ([#158469](https://github.com/pytorch/pytorch/pull/158469))
- Add `expanded_def` option for FX printing, render descriptor, update tests ([#158708](https://github.com/pytorch/pytorch/pull/158708))
- Remove `co_lnotab` in favor of `co_linetable` ([#159227](https://github.com/pytorch/pytorch/pull/159227))
- Remove duplicate imports ([#161685](https://github.com/pytorch/pytorch/pull/161685))
- Include Output tensor metadata for CompiledFxGraph ([#159311](https://github.com/pytorch/pytorch/pull/159311))
### Untopiced

### not user facing
### security
