import tempfile
import unittest
from pathlib import Path

from scripts.check_release_branch_coverage import (
    Commit,
    commit_ids,
    compute_effective_commits,
    normalize_version,
    parse_patch_equivalent_shas,
    pr_equivalent_shas,
    scan_notes,
)


class CheckReleaseBranchCoverageTest(unittest.TestCase):
    def test_normalize_version(self):
        self.assertEqual(normalize_version("2.14"), ("2.14.0", 2, 14, 0))
        self.assertEqual(normalize_version("2.14.1"), ("2.14.1", 2, 14, 1))

    def test_parse_patch_equivalent_shas(self):
        base_equivalent = "a" * 40
        release_only = "b" * 40
        output = f"- {base_equivalent}\n+ {release_only}\n"

        self.assertEqual(parse_patch_equivalent_shas(output), {base_equivalent})

    def test_pr_equivalence_handles_combined_backport_and_revert_polarity(self):
        first = Commit("a" * 40, (), "First change (#100)", "")
        second = Commit("b" * 40, (), "Second change (#101)", "")
        revert = Commit(
            "c" * 40,
            (),
            'Revert "First change (#100)" (#102)',
            f"This reverts commit {first.sha}.\n"
            "Pull Request resolved: https://github.com/pytorch/pytorch/pull/102\n",
        )
        combined_backport = Commit(
            "d" * 40,
            (),
            "Backport two changes (#200)",
            "Pull Request resolved: https://github.com/pytorch/pytorch/pull/100\n"
            "Pull Request resolved: https://github.com/pytorch/pytorch/pull/101\n",
        )
        base_original = Commit(
            "e" * 40,
            (),
            "Backport first change (#201)",
            "Pull Request resolved: https://github.com/pytorch/pytorch/pull/102\n",
        )

        equivalents = pr_equivalent_shas(
            [first, second, revert],
            [combined_backport, base_original],
            Path("."),
            {},
        )

        self.assertEqual(equivalents, {first.sha, second.sha})

    def test_revert_and_revert_of_revert(self):
        original = Commit("a" * 40, (), "Feature (#100)", "")
        revert = Commit(
            "b" * 40,
            (),
            'Revert "Feature (#100)" (#101)',
            f"This reverts commit {original.sha}.",
        )
        restore = Commit(
            "c" * 40,
            (),
            'Revert "Revert feature" (#102)',
            f"This reverts commit {revert.sha}.",
        )

        effective, canceled, external, pairs = compute_effective_commits(
            [original, revert]
        )
        self.assertEqual(effective, [])
        self.assertEqual(canceled, [original])
        self.assertEqual(external, [])
        self.assertEqual(len(pairs), 1)

        effective, canceled, external, pairs = compute_effective_commits(
            [original, revert, restore]
        )
        self.assertEqual(effective, [original])
        self.assertEqual(canceled, [])
        self.assertEqual(external, [])
        self.assertEqual(len(pairs), 2)

    def test_revert_of_commit_before_range_is_an_effective_change(self):
        revert = Commit(
            "b" * 40,
            (),
            'Revert "Earlier feature (#100)"',
            f"This reverts commit {'a' * 40}.",
        )

        effective, canceled, external, pairs = compute_effective_commits([revert])

        self.assertEqual(effective, [revert])
        self.assertEqual(canceled, [])
        self.assertEqual(external, [revert])
        self.assertEqual(pairs, [])

    def test_cherry_pick_uses_resolved_trunk_pr(self):
        commit = Commit(
            "d" * 40,
            (),
            "Release branch fix (#200)",
            "Pull Request resolved: https://github.com/pytorch/pytorch/pull/150\n",
        )
        ids = commit_ids(commit, Path("."), {})
        self.assertEqual(ids.canonical_prs, frozenset({"150"}))
        self.assertEqual(ids.alias_prs, frozenset({"150", "200"}))

    def test_revert_subject_uses_last_pr_as_canonical(self):
        commit = Commit(
            "e" * 40,
            (),
            'Revert "Feature (#100)" (#101)',
            "",
        )

        ids = commit_ids(commit, Path("."), {})

        self.assertEqual(ids.canonical_prs, frozenset({"101"}))
        self.assertEqual(ids.alias_prs, frozenset({"100", "101"}))

    def test_scan_notes_tracks_visibility_and_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            version_dir = root / "2.14.0"
            done = version_dir / "done"
            done.mkdir(parents=True)
            (done / "result_cuda.md").write_text(
                "## cuda\n"
                "### bug fixes\n"
                "- Fix a bug ([#123](https://github.com/pytorch/pytorch/pull/123))\n"
                "### not user facing\n"
                "- Internal changes (abcdef12345, 12345678901)\n"
            )
            inventory = scan_notes(version_dir, root)
            self.assertTrue(inventory.prs["123"][0].user_facing)
            self.assertFalse(inventory.hashes["abcdef12345"][0].user_facing)
            self.assertFalse(inventory.hashes["12345678901"][0].user_facing)


if __name__ == "__main__":
    unittest.main()
