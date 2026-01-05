
# Release Notes worksheet inductor

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.
* Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

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

## inductor
### bc breaking
### deprecation
### new features
- Add experimental Pallas TorchInductor backend. ([#166822](https://github.com/pytorch/pytorch/pull/166822))
- Add Pallas TPU backend support. ([#167774](https://github.com/pytorch/pytorch/pull/167774))
- Add Flash Attention support to FlexAttention. ([#161118](https://github.com/pytorch/pytorch/pull/161118))
- Add deterministic mode for Inductor compilation. ([#163589](https://github.com/pytorch/pytorch/pull/163589)) ([#165950](https://github.com/pytorch/pytorch/pull/165950)) ([#164532](https://github.com/pytorch/pytorch/pull/164532))
- Enable custom op autotune decompositions and parameter tuning. ([#164212](https://github.com/pytorch/pytorch/pull/164212))  ([#167193](https://github.com/pytorch/pytorch/pull/167193))
- Expose `torch.compiler.config.force_disable_caches` as a public API. ([#166699](https://github.com/pytorch/pytorch/pull/166699))
- Add HOP for additional control dependencies to enforce explicit scheduling. ([#164568](https://github.com/pytorch/pytorch/pull/164568))

### improvements
- Pruned failed compilations from Autotuning candidates ([#162673](https://github.com/pytorch/pytorch/pull/162673))
- Extend triton_mm auto-tune options for HIM shapes ([#163273](https://github.com/pytorch/pytorch/pull/163273))
- Various fixes for AOTI-FX backend
    - Solve for undefined symbols in dynamic input shapes ([#163044](https://github.com/pytorch/pytorch/pull/163044))
    - Support symbol and dynamic scalar graph inputs and outputs ([#163596](https://github.com/pytorch/pytorch/pull/163596))
    - Support unbacked symbol definitions ([#163729](https://github.com/pytorch/pytorch/pull/163729))
    - Generalize FloorDiv conversion to handle more complex launch grids. ([#163828](https://github.com/pytorch/pytorch/pull/163828))
    - Don't flatten constant args ([#166144](https://github.com/pytorch/pytorch/pull/166144))
    - Support SymInt placeholder([#167757](https://github.com/pytorch/pytorch/pull/167757))
    - Support torch.cond ([#163234](https://github.com/pytorch/pytorch/pull/163234))
- Add tanh, exp, and sigmoid activations for Cutlass backend. ([#162535](https://github.com/pytorch/pytorch/pull/162535)) ([#162536](https://github.com/pytorch/pytorch/pull/162536))
- Hardened the experimental horizontal fusion `torch._inductor.config.combo_kernels` ([#162442](https://github.com/pytorch/pytorch/pull/162442)) ([#166274](https://github.com/pytorch/pytorch/pull/166274)) ([#162759](https://github.com/pytorch/pytorch/pull/162759)) ([#167781](https://github.com/pytorch/pytorch/pull/167781)) ([#168127](https://github.com/pytorch/pytorch/pull/168127)) ([#168946](https://github.com/pytorch/pytorch/pull/168946)) ([#168109](https://github.com/pytorch/pytorch/pull/168109)) ([#164918](https://github.com/pytorch/pytorch/pull/164918))
- Enable TMA store for TMA matmul templates on Triton. ([#160480](https://github.com/pytorch/pytorch/pull/160480))
- Add Blackwell GPU templates (persistent matmul, FP8 scaled persistent + TMA GEMMs, CuTeDSL grouped GEMM, FlexFlash forward, FlexAttention configs). ([#162916](https://github.com/pytorch/pytorch/pull/162916)) ([#163147](https://github.com/pytorch/pytorch/pull/163147)) ([#167340](https://github.com/pytorch/pytorch/pull/167340)) ([#167040](https://github.com/pytorch/pytorch/pull/167040)) ([#165760](https://github.com/pytorch/pytorch/pull/165760))
- Support `qconv_pointwise.tensor` and `qconv2d_pointwise.binary_tensor` quantized operations. ([#166608](https://github.com/pytorch/pytorch/pull/166608))
- Support `out_dtype` argument for matmul operations. ([#163393](https://github.com/pytorch/pytorch/pull/163393))
- Add support for bound methods in pattern matcher. ([#167795](https://github.com/pytorch/pytorch/pull/167795))
- Add way to register custom rules for graph partitioning. ([#166458](https://github.com/pytorch/pytorch/pull/166458)) ([#163310](https://github.com/pytorch/pytorch/pull/163310))
- Add codegen support for `fast_tanhf` on ROCm. ([#162052](https://github.com/pytorch/pytorch/pull/162052))
- Support deepseek-style FP8 scaling in Inductor. ([#164404](https://github.com/pytorch/pytorch/pull/164404))
- Enable int64 indexing in convolution and matmul templates. ([#162506](https://github.com/pytorch/pytorch/pull/162506))
- Add SDPA patterns for T5 variants when batch size is 1. ([#163252](https://github.com/pytorch/pytorch/pull/163252))
- Add mechanism to get optimal autotune decision for FlexAttention. ([#165817](https://github.com/pytorch/pytorch/pull/165817))
- Add fallback config `fallback_embedding_bag_byte_unpack`. ([#163803](https://github.com/pytorch/pytorch/pull/163803))
- Expose config for FX bucket all_reduces. ([#167634](https://github.com/pytorch/pytorch/pull/167634))
- Add in-kernel NaN check support. ([#166008](https://github.com/pytorch/pytorch/pull/166008))
- Enable `pad_mm` and `decompose_mm_pass` pass on Intel GPU. ([#166618](https://github.com/pytorch/pytorch/pull/166618))  ([#166613](https://github.com/pytorch/pytorch/pull/166613))
- Improve CUDA support for int8pack_mm weight-only quantization pattern. ([#161680](https://github.com/pytorch/pytorch/pull/161680)) ([#161848](https://github.com/pytorch/pytorch/pull/161848)) ([#163461](https://github.com/pytorch/pytorch/pull/163461))
- Improve heuristics for pointwise kernels on ROCm. ([#163197](https://github.com/pytorch/pytorch/pull/163197))
- Enable mix-order reduction fusion earlier and allow fusing more nodes. ([#168209](https://github.com/pytorch/pytorch/pull/168209))
- Make mix order reduction work with dynamic shapes ([#168117](https://github.com/pytorch/pytorch/pull/168117))
- Better use of memory tracking ([#168121](https://github.com/pytorch/pytorch/pull/168121))
- Turn on LOAF (for OSS) by default. ([#162030](https://github.com/pytorch/pytorch/pull/162030))
- Log kernel autotuning results to CSV. ([#164191](https://github.com/pytorch/pytorch/pull/164191))
- Add warning for CUDA graph re-recording from dynamic shapes. ([#162696](https://github.com/pytorch/pytorch/pull/162696))
- Quiesce triton compile workers by default. ([#169485](https://github.com/pytorch/pytorch/pull/169485))
- Support masked vectorization for tail loops with integer and bool datatypes. ([#165885](https://github.com/pytorch/pytorch/pull/165885))
- Support tile-wise (1x128) FP8 scaling in Inductor. ([#165132](https://github.com/pytorch/pytorch/pull/165132))
- Support fallback for all GEMM-like operations. ([#165755](https://github.com/pytorch/pytorch/pull/165755))
- Enable Triton kernels with unbacked inputs. ([#164509](https://github.com/pytorch/pytorch/pull/164509))
- Add AVX512-VNNI-based micro kernel for CPU GEMM template. ([#166846](https://github.com/pytorch/pytorch/pull/166846))
- Support mixed dtype in `native_layer_norm_backward` meta function. ([#159830](https://github.com/pytorch/pytorch/pull/159830))
- Add tech specs for MI350 GPU. ([#166576](https://github.com/pytorch/pytorch/pull/166576))
- Add `assume_32bit_indexing` inductor config option. ([#167784](https://github.com/pytorch/pytorch/pull/167784))
- Wire up mask_mod and blockmask to FlexFlash implementation. ([#166359](https://github.com/pytorch/pytorch/pull/166359))
- More aggressive mix order reduction for better fusion. ([#166382](https://github.com/pytorch/pytorch/pull/166382))
- Mix order reduction heuristics and tuning. ([#166585](https://github.com/pytorch/pytorch/pull/166585))

### bug fixes
- Fix some edge cases ([#162295](https://github.com/pytorch/pytorch/pull/162295))
- Fix TMA transpose logic to handle 1D shapes + string differences ([#163966](https://github.com/pytorch/pytorch/pull/163966))
- fix flex attention eager: dont round down scores to low-precision (closes #163588) ([#163986](https://github.com/pytorch/pytorch/pull/163986))
- Fix a condition error in torch/_inductor/codegen/debug_utils.py ([#165033](https://github.com/pytorch/pytorch/pull/165033))
- Thread deterministic config vars to subproc compilation ([#165729](https://github.com/pytorch/pytorch/pull/165729))
- Fix identity expansion. ([#165066](https://github.com/pytorch/pytorch/pull/165066))
- Fix FP8 activation quantization for duplicate forward outputs. ([#163364](https://github.com/pytorch/pytorch/pull/163364))
- Fix decomposition issues (`repeat_interleave` out-of-bounds indices, `divmod` error, `alpha`/`beta` handling). ([#165368](https://github.com/pytorch/pytorch/pull/165368)) ([#163482](https://github.com/pytorch/pytorch/pull/163482)) ([#167317](https://github.com/pytorch/pytorch/pull/167317))
- Fix dynamic shaped heads check in FlexFlash. ([#165866](https://github.com/pytorch/pytorch/pull/165866))
- Fix `argmin`/`argmax` returning incorrect indices for non-contiguous tensors. ([#165983](https://github.com/pytorch/pytorch/pull/165983))
- Fix unbacked float symbol handling in kernel codegen. ([#166890](https://github.com/pytorch/pytorch/pull/166890))
- Fix `static_input_indices` subclass remapping under training. ([#167127](https://github.com/pytorch/pytorch/pull/167127))
- Fix `torch.cond` HOP device handling in inductor. ([#167354](https://github.com/pytorch/pytorch/pull/167354))
- Fix `CppTile2DKernel` for FP8 datatype. ([#167451](https://github.com/pytorch/pytorch/pull/167451))
- Fix user-defined Triton kernel output with `.cpu()` correctness issue. ([#168281](https://github.com/pytorch/pytorch/pull/168281))
- Fix viewed outputs getting padded incorrectly. ([#163398](https://github.com/pytorch/pytorch/pull/163398))
- Fix lowering issues (`as_strided` with `.view(dtype)` inputs, symbolic shapes in FlexAttention, `sym_size_`/`sym_stride`). ([#163319](https://github.com/pytorch/pytorch/pull/163319)) ([#168383](https://github.com/pytorch/pytorch/pull/168383)) ([#167565](https://github.com/pytorch/pytorch/pull/167565))
- Fix error from custom CUDA allocators. ([#163422](https://github.com/pytorch/pytorch/pull/163422))
- Fix `copy_` for scalar in inductor. ([#164167](https://github.com/pytorch/pytorch/pull/164167))
- Fix bug with serialization after AOTAutogradCache hit. ([#165474](https://github.com/pytorch/pytorch/pull/165474))
- Fix `searchsorted` for non-dense tensors. ([#165064](https://github.com/pytorch/pytorch/pull/165064))
- Fix constant folder issues. ([#166655](https://github.com/pytorch/pytorch/pull/166655))
- Fix constant creation issues. ([#167398](https://github.com/pytorch/pytorch/pull/167398))
- Fix picking wrong contiguous node. ([#168371](https://github.com/pytorch/pytorch/pull/168371))
- Fix inner reduction decision logic. ([#168391](https://github.com/pytorch/pytorch/pull/168391))
- Fix device determination logic in Conditional. ([#169199](https://github.com/pytorch/pytorch/pull/169199))
- Fix pattern matcher `FailedMatch` format string. ([#169611](https://github.com/pytorch/pytorch/pull/169611))
- Fix SyntaxError from truncated Unicode escape in Windows compile-time auto-tuning block. ([#169286](https://github.com/pytorch/pytorch/pull/169286))
- Optimize sum reduction heuristics. ([#163144](https://github.com/pytorch/pytorch/pull/163144))
- Optimize scalar `welford_reduce`. ([#162709](https://github.com/pytorch/pytorch/pull/162709))
- Disable mixed-order reduction for cpp-wrapper. ([#169859](https://github.com/pytorch/pytorch/pull/169859))
- Capture Triton timeout errors without crashing the job. ([#169064](https://github.com/pytorch/pytorch/pull/169064))
- Correctly set `max_numwarps` in coordinate descent tuner. ([#159146](https://github.com/pytorch/pytorch/pull/159146))
- Fix Triton `group_m` config. ([#169514](https://github.com/pytorch/pytorch/pull/169514))
- Fix convolution autotune check when `groups != 1`. ([#163094](https://github.com/pytorch/pytorch/pull/163094))
- Fix constant shape for float constants. ([#164241](https://github.com/pytorch/pytorch/pull/164241))
- Fix Diode/exhaustive autotune crash on AMD. ([#169225](https://github.com/pytorch/pytorch/pull/169225))
- Fix `get_raw_stream` undefined error. ([#163707](https://github.com/pytorch/pytorch/pull/163707))
- Fix runtime error in context on cpu-only machine when compile for GPU. ([#165220](https://github.com/pytorch/pytorch/pull/165220))
- Fix AMD CPU max-autotune breakage. ([#168079](https://github.com/pytorch/pytorch/pull/168079))
- Fix bad merge duplicate pre pass. ([#165917](https://github.com/pytorch/pytorch/pull/165917))
- Fix layout constraint for `weight_norm` backward. ([#167667](https://github.com/pytorch/pytorch/pull/167667))
- Fix cross-process group overlap. ([#169384](https://github.com/pytorch/pytorch/pull/169384))
- Fix WeakDeps (WAR deps) handling during fusion. ([#162316](https://github.com/pytorch/pytorch/pull/162316))
- Fix unbacked replacement where LHS is purely backed expr and RHS is unbacked expr. ([#164013](https://github.com/pytorch/pytorch/pull/164013))
- Fix stride rounding on Blockwise128x128 to accommodate for small shapes. ([#164953](https://github.com/pytorch/pytorch/pull/164953))
- Fix loop pipelining for 2D/2D case of Triton grouped MM. ([#165265](https://github.com/pytorch/pytorch/pull/165265))
- Fix persistent rblock statically_known_leq error cases. ([#165657](https://github.com/pytorch/pytorch/pull/165657))

### performance
- Naive foreach autotune support ([#162053](https://github.com/pytorch/pytorch/pull/162053))
- Invert unary read and write for better fusion. ([#161404](https://github.com/pytorch/pytorch/pull/161404))
- Generate fused RMS/layer norm backward. ([#165370](https://github.com/pytorch/pytorch/pull/165370))
- Optimize cold compile time when cudagraphs-partition is enabled. ([#167132](https://github.com/pytorch/pytorch/pull/167132))
- Reduce cold compilation time caused by duplicated user-defined Triton kernels. ([#168292](https://github.com/pytorch/pytorch/pull/168292))
- Optimize identity permute in `empty_permuted` decomposition. ([#169731](https://github.com/pytorch/pytorch/pull/169731))
- Properly enlarge XBLOCK/set num_warps=1 for B200 inner persistent reductions. ([#168335](https://github.com/pytorch/pytorch/pull/168335))
- Improved heuristic for operator reordering for peak memory. ([#161810](https://github.com/pytorch/pytorch/pull/161810))
- Add more configs for pointwise kernels on ROCm. ([#166470](https://github.com/pytorch/pytorch/pull/166470))
- Improve A16W8 performance for CPU GEMM template. ([#162479](https://github.com/pytorch/pytorch/pull/162479))
- Make mix-order-reduction split size not depends on split-reduction heuristics ([#166461](https://github.com/pytorch/pytorch/pull/166461))
- Less aggressive persistent reduction when it could induce large masking with dynamic shapes. ([#163365](https://github.com/pytorch/pytorch/pull/163365))

### docs
- Updated documentation for `tlparse` ([#171339](https://github.com/pytorch/pytorch/pull/171339))  ([#162975](https://github.com/pytorch/pytorch/pull/162975)). `tlparse` is a compilation report tool that processes `TORCH_TRACE` logs to generate interactive HTML reports showing how your model was compiled. When reporting bugs to PyTorch developers, we encourage you to  attach the trace log or `tlparse` output to provide critical debugging information to help us bisect the issue.
- Update FlexConfig documentation. ([#162533](https://github.com/pytorch/pytorch/pull/162533))
### devs
- Add API for scheduling overlap from inductor configs. ([#169693](https://github.com/pytorch/pytorch/pull/169693))
- Make `LOCK_TIMEOUT` in codecache configurable. ([#165030](https://github.com/pytorch/pytorch/pull/165030))
- Add debug output for specific pattern matching. ([#169603](https://github.com/pytorch/pytorch/pull/169603))
- Add overridable env var for disabling FX graph cache. ([#166138](https://github.com/pytorch/pytorch/pull/166138))
- Add subsystem support to pattern matcher. ([#163922](https://github.com/pytorch/pytorch/pull/163922))
- Add pre-grad graph bisecting support. ([#166344](https://github.com/pytorch/pytorch/pull/166344))
- Decouple flags for optimization and debug symbols. ([#167385](https://github.com/pytorch/pytorch/pull/167385)) ([#167575](https://github.com/pytorch/pytorch/pull/167575))
- Introduce HOP for inductor compiled regions to allow torch dispatch. ([#167844](https://github.com/pytorch/pytorch/pull/167844))

### Untopiced
### not user facing
- Use upper bound for persistent rblock ([#162441](https://github.com/pytorch/pytorch/pull/162441))
- Do loop reordering in a separate final round ([#162355](https://github.com/pytorch/pytorch/pull/162355))
- In emulate_precision_casts, disable fma fusion in triton ([#163073](https://github.com/pytorch/pytorch/pull/163073))
- Enable Epilogue Subtiling in the blackwell ws template ([#163145](https://github.com/pytorch/pytorch/pull/163145))
- Refactor memory estimator to use node storages, add test ([#164783](https://github.com/pytorch/pytorch/pull/164783))
- Add reduction tag to 98 reduction operator variants across 21 operator families. ([#165155](https://github.com/pytorch/pytorch/pull/165155))
- Don't tune xblock for reduction ([#164801](https://github.com/pytorch/pytorch/pull/164801))
- Only generate compile-time auto-tuning block in the main graph ([#167131](https://github.com/pytorch/pytorch/pull/167131))
- Allow add_persistent_r_block to scale up rblock up to a limit ([#162296](https://github.com/pytorch/pytorch/pull/162296))
- Use reduction hint for aggressive rblock ([#163371](https://github.com/pytorch/pytorch/pull/163371))

### security
