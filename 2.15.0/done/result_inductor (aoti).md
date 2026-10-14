
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
- Add `num_runners` and `use_stream_affinity` keyword arguments to `torch._inductor.aoti_load_package` (also exposed through `AOTIModelPackageLoader` and the PT2 archive loader). With `use_stream_affinity=True`, each non-null CUDA or XPU stream keeps the same model instance across calls, and calls on the same stream run one after another. This is intended for controlled multi-stream benchmarking and can reduce host-side pipelining ([#194783](https://github.com/pytorch/pytorch/pull/194783))
- Add an optional lifecycle observer to the C++ `AOTIModelContainerRunner`. Attach a `torch::inductor::AOTIModelContainerObserver` subclass with `set_observer()` to get begin/end callbacks, including whether the call succeeded, around inference, constant swaps, buffer updates and constant folding for each container. These regions also appear in `torch.profiler` traces, and the overhead is a single null check when no observer is attached ([#193999](https://github.com/pytorch/pytorch/pull/193999))
### improvements
- Support `torch.compiler.nested_compile_region` (`invoke_subgraph`) in the AOTInductor C++ wrapper, and apply a region's own Inductor config options during code generation ([#194703](https://github.com/pytorch/pytorch/pull/194703), [#194704](https://github.com/pytorch/pytorch/pull/194704))
- Support host-side TMA `TensorDescriptor` arguments created inside `torch.library.triton_op` in AOTInductor C++ wrappers ([#193608](https://github.com/pytorch/pytorch/pull/193608))
- Honor Triton's per-kernel `launch_pdl` option (programmatic dependent launch) in AOTInductor CUDA kernel launches ([#194079](https://github.com/pytorch/pytorch/pull/194079))
- Catch C++ exceptions at the exported AOTInductor runtime entry points and return `AOTI_RUNTIME_FAILURE`, instead of letting them unwind across the C ABI ([#194613](https://github.com/pytorch/pytorch/pull/194613))
- Add `config.aot_inductor.check_upperbound` (default `True`) to control whether the runtime input checks enabled by `AOTI_RUNTIME_CHECK_INPUTS=1` reject dimensions above the upper bound inferred at compile time ([#196131](https://github.com/pytorch/pytorch/pull/196131))
- Add the `AOTI_TORCH_SAVE_DIR` environment variable to choose where the AOTInductor intermediate-value debug printer saves tensors, and fix those files being written next to the dump directory instead of inside it ([#195869](https://github.com/pytorch/pytorch/pull/195869))
- Add the `TORCHINDUCTOR_LITE_MODE=1` environment variable, which applies the same configuration as `torch.compile(mode="lite")` (all ops fall back to ATen) globally, including to AOTInductor compilation in subprocesses ([#195880](https://github.com/pytorch/pytorch/pull/195880))
- Make the error for a missing pytree registration actionable when loading an AOTInductor package that returns a custom type: it now explains that the defining module must be imported or the type registered with a matching `serialized_type_name` ([#186900](https://github.com/pytorch/pytorch/pull/186900))
- Extend kernel profiling in the AOTInductor C++ wrapper (`TORCHINDUCTOR_CPP_ENABLE_KERNEL_PROFILE=1`) to fallback, template and combo kernels and to proxy-executor and dispatcher fallbacks, and record input shapes for extern/ATen kernels ([#179699](https://github.com/pytorch/pytorch/pull/179699), [#198433](https://github.com/pytorch/pytorch/pull/198433), [#179700](https://github.com/pytorch/pytorch/pull/179700), [#191063](https://github.com/pytorch/pytorch/pull/191063))
- `torch._inductor.aoti_load_package` now documents that it accepts an extracted package directory, and loads a directory directly instead of first trying it as an archive, which logged misleading warnings ([#195115](https://github.com/pytorch/pytorch/pull/195115))
- Add `torch._inductor.config.unsafe_skip_scalar_range_asserts` (`TORCHINDUCTOR_UNSAFE_SKIP_SCALAR_RANGE_ASSERTS=1`) to skip generated range-bound asserts (inequalities against a constant such as `u0 >= 4`, including ones written with `torch._check`) while keeping equality asserts, for cases where the bounds inferred at compile time are too strict ([#192857](https://github.com/pytorch/pytorch/pull/192857))
- Reduce peak device memory while compiling with AOTInductor: optionally offload graph constants to disk during compile-time autotuning with `torch._inductor.config.aot_inductor.autotune_offload_constants_min_device_fraction` (default `1.0`, which never triggers; for example `0.10` enables it), and release cached allocator blocks once constants have been serialized ([#197462](https://github.com/pytorch/pytorch/pull/197462), [#197659](https://github.com/pytorch/pytorch/pull/197659))
### bug fixes
- Fix AOTInductor compilation and runtime failures when operators fall back to ATen through the proxy executor or C shim, as happens for every operator under `torch.compile(mode="lite")`: symbolic scalars in `Scalar` and `Tensor` arguments, `sym_stride`, defaulted keyword-only arguments, integer `alpha` on integral tensors, empty integer-list arguments, and missing `Optional[Device]`/list/tuple arguments ([#193767](https://github.com/pytorch/pytorch/pull/193767), [#199204](https://github.com/pytorch/pytorch/pull/199204), [#193768](https://github.com/pytorch/pytorch/pull/193768), [#194261](https://github.com/pytorch/pytorch/pull/194261), [#194262](https://github.com/pytorch/pytorch/pull/194262), [#194324](https://github.com/pytorch/pytorch/pull/194324), [#194700](https://github.com/pytorch/pytorch/pull/194700))
- Fix runtime constant folding (`aot_inductor.use_runtime_constant_folding`) dispatching the wrong kernel when the constant-folding graph calls an operator through the proxy executor ([#199295](https://github.com/pytorch/pytorch/pull/199295))
- Fix AOTInductor compilation of `cond`/`while_loop` models whose subgraphs hold tensor constants failing with `Can not find the original value for ..._constant0` ([#199188](https://github.com/pytorch/pytorch/pull/199188))
- Fix AOTInductor packages losing buffer mutations (for example, a counter buffer returning the same value on every call) because a mutated buffer was constant-folded ([#185077](https://github.com/pytorch/pytorch/pull/185077))
- Fix generated C++ wrappers failing to compile with `use of undeclared identifier 'int_array_N'` ([#193621](https://github.com/pytorch/pytorch/pull/193621)), with a duplicate stream variable when both the condition and body of a `while_loop` launch GPU kernels ([#196324](https://github.com/pytorch/pytorch/pull/196324)), and with symbolic numel redefinitions when kernel profiling is enabled ([#179698](https://github.com/pytorch/pytorch/pull/179698))
- Check the alignment of fallback-kernel outputs in C++ wrappers when `alignment_asserts` is enabled, matching the Python wrapper ([#184114](https://github.com/pytorch/pytorch/pull/184114))
- Fix memory leaks in the AOTInductor runtime: user-managed constant handles were never freed ([#194480](https://github.com/pytorch/pytorch/pull/194480)), and mmap-backed constants were not unmapped when a model loaded with `aoti_load_package` was destroyed ([#195090](https://github.com/pytorch/pytorch/pull/195090))
- Share one host-to-device stream per device for pinned constant staging instead of creating one per staging pool, fixing leaked hardware queues on ROCm ([#193249](https://github.com/pytorch/pytorch/pull/193249))
- Fix AOTInductor MPS artifacts failing to `dlopen` on other machines because of an unused OpenMP library dependency ([#198232](https://github.com/pytorch/pytorch/pull/198232))
- Fix AOTInductor-generated MPS wrappers segfaulting when Metal shader compilation or kernel lookup fails; the Metal compiler error is now raised ([#196634](https://github.com/pytorch/pytorch/pull/196634))
- Fix AOTInductor generating C++ that uses an undeclared unbacked symbol when a `torch.cond` predicate depends on it (for example `u0 > 0`) ([#186094](https://github.com/pytorch/pytorch/pull/186094))
- Fix AOTInductor C++ wrapper lowering failing for custom ops that return nested tensor lists with data-dependent sizes, such as `tuple[list[Tensor], list[Tensor]]` ([#194644](https://github.com/pytorch/pytorch/pull/194644))
- Fix AOTInductor packaging of models that return `torch.return_types` outputs (for example from `torch.max` or `torch.topk`) ([#197128](https://github.com/pytorch/pytorch/pull/197128))
### performance
- Parallelize pinned host staging copies when loading AOTInductor CUDA constants ([#195257](https://github.com/pytorch/pytorch/pull/195257))
- Avoid an extra device-to-device copy for each user-defined Triton kernel in `torch.compile(mode="lite")` by running the reinplacing pass before decomposing the functional Triton kernel wrapper ([#194325](https://github.com/pytorch/pytorch/pull/194325))
### docs
### devs
- Add `DeviceOpOverrides.aten_device_type()` so in-tree and out-of-tree backends provide their ATen device type for AOTInductor C++ wrapper code generation, replacing the mutable global `DEVICE_TO_ATEN` mapping ([#193904](https://github.com/pytorch/pytorch/pull/193904))
### Untopiced
### not user facing
- Compile internal AOTInductor CPU packages against both libstdc++ and a private libc++ ([#191241](https://github.com/pytorch/pytorch/pull/191241))
- Replace raw `throw`s in the AOTInductor runtime with checks ([#195148](https://github.com/pytorch/pytorch/pull/195148))
- Fix grammar and spelling in comments and docstrings ([#193965](https://github.com/pytorch/pytorch/pull/193965), [#194417](https://github.com/pytorch/pytorch/pull/194417), [#194254](https://github.com/pytorch/pytorch/pull/194254), [#194494](https://github.com/pytorch/pytorch/pull/194494))
- C++ code cleanups with no behavior change ([#194961](https://github.com/pytorch/pytorch/pull/194961), [#194876](https://github.com/pytorch/pytorch/pull/194876), [#195299](https://github.com/pytorch/pytorch/pull/195299), [#196355](https://github.com/pytorch/pytorch/pull/196355), [#199453](https://github.com/pytorch/pytorch/pull/199453), [#199467](https://github.com/pytorch/pytorch/pull/199467), [#199448](https://github.com/pytorch/pytorch/pull/199448))
- Tighten type annotations in Inductor code generation ([#196617](https://github.com/pytorch/pytorch/pull/196617))
### security
