
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
- The deprecated `use_cuda` argument has been removed from `torch.profiler.profile` and `torch.autograd.profiler.profile` ([#192543](https://github.com/pytorch/pytorch/pull/192543))

    Passing `use_cuda` to either profiler now raises `TypeError: profile.__init__() got an unexpected keyword argument 'use_cuda'`. Select CUDA explicitly through `activities` when using `torch.profiler.profile`, or use `use_device="cuda"` with `torch.autograd.profiler.profile`.

    Version 2.13:

    ```python
    with torch.profiler.profile(use_cuda=True) as prof:
        run_workload()

    with torch.autograd.profiler.profile(use_cuda=True) as prof:
        run_workload()
    ```

    Version 2.14:

    ```python
    with torch.profiler.profile(
        activities=[
            torch.profiler.ProfilerActivity.CPU,
            torch.profiler.ProfilerActivity.CUDA,
        ]
    ) as prof:
        run_workload()

    with torch.autograd.profiler.profile(use_device="cuda") as prof:
        run_workload()
    ```

### deprecation
- The experimental `profiler_metrics` and `profiler_measure_per_kernel` options no longer enable CUPTI range profiling and now emit a `FutureWarning` when supplied ([#187204](https://github.com/pytorch/pytorch/pull/187204))

    Kineto no longer supports this range-profiler path on PyTorch's supported CUDA versions. The arguments remain accepted temporarily for compatibility, but they are ignored and have no direct replacement.

    Before:

    ```python
    config = torch.profiler._ExperimentalConfig(
        profiler_metrics=["sm__cycles_elapsed.avg"],
        profiler_measure_per_kernel=True,
    )
    ```

    After:

    ```python
    config = torch.profiler._ExperimentalConfig()
    ```

- The `with_modules` profiler option is deprecated and now emits a `FutureWarning` ([#192808](https://github.com/pytorch/pytorch/pull/192808))

    `with_modules=True` only collected module hierarchy for TorchScript models and did nothing in eager mode. For eager models, use `with_stack=True` to record `nn.Module` events.

    Before:

    ```python
    with torch.profiler.profile(with_modules=True) as prof:
        run_workload()
    ```

    After:

    ```python
    with torch.profiler.profile(with_stack=True) as prof:
        run_workload()
    ```

### new features
- Memory snapshots can now include CPU pinned-memory allocations by passing `record_pinned_host_memory=True` to `torch.cuda.memory._record_memory_history()` ([#182407](https://github.com/pytorch/pytorch/pull/182407))

    Pinned-memory allocator state and history are available in the snapshot's `host_segments` and `host_traces` fields. Pass `record_cuda=False` to record only pinned host memory; the web memory visualizer does not yet display host-memory data.

- Profiler events now expose Kineto metadata as typed values through `FunctionEvent.metadata` when `expose_kineto_event_metadata=True` is enabled ([#191756](https://github.com/pytorch/pytorch/pull/191756))

    The new dictionary avoids reparsing JSON strings and automatically includes metadata fields supported by the active profiler backend.

### improvements
- XPU profiling now records `OVERHEAD` activities, making the profiler's own collection cost visible on a dedicated track in exported traces ([#187835](https://github.com/pytorch/pytorch/pull/187835))

### bug fixes
- `key_averages()` now excludes individual Python function events by default so frames such as `threading.py: wait` do not obscure operator-level hotspots; pass `include_python_functions=True` to retain the previous view ([#188631](https://github.com/pytorch/pytorch/pull/188631))
- Clamp incomplete Python function events to their parent event's end time so exported traces retain correct nesting instead of placing overrunning events on unrelated tracks ([#190950](https://github.com/pytorch/pytorch/pull/190950))
- Avoid importing the experimental CUPTI monitor during ordinary `record_function` profiling, preventing repeated warnings and tracebacks on systems with incompatible `cupti-python` versions ([#187874](https://github.com/pytorch/pytorch/pull/187874))
- Fix reference leaks when reading the `layout` and `dtype` properties of profiler tensor metadata ([#187068](https://github.com/pytorch/pytorch/pull/187068))

### performance
### docs
### devs
- Add documented CUDA graph instantiate and destroy hooks for the experimental CUPTI monitor, allowing it to observe graph lifecycles without modifying graph execution code ([#191299](https://github.com/pytorch/pytorch/pull/191299))

### Untopiced
### not user facing
- Remove unused private profiler-analysis helpers and the obsolete Python CUPTI reference decoder ([#187362](https://github.com/pytorch/pytorch/pull/187362), [#187439](https://github.com/pytorch/pytorch/pull/187439), [#188096](https://github.com/pytorch/pytorch/pull/188096))
- Expand, reorganize, and stabilize profiler tests and diagnostics without changing production behavior ([#186970](https://github.com/pytorch/pytorch/pull/186970), [#187363](https://github.com/pytorch/pytorch/pull/187363), [#188210](https://github.com/pytorch/pytorch/pull/188210), [#186812](https://github.com/pytorch/pytorch/pull/186812), [#188753](https://github.com/pytorch/pytorch/pull/188753), [#188264](https://github.com/pytorch/pytorch/pull/188264), [#189559](https://github.com/pytorch/pytorch/pull/189559), [#191668](https://github.com/pytorch/pytorch/pull/191668), [#185617](https://github.com/pytorch/pytorch/pull/185617))
- Refactor the experimental CUPTI monitor's record schema, native decoder, multiplexer, observer routing, clock alignment, code generation, background flushing, singleton configuration, and version-gated timestamp and filtering paths ([#186811](https://github.com/pytorch/pytorch/pull/186811), [#187515](https://github.com/pytorch/pytorch/pull/187515), [#186439](https://github.com/pytorch/pytorch/pull/186439), [#186855](https://github.com/pytorch/pytorch/pull/186855), [#188942](https://github.com/pytorch/pytorch/pull/188942), [#189168](https://github.com/pytorch/pytorch/pull/189168), [#189109](https://github.com/pytorch/pytorch/pull/189109), [#188621](https://github.com/pytorch/pytorch/pull/188621), [#189083](https://github.com/pytorch/pytorch/pull/189083), [#189185](https://github.com/pytorch/pytorch/pull/189185), [#190353](https://github.com/pytorch/pytorch/pull/190353), [#190354](https://github.com/pytorch/pytorch/pull/190354))
- Add private CUPTI-monitor support for graph-node timing, peer-to-peer copy records, performance-monitor sampling, GPU counters, logical lanes, graph dependencies and graph-node rendering, and native Perfetto export ([#186802](https://github.com/pytorch/pytorch/pull/186802), [#188211](https://github.com/pytorch/pytorch/pull/188211), [#188849](https://github.com/pytorch/pytorch/pull/188849), [#188019](https://github.com/pytorch/pytorch/pull/188019), [#190411](https://github.com/pytorch/pytorch/pull/190411), [#190850](https://github.com/pytorch/pytorch/pull/190850), [#190851](https://github.com/pytorch/pytorch/pull/190851), [#191689](https://github.com/pytorch/pytorch/pull/191689), [#191690](https://github.com/pytorch/pytorch/pull/191690), [#188939](https://github.com/pytorch/pytorch/pull/188939), [#187898](https://github.com/pytorch/pytorch/pull/187898), [#191667](https://github.com/pytorch/pytorch/pull/191667))
- Convert internal profiler and NCCL metadata plumbing to typed fields ([#189442](https://github.com/pytorch/pytorch/pull/189442), [#190676](https://github.com/pytorch/pytorch/pull/190676), [#190371](https://github.com/pytorch/pytorch/pull/190371), [#190923](https://github.com/pytorch/pytorch/pull/190923))
- Harden experimental CUPTI trace export and metadata presentation around observer-registration failures, copy-engine channels, graph node identifiers, and captured-graph annotation spans ([#188132](https://github.com/pytorch/pytorch/pull/188132), [#190962](https://github.com/pytorch/pytorch/pull/190962), [#191119](https://github.com/pytorch/pytorch/pull/191119), [#191118](https://github.com/pytorch/pytorch/pull/191118))
- Vendor and package the build prerequisites for experimental Perfetto and CUPTI support ([#188018](https://github.com/pytorch/pytorch/pull/188018), [#192260](https://github.com/pytorch/pytorch/pull/192260))

### security
