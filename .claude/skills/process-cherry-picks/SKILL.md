---
name: process-cherry-picks
description: Process cherry-picks from a release tracker issue. Trigger on "process cherry-picks", "cherry-picks", "update cherry picks".
---

# Process Cherry-Picks

Parse a GitHub release tracker issue, handle reverts by removing entries from worksheets, and add new cherry-picks to `cherrypicks.md`.

## Usage

```
/process-cherry-picks <version> <tracker-issue-url>
```

Both arguments are required. Do NOT guess the tracker issue URL — always require the user to provide it.

## Instructions

### Step 0: Validate inputs

1. Check that both `<version>` and `<tracker-issue-url>` are provided. If either is missing, ask the user.
2. Extract the issue number from the URL (e.g., `175093` from `https://github.com/pytorch/pytorch/issues/175093`).
3. Fetch the issue title:
   ```bash
   gh issue view <number> --repo pytorch/pytorch --json title --jq '.title'
   ```
4. Validate the title contains the version string. The title format is `[v.<version>] Release Tracker` or `[v<version>] Release Tracker` (e.g., `[v.2.11.0] Release Tracker`). If the version doesn't match, error out with a clear message: "Issue #NNNNN is for version X.Y.Z but you specified A.B.C".
5. Confirm `<version>/` directory exists.
6. Confirm `<version>/cherrypicks.md` exists (the template should already be there with empty `## <category>` headings).

### Step 1: Parse tracker issue comments

Fetch comments:
```bash
gh issue view <number> --repo pytorch/pytorch --comments
```

Parse each comment looking for the structured cherry-pick template:
```
Link to landed trunk PR (if applicable):
* <URL or NA>

Link to release branch PR:
* <URL>

Criteria Category:
* <category text>
```

Handle these variations:
- Bullet markers: `*` or `-`
- PR references: full GitHub URLs (`https://github.com/pytorch/pytorch/pull/NNNNN`) or shorthand (`#NNNNN`)
- Multiple PRs per field (listed as separate bullets)
- Extended description text after the criteria category
- "NA" or empty for trunk PR (release-only changes)

**Skip non-structured comments** — discussion, status messages like "Please monitor...", etc. A comment is structured if it contains both "Link to landed trunk PR" and "Link to release branch PR".

For each structured entry, extract:
- `trunk_prs`: list of PR numbers (empty list if "NA")
- `release_branch_prs`: list of PR numbers
- `criteria`: the criteria category text (e.g., "Critical", "Reverted on trunk", "CI changes", "Release only changes", "Regression", "Docs")

### Step 2: Filter to merged cherry-picks only

**Do NOT rely on `@<username> merged` annotations in issue comments** — these are unreliable and frequently missing for entries that were actually merged. Instead, check the actual merge state of each release branch PR via GraphQL:

```bash
gh api graphql -f query='
{
  pr175108: repository(owner: "pytorch", name: "pytorch") {
    pullRequest(number: 175108) { number merged }
  }
  pr175159: repository(owner: "pytorch", name: "pytorch") {
    pullRequest(number: 175159) { number merged }
  }
}'
```

Build the query with one alias per release branch PR (up to 100 per query, split if needed). A cherry-pick entry is merged if and only if `merged: true` on its release branch PR. If an entry has multiple release branch PRs, it is merged if at least one of them is merged.

Only process entries whose release branch PR is merged. Report skipped/unmerged entries so the user knows what was excluded and can follow up.

### Step 3: Separate reverts from new commits

- **Reverts**: entries where the criteria text contains "Reverted on trunk" (case-insensitive). The trunk PR(s) are the ones that were reverted — their entries should be removed from the release notes worksheets.
- **New commits**: everything else (Critical, Regression, CI changes, Release only, Docs, etc.).

### Step 4: Handle reverts — remove from worksheets

For each revert entry:
1. Get the trunk PR number(s) — these are the PRs being reverted.
2. Search all `<version>/done/result_*.md` and `<version>/todo/result_*.md` worksheets for each PR number (grep for `#NNNNN`).
3. If found, remove the entire entry: the `- ... ([#NNNNN](...))` line AND any indented continuation lines below it (for bc breaking entries with multi-line write-ups — keep removing lines until hitting another `- ` entry, a `###` heading, or a blank line followed by a non-indented line).
4. Write the updated worksheet.
5. Report: which worksheet was modified, what entry was removed.
6. If the PR is not found in any worksheet, note it — it may have already been removed, was never included, or was in `### not user facing` and already dropped.

