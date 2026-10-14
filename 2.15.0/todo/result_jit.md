
# Release Notes worksheet jit

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

## jit
### bc breaking
- Operators called through `torch.ops.*` and `torch._C._dispatch_call_boxed` now use PyTorch's own warning and exception translation instead of pybind11's ([#193451](https://github.com/pytorch/pytorch/pull/193451))

    We make `torch.ops.*` calls go through the same exception and warning translation as the rest of the library. This means that some exception translation that used to be handled by pybind is now handled natively. User-defined pybind exception translation is thus lost. Restoring it may be done in a future release as part of a broader exception handler improvement.

    In addition, `TORCH_WARN` warnings from these operators now reach Python's `warnings` module, so they raise when warnings are turned into errors (`-W error`). `std::out_of_range` still becomes `IndexError` ([#195713](https://github.com/pytorch/pytorch/pull/195713)).

    Version 2.14:

    ```python
    # C++ op: throw std::invalid_argument("bad size");
    try:
        torch.ops.my_lib.my_op(x)
    except ValueError:  # pybind11 translation
        ...
    ```

    Version 2.15:

    ```python
    # C++ op: TORCH_CHECK_VALUE(false, "bad size");
    try:
        torch.ops.my_lib.my_op(x)
    except ValueError:
        ...

    # TORCH_WARN from the op is now a Python warning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        torch.ops.my_lib.my_op(x)
    ```

### deprecation
### new features
### improvements
- Use Sleef in NNC on aarch64 ([#198002](https://github.com/pytorch/pytorch/pull/198002))
### bug fixes
- Fix `torch.jit.Attribute` and `nn.Module` class annotations being lost on Python 3.14; this requires `typing-extensions>=4.13` ([#195201](https://github.com/pytorch/pytorch/pull/195201), [#199074](https://github.com/pytorch/pytorch/pull/199074))
- Fix constant pooling merging `0.0` with `-0.0` ([#192605](https://github.com/pytorch/pytorch/pull/192605))
- Fix `torch.jit.export_opnames` missing ops inside `torch.jit.fork` subgraphs ([#197333](https://github.com/pytorch/pytorch/pull/197333))
### performance
- Speed up `torch.jit.load` and graph pre-optimization ([#194035](https://github.com/pytorch/pytorch/pull/194035), [#193107](https://github.com/pytorch/pytorch/pull/193107), [#193250](https://github.com/pytorch/pytorch/pull/193250), [#194009](https://github.com/pytorch/pytorch/pull/194009))
### docs
### devs
- `c10::List` iterators satisfy `std::random_access_iterator`, and `List<T>::emplace` now constructs a `T` ([#196002](https://github.com/pytorch/pytorch/pull/196002))
### Untopiced
### not user facing
- Add META's Math Library (#198207) ([#198207](https://github.com/pytorch/pytorch/pull/198207))
- Fix grammar and typos in code comments and docstrings ([#194491](https://github.com/pytorch/pytorch/pull/194491))
- Fix grammar in comments and docstrings ([#194624](https://github.com/pytorch/pytorch/pull/194624))
- [RAWTHROW][10] torch/csrc/jit: 744 findings down to four subdirectories ([#195764](https://github.com/pytorch/pytorch/pull/195764))
- [RAWTHROW][12] torch/csrc/jit/python: 49 conversions, tensorexpr is all that is left ([#195859](https://github.com/pytorch/pytorch/pull/195859))
- [caffe2][buck] Hoist XNNPACK dep out of aten_cpu into :aten_native_xnnpack (#197457) ([#197457](https://github.com/pytorch/pytorch/pull/197457))
- Use c10::bit_cast for type punning instead of memcpy ([#194149](https://github.com/pytorch/pytorch/pull/194149))
- Replace std::bind with std::bind_front where possible ([#195598](https://github.com/pytorch/pytorch/pull/195598))
- [RAWTHROW][15] torch/csrc/jit/tensorexpr: 294 conversions, the burn-down list is empty ([#198500](https://github.com/pytorch/pytorch/pull/198500))
### security
