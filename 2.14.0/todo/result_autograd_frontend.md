
# Release Notes worksheet autograd_frontend

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

## autograd_frontend
### bc breaking
### deprecation
### new features
- Add torch.autograd.graph.node_creation_hook ([#189284](https://github.com/pytorch/pytorch/pull/189284))
- autograd: add ctx.set_output_grad_dtype ([#189634](https://github.com/pytorch/pytorch/pull/189634))
### improvements
### bug fixes
- Fix pow backward crash when base is a bool scalar ([#182564](https://github.com/pytorch/pytorch/pull/182564))
- [partitioner] Fix memory-budget short-circuit emitting non-saveable tuple node ([#188014](https://github.com/pytorch/pytorch/pull/188014))
- Fix ldexp gradient for negative integer exponents ([#186566](https://github.com/pytorch/pytorch/pull/186566))
- Fix max_pool double backward under vmap for channels_last inputs ([#191678](https://github.com/pytorch/pytorch/pull/191678))
### performance
### docs
### devs
### Untopiced
- Implement Double Backward for `cdist` and `pdist` ([#188901](https://github.com/pytorch/pytorch/pull/188901))
- Stop copying at::Tensor when profiler is off ([#189582](https://github.com/pytorch/pytorch/pull/189582))
- Use `ArrayRef<const Variable*> in autograd.Function.apply ([#189788](https://github.com/pytorch/pytorch/pull/189788))
- Move autograd.Function output instead of copying it ([#189800](https://github.com/pytorch/pytorch/pull/189800))
- Fix misleading full-backward-hook warning for pre-hook-only modules ([#190685](https://github.com/pytorch/pytorch/pull/190685))
- native_group_norm_backward: Fix precision errors ([#190245](https://github.com/pytorch/pytorch/pull/190245))
- [autograd] Guard end-of-backward leaf syncs that cross a CUDA graph capture boundary ([#189591](https://github.com/pytorch/pytorch/pull/189591))
- Error on unsupported batch norm third derivatives ([#186779](https://github.com/pytorch/pytorch/pull/186779))
- [autograd] Align clamp and min/max subgradients with dispatcher schemas ([#191142](https://github.com/pytorch/pytorch/pull/191142))
- [BE][Ez]: Improve constant folding backwards in derivatives.yaml ([#192611](https://github.com/pytorch/pytorch/pull/192611))
### not user facing
- Fix DeviceContext mode leaks from checkpoint recompute and set_default_device restore ([#189286](https://github.com/pytorch/pytorch/pull/189286))
- [autograd] Fall back to tensor backward for symbolic pow exponent ([#185851](https://github.com/pytorch/pytorch/pull/185851))
- native_group_norm: Handle non-contiguous tensors, rather than throwing ([#186414](https://github.com/pytorch/pytorch/pull/186414))
- [autograd] Expose wrapped node on CopySlices ([#190806](https://github.com/pytorch/pytorch/pull/190806))
- [autograd] Preserve dynamic content in THPFunction error messages ([#191748](https://github.com/pytorch/pytorch/pull/191748))
- Don't leak objects returned by users setup_context ([#191966](https://github.com/pytorch/pytorch/pull/191966))
- [BE][Ez]: Improve readability and accuracy of log2/log10 backwards ([#192613](https://github.com/pytorch/pytorch/pull/192613))
### security
