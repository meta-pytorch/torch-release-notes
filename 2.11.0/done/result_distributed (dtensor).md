
# Release Notes worksheet distributed (dtensor)

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

## distributed (dtensor)
### bc breaking
- `DTensor.to_local()` backward now converts `Partial` placements to `Replicate` by default when `grad_placements` is not provided. ([#173454](https://github.com/pytorch/pytorch/pull/173454))

  Previously, calling `to_local()` on a `Partial` DTensor would preserve the `Partial` placement in the backward gradient, which could produce incorrect gradients when combined with `from_local()`. Now, the backward pass automatically maps `Partial` forward placements to `Replicate` gradient placements, matching the behavior of `from_local()`.

  Users who relied on the previous behavior (where `to_local()` backward preserved `Partial` gradients) may see different gradient values. To ensure correctness, explicitly pass `grad_placements` to `to_local()`.

  Version 2.10:
  ```python
  # Partial placement preserved in backward — could produce incorrect gradients
  local_tensor = partial_dtensor.to_local()
  ```

  Version 2.11:
  ```python
  # Partial → Replicate in backward by default (correct behavior)
  local_tensor = partial_dtensor.to_local()
  # Or explicitly specify grad_placements for full control:
  local_tensor = partial_dtensor.to_local(grad_placements=[Replicate()])
  ```
- `_PhiloxState.seed` and `_PhiloxState.offset` now return `torch.Tensor` instead of `int` ([#173876](https://github.com/pytorch/pytorch/pull/173876))

  The DTensor RNG internal `_PhiloxState` class changed its `seed` and `offset` properties to return tensors instead of Python ints, and the setters now expect tensors. This makes the RNG state compatible with PT2 tracing (the previous `.item()` calls were not fake-tensor friendly).

  Code that directly reads `_PhiloxState.seed` or `_PhiloxState.offset` and treats them as ints will break. Call `.item()` to get the int value. When setting, wrap the value in a tensor.

  Version 2.10:
  ```python
  from torch.distributed.tensor._random import _PhiloxState

  philox = _PhiloxState(state)
  seed: int = philox.seed          # returned int
  philox.offset = 42               # accepted int
  ```

  Version 2.11:
  ```python
  from torch.distributed.tensor._random import _PhiloxState

  philox = _PhiloxState(state)
  seed: int = philox.seed.item()   # now returns Tensor; call .item() for int
  philox.offset = torch.tensor([42], dtype=torch.int64)  # must pass Tensor
  ```
### deprecation
### new features
### improvements
- Add OpSchema.args_meta, kwargs_meta helpers ([#170358](https://github.com/pytorch/pytorch/pull/170358))
- Support misc sym ops ([#172268](https://github.com/pytorch/pytorch/pull/172268))
- DTensor Ops: Add linearity support for neg operation ([#172563](https://github.com/pytorch/pytorch/pull/172563))
- Add SymInt support for DTensor mesh coordinate computation in PT2 ([#169552](https://github.com/pytorch/pytorch/pull/169552))
- Enable single-dim strategy for addmm and baddbmm ([#172387](https://github.com/pytorch/pytorch/pull/172387))
- Support uneven _StridedShard redistribution ([#172266](https://github.com/pytorch/pytorch/pull/172266))
- Update TP api to support single-dim strategies ([#173567](https://github.com/pytorch/pytorch/pull/173567))
- Initial support for decomps + sharding prop ([#171652](https://github.com/pytorch/pytorch/pull/171652))
- Add shard prop cache logging ([#173775](https://github.com/pytorch/pytorch/pull/173775))
- Optimize redistribute comms using flattened meshes ([#174630](https://github.com/pytorch/pytorch/pull/174630))
### bug fixes
- Preserve `Partial(max/min)` reduce op type on `torch.max`/`torch.min` output DTensors ([#170203](https://github.com/pytorch/pytorch/pull/170203))
- Prevent pointwise operations between `Partial` DTensors with different reduce ops ([#170209](https://github.com/pytorch/pytorch/pull/170209))
- Fix OpInfo.schema type and add asserts ([#170790](https://github.com/pytorch/pytorch/pull/170790))
- Fix _StridedShard(sf=) bug in single dim strategy ([#171942](https://github.com/pytorch/pytorch/pull/171942))
- Fix incorrect Tensor Meta Population ([#172304](https://github.com/pytorch/pytorch/pull/172304))
- Single_dim fix symint + _create_expanded_strategy ([#172421](https://github.com/pytorch/pytorch/pull/172421))
- Single dim fix inplace op expansion ([#172477](https://github.com/pytorch/pytorch/pull/172477))
- Fix single-dim output_meta validation ([#172293](https://github.com/pytorch/pytorch/pull/172293))
- Fix redistribute cost crashing on non-participating ranks ([#172478](https://github.com/pytorch/pytorch/pull/172478))
- Fix t() sharding strategy for 1D tensors ([#173964](https://github.com/pytorch/pytorch/pull/173964))
- Fix unsupported op error ([#170889](https://github.com/pytorch/pytorch/pull/170889))
- Fix DTensor honor single-dim RuntimeSchemaInfo ([#174312](https://github.com/pytorch/pytorch/pull/174312))
- Fix device_mesh extraction from kwargs ([#173489](https://github.com/pytorch/pytorch/pull/173489))
- Fix StridedShard usage conflict with shard order ([#174831](https://github.com/pytorch/pytorch/pull/174831))
- Fix bucketize with Partial inputs ([#173937](https://github.com/pytorch/pytorch/pull/173937))
- Fix embedding_dense_backward cache key missing num_weights ([#174727](https://github.com/pytorch/pytorch/pull/174727))
### performance
### docs
### devs
- Add DTensor performance benchmarks for collectives, `from_local`/`to_local`, and backward passes ([#171576](https://github.com/pytorch/pytorch/pull/171576))
- Add DTensor benchmarks for miscellaneous dispatch paths ([#171847](https://github.com/pytorch/pytorch/pull/171847))
### Untopiced
### not user facing
- Fix redistribute_cost to detect shard_order ([#170106](https://github.com/pytorch/pytorch/pull/170106))
- Fix redistribute_cost using incorrect comm_bytes_gb ([#170107](https://github.com/pytorch/pytorch/pull/170107))
- Refactor redistribute_cost function ([#170108](https://github.com/pytorch/pytorch/pull/170108))
- Update redistribute planner cost function based on communication cost ([#170109](https://github.com/pytorch/pytorch/pull/170109))
- Fix _StridedShard to Replicate padding issue ([#170914](https://github.com/pytorch/pytorch/pull/170914))
- Add conversion from Replicate to _StridedShard ([#171337](https://github.com/pytorch/pytorch/pull/171337))
- Make single-dim rules support multi-output ops ([#172257](https://github.com/pytorch/pytorch/pull/172257))
- Add type hints to torch/_functorch files ([#173543](https://github.com/pytorch/pytorch/pull/173543))
- Refactor _select_min_cost_strategy as a util ([#170197](https://github.com/pytorch/pytorch/pull/170197))
- Remove is_backward from redistribute_local_tensor ([#170147](https://github.com/pytorch/pytorch/pull/170147))
- Ensure op_info is never None in slow path ([#170584](https://github.com/pytorch/pytorch/pull/170584))
- Optimize strfmt for ExplicitRedistributionContext ([#170405](https://github.com/pytorch/pytorch/pull/170405))
- Hook up output tensor_meta to expand util ([#170827](https://github.com/pytorch/pytorch/pull/170827))
- Single-dim foreach strategy ([#170631](https://github.com/pytorch/pytorch/pull/170631))
- LRU cachable OpStrategy ([#171223](https://github.com/pytorch/pytorch/pull/171223))
- Make copy_ work with more Partial placements ([#170704](https://github.com/pytorch/pytorch/pull/170704))
- Ban redistribute from one partial type to another ([#172041](https://github.com/pytorch/pytorch/pull/172041))
- Make redistribution cost for different partials infinite ([#172042](https://github.com/pytorch/pytorch/pull/172042))
- Handle out= ops in single-dim expander ([#172276](https://github.com/pytorch/pytorch/pull/172276))
- Insert Replicate at beginning for matmul single dim ([#172150](https://github.com/pytorch/pytorch/pull/172150))
- DTensor Ops: Made aten.div.* linearity similar to aten.mul.* ([#172514](https://github.com/pytorch/pytorch/pull/172514))
- Make expand_to_full_mesh_op_strategy filter incompatible out= strategies ([#172420](https://github.com/pytorch/pytorch/pull/172420))
- Log DTensor output placements ([#172688](https://github.com/pytorch/pytorch/pull/172688))
- Redistribute to replicate in from_local backward for partial ([#173153](https://github.com/pytorch/pytorch/pull/173153))
- No-op redistribution shouldn't create _TransformInfo ([#172924](https://github.com/pytorch/pytorch/pull/172924))
- Single-dim strategy validation infra ([#172990](https://github.com/pytorch/pytorch/pull/172990))
- S->P(sum) strategy for _powsum ([#172604](https://github.com/pytorch/pytorch/pull/172604))
- Make RedistributionPlanner handle all partials ([#172479](https://github.com/pytorch/pytorch/pull/172479))
- Single-dim expander raises clear inplace error ([#173572](https://github.com/pytorch/pytorch/pull/173572))
- Infer RuntimeSchemaInfo for decomposition ops ([#174422](https://github.com/pytorch/pytorch/pull/174422))
- Set static args for decomp OpSchema ([#174616](https://github.com/pytorch/pytorch/pull/174616))
- Strategy Validation: placement utilities and data structures ([#174798](https://github.com/pytorch/pytorch/pull/174798))
- Skip decomposition for CIA ops ([#174918](https://github.com/pytorch/pytorch/pull/174918))
- Reapply "Refactor strategy/rule registration into dedicated module (#168221)" (a695f3cbd3c)
### security
