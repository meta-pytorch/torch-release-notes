---
name: categorize-miscategorized
description: Distribute miscategorized PRs back to correct worksheets. Trigger on "categorize miscategorized", "distribute miscategorized", "process miscategorized".
---

# Categorize Miscategorized PRs

Read `miscategorized.md`, determine where each PR belongs, and append it to the correct worksheet's category section.

## Usage

```
/categorize-miscategorized <version>
```

Where `<version>` is the PyTorch release version (e.g., `2.11.0`).

## Instructions

### Step 0: Validate inputs

1. Check that the `<version>` argument was provided. If missing, ask the user.
2. Confirm the `<version>/` directory exists.
3. Confirm `<version>/miscategorized.md` exists and is non-empty. If empty or missing, tell the user there's nothing to process.

### Step 1: Build area map

Scan `<version>/todo/` and `<version>/done/` for `result_<area>.md` files.
- Strip the `result_` prefix and `.md` suffix to get valid area names (e.g., `distributed (dtensor)`, `fx`, `inductor (aoti)`).
- Record whether each area's file is in `todo/` or `done/`.

### Step 2: Parse miscategorized.md

Parse the file into structured entries. Each entry has: PR number (or bare commit hash), description text, section header context, and provenance annotations.

Extract the "target area hint" from section headers using these patterns:

| Header pattern | Target area |
|---|---|
| `## <area> (from <source>)` | `<area>` (e.g., `## distributed (dtensor) (from distributed)` -> `distributed (dtensor)`) |
| `## From <source> worksheet` / `### <area>` | `<area>` (the `### <area>` sub-heading) |
| `## not user facing` | Category hint only; area is TBD — needs label resolution |
| Ambiguous headers like `## CPU / Linear algebra` | Needs label resolution |

### Step 3: Resolve bare commit hashes

For entries that reference a bare commit hash instead of a PR number:

```bash
gh api repos/pytorch/pytorch/commits/<HASH>/pulls --jq '.[0].number'
```

If no PR is found, mark the entry as LOW confidence and leave it in miscategorized.

### Step 4: Batch-fetch labels via GraphQL

Reuse the gen-release-notes GraphQL batch pattern (up to 100 aliases per query):

```bash
gh api graphql -f query='
{
  pr170057: repository(owner: "pytorch", name: "pytorch") {
    pullRequest(number: 170057) {
      number
      state
      title
      labels(first: 10) { nodes { name } }
    }
  }
  pr169979: repository(owner: "pytorch", name: "pytorch") {
    pullRequest(number: 169979) {
      number
      state
      title
      labels(first: 10) { nodes { name } }
    }
  }
}'
```

Generate the full query programmatically for all PR numbers. Fetch: `release notes:` labels, `module:` labels, `topic:` labels, state, title. Split into multiple queries if more than 100 PRs.

### Step 5: Classify each PR (confidence levels)

Apply this priority chain to determine the target area:

1. **`release notes: <X>` label -> HIGH confidence** if `<X>` matches a worksheet area. This is the authoritative signal and overrides section header hints.
2. **Section header hint -> HIGH confidence** if it matches a valid worksheet area name exactly (e.g., entries under `## distributed (dtensor) (from distributed)` go to `distributed (dtensor)`).
3. **`module: <X>` label -> MEDIUM confidence.** Map module names to areas (e.g., `module: dtensor` -> `distributed (dtensor)`, `module: inductor` -> `inductor`).
4. **Title keyword matching -> MEDIUM confidence.** Prefixes like `[DTensor]`, `[AOTI]`, `[ROCm]`, `[xpu]`, `[caffe2]`, `[MPS]` etc. map to their respective areas.
5. **"not user facing" entries** — use module/title keywords to pick the best worksheet. For caffe2/build entries, suggest `build_frontend` or `releng`. For JIT entries, suggest `fx`. If truly ambiguous, LOW confidence.
6. **No match -> LOW confidence** — leave in miscategorized with a suggestion annotation.

### Step 6: Determine category within target worksheet

Use `topic:` labels and title keywords to pick the correct `### <category>` heading:

| Signal | Category |
|---|---|
| `topic: bug fixes` or title contains "Fix"/"fix" | `### bug fixes` |
| `topic: improvements` | `### improvements` |
| `topic: new feature` | `### new features` |
| `topic: performance` | `### performance` |
| `topic: bc breaking` or `[BC Breaking]` in title | `### bc breaking` |
| `topic: docs` or `[doc]` in title | `### docs` |
| `topic: not user facing` or `[BE]`/`Refactor`/`Clean up`/`typing`/`remove unused` in title | `### not user facing` |
| Default for internal-looking PRs | `### not user facing` |
| Default otherwise | `### improvements` |

