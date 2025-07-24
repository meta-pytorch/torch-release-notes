# cherry picks
## bc breaking

## deprecation

## new features

## improvements

## bug fixes

## performance

## docs

## devs

## Untopiced
- [Release Only] Remove nvshmem from list of preload libraries (#158925)
- Move out super large one off foreach_copy test (#158880)
- Revert "[Dynamo] Allow inlining into AO quantization modules (#152934)" (#158677)
- [MPS] Switch Cholesky  decomp to column wise (#158237)
- [MPS] Reimplement `tri[ul]` as Metal shaders (#158867)
- Cherry pick PR 158746 (#158801)
- [cherry-pick] Unify torch.tensor and torch.ops.aten.scalar_tensor behavior (#158537) (#158655)
- [Dynamo] Use proper sources for constructing dataclass defaults (#158689)
- Pull latest Sphinx theme (#158595) (#158673)
- [cherry-pick] Fix AArch64 segfaults by disabling strict-aliasing in GridSamplerKernel for GCC 12 and above (#158445)
- [async-TP] Turn asserts back into silent skips (#158736)
- [cherry-pick][Docker builds] Move from Miniconda to Miniforge (#158370) (#158756)
- [cherry-pick][release 2.8] Update OpenBLAS commit  (#151547) (#158243)
- [Reland] Add warning about removed sm50 and sm60 arches (#158744)
- [cherry-pick] temporarily disabling generation of weblinks for torch v2.8 & removing string literals for weblink generation (#157951)
- Add stride check for attn_mask on non-cpu device (#158618)
- [CUDA] Use runtime driver API for cuStreamWriteValue32 (#158585)
- [cherry-pick][inductor][triton] Update HAS_WARP_SPEC to check triton.Config params. Update Triton Hash to top of release/3.4.x stack (#158646)
- Add warning about removed sm50 and sm60 arches (#158478)
- Add flag to fx.passes.split_module to normalize input names (#157793)
- [MPS] Fix `index_kernel` for large tensors (#158239)
- Fix einops x torch.compile interaction (#157754)
- Fix #156261 _foreach_copy indexing (#158238)
- Add sm_70 to windows 12.9 build (#158265)
- docs: add get_default_backend_for_device to distributed documentation (#158236)
- don't error out in empty_cache under mempool context (#158180)
- [autograd] Avoid creating and recording event when unnecessary (#157914)
- [aarch64] Add sm_80 to CUDA SBSA build (#158118)
- [user triton] AOT inductor support for device-side TMA (#157241)
- Add sm_70 arch for linux cuda 12.8 and 12.9 builds (#157968)
- Revert "Turn on compile with NVSHMEM (#154538)" (#158040)
- Revert "Add NVSHMEM to PYTORCH_EXTRA_INSTALL_REQUIREMENTS (#154568)" (#158039)
- [cherry-pick] revert #156552 (#156767)
- cherrypick revert of #152932 for release 2.8 (#158031)
- [inductor][user triton] sanitize triple-quoted docstrings in kernel definitions (#157454)
- [release] Triton pin update to 3.4 (#157752)
- [inductor][static launcher] Skip correctness test for test_floats (#157200)
- [ONNX] Bump onnxscript api for torch 2.8 (#157137)
- Fix macOS build with `USE_MPS=OFF` (#156932)
- [dynamo] do not issue lru_cache warning for functions in the top-level torch namespace (#157718)
- [dynamo] Fix source for lru_cache method (#157308)
- [cherry-pick] Organize BUCK for torch/standalone and Rename torch::standalone to headeronly (#157418)
- [PowerPC] Fixed build issue for vsx vec256 complexfloat and scaled_mm_out_cpu  (#157422)
- [ONNX] Fix conversion of attention - 4D (#157509)
- [dynamo] Fix bug in dict(mapping_proxy) (#157515)
- [cherry-pick] [fake tensor] fix issue of no attribute tags (#156689) (#157519)
- Add einops x torch.compile testing in PyTorch CI (#157416) (#157588)
- Fix cuda 12.9 aarch64 GPU builds. Update CUDA_STABLE variable.  (#157641)
- Remove +PTX from CUDA 12.8 builds (#157634)
- Cleanup leftover miniconda brew installation (#157567)
- Fix GITHUB_OUTPUT syntax in create_release.yml workflow (#157539)
- [aarch64] Add back NCCL lib to cuda arm wheel (#157105)
- [MPS] Revert cumsum/cumprod to MPSGraph implementation (#157494)
- [ez] Disable some failing periodic tests (#157560)
- Revert "Update triton version to 3.4" (#157471)
- [ROCm] Bump AOTriton to 0.10b (#156845)
- [cherry-pick] revert #156517 on release 2.8 (#156768)
- Fix environment and push env var for docker image builds for binary builds  (#156916)
- Update triton version to 3.4 (#156890)
- [cherry pick] revert #155412 (#156757)
- [RELEASE 2.8] Release only changes (#156728)

## security

## not user facing

## Added to final.md directly
