
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
- `torch.compile` now fully works in Python 3.14 ([#167384](https://github.com/pytorch/pytorch/pull/167384))
- Add option to error or disable applying side effects ([#167239](https://github.com/pytorch/pytorch/pull/167239))
- Config flag (`skip_fwd_side_effects_in_bwd_under_checkpoint`) to allow eager and compile activation-checkpointing divergence for side-effects ([#165775](https://github.com/pytorch/pytorch/pull/165775))
- `torch._higher_order_ops.print` for enabling printing without graph breaks or reordering ([#167571](https://github.com/pytorch/pytorch/pull/167571))
### improvements
- Turn on `capture_scalar_outputs` and `capture_dynamic_output_shape_ops` when `fullgraph=True` ([#163121](https://github.com/pytorch/pytorch/pull/163121), [#163123](https://github.com/pytorch/pytorch/pull/163123))
- Improved tracing for `dict` key hashing ([#169204](https://github.com/pytorch/pytorch/pull/169204))
- Tracing support for `torch.cuda.stream` ([#166472](https://github.com/pytorch/pytorch/pull/166472))
- Improved tracing of `torch.autograd.Function`s ([#166788](https://github.com/pytorch/pytorch/pull/166788))
- Miscellaneous smaller tracing support additions:
  - Extend `collections.defaultdict` support with `*args`, `**kwargs` and custom `default_factory` ([#166793](https://github.com/pytorch/pytorch/pull/166793))
  - Support for bitwise xor ([#166065](https://github.com/pytorch/pytorch/pull/166065))
  - Support `repr` on user-defined objects ([#167372](https://github.com/pytorch/pytorch/pull/167372))
  - Support new typing union syntax `X | Y` ([#166599](https://github.com/pytorch/pytorch/pull/166599))
### bug fixes
- Fixed `cProfile` usage with `torch.compile` in Python 3.12+ ([#170013](https://github.com/pytorch/pytorch/pull/170013))
- Fix memory leak in tensor subclass metadata guard ([#167352](https://github.com/pytorch/pytorch/pull/167352))
### performance
- Faster tracing of some pytree functions ([#168342](https://github.com/pytorch/pytorch/pull/168342))
### docs
- Updated documentation for `tlparse` ([#171339](https://github.com/pytorch/pytorch/pull/171339)).
  `tlparse` is a compilation report tool that processes `TORCH_TRACE` logs to generate interactive HTML reports showing how your model was compiled.
  When reporting bugs to PyTorch developers, we encourage you to attach the trace log or `tlparse` output to provide critical debugging information to help us bisect the issue.
### devs
### Untopiced
### not user facing
### security
