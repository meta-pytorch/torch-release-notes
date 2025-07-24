# cherry picks
## bc breaking
### cuda
- Add warning about removed sm50 and sm60 arches ([#158478](https://github.com/pytorch/pytorch/pull/158478), [#158744](https://github.com/pytorch/pytorch/pull/158744))

## deprecation

## new features

## improvements
### cuda
- Don't error out in `empty_cache` under mempool context ([#158180](https://github.com/pytorch/pytorch/pull/158180))

### dynamo
- Do not issue `lru_cache` warning for functions in the top-level `torch` namespace ([#157718](https://github.com/pytorch/pytorch/pull/157718))

### fx
- Add flag to `fx.passes.split_module` to normalize input names ([#157793](https://github.com/pytorch/pytorch/pull/157793))

### inductor (aoti)
- Support for device-side TMA ([#157241](https://github.com/pytorch/pytorch/pull/157241))

## bug fixes
### cuda
- Fix IMAs from invalid `_foreach_copy` indexing ([#158238](https://github.com/pytorch/pytorch/pull/158238))

### cpu (aarch64)
- Fix segfaults by disabling strict-aliasing in `GridSamplerKernel` for GCC 12 and above ([#158445](https://github.com/pytorch/pytorch/pull/158445))

### distributed
- Revert "Turn on compile with NVSHMEM (#154538)" ([#158040](https://github.com/pytorch/pytorch/pull/158040))

### distributed (tensor parallel)
- Turn async-TP applicability asserts back into silent skips ([#158736](https://github.com/pytorch/pytorch/pull/158736))

### dynamo
- Fix einops x torch.compile interaction ([#157754](https://github.com/pytorch/pytorch/pull/157754))
- Use proper sources for constructing dataclass defaults ([#158689](https://github.com/pytorch/pytorch/pull/158689))
- Fix source for `lru_cache` method ([#157308](https://github.com/pytorch/pytorch/pull/157308))
- Fix bug in `dict(mapping_proxy)` ([#157515](https://github.com/pytorch/pytorch/pull/157515))
- Revert "[Dynamo] Allow inlining into AO quantization modules (#152934)" ([#158677](https://github.com/pytorch/pytorch/pull/158677))
- Handle missing `tags` attribute for fake tensors (#156689) ([#157519](https://github.com/pytorch/pytorch/pull/157519))

### inductor
- Sanitize triple-quoted docstrings in triton kernel definitions ([#157454](https://github.com/pytorch/pytorch/pull/157454))
- Add stride check for `attn_mask` on non-cpu device ([#158618](https://github.com/pytorch/pytorch/pull/158618))

### mps
- Switch Cholesky decomp to column-wise ([#158237](https://github.com/pytorch/pytorch/pull/158237))
- Reimplement `tri[ul]` as Metal shaders ([#158867](https://github.com/pytorch/pytorch/pull/158867))
- Fix `index_kernel` for large tensors ([#158239](https://github.com/pytorch/pytorch/pull/158239))

### onnx
- [ONNX] Fix conversion of attention - 4D ([#157509](https://github.com/pytorch/pytorch/pull/157509))

### python_frontend
- Unify `torch.tensor` and `torch.ops.aten.scalar_tensor` behavior ([#158655](https://github.com/pytorch/pytorch/pull/158655))

## performance
### autograd
- Avoid creating and recording event when unnecessary ([#157914](https://github.com/pytorch/pytorch/pull/157914))

### mps
- Revert `cumsum`/`cumprod` to `MPSGraph` implementation ([#157494](https://github.com/pytorch/pytorch/pull/157494))

## docs
### distributed
- Document `get_default_backend_for_device` ([#158236](https://github.com/pytorch/pytorch/pull/158236))

## devs

## Untopiced

## security

## not user facing
- Move out super large one off foreach_copy test ([#158880](https://github.com/pytorch/pytorch/pull/158880))
- [inductor][static launcher] Skip correctness test for test_floats ([#157200](https://github.com/pytorch/pytorch/pull/157200))
- [ez] Disable some failing periodic tests ([#157560](https://github.com/pytorch/pytorch/pull/157560))
- Add einops x torch.compile testing in PyTorch CI (#157416) ([#157588](https://github.com/pytorch/pytorch/pull/157588))
- Pull latest Sphinx theme (#158595) ([#158673](https://github.com/pytorch/pytorch/pull/158673))
- Cherry pick PR 158746 ([#158801](https://github.com/pytorch/pytorch/pull/158801))
- [cherry-pick][Docker builds] Move from Miniconda to Miniforge (#158370) ([#158756](https://github.com/pytorch/pytorch/pull/158756))
- [release] Triton pin update to 3.4 ([#157752](https://github.com/pytorch/pytorch/pull/157752))
- Update triton version to 3.4 ([#156890](https://github.com/pytorch/pytorch/pull/156890))
- [ONNX] Bump onnxscript api for torch 2.8 ([#157137](https://github.com/pytorch/pytorch/pull/157137))
- Fix cuda 12.9 aarch64 GPU builds. Update CUDA_STABLE variable.  ([#157641](https://github.com/pytorch/pytorch/pull/157641))
- Revert "Update triton version to 3.4" ([#157471](https://github.com/pytorch/pytorch/pull/157471))
- [cherry-pick] revert #156517 on release 2.8 ([#156768](https://github.com/pytorch/pytorch/pull/156768))
- [PowerPC] Fixed build issue for vsx vec256 complexfloat and scaled_mm_out_cpu  ([#157422](https://github.com/pytorch/pytorch/pull/157422))
- Fix macOS build with `USE_MPS=OFF` ([#156932](https://github.com/pytorch/pytorch/pull/156932))
- Remove +PTX from CUDA 12.8 builds ([#157634](https://github.com/pytorch/pytorch/pull/157634))
- Add sm_70 arch for linux cuda 12.8 and 12.9 builds ([#157968](https://github.com/pytorch/pytorch/pull/157968))
- Add sm_70 to windows 12.9 build ([#158265](https://github.com/pytorch/pytorch/pull/158265))
- [aarch64] Add sm_80 to CUDA SBSA build ([#158118](https://github.com/pytorch/pytorch/pull/158118))
- [ROCm] Bump AOTriton to 0.10b ([#156845](https://github.com/pytorch/pytorch/pull/156845))
- [aarch64] Add back NCCL lib to cuda arm wheel ([#157105](https://github.com/pytorch/pytorch/pull/157105))
- Fix environment and push env var for docker image builds for binary builds  ([#156916](https://github.com/pytorch/pytorch/pull/156916))
- [cherry pick] revert #155412 ([#156757](https://github.com/pytorch/pytorch/pull/156757))
- [RELEASE 2.8] Release only changes ([#156728](https://github.com/pytorch/pytorch/pull/156728))
- [cherry-pick][inductor][triton] Update HAS_WARP_SPEC to check triton.Config params. Update Triton Hash to top of release/3.4.x stack ([#158646](https://github.com/pytorch/pytorch/pull/158646))
- [cherry-pick] revert #156552 ([#156767](https://github.com/pytorch/pytorch/pull/156767))
- cherrypick revert of #152932 for release 2.8 ([#158031](https://github.com/pytorch/pytorch/pull/158031))
- [cherry-pick] Organize BUCK for torch/standalone and Rename torch::standalone to headeronly ([#157418](https://github.com/pytorch/pytorch/pull/157418))
- Cleanup leftover miniconda brew installation ([#157567](https://github.com/pytorch/pytorch/pull/157567))
- Fix GITHUB_OUTPUT syntax in create_release.yml workflow ([#157539](https://github.com/pytorch/pytorch/pull/157539))
- Revert "Add NVSHMEM to PYTORCH_EXTRA_INSTALL_REQUIREMENTS (#154568)" ([#158039](https://github.com/pytorch/pytorch/pull/158039))
- [CUDA] Use runtime driver API for cuStreamWriteValue32 ([#158585](https://github.com/pytorch/pytorch/pull/158585))
- [Release Only] Remove nvshmem from list of preload libraries ([#158925](https://github.com/pytorch/pytorch/pull/158925))
- [cherry-pick][release 2.8] Update OpenBLAS commit  (#151547) ([#158243](https://github.com/pytorch/pytorch/pull/158243))
- [cherry-pick] temporarily disabling generation of weblinks for torch v2.8 & removing string literals for weblink generation ([#157951](https://github.com/pytorch/pytorch/pull/157951))

## Added to final.md directly
