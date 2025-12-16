
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
### improvements
### bug fixes
- Bugfix for doing negative padding ([#161639](https://github.com/pytorch/pytorch/pull/161639))
### performance
### docs
- [AOTI] Update AOTInductor tutorial ([#163808](https://github.com/pytorch/pytorch/pull/163808))
### devs
### Untopiced
- [WOQ] Add XPU kernel for _weight_int8pack_mm ([#160938](https://github.com/pytorch/pytorch/pull/160938))
- [2/N] Use filesystem in inductor ([#163465](https://github.com/pytorch/pytorch/pull/163465))
- [3/N] Use std::filesystem in inductor ([#163632](https://github.com/pytorch/pytorch/pull/163632))
- [aoti] Load metadata w/o loading package ([#163779](https://github.com/pytorch/pytorch/pull/163779))
- [CodeClean] Replace std::runtime_error with TORCH_CHECK ([#164130](https://github.com/pytorch/pytorch/pull/164130))
- [GR v0] AOTI Enablement - Fix GR model AOTI inplace update by skipping empty named (#165970) ([#166037](https://github.com/pytorch/pytorch/pull/166037))
- [xpu][feature] [1/3] add fp8 scaled_mm implementation for XPU ([#165978](https://github.com/pytorch/pytorch/pull/165978))
- [strobelight][gpusnoop] compress aoti stack ([#169291](https://github.com/pytorch/pytorch/pull/169291))
- Add full to stable ops (supported via generate c shim rather than torch_call_dispatcher) ([#169872](https://github.com/pytorch/pytorch/pull/169872))
- Add squeeze, unsqueeze, matmul, select, subtract to stable ops ([#169880](https://github.com/pytorch/pytorch/pull/169880))
### not user facing
- [Inductor-FX] Support ScatterFallback ([#162686](https://github.com/pytorch/pytorch/pull/162686))
- [Inductor-FX] Support IndexPutFallback ([#162863](https://github.com/pytorch/pytorch/pull/162863))
- [AOTI] Fix model_package_loader get_cpp_compile_command ([#163561](https://github.com/pytorch/pytorch/pull/163561))
- [AOTI] Add verbose error information for extract file ([#163718](https://github.com/pytorch/pytorch/pull/163718))
- [Inductor-FX] Support Tensor.item ([#165599](https://github.com/pytorch/pytorch/pull/165599))
- Support python slicing with tensor inputs. ([#165074](https://github.com/pytorch/pytorch/pull/165074))
- Switch to pyrefly as only type checker ([#166197](https://github.com/pytorch/pytorch/pull/166197))
- Remove ifndef C10_MOBILE around aoti_torch_abi_version impl ([#166882](https://github.com/pytorch/pytorch/pull/166882))
- Introducing the StableIValue representation of list :D ([#165953](https://github.com/pytorch/pytorch/pull/165953))
- [precompile] Integrate AOTI as a backend. ([#167338](https://github.com/pytorch/pytorch/pull/167338))
- [precompile] Integrate AOTI as a backend. ([#167338](https://github.com/pytorch/pytorch/pull/167338))
- [STABLE ABI] Add mutable_data_ptr() and const_data_ptr() methods to torch::stable::Tensor. ([#161891](https://github.com/pytorch/pytorch/pull/161891))
- Follow up on #161891 move additions to stable shim and use version guards ([#168025](https://github.com/pytorch/pytorch/pull/168025))
- Revise stableivalue from/to deprecation ([#168155](https://github.com/pytorch/pytorch/pull/168155))
- [7/N] Use Python 3.10 typing ([#167790](https://github.com/pytorch/pytorch/pull/167790))
- Add sum support for qlinear_binary templated implementation ([#163249](https://github.com/pytorch/pytorch/pull/163249))
- [xpu][feature] [3/3] Register the `scaled_mm` and `scaled_mm_v2` for xpu ([#166056](https://github.com/pytorch/pytorch/pull/166056))
- [xpu][feature][2/N]Enable SDPA XPU FlashAttention backend with SYCL-TLA implementation ([#167057](https://github.com/pytorch/pytorch/pull/167057))
### security
