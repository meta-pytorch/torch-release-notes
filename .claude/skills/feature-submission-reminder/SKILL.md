---
name: feature-submission-reminder
description: Draft a dev-discuss.pytorch.org forum post that calls for feature submissions for an upcoming PyTorch release, in the style of "Reminder — Calls for Features & Upcoming Branch Cut". Use when the user asks for a release announcement, feature-submission reminder, call-for-features post, or dev-discuss post for a release. Produces a Markdown draft that merges the official key-dates timeline with the AI-identified feature list, and asks owning teams to file "Release highlight for Proposed Feature" issues.
---

# Feature Submission Reminder Skill

Draft a dev-discuss.pytorch.org forum post in the
"Reminder — Calls for Features" style for an upcoming (or in-flight)
PyTorch release. The post combines:

1. A call to feature owners to file release-highlight issues.
2. The AI-identified feature list (via `release-blog-features` skill
   output, if available).
3. The official release timeline (M1-M6) from the dev-discuss
   key-dates post.

Reference exemplar:
<https://dev-discuss.pytorch.org/t/reminder-calls-for-features-upcoming-branch-cut/3225>

## Usage

```
/feature-submission-reminder <version>
```

Defaults:
- `<version>`: the upcoming release (e.g. `2.12`). Required.

Optional inputs the user may provide:
- **Key-dates URL** — a link to the release's `pytorch-release-<v>-key-dates`
  post on dev-discuss. If omitted, ask the user for it before drafting.
- **Feature list** — either a path to a Markdown file, the raw list in
  the conversation, or `auto` to call the `release-blog-features`
  skill against `release/<prev>` → `release/<version>`.

## Workflow

### Step 1 — Gather timeline

If the user provided a key-dates URL, fetch it with `WebFetch` and
extract the milestone rows verbatim — do **not** paraphrase dates.

The milestones typically follow this schema (from the 2.12 key-dates
post); confirm against the source before committing:

- **M1** — Release announcement
- **M2** — All PRs landed / Feature submission closed
- **M3.1** — Release branch cut
- **M4** — Release branch finalized, final RC, feature classifications
- **M4.1** — Tutorial drafts submission deadline
- **M5** — External-facing content finalized
- **M6** — Release Day

Mark any milestone whose date is in the past as `**Done**` alongside
the date. Do not invent M3.2/M3.3 rows if they aren't in the source.

### Step 2 — Gather feature list

Priority order:

1. If the user supplied a feature list inline or at a file path, use
   that directly.
2. If there is a recent `<version>/blog-draft.md` in this repo (from
   `release-blog-features`), reuse its **major features** section.
3. Otherwise, invoke the `release-blog-features` skill against
   `release/<prev>` → `release/<version>` and use its output.

Apply the "major features only" filter (≥4 PRs each) unless the user
asks for the long list.

### Step 3 — Draft the post

Use [announcement-template.md](announcement-template.md) as the
starting point. Substitute:

- `{{VERSION}}` — release version (e.g., `2.12`)
- `{{FEATURES_MARKDOWN}}` — the grouped feature list
- `{{TIMELINE_TABLE}}` — the M1-M6 table with dates from Step 1
- `{{KEY_DATES_URL}}` — link back to the source key-dates post

Always include:

- The AI-identified label on the feature section (e.g.,
  "Features Identified by AI") and a note that the list is not
  authoritative.
- A blockquoted ask: *"If your team is responsible for one of the
  features below, please submit a Release highlight for Proposed
  Feature issue."*
- An explicit call for missing features (especially in areas where
  AI scans typically under-sample — MPS, Quantization, CPU/Arm).

### Step 4 — Save and (optionally) publish

Save the draft to `<version>/feature-submission-reminder.md` in this
repo.

If the user asks for a Google Doc version, use the `google-docs`
skill:

```
gdocs create "PyTorch <version> Release — Call for Features" \
    --from <version>/feature-submission-reminder.md
```

Do **not** post to dev-discuss directly — the release manager will
review the draft and post it.

## Required elements

Every draft must contain:

1. **Title line** in the format `Reminder — Calls for Features & Upcoming Branch Cut: PyTorch <version>`.
2. **How to submit** section listing the two canonical mechanisms
   (new issue via template, or tag an existing RFC with
   `release-feature-request`).
3. **Checklist of what to include** in each feature submission:
   availability in the release, API stability tag, tutorial links,
   blog blurb, platform caveats.
4. **Feature list** with clear "AI-identified, not authoritative"
   framing.
5. **Timeline table** with exact dates from the key-dates post.
6. **Closing sign-off**: `Cheers,` / `Team PyTorch`.

## Things to avoid

- **Don't invent milestones or dates.** If the key-dates post doesn't
  list M3.2/M3.3, don't add them. If a date is missing, mark it
  `TODO(release-manager)`.
- **Don't claim authority.** Every feature description should be
  framed as an AI-generated starting point, not a team-confirmed
  description.
- **Don't include PR numbers in the feature list.** The reminder post
  is a call-to-action for teams, not a release-notes dump. Keep it
  readable.
- **Don't publish.** This skill drafts posts; it never posts them.
