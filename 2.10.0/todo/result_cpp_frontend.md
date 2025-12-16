
# Release Notes worksheet cpp_frontend

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

## cpp_frontend
### bc breaking
### deprecation
### new features
- Migrate DeviceType to torch/headeronly ([#163999](https://github.com/pytorch/pytorch/pull/163999))
- Add torch::stable::Device ([#166579](https://github.com/pytorch/pytorch/pull/166579))
- Add stable::Tensor.device() ([#166694](https://github.com/pytorch/pytorch/pull/166694))
- Redo add parallel_for to torch/csrc/stable ([#166695](https://github.com/pytorch/pytorch/pull/166695))
- Add shim for at::get_num_threads ([#167362](https://github.com/pytorch/pytorch/pull/167362))
- Move MemoryFormat/Layout to headeronly ([#168034](https://github.com/pytorch/pytorch/pull/168034))
- Add string support for ABI stable custom ops ([#168370](https://github.com/pytorch/pytorch/pull/168370))
- Add element_size, storage_offset and set_requires_grad to stable Tensor ([#169703](https://github.com/pytorch/pytorch/pull/169703))
- Add sum and sum_out to stable ops ([#168062](https://github.com/pytorch/pytorch/pull/168062))
### improvements
- Add torch::stable::Tensor sizes and strides ([#165153](https://github.com/pytorch/pytorch/pull/165153))
- fix the cpp_builder error under riscv ([#167071](https://github.com/pytorch/pytorch/pull/167071))
- making TORCH_CHECK_{COND} non-fatal ([#167004](https://github.com/pytorch/pytorch/pull/167004))
- Migrate TypeTraits, TypeList, Metaprogramming to torch:: headeronly ([#167386](https://github.com/pytorch/pytorch/pull/167386))
- [codemod][lowrisk] Remove unused exception parameter from caffe2/caffe2/serialize/inline_container.cc ([#167612](https://github.com/pytorch/pytorch/pull/167612))
- Upgrade stable new_{empty/zeros} that had only dtype argument to full version ([#169711](https://github.com/pytorch/pytorch/pull/169711))
### bug fixes
- Fix #164742, all header-impl'd userfacing functions should be inline ([#164871](https://github.com/pytorch/pytorch/pull/164871))
### performance
### docs
### devs
### Untopiced
- fix cpp extension distributed warning spew ([#162764](https://github.com/pytorch/pytorch/pull/162764))
- Port shared_ptr optimization in std::shared_ptr to intrusive_ptr ([#162784](https://github.com/pytorch/pytorch/pull/162784))
- [submodule] Bump libfmt to 12.0.0 ([#163441](https://github.com/pytorch/pytorch/pull/163441))
- Combine strong and weak refcounts in intrusive_ptr in a single refcount ([#163394](https://github.com/pytorch/pytorch/pull/163394))
- Move version.h to torch/headeronly ([#164381](https://github.com/pytorch/pytorch/pull/164381))
- [2/N] Mark unused parameters in C++ code ([#165121](https://github.com/pytorch/pytorch/pull/165121))
- Add HIDDEN_NAMESPACE_BEGIN and END macros for hiding header APIs ([#166076](https://github.com/pytorch/pytorch/pull/166076))
- Hide all APIs in torch::stable ([#166077](https://github.com/pytorch/pytorch/pull/166077))
- Hide stable Library structs instead of using anon namespace ([#166078](https://github.com/pytorch/pytorch/pull/166078))
- Hide APIs in torch::headeronly ([#166079](https://github.com/pytorch/pytorch/pull/166079))
- Add TORCH_TARGET_VERSION for stable ABI ([#164356](https://github.com/pytorch/pytorch/pull/164356))
- Add scaffolding for aoti_torch_call_dispatcher BC with native ops ([#163683](https://github.com/pytorch/pytorch/pull/163683))
- Add scaffolding for StableIValue FC/BC (no PoC) ([#164332](https://github.com/pytorch/pytorch/pull/164332))
- Replace decltype(auto) with auto ([#166537](https://github.com/pytorch/pytorch/pull/166537))
- [3/N] Add clang-tidy readability checks ([#164692](https://github.com/pytorch/pytorch/pull/164692))
- [2/N] Use `key in dict` for existence checks ([#167174](https://github.com/pytorch/pytorch/pull/167174))
- Fix use of TORCH_CHECK in torch/csrc/stable ([#167495](https://github.com/pytorch/pytorch/pull/167495))
- Add empty to stable ops ([#167592](https://github.com/pytorch/pytorch/pull/167592))
- Add reshape, view, flatten to torch/csrc/stable ([#167600](https://github.com/pytorch/pytorch/pull/167600))
- Move CppTypeToScalarType to torch/headeronly ([#167610](https://github.com/pytorch/pytorch/pull/167610))
- Add shim for getCurrentBlasHandle ([#168276](https://github.com/pytorch/pytorch/pull/168276))
- Add C++ wrapper for shim from_blob in stable/csrc/ops.h ([#168380](https://github.com/pytorch/pytorch/pull/168380))
- Add STD_CUDA_{KERNEL_LAUNCH_}CHECK ([#169385](https://github.com/pytorch/pytorch/pull/169385))
- Make TORCH_BOX support const ref arguments ([#169563](https://github.com/pytorch/pytorch/pull/169563))
- Add to and contiguous to stable ops ([#169709](https://github.com/pytorch/pytorch/pull/169709))
- [4/N] Remove unused header inclusion ([#169216](https://github.com/pytorch/pytorch/pull/169216))
### not user facing
- Move AT_FORALL_... macros and ScalarTypeToCPPTypeT to headeronly ([#164350](https://github.com/pytorch/pytorch/pull/164350))
- Remove workaround to old CUDA bug ([#164354](https://github.com/pytorch/pytorch/pull/164354))
- Move toString(ScalarType) and ScalarType ostream operator to headeronly (#164405) ([#166018](https://github.com/pytorch/pytorch/pull/166018))
- Move toUnderlying to headeronly ([#165694](https://github.com/pytorch/pytorch/pull/165694))
- Move AT_DISPATCH_V2 helper macros to headeronly and add THO_DISPATCH_V2_TMPL ([#165856](https://github.com/pytorch/pytorch/pull/165856))
- add missing cpp standard lib in HeaderOnlyArrayRef.h ([#167337](https://github.com/pytorch/pytorch/pull/167337))
- [codemod][lowrisk] Remove unused exception parameter from caffe2/torch/csrc/jit/backends/coreml/objc/PTMCoreMLBackend.mm ([#167604](https://github.com/pytorch/pytorch/pull/167604))
- Move isQIntType to headeronly ([#167772](https://github.com/pytorch/pytorch/pull/167772))
- [codemod][lowrisk] Remove unused exception parameter from caffe2/torch/csrc/Exceptions.h ([#168056](https://github.com/pytorch/pytorch/pull/168056))
- [codemod][lowrisk] Remove unused exception parameter from caffe2/torch/csrc/Storage.cpp ([#168184](https://github.com/pytorch/pytorch/pull/168184))
- Move c10/util/Deprecated.h to headeronly ([#168173](https://github.com/pytorch/pytorch/pull/168173))
- Add shims for setCurrentCUDAStream, getStreamFromPool, and synchronize. ([#169376](https://github.com/pytorch/pytorch/pull/169376))
### security
