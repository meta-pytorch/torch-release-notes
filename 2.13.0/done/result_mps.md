
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
- Add Flex Attention support for MPS ([#182552](https://github.com/pytorch/pytorch/pull/182552), [#186215](https://github.com/pytorch/pytorch/pull/186215))
- Add support for `torch.distributions.Dirichlet` on MPS by adding `_sample_dirichlet` and `_dirichlet_grad` Metal implementations ([#185458](https://github.com/pytorch/pytorch/pull/185458), [#185854](https://github.com/pytorch/pytorch/pull/185854))
- Add `grid_sampler_2d` backward support on MPS ([#179756](https://github.com/pytorch/pytorch/pull/179756))
- Add `lcm` support on MPS via a new Metal kernel ([#186279](https://github.com/pytorch/pytorch/pull/186279))
### improvements
- Migrate many ops from MPSGraph to native Metal kernels for `bernoulli` ([#182210](https://github.com/pytorch/pytorch/pull/182210)), `native_dropout` ([#182232](https://github.com/pytorch/pytorch/pull/182232)), `uniform`/`normal`/`randint` ([#182386](https://github.com/pytorch/pytorch/pull/182386)), `randperm` ([#182528](https://github.com/pytorch/pytorch/pull/182528)), comparison ops eq/ne/lt/le/gt/ge ([#183019](https://github.com/pytorch/pytorch/pull/183019)), bitwise ops ([#182839](https://github.com/pytorch/pytorch/pull/182839)), scatter/gather ([#184028](https://github.com/pytorch/pytorch/pull/184028)), copy-cast ([#184740](https://github.com/pytorch/pytorch/pull/184740)), gelu/gelu_backward ([#181451](https://github.com/pytorch/pytorch/pull/181451)), replication pad ([#183065](https://github.com/pytorch/pytorch/pull/183065)), embedding backward ([#185119](https://github.com/pytorch/pytorch/pull/185119)), `trace` ([#183627](https://github.com/pytorch/pytorch/pull/183627)), `count_nonzero` ([#180725](https://github.com/pytorch/pytorch/pull/180725)), amax/amin/aminmax/all/any ([#180752](https://github.com/pytorch/pytorch/pull/180752)), and cumsum/cumprod ([#185609](https://github.com/pytorch/pytorch/pull/185609))
- Add `native_group_norm` and `native_group_norm_backward` Metal implementations ([#183830](https://github.com/pytorch/pytorch/pull/183830), [#184437](https://github.com/pytorch/pytorch/pull/184437))
- Add `topk` and `kthvalue` Metal kernels ([#184106](https://github.com/pytorch/pytorch/pull/184106))
- Add Metal single-block and multi-block sort, including a stable sort path ([#180714](https://github.com/pytorch/pytorch/pull/180714), [#182242](https://github.com/pytorch/pytorch/pull/182242), [#181736](https://github.com/pytorch/pytorch/pull/181736))
- Add complex support to `c10/metal/reduction_utils.h` ([#180708](https://github.com/pytorch/pytorch/pull/180708)) and a complex->bool specialization ([#185938](https://github.com/pytorch/pytorch/pull/185938))
- Support integer inputs to `histc` ([#178624](https://github.com/pytorch/pytorch/pull/178624))
- Support `out` variants of unary ops ([#184743](https://github.com/pytorch/pytorch/pull/184743))
- Improvements to SDPA Metal kernels: prefill attention kernels ([#181575](https://github.com/pytorch/pytorch/pull/181575)), GQA support ([#183280](https://github.com/pytorch/pytorch/pull/183280)), `is_causal` support ([#181855](https://github.com/pytorch/pytorch/pull/181855)), head dim 256 ([#181852](https://github.com/pytorch/pytorch/pull/181852)), float mask support ([#183458](https://github.com/pytorch/pytorch/pull/183458)), and a clearer error for causal + attn mask ([#181856](https://github.com/pytorch/pytorch/pull/181856))
- Add an ILP variant for binary tensor iterators and replace unary VEC4 with a generic ILP-per-thread dense kernel ([#182155](https://github.com/pytorch/pytorch/pull/182155), [#181509](https://github.com/pytorch/pytorch/pull/181509), [#183055](https://github.com/pytorch/pytorch/pull/183055))
- Make several Metal kernels stride-aware to avoid unnecessary `.contiguous()` calls: Col2Im ([#181949](https://github.com/pytorch/pytorch/pull/181949)), Im2Col ([#182709](https://github.com/pytorch/pytorch/pull/182709)), Repeat ([#182718](https://github.com/pytorch/pytorch/pull/182718)), LossOps ([#182714](https://github.com/pytorch/pytorch/pull/182714)), and HistogramKernel ([#181951](https://github.com/pytorch/pytorch/pull/181951))
- Enable NDHWC+DHWIO fast path for `Conv3d` on `channels_last_3d` ([#184612](https://github.com/pytorch/pytorch/pull/184612))
- Clear the MPSGraph cache in `torch.mps.empty_cache()` ([#181485](https://github.com/pytorch/pytorch/pull/181485))
- Add a private API to get the host alias of Metal storage ([#180961](https://github.com/pytorch/pytorch/pull/180961))
- Add input validation: `stride > 0` in pool ops ([#184875](https://github.com/pytorch/pytorch/pull/184875)), `F.fold` ([#182067](https://github.com/pytorch/pytorch/pull/182067)), im2col ([#183593](https://github.com/pytorch/pytorch/pull/183593)), and bernoulli probabilities ([#185065](https://github.com/pytorch/pytorch/pull/185065))
- Alert on non-deterministic algorithms on MPS ([#185061](https://github.com/pytorch/pytorch/pull/185061))
- Raise a clear not-implemented error for `dropout_p` ([#184126](https://github.com/pytorch/pytorch/pull/184126))
- Use proper precise log functions in unary kernels ([#185381](https://github.com/pytorch/pytorch/pull/185381))
### bug fixes
- Fix LSTM train/eval error ([#180873](https://github.com/pytorch/pytorch/pull/180873)) and LSTM dropout not being applied correctly ([#185351](https://github.com/pytorch/pytorch/pull/185351))
- Fix `multinomial` SIGSEGV ([#180493](https://github.com/pytorch/pytorch/pull/180493))
- Fix async copy failing ([#181017](https://github.com/pytorch/pytorch/pull/181017))
- Work around a MetalPerformancePrimitives bug for `F.linear` on M5+ ([#181466](https://github.com/pytorch/pytorch/pull/181466))
- Fix sliced sum reduction ([#182688](https://github.com/pytorch/pytorch/pull/182688)) and Metal unary operator behavior on large strided tensors ([#183447](https://github.com/pytorch/pytorch/pull/183447))
- Fix uint32 offset overflow in scatter/gather kernels for strided views crossing 2^32 elements ([#182054](https://github.com/pytorch/pytorch/pull/182054)) and move col2im offset/stride to long to avoid overflow corruption ([#185664](https://github.com/pytorch/pytorch/pull/185664))
- Fix NaN handling: `relu` ([#183571](https://github.com/pytorch/pytorch/pull/183571)), `softshrink` ([#183710](https://github.com/pytorch/pytorch/pull/183710)), `hardsigmoid` ([#183939](https://github.com/pytorch/pytorch/pull/183939)), `cholesky` ([#184588](https://github.com/pytorch/pytorch/pull/184588)), and `fast::tanh` overflow ([#186286](https://github.com/pytorch/pytorch/pull/186286)); return NaN for std/var on empty input ([#184510](https://github.com/pytorch/pytorch/pull/184510))
- Fix `layer_norm_backward` silent correctness bug for frozen inputs ([#183893](https://github.com/pytorch/pytorch/pull/183893))
- Fix Welford reduction codegen with dynamic shapes ([#184206](https://github.com/pytorch/pytorch/pull/184206)), a missing barrier in Welford reductions ([#184328](https://github.com/pytorch/pytorch/pull/184328)), and an Inductor undeclared identifier in multi-pass Welford reductions ([#184502](https://github.com/pytorch/pytorch/pull/184502))
- Fix SDPA vector kernel mask offset for partially broadcast masks ([#184180](https://github.com/pytorch/pytorch/pull/184180)) and additive mask scaling in prefill attention ([#184400](https://github.com/pytorch/pytorch/pull/184400))
- Fix `_amp_foreach_non_finite_check_and_unscale_` zeroing fp16/bf16 grads ([#184286](https://github.com/pytorch/pytorch/pull/184286)) and stop ignoring grad scale and found_inf ([#186360](https://github.com/pytorch/pytorch/pull/186360))
- Materialize neg bit in `copy_kernel_mps` ([#184403](https://github.com/pytorch/pytorch/pull/184403))
- Fix `sort` returning out-of-bounds indices for bool/int-max/NaN inputs ([#184620](https://github.com/pytorch/pytorch/pull/184620))
- Fix generator clone ([#185002](https://github.com/pytorch/pytorch/pull/185002))
- Fix `fill_` on byte-dtype views with misaligned storage offset ([#183790](https://github.com/pytorch/pytorch/pull/183790))
- Fix complex exp family on the real axis using `precise::sincos` ([#184749](https://github.com/pytorch/pytorch/pull/184749))
- Make `deviceCount()` consistent with Python to fix `at::manual_seed()` ([#164571](https://github.com/pytorch/pytorch/pull/164571))
- Fix `scale` not being cached ([#184122](https://github.com/pytorch/pytorch/pull/184122))
- Fix attention compilation on nightly ([#186399](https://github.com/pytorch/pytorch/pull/186399))
- Fix the FFT warning ([#183061](https://github.com/pytorch/pytorch/pull/183061))
- Disallow bitwise shifts for bool dtype ([#186558](https://github.com/pytorch/pytorch/pull/186558))
- Fix bucketization speed/correctness ([#185622](https://github.com/pytorch/pytorch/pull/185622))
- Make index copy fast ([#185750](https://github.com/pytorch/pytorch/pull/185750))
- Enable and fix large-tensor tests on MPS ([#182863](https://github.com/pytorch/pytorch/pull/182863))
### performance
- Fully utilize Philox state in distribution kernels ([#182247](https://github.com/pytorch/pytorch/pull/182247))
- 2D dispatch for strided unary kernels ([#185291](https://github.com/pytorch/pytorch/pull/185291))
- Templatize Im2Col to regain performance when 32-bit indexing suffices ([#185860](https://github.com/pytorch/pytorch/pull/185860))
- Faster norms ([#186076](https://github.com/pytorch/pytorch/pull/186076))
### docs
### devs
### not user facing
- Fix MacOS 26.2->26.3 test failures ([#181742](https://github.com/pytorch/pytorch/pull/181742))
- Enable `test_reductions.py` with skips ([#179407](https://github.com/pytorch/pytorch/pull/179407))
- Use `= default` for trivial default ctors ([#180769](https://github.com/pytorch/pytorch/pull/180769))
- Refactor `grid_sampler_3d` backward to reuse shared backward helpers ([#180849](https://github.com/pytorch/pytorch/pull/180849))
- Remove unused autocast bfloat16 check ([#174454](https://github.com/pytorch/pytorch/pull/174454))
- Use `c10::checked_convert` instead of `safe_downcast` ([#182704](https://github.com/pytorch/pytorch/pull/182704))
- Validate random ops by metadata + stats ([#182881](https://github.com/pytorch/pytorch/pull/182881))
- Cleanup `_cdist_backward` implementation and route `_cdist` fwd/backward through cdist stubs ([#183615](https://github.com/pytorch/pytorch/pull/183615), [#183635](https://github.com/pytorch/pytorch/pull/183635))
- Drop `expectedFailureMPS` on `test_adaptive_pooling_no_suppot_input`; add max int-pool test ([#184887](https://github.com/pytorch/pytorch/pull/184887))
- Fix failing conv test on main ([#185978](https://github.com/pytorch/pytorch/pull/185978))
- Remove dead code from `ScanKernel.metal` ([#186264](https://github.com/pytorch/pytorch/pull/186264))
- Fix Metal compilation warnings ([#186267](https://github.com/pytorch/pytorch/pull/186267))
- Use rvalue overload for stringstream str ([#186552](https://github.com/pytorch/pytorch/pull/186552))
- Clean up the 32/64bit offset checks for im2col/col2im ([#186109](https://github.com/pytorch/pytorch/pull/186109))
- Fix typo `MPSGaph` -> `MPSGraph` ([#182047](https://github.com/pytorch/pytorch/pull/182047))
- Clean up TODO for ilp per thread ([#182658](https://github.com/pytorch/pytorch/pull/182658))
- Simplify unary Metal shaders with constant folding ([#184921](https://github.com/pytorch/pytorch/pull/184921))
- Use `std::clamp` ([#185422](https://github.com/pytorch/pytorch/pull/185422))
- Put decode kernels in separate files ([#181527](https://github.com/pytorch/pytorch/pull/181527))
- `if constexpr` replace ([#182140](https://github.com/pytorch/pytorch/pull/182140))
- Do not include `_native` headers when not used ([#186456](https://github.com/pytorch/pytorch/pull/186456))
- Make `IMPSAllocator` inherit from `c10::DeviceAllocator` ([#186748](https://github.com/pytorch/pytorch/pull/186748))
- Clear slot when val is not provided ([#186593](https://github.com/pytorch/pytorch/pull/186593))
- Route `multinomial` through the shared stub frontend ([#186563](https://github.com/pytorch/pytorch/pull/186563))
- Drop dead non-unified-memory handling, error out instead ([#186806](https://github.com/pytorch/pytorch/pull/186806))
### security
