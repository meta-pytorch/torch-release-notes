
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
### improvements
### bug fixes
- Fix torch.trace backward for non-square matrices ([#175068](https://github.com/pytorch/pytorch/pull/175068))
- [autograd] Explicitly error when layer_norm computes 3rd order derivatives ([#176234](https://github.com/pytorch/pytorch/pull/176234))
- Fix _wrap_sync_node to replace deps in output node's nested args ([#178471](https://github.com/pytorch/pytorch/pull/178471))
### performance
### docs
### devs
### Untopiced
- Use non-blocking copy in save_on_cpu pack ([#175421](https://github.com/pytorch/pytorch/pull/175421))
- No longer use autograd.Function to save inputs in torch.utils.checkpoint  ([#174327](https://github.com/pytorch/pytorch/pull/174327))
- Implement narrow_copy derivative ([#175609](https://github.com/pytorch/pytorch/pull/175609))
- [varlen] expose num_splits to provide option to disable split_kv ([#176905](https://github.com/pytorch/pytorch/pull/176905))
- Register numel, dim, get_device, storage_offset, is_contiguous in native_functions.yaml ([#177200](https://github.com/pytorch/pytorch/pull/177200))
- [BE]: Implement higher order derivative to grid_sample  ([#177487](https://github.com/pytorch/pytorch/pull/177487))
- Support user AutoNamingMode in SAC ([#175348](https://github.com/pytorch/pytorch/pull/175348))
### not user facing
- Replace PyObject_Type with Py_TYPE ([#178835](https://github.com/pytorch/pytorch/pull/178835))
- [autograd] Fix thread-unsafe lazy init of setup_context cache ([#179475](https://github.com/pytorch/pytorch/pull/179475))
- [autograd] Implement backward and forward AD for torch.aminmax ([#175215](https://github.com/pytorch/pytorch/pull/175215))
### security
