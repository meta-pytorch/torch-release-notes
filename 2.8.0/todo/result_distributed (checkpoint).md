
# Release Notes worksheet distributed (checkpoint)

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

## distributed (checkpoint)
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- [DCP][Ez]: Fix broadcast_object bug in DCP utils ([#155912](https://github.com/pytorch/pytorch/pull/155912))
### performance
### docs
### devs
### Untopiced
### not user facing
- Remove test_get_model_state_dict_del_memory  ([#149460](https://github.com/pytorch/pytorch/pull/149460))
- Support huggingface reading and writing for multi rank case ([#148189](https://github.com/pytorch/pytorch/pull/148189))
- Fix bug in _load_state_dict_from_keys method ([#150058](https://github.com/pytorch/pytorch/pull/150058))
- [DTensor][tp] fix errors in FSDP+TP checkpointing test ([#150354](https://github.com/pytorch/pytorch/pull/150354))
- Add a param for save format in Storage Writer ([#150025](https://github.com/pytorch/pytorch/pull/150025))
- Remove ls from filesystem base ([#151117](https://github.com/pytorch/pytorch/pull/151117))
- [DCP] Add logging for _stateful_to_state_dict(), stage_state_dict(), and synchronize_staging() ([#151320](https://github.com/pytorch/pytorch/pull/151320))
- [DCP] Add logging for _stateful_to_state_dict(), stage_state_dict(), and synchronize_staging() ([#151320](https://github.com/pytorch/pytorch/pull/151320))
- [ez] Don't always pass HF token to fsspec ([#151464](https://github.com/pytorch/pytorch/pull/151464))
- [ez] Fsspec Filesystem ls details should be false ([#152693](https://github.com/pytorch/pytorch/pull/152693))
- [BE]: Add PEP621 project section to pyproject.toml ([#153055](https://github.com/pytorch/pytorch/pull/153055))
- Fix HF loading when there's no metadata file to work with fsspec ([#152856](https://github.com/pytorch/pytorch/pull/152856))
- [BE]: Add PEP621 project section to pyproject.toml ([#153055](https://github.com/pytorch/pytorch/pull/153055))
- [DSD] Don't pop tensors if they are on Meta device ([#153185](https://github.com/pytorch/pytorch/pull/153185))
- [DSD] Don't pop tensors if they are on Meta device ([#153185](https://github.com/pytorch/pytorch/pull/153185))
- remove allow-untyped-defs from torch/distributed/checkpoint/resharding.py ([#154626](https://github.com/pytorch/pytorch/pull/154626))
- Fix typo in dcp module ([#154815](https://github.com/pytorch/pytorch/pull/154815))
- [BE]: Backport runtime_checkable perf improvements/behavior from 3.12 ([#155130](https://github.com/pytorch/pytorch/pull/155130))
- [DCP][PyTorch Staging APIs][2/x] Handle 0-elem case + ShardedTensor copy for staging ([#156092](https://github.com/pytorch/pytorch/pull/156092))
- [BE][PYFMT] migrate PYFMT for `test/[a-h]*/` to `ruff format` ([#144555](https://github.com/pytorch/pytorch/pull/144555))
### security
