# cherry picks
## bc breaking
## deprecation
## new features
### ONNX
- Support custom empty tensor shapes in `InputObserver` for multimodal LLM export ([#174964](https://github.com/pytorch/pytorch/pull/174964))
## improvements
## bug fixes
### MPS
- Fix 2-pass SDPA memory corruption by forcing float accumulators ([#174945](https://github.com/pytorch/pytorch/pull/174945))
## performance
## docs
### XPU
- Update previous version 2.10 installation in get start xpu ([#176141](https://github.com/pytorch/pytorch/pull/176141))
## devs
## Untopiced
## security
## not user facing
### Build Frontend
- Remove python constraint on setuptools ([#175577](https://github.com/pytorch/pytorch/pull/175577))
### CPU
- Fix UB: use vector::resize() instead of reserve() before operator[] access ([#175315](https://github.com/pytorch/pytorch/pull/175315))
- Fix Identity comparability and evalf recursion ([#175975](https://github.com/pytorch/pytorch/pull/175975))
### Dynamo
- Update inductor expected accuracy files ([#175041](https://github.com/pytorch/pytorch/pull/175041))
- Skip pytorch_CycleGAN_and_pix2pix from inductor benchmarks ([#175066](https://github.com/pytorch/pytorch/pull/175066))
- Disable einops 0.8.2 check on PyTorch ([#175351](https://github.com/pytorch/pytorch/pull/175351))
- Bump transformers version to 5.2.0 ([#175274](https://github.com/pytorch/pytorch/pull/175274))
### Inductor
- Avoid multi-stage for mix-order-red by default ([#176228](https://github.com/pytorch/pytorch/pull/176228))
### ROCm
- Forward fix #174087, take 4 ([#175098](https://github.com/pytorch/pytorch/pull/175098))
### Release Engineering
- Release only changes for 2.11 ([#175091](https://github.com/pytorch/pytorch/pull/175091))
- Fix macOS arm64 libtorch release upload failure ([#175100](https://github.com/pytorch/pytorch/pull/175100))
- Move CUDA 12.8 GPU tests from per-commit trunk to periodic ([#175067](https://github.com/pytorch/pytorch/pull/175067))
- Remove CUDA 12.4 periodic tests ([#175170](https://github.com/pytorch/pytorch/pull/175170))
- Add CUDA 13 periodic tests ([#174850](https://github.com/pytorch/pytorch/pull/174850))
- Remove +ptx from CUDA 13.0 builds ([#175567](https://github.com/pytorch/pytorch/pull/175567))
- Update inductor CI jobs to CUDA 13.0 ([#175826](https://github.com/pytorch/pytorch/pull/175826))
