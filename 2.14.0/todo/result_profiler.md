
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
### deprecation
### new features
- Support memory snapshot for CPU pinned memory ([#182407](https://github.com/pytorch/pytorch/pull/182407))
- Support memory snapshot for CPU pinned memory ([#182407](https://github.com/pytorch/pytorch/pull/182407))
### improvements
### bug fixes
### performance
### docs
### devs
### Untopiced
- Remove profiler_metrics and profiler_measure_per_kernel ([#187204](https://github.com/pytorch/pytorch/pull/187204))
- [Profiler] Remove pattern matcher and tests ([#187362](https://github.com/pytorch/pytorch/pull/187362))
- [Profiler] Remove BasicEvaluation class and tests ([#187439](https://github.com/pytorch/pytorch/pull/187439))
- [Profiler] Exclude Python function events from key_averages() by default ([#188631](https://github.com/pytorch/pytorch/pull/188631))
- [Profiler] Clamp overrun python events ([#190950](https://github.com/pytorch/pytorch/pull/190950))
- [profiler][cupti] Add generic CUDA-graph lifecycle hooks ([#191299](https://github.com/pytorch/pytorch/pull/191299))
- [Profiler] Add a path to build typed metadata events straight from Kineto ([#191756](https://github.com/pytorch/pytorch/pull/191756))
### not user facing
- [Profiler] Fix a set of profiler tests ([#186970](https://github.com/pytorch/pytorch/pull/186970))
- [Profiler] Reduce wait time for profiler test ([#187363](https://github.com/pytorch/pytorch/pull/187363))
- [profiler][cupti] Record-field registry + cupti-python record types for columnar decode ([#186811](https://github.com/pytorch/pytorch/pull/186811))
- [profiler][cupti] Native GIL-free decode worker (CuptiMonitorDecoder) ([#187515](https://github.com/pytorch/pytorch/pull/187515))
- [profiler][cupti] Make the CUPTI monitor a multiplexer with columnar UDR decoding ([#186439](https://github.com/pytorch/pytorch/pull/186439))
- [profiler][cupti] ProfilerObserver + record_function annotation routing ([#186855](https://github.com/pytorch/pytorch/pull/186855))
- [profiler][cupti] Only import the CUPTI monitor when a session is using it ([#187874](https://github.com/pytorch/pytorch/pull/187874))
- [profiler][cupti] Add NodeTimerObserver: always-on per-graph-node timing ([#186802](https://github.com/pytorch/pytorch/pull/186802))
- [profiler][cupti] Don't crash trace export when the ProfilerObserver fails to register ([#188132](https://github.com/pytorch/pytorch/pull/188132))
- [profiler][cupti] Add MEMCPY2 (peer-to-peer) record support ([#188211](https://github.com/pytorch/pytorch/pull/188211))
- [profiler][cupti] Vendor Perfetto C++ tracing SDK amalgamation (v56.1) ([#188018](https://github.com/pytorch/pytorch/pull/188018))
- [profiler][cupti] Move CUPTI monitor tests out of test_profiler.py ([#188210](https://github.com/pytorch/pytorch/pull/188210))
- [profiler][cupti] Tests for the CUPTI monitor: records + columnar decode ([#186812](https://github.com/pytorch/pytorch/pull/186812))
- [profiler][cupti] Remove unused Python reference decoder (CuptiMonitorBuffer) ([#188096](https://github.com/pytorch/pytorch/pull/188096))
- [Profiler] Disable profiler test which is causing test pollution ([#188753](https://github.com/pytorch/pytorch/pull/188753))
- [profiler][cupti] Align monitor record clock to kineto's realtime clock ([#188942](https://github.com/pytorch/pytorch/pull/188942))
- [profiler][cupti] PM sampling engine ([#188849](https://github.com/pytorch/pytorch/pull/188849))
- [profiler][cupti] PM-sampling GPU utilization counters (SM-active %, DRAM BW %) ([#188019](https://github.com/pytorch/pytorch/pull/188019))
- [profiler] Validate chrome trace by event name, not fixed offset ([#188264](https://github.com/pytorch/pytorch/pull/188264))
- [profiler][cupti] Engage the approx-clock timestamp callback via the per-subscriber attribute ([#189168](https://github.com/pytorch/pytorch/pull/189168))
- [profiler][cupti] Resolve a version-gated CUPTI header and conditionally install libclang for the field-id codegen ([#189109](https://github.com/pytorch/pytorch/pull/189109))
- [profiler][cupti] Generate CUPTI field-id catalogs from the ABI as Field(id, ctype) ([#188621](https://github.com/pytorch/pytorch/pull/188621))
- [Profiler] Add logging to failing metadatajson test ([#189559](https://github.com/pytorch/pytorch/pull/189559))
- [Profiler] Use Kineto typed metadata fields for PyTorch-side generic metadata ([#189442](https://github.com/pytorch/pytorch/pull/189442))
- [profiler][cupti] Drive periodic cuptiActivityFlushAll from the decode thread ([#189083](https://github.com/pytorch/pytorch/pull/189083))
- [profiler][cupti] Make CuptiMonitor a singleton configured via a global configure() ([#189185](https://github.com/pytorch/pytorch/pull/189185))
- [profiler][cupti] Reassign graphed kernels onto a pluggable logical lane during export ([#190411](https://github.com/pytorch/pytorch/pull/190411))
- [profiler][cupti] Drop the decoder cbid-filter workaround ([#190353](https://github.com/pytorch/pytorch/pull/190353))
- [profiler][cupti] Arm the approx-timestamp callback even with a pre-existing CUDA context ([#190354](https://github.com/pytorch/pytorch/pull/190354))
- [Profiler] Use typed metadata for Event Idx ([#190676](https://github.com/pytorch/pytorch/pull/190676))
- [profiler][cupti] Select CHANNEL_ID/CHANNEL_TYPE for memcpy/memset activities ([#190962](https://github.com/pytorch/pytorch/pull/190962))
- [profiler][cupti] Emit only the lower 32-bit node id in the chrome trace args ([#191119](https://github.com/pytorch/pytorch/pull/191119))
- [profiler][cupti] Keep GPU user-annotation spans on the capture stream ([#191118](https://github.com/pytorch/pytorch/pull/191118))
- [Profiler] Pass typed NCCL metadata to Kineto ([#190371](https://github.com/pytorch/pytorch/pull/190371))
- [profiler][cupti] Record graph node dependencies and draw them in the JSON export ([#190850](https://github.com/pytorch/pytorch/pull/190850))
- [profiler][cupti] Clean up graph-node registries on CUDA graph destruction ([#190851](https://github.com/pytorch/pytorch/pull/190851))
- [Profiler] Use typed metadata for parent id ([#190923](https://github.com/pytorch/pytorch/pull/190923))
- [profiler] Enable OVERHEAD activity type for the XPU backend ([#187835](https://github.com/pytorch/pytorch/pull/187835))
- [profiler][cupti] CUDA_EVENT -> graph event-record node bridge, span rendering + dependency-arrow traversal ([#191689](https://github.com/pytorch/pytorch/pull/191689))
- [profiler][cupti] Render CUPTI GRAPH_HOST_NODE activity in the profiler export ([#191690](https://github.com/pytorch/pytorch/pull/191690))
- [profiler][cupti] Environment + per-kernel cycle GPU counters in the JSON export ([#188939](https://github.com/pytorch/pytorch/pull/188939))
- [profiler][cupti] Native protozero .pftrace encoder ([#187898](https://github.com/pytorch/pytorch/pull/187898))
- [profiler][cupti] Python .pftrace export from the columnar window ([#191667](https://github.com/pytorch/pytorch/pull/191667))
- [profiler][cupti] Tests for .pftrace export ([#191668](https://github.com/pytorch/pytorch/pull/191668))
- [torch][profiler] Fix refcount leaks in _TensorMetadata layout/dtype getters (#187068) ([#187068](https://github.com/pytorch/pytorch/pull/187068))
- [profiler][cupti] Install the generated _cupti_stubs.py into the wheel ([#192260](https://github.com/pytorch/pytorch/pull/192260))
- [Profiler] Refactor test_trace_validator.py ([#185617](https://github.com/pytorch/pytorch/pull/185617))
### security
