
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
- Support serializing nested integer and floating-point list arguments, including empty nested lists, for custom operators in exported programs. ([#189424](https://github.com/pytorch/pytorch/pull/189424))
### performance
- Reduce decomposition-time complexity for large exported graphs from super-linear to linear growth by avoiding repeated scans of graph-signature and module metadata. ([#177927](https://github.com/pytorch/pytorch/pull/177927))
### docs
### devs
- Improve raw Triton kernel errors during non-strict export with guidance to define the kernel through `torch.library.triton_op` and launch it through `torch.library.wrap_triton` or `torch._library.capture_triton`. ([#185827](https://github.com/pytorch/pytorch/pull/185827))
- Improve the readability of draft-export reports on light terminal backgrounds by using red for warning banners, green for success banners, and the terminal's default color for failure details. ([#186070](https://github.com/pytorch/pytorch/pull/186070))
### bug fixes
- Prevent `ExportedProgram.module()` from raising `RecursionError` while generating guard messages for deeply nested symbolic-shape expressions. ([#186993](https://github.com/pytorch/pytorch/pull/186993))
- Fix `torch.export.unflatten` failing to restore parameters, buffers, and constants for non-contiguously numbered repeated module calls. ([#188185](https://github.com/pytorch/pytorch/pull/188185))
- Fix strict export of parameters from modules stored in unregistered Python containers by treating the traced-only parameters as constants instead of attempting to restore them from the eager module's state. ([#185728](https://github.com/pytorch/pytorch/pull/185728))
- Fix non-strict export of tensor indexing under `vmap` when the index is a batched scalar tensor. ([#186894](https://github.com/pytorch/pytorch/pull/186894))
### not user facing
- Enable stricter static type checking for private export and serialization modules, with no runtime behavior change. ([#187711](https://github.com/pytorch/pytorch/pull/187711))
- Remove duplicated words from docstrings across export and other PyTorch modules. ([#188884](https://github.com/pytorch/pytorch/pull/188884))
- Support `ObjectSpec`, `SeqSpec`, and `DictSpec` container types when using shape specifications with strict export. ([#186167](https://github.com/pytorch/pytorch/pull/186167))
- Add the `torch.fx.experimental.dynamic_spec.dynamic_spec` decorator for attaching a dynamic-shape specification to a function or `nn.Module.forward`. `torch.compile`, `torch.export.export`, and `make_fx` automatically use the attached specification; passing a conflicting call-site specification raises an error. ([#187639](https://github.com/pytorch/pytorch/pull/187639))
### security
