
# Release Notes worksheet inductor (aoti)

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

## inductor (aoti)
### bc breaking
### deprecation
### new features
- Add `AOTInductorModelContainerCreateWithExternalConstants`, allowing callers to construct an AOTInductor model container from caller-owned weight tensors for zero-copy sharing such as CUDA IPC ([#188643](https://github.com/pytorch/pytorch/pull/188643))

  The new C API skips loading constants from the package and leaves ownership with the caller. Existing model-container creation and constant-loading paths are unchanged unless external constants are explicitly provided.
- Support explicit user-defined streams in the AOTInductor C++ wrapper. A compiled region that selects a stream with `torch.cuda.stream(...)` now emits stream-guard code so its kernels run on the requested stream, instead of always running on the default stream ([#182971](https://github.com/pytorch/pytorch/pull/182971))
### improvements
- Support `int[]`, `SymInt[]`, and optional integer-list arguments in AOTI eager cache keys, enabling cached compilation for operators such as `new_zeros`, `mean.dim`, and `count_nonzero.dim_IntList` ([#187360](https://github.com/pytorch/pytorch/pull/187360))
- Support lazy autotuning when compiling with the AOTInductor dual-wrapper, so Triton autotuning is deferred to a first JIT pass rather than being done during ahead-of-time compilation ([#184735](https://github.com/pytorch/pytorch/pull/184735))
- Support `torch.cond` and `torch.while_loop` when compiling with the AOTInductor dual-wrapper ([#184736](https://github.com/pytorch/pytorch/pull/184736))
- Add an `AOTI_LOG_LOADING` environment variable. When it is set, AOTInductor prints timing and diagnostic messages for each stage of constant loading, prefixed with `[AOTI_LOAD]`, without requiring a rebuild ([#186309](https://github.com/pytorch/pytorch/pull/186309))
- Check the error codes returned by the generated `scatter`, `index_put`, `clone`, and tensor-handle shim calls, so a failure inside one of these fallbacks raises an error instead of being silently ignored ([#190909](https://github.com/pytorch/pytorch/pull/190909), [#190910](https://github.com/pytorch/pytorch/pull/190910))
### bug fixes
- Fix C++ wrapper fallback operators with `Any` arguments, including distributed operators such as `all_gather_into_tensor`, failing to compile or dispatch ([#188124](https://github.com/pytorch/pytorch/pull/188124))
- Route custom operators with `SymInt`, `SymBool`, or `SymFloat` arguments through boxed C++ wrapper dispatch, avoiding runtime `API call failed` errors ([#188154](https://github.com/pytorch/pytorch/pull/188154))
- Box `None` passed to non-optional tensor arguments as an undefined tensor in C++ wrappers, matching eager custom-operator behavior ([#188485](https://github.com/pytorch/pytorch/pull/188485))
- Fix C++ wrappers dereferencing a null tensor handle when a Python fallback operator returns a one-element `Tensor[]` ([#190551](https://github.com/pytorch/pytorch/pull/190551))
- Emit portable `std::array::data()` pointers in generated CPU wrappers instead of relying on iterator-to-pointer conversion ([#191240](https://github.com/pytorch/pytorch/pull/191240))
- Package AOTInductor CUDA multi-architecture kernels for the requested deployment architecture instead of the physical compilation GPU ([#185328](https://github.com/pytorch/pytorch/pull/185328))
- Fix AOTInductor C++ wrappers recovering integer symbols from composed dynamic sizes through floating-point division, which could truncate valid runtime dimensions ([#185841](https://github.com/pytorch/pytorch/pull/185841))
- Fail fast with a clear error when loading a CUDA AOTInductor package in a process without CUDA or ROCm available ([#186943](https://github.com/pytorch/pytorch/pull/186943))
- Fix C++ wrapper fallback output indexing for mutable custom operators and remove invalid 16-byte alignment assumptions for misaligned tensor views ([#187331](https://github.com/pytorch/pytorch/pull/187331))
- Preserve C++ wrapper input slots when graphs contain Python-only custom-class inputs ([#188030](https://github.com/pytorch/pytorch/pull/188030))
- Pass the device the model was actually loaded on to custom operator fallbacks, instead of the device recorded when the model was compiled. Previously a model compiled for one GPU and then loaded on another would hand the wrong device to its custom ops ([#184741](https://github.com/pytorch/pytorch/pull/184741))
- Synchronize the default stream after copying model constants on AMD GPUs, fixing a race in which inference could read constants before the copy had completed ([#186963](https://github.com/pytorch/pytorch/pull/186963))
- Fix a 32-bit integer overflow when computing the SYCL global launch range in the AOTInductor runtime, which produced incorrect launch dimensions for large grids on XPU ([#187307](https://github.com/pytorch/pytorch/pull/187307))
- Fix a GPU memory leak where input tensor handles were not released when an input runtime check failed inside `run_impl` ([#189503](https://github.com/pytorch/pytorch/pull/189503))
- Free constants that have not yet been transferred when `run_const_fold` throws, fixing a memory leak on the constant-folding error path ([#189505](https://github.com/pytorch/pytorch/pull/189505))
- Fix a segmentation fault in `run_const_fold` on XPU when the stream argument is null ([#189517](https://github.com/pytorch/pytorch/pull/189517))
- Make the C++ wrapper's debug synchronization device-aware, fixing a regression on ROCm ([#190071](https://github.com/pytorch/pytorch/pull/190071))
- Fix a missing CUDA header in the generated constant graph when compiling with the dual-wrapper, which made the generated code fail to compile ([#191050](https://github.com/pytorch/pytorch/pull/191050))
- Skip CUDA stream event code generation in the AOTInductor C++ wrapper on XPU, where those APIs do not apply ([#190637](https://github.com/pytorch/pytorch/pull/190637))
### performance
- Add an opt-in pinned, asynchronous host-to-device path for AOTInductor constant loading through `AOTI_COPY_USE_PINNED_ASYNC=1`, avoiding the device-wide synchronization caused by pageable-memory copies ([#186258](https://github.com/pytorch/pytorch/pull/186258))
### docs
### devs
- Add `TORCHINDUCTOR_CPP_ENABLE_KERNEL_CONTEXT_GUARD` to opt into kernel-context metadata when profiling generated C++ wrappers ([#184513](https://github.com/pytorch/pytorch/pull/184513))
### not user facing
- Correct spelling and grammar in internal Inductor and distributed comments and log strings without changing behavior ([#190039](https://github.com/pytorch/pytorch/pull/190039))
- Move `win32-headers.h` from `c10/util` to `torch/headeronly` and update the AOTInductor use of it; the old header now forwards to the new location ([#186962](https://github.com/pytorch/pytorch/pull/186962))
- Refactor and refine `sycl_runtime_wrappers.h` and `xpu.cpp` ([#190143](https://github.com/pytorch/pytorch/pull/190143))
- Include the manually written AOTInductor shims in the shim linter ([#191266](https://github.com/pytorch/pytorch/pull/191266))
- Remove obsolete Python wrapper symbol extraction ([#184460](https://github.com/pytorch/pytorch/pull/184460))
- Drop a no-op hipify wrapper on the CUDA debug-sync path ([#190472](https://github.com/pytorch/pytorch/pull/190472))
### security
