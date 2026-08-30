
# Release Notes worksheet fx

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

## fx
### bc breaking
### deprecation
### new features
### improvements
- Allow `split_const_subgraphs()` callers to supply an `is_impure_node` callback so destination-passing operations and other side-effecting nodes are preserved during dead-code elimination. ([#190716](https://github.com/pytorch/pytorch/pull/190716))
- Make `get_source_partitions()` return input nodes, output nodes, and parameters in deterministic graph order. ([#188965](https://github.com/pytorch/pytorch/pull/188965))
### bug fixes
- Respect deferred runtime-assert bounds when deriving optimization hints for unbacked symbolic sizes, preventing negative storage sizes and downstream CUDA indexing failures ([#190589](https://github.com/pytorch/pytorch/pull/190589))
- Make selected Dynamo, Inductor, and FX tracing state thread-local to prevent race conditions when `torch.compile` is invoked concurrently from multiple threads ([#168999](https://github.com/pytorch/pytorch/pull/168999))
- Fix FX `GraphModule` serialization when generated code contains string type annotations. ([#185051](https://github.com/pytorch/pytorch/pull/185051))
- Fix scripting FX-generated modules with nested `Optional[Dict[...]]` annotations on Python 3.14. ([#190580](https://github.com/pytorch/pytorch/pull/190580))
- Skip constant folding for `get_attr` nodes whose targets cannot be resolved or refer to modules. ([#191939](https://github.com/pytorch/pytorch/pull/191939))
- Preserve non-persistent buffer registration when an FX `GraphModule` copies attributes, keeping those buffers out of `state_dict()`. ([#191708](https://github.com/pytorch/pytorch/pull/191708))
- Fix Z3 translation validation for graphs containing symbolic boolean negation through `torch.sym_not`. ([#185147](https://github.com/pytorch/pytorch/pull/185147))
- Fix FX-generated code raising `NameError` for complex constants whose imaginary component is `nan` or `inf`. ([#188596](https://github.com/pytorch/pytorch/pull/188596))
- Preserve signed zero when FX code generation emits complex constants with a zero real or imaginary component. ([#185550](https://github.com/pytorch/pytorch/pull/185550))
- Apply `skip_folding_node_fn` recursively to `call_module` subgraphs so FX constant folding does not evaluate skipped or symbolic nodes inside them. ([#189487](https://github.com/pytorch/pytorch/pull/189487))
- Return valid `tuple[...]` annotations from `get_signature_for_torch_op` for operators that return multiple tensors. ([#189142](https://github.com/pytorch/pytorch/pull/189142))
### performance
- Speed up `GraphModule.delete_all_unused_submodules()` by using constant-time membership checks while determining submodule liveness. ([#178320](https://github.com/pytorch/pytorch/pull/178320))
- Release inputs to boxed FX calls before dispatch when they have no other uses, reducing peak memory in compiled backward graphs. ([#187186](https://github.com/pytorch/pytorch/pull/187186))
### docs
### devs
- Allow exported profiler timelines to include source-stack provenance for Inductor-generated kernels when `TORCH_COMPILE_DEBUG_EXTEND=1` ([#186230](https://github.com/pytorch/pytorch/pull/186230))
- Preserve device indices such as `cuda:7` in functorch minifier repro inputs so generated repros run on the original device. ([#186547](https://github.com/pytorch/pytorch/pull/186547))
### not user facing
- Fix internal lint violations in Inductor communication lowering and FX unification code without changing runtime behavior ([#191866](https://github.com/pytorch/pytorch/pull/191866))
- Correct typos in FX comments, docstrings, and diagnostics without changing behavior ([#188870](https://github.com/pytorch/pytorch/pull/188870))
- Restore the previous internal generalized-scatter graph representation. ([#188219](https://github.com/pytorch/pytorch/pull/188219))
- Make TorchFuzz-generated `gather` and `index_select` indices deterministic across devices and runs. ([#189553](https://github.com/pytorch/pytorch/pull/189553))
- Make the profiler stack-trace augmentation test account for Windows using cuBLAS instead of cuBLASLt. ([#188491](https://github.com/pytorch/pytorch/pull/188491))
- Avoid a `linecache` loader warning on Python 3.15. ([#187221](https://github.com/pytorch/pytorch/pull/187221))
### security
