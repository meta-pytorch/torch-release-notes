
# Release Notes worksheet dataloader_frontend

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

## dataloader_frontend
### bc breaking
- Remove data_source argument from Sampler ([#163134](https://github.com/pytorch/pytorch/pull/163134))
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [1/N] Remove 'type: ignore' suppressions  ([#163468](https://github.com/pytorch/pytorch/pull/163468))
- [BC breaking] Remove deprecated imports for torch.utils.data.datapipes.iter.grouping ([#163438](https://github.com/pytorch/pytorch/pull/163438))
- [2/N] Add return types of Python functions ([#167203](https://github.com/pytorch/pytorch/pull/167203))
- [2/N] Use Python 3.10 typing ([#167167](https://github.com/pytorch/pytorch/pull/167167))
- [13/N] Use Python 3.10 typing  ([#169647](https://github.com/pytorch/pytorch/pull/169647))
- Fix pin memory return type when input is a tuple ([#169690](https://github.com/pytorch/pytorch/pull/169690))
### not user facing
- Skip test_ind_worker_queue on Windows and macOS (flaky) ([#162555](https://github.com/pytorch/pytorch/pull/162555))
- Update RandomSampler docstring. data_source must be Sized not Dataset ([#158857](https://github.com/pytorch/pytorch/pull/158857))
- remove allow-untyped-defs from ./torch/utils/data/datapipes/iter/fileopener.py ([#163469](https://github.com/pytorch/pytorch/pull/163469))
- [torch/utils][Code Clean] Clean asserts in `benchmark/` and `data/` in `torch/utils/` ([#165299](https://github.com/pytorch/pytorch/pull/165299))
- [3.14, dataloader] handle forkserver default mp start method in 3.14 ([#167387](https://github.com/pytorch/pytorch/pull/167387))
- [3.14, dataloader] handle forkserver default mp start method in 3.14 ([#167387](https://github.com/pytorch/pytorch/pull/167387))
- Fix dataloader tests failing on python 3.14 ([#167429](https://github.com/pytorch/pytorch/pull/167429))
### security
