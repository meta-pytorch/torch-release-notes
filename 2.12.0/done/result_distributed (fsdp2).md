
# Release Notes worksheet distributed (fsdp2)

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

## distributed (fsdp2)
### bc breaking
### deprecation
- Compiling through FSDP2 hooks without graph breaks is no longer supported ([#174863](https://github.com/pytorch/pytorch/pull/174863), [#174906](https://github.com/pytorch/pytorch/pull/174906)). If you use compiled autograd with FSDP2, update your code to allow graph breaks around FSDP2 hooks or disable compiled autograd for the FSDP2 training step.

  Version 2.11:
  ```python
  with torch._dynamo.config.patch(compiled_autograd=True):
      compiled_model = torch.compile(fsdp_model, fullgraph=True)
      loss = compiled_model(input).sum()
      loss.backward()
  ```

  Version 2.12:
  ```python
  # Either run FSDP2 backward without fullgraph.
  compiled_model = torch.compile(fsdp_model, fullgraph=False)
  loss = compiled_model(input).sum()
  loss.backward()

  # Or apply compile before applying FSDP.
  compiled_model_pre_fsdp = torch.compile(model, fullgraph=True)
  compiled_model = fully_shard(compiled_model_pre_fsdp, ...)
  loss = compiled_model(input).sum()
  loss.backward()
  ```

### new features
- Support per-parameter meshes in FSDP2, enabling different parameter groups to shard over different meshes ([#173509](https://github.com/pytorch/pytorch/pull/173509))
- Support `fully_shard` with DTensors on a full SPMD mesh via `DataParallelMeshDims` ([#176334](https://github.com/pytorch/pytorch/pull/176334))
- Add FSDP2 support for non-floating-point parameters by excluding non-float parameters from reduce-scatter while still sharding and all-gathering them as needed ([#177948](https://github.com/pytorch/pytorch/pull/177948))
### improvements
- Allow `ModuleList`/`ModuleDict` subclasses that implement `forward()` ([#175033](https://github.com/pytorch/pytorch/pull/175033))
- FSDP2: Support dataclass args/kwargs output without memory leakage ([#174692](https://github.com/pytorch/pytorch/pull/174692))
- Share more implementation code between replicate and FSDP2 `fully_shard` ([#173580](https://github.com/pytorch/pytorch/pull/173580))
- Consolidate FSDP2 `shard_mesh` and `shard_mesh_from_root` handling ([#174107](https://github.com/pytorch/pytorch/pull/174107))
### bug fixes
- Fix FSDP2 `split_with_sizes_copy()` missing `dim` argument ([#169173](https://github.com/pytorch/pytorch/pull/169173))
- Fix mixed DTensor errors with nested FSDP and activation checkpointing ([#171779](https://github.com/pytorch/pytorch/pull/171779))
- Fix tied weights with uneven sharding across separate FSDP groups ([#176225](https://github.com/pytorch/pytorch/pull/176225))
- Revert FSDP2 communication-op FQN annotations due to `async_op=True` profiler trace issues ([#182100](https://github.com/pytorch/pytorch/pull/182100))
### performance
- Improve FSDP2 parameter FQN lookup from quadratic to linear complexity ([#174675](https://github.com/pytorch/pytorch/pull/174675))
- Overlap FSDP2 reduce-scatter with compute for per-parameter meshes ([#177319](https://github.com/pytorch/pytorch/pull/177319))
- Cache FSDP2 `shard_mesh` to avoid repeated submesh creation ([#179655](https://github.com/pytorch/pytorch/pull/179655))
### docs
### devs
- Fix `fully_shard` argument type hints for better type-checking consistency ([#171574](https://github.com/pytorch/pytorch/pull/171574))
### Untopiced
### not user facing
- Add CUDA graph coverage for FSDP2 ([#171835](https://github.com/pytorch/pytorch/pull/171835))
- Reverted or superseded FSDP2 changes with no standalone release-note entry ([#173415](https://github.com/pytorch/pytorch/pull/173415), [#173838](https://github.com/pytorch/pytorch/pull/173838))
- Run more FSDP2 tests on CPU ([#173986](https://github.com/pytorch/pytorch/pull/173986), [#174048](https://github.com/pytorch/pytorch/pull/174048))
### security
