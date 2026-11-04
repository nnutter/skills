---
name: pr-stack
description: Wrap up a finished feature branch as review-ready pull requests. Squash trial-and-error commits, split refactors away from features and fixes, prove that every commit passes the repository checks, then open the changes as 1 GitHub stack with `gh stack`, with 1 release-note title per pull request and no body. Use when a branch is ready to hand off, when history contains trial and error, when 1 branch must become several pull requests, or when release notes are built from pull request titles.
---

# Prepare a PR stack

Use this skill to turn a finished branch into pull requests.

GitHub builds release notes from the titles of merged pull requests.
Each pull request MUST therefore carry exactly 1 user-facing change, and its title MUST read as 1 release-note line.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

[RFC2119]: https://www.rfc-editor.org/rfc/rfc2119
[RFC8174]: https://www.rfc-editor.org/rfc/rfc8174

## Requirements

Check these before you change anything.
If 1 of them is missing, stop and report it.
Do not rewrite history to work around a missing requirement.

- A feature branch and a known base branch, such as its upstream or the default branch.
- A clean working tree.
- Permission to rewrite history, to push branches, and to open pull requests.
- The repository check commands.
  The `go-template` baseline provides `mise run check` and `mise run test`.
- A remote that accepts `git push`, and an authenticated `gh` with the `stack` extension.
  `gh stack --help` MUST succeed.
  When it does not, stop and report it.
  Do not build the stack by hand with `gh pr create`.
- No review session in progress.
  `timber review status --is-reviewing --json` reports 1.

## Vocabulary

- Base branch: the branch that the stack starts from.
- Group: the commits that 1 pull request contains.
- PR stack: a GitHub stack, as the `gh stack` extension creates it.
  It is an ordered set of pull requests, where each 1 is based on the branch of the pull request below it.
- Trial and error: a commit that repairs work from an earlier commit on the same branch.

## 1. Record the state

Read the branch before you change it:

```sh
base=$(git merge-base HEAD <base-branch>)
git log --reverse --format='%h %s' "$base"..HEAD
git diff --name-status "$base" HEAD
```

Keep a backup ref until the user asks you to delete it:

```sh
git update-ref refs/agents/<session-id>/backup HEAD
```

Do not create a backup branch in `refs/heads/`.
Report the ref name in the final report.

## 2. Classify every commit

Read the diff of each commit.
The subject can be wrong, so do not classify from the subject alone.

Each commit MUST be exactly 1 of these kinds:

- Trial and error.
  The commit repairs an earlier commit on the branch: work in progress, "fix tests", "try again", or an incomplete part of earlier work.
  These commits MUST be squashed into the commit they repair, and they MUST NOT reach the stack.
- Refactoring.
  The commit changes the structure of the code and does not change behavior that a user can see.
  A refactoring subject MUST carry the `Refactor:` prefix.
  A commit MUST contain 1 kind of refactoring only.
- User-facing feature or fix.
  The commit changes behavior, output, or a public interface.
- Support.
  The commit adds tests, documentation, build steps, or configuration for a change that the user can see.

### Keep refactors out of feature and fix commits

A commit MUST NOT mix a refactoring with a feature or a fix.
This skill follows the refactoring rules of the project `AGENTS.md`: 1 commit shows 1 logical change, and 1 commit contains 1 kind of refactoring.
Read the project `AGENTS.md` when it exists and apply its rules as well.

If a commit contains both, split it before you build the groups:

1. Mark it with `edit` in an interactive rebase from its parent.
1. Run `git reset HEAD^` to unstage the whole change.
   The files keep their content.
1. Run `git add -p` and stage the refactoring only.
1. Commit the refactoring with a `Refactor:` prefix in its subject.
1. Stage the remaining change and commit it with the original subject.
1. Continue the rebase.

Preserve the trailers of the original commit, such as `Change-Id:`.
Use the `fracture` skill when it is available.
The 2 commits together MUST reproduce the patch of the original commit.

Apply the same rule to 2 different refactorings in 1 commit, and to a feature and an unrelated fix in 1 commit.

## 3. Build the groups

Walk the commits from oldest to newest and put each 1 in a group.

- A user-facing feature or fix opens a new group, unless it continues the work of the current group.
- A refactoring or a support commit joins the group of the change that it supports.
  A refactoring that prepares a change sits before that change in the same group.
- A trial-and-error commit joins the commit that it repairs, and thereby the group of that commit.

A group MUST contain at least 1 user-facing change, because the group becomes 1 release note.
A group SHOULD NOT contain 2 unrelated user-facing changes.
Split such a group into 2 stacked pull requests.

Prefer a small number of groups.
1 pull request is correct when the branch carries 1 user-facing change.

Order the groups so that each 1 depends only on the groups before it.

## 4. Propose the plan

Report a table with these columns: group, current commits, final commits, branch name, pull request title, base branch.

Also report:

- each commit to squash and the commit that receives it;
- each commit to split, and the 2 commits that replace it;
- each commit to drop because it becomes empty;
- any user-facing change that has no group.

Stop and wait for approval before you rewrite history.

## 5. Squash and split

Squash trial and error with `fixup` actions, which keep the message and the `Change-Id` of the target commit:

