---
name: gen-patch-release-notes
description: Generate the GitHub release notes for a PyTorch PATCH (bug-fix) release like 2.12.1, 2.9.1, 2.7.1. Patch releases are very minimal — a short intro, an optional "Regression fixes" / "Tracked Regressions" section, and a few category buckets of cherry-picked fixes. Use when the user says "patch release notes", "gen patch release notes", "bug fix release notes", or names a patch version (X.Y.Z with Z > 0).
---

# Generate PyTorch Patch (Bug-Fix) Release Notes

Generate the GitHub release description for a PyTorch **patch** release (e.g. `2.12.1`). A patch
release ships only the cherry-picked fixes that landed on the `release/X.Y` branch after the
previous tag. The notes are intentionally **minimal** — do not write feature descriptions,
BC-breaking migration guides, or before/after code. Just a short intro, an optional regression
section, and a few category buckets each containing one bullet per fix.

This is the patch-release counterpart to the major-release `gen-release-notes` skill. It does
**not** use the `todo/`/`done/` worksheet structure — patch notes are posted directly to the
GitHub release, so this skill outputs a single markdown file.

See `patch-template.md` in this skill directory for the exact target structure and a worked
example based on the real v2.9.1 / v2.7.1 releases.

## Usage

```
/gen-patch-release-notes <version> [regression-issues...]
```

- `<version>` — the patch version, `X.Y.Z` with `Z > 0` (e.g. `2.12.1`). Required.
- `regression-issues...` — optional list of pytorch/pytorch issue numbers (or URLs) that are
  **fixed** in this release and should be called out under **Regression fixes**
  (e.g. `181248 187081`). If omitted, the skill auto-discovers candidates from the milestone.

If the version is missing or not a patch version (Z == 0), ask the user. Z == 0 is a major/minor
release — point them at `gen-release-notes` instead.

## Inputs and sources

| What | Where it comes from |
|------|--------------------|
| Fixed cherry-picks | Commits on `release/X.Y` after the `vX.Y.(Z-1)` tag, in `pytorch/pytorch` |
| Per-PR title + area | The `release notes: <area>` label on each original PR |
| Regression fixes | Issue numbers passed by the user, or open/closed issues on the `X.Y.Z` milestone |

A local `pytorch/pytorch` checkout is the most reliable source for the cherry-pick list. Common
local clone: `/data/users/atalman/pytorch`. If none is available, fall back to the GitHub API
(Step 1b). `gh` must be authenticated for label/issue lookups.

## Instructions

### Step 0: Validate inputs

1. Parse `<version>` as `X.Y.Z`. If `Z == 0`, stop and tell the user this is a minor release —
   use `gen-release-notes`. If the version is malformed or missing, ask.
2. Compute the base tag:
   - `vX.Y.0` when `Z == 1`
   - `vX.Y.(Z-1)` otherwise (e.g. base for `2.12.2` is `v2.12.1`).
3. The release branch is `release/X.Y` (e.g. `release/2.12` for `2.12.1`).

### Step 1: Collect the cherry-picked fixes

#### Step 1a: From a local pytorch checkout (preferred)

Locate a `pytorch/pytorch` clone (try `/data/users/atalman/pytorch`). Identify the remote that
points at `github.com/pytorch/pytorch` (often `origin` or `upstream`) and fetch the live branch —
local `release/X.Y` is frequently stale:

```bash
PT=/data/users/atalman/pytorch
REMOTE=$(git -C "$PT" remote -v | awk '/github\.com[:/]pytorch\/pytorch(\.git)? \(fetch\)/{print $1; exit}')
git -C "$PT" fetch "$REMOTE" release/X.Y --tags --quiet
git -C "$PT" log --oneline "vX.Y.(Z-1)..$REMOTE/release/X.Y"
```

Each line is a cherry-pick commit; the trailing `(#NNNNN)` is the **original** PR number (this is
what the notes link to — not the cherry-pick PR). Extract them:

```bash
git -C "$PT" log --pretty='%s' "vX.Y.(Z-1)..$REMOTE/release/X.Y" \
  | grep -oE '\(#[0-9]+\)$' | tr -dc '0-9\n'
```

Drop noise before categorizing:
- **Revert pairs**: if a commit and its `Revert "..."` both appear in the range, drop both — the
  net change is zero and it should not be in the notes.
- Version-bump / branch-cut commits (e.g. "Advance release version…", `.ci` pins), and any commit
  with no `(#NNNNN)`.

#### Step 1b: Fallback — GitHub API (no local checkout)

