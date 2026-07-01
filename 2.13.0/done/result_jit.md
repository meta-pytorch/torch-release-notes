
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
- Bare `PyObject` is no longer allowed in operator schemas ([#184209](https://github.com/pytorch/pytorch/pull/184209))

  Bare `PyObject` was accidentally accepted in operator schema strings in
  PyTorch 2.12 while adding support for registered opaque type names. This was
  undocumented and is now rejected, since `torch.compile` does not support
  arbitrary `PyObject` inputs to custom ops. Registered opaque type names
  continue to work. If you parse or register a schema with a bare `PyObject`
  argument or return type, you will now get a schema parse error; switch to a
  registered opaque type name instead.

  Version 2.12:
  ```python
  >>> from torch._C import parse_schema
  >>> parse_schema("foo(PyObject x) -> ()")  # accepted
  ```

  Version 2.13:
  ```python
  >>> from torch._C import parse_schema
  >>> parse_schema("foo(PyObject x) -> ()")  # raises a schema parse error
  ```
### deprecation
### new features
### improvements
### bug fixes
- Fix OOB read in `MemoryReadAdapter::read` ([#181193](https://github.com/pytorch/pytorch/pull/181193))
- Validate tensor sizes/strides/storage_offset in C++ Unpickler ([#183381](https://github.com/pytorch/pytorch/pull/183381))
- Fix integer overflow in Unpickler storage size computation ([#181310](https://github.com/pytorch/pytorch/pull/181310))
- Fix `broadcast_shapes` op missing in selective builds ([#180860](https://github.com/pytorch/pytorch/pull/180860))
- Fix `binary_cross_entropy` SymInt error with dynamic shapes by registering `aten::broadcast_shapes` as a TorchScript builtin ([#180583](https://github.com/pytorch/pytorch/pull/180583))
- Fix use-after-free in symbolic-shape runtime fusion guard ([#183760](https://github.com/pytorch/pytorch/pull/183760))
- Apply bugfixes when enabling Link-Time Optimizations ([#180868](https://github.com/pytorch/pytorch/pull/180868))
### performance
### docs
### devs
- Add `torch._C._jit_replace_submodule` to swap submodules in scripted modules while updating parent types and remapping referenced types across graphs ([#180296](https://github.com/pytorch/pytorch/pull/180296))
- Use `TORCH_CHECK` instead of `AT_ASSERT` for single input/output node helpers, producing clearer error messages ([#181282](https://github.com/pytorch/pytorch/pull/181282))
- Expose `overlapsWithUsedNodes` and `getVmap` from `SubgraphRewriter` ([#183333](https://github.com/pytorch/pytorch/pull/183333))
### not user facing
- Fix typos in comments, docstrings, and error messages ([#181391](https://github.com/pytorch/pytorch/pull/181391))
- Fix typos in comments and docstrings ([#181970](https://github.com/pytorch/pytorch/pull/181970))
- Fix typos in comments: recoding -> recording, sppecified -> specified ([#181983](https://github.com/pytorch/pytorch/pull/181983))
- Fix typos in comment and deprecation message ([#182685](https://github.com/pytorch/pytorch/pull/182685))
- Fix "dont" typos across JIT, dynamo, and fx modules ([#182702](https://github.com/pytorch/pytorch/pull/182702))
- Fix typos in C++ comments ([#182767](https://github.com/pytorch/pytorch/pull/182767))
- Fix "its'" typos to "its" across AOT autograd and JIT frontend ([#185242](https://github.com/pytorch/pytorch/pull/185242))
- Fix typo "onceto" -> "once to" in JIT CSE comments ([#185584](https://github.com/pytorch/pytorch/pull/185584))
- Fix duplicate word typo in LLVM JIT comment ([#184213](https://github.com/pytorch/pytorch/pull/184213))
- Fix article and spelling typos in comments and docstrings ([#185230](https://github.com/pytorch/pytorch/pull/185230))
- [BE][Ez]: Make IValueArray move only ([#181517](https://github.com/pytorch/pytorch/pull/181517))
- [BE][Ez]: Append single char instead of str literal overload ([#186477](https://github.com/pytorch/pytorch/pull/186477))
- Use C++20 concepts where it improves readability ([#179286](https://github.com/pytorch/pytorch/pull/179286))
- Replace c10::ssize with std::ssize ([#184775](https://github.com/pytorch/pytorch/pull/184775))
- Use pop in place of last() + drop() in JIT runtime ([#184063](https://github.com/pytorch/pytorch/pull/184063))
- [preproc] shared lock for jit ([#175181](https://github.com/pytorch/pytorch/pull/175181))
- Avoid unnecessary std::string construction in JIT object copy ([#183011](https://github.com/pytorch/pytorch/pull/183011))
- [Regional AOTI] Mutate root ScriptModule in place in `_replace_submodule_with_typecheck_pybind` ([#185321](https://github.com/pytorch/pytorch/pull/185321))
- Add LLVM 23+ branch for `ObjectLinkingLayerCreator` in tensorexpr ([#180746](https://github.com/pytorch/pytorch/pull/180746))
- Fix duplicated article "the the" typos in comments ([#181672](https://github.com/pytorch/pytorch/pull/181672))
- Fix typos across torch codebase ([#181813](https://github.com/pytorch/pytorch/pull/181813))
- Fix duplicate-word typos and a misspelling in comments and docs ([#181934](https://github.com/pytorch/pytorch/pull/181934))
- Fix typos in comments, docstrings, and documentation ([#181966](https://github.com/pytorch/pytorch/pull/181966))
- Fix typos in comments and docstrings across torch ([#181978](https://github.com/pytorch/pytorch/pull/181978))
- Fix typos in comments and documentation ([#185241](https://github.com/pytorch/pytorch/pull/185241))
### security
