# cherry picks

## bc breaking

## deprecation

## new features

## improvements
### torch.nn
- Split onehot checks for CPU and accelerators ([#181211](https://github.com/pytorch/pytorch/pull/181211))
### Release Engineering
- Make CUDA 13.0 cross-compilation work ([#181287](https://github.com/pytorch/pytorch/pull/181287))
### Ahead-Of-Time Inductor (AOTI)
- Call latest c_shim version for versioned fallback ops ([#181548](https://github.com/pytorch/pytorch/pull/181548))
- Add BC-safe c_shim v2 for `_scaled_dot_product_attention_math_for_mps` `enable_gqa` ([#181549](https://github.com/pytorch/pytorch/pull/181549))
### MPS
- Add `enable_gqa` parameter to SDPA MPS meta registration ([#181550](https://github.com/pytorch/pytorch/pull/181550))
### C++ Frontend
- Reland `at::Tag` header-only changes and add a `library.def` override for tags ([#181608](https://github.com/pytorch/pytorch/pull/181608))

## bug fixes
### Inductor
- Include `lazy_triton_compile.h` in the XPU `cpp_wrapper` header ([#180815](https://github.com/pytorch/pytorch/pull/180815))
- Fix cudagraphs compatibility with the current stream ([#180916](https://github.com/pytorch/pytorch/pull/180916))
- Revert native API stamp-out for BMM outer product ([#181658](https://github.com/pytorch/pytorch/pull/181658))
- Fix dynamic shape tile issue ([#181795](https://github.com/pytorch/pytorch/pull/181795))
- Avoid raw stream name collisions in Inductor ([#182178](https://github.com/pytorch/pytorch/pull/182178))
### Dynamo
- Fix `cuda_stream` pointer extraction for generic `torch.Stream` ([#181019](https://github.com/pytorch/pytorch/pull/181019))
- Warn instead of erroring on `fullgraph=True` fallback to eager ([#181940](https://github.com/pytorch/pytorch/pull/181940))
### MPS
- Fix sliced `channels_last` tensor handling ([#181107](https://github.com/pytorch/pytorch/pull/181107))
- Fix SDPA wrong output for permuted q/k/v with `B > 1` ([#181886](https://github.com/pytorch/pytorch/pull/181886))
- Fix bool mask handling in the 1-pass SDPA decode kernel ([#182311](https://github.com/pytorch/pytorch/pull/182311))
### FX
- Fix the `MetaProxy` error caused by skipping dispatch ([#181170](https://github.com/pytorch/pytorch/pull/181170))
- Preserve `FakeScriptObject` for value-type opaques ([#181454](https://github.com/pytorch/pytorch/pull/181454))
### Linear Algebra Frontend
- Revert pytorch/pytorch#172340 ([#181364](https://github.com/pytorch/pytorch/pull/181364))
### Distributed FSDP
- Revert PR 178223 to bring back all-gather prefetching ([#181669](https://github.com/pytorch/pytorch/pull/181669))
### Distributed FSDP2
- Revert "[FSDP2] add fqn to communication ops" ([#182157](https://github.com/pytorch/pytorch/pull/182157))
### Release Engineering
- Fix stale `PYTORCH_RELEASES_CODE_CC` dict ([#182369](https://github.com/pytorch/pytorch/pull/182369))

## performance
### CPU (AArch64)
- Add TLS `stack_bounds` to avoid expensive reads ([#181137](https://github.com/pytorch/pytorch/pull/181137))

## docs
### Release Engineering
- Skip `llms-full.txt` during Sphinx builds and generate it in nightly push ([#181070](https://github.com/pytorch/pytorch/pull/181070))
- Disable `llms-full.txt` ([#181141](https://github.com/pytorch/pytorch/pull/181141))
- Fix link to C++ torch stable docs ([#181613](https://github.com/pytorch/pytorch/pull/181613))
- Use full clone for docs build to fix nightly hang ([#181661](https://github.com/pytorch/pytorch/pull/181661))
- Add checkout-mode input to setup-linux action ([#181702](https://github.com/pytorch/pytorch/pull/181702))
- Make docs build behave the same for `push=true` and `push=false` ([#181921](https://github.com/pytorch/pytorch/pull/181921))
- Reduce sidebar navigation size for generated API pages ([#181943](https://github.com/pytorch/pytorch/pull/181943))

## devs

## security

## Untopiced

## not user facing
### Release Engineering
- Enable fetch-tags in checkout-pytorch to fix release tag detection ([#180508](https://github.com/pytorch/pytorch/pull/180508))
- Increase Python docs build timeout to 45 minutes ([#180847](https://github.com/pytorch/pytorch/pull/180847))
- Remove cu132-to-cu130 wheel install fallback in Dockerfile ([#181577](https://github.com/pytorch/pytorch/pull/181577))
### ROCm
- Fix `inline_asm_elementwise` for ROCm ([#180600](https://github.com/pytorch/pytorch/pull/180600))
- Add ROCm-specific XFAILs for `torchinductor_opinfo_property` ([#180687](https://github.com/pytorch/pytorch/pull/180687))
- Update `scaled_mm` DeepSeek error message ([#180690](https://github.com/pytorch/pytorch/pull/180690))
- Enable ROCm swizzle checks and update `scaled_mm` swizzle tests ([#180691](https://github.com/pytorch/pytorch/pull/180691))
- Resolve timeouts from hipBLASLt module creation during graph capture ([#180692](https://github.com/pytorch/pytorch/pull/180692))
- Fix `evaluate_platform_supports_fp8` false-positive ([#180715](https://github.com/pytorch/pytorch/pull/180715))
- Run `test_scaled_mm_deepseek_error_messages` on MI350 architecture ([#180897](https://github.com/pytorch/pytorch/pull/180897))
- Remove previously retained Triton 3.7 skip for `torchinductor_opinfo` test ([#180903](https://github.com/pytorch/pytorch/pull/180903))
- Skip `test_autoheuristic` in code; the test was already disabled by issue ([#180927](https://github.com/pytorch/pytorch/pull/180927))
### Distributed (c10d)
- Fix `groupName` in `IntraNodeComm` ([#180809](https://github.com/pytorch/pytorch/pull/180809))
- Skip NCCL suspend/get_memory_stats/resume tests for NCCL older than 2.29.7 ([#180693](https://github.com/pytorch/pytorch/pull/180693))
### XPU
- Enable `bmm_outer_product` Triton override for XPU ([#180816](https://github.com/pytorch/pytorch/pull/180816))
- Update torch-xpu-ops commit pin ([#180965](https://github.com/pytorch/pytorch/pull/180965))
### Inductor
- Fix `SymBool` pickling issue with `torch.cond` ([#180934](https://github.com/pytorch/pytorch/pull/180934))
- Fix Triton crash in mixed-device case for BMM ([#181294](https://github.com/pytorch/pytorch/pull/181294))
- Avoid failing on Triton kernels in pickling errors ([#181751](https://github.com/pytorch/pytorch/pull/181751))
### Dynamo
- Filter aliased intermediates in `autograd.Function` forward tracing ([#180964](https://github.com/pytorch/pytorch/pull/180964))
- Save XPU autocast state in Dynamo global state ([#181349](https://github.com/pytorch/pytorch/pull/181349))
- Disable dispatch modes when pickling AOTAutograd cache entries ([#181381](https://github.com/pytorch/pytorch/pull/181381))
- Disable recursive dict tag optimization ([#181925](https://github.com/pytorch/pytorch/pull/181925))
