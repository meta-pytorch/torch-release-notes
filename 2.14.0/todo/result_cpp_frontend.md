
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
- Adding conversion from PyObject to torch::stable::tensor ([#183323](https://github.com/pytorch/pytorch/pull/183323))
### improvements
- [BE] Do not include <windows.h> directly ([#187673](https://github.com/pytorch/pytorch/pull/187673))
- Simplify waiting using std::latch + fix iOS PACKAGE modifier (#188279) ([#188281](https://github.com/pytorch/pytorch/pull/188281))
- [c++20] Simplify waiting using std::latch in ParallelNative.cpp (#188981) ([#188981](https://github.com/pytorch/pytorch/pull/188981))
- revert the std::latch changes in ParallelNative (D109888039 + D110655102) (#189204) ([#189204](https://github.com/pytorch/pytorch/pull/189204))
- c10 macros: add C10_LIFETIMEBOUND ([#189912](https://github.com/pytorch/pytorch/pull/189912))
- Add stable::Tensor has_storage ([#189877](https://github.com/pytorch/pytorch/pull/189877))
- c10/util/intrusive_ptr.h: add [[nodiscard]] to query methods (#186519) ([#186519](https://github.com/pytorch/pytorch/pull/186519))
- Let deprecated-declarations warn (not error) in c10/ATen/torch builds ([#189948](https://github.com/pytorch/pytorch/pull/189948))
- c10 TensorAccessor: add C10_LIFETIMEBOUND to borrowed sizes_/strides_ ([#190075](https://github.com/pytorch/pytorch/pull/190075))
- aten TensorRef/OptionalTensorRef: add C10_LIFETIMEBOUND ([#190074](https://github.com/pytorch/pytorch/pull/190074))
- Simplify c10 TypeSafeSignMath tag-dispatch with if constexpr ([#190081](https://github.com/pytorch/pytorch/pull/190081))
- c10 MaybeOwned: add C10_LIFETIMEBOUND to borrow entry points ([#190077](https://github.com/pytorch/pytorch/pull/190077))
- torch/headeronly/core/TensorAccessor.h: replace typedef with using ([#185956](https://github.com/pytorch/pytorch/pull/185956))
- [12/12] Enforce C++20 minimum in header guards (#178150) ([#178150](https://github.com/pytorch/pytorch/pull/178150))
- StorageMethods: reject negative requested storage size (don't wrap to size_t) ([#190652](https://github.com/pytorch/pytorch/pull/190652))
- c10/util/intrusive_ptr.h: replace hand-written comparison operators with operator<=> ([#186634](https://github.com/pytorch/pytorch/pull/186634))
- c10 HeaderOnlyArrayRef: add C10_LIFETIMEBOUND to borrowing constructors (#190078) ([#190078](https://github.com/pytorch/pytorch/pull/190078))
- Add c10::safe_conv (strict, integer-only) and c10::unsafe_wrapping_convert (#190092) ([#190092](https://github.com/pytorch/pytorch/pull/190092))
### bug fixes
- Drop `noexcept` from  `TensorMaker::computeStorageSize`  ([#188062](https://github.com/pytorch/pytorch/pull/188062))
- Fix uninitialized return in Chebyshev polynomial helpers for NaN inputs ([#187767](https://github.com/pytorch/pytorch/pull/187767))
- Add Scalar(long long) constructor guard for NetBSD and other LP64 BSDs ([#188941](https://github.com/pytorch/pytorch/pull/188941))
### performance
### docs
### devs
### Untopiced
- c10/util/ArrayRef.h: specialize std::ranges::enable_borrowed_range ([#186635](https://github.com/pytorch/pytorch/pull/186635))
- [cpp_extension] Replace FileBaton with filelock to fix stale-lock deadlock ([#190543](https://github.com/pytorch/pytorch/pull/190543))
- Fix "a/an" article typos in code comments ([#190600](https://github.com/pytorch/pytorch/pull/190600))
- [Stable C shim] Fix memory leak in StableIValue -> std::string conversion ([#190493](https://github.com/pytorch/pytorch/pull/190493))
- c10/util/overflows.h: fix float->int range check at wide-integer boundary ([#190651](https://github.com/pytorch/pytorch/pull/190651))
- Add stable Tensor overloads for bitwise_and/or/left_shift/right_shift (2.14+) ([#191973](https://github.com/pytorch/pytorch/pull/191973))
- Add stable permute and view_dtype (2.14+) ([#192083](https://github.com/pytorch/pytorch/pull/192083))
- Add stable Tensor overloads for index_select, floor_divide, and is_pinned (2.14+)  ([#192097](https://github.com/pytorch/pytorch/pull/192097))
- Migrate c10/util/complex_utils.h to headeronly ([#192552](https://github.com/pytorch/pytorch/pull/192552))
- Migrate ATen/NumericUtils.h isinf and isnan to headeronly ([#192557](https://github.com/pytorch/pytorch/pull/192557))
- Migrate fastAtomicAdd to headeronly ([#192844](https://github.com/pytorch/pytorch/pull/192844))
### not user facing
- Validate num_heads before division in MultiheadAttention ([#186376](https://github.com/pytorch/pytorch/pull/186376))
- c10 intrusive_ptr: add [[nodiscard]] to weak_intrusive_ptr comparison operators ([#189930](https://github.com/pytorch/pytorch/pull/189930))
- c10 Bitset: add [[nodiscard]] to query methods ([#189935](https://github.com/pytorch/pytorch/pull/189935))
- c10 IntrusiveList: add [[nodiscard]] to observer methods ([#189936](https://github.com/pytorch/pytorch/pull/189936))
- c10 intrusive_ptr: add [[nodiscard]] to raw::weak_intrusive_ptr helpers ([#189934](https://github.com/pytorch/pytorch/pull/189934))
- c10 Array: add [[nodiscard]] to array_of ([#189933](https://github.com/pytorch/pytorch/pull/189933))
- c10 ArrayRef: add [[nodiscard]] to observers and makeArrayRef factories ([#189931](https://github.com/pytorch/pytorch/pull/189931))
- c10 intrusive_ptr: add [[nodiscard]] to intrusive_ptr comparison operators ([#189929](https://github.com/pytorch/pytorch/pull/189929))
- c10 UniqueVoidPtr: add [[nodiscard]] to query and ownership methods ([#189932](https://github.com/pytorch/pytorch/pull/189932))
- c10 SmallVector: add [[nodiscard]] to observers, comparisons and factories ([#189924](https://github.com/pytorch/pytorch/pull/189924))
- c10 intrusive_ptr: add [[nodiscard]] to make_intrusive ([#189923](https://github.com/pytorch/pytorch/pull/189923))
- c10 OptionalArrayRef: add [[nodiscard]] to observer methods ([#189919](https://github.com/pytorch/pytorch/pull/189919))
- c10 ExclusivelyOwned: add [[nodiscard]] to query and ownership methods ([#189922](https://github.com/pytorch/pytorch/pull/189922))
- c10 string_view: add [[nodiscard]] to query methods ([#189921](https://github.com/pytorch/pytorch/pull/189921))
- c10 intrusive_ptr: add [[nodiscard]] to raw::intrusive_ptr helpers ([#189918](https://github.com/pytorch/pytorch/pull/189918))
- c10 SmallBuffer: add [[nodiscard]] to observer methods ([#189916](https://github.com/pytorch/pytorch/pull/189916))
- c10/core/impl/SizesAndStrides.h: add [[nodiscard]] to size() and isInline() ([#186636](https://github.com/pytorch/pytorch/pull/186636))
- c10 StringUtil: add [[nodiscard]] to value-returning helpers (#189928) ([#189928](https://github.com/pytorch/pytorch/pull/189928))
### security