### Step 7: Move PRs to worksheets

Group HIGH and MEDIUM confidence PRs by target area. For each area:

1. Read the worksheet (from `todo/` or `done/`).
2. For each PR: strip provenance annotations from the end of the entry line. These annotations can contain backticks, commas, and nested parentheses — match everything from the last `(from:` or `(suggestion:` to end of line. Examples: `(from: dynamo, labeled \`release notes: distributed (c10d)\`)`, `(from: dynamo, XPU/inductor test)`. Then locate the target `### <category>` heading, and append the cleaned entry after existing entries under that heading (before the next `###` heading).
3. Write the updated worksheet.
4. Remove moved entries from miscategorized.md.

### Step 7a: Format moved entries

After all entries have been moved, ensure each one meets the formatting standards defined in `.claude/skills/gen-release-notes/SKILL.md` under "Category guidelines" (Step 3b). The key points:

- **`bc breaking`, `deprecation`, `new features`**: For each entry that is just a bare one-liner (title + PR link with no expanded description below it), fetch the PR body and diff, then rewrite it with the full polished format. BC breaking entries MUST have summary, impact, workaround, and before/after code examples. Deprecation entries MUST have before/after code. New features MUST have a clean description.
- **All other categories** (`improvements`, `bug fixes`, `performance`, `docs`, `devs`, `not user facing`, `security`): Condensed one-liners are fine, but you MUST clean up noisy title prefixes on every entry. This is a separate pass from the detailed write-ups above — do it for all moved entries regardless of category.

**Title prefix cleanup (all categories):**

Strip bracketed prefixes that are internal tags, not meaningful to end users. Common patterns to remove:
- Team/infra tags: `[BE]`, `[BE][Ez]`, `[pytorch]`, `[pytorch][PR]`, `[codemod]`, `[reland]`
- Area tags that duplicate the worksheet context: `[jit]`, `[caffe2]`, `[DTensor]`, `[AOTI]`, `[ROCm]`, `[xpu]`, `[functorch]`, `[inductor]`, `[dynamo]`, `[export]`
- Compound tags: `[folly][caffe2]`, `[aarch64][caffe2]`, `[pytorch][caffe2]`, `[caffe2][cudnn]`
- Series tags: `[18/N]`, `[19/N]`

Keep prefixes that add useful context not obvious from the worksheet heading, e.g. `[BC Breaking]` in a bc breaking section is redundant and should be removed, but `[xpu][feature]` in the inductor (aoti) worksheet — keep `[xpu]` since it tells the reader the entry is XPU-specific.

After stripping prefixes, capitalize the first letter of the remaining text. If the entry becomes empty or nonsensical after stripping, leave it as-is.

Example cleanups:
- `[jit] Raise ValueError for invalid fusion strategy` → `Raise ValueError for invalid fusion strategy`
- `[BE] remove redudant items in unordered_set` → `Remove redundant items in unordered_set`
- `[pytorch][PR] [reland][ROCm] remove caffe2 from hipify` → `Remove caffe2 from hipify`
- `[DTensor][BE] remove is_backward from redistribute_local_tensor` → `Remove is_backward from redistribute_local_tensor`

```bash
gh pr view <NUMBER> --repo pytorch/pytorch --json title,body,labels
gh pr diff <NUMBER> --repo pytorch/pytorch  # for bc breaking / deprecation
```

Process entries needing detailed write-ups in batches, editing the worksheet after each batch (same pattern as gen-release-notes Step 3b). Do not accumulate all rewrites in memory.

### Step 8: Update miscategorized.md

- For LOW confidence entries: add `(suggestion: likely belongs in <area> as <category>, reason: <brief explanation>)` where the reason explains the signal (e.g., "title mentions DTensor", "module: sparse label", "caffe2 build infrastructure change"). This helps the human reviewer quickly decide.
- Remove empty sections (headers with no entries under them).
- If all entries were moved, write: `<!-- All entries have been distributed to their respective worksheets. -->`

### Step 9: Report

Tell the user:
- Total PRs processed
- Moved count, broken down by target area
- Remaining count (LOW confidence) with suggested areas
- Which `done/` worksheets were modified (flag these for re-review)
- Do NOT commit unless asked.

## Key references

| File | Why |
|---|---|
| `.claude/skills/gen-release-notes/SKILL.md` | Pattern for skill structure, GraphQL batch-fetch, entry format, categories |
| `merge.py` lines 94-134 | `module_name_mapping` dict — canonical area short names |
| `<version>/miscategorized.md` | Input format to parse |
| Any `result_<area>.md` worksheet | Output format — preamble + `## <area>` + `### <category>` sections |
