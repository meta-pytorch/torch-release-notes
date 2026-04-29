
# Release Notes worksheet quantization

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

## quantization
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- Fix activation quantization creating duplicate backward placeholders ([#180287](https://github.com/pytorch/pytorch/pull/180287))
### performance
### docs
### devs
### Untopiced
### not user facing
- Remove unused suppressions ([#175464](https://github.com/pytorch/pytorch/pull/175464))
- Add do_not_emit_stack_traces config to skip stack trace collection during FX tracing ([#175423](https://github.com/pytorch/pytorch/pull/175423))
- Add pre_grad_pass_timing config for early vs late pre-grad passes ([#177429](https://github.com/pytorch/pytorch/pull/177429))
- [pytorch] address violations of warning unreachable-code-return in aten ([#177795](https://github.com/pytorch/pytorch/pull/177795))
- Remove stale Python comments ([#179106](https://github.com/pytorch/pytorch/pull/179106))
- Add autograd_cache_key to aot_autograd with tests ([#178152](https://github.com/pytorch/pytorch/pull/178152))
- Finish test/onnx and test/quantization assert removal ([#174686](https://github.com/pytorch/pytorch/pull/174686))
- [BE] Add Union/Optional rewrites to optim through special subdirectories ([#176011](https://github.com/pytorch/pytorch/pull/176011))
- [BE] Apply UP007 and 045 to amp - autograd dirs ([#175937](https://github.com/pytorch/pytorch/pull/175937))
- [OrderedDict] Set the correct dict class in UserDefinedDictVariable ([#175979](https://github.com/pytorch/pytorch/pull/175979))
- Remove unused static_inputs_log from aot_autograd.py ([#177428](https://github.com/pytorch/pytorch/pull/177428))
- [inductor] Fix RNG order change caused by reorder_for_locality ([#176842](https://github.com/pytorch/pytorch/pull/176842))
- Create fx_config outside of try_load ([#177847](https://github.com/pytorch/pytorch/pull/177847))
- Move fallback logic for cudagraphs into create_fx_config ([#177850](https://github.com/pytorch/pytorch/pull/177850))
- Remove unused param boxed_forward_device_index from prepare_aot_module_simplified ([#177851](https://github.com/pytorch/pytorch/pull/177851))
- [Docs] Check __all__ exports in coverage to catch decorated callables ([#178410](https://github.com/pytorch/pytorch/pull/178410))
- Avoid decomposing and recomposing CompilerConfigExtra ([#177871](https://github.com/pytorch/pytorch/pull/177871))
- Split prepare_aot_config out of prepare_aot_module_simplified ([#178171](https://github.com/pytorch/pytorch/pull/178171))
- Simplify prepare_aot_config by moving caller-specific logic to prepare_aot_module_simplified ([#178527](https://github.com/pytorch/pytorch/pull/178527))
### security
