
# Release Notes worksheet distributed (miscellaneous)

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

## distributed (miscellaneous)
### bc breaking
### deprecation
### new features
- Support passing extra keyword arguments to the loss function in pipeline schedules via a new `loss_kwargs` parameter to `step()`, enabling loss functions that require arguments beyond `(output, target)` (such as chunked cross-entropy needing token counts for scaling) ([#181057](https://github.com/pytorch/pytorch/pull/181057))
### improvements
- Allow `elastic_launch`/`launch_agent` to accept a pre-created torchelastic health check server, so it can be started before rendezvous ([#180543](https://github.com/pytorch/pytorch/pull/180543))
- Add an `overlap_pp_comm` flag to pipeline schedules (default `True`) that, when set to `False`, defers each pipeline RECV op to immediately before the compute op that consumes it, using rank-parity P2P ordering to avoid deadlock (helps platforms such as AMD ROCm where a pending RECV blocks unrelated compute) ([#178815](https://github.com/pytorch/pytorch/pull/178815))
### bug fixes
- Fix the torchelastic agent hanging indefinitely (and never exiting) when workers become stuck in an uninterruptible (D-state) process that `SIGKILL` cannot reap; the final `proc.join()`/`proc.wait()` in `_close` is now bounded by a timeout and the unkillable PID is logged ([#185414](https://github.com/pytorch/pytorch/pull/185414))
- Fix pipelining producing incorrect results or cryptic runtime errors when a `PipelineScheduleMulti` topology communicates between non-adjacent stages (e.g. skip connections); this is now detected at initialization and raises a clear `RuntimeError` ([#179293](https://github.com/pytorch/pytorch/pull/179293))
- Fix `RuntimeError: only Tensors of floating point dtype can require gradients` when building a pipeline for models with non-float intermediates (such as Hugging Face transformer models) ([#183582](https://github.com/pytorch/pytorch/pull/183582))
- Make `LocalTensorMode` transparent to `torch.compile` so compilation proceeds as if the debugging mode were not active ([#182667](https://github.com/pytorch/pytorch/pull/182667))
- Fix `AssertionError` in elastic `c10d` rendezvous when a node's rank changes across rendezvous rounds (e.g. a node becomes rank 0 after a peer leaves) ([#182375](https://github.com/pytorch/pytorch/pull/182375))
- Fix shared-weight gradient double-counting in zero-bubble pipeline schedules ([#181365](https://github.com/pytorch/pytorch/pull/181365))
- Fix `None` gradient handling in pipeline backward send/recv ([#182182](https://github.com/pytorch/pytorch/pull/182182))
- Fix a pipelining crash when `split_module` interleaves `get_attr` nodes with placeholder nodes ([#182644](https://github.com/pytorch/pytorch/pull/182644))
### performance
### docs
- Convert the torchelastic `elastic/quickstart.rst` from reStructuredText to MyST Markdown ([#182569](https://github.com/pytorch/pytorch/pull/182569))
- Convert the RPC `rpc/rref.rst` from reStructuredText to MyST Markdown ([#182877](https://github.com/pytorch/pytorch/pull/182877))
- Clarify that `--node-rank` is only used with static rendezvous ([#182374](https://github.com/pytorch/pytorch/pull/182374))
- Add API reference documentation for previously-undocumented functions in `torch.distributed.rpc` ([#183393](https://github.com/pytorch/pytorch/pull/183393))
- Add API reference documentation for previously-undocumented functional optimizer APIs in `torch.distributed.optim` ([#182871](https://github.com/pytorch/pytorch/pull/182871))
### devs
### not user facing
- Fix typos in comments and docstrings across distributed, decomp, and fx modules ([#181979](https://github.com/pytorch/pytorch/pull/181979))
- Fix typos in comments and error messages ([#181965](https://github.com/pytorch/pytorch/pull/181965))
- Remove unused noqa directives in `torch/`, batch 1 ([#180134](https://github.com/pytorch/pytorch/pull/180134))
- Fix typos in distributed and data loading modules ([#183326](https://github.com/pytorch/pytorch/pull/183326))
- [xpu][test] Port distributed _shard tests cases on Intel GPUs ([#180881](https://github.com/pytorch/pytorch/pull/180881))
- Convert rpc/distributed_autograd.rst from rST to MyST Markdown ([#182926](https://github.com/pytorch/pytorch/pull/182926))
- [BE][Ez]: Add missing typing vars for decorators. Prevent type erasure ([#183116](https://github.com/pytorch/pytorch/pull/183116))
### security
