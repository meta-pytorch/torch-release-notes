
# Release Notes worksheet quantization

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

## quantization
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [FIX] remove the duplicate key in DEFAULT_STATIC_QUANT_MODULE_MAPPINGS ([#149043](https://github.com/pytorch/pytorch/pull/149043))
- Update logic when producing key name for keep_original_weights ([#149171](https://github.com/pytorch/pytorch/pull/149171))
- Enable qint8 and quint8 add for AArch64 using ACL directly ([#148653](https://github.com/pytorch/pytorch/pull/148653))
- [Build] Guard per-op headers in ACLUtils.cpp ([#149417](https://github.com/pytorch/pytorch/pull/149417))
- torch.Size input ([#149414](https://github.com/pytorch/pytorch/pull/149414))
- add `torch.float4_e2m1fn_x2` to PyTorch ([#148791](https://github.com/pytorch/pytorch/pull/148791))
- Improve attr mismatch msg ([#149576](https://github.com/pytorch/pytorch/pull/149576))
- [Intel GPU] Allow XPU backend in Quantize operators ([#150288](https://github.com/pytorch/pytorch/pull/150288))
- [Quant][PT2E] add a lowering pass for x86 backend ([#149708](https://github.com/pytorch/pytorch/pull/149708))
- [AO] update port_metadata_pass to support quant_affine ops ([#150642](https://github.com/pytorch/pytorch/pull/150642))
- [AO] Add Moving Average Affine Observer ([#150643](https://github.com/pytorch/pytorch/pull/150643))
- [AO] Refactor convert and add QuantAffinePlaceholderObserver ([#150644](https://github.com/pytorch/pytorch/pull/150644))
- [Quant][PT2E][X86] enable qconv1d-relu fusion ([#150751](https://github.com/pytorch/pytorch/pull/150751))
- [AO] fix per token block size calculation ([#150890](https://github.com/pytorch/pytorch/pull/150890))
- Fix torchscript issues with reference quantized modules ([#150870](https://github.com/pytorch/pytorch/pull/150870))
- [BE][1/2] Move original_weights_lookup attribute to constant ([#151241](https://github.com/pytorch/pytorch/pull/151241))
- [Sana][HybridCache] Fix bug in detect_attr_assignment ([#151824](https://github.com/pytorch/pytorch/pull/151824))
- [standalone_compile] Dynamic shape handling ([#151788](https://github.com/pytorch/pytorch/pull/151788))
- [Quant][X86] add an op to compute uint8 pointwise mul ([#151112](https://github.com/pytorch/pytorch/pull/151112))
- [1/N] Deprecate c10::string_view and at::string ([#151972](https://github.com/pytorch/pytorch/pull/151972))
- [fbgemm] Implement __obj_flatten__ for LinearPackedParamsBase ([#152619](https://github.com/pytorch/pytorch/pull/152619))
- Avoid  std::chrono::system_clock  ([#153135](https://github.com/pytorch/pytorch/pull/153135))
- [torch][ao] Properly strip tracking stats in  _fold_conv_bn_qat for 1D ([#152982](https://github.com/pytorch/pytorch/pull/152982))
- [Refactor] Explicilty spell out the namespace for device() function ([#153248](https://github.com/pytorch/pytorch/pull/153248))
- [Quant][X86] add ops to compute uint8 pointwise add/add_relu ([#152411](https://github.com/pytorch/pytorch/pull/152411))
- [Quant][X86] add an op to compute uint8 batch norm 2d ([#152811](https://github.com/pytorch/pytorch/pull/152811))
- Add deprecation warning for `torch.ao.quantization` ([#153892](https://github.com/pytorch/pytorch/pull/153892))
- BE: Type previously untyped decorators ([#154515](https://github.com/pytorch/pytorch/pull/154515))
- [Reland][pytorch] Patch the _is_conv_node function ([#154473](https://github.com/pytorch/pytorch/pull/154473))
- Fix incorrect get_default_qat_qconfig in prepare_qat_fx docs. ([#155100](https://github.com/pytorch/pytorch/pull/155100))
- Support boolean tensor for torch.fused_moving_avg_obs_fake_quant on CUDA ([#153699](https://github.com/pytorch/pytorch/pull/153699))
- Remove outdated Android workarounds of nearbyintf ([#151292](https://github.com/pytorch/pytorch/pull/151292))
### not user facing
- Add test coverage ([#149182](https://github.com/pytorch/pytorch/pull/149182))
- Use correct boxed_forward_device_index when running `CompiledFxGraph.post_compile` ([#148130](https://github.com/pytorch/pytorch/pull/148130))
- [Codemod][AddExplicitStrictExportForTrainingInferenceArg] caffe2/ ([#149595](https://github.com/pytorch/pytorch/pull/149595))
- [Codemod][AddExplicitStrictExportForTrainingInferenceArg] caffe2/torch/ao ([#150826](https://github.com/pytorch/pytorch/pull/150826))
- Enable modernize-use-default-member-init ([#149046](https://github.com/pytorch/pytorch/pull/149046))
- [aot autograd][logging] Profile large missing gaps in compile time tracing ([#151256](https://github.com/pytorch/pytorch/pull/151256))
- [Easy] enable PYFMT for torch/quantization/eager ([#150761](https://github.com/pytorch/pytorch/pull/150761))
- [BE][Easy]: Simplify reversed call in graph matcher ([#151674](https://github.com/pytorch/pytorch/pull/151674))
- [BE] Replace func_name with __func__ ([#152553](https://github.com/pytorch/pytorch/pull/152553))
- Enable -Wunused on torch targets ([#150077](https://github.com/pytorch/pytorch/pull/150077))
- Enable -Wunused on torch targets ([#150077](https://github.com/pytorch/pytorch/pull/150077))
- `has_triton`: Use the device interface for detecting Triton availability ([#139171](https://github.com/pytorch/pytorch/pull/139171))
- [Ez][BE]: Ensure matplotlib remains optional dependency via fake_quantize ([#153244](https://github.com/pytorch/pytorch/pull/153244))
- [BE]: Update ruff to 0.11.8 ([#153249](https://github.com/pytorch/pytorch/pull/153249))
- [compile-time traces] Profile large missing gaps in compile time ([#151256](https://github.com/pytorch/pytorch/pull/151256))
- [aotd] Support saved tensors hooks in aot_autograd ([#150032](https://github.com/pytorch/pytorch/pull/150032))
- remove allow-untyped-defs from torch/ao/quantization/stubs.py ([#154622](https://github.com/pytorch/pytorch/pull/154622))
- [BE][Ez]: Remove unneeded mypy suppressions ([#154800](https://github.com/pytorch/pytorch/pull/154800))
- [TEST][Quantization] Skip test_learnable due to hypothesis ([#152819](https://github.com/pytorch/pytorch/pull/152819))
- [inductor] Add typing to _inductor/ir.py ([#149958](https://github.com/pytorch/pytorch/pull/149958))
- Add __main__ guards to ao tests ([#154612](https://github.com/pytorch/pytorch/pull/154612))
- Add __main__ guards to quantization tests ([#154728](https://github.com/pytorch/pytorch/pull/154728))
- remove allow-untyped-defs from adaround_fake_quantize.py ([#155621](https://github.com/pytorch/pytorch/pull/155621))
- [BE][PYFMT] migrate PYFMT for `torch/ao/` to `ruff format` ([#148185](https://github.com/pytorch/pytorch/pull/148185))
- [Precompile] Hook up backend="inductor"  ([#155387](https://github.com/pytorch/pytorch/pull/155387))
- [Precompile] Hook up backend="inductor"  ([#155387](https://github.com/pytorch/pytorch/pull/155387))
- Fix clang-tidy bugprone* warnings ([#148529](https://github.com/pytorch/pytorch/pull/148529))
### security
