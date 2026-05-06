
# Release Notes worksheet linalg_frontend

## linalg_frontend
### bc breaking
### deprecation
- Deprecated MAGMA backend for `torch.linalg.eigh` on CUDA; now dispatches to cuSolver unconditionally ([#174619](https://github.com/pytorch/pytorch/pull/174619))
- Deprecated MAGMA backend for `torch.linalg.lu_solve` on CUDA; now dispatches to cuSolver/cuBLAS unconditionally ([#174248](https://github.com/pytorch/pytorch/pull/174248))
- Deprecated MAGMA backend for `torch.linalg.cholesky_inverse` on CUDA; now dispatches to cuSolver unconditionally ([#174681](https://github.com/pytorch/pytorch/pull/174681))
- Deprecated MAGMA backend for `torch.linalg.cholesky_solve` on CUDA; now dispatches to cuSolver unconditionally ([#174769](https://github.com/pytorch/pytorch/pull/174769))
### new features
### improvements
- Added `_int_mm` unsigned int8 × signed int8 (u8s8) support on CPU ([#168226](https://github.com/pytorch/pytorch/pull/168226))
- Added FP64 support for TunableOp on ROCm via hipBLASLt ([#178195](https://github.com/pytorch/pytorch/pull/178195))
### bug fixes
- Fixed `addmv` backward pass failure ([#165777](https://github.com/pytorch/pytorch/pull/165777))
- Fixed determinant gradient for 1×1 matrices ([#171225](https://github.com/pytorch/pytorch/pull/171225))
- Fixed `linalg.det` backward for 0-dimensional inputs ([#177498](https://github.com/pytorch/pytorch/pull/177498))
- Fixed `cholesky(upper=True)` on macOS for matrices larger than block size ([#179154](https://github.com/pytorch/pytorch/pull/179154))
### performance
- Improved `torch.cholesky_solve` performance for batched inputs on CUDA via cuSolver ([#175898](https://github.com/pytorch/pytorch/pull/175898))
### docs
### devs
### not user facing
- [BE][Ez]: Add missing std::move on std::make_tuple return calls ([#177982](https://github.com/pytorch/pytorch/pull/177982))
- Ensure test_tensorinv uses well-conditioned inputs ([#175283](https://github.com/pytorch/pytorch/pull/175283))
- [BE]: Add missing reserve() calls ([#175503](https://github.com/pytorch/pytorch/pull/175503))
- [ROCm][CI][TunableOp] Make TunableOp submatrix count backend-aware ([#178448](https://github.com/pytorch/pytorch/pull/178448))
- [UT][ROCm][TunableOp] Fix test_call_count_tunableop to correctly extract kernel names for RDNA ([#177125](https://github.com/pytorch/pytorch/pull/177125))
### security
