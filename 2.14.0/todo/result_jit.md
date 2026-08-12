
# Release Notes worksheet jit

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

## jit
### bc breaking
- Remove deprecated isIntegral overloads ([#187115](https://github.com/pytorch/pytorch/pull/187115))
### deprecation
### new features
### improvements
### bug fixes
- [JIT] Reject bare `list`/`tuple` value annotations ([#188779](https://github.com/pytorch/pytorch/pull/188779))
### performance
### docs
### devs
### Untopiced
- [ROCm] Rename duplicate hiprtc names for jit to avoid symbol collision ([#185656](https://github.com/pytorch/pytorch/pull/185656))
- [SR] Node executor registry in SR ([#187538](https://github.com/pytorch/pytorch/pull/187538))
- Remove static initializers from lexer.cpp (#181118) ([#181118](https://github.com/pytorch/pytorch/pull/181118))
- [JIT] Skip re-walking already-scripted modules in the prepare pass (#187863) ([#187863](https://github.com/pytorch/pytorch/pull/187863))
- [AI Codemod][PerfAICT-MapSetRehash] Pre-reserve memo_ map to avoid rehashing during DCE side-effect analysis ([#188121](https://github.com/pytorch/pytorch/pull/188121))
- [AI Codemod][PerfAICT-VecRealloc] perf: call reserve() on vector to avoid unnecessary re-allocation (#183813) ([#183813](https://github.com/pytorch/pytorch/pull/183813))
- Fix spelling errors in comments and docstrings ([#190198](https://github.com/pytorch/pytorch/pull/190198))
- [torch] Fix deprecated getPointerTo to be compatible with LLVM 24 (#192381) ([#192381](https://github.com/pytorch/pytorch/pull/192381))
### not user facing
- Use C++20 concepts where it improves readability ([#179286](https://github.com/pytorch/pytorch/pull/179286))
### security
