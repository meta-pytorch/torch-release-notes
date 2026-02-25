
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
- [xpu][feature] [1/6] Add trace support on XPU caching allocator ([#168262](https://github.com/pytorch/pytorch/pull/168262))
- [xpu][feature] [2/6] Track stack context for xpu caching allocator ([#169280](https://github.com/pytorch/pytorch/pull/169280))
- [xpu][feature] [3/6] Add snapshot support on XPU caching allocator ([#169203](https://github.com/pytorch/pytorch/pull/169203))
- [xpu][feature] Introduce some additional metrics for memory stats of XPU caching allocator ([#169812](https://github.com/pytorch/pytorch/pull/169812))
- Optimizes the performance of the int_mm which mat2 tensor is non-contiguous on Intel GPU ([#169555](https://github.com/pytorch/pytorch/pull/169555))
- [xpu][feature]Fallbacks memory efficient attention to math attention on XPU ([#166936](https://github.com/pytorch/pytorch/pull/166936))
- [xpu][feature] Add skip actions support to filter out memory trace ([#170760](https://github.com/pytorch/pytorch/pull/170760))
- Support torch.accelerator.get_device_capability on XPU ([#170747](https://github.com/pytorch/pytorch/pull/170747))
- [xpu][fix] Use small pool for 1MB allocation ([#171453](https://github.com/pytorch/pytorch/pull/171453))
- [xpu][feature] [4/6] Introduce record memory history for XPU in cpp part ([#169296](https://github.com/pytorch/pytorch/pull/169296))
- [xpu][feature] [5/6] Introduce memory snapshot for XPU in frontend part ([#169442](https://github.com/pytorch/pytorch/pull/169442))
- [xpu][feature] [6/6] Introduce _record_memory_history for XPU in frontend part ([#169559](https://github.com/pytorch/pytorch/pull/169559))
- [xpu][fix] Fix wrong signature on XPU memory docs ([#172933](https://github.com/pytorch/pytorch/pull/172933))
- [xpu][utils] Add a helper function to XPU for code reuse ([#173333](https://github.com/pytorch/pytorch/pull/173333))
- The frontend python APIs for XPUGraph capture/replay etc. ([#174046](https://github.com/pytorch/pytorch/pull/174046))
- [xpu][feature] Add local_mem_size to XPU device property ([#172314](https://github.com/pytorch/pytorch/pull/172314))
### not user facing
- [xpu][test][FlexAttention]Enable the test_GQA on Intel XPU ([#166376](https://github.com/pytorch/pytorch/pull/166376))
- xpu: add a test to verify all torch xpu libraries are linked on Linux ([#169322](https://github.com/pytorch/pytorch/pull/169322))
### security
