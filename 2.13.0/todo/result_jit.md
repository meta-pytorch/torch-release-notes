
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
### deprecation
### new features
### improvements
### bug fixes
- Fix OOB read in MemoryReadAdapter::read ([#181193](https://github.com/pytorch/pytorch/pull/181193))
- Validate tensor sizes/strides/storage_offset in C++ Unpickler ([#183381](https://github.com/pytorch/pytorch/pull/183381))
### performance
### docs
### devs
### Untopiced
- [PyTorch] Fix broadcast_shapes op missing in selective builds (#180860) ([#180860](https://github.com/pytorch/pytorch/pull/180860))
- Use TORCH_CHECK instead of AT_ASSERT for single input/output node helpers ([#181282](https://github.com/pytorch/pytorch/pull/181282))
- Apply bugfixes from LTO enablement PR ([#180868](https://github.com/pytorch/pytorch/pull/180868))
- Fix typos in comments, docstrings, and error messages ([#181391](https://github.com/pytorch/pytorch/pull/181391))
- [PyTorch] Add _jit_replace_submodule (#180296) ([#180296](https://github.com/pytorch/pytorch/pull/180296))
- [BE][Ez]: Make IValueArray move only ([#181517](https://github.com/pytorch/pytorch/pull/181517))
- Fix typos in comments and docstrings ([#181970](https://github.com/pytorch/pytorch/pull/181970))
- Fix typos in comments: recoding -> recording, sppecified -> specified ([#181983](https://github.com/pytorch/pytorch/pull/181983))
- [preproc] shared lock for jit (#175181) ([#175181](https://github.com/pytorch/pytorch/pull/175181))
- Fix typos in comment and deprecation message ([#182685](https://github.com/pytorch/pytorch/pull/182685))
- Fix "dont" typos across JIT, dynamo, and fx modules ([#182702](https://github.com/pytorch/pytorch/pull/182702))
- Fix typos in C++ comments ([#182767](https://github.com/pytorch/pytorch/pull/182767))
- [AI Codemod][PerfAICT-ObjCpy] perf: Avoid unnecessary std::string construction (#183011) ([#183011](https://github.com/pytorch/pytorch/pull/183011))
- Fix use-after-free in symbolic-shape runtime fusion guard ([#183760](https://github.com/pytorch/pytorch/pull/183760))
- Use pop in place of last() + drop() in JIT runtime ([#184063](https://github.com/pytorch/pytorch/pull/184063))
- Disallow bare PyObject in operator schemas ([#184209](https://github.com/pytorch/pytorch/pull/184209))
- Fix integer overflow in Unpickler storage size computation ([#181310](https://github.com/pytorch/pytorch/pull/181310))
- Fix "its'" typos to "its" across AOT autograd and JIT frontend ([#185242](https://github.com/pytorch/pytorch/pull/185242))
- [Regional AOTI] Mutate root ScriptModule in place in _replace_submodule_with_typecheck_pybind (#185321) ([#185321](https://github.com/pytorch/pytorch/pull/185321))
- Fix typo "onceto" -> "once to" in JIT CSE comments ([#185584](https://github.com/pytorch/pytorch/pull/185584))
- [export] Fix torch.export.load GIL contention during tensor deserialization ([#175983](https://github.com/pytorch/pytorch/pull/175983))
### not user facing
- [PyTorch] Fix binary_cross_entropy SymInt error with dynamic shapes (#180583) ([#180583](https://github.com/pytorch/pytorch/pull/180583))
- Use C++20 concepts where it improves readability ([#179286](https://github.com/pytorch/pytorch/pull/179286))
- Fix duplicate word typo in LLVM JIT comment ([#184213](https://github.com/pytorch/pytorch/pull/184213))
- Replace c10::ssize with std::ssize ([#184775](https://github.com/pytorch/pytorch/pull/184775))
- Fix article and spelling typos in comments and docstrings ([#185230](https://github.com/pytorch/pytorch/pull/185230))
- [CPU Kernel Fusion Framework] Expose overlapsWithUsedNodes and getVmap from SubgraphRewriter (#183333) ([#183333](https://github.com/pytorch/pytorch/pull/183333))
- [BE][Ez]: Append single char instead of str literal overload ([#186477](https://github.com/pytorch/pytorch/pull/186477))
### security