### Step 5: Handle new commits — categorize and format

For each new (non-revert) merged cherry-pick:

1. Determine the PR number to categorize. Use the **trunk PR** if available (it has the original labels); fall back to the release branch PR if trunk is "NA".

2. **Batch-fetch labels via GraphQL** — same pattern as `/categorize-miscategorized` Step 4. Build a query with up to 100 aliases:
   ```bash
   gh api graphql -f query='
   {
     pr175100: repository(owner: "pytorch", name: "pytorch") {
       pullRequest(number: 175100) {
         number
         state
         title
         labels(first: 20) { nodes { name } }
       }
     }
   }'
   ```

3. **Classify area**: follow the exact classification logic defined in `.claude/skills/categorize-miscategorized/SKILL.md` Step 5. Priority chain: `release notes:` labels (HIGH) → `module:` labels (MEDIUM) → title keywords (MEDIUM) → LOW if no match.

4. **Classify category**: follow the exact logic in `.claude/skills/categorize-miscategorized/SKILL.md` Step 6. Use `topic:` labels and title keywords to determine `## bc breaking`, `## bug fixes`, `## improvements`, etc.

5. **Format entries**: follow the exact formatting standards defined in `.claude/skills/gen-release-notes/SKILL.md` under "Category guidelines" (Step 3b):
   - **`bc breaking`, `deprecation`, `new features`**: fetch the PR body and diff, write full detailed entries (summary, impact, workaround, before/after code examples for bc breaking; before/after code for deprecation; clean description for new features).
   - **All other categories**: condensed one-liners are fine. Clean up noisy title prefixes using the same rules as `.claude/skills/categorize-miscategorized/SKILL.md` Step 7a.

### Step 6: Write to cherrypicks.md

The `cherrypicks.md` format differs from the area worksheets — it uses `## <category>` top-level headings with `### <Area>` subheadings grouped by functional area. Area names use the "nice names" from `merge.py` `module_name_mapping` (e.g., "Inductor", "Distributed", "FX", "MPS"). See `2.10.0/cherrypicks.md` for a populated example.

For each categorized entry:
1. Read the current `<version>/cherrypicks.md`.
2. Find the `## <category>` heading (e.g., `## bug fixes`).
3. Find or create the `### <Area>` subheading under it (use the nice name from `module_name_mapping`).
4. Append the formatted entry under that subheading.
5. Write the updated file.

Entries that can't be confidently categorized (LOW confidence) go under `## Untopiced` with a note explaining why.

### Step 7: Handle special criteria categories

The criteria text from the tracker issue provides hints but is NOT authoritative for categorization — always prefer PR labels. However, use these criteria-based defaults:

- **"CI changes"** and **"Release only changes"**: typically `## not user facing` unless PR labels/title indicate otherwise.
- **"Docs"** criteria: likely `## docs`, but verify with labels.
- **"Critical"**, **"Regression"**, **"Fixnewfeature"**: categorize normally based on PR labels/title — these just explain *why* it was cherry-picked, not *what type* of change it is.

### Step 8: Report

Tell the user:
- Total cherry-pick comments found in the tracker issue
- Merged vs unmerged/pending count
- **Reverts processed**: which trunk PRs were removed from which worksheets (or noted as not found)
- **New entries added** to cherrypicks.md, broken down by `## category` / `### Area`
- Any entries that couldn't be categorized (LOW confidence) — listed with suggestions
- **Unmerged/pending entries**: list every single one with its trunk PR number(s), release branch PR number(s), criteria text, and the PR title (fetch titles if not already fetched). This lets the user see exactly what was skipped and decide whether to re-run later.
- Do NOT commit unless asked.

## Key references

| File | Why |
|---|---|
| `.claude/skills/categorize-miscategorized/SKILL.md` | Reuse: area classification (Step 5), category classification (Step 6), title cleanup (Step 7a) — follow the exact same logic |
| `.claude/skills/gen-release-notes/SKILL.md` | Reuse: formatting standards ("Category guidelines" in Step 3b) — follow the exact same format |
| `merge.py` lines 94-134 | `module_name_mapping` — maps short area names to nice display names for `### <Area>` subheadings in cherrypicks.md |
| `<version>/cherrypicks.md` | Output file — `## category` + `### Area` structure |
| `2.10.0/cherrypicks.md` | Example of a populated cherrypicks.md to match format |
