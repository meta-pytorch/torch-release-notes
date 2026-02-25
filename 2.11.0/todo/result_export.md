
# Release Notes worksheet export

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

## export
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [export] Deepcopy graph signature when unlifting ([#170461](https://github.com/pytorch/pytorch/pull/170461))
- [reland][export] Make RNNs exportable on GPUs ([#169710](https://github.com/pytorch/pytorch/pull/169710))
- Serialize from_node info in torch export serializer ([#171726](https://github.com/pytorch/pytorch/pull/171726))
- Ensure tensor name consistency before and after torch.export.save ([#171954](https://github.com/pytorch/pytorch/pull/171954))
- [nativert] Add MtiaTritonKernelManager for MTIA Triton kernel execution ([#171492](https://github.com/pytorch/pytorch/pull/171492))
- [nativert] Refactor LaunchParams to use target-specific subclasses ([#172084](https://github.com/pytorch/pytorch/pull/172084))
- Harden non strict leak detector some more ([#172597](https://github.com/pytorch/pytorch/pull/172597))
- Fix the incomplete tensor (cuDNN packs) on torch.export ([#172805](https://github.com/pytorch/pytorch/pull/172805))
- Fix import error in aoti load ([#173751](https://github.com/pytorch/pytorch/pull/173751))
- support strobelight profiling export ([#174606](https://github.com/pytorch/pytorch/pull/174606))
- add nested tensor serialization support ([#174720](https://github.com/pytorch/pytorch/pull/174720))
### not user facing
- Support shift operations in serialize/export ([#167913](https://github.com/pytorch/pytorch/pull/167913))
- [export] check in state dict utils ([#171599](https://github.com/pytorch/pytorch/pull/171599))
- Remove assert for export files ([#172124](https://github.com/pytorch/pytorch/pull/172124))
- [export] Use bytecode to flatten graph inputs. (#171110) ([#172870](https://github.com/pytorch/pytorch/pull/172870))
- [export] Use bytecode to flatten graph inputs. (#171110) ([#172870](https://github.com/pytorch/pytorch/pull/172870))
- Opt in files typechecking ([#172969](https://github.com/pytorch/pytorch/pull/172969))
- Simplify_ zipfile_ syntax ([#173378](https://github.com/pytorch/pytorch/pull/173378))
- Start removing assert in torch/_export ([#172481](https://github.com/pytorch/pytorch/pull/172481))
- More torch/_export migration ([#172487](https://github.com/pytorch/pytorch/pull/172487))
- Finish functorch and export assert removal ([#174212](https://github.com/pytorch/pytorch/pull/174212))
### security
