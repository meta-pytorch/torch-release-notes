
# Release Notes worksheet dynamo

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.
* Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

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

## dynamo
### bc breaking
- For HigherOrderOperators (e.g. `cond`), we enforced a stricter aliasing/mutation check, which will explicitly error out if they doesn't support alias/mutation among inputs and outputs
  ([#148953](https://github.com/pytorch/pytorch/pull/148953), [#146658](https://github.com/pytorch/pytorch/pull/146658)).

  For affected HigherOrderOperators, add `.clone()` to aliased outputs.

  Version 2.7.0
  ```python
  import torch

  @torch.compile(backend="eager")
  def fn(x):
      return torch.cond(x.sum() > 0, lambda x: x, lambda x: x + 1, [x])

  fn(torch.ones(3))
  ```

  Version 2.8.0
  ```python
  import torch

  @torch.compile(backend="eager")
  def fn(x):
      return torch.cond(x.sum() > 0, lambda x: x.clone(), lambda x: x + 1, [x])

  fn(torch.ones(3))
  ```
### deprecation
- Deprecate `enable_cpp_framelocals_guard_eval` Dynamo config variable ([#151008](https://github.com/pytorch/pytorch/pull/151008)).
  This config no longer has any effect.
### new features
- Hierarchical compilation via `nested_compile_region` ([#156449](https://github.com/pytorch/pytorch/pull/156449))
- Allow guards to be dropped with custom filter functions via `guard_filter_fn` ([#150936](https://github.com/pytorch/pytorch/pull/150936))
- `dont_skip_tracing` decorator to skip over most Dynamo skipfiles rules ([#150586](https://github.com/pytorch/pytorch/pull/150586))
### improvements
- Add reason field to `torch.compiler.disable` ([#150341](https://github.com/pytorch/pytorch/pull/150341))
- Misc. increased tracing support, e.g. for Python sets ([#153150]https://github.com/pytorch/pytorch/pull/153150))
- Always trace into a Tensor subclass' `__torch_function__` ([#149792](https://github.com/pytorch/pytorch/pull/149792))
- [Compiled Autograd] Eliminated all dynamic shapes recompiles for compile time reduction ([#151962](https://github.com/pytorch/pytorch/pull/151962), [#152119](https://github.com/pytorch/pytorch/pull/152119),
  [#151962](https://github.com/pytorch/pytorch/pull/151962), [#149707](https://github.com/pytorch/pytorch/pull/149707), [#149709](https://github.com/pytorch/pytorch/pull/149709),
  [#148799](https://github.com/pytorch/pytorch/pull/148799), [#148801](https://github.com/pytorch/pytorch/pull/148801))
- Trace `namedtuple` subclasses ([#153982](https://github.com/pytorch/pytorch/pull/153982))
### bug fixes
- Fix spammy errors when user passes an invalid `TORCH_LOGS` argument ([#151678](https://github.com/pytorch/pytorch/pull/151678))
- Eliminated silent incorrectness in the Compiled Autograd initial trace ([#149014](https://github.com/pytorch/pytorch/pull/149014),
  [#155521](https://github.com/pytorch/pytorch/pull/155521), [#155289](https://github.com/pytorch/pytorch/pull/155289), [#149336](https://github.com/pytorch/pytorch/pull/149336))
- [Compiled Autograd] Fixed unpack hook semantics for memory savings in checkpointing and offloading ([#147242](https://github.com/pytorch/pytorch/pull/147242), [#153300](https://github.com/pytorch/pytorch/pull/153300))
### performance
### docs
<!-- programming model docs, if we can get that in 2.8 -->
### devs
### Untopiced
### not user facing
### security
