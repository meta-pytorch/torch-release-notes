---
name: gen-final-notes
description: Merge completed worksheets into the final release notes and polish them. Trigger on "gen final notes", "generate final release notes", "build final.md", "merge release notes", "finalize release notes". This is the LAST step of the release-notes pipeline, after all <version>/done/result_*.md worksheets are complete.
---

# Generate Final Release Notes

Merge every completed worksheet in `<version>/done/` into a single `<version>/final.md`, verify nothing was lost, verify the most important entries actually match their PRs, and copy-edit the whole document.

## Scope: only edit `final.md`

- **Step 1 generates `<version>/final.md` from the worksheets. After that, all edits in this skill are made to `final.md` only.** The `<version>/done/result_*.md` worksheets are **read-only** for the rest of the run (they are read for verification, never modified).
- Because every edit lands in `final.md`, **do not re-run `merge.py` after Step 1** — regenerating would overwrite all the polish. Run the merge exactly once, at the start.
- `final.md` is a **single file**, so subagents must **not** edit it in parallel (concurrent writes clobber each other). Use subagents for read-only work (fetching PRs, reviewing text) that **returns** findings/edits; the main agent applies edits to `final.md` **serially**.
- Use **present-tense imperative** verbs in entries ("Add", "Fix", "Support", "Remove"), never past tense.

## Usage

```
/gen-final-notes <version>
```

Where `<version>` is the PyTorch release version (e.g., `2.13.0`).

## Instructions

### Step 0: Validate inputs & environment

1. If `<version>` is missing, ask the user.
2. Confirm `<version>/done/` exists and contains `result_*.md` files.
3. Ensure the `marko` markdown library is installed (merge.py needs it):
   ```bash
   python -c "import marko" 2>/dev/null || pip install marko
   ```

### Step 1: Run merge.py (the only step that reads the worksheets to write output)

```bash
python merge.py -d "<version>/done" -o "<version>/final.md"
```

- The version in the title is inferred from the `--dir` parent (`<version>/done` → `<version>`); pass `-v <version>` to override.
- **Recovery — `AssertionError: no nice name for <area> found`:** a worksheet has a module name not in merge.py's `module_name_mapping`. Add that area to the dict (`write_output` in `merge.py`) with a sensible display name, then re-run. Every release tends to add/rename a few areas. (This edits `merge.py`, not a worksheet — allowed.)
- Note which categories report "Found no commits … skipping" — expected for empty sections (e.g. `security`).

After this step, do not run `merge.py` again.

#### Required merge.py formatting behavior (verify the output has all of this)

`merge.py` must produce output matching the finished style of prior releases (e.g. `2.12.0/final.md`). Confirm the generated `final.md` has:

1. **Title + table of contents + Highlights placeholder** at the top: `# PyTorch <version> Release Notes`, the `- [Highlights](#highlights)` … TOC list, then a `# Highlights` section containing `TODO` and the "For more details …" line. (Version inferred from the `--dir` parent, or `-v`.)
2. **A blank line after every `#` and `##` heading.**
3. **Multi-line entries indented properly.** BC-breaking / deprecation entries with multi-paragraph bodies and fenced `Version X / Y` code blocks must have every continuation line indented 2 spaces so it stays *inside* the bullet. If indentation is missing, the `#`/`###` lines inside a code fence get parsed as top-level headings — the classic symptom is the Step 2 heading count coming out **> 11**. Handled by the `render_commit()` helper.
4. **Loose-list spacing:** when any entry in a module block spans multiple lines, a blank line separates every bullet in that block (otherwise the markdown renders incorrectly).
5. **Worksheet preamble filtered out:** the `## 1.`, `## 2.`, `## 3.` instruction headings from each worksheet must NOT appear — `parse_result_md` skips level-2 headings matching `^\d+\.`.

If any is missing, put the fix in `merge.py` so it's reproducible, then re-run Step 1. These enhancements may be carried as uncommitted changes from a prior release, so verify `merge.py` isn't in a pre-enhancement state (`git status merge.py`) and commit it once confirmed.

### Step 2: Verify all commits moved from done/ to final.md

Reconcile PR numbers between the worksheets (read-only) and `final.md`, reusing merge.py's own parser so the check matches the real pipeline. Write and run this:

