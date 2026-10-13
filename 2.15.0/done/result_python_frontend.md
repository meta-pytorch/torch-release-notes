
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

  Nested jagged tensors (NJTs) and strided nested tensors are no longer on the default `weights_only` allowlist, and importing `torch.nested` no longer calls `torch.serialization.add_safe_globals` for them. Loading a checkpoint that contains a nested tensor with `weights_only=True` (the default for `torch.load`) now fails with the generic unsupported-global error, for example `Unsupported global: GLOBAL torch.nested._internal.nested_tensor._rebuild_njt was not an allowed global by default` (or `GLOBAL torch._utils._rebuild_nested_tensor` for strided nested tensors). To keep loading such checkpoints, opt in explicitly with `torch.serialization.safe_globals` (or `add_safe_globals`), or load with `weights_only=False` if you trust the file.

  Version 2.14:
  ```python
  import torch

  njt = torch.nested.nested_tensor([[1, 2, 3], [4, 5]], layout=torch.jagged)
  torch.save(njt, "njt.pt")
  loaded = torch.load("njt.pt", weights_only=True)  # works
  ```

  Version 2.15:
  ```python
  import torch
  from torch.nested._internal.nested_tensor import _rebuild_njt, NestedTensor

  njt = torch.nested.nested_tensor([[1, 2, 3], [4, 5]], layout=torch.jagged)
  torch.save(njt, "njt.pt")
  torch.load("njt.pt", weights_only=True)
  # _pickle.UnpicklingError: Weights only load failed. ... Unsupported global:
  # GLOBAL torch.nested._internal.nested_tensor._rebuild_njt was not an allowed global by default ...

  with torch.serialization.safe_globals([_rebuild_njt, NestedTensor]):
      loaded = torch.load("njt.pt", weights_only=True)  # works

  # Strided nested tensors:
  with torch.serialization.safe_globals([torch._utils._rebuild_nested_tensor]):
      loaded = torch.load("strided_nt.pt", weights_only=True)
  ```

