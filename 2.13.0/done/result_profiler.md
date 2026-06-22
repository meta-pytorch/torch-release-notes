
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
### new features
- Profiler/Kineto now emits channel metadata on CUDA backends ([#185968](https://github.com/pytorch/pytorch/pull/185968))

### improvements
- The memory viz tool now more accurately represents GPU footprint when impacted by fragmentation ([#180515](https://github.com/pytorch/pytorch/pull/180515))
- The memory viz tool now aggregates stripes per-pool to improve visualization for large snapshots ([#180613](https://github.com/pytorch/pytorch/pull/180613))
- Profiler now also exposes CUDA occupancy metadata as a nested dictionary in the .events() output ([#180275](https://github.com/pytorch/pytorch/pull/180275))

### bug fixes
- Fix an issue where profiler would issue a "Profiler clears events at the end of each cycle" warning even when no cycles are used in the schedule ([#180387](https://github.com/pytorch/pytorch/pull/180387))
- Ensures that Profiler does not keep driving Kineto transitions even when GPU collection has stopped ([#180698](https://github.com/pytorch/pytorch/pull/180698))

### performance

### docs
- Remove references to _KinetoProfile in public docs ([#180672](https://github.com/pytorch/pytorch/pull/180672))

### devs

### Untopiced

### not user facing
- [Profiler] Improve events() <> chrome trace parity test ([#180085](https://github.com/pytorch/pytorch/pull/180085))
- [Profiler] Add ryanzhang22 as a profiler owner ([#180680](https://github.com/pytorch/pytorch/pull/180680))
- Fix profiler event canonicalization with PEP 657 caret lines ([#184275](https://github.com/pytorch/pytorch/pull/184275))
- [profiler] Add channel / channel_type dummy fields to EventMetadata ([#184560](https://github.com/pytorch/pytorch/pull/184560))
- [Profiler] Guard traceActivities() behind USE_KINETO ([#184916](https://github.com/pytorch/pytorch/pull/184916))
- [Profiler] Fix gc test by checking for at least one gc event between bounds ([#186832](https://github.com/pytorch/pytorch/pull/186832))
- Add experimental profiler integration for the CUPTI monitor ([#186037](https://github.com/pytorch/pytorch/pull/186037))
- Update profiler .pyi stub ([#180400](https://github.com/pytorch/pytorch/pull/180400))
- [Profiler] Add trace_only ExperimentalConfig flag to speed up __exit__ ([#184306](https://github.com/pytorch/pytorch/pull/184306))
- [Profiler] Propagate NCCL collective metadata to GPU kernels in Pytho… ([#184637](https://github.com/pytorch/pytorch/pull/184637))
- [Profiler][PrivateUse1] Expose backend name as alias in ProfilerActivity for PrivateUse1 ([#180421](https://github.com/pytorch/pytorch/pull/180421))
- [Profiler][PrivateUse1] Make `PrivateUse1ProfilerRegistry::registerWithKineto()` private to fix data race ([#180332](https://github.com/pytorch/pytorch/pull/180332))
- [profiler] Add profiler chrome trace validator with rules ([#177947](https://github.com/pytorch/pytorch/pull/177947))
- Adds helper function _rename_profiler_activity ([#181652](https://github.com/pytorch/pytorch/pull/181652))
### security
