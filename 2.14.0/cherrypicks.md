# cherry picks

## bc breaking

## deprecation

## new features

### Ahead-Of-Time Inductor (AOTI)
- Add `aoti_torch_mps_set_arg_bytes` to the stable MPS AOTI shim so custom Metal kernels can pass scalar and structured arguments without temporary tensors ([#190932](https://github.com/pytorch/pytorch/pull/190932))

### C++ Frontend
- Make `fastAtomicAdd` available from PyTorch's header-only C++ headers ([#193604](https://github.com/pytorch/pytorch/pull/193604))

## improvements

## bug fixes

### Autograd
- Fix Python reference leaks in the autograd C++ bindings ([#187069](https://github.com/pytorch/pytorch/pull/187069))

### cuDNN
- Disable cuDNN SDPA decoding on cuDNN and device combinations affected by incorrect decoding results ([#194927](https://github.com/pytorch/pytorch/pull/194927))

### Inductor
- Disable `batch_linear_lhs` by default on XPU to prevent Qwen 3.5 and 3.8 crashes caused by non-contiguous split views ([#194225](https://github.com/pytorch/pytorch/pull/194225))
- Fix loop-local load common-subexpression elimination so Inductor does not reuse loads outside their valid loop scope ([#194786](https://github.com/pytorch/pytorch/pull/194786))

### MPS
- Fix `torch.mm`, `torch.addmm`, and `torch.bmm` with an `out=` tensor slice producing incorrect results on macOS 14 ([#193385](https://github.com/pytorch/pytorch/pull/193385))
- Raise clear errors for MPS reductions on tensors requiring 64-bit indexing instead of silently returning incorrect results or aborting ([#194082](https://github.com/pytorch/pytorch/pull/194082))
- Prevent `pin_memory()` from reusing MPS buffers still referenced by in-flight GPU work, avoiding corruption of newly pinned data ([#193819](https://github.com/pytorch/pytorch/pull/193819))

### Profiler
- Exclude host-side `OVERHEAD` activities from CUDA and XPU device totals so profiler device time is not double-counted ([#193924](https://github.com/pytorch/pytorch/pull/193924))

### Python Frontend
- Avoid eagerly initializing accelerator runtimes when calling `torch.get_device_module()` ([#190751](https://github.com/pytorch/pytorch/pull/190751))
- Respect process CPU affinity and cpuset limits when choosing the default thread count, preventing excessive threads and `libgomp: Thread creation failed` errors in constrained environments ([#194605](https://github.com/pytorch/pytorch/pull/194605))

### Release Engineering
- Fix Windows Python 3.15 wheel builds by pinning Cython below 3.3 and using NumPy 2.5.2 ([#194618](https://github.com/pytorch/pytorch/pull/194618))
- Fix macOS Python 3.15 wheel builds by pinning Cython below 3.3 and using NumPy 2.5.2 ([#194734](https://github.com/pytorch/pytorch/pull/194734))

### ROCm
- Fix ROCm 7.14 `shared-with-deps` libtorch packages by bundling their transitive ROCm SDK libraries ([#193242](https://github.com/pytorch/pytorch/pull/193242))
- Make ROCm wheels self-contained by rewriting bundled-library dependencies after all libraries are copied ([#189906](https://github.com/pytorch/pytorch/pull/189906))
- Make Inductor's CPU ISA probe work with self-contained ROCm wheels by retrying after importing `torch` ([#189900](https://github.com/pytorch/pytorch/pull/189900))

### XPU
- Fix XPU Inductor code generation by defining `current_device_idx_expr` ([#192996](https://github.com/pytorch/pytorch/pull/192996))
- Restore fused `_safe_softmax` dispatch on XPU, fixing a 10–27% eager performance regression in affected models ([#193786](https://github.com/pytorch/pytorch/pull/193786))
- Fix FFT dtype handling on XPU by avoiding an inconsistent `float16`-to-`float32` promotion ([#192733](https://github.com/pytorch/pytorch/pull/192733))

## performance

### CPU (x86)
- Restore the PyTorch 2.13 oneDNN version on CPU to address a vLLM performance regression ([#194089](https://github.com/pytorch/pytorch/pull/194089))

## docs

### XPU
- Document WSL2 support in the XPU getting-started guide ([#192398](https://github.com/pytorch/pytorch/pull/192398))
- Document XPU support for symmetric memory tensors ([#193475](https://github.com/pytorch/pytorch/pull/193475))
- Remove end-of-life Ubuntu 25.10 from the XPU supported-OS list ([#194145](https://github.com/pytorch/pytorch/pull/194145))

## devs

## security

## Untopiced

## not user facing

### Build Frontend
- Bundle the CUDA 13.4 `ptxas` binary in nightly wheels for Rubin testing ([#192653](https://github.com/pytorch/pytorch/pull/192653))

### C++ Frontend
- Skip non-self-contained `complex_utils.h` in the header-only binary smoke test ([#193218](https://github.com/pytorch/pytorch/pull/193218))

### Release Engineering
- Apply release-only version and CI changes to the 2.14 branch ([#193018](https://github.com/pytorch/pytorch/pull/193018))
- Bump cuDNN to 9.25.0.15 for CUDA 13.4 RC1 wheels ([#192843](https://github.com/pytorch/pytorch/pull/192843))
- Refresh release runner groups automatically when a release tag is pushed ([#193186](https://github.com/pytorch/pytorch/pull/193186))
- Remove CUDA 13.4 from the 2.14 binary build matrix ([#194374](https://github.com/pytorch/pytorch/pull/194374))
- Update the Python 3.15 NumPy build pin to 2.5.2 ([#194741](https://github.com/pytorch/pytorch/pull/194741))
- Make the Docker release validation job use the channel matching the pushed image ([#194788](https://github.com/pytorch/pytorch/pull/194788))
- Pin Cython below 3.3 for Windows Triton wheel builds ([#194914](https://github.com/pytorch/pytorch/pull/194914))

### ROCm
- Update MI300 runner labels and re-enable MI300 CI workflows ([#192262](https://github.com/pytorch/pytorch/pull/192262))

### XPU
- Fix XPU CI coverage for CUDA-only tests and `torch.polar` half-precision behavior ([#192728](https://github.com/pytorch/pytorch/pull/192728))
- Fix malformed XPU dispatch formatting in `native_functions.yaml` ([#193184](https://github.com/pytorch/pytorch/pull/193184))
- Update the `torch-xpu-ops` commit pin for the 2.14 release ([#194235](https://github.com/pytorch/pytorch/pull/194235))
