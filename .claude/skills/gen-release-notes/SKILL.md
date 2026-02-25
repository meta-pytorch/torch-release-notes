---
name: gen-release-notes
description: Generate PyTorch release notes for a functional area. Use when the user says "gen-release-notes", "release notes", or wants to write/complete release notes for a functional area like "aotdispatcher", "dynamo", "inductor", etc.
---

# Generate PyTorch Release Notes

Generate and complete the release notes worksheet for a given functional area.

## Usage

```
/gen-release-notes <area>
```

Where `<area>` is the functional area name (e.g., `aotdispatcher`, `dynamo`, `inductor`).

## Instructions

### Step 0: Validate inputs

1. Check that the area argument was provided. If not, list the available areas from the `todo/` directory of the latest release and ask the user to pick one.
2. Find the latest release directory (highest version number in the repo root, e.g., `2.11.0/`). Be careful with version comparison — compare numerically, not lexicographically (e.g., `2.11.0` > `2.9.0`).
3. Confirm the worksheet file exists at `<version>/todo/result_<area>.md`. If it's already in `done/`, tell the user it's already completed and ask if they want to re-process it.

### Step 1: Read the worksheet

**Read the worksheet** at `<version>/todo/result_<area>.md`. The worksheet contains:
- An instructional preamble (everything before `## <area>`)
- Category headings (`### bc breaking`, `### new features`, etc.) with some pre-sorted PRs
- A `### Untopiced` section with PRs that haven't been categorized yet — this is typically where the bulk of the work is

Trust the worksheet contents — do not search GitHub for missing PRs or verify that PRs are on the release branch. The worksheet was generated from the actual release branch and is the source of truth.

### Step 2: Understand each PR

For PRs in the worksheet, the title is usually sufficient to categorize. Only fetch additional detail when needed:
- For potential BC-breaking changes or deprecations, always read the full PR body and diff to write a proper migration guide.
- For new features, read the PR body to write a clear description.
- For ambiguous titles, fetch the PR body to determine the correct category.

```bash
gh pr view <NUMBER> --repo pytorch/pytorch --json title,body,labels
gh pr diff <NUMBER> --repo pytorch/pytorch  # only when needed
```

Some worksheet entries may reference bare commit hashes (e.g., `d2305bd68fe`) instead of PR links. Look up the corresponding PR number so all entries have a consistent `[#NNNNN](...)` link format:
```bash
gh api repos/pytorch/pytorch/commits/<HASH>/pulls --jq '.[0].number'
```

Determine for each PR:
- Is it user-facing or internal-only?
- Is it a BC-breaking change, deprecation, new feature, improvement, bug fix, performance change, docs, developer-facing, or security-related?
- Does it belong to this area or should it be moved to `miscategorized.md`?

### Step 3: Check miscategorized.md

Read `<version>/miscategorized.md` if it exists. If it's empty or doesn't exist, skip this step. Otherwise, check if any entries there belong to this functional area. If so, incorporate them into the worksheet. Note which entries you're claiming so the user can remove them from miscategorized.md (don't edit miscategorized.md directly, since other areas may be editing it concurrently).

### Step 4: Categorize and write up

Edit the worksheet file in place, preserving the instructional preamble (everything before `## <area>`). Only modify the content under `## <area>`.

Move all PRs from `### Untopiced` into the correct category, leaving it empty. The category headings under `## <area>` should be:

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

    Version 2.10.0:
    ```python
    >>> torch.foo(bar)
    old_result
    ```

    Version 2.11.0:
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
- **devs**: Developer-facing changes, can be condensed.
- **not user facing**: List items here so reviewers can verify, but these will be dropped from the final merged release notes.
- **security**: Security-related fixes.

Format each entry as:
```
- Description of the change ([#NNNNN](https://github.com/pytorch/pytorch/pull/NNNNN))
```

For bc breaking, deprecation, and new features, each entry MUST be polished and clear for end users. For the other sections, you do NOT need to polish every entry — summarize and group related changes where it makes sense.

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
