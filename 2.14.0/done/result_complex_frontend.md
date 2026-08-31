
# Release Notes worksheet complex_frontend

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

## complex_frontend
### bc breaking
- Complex type promotion for `bfloat16` now uses the new `torch.bcomplex32` shell dtype instead of `torch.complex64` ([#186928](https://github.com/pytorch/pytorch/pull/186928))

  `torch.bcomplex32` stores real and imaginary components as `bfloat16`. Operations that combine a `bfloat16` tensor with a complex scalar or otherwise request its corresponding complex type can therefore produce `bcomplex32` instead of `complex64`. Because `bcomplex32` is a shell dtype with limited operator support, an operation that previously ran in `complex64` may now raise a not-implemented error. Explicitly cast to `complex64` when the previous precision or operator coverage is required.

  Version 2.13:

  ```python
  x = torch.ones(4, dtype=torch.bfloat16)
  assert torch.result_type(x, 1j) == torch.complex64
  ```

  Version 2.14:

  ```python
  x = torch.ones(4, dtype=torch.bfloat16)
  assert torch.result_type(x, 1j) == torch.bcomplex32

  # Preserve the previous complex64 behavior explicitly.
  y = x.to(torch.complex64) + 1j
  ```
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### not user facing
- Fix private `ComplexTensor.mul_` in-place identity and result semantics, and support real left-hand operands in `torch.ne` for `ComplexTensor` values ([#188839](https://github.com/pytorch/pytorch/pull/188839))
### security
