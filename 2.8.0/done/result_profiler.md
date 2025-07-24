
# Release Notes worksheet Profiler

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

## Profiler
### bc breaking
### deprecation
### new features
- Add Flag to Toggle Global and Local Callbacks for Annotations ([#154932](https://github.com/pytorch/pytorch/pull/154932))
- Pass Overload Names To Kineto ([#149333](https://github.com/pytorch/pytorch/pull/149333))
- Memory Snapshot On Demand ([#150559](https://github.com/pytorch/pytorch/pull/150559))
- Add PT2 Compile Context to Visualizer ([#152862](https://github.com/pytorch/pytorch/pull/152862))
- Add PT2 to Memory Snapshot ([#152707](https://github.com/pytorch/pytorch/pull/152707))
- Enable `Profiler.key_averages().table()` for HPU devices ([#150770](https://github.com/pytorch/pytorch/pull/150770))

### improvements
- Set Duration to -1 for unfinished CPU events ([#150131](https://github.com/pytorch/pytorch/pull/150131))
- Start at index with most events ([#154571](https://github.com/pytorch/pytorch/pull/154571))
- Remove `compile_context` handle even if `compile_context` not set ([#154664](https://github.com/pytorch/pytorch/pull/154664))
- Remove temp flag for on-demand Memory Snapshot ([#151068](https://github.com/pytorch/pytorch/pull/151068))


### bug fixes
- Fix Empty C Call Queue in Python Tracer ([#150370](https://github.com/pytorch/pytorch/pull/150370))
- Remove Decref From Python Context in Python Tracer ([#151625](https://github.com/pytorch/pytorch/pull/151625))
- Induce Inductor Import before Profiling ([#155243](https://github.com/pytorch/pytorch/pull/155243))
- `CUPTI_LAZY_REINIT` disable skipped for CUDA >= 12.6 ([#151124](https://github.com/pytorch/pytorch/pull/151124))
- Change 'b' to 'B' in FunctionEvent Frontend ([#156250](https://github.com/pytorch/pytorch/pull/156250))
- Enable all configured activities in CUPTI Range Profiler mode ([#154749](https://github.com/pytorch/pytorch/pull/154749))


### performance
### docs
### devs
### Untopiced
### not user facing
### security
