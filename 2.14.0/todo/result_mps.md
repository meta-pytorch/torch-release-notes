
# Release Notes worksheet mps

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

## mps
### bc breaking
### deprecation
### new features
### improvements
- [MPS][BE] Migrate upsample nearest forward to Metal kernels ([#186989](https://github.com/pytorch/pytorch/pull/186989))
- [MPS] median and nanmedian to metal ([#187060](https://github.com/pytorch/pytorch/pull/187060))
- [MPS] Propagate MPS dispatch key to functorch wrapper tensors ([#187282](https://github.com/pytorch/pytorch/pull/187282))
- [MPS] Faster Cholesky via panel factorization with matmul2d trailing update ([#187022](https://github.com/pytorch/pytorch/pull/187022))
- [MPS] Faster reductions on non-contiguous inputs ([#187313](https://github.com/pytorch/pytorch/pull/187313))
- [MPS] logical not metal kernel ([#187324](https://github.com/pytorch/pytorch/pull/187324))
- [MPS] Migrate index_add and index_select to Metal kernels ([#187109](https://github.com/pytorch/pytorch/pull/187109))
- [MPS] Migrate argmin/argmax from MPSGraph to Metal kernels ([#187304](https://github.com/pytorch/pytorch/pull/187304))
- MPS: reject complex inputs in avg_pool templates ([#187671](https://github.com/pytorch/pytorch/pull/187671))
- [MPS] Add Binomial Metal kernel ([#187078](https://github.com/pytorch/pytorch/pull/187078))
- [MPS] Bucket large allocations to bound caching-allocator reserved memory during decode ([#187441](https://github.com/pytorch/pytorch/pull/187441))
- [MPS] Move mish to Metal kernel instead of MPSGraph ([#187906](https://github.com/pytorch/pytorch/pull/187906))
- [MPS] propagate nan for attention kernels on mps ([#188147](https://github.com/pytorch/pytorch/pull/188147))
- [MPS] proper error for batch norm when input is unsupported dtype ([#188265](https://github.com/pytorch/pytorch/pull/188265))
- [MPS] Add `ctc_loss` forward pass ([#187716](https://github.com/pytorch/pytorch/pull/187716))
- [MPS] Faster Cholesky via panel factorization with matmul2d trailing update ([#187022](https://github.com/pytorch/pytorch/pull/187022))
- [MPS] Parallelize Welford reduction in Metal codegen ([#188412](https://github.com/pytorch/pytorch/pull/188412))
- [MPS] support flex_attention return_aux max_scores ([#188362](https://github.com/pytorch/pytorch/pull/188362))
- [MPS] Support SymInt captures in flex_attention score_mod/mask_mod ([#188403](https://github.com/pytorch/pytorch/pull/188403))
- [MPS] linspace to metal ([#188905](https://github.com/pytorch/pytorch/pull/188905))
- [MPS] Port arange to metal kernel ([#188921](https://github.com/pytorch/pytorch/pull/188921))
- [MPS] Flex attention SymInt captures as int32 when they fit ([#188663](https://github.com/pytorch/pytorch/pull/188663))
- [MPS] Regenerate metallib header when generator script changes ([#189179](https://github.com/pytorch/pytorch/pull/189179))
- [MPS] Migrate lu_factor to Metal kernels ([#187038](https://github.com/pytorch/pytorch/pull/187038))
- [MPS] Migrate lu_factor to Metal kernels ([#187038](https://github.com/pytorch/pytorch/pull/187038))
- [MPS] Migrate lu_factor to Metal kernels ([#187038](https://github.com/pytorch/pytorch/pull/187038))
- [MPS] add matrix exp on MPS ([#188954](https://github.com/pytorch/pytorch/pull/188954))
- [MPS] add linalg polar ([#189701](https://github.com/pytorch/pytorch/pull/189701))
- [MPS] avoid double synchronization in bincount ([#190115](https://github.com/pytorch/pytorch/pull/190115))
- [MPS] Gemv kernels ([#186927](https://github.com/pytorch/pytorch/pull/186927))
- [MPS] Reuse unary dispatch stubs for inverse hyperbolic ops ([#190327](https://github.com/pytorch/pytorch/pull/190327))
- [MPS] F.linear fix for [B,1,K] (seq=1 decode) 8.5x regression on bf16/fp16 ([#189855](https://github.com/pytorch/pytorch/pull/189855))
- [Metal][ops] nonzero: support tensors above 2^32 elements (#149325) ([#188816](https://github.com/pytorch/pytorch/pull/188816))
- [MPS] Use float linspace kernel for small integral ranges ([#191060](https://github.com/pytorch/pytorch/pull/191060))
- [MPS] Faster reductions (1/5): skip input up-casts and vec4 full reductions ([#191101](https://github.com/pytorch/pytorch/pull/191101))
- [MPS] Reduce allocator fragmentation with placement heaps ([#190438](https://github.com/pytorch/pytorch/pull/190438))
- [MPS] Migrate conv3d to metal kernels ([#188802](https://github.com/pytorch/pytorch/pull/188802))
- [MPS] add support for complex cholesky ([#191836](https://github.com/pytorch/pytorch/pull/191836))
- [MPS] Fix MPP prefill attention for macos 26 machines ([#191794](https://github.com/pytorch/pytorch/pull/191794))
- [MPS] Faster reductions (2/5): inner-dim reductions ([#191097](https://github.com/pytorch/pytorch/pull/191097))
- [MPS] Vectorized contiguous cat fast path for any dimension ([#188200](https://github.com/pytorch/pytorch/pull/188200))
- [MPS] Enable mpp conv3d for no bias terms ([#192229](https://github.com/pytorch/pytorch/pull/192229))
- [MPS][BE] Pad int3 arguments to 16 bytes ([#191640](https://github.com/pytorch/pytorch/pull/191640))
- [MPS] Faster reductions (4/5): argmax/argmin strided, split-K and dim=None paths ([#191099](https://github.com/pytorch/pytorch/pull/191099))
- [MPS] Fix `torch.hypot` extreme value behavior ([#192541](https://github.com/pytorch/pytorch/pull/192541))
### bug fixes
- [MPS] Handle empty indexes in index_add ([#186990](https://github.com/pytorch/pytorch/pull/186990))
- [MPS] Matmul for strided out errors on mac OS 14/15 ([#187255](https://github.com/pytorch/pytorch/pull/187255))
- [MPS] Fix CPU scalar storage_offset ignored in binary op fast path ([#187229](https://github.com/pytorch/pytorch/pull/187229))
- Fix baddbmm nan propagation and test ([#187522](https://github.com/pytorch/pytorch/pull/187522))
- [MPS] Refactor inlined Metal reduction logic into shared header ([#187541](https://github.com/pytorch/pytorch/pull/187541))
- [MPS] fix threshold for empty input ([#187719](https://github.com/pytorch/pytorch/pull/187719))
- [MPS] Fix linear backward reshape->matmul->reshape > 4D issue ([#187379](https://github.com/pytorch/pytorch/pull/187379))
- [MPS] Fix BatchNorm channels_last backward crash ([#188371](https://github.com/pytorch/pytorch/pull/188371))
- [MPS] Fix baddbmm for empty inputs ([#188808](https://github.com/pytorch/pytorch/pull/188808))
- [MPS] Fix incorrect conv2d output for kernel size >= 256 ([#188359](https://github.com/pytorch/pytorch/pull/188359))
- [MPS] fix floor divide ([#189252](https://github.com/pytorch/pytorch/pull/189252))
- [MPS] Make pin_memory return CPU-aliased storage backed by a unified MTLBuffer ([#181720](https://github.com/pytorch/pytorch/pull/181720))
- [MPS] Prevent dtype-converting D2H copies from overwriting source ([#189572](https://github.com/pytorch/pytorch/pull/189572))
- [MPS] Compute integer abs exactly instead of through float32 ([#190053](https://github.com/pytorch/pytorch/pull/190053))
- [MPS] Fix complex64 linear crash on macOS 27 by flattening input outside the graph ([#190352](https://github.com/pytorch/pytorch/pull/190352))
- [MPS] Handle in_features=0 in linear forward and backward ([#190051](https://github.com/pytorch/pytorch/pull/190051))
- [MPS] Fix torch.nextafter for bfloat16 ([#190481](https://github.com/pytorch/pytorch/pull/190481))
- [MPS] Gather non-dense equal-strided views in MPS-to-CPU copy ([#189966](https://github.com/pytorch/pytorch/pull/189966))
- [MPS] Preserve precision for integral linspace ([#189630](https://github.com/pytorch/pytorch/pull/189630))
- [MPS] Faster reductions (0/5): fix int64 min/max over partial simdgroups ([#191104](https://github.com/pytorch/pytorch/pull/191104))
- [MPS] fix adaptive max pooling for non-divisible sizes ([#189659](https://github.com/pytorch/pytorch/pull/189659))
- [MPS] fix older gpu gen mac matmul failures ([#183535](https://github.com/pytorch/pytorch/pull/183535))
- [MPS] Change exponential to return values in  `(0, inf)` instead of `[0, inf)` range ([#192621](https://github.com/pytorch/pytorch/pull/192621))
### performance
- [MPS] Migrate GLU to Metal ([#187833](https://github.com/pytorch/pytorch/pull/187833))
### docs
### devs
### Untopiced
- [MPS] Native Metal kernel for Poisson distribution ([#173319](https://github.com/pytorch/pytorch/pull/173319))
- [MPS] Migrate sigmoid_backward from MPSGraph to Metal ([#187151](https://github.com/pytorch/pytorch/pull/187151))
- [MPS] Migrate log_sigmoid forward/backward from MPSGraph to Metal ([#187228](https://github.com/pytorch/pytorch/pull/187228))
- [aten] Fix CPU and MPS logit for eps > 0.5 ([#181297](https://github.com/pytorch/pytorch/pull/181297))
- [MPS] Fix the fft issues if target dim not among the last four ([#186967](https://github.com/pytorch/pytorch/pull/186967))
- [MPS] Native SVD, eigh, and lstsq via Jacobi kernels ([#185954](https://github.com/pytorch/pytorch/pull/185954))
- [MPS] Support returning lse in flex attention ([#187768](https://github.com/pytorch/pytorch/pull/187768))
- [MPS] Add missing kernel coalescing calls in LinearAlgebra.mm ([#188308](https://github.com/pytorch/pytorch/pull/188308))
- [MPS] Add `ctc_loss` backward pass ([#188187](https://github.com/pytorch/pytorch/pull/188187))
- [MPS] Vectorize elementwise ops on inner-contiguous (sliced/strided) views ([#188483](https://github.com/pytorch/pytorch/pull/188483))
- [MPS] Fix F.linear dropping bias for vector-shaped inputs ([#188619](https://github.com/pytorch/pytorch/pull/188619))
- [MPS] Guard cummax/cummin against complex dtypes ([#188038](https://github.com/pytorch/pytorch/pull/188038))
- [MPS] Reject complex logaddexp2 inputs before Metal dispatch ([#188800](https://github.com/pytorch/pytorch/pull/188800))
- Fix MPS baddbmm/addbmm crash on size-0 tensors  ([#187879](https://github.com/pytorch/pytorch/pull/187879))
- [MPS] Add `_upsample_(bilinear|bicubic)2d_aa_backward` ([#188819](https://github.com/pytorch/pytorch/pull/188819))
- [MPS] Migrate lu solve to metal kernels ([#189200](https://github.com/pytorch/pytorch/pull/189200))
- [MPS] Fix two exec_ternary_kernel dispatch bugs ([#189624](https://github.com/pytorch/pytorch/pull/189624))
- [MPS] copy for contiguous same-dtype using a compute kernel ([#188613](https://github.com/pytorch/pytorch/pull/188613))
- [MPS] Migrate nan_to_num to a Metal kernel with an ILP dense variant ([#189489](https://github.com/pytorch/pytorch/pull/189489))
- [MPS] Add `geqrf` and refactor `linalg_qr` ([#189192](https://github.com/pytorch/pytorch/pull/189192))
- [MPS] Apply inter-layer dropout in LSTM backward and fix dropout=1 NaN ([#190059](https://github.com/pytorch/pytorch/pull/190059))
- [MPS] Blit CPU<->MPS copies directly from pinned buffers with event-deferred reclaim ([#189512](https://github.com/pytorch/pytorch/pull/189512))
- [MPS] Fix native_layer_norm for small-variance rows via two-pass kernel ([#190492](https://github.com/pytorch/pytorch/pull/190492))
- [MPS] Fix F.linear with bias corrupting rows when a batch dim exceeds 2^16 ([#189496](https://github.com/pytorch/pytorch/pull/189496))
- [Metal][ops] add EmbeddingBag offsets validation (#170370) ([#187572](https://github.com/pytorch/pytorch/pull/187572))
- [MPS] Support mixed-dtype affine params in layer_norm forward and backward ([#190055](https://github.com/pytorch/pytorch/pull/190055))
- [MPS] Add MPS stream pool and Python bindings ([#190375](https://github.com/pytorch/pytorch/pull/190375))
- [MPS] Fast atomic-free path for flat torch.unique (fixes #97310 perf + #111173 correctness) ([#184780](https://github.com/pytorch/pytorch/pull/184780))
- [MPS] enable metal performance primitives attention ([#182256](https://github.com/pytorch/pytorch/pull/182256))
- [MPS] nonzero: recompute intra-block prefixes in scatter, drop per-element scratch ([#191274](https://github.com/pytorch/pytorch/pull/191274))
- Tidy MPSGuardImpl: name capability bitmask and fix clang-tidy nits ([#185758](https://github.com/pytorch/pytorch/pull/185758))
- Fix MPS fused RMSNorm: do the weight multiply in fp32 to match CPU/CUDA ([#189617](https://github.com/pytorch/pytorch/pull/189617))
- [MPS] Faster reductions (3/5): strided/batched outer, small-dim and narrow kernels ([#191098](https://github.com/pytorch/pytorch/pull/191098))
- [MPS] Fix conv2d/backward with non-contiguous weights ([#192303](https://github.com/pytorch/pytorch/pull/192303))
- [MPS] Faster reductions (5/5): migrate min/max from MPSGraph to Metal ([#191100](https://github.com/pytorch/pytorch/pull/191100))
### not user facing
- [BE][MPS] Fix flase-positive compiler warnings ([#186822](https://github.com/pytorch/pytorch/pull/186822))
- [MPS] Enable device type tests for TestDistributions, allow MPS ([#186153](https://github.com/pytorch/pytorch/pull/186153))
- [MPS] Fix vectype specialization for long ([#187542](https://github.com/pytorch/pytorch/pull/187542))
- [MPS] [BE] Fix compilation warning ([#187753](https://github.com/pytorch/pytorch/pull/187753))
- [mps] Add dependencies for metallib headers in CMake ([#187087](https://github.com/pytorch/pytorch/pull/187087))
- [MPS] igamma/igammac: add TORCH_CHECK_TYPE guard for complex dtypes ([#188134](https://github.com/pytorch/pytorch/pull/188134))
- [BE][Ez]: Microptimize MPS Operation Utils ([#188342](https://github.com/pytorch/pytorch/pull/188342))
- [BE] Fix compilation warnings ([#188416](https://github.com/pytorch/pytorch/pull/188416))
- [BE][MPS] Call function directly ([#188414](https://github.com/pytorch/pytorch/pull/188414))
- [MPS] adding jhavukainen as code owner to MPS files ([#188620](https://github.com/pytorch/pytorch/pull/188620))
- [BE] Rename `is_macos_13_or_newer` to `is_macos_at_least` ([#188645](https://github.com/pytorch/pytorch/pull/188645))
- [BE] Fix -Wc99-designator warning in `getMPSScalar` ([#188910](https://github.com/pytorch/pytorch/pull/188910))
- [MPS] Add `@serialTest` to `test_group_norm_backward_large_input` ([#188855](https://github.com/pytorch/pytorch/pull/188855))
- [MPS] Reject bool inputs in linalg.cross at the meta dispatch boundary ([#187274](https://github.com/pytorch/pytorch/pull/187274))
- [BE][MPS] Factor host-buffer wrapping into buffer_with_offset_from_tensor ([#189256](https://github.com/pytorch/pytorch/pull/189256))
- [MPS] Remove dead xfail/tolerance keys from MPS test infra ([#186046](https://github.com/pytorch/pytorch/pull/186046))
- [MPS] Add `largeTensorTest` to `test_group_norm_backward_large_input` ([#189215](https://github.com/pytorch/pytorch/pull/189215))
- [BE] Use is_apple_family_or_newer helper ([#189867](https://github.com/pytorch/pytorch/pull/189867))
- [BE] use round up utility ([#189869](https://github.com/pytorch/pytorch/pull/189869))
- [BE] [MPS] Pass kernel name to exec_unary_kernel_raw as `string_view` ([#189981](https://github.com/pytorch/pytorch/pull/189981))
- [BE][Ez]: Optimize some TensorIter calls to use const_inputs ([#191358](https://github.com/pytorch/pytorch/pull/191358))
- [MPS] Drain in-flight work before stopping metal capture ([#191362](https://github.com/pytorch/pytorch/pull/191362))
- [BE][MPS] Fix unused parameters warnings in Unique.metal ([#191636](https://github.com/pytorch/pytorch/pull/191636))
- [BE] add test for metal nchw_to_nhwc_kernel ([#191810](https://github.com/pytorch/pytorch/pull/191810))
- [BE][MPS] Remove unused kernel parameters ([#191970](https://github.com/pytorch/pytorch/pull/191970))
- [BE] move gemv kernels to separate file (1/N) ([#192053](https://github.com/pytorch/pytorch/pull/192053))
- [BE] factor gemv launch setup into helpers (2/N) ([#192054](https://github.com/pytorch/pytorch/pull/192054))
- [BE] Use has_mpp helper in conv3d metal kernels ([#192807](https://github.com/pytorch/pytorch/pull/192807))
### security
