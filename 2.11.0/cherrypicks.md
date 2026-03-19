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
- Fix half-precision type mismatches in Metal shader codegen ([#176436](https://github.com/pytorch/pytorch/pull/176436))
### CUDA
- Fix the torch.Stream context manager reentrance ([#176568](https://github.com/pytorch/pytorch/pull/176568))
## performance
## docs
### XPU
- Update previous version 2.10 installation in get start xpu ([#176141](https://github.com/pytorch/pytorch/pull/176141))
### Docs
- Update pytorch_sphinx_theme2 version to 0.4.6 ([#177562](https://github.com/pytorch/pytorch/pull/177562))
## devs
## Untopiced
## security
## not user facing
### Build Frontend
- Remove python constraint on setuptools ([#175577](https://github.com/pytorch/pytorch/pull/175577))
### C++ Frontend
- Let stable::from_blob accept a lambda as deleter ([#175089](https://github.com/pytorch/pytorch/pull/175089))
### CPU
- Fix UB: use vector::resize() instead of reserve() before operator[] access ([#175315](https://github.com/pytorch/pytorch/pull/175315))
- Fix Identity comparability and evalf recursion ([#175975](https://github.com/pytorch/pytorch/pull/175975))
### cuDNN
- Upgrade cuDNN to 9.19 for 12.8 and 13.0 wheels ([#174310](https://github.com/pytorch/pytorch/pull/174310), [#175547](https://github.com/pytorch/pytorch/pull/175547))
### Dynamo
- Update inductor expected accuracy files ([#175041](https://github.com/pytorch/pytorch/pull/175041))
- Skip pytorch_CycleGAN_and_pix2pix from inductor benchmarks ([#175066](https://github.com/pytorch/pytorch/pull/175066))
- Disable einops 0.8.2 check on PyTorch ([#175351](https://github.com/pytorch/pytorch/pull/175351))
- Bump transformers version to 5.2.0 ([#175274](https://github.com/pytorch/pytorch/pull/175274))
- Fix acc failure for vit_base_patch14_dinov2.lvd142m ([#177042](https://github.com/pytorch/pytorch/pull/177042))
- Update vLLM pinned commit ([#175238](https://github.com/pytorch/pytorch/pull/175238))
### Inductor
- Avoid multi-stage for mix-order-red by default ([#176228](https://github.com/pytorch/pytorch/pull/176228))
- Don't unfuse addmm for bf16/fp16 to avoid precision loss ([#176848](https://github.com/pytorch/pytorch/pull/176848))
- Reject non-contiguous subnode fusion in mix-order reduction ([#176131](https://github.com/pytorch/pytorch/pull/176131))
### ROCm
- Forward fix #174087, take 4 ([#175098](https://github.com/pytorch/pytorch/pull/175098))
- Added CUDA check to test_pattern_matcher ([#175092](https://github.com/pytorch/pytorch/pull/175092))
### XPU
- Fix SyclExtension Windows build for oneAPI 2025.3+ breaking change ([#170701](https://github.com/pytorch/pytorch/pull/170701))
### Release Engineering
- Release only changes for 2.11 ([#175091](https://github.com/pytorch/pytorch/pull/175091))
- Fix macOS arm64 libtorch release upload failure ([#175100](https://github.com/pytorch/pytorch/pull/175100))
- Move CUDA 12.8 GPU tests from per-commit trunk to periodic ([#175067](https://github.com/pytorch/pytorch/pull/175067))
- Remove CUDA 12.4 periodic tests ([#175170](https://github.com/pytorch/pytorch/pull/175170))
- Add CUDA 13 periodic tests ([#174850](https://github.com/pytorch/pytorch/pull/174850))
- Remove +ptx from CUDA 13.0 builds ([#175567](https://github.com/pytorch/pytorch/pull/175567))
- Update inductor CI jobs to CUDA 13.0 ([#175826](https://github.com/pytorch/pytorch/pull/175826))
- Upgrade ROCm CI to 7.2 ([#173188](https://github.com/pytorch/pytorch/pull/173188))
- Switch vLLM test and benchmark workflows to CUDA 13.0 ([#175393](https://github.com/pytorch/pytorch/pull/175393))
- Fix pep517 release handling ([#175635](https://github.com/pytorch/pytorch/pull/175635))
- Windows override AMI pre-installed cudnn ([#177027](https://github.com/pytorch/pytorch/pull/177027))
- Unpin cuda-bindings dependencies ([#176042](https://github.com/pytorch/pytorch/pull/176042))
- Stop using G3 runners ([#175938](https://github.com/pytorch/pytorch/pull/175938))
- Add an option to install cuda if required cuda/cudnn on windows AMI do not match ([#177273](https://github.com/pytorch/pytorch/pull/177273))
