
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
- Add pad and narrow to torch/csrc/stable/ops.h ([#159328](https://github.com/pytorch/pytorch/pull/159328))
- Add getCurrentDeviceIndex to torch::stable::accelerator ([#160453](https://github.com/pytorch/pytorch/pull/160453))
- Add new_zeros dtype variant to the shim and as a stable op ([#161597](https://github.com/pytorch/pytorch/pull/161597))
### improvements
- [MPS] Add boilerplate sparse code support ([#157238](https://github.com/pytorch/pytorch/pull/157238))
- Add `avg_pool3d` for MPS ([#158877](https://github.com/pytorch/pytorch/pull/158877))
- [MPS] Add max_unpool1d/2d/3d ([#159789](https://github.com/pytorch/pytorch/pull/159789))
### bug fixes
### performance
### docs
### devs
### Untopiced
- Better error message when no .so/cpp files are found ([#156863](https://github.com/pytorch/pytorch/pull/156863))
- Add `max_pool3d` for MPS ([#156467](https://github.com/pytorch/pytorch/pull/156467))
- Add `max_pool3d` backward pass for MPS ([#157498](https://github.com/pytorch/pytorch/pull/157498))
- [AOTI] Split aoti_runtime/model.h to prepare for model static linking ([#157592](https://github.com/pytorch/pytorch/pull/157592))
- Change AOTI_RUNTIME_DEVICE_CHECK to be device device specific ([#157818](https://github.com/pytorch/pytorch/pull/157818))
- [BE][testing] fix aot_inductor_package internally ([#158270](https://github.com/pytorch/pytorch/pull/158270))
- [BE]Clean up old APIs in AOTI c shim ([#158400](https://github.com/pytorch/pytorch/pull/158400))
- Enable generating generic c_shim that doesn't bypass dispatcher ([#158974](https://github.com/pytorch/pytorch/pull/158974))
- Enable _int_mm on Intel GPU ([#157769](https://github.com/pytorch/pytorch/pull/157769))
- Add `avg_pool3d` backward pass for MPS ([#159089](https://github.com/pytorch/pytorch/pull/159089))
- Cut a version of TORCH_ERROR_CODE_CHECK in headeronly from AOTI ([#159604](https://github.com/pytorch/pytorch/pull/159604))
- Update torch::stable::Tensor() default constructor ([#159507](https://github.com/pytorch/pytorch/pull/159507))
- Add beginnings of torch::stable::accelerator ([#159679](https://github.com/pytorch/pytorch/pull/159679))
- Port amax to stable ABI ([#160214](https://github.com/pytorch/pytorch/pull/160214))
- Add new_empty (with dtype argument only) to torch::stable ([#159508](https://github.com/pytorch/pytorch/pull/159508))
- [AOTI] Fix a bug from load_constants ([#161887](https://github.com/pytorch/pytorch/pull/161887))
### not user facing
- [cpp wrapper] add AOTI shim for collective ops ([#154492](https://github.com/pytorch/pytorch/pull/154492))
- [BE][PYFMT] migrate PYFMT for `torch/_[a-h]*/` to `ruff format` ([#144551](https://github.com/pytorch/pytorch/pull/144551))
- [AOTI] Add missing ops to set of C-shim ops which can have nullptr returns ([#158073](https://github.com/pytorch/pytorch/pull/158073))
- [AOT_inductor] model_base.h add Windows include files. ([#158477](https://github.com/pytorch/pytorch/pull/158477))
- [AOTI] add WIN32 implement for create_temp_dir ([#158570](https://github.com/pytorch/pytorch/pull/158570))
- [AOTI] package loader normalize path separator ([#158630](https://github.com/pytorch/pytorch/pull/158630))
- [AOTI] add Windows file ext to package loader. ([#158578](https://github.com/pytorch/pytorch/pull/158578))
- [AOTI] windows package load dev ([#158671](https://github.com/pytorch/pytorch/pull/158671))
- [AOTI] fix extract file failed on Windows. ([#158702](https://github.com/pytorch/pytorch/pull/158702))
- [AOTI] normalize path and process model files. ([#158705](https://github.com/pytorch/pytorch/pull/158705))
- [AOTI] explicit aoti wrapper functions for Windows. ([#158713](https://github.com/pytorch/pytorch/pull/158713))
- Grab bag of (mostly) typing improvements ([#158075](https://github.com/pytorch/pytorch/pull/158075))
- [AOTI] Add more default options to compile_standalone ([#158560](https://github.com/pytorch/pytorch/pull/158560))
- [AOTI] add windows support for get_cpp_compile_command ([#158732](https://github.com/pytorch/pytorch/pull/158732))
- [AOTI] windows package load dev ([#158671](https://github.com/pytorch/pytorch/pull/158671))
- [aoti][mps] Fix update constants buffer ([#158349](https://github.com/pytorch/pytorch/pull/158349))
- [AOTI] normalize path and process model files. ([#158705](https://github.com/pytorch/pytorch/pull/158705))
- [AOTI] fix extract file failed on Windows. ([#158702](https://github.com/pytorch/pytorch/pull/158702))
- [aoti][mps] Initialize mps kernels first ([#159753](https://github.com/pytorch/pytorch/pull/159753))
- [Easy] Fix wrong propagation of fallback_ops_dict in gen_aoti_c_shim ([#159904](https://github.com/pytorch/pytorch/pull/159904))
- [AOTI] Add more default options to compile_standalone ([#158560](https://github.com/pytorch/pytorch/pull/158560))
- Fix unbacked symint and memory leak in inductor memory planning ([#159839](https://github.com/pytorch/pytorch/pull/159839))
- [AOTI] normalize_path_separator zip file path ([#161781](https://github.com/pytorch/pytorch/pull/161781))
- Always build USE_DISTRIBUTED. ([#160449](https://github.com/pytorch/pytorch/pull/160449))
- [AOTI] split too long string to smaller pieces when its length larger than 16000, fix msvc c2026. ([#161850](https://github.com/pytorch/pytorch/pull/161850))
- [AOTI] Add Windows-compatible implementation of the mmap-related funcs ([#161805](https://github.com/pytorch/pytorch/pull/161805))
- Always build USE_DISTRIBUTED. ([#160449](https://github.com/pytorch/pytorch/pull/160449))
- [reland] Add inductor provenance mapping for cpp extern kernel (#161656) ([#162069](https://github.com/pytorch/pytorch/pull/162069))
- Always build USE_DISTRIBUTED. ([#160449](https://github.com/pytorch/pytorch/pull/160449))
- Always build USE_DISTRIBUTED. ([#160449](https://github.com/pytorch/pytorch/pull/160449))
- Always build USE_DISTRIBUTED. ([#160449](https://github.com/pytorch/pytorch/pull/160449))
### security
