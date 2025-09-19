
# Release Notes worksheet autograd_frontend

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

## autograd_frontend
### bc breaking
### deprecation
### new features
### improvements
- Support deterministic `torch.nn.Upsample` `mode="trilinear"` backward ([#154239](https://github.com/pytorch/pytorch/pull/154239))
### bug fixes
- Fix `torch.autograd.Function` memory leak due to `torch.utils.checkpiont` early stopping ([#161171](https://github.com/pytorch/pytorch/pull/161171))
- Fix `torch.autograd.graph.GradientEdge` for `torch.autograd.Function` ([#160098](https://github.com/pytorch/pytorch/pull/160098))
- Match 0-dim gradients device type regardless of subclass-ness ([#160165](https://github.com/pytorch/pytorch/pull/160165))

### performance
- Fix SVD forward-mode AD multiplication priority ([#161027](https://github.com/pytorch/pytorch/pull/161027))

### docs
- Improve `torch.inference_mode` docs and error message ([#161164](https://github.com/pytorch/pytorch/pull/161164))

### devs
### Untopiced
### not user facing
- [autograd] torch._C._set_view_replay_enabled state leaking into other tests ([#159840](https://github.com/pytorch/pytorch/pull/159840))
- Add new parameter for gen_pyi.py to make it more configureable. ([#161772](https://github.com/pytorch/pytorch/pull/161772))
- Remove guard_size_oblivious from default contiguity python check, and add aten.sym_is_contiguous. [attempt2] ([#160869](https://github.com/pytorch/pytorch/pull/160869))
- [while_loop][autograd] add hop while_loop_stack_output ([#160467](https://github.com/pytorch/pytorch/pull/160467))

### security
