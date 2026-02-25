
# Release Notes worksheet distributed (dtensor)

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

## distributed (dtensor)
### bc breaking
- [DTensor] Fix `to_local` backward by providing default `grad_placement` type ([#173454](https://github.com/pytorch/pytorch/pull/173454))
### deprecation
### new features
### improvements
### bug fixes
- Preserve Partial(max/min) on torch.max/min ([#170203](https://github.com/pytorch/pytorch/pull/170203))
- Prevent pointwise operations between Partials which are different ([#170209](https://github.com/pytorch/pytorch/pull/170209))
### performance
### docs
### devs
### Untopiced
- [DTensor] pr time benchmarks for collectives, from/to_local, backwards ([#171576](https://github.com/pytorch/pytorch/pull/171576))
- [DTensor] benchmark for misc dispatch paths ([#171847](https://github.com/pytorch/pytorch/pull/171847))
### not user facing
- [DTensor] Fix redistribute_cost to detect shard_order ([#170106](https://github.com/pytorch/pytorch/pull/170106))
- [DTensor] Fix redistribute_cost using incorrect comm_bytes_gb ([#170107](https://github.com/pytorch/pytorch/pull/170107))
- [DTensor] refactor redistribute_cost function ([#170108](https://github.com/pytorch/pytorch/pull/170108))
- [DTensor] Update redistribute planner cost function based on communication cost ([#170109](https://github.com/pytorch/pytorch/pull/170109))
- [DTensor] Fix _StridedShard to Replicate padding issue ([#170914](https://github.com/pytorch/pytorch/pull/170914))
- [DTensor] Added conversion from Replicate to _StridedShard ([#171337](https://github.com/pytorch/pytorch/pull/171337))
- Make placements opaque ([#171482](https://github.com/pytorch/pytorch/pull/171482))
- [DTensor] Make single-dim rules support multi-output ops ([#172257](https://github.com/pytorch/pytorch/pull/172257))
- Make placements opaque ([#171482](https://github.com/pytorch/pytorch/pull/171482))
- Make placements opaque ([#171482](https://github.com/pytorch/pytorch/pull/171482))
- [BE][Functorch] Add type hints to torch/_functorch files pt 3 ([#173543](https://github.com/pytorch/pytorch/pull/173543))
- [dtensor] fix flatten mesh dims arg relative to submesh ([#173790](https://github.com/pytorch/pytorch/pull/173790))
- [DTensor] support Partial input for matmul in single-dim registration ([#174926](https://github.com/pytorch/pytorch/pull/174926))
- [DTensor] support Partial input for matmul in single-dim registration ([#174926](https://github.com/pytorch/pytorch/pull/174926))
### security
