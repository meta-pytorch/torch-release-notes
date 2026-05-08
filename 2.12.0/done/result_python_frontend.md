
# Release Notes worksheet python_frontend

## python_frontend
### bc breaking
### deprecation
### new features
- Introduced `torch.accelerator.Graph` as a unified frontend Graph interface ([#171285](https://github.com/pytorch/pytorch/pull/171285))
### improvements
- Used compiler wrapper when building C++ extensions ([#175696](https://github.com/pytorch/pytorch/pull/175696))
- Updated `uniform` and `normal` sampling on CPU to improve fp16/bf16 results ([#175988](https://github.com/pytorch/pytorch/pull/175988))
- Changed `requires_grad` to `Optional[bool]` in `torch.asarray` ([#170897](https://github.com/pytorch/pytorch/pull/170897))
### bug fixes
- Fixed `torch.isclose` broadcast failure with `equal_nan=True` ([#175244](https://github.com/pytorch/pytorch/pull/175244))
### performance
### docs
- Documented `get_device_capability` and clarified supported dtypes ([#178397](https://github.com/pytorch/pytorch/pull/178397))
- Fixed typo in `index_copy` doc ([#175843](https://github.com/pytorch/pytorch/pull/175843))
- Updated `amax` doc ([#175863](https://github.com/pytorch/pytorch/pull/175863))
- Updated `take_along_dim` doc ([#175844](https://github.com/pytorch/pytorch/pull/175844))
### devs
### not user facing
- Added `is_capturing` method for `c10::Stream` and `torch.Stream` ([#171443](https://github.com/pytorch/pytorch/pull/171443))
- [BE][Ez]: Torch typing improve is_storage ([#177872](https://github.com/pytorch/pytorch/pull/177872))
- [1/N] Use torch._utils.cpu_count ([#178742](https://github.com/pytorch/pytorch/pull/178742))
- [test] Pass a tuple of 2 `SwizzleType` to nvfp4 `scaled_mm_v2` with two scales ([#177625](https://github.com/pytorch/pytorch/pull/177625))
- [BE] Remove `onlyCPU` decorator for nonzero_static tests ([#179591](https://github.com/pytorch/pytorch/pull/179591))
- Initial implementation of stateless RNG APIs ([#177229](https://github.com/pytorch/pytorch/pull/177229))
- Stateless RNG APIs for uniform & normal generation ([#177230](https://github.com/pytorch/pytorch/pull/177230))
### security
