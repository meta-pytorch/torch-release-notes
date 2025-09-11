
# Release Notes worksheet optim

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

## optim
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
- [small][muon] Use addmm for Newton–Schulz orthogonalization ([#161379](https://github.com/pytorch/pytorch/pull/161379))
### docs
### devs
### Untopiced
- updated adafactor doc  #154862 ([#155248](https://github.com/pytorch/pytorch/pull/155248))
- swa avoid stream sync ([#157705](https://github.com/pytorch/pytorch/pull/157705))
- [BE] document Adadelta and Adagrad APIs properly ([#158483](https://github.com/pytorch/pytorch/pull/158483))
- Document the rest of the specific optimizer module APIs ([#158669](https://github.com/pytorch/pytorch/pull/158669))
- Split out C++ code from fused adagrad PR ([#159008](https://github.com/pytorch/pytorch/pull/159008))
- [BE] Remove more optim entries from docs coverage ignore list ([#160194](https://github.com/pytorch/pytorch/pull/160194))
- Optimzie `zero_grad` description ([#161239](https://github.com/pytorch/pytorch/pull/161239))
- [muon] Introduce Muon optimizer to PyTorch ([#160213](https://github.com/pytorch/pytorch/pull/160213))
- Fix LBFGS warning convert a tensor with requires_grad=True to a scalar ([#160389](https://github.com/pytorch/pytorch/pull/160389))
- Fix `SequentialLR` deprecate warning about invoke `step(epoch)` ([#149392](https://github.com/pytorch/pytorch/pull/149392))
- Unify TypeAlias definitions in optimizer.py ([#161493](https://github.com/pytorch/pytorch/pull/161493))
### not user facing
- [Pyrefly][Refactor] Replace dict() calls with literal dict syntax for improved readability ([#157735](https://github.com/pytorch/pytorch/pull/157735))
### security
