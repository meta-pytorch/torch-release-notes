
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
### bug fixes
### performance
- [fx] Use a set for submodule liveness in delete_all_unused_submodules ([#178320](https://github.com/pytorch/pytorch/pull/178320))
- [perf] Avoid recomputing invariant work in SymNode.expr and tensor metadata ([#192677](https://github.com/pytorch/pytorch/pull/192677))
### docs
### devs
### Untopiced
- Bound wide unbacked substitutions in optimization_hint ([#185884](https://github.com/pytorch/pytorch/pull/185884))
- Preserve signed zero in FX complex codegen ([#185550](https://github.com/pytorch/pytorch/pull/185550))
- [PT2] Preserve symbolic metadata across tracing ([#187231](https://github.com/pytorch/pytorch/pull/187231))
- add specific dynamic spec message on data dependnet errors when dyanmic spec API is used. ([#187143](https://github.com/pytorch/pytorch/pull/187143))
- [dynamo, 3.15] Silence linecache warning ([#187221](https://github.com/pytorch/pytorch/pull/187221))
- [ShapesSpec] @dynamic_spec decorator for attaching ShapesSpec to functions/modules. (DS property of compiled function) ([#187639](https://github.com/pytorch/pytorch/pull/187639))
- Propagate local ranges during symbolic simplification ([#187350](https://github.com/pytorch/pytorch/pull/187350))
- Revert "Tighten generalized scatter graph target (#184075)" ([#188219](https://github.com/pytorch/pytorch/pull/188219))
- [dynamo, nested graph breaks] fix complex constant codegen for nan/inf imaginary parts ([#188596](https://github.com/pytorch/pytorch/pull/188596))
- Preserve device index in functorch minifier repro inputs ([#186547](https://github.com/pytorch/pytorch/pull/186547))
- [dynamic_shapes][bugfix] Rebuild sympy.Pow in proxy tracing (#188278) ([#188278](https://github.com/pytorch/pytorch/pull/188278))
- fx: Fix incorrect return_annotation for tuple types in operator schemas ([#189142](https://github.com/pytorch/pytorch/pull/189142))
- [fx][const_fold] apply skip_folding_node_fn recursively to call_module subgraphs (#189487) ([#189487](https://github.com/pytorch/pytorch/pull/189487))
- [torchfuzz] Make gather/index_select indices deterministic across runs ([#189553](https://github.com/pytorch/pytorch/pull/189553))
- Simplify Min/Max using ShapeEnv value ranges ([#186248](https://github.com/pytorch/pytorch/pull/186248))
- Fix non-deterministic node ordering in get_source_partitions() ([#188965](https://github.com/pytorch/pytorch/pull/188965))
- [make_fx] Decompose detach by default for higher-order grads ([#186845](https://github.com/pytorch/pytorch/pull/186845))
- Fix FX GraphModule serialization of string annotations ([#185051](https://github.com/pytorch/pytorch/pull/185051))
- [cond] Register max(size, 1) stride key form in branch output merging ([#189525](https://github.com/pytorch/pytorch/pull/189525))
- [FX] Fix TorchScript scripting on Python 3.14 (#190580) ([#190580](https://github.com/pytorch/pytorch/pull/190580))
- [fx] const_fold: forward an is_impure_node callback to eliminate_dead_code (#190716) ([#190716](https://github.com/pytorch/pytorch/pull/190716))
- [fx] _rename_unbacked_to: unify instead of assert on unbacked dest (#190083) ([#190083](https://github.com/pytorch/pytorch/pull/190083))
- [PyTorch][FX] Skip const folding for get_attr nodes with unresolvable/module targets ([#191939](https://github.com/pytorch/pytorch/pull/191939))
- [Torch] Preserve non-persistent buffers in fx.GraphModule (#191708) ([#191708](https://github.com/pytorch/pytorch/pull/191708))
- Fix Z3 translation validation for torch.sym_not ([#185147](https://github.com/pytorch/pytorch/pull/185147))
### not user facing
- [fx] Support boxed call argument lifetimes in codegen ([#187186](https://github.com/pytorch/pytorch/pull/187186))
- Fix test_profiler_stack_trace_augmentation on Windows ([#188491](https://github.com/pytorch/pytorch/pull/188491))
### security
