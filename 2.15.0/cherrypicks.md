# cherry picks

## bc breaking

## deprecation

## new features

### C++ Frontend
- Add stable ABI conversions for `torch.dtype`/`torch.device` Python objects and a `torch::stable::is_tensor_pyobject` check ([#192774](https://github.com/pytorch/pytorch/pull/192774))

### Distributed (c10d)
- Add `ProcessGroupNCCL.Options.lazy_init` so `nccl` and `nccl-lazy` groups create their communicator on first use instead of allocating ~200 MiB in `new_group` ([#200020](https://github.com/pytorch/pytorch/pull/200020))

## improvements

## bug fixes

### Build Frontend
- Ship `top_level.txt` in wheels again, fixing slow `importlib.metadata.packages_distributions()` calls that delayed importing libraries like `transformers` ([#201347](https://github.com/pytorch/pytorch/pull/201347))

### Distributed (c10d)
- Fix `register_mem_pool(pool, symm=True)` on the `nccl` backend not registering later pool segments as symmetric windows ([#200771](https://github.com/pytorch/pytorch/pull/200771))
- Fix `all_gather` on the `nccl` backend failing with `RuntimeError: shape '[...]' is invalid for input of size 0` when outputs contain zero-element tensors ([#200585](https://github.com/pytorch/pytorch/pull/200585)) (not in the final RC; ships only if another RC is cut)

### Export
- Fix `torch.export.export` raising `GuardOnDataDependentSymNode` for `x[mask] = scalar` when `x` has a data-dependent size ([#200412](https://github.com/pytorch/pytorch/pull/200412))

### Inductor
- Fix wrong results from fusions that dropped non-default kwargs such as `add(..., alpha=a)`; `add` with `alpha != 1` is no longer fused into `addmm` ([#199871](https://github.com/pytorch/pytorch/pull/199871), [#200442](https://github.com/pytorch/pytorch/pull/200442))
- Fix `InductorError: AttributeError: 'NotImplementedType' object has no attribute 'expr'` when fusing a prologue with a `float16`/`bfloat16` cast into a Triton matmul ([#201029](https://github.com/pytorch/pytorch/pull/201029))

### MPS
- Fix `torch.linalg.svd` returning non-orthonormal `U`/`Vh` with `full_matrices=True`, inaccurate results for very small or large entries, and zero `pinv`/`lstsq` for small singular values ([#200536](https://github.com/pytorch/pytorch/pull/200536), [#200776](https://github.com/pytorch/pytorch/pull/200776), [#200649](https://github.com/pytorch/pytorch/pull/200649))
- Fix complex division (and complex `linalg.solve`, `solve_triangular`, `det`) returning NaN or 0 for extreme magnitudes, and complex `pow` returning 0 for every zero base ([#200765](https://github.com/pytorch/pytorch/pull/200765), [#200564](https://github.com/pytorch/pytorch/pull/200564))
- Fix `var`/`std` returning 0 instead of NaN for NaN/Inf inputs, `float16` `addmm` overflowing to `inf` with `beta=0`, and `grouped_mm` silently accepting mismatched dtypes ([#200758](https://github.com/pytorch/pytorch/pull/200758), [#200657](https://github.com/pytorch/pytorch/pull/200657), [#200659](https://github.com/pytorch/pytorch/pull/200659))
- Fix `torch.compile` truncating `int64` constants to 32 bits ([#201060](https://github.com/pytorch/pytorch/pull/201060))

### Python Frontend
- Fix `torch.isfinite` reporting NaN as finite for `float8_e8m0fnu` ([#199878](https://github.com/pytorch/pytorch/pull/199878))

### Release Engineering
- Make Python 3.15 Linux wheels depend on `triton`, so `torch.compile` works on GPU after `pip install torch` ([#200294](https://github.com/pytorch/pytorch/pull/200294))

### XPU
- Fix Inductor treating every XPU kernel that uses scratch memory as spilling registers ([#197061](https://github.com/pytorch/pytorch/pull/197061))

## performance

### CUDA
- Fix a 10-30x slowdown of `gather`, `index_select`, `x[idx]` and `scatter_add` on rows of 16 or 32 bytes ([#200995](https://github.com/pytorch/pytorch/pull/200995))

### MPS
- Speed up `softmax` over a non-innermost dim and `relu`, `clamp_min`, `leaky_relu` and other scalar-argument unary ops on row-strided views ([#199758](https://github.com/pytorch/pytorch/pull/199758), [#199933](https://github.com/pytorch/pytorch/pull/199933))

## docs

## devs

## security

### Python Frontend
- After `import torch.distributed`, `torch.load(weights_only=True)` and `get_unsafe_globals_in_checkpoint` no longer treat builtin exceptions as safe globals (a process-wide allowlist added in 2.14), and loading no longer calls overridden `append`/`extend` on allowlisted `list` subclasses. Checkpoints with pickled exceptions now need `torch.serialization.add_safe_globals`; object collectives are unchanged ([#200956](https://github.com/pytorch/pytorch/pull/200956))

## Untopiced

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
- Revert "[aoti] Use the proxy executor for _quantized ops without a C shim": revert of #199336 on release/2.15, original entry removed ([#199960](https://github.com/pytorch/pytorch/pull/199960))
- Revert "Preserve channels_last_3d in InstanceNorm3d": revert of #199112 on release/2.15, original entry removed ([#199961](https://github.com/pytorch/pytorch/pull/199961))
- Revert "Prune unused view ops from proxy tensor traces": revert of #198515 on release/2.15, original entry removed ([#199962](https://github.com/pytorch/pytorch/pull/199962))
- Revert "[aoti] Clone outputs that alias a constant through a fallback view op": revert of #199323 on release/2.15, original entry removed ([#199963](https://github.com/pytorch/pytorch/pull/199963))

### ROCm
- Remove stale exp/silu Inductor xfails after Triton 3.9 ([#199926](https://github.com/pytorch/pytorch/pull/199926))

### Distributed (pipeline)
- Use a microbatched reference in `test_schedule_releases_output_before_backward` ([#199624](https://github.com/pytorch/pytorch/pull/199624))

### MPS
- Require macOS 15.0+ and report a missing GPU separately: already covered in result_mps.md ([#200062](https://github.com/pytorch/pytorch/pull/200062))

### XPU
- Update the torch-xpu-ops commit pin: already covered in result_xpu.md ([#200223](https://github.com/pytorch/pytorch/pull/200223))
- Update the torch-xpu-ops commit pin on release/2.15 ([#201064](https://github.com/pytorch/pytorch/pull/201064))
- Update OMIX to 0.4.1 and pyzes to 0.1.3 on release/2.15 ([#201079](https://github.com/pytorch/pytorch/pull/201079))
- Update the torch-xpu-ops commit pin on release/2.15 to revert a kernel refactor that caused nearest-neighbor upsampling correctness regressions ([#201553](https://github.com/pytorch/pytorch/pull/201553))
