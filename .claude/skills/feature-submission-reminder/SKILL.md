---
name: feature-submission-reminder
description: Draft a dev-discuss.pytorch.org forum post that calls for feature submissions for an upcoming PyTorch release, in the style of "Reminder — Call for Features". Use when the user asks for a release announcement, feature-submission reminder, call-for-features post, or dev-discuss post for a release. Produces a Markdown draft that merges the official key-dates timeline with the AI-identified feature list, and asks owning teams to file "Release highlight for Proposed Feature" issues.
disable-model-invocation: true
---

# Feature Submission Reminder Skill

Draft a dev-discuss.pytorch.org forum post in the
"Reminder — Call for Features" style for an upcoming (or in-flight)
PyTorch release. The post combines:

1. A call to feature owners to file release-highlight issues.
2. The AI-identified feature list (via `release-blog-features` skill
   output, if available).
3. The official release timeline (M1-M6) from the dev-discuss
   key-dates post.

Reference exemplars, most recent first:
- <https://dev-discuss.pytorch.org/t/reminder-call-for-features-pytorch-2-13/3405>
- <https://dev-discuss.pytorch.org/t/reminder-calls-for-features-upcoming-branch-cut/3225>

Fetch the most recent one and match its title and section wording; the
format drifts between releases.

## Usage

```
/feature-submission-reminder <version>
```

Defaults:
- `<version>`: the upcoming release (e.g. `2.14`). Required.

Optional inputs the user may provide:
- **Key-dates URL** — a link to the release's `pytorch-release-<v>-key-dates`
  post on dev-discuss. If omitted, ask the user for it before drafting.
- **Feature list** — either a path to a Markdown file, the raw list in
  the conversation, or `auto` to call the `release-blog-features`
  skill against `release/<prev>` → `release/<version>`.

## Output format: paste-ready for Discourse

The release manager pastes this into the dev-discuss composer by hand.
The skill does not post it, so the draft must survive a copy-paste.

- **Put the title outside the body.** Discourse takes the title in its
  own field, so a `#` H1 at the top of the body renders as a duplicate
  heading. Emit the title on a labelled line at the top of the file,
  then a `----` separator, then the body.
- **Keep links inline** as `[text](url)`. A bare URL on its own line
  becomes an onebox preview card in Discourse, which is not wanted
  mid-paragraph.
- **Avoid `**bold**` emphasis, and tell the user to paste as plain
  text.** Discourse converts pasted *HTML* to Markdown, and most
  sources put HTML on the clipboard: copying from a syntax-highlighting
  editor or a rendered file view yields `<strong>**IMPORTANT**</strong>`,
  which Discourse turns into `**\*\*IMPORTANT\*\***`. Plain-text paste
  (Cmd+Shift+V / Ctrl+Shift+V) avoids it, but emphasis markers are the
  first thing to break if the user forgets, so prefer plain wording and
  lean on headings and lists for structure. Put the plain-text-paste
  instruction in the file itself, above the separator.
- **Wrap identifiers containing underscores in backticks.** Discourse
  treats `_word_` as italics, so `_set_pg_timeout` renders wrong
  unbackticked.
- **Avoid bare `@handle`.** Discourse turns it into a user mention.
  Backtick it or use the person's name.
- Standard Discourse markdown is otherwise fine: `##` headings, `-`
  bullets, numbered lists, `>` blockquotes, tables.

## Workflow

### Step 1 — Gather timeline

If the user provided a key-dates URL, fetch it with `WebFetch` and
extract the milestone rows verbatim — do **not** paraphrase dates.

The milestones typically follow this schema; confirm against the source
before committing:

- **M1** — Release announcement
- **M2** — All PRs landed / Feature submission closed
- **M3** — Release branch cut, RC1 for PyTorch and Torchvision
- **M4** — Release branch finalized, final RC, feature classifications
- **M4.1** — Tutorial drafts submission deadline
- **M5** — External-facing content finalized
- **M6** — Release Day

Mark any milestone whose date is in the past as `**Done**` alongside
the date. Do not invent M3.1/M3.2 rows if they aren't in the source.

