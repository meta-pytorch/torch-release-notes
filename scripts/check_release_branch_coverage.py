#!/usr/bin/env python3
"""Check that effective commits on a PyTorch release branch appear in release notes.

The checker compares a PyTorch git range with the release-note source files for a
version. It understands normal PR commits, release-branch cherry-picks, direct
commits referenced by SHA, and explicit git reverts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


PR_URL_RE = re.compile(r"https://github\.com/pytorch/pytorch/pull/(\d+)")
SUBJECT_PR_RE = re.compile(r"#(\d+)")
RESOLVED_PR_RE = re.compile(
    r"(?im)^Pull Request resolved:\s*"
    r"https://github\.com/pytorch/pytorch/pull/(\d+)\s*$"
)
CHERRY_PICK_RE = re.compile(r"\(cherry picked from commit ([0-9a-f]{7,40})\)", re.I)
REVERT_TARGET_RE = re.compile(r"This reverts commit ([0-9a-f]{7,40})", re.I)
HEX_TOKEN_RE = re.compile(r"(?<![0-9a-f])([0-9a-f]{7,40})(?![0-9a-f])", re.I)
NON_USER_FACING = {"not user facing", "untopiced"}


class AuditError(RuntimeError):
    pass


@dataclass(frozen=True)
class Commit:
    sha: str
    parents: Tuple[str, ...]
    subject: str
    body: str


@dataclass(frozen=True)
class CommitIds:
    canonical_prs: frozenset[str]
    alias_prs: frozenset[str]


@dataclass(frozen=True)
class NoteLocation:
    path: str
    line: int
    category: Optional[str]
    user_facing: bool


@dataclass
class NoteInventory:
    prs: Dict[str, List[NoteLocation]]
    hashes: Dict[str, List[NoteLocation]]
    files: List[str]


def run_git(repo: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if process.returncode:
        detail = process.stderr.strip() or process.stdout.strip()
        raise AuditError(f"git {' '.join(args)} failed in {repo}: {detail}")
    return process.stdout


def normalize_version(version: str) -> Tuple[str, int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)(?:\.(\d+))?", version)
    if not match:
        raise AuditError(f"invalid version {version!r}; expected X.Y or X.Y.Z")
    major, minor, patch = (int(match.group(1)), int(match.group(2)), int(match.group(3) or 0))
    return f"{major}.{minor}.{patch}", major, minor, patch


def default_refs(major: int, minor: int, patch: int) -> Tuple[str, str]:
    release_ref = f"origin/release/{major}.{minor}"
    if patch:
        base_ref = f"v{major}.{minor}.0"
    elif minor:
        base_ref = f"v{major}.{minor - 1}.0"
    else:
        raise AuditError("cannot infer the previous release for X.0.0; pass --base-ref")
    return base_ref, release_ref


def load_commits(repo: Path, base_ref: str, release_ref: str) -> Tuple[str, str, List[Commit]]:
    merge_base = run_git(repo, "merge-base", base_ref, release_ref).strip()
    release_sha = run_git(repo, "rev-parse", f"{release_ref}^{{commit}}").strip()
    raw = run_git(
        repo,
        "log",
        "--reverse",
        "--format=%H%x1f%P%x1f%s%x1f%b%x1e",
        f"{merge_base}..{release_ref}",
    )
    commits: List[Commit] = []
    for record in raw.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        fields = record.split("\x1f", 3)
        if len(fields) != 4:
            raise AuditError("could not parse git log output")
        sha, parents, subject, body = fields
        commits.append(Commit(sha, tuple(parents.split()), subject, body))
    return merge_base, release_sha, commits


def parse_patch_equivalent_shas(output: str) -> set[str]:
    result: set[str] = set()
    for line in output.splitlines():
        match = re.fullmatch(r"([+-]) ([0-9a-f]{40})", line)
        if not match:
            raise AuditError(f"could not parse git cherry output: {line!r}")
        if match.group(1) == "-":
            result.add(match.group(2))
    return result


def patch_equivalent_shas(repo: Path, base_ref: str, release_ref: str) -> set[str]:
    """Return release-branch commits whose patches already exist in the base.

    Minor release branches diverge before the preceding release is tagged. A
    change can therefore occur in both histories under different SHAs after it
    is cherry-picked to the preceding release. ``git cherry`` uses stable patch
    IDs to identify those equivalent commits.
    """
    return parse_patch_equivalent_shas(run_git(repo, "cherry", base_ref, release_ref))


def resolve_sha_prefix(prefix: str, commits: Dict[str, Commit]) -> Optional[str]:
    matches = [sha for sha in commits if sha.startswith(prefix)]
    return matches[0] if len(matches) == 1 else None


def compute_effective_commits(
    commits: Sequence[Commit],
) -> Tuple[List[Commit], List[Commit], List[Commit], List[Tuple[Commit, Commit]]]:
    """Return effective roots, canceled roots, external reverts, and revert pairs.

    A revert whose target predates the comparison range is itself an effective
    release change. It is returned as an external revert for visibility, but it
    remains in the effective set and is not an audit error by itself.
    """
    by_sha = {commit.sha: commit for commit in commits}
    effects: Dict[str, Counter[str]] = {}
    balance: Counter[str] = Counter()
    external_reverts: List[Commit] = []
    revert_pairs: List[Tuple[Commit, Commit]] = []

    for commit in commits:
        match = REVERT_TARGET_RE.search(commit.body)
        target_sha = resolve_sha_prefix(match.group(1), by_sha) if match else None
        if target_sha and target_sha in effects:
            effect = Counter({sha: -count for sha, count in effects[target_sha].items()})
            revert_pairs.append((commit, by_sha[target_sha]))
        else:
            effect = Counter({commit.sha: 1})
            if match:
                external_reverts.append(commit)
        effects[commit.sha] = effect
        balance.update(effect)

    roots = [commit for commit in commits if effects[commit.sha] == Counter({commit.sha: 1})]
    effective = [commit for commit in roots if balance[commit.sha] > 0]
    canceled = [commit for commit in roots if balance[commit.sha] == 0]
    return effective, canceled, external_reverts, revert_pairs


def commit_ids(commit: Commit, repo: Path, cache: Dict[str, CommitIds]) -> CommitIds:
    if commit.sha in cache:
        return cache[commit.sha]

    subject_pr_list = SUBJECT_PR_RE.findall(commit.subject)
    subject_prs = set(subject_pr_list)
    resolved_prs = set(RESOLVED_PR_RE.findall(commit.body))
    aliases = subject_prs | resolved_prs
    canonical = set(resolved_prs)
    if not canonical and subject_pr_list:
        # Revert subjects can mention both the reverted PR and the revert PR.
        # GitHub appends the current PR number last.
        canonical.add(subject_pr_list[-1])

    cherry = CHERRY_PICK_RE.search(commit.body)
    if cherry and not resolved_prs:
        try:
            source = run_git(repo, "show", "-s", "--format=%H%x1f%s%x1f%b", cherry.group(1))
            sha, subject, body = source.split("\x1f", 2)
            source_ids = commit_ids(Commit(sha.strip(), (), subject, body), repo, cache)
            aliases.update(source_ids.alias_prs)
            canonical.update(source_ids.canonical_prs)
        except (AuditError, ValueError):
            pass

    result = CommitIds(frozenset(canonical), frozenset(aliases))
    cache[commit.sha] = result
    return result


def pr_equivalent_shas(
    commits: Sequence[Commit],
    base_commits: Sequence[Commit],
    repo: Path,
    cache: Dict[str, CommitIds],
) -> set[str]:
    """Match commits already shipped in the base by canonical PR identity.

    This supplements patch-ID matching for backports that needed conflict
    resolution or combined several commits into one. Reverts only match other
    reverts, preventing an original change and its backout from being conflated.
    Callers should pass only effective commits so an earlier attempt from the
    same PR that was reverted in the release range is not excluded by mistake.
    """
    base_keys = {
        (pr, bool(REVERT_TARGET_RE.search(commit.body)))
        for commit in base_commits
        for pr in commit_ids(commit, repo, cache).canonical_prs
    }
    return {
        commit.sha
        for commit in commits
        if any(
            (pr, bool(REVERT_TARGET_RE.search(commit.body))) in base_keys
            for pr in commit_ids(commit, repo, cache).canonical_prs
        )
    }


def note_files(version_dir: Path) -> List[Path]:
    files = sorted(version_dir.glob("done/result_*.md"))
    files.extend(sorted(version_dir.glob("todo/result_*.md")))
    for relative in ("miscategorized.md", "cherrypicks.md", "done/cherrypicks.md"):
        path = version_dir / relative
        if path.is_file():
            files.append(path)
    return files


def scan_notes(version_dir: Path, notes_root: Path) -> NoteInventory:
    pr_locations: Dict[str, List[NoteLocation]] = defaultdict(list)
    hash_locations: Dict[str, List[NoteLocation]] = defaultdict(list)
    files = note_files(version_dir)
    if not files:
        raise AuditError(f"no release-note source files found under {version_dir}")

    for path in files:
        relative = str(path.relative_to(notes_root))
        is_cherrypicks = path.name == "cherrypicks.md"
        is_miscategorized = path.name == "miscategorized.md"
        category: Optional[str] = None
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            if is_cherrypicks and line.startswith("## "):
                category = line[3:].strip().lower()
            elif not is_cherrypicks and line.startswith("### "):
                category = line[4:].strip().lower()

            user_facing = not is_miscategorized and category not in NON_USER_FACING
            location = NoteLocation(relative, line_number, category, user_facing)
            for pr in PR_URL_RE.findall(line):
                pr_locations[pr].append(location)
            for token in HEX_TOKEN_RE.findall(line):
                hash_locations[token.lower()].append(location)

    return NoteInventory(dict(pr_locations), dict(hash_locations), [str(p.relative_to(notes_root)) for p in files])


def matching_hashes(sha: str, hashes: Iterable[str]) -> List[str]:
    return sorted(
        prefix for prefix in hashes if sha.startswith(prefix) or prefix.startswith(sha)
    )


def locations_text(locations: Sequence[NoteLocation]) -> str:
    rendered = []
    for location in locations:
        category = f" [{location.category}]" if location.category else ""
        visibility = "user-facing" if location.user_facing else "internal"
        rendered.append(f"{location.path}:{location.line}{category}, {visibility}")
    return "; ".join(rendered)


class Palette:
    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    def paint(self, code: str, value: str) -> str:
        return f"\033[{code}m{value}\033[0m" if self.enabled else value

    def red(self, value: str) -> str:
        return self.paint("31;1", value)

    def green(self, value: str) -> str:
        return self.paint("32;1", value)

    def yellow(self, value: str) -> str:
        return self.paint("33;1", value)

    def cyan(self, value: str) -> str:
        return self.paint("36;1", value)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    script_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", nargs="?", default="2.14.0", help="release-note directory, default: 2.14.0")
    parser.add_argument("--notes-root", type=Path, default=script_root, help="torch-release-notes checkout")
    parser.add_argument("--pytorch-repo", type=Path, default=script_root.parent / "pytorch", help="local pytorch checkout")
    parser.add_argument("--base-ref", help="start ref; default: previous minor release tag")
    parser.add_argument("--release-ref", help="end ref; default: origin/release/X.Y")
    parser.add_argument("--fetch", action="store_true", help="fetch the inferred remote release branch before checking")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="also fail for PR references absent from the selected release range",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--color", choices=("auto", "always", "never"), default="auto")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        version, major, minor, patch = normalize_version(args.version)
        notes_root = args.notes_root.resolve()
        pytorch_repo = args.pytorch_repo.resolve()
        version_dir = notes_root / version
        if not version_dir.is_dir():
            raise AuditError(f"release-note directory does not exist: {version_dir}")
        if not (pytorch_repo / ".git").exists():
            raise AuditError(f"not a git checkout: {pytorch_repo}")

        inferred_base, inferred_release = default_refs(major, minor, patch)
        base_ref = args.base_ref or inferred_base
        release_ref = args.release_ref or inferred_release
        if args.fetch:
            if "/" not in release_ref:
                raise AuditError("--fetch requires a remote-qualified --release-ref such as origin/release/2.14")
            remote, remote_branch = release_ref.split("/", 1)
            run_git(pytorch_repo, "fetch", remote, remote_branch)

        merge_base, release_sha, branch_commits = load_commits(
            pytorch_repo, base_ref, release_ref
        )
        branch_by_sha = {commit.sha: commit for commit in branch_commits}
        patch_equivalents = patch_equivalent_shas(
            pytorch_repo, base_ref, release_ref
        )
        unknown_equivalents = patch_equivalents - set(branch_by_sha)
        if unknown_equivalents:
            raise AuditError(
                "git cherry returned commits outside the comparison range: "
                + ", ".join(sorted(unknown_equivalents))
            )
        patch_unique_commits = [
            commit for commit in branch_commits if commit.sha not in patch_equivalents
        ]
        effective, canceled, external_reverts, revert_pairs = compute_effective_commits(
            patch_unique_commits
        )

        id_cache: Dict[str, CommitIds] = {}
        _, _, base_branch_commits = load_commits(
            pytorch_repo, merge_base, base_ref
        )
        pr_equivalents = pr_equivalent_shas(
            effective, base_branch_commits, pytorch_repo, id_cache
        )
        equivalent_shas = patch_equivalents | pr_equivalents
        base_equivalent = [
            commit for commit in branch_commits if commit.sha in equivalent_shas
        ]
        audit_commits = [
            commit for commit in branch_commits if commit.sha not in equivalent_shas
        ]
        effective = [commit for commit in effective if commit.sha not in pr_equivalents]
        external_reverts = [
            commit for commit in external_reverts if commit.sha not in pr_equivalents
        ]
        notes = scan_notes(version_dir, notes_root)

        active_ids = {commit.sha: commit_ids(commit, pytorch_repo, id_cache) for commit in effective}
        canceled_ids = {commit.sha: commit_ids(commit, pytorch_repo, id_cache) for commit in canceled}
        base_equivalent_ids = {
            commit.sha: commit_ids(commit, pytorch_repo, id_cache)
            for commit in base_equivalent
        }

        active_alias_prs = set().union(*(ids.alias_prs for ids in active_ids.values())) if active_ids else set()
        active_canonical_prs = set().union(*(ids.canonical_prs for ids in active_ids.values())) if active_ids else set()
        canceled_alias_prs = set().union(*(ids.alias_prs for ids in canceled_ids.values())) if canceled_ids else set()
        base_equivalent_alias_prs = (
            set().union(*(ids.alias_prs for ids in base_equivalent_ids.values()))
            if base_equivalent_ids
            else set()
        )
        note_prs = set(notes.prs)
        note_hashes = set(notes.hashes)

        missing = []
        accounted = []
        for commit in effective:
            ids = active_ids[commit.sha]
            matched_prs = sorted(ids.alias_prs & note_prs, key=int)
            matched_hashes = matching_hashes(commit.sha, note_hashes)
            item = {
                "sha": commit.sha,
                "subject": commit.subject,
                "canonical_prs": sorted(ids.canonical_prs, key=int),
                "aliases": sorted(ids.alias_prs, key=int),
            }
            if matched_prs or matched_hashes:
                item["matched_prs"] = matched_prs
                item["matched_hashes"] = matched_hashes
                accounted.append(item)
            else:
                missing.append(item)

        reverted_references = []
        for pr in sorted((note_prs & canceled_alias_prs) - active_alias_prs, key=int):
            locations = notes.prs[pr]
            reverted_references.append(
                {
                    "pr": pr,
                    "user_facing": any(location.user_facing for location in locations),
                    "locations": [location.__dict__ for location in locations],
                }
            )

        base_only_alias_prs = (
            base_equivalent_alias_prs - active_alias_prs - canceled_alias_prs
        )
        base_release_references = []
        for commit in base_equivalent:
            ids = base_equivalent_ids[commit.sha]
            matched_prs = sorted(ids.alias_prs & note_prs & base_only_alias_prs, key=int)
            matched_hashes = matching_hashes(commit.sha, note_hashes)
            if not matched_prs and not matched_hashes:
                continue
            locations = []
            for pr in matched_prs:
                locations.extend(notes.prs[pr])
            for commit_hash in matched_hashes:
                locations.extend(notes.hashes[commit_hash])
            locations = sorted(
                set(locations), key=lambda location: (location.path, location.line)
            )
            base_release_references.append(
                {
                    "sha": commit.sha,
                    "subject": commit.subject,
                    "matched_prs": matched_prs,
                    "matched_hashes": matched_hashes,
                    "user_facing": any(
                        location.user_facing for location in locations
                    ),
                    "locations": [location.__dict__ for location in locations],
                }
            )

        note_only_prs = sorted(
            note_prs
            - active_alias_prs
            - canceled_alias_prs
            - base_equivalent_alias_prs,
            key=int,
        )
        release_only_prs = sorted(active_canonical_prs - note_prs, key=int)
        release_date = run_git(pytorch_repo, "show", "-s", "--format=%cI", release_sha).strip()

        result = {
            "version": version,
            "pytorch_repo": str(pytorch_repo),
            "notes_root": str(notes_root),
            "base_ref": base_ref,
            "merge_base": merge_base,
            "release_ref": release_ref,
            "release_sha": release_sha,
            "release_date": release_date,
            "summary": {
                "branch_commits": len(branch_commits),
                "base_equivalent_commits": len(base_equivalent),
                "patch_equivalent_commits": len(patch_equivalents),
                "pr_equivalent_commits": len(pr_equivalents),
                "audited_commits": len(audit_commits),
                "effective_commits": len(effective),
                "canceled_commits": len(canceled),
                "revert_pairs": len(revert_pairs),
                "external_reverts": len(external_reverts),
                "note_files": len(notes.files),
                "note_prs": len(note_prs),
                "accounted_commits": len(accounted),
                "missing_commits": len(missing),
                "release_only_prs": len(release_only_prs),
                "note_only_prs": len(note_only_prs),
                "reverted_references": len(reverted_references),
                "base_release_references": len(base_release_references),
            },
            "missing_commits": missing,
            "release_only_prs": release_only_prs,
            "base_equivalent_commits": [
                {
                    "sha": commit.sha,
                    "subject": commit.subject,
                    "matched_by": (
                        "patch-id" if commit.sha in patch_equivalents else "pull-request"
                    ),
                }
                for commit in base_equivalent
            ],
            "base_release_references": base_release_references,
            "note_only_prs": [
                {
                    "pr": pr,
                    "locations": [location.__dict__ for location in notes.prs[pr]],
                }
                for pr in note_only_prs
            ],
            "reverted_references": reverted_references,
            "external_reverts": [
                {"sha": commit.sha, "subject": commit.subject} for commit in external_reverts
            ],
        }

        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            use_color = args.color == "always" or (
                args.color == "auto" and sys.stdout.isatty() and "NO_COLOR" not in os.environ
            )
            colors = Palette(use_color)
            print(f"PyTorch {version} release-branch coverage")
            print(f"  range: {base_ref} ({merge_base[:11]}) .. {release_ref} ({release_sha[:11]})")
            print(f"  release ref date: {release_date}")
            print(f"  branch commits since merge-base: {len(branch_commits)}")
            print(
                f"  already present in {base_ref} by patch/PR equivalence: "
                f"{len(base_equivalent)} ({len(patch_equivalents)} patch, "
                f"{len(pr_equivalents)} PR); audited commits: {len(audit_commits)}"
            )
            print(f"  effective after explicit reverts: {len(effective)}")
            print(f"  accounted commits: {len(accounted)}; missing commits: {len(missing)}")
            print(f"  note files: {len(notes.files)}; note PR references: {len(note_prs)}")

            print()
            print(colors.red(f"- RELEASE - NOTES: {len(missing)} effective commits not accounted for"))
            for item in missing:
                prs = ", ".join(f"#{pr}" for pr in item["canonical_prs"] or item["aliases"])
                suffix = f" [{prs}]" if prs else ""
                print(colors.red(f"  - {item['sha'][:11]}{suffix} {item['subject']}"))

            print()
            print(colors.cyan(f"+ NOTES - RELEASE: {len(note_only_prs)} PRs not found in the selected release range"))
            for pr in note_only_prs:
                print(colors.cyan(f"  + #{pr}: {locations_text(notes.prs[pr])}"))

            print()
            print(
                colors.yellow(
                    f"! ALREADY IN {base_ref} BUT REFERENCED: "
                    f"{len(base_release_references)} commits"
                )
            )
            for item in base_release_references:
                marker = "USER-FACING" if item["user_facing"] else "internal"
                identifiers = [f"#{pr}" for pr in item["matched_prs"]]
                identifiers.extend(item["matched_hashes"])
                matched = ", ".join(identifiers)
                locations = [NoteLocation(**location) for location in item["locations"]]
                print(
                    colors.yellow(
                        f"  ! {item['sha'][:11]} [{marker}; {matched}] "
                        f"{item['subject']}: {locations_text(locations)}"
                    )
                )

            print()
            print(colors.yellow(f"! REVERTED BUT REFERENCED: {len(reverted_references)} PRs"))
            for item in reverted_references:
                marker = "USER-FACING" if item["user_facing"] else "internal"
                locations = [NoteLocation(**location) for location in item["locations"]]
                print(colors.yellow(f"  ! #{item['pr']} [{marker}]: {locations_text(locations)}"))

            if external_reverts:
                print()
                print(
                    colors.yellow(
                        f"~ REVERT TARGETS OUTSIDE RANGE: {len(external_reverts)} "
                        "(counted as effective commits)"
                    )
                )
                for commit in external_reverts:
                    print(colors.yellow(f"  ~ {commit.sha[:11]} {commit.subject}"))

            if (
                not missing
                and not reverted_references
                and not base_release_references
                and not note_only_prs
            ):
                print()
                print(colors.green("Coverage sets match."))

        user_facing_reverts = any(item["user_facing"] for item in reverted_references)
        user_facing_base_references = any(
            item["user_facing"] for item in base_release_references
        )
        failed = bool(missing or user_facing_reverts or user_facing_base_references)
        if args.strict:
            failed = failed or bool(note_only_prs)
        return 1 if failed else 0
    except AuditError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
