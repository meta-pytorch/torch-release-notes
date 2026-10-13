
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

    `TORCH_DISABLE_ADDR2LINE` now defaults to on. Launching `addr2line` to symbolize C++ frames is slow and can hang, so it was commonly disabled in production. This affects every place PyTorch symbolizes captured C++ stacks, such as `TORCH_SHOW_CPP_STACKTRACES=1` error messages and C++ frames in CUDA memory snapshots recorded with `torch.cuda.memory._record_memory_history(stacks="all")`. With `dladdr`, C++ frames report the shared library and offset plus the exported symbol name when one is available, instead of a source file and line number, and the `symbolizing C++ stack trace for exception; if this hangs, rerun with TORCH_DISABLE_ADDR2LINE=1...` warning is no longer printed. To get file/line information back, set `TORCH_DISABLE_ADDR2LINE=0`. `TORCH_SYMBOLIZE_MODE` (`dladdr`, `addr2line`, or `fast`) still takes precedence when set.

    Version 2.14:

    ```bash
    # addr2line symbolization by default
    TORCH_SHOW_CPP_STACKTRACES=1 python train.py
    ```

    Version 2.15:

    ```bash
    # dladdr symbolization by default; opt back into addr2line with either of:
    TORCH_SHOW_CPP_STACKTRACES=1 TORCH_DISABLE_ADDR2LINE=0 python train.py
    TORCH_SHOW_CPP_STACKTRACES=1 TORCH_SYMBOLIZE_MODE=addr2line python train.py
    ```

- CUDA memory snapshots record the allocator's `mallocWithAddress` tag in a new `internal_metadata` field instead of appending it to `user_metadata` ([#193432](https://github.com/pytorch/pytorch/pull/193432))

    When the caching allocator serves an exact-address allocation (for example `UntypedStorage._resize_with_addr_`), it records a synthetic malloc/free pair for the prefix block and tags it as `mallocWithAddress`. Previously it did this by temporarily appending `"\nmallocWithAddress"` to the thread's user metadata, which changed what users set with `torch.cuda.memory._set_memory_metadata` and broke metadata that was JSON. Now `user_metadata` in trace entries from `torch.cuda.memory._snapshot()` is exactly what the user set, and the tag appears under a separate `internal_metadata` key that is only present when the allocator tagged the event. The memory visualizer shows it under "Internal Metadata". Tools that searched `user_metadata` for `mallocWithAddress` must read `internal_metadata` instead. As part of this change, `torch.cuda.memory._set_memory_metadata` also accepts a dict, which is stored as compact JSON.

    Version 2.14:

    ```python
    trace = torch.cuda.memory._snapshot()["device_traces"][device]
    tagged = [e for e in trace if "mallocWithAddress" in e["user_metadata"]]
    ```

    Version 2.15:

    ```python
    trace = torch.cuda.memory._snapshot()["device_traces"][device]
    tagged = [e for e in trace if e.get("internal_metadata") == "mallocWithAddress"]
    ```

