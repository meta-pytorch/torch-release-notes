# PyTorch Release Blog — Output Template & Examples

Use this template when drafting a release blog. It mirrors the
structure of <https://pytorch.org/blog/pytorch-2-13-release-blog/>.

**Verify against the latest published post before drafting.** The
format drifts between releases; this file records it as of 2.13.

## Template

```markdown
We are excited to announce the release of PyTorch® <VERSION>
([release notes](https://github.com/pytorch/pytorch/releases/tag/v<VERSION>.0))!

The PyTorch <VERSION> release features the following changes:

- **<Headline feature>,** <one clause on what it does or how much faster>
- **<Headline feature>,** <...>
- ...
- **Broader platform support**: <ROCm / Arm / XPU one-liners>

This release is composed of <N> commits from <M> contributors since
PyTorch <PREV>. We want to sincerely thank our dedicated community for
your contributions. As always, we encourage you to try these out and
report any issues as we improve <VERSION>. More information about how
to get started with the PyTorch 2-series can be found at our
[Getting Started](https://pytorch.org/get-started/locally/) page.

Have questions? Join us on <DATE> for a live Q&A with panelists
<NAMES> and moderator <NAME>. We will provide a brief overview of the
release and answer your questions live. [Register today.](<URL>)

Throughout the 2.x series, PyTorch has been evolving from a
research-first framework into a unified, hardware-agnostic platform for
production training and inference at scale. [PyTorch <N-2>](<URL>)
<what it added>. [PyTorch <N-1>](<URL>) <what it added>.

PyTorch <VERSION> <one paragraph on how this release extends those
threads>.

## Performance Improvements

### <Entry title>

<Paragraph 1: the problem with the status quo.>

<Paragraph 2: what changed, and what it means for the user.>

API Unstable

(PR [#<PR>](https://github.com/pytorch/pytorch/pull/<PR>) by <Name>, <Company>)

## Core Features

### <Entry title>
...

## Distributed Training

### <Entry title>
...

## Compilation and Export

### <Entry title>
...

## Platform Features and Updates

### CUDA

#### <Entry title>
...

### ROCm

#### <Entry title>
...

### Arm

#### <Entry title>
...

### XPU (Intel GPUs)

#### <Entry title>
...

### C++ ABI

#### <Entry title>
...

## Profiling and Debugging

### <Entry title>
...

## Deprecations and Backwards-Incompatible Changes

- **<Change>.** <What to do instead.> See [#<PR>](...).

## Non-Feature Updates

- **Python support**: <changes>. See [#<PR>](...).
- **CUDA**: <default build, versions added/removed>. See [#<PR>](...).
- **Triton**: pin advanced to <version>. See [#<PR>](...).
- **oneDNN**: submodule upgraded to <version>. See [#<PR>](...).
```

## Worked example (from the 2.13 blog)

Note the shape of an entry: problem first, then the fix, then the
designation on its own line, then attribution.

```markdown
### Deterministic Backward for FlexAttention Flash Backend

This improvement focuses on correctness and debugging for the existing
CUDA implementation of FlexAttention by making gradient computation
reproducible. By default, the FlexAttention flash backend uses atomic
operations in the backward pass for dQ accumulation, which introduces
non-determinism — repeated runs on the same input can produce slightly
different gradients. This makes debugging, regression testing, and
reproducible research difficult.

The new deterministic backward path (compute_dq_write_order) replaces
atomics with a pre-computed write ordering that guarantees bit-for-bit
reproducible gradients without meaningful performance penalty. The
measured end-to-end overhead on create_block_mask is well under 1% at
longer sequence lengths (e.g., +0.2% at S=32768), making determinism
effectively free for most production workloads. Users can opt in via
the existing torch.use_deterministic_algorithms(True) setting with no
additional code changes.

API Unstable

(PR [#174813](https://github.com/pytorch/pytorch/pull/174813) by Driss Guessous, Meta)
```

And a highlight bullet, for tone:

```markdown
- **FlexAttention lands on Apple Silicon (MPS),** with up to ~12x
  speedup over SDPA on sparse patterns, and gains a deterministic
  backward path on CUDA for reproducible gradient computation
```

## Designations — how to pick

| Designation      | When to use                                                                   |
|------------------|-------------------------------------------------------------------------------|
| `API Unstable`   | The default for anything new. Placed on its own line before the attribution.   |
| *(omitted)*      | Long-standing stable surfaces. When unsure, omit and add a `TODO`.             |

**Stable, Beta and Prototype are retired.** The 2.13 post's own
changelog reads: *"Removed two instances of prototype which is a
designation that we no longer use."*

Do not render designations as heading prefixes (`### [Beta] Foo`) —
they are body text on a line of their own.

## Section names — canonical list

Top-level sections, in the order 2.13 used them:

1. Performance Improvements
2. Core Features
3. Distributed Training
4. Compilation and Export
5. Platform Features and Updates
6. Profiling and Debugging
7. Deprecations and Backwards-Incompatible Changes
8. Non-Feature Updates

Backend subsections under Platform Features and Updates: CUDA, ROCm,
Arm, XPU (Intel GPUs), C++ ABI. Use `###` for the backend and `####`
for entries beneath it.

Placement notes worth remembering:

- A large backend rewrite goes under **Performance Improvements**, not
  its platform section. 2.13 filed "Large MPS Op Migration to Native
  Metal" there.
- A backend-specific compiler feature goes under its **platform**, not
  Compilation and Export. 2.13 filed the CuTeDSL Inductor backend
  under CUDA.
- Release-engineering items that ship a feature (e.g. Python 3.15
  wheels) can be a **Core Features** entry; pure version bumps belong
  in Non-Feature Updates.

## Things to avoid

- **Don't use retired designations.** No Stable, Beta or Prototype.
- **Don't put designations in headings.** They are body text.
- **Don't skip attribution.** Every entry ends with `(PR #NNN by Name,
  Company)`. Worksheets have no author data, so fetch it from the API
  and leave a TODO to convert handles to names.
- **Don't invent speedup numbers.** Only cite numbers that appear in
  the PR body or on a linked dashboard. If a number comes from a PR
  title, say so.
- **Don't list ghstack sub-PRs.** Collapse a stack to one entry.
- **Don't include reverts.** If `#A` was reverted by `#B` before the
  branch cut, neither belongs in the blog. Check the release branch
  for reverts too, not just main.
- **Don't write commit-style descriptions.** "Fix segfault in foo when
  bar" belongs in release notes, not the blog. Lead with the problem
  the reader has.
- **Don't infer the support matrix.** Read CUDA, ROCm and Python
  versions off `generate_binary_build_matrix.py` on both release
  branches and diff them.
