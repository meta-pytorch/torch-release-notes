
# Release Notes worksheet cpp_frontend

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

## cpp_frontend
### bc breaking
### deprecation
### new features
- Add `torch::stable::sort` to the stable ABI, returning the sorted values and indices (with optional stable sorting) ([#198038](https://github.com/pytorch/pytorch/pull/198038))
- Make more `c10/util` helpers available header-only under `torch/headeronly/util` (`MathConstants.h`, `copysign.h`, `Load.h`, `BFloat16-math.h`, `irange.h`, `TypeCast.h` and `overflows.h`); the old `c10/util` headers keep working as forwarding includes ([#194673](https://github.com/pytorch/pytorch/pull/194673), [#194781](https://github.com/pytorch/pytorch/pull/194781))
### improvements
- Add a `gil_not_used` option to `torch.utils.cpp_extension.load_inline` so generated pybind11 modules can be imported on free-threaded Python without re-enabling the GIL ([#196802](https://github.com/pytorch/pytorch/pull/196802))
- Raise a compile-time `#error` when an extension sets `TORCH_TARGET_VERSION` newer than the libtorch headers it is compiled against ([#193962](https://github.com/pytorch/pytorch/pull/193962))
- Add a hint to the operator registration error for unsupported symbolic C++ kernel signatures (e.g. `const SymIntArrayRef&`), which previously looked like an `int[]` vs `SymInt[]` schema mismatch ([#197736](https://github.com/pytorch/pytorch/pull/197736))
### bug fixes
- Fix `torch::nn::Sequential::clone()` replacing submodule names with their indices, which changed `state_dict` keys of the clone ([#195107](https://github.com/pytorch/pytorch/pull/195107))
- Fix `torch::nn::functional::multi_head_attention_forward` crashing the process with an integer division by zero when `num_heads` is 0; it now raises an error ([#195381](https://github.com/pytorch/pytorch/pull/195381))
- Fix `std::numeric_limits<c10::BFloat16>::signaling_NaN()` returning infinity ([#195415](https://github.com/pytorch/pytorch/pull/195415))
- Fix the C++20 requirement check in `ATen/ATen.h` and `torch/all.h` never firing on MSVC and Windows nvcc, so building with an older standard now fails with a clear error ([#197417](https://github.com/pytorch/pytorch/pull/197417))
- Fix the fast symbolizer (`TORCH_SYMBOLIZE_MODE=fast`) producing no file/line information on aarch64 and for DWARF 2/3 and clang DWARF 5 debug info ([#195799](https://github.com/pytorch/pytorch/pull/195799))
- Fix downstream C++ projects failing to compile against libtorch headers (e.g. `'requires' only available with '-std=c++20'`) because the exported CMake `torch` target did not propagate the C++20 requirement; CUDA sources in downstream projects must still set `CMAKE_CUDA_STANDARD` themselves ([#190784](https://github.com/pytorch/pytorch/pull/190784))
- Fix a `no type named 'time_t' in namespace 'std'` compile error with clang when including `torch/csrc/stable/macros.h` ([#197021](https://github.com/pytorch/pytorch/pull/197021))
### performance
### docs
### devs
### Untopiced
### not user facing
- Rely on C++20 autogenerated `operator!=` ([#184795](https://github.com/pytorch/pytorch/pull/184795))
- Fix typos and grammar in code comments and docstrings ([#194419](https://github.com/pytorch/pytorch/pull/194419), [#194492](https://github.com/pytorch/pytorch/pull/194492), [#194567](https://github.com/pytorch/pytorch/pull/194567))
### security
