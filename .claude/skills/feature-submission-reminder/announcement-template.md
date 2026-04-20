# Reminder — Calls for Features & Upcoming Branch Cut: PyTorch {{VERSION}}

Hi everyone,

As we head into the PyTorch {{VERSION}} release cycle, this is a
reminder to feature owners to **file a release-highlight issue** for
every feature you want tracked in the release.

## How to submit a feature

Please either:

1. **Open a new issue** on `pytorch/pytorch` using the
   **"Release highlight for Proposed Feature"** template, **or**
2. Tag an existing RFC / tracking issue with the
   **`release-feature-request`** label.

For each feature, include:

- What will be available in **release {{VERSION}}** (API surface,
  stability tag: Stable / Beta / Prototype)
- Link(s) to **relevant tutorials** (new or updated)
- A short **blog-post write-up** (2-3 paragraphs, usable as-is in the
  release blog)
- Any platform or backend caveats (CUDA / ROCm / XPU / MPS / CPU-Arm)

The running list of tracked features lives here:
<https://github.com/pytorch/pytorch/issues?q=label%3Arelease-feature-request+is%3Aissue>

## {{VERSION}} Features Identified by AI

The following major features were identified by an AI-assisted scan
of the `release/{{PREV_VERSION}} → release/{{VERSION}}` commit diff.
This list is a starting point, not authoritative — descriptions and
stability tags have not been reviewed by the feature owners.

> **Note:** If your team is responsible for one of the features
> below, please submit a **"Release highlight for Proposed Feature"**
> issue so we can track the official description, tutorial, and blog
> write-up. Corrections and missing features are equally welcome —
> reply on this thread or open an issue.

{{FEATURES_MARKDOWN}}

## {{VERSION}} Release Timeline

Official dates from the
[PyTorch Release {{VERSION}} Key Dates]({{KEY_DATES_URL}}) post:

{{TIMELINE_TABLE}}

## How to help

- **Feature owners:** file a release-highlight issue (template above)
  with your blog blurb + tutorial links.
- **Tutorial authors:** PRs to `pytorch/tutorials` with the
  `{{VERSION}}-release` label are tracked against M4.1.
- **Everyone else:** please review the feature list above and reply
  in this thread if something major is **missing** — particularly
  for MPS, Quantization, and CPU/Arm, where the diff-based scan
  typically catches few candidates.

If you have questions, reach out in `#release-engineering` on Slack
or reply on this topic.

Cheers,
Team PyTorch
