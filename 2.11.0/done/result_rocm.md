
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
caffe2 support is fully removed from ROCm PyTorch's hipify preprocessing.  This is known as "hipify v2" behavior.  
#### hipify v1 background
When caffe2 and PyTorch were separate projects, the ROCm support strategies were different.  For caffe2, all files and classes would be renamed following the pattern of CUDA to HIP, Cuda to Hip, cuda to hip, and so on.  PyTorch did not rename classes, but would create new files following the same renaming pattern (e.g., aten/src/ATen/cuda/CUDABlas.h to aten/src/ATen/hip/HIPBlas.h).  As a consequence, caffe2 had a distinct device backend named "HIP" (renamed from "CUDA") while ROCm PyTorch masquerades as the "cuda" device (`torch.empty(1, device="cuda")`).  Once caffe2 and PyTorch projects were merged, this caused a mismatch between caffe2 expecting to use a "HIP" device while PyTorch expecting a "cuda" device.  To alleviate this mismatch, "Masquerading" classes were created under aten/src/ATen/hip/impl.
- HIPAllocatorMasqueradingAsCUDA.h
- HIPCachingAllocatorMasqueradingAsCUDA.h
- HIPGuardImplMasqueradingAsCUDA.h
- HIPStreamMasqueradingAsCUDA.h
These classes were often transparently utilized during ROCm PyTorch's hipify preprocessing of source files.  All files under c10/ and caffe2/ were hipified using the caffe2 renaming behavior, while all other "PyTorch" files used the other strategy.  The Masquerading classes would replace their CUDA counterpart during hipify preprocessing.  For example, c10/cuda/CUDAStream.h's CUDAStream would be replaced by aten/src/ATen/hip/impl/HIPStreamMasqueradingAsCUDA.h's HIPStreamMasqueradingAsCUDA.  These Masquerading classes call the underlying caffe2 code and create "HIP" devices, and the device would be reset to "cuda" by the Masquerading classes.
#### hipify v2 new behavior
Hipify v2 ([#174087](https://github.com/pytorch/pytorch/pull/174087), [#174300](https://github.com/pytorch/pytorch/pull/174300), [#174388](https://github.com/pytorch/pytorch/pull/174388), [#174499](https://github.com/pytorch/pytorch/pull/174499), [#175098](https://github.com/pytorch/pytorch/pull/175098)) makes the following changes:
- "Masquerading" classes are deprecated. Reworked to be thin shells around existing classes, for backward compatibility.
- Do not rename "CUDA" classes to "HIP". Only rename CUDA Runtime APIs. Files are still renamed out of place.
- Removes caffe2 work-arounds for HIP device versus CUDA device.
Great care has been taken to make this change backwards compatible.  Though PyTorch today builds cleanly using hipify v2 behavior, downstream PyTorch extension projects that explicitly included Masquerading headers or called Masquerading APIs could be affected, resulting in failed builds.  As an example, before backwards compatibility was realized, the xformers project had failed to build using the hipify v2 changes.  A [PR demonstrates the changes that were initially necessary to work around the build failures,](https://github.com/facebookresearch/xformers/pull/1351) but such changes are no longer necessary after hipify v2 BC-breaking behavior was improved.
### new features
- Expose device properties clock_rate, memory_clock_rate, memory_bus_width, memory_per_block, shared_memory_per_block. ([#170572](https://github.com/pytorch/pytorch/pull/170572))
- Support for device-side assertions via TORCH_USE_HIP_DSA. ([#172679](https://github.com/pytorch/pytorch/pull/172679))
- Attention operator support on gfx1151/1152/1153 via AOTriton 0.11.2b.
- Enable scaled group mm on gfx950. ([#173737](https://github.com/pytorch/pytorch/pull/173737))
- Enable group gemm on gfx90a. ([#169356](https://github.com/pytorch/pytorch/pull/169356))
- Enable MIOpen backend for CTC Loss. ([#170749](https://github.com/pytorch/pytorch/pull/170749))
- Add hipsparseSpSV and hipsparseSpSM support for triangular solve. ([#171097](https://github.com/pytorch/pytorch/pull/171097))
- Support for PyTorch's StaticCudaLauncher, which provides static compilation and launching of Triton kernels. ([#166492](https://github.com/pytorch/pytorch/pull/166492))
### improvements
- addmm behavior now takes into account preferred BLAS backend instead of forcing hipblaslt. ([#174350](https://github.com/pytorch/pytorch/pull/174350))
- Enable hipBLASLt on gfx1103. ([#172180](https://github.com/pytorch/pytorch/pull/172180))
### bug fixes
- Sliding window attention nan issue is fixed by AOTriton 0.11.2b. ([#173204](https://github.com/pytorch/pytorch/issues/173204), [#174105](https://github.com/pytorch/pytorch/pull/174105))
- Increase the event_name attribute of autograd's profiler_util.py to avoid truncation of long HIP events. ([#174366](https://github.com/pytorch/pytorch/pull/174366))
- Cholesky operator via MAGMA was missing a sync operation. ([#172112](https://github.com/pytorch/pytorch/pull/172112))
- Updated patched libdrm in bundled release wheels to avoid missing amdgpu.ids warning and properly return AMDGPU marketing names. ([#174811](https://github.com/pytorch/pytorch/pull/174811))
- Fix fake_quantize undefined behavior with inf. ([#171777](https://github.com/pytorch/pytorch/pull/171777))
- Fix deterministic scan kernel edge case. ([#170763](https://github.com/pytorch/pytorch/pull/170763))
- Use torch's caching allocator for CK workspaces, for better memory behavior and hipGraph capture. ([#172311](https://github.com/pytorch/pytorch/pull/172311))
- Grouped gemm 2d2d has uninitalized data. ([#174314](https://github.com/pytorch/pytorch/pull/174314))
### performance
- MIOpen channels last support remains opt-in using the environment variables PYTORCH_MIOPEN_SUGGEST_NHWC=1 and PYTORCH_MIOPEN_SUGGEST_NHWC_BATCHNORM=1. ([#170780](https://github.com/pytorch/pytorch/pull/170780))
- New fx pass to reduce atomic contention. ([#168073](https://github.com/pytorch/pytorch/pull/168073))
- TopK performance improvements; single-block warp-level compaction ([#171940](https://github.com/pytorch/pytorch/pull/171940)), warp merge sort ([#170029](https://github.com/pytorch/pytorch/pull/170029)).
- Enable fastSpecializedAtomicAdd for gfx950, improving performance of index-based operators like embedding bag, sampling, and scatter/gather. ([#170330](https://github.com/pytorch/pytorch/pull/170330))
- Optimize radix select by caching data on shared memory. ([#172517](https://github.com/pytorch/pytorch/pull/172517))
- Optimize reduction operator launch configuration for better performance. ([#173576](https://github.com/pytorch/pytorch/pull/173576))
- Improvements to inductor reduction kernel heuristics for MI350. ([#170931](https://github.com/pytorch/pytorch/pull/170931))
### docs
### devs
- Fix unused-result warning in UniqueCub.cu ([#174203](https://github.com/pytorch/pytorch/pull/174203))
- Use rocm_sdk preloaded libraries for hiprtc and amdhip64. ([#169855](https://github.com/pytorch/pytorch/pull/169855))
- Fix torch.utils.cpp_extension build folder accelerator detection ROCm ([#170784](https://github.com/pytorch/pytorch/pull/170784))
- Unify hipBLASLt architecture lists into common hook methods. ([#172791](https://github.com/pytorch/pytorch/pull/172791))
### Untopiced
### not user facing
### security
