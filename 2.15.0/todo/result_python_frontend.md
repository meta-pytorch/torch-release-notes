
# Release Notes worksheet python_frontend

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

## python_frontend
### bc breaking
- Nested tensors are no longer allowlisted for `torch.load(..., weights_only=True)` ([#194380](https://github.com/pytorch/pytorch/pull/194380))

  Nested jagged and strided nested tensors are no longer on the default `weights_only` allowlist. Loading a checkpoint that contains one with `weights_only=True` (the default) now fails with `Unsupported global: GLOBAL torch.nested._internal.nested_tensor._rebuild_njt was not an allowed global by default` (or `GLOBAL torch._utils._rebuild_nested_tensor` for strided nested tensors). Opt in with `torch.serialization.safe_globals`, or use `weights_only=False` for trusted files.

  Version 2.14:
  ```python
  loaded = torch.load("njt.pt", weights_only=True)  # works
  ```

  Version 2.15:
  ```python
  from torch.nested._internal.nested_tensor import _rebuild_njt, NestedTensor
  with torch.serialization.safe_globals([_rebuild_njt, NestedTensor]):
      loaded = torch.load("njt.pt", weights_only=True)
  ```

- `import torch` can no longer be re-executed in the same process, including via `importlib.reload(torch)` ([#194654](https://github.com/pytorch/pytorch/pull/194654))

  `importlib.reload(torch)` and `del sys.modules["torch"]` + re-import now raise, as does retrying `import torch` after it failed. Re-running the module body was already unsafe in exactly the same way as the retry, so the new check does not distinguish the two. Normal use is unaffected: a successful import leaves `torch` in `sys.modules` so the body never re-runs, and re-entrant imports from a backend extension during autoload still short-circuit on `sys.modules` without reaching the check.

  Version 2.14:
  ```python
  import importlib
  import torch

  importlib.reload(torch)
  # RuntimeError: Only a single TORCH_LIBRARY can be used to register the namespace triton; ...
  # (re-importing after a failed `import torch` failed with similarly misleading errors or could segfault)
  ```

  Version 2.15:
  ```python
  import importlib
  import torch

  importlib.reload(torch)
  # ImportError: `torch` can only be initialized once per process, so this module cannot
  # be imported again: neither via `importlib.reload(torch)`, nor by re-importing after
  # a failed `import torch`.
  ```

### deprecation
### new features
### improvements
- Saturate out-of-range integer scalar bounds in `clamp` and `hardtanh` instead of wrapping or raising (e.g. `torch.clamp(uint8_tensor, min=-255)` is a no-op) ([#193169](https://github.com/pytorch/pytorch/pull/193169))
- Support empty batch dimensions in FFT operations on CPU, CUDA and MPS ([#190483](https://github.com/pytorch/pytorch/pull/190483))
- Add `skip_unsupported` to `FlopCounterMode` to warn instead of failing on higher-order operators without a FLOP formula, and count `flex_attention` FLOPs ([#167224](https://github.com/pytorch/pytorch/pull/167224))
- Support `Optional[list[Tensor]]` annotations in `torch.library.infer_schema` and `custom_op` ([#187012](https://github.com/pytorch/pytorch/pull/187012))
- Make `torch.iinfo` and `torch.finfo` hashable ([#193290](https://github.com/pytorch/pytorch/pull/193290))
- Name the context manager in tracebacks through `torch.no_grad`-style decorators ([#186502](https://github.com/pytorch/pytorch/pull/186502))
- Raise `NotImplementedError` instead of `RuntimeError` for `mean`, `var`, `std` and related ops on integer tensors ([#192351](https://github.com/pytorch/pytorch/pull/192351))
- Improve type stubs for `Tensor @ scalar` and `torch.utils` re-exports ([#195220](https://github.com/pytorch/pytorch/pull/195220), [#195289](https://github.com/pytorch/pytorch/pull/195289))
- Add `torch.mtia.is_current_stream_capturing()` ([#196354](https://github.com/pytorch/pytorch/pull/196354))
### bug fixes
- Fix `torch.asarray` on buffer-protocol objects to take the dtype from the buffer format ([#188784](https://github.com/pytorch/pytorch/pull/188784))
- Fix `torch.load` with `map_location="meta"` or `FakeTensorMode` losing storage sharing ([#193566](https://github.com/pytorch/pytorch/pull/193566))
- Fix `torch.aminmax` returning wrong results for overlapping `out=` tensors ([#195342](https://github.com/pytorch/pytorch/pull/195342))
- Fix `torch.accelerator.empty_host_cache()` segfaulting on MPS ([#197593](https://github.com/pytorch/pytorch/pull/197593))
- Fix `Multinomial.entropy()` precision for `float64` and after `expand()` ([#198006](https://github.com/pytorch/pytorch/pull/198006))
- Fix `torch.finfo(torch.float8_e5m2fnuz).eps` being off by 2x ([#198855](https://github.com/pytorch/pytorch/pull/198855))
- Fix `Tensor.__dlpack__` exporting tensors on a non-current non-CUDA device ([#195721](https://github.com/pytorch/pytorch/pull/195721))
- Fix `torch.isinf`/`isfinite` raising for fp8 dtypes without infinity ([#197444](https://github.com/pytorch/pytorch/pull/197444))
- Fix `FlopCounterMode` for CPU flash attention and nested attention backward ([#195801](https://github.com/pytorch/pytorch/pull/195801), [#196461](https://github.com/pytorch/pytorch/pull/196461))
### performance
- Reduce `TensorIterator` overhead and dtype refcount contention under free-threading ([#194422](https://github.com/pytorch/pytorch/pull/194422), [#194371](https://github.com/pytorch/pytorch/pull/194371))
### docs
- Document undefined behavior of bool tensors holding bytes other than 0/1, and clarify `Tensor.index_add_`'s `index` argument ([#199012](https://github.com/pytorch/pytorch/pull/199012), [#193403](https://github.com/pytorch/pytorch/pull/193403))
### devs
### Untopiced
### not user facing
- Enable more `test_ops.py` tests on XPU and define XPU expected failures in the OpInfo database ([#178849](https://github.com/pytorch/pytorch/pull/178849), [#179549](https://github.com/pytorch/pytorch/pull/179549))
- Fix the `rand_like` OpInfo entry, which tested `torch.randn_like` ([#193975](https://github.com/pytorch/pytorch/pull/193975))
- Fix the `nn.functional.threshold` OpInfo reference inputs for NumPy >= 2.5 strict `uint8` casting ([#189273](https://github.com/pytorch/pytorch/pull/189273))
- Fix a stale test-class name in the `conv_transpose3d` redispatch skip ([#196608](https://github.com/pytorch/pytorch/pull/196608))
- Widen the fp16 redispatch test tolerance for `linear_cross_entropy` OpInfos ([#197565](https://github.com/pytorch/pytorch/pull/197565))
- Skip the `conv_transpose1d` complex32 reference test on MI200 ([#198025](https://github.com/pytorch/pytorch/pull/198025))
- Make `tensor[indices] = scalar` dispatch to `index_fill_` instead of first materializing the scalar as a tensor ([#195787](https://github.com/pytorch/pytorch/pull/195787)) (cut for length)
### security
- Fix `torch.load(weights_only=True)` exposing uninitialized pybind11-backed objects (such as DTensor placements) when a checkpoint uses the `NEWOBJ` opcode without a matching `BUILD`; such checkpoints are now rejected as corrupt or malicious ([#194647](https://github.com/pytorch/pytorch/pull/194647))
- Fix a stack buffer overflow in `torch_shm_manager` (libshm) when the Unix socket path is too long (e.g. a long `TMPDIR`); it now raises an error ([#195183](https://github.com/pytorch/pytorch/pull/195183))
