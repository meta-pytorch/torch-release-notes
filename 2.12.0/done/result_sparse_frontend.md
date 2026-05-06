
# Release Notes worksheet sparse_frontend

## sparse_frontend
### bc breaking
### deprecation
### new features
### improvements
- Implemented `clone` operator for semi-structured sparse tensors ([#174991](https://github.com/pytorch/pytorch/pull/174991))
- Allowed semi-structured sparse tensors to be instantiated with `alg_id` ([#178659](https://github.com/pytorch/pytorch/pull/178659))
- Enabled FP8 semi-structured sparsity on ROCm via hipSPARSELt ([#179310](https://github.com/pytorch/pytorch/pull/179310))
### bug fixes
- Fixed `torch.bmm(COO, Dense)` memory misalignment on CUDA ([#175347](https://github.com/pytorch/pytorch/pull/175347))
### performance
- Reduced CPU overhead in sparse operations for improved performance ([#179193](https://github.com/pytorch/pytorch/pull/179193))
- Minor performance improvements for `torch.bmm(COO, Dense)` ([#175347](https://github.com/pytorch/pytorch/pull/175347))
### docs
### devs
- Included `thrust/pair.h` in each translation unit where `thrust::pair` is used ([#169267](https://github.com/pytorch/pytorch/pull/169267))
- Implemented branch-free and guard-free padding+mul operator for semi-structured sparsity ([#177699](https://github.com/pytorch/pytorch/pull/177699))
### not user facing
- [CUDA] Abate `thrust::distance` deprecation warnings ([#171722](https://github.com/pytorch/pytorch/pull/171722))
- [BE] Use `REGISTER_ALL_CPU_DISPATCH` ([#176255](https://github.com/pytorch/pytorch/pull/176255))
- Fix: treat empty tensors as contiguous in sparse validation ([#178419](https://github.com/pytorch/pytorch/pull/178419))
- fix unit test failure in semi_structure to() op (#178667) ([#178667](https://github.com/pytorch/pytorch/pull/178667))
- [TorchAO][hipSPARSELt] Add alg_id to FP8 semi-structured sparsity benchmark ([#179926](https://github.com/pytorch/pytorch/pull/179926))
### security
