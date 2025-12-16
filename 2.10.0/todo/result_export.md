
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
- [Docs] Add warning that `torch.export.load` uses `pickle` ([#167557](https://github.com/pytorch/pytorch/pull/167557))
### devs
### Untopiced
- [triton][export] serialization in internal path + unit tests ([#162200](https://github.com/pytorch/pytorch/pull/162200))
- [serialization] Add pte file to archive ([#162520](https://github.com/pytorch/pytorch/pull/162520))
- fix var args for shape guards ([#162633](https://github.com/pytorch/pytorch/pull/162633))
- Fix torch export with dict input nested in args ([#162618](https://github.com/pytorch/pytorch/pull/162618))
- Don't skip register_dataclass unflatten in dynamo ([#162557](https://github.com/pytorch/pytorch/pull/162557))
- Fix inconsistent test and add new tracer as config ([#162558](https://github.com/pytorch/pytorch/pull/162558))
- Move export_db to use new tracer, remove restriction on optional inputs ([#162993](https://github.com/pytorch/pytorch/pull/162993))
- [export] Remove .contiguous() when saving weights to raw bytes ([#163587](https://github.com/pytorch/pytorch/pull/163587))
- [export] handling NamedTuple inputs ([#162959](https://github.com/pytorch/pytorch/pull/162959))
- [Dynamic Shape][BE] trim _DimHint serialization ([#163891](https://github.com/pytorch/pytorch/pull/163891))
- Fix various bugs in subclass input in export ([#163770](https://github.com/pytorch/pytorch/pull/163770))
- [export] avoid checks during tracing of export verification ([#164219](https://github.com/pytorch/pytorch/pull/164219))
- [export] Explicitly passing requires_grad to nn.Parameter() in deserialization ([#164290](https://github.com/pytorch/pytorch/pull/164290))
- [RELAND v2] Close some sources of fake tensors ([#164372](https://github.com/pytorch/pytorch/pull/164372))
- [export] Better state_dict and constant dedup in torch.export.save ([#164196](https://github.com/pytorch/pytorch/pull/164196))
- [export] Fix weight sharing when there is no complete tensor ([#164857](https://github.com/pytorch/pytorch/pull/164857))
- Better handling of restore_state_dict ([#164401](https://github.com/pytorch/pytorch/pull/164401))
- [PT2 Archive] Use tensor dtype while deduping/grouping weights (state_dict/constants) ([#165090](https://github.com/pytorch/pytorch/pull/165090))
- Forward fix inductor failure (#165363) ([#165443](https://github.com/pytorch/pytorch/pull/165443))
- [torch.export] Rmoving unused constants - add support for corner case ([#165205](https://github.com/pytorch/pytorch/pull/165205))
- [torch.export] Add original module type to UnflattenedModule class ([#166145](https://github.com/pytorch/pytorch/pull/166145))
- [triton][nativert] Add num_cpu_threads for triton-cpu ([#166255](https://github.com/pytorch/pytorch/pull/166255))
- [torch.export] Refactor placeholder_naming_pass to reduce CCN ([#166600](https://github.com/pytorch/pytorch/pull/166600))
- Fix: Improve fallback behavior in `deserialize_torch_artifact` and relocate test into `TestSaveLoad` ([#158247](https://github.com/pytorch/pytorch/pull/158247))
- [torch.export] Copy common custom metadata of children node to parent (call_module) node ([#167952](https://github.com/pytorch/pytorch/pull/167952))
### not user facing
- [export] Skip the check instead of disable ([#164084](https://github.com/pytorch/pytorch/pull/164084))
- [DTensor][Export] Supporting exporting a model with DTensor params/inputs ([#163609](https://github.com/pytorch/pytorch/pull/163609))
- Don't use C++ CIA decomps if there's a Python one ([#164970](https://github.com/pytorch/pytorch/pull/164970))
- Revert "[export] Turn on install_free_tensors flag (#164691)" ([#165353](https://github.com/pytorch/pytorch/pull/165353))
- AOTI util deprecated flow using the new tracer ([#165582](https://github.com/pytorch/pytorch/pull/165582))
- [export, 3.14] handle patching methods with functools.partial correctly in non-strict export ([#167396](https://github.com/pytorch/pytorch/pull/167396))
- [export, 3.14] handle patching methods with functools.partial correctly in non-strict export ([#167396](https://github.com/pytorch/pytorch/pull/167396))
### security
