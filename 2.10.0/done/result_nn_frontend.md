
# Release Notes worksheet nn_frontend

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

## nn_frontend
### bc breaking
- Remove Nested Jagged Tensor support from `nn.attention.flex_attention` ([#161734](https://github.com/pytorch/pytorch/pull/161734))

This commit removes `nn.attention.flex_attention.create_nested_block_mask`.

### deprecation
### new features
- Add `nn.functional.scaled_mm` ([#164142](https://github.com/pytorch/pytorch/pull/164142))
- Add `nn.attention.varlen_attn` ([#164502](https://github.com/pytorch/pytorch/pull/164502), [#164504](https://github.com/pytorch/pytorch/pull/164504))
- Add `nn.functional.grouped_mm` ([#168298](https://github.com/pytorch/pytorch/pull/168298))

### improvements
- Support batch size 0 for flash attention in `scaled_dot_product_attention` ([#166318](https://github.com/pytorch/pytorch/pull/166318))
- Raise an error when using a sliced `BlockMask` in `nn.functional.flex_attention` ([#164702](https://github.com/pytorch/pytorch/pull/164702))

### bug fixes
- Fix silent correctness when backpropagating to `score_mod` in `nn.functional.flex_attention` ([#163677](https://github.com/pytorch/pytorch/pull/163677))
- Fix bug in `nn.Module.load_state_dict` for singleton tensor ([#166335](https://github.com/pytorch/pytorch/pull/166335))

### performance
### docs
- Update CTCLoss docs float32 input required for CuDNN ([#162042](https://github.com/pytorch/pytorch/pull/162042))
- Update LPPool docs to clarify ceil_mode padding semantics when ceil_mode=True ([#163186](https://github.com/pytorch/pytorch/pull/163186))

### devs
### Untopiced
### not user facing
### security
