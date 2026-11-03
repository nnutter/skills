#!/usr/bin/env bash
# Run a check command at every commit in a range, each in a scratch worktree.
set -euo pipefail

readonly DEFAULT_COMMAND='mise run check && mise run test'

usage() {
  cat >&2 <<'EOF'
Usage: check-history.sh [-k|--keep] <base> [<tip>] [-- <command>]

Run <command> with sh -c at every commit in <base>..<tip> and stop at the
first commit that fails. Each commit gets a fresh worktree, so a build
artifact from 1 commit cannot hide a failure in the next one.

The default command is: mise run check && mise run test

Options:
  -k, --keep   Keep the worktree of the failed commit and print its path.
  -h, --help   Show this message.

Exit status: 0 when every commit passes, 1 when a commit fails, 2 for a
usage error.
EOF
}

keep=0
while (($# > 0)); do
  case $1 in
    -k | --keep)
      keep=1
      shift
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      printf 'check-history.sh: unknown option: %s\n' "$1" >&2
      usage
      exit 2
      ;;
    *) break ;;
  esac
done

if (($# == 0)); then
  usage
  exit 2
fi
base=$1
shift

tip=HEAD
if (($# > 0)) && [[ $1 != -- ]]; then
  tip=$1
  shift
fi
if (($# > 0)) && [[ $1 == -- ]]; then
  shift
fi
check_command=$DEFAULT_COMMAND
if (($# > 0)); then
  check_command=$*
fi

# Git's rebase environment can redirect commands away from the worktree.
while IFS='=' read -r name _; do
  case $name in GIT_*) unset "$name" ;; esac
done < <(env)

for rev in "$base" "$tip"; do
  if ! git rev-parse --verify --quiet "$rev^{commit}" >/dev/null; then
    printf 'check-history.sh: not a commit: %s\n' "$rev" >&2
    exit 2
  fi
done
base=$(git rev-parse --verify "$base^{commit}")
tip=$(git rev-parse --verify "$tip^{commit}")

if [[ $(git rev-list --count "$base".."$tip") == 0 ]]; then
  printf 'check-history.sh: no commits in %s..%s\n' "${base:0:12}" "${tip:0:12}" >&2
  exit 2
fi

scratch=$(mktemp -d)
tree=$scratch/tree

cleanup() {
  if [[ -d $tree ]]; then
    if ((keep)); then
      printf 'kept: %s\n' "$tree" >&2
    else
      git worktree remove --force "$tree" >/dev/null 2>&1 || true
    fi
  fi
  if ((!keep)); then
    rm -rf -- "$scratch"
  fi
}
trap cleanup EXIT

git worktree add --detach --quiet "$tree" "$base"

total=0
while IFS= read -r commit; do
  total=$((total + 1))
  subject=$(git log -1 --format=%s "$commit")
  printf '\n=== %s %s\n' "${commit:0:12}" "$subject" >&2
  # A check can change files, so reset the worktree and remove ignored output
  # before the next commit.
  git -C "$tree" checkout --detach --quiet --force "$commit"
  git -C "$tree" clean -xdffq
  if ! (cd "$tree" && sh -c "$check_command"); then
    printf '\nFAILED: %s %s\n' "${commit:0:12}" "$subject" >&2
    exit 1
  fi
done < <(git rev-list --reverse "$base".."$tip")

printf '\nOK: %d commit(s) passed in %s..%s\n' "$total" "${base:0:12}" "${tip:0:12}"
