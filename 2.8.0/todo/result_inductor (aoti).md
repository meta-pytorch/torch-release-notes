
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
- Torchbind objects supported in AOTInductor ([#150196](https://github.com/pytorch/pytorch/pull/150196), [#154265](https://github.com/pytorch/pytorch/pull/154265))
### improvements
- [MPS] Implement backward pass for interpolate_trilinear ([#156373](https://github.com/pytorch/pytorch/pull/156373))
- Add _weight_int4pack_mm to the C shim fallback list ([#151059](https://github.com/pytorch/pytorch/pull/151059))
- Add RECORD_FUNCTION for AOTI ([#150150](https://github.com/pytorch/pytorch/pull/150150))
### bug fixes
### performance
### docs
### devs
### Untopiced
- Improve stable library apis per Scott's feedback ([#152040](https://github.com/pytorch/pytorch/pull/152040))
- [AOTInductor] Inherit Buffer if not being updated ([#152092](https://github.com/pytorch/pytorch/pull/152092))
- [AOTI] Fix a memory leak in model_package_loader ([#152334](https://github.com/pytorch/pytorch/pull/152334))
- [aotinductor] Don't alloc weights if they don't exist ([#152692](https://github.com/pytorch/pytorch/pull/152692))
- [AOTInductor] Fix state of ConstantFolding ([#153152](https://github.com/pytorch/pytorch/pull/153152))
- [AOTI][XPU] Refactor AOTInductor runtime API for Intel GPU. ([#153929](https://github.com/pytorch/pytorch/pull/153929))
- [AOTI][refactor] Fix an anonymous namespace issue ([#154033](https://github.com/pytorch/pytorch/pull/154033))
- [3/n][Optimus][Auto-AC][reland] Support any fp8 quantization type and set scaling as the default" ([#154057](https://github.com/pytorch/pytorch/pull/154057))
- Use get_device_context in aoti runtime for XPU directly ([#154360](https://github.com/pytorch/pytorch/pull/154360))
- Add new ops in fallback ops ([#154251](https://github.com/pytorch/pytorch/pull/154251))
- [4/n][Optimus][Auto-AC] Expose the config to skip the dynamo gaurds to avoid recompile ([#154152](https://github.com/pytorch/pytorch/pull/154152))
- [debug_printer][BE] Fix float8 type printing for min/max value printing ([#154466](https://github.com/pytorch/pytorch/pull/154466))
- Move c10/macros/Export.h to torch/standalone ([#154850](https://github.com/pytorch/pytorch/pull/154850))
- [ez][AOTI] Fix index offset for Optional Tensor Return ([#155073](https://github.com/pytorch/pytorch/pull/155073))
- Add C shim for at::pad and fix some typos ([#155226](https://github.com/pytorch/pytorch/pull/155226))
- [AOTI] Enable OP `test__weight_int4pack_mm_with_scales_and_zeros` in AOTI. ([#155780](https://github.com/pytorch/pytorch/pull/155780))
- [BE][AOTI] Combine DynamicArgType in Proxy Executors ([#155871](https://github.com/pytorch/pytorch/pull/155871))
- [aoti] Add more to error message ([#155974](https://github.com/pytorch/pytorch/pull/155974))
- Add a basic shim and stable::Tensor is_contiguous API ([#156228](https://github.com/pytorch/pytorch/pull/156228))
- Add C shim fallback for fill_ ([#156245](https://github.com/pytorch/pytorch/pull/156245))
- [PT2]Add weight and constant config path template ([#156359](https://github.com/pytorch/pytorch/pull/156359))
- Add shim fallback for narrow ([#156496](https://github.com/pytorch/pytorch/pull/156496))
### not user facing
- [AOTI][reland] Remove typedef for half and bfloat16 ([#151109](https://github.com/pytorch/pytorch/pull/151109))
- [AOTI] Embed cubin files into .so ([#150739](https://github.com/pytorch/pytorch/pull/150739))
- [Lint] Update clang-format to 19.1.4 ([#153889](https://github.com/pytorch/pytorch/pull/153889))
- cpp_wrapper: build non-performance-sensitive code at O1 ([#148773](https://github.com/pytorch/pytorch/pull/148773))
- cpp_wrapper: build non-performance-sensitive code at O1 ([#148773](https://github.com/pytorch/pytorch/pull/148773))
- [AOTI] Extend torchgen to generate C shim with version number ([#147745](https://github.com/pytorch/pytorch/pull/147745))
- [BE][Ez]: Remove unnecessary accesses of dim vector ([#155334](https://github.com/pytorch/pytorch/pull/155334))
- [aoti] Update cshim for all backends ([#155604](https://github.com/pytorch/pytorch/pull/155604))
- [aoti][mps] Fix int/symint kernel args ([#155583](https://github.com/pytorch/pytorch/pull/155583))
- [AOTInductor] Reuse input information instead of directly applying unbacked_symint_fallback ([#156133](https://github.com/pytorch/pytorch/pull/156133))
- [Intel GPU][AOTI] Add xpu mkldnn ops support for AOTInductor. ([#154586](https://github.com/pytorch/pytorch/pull/154586))
- Add an option for cpp_wrapper to compile entry and kernel separately ([#156050](https://github.com/pytorch/pytorch/pull/156050))
- Fix torchgen update-aoti-shim ([#156323](https://github.com/pytorch/pytorch/pull/156323))
### security
