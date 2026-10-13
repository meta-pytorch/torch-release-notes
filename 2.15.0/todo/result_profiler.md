
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
- Separate allocator-internal trace tags from user metadata ([#193432](https://github.com/pytorch/pytorch/pull/193432))
- Disable addr2line symbolization by default ([#195462](https://github.com/pytorch/pytorch/pull/195462))
### deprecation
### new features
- [CUDA] Capture Python launch stacks for CUDA graphs ([#198419](https://github.com/pytorch/pytorch/pull/198419))
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- Deprecate the profiler's adjust_profiler_step option ([#193042](https://github.com/pytorch/pytorch/pull/193042))
- Rename the CUPTI monitor to Cuspy ([#195881](https://github.com/pytorch/pytorch/pull/195881))
- [Docs] Fix Python comments in profiler example ([#190369](https://github.com/pytorch/pytorch/pull/190369))
- [Profiler] Introduce ProfilerActivityConfig as a way to trigger additional Kineto profilers ([#196065](https://github.com/pytorch/pytorch/pull/196065))
- [Profiler] Introduce CuspyConfig as a way to trigger cuspy without experimental configs ([#196066](https://github.com/pytorch/pytorch/pull/196066))
- Resolve Cuspy annotations by source graph node id in both observers ([#196529](https://github.com/pytorch/pytorch/pull/196529))
- [cuspy] Render GPU-side annotations on the lane their kernels actually draw on (#197354) ([#197354](https://github.com/pytorch/pytorch/pull/197354))
- [Profiler] Remove deprecated metadata json field ([#198265](https://github.com/pytorch/pytorch/pull/198265))
- [Profiler] Remove deprecated experimental config options ([#198262](https://github.com/pytorch/pytorch/pull/198262))
- [Profiler] Add a deprecation warning for profiler's nvprof handlers ([#198396](https://github.com/pytorch/pytorch/pull/198396))
- [Profiler] Add deprecation warning for EventMetadata ([#198405](https://github.com/pytorch/pytorch/pull/198405))
### not user facing
- [profiler][cupti] Turn kernel latency timestamps back off when nothing wants QUEUED ([#192370](https://github.com/pytorch/pytorch/pull/192370))
- [profiler][cupti] Give logical lanes their own reserved id range ([#192393](https://github.com/pytorch/pytorch/pull/192393))
- [profiler][cupti] Stop freeing activity buffers CUPTI may still own ([#195471](https://github.com/pytorch/pytorch/pull/195471))
- [Profiler] Add typed metadata support for kwargs metadata ([#196352](https://github.com/pytorch/pytorch/pull/196352))
- [profiler][cuspy] Use the documented forced flush when a field selection changes ([#196548](https://github.com/pytorch/pytorch/pull/196548))
- [profiler] Fix unlinked runtime/driver events be counted in device time ([#196282](https://github.com/pytorch/pytorch/pull/196282))
- [Profiler] Add a merge rule for Profiler ([#197474](https://github.com/pytorch/pytorch/pull/197474))
- [Profiler] Fix up test_python_export_envelope_matches_kineto  ([#195935](https://github.com/pytorch/pytorch/pull/195935))
- [Profiler] Lint exclusions to prepare for upstreaming ([#198013](https://github.com/pytorch/pytorch/pull/198013))
- [Profiler] Add one more person to the Profiler merge rule ([#198009](https://github.com/pytorch/pytorch/pull/198009))
- [Profiler] Read event idx directly in collection.cpp ([#198665](https://github.com/pytorch/pytorch/pull/198665))
- [Profiler] Simplify how shape handling works in collection.cpp ([#198540](https://github.com/pytorch/pytorch/pull/198540))
- [Profiler] Enable Kineto tests ([#198813](https://github.com/pytorch/pytorch/pull/198813))
- [Profiler] Upstreaming Kineto into Pytorch ([#198648](https://github.com/pytorch/pytorch/pull/198648))
- [profiler][xpu] Test that ac2g CPU->GPU flow arrows end on the device ([#194904](https://github.com/pytorch/pytorch/pull/194904))
- [Profiler] Update Kineto readme ([#199364](https://github.com/pytorch/pytorch/pull/199364))
- [Profiler] Delete unneeded Kineto code ([#199359](https://github.com/pytorch/pytorch/pull/199359))
### security
