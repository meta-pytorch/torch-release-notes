
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
- Support fake-tensor tracing of sparse compressed tensor constructors (`torch.sparse_compressed_tensor` and friends), `_to_dense` for every sparse layout, and layout queries on `FunctionalTensor`s that wrap sparse tensors, as groundwork for compiling sparse compressed tensor creation ([#192091](https://github.com/pytorch/pytorch/pull/192091))
- Fix type annotations on FX public APIs: `Tracer(autowrap_modules=...)` now accepts any-length `tuple[ModuleType, ...]`, and `CodeGen.process_inputs` returns `tuple[Any, ...]` ([#195467](https://github.com/pytorch/pytorch/pull/195467), [#188287](https://github.com/pytorch/pytorch/pull/188287))
### bug fixes
- Keep `torch._check(not expr)` on a symbolic boolean as a runtime assertion under `torch.compile` and strict export by lowering Python `not` to `torch.sym_not`, instead of constant-folding it away and later failing with a data-dependent guard error; non-strict export now gives an error hint that points to `torch.sym_not()` ([#186043](https://github.com/pytorch/pytorch/pull/186043))
- Fix `TypeError` from `expect_true` and symbolic solving when comparing two symbolic booleans for equality (e.g. `Eq(Eq(u0, 1), Eq(u1, 1))`) ([#186461](https://github.com/pytorch/pytorch/pull/186461))
- Fix `IndexError: list index out of range` and `AssertionError: sources must not be empty for symbol` in guard generation when recompiling a model that takes a jagged `NestedTensor` input whose batch size changes ([#193059](https://github.com/pytorch/pytorch/pull/193059))
- Fix unguardable guards for `NestedTensor` reductions with `keepdim=True` by statically evaluating symbolic expressions that only involve the nested (ragged) size ([#184628](https://github.com/pytorch/pytorch/pull/184628))
- Fix `AttributeError: 'int' object has no attribute 'is_nonnegative'` when lowering a modulo of two plain integers during symbolic shape computation ([#198395](https://github.com/pytorch/pytorch/pull/198395))
- Simplify `C * (x // C)` back to `x` when `x` is known to be divisible by `C`, so equivalent symbolic shapes such as `x` and `2 * (x // 2)` are recognized as equal again ([#198808](https://github.com/pytorch/pytorch/pull/198808))
- Fix `assert_size_stride` failures such as `stride 24576==14336 at dim=0` on the second call of a compiled training graph under dynamic shapes, by keeping the strides of saved activations symbolic instead of baking in the first call's values ([#194420](https://github.com/pytorch/pytorch/pull/194420))
- Fix silently stale results under `torch._dynamo.config.specialize_float=False`, where a Python float argument used by an op that cannot take a tensor scalar was baked into a cached graph and reused for later calls with a different value ([#195040](https://github.com/pytorch/pytorch/pull/195040))
- Fix `torch._dynamo.config.canonicalize_output_graph_node_order=True` moving computation outside a `torch.inference_mode()` region, which made outputs silently require grad ([#195518](https://github.com/pytorch/pytorch/pull/195518))
- Fix AOTInductor silently dropping deferred runtime assertions on data-dependent sizes (for example `torch._check(x.nonzero().size(0) < 10)`) when lite mode (`selective_decompose`) is enabled ([#199294](https://github.com/pytorch/pytorch/pull/199294))
- Fix pickling and `torch.load` of `GraphModule`s produced by `aot_export_module` and non-strict `torch.export` ([#186418](https://github.com/pytorch/pytorch/pull/186418))
- Fix `RuntimeError: Cannot access data pointer of Tensor` when pickling an FX graph with `GraphPickler` whose node metadata contains a fake view tensor ([#194771](https://github.com/pytorch/pytorch/pull/194771))
- Fix printing an FX graph whose node metadata holds a BSR or BSC sparse tensor, which raised `Sparse BSR tensors do not have strides` and broke exporting such models when `TORCH_TRACE` was set ([#195253](https://github.com/pytorch/pytorch/pull/195253))
- Fix `torch.fx.subgraph_rewriter.replace_pattern` leaving a topologically invalid graph when adjacent matches share a node through a list argument (for example nested `torch.cat` patterns) ([#185365](https://github.com/pytorch/pytorch/pull/185365))
- Fix `torch.fx.wrap` keeping its caller's stack frames, and every tensor they reference, alive until the cyclic garbage collector runs ([#198561](https://github.com/pytorch/pytorch/pull/198561))
- Fix `torch.export` permanently retaining every traced graph, and through it the module and its parameters, in a debug-only map used for fake-tensor leak detection ([#198295](https://github.com/pytorch/pytorch/pull/198295))
- Make the FX accelerator splitter's fusion discovery deterministic, so identical graphs always produce the same accelerator submodules ([#198684](https://github.com/pytorch/pytorch/pull/198684))
- Fix `KeyError` in `torch.fx.experimental.shape_inference` when `ShapeEnv` assigns non-sequential symbol names ([#197491](https://github.com/pytorch/pytorch/pull/197491))
### performance
- Reduce compile time under dynamic shapes by caching the results of symbolic binary arithmetic, skipping `ShapeEnv` event-recording overhead when recording is off, and avoiding repeated free-symbol scans during axiom matching (about 2% total compile time from event recording alone on a reported model) ([#193219](https://github.com/pytorch/pytorch/pull/193219), [#193161](https://github.com/pytorch/pytorch/pull/193161), [#195623](https://github.com/pytorch/pytorch/pull/195623))
- Avoid deep-copying `from_node` provenance in FX `NodeSource`, removing roughly quadratic cost in the number of passes and cutting a reported export-and-lowering workflow from 406s to 342s ([#193051](https://github.com/pytorch/pytorch/pull/193051))
- Speed up the FX accelerator splitter on large graphs by skipping fusion discovery when every node is supported and making fusion dependency updates linear in fusion group size ([#198519](https://github.com/pytorch/pytorch/pull/198519), [#198654](https://github.com/pytorch/pytorch/pull/198654))
### docs
### devs
- Fix generated minifier repros failing with `allocated size does not match required size` when a `repeat_interleave` input uses `int32` repeats ([#197035](https://github.com/pytorch/pytorch/pull/197035))
### Untopiced
### not user facing
- Support `torch.nn.functional.scaled_addmm` and `scaled_addmm_` under `torch.compile`, lowered through Inductor's extern-kernel fallback with reinplacing of the functional form ([#195410](https://github.com/pytorch/pytorch/pull/195410)) (may belong in nn_frontend, next to #195409)
- Skip `ShapeEnv.replace` for symbolic booleans that are already constant; no measurable wall-clock change ([#193159](https://github.com/pytorch/pytorch/pull/193159))
- Make tensor device observations rank-portable under the in-progress compile-on-one-rank mode ([#196151](https://github.com/pytorch/pytorch/pull/196151))
- Add hardware classification to FX test classes ([#192455](https://github.com/pytorch/pytorch/pull/192455), [#192470](https://github.com/pytorch/pytorch/pull/192470), [#192450](https://github.com/pytorch/pytorch/pull/192450), [#192451](https://github.com/pytorch/pytorch/pull/192451), [#193274](https://github.com/pytorch/pytorch/pull/193274), [#192929](https://github.com/pytorch/pytorch/pull/192929), [#194857](https://github.com/pytorch/pytorch/pull/194857), [#194879](https://github.com/pytorch/pytorch/pull/194879), [#192742](https://github.com/pytorch/pytorch/pull/192742))
### security
