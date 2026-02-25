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

### Step 1: Read the worksheet and gather PRs

1. **Read the worksheet** at `<version>/todo/result_<area>.md`. The worksheet contains:
   - An instructional preamble (everything before `## <area>`)
   - Category headings (`### bc breaking`, `### new features`, etc.) with some pre-sorted PRs
   - A `### Untopiced` section with PRs that haven't been categorized yet — this is typically where the bulk of the work is

2. **Determine the release window**: Find the previous release tag. The current version directory name (e.g., `2.11.0`) tells you what release you're writing notes for. Find the `.0` release immediately before it (not a patch release):
   ```bash
   gh api repos/pytorch/pytorch/releases --jq '[.[] | select(.prerelease == false)] | .[] | "\(.tag_name) \(.published_at)"' | head -10
   ```
   Pick the `.0` release whose major.minor version is immediately prior to the current one (e.g., for 2.11.0, use v2.10.0 — not v2.10.1 or any other patch release, since the `.0` release marks the branch cut).

   Also determine the **branch cut date** for the current release. Check if the release branch exists:
   ```bash
   gh api repos/pytorch/pytorch/branches/release/<major.minor> --jq '.commit.sha' 2>/dev/null
   ```
   If the branch exists, find when it was created by looking at the earliest commit on the branch that diverges from main. Use this as the end date for the search window instead of today's date, to avoid including PRs that landed on main after the branch cut.

3. **Search GitHub for any missing PRs** that closed after the previous release. First, verify the exact label name by checking one of the PRs already listed in the worksheet (the label is typically `release notes: <area>`). Then search:
   ```bash
   gh pr list --repo pytorch/pytorch --label "release notes: <area>" --state all --search "closed:YYYY-MM-DD..YYYY-MM-DD" --limit 500 --json number,title,closedAt,labels
   ```
   Use the previous release date as the start and the branch cut date as the end. Use `--limit 500` to ensure all results are returned.

   **Filtering merged vs. abandoned PRs**: Only include PRs that actually landed:
   - PRs with state MERGED are confirmed landed.
   - ghstack PRs show as CLOSED (not MERGED) on GitHub. Check for the `Merged` label in the labels array to confirm they actually landed.
   - Exclude CLOSED PRs that lack both a merge commit and the `Merged` label — these were abandoned or closed without merging.

   **Multi-area PRs**: A PR may have labels for multiple functional areas (e.g., both `release notes: dynamo` and `release notes: inductor`). If a PR is labeled for this area, include it. It may appear in other areas' release notes too — that's expected.

4. **Verify PRs are on the release branch**: A PR being closed/merged in the time window does NOT guarantee it made the branch cut. Verify that **all** PRs — both from the GitHub search AND pre-existing in the worksheet — are actually on the release branch. The pytorch/pytorch release branch is named `release/<major.minor>` (e.g., `release/2.11`).

   To get the commit SHA, prefer the merge commit when available (non-ghstack PRs), falling back to the last PR commit for ghstack PRs:
   ```bash
   # Try merge commit first
   gh pr view <NUMBER> --repo pytorch/pytorch --json mergeCommit --jq '.mergeCommit.oid'
   # If empty (ghstack PR), use the last commit in the PR
   gh pr view <NUMBER> --repo pytorch/pytorch --json commits --jq '.commits[-1].oid'
   ```

   Then check if the commit is an ancestor of the release branch. Note: the `/` in `release/2.11` must be URL-encoded as `%2F`:
   ```bash
   gh api repos/pytorch/pytorch/compare/<COMMIT_SHA>...release%2F<major.minor> --jq '.status'
   ```
   - `"behind"` or `"identical"` → commit is on the release branch (include it)
   - `"diverged"` or `"ahead"` → commit is NOT on the release branch (exclude it)

   Remove any PRs that are not on the release branch, whether they came from the GitHub search or were already in the worksheet.

5. **Check for reverted PRs**: Search for revert PRs in the same release window:
   ```bash
   gh pr list --repo pytorch/pytorch --state all --search "closed:YYYY-MM-DD..YYYY-MM-DD revert in:title" --label "release notes: <area>" --limit 100 --json number,title,labels
   ```
   If a PR was merged and then reverted (and the revert is also on the release branch), exclude both the original PR and the revert from the release notes — the net effect is zero.

6. **Exclude cherry-picks**: If `<previous_version>/cherrypicks.md` exists (e.g., `2.10.0/cherrypicks.md`), read it. Any PR numbers listed there were already included in the previous release via cherry-pick and should be removed from the current worksheet if present, even though these commits are also on the current release branch — the goal is to avoid double-counting across releases. Note that PR number formats in the cherry-picks file are inconsistent — you may see `(#170723)`, `(170124)` (no `#`), or `(triton#8248)` (cross-repo). Extract all numeric PR IDs for pytorch/pytorch when scanning. Skip this step if the file doesn't exist.

7. **Cross-reference**: Compare the verified GitHub results with what's in the worksheet (both pre-sorted and Untopiced). Note any PRs that are missing from the worksheet.

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
- Whether any PRs were found on GitHub but missing from the worksheet
- Whether anything in miscategorized.md belongs to this area
- Remind them to review the result and open a PR when ready

Do NOT commit or open a PR automatically unless the user asks.
