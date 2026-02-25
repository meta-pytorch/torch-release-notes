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

The worksheet also contains its own instructions in the preamble. Follow the instructions in **this skill document**, which supersede the worksheet's instructions where they differ.

### Step 2: Check miscategorized.md

Read `<version>/miscategorized.md` if it exists. If it's empty or doesn't exist, skip this step. Otherwise, check if any entries there belong to this functional area. If so, incorporate them into the worksheet and remove them from miscategorized.md.

### Step 3: Categorize and write up

Edit the worksheet file in place, preserving the instructional preamble (everything before `## <area>`). Only modify the content under `## <area>`.

**Process PRs in batches of 5–10** rather than attempting all at once. For each batch:
1. Fetch any needed details for the batch using multiple `gh` calls in a single tool-calling round.
2. Categorize each PR and edit the worksheet, writing entries into the correct sections.
3. Move to the next batch.

This keeps each round of work small and makes progress incrementally.

**Important:** Also review PRs pre-sorted into `### not user facing` — some may actually be user-facing (bug fixes, improvements, performance) and should be moved to the correct category.

#### When to fetch PR details

For most PRs, the title is sufficient to categorize. Only fetch additional detail when needed:
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

#### What to determine for each PR

- Is it user-facing or internal-only?
- Is it a BC-breaking change, deprecation, new feature, improvement, bug fix, performance change, docs, developer-facing, or security-related?
- Does it belong to this area or should it be moved to `miscategorized.md`? Check the PR's `release notes:` labels — if a PR is labeled for a different area (e.g., `release notes: fx` on a PR in the distributed worksheet), it belongs in miscategorized.md.

Remove any duplicate entries in the worksheet (same PR listed more than once).

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
- **devs**: Developer-facing changes, can be condensed.
- **not user facing**: List items here so reviewers can verify, but these will be dropped from the final merged release notes.
- **security**: Security-related fixes.

Format each entry as:
```
- Description of the change ([#NNNNN](https://github.com/pytorch/pytorch/pull/NNNNN))
```

For bc breaking, deprecation, and new features, each entry MUST be polished and clear for end users. For the other sections, you do NOT need to polish every entry — summarize and group related changes where it makes sense.

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
