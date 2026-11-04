#!/usr/bin/env python3
"""Behavior of the PR stack branch name script."""

import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "pr-stack" / "scripts" / "stack-branch-names"


def git_environment() -> dict[str, str]:
	# A hook or an agent session can redirect Git away from the test repository.
	return {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}


class StackBranchNamesTest(unittest.TestCase):
	def setUp(self) -> None:
		self.tmp = tempfile.TemporaryDirectory()
		self.addCleanup(self.tmp.cleanup)
		self.project = Path(self.tmp.name)
		self.run_git("init", "-q")
		self.run_git("commit", "-q", "--allow-empty", "-m", "Base")

	def run_git(self, *args: str) -> subprocess.CompletedProcess[str]:
		result = subprocess.run(("git", *args), cwd=self.project, env=git_environment(), text=True,
		                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
		self.assertEqual(result.returncode, 0, result.stdout)
		return result

	def names(self, *args: str, cwd: Path | None = None, seed: str | None = None,
	          check: bool = True) -> list[str]:
		env = git_environment()
		if seed is not None:
			env["STACK_NAMES_SEED"] = seed
		result = subprocess.run((str(SCRIPT), *args), cwd=cwd or self.project, env=env, text=True,
		                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
		if check:
			self.assertEqual(result.returncode, 0, result.stderr)
		return result.stdout.splitlines()

	def test_prints_one_name_per_group_below_the_top(self) -> None:
		for count in (1, 2, 5):
			with self.subTest(count=count):
				names = self.names("foo", str(count))
				self.assertEqual(len(names), count)

	def test_names_the_top_group_never_appears(self) -> None:
		for name in self.names("foo", "10"):
			self.assertRegex(name, r"^foo-[a-z]{2,10}-[a-z]{2,10}$")

	def test_names_are_unique(self) -> None:
		names = self.names("foo", "40")
		self.assertEqual(len(set(names)), len(names))

	def test_seed_repeats_the_same_names(self) -> None:
		self.assertEqual(self.names("foo", "3", seed="7"), self.names("foo", "3", seed="7"))

	def test_skips_a_name_that_a_branch_already_has(self) -> None:
		taken = self.names("foo", "3", seed="7")
		self.run_git("branch", taken[0])
		self.run_git("update-ref", f"refs/remotes/origin/{taken[1]}", "HEAD")
		for name in self.names("foo", "3", seed="7"):
			self.assertNotIn(name, taken[:2])

	def test_zero_groups_below_the_top_prints_nothing(self) -> None:
		self.assertEqual(self.names("foo", "0"), [])

	def test_rejects_a_count_that_is_not_a_number(self) -> None:
		with self.assertRaises(AssertionError):
			self.names("foo", "two")

	def test_reports_a_directory_that_is_not_a_repository(self) -> None:
		# A directory outside the test repository, since Git finds a parent repository.
		outside = tempfile.TemporaryDirectory()
		self.addCleanup(outside.cleanup)
		result = subprocess.run((str(SCRIPT), "foo", "1"), cwd=outside.name, env=git_environment(),
		                        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
		self.assertEqual(result.returncode, 2)
		self.assertIn("not a git repository", result.stderr)


if __name__ == "__main__":
	unittest.main()
