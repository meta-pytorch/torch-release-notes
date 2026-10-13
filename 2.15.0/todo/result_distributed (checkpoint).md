
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
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- Avoid Tensor refcount churn during c10::List<optional<Tensor>> iteration ([#192550](https://github.com/pytorch/pytorch/pull/192550))
- Fix grammar and typos in docs and docstrings ([#194415](https://github.com/pytorch/pytorch/pull/194415))
- Fix grammar and typos in code comments and docstrings ([#194493](https://github.com/pytorch/pytorch/pull/194493))
- [S615805][S694227][PyTorch] Safely preserve tensor strides (#194251) ([#194251](https://github.com/pytorch/pytorch/pull/194251))
- Fix remaining checkpoint filesystem races flagged in #194614 ([#196591](https://github.com/pytorch/pytorch/pull/196591))
- Make Fsspec filesystem checkpointing public and exposing cache_staged_state_dict to enable async save ([#188698](https://github.com/pytorch/pytorch/pull/188698))
- Make Fsspec filesystem checkpointing public and exposing cache_staged_state_dict to enable async save ([#188698](https://github.com/pytorch/pytorch/pull/188698))
### not user facing
- [Testcase Refactoring]Add hw_classification to test_compatibility.py ([#192184](https://github.com/pytorch/pytorch/pull/192184))
- Report a child's KeyboardInterrupt instead of exiting 0 in spawn ([#194439](https://github.com/pytorch/pytorch/pull/194439))
- Fix EADDRINUSE from hard-coded MASTER_PORT in distributed test fixtures ([#194377](https://github.com/pytorch/pytorch/pull/194377))
- [Testcase Refactoring]Add hw_classification to test_quantized_hf_storage.py ([#192194](https://github.com/pytorch/pytorch/pull/192194))
- [Testcase Refactoring] Add HardwareClassification to test_hf_storage.py ([#193085](https://github.com/pytorch/pytorch/pull/193085))
- [Testcase Refactoring] Add HardwareClassification to test_checkpointer.py ([#193119](https://github.com/pytorch/pytorch/pull/193119))
- [Testcase Refactoring] Tag test_checkpoint_process.py classes with hw_classification ([#193523](https://github.com/pytorch/pytorch/pull/193523))
- [Testcase Refactoring][DCP] Classify checkpoint barrier tests by hardware requirements ([#194199](https://github.com/pytorch/pytorch/pull/194199))
- [Testcase Refactoring][DCP] Classify checkpoint writer tests by hardware requirements ([#194200](https://github.com/pytorch/pytorch/pull/194200))
- [inductor][bucketing] Fuse uneven reduce-scatter packing ([#196647](https://github.com/pytorch/pytorch/pull/196647))
- [Testcase Refactoring][DCP] Classify deduplicated tensor tests by hardware requirements ([#194202](https://github.com/pytorch/pytorch/pull/194202))
- [ROCm] Re-enable distributed tests with resolved flaky history ([#196484](https://github.com/pytorch/pytorch/pull/196484))
- [Testcase Refactoring] Add HardwareClassification to test_nested_dict.py ([#193117](https://github.com/pytorch/pytorch/pull/193117))
- [Testcase Refactoring] Add HardwareClassification to test_types.py ([#193105](https://github.com/pytorch/pytorch/pull/193105))
- [Testcase Refactoring] Add HardwareClassification to test_builder.py ([#193087](https://github.com/pytorch/pytorch/pull/193087))
- [CI] Fix retry teardown and run distributed/test_store in-process ([#197324](https://github.com/pytorch/pytorch/pull/197324))
- [Testcase Refactoring] Tag test_traverse.py TestTraverse with hw_classification ([#193524](https://github.com/pytorch/pytorch/pull/193524))
- [distributed] Wait directly for async checkpoint completion in tests ([#197641](https://github.com/pytorch/pytorch/pull/197641))
- [distributed] Resolve checkpoint test futures without sleeping ([#197638](https://github.com/pytorch/pytorch/pull/197638))
- [distributed] Reuse workers for checkpoint state-dict utility tests ([#197647](https://github.com/pytorch/pytorch/pull/197647))
- Reuse workers for checkpoint replication staging tests ([#197693](https://github.com/pytorch/pytorch/pull/197693))
- Reuse workers for safetensors consolidation tests ([#197694](https://github.com/pytorch/pytorch/pull/197694))
- [distributed] Reuse checkpoint ordering test workers ([#197704](https://github.com/pytorch/pytorch/pull/197704))
- [distributed] Reuse workers for checkpoint collective wrapper tests ([#197654](https://github.com/pytorch/pytorch/pull/197654))
- Reuse workers for FSDP model checkpoint tests ([#197688](https://github.com/pytorch/pytorch/pull/197688))
- [distributed] Reuse workers for tensor-parallel checkpoint tests ([#197665](https://github.com/pytorch/pytorch/pull/197665))
- [distributed] Reuse workers for checkpoint resharding tests ([#197666](https://github.com/pytorch/pytorch/pull/197666))
- [distributed] Reuse workers for HSDP checkpoint tests ([#197667](https://github.com/pytorch/pytorch/pull/197667))
- [distributed] Reuse workers for FSDP optimizer checkpoint tests ([#197670](https://github.com/pytorch/pytorch/pull/197670))
- [distributed] Reuse safetensors resharding workers ([#197677](https://github.com/pytorch/pytorch/pull/197677))
- [distributed] Reuse Gloo filesystem checkpoint workers ([#197683](https://github.com/pytorch/pytorch/pull/197683))
- [distributed] Reuse accelerator checkpoint workers ([#197684](https://github.com/pytorch/pytorch/pull/197684))
- [distributed] Reuse workers for FSDP checkpoint conversion tests ([#197668](https://github.com/pytorch/pytorch/pull/197668))
- [distributed] Reuse workers for checkpoint initialization-info tests ([#197657](https://github.com/pytorch/pytorch/pull/197657))
### security
