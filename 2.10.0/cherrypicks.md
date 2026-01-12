# cherry picks
## bc breaking


## deprecation


## new features
### 

## improvements
### Profiler
### Inductor


## bug fixes
### Distributed
- Add doc about Copy Engine collectives (#171811)
### Distributed (c10d)
- [c10d] Add thread safety when calling ncclCommGetAsyncError (#170424)
### Inductor
- Fix vllm issue for flex (#170499)
- [cherry-pick] Revert "[Inductor] ReLU/GELU(Addmm) fusions (#168157)" (#170724)
- [cherry-pick] Revert "[Inductor XPU GEMM] Step 1/N: Refactor cutlass configuration. (#160174)" (#170726)
- [dynamo][DebugMode] make ModTracker a no-op in compiled regions (170124)
- [inductor] Fix cudagraph skip for index_put_ with boolean indices, graph partitioning logic (#170103)
- [dynamo] do not include source hashes in pickle (#170723)
- [Resubmit] Fix _split_iteration_ranges handling gt handling for two-dimensional tiling (#170786)
- Avoid closing random file handles in Inductor (#169065)
- [xpu][fix][inductor] fallback bfloat16 atomics to eager (#170755)
- [dynamo] Disable gc after compile by default on free-threaded python (#171749)
- [PowerPC] Fix strict-aliasing bug in VecMask causing incorrect argmax in compile mode (#169164)
- [Inductor] Fix constants handling for Triton constexpr (triton#8248) (#169782)
- Revert "[Inductor] Fix constants handling for Triton constexpr (triton#8248)" (#171926)
- [CI] Add IoU-based accuracy checking for inductor tests segmentation models (#171927)
- Skip modded_nanogpt model in TorchInductor benchmark (#172125)
### Build Frontend
### torch.compile
### torch.export
- Revert "[annotation][export] Add metadata hook for all nodes created … (#170714)
- ci: Ensure we pin onnx-ir (#170792)
### MPSInductor
### MPS
- [MPS] Binary dense scalar kernels (#169764)
- [MPS] binary dense scalar kernels (#170337)
- [MPS] Remove error-checking sync point from MaxUnpool (#172046)
### ROCm
- [ROCm][CI] additional PLATFORM_SUPPORTS_SYMM_MEM skips (#170630)
### CUDA
- [cuDNN] Add check for GPU/cuDNN compatibility on import (#169409)
- [cuDNN][submodule] Upgrade to cuDNN frontend 1.16.1 (#170591)
- [CUDA] Upgrade cuDNN to 9.15.1 for CUDA 13 builds (#169412)
- [cuDNN][SDPA] cuDNN SDPA off-by-default for cuda versions < 12.9 (#171627)
- [cuDNN][Convolution] Disable a cuDNN Convolution engine preemptively (#171747)
### FX
- [Py 3.14] Cleanup graphs for failed tracer outputs (#169642)
### XPU
- [release/2.10] xpu commit pin update for bug fix cherry-pick (#171497)
### Deployment
- [cd] fix manylinux_2_28 tag in wheel name for aarch64 wheels (#170158)
### Sparse
- Remove exp for sparse (#171776)
### Python Frontend
- A few weights_only unpickler fixes (#170085)


## performance
### Intel
### Inductor 
### ROCm
- [ROCm] Enable shared memory based pruning for Triton configs (#169974)
### Distributed (c10d)
- [c10d] Integrate NCCL new ncclAllToAll into PT (#164265)
- [c10d][Sym mem] Make nccl backend full fledged with nccl 2.28.9-1 (#168129)

## docs
### XPU
- Update XPU get-started with new client gpu & update format (#169810)
### ONNX
### Build Frontend

## devs
### XPU

## Untopiced
## security


## not user facing
- [dcp] remove psutil dependency in asyncprocessexecutor for oss (#169985)
- [Inductor] ExternKernelBenchmarkRequest best attempt (#169971)
- Official Docker builds forward fix. Use default python env (#170338)
- [xpu][fix] Fix triton heuristic on reduction (#169257)
- Add python3-dev to Dockerfile dependencies (#170456)
- [ATen][FBGEMM] Add sm103a and sm110a flags to the FBGEMM GENAI kernels (169658)
- [Inductor] Unit test for ExternKernelBenchmarkRequest TensorMeta construction (#170445)
- Docker: install gcc in CUDA runtime images for torch.compile (#170235)
- update doc for tlparse (#171339)
- [SymmMem] Add doc for MemPool support (#171728)
- [SymmMem] Add doc for tiled operators (#171737)
- Update libtorch stable abi doc to use TORCH_BOX macro (#170453)
- Add supported StableIValue types to docs (#168385)
- Link to cpp doc in libtorch_stable_abi doc (#171626)
- Make FC/BC policy explicit in libtorch stable ABI doc (#171751)
- Fix CXXABI_1.3.15 error (#151700)
- Rename _get_cuda_runtime_library to _get_cuda_library (#170908)
- [CI] Bump Torchbench pin (#171745)
- Convert vllm test to yaml (#170452)
- Switch vLLM CI jobs to CUDA 12.9 (#170513)
- Update persons_of_interest.rst (#172031)
- Touch __init__.py in vendored_templates for CuTeDSL Grouped MM template (#170566)
- Bump fbgemm and torchrec pinned commit (#172147)

## Added to final.md directly
