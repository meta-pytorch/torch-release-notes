
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
- Set non-strict export as default mode ([#148790](https://github.com/pytorch/pytorch/pull/148790))
- Remove torch.export.export_for_inference ([#149078](https://github.com/pytorch/pytorch/pull/149078))
- [BC-breaking] Set NonStrict as default for export_for_training ([#150941](https://github.com/pytorch/pytorch/pull/150941))
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- [export] Fix tensor_constant and buffer naming conflicts in TS converter ([#148803](https://github.com/pytorch/pytorch/pull/148803))
- Fix outdated docstring of torch.export.export regarding strict flag ([#149077](https://github.com/pytorch/pytorch/pull/149077))
- [torchbench] fix dynamic_shapes spec for moco ([#148772](https://github.com/pytorch/pytorch/pull/148772))
- [export] Minor refactor to trace.py ([#149240](https://github.com/pytorch/pytorch/pull/149240))
- [export] Update remove runtime asserts pass ([#149198](https://github.com/pytorch/pytorch/pull/149198))
- [export] Add TracingContext ([#149294](https://github.com/pytorch/pytorch/pull/149294))
- debug ival swap ([#149206](https://github.com/pytorch/pytorch/pull/149206))
- Fix dynamic shapes repordering bug ([#149528](https://github.com/pytorch/pytorch/pull/149528))
- Monkeypatch fake mode so it errors on invalid custom ops ([#149410](https://github.com/pytorch/pytorch/pull/149410))
- [export] Handle non OpNamespace type during decomposition. ([#149431](https://github.com/pytorch/pytorch/pull/149431))
- preserve custom meta in placeholders ([#149661](https://github.com/pytorch/pytorch/pull/149661))
- Fix subclass access custom op bug ([#149698](https://github.com/pytorch/pytorch/pull/149698))
- pretty print graph signature ([#149710](https://github.com/pytorch/pytorch/pull/149710))
- [export] Patch dynamo configs when nonstrict tracing ([#149295](https://github.com/pytorch/pytorch/pull/149295))
- [export] Add mark_compiled_region support ([#149296](https://github.com/pytorch/pytorch/pull/149296))
- [export] Save unflattened gm ([#150030](https://github.com/pytorch/pytorch/pull/150030))
- fix range constraints for expr ([#150103](https://github.com/pytorch/pytorch/pull/150103))
- [reland] Support torchbind in OSS proxy executor ([#150196](https://github.com/pytorch/pytorch/pull/150196))
- [export] min/max ranges for dim hints ([#149590](https://github.com/pytorch/pytorch/pull/149590))
- infer dynamic shapes through additional inputs ([#150144](https://github.com/pytorch/pytorch/pull/150144))
- [pytree] Register normal class to register_dataclass ([#147752](https://github.com/pytorch/pytorch/pull/147752))
- multidimensional slicing ([#150104](https://github.com/pytorch/pytorch/pull/150104))
- [export] Fix deserialization issue ([#150515](https://github.com/pytorch/pytorch/pull/150515))
- [aoti] Fix  cannot determine truth value of Relation error when propagating unbacked symint in lowering ([#150570](https://github.com/pytorch/pytorch/pull/150570))
- [export] Make aoti_call_delegate hop traceable ([#148804](https://github.com/pytorch/pytorch/pull/148804))
- [export] raise when Dim.DYNAMIC 0/1 specializes ([#150716](https://github.com/pytorch/pytorch/pull/150716))
- Expand allowed_getattr_types_for_subgm to torch.Tensor ([#150867](https://github.com/pytorch/pytorch/pull/150867))
- Fix aten.div type promotion for FakeTensor ([#150874](https://github.com/pytorch/pytorch/pull/150874))
- [export] Refine draft-export CVE with Dim.AUTO ([#150876](https://github.com/pytorch/pytorch/pull/150876))
- Add real_tensor to the FakeTensor in node.meta["val"] ([#150948](https://github.com/pytorch/pytorch/pull/150948))
- [export] check tuple length mismatch for dynamic_shapes spec ([#150976](https://github.com/pytorch/pytorch/pull/150976))
- [export] Make draft-export predispatch=True by default ([#151051](https://github.com/pytorch/pytorch/pull/151051))
- [export] Add draft-export to error msg ([#151065](https://github.com/pytorch/pytorch/pull/151065))
- [export] Integrate meta kernel generation with draft-export ([#150809](https://github.com/pytorch/pytorch/pull/150809))
- Fix implicit state dict modification ([#151436](https://github.com/pytorch/pytorch/pull/151436))
- [doc fix] fix torch export docs for preserve_module_call_signature ([#151140](https://github.com/pytorch/pytorch/pull/151140))
- [export] suggest dynamic re-export in input constraints hook ([#151624](https://github.com/pytorch/pytorch/pull/151624))
- Rename register_fake_profile to unsafe_generate_fake_kernels ([#151797](https://github.com/pytorch/pytorch/pull/151797))
- Infra for handling builtin ops (min, max, math.pow) ([#151348](https://github.com/pytorch/pytorch/pull/151348))
- [export] Enable symint inputs for AdditionalInputs and ShapesCollection ([#151842](https://github.com/pytorch/pytorch/pull/151842))
- [DRAFT] INitial version of sticky export ([#151047](https://github.com/pytorch/pytorch/pull/151047))
- [export] improve error message for deserializing custom triton op ([#152029](https://github.com/pytorch/pytorch/pull/152029))
- [export] Preserve custom metadata for tensor constants ([#152241](https://github.com/pytorch/pytorch/pull/152241))
- Fix additional inputs to error on inconsistent constants ([#151970](https://github.com/pytorch/pytorch/pull/151970))
- [export] support SymInt minlength for torch.bincount() ([#152497](https://github.com/pytorch/pytorch/pull/152497))
- [export][be] better type annotation for lift_constants_pass ([#152072](https://github.com/pytorch/pytorch/pull/152072))
- [export] warn when Dim.AUTO 0/1 specializes ([#151827](https://github.com/pytorch/pytorch/pull/151827))
- [export] Ignore None buffers ([#152571](https://github.com/pytorch/pytorch/pull/152571))
- BE: Swap functorch --> torch._higher_order_ops ([#152620](https://github.com/pytorch/pytorch/pull/152620))
- [IR] Input Adapter refactor prototype (#152459) ([#152575](https://github.com/pytorch/pytorch/pull/152575))
- [export] Add draft-export docs ([#152637](https://github.com/pytorch/pytorch/pull/152637))
- [export] Unflatten None ([#153000](https://github.com/pytorch/pytorch/pull/153000))
- Mini tutorial for provenance tracking ([#152211](https://github.com/pytorch/pytorch/pull/152211))
- [dynamic shapes] guard_or_false for computeStorageNbytes ([#150483](https://github.com/pytorch/pytorch/pull/150483))
- GPU lowering uses aoti_call_delegate ([#153282](https://github.com/pytorch/pytorch/pull/153282))
- [export] support functools.partial forward (non-strict) ([#153408](https://github.com/pytorch/pytorch/pull/153408))
- [export] Make draft_export public ([#153219](https://github.com/pytorch/pytorch/pull/153219))
- [export] Support no inputs in unflattened module ([#153474](https://github.com/pytorch/pytorch/pull/153474))
- [export] Remove unused constants ([#153800](https://github.com/pytorch/pytorch/pull/153800))
- [export] avoid float/bool specialization for scalar tensor construction ([#154661](https://github.com/pytorch/pytorch/pull/154661))
- [Export] Add math module for deserialization ([#154643](https://github.com/pytorch/pytorch/pull/154643))
- Adding from_node for nodes in gm.module() ([#155053](https://github.com/pytorch/pytorch/pull/155053))
- Preserve Enum types during torch.export serialization and deserialization ([#154821](https://github.com/pytorch/pytorch/pull/154821))
- Fix spelling mistake ([#155495](https://github.com/pytorch/pytorch/pull/155495))
- [Export] Fix some typos in docstring ([#155485](https://github.com/pytorch/pytorch/pull/155485))
- [export] Fix serialization for call_torchbind hop with as_none argument ([#155647](https://github.com/pytorch/pytorch/pull/155647))
- pyfmt lint more export files ([#155783](https://github.com/pytorch/pytorch/pull/155783))
- [export] Remove broken check for multiple cpp files in PT2 package ([#155149](https://github.com/pytorch/pytorch/pull/155149))
- Handle aten.to at submodule boundaries  ([#153972](https://github.com/pytorch/pytorch/pull/153972))
- [export] Update documents for ExportGraphSiganture ([#156244](https://github.com/pytorch/pytorch/pull/156244))
- [ez][export] Better error message for schema check in torch.export.load ([#156361](https://github.com/pytorch/pytorch/pull/156361))
- [export] update docs for Dims ([#156262](https://github.com/pytorch/pytorch/pull/156262))
### not user facing
- [export] set is_exporting() for strict ([#151833](https://github.com/pytorch/pytorch/pull/151833))
- [export][cond] support merging constant ints as unbacked symint ([#152742](https://github.com/pytorch/pytorch/pull/152742))
- [export][cond] support merging constant ints as unbacked symint ([#152742](https://github.com/pytorch/pytorch/pull/152742))
- pyfmt lint torch/_export/serde/serialize.py ([#154485](https://github.com/pytorch/pytorch/pull/154485))
- pyfmt lint  torch/_export/serde/schema.py ([#154487](https://github.com/pytorch/pytorch/pull/154487))
- pyfmt lint torch/_export/passes/replace_view_ops_with_view_copy_ops_pass.py ([#154488](https://github.com/pytorch/pytorch/pull/154488))
- [multigraph] use specializations in compile_and_call_fx_graph ([#153449](https://github.com/pytorch/pytorch/pull/153449))
### security
