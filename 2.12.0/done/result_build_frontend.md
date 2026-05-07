
# Release Notes worksheet build_frontend

## build_frontend
### bc breaking
- Strengthened SVE compile check in `FindARM.cmake`, which may reject previously accepted but incorrect SVE configurations ([#176646](https://github.com/pytorch/pytorch/pull/176646))
- Updated minimum CUDA version required to build PyTorch to 12.1 ([#178925](https://github.com/pytorch/pytorch/pull/178925))
- Enforced C++20 minimum in CMake build files ([#178662](https://github.com/pytorch/pytorch/pull/178662))
### deprecation
### new features
### improvements
- Simplified SVE256 detection ([#176247](https://github.com/pytorch/pytorch/pull/176247))
- Removed ARMv7 checks ([#176645](https://github.com/pytorch/pytorch/pull/176645))
### bug fixes
- Fixed `TORCH_BUILD_VERSION` not updating when `version.txt` changes ([#176167](https://github.com/pytorch/pytorch/pull/176167))
### performance
### docs
### devs
- Included `CMAKE_CUDA_FLAGS` in build settings report ([#175236](https://github.com/pytorch/pytorch/pull/175236))
- Enforced C++20 for XPU SYCL device compilation ([#179497](https://github.com/pytorch/pytorch/pull/179497))
### not user facing
- Add license for bundled libomp.dylib ([#174400](https://github.com/pytorch/pytorch/pull/174400))
- [CMake] Bump C++ version to 20 ([#167929](https://github.com/pytorch/pytorch/pull/167929))
### security
