
# Release Notes worksheet cpp_frontend

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

## cpp_frontend
### bc breaking
- [autograd] Convert shared_ptr<Node> to intrusive_ptr<Node> ([#181139](https://github.com/pytorch/pytorch/pull/181139))
### deprecation
### new features
### improvements
- [12/12] Enforce C++20 minimum in header guards (#178150) ([#178150](https://github.com/pytorch/pytorch/pull/178150))
- Add stable ABI for torch Library set_python_module ([#182720](https://github.com/pytorch/pytorch/pull/182720))
- Add == overloads for HeaderOnlyArrayRef ([#185379](https://github.com/pytorch/pytorch/pull/185379))
- Add == overloads for HeaderOnlyArrayRef ([#185379](https://github.com/pytorch/pytorch/pull/185379))
- c10/core/DispatchKeySet.h: add [[nodiscard]] to all query methods ([#185960](https://github.com/pytorch/pytorch/pull/185960))
- Add highlevel C++ torch::stable::Generator ([#186423](https://github.com/pytorch/pytorch/pull/186423))
### bug fixes
### performance
- [c10] Fix reduced-precision rsqrt double promotion ([#181232](https://github.com/pytorch/pytorch/pull/181232))
### docs
### devs
### Untopiced
- Added c10::layout typecaster for torch.layout ([#179607](https://github.com/pytorch/pytorch/pull/179607))
- FakeTensor C++ Migration: Modifying TensorImpl ([#181387](https://github.com/pytorch/pytorch/pull/181387))
- Add default args support to def_static ([#175644](https://github.com/pytorch/pytorch/pull/175644))
- Fix typos in export wrapper docstring and transformer module comment ([#181972](https://github.com/pytorch/pytorch/pull/181972))
- Add C++ API support for controlling scientific notation in tensor printing ([#173321](https://github.com/pytorch/pytorch/pull/173321))
- Deduplicate `operator<<` for `Vectorized<T>` ([#185502](https://github.com/pytorch/pytorch/pull/185502))
- [BE][Ez]: Micro-opt char literal ostream overloads ([#186387](https://github.com/pytorch/pytorch/pull/186387))
- [EZ] Add check for mode in embedding bag ([#186428](https://github.com/pytorch/pytorch/pull/186428))
### not user facing
- [BE] Use [[maybe_unused]] instead of (void)what in ReadAdapter overrides ([#181192](https://github.com/pytorch/pytorch/pull/181192))
- Move intrusive_ptr's is_always_lock_free static_assert to .cpp ([#181719](https://github.com/pytorch/pytorch/pull/181719))
- Update torch-xpu-ops pin to pick up C++20 fixes ([#184649](https://github.com/pytorch/pytorch/pull/184649))
### security
