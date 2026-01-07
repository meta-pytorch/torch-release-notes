
# Release Notes worksheet distributed (checkpoint)

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

## distributed (checkpoint)
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- Avoid multiple storage writer resets in async save ([#159448](https://github.com/pytorch/pytorch/pull/159448))
- DTensor slice dequantization with proper block alignment ([#163532](https://github.com/pytorch/pytorch/pull/163532))
- Add option to use PrefixStore to create checkpoint background process ([#166560](https://github.com/pytorch/pytorch/pull/166560))
### performance
- Add timeout for checkpoint background process join ([#162828](https://github.com/pytorch/pytorch/pull/162828))
- Disable GC in process based async checkpointing ([#169613](https://github.com/pytorch/pytorch/pull/169613))
- Optimize global save-plan validation ([#166820](https://github.com/pytorch/pytorch/pull/166820))
- state dict staging fixes ([#166025](https://github.com/pytorch/pytorch/pull/166025))
### docs
### devs
### Untopiced
### not user facing
- Port 4 dynamo test files for the intel XPU ([#160953](https://github.com/pytorch/pytorch/pull/160953))
- UT/Examples for resharding checkpoint save/loads for distributed tensors with uneven shards. ([#160533](https://github.com/pytorch/pytorch/pull/160533))
- [CI][CUDA] Add periodic b200 distributed job ([#159323](https://github.com/pytorch/pytorch/pull/159323))
- [2/N] Correctly use test parameters  ([#166783](https://github.com/pytorch/pytorch/pull/166783))
- Add missing super().setUp() ([#167163](https://github.com/pytorch/pytorch/pull/167163))
- remove psutil dependency in asyncprocessexecutor for oss ([#169985](https://github.com/pytorch/pytorch/pull/169985))
- Add logging for individual state_dict calls ([#169511](https://github.com/pytorch/pytorch/pull/169511))
- Add huggingface storage reader for MXFP4 quantized GPT-OSS checkpoint ([#167672](https://github.com/pytorch/pytorch/pull/167672))
- Make `_flatten_optim_state_dict` and `_unflatten_optim_state_dict` handle arbitrary-level of nested optim dictionaries by recursion ([#165071](https://github.com/pytorch/pytorch/pull/165071))
- Add option to use PrefixStore to create checkpoint background process ([#166560](https://github.com/pytorch/pytorch/pull/166560))
- Replace assert statements in distributed checkpoint with explicit checks (distributed) ([#165256](https://github.com/pytorch/pytorch/pull/165256))
### security
