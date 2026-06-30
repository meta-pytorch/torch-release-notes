---
name: gen-release-notes
description: Generate PyTorch release notes for a functional area. Use when the user says "gen-release-notes", "release notes", or wants to write/complete release notes for a functional area like "aotdispatcher", "dynamo", "inductor", etc.
---

# Generate PyTorch Release Notes

Generate and complete the release notes worksheet for a given functional area.

## Usage

```
/gen-release-notes <version> <area>
```

Where `<version>` is the PyTorch release version (e.g., `2.11.0`) and `<area>` is the functional area name (e.g., `aotdispatcher`, `dynamo`, `inductor`).

## Instructions

### Step 0: Validate inputs

1. Check that both the version and area arguments were provided. If the version is missing, ask the user which version to use. If the area is missing, list the available areas from the `<version>/todo/` directory and ask the user to pick one.
2. Confirm the version directory exists (e.g., `2.11.0/`). If not, tell the user the version was not found and list the available version directories.
3. Confirm the worksheet file exists at `<version>/todo/result_<area>.md`. If it's already in `done/`, tell the user it's already completed and ask if they want to re-process it.

### Step 1: Read the worksheet

**Read the worksheet** at `<version>/todo/result_<area>.md`. The worksheet contains:
- An instructional preamble (everything before `## <area>`)
- Category headings (`### bc breaking`, `### new features`, etc.) with some pre-sorted PRs
- A `### Untopiced` section with PRs that haven't been categorized yet — this is typically where the bulk of the work is

Trust the worksheet contents — do not search GitHub for missing PRs or verify that PRs are on the release branch. The worksheet was generated from the actual release branch and is the source of truth.

The worksheet also contains its own instructions in the preamble. Follow the instructions in **this skill document**, which supersede the worksheet's instructions where they differ.

### Step 2: Check miscategorized.md

Read `<version>/miscategorized.md` if it exists. If it's empty or doesn't exist, skip this step. Otherwise, check if any entries there belong to this functional area. If so, incorporate them into the worksheet and remove them from miscategorized.md.

### Step 3: Categorize and write up

Edit the worksheet file in place, preserving the instructional preamble (everything before `## <area>`). Only modify the content under `## <area>`.

#### Step 3a: Triage — batch-fetch labels and separate miscategorized PRs

Before doing any detailed categorization, do a fast triage pass to identify which PRs belong in this worksheet vs. other areas. Extract all PR numbers from the worksheet and batch-fetch their `release notes:` labels using GraphQL:

```bash
# Batch-fetch labels for up to 100 PRs at once using GraphQL aliases.
# Build a query with one alias per PR, e.g.:
gh api graphql -f query='
{
  pr170057: repository(owner: "pytorch", name: "pytorch") {
    pullRequest(number: 170057) {
      number
      labels(first: 10) { nodes { name } }
    }
  }
  pr169979: repository(owner: "pytorch", name: "pytorch") {
    pullRequest(number: 169979) {
      number
      labels(first: 10) { nodes { name } }
    }
  }
}'
```

Generate the full query programmatically for all PR numbers in the worksheet. GraphQL supports ~100 aliases per query, so split into multiple queries if needed. This replaces individual `gh pr view` calls and is dramatically faster.

Using the labels, split PRs into two groups:
1. **Stays here**: PRs labeled for this area (or with no `release notes:` label, or labeled for a sub-area that has no separate worksheet).
2. **Miscategorized**: PRs labeled for a different area that has its own worksheet.

Immediately edit the worksheet to remove miscategorized PRs, and append them to `<version>/miscategorized.md`. This reduces the working set for detailed categorization.

Also at this stage:
- Remove duplicate entries (same PR listed more than once).
- Remove PRs that were never merged (check for `Reverted` label or `state: CLOSED` if suspicious).
- Look up bare commit hashes to find their PR numbers:
  ```bash
  gh api repos/pytorch/pytorch/commits/<HASH>/pulls --jq '.[0].number'
  ```

#### Step 3b: Categorize remaining PRs in batches

