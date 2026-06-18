
# Release Notes worksheet xpu

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

## xpu
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [xpu][refine] Clean up unsed code about oneDNN ([#180531](https://github.com/pytorch/pytorch/pull/180531))
- [XPU] Register XPUPluggableAllocator pybind11 to fix c10::Allocator conversion ([#179392](https://github.com/pytorch/pytorch/pull/179392))
- [xpu][feature] Support fork-safe device_count by pyzes ([#178496](https://github.com/pytorch/pytorch/pull/178496))
- [xpu][fix] Refine oneDNN stride check ([#166861](https://github.com/pytorch/pytorch/pull/166861))
- [xpu][fix] Respect device index -1 for getGlobalIdxFromDevice ([#181361](https://github.com/pytorch/pytorch/pull/181361))
- Clean up CMake related to XPU ([#181355](https://github.com/pytorch/pytorch/pull/181355))
- [xpu][feature] Add torch.xpu.temperature to query GPU temperature ([#181082](https://github.com/pytorch/pytorch/pull/181082))
- Add TraceTracker callback in XPUCachingAllocator ([#180502](https://github.com/pytorch/pytorch/pull/180502))
- [xpu][feature] Add torch.xpu.clock_rate to query GPU frequency ([#183427](https://github.com/pytorch/pytorch/pull/183427))
- [xpu][feature] Add torch.xpu.power_draw to query GPU card power ([#183428](https://github.com/pytorch/pytorch/pull/183428))
- [xpu][feature] Add torch.xpu.utilization to query GPU engine utilization ([#183429](https://github.com/pytorch/pytorch/pull/183429))
- [xpu][feature] Add torch.xpu.memory_usage to query GPU memory bandwidth usage ([#183430](https://github.com/pytorch/pytorch/pull/183430))
- [xpu][feature] Add torch.xpu.device_memory_used to query GPU used device global memory ([#183431](https://github.com/pytorch/pytorch/pull/183431))
- xpu: enable dpclang sycl compiler ([#179763](https://github.com/pytorch/pytorch/pull/179763))
- [xpu][feature] Add is_integrated_gpu to XPU device properties ([#182624](https://github.com/pytorch/pytorch/pull/182624))
- [xpu][feature] Add device-wide synchronization ([#182630](https://github.com/pytorch/pytorch/pull/182630))
- [xpu] Refactor OneDNN C API to C++ API ([#184486](https://github.com/pytorch/pytorch/pull/184486))
- [XPU] Drop SYCL < 2025 version guards ([#185204](https://github.com/pytorch/pytorch/pull/185204))
- xpu: match dpclang SYCL_LIBRARY setting with icpx ([#185571](https://github.com/pytorch/pytorch/pull/185571))
- Add oneDNN LSTM primitive support for XPU inference ([#185531](https://github.com/pytorch/pytorch/pull/185531))
### not user facing
### security
