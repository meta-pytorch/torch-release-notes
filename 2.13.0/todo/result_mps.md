
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
- [MPS] fix multinomial sigsegv error ([#180493](https://github.com/pytorch/pytorch/pull/180493))
- [MPS] Replace sum/nansum/mean ops wth native Metal kernel ([#180709](https://github.com/pytorch/pytorch/pull/180709))
- [MPS] Replace sum/nansum/mean ops wth native Metal kernel ([#180709](https://github.com/pytorch/pytorch/pull/180709))
- [MPS] Private API to get host alias of Metal storage ([#180961](https://github.com/pytorch/pytorch/pull/180961))
- [MPS] put decode kernels in separate files ([#181527](https://github.com/pytorch/pytorch/pull/181527))
- [MPS] Add Metal single-block sort path - Part 1 ([#180714](https://github.com/pytorch/pytorch/pull/180714))
- [MPS] Enhance Col2Im tensor op to avoid .contiguous() call and make corresponding Metal kernel stride-aware  ([#181949](https://github.com/pytorch/pytorch/pull/181949))
- [MPS] is_causal for decode kernels ([#181855](https://github.com/pytorch/pytorch/pull/181855))
- [MPS] add stable sort for single block ([#181736](https://github.com/pytorch/pytorch/pull/181736))
- [MPS] add head dim=256 for decode kernels ([#181852](https://github.com/pytorch/pytorch/pull/181852))
- [MPS] if constexpr replace ([#182140](https://github.com/pytorch/pytorch/pull/182140))
- [MPS] Add ILP variant for binary tensor iterators ([#182155](https://github.com/pytorch/pytorch/pull/182155))
- [MPS] Migrate bernoulli to Metal ([#182210](https://github.com/pytorch/pytorch/pull/182210))
- [MPS] Fuse native_dropout into a single Metal kernel ([#182232](https://github.com/pytorch/pytorch/pull/182232))
- [MPS] Migrate uniform/normal and randint to Metal ([#182386](https://github.com/pytorch/pytorch/pull/182386))
- [MPS] enable gqa in sdpa metal kernels ([#183280](https://github.com/pytorch/pytorch/pull/183280))
- [MPS] Migrate comparison ops (eq/ne/lt/le/gt/ge) from MPSGraph to Metal ([#183019](https://github.com/pytorch/pytorch/pull/183019))
- [MPS] fix fft warning ([#183061](https://github.com/pytorch/pytorch/pull/183061))
- [MPS] support float masks to decode attn kernels ([#183458](https://github.com/pytorch/pytorch/pull/183458))
- [MPS] add im2col validation ([#183593](https://github.com/pytorch/pytorch/pull/183593))
- [MPS] Migrate scatter/gather ops to Metal with async bounds checking ([#184028](https://github.com/pytorch/pytorch/pull/184028))
- [MPS] Validate stride > 0 in pool ops to match CPU behavior ([#184875](https://github.com/pytorch/pytorch/pull/184875))
- [MPS] alert on non deterministic algorithms ([#185061](https://github.com/pytorch/pytorch/pull/185061))
- [MPS] Validate probabilities in bernoulli ([#185065](https://github.com/pytorch/pytorch/pull/185065))
- [MPS] Enable NDHWC+DHWIO fast path for Conv3d on channels_last_3d ([#184612](https://github.com/pytorch/pytorch/pull/184612))
- [MPS] fix bucketization speed ([#185622](https://github.com/pytorch/pytorch/pull/185622))
- [MPS] topk+kth value metal kernels ([#184106](https://github.com/pytorch/pytorch/pull/184106))
- [MPS] make index copy fast ([#185750](https://github.com/pytorch/pytorch/pull/185750))
- [MPS] Support captured buffers in flex attention ([#186215](https://github.com/pytorch/pytorch/pull/186215))
- [MPS] Add lcm Metal kernel ([#186279](https://github.com/pytorch/pytorch/pull/186279))
- [MPS] Implement _assert_async ([#186562](https://github.com/pytorch/pytorch/pull/186562))
- [MPS] clear slot when val is not provided ([#186593](https://github.com/pytorch/pytorch/pull/186593))
- [BE] [MPS] Do not include `_native` headers when not used ([#186456](https://github.com/pytorch/pytorch/pull/186456))
- [BE] Make `IMPSAllocator` inherit form `c10::DeviceAllocator` ([#186748](https://github.com/pytorch/pytorch/pull/186748))
- [MPS] faster norms ([#186076](https://github.com/pytorch/pytorch/pull/186076))
### bug fixes
- [MPS] fix lstm train/eval error ([#180873](https://github.com/pytorch/pytorch/pull/180873))
- [MPS] fix async copy failing ([#181017](https://github.com/pytorch/pytorch/pull/181017))
- [MPS] Workaround  MetalPerformancePrimitives bug for F.linear on M5+ ([#181466](https://github.com/pytorch/pytorch/pull/181466))
- [MPS] fix Macos 26.2->26.3 tests failures ([#181742](https://github.com/pytorch/pytorch/pull/181742))
- [MPS] sdpa causal with attn mask proper error ([#181856](https://github.com/pytorch/pytorch/pull/181856))
- [MPS] Sum sliced reduction fix ([#182688](https://github.com/pytorch/pytorch/pull/182688))
- [MPS] Migrate bitwise ops to TensorIterator infrastructure ([#182839](https://github.com/pytorch/pytorch/pull/182839))
- [MPS] Add input validation to F.fold to match CPU/CUDA behavior ([#182067](https://github.com/pytorch/pytorch/pull/182067))
- [MPS] Fix Metal unary operators behavior on large strided tensors ([#183447](https://github.com/pytorch/pytorch/pull/183447))
- [MPS] Migrate replication pad to metal ([#183065](https://github.com/pytorch/pytorch/pull/183065))
- [MPS] fix nans for relu ([#183571](https://github.com/pytorch/pytorch/pull/183571))
- [MPS] propagate nan for softshrink ([#183710](https://github.com/pytorch/pytorch/pull/183710))
- [MPS] Fix layer_norm_backward silent correctness bug for frozen inputs ([#183893](https://github.com/pytorch/pytorch/pull/183893))
- [MPS] Fix welford reuduction codegen with dynamic shapes ([#184206](https://github.com/pytorch/pytorch/pull/184206))
- [MPS] Fix SDPA vector kernel mask offset for partially broadcast masks ([#184180](https://github.com/pytorch/pytorch/pull/184180))
- [MPS] Fix _amp_foreach_non_finite_check_and_unscale_ zeroing fp16/bf16 grads ([#184286](https://github.com/pytorch/pytorch/pull/184286))
- [MPS] hardsigmoid nan fixes ([#183939](https://github.com/pytorch/pytorch/pull/183939))
- [MPS] fix missing barrier in welford reductions ([#184328](https://github.com/pytorch/pytorch/pull/184328))
- [MPS] Materialize neg bit in copy_kernel_mps ([#184403](https://github.com/pytorch/pytorch/pull/184403))
- [MPS] Fix additive mask scaling in prefill attention ([#184400](https://github.com/pytorch/pytorch/pull/184400))
- [MPS] Fix Inductor undeclared identifier in multi-pass welford reductions ([#184502](https://github.com/pytorch/pytorch/pull/184502))
- [MPS] Handle NaNs properly in cholesky ([#184588](https://github.com/pytorch/pytorch/pull/184588))
- [MPS] Fix sort returning out-of-bounds indices for bool/int-max/NaN inputs ([#184620](https://github.com/pytorch/pytorch/pull/184620))
- [MPS] Fix generator clone ([#185002](https://github.com/pytorch/pytorch/pull/185002))
- [MPS] embedding backward to metal ([#185119](https://github.com/pytorch/pytorch/pull/185119))
- [MPS] Fix LSTM dropout not being applied correctly ([#185351](https://github.com/pytorch/pytorch/pull/185351))
- [MPS] Add complex->bool specialization ([#185938](https://github.com/pytorch/pytorch/pull/185938))
- [MPS] fix attention compilation on nightly ([#186399](https://github.com/pytorch/pytorch/pull/186399))
- [MPS] Return NaN for std/var on empty input ([#184510](https://github.com/pytorch/pytorch/pull/184510))
- [MPS] Don't ignore grad scale and found inf ([#186360](https://github.com/pytorch/pytorch/pull/186360))
- [MPS] Metal cumsum cumprod kernels ([#185609](https://github.com/pytorch/pytorch/pull/185609))
### performance
- [MPS] Fully utilize Philox state in distribution kernels ([#182247](https://github.com/pytorch/pytorch/pull/182247))
- [MPS] 2D dispatch for strided unary kernels ([#185291](https://github.com/pytorch/pytorch/pull/185291))
- [MPS] Templatize Im2Col to regain performance for cases where 32-bit indexing suffices ([#185860](https://github.com/pytorch/pytorch/pull/185860))
### docs
### devs
### Untopiced
- [MPS] GridSampler2D backward ([#179756](https://github.com/pytorch/pytorch/pull/179756))
- [MPS] Support integer inputs to `histc` ([#178624](https://github.com/pytorch/pytorch/pull/178624))
- [MPS] Add complex support to `c10/metal/reduction_utils.h` ([#180708](https://github.com/pytorch/pytorch/pull/180708))
- Replace MPSGraph count_nonzero with custom Metal kernel ([#180725](https://github.com/pytorch/pytorch/pull/180725))
- [MPS] Replace unary VEC4 with generic ILP_PER_THREAD dense kernel ([#181509](https://github.com/pytorch/pytorch/pull/181509))
- [MPS] Prefill attn kernels ([#181575](https://github.com/pytorch/pytorch/pull/181575))
- [MPS] Clear MPSGraphCache in torch.mps.empty_cache() ([#181485](https://github.com/pytorch/pytorch/pull/181485))
- [MPS] Fix typo `MPSGaph` should be `MPSGraph` ([#182047](https://github.com/pytorch/pytorch/pull/182047))
- [MPS] Fix uint32 offset overflow in scatter/gather kernels for strided views crossing 2^32 elements ([#182054](https://github.com/pytorch/pytorch/pull/182054))
- [MPS] cleanup TODO ilp per thread ([#182658](https://github.com/pytorch/pytorch/pull/182658))
- [MPS] Enable and fix large tensor failing tests on MPS ([#182863](https://github.com/pytorch/pytorch/pull/182863))
- [MPS] Enhance Im2Col tensor op to avoid unnecessary .contiguous() call ([#182709](https://github.com/pytorch/pytorch/pull/182709))
- [MPS] Enhance Repeat tensor ops to avoid .contiguous() call on repeat tensor and make Metal shader stride aware instead ([#182718](https://github.com/pytorch/pytorch/pull/182718))
- [Metal] Binary tensor iterator fixes/improvements ([#183055](https://github.com/pytorch/pytorch/pull/183055))
- [MPS] Migrate gelu and gelu_backward to metal ([#181451](https://github.com/pytorch/pytorch/pull/181451))
- [MPS] multi block sort (part 2) ([#182242](https://github.com/pytorch/pytorch/pull/182242))
- [MPS] trace to metal ([#183627](https://github.com/pytorch/pytorch/pull/183627))
- [MPS] Fix fill_ on byte-dtype views with misaligned storage offset ([#183790](https://github.com/pytorch/pytorch/pull/183790))
- [MPS] Migrate amax/amin/aminmax/all/any to Metal ([#180752](https://github.com/pytorch/pytorch/pull/180752))
- [MPS] dropout_p loud not implemented error ([#184126](https://github.com/pytorch/pytorch/pull/184126))
- [MPS] Make deviceCount() implementation consistent with Python to fix at::manual_seed() ([#164571](https://github.com/pytorch/pytorch/pull/164571))
- [MPS] fix not caching of scale ([#184122](https://github.com/pytorch/pytorch/pull/184122))
- [MPS] Add `native_group_norm` Metal implementation ([#183830](https://github.com/pytorch/pytorch/pull/183830))
- [MPS] Fix complex exp family on real axis; use precise::sincos ([#184749](https://github.com/pytorch/pytorch/pull/184749))
- [MPS] Support `out` flavors of unary ops ([#184743](https://github.com/pytorch/pytorch/pull/184743))
- [BE][Ez]: Simplify unary Metal shaders with constant folding ([#184921](https://github.com/pytorch/pytorch/pull/184921))
- [MPS] Add `native_group_norm_backward` Metal implementation ([#184437](https://github.com/pytorch/pytorch/pull/184437))
- [BE] Use `std::clamp` ([#185422](https://github.com/pytorch/pytorch/pull/185422))
- [BE][Ez]: Update unary to use proper precise log functions ([#185381](https://github.com/pytorch/pytorch/pull/185381))
- [MPS] Add `_sample_dirichlet` for MPS ([#185458](https://github.com/pytorch/pytorch/pull/185458))
- [MPS] Flex attention ([#182552](https://github.com/pytorch/pytorch/pull/182552))
- [MPS] Migrate randperm off MPSGraph to Metal ([#182528](https://github.com/pytorch/pytorch/pull/182528))
- Move col2im offset and stride to long to avoid overflows leading to corruption ([#185664](https://github.com/pytorch/pytorch/pull/185664))
- [MPS] Add `_dirichlet_grad` Metal implementation ([#185854](https://github.com/pytorch/pytorch/pull/185854))
- [MPS] Migrate copy-cast ops to Metal ([#184740](https://github.com/pytorch/pytorch/pull/184740))
- [MPS] Enhance LossOps tensor ops to avoid unnecessary .contiguous() calls on grad_output tensor ([#182714](https://github.com/pytorch/pytorch/pull/182714))
- [MPS] Fix fast::tanh overflow to nan ([#186286](https://github.com/pytorch/pytorch/pull/186286))
- [MPS] Enhance HistogramKernel tensor op to avoid unnecessary .contiguous() call ([#181951](https://github.com/pytorch/pytorch/pull/181951))
- [BE][MPS] Bitwise shifts should not be implemented for bool ([#186558](https://github.com/pytorch/pytorch/pull/186558))
- [BE] [MPS] Route multinomial through the shared stub frontend ([#186563](https://github.com/pytorch/pytorch/pull/186563))
- [BE][MPS] Drop dead non-unified-memory handling, error out instead ([#186806](https://github.com/pytorch/pytorch/pull/186806))
### not user facing
- [MPS] Enable `test_reductions.py` with skips ([#179407](https://github.com/pytorch/pytorch/pull/179407))
- Use = default for trivial default ctors ([#180769](https://github.com/pytorch/pytorch/pull/180769))
- [BE] Refactor grid_sampler_3d backward to reuse shared backward helpers ([#180849](https://github.com/pytorch/pytorch/pull/180849))
- [mps] Remove unused autocast bfloat16 check ([#174454](https://github.com/pytorch/pytorch/pull/174454))
- [BE] Use `c10::checked_convert` instead of `safe_downcast` ([#182704](https://github.com/pytorch/pytorch/pull/182704))
- [BE] [MPS] Validate random ops by metadata + stats ([#182881](https://github.com/pytorch/pytorch/pull/182881))
- [MPS][BE] Cleanup _cdist_backward implementation ([#183615](https://github.com/pytorch/pytorch/pull/183615))
- [BE] [MPS] Route _cdist fwd and backward through cdist stubs ([#183635](https://github.com/pytorch/pytorch/pull/183635))
- [MPS] Drop expectedFailureMPS on test_adaptive_pooling_no_suppot_input; add max int-pool test ([#184887](https://github.com/pytorch/pytorch/pull/184887))
- [MPS] fix failing conv test on main ([#185978](https://github.com/pytorch/pytorch/pull/185978))
- [BE] Remove dead code from ScanKernel.metal ([#186264](https://github.com/pytorch/pytorch/pull/186264))
- [BE] Fix Metal compilation warnings ([#186267](https://github.com/pytorch/pytorch/pull/186267))
- [BE][Ez]: Use rvalue overload for stringstream str ([#186552](https://github.com/pytorch/pytorch/pull/186552))
- Cleaning up the 32/64bit offset checks for im2col/col2im ([#186109](https://github.com/pytorch/pytorch/pull/186109))
### security
