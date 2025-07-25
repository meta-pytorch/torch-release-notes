
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
- Add missing in-place on view check to custom autograd.Function ([#153094](https://github.com/pytorch/pytorch/pull/153094))

  In 2.8.0, if a custom autograd.Function mutates a view of a leaf requiring grad,
  it now properly raises an error. Previously, it would silently leak memory.
  ```
     class Func(torch.autograd.Function):
          @staticmethod
          def forward(ctx, inp):
              inp.add_(1)
              ctx.mark_dirty(inp)
              return inp
  
          @staticmethod
          def backward(ctx, gO):
              pass
  
      a = torch.tensor([1.0, 2.0], requires_grad=True)
      b = a.view_as(a)
      Func.apply(b)
  ```
  Output:

  2.8.0
  ```
  RuntimeError: a view of a leaf Variable that requires grad is being used in an in-place operation
  ```
  2.7.0
  ```
  Runs without error, but leaks memory
  ```

### deprecation
### new features
### improvements
- Improve error message when view of intermediate is returned from autograd.Function and marked dirty ([#149543](https://github.com/pytorch/pytorch/pull/149543))
- Fix `torch.autograd.backward` `inputs` validation ([#150975](https://github.com/pytorch/pytorch/pull/150975))

### bug fixes
### performance
- Rewrite autograd streams synchronization ([#151079](https://github.com/pytorch/pytorch/pull/151079))
### docs
- Update docs of `torch.autograd.graph.saved_tensors_hooks` to avoid ref cycle ([#153049](https://github.com/pytorch/pytorch/pull/153049))
- Mention that it's possible to set debug=True in `torch.utils.checkpoint.checkpoint` error messages ([#155593](https://github.com/pytorch/pytorch/pull/155593))
- Add more details on why `ctx.save_for_backward` is important in extending autograd note ([#153005](https://github.com/pytorch/pytorch/pull/153005))
- Update gradient behavior note in `torch.amin` and `torch.amax` ([#155071](https://github.com/pytorch/pytorch/pull/155071))

### devs
### Untopiced
### not user facing
- Add missing attr access check for legacy autograd.Function ([#155055](https://github.com/pytorch/pytorch/pull/155055))
- [3/N] Use internal linkage in C++ files  ([#151297](https://github.com/pytorch/pytorch/pull/151297))

### security
