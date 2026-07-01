
# Release Notes worksheet quantization

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

## quantization
### bc breaking
- The `onednn::qconv2d_pointwise.binary` and `.binary_tensor` operators no longer alias their input. Previously these ops mutated the `qaccum` input buffer and returned it directly, violating the PyTorch invariant that custom operator outputs must not alias inputs. This silently bypassed aliasing checks via the old `-> Tensor(a!)` schema and would become a hard error in PyTorch 2.12, so the schema and implementation were corrected to return a fresh output ([#177171](https://github.com/pytorch/pytorch/pull/177171))
### deprecation
- Creating tensors with the quantized dtypes `quint8`, `qint8`, and `qint32` is now deprecated and emits a `DeprecationWarning`. This covers both Python and C++ call sites; see [#184982](https://github.com/pytorch/pytorch/issues/184982) for migration guidance ([#184984](https://github.com/pytorch/pytorch/pull/184984))

  Version 2.12:
  ```python
  >>> x = torch.quantize_per_tensor(torch.randn(3), 0.1, 0, torch.quint8)
  ```

  Version 2.13:
  ```python
  >>> x = torch.quantize_per_tensor(torch.randn(3), 0.1, 0, torch.quint8)
  UserWarning: Creating tensors with quantized dtypes (quint8, qint8, qint32) is deprecated
  ```
### new features
### improvements
### bug fixes
- Fix a segmentation fault when running fp8 qlinear on x86 CPU without AMX, caused by the qlinear primitive cache ([#184317](https://github.com/pytorch/pytorch/pull/184317))
### performance
### docs
### devs
### not user facing
- Remove unused noqa directives in torch/, batch 5 and batch 3 ([#180139](https://github.com/pytorch/pytorch/pull/180139), [#180137](https://github.com/pytorch/pytorch/pull/180137))
- [split] Remove LEGACY template parameter from callers of fbgemm::Quantize ([#181067](https://github.com/pytorch/pytorch/pull/181067))
- Use const_data_ptr in quantization code ([#180970](https://github.com/pytorch/pytorch/pull/180970), [#182245](https://github.com/pytorch/pytorch/pull/182245), [#182267](https://github.com/pytorch/pytorch/pull/182267))
- [Build/BUCK] Fix torch_headers header deduplication for Windows MSVC ([#181495](https://github.com/pytorch/pytorch/pull/181495))
- Fix typos in comments, docstrings, error messages, and documentation ([#181991](https://github.com/pytorch/pytorch/pull/181991), [#182540](https://github.com/pytorch/pytorch/pull/182540), [#182761](https://github.com/pytorch/pytorch/pull/182761), [#185643](https://github.com/pytorch/pytorch/pull/185643))
- Remove unused noqa directives in non-torch/, batch 2 ([#180141](https://github.com/pytorch/pytorch/pull/180141))
- [CUDA][FP8][CPU][TEST] Properly saturate E4M3 on finite-overflow on CPU/C++ conversion code ([#178817](https://github.com/pytorch/pytorch/pull/178817))
- Enable RUF100 ([#180142](https://github.com/pytorch/pytorch/pull/180142))
- [test] Fix duplicated-word typos in test comments and docstrings ([#181132](https://github.com/pytorch/pytorch/pull/181132))
- Back out #180958 and #180679 ([#181163](https://github.com/pytorch/pytorch/pull/181163))
- [Docs] Check __all__ exports in coverage to catch decorated callables ([#178410](https://github.com/pytorch/pytorch/pull/178410))
- Fix duplicate word typos across the codebase ([#181268](https://github.com/pytorch/pytorch/pull/181268))
- [compile] fix diagonal_scatter backward ([#183720](https://github.com/pytorch/pytorch/pull/183720))
- Fix test_qrnncell unit-test failure ([#174125](https://github.com/pytorch/pytorch/pull/174125))
- Enable missing test in XPU backend when bug fixed ([#181822](https://github.com/pytorch/pytorch/pull/181822))
- [BE][Ez]: Add missing std::move in std::make_tuple calls ([#185254](https://github.com/pytorch/pytorch/pull/185254))
- [reland][Inductor][X86] Remove deprecated fusion patterns ([#178466](https://github.com/pytorch/pytorch/pull/178466))
- Disable XNNPACK by default in CMake ([#185297](https://github.com/pytorch/pytorch/pull/185297))
- [BE][Ez]: More semi-automated edits to move return values ([#186480](https://github.com/pytorch/pytorch/pull/186480))
- Remove unused noqa directives in torch/, batch 2 ([#180136](https://github.com/pytorch/pytorch/pull/180136))
### security
