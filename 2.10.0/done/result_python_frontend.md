
# Release Notes worksheet python_frontend

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

## python_frontend
### bc breaking
#### Fix python argument parsing for functions that take either tuple or vararg of ints ([#163081](https://github.com/pytorch/pytorch/pull/163081))

A bug was leading to some arguments being ignored. They will no longer be ignored!

Version <2.9
```python
import torch

my_tensor = torch.tensor([[0, 1, 2], [3, 4, 5]])

my_tensor.reshape((3, 2), torch.float32)
# tensor([[0, 1],
#         [2, 3],
#         [4, 5]])
# Note that the Tensor is NOT a float32
# and reshape doesn't expect a dtype argument!
```

Version >=2.10
```python
import torch

my_tensor = torch.tensor([[0, 1, 2], [3, 4, 5]])

my_tensor.reshape((3, 2), torch.float32)
# TypeError: reshape() takes 1 positional argument but 2 were given
# We get the expected error
```


### deprecation
### new features
### improvements
In the python frontend, the main improvements are:
- Improved `torch.library` and custom ops to support view functions ([#164520](https://github.com/pytorch/pytorch/pull/164520))
- Rework PyObject preservation to make it thread safe, significantly simpler and better handle some edge cases ([#167564](https://github.com/pytorch/pytorch/pull/167564))
- Remove reference cycle in torch.save to improve memory usage ([#165204](https://github.com/pytorch/pytorch/pull/165204))
- Add `generator` arg to `rand*_like` APIs ([#166160](https://github.com/pytorch/pytorch/pull/166160))
- support negative index arguments to torch.take_along_dim negative ([#152161](https://github.com/pytorch/pytorch/pull/152161))


### bug fixes
### performance
### docs
### devs
### Untopiced
### not user facing
### security
