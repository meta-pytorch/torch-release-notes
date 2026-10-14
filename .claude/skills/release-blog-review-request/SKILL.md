---
name: release-blog-review-request
description: Collect the people credited in a PyTorch release blog draft and prepare the message that asks them to review it. Use when the user asks to extract names or contributors from the release blog, list who to tag, find entries whose affiliation is still TODO, or draft a "please review the blog" request for the feature owners. Produces copy-ready name lists and a per-section owner list; it never posts anything.
disable-model-invocation: true
---

# Release Blog Review Request Skill

After `release-blog-features` produces a draft, each entry credits its PR
authors as `Name, Affiliation`. This skill turns those credits into:

1. A copy-ready list of everyone credited, for tagging.
2. The entries whose affiliation or name is still `TODO`.
3. A per-section owner list, so each person can find the part to check.
4. The review-request message to send.

## Usage

```
/release-blog-review-request <path-to-blog-draft.md> [review-doc-url]
```

- The draft must be Markdown or plain text with the credits in the
  `(PRs #1, #2 and #3 by Name, Affiliation; #4 by ...)` form. PR numbers
  may be Markdown links and the credit may wrap across lines.
- If the draft lives in a document you cannot read (access-restricted,
  untrusted authors), ask the user to export it to a file. Do not try
  to get around an access restriction.
- Ask who the release manager is and leave them out of the tag list.

## Workflow

### Step 1: Extract the credits

```
python3 -I .claude/skills/release-blog-review-request/extract_contributors.py \
    <draft.md> --exclude "<release manager name>"
```

It prints the entry count, an `@Name` mention line, the entries whose
affiliation is `TODO`, and each section with its people. Use `--json`
for the raw records.

Check the output before using it:

- An entry credited as `TODO(name, affiliation: GitHub <handle>)` has no
  real name yet. It is listed by GitHub handle and left out of the
  mention line.
- The same person can appear under several sections. They are listed
  once, with all their PRs.
- If the count looks low, look for credits the pattern missed (a
  different wording than `by Name, Affiliation`) and say so rather than
  presenting the list as complete.

### Step 2: Offer the list in the shape the user needs

- **One mention line**, as the script prints it, for pasting into a
  message.
- **One name per line**, if the user wants to tag people one at a time.
- **The TODO list**, with PR numbers, if they are chasing affiliations.
  If asked to fill them in, use the order from `release-blog-features`:
  the previous published blog, the commit email domain, the GitHub
  profile. Mark anything still unconfirmed `TODO(affiliation)`.

Pasted `@Name` text does not become a notification. Slack and similar
tools create a mention only when the user types the `@` and picks the
person, so tell the user to retype the `@` on the names that matter,
or to use a channel-wide mention if everyone is in the channel.

### Step 3: Draft the message

Use this wording, with the review document's link:

```
Can you review the following draft for the <version> release blogpost?
Make sure the feature you worked on is correctly described: <doc url>

Please leave comments in the doc, and use this thread for questions. If
your affiliation is marked TODO, please tell us what to put there.
```

Then add a "Who should check which section" list, one line per section:
`Section name: @Name @Name`. Take the sections and names from the
script's "By section" output.

A thread needs a parent message in a channel; a group DM holds only
about 9 people, so it cannot cover a whole release. Ask which channel
to use. Contributors outside the user's company are in a different
workspace, and a workspace the assistant has no access to cannot be
posted to from here, so write the message to a file for the user to
paste.

### Step 4: Do not send

Show the user the message and the recipient list. Post only when they
confirm the channel and the recipients, and only to a workspace you can
reach. If a name matched more than one person in a directory lookup,
confirm it with the user instead of picking one.

## Keep private data out of this repository

This repository is public. Do not commit the extracted name lists,
review links, Slack handles or internal usernames. Write them to a
scratch file outside the repository.