- Remove the deprecated `profiler_metrics` and `profiler_measure_per_kernel` arguments from `torch._C._profiler._ExperimentalConfig` ([#198262](https://github.com/pytorch/pytorch/pull/198262))

    These options have been ignored and have emitted a `FutureWarning` since 2.14. Passing them by keyword now raises a `TypeError` from the `_ExperimentalConfig` constructor, and the read-only `profiler_metrics` / `profiler_measure_per_kernel` attributes are gone. Because they were the first two constructor arguments, every remaining argument moved two positions to the left: code that builds `_ExperimentalConfig` positionally will silently set the wrong options and must switch to keyword arguments. The pickled state layout also changed, so `_ExperimentalConfig` objects pickled by earlier releases cannot be restored. Drop the arguments; there is no replacement. To collect hardware counters, use `torch.profiler.PerformanceMetricsConfig` (see new features).

    Version 2.14:

    ```python
    cfg = torch._C._profiler._ExperimentalConfig(
        profiler_metrics=["sm__cycles_elapsed.avg"],
        profiler_measure_per_kernel=True,
        verbose=True,
    )
    ```

    Version 2.15:

    ```python
    cfg = torch._C._profiler._ExperimentalConfig(verbose=True)
    ```

- Remove the deprecated `FunctionEvent.metadata_json` property ([#198265](https://github.com/pytorch/pytorch/pull/198265))

    `metadata_json` was deprecated in 2.12. Accessing it on events from `prof.events()` now raises `AttributeError: 'FunctionEvent' object has no attribute 'metadata_json'`, and the `metadata_json` constructor argument of `torch.autograd.profiler_util.FunctionEvent` is removed. The 2.12 deprecation message pointed to `event_metadata`, but that is itself deprecated in this release (see deprecations), so use `FunctionEvent.metadata`, a dict of typed values populated when `_ExperimentalConfig(expose_kineto_event_metadata=True)` is set.

    Version 2.14:

    ```python
    for event in prof.events():
        metadata = event.metadata_json  # JSON string, FutureWarning
    ```

    Version 2.15:

    ```python
    for event in prof.events():
        metadata = event.metadata  # dict[str, Any] or None
    ```

- Rename the experimental CUPTI monitor profiler backend to Cuspy, without aliases for the old names ([#195881](https://github.com/pytorch/pytorch/pull/195881))

    The experimental in-process CUPTI collection backend selected through `_ExperimentalConfig(custom_profiler_config=...)` is now called Cuspy. The backend value `"cupti_monitor"` is now `"cuspy"`, the `{"cupti_monitor": true}` key is now `{"cuspy": true}`, and the `"cupti_monitor_async_export"` key is now `"cuspy_async_export"`. The old backend names are no longer recognized and the profiler silently falls back to the default Kineto backend. Setting `"cupti_monitor_async_export"` no longer raises an error. The private `torch.profiler._cupti` package moved to `torch.profiler._cuspy` and `torch._C._profiler._cupti_monitor` to `torch._C._profiler._cuspy`. Prefer the new `torch.profiler.CuspyConfig` (see new features) over `custom_profiler_config`.

    Version 2.14:

    ```python
    cfg = _ExperimentalConfig(
        custom_profiler_config='{"backend":"cupti_monitor","cupti_monitor_async_export":true}'
    )
    ```

    Version 2.15:

    ```python
    cfg = _ExperimentalConfig(
        custom_profiler_config='{"backend":"cuspy","cuspy_async_export":true}'
    )
    ```

### deprecation
- The experimental `adjust_profiler_step` option of `_ExperimentalConfig` is deprecated and no longer has any effect ([#193042](https://github.com/pytorch/pytorch/pull/193042))

    `adjust_profiler_step=True` used to move the start of each `ProfilerStep#N` annotation forward to its parent Python event so the two did not partly overlap. Moving the annotation made downstream tools misreport step durations, and the option has been off by default since it was moved behind the experimental config. The alignment has been removed. Passing `adjust_profiler_step=True` (by keyword or position) now emits `FutureWarning: adjust_profiler_step is deprecated and ignored. It will be removed in a future release.` when the profiler starts. Remove the argument.

    Version 2.14:

    ```python
    with torch.profiler.profile(
        experimental_config=torch._C._profiler._ExperimentalConfig(adjust_profiler_step=True),
    ) as prof:
        ...
    ```

    Version 2.15:

    ```python
    with torch.profiler.profile() as prof:
        ...
    ```

- `torch.autograd.profiler.load_nvprof`, `torch.autograd.profiler.parse_nvprof_trace`, and `torch.autograd.profiler.EnforceUnique` are deprecated and will be removed in PyTorch 2.17 ([#198396](https://github.com/pytorch/pytorch/pull/198396))

    These helpers read traces from NVIDIA's `nvprof`, which is deprecated and does not support recent GPUs. Calling them now emits a `FutureWarning` such as `` `torch.autograd.profiler.load_nvprof` is deprecated and will be removed in PyTorch 2.17. `` Use `torch.profiler.profile` to collect GPU traces, or run under Nsight Systems with `torch.autograd.profiler.emit_nvtx()` for NVTX ranges.

    Version 2.14:

    ```python
    events = torch.autograd.profiler.load_nvprof("trace.prof")
    ```

    Version 2.15:

    ```python
    with torch.profiler.profile(
        activities=[torch.profiler.ProfilerActivity.CPU, torch.profiler.ProfilerActivity.CUDA]
    ) as prof:
        run_workload()
    events = prof.events()
    ```

- `FunctionEvent.event_metadata` is deprecated in favor of `FunctionEvent.metadata` ([#198405](https://github.com/pytorch/pytorch/pull/198405))

    `event_metadata` returned an `EventMetadata` object built from raw string metadata. `metadata` is a plain `dict[str, Any]` of typed values, and it now also includes fields that Kineto stores as raw JSON, so it carries everything `event_metadata` did. Accessing `event_metadata` now emits `` FutureWarning: `event_metadata` is deprecated. Use `metadata` instead. ``

    Version 2.14:

    ```python
    grid = event.event_metadata.grid
    ```

    Version 2.15:

    ```python
    grid = event.metadata["grid"]
    ```

### new features
- Add `torch.profiler.ProfilerActivityConfig` and `torch.profiler.PerformanceMetricsConfig` to configure extra collection, such as CUDA hardware performance counters, per activity group ([#196065](https://github.com/pytorch/pytorch/pull/196065))

    An entry in the `activities` argument of `torch.profiler.profile` can now map a `ProfilerActivity` to a `ProfilerActivityConfig` (the existing form, a list of activity-type names, still works). `ProfilerActivityConfig.activity_types` selects the fine-grained activity types to collect (`None` keeps the defaults), and `profiler_configs` takes extra profiler configurations. `PerformanceMetricsConfig(metric_names=..., sampling_interval_ms=..., lookback_window_ms=...)` collects CUPTI PM sampling metrics on the current CUDA device; this requires a Kineto build with CUPTI PM sampling support.

    ```python
    from torch.profiler import (
        PerformanceMetricsConfig, profile, ProfilerActivity, ProfilerActivityConfig,
    )

    cuda_config = ProfilerActivityConfig(
        profiler_configs=[PerformanceMetricsConfig(metric_names=["sm__cycles_active.avg"])]
    )
    with profile(activities=[ProfilerActivity.CPU, {ProfilerActivity.CUDA: cuda_config}]) as prof:
        run_workload()
    ```

- Add `torch.profiler.CuspyConfig` to enable the experimental Cuspy CUDA collection backend without `_ExperimentalConfig` ([#196066](https://github.com/pytorch/pytorch/pull/196066))

    Pass a `CuspyConfig` in the `profiler_configs` of the CUDA `ProfilerActivityConfig` to use Cuspy. Its flags `enable_cuda_sync_events`, `enable_environment_counters`, `enable_graph_dependencies`, and `enable_event_node_ids` replace the matching `custom_profiler_config` keys, and a `PerformanceMetricsConfig` in the same list configures Cuspy's PM sampling for that session. CPU activity must also be enabled. The `custom_profiler_config` route still works during the migration.

    ```python
    cuda_config = torch.profiler.ProfilerActivityConfig(
        profiler_configs=[
            torch.profiler.PerformanceMetricsConfig(
                metric_names=["sm__cycles_active.avg.pct_of_peak_sustained_elapsed"],
            ),
            torch.profiler.CuspyConfig(enable_graph_dependencies=True),
        ],
    )
    with torch.profiler.profile(
        activities=[
            torch.profiler.ProfilerActivity.CPU,
            {torch.profiler.ProfilerActivity.CUDA: cuda_config},
        ],
    ) as prof:
        run_workload()
    ```

- Record the Python launch stack of each CUDA graph node during capture ([#198419](https://github.com/pytorch/pytorch/pull/198419))

    Capture with `torch.cuda.graph(g, enable_annotations=True, annotation_config={"record_py_stacks": True})` to record the user Python frames that launched each kernel, memcpy, memset, event, and host node. Read them with `torch.cuda.graph_annotations.get_kernel_py_stacks()` or save them as gzip-compressed JSON next to a trace with `torch.cuda.graph_annotations.dump_kernel_py_stacks(path)`. Framework and generated Inductor frames are filtered by default; `annotation_config["py_stack_filter_paths"]` replaces the filter list (`[]` disables filtering). Recording requires `cupti-python` and CUPTI >= 13.3, and needs a CUPTI subscription that no other profiler holds.

    ```python
    from torch.cuda.graph_annotations import dump_kernel_py_stacks

    g = torch.cuda.CUDAGraph()
    with (
        torch.autograd.grad_mode.set_multithreading_enabled(False),
        torch.cuda.graph(g, enable_annotations=True, annotation_config={"record_py_stacks": True}),
    ):
        y = x @ x.t()
    dump_kernel_py_stacks("graph_stacks.json.gz")
    ```

### improvements
- Cuspy now resolves CUDA graph annotations by the capture graph's node id, so graphs captured with `annotation_config={"key_by": "source"}` show their annotations in Cuspy traces ([#196529](https://github.com/pytorch/pytorch/pull/196529))
### bug fixes
- Fix device time of profiler events being inflated by unrelated runtime/driver events that share a correlation id ([#196282](https://github.com/pytorch/pytorch/pull/196282))
- Fix `record_function` kwargs metadata being passed to Kineto as raw JSON fragments instead of typed values ([#196352](https://github.com/pytorch/pytorch/pull/196352))
- Fix intermittent heap corruption at profiler teardown in the experimental CUPTI monitor (Cuspy) backend caused by freeing activity buffers CUPTI still owned ([#195471](https://github.com/pytorch/pytorch/pull/195471))
- Fix the profiler warning for free-threaded Python never being emitted on Python 3.13t ([#194697](https://github.com/pytorch/pytorch/pull/194697))
### performance
### docs
- Fix C++-style comments in the `toggle_collection_dynamic` example of `torch.profiler.profile` ([#190369](https://github.com/pytorch/pytorch/pull/190369))
### devs
- Kineto source is now part of the PyTorch repository under `third_party/kineto` instead of a git submodule ([#198648](https://github.com/pytorch/pytorch/pull/198648))
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
### security