Now process the remaining PRs (the ones staying in this worksheet) **in batches of 20**. For each batch:
1. Fetch any needed details for the batch using multiple `gh` calls in a single tool-calling round (see "When to fetch PR details" below).
2. Categorize each PR and **immediately edit the worksheet**, writing entries into the correct category sections.
3. Move to the next batch.

**Edit the worksheet after every batch** — do NOT accumulate all categorizations in memory and write once at the end. Incremental edits are faster, reduce risk of errors, and make progress visible.

**Important — do not skip `### not user facing`.** Pre-sorting (and the GitHub `topic: not user facing` label) reflects the *author's* judgment, which is sometimes wrong. Give every entry in `### not user facing` the **same body-level review** as the other sections — do not let the section title or the `topic: not user facing` label cause you to skim past it. For each entry, fetch the PR body (`gh pr view <NUM> --repo pytorch/pytorch --json title,body,labels`) when its user impact is not obvious from the title, and **promote it to the correct category** if any of these are true:
- It fixes a bug/crash/hang/assert a user could hit, or links a closed issue (`Fixes #NNNNN` / `Closes #NNNNN`) → `### bug fixes`.
- It delivers a measurable performance improvement (e.g. the body shows benchmark/MFU/latency gains) → `### performance`.
- It adds or changes a user-visible capability, API, or behavior → `### new features` / `### improvements`.

Only genuinely internal changes stay in `### not user facing`: test-only changes, CI/lint/formatting, internal refactors with no behavior change, typo fixes in comments, and changes whose `release notes:` label points at a *different* area (those go to `miscategorized.md`). When unsure whether something is user-facing, read the body rather than trusting the label.

#### When to fetch PR details

For most PRs, the title is sufficient to categorize. Only fetch additional detail when needed:
- For potential BC-breaking changes or deprecations, always read the full PR body and diff to write a proper migration guide.
  - Verify concrete behavioral claims against the merged diff, do not trust the PR description for them. Whenever an entry would state a specific, checkable detail, confirm it exists in `gh pr diff <NUM> --repo pytorch/pytorch` before writing it. This applies to config flags, env vars, warnings, or error messages.
- For new features, read the PR body to write a clear description.
- For ambiguous titles, fetch the PR body to determine the correct category.

If the diff doesn't back up the claim, describe what actually merged (and recategorize accordingly — e.g. a "deprecation" with no warning in the diff is not a deprecation).

```bash
gh pr view <NUMBER> --repo pytorch/pytorch --json title,body,labels
gh pr diff <NUMBER> --repo pytorch/pytorch  # only when needed
```

#### What to determine for each PR

- Is it user-facing or internal-only?
- Is it a BC-breaking change, deprecation, new feature, improvement, bug fix, performance change, docs, developer-facing, or security-related?
- Does it belong to this area or should it be moved to `miscategorized.md`? Check the PR's `release notes:` labels — if a PR is labeled for a different area (e.g., `release notes: fx` on a PR in the distributed worksheet), it belongs in miscategorized.md.

Move all PRs from `### Untopiced` into the correct category, leaving it empty. Any PRs that belong to a different area should be added to `<version>/miscategorized.md` with a note about which area they came from and which area they belong to.

The category headings under `## <area>` should be:

```markdown
### bc breaking
### deprecation
### new features
### improvements
### bug fixes
### performance
### docs
### devs
### not user facing
### security
```

#### Category guidelines

All category headings must be present even if empty.