```sh
GIT_SEQUENCE_EDITOR='sed -i.bak -e "s/^pick <repair-sha>/fixup <repair-sha>/"' \
  git rebase -i --no-autosquash --empty=drop "$base"
```

Repeat 1 `sed` expression for each trial-and-error commit, or mark the commits with `git commit --fixup=<target>` first and use `--autosquash`.
`fixup` keeps 1 `Change-Id` per commit; `squash` and a copied message can leave more than 1.

Do not reword a commit unless the plan says so.
Do not change the content of a commit in this step; step 6 repairs failures.

The rewritten history MUST have the same content as the backup:

```sh
git diff "$(git rev-parse refs/agents/<session-id>/backup)" HEAD
```

This command MUST print nothing.

## 6. Verify every commit

Run the repository checks at every commit, not only at the tip:

```sh
scripts/check-history.sh "$base" HEAD -- 'mise run check && mise run test'
```

The script gives each commit a fresh worktree, runs the command, stops at the first failure, and removes the worktree.
It reports each commit on stderr and `OK: <n> commit(s) passed` on stdout.
Use `--keep` to keep the worktree of a failed commit for debugging.

A scratch worktree is a new path, so `mise` can refuse its configuration.
Set `MISE_TRUSTED_CONFIG_PATHS` or run `mise trust` in that path.

When a commit fails, repair that commit instead of adding a later commit that repairs it:

1. Run `git commit --fixup=<failed-commit>` with the fix.
1. Run `git rebase -i --autosquash "$base"` to fold the fix into the failed commit.
1. Run the check script again for the whole range.

A later repair leaves a commit in the history that does not pass its own checks.

## 7. Build the stack

Create 1 branch for each group, in order from the bottom of the stack.
The branch of a group points at the last commit of that group.

```sh
git branch --no-track "<feature>/1-<slug>" "<commit-1>"
git branch --no-track "<feature>/2-<slug>" "<commit-2>"
```

Use 2 to 4 words of the pull request title as the `<slug>`, in lower case and separated by `-`.
`--no-track` stops a stack branch from taking the base branch as its upstream before the stack tool sets the upstream.

Register the branches as 1 stack, from bottom to top:

```sh
gh stack init --base "<base-branch>" "<feature>/1-<slug>" "<feature>/2-<slug>"
```

`gh stack init` adopts the existing branches.
The first branch is based on the base branch, and each later branch is based on the branch below it.
Keep the local feature branch at the final commit.
The feature branch is not part of the stack, so do not push it.

## 8. Submit the stack

Push the branches and open the pull requests with 1 command:

```sh
gh stack submit --auto --open
```

`gh stack submit` pushes all branches atomically, opens 1 pull request for each branch, sets the base branch of each pull request, and links the pull requests into 1 GitHub stack.
`--auto` skips the interactive editor, which an agent cannot use.
`--open` marks the new pull requests as ready for review.

Then set the title of each pull request, and leave the body empty:

```sh
gh pr edit "<feature>/1-<slug>" --title "<title>" --body ""
```

The title becomes 1 release note line, so write it for the user:

- 1 user-facing change in 1 line, in the imperative mood, such as `Add a retry to the upload task`.
- 72 characters or fewer.
- No `WIP`, no `Refactor:` prefix, and no internal term that a user of the product cannot read.
- The title names the change, not the files.

Set no body.
`--body ""` clears any body that `gh stack submit` generates.
The stack carries the order of the pull requests, so the body does not need to repeat it.

## 9. Report

Report a table with these columns: pull request URL, title, base branch, head branch, commits.
Read the stack with `gh stack view --json` and `gh stack view --short`.

Also report:

- the backup ref;
- the result of the check script;
- the groups that you did not create, and why.

## After a merge

Keep the stack correct with `gh stack`:

```sh
gh stack sync
```

`gh stack sync` fetches, rebases each branch onto the branch below it, pushes the branches, and syncs the pull requests.
Merge a stack only when the user asks:

```sh
gh stack merge
```

## Constraints

- Rewrite history, push, and open pull requests only after the user approves the plan.
  `gh stack submit` pushes the branches and opens the pull requests, so it needs that approval too.
- Use `--force-with-lease`.
  Do not force-push a branch that you did not create, and do not force-push the base branch at any time.
- Do not commit an empty change.
- Do not leave a trial-and-error commit, a mixed refactor and feature commit, or a commit that fails the checks.
- When a remote branch of the same name exists, fetch it and compare it first.
  Report any commit that you did not review.

## Verification

Check the result before you report it:

- `git diff "$(git rev-parse refs/agents/<session-id>/backup)" HEAD` prints nothing.
- `git log --oneline "$base"..HEAD` shows only the planned commits, and each refactoring subject carries the `Refactor:` prefix.
- No commit contains both a refactoring and a feature or fix.
- Each commit message holds at most 1 `Change-Id:` trailer.
- Each stack branch points at the last commit of its group, and the local feature branch points at the final commit.
- `scripts/check-history.sh` reports `OK` for the whole range.
- `gh stack view --short` lists the branches in the planned order.
- Each pull request shows the planned base branch: `gh pr view <number> --json baseRefName`.
- Each pull request title reads as 1 release-note line, and its body is empty: `gh pr view <number> --json title,body`.
