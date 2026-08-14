---
name: release-blog-features
description: Produce a draft PyTorch release blog by comparing two release branches (e.g., release/2.13 vs release/2.14). Use when the user asks to generate a release blog, list new features for a release, compare release branches, or draft content for pytorch.org/blog. Organizes features the way recent posts do (https://pytorch.org/blog/pytorch-2-13-release-blog/) — grouped by topic (Performance Improvements, Core Features, Distributed Training, Compilation and Export, Platform Features and Updates, Profiling and Debugging), with each entry carrying an "API Unstable" designation and a PR attribution.
disable-model-invocation: true
---

# PyTorch Release Blog Features Skill

Produce a draft release blog post by diffing two release branches and
organizing the noteworthy changes into the format used on
pytorch.org/blog.

## Usage

The user invokes the skill with two release branches (a "base" and a
"target"), for example:

```
Generate the 2.14 release blog (release/2.13 → release/2.14)
```

Default behavior when the user only gives the target version:
- base = `release/<previous-minor>` (e.g. `release/2.13` for target 2.14)
- target = `release/<target>` (e.g. `release/2.14`)

Always confirm the two refs you'll compare before doing any heavy work.

## Read the most recent published blog first

**Do this before drafting.** Fetch the previous release's blog post
(e.g. <https://pytorch.org/blog/pytorch-2-13-release-blog/>) and match
its structure. The format changes between releases — designations have
been retired, sections renamed — and the published post is the only
authoritative source for the current shape. Everything below describes
the format as of 2.13; verify it still holds.

## What to produce

A Markdown document mirroring the previous release's blog. See
[reference-structure.md](reference-structure.md) for the full template.
In outline:

1. **Header** — one-line announcement with a release-notes link, a
   bulleted highlight list, the commit/contributor count with thanks,
   a live Q&A paragraph, and a short narrative placing the release in
   the 2.x arc.
2. **Topic sections** — Performance Improvements, Core Features,
   Distributed Training, Compilation and Export, Platform Features and
   Updates (subsectioned per backend), Profiling and Debugging.
3. **Deprecations and Backwards-Incompatible Changes**.
4. **Non-Feature Updates** — version matrix, dependency bumps.

### Designations

Recent blogs use exactly one designation, **API Unstable**, placed on
its own line after an entry's prose and before the PR attribution:

```markdown
### Deterministic Backward for FlexAttention Flash Backend

<two or three paragraphs>

API Unstable

(PR [#174813](https://github.com/pytorch/pytorch/pull/174813) by Driss Guessous, Meta)
```

**Stable, Beta and Prototype are retired.** The 2.13 post carries an
explicit changelog note: *"Removed two instances of prototype which is
a designation that we no longer use."* Do not reintroduce them, and do
not put designations in headings as a `[Tag]` prefix — they are body
text.

If you cannot tell whether something is API Unstable, leave the line
off and flag it with `TODO(release-manager):` rather than guessing.

### Attribution

Every entry ends with a PR attribution naming the authors and their
affiliations: `(PR #NNNNN by Firstname Lastname, Company)`. Multiple
PRs and authors are grouped in one line.

The worksheets carry **no author metadata**, so fetch it:

```bash
# gh may not be available; the REST API works with any token
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/pytorch/pytorch/pulls/<NUM> \
  | jq -r '.user.login, .title'
```

That gives you handles, not real names or affiliations. Emit handles
and leave a `TODO(release-manager)` to convert them, unless the user
supplies a mapping — do not guess someone's employer.

### Entry voice

Published entries open with the *problem*, then the fix. Compare:

- Bad (commit voice): "Adds a stream pool to MPS."
- Good: "Long-running decode workloads grew the MPS caching allocator's
  reserved footprint faster than necessary. The allocator now buckets
  large allocations..."

Two or three paragraphs per entry. Lift phrasing from the PR body's
summary rather than re-describing the diff. Where the previous release
introduced something this release extends, say so explicitly ("Building
on FlexAttention's arrival on MPS in 2.13, ...") — the published blogs
consistently thread releases together.

Do **not** invent features, metrics, or API names. If something is
ambiguous, mark it with `TODO:` so the release manager can resolve it.

## Workflow

### Step 1 — Resolve the refs

```bash
# In the pytorch/pytorch checkout, not this repo:
git fetch origin release/<base> release/<target> --no-tags

# Determine the merge-base — this is the effective "cut point"
git merge-base origin/release/<base> origin/release/<target>
```

Prefer `origin/release/<x>` over bare `release/<x>` when fetching, and
use the actual tag (e.g. `v2.13.0`) over the branch when it exists,
because the branch may contain post-release cherry-picks.

### Step 2 — Collect the commit list

**Option A: reuse the worksheets in this repo (preferred).**

This repo categorizes PRs per area in `<X.Y.Z>/done/result_<area>.md`
and `<X.Y.Z>/todo/result_<area>.md` (via `gen-release-notes`). Note the
directory is the full `X.Y.Z` version, e.g. `2.14.0/`, not `2.14/`.

```bash
ls <X.Y.Z>/done/ <X.Y.Z>/todo/
```

**Check how much triage has actually happened before trusting the
topic headings.** A completed worksheet sorts PRs under `### new
features`, `### improvements`, `### performance` and so on. An
untriaged one leaves everything under `### Untopiced`. In practice the
blog is often drafted before triage finishes — for 2.14, 46 of 47
worksheets were still in `todo/` with 1,202 PRs under `### Untopiced`
and only 11 sorted into `### new features`.

When that is the case:

- Draw candidates from `### Untopiced` plus `### improvements`,
  `### performance` and `### new features`.
- Skip `### not user facing`, and skip `result_skip.md` and
  `result_not needed.md` entirely.
- **Say so in the draft.** Add a note stating which worksheets were
  untriaged and that coverage is best-effort, so the release manager
  knows the draft is not a complete scan.

Entry format in the worksheets is one bullet per PR:

```
- <title> ([#189417](https://github.com/pytorch/pytorch/pull/189417))
```

**Option B: raw git log + PR lookup** (use when worksheets are not
available):

```bash
git log --pretty=format:'%H %s' \
    origin/release/<base>..origin/release/<target> \
    > /tmp/release-commits.txt
```

Then batch-fetch labels via the REST or GraphQL API. GraphQL supports
~100 aliases per query, so split into multiple queries.

### Step 3 — Filter to "blog-worthy" changes

A release has thousands of commits; the blog highlights a few dozen.
Use these signals, in order:

1. **`release notes:` labels** — the canonical source of user-facing
   changes.
2. **New public APIs** — additions to `torch/`, `torch/nn/`,
   `torch/distributed/`, `torch/export/`, especially new modules or
   new `__all__` entries.
3. **Wording in the PR body** — a `## Summary` that describes a new
   public API or a measured speedup.
4. **Platform enablement** — new backends, new hardware, new wheel
   variants (ROCm, XPU, CUDA major bump, aarch64, riscv64).

Ignore: pure refactors, test infra, lint fixes, typo fixes, internal
dispatcher churn, reverts, and cherry-picks that land on both branches.

Typo-fix PRs are a large share of the `Untopiced` pool and are never
blog-worthy; filter them early.

### Step 4 — Group by topic

Group survivors into the sections the previous blog used. As of 2.13:

- **Performance Improvements** — including large backend rewrites, e.g.
  the MPS Metal migration lived here, not under MPS.
- **Core Features** — new ops, frontend APIs, autograd surfaces.
- **Distributed Training** — c10d, backends, FSDP, DTensor, symmetric
  memory, pipelining.
- **Compilation and Export** — Dynamo, dynamic shapes, AOTInductor,
  backend registration.
- **Platform Features and Updates** — `### CUDA`, `### ROCm`,
  `### Arm`, `### MPS`, `### XPU (Intel GPUs)`, `### C++ ABI`, each
  with `####` entries.
- **Profiling and Debugging**.

A backend-specific compiler feature goes under its platform, not under
Compilation: 2.13 filed the CuTeDSL Inductor backend under CUDA.

### Step 5 — Apply the "major feature" threshold

When the user asks for **major features only**, drop any feature backed
by 3 or fewer PRs — after Step 6, so a collapsed stack counts as its
full size. Smaller entries belong in the long release notes.

### Step 6 — Deduplicate ghstack stacks

A feature often lands as 5-40 ghstack PRs. Collapse them to one entry
citing the user-facing PRs. For 2.14, NVGEMM was ~35 PRs and the
torchcomms `nccl2` backend ~40; each became a single entry with a
handful of representative links.

### Step 7 — Draft the blog

Open [reference-structure.md](reference-structure.md) and follow the
template. Write for a PyTorch user deciding whether to upgrade, not for
a reviewer.

### Step 8 — Gather stats for the header

```bash
# In the pytorch/pytorch checkout:
git log --no-merges --oneline v<base>.0..origin/release/<target> | wc -l
git log --format='%an' v<base>.0..origin/release/<target> | sort -u | wc -l
```

### Step 9 — Verify the support matrix

Do not carry version numbers over from the previous blog or infer them
from PR titles. Read them off the release branch:

```bash
git show origin/release/<target>:.github/scripts/generate_binary_build_matrix.py \
  | grep -E '^(CUDA_ARCHES|CUDA_STABLE|ROCM_ARCHES|FULL_PYTHON_VERSIONS)'
```

Diff against the base branch's copy so you can state what was added and
dropped. Watch for architectures that are built but deliberately not
advertised — 2.14 built CUDA 13.4 while excluding it from Windows and
the docker release matrix, so it was not a 2.14 install option.

## Output

Save the draft to `<X.Y.Z>/blog-draft.md` in this repo. Do not commit
automatically — the release manager will review and move the polished
version into the pytorch.org blog repo.

## Best practices

- **Read the previous blog first.** The format drifts; the published
  post is authoritative, this skill is a summary of it.
- **Confirm scope before you dig in.** Thousands of commits; the user
  cares about a few dozen entries.
- **Let the PR author's words do the work.** Lift phrasing from the PR
  body's summary rather than re-describing the change from the diff.
- **Flag uncertainty.** `TODO(release-manager): is this API Unstable?`
  is more useful than a confident guess.
- **Don't overclaim performance.** Only cite speedups that appear in
  the PR body or a linked dashboard — never invent numbers. When a
  number comes from a PR title, attribute it that way ("the PR reports
  recovering an 8.5x regression").
- **Skip reverts and follow-ups.** If PR #A landed and PR #B reverted
  it before the release branch was cut, neither belongs in the blog.
  Check reverts on the release branch too, not just on main.
