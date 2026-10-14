
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
- The MPS backend now requires macOS 15 (Sequoia) or newer ([#199261](https://github.com/pytorch/pytorch/pull/199261), [#200290](https://github.com/pytorch/pytorch/pull/200290))

  macOS 14 has reached end of life, so its MPS workarounds were removed. On macOS 14, `torch.backends.mps.is_available()` returns `False` and allocating on `mps` raises the error below. To keep using MPS, stay on PyTorch 2.14 or upgrade macOS; CPU builds still run on older macOS. C++ extensions: `at::mps::MacOSVersion::MACOS_14_4` was removed.

  ```python
  >>> torch.ones(2, device="mps")  # 2.15 on macOS 14
  RuntimeError: The MPS backend is supported on macOS 15.0+. Current OS version can be queried using `sw_vers`
  ```
### deprecation
### new features
- Add a public MPS stream API (`torch.mps.Stream`, `current_stream()`, `default_stream()`, `set_stream()`, the `torch.mps.stream()` context manager) and `Tensor.record_stream` on MPS ([#191415](https://github.com/pytorch/pytorch/pull/191415), [#193464](https://github.com/pytorch/pytorch/pull/193464))
- Add `torch.float8_e4m3fn` support on MPS ([#194074](https://github.com/pytorch/pytorch/pull/194074), [#196915](https://github.com/pytorch/pytorch/pull/196915), [#196918](https://github.com/pytorch/pytorch/pull/196918), [#196945](https://github.com/pytorch/pytorch/pull/196945), [#196955](https://github.com/pytorch/pytorch/pull/196955), [#197383](https://github.com/pytorch/pytorch/pull/197383), [#197801](https://github.com/pytorch/pytorch/pull/197801))
- Support `float8_e4m3fn` inputs in `torch.nn.functional.scaled_mm` on MPS ([#196916](https://github.com/pytorch/pytorch/pull/196916))
### improvements
- Add MPS support for `torch.logspace`, `torch.take`/`Tensor.put_`, `torch.frexp`, `torch.heaviside`, `torch.special.laguerre_polynomial_l`, and unsigned integer comparisons ([#190495](https://github.com/pytorch/pytorch/pull/190495), [#192980](https://github.com/pytorch/pytorch/pull/192980), [#194110](https://github.com/pytorch/pytorch/pull/194110), [#195265](https://github.com/pytorch/pytorch/pull/195265), [#195225](https://github.com/pytorch/pytorch/pull/195225), [#198860](https://github.com/pytorch/pytorch/pull/198860))
- Add complex64 support on MPS for `linalg.lu_factor`, `linalg.lu_solve`, triangular solves and `tanh` backward ([#188473](https://github.com/pytorch/pytorch/pull/188473), [#195369](https://github.com/pytorch/pytorch/pull/195369), [#195861](https://github.com/pytorch/pytorch/pull/195861), [#195601](https://github.com/pytorch/pytorch/pull/195601))
- Support `sinh`, `hypot`, `ldexp` and other math ops in `torch.compile` on MPS ([#197403](https://github.com/pytorch/pytorch/pull/197403))
- Add `PYTORCH_MPS_METAL_VERSION` to choose the Metal language version ([#196881](https://github.com/pytorch/pytorch/pull/196881))
- Raise an error under `torch.use_deterministic_algorithms(True)` for nondeterministic MPS ops ([#195754](https://github.com/pytorch/pytorch/pull/195754))
- Compute half and bfloat16 `torch.lerp` in float on MPS ([#196923](https://github.com/pytorch/pytorch/pull/196923))
- Add a native MPS implementation of `torch.nn.functional.grouped_mm` for mixture-of-experts models ([#194933](https://github.com/pytorch/pytorch/pull/194933), [#198725](https://github.com/pytorch/pytorch/pull/198725))
### bug fixes
- Fix crashes and wrong results in MPS `linalg.svd`, `linalg.lstsq` and `linalg.solve` ([#195949](https://github.com/pytorch/pytorch/pull/195949), [#196128](https://github.com/pytorch/pytorch/pull/196128), [#195872](https://github.com/pytorch/pytorch/pull/195872), [#196139](https://github.com/pytorch/pytorch/pull/196139), [#199063](https://github.com/pytorch/pytorch/pull/199063), [#199694](https://github.com/pytorch/pytorch/pull/199694), [#199031](https://github.com/pytorch/pytorch/pull/199031))
- Fix `torch.compile` on MPS: wrong `argmax`/`argmin` indices, `channels_last` conv backward stride errors, and a misleading "Not enough SMs" warning ([#199134](https://github.com/pytorch/pytorch/pull/199134), [#199132](https://github.com/pytorch/pytorch/pull/199132), [#174241](https://github.com/pytorch/pytorch/pull/174241), [#192375](https://github.com/pytorch/pytorch/pull/192375))
- Raise errors instead of aborting the process on MPS for mixed-dtype inputs (`batch_norm`, `mse_loss`, `addr`, ...), 1-D-weight `linear` backward, empty `BCELoss`, and failures inside dispatch blocks ([#198740](https://github.com/pytorch/pytorch/pull/198740), [#198738](https://github.com/pytorch/pytorch/pull/198738), [#198739](https://github.com/pytorch/pytorch/pull/198739), [#187989](https://github.com/pytorch/pytorch/pull/187989), [#196204](https://github.com/pytorch/pytorch/pull/196204), [#196893](https://github.com/pytorch/pytorch/pull/196893))
- Fix silent wrong results for large MPS tensors in `torch.cat`, `arange`/`linspace`, `nll_loss`, padding and pooling, and fix `histogram` aborts and out-of-range counts ([#189965](https://github.com/pytorch/pytorch/pull/189965), [#198593](https://github.com/pytorch/pytorch/pull/198593), [#198776](https://github.com/pytorch/pytorch/pull/198776), [#198592](https://github.com/pytorch/pytorch/pull/198592), [#195147](https://github.com/pytorch/pytorch/pull/195147), [#196985](https://github.com/pytorch/pytorch/pull/196985), [#194460](https://github.com/pytorch/pytorch/pull/194460), [#195714](https://github.com/pytorch/pytorch/pull/195714), [#198416](https://github.com/pytorch/pytorch/pull/198416))
- Unify padding and pooling shape checks across CPU, CUDA and MPS ([#196457](https://github.com/pytorch/pytorch/pull/196457), [#196230](https://github.com/pytorch/pytorch/pull/196230))
- Propagate NaN/Inf in MPS `addmm`/`addbmm`/`baddbmm` with `beta=0` and `add`/`sub` with `alpha=0` ([#193850](https://github.com/pytorch/pytorch/pull/193850), [#194474](https://github.com/pytorch/pytorch/pull/194474), [#196661](https://github.com/pytorch/pytorch/pull/196661))
- Fix MPS `pow` with integer exponents, and complex `std`/`var`, `pow` and logical ops ([#195585](https://github.com/pytorch/pytorch/pull/195585), [#195344](https://github.com/pytorch/pytorch/pull/195344), [#195592](https://github.com/pytorch/pytorch/pull/195592))
- Fix wrong MPS results in large `var`/`std` reductions, permuted `softplus`, `lerp` with a scalar weight, `rand` hitting its upper bound, bfloat16 `nextafter`, and small-input `expm1` ([#198495](https://github.com/pytorch/pytorch/pull/198495), [#197000](https://github.com/pytorch/pytorch/pull/197000), [#196662](https://github.com/pytorch/pytorch/pull/196662), [#197081](https://github.com/pytorch/pytorch/pull/197081), [#193897](https://github.com/pytorch/pytorch/pull/193897), [#198771](https://github.com/pytorch/pytorch/pull/198771))
- Fix MPS `scaled_dot_product_attention` output shape with broadcast batch/head dims, and `scatter_add_`/`index_add_` on offset `bool` views ([#189631](https://github.com/pytorch/pytorch/pull/189631), [#195081](https://github.com/pytorch/pytorch/pull/195081))
- Raise errors for MPS command buffer failures (such as out of memory) and MPS-to-CPU copies to `float64` instead of returning wrong outputs ([#198883](https://github.com/pytorch/pytorch/pull/198883), [#197722](https://github.com/pytorch/pytorch/pull/197722))
- Fix crashes and hangs when running MPS ops from multiple threads, and hangs in MPS event `elapsed_time()` ([#167541](https://github.com/pytorch/pytorch/pull/167541), [#197836](https://github.com/pytorch/pytorch/pull/197836), [#196395](https://github.com/pytorch/pytorch/pull/196395))
- Fix DLPack export of sliced MPS tensors, Metal debug-layer validation failures, and `active_bytes` in MPS memory stats ([#182924](https://github.com/pytorch/pytorch/pull/182924), [#199452](https://github.com/pytorch/pytorch/pull/199452), [#193838](https://github.com/pytorch/pytorch/pull/193838))
### performance
- Move more MPS ops (`softmax`, `nll_loss`, padding, `where`, ...) to native Metal kernels, cutting launch overhead and driver memory growth with variable shapes ([#196071](https://github.com/pytorch/pytorch/pull/196071), [#195441](https://github.com/pytorch/pytorch/pull/195441), [#195153](https://github.com/pytorch/pytorch/pull/195153), [#195368](https://github.com/pytorch/pytorch/pull/195368), [#193826](https://github.com/pytorch/pytorch/pull/193826), [#198719](https://github.com/pytorch/pytorch/pull/198719), [#198688](https://github.com/pytorch/pytorch/pull/198688), [#198497](https://github.com/pytorch/pytorch/pull/198497), [#196924](https://github.com/pytorch/pytorch/pull/196924), [#189548](https://github.com/pytorch/pytorch/pull/189548), [#199687](https://github.com/pytorch/pytorch/pull/199687), [#198878](https://github.com/pytorch/pytorch/pull/198878))
- Speed up MPS reductions, linear algebra, GEMV, convolutions, `histc`, masked fill, dropout and sort ([#198494](https://github.com/pytorch/pytorch/pull/198494), [#198611](https://github.com/pytorch/pytorch/pull/198611), [#198635](https://github.com/pytorch/pytorch/pull/198635), [#197397](https://github.com/pytorch/pytorch/pull/197397), [#198646](https://github.com/pytorch/pytorch/pull/198646), [#199278](https://github.com/pytorch/pytorch/pull/199278), [#198721](https://github.com/pytorch/pytorch/pull/198721), [#197862](https://github.com/pytorch/pytorch/pull/197862), [#196241](https://github.com/pytorch/pytorch/pull/196241), [#196900](https://github.com/pytorch/pytorch/pull/196900), [#195944](https://github.com/pytorch/pytorch/pull/195944), [#198732](https://github.com/pytorch/pytorch/pull/198732), [#195950](https://github.com/pytorch/pytorch/pull/195950), [#193623](https://github.com/pytorch/pytorch/pull/193623), [#193167](https://github.com/pytorch/pytorch/pull/193167), [#192164](https://github.com/pytorch/pytorch/pull/192164), [#196016](https://github.com/pytorch/pytorch/pull/196016), [#195020](https://github.com/pytorch/pytorch/pull/195020), [#195011](https://github.com/pytorch/pytorch/pull/195011), [#198960](https://github.com/pytorch/pytorch/pull/198960), [#196922](https://github.com/pytorch/pytorch/pull/196922))
### docs
- Note MPS lacks `float64` support ([#193545](https://github.com/pytorch/pytorch/pull/193545))
### devs
- Fix building with clang 16 and Apple clang 15 ([#199115](https://github.com/pytorch/pytorch/pull/199115))
- Fix building with a Metal 4 toolchain against older macOS SDKs, and deprecation warnings with the macOS 27 SDK ([#196104](https://github.com/pytorch/pytorch/pull/196104), [#197200](https://github.com/pytorch/pytorch/pull/197200))
- `at::mps::MPSProfiler` `begin*`/`end*` methods take the `MPSStream*`; stream-less `begin*` overloads are deprecated ([#192525](https://github.com/pytorch/pytorch/pull/192525), [#193611](https://github.com/pytorch/pytorch/pull/193611))
- Add a native MPS implementation of the private `torch._int_mm` op, which also enables it in AOTInductor on MPS ([#193153](https://github.com/pytorch/pytorch/pull/193153))
### not user facing
- Remove dead MPS code ([#193730](https://github.com/pytorch/pytorch/pull/193730), [#193731](https://github.com/pytorch/pytorch/pull/193731), [#193732](https://github.com/pytorch/pytorch/pull/193732), [#193733](https://github.com/pytorch/pytorch/pull/193733), [#193734](https://github.com/pytorch/pytorch/pull/193734))
- Internal MPS refactors and cleanups: inline the MPS allocator block comparator, use transparent functors, change `MPSEventPtr` to `intrusive_ptr`, use a typed struct for LU scratch space, remove the obsolete `isLowPower` check, delete the `relu_mps` dispatch and `[scatter|gather]ViewTensor` wrappers, and pass bool kernel parameters as `bool` ([#195374](https://github.com/pytorch/pytorch/pull/195374), [#195753](https://github.com/pytorch/pytorch/pull/195753), [#195867](https://github.com/pytorch/pytorch/pull/195867), [#195297](https://github.com/pytorch/pytorch/pull/195297), [#195365](https://github.com/pytorch/pytorch/pull/195365), [#197068](https://github.com/pytorch/pytorch/pull/197068), [#197742](https://github.com/pytorch/pytorch/pull/197742), [#196157](https://github.com/pytorch/pytorch/pull/196157))
- Move the `MetalShaderLibrary` cache lock out of the class, so the race fix in #167541 does not change the class layout seen by C++ extensions ([#197837](https://github.com/pytorch/pytorch/pull/197837))
- Fix out-of-bounds reads in the new `nll_loss` backward Metal kernel for 1-D inputs, a regression from #195153 that never shipped ([#195411](https://github.com/pytorch/pytorch/pull/195411))
- Turn an abort in the private `aten._fft_c2r` op on mismatched sizes (not reachable through public FFT APIs) into an internal assert ([#199055](https://github.com/pytorch/pytorch/pull/199055))
- Widen the RAWTHROW lint to `.mm` and other source extensions ([#198231](https://github.com/pytorch/pytorch/pull/198231))
- MPS test changes: invert the complex op allowlist into a denylist, remove stale skips, delete a duplicate error-input test, stop requesting grads in `test_output_match`, move an `addcmul`/`addcdiv` test to OpInfo, and fix large-tensor test skips ([#195341](https://github.com/pytorch/pytorch/pull/195341), [#178781](https://github.com/pytorch/pytorch/pull/178781), [#196715](https://github.com/pytorch/pytorch/pull/196715), [#198743](https://github.com/pytorch/pytorch/pull/198743), [#198753](https://github.com/pytorch/pytorch/pull/198753), [#199181](https://github.com/pytorch/pytorch/pull/199181))
### security
