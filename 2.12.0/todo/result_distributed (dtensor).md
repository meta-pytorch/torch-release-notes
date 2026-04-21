
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
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
### not user facing
- Make placements opaque ([#171482](https://github.com/pytorch/pytorch/pull/171482))
- Fix CPU test tolerances for low-precision operations ([#174953](https://github.com/pytorch/pytorch/pull/174953))
- [DTensor] Fixes a potential hang in ShardingPropagator when using multi-threading test ([#174820](https://github.com/pytorch/pytorch/pull/174820))
- Attempt to repro ([#175289](https://github.com/pytorch/pytorch/pull/175289))
- Add FakeTensor, ProxyTensor and serialization support to inductor_compiled_code HOP ([#174504](https://github.com/pytorch/pytorch/pull/174504))
- Add FakeTensor, ProxyTensor and serialization support to inductor_compiled_code HOP ([#174504](https://github.com/pytorch/pytorch/pull/174504))
- Make DeviceMesh opaque ([#169867](https://github.com/pytorch/pytorch/pull/169867))
- Start removing asserts in torch/distributed ([#174688](https://github.com/pytorch/pytorch/pull/174688))
- Start removing asserts in torch/distributed ([#174688](https://github.com/pytorch/pytorch/pull/174688))
- [DTensor] Enable Dijkstra search in sharding propagation ([#175999](https://github.com/pytorch/pytorch/pull/175999))
- [dtensor] Register sharding strategy for inductor_prims.fma ([#177424](https://github.com/pytorch/pytorch/pull/177424))
- [DTensor] Fix DTensor subclass __torch_dispatch__ bypass ([#177878](https://github.com/pytorch/pytorch/pull/177878))
- [Bugfix] Fix by copying sym shapes as needed ([#178210](https://github.com/pytorch/pytorch/pull/178210))
- Add support for twice-differentiable DTensor redistribution ([#160509](https://github.com/pytorch/pytorch/pull/160509))
- Centralize use_strided_shard_as_shard_order propagation for all ops ([#179208](https://github.com/pytorch/pytorch/pull/179208))
### security
