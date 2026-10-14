
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
- Support pruned tables in quantized `embedding_bag` on CUDA ([#194934](https://github.com/pytorch/pytorch/pull/194934))
- Upgrade oneDNN to v3.13 ([#196712](https://github.com/pytorch/pytorch/pull/196712))
### bug fixes
- Fix FX FP16/BF16 linear weight folding `KeyError` for shared weights ([#194292](https://github.com/pytorch/pytorch/pull/194292))
### performance
- Speed up AArch64 small-batch QNNPACK linear 2-4x ([#193595](https://github.com/pytorch/pytorch/pull/193595))
### docs
### devs
### Untopiced
### not user facing
- Annotate, refactor and enable quantization and AO sparsity tests for hardware classification, XPU and out-of-tree backends ([#190889](https://github.com/pytorch/pytorch/pull/190889), [#191200](https://github.com/pytorch/pytorch/pull/191200), [#191202](https://github.com/pytorch/pytorch/pull/191202), [#192479](https://github.com/pytorch/pytorch/pull/192479), [#192636](https://github.com/pytorch/pytorch/pull/192636), [#192964](https://github.com/pytorch/pytorch/pull/192964), [#192965](https://github.com/pytorch/pytorch/pull/192965), [#193000](https://github.com/pytorch/pytorch/pull/193000), [#193001](https://github.com/pytorch/pytorch/pull/193001), [#193013](https://github.com/pytorch/pytorch/pull/193013), [#193014](https://github.com/pytorch/pytorch/pull/193014), [#193177](https://github.com/pytorch/pytorch/pull/193177), [#193588](https://github.com/pytorch/pytorch/pull/193588), [#193650](https://github.com/pytorch/pytorch/pull/193650), [#193848](https://github.com/pytorch/pytorch/pull/193848), [#194192](https://github.com/pytorch/pytorch/pull/194192), [#194440](https://github.com/pytorch/pytorch/pull/194440), [#194500](https://github.com/pytorch/pytorch/pull/194500), [#194925](https://github.com/pytorch/pytorch/pull/194925), [#195433](https://github.com/pytorch/pytorch/pull/195433), [#195965](https://github.com/pytorch/pytorch/pull/195965), [#195989](https://github.com/pytorch/pytorch/pull/195989), [#195998](https://github.com/pytorch/pytorch/pull/195998), [#197791](https://github.com/pytorch/pytorch/pull/197791), [#197794](https://github.com/pytorch/pytorch/pull/197794), [#199060](https://github.com/pytorch/pytorch/pull/199060), [#185648](https://github.com/pytorch/pytorch/pull/185648))
- Modernize C++ code using C++20 features and add missing `std::move`s ([#179397](https://github.com/pytorch/pytorch/pull/179397), [#187002](https://github.com/pytorch/pytorch/pull/187002), [#195032](https://github.com/pytorch/pytorch/pull/195032))
- Modernize CMake usage ([#197814](https://github.com/pytorch/pytorch/pull/197814), [#198957](https://github.com/pytorch/pytorch/pull/198957))
- Fix printf-style specifiers in assertion messages and remove stale comments ([#189338](https://github.com/pytorch/pytorch/pull/189338))
- Fix typos and grammar in comments and docstrings ([#193963](https://github.com/pytorch/pytorch/pull/193963), [#194627](https://github.com/pytorch/pytorch/pull/194627), [#194565](https://github.com/pytorch/pytorch/pull/194565))
### security
