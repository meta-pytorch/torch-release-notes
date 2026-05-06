
# Release Notes worksheet profiler

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

## profiler
### bc breaking
### deprecation
- Profiler's metadata_json field is now deprecated, use event_metadata instead. ([#179417](https://github.com/pytorch/pytorch/pull/179417))
### new features
- Profiler's Activity selection allows for fine-grained activity type selection. ([#176351](https://github.com/pytorch/pytorch/pull/176351))
- Memory visualize has a new tab to show private pool memory view ([#177289](https://github.com/pytorch/pytorch/pull/177289))
### improvements
- Profiler's events() method now has parity with information returned in export_chrome_trace(). ([#177662](https://github.com/pytorch/pytorch/pull/177662), [#177888](https://github.com/pytorch/pytorch/pull/177888), [#178168](https://github.com/pytorch/pytorch/pull/178168), [#178597](https://github.com/pytorch/pytorch/pull/178597), [#178901](https://github.com/pytorch/pytorch/pull/178901), [#179714](https://github.com/pytorch/pytorch/pull/179714))
### bug fixes
### performance
### docs
### devs
### Untopiced
### not user facing
- [profiler] Make ValueCache per-thread for free-threaded Python safety ([#178552](https://github.com/pytorch/pytorch/pull/178552))
- [profiler] Fix thread-safety of PyEval_SetProfile for free-threaded Python ([#178551](https://github.com/pytorch/pytorch/pull/178551))
- [Profiler] Add priority key to EventsMetadata ([#180100](https://github.com/pytorch/pytorch/pull/180100))
- privateuse1 backend integration with kineto ([#172154](https://github.com/pytorch/pytorch/pull/172154))
- [pytorch][profiler] Emit Input Strides metadata regardless of record_concrete_inputs setting (#176823) ([#176823](https://github.com/pytorch/pytorch/pull/176823))
- [Profiler] Add a test to validate kernel metadata is present in output ([#177745](https://github.com/pytorch/pytorch/pull/177745))
- [Profiler] Bump kineto submodule hash ([#178286](https://github.com/pytorch/pytorch/pull/178286))
- [Profiler] Some code cleanup ([#178266](https://github.com/pytorch/pytorch/pull/178266))
- [profiler] Acquire GIL in PythonTracer destructor before Py_XDECREF ([#178830](https://github.com/pytorch/pytorch/pull/178830))
- [Profiler] Reduce size of the payload used in test_profiler_name_pattern ([#179626](https://github.com/pytorch/pytorch/pull/179626))
- [Profiler] Fix profiler test_kineto_kernel_metadata_in_trace on ROCm machines ([#179815](https://github.com/pytorch/pytorch/pull/179815))
### security
