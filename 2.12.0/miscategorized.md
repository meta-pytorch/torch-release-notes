# Miscategorized PRs

PRs that ended up in the wrong worksheet, organized by which area they belong to.

## belongs to: aotdispatcher
- Add UUID-based cache key support for pre-grad custom passes ([#177403](https://github.com/pytorch/pytorch/pull/177403)) _(from inductor worksheet)_
- Add autograd_cache_key to compile_fx with tests ([#178172](https://github.com/pytorch/pytorch/pull/178172)) _(from inductor worksheet)_
- Add autograd_cache_key to standalone_compile with tests ([#178173](https://github.com/pytorch/pytorch/pull/178173)) _(from inductor worksheet)_

## belongs to: cuda
- [CUDA] Add support for torch.cond with cuda graphs ([#168912](https://github.com/pytorch/pytorch/pull/168912)) _(from inductor worksheet)_
- [inductor] Fix CUTLASS illegal memory access via subprocess isolation (#171094) ([#172123](https://github.com/pytorch/pytorch/pull/172123)) _(from inductor worksheet)_

## belongs to: distributed (torchelastic)
- [BE][Ez]: Improve logger calls to remove eager str casts ([#178414](https://github.com/pytorch/pytorch/pull/178414)) _(from inductor worksheet)_

## belongs to: dynamo
- [user-streams] Enforce barriers across syncs w/ dependency HOP ([#168894](https://github.com/pytorch/pytorch/pull/168894)) _(from inductor worksheet)_
- Fixes bmm/ matmul mixed dtype in compile ([#177696](https://github.com/pytorch/pytorch/pull/177696)) _(from inductor worksheet)_

## belongs to: fx
- Delete size_vars size_hint API ([#175365](https://github.com/pytorch/pytorch/pull/175365)) _(from inductor worksheet)_
- [inductor] Decompose mm/addmm to pointwise mul when K==1 ([#175825](https://github.com/pytorch/pytorch/pull/175825)) _(from inductor worksheet)_
- Use FloorDiv and Mod instead of // and % on sympy exprs ([#177051](https://github.com/pytorch/pytorch/pull/177051)) _(from inductor worksheet)_
- [Inductor] repeat_interleave fx graph runnable fix (#177909) ([#177909](https://github.com/pytorch/pytorch/pull/177909)) _(from inductor worksheet)_

## belongs to: inductor (aoti)
- [AOTI] Fix the SIGPE by adding additional check logics in the codegen of the ([#170669](https://github.com/pytorch/pytorch/pull/170669)) _(from inductor worksheet)_
- Allow custom op with `Optional[List[T]]` in cpp wrapper ([#174460](https://github.com/pytorch/pytorch/pull/174460)) _(from inductor worksheet)_
- Fix scratch size for TMA in C++ wrapper ([#175385](https://github.com/pytorch/pytorch/pull/175385)) _(from inductor worksheet)_
- [inductor] Add lazy Triton kernel compilation for cpp-wrapper ([#175416](https://github.com/pytorch/pytorch/pull/175416)) _(from inductor worksheet)_
- [inductor] Add TMA support for lazy Triton kernel compilation ([#175548](https://github.com/pytorch/pytorch/pull/175548)) _(from inductor worksheet)_
- [inductor] Add compile backend registry and custom device support for AOTI eager ([#175605](https://github.com/pytorch/pytorch/pull/175605)) _(from inductor worksheet)_
- [BE][inductor] Apply PEP 604 type annotations (part 1/3) ([#175675](https://github.com/pytorch/pytorch/pull/175675)) _(from inductor worksheet)_
- [torch][inductor] Emit int64_t type declaration for kernel numel variables ([#176922](https://github.com/pytorch/pytorch/pull/176922)) _(from inductor worksheet)_
- [inductor] Fix CPP wrapper lazy compile for scalar tensor args ([#178478](https://github.com/pytorch/pytorch/pull/178478)) _(from inductor worksheet)_
- Fix triton kernel stream for user stream contexts ([#178547](https://github.com/pytorch/pytorch/pull/178547)) _(from inductor worksheet)_
- Hipify CUdeviceptr in lazy scratch allocation codegen ([#179978](https://github.com/pytorch/pytorch/pull/179978)) _(from inductor worksheet)_

## belongs to: jit
- [1/12] Upgrade runtime JIT/Inductor codegen to C++20 ([#176502](https://github.com/pytorch/pytorch/pull/176502)) _(from inductor worksheet)_

## belongs to: optim
- [XPU] Enable skipped inductor test on Intel GPU - generalize code and enable xpu for functions under torch/ folder ([#174053](https://github.com/pytorch/pytorch/pull/174053)) _(from inductor worksheet)_

## belongs to: releng
- [Inductor][CUTLASS] Fix subprocess benchmark crash for addmm with input_reorder ([#177930](https://github.com/pytorch/pytorch/pull/177930)) _(from inductor worksheet)_
- [Inductor] Add deterministic mode for benchmark perf tests ([#178233](https://github.com/pytorch/pytorch/pull/178233)) _(from inductor worksheet)_

## belongs to: rocm
- [ROCm] Tune Flex-Attention occupancy for head_dim=64/128/256 ([#176261](https://github.com/pytorch/pytorch/pull/176261)) _(from inductor worksheet)_

## belongs to: xpu
- Enable FMA-based addcdiv lowering for XPU ([#176163](https://github.com/pytorch/pytorch/pull/176163)) _(from inductor worksheet)_
## MPS

- [MPS] Add nonzero_static implementation ([#179589](https://github.com/pytorch/pytorch/pull/179589)) — from inductor (aoti)

## Export

- export: add float8_e8m0fnu serde support ([#176270](https://github.com/pytorch/pytorch/pull/176270)) — from inductor (aoti)
- Support `torch.uint{32,64}` in `torch.export.save` ([#179434](https://github.com/pytorch/pytorch/pull/179434)) — from inductor (aoti)
