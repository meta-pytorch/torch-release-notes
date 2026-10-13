
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
- The MPS backend now requires macOS 15 (Sequoia) or newer ([#199261](https://github.com/pytorch/pytorch/pull/199261))

  macOS 14 (Sonoma) has reached end of life, so the MPS backend no longer carries the workarounds it needed there (for example, gathering strided or offset tensors into contiguous copies before passing them to MPSGraph, and the macOS 14 fallbacks in convolution, matmul, normalization and RNN ops). The follow-up cherry-pick [#200290](https://github.com/pytorch/pytorch/pull/200290) makes the requirement explicit. On macOS 14, `torch.backends.mps.is_available()` returns `False`, and allocating a tensor on the `mps` device raises:

  ```
  RuntimeError: The MPS backend is supported on macOS 15.0+. Current OS version can be queried using `sw_vers`
  ```

  If macOS is new enough but PyTorch finds no Metal GPU it can use (for example inside a VM, sandbox or container), the error now says that instead of asking you to check `sw_vers`. To keep using MPS on macOS 14, stay on PyTorch 2.14 or upgrade macOS. CPU builds of PyTorch still run on older macOS versions.

  C++ extensions are affected as well. The `at::mps::MacOSVersion::MACOS_14_4` enum member was removed (the enum now starts at `MACOS_15_0`), and `torch.backends.mps.is_macos_or_newer(14, minor)` now always returns `True`.

  Version 2.14 (on macOS 14):

  ```python
  >>> torch.backends.mps.is_available()
  True
  >>> torch.ones(2, device="mps")
  tensor([1., 1.], device='mps:0')
  ```

  Version 2.15 (on macOS 14):

  ```python
  >>> torch.backends.mps.is_available()
  False
  >>> torch.ones(2, device="mps")
  RuntimeError: The MPS backend is supported on macOS 15.0+. Current OS version can be queried using `sw_vers`
  ```
### deprecation
- Deprecate calling the C++ `at::mps::MPSProfiler` `begin*` profiling functions without a stream ([#192525](https://github.com/pytorch/pytorch/pull/192525), [#193611](https://github.com/pytorch/pytorch/pull/193611))

  The `beginProfileKernel`, `beginProfileCopy`, `beginProfileGPUInterval`, `endProfileKernel` and `endProfileCopy` methods now have overloads that take the `MPSStream*` the work runs on. The old overloads without a stream still work and use the current MPS stream, but the `begin*` ones emit a deprecation warning such as `beginProfileKernel() called without a stream, may end up profiling the wrong stream`. C++ extensions that profile their own Metal kernels should pass the stream explicitly.

  Version 2.14:
  ```cpp
  auto& profiler = at::mps::getMPSProfiler();
  profiler.beginProfileKernel(pso, "my_kernel", {input, output});
  // ... encode the kernel ...
  profiler.endProfileKernel(pso);
  ```

  Version 2.15:
  ```cpp
  auto& profiler = at::mps::getMPSProfiler();
  at::mps::MPSStream* stream = at::mps::getCurrentMPSStream();
  profiler.beginProfileKernel(pso, "my_kernel", {input, output}, stream);
  // ... encode the kernel ...
  profiler.endProfileKernel(pso, stream);
  ```
### new features
- Add a public MPS stream API: `torch.mps.Stream` (with `synchronize()` and `stream_id`), `torch.mps.current_stream()`, `torch.mps.default_stream()`, `torch.mps.set_stream()` and the `torch.mps.stream()` context manager. These mirror the CUDA APIs, so independent workloads can be queued on separate MPS streams. Add `Tensor.record_stream` for MPS so the allocator does not reuse a tensor's memory until the recorded stream is done with it. For events on non-default streams, use `torch.Event("mps")`; `torch.mps.event.Event.record()` and `wait()` raise `NotImplementedError` when the current stream is not the default stream ([#191415](https://github.com/pytorch/pytorch/pull/191415), [#193464](https://github.com/pytorch/pytorch/pull/193464))

  ```python
  s = torch.mps.Stream()
  with torch.mps.stream(s):
      y = torch.sin(x)
  s.synchronize()
  ```
- Add `torch.float8_e4m3fn` support on MPS, including tensor creation, copies and casts, `item()`, `torch.eye`, gather/scatter, `torch.cat` and constant padding ([#194074](https://github.com/pytorch/pytorch/pull/194074), [#196915](https://github.com/pytorch/pytorch/pull/196915), [#196918](https://github.com/pytorch/pytorch/pull/196918), [#196945](https://github.com/pytorch/pytorch/pull/196945), [#196955](https://github.com/pytorch/pytorch/pull/196955), [#197383](https://github.com/pytorch/pytorch/pull/197383), [#197801](https://github.com/pytorch/pytorch/pull/197801))
- Add a native MPS implementation of grouped matrix multiplication (`torch._grouped_mm`), used by mixture-of-experts models, with a dedicated matrix-vector path for decoding-sized inputs ([#194933](https://github.com/pytorch/pytorch/pull/194933), [#198725](https://github.com/pytorch/pytorch/pull/198725))
- Add a native MPS implementation of `torch._int_mm` (int8 or uint8 by int8 matrix multiplication into int32), which also enables it in AOTInductor on MPS ([#193153](https://github.com/pytorch/pytorch/pull/193153))
- Support `float8_e4m3fn` inputs in `torch.nn.functional.scaled_mm` (`_scaled_mm_v2`) on MPS, with tensorwise and rowwise scaling, optional bias, and fp32, fp16, bf16 or fp8 outputs ([#196916](https://github.com/pytorch/pytorch/pull/196916))
### improvements
- Add MPS support for `torch.logspace`, `torch.take`/`Tensor.put_`, `torch.frexp`, `torch.heaviside` and `torch.special.laguerre_polynomial_l` ([#190495](https://github.com/pytorch/pytorch/pull/190495), [#192980](https://github.com/pytorch/pytorch/pull/192980), [#194110](https://github.com/pytorch/pytorch/pull/194110), [#195265](https://github.com/pytorch/pytorch/pull/195265), [#195225](https://github.com/pytorch/pytorch/pull/195225))
- Add complex64 support on MPS for `torch.linalg.lu_factor` (and therefore `det`, `slogdet` and `lu`), `torch.linalg.lu_solve` (enabling complex backward for `det`, `slogdet`, `logdet` and `solve`), triangular solves (`triangular_solve`, `linalg.solve_triangular`, `cholesky_solve`), and `tanh` backward ([#188473](https://github.com/pytorch/pytorch/pull/188473), [#195369](https://github.com/pytorch/pytorch/pull/195369), [#195861](https://github.com/pytorch/pytorch/pull/195861), [#195601](https://github.com/pytorch/pytorch/pull/195601))
- Support `uint16`, `uint32` and `uint64` inputs in MPS comparison ops ([#198860](https://github.com/pytorch/pytorch/pull/198860))
- Support `sinh`, `cosh`, `asinh`, `acosh`, `hypot`, `copysign`, `logical_xor`, `frexp` and `ldexp` in `torch.compile` on MPS instead of raising `NotImplementedError` ([#197403](https://github.com/pytorch/pytorch/pull/197403))
- Add the `PYTORCH_MPS_METAL_VERSION` environment variable (`3.1`, `3.2` or `4.0`) to choose the Metal language version used by the MPS backend; values below `4.0` load the Metal 3 shader library and disable the Metal Performance Primitives kernels. Also stop using Metal Performance Primitives kernels on paravirtualized GPUs and on builds without Metal 4 shaders, where they cannot run ([#196881](https://github.com/pytorch/pytorch/pull/196881))
- Raise an error under `torch.use_deterministic_algorithms(True)` for nondeterministic MPS ops that use atomic adds, including embedding, embedding bag, grid sampler, pooling and upsample backward ([#195754](https://github.com/pytorch/pytorch/pull/195754))
- Compute `float16` and `bfloat16` `torch.lerp` in float precision on MPS, matching CPU and CUDA ([#196923](https://github.com/pytorch/pytorch/pull/196923))
### bug fixes
- Fix several MPS `torch.linalg.svd` problems: Metal compiler crashes when launching the SVD kernel (`linalg.svd`, `svdvals`, `lstsq`), wrong results for conjugated or column-major complex inputs, a crash in complex `torch.svd(out=)`, non-orthonormal `U` for rank-deficient inputs, and poor convergence for ill-conditioned inputs ([#195949](https://github.com/pytorch/pytorch/pull/195949), [#196128](https://github.com/pytorch/pytorch/pull/196128), [#195872](https://github.com/pytorch/pytorch/pull/195872), [#196139](https://github.com/pytorch/pytorch/pull/196139), [#199063](https://github.com/pytorch/pytorch/pull/199063))
- Fix `torch.linalg.lstsq` raising `IndexError` on MPS for empty inputs ([#199694](https://github.com/pytorch/pytorch/pull/199694))
- Make MPS `linalg.solve`, `linalg.solve_triangular` and `cholesky_solve` return column-major results like CPU and CUDA, fixing `torch.compile` stride assertion failures ([#199031](https://github.com/pytorch/pytorch/pull/199031))
- Fix MPS convolution backward returning `grad_input` in the wrong memory format for `channels_last` inputs, which broke `torch.compile` ([#174241](https://github.com/pytorch/pytorch/pull/174241))
- Fix `torch.nn.functional.linear` backward aborting the process on MPS when `weight` is 1-D ([#187989](https://github.com/pytorch/pytorch/pull/187989))
- Fix `F.pad`, `reflection_pad3d` and `replication_pad3d` silently corrupting outputs for rank > 4 tensors with at least 2^16 inner elements, and wrong `reflection_pad1d` backward gradients for inputs longer than 65536 ([#195147](https://github.com/pytorch/pytorch/pull/195147), [#196985](https://github.com/pytorch/pytorch/pull/196985))
- Unify reflection/replication padding and pooling shape checks across CPU, CUDA and MPS, so invalid inputs (for example a non-positive output size, or bad `max_unpool` arguments) raise the same errors on all backends ([#196457](https://github.com/pytorch/pytorch/pull/196457), [#196230](https://github.com/pytorch/pytorch/pull/196230))
- Raise `NotImplementedError` for MPS pooling ops that would need 64-bit indexing, instead of returning wrong results ([#194460](https://github.com/pytorch/pytorch/pull/194460))
- Fix silent wrong results for very large tensors on MPS: `torch.cat` outputs over 2^31 elements, `arange`/`linspace`/`logspace` over 2^32 elements, and `nll_loss`/`cross_entropy` returning 0 for rows past a 2^31 flat index (the `nll_loss` fix also handles fp16 inputs with more than 65504 targets). Kernel launches whose grid does not fit in 32 bits now raise ([#189965](https://github.com/pytorch/pytorch/pull/189965), [#198593](https://github.com/pytorch/pytorch/pull/198593), [#198776](https://github.com/pytorch/pytorch/pull/198776), [#198592](https://github.com/pytorch/pytorch/pull/198592))
- Fix `torch.histogram`/`histogramdd`/`histc` aborting the process for large bin counts, stop MPS `histogram` from counting values just outside the bin edges that CPU and NumPy drop, and reduce its memory use with atomic counters ([#195714](https://github.com/pytorch/pytorch/pull/195714), [#198416](https://github.com/pytorch/pytorch/pull/198416))
- Fix mixed-dtype inputs aborting the process on MPS: `batch_norm` with half inputs and float32 running stats (now computed in float, as on CPU and CUDA), `mse_loss`, `smooth_l1_loss`, `huber_loss` and `addr` (now promoted), and `addbmm`/`huber_loss_backward` (now raise like CPU and CUDA). `addr` also returns the promoted dtype ([#198740](https://github.com/pytorch/pytorch/pull/198740), [#198738](https://github.com/pytorch/pytorch/pull/198738), [#198739](https://github.com/pytorch/pytorch/pull/198739))
- Fix `torch.lerp` with a scalar weight of a different dtype on MPS ([#196662](https://github.com/pytorch/pytorch/pull/196662))
- Fix MPS `addbmm`, `baddbmm` and `addmm` propagating NaN/Inf from `input` when `beta=0` for empty and complex inputs, and fix complex `alpha`/`beta` in `addmm` ([#193850](https://github.com/pytorch/pytorch/pull/193850), [#194474](https://github.com/pytorch/pytorch/pull/194474))
- Propagate NaN/Inf in MPS `add`/`sub` when `alpha=0`, matching CPU ([#196661](https://github.com/pytorch/pytorch/pull/196661))
- Fix complex `std`/`var` on MPS returning a wrong complex result instead of a real tensor ([#195344](https://github.com/pytorch/pytorch/pull/195344))
- Fix logical ops on complex MPS tensors ignoring the imaginary part ([#195592](https://github.com/pytorch/pytorch/pull/195592))
- Fix MPS `pow(Tensor, Tensor)` results for integer powers diverging from CPU, and add complex support ([#195585](https://github.com/pytorch/pytorch/pull/195585))
- Fix MPS `var`/`std`/`var_mean` intermittently returning wrong values for large reductions ([#198495](https://github.com/pytorch/pytorch/pull/198495))
- Fix MPS `softplus` returning incorrect results on permuted inputs ([#197000](https://github.com/pytorch/pytorch/pull/197000))
- Fix `torch.nextafter` flushing `bfloat16` subnormals to zero on MPS ([#193897](https://github.com/pytorch/pytorch/pull/193897))
- Improve MPS `expm1` accuracy for small inputs ([#198771](https://github.com/pytorch/pytorch/pull/198771))
- Fix `torch.rand` and `uniform_` on MPS sometimes returning the excluded upper bound ([#197081](https://github.com/pytorch/pytorch/pull/197081))
- Fix `scatter_add_`, `index_add_` and `index_put_(accumulate=True)` writing to the wrong elements for `bool` views at storage offsets that are not a multiple of 4 ([#195081](https://github.com/pytorch/pytorch/pull/195081))
- Fix `F.scaled_dot_product_attention` on MPS returning the wrong output shape when batch or head dimensions need broadcasting ([#189631](https://github.com/pytorch/pytorch/pull/189631))
- Fix `nn.BCELoss` raising an internal assert on MPS for zero-element inputs ([#196204](https://github.com/pytorch/pytorch/pull/196204))
- Raise an error for dtype-converting MPS-to-CPU copies to dtypes Metal cannot represent (such as `float64`), instead of silently leaving the destination unwritten ([#197722](https://github.com/pytorch/pytorch/pull/197722))
- Fix compiled `argmax`/`argmin` on MPS returning wrong indices for transposed, sliced and `bfloat16` inputs ([#199134](https://github.com/pytorch/pytorch/pull/199134), [#199132](https://github.com/pytorch/pytorch/pull/199132))
- Stop `torch.compile` on MPS from emitting a misleading "Not enough SMs" warning ([#192375](https://github.com/pytorch/pytorch/pull/192375))
- Fix `torch.utils.dlpack` exports of sliced MPS tensors through the non-owning DLPack exchange API, which produced an invalid buffer pointer ([#182924](https://github.com/pytorch/pytorch/pull/182924))
- Report Metal command buffer failures (such as running out of GPU memory) as errors at the next synchronization point, instead of silently returning zero-filled outputs ([#198883](https://github.com/pytorch/pytorch/pull/198883))
- Fix crashes, hangs and "A command encoder is already encoding to this command buffer" errors when running MPS ops from multiple threads ([#167541](https://github.com/pytorch/pytorch/pull/167541), [#197836](https://github.com/pytorch/pytorch/pull/197836))
- Fix MPS events hanging in `elapsed_time()` after `synchronize()`, and occasionally reporting negative elapsed times ([#196395](https://github.com/pytorch/pytorch/pull/196395))
- Raise an exception instead of aborting the process when an MPS op fails inside a dispatch block (for example `clamp_min(1e40)` on a float tensor) ([#196893](https://github.com/pytorch/pytorch/pull/196893))
- Fix MPS kernels failing Metal debug layer validation (`MTL_DEBUG_LAYER=1`) for half-precision tensors at odd offsets ([#199452](https://github.com/pytorch/pytorch/pull/199452))
- Report `active_bytes` in MPS memory stats instead of always returning 0 ([#193838](https://github.com/pytorch/pytorch/pull/193838))
### performance
- Move more MPS ops from MPSGraph to native Metal kernels. This lowers launch overhead, speeds up strided inputs, and stops MPSGraph from caching one graph per input shape, which made driver memory grow under variable-length workloads (for example, from 21 GB to 8 GB peak in a variable-length LLM training run with `nll_loss`, and by over 250 GB when decoding the Wan2.2 VAE with `F.pad`). Ops moved: `softmax`, `log_softmax`, `nll_loss` backward, constant/reflection/replication padding, `flip`, `where`, `prod`, rounding ops (`floor`, `ceil`, `trunc`, ...), `addcmul`/`addcdiv`, `isposinf`/`isneginf`, `logit` backward, upsample backward and `conv1d` ([#196071](https://github.com/pytorch/pytorch/pull/196071), [#195441](https://github.com/pytorch/pytorch/pull/195441), [#195153](https://github.com/pytorch/pytorch/pull/195153), [#195368](https://github.com/pytorch/pytorch/pull/195368), [#193826](https://github.com/pytorch/pytorch/pull/193826), [#198719](https://github.com/pytorch/pytorch/pull/198719), [#198688](https://github.com/pytorch/pytorch/pull/198688), [#198497](https://github.com/pytorch/pytorch/pull/198497), [#196924](https://github.com/pytorch/pytorch/pull/196924), [#189548](https://github.com/pytorch/pytorch/pull/189548), [#199687](https://github.com/pytorch/pytorch/pull/199687), [#198878](https://github.com/pytorch/pytorch/pull/198878))
- Speed up MPS reductions: shared reduction kernels for `norm` and `std`/`var`, faster reductions over adjacent dims and size-1 dims, in-place full reductions of strided inputs, and one-thread-per-output short reductions in `torch.compile` ([#198494](https://github.com/pytorch/pytorch/pull/198494), [#198611](https://github.com/pytorch/pytorch/pull/198611), [#198635](https://github.com/pytorch/pytorch/pull/198635), [#197397](https://github.com/pytorch/pytorch/pull/197397), [#198646](https://github.com/pytorch/pytorch/pull/198646), [#199278](https://github.com/pytorch/pytorch/pull/199278))
- Speed up matrix-vector workloads typical of LLM decoding: use GEMV kernels for `F.linear`, and add a GEMV fast path for fp8 `scaled_mm` ([#198721](https://github.com/pytorch/pytorch/pull/198721), [#197862](https://github.com/pytorch/pytorch/pull/197862))
- Speed up MPS linear algebra: blocked triangular solves that no longer depend on `MPSMatrixSolveTriangular`, specialized small batched triangular solves, register-resident inverses for matrices up to 4x4, blocked Householder QR, and running small `linalg.svd` inputs on the GPU instead of falling back to CPU ([#196241](https://github.com/pytorch/pytorch/pull/196241), [#196900](https://github.com/pytorch/pytorch/pull/196900), [#195944](https://github.com/pytorch/pytorch/pull/195944), [#198732](https://github.com/pytorch/pytorch/pull/198732), [#195950](https://github.com/pytorch/pytorch/pull/195950))
- Speed up MPS convolutions: `channels_last` conv2d backward, and conv3d weight permutation ([#193623](https://github.com/pytorch/pytorch/pull/193623), [#193167](https://github.com/pytorch/pytorch/pull/193167))
- Speed up `histc` with atomic counters instead of a large per-element temporary, and remove a GPU-to-CPU sync from it ([#192164](https://github.com/pytorch/pytorch/pull/192164), [#196016](https://github.com/pytorch/pytorch/pull/196016))
- Speed up `x[bool_mask] = scalar` (via the `masked_fill_` fast path), out-of-place `F.dropout` (via the fused kernel), float `sort`/`topk` on short rows, and strided ternary ops (up to 5x) on MPS ([#195020](https://github.com/pytorch/pytorch/pull/195020), [#195011](https://github.com/pytorch/pytorch/pull/195011), [#198960](https://github.com/pytorch/pytorch/pull/198960), [#196922](https://github.com/pytorch/pytorch/pull/196922))
### docs
- Document that the MPS backend does not support double precision (`float64`) ([#193545](https://github.com/pytorch/pytorch/pull/193545))
### devs
- Fix building PyTorch with clang 16 and Apple clang 15 ([#199115](https://github.com/pytorch/pytorch/pull/199115))
- Fix building with a Metal 4 toolchain against an older macOS SDK, where the Metal Performance Primitives headers are missing ([#196104](https://github.com/pytorch/pytorch/pull/196104))
- Fix deprecation warnings when building against the macOS 27 SDK: drop the unused managed storage mode from the MPS allocator, and check for the `MTLGPUFamilyApple7` GPU family instead of the deprecated `MTLGPUFamilyMac2` when picking the MPS device ([#197200](https://github.com/pytorch/pytorch/pull/197200))
### not user facing
- Remove dead MPS code ([#193730](https://github.com/pytorch/pytorch/pull/193730), [#193731](https://github.com/pytorch/pytorch/pull/193731), [#193732](https://github.com/pytorch/pytorch/pull/193732), [#193733](https://github.com/pytorch/pytorch/pull/193733), [#193734](https://github.com/pytorch/pytorch/pull/193734))
- Internal MPS refactors and cleanups: inline the MPS allocator block comparator, use transparent functors, change `MPSEventPtr` to `intrusive_ptr`, use a typed struct for LU scratch space, remove the obsolete `isLowPower` check, delete the `relu_mps` dispatch and `[scatter|gather]ViewTensor` wrappers, and pass bool kernel parameters as `bool` ([#195374](https://github.com/pytorch/pytorch/pull/195374), [#195753](https://github.com/pytorch/pytorch/pull/195753), [#195867](https://github.com/pytorch/pytorch/pull/195867), [#195297](https://github.com/pytorch/pytorch/pull/195297), [#195365](https://github.com/pytorch/pytorch/pull/195365), [#197068](https://github.com/pytorch/pytorch/pull/197068), [#197742](https://github.com/pytorch/pytorch/pull/197742), [#196157](https://github.com/pytorch/pytorch/pull/196157))
- Move the `MetalShaderLibrary` cache lock out of the class, so the race fix in #167541 does not change the class layout seen by C++ extensions ([#197837](https://github.com/pytorch/pytorch/pull/197837))
- Fix out-of-bounds reads in the new `nll_loss` backward Metal kernel for 1-D inputs, a regression from #195153 that never shipped ([#195411](https://github.com/pytorch/pytorch/pull/195411))
- Turn an abort in the private `aten._fft_c2r` op on mismatched sizes (not reachable through public FFT APIs) into an internal assert ([#199055](https://github.com/pytorch/pytorch/pull/199055))
- Widen the RAWTHROW lint to `.mm` and other source extensions ([#198231](https://github.com/pytorch/pytorch/pull/198231))
- MPS test changes: invert the complex op allowlist into a denylist, remove stale skips, delete a duplicate error-input test, stop requesting grads in `test_output_match`, move an `addcmul`/`addcdiv` test to OpInfo, and fix large-tensor test skips ([#195341](https://github.com/pytorch/pytorch/pull/195341), [#178781](https://github.com/pytorch/pytorch/pull/178781), [#196715](https://github.com/pytorch/pytorch/pull/196715), [#198743](https://github.com/pytorch/pytorch/pull/198743), [#198753](https://github.com/pytorch/pytorch/pull/198753), [#199181](https://github.com/pytorch/pytorch/pull/199181))
### security
