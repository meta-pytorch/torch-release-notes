
# Release Notes worksheet rocm

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

## rocm
### bc breaking
### deprecation
### new features
### improvements
- Enable Composable Kernel (CK) SDPA flash attention on RDNA4 (gfx1200/gfx1201) ([#188114](https://github.com/pytorch/pytorch/pull/188114))
- Update AOTriton to 0.14.2b, adding FlyDSL SDPA kernels for gfx950 and gfx1201, ROCm 10 packages, and several attention correctness fixes ([#197747](https://github.com/pytorch/pytorch/pull/197747))
- Add a gfx950 pre-swizzled MX FP4/FP8 block-scale layout for `scaled_mm`, exposed as `torch.nn.functional.SwizzleType.SWIZZLE_32_8` (requires ROCm 7.13 for MX FP4 and ROCm 7.14 for MX FP8) ([#190290](https://github.com/pytorch/pytorch/pull/190290))
- Allow all four operand layouts in `torch._scaled_mm` with FP8 tensorwise scaling on ROCm, instead of requiring TN ([#196884](https://github.com/pytorch/pytorch/pull/196884))
- Add gfx1250 Tensor Data Mover (TDM) support to Inductor for dense `mm`/`addmm`, generic pointwise/reduction tensor-descriptor codegen, and FlexAttention forward and decode ([#191166](https://github.com/pytorch/pytorch/pull/191166), [#196525](https://github.com/pytorch/pytorch/pull/196525), [#197329](https://github.com/pytorch/pytorch/pull/197329))
- hipBLAS and hipBLASLt workspaces are now allocated per operation from the caching allocator by default, matching CUDA, so graphs captured on the same stream no longer share a workspace. Set `TORCH_CUBLAS_WORKSPACE_CACHE=1` to keep the previous persistent workspace cache ([#196920](https://github.com/pytorch/pytorch/pull/196920))
- Check AOTriton attention return codes at the call site, so launch failures are reported by the attention op that caused them rather than by a later, unrelated HIP call ([#194100](https://github.com/pytorch/pytorch/pull/194100))
- Fall back to the native RNN implementation when MIOpen RNN fails at runtime on a device ([#189658](https://github.com/pytorch/pytorch/pull/189658))
- Disable Inductor's Origami GEMM heuristics on ROCm 10.0 and later, where the Origami Python package is not yet API-compatible ([#193843](https://github.com/pytorch/pytorch/pull/193843))
- Add MI355X to Inductor's device info table so `get_device_tflops` and related estimates use correct peak values ([#196365](https://github.com/pytorch/pytorch/pull/196365))
- Report the ROCm SDK version and the HIP runtime version separately in `collect_env` and extension build cache keys ([#193602](https://github.com/pytorch/pytorch/pull/193602))
- Expose the `hsa_queue` field in profiler `EventMetadata` for kernel and copy events on ROCm ([#196487](https://github.com/pytorch/pytorch/pull/196487))
- Add dynamic-shape support to TunableOp GEMM tuning: inside the new `torch.cuda.tunable.dynamic_dims_mask(M=..., N=..., K=..., BATCH=...)` context, tuned results for `mm`, `addmm`, `bmm`, `baddbmm` and `_scaled_mm` are also saved under wildcard entries for the dynamic dimensions. With `torch.cuda.tunable.wildcard_fallback_enable()` (or `PYTORCH_TUNABLEOP_WILDCARD_FALLBACK=1`), a shape that misses the tuned table reuses a matching wildcard entry. Inductor can produce these entries during autotuning when `torch._inductor.config.cuda.autotune_tunableop_dynamic_dims_wildcard = True`. Both options are off by default ([#191658](https://github.com/pytorch/pytorch/pull/191658))
### bug fixes
- Fix CK flash attention dropout returning a wrong seed/offset to autograd when the GPU is busy, by building the seed tensors from host values ([#197563](https://github.com/pytorch/pytorch/pull/197563))
- Fix `pdist` and `cdist` failing to launch with more than 2^24 outputs ([#188006](https://github.com/pytorch/pytorch/pull/188006))
- Fix the native BMM outer-product kernel failing to launch past HIP's work-item limit; such cases now fall back to ATen ([#194131](https://github.com/pytorch/pytorch/pull/194131))
- Fix FP8 GEMMs failing with `HIPBLAS_STATUS_INTERNAL_ERROR` on ROCm 7.14 by raising the default hipBLASLt workspace to 80 MiB ([#197201](https://github.com/pytorch/pytorch/pull/197201))
- Fix `F.batch_norm` on sharded DTensor inputs failing on ROCm with "Operator aten.miopen_batch_norm.default does not have a sharding strategy registered" ([#197160](https://github.com/pytorch/pytorch/pull/197160))
- Fix `~CUDAGraph` leaving the calling thread on the graph's capture device ([#197903](https://github.com/pytorch/pytorch/pull/197903))
- Fix memory-efficient attention failing with `hipErrorInvalidValue` on empty inputs ([#198022](https://github.com/pytorch/pytorch/pull/198022))
- Fix `torch.backends.cudnn.flags(depthwise_kernel="native")` being ignored on ROCm, where MIOpen depthwise was always chosen ([#198221](https://github.com/pytorch/pytorch/pull/198221))
- Fix PyTorch's `amdsmi` import shim overriding the `libamd_smi.so` library that `amdsmi` selected ([#197482](https://github.com/pytorch/pytorch/pull/197482))
- Fix hipify rewriting `std::max`/`std::min` to `::max`/`::min`, which silently narrowed 64-bit and unsigned host arguments to `int` ([#199444](https://github.com/pytorch/pytorch/pull/199444))
- Fix nondeterministic output order from `torch.topk` on slices longer than 256 elements ([#199425](https://github.com/pytorch/pytorch/pull/199425))
- Fix incorrect results from Inductor's BF16 atomic accumulation (for example `index_put_` with repeated indices) on gfx11/gfx12 GPUs by using the existing fallback ([#198199](https://github.com/pytorch/pytorch/pull/198199))
- Fix a spurious "Ignoring invalid value for boolean flag AMD_SERIALIZE_KERNEL: 3" warning in device-side error messages ([#186652](https://github.com/pytorch/pytorch/pull/186652))
- Fix incorrect SDPA results on gfx11 GPUs with AOTriton 0.11 and later by capping the supported head dimension at 256 ([#194280](https://github.com/pytorch/pytorch/pull/194280))
- Fix crashes and hangs when a captured backward pass creates a hipBLASLt handle during CUDA graph capture ([#196399](https://github.com/pytorch/pytorch/pull/196399))
- Fix flash attention (CK forward/backward and AOTriton forward) failing with "batch size must be positive" on an empty batch; it now returns empty outputs like CUDA ([#195812](https://github.com/pytorch/pytorch/pull/195812), [#195813](https://github.com/pytorch/pytorch/pull/195813), [#196723](https://github.com/pytorch/pytorch/pull/196723))
- Fix JIT C++ extensions that include ATen CUDA headers failing with `hipblas/hipblas.h: No such file or directory` when ROCm comes from TheRock pip wheels ([#196503](https://github.com/pytorch/pytorch/pull/196503))
- Fix the CUDA stream pool handing out the same HIP stream repeatedly when GPU tracing is enabled ([#188252](https://github.com/pytorch/pytorch/pull/188252))
- Fix TunableOp `PYTORCH_TUNABLEOP_RECORD_UNTUNED` not recording GEMMs that miss the tuned table on the BLAS fast path ([#194939](https://github.com/pytorch/pytorch/pull/194939))
- Stop RCCL 2.28+ from printing a deprecation warning on every all-to-all by calling `ncclAlltoAll`/`ncclAlltoAllv` ([#197534](https://github.com/pytorch/pytorch/pull/197534), [#199124](https://github.com/pytorch/pytorch/pull/199124))
### performance
- Cache the device warp size used by the BMM outer-product launch guard instead of querying it on every call ([#196368](https://github.com/pytorch/pytorch/pull/196368))
### docs
- Document SDPA BSHD vs. BHSD layout performance on the gfx1151 integrated GPU ([#190771](https://github.com/pytorch/pytorch/pull/190771))
- Document hipFile support in the GPUDirect Storage docs ([#195478](https://github.com/pytorch/pytorch/pull/195478))
- Note MI300 accuracy issues in `torch.set_float32_matmul_precision` ([#190736](https://github.com/pytorch/pytorch/pull/190736))
### devs
- `torch.utils.cpp_extension.ROCM_VERSION` now comes from the ROCm SDK version (`torch.version.rocm`, major.minor) instead of the HIP runtime version ([#194985](https://github.com/pytorch/pytorch/pull/194985))
- Fix source builds linking against a system-wide ROCm instead of the configured one because of libnuma rpath-link handling ([#194268](https://github.com/pytorch/pytorch/pull/194268))
### Untopiced
### not user facing
- [ROCm] Build and test the cublas and cusolver cpp extensions ([#197816](https://github.com/pytorch/pytorch/pull/197816))
### security
