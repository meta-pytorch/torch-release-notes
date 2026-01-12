- Replace export_for_training with export ([#162396](https://github.com/pytorch/pytorch/pull/162396))


## ROCm

- [ROCm][Inductor][CK backend] Install rocm-composable-kernel python package on ROCm Linux CI docker images ([#162288]- (https://github.com/pytorch/pytorch/pull/162288))

## Inductor / AOTI

- [AOTI] Pass comments from metadata to the autotune block ([#163600](https://github.com/pytorch/pytorch/pull/163600))
- Support python slicing with tensor inputs. ([#165074](https://github.com/pytorch/pytorch/pull/165074))
- Allow GraphPickler to pickle graph modules containing AOTCompiled subgraphs ([#165844](https://github.com/pytorch/- pytorch/pull/165844))
- [Inductor] Lower fallback nodes annotated with "should_fallback" ([#166339](https://github.com/pytorch/pytorch/pull/- 166339))
- Inductor Lite Mode ([#167115](https://github.com/pytorch/pytorch/pull/167115))
- [Flex] Changing how bwd configs are setup and updating default b200 config ([#163318](https://github.com/pytorch/- pytorch/pull/163318))
- [FlexFlash] CuteDSL flat indexer needs to be colexigraphic in coordinate space ([#166657](https://github.com/- pytorch/pytorch/pull/166657))
- [inductor] Fix bugs in emulate_precision_casts ([#163520](https://github.com/pytorch/pytorch/pull/163520))
- [aoti] Save compute information ([#163792](https://github.com/pytorch/pytorch/pull/163792))
- Fix aot_compile typing. ([#168320](https://github.com/pytorch/pytorch/pull/168320))
- Distributed Autotuning ([#163369](https://github.com/pytorch/pytorch/pull/163369))
- add the option to disable functionalization in AOTDispatcher ([#164577](https://github.com/pytorch/pytorch/pull/164577))


## Not User Facing

- Support propagating custom meta field to backward graph nodes ([#164174](https://github.com/pytorch/pytorch/pull/164174))
- [Optimus] Add batch dropout pattern ([#162443](https://github.com/pytorch/pytorch/pull/162443))
- Add suppressions to torch/_inductor ([#165062](https://github.com/pytorch/pytorch/pull/165062))
- Fix self assignment ([#165816](https://github.com/pytorch/pytorch/pull/165816))
- [effects] Add register_effectful_op ([#163284](https://github.com/pytorch/pytorch/pull/163284))
- Fixes bug with tolist calls to GradTrackingTensors ([#165184](https://github.com/pytorch/pytorch/pull/165184))
- Add GroupName NewType ([#167552](https://github.com/pytorch/pytorch/pull/167552))
- Native matmul ([#157743](https://github.com/pytorch/pytorch/pull/157743))
- Fix slotscheck warnings ([#169348](https://github.com/pytorch/pytorch/pull/169348))
- Fix: ShapeEnv not propagated properly to inductor SizeVars ([#162927](https://github.com/pytorch/pytorch/pull/- 162927))
- Allow unbacked to unbacked replacements if rhs unbacked symbols are all inputs ([#163652](https://github.com/- pytorch/pytorch/pull/163652))
- [cutlass-4][take 2] upgrade to cutlass 4.2.1 ([#164159](https://github.com/pytorch/pytorch/pull/164159))
- Warn if AccumulateGrad stream does not match producer node stream ([#166136](https://github.com/pytorch/pytorch/pull/166136))
- remove more ([#164753](https://github.com/pytorch/pytorch/pull/164753))
- FakeTensorMode shouldn't cache syms when tracing ([#164718](https://github.com/pytorch/pytorch/pull/164718))
- Return fake mode from export graph capture API ([#164730](https://github.com/pytorch/pytorch/pull/164730))
- [scan] create fw and bw graphs via partitioning ([#162754](https://github.com/pytorch/pytorch/pull/162754))
- Add suppressions for _inductor/codegen ([#165659](https://github.com/pytorch/pytorch/pull/165659))
- Remove unnecessary noqa suppressions  ([#164106](https://github.com/pytorch/pytorch/pull/164106))
- Fix incorrect homogeneous tuple types ([#169463](https://github.com/pytorch/pytorch/pull/169463))
- [compile-on-one-rank] Step 1: DeviceId ([#166680](https://github.com/pytorch/pytorch/pull/166680))
- Apply ruff UP035 rule ([#166225](https://github.com/pytorch/pytorch/pull/166225))
- Add grid and input information for Triton Kernels for profiling in Kineto. ([#160131](https://github.com/pytorch/pytorch/pull/160131)) ([#160380](https://github.com/pytorch/pytorch/pull/160380))
- Add AOTI mingw cross compilation ([#163188](https://github.com/pytorch/pytorch/pull/163188))
- Back out "Make PT2 compile backprop through custom op without autograd key a hard error (#166367)" ([#168142](https://github.com/pytorch/pytorch/pull/168142))
- [DebugMode] record triton kernels, run-to-run determinism checks ([#167028](https://github.com/pytorch/pytorch/pull/167028))
- [2/N] Use context managers ([#167404](https://github.com/pytorch/pytorch/pull/167404))
- Fix invalid f-strings ([#164112](https://github.com/pytorch/pytorch/pull/164112))
- [inductor] Add FLOAT_IS_NAN and COMPLEX_IS_NAN guards ([#162537](https://github.com/pytorch/pytorch/pull/162537))
- Replace c10::call_once with static initialization ([#166381](https://github.com/pytorch/pytorch/pull/166381))
- Use Python 3.10 typing ([#148418](https://github.com/pytorch/pytorch/pull/148418))
- [15/N] Use Python 3.10 typing ([#169768](https://github.com/pytorch/pytorch/pull/169768))
- [12/N] Use Python 3.10 typing ([#169355](https://github.com/pytorch/pytorch/pull/169355))
- [9/N] Use Python 3.10 typing  ([#167806](https://github.com/pytorch/pytorch/pull/167806))
- Switch to pyrefly as only type checker ([#166197](https://github.com/pytorch/pytorch/pull/166197))
- Enable PLW0127 in ruff ([#165851](https://github.com/pytorch/pytorch/pull/165851))
- Fix readibility checks in TIDY and apply them ([#164475](https://github.com/pytorch/pytorch/pull/164475))
- [6/N] Apply ruff UP035 rule ([#164438](https://github.com/pytorch/pytorch/pull/164438))
- Add pyrefly suppressions 2/n ([#164513](https://github.com/pytorch/pytorch/pull/164513))
- [1/N] Fix ruff warnings ([#164333](https://github.com/pytorch/pytorch/pull/164333))
- [4/N] Use Python 3.10 typing ([#167458](https://github.com/pytorch/pytorch/pull/167458))
- [2/N] Remove unused header inclusion ([#165831](https://github.com/pytorch/pytorch/pull/165831))
- Redirect all use of filesystem to c10/utils/FileSystem.h ([#162914](https://github.com/pytorch/pytorch/pull/162914))

## XPU

- Add XPU kernel for _weight_int8pack_mm ([#160938](https://github.com/pytorch/pytorch/pull/160938))
- Register the `scaled_mm` and `scaled_mm_v2` for xpu ([#166056](https://github.com/pytorch/pytorch/pull/166056))


## CUDA

- [CUDA] Large tensor maxpool crash fix ([#165374](https://github.com/pytorch/pytorch/pull/165374))
- [CUDA] fix reflection padding for large batch size ([#165942](https://github.com/pytorch/pytorch/pull/165942))
- [CUDA] Large max pool fix ([#167427](https://github.com/pytorch/pytorch/pull/167427))

## ROCM
- [ROCm] fix miopen batchnorm changing output format ([#162112](https://github.com/pytorch/pytorch/pull/162112))
- Add SVE128 ISA ([#158932](https://github.com/pytorch/pytorch/pull/158932))
