
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
- [BE][MPS] Remove MacOS-14 workarounds ([#199261](https://github.com/pytorch/pytorch/pull/199261))
### deprecation
### new features
### improvements
- [MPS] Add logspace.out ([#190495](https://github.com/pytorch/pytorch/pull/190495))
- [MPS] Implement put_ and take ([#192980](https://github.com/pytorch/pytorch/pull/192980))
- [MPS] Migrate isposinf and isneginf to Metal kernels ([#189548](https://github.com/pytorch/pytorch/pull/189548))
- [MPS] Add Metal kernel for conv3d DHWIO weight permute ([#193167](https://github.com/pytorch/pytorch/pull/193167))
- [MPS] Fix conv2d backward channels_last performance ([#193623](https://github.com/pytorch/pytorch/pull/193623))
- [MPS] Migrate flip to metal kernels ([#193826](https://github.com/pytorch/pytorch/pull/193826))
- [MPS] enable masked_fill fast path for scalar boolean indexing ([#195020](https://github.com/pytorch/pytorch/pull/195020))
- [MPS] route dropout through the fused kernel ([#195011](https://github.com/pytorch/pytorch/pull/195011))
- [MPS] Migrate nll_loss backward from MPSGraph to a Metal kernel ([#195153](https://github.com/pytorch/pytorch/pull/195153))
- [MPS] Add special_laguerre_polynomial_l ([#195225](https://github.com/pytorch/pytorch/pull/195225))
- [MPS] Add complex64 support to linalg.lu_solve ([#195369](https://github.com/pytorch/pytorch/pull/195369))
- [MPS] Migrate constant pad to metal ([#195368](https://github.com/pytorch/pytorch/pull/195368))
- [MPS] Migrate logit_backward and tanh_backward to Metal ([#195601](https://github.com/pytorch/pytorch/pull/195601))
- [MPS] migrate log softmax to metal ([#195441](https://github.com/pytorch/pytorch/pull/195441))
- [MPS] Remove GPU<->CPU sync in histc ([#196016](https://github.com/pytorch/pytorch/pull/196016))
- [MPS] Remove svd_kernel_mps small-input CPU gate ([#195950](https://github.com/pytorch/pytorch/pull/195950))
- [MPS] Solve triangular systems by blocks, drop MPSMatrixSolveTriangular ([#196241](https://github.com/pytorch/pytorch/pull/196241))
- [MPS] Migrate softmax to metal kernels ([#196071](https://github.com/pytorch/pytorch/pull/196071))
- [MPS] Add float8_e4m3fn dtype support ([#194074](https://github.com/pytorch/pytorch/pull/194074))
- [MPS] Introduce `PYTORCH_MPS_METAL_VERSION` ([#196881](https://github.com/pytorch/pytorch/pull/196881))
- [MPS] Add float8_e4m3fn support to eye ([#196915](https://github.com/pytorch/pytorch/pull/196915))
- [MPS] add fp8_e4m3 gather ([#196918](https://github.com/pytorch/pytorch/pull/196918))
- [MPS] add fp8_e4m3 cat ([#196945](https://github.com/pytorch/pytorch/pull/196945))
- [MPS] Add metal scatter kernel instantiation for fp8 dtype for fp8_e4m3 ([#196955](https://github.com/pytorch/pytorch/pull/196955))
- [MPSInductor] Add some of the missing ops in mps inductor ([#197403](https://github.com/pytorch/pytorch/pull/197403))
- [MPS] Add float8_e4m3fn support to item() ([#197383](https://github.com/pytorch/pytorch/pull/197383))
- [MPS] optimize small batched triangular solves ([#196900](https://github.com/pytorch/pytorch/pull/196900))
- [MPS] Add constant pad for fp8_e4m3 dtype ([#197801](https://github.com/pytorch/pytorch/pull/197801))
- [MPS] Use atomic counters for histc ([#192164](https://github.com/pytorch/pytorch/pull/192164))
- [MPS] Add heaviside ([#195265](https://github.com/pytorch/pytorch/pull/195265))
- [BE] Refactor reductions on MPS ([#198494](https://github.com/pytorch/pytorch/pull/198494))
- [MPS] Port std/var to the shared reduction kernels ([#198495](https://github.com/pytorch/pytorch/pull/198495))
- [MPS] Use atomic counters for histogram/histogramdd and drop the eps slack ([#198416](https://github.com/pytorch/pytorch/pull/198416))
- [MPS] Port norm to the shared reduction kernels ([#198611](https://github.com/pytorch/pytorch/pull/198611))
- [MPS] Improve adjacent dim reduction ([#198635](https://github.com/pytorch/pytorch/pull/198635))
- [MPS] migrate where to metal ([#198719](https://github.com/pytorch/pytorch/pull/198719))
- [MPS] Add unsigned integer support to comparison ops ([#198860](https://github.com/pytorch/pytorch/pull/198860))
- [MPS] Add register-resident Metal kernels for small-matrix inverse ([#195944](https://github.com/pytorch/pytorch/pull/195944))
- [MPS] Add unsigned integer support to comparison ops ([#198860](https://github.com/pytorch/pytorch/pull/198860))
- [MPS] Capture command buffer execution errors instead of ignoring them ([#198883](https://github.com/pytorch/pytorch/pull/198883))
- [MPS] prod to metal ([#198688](https://github.com/pytorch/pytorch/pull/198688))
- [MPS] grouped mm gemvs ([#198725](https://github.com/pytorch/pytorch/pull/198725))
- [MPS] Sort floats on integer keys in single-block sort/topk ([#198960](https://github.com/pytorch/pytorch/pull/198960))
- [MPS] Enable gemv kernels for linear ([#198721](https://github.com/pytorch/pytorch/pull/198721))
- [MPS] conv1d to metal ([#198878](https://github.com/pytorch/pytorch/pull/198878))
- [MPS] Migrate upsample backward to metal ([#199687](https://github.com/pytorch/pytorch/pull/199687))
### bug fixes
- [Fix] DLPack toDLPackNonOwning: handle MPS storage_offset ([#182924](https://github.com/pytorch/pytorch/pull/182924))
- [MPS] Fix beta=0 for empty addbmm and baddbmm ([#193850](https://github.com/pytorch/pytorch/pull/193850))
- [MPS] Raise NotImplementedError for pooling ops that require 64-bit indexing ([#194460](https://github.com/pytorch/pytorch/pull/194460))
- [MPS] Ignore bias in complex `[b]add[b]mm` when beta is 0 ([#194474](https://github.com/pytorch/pytorch/pull/194474))
- [MPS] Fix bool atomic_add on misaligned storage offsets ([#195081](https://github.com/pytorch/pytorch/pull/195081))
- [MPS] Fix complex std/var to return a real result ([#195344](https://github.com/pytorch/pytorch/pull/195344))
- [MPS] Fix nll_loss_backward for 1D (no batch dim) input ([#195411](https://github.com/pytorch/pytorch/pull/195411))
- [BE][MPS] Migrate remaining logical ops to Metal ([#195592](https://github.com/pytorch/pytorch/pull/195592))
- [MPS] Migrate `pow_Tensor_Tensor.out` to Metal ([#195585](https://github.com/pytorch/pytorch/pull/195585))
- [MPS] Fix svd_jacobi Metal compiler crash ([#195949](https://github.com/pytorch/pytorch/pull/195949))
- [MPS] Fix complex SVD on conjugated/column-major input ([#196128](https://github.com/pytorch/pytorch/pull/196128))
- [MPS] Orthonormalize null-space U columns in svd_jacobi ([#196139](https://github.com/pytorch/pytorch/pull/196139))
- [MPS] Add naive triangular_solve for complex numbers ([#195861](https://github.com/pytorch/pytorch/pull/195861))
- [BE] Unify Pooling shape checks across backends / families ([#196230](https://github.com/pytorch/pytorch/pull/196230))
- [MPS] Fix lerp with a mixed-dtype scalar weight ([#196662](https://github.com/pytorch/pytorch/pull/196662))
- [Fix] DLPack toDLPackNonOwning: handle MPS storage_offset ([#182924](https://github.com/pytorch/pytorch/pull/182924))
- [MPS] Raise when a castout kernel is asked to store a dtype Metal cannot represent ([#197722](https://github.com/pytorch/pytorch/pull/197722))
- [MPS] Fix  race conditions in `MetalShaderLibrary` ([#167541](https://github.com/pytorch/pytorch/pull/167541))
- [MPS] Keep stream command-buffer state on the serial queue ([#197836](https://github.com/pytorch/pytorch/pull/197836))
- [MPS] Keep stream command-buffer state on the serial queue ([#197836](https://github.com/pytorch/pytorch/pull/197836))
- [MPS] Support range factories with more than 2^32 elements ([#198593](https://github.com/pytorch/pytorch/pull/198593))
- [MPS] Improve expm1 accuracy near zero ([#198771](https://github.com/pytorch/pytorch/pull/198771))
- [MPS] Fix mixed-dtype batch_norm aborts and accumulate in float ([#198740](https://github.com/pytorch/pytorch/pull/198740))
- [MPS][Inductor] Fix argmax/argmin indices for transposed and sliced inputs ([#199134](https://github.com/pytorch/pytorch/pull/199134))
- [MPS][Inductor] Fix wrong bf16 argmax/argmin indices ([#199132](https://github.com/pytorch/pytorch/pull/199132))
- [MPS] Bind byte-copy and scalar kernel inputs as `device const uchar*` ([#199452](https://github.com/pytorch/pytorch/pull/199452))
- [MPS] Fix SDPA batch and head broadcasting ([#189631](https://github.com/pytorch/pytorch/pull/189631))
- [MPS] Fix linalg.lstsq on empty inputs ([#199694](https://github.com/pytorch/pytorch/pull/199694))
### performance
- [MPS] Speed up strided ternary kernels up to 5x ([#196922](https://github.com/pytorch/pytorch/pull/196922))
### docs
### devs
### Untopiced
- [BE] Removing dead code from MPS (1/5) ([#193730](https://github.com/pytorch/pytorch/pull/193730))
- [BE] Removing dead code from MPS (2/5) ([#193731](https://github.com/pytorch/pytorch/pull/193731))
- [BE] Removing dead code from MPS (3/5) ([#193732](https://github.com/pytorch/pytorch/pull/193732))
- [BE] Removing dead code from MPS (4/5) ([#193733](https://github.com/pytorch/pytorch/pull/193733))
- [BE] Removing dead code from MPS (5/5) ([#193734](https://github.com/pytorch/pytorch/pull/193734))
- [MPS] Track active_bytes and enable torch.accelerator memory tests ([#193838](https://github.com/pytorch/pytorch/pull/193838))
- [MPS] Fix bfloat16 nextafter flushing subnormals to zero ([#193897](https://github.com/pytorch/pytorch/pull/193897))
- [inductor] Only run is_big_gpu SM check when GEMM templates are in play ([#192375](https://github.com/pytorch/pytorch/pull/192375))
- [MPS] Fix linear backward SIGABRT with a 1-D weight ([#187989](https://github.com/pytorch/pytorch/pull/187989))
- [MPS] Add complex64 support to linalg.lu_factor (unblocks complex det/slogdet/lu) ([#188473](https://github.com/pytorch/pytorch/pull/188473))
- [BE]: Inline the BlockComparison set comporator for MPS allocator ([#195374](https://github.com/pytorch/pytorch/pull/195374))
- [MPS] Fix pad corrupting rank > 4 tensors with >= 2^16 inner elements ([#195147](https://github.com/pytorch/pytorch/pull/195147))
- [MPS] Fix conv backward to preserve input memory format ([#174241](https://github.com/pytorch/pytorch/pull/174241))
- [MPS] Add frexp.Tensor_out ([#194110](https://github.com/pytorch/pytorch/pull/194110))
- [BE][MPS] Migrate conj_physical to Metal ([#195872](https://github.com/pytorch/pytorch/pull/195872))
- [MPS] Fix histogram abort at large bin counts and drop the per-edge sync ([#195714](https://github.com/pytorch/pytorch/pull/195714))
- [MPS] Change `MPSEventPtr` to `intrusive_ptr` ([#195867](https://github.com/pytorch/pytorch/pull/195867))
- [MPS] Implement grouped_mm ([#194933](https://github.com/pytorch/pytorch/pull/194933))
- [BE][Ez]: Use transparent functors to remove cast and UB ([#195753](https://github.com/pytorch/pytorch/pull/195753))
- [MPS] Add nondeterministic alerts for ops that use `atomic_add` ([#195754](https://github.com/pytorch/pytorch/pull/195754))
- [BE] Unify reflection/replication padding shape checks ([#196457](https://github.com/pytorch/pytorch/pull/196457))
- [MPS] Make event synchronization and timing reliable ([#196395](https://github.com/pytorch/pytorch/pull/196395))
- [MPS] Add `Tensor.record_stream` for MPS ([#193464](https://github.com/pytorch/pytorch/pull/193464))
- [BE][MPS] Use `dispatch_sync_with_rethrow` ([#196893](https://github.com/pytorch/pytorch/pull/196893))
- [MPS] fix rand and uniform_ upper-bound rounding ([#197081](https://github.com/pytorch/pytorch/pull/197081))
- [MPS] fix rand and uniform_ upper-bound rounding ([#197081](https://github.com/pytorch/pytorch/pull/197081))
- [BE][MPS] Remove deprecated declaration ([#197200](https://github.com/pytorch/pytorch/pull/197200))
- [MPS] Route reductions over size-1 dims to the inner kernels ([#197397](https://github.com/pytorch/pytorch/pull/197397))
- [MPS] migrate reflection/replication pad to metal ([#196985](https://github.com/pytorch/pytorch/pull/196985))
- [MPS] Fix cat int32 offset overflow for outputs over 2^31 elements ([#189965](https://github.com/pytorch/pytorch/pull/189965))
- [MPS] Guard MPP attention include on header availability ([#196104](https://github.com/pytorch/pytorch/pull/196104))
- [MPS] Fix binary_cross_entropy on zero-element tensors ([#196204](https://github.com/pytorch/pytorch/pull/196204))
- [BE] Move MetalShaderLibrary cache guard out of the class ([#197837](https://github.com/pytorch/pytorch/pull/197837))
- [MPS] migrate rounding ops ([#198497](https://github.com/pytorch/pytorch/pull/198497))
- [MPS] Add gemv fast path for fp8 scaled_mm ([#197862](https://github.com/pytorch/pytorch/pull/197862))
- [MPS] Check that 1D/2D/3D dispatch grid dims fit in uint32 ([#198592](https://github.com/pytorch/pytorch/pull/198592))
- [MPS] Migrate `addc[mul|div]` to Metal ([#196924](https://github.com/pytorch/pytorch/pull/196924))
- [MPS] Promote mixed-dtype operands in the loss kernels and addr ([#198738](https://github.com/pytorch/pytorch/pull/198738))
- [MPS] Raise instead of aborting for addbmm and huber_loss_backward dtype mismatches ([#198739](https://github.com/pytorch/pytorch/pull/198739))
- [MPS] Fix Jacobi SVD convergence for small columns ([#199063](https://github.com/pytorch/pytorch/pull/199063))
- [MPS] Fix Jacobi SVD convergence for small columns ([#199063](https://github.com/pytorch/pytorch/pull/199063))
- [MPS] Add `torch.mps.Stream` and context manager ([#191415](https://github.com/pytorch/pytorch/pull/191415))
- [MPS] Speed up QR with blocked householder updates ([#198732](https://github.com/pytorch/pytorch/pull/198732))
- [MPS] Turn _fft_c2r size mismatch abort into an internal assert ([#199055](https://github.com/pytorch/pytorch/pull/199055))
- Fix building with clang 16 and Apple clang 15 ([#199115](https://github.com/pytorch/pytorch/pull/199115))
- [MPS] Return column-major results from linalg solves ([#199031](https://github.com/pytorch/pytorch/pull/199031))
- [MPS] [Inductor] Reduce short reductions in one thread per output ([#199278](https://github.com/pytorch/pytorch/pull/199278))
- [MPS] Migrate nll_loss forward to Metal kernel to fix 2**31 flat-index overflow (#198471) ([#198776](https://github.com/pytorch/pytorch/pull/198776))
- [MPS] Reduce strided inputs in place for full reductions ([#198646](https://github.com/pytorch/pytorch/pull/198646))
### not user facing
- [BE][MPS] Invert complex op allowlist to denylist ([#195341](https://github.com/pytorch/pytorch/pull/195341))
- [BE] [MPS] Use a typed struct for LU scratch space ([#195297](https://github.com/pytorch/pytorch/pull/195297))
- [BE] Remove obsolete `isLowPower` check ([#195365](https://github.com/pytorch/pytorch/pull/195365))
- [MPS] Remove stale @skipIfMPS from test_nn.py ([#178781](https://github.com/pytorch/pytorch/pull/178781))
- [MPS] Document lack of double precision support ([#193545](https://github.com/pytorch/pytorch/pull/193545))
- [BE][MPS] Delete duplicate op-db error-input test ([#196715](https://github.com/pytorch/pytorch/pull/196715))
- [BE][MPS] Route add/sub through the common add_stub ([#196661](https://github.com/pytorch/pytorch/pull/196661))
- [MPS] Route lerp through the shared ternary kernels ([#196923](https://github.com/pytorch/pytorch/pull/196923))
- [MPS][BE] Delete relu_mps dispatch ([#197068](https://github.com/pytorch/pytorch/pull/197068))
- [BE][MPS] Treat bool params as bool ([#196157](https://github.com/pytorch/pytorch/pull/196157))
- [MPS] Migrate `softplus` to Metal ([#197000](https://github.com/pytorch/pytorch/pull/197000))
- [BE] Delete `[scatter|gather]ViewTensor` wrappers ([#197742](https://github.com/pytorch/pytorch/pull/197742))
- [RAWTHROW][13] widen include_patterns: 20 conversions, 11 that must not be ([#198231](https://github.com/pytorch/pytorch/pull/198231))
- [MPS] Don't request grads in test_output_match ([#198743](https://github.com/pytorch/pytorch/pull/198743))
- [MPS] Move addc{mul,div} value=0 non-finite test to OpInfo ([#198753](https://github.com/pytorch/pytorch/pull/198753))
- [MPS] Fix large tensor skips for `grid_sample` and `bmm` tests ([#199181](https://github.com/pytorch/pytorch/pull/199181))
### security
