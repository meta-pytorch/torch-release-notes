
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

    Previously, `TORCH_WARN` / `TORCH_WARN_ONCE` warnings raised by operators (including custom C++ operators) invoked through `torch.ops.*` were printed straight to stderr, so `warnings.catch_warnings()` and `warnings.filterwarnings()` had no effect on them. These calls now go through the same handling as the rest of `torch`, so the warnings reach Python's `warnings` module (as `UserWarning`, or the matching warning class such as `DeprecationWarning`). This is a behavior change if you run with warnings turned into errors (`-W error` or `warnings.simplefilter("error")`): such a warning now raises an exception.

    C++ exceptions are also translated by PyTorch rather than pybind11. `c10` errors (`TORCH_CHECK` and friends) map to the same Python types as before, and `std::out_of_range` still becomes `IndexError` ([#195713](https://github.com/pytorch/pytorch/pull/195713)). However, any other standard or user-defined C++ exception raised by a custom operator becomes a `RuntimeError` with the same message. This includes exceptions pybind11 used to map to `ValueError`, `OverflowError` or `MemoryError`, and exceptions with a translator registered through `py::register_exception` or `py::register_exception_translator`. If you need a specific Python exception type from a custom operator, throw the matching `c10` error, for example `TORCH_CHECK_VALUE(...)` for `ValueError` or `TORCH_CHECK_TYPE(...)` for `TypeError`.

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
- Enable Sleef vectorized math in the NNC (TensorExpr) LLVM codegen on aarch64 ([#198002](https://github.com/pytorch/pytorch/pull/198002))
### bug fixes
- Fix `torch.jit.Attribute` annotations on `ScriptModule` being lost on Python 3.14 ([#195201](https://github.com/pytorch/pytorch/pull/195201))
- Fix constant pooling and CSE merging `0.0` with `-0.0` float constants (giving wrong results for ops like `copysign`, `reciprocal`, `atan2`) and failing to pool identical NaN constants ([#192605](https://github.com/pytorch/pytorch/pull/192605))
- Fix `torch.jit.export_opnames` missing operators used inside `torch.jit.fork` / `torch.jit.wait` subgraphs ([#197333](https://github.com/pytorch/pytorch/pull/197333))
- Fix `torch.jit.script` missing class-level attribute annotations on `nn.Module` subclasses on Python 3.14, where lazily evaluated annotations are not reliably visible through module instances, and resolve inherited annotations along the class MRO. This raises the minimum `typing-extensions` requirement to 4.13.0 ([#199074](https://github.com/pytorch/pytorch/pull/199074))
### performance
- Speed up `torch.jit.load` deserialization by skipping type-tag restoration for archives at version 3 or later, using a faster visited set when it is needed, and avoiding `IValue` copies in the unpickler ([#194035](https://github.com/pytorch/pytorch/pull/194035), [#193107](https://github.com/pytorch/pytorch/pull/193107), [#193250](https://github.com/pytorch/pytorch/pull/193250))
- Speed up TorchScript graph pre-optimization by sharing one alias analysis across peephole sub-passes ([#194009](https://github.com/pytorch/pytorch/pull/194009))
### docs
### devs
- `c10::List` iterators now satisfy the C++20 `std::random_access_iterator` concept and work with `std::ranges` algorithms, and `c10::List<T>::emplace` now constructs a `T` (so `List<double>().emplace(pos, 1)` stores a double instead of an int) ([#196002](https://github.com/pytorch/pytorch/pull/196002))
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
