
# Release Notes worksheet inductor (aoti)

The main goal of this process is to rephrase all the commit messages below to make them **clear and easy to read** by the end user. You should follow the following instructions to do so:

* **Please clean up and format commit titles to be readable by the general PyTorch user.** Make sure you're [following the guidance here](https://docs.google.com/document/d/14OmgGBr1w6gl1VO47GGGdwrIaUNr92DFhQbY_NEk8mQ/edit)! Your resulting notes must be consistent and easy to read.
* Please sort commits into the following categories (you should not rename the categories!), I tried to pre-sort these to ease your work, feel free to move commits around if the current categorization is not good.
* Anything that is not public facing needs to be removed.
* If anything is miscategorized/belongs to another domain, move it to `miscategorized.md`.
* Please scan through `miscategorized.md` and handle any commits that belong within your domain according to these instructions.
* We place a lot of emphasis on the “BC-breaking” and “deprecation” sections. Those should be where the most effort goes in. The “improvements” and “bug fixes” for Python API should be nice as well.
* Once you are finished, move this very file from `todo/` to `done/` and submit a pull request.

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

## inductor (aoti)
### bc breaking
### deprecation
- Move from/to to torch::stable::detail ([#164956](https://github.com/pytorch/pytorch/pull/164956))
### new features
- Integrate AOTI as a backend. ([#167338](https://github.com/pytorch/pytorch/pull/167338))
- Add AOTI mingw cross compilation for Windows. ([#163188](https://github.com/pytorch/pytorch/pull/163188))
### improvements

### bug fixes
- Bugfix for doing negative padding ([#161639](https://github.com/pytorch/pytorch/pull/161639))
- Fix unbounded number of substitutions when equality checks contain Max expr ([#163685](https://github.com/pytorch/pytorch/pull/163685))
- Use atomic API when trying to apply size hints to input tensor strides. ([#163660](https://github.com/pytorch/pytorch/pull/163660))
- Fix a mixed-device bug for scatter_add ([#167341](https://github.com/pytorch/pytorch/pull/167341))
- Fix a small buffer mutation issue ([#169347](https://github.com/pytorch/pytorch/pull/169347))
- Fix `aot_compile` typing. ([#168320](https://github.com/pytorch/pytorch/pull/168320))
### performance
### docs
- [AOTI] Update AOTInductor tutorial ([#163808](https://github.com/pytorch/pytorch/pull/163808))
### devs
### Untopiced
### not user facing
- Use filesystem in inductor ([#163465](https://github.com/pytorch/pytorch/pull/163465)) ([#163632](https://github.com/pytorch/pytorch/pull/163632))
- Load metadata w/o loading package ([#163779](https://github.com/pytorch/pytorch/pull/163779))
- Replace std::runtime_error with TORCH_CHECK ([#164130](https://github.com/pytorch/pytorch/pull/164130))
- AOTI Enablement - Fix GR model AOTI inplace update by skipping empty named (#165970) ([#166037](https://github.com/pytorch/pytorch/pull/166037))
- Compress aoti stack ([#169291](https://github.com/pytorch/pytorch/pull/169291))
- Add full to stable ops (supported via generate c shim rather than torch_call_dispatcher) ([#169872](https://github.com/pytorch/pytorch/pull/169872))
- Add squeeze, unsqueeze, matmul, select, subtract to stable ops ([#169880](https://github.com/pytorch/pytorch/pull/169880))
- Fix provenance tracking kernel name for fallback kernels ([#162628](https://github.com/pytorch/pytorch/pull/162628))
- Use CudaCachingAllocator for memory allocation ([#162893](https://github.com/pytorch/pytorch/pull/162893))
- Save `threads_per_warp` from tirton compiled kernel for launching kernel correctly in cpp wrapper. ([#163315](https://github.com/pytorch/pytorch/pull/163315))
- Fix redundant H2D/D2H memcpy in cpp_wrapper by creating scalar tensors on CPU ([#160584](https://github.com/pytorch/pytorch/pull/160584))
- Refactor Provenance Tracking ([#163378](https://github.com/pytorch/pytorch/pull/163378))
- Back out "Revert D81959389" ([#163905](https://github.com/pytorch/pytorch/pull/163905))
- Add ABI stable method for updating constant buffer ([#163819](https://github.com/pytorch/pytorch/pull/163819))
- Add an option to put store large mmap weights on disk ([#164526](https://github.com/pytorch/pytorch/pull/164526))
- Support libtorch and posix mingw flavor ([#165574](https://github.com/pytorch/pytorch/pull/165574))
- Fix incorrect function signature in template ([#165567](https://github.com/pytorch/pytorch/pull/165567))
- Fix pyrefly ignore syntax in _inductor ([#166247](https://github.com/pytorch/pytorch/pull/166247))
- Remove c10 as linked library ([#165489](https://github.com/pytorch/pytorch/pull/165489))
- Split CPU and GPU code paths in AOTI hipify utilities ([#165696](https://github.com/pytorch/pytorch/pull/165696))
- Add python stack trace to AOTI generated code ([#160539](https://github.com/pytorch/pytorch/pull/160539))
- Fix unknown constant type for device-moved constants ([#168138](https://github.com/pytorch/pytorch/pull/168138))
- Set device info for subgraphs ([#169001](https://github.com/pytorch/pytorch/pull/169001))
- Add check_lowerbound config for AOTI lowering ([#169430](https://github.com/pytorch/pytorch/pull/169430))
- Use arg signature to derive the right kernel input type for "sympy.Integer" as well ([#169135](https://github.com/pytorch/pytorch/pull/169135))
- Support ScatterFallback ([#162686](https://github.com/pytorch/pytorch/pull/162686))
- Support IndexPutFallback ([#162863](https://github.com/pytorch/pytorch/pull/162863))
- Fix model_package_loader get_cpp_compile_command ([#163561](https://github.com/pytorch/pytorch/pull/163561))
- Add verbose error information for extract file ([#163718](https://github.com/pytorch/pytorch/pull/163718))
- Support Tensor.item ([#165599](https://github.com/pytorch/pytorch/pull/165599))
- Remove ifndef C10_MOBILE around aoti_torch_abi_version impl ([#166882](https://github.com/pytorch/pytorch/pull/166882))
- Introducing the StableIValue representation of list :D ([#165953](https://github.com/pytorch/pytorch/pull/165953))
- Add mutable_data_ptr() and const_data_ptr() methods to torch::stable::Tensor. ([#161891](https://github.com/pytorch/pytorch/pull/161891))
- Follow up on #161891 move additions to stable shim and use version guards ([#168025](https://github.com/pytorch/pytorch/pull/168025))
- Revise stableivalue from/to deprecation ([#168155](https://github.com/pytorch/pytorch/pull/168155))
- Use Python 3.10 typing ([#167790](https://github.com/pytorch/pytorch/pull/167790))
- Add sum support for qlinear_binary templated implementation ([#163249](https://github.com/pytorch/pytorch/pull/163249))
- Save compute information metadata (device, platform, ISA, compute capability). ([#163792](https://github.com/pytorch/pytorch/pull/163792))
- Allow GraphPickler to pickle graph modules containing AOTCompiled subgraphs. ([#165844](https://github.com/pytorch/pytorch/pull/165844))
- Pass comments from metadata to the autotune block for debugging. ([#163600](https://github.com/pytorch/pytorch/pull/163600))
### security
