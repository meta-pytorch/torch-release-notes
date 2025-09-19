
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
### new features
### improvements
- Enable AOTI for CPU on Windows ([#158915](https://github.com/pytorch/pytorch/pull/158915))
- re-enable TMA templates w/ AOTI ([#157819](https://github.com/pytorch/pytorch/pull/157819))
- Don't allow int32 indices if {non-inf, > int32_max} upper bound is provided ([#159433](https://github.com/pytorch/pytorch/pull/159433))
- Add RecordFunction to C shim so that profiling works with AOTI ([#159842](https://github.com/pytorch/pytorch/pull/159842))
- Add AOTI C shim functions for collective ops ([#154492](https://github.com/pytorch/pytorch/pull/154492))
- Add missing ops to set of C-shim ops which can have nullptr returns ([#158073](https://github.com/pytorch/pytorch/pull/158073))

### bug fixes
- Fix a bug from load_constants ([#161887](https://github.com/pytorch/pytorch/pull/161887))
- Fix wrong propagation of fallback_ops_dict in gen_aoti_c_shim ([#159904](https://github.com/pytorch/pytorch/pull/159904))
- Fix unbacked symint and memory leak in inductor memory planning ([#159839](https://github.com/pytorch/pytorch/pull/159839))
- Fix memory leak in AOTI when calling `aoti_torch_as_strided` ([#162118](https://github.com/pytorch/pytorch/pull/162118))

### performance
### docs
### devs
- Better error message when no .so/cpp files are found ([#156863](https://github.com/pytorch/pytorch/pull/156863))
- Clean up old APIs in AOTI c shim ([#158400](https://github.com/pytorch/pytorch/pull/158400))
- Add inductor provenance mapping for cpp extern kernel (#161656) ([#162069](https://github.com/pytorch/pytorch/pull/162069))
- Print out error msg when nvcc compiler fails ([#157203](https://github.com/pytorch/pytorch/pull/157203))
- Add kernel information JSON generation for AOTI packages ([#160540](https://github.com/pytorch/pytorch/pull/160540))

### Untopiced
### not user facing
- Change AOTI_RUNTIME_DEVICE_CHECK to be device device specific ([#157818](https://github.com/pytorch/pytorch/pull/157818))
- Split aoti_runtime/model.h to prepare for model static linking ([#157592](https://github.com/pytorch/pytorch/pull/157592))
- model_base.h add Windows include files. ([#158477](https://github.com/pytorch/pytorch/pull/158477))
- add WIN32 implement for create_temp_dir ([#158570](https://github.com/pytorch/pytorch/pull/158570))
- package loader normalize path separator ([#158630](https://github.com/pytorch/pytorch/pull/158630))
- add Windows file ext to package loader. ([#158578](https://github.com/pytorch/pytorch/pull/158578))
- windows package load dev ([#158671](https://github.com/pytorch/pytorch/pull/158671))
- fix extract file failed on Windows. ([#158702](https://github.com/pytorch/pytorch/pull/158702))
- normalize path and process model files. ([#158705](https://github.com/pytorch/pytorch/pull/158705))
- explicit aoti wrapper functions for Windows. ([#158713](https://github.com/pytorch/pytorch/pull/158713))
- add windows support for get_cpp_compile_command ([#158732](https://github.com/pytorch/pytorch/pull/158732))
- windows package load dev ([#158671](https://github.com/pytorch/pytorch/pull/158671))
- normalize_path_separator zip file path ([#161781](https://github.com/pytorch/pytorch/pull/161781))
- split too long string to smaller pieces when its length larger than 16000, fix msvc c2026. ([#161850](https://github.com/pytorch/pytorch/pull/161850))
- Add Windows-compatible implementation of the mmap-related funcs ([#161805](https://github.com/pytorch/pytorch/pull/161805))
- add format_consts_to_cpp function for Windows development. ([#157608](https://github.com/pytorch/pytorch/pull/157608))
- fix clang-asan for consts_cpp. ([#158175](https://github.com/pytorch/pytorch/pull/158175))
- fix split_aot_inductor_output_path on Windows. ([#162058](https://github.com/pytorch/pytorch/pull/162058))
- skip ld and objcopy on Windows. ([#158545](https://github.com/pytorch/pytorch/pull/158545))
- Use format_consts_to_cpp on Windows. ([#158543](https://github.com/pytorch/pytorch/pull/158543))
- add zero size consts asm handler ([#159225](https://github.com/pytorch/pytorch/pull/159225))
- [inductor] Skip some AOTI UTs on Windows. ([#160287](https://github.com/pytorch/pytorch/pull/160287))
- align signature to model_base.h ([#158554](https://github.com/pytorch/pytorch/pull/158554))
- [XPU] switch xpu to use consts cpp build. ([#158425](https://github.com/pytorch/pytorch/pull/158425))
- Grab bag of (mostly) typing improvements ([#158075](https://github.com/pytorch/pytorch/pull/158075))
- [mps] Initialize mps kernels first ([#159753](https://github.com/pytorch/pytorch/pull/159753))
- [mps] Fix update constants buffer ([#158349](https://github.com/pytorch/pytorch/pull/158349))
- add flag AOT_INDUCTOR_ENABLE_LTO ([#157773](https://github.com/pytorch/pytorch/pull/157773))
- add flag TORCHINDUCTOR_CPP_FORCE_INLINE_KERNEL ([#157949](https://github.com/pytorch/pytorch/pull/157949))

### security
