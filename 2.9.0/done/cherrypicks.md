# cherry picks
## bc breaking
## deprecation
## new features
## improvements
### inductor
- [Graph Partition] improve custom op output alias ([#163380](https://github.com/pytorch/pytorch/pull/163380))

## bug fixes
### cuda
- [cuDNN][SDPA][submodule] Roll-back cuDNN frontend upgrade, update Meta registration ([#163265](https://github.com/pytorch/pytorch/pull/163265))

### cpu (aarch64)
- Fix the regression issue caused by non-arrch64 platforms not hitting the MKLDNN path ([#162778](https://github.com/pytorch/pytorch/pull/162778))

### inductor
- [Cherry Pick][Graph Partition] allow sharing default device context ([#163097](https://github.com/pytorch/pytorch/pull/163097))

### inductor (aoti)
- Revert "Make distributed modules importable even when backend not built ([#163024](https://github.com/pytorch/pytorch/pull/163024))

### export
- Add decomp rule to assert_tensor_metadata for BatchedTensors ([#163361](https://github.com/pytorch/pytorch/pull/163361))

## performance

## docs

## devs

## Untopiced

## security

## not user facing
- [Release 2.9] Release only changes ([#162493](https://github.com/pytorch/pytorch/pull/162493))
- CUDA 13.0 Windows Nvidia Driver update to 580.88 ([#162501](https://github.com/pytorch/pytorch/pull/162501))
- [CD] Aarch64 Fix packaging libarm_compute.so and other libraries to the aarch64 CUDA wheels ([#162596](https://github.com/pytorch/pytorch/pull/162596))
- fix typo: summit -> submit ([#162597](https://github.com/pytorch/pytorch/pull/162597))
- [ONNX] Update export docstring & Set fallback=False by default ([#162637](https://github.com/pytorch/pytorch/pull/162637))
- Support vmap + custom autograd function/improve DTensor constructor inefficiency ([#162738](https://github.com/pytorch/pytorch/pull/162738))
- [Release 2.9] Update torch-xpu-ops commit pin ([#162935](https://github.com/pytorch/pytorch/pull/162935))
- fix deterministic scatter_add path for multi-d tensors ([#162977](https://github.com/pytorch/pytorch/pull/162977))
- [ez][CI] Fix docs push in nightly workflow ([#163085](https://github.com/pytorch/pytorch/pull/163085))
- [SymmMem] Fix NVSHMEM plugin + Triton 3.5 ([#163262](https://github.com/pytorch/pytorch/pull/163262))
- Skip test_ind_worker_queue on Windows and macOS (flaky) ([#163363](https://github.com/pytorch/pytorch/pull/163363))

## Added to final.md directly