```bash
gh api --paginate "repos/pytorch/pytorch/compare/vX.Y.(Z-1)...release/X.Y" \
  --jq '.commits[].commit.message' | head -1 -c 200   # title is first line; parse (#NNNNN)
```

Or parse the cherry-pick tracker issue if the user supplies one (same format the
`process-cherry-picks` skill consumes).

### Step 2: Enrich and categorize (minimal)

Batch-fetch the `release notes:` label and title for every original PR with one GraphQL query
(same technique as `gen-release-notes` — ~100 aliases per query):

```bash
gh api graphql -f query='
{
  pr165601: repository(owner:"pytorch", name:"pytorch") { pullRequest(number:165601) {
    number title labels(first:15){nodes{name}} } }
  # ...one alias per PR...
}'
```

Map each PR's `release notes:` label to a **patch section header**, collapsing to the few buckets
actually present (do NOT emit empty sections):

| `release notes:` label(s) | Section header |
|---|---|
| `dynamo`, `inductor`, `export`, `fx`, `aotdispatch`, `aotinductor` | **Torch.compile** |
| `distributed*` (c10d, dtensor, fsdp, …) | **Distributed** |
| `cuda`, `cudnn`, `linalg` (CUDA-specific) | **CUDA** |
| `mps` | **MPS** |
| `rocm` | **ROCm** |
| `xpu` | **XPU** |
| `releng`, `build` | **Releng / Build** |
| anything else / unlabeled | **Other** |

Guidelines:
- One bullet per fix, lightly cleaned from the PR title (strip `[area]` prefixes, fix
  capitalization). **Do not** write descriptions, rationale, or code — patch notes are terse.
- Group several PRs that fix one thing into a single bullet with multiple links.
- Bullet format:
  ```
  - <short description> ([#NNNNN](https://github.com/pytorch/pytorch/pull/NNNNN))
  ```
- Section order: **Regression fixes** (Step 3) first, then Torch.compile, Distributed, CUDA, MPS,
  ROCm, XPU, Releng / Build, then **Other** last.

### Step 3: Regression fixes section

A patch release usually leads with the headline regressions it fixes (see v2.9.1 "Tracked
Regressions").

1. **If the user passed issue numbers** (e.g. `181248 187081`): for each, fetch the title and the
   fixing PR(s):
   ```bash
   gh issue view <N> --repo pytorch/pytorch --json title,milestone,closedByPullRequestsReferences
   ```
   Write one bullet per regression: a plain-language description of the symptom, then links to the
   **issue** and the fixing **PR(s)**. If the regression is fixed by a cherry-pick already found in
   Step 1, link that PR and remove it from its category bucket so it is not listed twice.
2. **If no issues were passed**: auto-discover candidates from the milestone and ask the user which
   to feature:
   ```bash
   gh issue list --repo pytorch/pytorch --milestone "X.Y.Z" --state all \
     --json number,title,state,url --limit 200
   ```
   Surface the ones whose titles mention "regression" prominently. Do not invent regressions.
3. Heading: use **`## Regression fixes`** when the listed issues are fixed in this release. Reserve
   **`## Tracked Regressions`** for *known, still-open* regressions that ship *with* the release and
   need a workaround (as in v2.9.1). Confirm with the user if a referenced issue is still open.

### Step 4: Assemble the release notes

Follow `patch-template.md`. Skeleton:

```markdown
# PyTorch X.Y.Z Release, bug fix release

This release is meant to fix the following regressions and silent correctness issues:

## Regression fixes
- <regression description> ([#<issue>](...), [#<fixPR>](...))

## Torch.compile
- ...

## Distributed
- ...

## Other
- ...

These were fixed by cherry-picking onto the `release/X.Y` branch. We recommend updating to the
latest patch release — see installation instructions at https://pytorch.org/get-started/locally/ .
```

Keep it short. Omit any section with no entries. Omit the Regression fixes section entirely if
there are none.

### Step 5: Output

Write the result to `<version>/RELEASE_NOTES.md` in this repo (create the directory if needed) and
print it to the user. Do **not** post to GitHub and do **not** commit unless the user explicitly
asks — the maintainer pastes it into the GitHub release draft.

### Step 6: Report

Tell the user:
- The base tag and release branch used, and how many cherry-picks were found.
- How many revert-pairs / non-fix commits were dropped.
- Which sections were emitted and the bullet count per section.
- Which regressions were featured under Regression fixes.
- Any PRs that lacked a `release notes:` label and were placed under **Other** (so they can verify).

Remind them to review, then paste into the GitHub release draft for `vX.Y.Z`.
