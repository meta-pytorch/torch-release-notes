
# Release Notes worksheet autograd_frontend

## autograd_frontend
### bc breaking
### deprecation
### new features
### improvements
- Implemented `narrow_copy` derivative ([#175609](https://github.com/pytorch/pytorch/pull/175609))
- Implemented higher-order derivatives for `grid_sample` ([#177487](https://github.com/pytorch/pytorch/pull/177487))
- Implemented backward and forward AD for `torch.aminmax` ([#175215](https://github.com/pytorch/pytorch/pull/175215))
- Exposed `num_splits` in varlen attention to allow disabling split_kv ([#176905](https://github.com/pytorch/pytorch/pull/176905))
- Added user `AutoNamingMode` support in Selective Activation Checkpointing ([#175348](https://github.com/pytorch/pytorch/pull/175348))
- Refactored `torch.utils.checkpoint` to no longer use `autograd.Function` for saving inputs ([#174327](https://github.com/pytorch/pytorch/pull/174327))
### bug fixes
- Fixed `torch.trace` backward for non-square matrices ([#175068](https://github.com/pytorch/pytorch/pull/175068))
- Added explicit error when `layer_norm` computes 3rd order derivatives ([#176234](https://github.com/pytorch/pytorch/pull/176234))
- Fixed `_wrap_sync_node` to replace deps in output node's nested args ([#178471](https://github.com/pytorch/pytorch/pull/178471))
- Fixed thread-unsafe lazy init of `setup_context` cache ([#179475](https://github.com/pytorch/pytorch/pull/179475))
### performance
- Used non-blocking copy in `save_on_cpu` pack hook for faster activation offloading ([#175421](https://github.com/pytorch/pytorch/pull/175421))
### docs
### devs
- Registered `numel`, `dim`, `get_device`, `storage_offset`, `is_contiguous` in `native_functions.yaml` ([#177200](https://github.com/pytorch/pytorch/pull/177200))
### not user facing
- Replace PyObject_Type with Py_TYPE ([#178835](https://github.com/pytorch/pytorch/pull/178835))
### security
