Title (paste into the title field): Reminder — Call for Features: PyTorch {{VERSION}}
Category: Release Announcements

Paste everything below this line into the composer body, using plain-text paste (Cmd+Shift+V / Ctrl+Shift+V).

----

Hi everyone,

This is a reminder to feature owners to file a release-highlight issue for every feature you want tracked in the {{VERSION}} release.

IMPORTANT: features that are not submitted will NOT be mentioned in the release blog or other comms.

## How to submit

Either one of:

1. Open a new issue on pytorch/pytorch using the "Release highlight for Proposed Feature" template, or
2. Label an existing RFC or tracking issue with `release-feature-request`.

Please include, per feature:

- What ships in {{VERSION}}: the API surface, plus a stability designation of either API Stable or API Unstable. (Beta and Prototype are no longer used as designations.)
- Tutorial links, new or updated.
- A short blog-post write-up, 2-3 paragraphs, usable as-is in the release blog.
- Any platform or backend caveats: CUDA, ROCm, XPU, MPS, CPU-Arm.

The running list of tracked features lives [here](https://github.com/pytorch/pytorch/issues?q=label%3Arelease-feature-request+is%3Aissue).

## {{VERSION}} Features Identified by AI

The following was identified by an AI-assisted scan of the `release/{{PREV_VERSION}}` to `release/{{VERSION}}` diff. This list is a starting point, not authoritative: descriptions and designations have not been reviewed by the feature owners, so it will miss things and mis-scope others.

> Note: if your team is responsible for one of the features below, please submit a "Release highlight for Proposed Feature" issue so we can track the official description, tutorial, and blog write-up. Corrections and missing features are equally welcome — reply on this thread or open an issue.

{{FEATURES_MARKDOWN}}

## {{VERSION}} Release Timeline

{{TIMELINE_TABLE}}

{{MILESTONE_STATUS_NOTE}}

## How you can help

- Feature owners: submit a release-highlight issue with the blog blurb and tutorial links.
- Tutorial authors: open PRs against pytorch/tutorials tagged `{{VERSION}}-release`. These are tracked toward M4.1.
- Everyone else: flag anything major that is missing from the list above, particularly in {{UNDER_SAMPLED_AREAS}}.

Questions welcome on this thread.

Cheers,

Team PyTorch
