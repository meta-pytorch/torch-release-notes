
# Release Notes worksheet profiler

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

## profiler
### bc breaking
- C++ stack traces are now symbolized with `dladdr` instead of `addr2line` by default ([#195462](https://github.com/pytorch/pytorch/pull/195462))

  `TORCH_DISABLE_ADDR2LINE` now defaults to on, since `addr2line` is slow and can hang. C++ frames in `TORCH_SHOW_CPP_STACKTRACES=1` errors and CUDA memory snapshots now show the library path and offset, plus the symbol name only if exported (otherwise `??`). To restore `addr2line`, set `TORCH_DISABLE_ADDR2LINE=0` or `TORCH_SYMBOLIZE_MODE=addr2line`.

  ```bash
  TORCH_SHOW_CPP_STACKTRACES=1 TORCH_DISABLE_ADDR2LINE=0 python train.py
  ```

- CUDA memory snapshots record the allocator's `mallocWithAddress` tag in a new `internal_metadata` field instead of appending it to `user_metadata` ([#193432](https://github.com/pytorch/pytorch/pull/193432))

  `user_metadata` in `torch.cuda.memory._snapshot()` trace entries is now exactly what was set with `torch.cuda.memory._set_memory_metadata` (which now also accepts a dict). Tools that searched `user_metadata` for `mallocWithAddress` must read `internal_metadata` instead.

  ```python
  # 2.14
  tagged = [e for e in trace if "mallocWithAddress" in e["user_metadata"]]
  # 2.15
  tagged = [e for e in trace if e.get("internal_metadata") == "mallocWithAddress"]
  ```

- Remove the deprecated `FunctionEvent.metadata_json` property ([#198265](https://github.com/pytorch/pytorch/pull/198265))

  Accessing it now raises `AttributeError: 'FunctionEvent' object has no attribute 'metadata_json'`, and the `metadata_json` constructor argument is removed. Use `FunctionEvent.metadata`, a dict populated when `_ExperimentalConfig(expose_kineto_event_metadata=True)` is set (not the deprecated `event_metadata`).

  ```python
  metadata = event.metadata_json  # 2.14: JSON string
  metadata = event.metadata  # 2.15: dict[str, Any] or None
  ```

- Rename the experimental CUPTI monitor profiler backend to Cuspy, without aliases for the old names ([#195881](https://github.com/pytorch/pytorch/pull/195881))

  In `_ExperimentalConfig(custom_profiler_config=...)`, `"cupti_monitor"` is now `"cuspy"` and `"cupti_monitor_async_export"` is now `"cuspy_async_export"`; old names silently fall back to the default Kineto backend. `prof.take_pending_cupti_export()` is now `take_pending_cuspy_export()` (the old name raises `AttributeError`). Prefer the new `torch.profiler.CuspyConfig`.

  ```python
  # 2.14
  cfg = _ExperimentalConfig(custom_profiler_config='{"backend":"cupti_monitor"}')
  # 2.15
  cfg = _ExperimentalConfig(custom_profiler_config='{"backend":"cuspy"}')
  ```

### deprecation
- `torch.autograd.profiler.load_nvprof`, `parse_nvprof_trace` and `EnforceUnique` are deprecated and will be removed in PyTorch 2.17 ([#198396](https://github.com/pytorch/pytorch/pull/198396))

  `nvprof` does not support recent GPUs. They now emit a `FutureWarning` such as `` `torch.autograd.profiler.load_nvprof` is deprecated and will be removed in PyTorch 2.17. `` Use `torch.profiler.profile` or Nsight Systems with `torch.autograd.profiler.emit_nvtx()`.

  ```python
  events = torch.autograd.profiler.load_nvprof("trace.prof")  # 2.14
  with torch.profiler.profile() as prof:  # 2.15
      run_workload()
  ```

- `FunctionEvent.event_metadata` is deprecated in favor of `FunctionEvent.metadata` ([#198405](https://github.com/pytorch/pytorch/pull/198405))

  `metadata` is a typed `dict[str, Any]` with everything `event_metadata` had. Accessing `event_metadata` emits `` FutureWarning: `event_metadata` is deprecated. Use `metadata` instead. ``

  ```python
  grid = event.event_metadata.grid  # 2.14
  grid = event.metadata["grid"]  # 2.15
  ```
### new features
- Add `torch.profiler.ProfilerActivityConfig` and `torch.profiler.PerformanceMetricsConfig` to configure collection per activity group, such as CUDA hardware performance counters ([#196065](https://github.com/pytorch/pytorch/pull/196065))
- Add `torch.profiler.CuspyConfig` to enable the experimental Cuspy CUDA collection backend without `_ExperimentalConfig` ([#196066](https://github.com/pytorch/pytorch/pull/196066))
- Record the Python launch stack of each CUDA graph node during capture with `annotation_config={"record_py_stacks": True}`, read via `torch.cuda.graph_annotations.get_kernel_py_stacks()` (requires CUPTI >= 13.3) ([#198419](https://github.com/pytorch/pytorch/pull/198419))

### improvements
- Show `key_by="source"` CUDA graph annotations in Cuspy traces ([#196529](https://github.com/pytorch/pytorch/pull/196529))
### bug fixes
- Fix inflated profiler device times from events sharing a correlation id ([#196282](https://github.com/pytorch/pytorch/pull/196282))
- Fix Cuspy teardown heap corruption and `record_function` kwargs sent as raw JSON ([#195471](https://github.com/pytorch/pytorch/pull/195471), [#196352](https://github.com/pytorch/pytorch/pull/196352))
### performance
### docs
- Fix the `toggle_collection_dynamic` example ([#190369](https://github.com/pytorch/pytorch/pull/190369))
### devs
- Kineto source now lives in `third_party/kineto` instead of a git submodule ([#198648](https://github.com/pytorch/pytorch/pull/198648))
- Remove the ignored `profiler_metrics` and `profiler_measure_per_kernel` `_ExperimentalConfig` arguments (now a `TypeError`), and deprecate the no-op `adjust_profiler_step` option ([#198262](https://github.com/pytorch/pytorch/pull/198262), [#193042](https://github.com/pytorch/pytorch/pull/193042))
### Untopiced
### not user facing
- [profiler][cupti] Turn kernel latency timestamps back off when nothing wants QUEUED ([#192370](https://github.com/pytorch/pytorch/pull/192370))
- [profiler][cupti] Give logical lanes their own reserved id range ([#192393](https://github.com/pytorch/pytorch/pull/192393))
- [profiler][cuspy] Use the documented forced flush when a field selection changes ([#196548](https://github.com/pytorch/pytorch/pull/196548))
- [Profiler] Add a merge rule for Profiler ([#197474](https://github.com/pytorch/pytorch/pull/197474))
- [Profiler] Fix up test_python_export_envelope_matches_kineto  ([#195935](https://github.com/pytorch/pytorch/pull/195935))
- [Profiler] Lint exclusions to prepare for upstreaming ([#198013](https://github.com/pytorch/pytorch/pull/198013))
- [Profiler] Add one more person to the Profiler merge rule ([#198009](https://github.com/pytorch/pytorch/pull/198009))
- [Profiler] Read event idx directly in collection.cpp ([#198665](https://github.com/pytorch/pytorch/pull/198665))
- [Profiler] Simplify how shape handling works in collection.cpp ([#198540](https://github.com/pytorch/pytorch/pull/198540))
- [Profiler] Enable Kineto tests ([#198813](https://github.com/pytorch/pytorch/pull/198813))
- [profiler][xpu] Test that ac2g CPU->GPU flow arrows end on the device ([#194904](https://github.com/pytorch/pytorch/pull/194904))
- [Profiler] Update Kineto readme ([#199364](https://github.com/pytorch/pytorch/pull/199364))
- [Profiler] Delete unneeded Kineto code ([#199359](https://github.com/pytorch/pytorch/pull/199359))
- Fix the profiler warning for free-threaded Python never being emitted on Python 3.13t ([#194697](https://github.com/pytorch/pytorch/pull/194697)) (cut for length)
### security
