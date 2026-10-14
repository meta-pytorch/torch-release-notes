
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
- Support fake-tensor tracing of sparse compressed tensor constructors and `_to_dense` ([#192091](https://github.com/pytorch/pytorch/pull/192091))
- Fix type annotations on `Tracer(autowrap_modules=...)` and `CodeGen.process_inputs` ([#195467](https://github.com/pytorch/pytorch/pull/195467), [#188287](https://github.com/pytorch/pytorch/pull/188287))
### bug fixes
- Keep `torch._check(not expr)` on a symbolic boolean as a runtime assertion, and fix a `TypeError` comparing two symbolic booleans ([#186043](https://github.com/pytorch/pytorch/pull/186043), [#186461](https://github.com/pytorch/pytorch/pull/186461))
- Fix guard errors for jagged `NestedTensor` inputs whose batch size changes or with `keepdim=True` reductions ([#193059](https://github.com/pytorch/pytorch/pull/193059), [#184628](https://github.com/pytorch/pytorch/pull/184628))
- Fix a crash on modulo of plain ints in symbolic shapes, and simplify `C * (x // C)` back to `x` ([#198395](https://github.com/pytorch/pytorch/pull/198395), [#198808](https://github.com/pytorch/pytorch/pull/198808))
- Fix `assert_size_stride` failures on the second call of a compiled training graph under dynamic shapes ([#194420](https://github.com/pytorch/pytorch/pull/194420))
- Fix stale results from a float argument baked into a cached graph under `specialize_float=False` ([#195040](https://github.com/pytorch/pytorch/pull/195040))
- Fix `canonicalize_output_graph_node_order` moving ops out of `inference_mode`, making outputs require grad ([#195518](https://github.com/pytorch/pytorch/pull/195518))
- Fix AOTInductor dropping runtime assertions on data-dependent sizes in lite mode ([#199294](https://github.com/pytorch/pytorch/pull/199294))
- Fix pickling `GraphModule`s from `aot_export_module` and non-strict export, and graphs with fake view tensors in metadata ([#186418](https://github.com/pytorch/pytorch/pull/186418), [#194771](https://github.com/pytorch/pytorch/pull/194771))
- Fix printing FX graphs with BSR or BSC tensors in node metadata ([#195253](https://github.com/pytorch/pytorch/pull/195253))
- Fix `replace_pattern` producing an invalid graph when adjacent matches share a node ([#185365](https://github.com/pytorch/pytorch/pull/185365))
- Fix memory leaks from `torch.fx.wrap` keeping caller frames alive and `torch.export` retaining every traced graph ([#198561](https://github.com/pytorch/pytorch/pull/198561), [#198295](https://github.com/pytorch/pytorch/pull/198295))
- Make the FX accelerator splitter's fusion discovery deterministic ([#198684](https://github.com/pytorch/pytorch/pull/198684))
- Fix `KeyError` in `shape_inference` with non-sequential symbol names ([#197491](https://github.com/pytorch/pytorch/pull/197491))
### performance
- Reduce compile time in `ShapeEnv` and FX `from_node` provenance tracking ([#193219](https://github.com/pytorch/pytorch/pull/193219), [#193161](https://github.com/pytorch/pytorch/pull/193161), [#195623](https://github.com/pytorch/pytorch/pull/195623), [#193051](https://github.com/pytorch/pytorch/pull/193051))
- Speed up the FX accelerator splitter on large graphs ([#198519](https://github.com/pytorch/pytorch/pull/198519), [#198654](https://github.com/pytorch/pytorch/pull/198654))
### docs
### devs
- Fix minifier repros failing for `repeat_interleave` with `int32` repeats ([#197035](https://github.com/pytorch/pytorch/pull/197035))
### Untopiced
### not user facing
- Skip `ShapeEnv.replace` for symbolic booleans that are already constant; no measurable wall-clock change ([#193159](https://github.com/pytorch/pytorch/pull/193159))
- Make tensor device observations rank-portable under the in-progress compile-on-one-rank mode ([#196151](https://github.com/pytorch/pytorch/pull/196151))
- Add hardware classification to FX test classes ([#192455](https://github.com/pytorch/pytorch/pull/192455), [#192470](https://github.com/pytorch/pytorch/pull/192470), [#192450](https://github.com/pytorch/pytorch/pull/192450), [#192451](https://github.com/pytorch/pytorch/pull/192451), [#193274](https://github.com/pytorch/pytorch/pull/193274), [#192929](https://github.com/pytorch/pytorch/pull/192929), [#194857](https://github.com/pytorch/pytorch/pull/194857), [#194879](https://github.com/pytorch/pytorch/pull/194879), [#192742](https://github.com/pytorch/pytorch/pull/192742))
### security
