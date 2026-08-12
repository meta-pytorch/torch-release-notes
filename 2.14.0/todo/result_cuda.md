
# Release Notes worksheet cuda

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

## cuda
### bc breaking
### deprecation
### new features
- Add public torch.cuda.graph_annotations module ([#189417](https://github.com/pytorch/pytorch/pull/189417))
- Annotate backward kernels in mark_kernels via node_creation_hook ([#191563](https://github.com/pytorch/pytorch/pull/191563))
### improvements
### bug fixes
- [CUDA graphs] Annotate kernels across graphs captured in sequence ([#186638](https://github.com/pytorch/pytorch/pull/186638))
- [cuda] Fix CUDA graph kernel-annotation remap for keep_graph=True ([#187741](https://github.com/pytorch/pytorch/pull/187741))
- [CUDA] Fix AvgPool2d backward handling of zero-padding  ([#188494](https://github.com/pytorch/pytorch/pull/188494))
- Fix heap overflow in CachingHostAllocator when rounding is disabled ([#192722](https://github.com/pytorch/pytorch/pull/192722))
### performance
### docs
### devs
### Untopiced
- Update torch cuda compatibility check ([#186285](https://github.com/pytorch/pytorch/pull/186285))
- [CUDA] torch.cuda: move green contexts to cuda python bindings ([#185527](https://github.com/pytorch/pytorch/pull/185527))
- [cuda] Unify CUDAGraph debug flag; move debug_dump to Python; add capture hooks ([#187749](https://github.com/pytorch/pytorch/pull/187749))
- [CUDA][CUDAGraph] Allow multiple pools in a single `CUDAGraph` ([#187929](https://github.com/pytorch/pytorch/pull/187929))
- [cuda] Keep _use_uvm allocator callbacks alive for the allocator's lifetime ([#188170](https://github.com/pytorch/pytorch/pull/188170))
- [CUDA] [GreenContext] deprecate set/pop context ([#188419](https://github.com/pytorch/pytorch/pull/188419))
- [fix][cuda][easy] signed zero in relu and clamp ([#185354](https://github.com/pytorch/pytorch/pull/185354))
- Fix `int32` overflow in `embedding_bag(mode="max")` backward pass ([#188661](https://github.com/pytorch/pytorch/pull/188661))
- [cudaMallocAsync] Trim the pool and retry once before raising OOM ([#188110](https://github.com/pytorch/pytorch/pull/188110))
- Add CUDA graph support for torch.while_loop ([#186055](https://github.com/pytorch/pytorch/pull/186055))
- [ROCm] fix wait instructions ([#188067](https://github.com/pytorch/pytorch/pull/188067))
- [cudaMallocAsync] Count graph-mem pool in memory_reserved() ([#186809](https://github.com/pytorch/pytorch/pull/186809))
- Fix 32-bit shift in Bitfield<uint64_t> non-PTX path ([#190410](https://github.com/pytorch/pytorch/pull/190410))
- Add 32-bit indexed kernel for CUDA FFT conjugate-symmetry fill ([#190269](https://github.com/pytorch/pytorch/pull/190269))
- Add destroy-callbacks and object retention to torch.cuda.CUDAGraph ([#190582](https://github.com/pytorch/pytorch/pull/190582))
- Add replay start/end hooks to torch.cuda.CUDAGraph ([#190602](https://github.com/pytorch/pytorch/pull/190602))
- Remove redundant zero-init of fully-overwritten buffers in CUDA kernels ([#190953](https://github.com/pytorch/pytorch/pull/190953))
- [ATen] [Native] [CUDA] Increase elements per thread for Rubin vectorized_elementwise_kernel ([#190546](https://github.com/pytorch/pytorch/pull/190546))
- Add half and bfloat16 support to angle on CUDA ([#191301](https://github.com/pytorch/pytorch/pull/191301))
- [CUDA][SDPA] Fix remap extents, causal key bound, and 32-bit dropout offsets in mem-efficient attention ([#192138](https://github.com/pytorch/pytorch/pull/192138))
- [cuda][graphs] Global lifecycle hooks for capture start/end and replay, plus a per-graph capture-start hook ([#192162](https://github.com/pytorch/pytorch/pull/192162))
- Increase clarity of CUDA errors by including excerpt from logs ([#191334](https://github.com/pytorch/pytorch/pull/191334))
- Fix (unused) return type for AtomicFPOp for BF16 ([#192548](https://github.com/pytorch/pytorch/pull/192548))
### not user facing
- [cuda graphs] Standardize string annotations on the "name" key ([#189406](https://github.com/pytorch/pytorch/pull/189406))
- [BE][CUDA] Migrate deprecated `thrust::` function objects to `cuda::std::` ([#191196](https://github.com/pytorch/pytorch/pull/191196))
- [BE] Delete old ROCm branches that apply to ROCM < 6.4 ([#192547](https://github.com/pytorch/pytorch/pull/192547))
### security
