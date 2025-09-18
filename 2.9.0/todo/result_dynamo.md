
# Release Notes worksheet dynamo

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

## dynamo
### bc breaking
### deprecation
### new features
- Experimental API for ahead-of-time compiling models in fullgraph mode ([#161383](https://github.com/pytorch/pytorch/pull/161383))
- Toggle erroring/resume on graph break with `torch._dynamo.error_on_graph_break` ([#161739](https://github.com/pytorch/pytorch/pull/161739), [#161747](https://github.com/pytorch/pytorch/pull/161747))
- Add a hook for recompilations ([#157961](https://github.com/pytorch/pytorch/pull/157961))
### improvements
- Improved tracing support for various Python builtin data structures/modules:
    - `list`s (e.g. [#153969](https://github.com/pytorch/pytorch/pull/153969))
    - `set`s (e.g. [#153150](https://github.com/pytorch/pytorch/pull/153150))
    - `dict`s (e.g. [#154794](https://github.com/pytorch/pytorch/pull/154794))
    - `iter` (e.g. [#156371](https://github.com/pytorch/pytorch/pull/156371))
    - `itertools` (e.g. [#159693](https://github.com/pytorch/pytorch/pull/159693))
    - `collections` (e.g. [#159365](https://github.com/pytorch/pytorch/pull/159365))
    - `collections.NamedTuple` ([#159367](https://github.com/pytorch/pytorch/pull/159367))
    - frozen `dataclasses.dataclass` ([#159529](https://github.com/pytorch/pytorch/pull/159529))
- Graph break error messages link to a website with more information ([#159011](https://github.com/pytorch/pytorch/pull/159011))
- Add option for TorchDispatchMode to ignore torch.compile internals ([#161648](https://github.com/pytorch/pytorch/pull/161648))
### bug fixes
- Fix segfault due to interaction between Dynamo backends and `torch.compiler.reset()` ([#156527](https://github.com/pytorch/pytorch/pull/156527))
- Fix crash due to bad interaction with recompilations and with blocks in Python 3.11+ ([#162318](https://github.com/pytorch/pytorch/pull/162318))
### performance
- Recursive `dict` tag optimization for faster guard evaluation ([#159183](https://github.com/pytorch/pytorch/pull/159183))
### docs
### devs
### Untopiced
### not user facing
### security