- **bc breaking**: These are the most important entries. Each must include:
  1. A summary of the change.
  2. The conditions under which a user would hit the change (symptoms, error messages — users often ctrl+F the release notes for error text).
  3. Workarounds to achieve the previous behavior, if possible.
  4. Before-and-after code snippets tagged with ` ```python ` showing the old behavior and new behavior.

  Example structure:
  ```
  - `torch.foo` now returns X instead of Y when called with Z ([#NNNNN](...))

    This change was made because [rationale]. Previously, `torch.foo(...)` would
    return Y. Users relying on the old behavior can [workaround].

    Version <previous_version>:
    ```python
    >>> torch.foo(bar)
    old_result
    ```

    Version <current_version>:
    ```python
    >>> torch.foo(bar)
    new_result
    ```
  ```

- **deprecation**: Must include a brief explanation plus before/after code showing what to use instead.
- **new features**: Clean, readable description of what's new.
- **improvements**: Can be condensed — summarize and group related changes.
- **bug fixes**: Can be condensed.
- **performance**: Can be condensed.
- **docs**: Can be condensed.
- **devs**: Changes that affect people who build PyTorch from source, develop in it, or extend it, can be condensed.
- **not user facing**: List items here so reviewers can verify, but these will be dropped from the final merged release notes. Usually this includes refactors with no behavior change, dead-code or duplicate-code removal with no user-visible effect, test/CI/lint-only changes, and changes confined to private APIs (names with a leading underscore).
- **security**: Security-related fixes.

Format each entry as:
```
- Description of the change ([#NNNNN](https://github.com/pytorch/pytorch/pull/NNNNN))
```

For bc breaking, deprecation, and new features, each entry MUST be polished and clear for end users. For the other sections, you do NOT need to polish every entry — summarize and group related changes where it makes sense.

#### Formatting standards

- **Release notes are not commit messages.** A commit title usually does not have enough context for an OSS user. Use the commit/PR title as a *starting point*, but rewrite it so that **someone who has used the feature in question can understand the change** from the release note alone. Expand cryptic or insider phrasing.
- **Remove component/feature "tags."** Do NOT keep or reintroduce tags that indicate the component or feature — e.g. `[dataloader]`, `[autograd]`, `[fx]`, `[nnc]`, `[c10d]`, `[FSDP2]`, `[DTensor]`, `[Docathon]`, `[BE]`, `[ROCm]`, `[reland]`. The notes are already placed under tagged *categories* (and, here, per-area worksheet files), so a tag in the title/text is **redundant**. This also means **do NOT convert a tag into a prefix** like `c10d:`, `FSDP:`, `DTensor:`, `DDP:`, `SymmMem:`, `Pipelining:`, etc. — just remove it and fold any genuinely useful context into the sentence itself.
- **Format programming elements in fixed-width.** Surround functions, methods, classes, arguments, etc. with backticks (`` `method` ``).
- **Only reference concepts that exist in public PyTorch.** The audience is OSS users, so an entry must be understandable in terms of the public `torch` API. Strip any internal/company-specific terms that leak in from a PR title or body — e.g. `MAST`, `APF`/`APS`, `justknobs`/`JK`, `thrift`, `fbcode`/`buck`, `Differential Revision`/`D1234567`, internal cluster/job/oncall names. If such a term names the *motivation* for the change, drop it and describe the **public-facing effect** instead (the API/behavior an OSS user sees). If after removing the internal terms there is no public-facing change left, the PR is internal-only and belongs in `### not user facing` (or `miscategorized.md` if it's another area).
- Write each entry as a **plain, self-contained sentence** in present tense (e.g. "Add a health check endpoint to the distributed debug server", "Fix gather on non-destination ranks for the TorchComms backend"). If the component matters for clarity, mention it naturally inside the sentence rather than as a leading label.
- Use the published PyTorch release notes (e.g. the v2.x.0 GitHub release pages) as the style reference, not the raw PR titles.
- **Do not trust the title's verb, and do not trust the pre-sorted category.** Many bug fixes are titled with a verb that describes *what the change does* (`Add`, `Support`, `Handle`, `Prevent`, `Make`, `Avoid`, ...) rather than the word "Fix", which makes them masquerade as features or improvements. Check the body: if it fixes a bug/crash/hang or links a closed issue (`Fixes #NNNNN`/`Closes #NNNNN`), **move it to `### bug fixes`** and **reword the entry around the symptom** (what was broken / the error the user saw), not the mechanism of the fix.


### Step 4: Verify

Re-read the completed worksheet and verify:
- `### Untopiced` is empty (all PRs categorized)
- No PR appears in more than one category
- All category headings are present
- BC-breaking and deprecation entries have before/after code examples

### Step 5: Move to done

Move the completed file from `todo/` to `done/`:
```bash
mv <version>/todo/result_<area>.md <version>/done/result_<area>.md
```

### Step 6: Report

Tell the user:
- How many PRs were processed
- Summary of what's in each non-empty category
- Whether anything in miscategorized.md belongs to this area
- Remind them to review the result and open a PR when ready

Do NOT commit or open a PR automatically unless the user asks.

## Area-specific guidance

### releng (Release Engineering)

Releng release notes follow recurring patterns across releases. Use these examples as a reference for how to categorize and write up common releng changes.

#### Typical releng categories

**BC breaking** — Changes that affect how users install or run PyTorch:
- CUDA version changes on PyPI (e.g., PyPI wheels switching from CUDA 12.x to CUDA 13.0)
- GPU architecture support removal from binary builds (e.g., Volta removed from CUDA 12.8+ builds)
- Package renames (e.g., `pytorch-triton` renamed to `triton`)

Each BC-breaking entry must explain what changed, why, and how users should adapt. Include install commands showing the old and new behavior.

Example (from 2.11.0):
```markdown
- PyPI wheels now ship with CUDA 13.0 instead of CUDA 12.x ([#172663](...))

  Starting with PyTorch 2.11, `pip install torch` on PyPI installs CUDA 13.0 wheels by default
  for both Linux x86_64 and Linux aarch64. Users whose systems have only CUDA 12.x drivers
  installed may encounter errors. CUDA 12.6 and 12.8 binaries remain available via
  `download.pytorch.org`.

  Version 2.10:
  ```bash
  # PyPI wheel used CUDA 12.x
  pip install torch
  ```

  Version 2.11:
  ```bash
  # PyPI wheel now uses CUDA 13.0
  pip install torch

  # To get CUDA 12.8 wheels instead:
  pip install torch --index-url https://download.pytorch.org/whl/cu128
  ```
```

**Improvements** — These recur from release to release. Group related PRs together:
- **CUDA version upgrades**: "Add support for CUDA X.Y" or "Upgrade to CUDA X.Y.Z" — group all CI/CD, binary build, benchmark, and driver PRs for that CUDA version into one entry.
- **ROCm version upgrades**: "Upgrade to ROCm X.Y" — group Docker images, magma tarballs, binary builds, CI coverage PRs.
- **New GPU architecture support**: "Add support for [GPU model] (gfxNNNN)" — group all PRs enabling a new GPU.
- **XPU/Intel upgrades**: "Upgrade XPU support package to X.Y"
- **Build infrastructure upgrades**: GCC version bumps, Ubuntu image migrations, etc.

Example entries (from 2.10.0):
```markdown
### improvements
- Add support for CUDA 13.0 in CI/CD including binary builds, inductor benchmarks, and
  upgrade to CUDA 13.0.2 ([#162455](...), [#162425](...), [#163787](...), ...)
- Upgrade to ROCm 7.0 and 7.1 ([#163860](...), [#163883](...), ...)
- Add support for MI355, MI300, gfx1100, gfx1150, gfx1151, and gfx950 GPU architectures
  ([#160215](...), [#167587](...), ...)
- Add B200 GPU support with symmetric memory testing and smoke tests ([#162988](...), ...)
- Upgrade XPU support package to 2025.3 ([#166829](...))
- Upgrade XPU build infrastructure to GCC 13 and Ubuntu 24.04 ([#162474](...), ...)
```

**New features** — Genuinely new capabilities (not upgrades of existing ones):
- New CI testing infrastructure (e.g., Pallas CI)
- New build formats (e.g., PEP 517 source distribution)
- New automated processes (e.g., auto-revert)

**Performance** — Benchmark infrastructure additions:
- New operator microbenchmarks added to CI
- New benchmark suites (e.g., HuggingFace LLM benchmarks)

**Devs** — Build system changes affecting source builders:
- Build tool migrations (e.g., setup.py to pip install)

**Not user facing** — The bulk of releng PRs are internal:
- Hash pin updates (vllm, audio, vision, xla, triton)
- CI runner changes (c7i migrations, runner type swaps)
- CI workflow refactors
- Dependency bumps (protobuf, setuptools, etc.)
- Docker image updates
- Linter/lint rule changes
- Individual test fixes or test additions
