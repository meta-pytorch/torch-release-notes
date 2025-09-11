
# Release Notes worksheet jit

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

## jit
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- added stubs for jit tree views ([#156504](https://github.com/pytorch/pytorch/pull/156504))
- Remove ts to export retracer ([#156857](https://github.com/pytorch/pytorch/pull/156857))
- [BE][12/16] fix typos in torch/ ([#156602](https://github.com/pytorch/pytorch/pull/156602))
- Fix 'dllimport attribute ignored on inline function' ([#157670](https://github.com/pytorch/pytorch/pull/157670))
- [1/n] Remove references to TorchScript in PyTorch docs ([#158305](https://github.com/pytorch/pytorch/pull/158305))
- [2/n] Remove references to TorchScript in PyTorch docs ([#158306](https://github.com/pytorch/pytorch/pull/158306))
- [3/n] Remove references to TorchScript in PyTorch docs ([#158315](https://github.com/pytorch/pytorch/pull/158315))
- [4/n] Remove references to TorchScript in PyTorch docs ([#158317](https://github.com/pytorch/pytorch/pull/158317))
- [BE][EZ] Minor doc fixes (193b29ee0c9)
- Fix warnings of unused-variable ([#158627](https://github.com/pytorch/pytorch/pull/158627))
- [TorchScript, PT2] Add torch._check compatibility support ([#159988](https://github.com/pytorch/pytorch/pull/159988))
- [TorchScript] thread-safe ErrorReport::CallStack ([#160386](https://github.com/pytorch/pytorch/pull/160386))
- [PT2]: Allow None for wrapped_fbgemm_linear_fp16_weight ([#160802](https://github.com/pytorch/pytorch/pull/160802))
- [TorchScript] ProfilingExecutor - RemoveProfileNodesAndSpecializeTypes None handling ([#161538](https://github.com/pytorch/pytorch/pull/161538))
- Fix non-const reference arguments in torch/csrc/jit/python/init.cpp ([#161300](https://github.com/pytorch/pytorch/pull/161300))
- Fix forced copying def_property_readonly for FunctionSchema & friends ([#161301](https://github.com/pytorch/pytorch/pull/161301))
- Add C++ function for torch.distributed.tensor._op_schema.is_view_op ([#161595](https://github.com/pytorch/pytorch/pull/161595))
- Avoid redundant PyTuple_GetSize call in _maybe_handle_torch_function ([#161633](https://github.com/pytorch/pytorch/pull/161633))
- Overload _get_operation_for_overload_or_packet & friends to accept ArrayRef ([#162219](https://github.com/pytorch/pytorch/pull/162219))
### not user facing
- Better fix for `__index__` SymInt issue ([#157201](https://github.com/pytorch/pytorch/pull/157201))
- [BE][8/16] fix typos in torch/ (torch/csrc/jit/) ([#156318](https://github.com/pytorch/pytorch/pull/156318))
- [BE][10/16] fix typos in torch/ (torch/csrc/jit/) ([#156320](https://github.com/pytorch/pytorch/pull/156320))
- [nativert] Add OSS version of ModelRunner ([#159268](https://github.com/pytorch/pytorch/pull/159268))
- [ROCm] Fix resource_strings.h ([#159996](https://github.com/pytorch/pytorch/pull/159996))
### security
