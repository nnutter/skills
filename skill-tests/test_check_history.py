#!/usr/bin/env python3
"""Behavioral checks for the pr-stack per-commit check script."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "pr-stack" / "scripts" / "check-history.sh"


class CheckHistoryTest(unittest.TestCase):
	def setUp(self) -> None:
		tmp = tempfile.TemporaryDirectory()
		self.addCleanup(tmp.cleanup)
		self.root = Path(tmp.name)
		self.repo = self.root / "repo"
		self.repo.mkdir()
		self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
		self.git("init", "-q")
		self.git("config", "user.name", "Test")
		self.git("config", "user.email", "test@example.invalid")

	def git(self, *args: str) -> subprocess.CompletedProcess[str]:
		return self.command("git", *args)

	def command(self, *args: str) -> subprocess.CompletedProcess[str]:
		result = subprocess.run(args, cwd=self.repo, env=self.env, text=True,
		                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
		self.assertEqual(result.returncode, 0, f"{args!r}\n{result.stdout}\n{result.stderr}")
		return result

	def commit(self, name: str) -> str:
		(self.repo / name).write_text(f"{name}\n")
		self.git("add", name)
		# A global hook manager would run against this fixture.
		self.git("-c", "core.hooksPath=/dev/null", "commit", "-qm", f"Add {name}")
		return self.repo_head()

	def remove(self, name: str) -> str:
		self.git("rm", "-q", name)
		self.git("-c", "core.hooksPath=/dev/null", "commit", "-qm", f"Remove {name}")
		return self.repo_head()

	def repo_head(self) -> str:
		return self.git("rev-parse", "HEAD").stdout.strip()

	def check_history(self, *args: str) -> subprocess.CompletedProcess[str]:
		return subprocess.run([str(SCRIPT), *args], cwd=self.repo, env=self.env, text=True,
		                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)

	def worktrees(self) -> list[str]:
		lines = self.git("worktree", "list", "--porcelain").stdout.splitlines()
		return [line.removeprefix("worktree ") for line in lines if line.startswith("worktree ")]

	def test_runs_the_command_at_every_commit_in_order(self) -> None:
		commits = [self.commit(name) for name in ("a.txt", "b.txt", "c.txt")]
		log = self.root / "log"
		result = self.check_history("HEAD~2", "HEAD", "--", f"git rev-parse HEAD >> {log}")
		self.assertEqual(result.returncode, 0, result.stderr)
		# The range starts above the base commit, so the first commit is absent.
		self.assertEqual(log.read_text().split(), commits[1:])
		self.assertIn("OK: 2 commit(s) passed", result.stdout)

	def test_reports_the_first_failing_commit_and_restores_the_checkout(self) -> None:
		self.commit("a.txt")
		commits = [self.remove("a.txt"), self.commit("c.txt")]
		head = self.repo_head()
		log = self.root / "log"
		result = self.check_history("HEAD~2", "HEAD", "--", f"git rev-parse HEAD >> {log}; test -f a.txt")
		self.assertEqual(result.returncode, 1, result.stderr)
		self.assertIn(f"FAILED: {commits[0][:12]} Remove a.txt", result.stderr)
		# The failing commit stops the run before the next commit.
		self.assertEqual(log.read_text().split(), [commits[0]])
		self.assertEqual(self.repo_head(), head)
		self.assertEqual(self.worktrees(), [str(self.repo)])

	def test_keep_leaves_the_worktree_of_the_failed_commit(self) -> None:
		self.commit("a.txt")
		self.commit("b.txt")
		result = self.check_history("--keep", "HEAD~1", "HEAD", "--", "test -f missing.txt")
		self.assertEqual(result.returncode, 1, result.stderr)
		kept = [line.removeprefix("kept: ") for line in result.stderr.splitlines() if line.startswith("kept: ")]
		self.assertEqual(len(kept), 1, result.stderr)
		self.assertTrue(Path(kept[0]).is_dir())
		self.assertIn(kept[0], self.worktrees())
		self.git("worktree", "remove", "--force", kept[0])
		shutil.rmtree(kept[0], ignore_errors=True)

	def test_usage_error_names_the_usage(self) -> None:
		result = self.check_history()
		self.assertEqual(result.returncode, 2)
		self.assertIn("Usage: check-history.sh", result.stderr)

	def test_empty_range_is_an_error(self) -> None:
		self.commit("a.txt")
		result = self.check_history("HEAD", "HEAD")
		self.assertEqual(result.returncode, 2)
		self.assertIn("no commits in", result.stderr)


if __name__ == "__main__":
	unittest.main()
