---
name: gen-commitlist
description: Bootstrap a new PyTorch release version in this repo by generating the categorized commit list and per-area worksheets. Use when starting a release (e.g. "gen commitlist for 2.13", "set up 2.13.0 worksheets", "generate the commits for the next release"). This is the UPSTREAM step that produces <version>/todo/result_*.md; use gen-release-notes to complete each worksheet.
---

# Generate Commit List & Worksheets for a New Release

This skill runs the `scripts/release_notes/` tooling in a PyTorch checkout to
produce the categorized commit list, then lands the per-area worksheets into a
new `<version>/` folder in THIS repo, following the layout in the repo
`CLAUDE.md` / `README.md`.

It is the **upstream / bootstrap** step. Once it finishes, the downstream skills
take over:
- `/gen-release-notes <version> <area>` — complete each `todo/result_<area>.md`.
- `/categorize-miscategorized` — reclassify PRs in `miscategorized.md`.

## Use the PREVIOUS release's cherry-pick tracker (important)

This skill needs the **previous** release's cherry-pick tracker, NOT the one for
the release you are generating notes for. When generating notes for 2.13.0, use
the `[v.2.12.0] Release Tracker`.

Why: the previous release's cherry-picks already shipped in that release, but
their trunk commits land inside this release's commit range. Without removing
them (Step 3), they would be wrongly listed again in this release's notes. So we
take the previous tracker and remove its cherry-picked commits from the commit
list we parse for the current release.

## Inputs to collect first

1. **PyTorch repo path** — ask which PyTorch checkout to use (e.g.
   `/data/users/<user>/pytorch`). The commitlist scripts run there. Store as
   `$PYTORCH`.
2. **Version** — the release version in `X.Y.Z` form, no `v` prefix (e.g.
   `2.13.0`). This names the output folder in this repo. Usually inferred in
   Step 1; ask only if tags are ambiguous.
3. **Previous version's cherry-pick tracker URL** (required) — the GitHub issue
   tracking the *previous* release's cherry-picks (e.g.
   `https://github.com/pytorch/pytorch/issues/180506` for `[v.2.12.0]`). Used in
   Step 3 to pre-remove already-shipped commits. Do not guess it — ask the user.
   You can sanity-check the title matches the previous version:
   `gh issue view <n> --repo pytorch/pytorch --json title`.

## Step 0: Environment

The scripts need `requests` (and `pandas`/`torch` for the optional classifier).
The system `python3` usually lacks these. Per the PyTorch repo's rules, do not
install or hunt for alternatives — use the project's environment. A conda env
(e.g. `conda activate pytorch-3.12`) typically works. Prefix every Python
command with the activation:

```bash
source ~/.conda/etc/profile.d/conda.sh 2>/dev/null || eval "$(conda shell.bash hook)"
conda activate pytorch-3.12
```

Confirm GitHub auth: `common.py` reads `$GITHUB_TOKEN` or the `github_oauth`
token in `~/.ghstackrc`; the cherry-pick scripts use `gh`, so verify
`gh auth status`. Then move into the scripts dir (later steps assume this cwd):

```bash
cd "$PYTORCH/scripts/release_notes"
```

## Step 1: Infer the base and endpoint tags, then confirm

The commit list spans `merge-base(<base>, <endpoint>)..<endpoint>`:

- **base** = the most recent *stable* release tag (e.g. `v2.12.0`).
- **endpoint** = the latest release candidate of the *next* release (e.g.
  `v2.13.0-rc6`).

Derive them from the tags; do not hardcode. Then **confirm with the user**
before the (long) run.

```bash
git -C "$PYTORCH" fetch --tags origin

# Most recent stable release tag (vMAJOR.MINOR.PATCH, no -rc) -> base.
# The strict semver filter avoids non-release tags like viable/strict/*.
BASE=$(git -C "$PYTORCH" tag -l 'v[0-9]*' | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -1)

# Infer the next minor version (vMAJOR.MINOR.0 -> vMAJOR.(MINOR+1).0)
read MAJ MIN <<<"$(echo "$BASE" | sed -E 's/^v([0-9]+)\.([0-9]+)\..*/\1 \2/')"
NEXT="v${MAJ}.$((MIN + 1)).0"
VERSION="${MAJ}.$((MIN + 1)).0"   # X.Y.Z folder name in this repo, no 'v'

# Latest rc for the next release -> endpoint
ENDPOINT=$(git -C "$PYTORCH" tag -l "${NEXT}-rc*" | sort -V | tail -1)

echo "base (last stable):   $BASE"
echo "version (this repo):  $VERSION"
echo "endpoint (latest rc): ${ENDPOINT:-<none found>}"
```

The base also tells you which **previous tracker** to ask for: it is the tracker
for `$BASE` (e.g. base `v2.12.0` -> ask for the `[v.2.12.0]` tracker URL).

Handle edge cases before confirming:
- **No rc tags yet** (`endpoint` empty): branch may not be cut, or tags need
  fetching. Ask how to proceed (wait, or use `origin/release/<NEXT>`).
- **base is a patch release** (e.g. `v2.12.1`): still a valid base; confirm the
  inferred next version.
