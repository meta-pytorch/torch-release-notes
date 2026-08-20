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
- Add FP8 blockwise scaling support for MXFP8/MXFP4/NVFP4 recipes to `scaled_mm`/`_scaled_mm_v2` on XPU ([#181726](https://github.com/pytorch/pytorch/pull/181726), [#181727](https://github.com/pytorch/pytorch/pull/181727), [#187315](https://github.com/pytorch/pytorch/pull/187315))
- Add symmetric memory ops (async tensor parallelism) support for XPU ([#185102](https://github.com/pytorch/pytorch/pull/185102))
- Add XPU Graph native recording mode support ([#188874](https://github.com/pytorch/pytorch/pull/188874))
- Add WSL2 support for XPU ([#192398](https://github.com/pytorch/pytorch/pull/192398))
- Add `torch.xpu.list_gpu_processes` to query per-process GPU memory usage on XPU ([#185192](https://github.com/pytorch/pytorch/pull/185192))
- Add `torch.xpu._sleep` support for benchmarking and testing on XPU ([#189527](https://github.com/pytorch/pytorch/pull/189527))

### improvements
- Add device-wide synchronization support on XPU ([#191900](https://github.com/pytorch/pytorch/pull/191900))
- Add IPC memory handle sharing support to `XPUCachingAllocator` on XPU ([#188789](https://github.com/pytorch/pytorch/pull/188789))
- Support headdim 32 and 256 for XPU FlashAttention ([#180646](https://github.com/pytorch/pytorch/pull/180646))
- Support float16/bfloat16 inputs for FFT operators on XPU (and CUDA) via promotion to float32 ([#180766](https://github.com/pytorch/pytorch/pull/180766))
- Enable TF32 fpmath mode for XPU deconvolution, matching the existing convolution behavior ([#185606](https://github.com/pytorch/pytorch/pull/185606))
- Refactor Inductor autotune subprocess device-visibility for robustness on XPU ([#183436](https://github.com/pytorch/pytorch/pull/183436))
- Add Intel GPU device info to the Inductor device datasheet for autotuning/performance modeling ([#187308](https://github.com/pytorch/pytorch/pull/187308), [#189819](https://github.com/pytorch/pytorch/pull/189819))
- Add `MemPool` deferred block handling in `XPUCachingAllocator` to fix XPU graph capture correctness ([#187931](https://github.com/pytorch/pytorch/pull/187931))
- Refine `clock_rate` and `power_draw` device property queries via pyzes 0.1.2 ([#188248](https://github.com/pytorch/pytorch/pull/188248), [#188256](https://github.com/pytorch/pytorch/pull/188256))
- Introduce "Xe" terminology to XPU device properties ([#191477](https://github.com/pytorch/pytorch/pull/191477))
- Support BMG-G31 architecture compilation for the SYCL-TLA CUTLASS backend on XPU ([#187040](https://github.com/pytorch/pytorch/pull/187040))
- Enable the XPU scope profiler to gather hardware metrics via the kineto plugin ([#165766](https://github.com/pytorch/pytorch/pull/165766))
- Enable the `OVERHEAD` activity type for the XPU profiler backend ([#187835](https://github.com/pytorch/pytorch/pull/187835))
- Harden the XPU Inductor compile path with a dedicated `XPUCompileError` and cache-clearing fixes ([#183530](https://github.com/pytorch/pytorch/pull/183530))
- Make the `ALLOW_TF32` decision in Inductor device-aware for XPU, fixing eager/compiled divergence ([#187948](https://github.com/pytorch/pytorch/pull/187948))
- Enable SYCL native fast-math approximations for `exp`, `log`, `log1p`, and `tan` on XPU ([#176262](https://github.com/pytorch/pytorch/pull/176262))
- Migrate XPU ATen ops registrations into `native_functions.yaml` ([#181233](https://github.com/pytorch/pytorch/pull/181233))
- Allow all memory-type pointers known by the driver in the Inductor static launcher for XPU ([#188240](https://github.com/pytorch/pytorch/pull/188240))

### bug fixes
- Fix empty tensors in `addmv` on XPU ([#174193](https://github.com/pytorch/pytorch/pull/174193))
- Fix OneDNN SDPA with GQA and a broadcasted mask on XPU ([#190503](https://github.com/pytorch/pytorch/pull/190503))
- Fix LSTM oneDNN integration to support bf16 bias and cell state on XPU ([#187334](https://github.com/pytorch/pytorch/pull/187334))
- Fix `max_unpool2d` channels-last stride mismatch on XPU ([#190189](https://github.com/pytorch/pytorch/pull/190189))
- Fix `bmm_outer_product` Triton override to support XPU tensors ([#188783](https://github.com/pytorch/pytorch/pull/188783))
- Fix a SIGSEGV in AOTInductor's `run_const_fold` when the XPU stream is null ([#189517](https://github.com/pytorch/pytorch/pull/189517))
- Fix CUTLASS `cpp_wrapper` compilation on XPU to use the correct code cache ([#186791](https://github.com/pytorch/pytorch/pull/186791))
- Fix a missing header include causing AOTI XPU compile failures ([#187137](https://github.com/pytorch/pytorch/pull/187137))
- Fix Inductor codegen for `current_device_idx_expr` on XPU ([#193083](https://github.com/pytorch/pytorch/pull/193083))
- Route `GPU_USER_ANNOTATION` kineto profiler events to `DeviceType::XPU` ([#191841](https://github.com/pytorch/pytorch/pull/191841))
- Fix `max_pool2d_backward` to correctly fall back to eager execution on XPU instead of a slower fused Triton kernel ([#187940](https://github.com/pytorch/pytorch/pull/187940))
- Fix the Inductor combo-kernel no-bench carve-out gate for XPU so eligible kernels fuse instead of being split out ([#187147](https://github.com/pytorch/pytorch/pull/187147))

### performance
- Fuse Half->Float upcast into softmax and reduction kernels on XPU ([#189999](https://github.com/pytorch/pytorch/pull/189999))
- Auto-enable the `batch_linear_lhs` fusion for XPU Inductor inference ([#181854](https://github.com/pytorch/pytorch/pull/181854))

### docs
- Update the XPU newly supported OS versions and simplified installation instructions ([#187923](https://github.com/pytorch/pytorch/pull/187923), [#190992](https://github.com/pytorch/pytorch/pull/190992))

### devs
- Upgrade the XPU support package (oneAPI Deep Learning Essentials) to 2026.1 ([#189593](https://github.com/pytorch/pytorch/pull/189593))
- Upgrade the bundled oneDNN submodule to v3.12.3, enabling SYCL Graph record/replay support on Intel GPUs ([#188785](https://github.com/pytorch/pytorch/pull/188785))
- Enable Triton XPU Windows wheel builds for Python 3.15 & 3.15t ([#186033](https://github.com/pytorch/pytorch/pull/186033))

### not user facing
### security
