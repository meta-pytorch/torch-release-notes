
# Release Notes worksheet inductor (aoti)

You should:

1. ensure commit categorization is correct
2. write up major features, bc-breaking changes, deprecations in detail
3. summarize the other sections

## 1. Ensure commit categorization is correct

* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.

The categories below are as follows:

* BC breaking: All commits that are BC-breaking. These are the most important commits. If any pre-sorted commit is actually BC-breaking, do move it to this section. Each commit should contain a paragraph explaining the rational behind the change as well as an example for how to update user code [BC-Guidelines](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit#heading=h.a9htwgvvec1m).
* Deprecations: All commits introducing deprecation. Each commit should include a small example explaining what should be done to update user code.
* new_features: All commits introducing a new feature (new functions, new submodule, new supported platform etc)
* improvements: All commits providing improvements to existing feature should be here (new backend for a function, new argument, better numerical stability)
* bug fixes: All commits that fix bugs and behaviors that do not match the documentation
* performance: All commits that are added mainly for performance (we separate this from improvements above to make it easier for users to look for it)
* documentation: All commits that add/update documentation
* Developers: All commits that are not end-user facing but still impact people that compile from source, develop into pytorch, extend pytorch, etc
* not user facing: All commits that are not public end-user facing and hence should be dropped from the release notes

## 2. Major features, BC-breaking changes, deprecations

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.

## 3. Summarize the other sections

For the other sections (improvements, bug fixes, performance, documentation, developers, not user facing) - use your
judgement to summarize the key PRs. You do not need to make every commit description perfect
(changed in v2.10 to simplify the process).

Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

Feel free to use https://github.com/pytorch/pytorch/releases/tag/v2.10.0 as an example.

## inductor (aoti)
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
- [inductor] Disambiguate nested graph stream variables ([#196324](https://github.com/pytorch/pytorch/pull/196324))
- [inductor] Register subgraph constants in root allocated_constant_name ([#199188](https://github.com/pytorch/pytorch/pull/199188))
- [inductor] AOTI: pass symbolic scalars in Tensor args to proxy-executor fallbacks ([#199204](https://github.com/pytorch/pytorch/pull/199204))
- [aoti] Share extern kernel nodes between the constant-folding and main graph ([#199295](https://github.com/pytorch/pytorch/pull/199295))
- [aoti] Clone outputs that alias a constant through a fallback view op ([#199323](https://github.com/pytorch/pytorch/pull/199323))
- [aoti] Use the proxy executor for _quantized ops without a C shim ([#199336](https://github.com/pytorch/pytorch/pull/199336))
### performance
### docs
### devs
### Untopiced
- Register `linalg_qr`, `geqrf`, and `linalg_householder_product` for XPU ([#187564](https://github.com/pytorch/pytorch/pull/187564))
- [aoti] Add private libc++ build support (#191239) ([#191239](https://github.com/pytorch/pytorch/pull/191239))
- [PyTorch][AOTI] Share one H2D stream per device instead of one per PinnedStagingPool (#193249) ([#193249](https://github.com/pytorch/pytorch/pull/193249))
- [MPS] Add native _int_mm support ([#193153](https://github.com/pytorch/pytorch/pull/193153))
- [MPS] Fix MPSProfiler `stream` arg backward compatibility ([#193611](https://github.com/pytorch/pytorch/pull/193611))
- [inductor] Fix missing int_array declarations in AOTI C++ wrapper ([#193621](https://github.com/pytorch/pytorch/pull/193621))
- [inductor] AOTI: handle SymInt in a Scalar arg for proxy-executor fallback kernels (#193767) ([#193767](https://github.com/pytorch/pytorch/pull/193767))
- Fix grammar and spelling errors in comments and docstrings ([#193965](https://github.com/pytorch/pytorch/pull/193965))
- [inductor] AOTI: skip fallback for aten.sym_stride.int in lite mode (#193768) ([#193768](https://github.com/pytorch/pytorch/pull/193768))
- [inductor] AOTI proxy executor: don't count defaulted kwarg-only args in the runtime arrays (#194261) ([#194261](https://github.com/pytorch/pytorch/pull/194261))
- Fix grammar typos in comments and docstrings ([#194417](https://github.com/pytorch/pytorch/pull/194417))
- Fix indefinite article and grammar typos in comments and docstrings ([#194254](https://github.com/pytorch/pytorch/pull/194254))
- [inductor] AOTI: route integer-scalar / integral-tensor ops off the c-shim to the proxy executor (#194262) ([#194262](https://github.com/pytorch/pytorch/pull/194262))
- Avoid folding mutated buffer storages ([#185077](https://github.com/pytorch/pytorch/pull/185077))
- Fix grammar and typos in code comments and docstrings ([#194494](https://github.com/pytorch/pytorch/pull/194494))
- [inductor] AOTI proxy executor: coerce a None empty (Sym)IntList arg to an empty list (#194324) ([#194324](https://github.com/pytorch/pytorch/pull/194324))
- [AOTInductor] Pluggable model-container lifecycle observer interface (#193999) ([#193999](https://github.com/pytorch/pytorch/pull/193999))
- [inductor] lite mode: run reinplacing before decomposing the functional Triton HOP (#194325) ([#194325](https://github.com/pytorch/pytorch/pull/194325))
- [inductor] AOTI cpp wrapper: pass a missing Optional[Device]/list/tuple as nullopt in the StableIValue path (#194700) ([#194700](https://github.com/pytorch/pytorch/pull/194700))
- [torch][inductor] Get shape information for extern/Aten kernels with enable_kernel_profile (#191063) ([#191063](https://github.com/pytorch/pytorch/pull/191063))
- [aoti] Prevent exceptions from crossing the AOTI C ABI (#194613) ([#194613](https://github.com/pytorch/pytorch/pull/194613))
- [AOTInductor] Support host-side PDL launches (#194079) ([#194079](https://github.com/pytorch/pytorch/pull/194079))
- Drop unused includes in torch/csrc and caffe2/serialize ([#194961](https://github.com/pytorch/pytorch/pull/194961))
- Add cpp wrapper fallback alignment assertions ([#184114](https://github.com/pytorch/pytorch/pull/184114))
- [aoti] Build legacy and ABI-compatible AOTI DSOs (#191241) ([#191241](https://github.com/pytorch/pytorch/pull/191241))
- [AOTInductor] Fix user-managed constant handle leak (#194480) ([#194480](https://github.com/pytorch/pytorch/pull/194480))
- [RAWTHROW][7] torch/csrc/inductor: 52 conversions, one annotated macro ([#195148](https://github.com/pytorch/pytorch/pull/195148))
- [inductor] AOTI cpp wrapper: support invoke_subgraph (#194703) ([#194703](https://github.com/pytorch/pytorch/pull/194703))
- [GPU][AOTI] Support host TMA in C++ wrappers (#193608) ([#193608](https://github.com/pytorch/pytorch/pull/193608))
- [inductor] AOTI cpp wrapper: keep a nested region's Inductor config (#194704) ([#194704](https://github.com/pytorch/pytorch/pull/194704))
- [Inductor] Route AOTI device type through DeviceOpOverrides ([#193904](https://github.com/pytorch/pytorch/pull/193904))
- Improve pytree missing registration error ([#186900](https://github.com/pytorch/pytorch/pull/186900))
- [torch][inductor] Fix numel variable scoping with enable_kernel_profile (#179698) ([#179698](https://github.com/pytorch/pytorch/pull/179698))
- [aotinductor] Add check_upperbound to gate the upperbound input check ([#196131](https://github.com/pytorch/pytorch/pull/196131))
- [inductor] TORCHINDUCTOR_LITE_MODE: re-run the AOTInductor suites under all-fallback mode (#195880) ([#195880](https://github.com/pytorch/pytorch/pull/195880))
- Add AOTI_TORCH_SAVE_DIR and fix the tensor-dump path join (#195869) ([#195869](https://github.com/pytorch/pytorch/pull/195869))
- [AOTI] Add opt-in stream-to-runtime affinity (#194783) ([#194783](https://github.com/pytorch/pytorch/pull/194783))
- [AOTInductor] Unmap mmap-backed constants on model destruction ([#195090](https://github.com/pytorch/pytorch/pull/195090))
- [MPS] Add _scaled_mm_v2 for float8_e4m3fn ([#196916](https://github.com/pytorch/pytorch/pull/196916))
- Add optional strict alignment asserts on graph inputs ([#196379](https://github.com/pytorch/pytorch/pull/196379))
- [inductor] Do not leave an unused OpenMP dependency in AOTI MPS artifacts ([#198232](https://github.com/pytorch/pytorch/pull/198232))
- [torch][inductor] Extend KernelContextGuard profiling to the fallback kernel paths (#179699) ([#179699](https://github.com/pytorch/pytorch/pull/179699))
- [torch][inductor] Extend KernelContextGuard profiling to template and combo kernels (#198433) ([#198433](https://github.com/pytorch/pytorch/pull/198433))
- [torch][inductor] Add RAIIAtenRecordFunctionHandle profiling to remaining uncovered kernel paths (#179700) ([#179700](https://github.com/pytorch/pytorch/pull/179700))
- [AOTInductor] Parallelize pinned constant staging copies ([#195257](https://github.com/pytorch/pytorch/pull/195257))
- Mark unused parameters in top-level torch/csrc ([#199453](https://github.com/pytorch/pytorch/pull/199453))
- Mark unused parameters in inductor and nativert ([#199467](https://github.com/pytorch/pytorch/pull/199467))
- Avoid returning void expressions in void functions ([#199448](https://github.com/pytorch/pytorch/pull/199448))
- Preserve NVGEMM benchmark layouts and aliases ([#199072](https://github.com/pytorch/pytorch/pull/199072))
### not user facing
- [MPS] Update profiler to act on a specified stream ([#192525](https://github.com/pytorch/pytorch/pull/192525))
- Use c10::fmap for container-to-vector transforms ([#194876](https://github.com/pytorch/pytorch/pull/194876))
- [inductor] Fix inductor dropping ordering dep between effectful ops with different kernel types ([#188301](https://github.com/pytorch/pytorch/pull/188301))
- Preserve original Dynamo minifier backend failures ([#186546](https://github.com/pytorch/pytorch/pull/186546))
- [BE][Ez]: Removes double probes in STL collections ([#195299](https://github.com/pytorch/pytorch/pull/195299))
- [BE][Ez]: Enable some optin cpp20 range features for AOT ArrayRef ([#196355](https://github.com/pytorch/pytorch/pull/196355))
- [inductor] Tighten remaining formatting annotations ([#196617](https://github.com/pytorch/pytorch/pull/196617))
- [Inductor] Canonicalize positional and keyword args in pre-grad batch math fusion (#198285) ([#198285](https://github.com/pytorch/pytorch/pull/198285))
### security