```python
# /tmp/verify_final.py  — run as: PYTHONPATH=. python /tmp/verify_final.py <version>
import re, glob, sys
from merge import parse_result_md

version = sys.argv[1]
CATEGORY_ORDER = {"bc breaking","deprecation","new features","improvements",
                  "bug fixes","performance","docs","security","devs"}
PR = re.compile(r'#(\d+)')
def prs(t): return set(PR.findall(t))

should_be, dropped = {}, {}   # pr -> [(module,cat)]   ;  (module,cat)->count
for fn in glob.glob(f"{version}/done/result_*.md"):
    with open(fn) as f: text = f.read()
    module, info = parse_result_md(text)
    for cat, commits in info.items():
        for c in commits:
            if cat in CATEGORY_ORDER:
                for p in prs(c): should_be.setdefault(p, []).append((module, cat))
        if cat not in CATEGORY_ORDER and cat != "not user facing":
            dropped[(module, cat)] = dropped.get((module, cat), 0) + len(commits)

final_prs = set()
with open(f"{version}/final.md") as f:
    for line in f:
        if line.startswith("- [") and "](#" in line:  # skip TOC
            continue
        final_prs |= prs(line)

missing = set(should_be) - final_prs
extra   = final_prs - set(should_be)
print(f"user-facing PRs in worksheets: {len(should_be)}")
print(f"PRs found in final.md:         {len(final_prs)}")
print(f"MISSING: {len(missing)}")
for p in sorted(missing, key=int): print(f"   #{p} <- {should_be[p]}")
print(f"EXTRA: {len(extra)}")
for p in sorted(extra, key=int): print(f"   #{p}")
print(f"NON-STANDARD categories dropped (NOT published): {dropped or 'none'}")
```

- **MISSING must be 0** and **EXTRA must be 0** at this point (right after generation). If not, investigate before continuing.
- **NON-STANDARD categories** flags commits under headings merge.py doesn't emit (e.g. a stray `Untopiced` category). Non-zero counts mean those commits are silently dropped — surface them to the user. (Fixing this means recategorizing in the worksheet, which is outside this skill's scope; flag it rather than editing worksheets.)
- Confirm the top-level heading count is exactly 11 (title + Highlights + 9 sections):
  ```bash
  grep -cE '^# ' "<version>/final.md"   # expect 11
  ```
  More than 11 means a multi-line entry's code fence or `#` line leaked out as a heading — fix that entry's indentation directly in `final.md`.

Run this reconciliation **before** the editing steps. After Steps 3–4 you may intentionally delete/alter entries, so a later MISSING result is expected only for those deliberate changes.

### Step 3: Verify BC-breaking / deprecation / new-feature entries against their PRs

These three sections get the most reader scrutiny, so verify each entry's summary actually matches what the PR did.

1. Extract every entry (and its PR number(s)) from the `# Backwards Incompatible Changes`, `# Deprecations`, and `# New Features` sections of `final.md`.
2. **Fan out to parallel subagents** (Agent tool, `general-purpose`) for the **read-only** fetch-and-compare work — this does not edit `final.md`, so it parallelizes safely. Split the entries into batches; give each agent the exact summary text + PR number(s) and these instructions:
   - Fetch each PR from `pytorch/pytorch` — use the **github-query skill** (`.llms/skills/claude-templates/github-query/SKILL.md`), or `gh pr view <n> --repo pytorch/pytorch --json title,body,url` and `gh pr diff <n>`. (If the github-query skill lacks credentials, it can be bootstrapped from the authenticated `gh` token.)
   - Judge: does the summary correctly describe the actual change (API names, direction, behavior)? Are code examples and version references correct? For a 2.X release, "Version 2.(X-1) → 2.X" framing is expected; flag references to unrelated versions.
   - Return per entry: `OK` / `MISMATCH` / `UNVERIFIABLE` with a one-to-three-sentence justification, and a collected MISMATCH list. Agents **report**; they do not edit.
