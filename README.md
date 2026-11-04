# Skills

Agent skills for repository tooling, branch wrap-up, and pull requests.

## Use

```sh
npx skills add nnutter/skills --skill go-template
npx skills add nnutter/skills --skill pr-stack
```

## Skills

| Skill | Use it to |
| --- | --- |
| [`go-template`](skills/go-template/SKILL.md) | Set up or standardize the tools, mise tasks, Git hooks, and CI of a Go repository. |
| [`pr-stack`](skills/pr-stack/SKILL.md) | Wrap up a branch: squash trial and error, keep refactors apart from features, check every commit, and open a PR stack. |

## Develop

```sh
mise run check
mise run test
# Uses a disposable repository and downloads Go tool dependencies.
mise run test-integration
```

The requirements in `go-template` apply to target Go repositories, not to this repository.
