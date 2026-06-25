
# Release Notes worksheet distributed (fsdp2)

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

## distributed (fsdp2)
### bc breaking
### deprecation
### new features
- Add `FSDPModule.set_separate_reduce_scatter_group` to give reduce-scatter its own NCCL communicator, enabling opt-in overlap of all-gather and reduce-scatter ([#186335](https://github.com/pytorch/pytorch/pull/186335))
- Add `set_reduce_scatter_max_input_buffers` to keep multiple reduce-scatter input buffers in flight, so backward compute no longer stalls waiting to recycle a single reduce-scatter buffer ([#186000](https://github.com/pytorch/pytorch/pull/186000))
### improvements
- Support forward-mode automatic differentiation (`torch.func.jvp`) on models wrapped with `fully_shard` or `replicate`, including with mixed precision ([#182732](https://github.com/pytorch/pytorch/pull/182732))
### bug fixes
- Fix stale `post_accumulate_grad_hook` results under `CPUOffloadPolicy` ([#180666](https://github.com/pytorch/pytorch/pull/180666))
- Fix reduce-scatter of unused DTensor parameters that previously raised a mixed `Tensor`/`DTensor` error in `chunk_cat` ([#183040](https://github.com/pytorch/pytorch/pull/183040))
- Fix `IndexError` for modules called with no forward inputs by preserving empty args/kwargs, matching FSDP1 behavior ([#183943](https://github.com/pytorch/pytorch/pull/183943))
- Remove redundant stream waits ([#183983](https://github.com/pytorch/pytorch/pull/183983))
- Fix a tensor-parallel + FSDP2 + mixed-precision bug where the unsharded compute tensor was wrapped back into a `DTensor` with a stale fp32 dtype, causing sharding propagation to fail in eager and `torch.compile` ([#183805](https://github.com/pytorch/pytorch/pull/183805))
- Fix incorrectly reduced gradients when running a partial forward of a `fully_shard([norm, head])` group for chunked loss, where the model forward runs `norm` only and `head` is called standalone per chunk; unshard/reshard previously relied on `_modules_to_run_forward` and produced wrong results for this pattern ([#180428](https://github.com/pytorch/pytorch/pull/180428))
- Add a warning when a grad-requiring forward output is a view tensor, since in-place ops on the view silently drop the pre-backward hook and cause backward to skip the all-gather and fail ([#181850](https://github.com/pytorch/pytorch/pull/181850))
- Fix incorrect `clip_grad_norm` results with multiple data-parallel shard axes (e.g. `dp_shard` + `cp` passed via `DataParallelMeshDims`), which exposed separate `Shard` axes with the wrong float32 reduction order and an incorrect `Shard` instead of `_StridedShard`; the axes are now flattened into a single shard axis in the sharding spec ([#183629](https://github.com/pytorch/pytorch/pull/183629))
- Fix recomputed tensor metadata diverging from the original forward under activation checkpointing when `cast_forward_inputs` is enabled, by casting forward inputs during recompute ([#182580](https://github.com/pytorch/pytorch/pull/182580))
- Fix incorrect resharding of full-DTensor parameters when tensor parallelism is also applied by using `_StridedShard` ([#186126](https://github.com/pytorch/pytorch/pull/186126))
### performance
### docs
- Document previously undocumented functions in `distributed.fsdp.fully_shard` ([#182866](https://github.com/pytorch/pytorch/pull/182866))
### devs
### not user facing
- Add unit test and invariant comments for HSDP all-reduce buffer lifetime ([#180900](https://github.com/pytorch/pytorch/pull/180900))
- Fix typos in comments, docstrings, and error messages ([#181990](https://github.com/pytorch/pytorch/pull/181990))
- Fix CUDA memory leak check failure in `test_fsdp_apply` ([#182774](https://github.com/pytorch/pytorch/pull/182774))
- Fix type erasure due to missing `Callable` annotation for a decorator ([#182990](https://github.com/pytorch/pytorch/pull/182990))
- Inline DISABLED-test skips from the auto-disabler JSON into source ([#185013](https://github.com/pytorch/pytorch/pull/185013))
### security
