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


## Added to final.md directly
