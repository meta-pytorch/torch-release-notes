
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
- Add native MPS support for binomial sampling ([#187078](https://github.com/pytorch/pytorch/pull/187078))
- Add MPS forward and backward support for `torch.nn.functional.ctc_loss` ([#187716](https://github.com/pytorch/pytorch/pull/187716), [#188187](https://github.com/pytorch/pytorch/pull/188187))
- Add MPS support for `torch.linalg.matrix_exp`, including complex inputs, on macOS 15 or newer ([#188954](https://github.com/pytorch/pytorch/pull/188954))
- Add native MPS Poisson sampling, eliminating its CPU fallback ([#173319](https://github.com/pytorch/pytorch/pull/173319))
- Add native float32 and complex64 MPS implementations of `torch.linalg.svd`, `svdvals`, `eigh`, `eigvalsh`, and `lstsq`, enabling dependent operations such as `matrix_rank`, `pinv`, and `cond` to remain on device ([#185954](https://github.com/pytorch/pytorch/pull/185954))
### improvements
- Support `return_aux(max_scores=True)` in MPS `flex_attention` forward ([#188362](https://github.com/pytorch/pytorch/pull/188362))
- Support SymInt captures in MPS `flex_attention` score and mask functions, including dynamically shaped compiled graphs ([#188403](https://github.com/pytorch/pytorch/pull/188403))
- Add MPS support for `torch.linalg.polar` ([#189701](https://github.com/pytorch/pytorch/pull/189701))
- Support MPS `torch.nonzero` on tensors containing more than 2^32 elements ([#188816](https://github.com/pytorch/pytorch/pull/188816))
- Add complex MPS support for Cholesky factorization ([#191836](https://github.com/pytorch/pytorch/pull/191836))
- Support key/value batch broadcasting and returning log-sum-exp values from MPS `flex_attention` ([#187722](https://github.com/pytorch/pytorch/pull/187722), [#187768](https://github.com/pytorch/pytorch/pull/187768))
- Add MPS backward support for antialiased bilinear and bicubic 2D upsampling ([#188819](https://github.com/pytorch/pytorch/pull/188819))
- Add complex MPS support to `torch.nan_to_num` and correctly resize empty `out=` tensors ([#189489](https://github.com/pytorch/pytorch/pull/189489))
- Add MPS `torch.geqrf` support and align the MPS `torch.linalg.qr` implementation with other backends ([#189192](https://github.com/pytorch/pytorch/pull/189192))
### bug fixes
- Preserve the MPS dispatch key through `torch.func` transforms so MPS autocast and autograd work under transforms such as `vmap` and `grad` ([#187282](https://github.com/pytorch/pytorch/pull/187282))
- Reject complex MPS average-pooling inputs with `NotImplementedError` instead of an internal MPSGraph error ([#187671](https://github.com/pytorch/pytorch/pull/187671))
- Propagate NaNs correctly through MPS scaled dot-product attention kernels ([#188147](https://github.com/pytorch/pytorch/pull/188147))
- Raise a clear error when MPS batch normalization receives an unsupported dtype ([#188265](https://github.com/pytorch/pytorch/pull/188265))
- Fix corrupted MPS prefill-attention output on macOS 26 by selecting the correct Metal cooperative-tensor ABI ([#191794](https://github.com/pytorch/pytorch/pull/191794))
- Fix Metal argument alignment that could make MPS kernels fail validation or crash under the Metal debug layer ([#191640](https://github.com/pytorch/pytorch/pull/191640))
- Fix `torch.hypot` producing incorrect results for extreme values ([#192541](https://github.com/pytorch/pytorch/pull/192541))
- Handle empty indices in MPS `index_add` and empty dimensions in threshold, `baddbmm`, and `addbmm` operations ([#186990](https://github.com/pytorch/pytorch/pull/186990), [#187719](https://github.com/pytorch/pytorch/pull/187719), [#188808](https://github.com/pytorch/pytorch/pull/188808), [#187879](https://github.com/pytorch/pytorch/pull/187879))
- Fix `mm` and `addmm` with strided output tensors on macOS 14 and 15 ([#187255](https://github.com/pytorch/pytorch/pull/187255))
- Respect `storage_offset` when an MPS binary operation consumes a zero-dimensional CPU tensor view ([#187229](https://github.com/pytorch/pytorch/pull/187229))
- Make MPS `baddbmm` follow its documented behavior by not propagating NaN or infinity from the input when `beta=0` ([#187522](https://github.com/pytorch/pytorch/pull/187522))
- Fix compiled MPS min/max reductions mishandling negative infinity ([#187541](https://github.com/pytorch/pytorch/pull/187541))
- Fix MPS linear backward for inputs with more than four dimensions and prevent complex high-rank linear operations from aborting on macOS 27 ([#187379](https://github.com/pytorch/pytorch/pull/187379), [#190352](https://github.com/pytorch/pytorch/pull/190352))
- Fix BatchNorm backward crashing for channels-last MPS tensors ([#188371](https://github.com/pytorch/pytorch/pull/188371))
- Fix incorrect MPS Conv2d output when a kernel spatial dimension is at least 256 ([#188359](https://github.com/pytorch/pytorch/pull/188359))
- Fix MPS floor division semantics ([#189252](https://github.com/pytorch/pytorch/pull/189252))
- Make MPS-backed pinned memory correctly appear as a CPU tensor while retaining its shared Metal buffer ([#181720](https://github.com/pytorch/pytorch/pull/181720))
- Prevent dtype-converting MPS-to-CPU copies from overwriting their source and correctly copy non-dense views with matching strides ([#189572](https://github.com/pytorch/pytorch/pull/189572), [#189966](https://github.com/pytorch/pytorch/pull/189966))
- Compute integer absolute values exactly instead of rounding through `float32` ([#190053](https://github.com/pytorch/pytorch/pull/190053))
- Handle zero `in_features` in MPS linear forward and backward without aborting ([#190051](https://github.com/pytorch/pytorch/pull/190051))
- Fix `torch.nextafter` returning its input unchanged for MPS `bfloat16` tensors ([#190481](https://github.com/pytorch/pytorch/pull/190481))
- Preserve exact integer values in MPS `torch.linspace` for large ranges ([#189630](https://github.com/pytorch/pytorch/pull/189630))
- Fix `int64` minimum and maximum reductions returning zero when a partial SIMD group contains only negative or positive values ([#191104](https://github.com/pytorch/pytorch/pull/191104))
- Fix adaptive max pooling for input sizes that are not divisible by the output size ([#189659](https://github.com/pytorch/pytorch/pull/189659))
- Fix large matrix multiplications producing incorrect results on M1 and M2 GPUs ([#183535](https://github.com/pytorch/pytorch/pull/183535))
- Keep MPS exponential samples strictly positive so `torch.multinomial(..., 1)` cannot select a zero-probability entry ([#192621](https://github.com/pytorch/pytorch/pull/192621))
- Make CPU and MPS `torch.logit` agree with other backends when `eps > 0.5` ([#181297](https://github.com/pytorch/pytorch/pull/181297))
- Fix MPS FFT operations when a transformed dimension is not among the tensor's final four dimensions ([#186967](https://github.com/pytorch/pytorch/pull/186967))
- Fix `torch.nn.functional.linear` dropping its bias for vector-shaped inputs on macOS 26 ([#188619](https://github.com/pytorch/pytorch/pull/188619))
- Raise clear unsupported-dtype errors for complex MPS inputs to `cummax`, `cummin`, and `logaddexp2` ([#188038](https://github.com/pytorch/pytorch/pull/188038), [#188800](https://github.com/pytorch/pytorch/pull/188800))
- Fix MPS ternary-kernel dispatch for large tensors and mixed-dtype `out=` tensors, including `torch.clamp` ([#189624](https://github.com/pytorch/pytorch/pull/189624))
- Apply inter-layer dropout correctly in MPS LSTM backward and avoid NaNs when `dropout=1` ([#190059](https://github.com/pytorch/pytorch/pull/190059))
- Improve MPS layer-normalization correctness for small-variance rows and add 64-bit indexing support ([#190492](https://github.com/pytorch/pytorch/pull/190492))
- Fix biased MPS linear operations corrupting rows when a batch dimension exceeds 2^16 ([#189496](https://github.com/pytorch/pytorch/pull/189496))
- Validate MPS `EmbeddingBag` offsets consistently with CPU and CUDA instead of silently returning incorrect results ([#187572](https://github.com/pytorch/pytorch/pull/187572))
- Support float32 affine parameters with float16 or bfloat16 MPS layer normalization in forward and backward ([#190055](https://github.com/pytorch/pytorch/pull/190055))
- Match CPU and CUDA RMSNorm precision by performing the fused affine multiplication in float32 ([#189617](https://github.com/pytorch/pytorch/pull/189617))
- Fix Conv2d forward and backward with non-contiguous MPS weights ([#192303](https://github.com/pytorch/pytorch/pull/192303))
- Raise clear unsupported-dtype errors for complex `igamma`/`igammac` and boolean `torch.linalg.cross` inputs on MPS ([#188134](https://github.com/pytorch/pytorch/pull/188134), [#187274](https://github.com/pytorch/pytorch/pull/187274))
- Prevent intermittent crashes when stopping a Metal capture by draining work from all active MPS streams first ([#191362](https://github.com/pytorch/pytorch/pull/191362))
### performance
- Reduce launch overhead and improve strided-input performance by moving nearest-neighbor upsampling, logical not, index operations, argmin/argmax, and Mish to native Metal kernels ([#186989](https://github.com/pytorch/pytorch/pull/186989), [#187324](https://github.com/pytorch/pytorch/pull/187324), [#187109](https://github.com/pytorch/pytorch/pull/187109), [#187304](https://github.com/pytorch/pytorch/pull/187304), [#187906](https://github.com/pytorch/pytorch/pull/187906))
- Speed up `median` and `nanmedian` and avoid large intermediate allocations by using native Metal kernels ([#187060](https://github.com/pytorch/pytorch/pull/187060))
- Speed up Cholesky factorization with panel factorization and matrix-multiplication trailing updates ([#187022](https://github.com/pytorch/pytorch/pull/187022))
- Speed up reductions on permuted contiguous inputs ([#187313](https://github.com/pytorch/pytorch/pull/187313))
- Reduce caching-allocator reserved memory during decoding by bucketing large allocations ([#187441](https://github.com/pytorch/pytorch/pull/187441))
- Speed up variance and normalization reductions in compiled MPS workloads with parallel Welford reduction ([#188412](https://github.com/pytorch/pytorch/pull/188412))
- Speed up `torch.linspace` and `torch.arange` by moving them to native Metal kernels ([#188905](https://github.com/pytorch/pytorch/pull/188905), [#188921](https://github.com/pytorch/pytorch/pull/188921))
- Speed up MPS `flex_attention` by using 32-bit symbolic captures when their values fit ([#188663](https://github.com/pytorch/pytorch/pull/188663))
- Speed up `torch.linalg.lu_factor` with native Metal kernels, especially for batched factorizations ([#187038](https://github.com/pytorch/pytorch/pull/187038))
- Reduce synchronization overhead in MPS `torch.bincount` ([#190115](https://github.com/pytorch/pytorch/pull/190115))
- Add optimized Metal GEMV paths for matrix-vector operations, including strided inputs and fused bias ([#186927](https://github.com/pytorch/pytorch/pull/186927))
- Eliminate a major half-precision `torch.nn.functional.linear` regression for three-dimensional sequence-length-one inputs used in batched decoding ([#189855](https://github.com/pytorch/pytorch/pull/189855))
- Speed up integral `torch.linspace` for small ranges by using the floating-point kernel where it remains sufficiently precise ([#191060](https://github.com/pytorch/pytorch/pull/191060))
- Speed up full and inner-dimension reductions by avoiding input materialization and adding specialized vectorized, packed-row, and split-K kernels ([#191101](https://github.com/pytorch/pytorch/pull/191101), [#191097](https://github.com/pytorch/pytorch/pull/191097))
- Reduce allocator fragmentation for dynamic-shape workloads by coalescing free ranges in placement heaps ([#190438](https://github.com/pytorch/pytorch/pull/190438))
- Speed up MPS Conv3d with native Metal and Metal Performance Primitives kernels, including convolutions without bias ([#188802](https://github.com/pytorch/pytorch/pull/188802), [#192229](https://github.com/pytorch/pytorch/pull/192229))
- Speed up contiguous, same-dtype `torch.cat` along any dimension with vectorized Metal copies ([#188200](https://github.com/pytorch/pytorch/pull/188200))
- Speed up `argmax` and `argmin` for strided tensors, full reductions, and shapes that benefit from split-K kernels ([#191099](https://github.com/pytorch/pytorch/pull/191099))
- Speed up GLU forward and backward with fused native Metal kernels ([#187833](https://github.com/pytorch/pytorch/pull/187833))
- Reduce dispatch overhead for sigmoid backward and log-sigmoid forward/backward by moving them to native Metal kernels ([#187151](https://github.com/pytorch/pytorch/pull/187151), [#187228](https://github.com/pytorch/pytorch/pull/187228))
- Speed up unary, binary, and copy operations on sliced or strided views whose innermost dimension is contiguous ([#188483](https://github.com/pytorch/pytorch/pull/188483))
- Speed up LU-based linear solves with native Metal kernels, particularly for batched systems and single right-hand sides ([#189200](https://github.com/pytorch/pytorch/pull/189200))
- Speed up contiguous same-dtype MPS copies with compute kernels and transfer pinned CPU buffers directly without rewrapping them ([#188613](https://github.com/pytorch/pytorch/pull/188613), [#189512](https://github.com/pytorch/pytorch/pull/189512))
- Add an atomic-free fast path for flat `torch.unique`, fixing incorrect large-int64 results and dramatically accelerating inputs with long duplicate runs ([#184780](https://github.com/pytorch/pytorch/pull/184780))
- Speed up scaled dot-product attention prefill with Metal Performance Primitives on supported macOS versions and GPU generations ([#182256](https://github.com/pytorch/pytorch/pull/182256))
- Reduce `torch.nonzero` memory use for very large tensors by recomputing per-block prefixes during scatter ([#191274](https://github.com/pytorch/pytorch/pull/191274))
- Speed up reductions over non-final dimensions with specialized strided, batched, narrow, and split-K kernels ([#191098](https://github.com/pytorch/pytorch/pull/191098))
- Speed up MPS `min` and `max` reductions by moving them from MPSGraph to Metal while fixing NaN index selection ([#191100](https://github.com/pytorch/pytorch/pull/191100))
### docs
### devs
- Regenerate bundled Metal library headers when their generator script changes ([#189179](https://github.com/pytorch/pytorch/pull/189179))
- Rebuild bundled Metal library headers when their source `.metal` files change ([#187087](https://github.com/pytorch/pytorch/pull/187087))
- Clean up Metal compiler warnings, including compatibility with Metal 3 and newer SDK diagnostics ([#186822](https://github.com/pytorch/pytorch/pull/186822), [#187753](https://github.com/pytorch/pytorch/pull/187753), [#188416](https://github.com/pytorch/pytorch/pull/188416), [#188910](https://github.com/pytorch/pytorch/pull/188910), [#191636](https://github.com/pytorch/pytorch/pull/191636), [#191970](https://github.com/pytorch/pytorch/pull/191970))
### not user facing
- Reuse shared unary dispatch stubs for inverse hyperbolic MPS operations ([#190327](https://github.com/pytorch/pytorch/pull/190327))
- Add missing command-encoder coalescing calls to internal MPS LU and solve implementations ([#188308](https://github.com/pytorch/pytorch/pull/188308))
- Add the internal MPS stream pool and low-level bindings that will support a future public stream API ([#190375](https://github.com/pytorch/pytorch/pull/190375))
- Clean up the internal MPS guard implementation and clang-tidy warnings ([#185758](https://github.com/pytorch/pytorch/pull/185758))
- Expand distribution tests to run on MPS and clean up obsolete MPS test exceptions ([#186153](https://github.com/pytorch/pytorch/pull/186153), [#186046](https://github.com/pytorch/pytorch/pull/186046))
- Correct an unused internal Metal vector-type specialization for 64-bit integers ([#187542](https://github.com/pytorch/pytorch/pull/187542))
- Simplify internal MPS operation utilities and Metal-header generation code ([#188342](https://github.com/pytorch/pytorch/pull/188342), [#188414](https://github.com/pytorch/pytorch/pull/188414))
- Update MPS code ownership and internal macOS/GPU-family helper names ([#188620](https://github.com/pytorch/pytorch/pull/188620), [#188645](https://github.com/pytorch/pytorch/pull/188645), [#189867](https://github.com/pytorch/pytorch/pull/189867))
- Stabilize the large MPS group-normalization backward test on memory-constrained runners ([#188855](https://github.com/pytorch/pytorch/pull/188855), [#189215](https://github.com/pytorch/pytorch/pull/189215))
- Consolidate internal host-buffer wrapping for CPU-to-MPS and MPS-to-CPU copies ([#189256](https://github.com/pytorch/pytorch/pull/189256))
- Use shared utility types and avoid unnecessary string and tensor-input copies in internal MPS kernel dispatch ([#189869](https://github.com/pytorch/pytorch/pull/189869), [#189981](https://github.com/pytorch/pytorch/pull/189981), [#191358](https://github.com/pytorch/pytorch/pull/191358))
- Add direct coverage for the Metal NCHW-to-NHWC conversion kernel ([#191810](https://github.com/pytorch/pytorch/pull/191810))
- Refactor GEMV kernels and launch configuration without changing behavior ([#192053](https://github.com/pytorch/pytorch/pull/192053), [#192054](https://github.com/pytorch/pytorch/pull/192054))
- Reuse the common Metal Performance Primitives capability helper in Conv3d kernels ([#192807](https://github.com/pytorch/pytorch/pull/192807))
### security
