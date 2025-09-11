
# Release Notes worksheet export

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

## export
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [export] Implement _compile_and_package for ExportPackage. ([#156638](https://github.com/pytorch/pytorch/pull/156638))
- [BE] Typo fix ([#156836](https://github.com/pytorch/pytorch/pull/156836))
- Remove unneccesary code to check autograd state ([#156855](https://github.com/pytorch/pytorch/pull/156855))
- Remove is_jit_trace option ([#157387](https://github.com/pytorch/pytorch/pull/157387))
- [export] Fix lift constants bug ([#157719](https://github.com/pytorch/pytorch/pull/157719))
- Fix from_node's graph_id in unlift() ([#157943](https://github.com/pytorch/pytorch/pull/157943))
- [non-strict export] uncovered cases of select and slice ([#157821](https://github.com/pytorch/pytorch/pull/157821))
- [exported_program] Remove _postprocess_graph_module_outputs ([#158059](https://github.com/pytorch/pytorch/pull/158059))
- Fix serialization of nans in torch.export ([#155359](https://github.com/pytorch/pytorch/pull/155359))
- Standalone compile API in _Exporter ([#158139](https://github.com/pytorch/pytorch/pull/158139))
- [export] Update docs ([#157750](https://github.com/pytorch/pytorch/pull/157750))
- Add FP8 Types ([#158430](https://github.com/pytorch/pytorch/pull/158430))
- Add deprecation warning ([#158203](https://github.com/pytorch/pytorch/pull/158203))
- Add caching for `_rename_without_collisions` ([#158594](https://github.com/pytorch/pytorch/pull/158594))
- [export] fix unbacked range deserialization ([#158681](https://github.com/pytorch/pytorch/pull/158681))
- [export][ez] Fix packaging ([#158855](https://github.com/pytorch/pytorch/pull/158855))
- [export] Fix public bindings ([#159109](https://github.com/pytorch/pytorch/pull/159109))
- [ez][export] add sym_sum to verified ops ([#159111](https://github.com/pytorch/pytorch/pull/159111))
- [export] assert fix in serdes ([#159060](https://github.com/pytorch/pytorch/pull/159060))
- unflatten closure ([#159418](https://github.com/pytorch/pytorch/pull/159418))
- [draft export] logging ([#159004](https://github.com/pytorch/pytorch/pull/159004))
- [export] _ccode for PythonMod ([#158851](https://github.com/pytorch/pytorch/pull/158851))
- [export] Fix nn_module_stack of assert_tensor_metadata nodes ([#159625](https://github.com/pytorch/pytorch/pull/159625))
- [export] Improve error messages ([#159881](https://github.com/pytorch/pytorch/pull/159881))
- [Export Schema] Remove deviceAllocationMap field ([#159653](https://github.com/pytorch/pytorch/pull/159653))
- [export] Apply move_to_device_pass to all submodules ([#159992](https://github.com/pytorch/pytorch/pull/159992))
- [export] Update move_to_device_pass for to.device ([#160528](https://github.com/pytorch/pytorch/pull/160528))
- [export] Remove unused Model, tensor_paths, constant_paths ([#161185](https://github.com/pytorch/pytorch/pull/161185))
- [export] Allow tempfile._TemporaryFileWrapper in package_pt2 ([#161203](https://github.com/pytorch/pytorch/pull/161203))
- Reland D80238201: [Torch.Export] Add flat arg paths in error message ([#160919](https://github.com/pytorch/pytorch/pull/160919))
- Fix the parity of original and exported module parameters ([#160600](https://github.com/pytorch/pytorch/pull/160600))
- [1/n][export] Refactor PT2 Archive weight saving and loading ([#160394](https://github.com/pytorch/pytorch/pull/160394))
- [APS IR] Minfor fix - use GetAttrKey in get_keystr to match with flat args path in unflatten ([#161453](https://github.com/pytorch/pytorch/pull/161453))
- [export] Update unflattening dynamo.disable ([#161306](https://github.com/pytorch/pytorch/pull/161306))
- switch prefer_deferred_runtime_asserts_over_guards in export ([#160111](https://github.com/pytorch/pytorch/pull/160111))
- [export] serialization support for triton_kernel_wrapper_functional ([#161314](https://github.com/pytorch/pytorch/pull/161314))
- [ez] Improve formatting in error messages for dynamic shapes ([#161573](https://github.com/pytorch/pytorch/pull/161573))
- fix tests caused by has_triton ([#161737](https://github.com/pytorch/pytorch/pull/161737))
- [export] Support complex constant in serde ([#161517](https://github.com/pytorch/pytorch/pull/161517))
- [unflatten] Fix test by supporting both MappingKey anf GetAttrKey ([#161599](https://github.com/pytorch/pytorch/pull/161599))
- [2/n][export] Refactor PT2 Archive weight saving and loading ([#161520](https://github.com/pytorch/pytorch/pull/161520))
- [export] Fix torch.export.load with storage offset ([#162172](https://github.com/pytorch/pytorch/pull/162172))
- [export] Move example inputs in move_to_device_pass ([#162301](https://github.com/pytorch/pytorch/pull/162301))
- [nativert] AOTI lowering and packaging as NativeRT delegate ([#162285](https://github.com/pytorch/pytorch/pull/162285))
### not user facing
- Document each of the private member variables on ExportedProgram ([#156704](https://github.com/pytorch/pytorch/pull/156704))
- [resubmit][export] add _union_dataclass to support comparing dataclasses that inherits from union. ([#156765](https://github.com/pytorch/pytorch/pull/156765))
- [BE] Add type and docs for _process_export_inputs ([#156830](https://github.com/pytorch/pytorch/pull/156830))
- [Dynamo][Better Engineering] Add typing annotations to guard and source (#158397) ([#159491](https://github.com/pytorch/pytorch/pull/159491))
- [AOTI] normalize_path_separator file path for Windows. ([#159726](https://github.com/pytorch/pytorch/pull/159726))
- Update export/schema.py ([#160220](https://github.com/pytorch/pytorch/pull/160220))
### security
