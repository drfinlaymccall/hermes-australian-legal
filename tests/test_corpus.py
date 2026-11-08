"""Fictional fixture only: no legislation or real-corpus dependency."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from au_legal import corpus


SLUG = "fictional-paperclip-rules-2099"
FIRST = "# Fictional rule 1\nImaginary paperclips are purple.\n"
SECOND = "# Fictional rule 1\nImaginary paperclips are green.\n"


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fictional-au-corpus-", dir=os.environ.get("TMPDIR"))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = {
            "PATH": os.defpath, "LANG": "C", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_AUTHOR_NAME": "Fictional Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
            "GIT_COMMITTER_NAME": "Fictional Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            "GIT_AUTHOR_DATE": "2099-01-01T12:00:00+00:00",
            "GIT_COMMITTER_DATE": "2099-01-01T12:00:00+00:00",
        }
        self.git("init", "-q")
        self.meta = {
            "corpus": "fictional/test-only", "name": "Fictional paperclip fixture — NOT LAW",
            "history_from": "2099-01-01", "record_to": "2099-06-30", "checked_on": "2099-07-01",
            "record_note": "Fictional derived copy. Only compilation days are represented.",
            "scope": {"when_absent": "Absence of fictional scope notes proves nothing."},
            "instruments": [{"folder": SLUG, "name": "Fictional Paperclip Rules 2099",
                             "register_id": "F2099L99999", "no_gaps_from": "2099-01-01",
                             "excluded_compilations": []}],
        }
        self.folder = self.root / "corpus" / SLUG
        self.folder.mkdir(parents=True)
        (self.folder / "s-001.md").write_text(FIRST, encoding="utf-8")
        (self.folder / "part-2").mkdir()
        (self.folder / "part-2" / "div-1.md").write_text("# Fictional division\nNot real law.\n", encoding="utf-8")
        self.commit_metadata()
        self.first_commit = self.git("rev-parse", "HEAD").strip()
        self.git("tag", SLUG + "/2099-01-01")
        (self.folder / "s-001.md").write_text(SECOND, encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "Fictional amendment\n\nIn-force: 2099-03-01\nCompilation: 2\nCompilation-id: F2099C99999\nKind: Amend")
        self.second_commit = self.git("rev-parse", "HEAD").strip()
        self.git("tag", "-a", SLUG + "/2099-03-01", "-m", "Fictional annotated compilation")
        # A future tag must not be treated as coverage after record_to.
        self.git("tag", SLUG + "/2099-12-01")

    def git(self, *args):
        return subprocess.run(
            ["git", "-c", "core.hooksPath=" + os.devnull, "-c", "core.fsmonitor=false", "-C", str(self.root), *args],
            env=self.env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, timeout=10,
        ).stdout

    def commit_metadata(self):
        (self.root / "corpus.json").write_text(json.dumps(self.meta), encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "Fictional fixture metadata")

    def query(self, filename="s-001.md", day="2099-04-01", instrument=SLUG):
        return corpus.provision(self.root, instrument, filename, day)

    def fingerprint(self):
        # Include .git objects, index, refs and config, not just tracked worktree files.
        out = {}
        for path in self.root.rglob("*"):
            key = path.relative_to(self.root).as_posix()
            if path.is_symlink():
                out[key] = ("symlink", os.readlink(path))
            elif path.is_file():
                out[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        return out

    def test_status_is_json_and_discloses_no_local_path(self):
        result = corpus.status(self.root)
        self.assertEqual(result["corpus_commit"], self.second_commit)
        self.assertEqual(result["metadata"], self.meta)
        self.assertEqual(result["instrument_slugs"], [SLUG])
        self.assertEqual(result["checked_on"], "2099-07-01")
        self.assertEqual(result["record_to"], "2099-06-30")
        self.assertTrue(result["caveats"])
        self.assertNotIn(str(self.root), json.dumps(result))

    def test_latest_tag_exact_text_full_commits_and_provenance(self):
        result = self.query()
        self.assertEqual(result["text"], SECOND)
        self.assertEqual(result["compilation_tag"], SLUG + "/2099-03-01")
        self.assertEqual(result["compilation_commit"], self.second_commit)
        self.assertEqual(result["corpus_commit"], self.second_commit)
        self.assertEqual(result["query_date"], "2099-04-01")
        self.assertEqual(result["last_change"]["commit"], self.second_commit)
        self.assertEqual(result["last_change"]["compilation_id"], "F2099C99999")
        self.assertEqual(result["source"]["register_id"], "F2099L99999")
        self.assertEqual(result["source"]["url"], "https://www.legislation.gov.au/F2099L99999")
        self.assertIn(self.meta["record_note"], result["caveats"])
        self.assertIn(self.meta["scope"]["when_absent"], result["caveats"])
        self.assertFalse(result["truncated"])
        json.dumps(result)

    def test_earlier_compilation_and_tag_boundary(self):
        self.assertEqual(self.query(day="2099-02-28")["text"], FIRST)
        self.assertEqual(self.query(day="2099-03-01")["text"], SECOND)
        self.assertEqual(self.query(day="2099-01-01")["compilation_commit"], self.first_commit)
        self.assertEqual(self.query(day="2099-06-30")["text"], SECOND)

    def test_nested_safe_filename(self):
        result = self.query(filename="part-2/div-1.md")
        self.assertEqual(result["text"], "# Fictional division\nNot real law.\n")

    def test_invalid_provision_paths(self):
        for value in ("../corpus.json", "/etc/passwd", "s-001.md:HEAD", "HEAD:s-001.md", "-s.md",
                      "part-2/../s-001.md", "part-2//div-1.md", "./s-001.md", "part-2/-bad.md",
                      "s-001.md\n", "s-001.md\x00", "C:\\s-001.md", "part-2\\div-1.md",
                      "s-001.txt", "", None, ["s-001.md"], "a/" * 20 + "b.md"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.query(filename=value)

    def test_only_exact_known_instrument_slug(self):
        for value in ("fictional", "F2099L99999", SLUG.upper(), "../" + SLUG, "--all", "HEAD", None, []):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.query(instrument=value)

    def test_strict_real_dates(self):
        for day in ("20990401", "2099-02-29", "2099-04-31", "0000-01-01", "2099-4-01",
                    "2099-04-01junk", "2099-04-01\n", " 2099-04-01", "2099-04-01T00:00:00",
                    "２０９９-０４-０１", "--all", "", None, 20990401):
            with self.subTest(day=day), self.assertRaises(ValueError):
                self.query(day=day)

    def test_record_boundaries_and_future_tags(self):
        for day in ("2098-12-31", "2099-07-01", "2099-12-01"):
            with self.subTest(day=day), self.assertRaises(ValueError):
                self.query(day=day)

    def test_dates_before_instrument_first_tag(self):
        self.git("tag", "-d", SLUG + "/2099-01-01")
        with self.assertRaises(ValueError):
            self.query(day="2099-02-01")

    def test_gap_period_is_blocked_not_presented_as_complete(self):
        self.meta["instruments"][0]["no_gaps_from"] = "2099-03-01"
        self.meta["instruments"][0]["excluded_compilations"] = ["2099-02-01"]
        self.commit_metadata()
        with self.assertRaisesRegex(ValueError, "gap|continuous"):
            self.query(day="2099-02-15")
        self.assertEqual(self.query(day="2099-03-01")["text"], SECOND)
        self.assertTrue(any("gap" in note.lower() for note in corpus.status(self.root)["caveats"]))

    def test_missing_and_invalid_critical_metadata(self):
        original = json.loads(json.dumps(self.meta))
        cases = [("record_to", None), ("record_to", "20990630"), ("checked_on", "2099-02-30"),
                 ("history_from", "2099-07-01"), ("instruments", []), ("record_note", "")]
        for key, value in cases:
            with self.subTest(key=key, value=value):
                self.meta = json.loads(json.dumps(original))
                if value is None:
                    del self.meta[key]
                else:
                    self.meta[key] = value
                self.commit_metadata()
                with self.assertRaises(ValueError):
                    self.query()
                with self.assertRaises(ValueError):
                    corpus.status(self.root)
        self.meta = original

    def test_invalid_instrument_metadata(self):
        for key, value in (("no_gaps_from", None), ("no_gaps_from", "2099-02-29"),
                           ("no_gaps_from", "2100-01-01"), ("register_id", "../bad"),
                           ("folder", "../bad"), ("excluded_compilations", ["2099-02-30"])):
            with self.subTest(key=key, value=value):
                original = dict(self.meta["instruments"][0])
                self.meta["instruments"][0][key] = value
                self.commit_metadata()
                with self.assertRaises(ValueError):
                    corpus.status(self.root)
                self.meta["instruments"][0] = original

    def test_uncommitted_metadata_is_not_trusted(self):
        (self.root / "corpus.json").write_text("not JSON", encoding="utf-8")
        self.assertEqual(corpus.status(self.root)["metadata"], self.meta)
        self.assertEqual(self.query()["text"], SECOND)

    def test_metadata_must_exist_as_regular_committed_file(self):
        self.git("rm", "-q", "corpus.json")
        self.git("commit", "-qm", "Remove fictional metadata")
        (self.root / "corpus.json").write_text(json.dumps(self.meta), encoding="utf-8")
        with self.assertRaises(ValueError):
            corpus.status(self.root)

    def test_invalid_json_and_duplicate_keys_are_blocked(self):
        for data in ("{}", "{broken", '{"record_to":"2099-06-30","record_to":"2100-01-01"}',
                     '{"other":NaN}'):
            with self.subTest(data=data):
                (self.root / "corpus.json").write_text(data, encoding="utf-8")
                self.git("add", "corpus.json")
                self.git("commit", "-qm", "Invalid fictional metadata")
                with self.assertRaises(ValueError):
                    corpus.status(self.root)

    def test_missing_empty_and_oversize_text_are_blocked(self):
        with self.assertRaises(ValueError):
            self.query(filename="missing.md")
        for text in ("", " \n\t", "x" * (corpus.MAX_TEXT_BYTES + 1)):
            with self.subTest(length=len(text)):
                (self.folder / "s-001.md").write_text(text, encoding="utf-8")
                self.git("add", ".")
                self.git("commit", "-qm", "Fictional invalid text")
                self.git("tag", "-f", SLUG + "/2099-03-01")
                with self.assertRaises(ValueError):
                    self.query()

    def test_worktree_and_git_symlinks_are_rejected(self):
        target = self.folder / "s-001.md"
        target.unlink()
        target.symlink_to("../../corpus.json")
        with self.assertRaises(ValueError):
            self.query()
        self.git("add", ".")
        self.git("commit", "-qm", "Fictional symlink")
        self.git("tag", "-f", SLUG + "/2099-03-01")
        target.unlink()  # Committed symlinks must fail even with no worktree symlink.
        with self.assertRaises(ValueError):
            self.query()

    def test_worktree_directory_symlink_is_rejected(self):
        nested = self.folder / "part-2"
        (nested / "div-1.md").unlink()
        nested.rmdir()
        nested.symlink_to(self.root)
        with self.assertRaises(ValueError):
            self.query(filename="part-2/div-1.md")

    def test_malformed_tag_date_is_not_a_revision_argument(self):
        self.git("tag", SLUG + "/2099-02-30")
        with self.assertRaises(ValueError):
            self.query()

    def test_environment_injection_is_removed_and_not_mutated(self):
        hostile = {"GIT_DIR": "/does/not/exist", "GIT_WORK_TREE": "/does/not/exist",
                   "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "alias.show",
                   "GIT_CONFIG_VALUE_0": "!false", "GIT_CONFIG_GLOBAL": "/does/not/exist",
                   "GIT_EXTERNAL_DIFF": "false", "GIT_CONFIG_PARAMETERS": "broken"}
        with mock.patch.dict(os.environ, hostile):
            before = dict(os.environ)
            self.assertEqual(self.query()["text"], SECOND)
            self.assertEqual(dict(os.environ), before)

    def test_git_global_configs_and_hooks_are_disabled(self):
        marker = self.root / "executed-marker"
        hooks = self.root / "evil-hooks"
        hooks.mkdir()
        hook = hooks / "post-checkout"
        hook.write_text("#!/bin/sh\ntouch " + str(marker) + "\n", encoding="utf-8")
        hook.chmod(0o755)
        self.git("config", "core.hooksPath", str(hooks))
        self.git("config", "core.fsmonitor", "touch " + str(marker))
        self.assertEqual(self.query()["text"], SECOND)
        self.assertFalse(marker.exists())

    def test_all_reads_leave_complete_tree_and_git_database_unchanged(self):
        before = self.fingerprint()
        corpus.status(self.root)
        self.query()
        self.query(day="2099-02-01")
        with self.assertRaises(ValueError):
            self.query(filename="../bad.md")
        self.assertEqual(self.fingerprint(), before)

    def test_invalid_repository_errors_do_not_leak_path(self):
        for path in (self.root / "missing", self.folder, "", None, []):
            with self.subTest(path=path), self.assertRaises(ValueError) as raised:
                corpus.status(path)
            self.assertNotIn(str(self.root), str(raised.exception))

    def test_output_limit_and_timeout_fail_closed(self):
        # Exercise the real bounded subprocess primitive with native Git, not corpus code.
        with self.assertRaisesRegex(ValueError, "limit|bounded"):
            corpus._git(self.root, ["show", "HEAD:corpus.json"], limit=8)
        with mock.patch.object(corpus, "GIT_TIMEOUT_SECONDS", 0):
            with self.assertRaisesRegex(ValueError, "timed out|timeout"):
                corpus.status(self.root)

    def test_last_change_failure_is_flagged_without_dropping_caveats(self):
        actual = corpus._git

        def no_log(root, args, **kwargs):
            if args[0] == "log":
                raise ValueError("Git history unavailable")
            return actual(root, args, **kwargs)

        with mock.patch.object(corpus, "_git", side_effect=no_log):
            result = self.query()
        self.assertIsNone(result["last_change"])
        self.assertIn(self.meta["record_note"], result["caveats"])
        self.assertTrue(any("last-change" in note.lower() for note in result["caveats"]))


if __name__ == "__main__":
    unittest.main()
