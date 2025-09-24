# cherry picks
## bc breaking
## deprecation
## new features
- NVSHMEM support for Triton 3.5 ([#163152](https://github.com/pytorch/pytorch/pull/163152))
## improvements
### export
- Support vmap + custom autograd function/improve DTensor constructor inefficiency ([#162240](https://github.com/pytorch/pytorch/pull/162240))

### inductor
- Share default device context when all graph partitions and cudagraph-unsafe ops are on the same device([#162873](https://github.com/pytorch/pytorch/pull/162873))

## bug fixes
### cuda
- Roll-back cuDNN frontend upgrade and update Meta registration due to compile issues ([#163104](https://github.com/pytorch/pytorch/pull/163104))

### CPU
- Add check so non-aarch64 platforms can hit `MKLDNN` path ([#162168](https://github.com/pytorch/pytorch/pull/162168))

### inductor
- Fix `FallbackKernel` alias function to avoid incorrect aliasing for custom ops ([#163227](https://github.com/pytorch/pytorch/pull/163227))

### distributed (symm_mem)
- Fix `put_signal` + `wait_until` hang ([#163194](https://github.com/pytorch/pytorch/pull/163194))

### export
- Remove `.contiguous()` when saving weights to raw bytes to preserve original storage size of tensor ([#163587](https://github.com/pytorch/pytorch/pull/163587))

## performance

## docs
### ONNX
- Update export docstring and set `fallback=False` by default ([#162622](https://github.com/pytorch/pytorch/pull/162622), [#162726](https://github.com/pytorch/pytorch/pull/162726))
- Fix typo in error message: summit -> submit ([#162587](https://github.com/pytorch/pytorch/pull/162587))

## devs

## Untopiced

## security

## not user facing
- Release only changes ([#162493](https://github.com/pytorch/pytorch/pull/162493))
- CUDA 13.0 Windows Nvidia Driver update to 580.88 ([#162425](https://github.com/pytorch/pytorch/pull/162425))
- Fix aarch64 linux packaging ([#162566](https://github.com/pytorch/pytorch/pull/162566))
- Update `torch-xpu-ops` commit pin ([#162935](https://github.com/pytorch/pytorch/pull/162935))
- Fix deterministic `scatter_add` path for multi-d tensors ([#162866](https://github.com/pytorch/pytorch/pull/162866))
- Fix docs push in nightly workflow ([#162657](https://github.com/pytorch/pytorch/pull/162657))
- Skip `test_ind_worker_queue` on Windows and macOS (flaky) ([#162555](https://github.com/pytorch/pytorch/pull/162555))
- Add decomp rule to `assert_tensor_metadata` for BatchedTensors ([#163008](https://github.com/pytorch/pytorch/pull/163008))
- Add way to register custom rule for if inductor should partition graph around an op ([#163310](https://github.com/pytorch/pytorch/pull/163310))
- Update NVIDIA driver to 580.82.07 ([#163111](https://github.com/pytorch/pytorch/pull/163111))
- Update 3.5 pin for triton ([#163382](https://github.com/pytorch/pytorch/pull/163382))
- CUDA 13.0 Warning update for supported architectures ([#163585](https://github.com/pytorch/pytorch/pull/163585))
- Update `pytorch_sphinx_theme2` to latest hash ([#163269](https://github.com/pytorch/pytorch/pull/163269))

## Added to final.md directly
