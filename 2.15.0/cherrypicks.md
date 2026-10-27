# cherry picks

Commits that reached release/2.15 after the branch cut through cherry-picks (44 commits, through the final RC rc7 plus two later picks; checked at `30c000d9a4b266157c9515acd195083898a00787`).
User-facing entries live in their area worksheets so merge.py includes them; this file records where each went.

## added to worksheets

- #192774: `done/result_cpp_frontend.md`, new features
- #200020: `done/result_distributed (c10d).md`, new features
- #201347: `todo/result_build_frontend.md`, bug fixes
- #200771: `done/result_distributed (c10d).md`, bug fixes
- #200585: `done/result_distributed (c10d).md`, bug fixes
- #200412: `todo/result_export.md`, bug fixes
- #199871, #200442: `todo/result_inductor.md`, bug fixes
- #201029: `todo/result_inductor.md`, bug fixes
- #200536, #200776, #200649: `todo/result_mps.md`, bug fixes
- #200765, #200564: `todo/result_mps.md`, bug fixes
- #200758, #200657, #200659: `todo/result_mps.md`, bug fixes
- #201060: `todo/result_mps.md`, bug fixes
- #199878: `todo/result_python_frontend.md`, bug fixes
- #200294: `done/result_releng.md`, bug fixes
- #197061: `done/result_xpu.md`, bug fixes
- #200995: `todo/result_cuda.md`, performance
- #199758, #199933: `todo/result_mps.md`, performance
- #200956: `todo/result_python_frontend.md`, security

## not user facing

### Release Engineering
- Release-only changes applied to the release/2.15 branch ([#199819](https://github.com/pytorch/pytorch/pull/199819))
- Build triton as abi3 wheels for Python 3.12+ in CI ([#197321](https://github.com/pytorch/pytorch/pull/197321))
- Revert the CUDA 13.4 `ptxas` bundling workaround for triton ([#199792](https://github.com/pytorch/pytorch/pull/199792))
- Remove redundant CPython 3.15 builds from manylinux Docker images ([#200653](https://github.com/pytorch/pytorch/pull/200653))
- Reclaim workspace ownership before checkout on XPU CI runners ([#200305](https://github.com/pytorch/pytorch/pull/200305))
- Locate `vcvarsall.bat` with `vswhere` on Windows arm64 CI ([#200250](https://github.com/pytorch/pytorch/pull/200250))
- Pin `pyarrow<26` in the torchtitan CI test on release/2.15 ([#200923](https://github.com/pytorch/pytorch/pull/200923))

### Reverts on release/2.15
- Revert cache-key prefetch at `torch.compile()` time: revert of #198747 on release/2.15, background source-hashing claim removed ([#202168](https://github.com/pytorch/pytorch/pull/202168))
- Revert "[aoti] Use the proxy executor for _quantized ops without a C shim": revert of #199336 on release/2.15, original entry removed ([#199960](https://github.com/pytorch/pytorch/pull/199960))
- Revert "Preserve channels_last_3d in InstanceNorm3d": revert of #199112 on release/2.15, original entry removed ([#199961](https://github.com/pytorch/pytorch/pull/199961))
- Revert "Prune unused view ops from proxy tensor traces": revert of #198515 on release/2.15, original entry removed ([#199962](https://github.com/pytorch/pytorch/pull/199962))
- Revert "[aoti] Clone outputs that alias a constant through a fallback view op": revert of #199323 on release/2.15, original entry removed ([#199963](https://github.com/pytorch/pytorch/pull/199963))

### ROCm
- Remove stale exp/silu Inductor xfails after Triton 3.9 ([#199926](https://github.com/pytorch/pytorch/pull/199926))

### Distributed (pipeline)
- Use a microbatched reference in `test_schedule_releases_output_before_backward` ([#199624](https://github.com/pytorch/pytorch/pull/199624))

### MPS
- Update MPS minimum-OS and missing-GPU error messages: already covered in result_mps.md; device availability still does not enforce the macOS 15 requirement ([#200062](https://github.com/pytorch/pytorch/pull/200062))

### XPU
- Update the torch-xpu-ops commit pin: already covered in result_xpu.md ([#200223](https://github.com/pytorch/pytorch/pull/200223))
- Update the torch-xpu-ops commit pin on release/2.15 ([#201064](https://github.com/pytorch/pytorch/pull/201064))
- Update OMIX to 0.4.1 and pyzes to 0.1.3 on release/2.15 ([#201079](https://github.com/pytorch/pytorch/pull/201079))
- Update the torch-xpu-ops commit pin on release/2.15 to revert a kernel refactor that caused nearest-neighbor upsampling correctness regressions ([#201553](https://github.com/pytorch/pytorch/pull/201553))
