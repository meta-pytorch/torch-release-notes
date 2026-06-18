
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
- [MPS] grid_sampler_3d backward pass ([#179388](https://github.com/pytorch/pytorch/pull/179388))
- [MPS] Flatten 5D tensors to 4D in batch_norm for performance ([#180335](https://github.com/pytorch/pytorch/pull/180335))
- [AOTI] Parallelize tensor-to-bytes for AOTI weight serialization ([#181280](https://github.com/pytorch/pytorch/pull/181280))
- [AOTI] Support mixed-device constants in update_constant_buffer ([#181114](https://github.com/pytorch/pytorch/pull/181114))
- [AOTI] Use fatbinary for multi-arch CUDA kernels ([#184456](https://github.com/pytorch/pytorch/pull/184456))
- [inductor] Enable CUTLASS  GEMM templates under JIT cpp_wrapper ([#181640](https://github.com/pytorch/pytorch/pull/181640))
### bug fixes
- [Inductor] Fix undefined identifier error in CppWrapper due to false … ([#178147](https://github.com/pytorch/pytorch/pull/178147))
- [inductor][cpp_wrapper] Scale lazy TMA scratch by grid (#182825) ([#182825](https://github.com/pytorch/pytorch/pull/182825))
### performance
### docs
### devs
### Untopiced
- Updating Assertion to Consider Gil-less Python Environments ([#180669](https://github.com/pytorch/pytorch/pull/180669))
- [AOTI] Add FP8 header files in aoti shim.h ([#178120](https://github.com/pytorch/pytorch/pull/178120))
- Fix folded constant offset indexing in AOTI constant buffer updateFix folded constant offset indexing in AOTI constant buffer update ([#179225](https://github.com/pytorch/pytorch/pull/179225))
- use reserve, move, and simplify vector construction in inductor ([#180940](https://github.com/pytorch/pytorch/pull/180940))
- Use std::move and c10::irange in Inductor  ([#181055](https://github.com/pytorch/pytorch/pull/181055))
- Fix FX DCE for OpOverloadPacket in is_impure() (#180886) ([#180886](https://github.com/pytorch/pytorch/pull/180886))
- Introduce versioning to generated C shims to support TORCH_TARGET_VERSION ([#181916](https://github.com/pytorch/pytorch/pull/181916))
- Add GPU stream synchronization after constant folding in AOTI (#181945) ([#181945](https://github.com/pytorch/pytorch/pull/181945))
- [export] Make Triton CPU AOTI work end-to-end through aoti_compile_and_package ([#182251](https://github.com/pytorch/pytorch/pull/182251))
- [export] Simplify wrapper-library detection in model_package_loader (#183027) ([#183027](https://github.com/pytorch/pytorch/pull/183027))
- [Stable C Shim] Shim functions to retrieve error message ([#180135](https://github.com/pytorch/pytorch/pull/180135))
- [AOTI] Enable shared model loading from directory to avoid redundant unzipping ([#172436](https://github.com/pytorch/pytorch/pull/172436))
- [aoti] Fix use-after-free in pointer_to_optional_list ([#183764](https://github.com/pytorch/pytorch/pull/183764))
- Use c10::make_scope_exit to avoid exception leaks ([#184520](https://github.com/pytorch/pytorch/pull/184520))
- [PyTorch][AOTI] Add throttled cudaMemcpy for AOTI constant loading (#184823) ([#184823](https://github.com/pytorch/pytorch/pull/184823))
- [AutoGenEager] Promote scalar literals to tensors for AOTI eager compilation (#185313) ([#185313](https://github.com/pytorch/pytorch/pull/185313))
- Add stable AOTI stream native-handle shim and Stream::nativeHandle() ([#183930](https://github.com/pytorch/pytorch/pull/183930))
- Fix Windows AOTI self-mmap size seek ([#186386](https://github.com/pytorch/pytorch/pull/186386))
### not user facing
- [inductor] Emit assert_size_stride in cpp_wrapper ([#177535](https://github.com/pytorch/pytorch/pull/177535))
- [inductor] Emit assert_alignment in cpp_wrapper ([#177538](https://github.com/pytorch/pytorch/pull/177538))
- [inductor] Emit assert_size_stride in cpp_wrapper ([#177535](https://github.com/pytorch/pytorch/pull/177535))
- [inductor] Emit assert_alignment in cpp_wrapper ([#177538](https://github.com/pytorch/pytorch/pull/177538))
- [inductor] Fix cpp_wrapper lazy compile for combo kernels with per-subkernel blocks ([#180462](https://github.com/pytorch/pytorch/pull/180462))
- [AOTI] Rename secondary_cpu_* to aux_cpu_* in model container ([#181152](https://github.com/pytorch/pytorch/pull/181152))
- [inductor] Fix cpp_wrapper lazy compile for combo kernels with per-subkernel blocks ([#180462](https://github.com/pytorch/pytorch/pull/180462))
- [aoti] Add c-shim for grid_sampler_3d and cudnn_grid_sampler ([#179440](https://github.com/pytorch/pytorch/pull/179440))
- [inductor] Emit assert_size_stride in cpp_wrapper (#181165) ([#181165](https://github.com/pytorch/pytorch/pull/181165))
- Fix deadlock in AOTInductorModelContainer::run() during concurrent constant folding (#181941) ([#181941](https://github.com/pytorch/pytorch/pull/181941))
- Remove plain asserts in torch/_dynamo/repro/ ([#182152](https://github.com/pytorch/pytorch/pull/182152))
- [AOTInductor] Preserve CUDA error messages across C ABI boundary (#182045) ([#182045](https://github.com/pytorch/pytorch/pull/182045))
- [inductor][refactor] Extract LazyKernelCompileResult to shared header ([#182264](https://github.com/pytorch/pytorch/pull/182264))
- [inductor][refactor] Extract helpers in CppWrapperCpu ([#182265](https://github.com/pytorch/pytorch/pull/182265))
- [inductor][refactor] Use AotOnlyBuffer for AOTI cpp_wrapper buffers ([#182304](https://github.com/pytorch/pytorch/pull/182304))
- [AOTInductor] Preserve CUDA error messages across C ABI boundary (#182045) ([#182045](https://github.com/pytorch/pytorch/pull/182045))
- Fix test_cdist_same_inputs ([#183079](https://github.com/pytorch/pytorch/pull/183079))
- [inductor][refactor] Add _target_buf context manager for self.prefix overrides ([#182982](https://github.com/pytorch/pytorch/pull/182982))
- [inductor][refactor] Restructure Triton wrapper signature ([#182911](https://github.com/pytorch/pytorch/pull/182911))
- [inductor][refactor] Use writeline_aot/splice_aot in AOTI emission helpers ([#182983](https://github.com/pytorch/pytorch/pull/182983))
- add _cdist_backward MPS kernel ([#183079](https://github.com/pytorch/pytorch/pull/183079))
- [inductor] Add DualIndentedBuffer for dual-mode codegen ([#182917](https://github.com/pytorch/pytorch/pull/182917))
- [inductor][refactor] Use DualIndentedBuffer for AOTI with lazy Triton kernel compilation ([#182953](https://github.com/pytorch/pytorch/pull/182953))
- [inductor][refactor] Split AssertSizeStrideLine emission ([#183730](https://github.com/pytorch/pytorch/pull/183730))
- Drop sig parameter from gen_static_dispatch_backend_signature ([#184144](https://github.com/pytorch/pytorch/pull/184144))
- [PyTorch][AOTI] Refactor AOTInductorModelContainer to use ConstantBufferSet ([#184781](https://github.com/pytorch/pytorch/pull/184781))
- [inductor][refactor] Extract profiled Triton launch emission ([#184734](https://github.com/pytorch/pytorch/pull/184734))
- [Torch] make AOTInductor's GPU memory deleter noexcept ([#184818](https://github.com/pytorch/pytorch/pull/184818))
- [Torch][AOTI] track and unload CUmodule handles to prevent GPU code object leaks (#184860) ([#184860](https://github.com/pytorch/pytorch/pull/184860))
- [inductor] Fix missing libtorch_python symbols in FBCODE when using cpp-wrapper (#185551) ([#185551](https://github.com/pytorch/pytorch/pull/185551))
- Fix Dynamo minifier module repro generation ([#184449](https://github.com/pytorch/pytorch/pull/184449))
- [Inductor] Handle hinted and fallback unbacked symbols ([#183840](https://github.com/pytorch/pytorch/pull/183840))
### security
