
# Release Notes worksheet caffe2

## caffe2
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
- Enabled hipsparselt in caffe2 HIP builds for ROCm ([#175810](https://github.com/pytorch/pytorch/pull/175810))
- Fixed pybind11 3.0.3 ambiguous return type deduction in caffe2 ([#179277](https://github.com/pytorch/pytorch/pull/179277))
### not user facing
- [rocm][7.0/7.2] Fix [[nodiscard]] build errors and BUCK deps across comms, gloo, caffe2 (#176671) ([#176671](https://github.com/pytorch/pytorch/pull/176671))
- [python/3.10 removal] Remove CPython 3.10 holdback for caffe2/test/distributed/elastic/rendezvous (#178071) ([#178071](https://github.com/pytorch/pytorch/pull/178071))
- [pybind11][codemod] Migrate PYBIND11_OVERLOAD to PYBIND11_OVERRIDE in caffe2/torch distributed ([#178876](https://github.com/pytorch/pytorch/pull/178876))
- [caffe2] Remove unused batch_box_cox perfkernel files ([#179515](https://github.com/pytorch/pytorch/pull/179515))
- [fbandroid][buckconfig removal] fbcode/caffe2/buckbuild.bzl (#178206) ([#178206](https://github.com/pytorch/pytorch/pull/178206))
### security
