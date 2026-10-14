#!/usr/bin/env python3
"""List the people named in the PR attribution lines of a release blog draft.

usage: extract_contributors.py BLOG.md [--exclude "Name"]... [--json]

Attribution lines look like
    (PRs #1, #2 and #3 by Name, Affiliation; #4 by Other Name, TODO(affiliation))
and the PR numbers may be Markdown links. The section of each entry is the
nearest preceding Markdown heading.
"""
import argparse
import json
import re
import sys
from collections import OrderedDict

BLOCK = re.compile(r"\(PRs?\s(?:[^()]|\([^()]*\))*\)", re.S)
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def parse(text):
    text = LINK.sub(r"\1", text)
    headings = [(m.start(), m.group(2).strip()) for m in re.finditer(r"^(#{1,6})\s+(.*)$", text, re.M)]
    people = OrderedDict()  # key -> {"name", "affiliation", "prs", "sections"}
    for m in BLOCK.finditer(text):
        section = next((h for pos, h in reversed(headings) if pos < m.start()), "")
        body = " ".join(m.group(0)[1:-1].split())
        for seg in body.split(";"):
            found = re.match(r"^(?:PRs?\s)?(?P<prs>#\d+(?:(?:\s*,\s*|\s+and\s+)#\d+)*)\s+by\s+(?P<who>.+)$", seg.strip())
            if not found:
                continue
            prs = re.findall(r"#\d+", found["prs"])
            who = found["who"].strip()
            handle = re.search(r"GitHub\s+@?([\w-]+)", who)
            if who.startswith("TODO("):
                name, aff = "", "TODO"
            else:
                name, _, aff = who.partition(",")
                name, aff = name.strip(), aff.strip()
            key = name or ("@" + handle[1] if handle else who)
            p = people.setdefault(key, {"name": name, "handle": handle[1] if handle else "", "affiliation": aff, "prs": [], "sections": []})
            p["prs"] += [x for x in prs if x not in p["prs"]]
            if section and section not in p["sections"]:
                p["sections"].append(section)
    return people


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("blog")
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    people = {k: v for k, v in parse(open(a.blog).read()).items() if k not in a.exclude}
    if a.json:
        json.dump(list(people.values()), sys.stdout, indent=1)
        return
    named = [p for p in people.values() if p["name"]]
    print(f"{len(people)} entries, {len(named)} with a name\n")
    print("Mentions:\n" + " ".join("@" + p["name"] for p in named) + "\n")
    print("Affiliation TODO:")
    for p in people.values():
        if p["affiliation"].startswith("TODO"):
            print(f"- {p['name'] or '(no name) GitHub ' + p['handle']} ({', '.join(p['prs'])})")
    print("\nBy section:")
    by_sec = OrderedDict()
    for p in people.values():
        for s in p["sections"]:
            by_sec.setdefault(s, []).append(p["name"] or "@" + p["handle"])
    for s, names in by_sec.items():
        print(f"- {s}: {', '.join(names)}")


if __name__ == "__main__":
    main()