- `import torch` can no longer be re-executed in the same process, including via `importlib.reload(torch)` ([#194654](https://github.com/pytorch/pytorch/pull/194654))

  Re-running `torch/__init__.py` (retrying `import torch` after it raised, `importlib.reload(torch)`, or `del sys.modules["torch"]` followed by `import torch`) re-initializes C++ global state that is already live. This corrupted memory and could later segfault at interpreter shutdown, or raise misleading errors such as `Only a single TORCH_LIBRARY can be used to register the namespace triton`. Any second execution of the module body now raises `ImportError: `torch` can only be initialized once per process, so this module cannot be imported again: neither via `importlib.reload(torch)`, nor by re-importing after a failed `import torch`.` A normal successful `import torch` is unaffected. If you relied on reloading `torch`, start a new Python process instead; if your first import fails, fix the cause and restart the interpreter.

  Version 2.14:
  ```python
  import importlib
  import torch

  importlib.reload(torch)  # appeared to work, but left the process in a corrupted state
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
- Integer scalar `clamp` bounds outside the input dtype's range are now saturated: a bound that cannot be reached becomes a no-op instead of wrapping around or raising (e.g. `torch.clamp(uint8_tensor, min=-255)` returns the input unchanged), while bounds that would force every element out of range (e.g. `min=256` for `uint8`) still raise; `hardtanh` follows the same rule, so negative bounds are now accepted for `uint8` inputs ([#193169](https://github.com/pytorch/pytorch/pull/193169))
- Support empty batch dimensions in FFT operations on CPU (MKL), CUDA and MPS, which previously failed with backend errors such as `CUFFT_INVALID_SIZE` ([#190483](https://github.com/pytorch/pytorch/pull/190483))
- Add a `skip_unsupported` argument to `torch.utils.flop_counter.FlopCounterMode`; when enabled, higher-order operators without a registered FLOP formula run with a warning and are reported by the new `get_unsupported_ops()` method instead of failing, and higher-order operators with a registered formula (such as `flex_attention`) are now counted ([#167224](https://github.com/pytorch/pytorch/pull/167224))
- Support `Optional[list[Tensor]]` and `Optional[list[Optional[Tensor]]]` annotations in `torch.library.infer_schema` (and therefore `torch.library.custom_op`) ([#187012](https://github.com/pytorch/pytorch/pull/187012))
- Make `torch.iinfo` and `torch.finfo` objects hashable, consistent with their equality, so they can be carried across graph breaks in `torch.compile` ([#193290](https://github.com/pytorch/pytorch/pull/193290))
- Tracebacks through functions decorated with `torch.no_grad`, `torch.inference_mode` and other context-manager decorators now name the context manager instead of a generic `decorate_context` frame ([#186502](https://github.com/pytorch/pytorch/pull/186502))
- `mean`, `var`, `std`, `var_mean`, `std_mean`, `nanmean` and `gradient` on integer tensors now raise `NotImplementedError` (a `RuntimeError` subclass) instead of a plain `RuntimeError` ([#192351](https://github.com/pytorch/pytorch/pull/192351))
- Improve type stubs: `Tensor @ scalar` is now rejected by static type checkers (it already raised `TypeError` at runtime), and `torch.utils` re-exports such as `ThroughputBenchmark` and `rename_privateuse1_backend` are marked as explicit ([#195220](https://github.com/pytorch/pytorch/pull/195220), [#195289](https://github.com/pytorch/pytorch/pull/195289))
- Add `torch.mtia.is_current_stream_capturing()`, matching the CUDA and XPU APIs, so device-agnostic code using `torch.get_device_module(device).is_current_stream_capturing()` works on MTIA ([#196354](https://github.com/pytorch/pytorch/pull/196354))
### bug fixes
- Fix `torch.asarray` on buffer-protocol objects (e.g. `array.array`, `memoryview`) without an explicit `dtype`: the dtype is now read from the buffer's declared format instead of being guessed, and unsupported formats or non-native byte order now raise an error asking for an explicit `dtype` ([#188784](https://github.com/pytorch/pytorch/pull/188784))
- Fix `torch.load` with `map_location="meta"` or under `FakeTensorMode` creating a separate storage for every reference to a shared storage, which dropped view/storage sharing and inflated the apparent checkpoint size ([#193566](https://github.com/pytorch/pytorch/pull/193566))
- Fix `torch.aminmax(x, out=(t, t))` silently returning wrong results when the two `out=` tensors overlap; it now raises an error ([#195342](https://github.com/pytorch/pytorch/pull/195342))
- Fix `torch.accelerator.empty_host_cache()` segfaulting on backends without a host allocator (such as MPS); it is now a no-op there ([#197593](https://github.com/pytorch/pytorch/pull/197593))
- Fix `torch.distributions.Multinomial.entropy()` losing precision for `float64` distributions and raising `AttributeError` after `expand()` ([#198006](https://github.com/pytorch/pytorch/pull/198006))
- Fix `torch.finfo(torch.float8_e5m2fnuz).eps` (and the C++ `std::numeric_limits` `epsilon()`/`round_error()`) returning values that were off by a factor of two ([#198855](https://github.com/pytorch/pytorch/pull/198855))
- Fix `Tensor.__dlpack__` silently exporting a tensor that lives on a non-current device on accelerators other than CUDA (e.g. XPU); the existing CUDA check now applies to every accelerator ([#195721](https://github.com/pytorch/pytorch/pull/195721))
- Fix `torch.isinf` and `torch.isfinite` raising `NotImplementedError` for fp8 dtypes that cannot represent infinity (`float8_e4m3fn`, `float8_e4m3fnuz`, `float8_e5m2fnuz`, `float8_e8m0fnu`) ([#197444](https://github.com/pytorch/pytorch/pull/197444))
- Fix `torch.utils.flop_counter.FlopCounterMode` reporting zero FLOPs for CPU flash attention, and failing on packed (nested) flash/efficient attention backward when the value head dimension differs from the query/key head dimension ([#195801](https://github.com/pytorch/pytorch/pull/195801), [#196461](https://github.com/pytorch/pytorch/pull/196461))
### performance
- Make `torch` dtype, layout, memory format and qscheme objects immortal, removing reference-count contention when many threads use them on free-threaded Python ([#194371](https://github.com/pytorch/pytorch/pull/194371))
- Reduce `TensorIterator` construction overhead, especially for all-contiguous inputs ([#194422](https://github.com/pytorch/pytorch/pull/194422))
- Make `tensor[indices] = scalar` dispatch to `index_fill_` instead of first materializing the scalar as a tensor ([#195787](https://github.com/pytorch/pytorch/pull/195787))
### docs
- Document that bool tensors whose bytes are neither 0 nor 1 (e.g. from `Tensor.view(torch.bool)` or `torch.empty(..., dtype=torch.bool)`) have undefined behavior ([#199012](https://github.com/pytorch/pytorch/pull/199012))
- Clarify that the `index` argument of `Tensor.index_add_` selects destination positions in `self` ([#193403](https://github.com/pytorch/pytorch/pull/193403))
### devs
### Untopiced
### not user facing
- Enable more `test_ops.py` tests on XPU and define XPU expected failures in the OpInfo database ([#178849](https://github.com/pytorch/pytorch/pull/178849), [#179549](https://github.com/pytorch/pytorch/pull/179549))
- Fix the `rand_like` OpInfo entry, which tested `torch.randn_like` ([#193975](https://github.com/pytorch/pytorch/pull/193975))
- Fix the `nn.functional.threshold` OpInfo reference inputs for NumPy >= 2.5 strict `uint8` casting ([#189273](https://github.com/pytorch/pytorch/pull/189273))
- Fix a stale test-class name in the `conv_transpose3d` redispatch skip ([#196608](https://github.com/pytorch/pytorch/pull/196608))
- Widen the fp16 redispatch test tolerance for `linear_cross_entropy` OpInfos ([#197565](https://github.com/pytorch/pytorch/pull/197565))
- Skip the `conv_transpose1d` complex32 reference test on MI200 ([#198025](https://github.com/pytorch/pytorch/pull/198025))
### security
- Fix `torch.load(weights_only=True)` exposing uninitialized pybind11-backed objects (such as DTensor placements) when a checkpoint uses the `NEWOBJ` opcode without a matching `BUILD`; such checkpoints are now rejected as corrupt or malicious ([#194647](https://github.com/pytorch/pytorch/pull/194647))
- Fix a stack buffer overflow in `torch_shm_manager` (libshm) when the Unix socket path is too long (e.g. a long `TMPDIR`); it now raises an error ([#195183](https://github.com/pytorch/pytorch/pull/195183))
