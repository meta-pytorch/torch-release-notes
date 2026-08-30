
# Release Notes worksheet distributed (c10d)

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

## distributed (c10d)
### bc breaking
### deprecation
### new features
### improvements
- Upgrade NCCL to 2.30.7 for CUDA 13.0 and CUDA 13.2 builds ([#187528](https://github.com/pytorch/pytorch/pull/187528))
### bug fixes
- Fix `destroy_process_group()` hanging after collectives run on partially split process groups by keeping group names consistent across ranks ([#190431](https://github.com/pytorch/pytorch/pull/190431))
### performance
- Enable Inductor's `simple_overlap` scheduler pass by default for compiled distributed workloads, moving collective starts earlier and waits later without reordering collectives or increasing peak memory ([#184235](https://github.com/pytorch/pytorch/pull/184235), [#184240](https://github.com/pytorch/pytorch/pull/184240))
### docs
### devs
- Add `split_group` support to the fake process-group backend used for distributed testing ([#186290](https://github.com/pytorch/pytorch/pull/186290))
- Correct `_distributed_c10d.pyi` type stubs for `_create_work_from_future` and the optional `ProcessGroupGloo` timeout argument ([#191633](https://github.com/pytorch/pytorch/pull/191633))
### not user facing
- Add reusable collective, point-to-point, CUDA Graph, and process-group backend test suites ([#190133](https://github.com/pytorch/pytorch/pull/190133))
- Correct spelling and grammar in distributed comments, docstrings, documentation, warnings, and log strings without changing behavior ([#187361](https://github.com/pytorch/pytorch/pull/187361), [#190035](https://github.com/pytorch/pytorch/pull/190035), [#190039](https://github.com/pytorch/pytorch/pull/190039))
### security
