
# Release Notes worksheet nn_frontend

## nn_frontend
### bc breaking
### deprecation
### new features
### improvements
- Added `bias` argument to `nn` normalization methods (`LayerNorm`, `GroupNorm`, `RMSNorm`, etc.) ([#176573](https://github.com/pytorch/pytorch/pull/176573))
- Improved `MultiMarginLoss` error message for inconsistent target size ([#174072](https://github.com/pytorch/pytorch/pull/174072))
- Added `enable_gqa` flag to `varlen_attn` ([#179468](https://github.com/pytorch/pytorch/pull/179468))
- Allowed `eps=0` in `batch_norm` during eval mode ([#175508](https://github.com/pytorch/pytorch/pull/175508))
- Added meta device support in `trunc_normal_` initialization ([#176240](https://github.com/pytorch/pytorch/pull/176240))
### bug fixes
- Fixed `trunc_normal_` low precision issue when used with half-precision dtypes ([#174997](https://github.com/pytorch/pytorch/pull/174997))
- Added dtype check to `nll_loss` meta function to prevent invalid input types ([#175151](https://github.com/pytorch/pytorch/pull/175151))
- Fixed numerical inconsistency in `Conv3d.reset_parameters` for channels_last format ([#175990](https://github.com/pytorch/pytorch/pull/175990))
- Fixed `MSELoss` failing to compute gradients when inputs have different dtypes ([#175743](https://github.com/pytorch/pytorch/pull/175743))
- Fixed `GroupNorm` backward correctness bug on AMD wavefront-64 GPUs ([#178872](https://github.com/pytorch/pytorch/pull/178872))
- Fixed `nn.functional.pad` compile crash with deterministic mode and replication padding ([#177166](https://github.com/pytorch/pytorch/pull/177166))
- Fixed FA4 integration in varlen attention ([#177675](https://github.com/pytorch/pytorch/pull/177675))
- Fixed issue #110505 ([#176559](https://github.com/pytorch/pytorch/pull/176559))
### performance
- Added NEON implementation of `interpolate` for bilinear/bicubic with antialias on ChannelsLast RGB images on ARM ([#176217](https://github.com/pytorch/pytorch/pull/176217))
- Parallelized `upsample_bicubic2d` across batch/channel dimensions — 4-43x speedup for VLM position embedding resizing ([#174578](https://github.com/pytorch/pytorch/pull/174578))
- Freed q, k, v early in `multi_head_attention_forward` to reduce peak memory usage ([#178452](https://github.com/pytorch/pytorch/pull/178452))
### docs
- Fixed varlen attention docstring ([#175261](https://github.com/pytorch/pytorch/pull/175261))
- Fixed device mismatch in `scaled_dot_product_attention` docstring example ([#178684](https://github.com/pytorch/pytorch/pull/178684))
- Fixed incorrect `attn_mask` shape in `scaled_dot_product_attention` docs ([#177999](https://github.com/pytorch/pytorch/pull/177999))
- Clarified `RMSNorm` `eps` parameter default behavior ([#173887](https://github.com/pytorch/pytorch/pull/173887))
- Improved `Conv2d` docs: clarified math variable to parameter mapping and fixed cross-correlation link ([#178965](https://github.com/pytorch/pytorch/pull/178965))
### devs
- Added flop registration to varlen attention ([#179500](https://github.com/pytorch/pytorch/pull/179500))
### not user facing
- [xpu][test][1/N] Enable tests of test_nn.py on Intel GPU - instantiate TestNN with instantiate_device_type_tests ([#166396](https://github.com/pytorch/pytorch/pull/166396))
- [rnn] Update condition in test_rnn_check_device ([#178981](https://github.com/pytorch/pytorch/pull/178981))
- [Testing] Add guard-page test for uint8 interpolate overread ([#180219](https://github.com/pytorch/pytorch/pull/180219))
- Add AArch64 xfails for inductor, nn, jit, and linalg tests ([#177584](https://github.com/pytorch/pytorch/pull/177584))
### security
