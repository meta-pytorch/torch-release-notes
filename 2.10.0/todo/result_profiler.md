
# Release Notes worksheet profiler

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

## profiler
### bc breaking
### deprecation
- [BE] Remove bottleneck ([#163210](https://github.com/pytorch/pytorch/pull/163210))
- [Profiler] Deprecate export_memory_timeline method ([#168036](https://github.com/pytorch/pytorch/pull/168036))
### new features
### improvements
### bug fixes
### performance
### docs
- [Profiler] Add Documentation for FunctionEvent ([#167688](https://github.com/pytorch/pytorch/pull/167688))
### devs
### Untopiced
- [RecordFunction] Add Scope for Record Function Fast ([#162661](https://github.com/pytorch/pytorch/pull/162661))
- Expose Kineto event metadata in PyTorch Profiler events ([#161624](https://github.com/pytorch/pytorch/pull/161624))
- [PyTorch] Add user_metadata display to memory visualizer ([#165939](https://github.com/pytorch/pytorch/pull/165939))
- Add warning for clearing profiler events at the end of each cycle ([#168066](https://github.com/pytorch/pytorch/pull/168066))
- [Profiler][PrivateUse1] Fix ProfilerState typo ('Disable'→'Disabled') and expose PRIVATEUSE1 in ActiveProfilerType ([#169166](https://github.com/pytorch/pytorch/pull/169166))
### not user facing
- Remove old NVTX interface ([#167637](https://github.com/pytorch/pytorch/pull/167637))
### security
