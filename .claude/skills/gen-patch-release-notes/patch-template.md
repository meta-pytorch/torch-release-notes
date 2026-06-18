# Patch release notes — target structure and examples

Patch (bug-fix) releases are **minimal**. The whole document is: a one-line title, a one-sentence
intro, an optional regression section, and a handful of category buckets with one terse bullet per
fix. No feature writeups, no BC-breaking migration guides, no before/after code.

## Skeleton

```markdown
# PyTorch X.Y.Z Release, bug fix release

This release is meant to fix the following regressions and silent correctness issues:

## Regression fixes
- <plain-language symptom of the regression> ([#<issue>](https://github.com/pytorch/pytorch/issues/<issue>), [#<fixPR>](https://github.com/pytorch/pytorch/pull/<fixPR>))

## Torch.compile
- <short fix description> ([#<PR>](https://github.com/pytorch/pytorch/pull/<PR>))

## Distributed
- <short fix description> ([#<PR>](https://github.com/pytorch/pytorch/pull/<PR>))

## Other
- <short fix description> ([#<PR>](https://github.com/pytorch/pytorch/pull/<PR>))

The release notes were generated from cherry-picks onto the `release/X.Y` branch. For installation
instructions see https://pytorch.org/get-started/locally/ .
```

Rules:
- Only include sections that have entries; drop empty ones.
- `## Regression fixes` first (fixed-in-this-release regressions). Use `## Tracked Regressions`
  instead only for *known, still-open* regressions shipping with the release that need a workaround.
- `## Other` is always last.
- Group multiple PRs that fix the same thing into one bullet with multiple links.

## Section headers seen in real patch releases

- **Regression fixes** / **Tracked Regressions**
- **Torch.compile**  (dynamo, inductor, export, fx)
- **Flex Attention**
- **Distributed**
- **CUDA**
- **MPS** / **MacOS**
- **ROCm**, **XPU**
- **Releng / Build**
- **Other**

## Worked example — abridged v2.9.1

```markdown
# PyTorch 2.9.1 Release, bug fix release

This release is meant to fix the following regressions and silent correctness issues:

## Tracked Regressions
- Significant memory regression in `F.conv3d` with bfloat16 inputs, introduced in 2.9.0.
  Workaround: install `nvidia-cudnn` 9.15+ from PyPI.
  ([#166643](https://github.com/pytorch/pytorch/issues/166643), [#166480](https://github.com/pytorch/pytorch/pull/166480), [#167111](https://github.com/pytorch/pytorch/pull/167111))

## Torch.compile
- Fix Inductor bug compiling Gemma ([#165601](https://github.com/pytorch/pytorch/pull/165601))
- Fix `InternalTorchDynamoError` in bytecode transformation ([#166036](https://github.com/pytorch/pytorch/pull/166036))
- Fix silent correctness bug in `error_on_graph_break` checkpoint handling ([#166586](https://github.com/pytorch/pytorch/pull/166586))
- Fix crash in `torch.bmm` with `torch.compile` ([#166457](https://github.com/pytorch/pytorch/pull/166457))

## Other
- Fix distributed crash with non-contiguous gather inputs ([#166181](https://github.com/pytorch/pytorch/pull/166181))
- Fix numeric issue in `CUDNN_ATTENTION` ([#166912](https://github.com/pytorch/pytorch/pull/166912), [#166570](https://github.com/pytorch/pytorch/pull/166570))
```

## Worked example — abridged v2.7.1 (shows more category buckets)

```markdown
# PyTorch 2.7.1 Release, bug fix release

This release is meant to fix the following regressions and silent correctness issues:

## Torch.compile
- Fix excessive cudagraph re-recording for HF LLM models ([#152287](https://github.com/pytorch/pytorch/pull/152287))
- Fix crash from exceptions in `torch.autocast` ([#152503](https://github.com/pytorch/pytorch/pull/152503))

## Flex Attention
- Fix assertion error from inductor permuting inputs ([#151959](https://github.com/pytorch/pytorch/pull/151959))
- Fix performance regression on nanogpt speedrun ([#152641](https://github.com/pytorch/pytorch/pull/152641))

## Distributed
- Fix extra CUDA context created by barrier ([#149144](https://github.com/pytorch/pytorch/pull/149144))
- Workaround for a random hang in NCCL 2.26 non-blocking mode ([#154055](https://github.com/pytorch/pytorch/pull/154055))

## MacOS
- Fix compilation error with Clang 17 ([#151344](https://github.com/pytorch/pytorch/pull/151344))
- Fix incorrect binary kernel results with wrapped scalar args on MPS ([#152997](https://github.com/pytorch/pytorch/pull/152997))

## Other
- Fix floating point exception in `torch.mkldnn_max_pool2d` ([#151848](https://github.com/pytorch/pytorch/pull/151848))
- Fix segfault in profiler with Python 3.13 ([#153848](https://github.com/pytorch/pytorch/pull/153848))
```