**Say where the release currently stands.** In practice this post goes
out *after* the branch cut: the 2.13 reminder was posted 24 June, with
M3 in the week of 8 June and M4 in the week of 22 June. A call for
features that lands after M2 reads as already-too-late unless the post
says otherwise. Fill `{{MILESTONE_STATUS_NOTE}}` with which milestones
are complete and note that feature classifications are published at M4,
so issues filed now can still make the blog.

### Step 2 — Gather feature list

Priority order:

1. If the user supplied a feature list inline or at a file path, use
   that directly.
2. If there is a recent `<X.Y.Z>/blog-draft.md` in this repo (from
   `release-blog-features`), reuse its feature sections.
3. Otherwise, invoke the `release-blog-features` skill against
   `release/<prev>` → `release/<version>` and use its output.

Apply the "major features only" filter (≥4 PRs each) unless the user
asks for the long list.

Group the list the way the blog does — Features, Performance
Improvements, Deprecations and BC-breaking changes, Non-Feature Updates
— so the two documents agree.

### Step 3 — Identify the under-sampled areas

The post asks readers to fill gaps, so name the areas most likely to
have them. **Derive this from the worksheet counts rather than reusing
last release's list**, which changes every cycle. Count candidate
entries per area in `<X.Y.Z>/todo/` and `<X.Y.Z>/done/` and name the
thinnest user-facing areas in `{{UNDER_SAMPLED_AREAS}}`.

For 2.14 the thin areas were Quantization (13 candidates, nearly all
typo fixes), ONNX (5), Export (9) and CPU x86/aarch64 (3 and 2), while
MPS was the single largest pool at 82 — the opposite of the standing
assumption that MPS is under-sampled.

### Step 4 — Draft the post

Use [announcement-template.md](announcement-template.md) as the
starting point. Substitute:

- `{{VERSION}}` — release version (e.g., `2.14`)
- `{{PREV_VERSION}}` — previous release (e.g., `2.13`)
- `{{FEATURES_MARKDOWN}}` — the grouped feature list
- `{{TIMELINE_TABLE}}` — the M1-M6 rows with dates from Step 1
- `{{MILESTONE_STATUS_NOTE}}` — which milestones are done (Step 1)
- `{{UNDER_SAMPLED_AREAS}}` — the thin areas (Step 3)

Always include:

- The AI-identified label on the feature section and a note that the
  list is not authoritative.
- A blockquoted ask: *"If your team is responsible for one of the
  features below, please submit a Release highlight for Proposed
  Feature issue."*
- An explicit call for missing features.

### Step 5 — Save

Save the draft to `<X.Y.Z>/feature-submission-reminder.md` in this
repo. Note the directory is the full `X.Y.Z` version, e.g. `2.14.0/`.

Do **not** post to dev-discuss directly — the release manager will
review the draft and post it.

## Required elements

Every draft must contain:

1. **Title line** outside the body, in the format used by the most
   recent post (2.13 used `Reminder — Call for Features: PyTorch <version>`;
   earlier posts used `Reminder — Calls for Features & Upcoming Branch Cut`).
2. **How to submit** section listing the two canonical mechanisms
   (new issue via template, or label an existing RFC with
   `release-feature-request`).
3. **Checklist of what to include** in each feature submission:
   what ships in the release, the stability designation, tutorial
   links, blog blurb, platform caveats.
4. **Feature list** with clear "AI-identified, not authoritative"
   framing.
5. **Timeline table** with exact dates from the key-dates post, plus a
   note on which milestones are complete.
6. **Closing sign-off**: `Cheers,` / `Team PyTorch`.

## Designations

Ask for **API Stable** or **API Unstable**. Beta and Prototype are
retired — the 2.13 release blog carries an explicit changelog note
that prototype "is a designation that we no longer use." Do not ask
feature owners for a Stable/Beta/Prototype tag.

## Things to avoid

- **Don't invent milestones or dates.** If the key-dates post doesn't
  list a milestone, don't add it. If a date is missing, mark it
  `TODO(release-manager)`.
- **Don't claim authority.** Every feature description should be
  framed as an AI-generated starting point, not a team-confirmed
  description.
- **Don't include PR numbers in the feature list.** The reminder post
  is a call-to-action for teams, not a release-notes dump. Keep it
  readable.
- **Don't reuse last release's list of under-sampled areas.** Recount
  from the worksheets.
- **Don't publish.** This skill drafts posts; it never posts them.
