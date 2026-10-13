
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
- Expose InputBuffer as ctx.input_grad_buffers in autograd.Function backward ([#196491](https://github.com/pytorch/pytorch/pull/196491))
### improvements
### bug fixes
- [autograd] Refresh view grad_fn before registering hooks ([#196514](https://github.com/pytorch/pytorch/pull/196514))
### performance
### docs
- [docs] Advertise torch_remat for region-level SAC ([#193998](https://github.com/pytorch/pytorch/pull/193998))
### devs
### Untopiced
- [autograd] Update fmin and fmax gradients to follow forward NaN handling behavior ([#193035](https://github.com/pytorch/pytorch/pull/193035))
- Add Autograd Support for Low-Level Bessel Functions ([#189872](https://github.com/pytorch/pytorch/pull/189872))
- [autograd] Expose queue_callback as torch.autograd.graph.queue_callback ([#193958](https://github.com/pytorch/pytorch/pull/193958))
- Fix fast gradcheck when non-differentiable outputs precede differentiable ones ([#194222](https://github.com/pytorch/pytorch/pull/194222))
- grid_sample: support mode='bicubic' with 5-D input, including its double backward ([#194787](https://github.com/pytorch/pytorch/pull/194787))
- Document that saved_tensors_hooks unpack ordering is unspecified ([#198016](https://github.com/pytorch/pytorch/pull/198016))
- Add forward AD support for grid_sample ([#195280](https://github.com/pytorch/pytorch/pull/195280))
### not user facing
- [RAWTHROW][1c] Remove the reason for eight annotated raw throws ([#193618](https://github.com/pytorch/pytorch/pull/193618))
- [RAWTHROW][2b] The long tail: delete eleven exclude patterns ([#194245](https://github.com/pytorch/pytorch/pull/194245))
- Bind the generated grad_fn loop variable by reference ([#194882](https://github.com/pytorch/pytorch/pull/194882))
- Fix TensorList storage sanity-check codegen ([#195857](https://github.com/pytorch/pytorch/pull/195857))
- [autograd] Expose explicit grad_dtype configuration ([#197504](https://github.com/pytorch/pytorch/pull/197504))
### security
