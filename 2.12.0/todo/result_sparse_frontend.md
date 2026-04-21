
# Release Notes worksheet sparse_frontend

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

## sparse_frontend
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- Implement clone operator for the semi tensor ([#174991](https://github.com/pytorch/pytorch/pull/174991))
- [cuSPARSE] torch.bmm(COO, Dense): fix for memory misalignment + minor perf improvements ([#175347](https://github.com/pytorch/pytorch/pull/175347))
- Include thrust/pair.h in each TU where thrust::pair is used ([#169267](https://github.com/pytorch/pytorch/pull/169267))
- implement branch free and guard free padding+mul operator (#177699) ([#177699](https://github.com/pytorch/pytorch/pull/177699))
- [HIM][sparsity][x/n] Allow semi tensor to be instantiated with alg_id (#178659) (#178659) ([#178659](https://github.com/pytorch/pytorch/pull/178659))
- Optimize the performance by reducing the cpu overhead (#179193) ([#179193](https://github.com/pytorch/pytorch/pull/179193))
- [TorchAO][hipSPARSELt] Enable FP8 semi-structured sparsity on ROCm (#179310) ([#179310](https://github.com/pytorch/pytorch/pull/179310))
- [TorchAO][hipSPARSELt] Add alg_id to FP8 semi-structured sparsity benchmark ([#179926](https://github.com/pytorch/pytorch/pull/179926))
### not user facing
- [CUDA] Abate `thrust::distance` deprecation warnings ([#171722](https://github.com/pytorch/pytorch/pull/171722))
- [BE] Use `REGISTER_ALL_CPU_DISPATCH` ([#176255](https://github.com/pytorch/pytorch/pull/176255))
- Fix: treat empty tensors as contiguous in sparse validation ([#178419](https://github.com/pytorch/pytorch/pull/178419))
- fix unit test failure in semi_structure to() op (#178667) (#178667) (#178667) ([#178667](https://github.com/pytorch/pytorch/pull/178667))
### security
