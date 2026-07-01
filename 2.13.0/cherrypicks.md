# cherry picks

## bc breaking

## deprecation

## new features

## improvements
### MPS
- Migrate argmin/argmax from MPSGraph to Metal kernels ([#188160](https://github.com/pytorch/pytorch/pull/188160))

### Release Engineering
- Bump CUDA 13.0 builds to 13.0.3 ([#187099](https://github.com/pytorch/pytorch/pull/187099))
- Revive CUDA 12.9 nightly binary builds ([#188162](https://github.com/pytorch/pytorch/pull/188162))
## bug fixes
### CUDA
- Fix 32-bit offset overflow in memory-efficient attention forward with `attn_bias` ([#187684](https://github.com/pytorch/pytorch/pull/187684))
- Fix bmm outer product Triton launch on non-current CUDA device ([#187983](https://github.com/pytorch/pytorch/pull/187983))
### FX
- Preserve FX graph cache guard provenance ([#187666](https://github.com/pytorch/pytorch/pull/187666))
### XPU
- Include `kernel_compile_result.h` in the AOTI `xpu.h` header ([#187417](https://github.com/pytorch/pytorch/pull/187417))
- Handle `pyzes` import failures gracefully on machines without a Level Zero driver ([#187422](https://github.com/pytorch/pytorch/pull/187422))
- Fix LSTM oneDNN integration ([#187560](https://github.com/pytorch/pytorch/pull/187560))
### Release Engineering
- Fix Windows libtorch x86_64 and arm64 packages overwriting each other ([#187973](https://github.com/pytorch/pytorch/pull/187973))

## performance

## docs

## devs
### Build Frontend
- Fix `build_with_debinfo.py` broken by `CONFIGURE_DEPENDS` globbing ([#188192](https://github.com/pytorch/pytorch/pull/188192))

## security

## Untopiced

## not user facing
### Release Engineering
- Apply release-only changes to the 2.13 branch ([#186959](https://github.com/pytorch/pytorch/pull/186959))
- Fetch tags in the unified manywheel build job so release tags are detected ([#187001](https://github.com/pytorch/pytorch/pull/187001))
- Full git fetch on tag pushes so release manywheel builds detect the tag ([#187055](https://github.com/pytorch/pytorch/pull/187055))
- Followup: full git fetch on tag pushes so release manywheel builds detect the tag ([#187058](https://github.com/pytorch/pytorch/pull/187058))
- Full git fetch on tag pushes so macOS release wheel builds detect the tag ([#187172](https://github.com/pytorch/pytorch/pull/187172))
- Make `spmd_type` a CI rather than CD dependency ([#187345](https://github.com/pytorch/pytorch/pull/187345))
- Remove setuptools upper bound ([#188190](https://github.com/pytorch/pytorch/pull/188190))
- Release-only changes required for CUDA 12.9 builds ([#188409](https://github.com/pytorch/pytorch/pull/188409))
### XPU
- Update torch-xpu-ops commit pin ([#186978](https://github.com/pytorch/pytorch/pull/186978))
- Skip `TestMultiprocessingDeviceType` on XPU due to lack of IPC support ([#187416](https://github.com/pytorch/pytorch/pull/187416))
