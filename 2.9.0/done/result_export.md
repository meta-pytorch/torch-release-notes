
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
- Switches off runtime asserts by default, in favor of a shape guards function. ([#160111](https://github.com/pytorch/pytorch/pull/160111), [#161178](https://github.com/pytorch/pytorch/pull/161178), [#161794](https://github.com/pytorch/pytorch/pull/161794))
To enable runtime asserts, use `export(..., prefer_deferred_runtime_asserts_over_guards=True)`. Also kills the `allow_complex_guards_as_runtime_asserts` flag, merging it into the former option.
Additionally, `exported_program.module()` will generate a call to a `_guards_fn` submodule that will run additional checks on inputs. Users who do not want this behavior can either remove this call in the graph, or do `exported_program.module(check_guards=False)` to avoid the generation.

### deprecation
- Deprecation for `export_for_training` API, in favor of equivalent `export` API ([#158203](https://github.com/pytorch/pytorch/pull/158203))
### new features
### improvements
- Add `_compile_and_package` method for ExportPackage ([#156638](https://github.com/pytorch/pytorch/pull/156638))
- Handle None & ellipsis slicing/select in non-strict ([#157821](https://github.com/pytorch/pytorch/pull/157821))
- Extend FP8 types in serialization ([#158430](https://github.com/pytorch/pytorch/pull/158430))
- Improve error messages for deserialization ([#159881](https://github.com/pytorch/pytorch/pull/159881))
- Support serialization for `triton_kernel_wrapper_functional` HOP ([#161314](https://github.com/pytorch/pytorch/pull/161314))
- Support serialization for complex constants ([#161517](https://github.com/pytorch/pytorch/pull/161517))
- Add runtime asserts to `while_loop` HOP subgraphs ([#158467](https://github.com/pytorch/pytorch/pull/158467))
- Warn on side-effectful code in strict mode ([#160060](https://github.com/pytorch/pytorch/pull/160060))
- Support for vmap in pre-dispatch export ([#154650](https://github.com/pytorch/pytorch/pull/154650))
### bug fixes
- Bug in constants lifting pass ([#157719](https://github.com/pytorch/pytorch/pull/157719))
- Fix `from_node` provenance in unlift pass ([#157943](https://github.com/pytorch/pytorch/pull/157943))
- Fix NaN serialization ([#155359](https://github.com/pytorch/pytorch/pull/155359))
- Fix deserialization for unbacked symbol ranges ([#158681](https://github.com/pytorch/pytorch/pull/158681))
- Fix runtime assert handling in deserialization ([#159060](https://github.com/pytorch/pytorch/pull/159060))
- Fix for FQN handling in unflattener ([#159418](https://github.com/pytorch/pytorch/pull/159418))
- Add _ccode method for PythonMod ([#158851](https://github.com/pytorch/pytorch/pull/158851))
- Fix nn_module_stack for `assert_tensor_metadata` nodes ([#159625](https://github.com/pytorch/pytorch/pull/159625))
- Fix usage for `move_to_device_pass` ([#159992](https://github.com/pytorch/pytorch/pull/159992), [#160528](https://github.com/pytorch/pytorch/pull/160528), [#162301](https://github.com/pytorch/pytorch/pull/162301))
- Avoid name overwrites for aliased exported module parameters ([#160600](https://github.com/pytorch/pytorch/pull/160600))
- Avoid inling dynamo.disables in unflattening ([#161306](https://github.com/pytorch/pytorch/pull/161306))
- Fix deserialization issue for storage offset ([#162172](https://github.com/pytorch/pytorch/pull/162172))
### performance
- Caching optimizations for placeholder naming pass ([#158594](https://github.com/pytorch/pytorch/pull/158594))
### docs
- Update docs around draft export, dynamism, and PT2 Archive ([#157750](https://github.com/pytorch/pytorch/pull/157750))
### devs
### Untopiced
### not user facing
- Document private member variables on ExportedProgram ([#156704](https://github.com/pytorch/pytorch/pull/156704))
- Add _union_dataclass to support comparing dataclasses inheriting from Union ([#156765](https://github.com/pytorch/pytorch/pull/156765))
- Add type and docs for _process_export_inputs ([#156830](https://github.com/pytorch/pytorch/pull/156830))
- Add typing annotations to guard and source (Dynamo) (#158397) ([#159491](https://github.com/pytorch/pytorch/pull/159491))
- Normalize_path_separator file path for AOTI (Windows) ([#159726](https://github.com/pytorch/pytorch/pull/159726))
- Update export/schema.py ([#160220](https://github.com/pytorch/pytorch/pull/160220))
- Typo fix in _trace.py ([#156836](https://github.com/pytorch/pytorch/pull/156836))
- Remove dead code for checking autograd state ([#156855](https://github.com/pytorch/pytorch/pull/156855))
- Remove is_jit_trace option ([#157387](https://github.com/pytorch/pytorch/pull/157387))
- Remove dead code for _postprocess_graph_module_outputs ([#158059](https://github.com/pytorch/pytorch/pull/158059))
- Add sym_sum to verified ops ([#159111](https://github.com/pytorch/pytorch/pull/159111))
- Fix packaging typo ([#158855](https://github.com/pytorch/pytorch/pull/158855))
- Fix public bindings for PT2 Archive ([#159109](https://github.com/pytorch/pytorch/pull/159109))
- Logging for draft export ([#159004](https://github.com/pytorch/pytorch/pull/159004))
- Remove unused `deviceAllocationMap` field in schema ([#159653](https://github.com/pytorch/pytorch/pull/159653))
- Remove unused `Model`, `tensor_paths`, `constant_paths` fields in schema ([#161185](https://github.com/pytorch/pytorch/pull/161185))
- Allow `tempfile._TemporaryFileWrapper` in `package_pt2` ([#161203](https://github.com/pytorch/pytorch/pull/161203))
- Improve arg names for errors in unflatten constraints hook ([#160919](https://github.com/pytorch/pytorch/pull/160919))
- Refactor PT2 Archive weight saving and loading ([#160394](https://github.com/pytorch/pytorch/pull/160394), [#161520](https://github.com/pytorch/pytorch/pull/161520))
- Use GetAttrKey in `get_keystr` to match unflattening ([#161453](https://github.com/pytorch/pytorch/pull/161453))
- Improve formatting in error messages for dynamic shapes ([#161573](https://github.com/pytorch/pytorch/pull/161573))
- Fix broken tests caused by Triton availabity check ([#161737](https://github.com/pytorch/pytorch/pull/161737))
- Fix unflattener test by supporting both MappingKey and GetAttrKey ([#161599](https://github.com/pytorch/pytorch/pull/161599))
- AOTI lowering and packaging as NativeRT delegate ([#162285](https://github.com/pytorch/pytorch/pull/162285))
- WIP `_dynamo_graph_capture_for_export` API ([#162167](https://github.com/pytorch/pytorch/pull/162167))
- WIP standalone compile API in _Exporter ([#158139](https://github.com/pytorch/pytorch/pull/158139))
### security
