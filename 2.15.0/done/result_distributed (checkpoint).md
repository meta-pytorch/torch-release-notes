
# Release Notes worksheet distributed (checkpoint)

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

## distributed (checkpoint)
### bc breaking
- Distributed checkpoint metadata now records tensor strides, so checkpoints saved with PyTorch 2.15 cannot be loaded by PyTorch 2.14 or earlier ([#194251](https://github.com/pytorch/pytorch/pull/194251))

  `TensorProperties` gains an optional `strides` field in the pickled `.metadata` file. In older versions `dcp.load` raises a `CheckpointException` reporting `too many values to unpack (expected 5)`. There is no flag to write the old format.

  Version 2.14 (loading a 2.15 checkpoint):
  ```python
  dcp.load(state_dict, checkpoint_id="/ckpt/step_100")
  # CheckpointException: ... too many values to unpack (expected 5)
  ```

  Version 2.15:
  ```python
  dcp.load(state_dict, checkpoint_id="/ckpt/step_100")  # loads 2.14 and 2.15 checkpoints
  ```
### deprecation
### new features
- `FsspecReader` and `FsspecWriter` are now public in `torch.distributed.checkpoint`, and `FsspecWriter` supports `dcp.async_save` through a new `cache_staged_state_dict` argument placed before `overwrite` (pass `overwrite` and later arguments by keyword); importing the old private `_fsspec_filesystem` module emits a `DeprecationWarning` ([#188698](https://github.com/pytorch/pytorch/pull/188698))
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
### not user facing
- Fix grammar and typos in docstrings and comments ([#194415](https://github.com/pytorch/pytorch/pull/194415), [#194493](https://github.com/pytorch/pytorch/pull/194493))
- Tag distributed checkpoint test classes with hardware classifications ([#192184](https://github.com/pytorch/pytorch/pull/192184), [#192194](https://github.com/pytorch/pytorch/pull/192194), [#193085](https://github.com/pytorch/pytorch/pull/193085), [#193087](https://github.com/pytorch/pytorch/pull/193087), [#193105](https://github.com/pytorch/pytorch/pull/193105), [#193117](https://github.com/pytorch/pytorch/pull/193117), [#193119](https://github.com/pytorch/pytorch/pull/193119), [#193523](https://github.com/pytorch/pytorch/pull/193523), [#193524](https://github.com/pytorch/pytorch/pull/193524), [#194199](https://github.com/pytorch/pytorch/pull/194199), [#194200](https://github.com/pytorch/pytorch/pull/194200), [#194202](https://github.com/pytorch/pytorch/pull/194202))
- Fix filesystem races in checkpoint save/load tests ([#196591](https://github.com/pytorch/pytorch/pull/196591))
- Re-enable ROCm distributed tests whose flaky history was resolved ([#196484](https://github.com/pytorch/pytorch/pull/196484))
- Fix retry teardown in distributed store tests and run `distributed/test_store` in-process ([#197324](https://github.com/pytorch/pytorch/pull/197324))
- Speed up checkpoint tests by waiting on futures directly instead of sleeping and by reusing worker processes across test cases ([#197638](https://github.com/pytorch/pytorch/pull/197638), [#197641](https://github.com/pytorch/pytorch/pull/197641), [#197647](https://github.com/pytorch/pytorch/pull/197647), [#197654](https://github.com/pytorch/pytorch/pull/197654), [#197657](https://github.com/pytorch/pytorch/pull/197657), [#197665](https://github.com/pytorch/pytorch/pull/197665), [#197666](https://github.com/pytorch/pytorch/pull/197666), [#197667](https://github.com/pytorch/pytorch/pull/197667), [#197668](https://github.com/pytorch/pytorch/pull/197668), [#197670](https://github.com/pytorch/pytorch/pull/197670), [#197677](https://github.com/pytorch/pytorch/pull/197677), [#197683](https://github.com/pytorch/pytorch/pull/197683), [#197684](https://github.com/pytorch/pytorch/pull/197684), [#197688](https://github.com/pytorch/pytorch/pull/197688), [#197693](https://github.com/pytorch/pytorch/pull/197693), [#197694](https://github.com/pytorch/pytorch/pull/197694), [#197704](https://github.com/pytorch/pytorch/pull/197704))
### security
