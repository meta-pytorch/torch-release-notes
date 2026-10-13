
# Release Notes worksheet distributed (fsdp)

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

## distributed (fsdp)
### bc breaking
### deprecation
### new features
- FSDP: allow extensions to release all-gather outputs ([#194114](https://github.com/pytorch/pytorch/pull/194114))
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [FSDP2] Guard _unsharded_param access in to_accumulated_grad_if_needed ([#194058](https://github.com/pytorch/pytorch/pull/194058))
- [Distributed][ROCm] Fix FSDP incorrectly drops and reuses memory when using both NO_SHARD and CPU offload ([#194519](https://github.com/pytorch/pytorch/pull/194519))
- [FSDP] Fix dangerous mutable default dictionary in _override_module_mixed_precision ([#194895](https://github.com/pytorch/pytorch/pull/194895))
- Widen FSDP param group stream type annotations to torch.Stream ([#196563](https://github.com/pytorch/pytorch/pull/196563))
- [Testcase Refactoring] Make FSDP tests device-agnostic for out-of-tree backends ([#187650](https://github.com/pytorch/pytorch/pull/187650))
- [xpu][symm_mem] Enable SymmetricMemory MemPool on XPU ([#197065](https://github.com/pytorch/pytorch/pull/197065))
- [FSDP] Clear deferred all-gather state after backward ([#196460](https://github.com/pytorch/pytorch/pull/196460))
- [FSDP2] Add gradient accumulation finalization API ([#196640](https://github.com/pytorch/pytorch/pull/196640))
- [FSDP2] Document that modifying parameters between forward and backward is unsupported ([#198826](https://github.com/pytorch/pytorch/pull/198826))
- [FSDP2] Record the consumer stream on the reduce-scatter output when a backend frees eagerly ([#193686](https://github.com/pytorch/pytorch/pull/193686))
- [FSDP2] Keep the reduce-scatter output alive for the all-reduce hook ([#198804](https://github.com/pytorch/pytorch/pull/198804))
- [FSDP2] Add gradient accumulation finalization API ([#196640](https://github.com/pytorch/pytorch/pull/196640))
- [FSDP2] Support asynchronous gradient finalization ([#196724](https://github.com/pytorch/pytorch/pull/196724))
- [fsdp2] Optionally keep unsharded storage across reshard ([#198417](https://github.com/pytorch/pytorch/pull/198417))
- [fsdp2][mp] per-param mixed_precision policy ([#196626](https://github.com/pytorch/pytorch/pull/196626))
- [FSDP2] Join pending all-gather with device stream ([#199677](https://github.com/pytorch/pytorch/pull/199677))
- [FSDP2] Copy byte payloads bytewise in the single-rank all-gather path ([#199733](https://github.com/pytorch/pytorch/pull/199733))
### not user facing
### security