- Respect an explicit user override (earlier rc, release-branch HEAD, a commit).

Show the commit count and confirm via `AskUserQuestion`:

```bash
echo "commits in range: $(git -C "$PYTORCH" rev-list --count "$(git -C "$PYTORCH" merge-base "$BASE" "$ENDPOINT")".."$ENDPOINT")"
```

## Step 2: Create the commit list

One GitHub GraphQL call per commit -> 20-40 min for a few thousand commits. Run
in the background with `--verbose` and monitor. The script refuses to overwrite
an existing `results/commitlist.csv`; confirm with the user before removing one.

```bash
python commitlist.py --create_new tags/<base> <endpoint> --verbose
```

Output: `results/commitlist.csv` (+ `results/data.json`, the resumable API
cache). Categorization is automatic: `release notes:` / `topic:` PR labels
first, then title bracket prefixes, then file-path keywords. Check the spread:

```bash
python commitlist.py --stat
```

## Step 3: Pre-remove the previous release's cherry-picks (always)

The commit range includes commits that were cherry-picked into the previous
release and already shipped there. Remove them using the **previous version's**
tracker URL from the inputs:

```bash
# Parse the previous tracker -> resolve each cherry-pick to its landed trunk
# commit and validate against the commitlist. Uses `gh`, takes a few minutes.
python parse_cherry_picks.py <prev_tracker_url> --commitlist results/commitlist.csv

# Remove the matched commits. Never mutates the input; writes a new file.
python remove_cherry_picks.py \
  --commitlist results/commitlist.csv \
  --cherry-picks results/cherry_picks_<issue_number>.csv
```

Outputs:
- `results/commitlist_no_cherry_picks.csv` — **the cleaned list to export from.**
- `results/cherry_pick_removals.log` — removed / not-found / skipped log.

"Not found" entries are cherry-picks whose trunk commit is outside this release's
range (already in an even older release, or revert-only) — nothing to remove.
"Skipped" are N/A rows with no trunk commit.

## Step 4: Categorize the remainder (optional)

Most commits arrive labeled; a few land `Uncategorized`. List them:

```bash
python - <<'EOF'
import csv
csv.field_size_limit(1000000)
with open("results/commitlist_no_cherry_picks.csv") as f:
    rows = [r for r in csv.DictReader(f) if r["category"] == "Uncategorized"]
print(f"Uncategorized: {len(rows)}")
for r in rows:
    pr = r["pr_link"].rsplit("/", 1)[-1] if r["pr_link"] else "no-PR"
    print(f"  #{pr} [{r['topic']}] {r['title']}")
EOF
```

You can leave these for the downstream `/gen-release-notes` pass, or assign them
now (interactive `python categorize.py --category Uncategorized`, or a direct
CSV edit matching by PR number). Valid categories/topics live in `common.py`.

**Do not normalize category names.** This repo's worksheet filenames use the raw
label string, including spaces and parens (e.g. `result_cpu (aarch64).md`,
`result_distributed (dtensor).md`). Downstream `merge.py` and the other skills
expect that form.

## Step 5: Export per-area worksheets

Export from the cleaned (cherry-pick-removed) list. Wipe stale files first:

```bash
rm -rf results/export
python commitlist.py --export_markdown --path results/commitlist_no_cherry_picks.csv
```

Output: `results/export/result_<area>.md`, one per category, each with a
worksheet header.

## Step 6: Land the new version folder in this repo

Create `<version>/` in this repo and populate it per the repo layout. Run from
this repo's root (`~/local/torch-release-notes`):

```bash
VERSION=<X.Y.Z>            # e.g. 2.13.0
EXPORT="$PYTORCH/scripts/release_notes/results"

mkdir -p "$VERSION/todo" "$VERSION/done"
cp "$EXPORT"/export/result_*.md "$VERSION/todo"/      # worksheets (keep result_skip.md)
rm -f "$VERSION/todo/result_Uncategorized.md"          # drop empty Uncategorized if present
touch "$VERSION/done/placeholder.md"                   # keep empty done/ tracked
cp "$EXPORT/commitlist_no_cherry_picks.csv" "$VERSION/commitlist.csv"  # gitignored
```

Then create a `miscategorized.md` stub (see an existing version, e.g. `2.12.0/`,
for the exact format). Do NOT create `cherrypicks.md` or `final.md` here — those
are added later in the release-notes process, matching the leaner initial seed.

If `<version>/` already exists, confirm before overwriting.

## Step 7: Report and hand off

Tell the user:
- Commit count, category spread, and any remaining `Uncategorized`.
- That `<version>/todo/` is populated and ready.
- Next: run `/gen-release-notes <version> <area>` per area to complete the
  worksheets.
- Do NOT commit or open a PR unless asked.

## Notes

- `commitlist.csv` is gitignored (see repo `.gitignore`); the worksheets are the
  tracked artifact.
- Duplicate titles / revert pairs in worksheets are expected; cleaned up during
  the `/gen-release-notes` pass.
- Re-running `--export_markdown` regenerates the whole `results/export/` dir.
