
# Release Notes worksheet python_frontend

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

## python_frontend
### bc breaking
#### Upgrade to DLPack 1.0. ([#145000](https://github.com/pytorch/pytorch/pull/145000))

This upgrade is doing the same BC-breaking changes as the DLPack release.
Objects in `torch.utils.dlpack` have been updated to reflect these changes, such as `DLDeviceType`.
See the PR for details on the exact changes and how to update your code.


- Raise appropriate errors in `torch.cat` ([#158249](https://github.com/pytorch/pytorch/pull/158249))
Raising ValueError, IndexError or TypeError where appropriate instead of the generic RuntimeError.
If you code was catching these error, you can update to catch the new error type.

### deprecation
### new features
- Add utility to get the kernel currently registered on the dispatcher ([#158393](https://github.com/pytorch/pytorch/pull/158393))
- Extend `__torch_function__` handler to be triggered by elements within a list ([#160256](https://github.com/pytorch/pytorch/pull/160256))

### improvements
- Speed up torch.load under FakeTensorMode by reducing random reads ([#157931](https://github.com/pytorch/pytorch/pull/157931))
- Make torch.utils.benchmark.utils.timer accelerator agnostic ([#157131](https://github.com/pytorch/pytorch/pull/157131))


### bug fixes
- Add option in `torch.utils.cpp_extension.load_inline` to override gencode ([#156850](https://github.com/pytorch/pytorch/pull/156850))
- Fix max_width computation in Tensor printing ([#126859](https://github.com/pytorch/pytorch/pull/126859))
- Improve pin_memory error message on CPU-only systems ([#159994](https://github.com/pytorch/pytorch/pull/159994))

### performance
### docs
- Improve documentation for `torch.lobpcg`, `torch.clone`, `torch.matmul`, `torch.max`, `torch.gather`, `torch.Tensor.scatter_`, `torch.empty_like`, `torch.randint`, `torch.mul`, `torch.min`, `torch.max`. `torch.sort`, `torch.full_like`, `torch.histogramdd`, `torch.hamming_window` ([#156139](https://github.com/pytorch/pytorch/pull/156139), [#157007](https://github.com/pytorch/pytorch/pull/157007), [#161424](https://github.com/pytorch/pytorch/pull/161424), [#156153](https://github.com/pytorch/pytorch/pull/156153), [#157929](https://github.com/pytorch/pytorch/pull/157929), [#157920](https://github.com/pytorch/pytorch/pull/157920), [#158050](https://github.com/pytorch/pytorch/pull/158050), [#158731](https://github.com/pytorch/pytorch/pull/158731), [#160312](https://github.com/pytorch/pytorch/pull/160312), [#161539](https://github.com/pytorch/pytorch/pull/161539), [#162051](https://github.com/pytorch/pytorch/pull/162051), [#158275](https://github.com/pytorch/pytorch/pull/158275), [#152682](https://github.com/pytorch/pytorch/pull/152682))
- Remove torchscript related sections in serialization docs ([#156648](https://github.com/pytorch/pytorch/pull/156648))
- Fix typo in `torch.set_float32_matmul_precision` docs ([#158191](https://github.com/pytorch/pytorch/pull/158191))
- Fix docstring for `torch.nn.utils.clip_grads_with_norm_` to reflect clamping behavior ([#158200](https://github.com/pytorch/pytorch/pull/158200))
- Fix the Doc issue on the description of edge_order in `torch.gradient` ([#159130](https://github.com/pytorch/pytorch/pull/159130))
- Add `torch.segment_reduce` docs ([#154352](https://github.com/pytorch/pytorch/pull/154352))
- Add examples to `torch.is_floating_point` and `torch.is_complex` docs ([#161951](https://github.com/pytorch/pytorch/pull/161951))

### devs
- Better sample inputs for addmm OpInfo ([#160234](https://github.com/pytorch/pytorch/pull/160234))

### Untopiced
### not user facing
### security
- Don't store flamegraph to tmp folder ([#157374](https://github.com/pytorch/pytorch/pull/157374))
