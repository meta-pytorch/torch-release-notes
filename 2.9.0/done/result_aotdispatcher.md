
# Release Notes worksheet aotdispatcher

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

## aotdispatcher
### bc breaking
### deprecation
### new features
- Add AOTDispatcher config to set backward autocast behavior ([#156356](https://github.com/pytorch/pytorch/pull/156356))
### improvements
- Skip logging in fp8 activation quantization if there are no nodes to be quantized ([#158129](https://github.com/pytorch/pytorch/pull/158129))
- Add aot_export_joint_with_descriptors and aot_compile_joint_with_descriptors ([#158715](https://github.com/pytorch/pytorch/pull/158715))
- Allow keeping input mutations in the graph for `_aot_export_function` ([#157730](https://github.com/pytorch/pytorch/pull/157730))
- Extract out prepare_aot_module_simplified for use in next PR ([#158319](https://github.com/pytorch/pytorch/pull/158319))
- Rename modules in AOTAutograd ([#158449](https://github.com/pytorch/pytorch/pull/158449))
- Track descriptors for all inputs/outputs of AOTAutograd traced graph ([#158624](https://github.com/pytorch/pytorch/pull/158624))
- Improve graph output alias with subclass error message ([#159619](https://github.com/pytorch/pytorch/pull/159619))
- Pass fw/bw compilers to aot_export_joint_with_descriptors ([#159814](https://github.com/pytorch/pytorch/pull/159814))

### bug fixes
### performance
### docs
### devs
### Untopiced
### not user facing
### security
