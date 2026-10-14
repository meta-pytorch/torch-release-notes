
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
- Add `num_runners` and `use_stream_affinity` arguments to `torch._inductor.aoti_load_package`, which keep each non-null CUDA or XPU stream on the same model instance across calls ([#194783](https://github.com/pytorch/pytorch/pull/194783))
- Add an optional lifecycle observer to the C++ `AOTIModelContainerRunner`: attach a `torch::inductor::AOTIModelContainerObserver` with `set_observer()` to get begin/end callbacks around inference, constant swaps and constant folding ([#193999](https://github.com/pytorch/pytorch/pull/193999))
### improvements
- Support `torch.compiler.nested_compile_region` in the AOTInductor C++ wrapper ([#194703](https://github.com/pytorch/pytorch/pull/194703), [#194704](https://github.com/pytorch/pytorch/pull/194704))
- Support host-side TMA `TensorDescriptor` arguments in `torch.library.triton_op` ([#193608](https://github.com/pytorch/pytorch/pull/193608)) and Triton's `launch_pdl` option ([#194079](https://github.com/pytorch/pytorch/pull/194079)) in AOTInductor C++ wrappers
- Return `AOTI_RUNTIME_FAILURE` from AOTInductor runtime entry points instead of letting C++ exceptions unwind across the C ABI ([#194613](https://github.com/pytorch/pytorch/pull/194613))
- Add `config.aot_inductor.check_upperbound` to control whether `AOTI_RUNTIME_CHECK_INPUTS=1` rejects dimensions above the compile-time upper bound ([#196131](https://github.com/pytorch/pytorch/pull/196131))
- Add `TORCHINDUCTOR_LITE_MODE=1` to apply `torch.compile(mode="lite")` globally, including to AOTInductor compilation ([#195880](https://github.com/pytorch/pytorch/pull/195880))
- Add `torch._inductor.config.unsafe_skip_scalar_range_asserts` to skip generated range asserts when compile-time bounds are too strict ([#192857](https://github.com/pytorch/pytorch/pull/192857))
- Reduce peak device memory during AOTInductor compilation ([#197462](https://github.com/pytorch/pytorch/pull/197462), [#197659](https://github.com/pytorch/pytorch/pull/197659))
- Extend AOTInductor C++ wrapper kernel profiling to fallback, template and combo kernels ([#179699](https://github.com/pytorch/pytorch/pull/179699), [#198433](https://github.com/pytorch/pytorch/pull/198433), [#179700](https://github.com/pytorch/pytorch/pull/179700), [#191063](https://github.com/pytorch/pytorch/pull/191063))
- `torch._inductor.aoti_load_package` now loads an extracted package directory directly ([#195115](https://github.com/pytorch/pytorch/pull/195115))
- Explain how to fix a missing pytree registration when loading a package that returns a custom type ([#186900](https://github.com/pytorch/pytorch/pull/186900))
- Add `AOTI_TORCH_SAVE_DIR` to choose where the AOTInductor debug printer saves tensors ([#195869](https://github.com/pytorch/pytorch/pull/195869))
### bug fixes
- Fix AOTInductor failures when operators fall back to ATen through the proxy executor or C shim, as under `torch.compile(mode="lite")` ([#193767](https://github.com/pytorch/pytorch/pull/193767), [#199204](https://github.com/pytorch/pytorch/pull/199204), [#193768](https://github.com/pytorch/pytorch/pull/193768), [#194261](https://github.com/pytorch/pytorch/pull/194261), [#194262](https://github.com/pytorch/pytorch/pull/194262), [#194324](https://github.com/pytorch/pytorch/pull/194324), [#194700](https://github.com/pytorch/pytorch/pull/194700))
- Fix AOTInductor C++ wrapper compile failures: undeclared `int_array_N` ([#193621](https://github.com/pytorch/pytorch/pull/193621)), duplicate stream variables in `while_loop` ([#196324](https://github.com/pytorch/pytorch/pull/196324)), kernel profiling ([#179698](https://github.com/pytorch/pytorch/pull/179698)), unbacked symbols in `torch.cond` predicates ([#186094](https://github.com/pytorch/pytorch/pull/186094)), and custom ops returning nested tensor lists ([#194644](https://github.com/pytorch/pytorch/pull/194644))
- Fix AOTInductor packages losing buffer mutations to constant folding ([#185077](https://github.com/pytorch/pytorch/pull/185077))
- Fix `cond`/`while_loop` models with subgraph tensor constants failing with `Can not find the original value for ..._constant0` ([#199188](https://github.com/pytorch/pytorch/pull/199188))
- Fix runtime constant folding dispatching the wrong kernel through the proxy executor ([#199295](https://github.com/pytorch/pytorch/pull/199295))
- Fix AOTInductor runtime leaks of constant handles and mmap-backed constants ([#194480](https://github.com/pytorch/pytorch/pull/194480), [#195090](https://github.com/pytorch/pytorch/pull/195090)) and of hardware queues on ROCm ([#193249](https://github.com/pytorch/pytorch/pull/193249))
- Fix AOTInductor MPS artifacts failing to `dlopen` on other machines ([#198232](https://github.com/pytorch/pytorch/pull/198232)) and segfaulting on Metal compile errors ([#196634](https://github.com/pytorch/pytorch/pull/196634))
- Fix packaging of models that return `torch.return_types` outputs, e.g. from `torch.max` ([#197128](https://github.com/pytorch/pytorch/pull/197128))
### performance
- Parallelize pinned host staging copies when loading CUDA constants ([#195257](https://github.com/pytorch/pytorch/pull/195257))
### docs
### devs
- Add `DeviceOpOverrides.aten_device_type()` so backends provide their ATen device type to AOTInductor C++ codegen ([#193904](https://github.com/pytorch/pytorch/pull/193904))
### Untopiced
### not user facing
- Compile internal AOTInductor CPU packages against both libstdc++ and a private libc++ ([#191241](https://github.com/pytorch/pytorch/pull/191241))
- Replace raw `throw`s in the AOTInductor runtime with checks ([#195148](https://github.com/pytorch/pytorch/pull/195148))
- Fix grammar and spelling in comments and docstrings ([#193965](https://github.com/pytorch/pytorch/pull/193965), [#194417](https://github.com/pytorch/pytorch/pull/194417), [#194254](https://github.com/pytorch/pytorch/pull/194254), [#194494](https://github.com/pytorch/pytorch/pull/194494))
- C++ code cleanups with no behavior change ([#194961](https://github.com/pytorch/pytorch/pull/194961), [#194876](https://github.com/pytorch/pytorch/pull/194876), [#195299](https://github.com/pytorch/pytorch/pull/195299), [#196355](https://github.com/pytorch/pytorch/pull/196355), [#199453](https://github.com/pytorch/pytorch/pull/199453), [#199467](https://github.com/pytorch/pytorch/pull/199467), [#199448](https://github.com/pytorch/pytorch/pull/199448))
- Tighten type annotations in Inductor code generation ([#196617](https://github.com/pytorch/pytorch/pull/196617))
- Check the alignment of fallback-kernel outputs in C++ wrappers when `alignment_asserts` is enabled, matching the Python wrapper ([#184114](https://github.com/pytorch/pytorch/pull/184114)) (cut for length)
- Avoid an extra device-to-device copy for each user-defined Triton kernel in `torch.compile(mode="lite")` ([#194325](https://github.com/pytorch/pytorch/pull/194325)) (cut for length)
### security
