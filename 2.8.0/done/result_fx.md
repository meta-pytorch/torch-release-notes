
# Release Notes worksheet fx

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

## fx
### bc breaking
### deprecation
### new features
### improvements
- Remove warnings on non-buffer tensor constants ([#148483](https://github.com/pytorch/pytorch/pull/148483))
- Update codegen compare op to == ([#150611](https://github.com/pytorch/pytorch/pull/150611))
- Map names to operand indices when const folding submodules ([#150692](https://github.com/pytorch/pytorch/pull/150692))
- Improve stacktrace when tracing ([#151029](https://github.com/pytorch/pytorch/pull/151029), [#155486](https://github.com/pytorch/pytorch/pull/155486))
- Support edge dialect ops in normalize_function ([#143689](https://github.com/pytorch/pytorch/pull/143689))
- Adding fbgemm to pickle whitelist ([#152079](https://github.com/pytorch/pytorch/pull/152079))
- Fix path naming in minifier ([#153130](https://github.com/pytorch/pytorch/pull/153130))
- Add graph_code_verbose_log artifact for fx passes ([#153775](https://github.com/pytorch/pytorch/pull/153775))
- Improve cache key graph printing performance ([#151928](https://github.com/pytorch/pytorch/pull/151928))
### bug fixes
### performance
### docs
- Rename `__is_node_supported` to `_is_node_supported` ([#149400](https://github.com/pytorch/pytorch/pull/149400))
- Fix 'intialize' -> 'initialize' typo ([#155301](https://github.com/pytorch/pytorch/pull/155301))
### devs
- Gracefully exit minimizer when there is no discrepancy in block mode ([#154076](https://github.com/pytorch/pytorch/pull/154076))
- Add __main__ guards to fx tests ([#154715](https://github.com/pytorch/pytorch/pull/154715))
### Untopiced

### not user facing
- [Partitioner] Reduce time consuming of partitions merger ([#146582](https://github.com/pytorch/pytorch/pull/146582))
- [Partitioner] Remove unnecessary upstream nodes in dependency viewer ([#146580](https://github.com/pytorch/pytorch/pull/146580))
- [fx] Recursive DCE on subgraphs ([#152772](https://github.com/pytorch/pytorch/pull/152772))
- [invoke_subgraph] Run missing graph passes recursively ([#152675](https://github.com/pytorch/pytorch/pull/152675))
- Thread through options so GraphPickler can allow all ops ([#152801](https://github.com/pytorch/pytorch/pull/152801))
- check fallback_value first.  ([#154493](https://github.com/pytorch/pytorch/pull/154493))
- [BE][Ez]: Optimize unnecessary lambda with operator ([#154722](https://github.com/pytorch/pytorch/pull/154722))
- Migrate from lru_cache to cache ([#155613](https://github.com/pytorch/pytorch/pull/155613))
- Fix provenance unit test ([#155747](https://github.com/pytorch/pytorch/pull/155747))
- Fix logging of failed tensorified ops ([#155982](https://github.com/pytorch/pytorch/pull/155982))
- [BE][PYFMT] migrate PYFMT for `torch/[e-n]*/` to `ruff format` ([#144553](https://github.com/pytorch/pytorch/pull/144553))
- remove allow-untyped-defs from torch/fx/passes/utils/fuser_utils.py ([#156538](https://github.com/pytorch/pytorch/pull/156538))

### security