3. **Common failure modes** (all seen in practice): wrong warning type (`DeprecationWarning` vs `UserWarning`), a stale version number copied from the PR body, and — most important — a **wrong PR linked entirely** (the summary describes something the PR didn't do). Cross-check a suspected wrong link against `<version>/commitlist.csv`: if the PR's row there describes something different and the PR is already used correctly by another entry, the entry is bogus.
4. The **main agent** applies fixes **to `final.md`** (serially): correct the wording, or delete a bogus entry. **Flag every change to the user** with the PR number and what was wrong. For anything you can't resolve confidently (e.g. a claim that maps to no PR in the release), do **not** silently substitute a PR — report it and ask.

### Step 4: Proofread, add code formatting, remove internal references

Copy-edit **all** published entries in `final.md`.

Because `final.md` is one file, do **review in parallel, apply serially**:
- **Fan out read-only reviewer subagents**, each assigned a section or line-range of `final.md` (the big sections — Improvements, Bug Fixes — can be split further). Each agent reads its range and **returns a list of precise `before → after` edits** (exact original substring + replacement). Agents must **not** edit the file.
- The **main agent applies** those edits to `final.md` with the Edit tool, one at a time.

Give each reviewer these rules:

**Goal 1 — inline code formatting:** wrap bare code identifiers in backticks (function/method names, class names, API names, argument names, dtypes, attribute names, file paths, env vars, config flags, C++/Metal symbols, decorators, dotted module paths). Signals: snake_case, CamelCase, dotted.paths, `()`, `::`, leading underscores, known API names. Do **not** wrap ordinary English or acronyms/proper names (NCCL, ROCm, HIP, SDPA, DDP, etc.). Never double-wrap.

**Goal 2 — grammar:** fix subject-verb agreement, articles, plurals, typos, awkward/run-on phrasing. Keep present-tense imperative style. Do not change technical meaning.

**Goal 3 — remove internal references:** strip internal-only content from entries:
- Bracketed internal tags at the start of a title: `[Optimus]`, `[BE]`, `[codemod]`, team/infra tags, and area tags that merely duplicate the section (see `categorize-miscategorized` Step 7a for the full list). Reword so the entry describes what the change does in user-facing terms.
- Internal codenames/systems (e.g. "Optimus" is the internal name for the pre-grad batch-fusion passes; "APS", "IGCTR", "AFOC", "MAST" are internal). Replace with the public concept or remove.
- Phabricator/Diff/task IDs (`D#######`, `P#######`, `T######`), `fbcode`, `Differential Revision`, internal URLs.

**Strict rules for every reviewer:**
- Only touch bullet text under the published category sections. Never touch PR/issue links or numbers, section/module headings, the TOC, the Highlights block, or anything inside existing backticks or fenced code blocks.
- Copy-editing only — do not reword/summarize substance (except when removing an internal tag requires a light reword). When unsure, leave as-is.

> Note: most internal-looking commits already lived under `not user facing` in the worksheets and never reached `final.md`, so you generally won't see Diff IDs or `[Dependabot]`/`[CI]` bumps here. Only fix internal refs that actually appear in `final.md`.

### Step 5: Final integrity check (on final.md)

Check for unbalanced inline backticks introduced by editing (the awk toggles a flag on code-fence marker lines — after stripping indentation — skips fenced content, then flags any remaining line with an odd number of backticks):

````bash
awk '
{ line=$0; sub(/^[ \t]+/,"",line) }
line ~ /^```/ { infence=!infence; next }
infence { next }
{ n=gsub(/`/,"`"); if (n%2==1) print NR": "$0 }
' "<version>/final.md"   # any output = a broken inline-code span to fix
````

Also re-check the heading count (`grep -cE '^# ' "<version>/final.md"` — still 11 unless you intentionally added/removed a section). Optionally re-run the Step 2 reconciliation, remembering that MISSING should now list **only** entries you intentionally deleted in Step 3.

### Step 6: Highlights (optional, last)

`# Highlights` in `final.md` is a `TODO` placeholder with no worksheet source. If the user wants it filled, edit it directly in `final.md`. Prior releases (e.g. `2.12.0/final.md`) use an HTML `<table>` of one-line highlights; match that style.

### Step 7: Report

Tell the user:
- That `final.md` was generated and the Step 2 reconciliation passed (X/X PRs, 0 missing, 0 extra).
- Any Step 3 PR-content mismatches found and how each was resolved (fixed / deleted / needs-your-input).
- A summary of Step 4 edits (roughly how many, notable internal-reference removals).
- Do **not** commit unless asked.

## Key references

| File | Why |
|---|---|
| `merge.py` | The merge script; `module_name_mapping` + `category_order` in `write_output` |
| `final_template.md` | Canonical section order and heading style for the final notes |
| `<version>/commitlist.csv` | Source of truth for which PRs belong to the release; use to confirm wrong-link suspicions |
| `.claude/skills/gen-release-notes/SKILL.md` | Entry format, category guidelines, GraphQL batch-fetch pattern |
| `.claude/skills/categorize-miscategorized/SKILL.md` (Step 7a) | Full list of internal title-prefix tags to strip |
| A prior `<version>/final.md` (e.g. `2.12.0`) | Reference for finished formatting incl. Highlights table |
