# Miscategorized commits

Welcome to the Pool of Miscategorized commits.
Add any commits that were miscategorized for your domain below.
Handle any commits that actually do belong to your domain and remove them from this list.

## Untopiced
- [fx] Add is_fx_symbolic_tracing flag ([#161385](https://github.com/pytorch/pytorch/pull/161385))
- [ROCm] Add FP8 rowwise support to _scaled_grouped_mm + Submodule update ([#159075](https://github.com/pytorch/pytorch/pull/159075))
- [CPU] Support GQA for flash attention ([#157893](https://github.com/pytorch/pytorch/pull/157893))
- Improve error message for torch.binomial enforcing float inputs ([#157658](https://github.com/pytorch/pytorch/pull/157658))
- Detach tensor before clone in SGD optimiser and other code ([#159204](https://github.com/pytorch/pytorch/pull/159204))
- Feature: Implement support for `cudnn_batch_norm_out` kernel to replace the autogen approach. ([#123020](https://github.com/pytorch/pytorch/pull/123020))

Serialization:
- Improve error message for weight-only load errors ([#159935](https://github.com/pytorch/pytorch/pull/159935))

StableABI:
- Add pad and narrow to torch/csrc/stable/ops.h ([#159328](https://github.com/pytorch/pytorch/pull/159328))
- Add getCurrentDeviceIndex to torch::stable::accelerator ([#160453](https://github.com/pytorch/pytorch/pull/160453))
- Add new_zeros dtype variant to the shim and as a stable op ([#161597](https://github.com/pytorch/pytorch/pull/161597))
- Update torch::stable::Tensor() default constructor ([#159507](https://github.com/pytorch/pytorch/pull/159507))
- Add beginnings of torch::stable::accelerator ([#159679](https://github.com/pytorch/pytorch/pull/159679))
- Port amax to stable ABI ([#160214](https://github.com/pytorch/pytorch/pull/160214))
- Add new_empty (with dtype argument only) to torch::stable ([#159508](https://github.com/pytorch/pytorch/pull/159508))
- Enable generating generic c_shim that doesn't bypass dispatcher ([#158974](https://github.com/pytorch/pytorch/pull/158974))
- Cut a version of TORCH_ERROR_CODE_CHECK in headeronly from AOTI ([#159604](https://github.com/pytorch/pytorch/pull/159604))

MPS:
- [MPS] Add boilerplate sparse code support ([#157238](https://github.com/pytorch/pytorch/pull/157238))
- Add `avg_pool3d` for MPS ([#158877](https://github.com/pytorch/pytorch/pull/158877))
- [MPS] Add max_unpool1d/2d/3d ([#159789](https://github.com/pytorch/pytorch/pull/159789))
- Add `max_pool3d` for MPS ([#156467](https://github.com/pytorch/pytorch/pull/156467))
- Add `max_pool3d` backward pass for MPS ([#157498](https://github.com/pytorch/pytorch/pull/157498))
- Add `avg_pool3d` backward pass for MPS ([#159089](https://github.com/pytorch/pytorch/pull/159089))
- Enable _int_mm on Intel GPU ([#157769](https://github.com/pytorch/pytorch/pull/157769))

## not user facing
- Fix Pandas version mismatch upon reinstalling numpy ([#158584](https://github.com/pytorch/pytorch/pull/158584))
