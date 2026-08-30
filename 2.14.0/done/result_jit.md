
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
- TorchScript APIs now emit visible `FutureWarning`s instead of normally hidden `DeprecationWarning`s ([#189914](https://github.com/pytorch/pytorch/pull/189914))

  Calls such as `torch.jit.script`, `torch.jit.trace`, `torch.jit.save`, and `torch.jit.load` now visibly direct users toward `torch.compile` or `torch.export`. Imports of `torch.utils.mkldnn` and `torch.distributed.optim` also avoid eagerly compiling TorchScript when those modules are merely imported.

  Before:

  ```python
  scripted = torch.jit.script(model)
  torch.jit.save(scripted, "model.pt")
  ```

  After:

  ```python
  exported = torch.export.export(model, example_inputs)
  torch.export.save(exported, "model.pt2")
  ```
### new features
### improvements
### bug fixes
- Make TorchScript reject bare `list` and `tuple` value annotations consistently with `Attempted to use list without a contained type` or the equivalent tuple error; specify an element type such as `list[int]` instead ([#188779](https://github.com/pytorch/pytorch/pull/188779))
- Fix runtime compilation of JIT fuser kernels on ROCm 7 when HIPRTC's `bfloat16` conversion symbols collide with PyTorch's embedded definitions ([#185656](https://github.com/pytorch/pytorch/pull/185656))
- Fix `torch.jit.script` failing with `Cannot re-assign modules in a ScriptModule with non-scripted module` when a wrapper contains an already-scripted child with a `__jit_ignored_attributes__` submodule ([#187863](https://github.com/pytorch/pytorch/pull/187863))
### performance
- Reduce JIT startup and compilation overhead by replacing lexer static hash maps with switch-based lookups, preallocating dead-code-elimination memoization storage, and reserving tuple type-parser storage ([#181118](https://github.com/pytorch/pytorch/pull/181118), [#188121](https://github.com/pytorch/pytorch/pull/188121), [#183813](https://github.com/pytorch/pytorch/pull/183813))
### docs
### devs
- Restore TensorExpr source-build compatibility with LLVM 24 after removal of legacy typed-pointer APIs ([#192381](https://github.com/pytorch/pytorch/pull/192381))
### not user facing
- Add an internal-only pluggable node-execution registry to Static Runtime; the OSS execution path is unchanged ([#187538](https://github.com/pytorch/pytorch/pull/187538))
- Fix spelling in comments and docstrings across PyTorch, including JIT internals ([#190198](https://github.com/pytorch/pytorch/pull/190198))
### security
