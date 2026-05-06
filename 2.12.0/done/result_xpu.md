
# Release Notes worksheet xpu

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

## xpu
### bc breaking
### deprecation
### new features
- Support `torch.accelerator.Graph` on XPU ([#176421](https://github.com/pytorch/pytorch/pull/176421))
- Added `memory_clock_rate` and `memory_bus_width` to XPU device properties ([#171967](https://github.com/pytorch/pytorch/pull/171967))
- Enable `split_group` API when TorchComms is used as a backend for TorchTitan on XPU ([#178236](https://github.com/pytorch/pytorch/pull/178236))

### improvements
- Support half precision FFT on XPU backend ([#171231](https://github.com/pytorch/pytorch/pull/171231))
- Support lazy Triton kernel compilation for cpp-wrapper on XPU (AOT Inductor) ([#179239](https://github.com/pytorch/pytorch/pull/179239))
- Add proper float64 handling for `addmv`, `addmm`, and `baddbmm` on XPU ([#174590](https://github.com/pytorch/pytorch/pull/174590))
- Enable FMA-based `addcdiv` lowering for XPU ([#176163](https://github.com/pytorch/pytorch/pull/176163))
- Enable `bmm_outer_product` Triton override for XPU ([#180816](https://github.com/pytorch/pytorch/pull/180816))
- Use version check for XPU fallback registration in Inductor ([#174679](https://github.com/pytorch/pytorch/pull/174679))
- Catch Intel Triton compilation/runtime errors as `IntelGPUError` in Inductor ([#169167](https://github.com/pytorch/pytorch/pull/169167))
- Improve Inductor UT coverage for XPU ([#174053](https://github.com/pytorch/pytorch/pull/174053), [#174054](https://github.com/pytorch/pytorch/pull/174054), [#174055](https://github.com/pytorch/pytorch/pull/174055), [#174056](https://github.com/pytorch/pytorch/pull/174056), [#174057](https://github.com/pytorch/pytorch/pull/174057), [#174058](https://github.com/pytorch/pytorch/pull/174058))
- Added Uint16/Uint32/Uint64/FP8 support to XPU device capability reporting ([#178467](https://github.com/pytorch/pytorch/pull/178467))

### bug fixes
- Fix `torch.compile` graph break inside `torch.autocast('xpu')` causing dtype mismatch ([#180309](https://github.com/pytorch/pytorch/pull/180309))
- Fix `conv2d` incorrect results and alignment errors for non-64-byte-aligned tensors on XPU ([#177956](https://github.com/pytorch/pytorch/pull/177956))
- Fix `nn.Embedding` module failures on XPU ([#178987](https://github.com/pytorch/pytorch/pull/178987))
- Fix XPU OneDNN symbol leak ([#172437](https://github.com/pytorch/pytorch/pull/172437))
- Fix meta kernel for `_scaled_dot_product_fused_attention_overrideable` to preserve query layout ([#178986](https://github.com/pytorch/pytorch/pull/178986))
- Fix tensorwise scaling settings on XPU ([#177810](https://github.com/pytorch/pytorch/pull/177810))
- Fix `DeviceOpOverrides` registered incorrectly on XPU ([#178959](https://github.com/pytorch/pytorch/pull/178959))
- Fix `SyclExtension` Windows build for oneAPI 2025.3+ breaking change ([#170701](https://github.com/pytorch/pytorch/pull/170701))

### performance
- Remove unnecessary device-to-host synchronization in `torch.nn.functional.one_hot` for XPU by skipping boundary validation checks only needed on CPU ([#179831](https://github.com/pytorch/pytorch/pull/179831))
- Add GEMM configs to XPU autotuning heuristic ([#177647](https://github.com/pytorch/pytorch/pull/177647))

### docs

### devs
- Enforce C++20 for XPU SYCL device compilation ([#179497](https://github.com/pytorch/pytorch/pull/179497), [#179613](https://github.com/pytorch/pytorch/pull/179613))

### not user facing
### security
