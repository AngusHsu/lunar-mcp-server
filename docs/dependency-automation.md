# Dependency automation

The repository uses Dependabot's native `uv` ecosystem to update
`pyproject.toml` and `uv.lock` together. GitHub Actions are monitored by a
separate ecosystem entry.

## Schedule and pull-request limits

- uv checks run weekly on Monday at 09:00 `Asia/Taipei`, with at most 10 open
  version-update pull requests.
- GitHub Actions checks run weekly on Monday at 09:30 `Asia/Taipei`, with at
  most 5 open version-update pull requests.
- uv pull requests receive the `dependencies` label. Actions pull requests also
  receive `github-actions`.
- Automatic merging is intentionally disabled. Every update receives the same
  CI and review as a human-authored pull request.

## Grouping policy

Only patch and minor updates are grouped. Major updates remain individual.

- `mcp` is excluded from all groups so SDK and protocol changes are reviewed in
  isolation.
- Core runtime utilities, astronomy packages, and Chinese calendar packages use
  distinct groups.
- Development-tool patch/minor updates can share one pull request.
- GitHub Actions patch/minor updates can share one pull request.

Required transitive lockfile changes travel with the applicable direct update.
An update must not combine MCP, core runtime, astronomy, and Chinese calendar
domains merely to make dependency resolution easier.

## Pull-request gates

The first CI job runs these commands before quality, compatibility, or artifact
jobs:

```bash
uv lock --check
uv sync --frozen
uv audit --frozen
```

All later project installs and `uv run` commands are frozen, so CI cannot repair
or rewrite an inconsistent lockfile. The complete test matrix continues to run
on Python 3.11–3.14, including the production STDIO MCP integration suite, and
artifact jobs continue to clean-install the wheel and sdist on Python 3.11 and
3.14.

A pull-request-only dependency-review workflow rejects any newly introduced
known vulnerability. `uv audit` separately audits the complete locked graph.
There is no advisory allow-list; an exception would require a documented change
reviewed in a pull request.

## Repository settings

Dependabot alerts and Dependabot security updates are enabled in repository
settings. The public repository's dependency graph enables GitHub dependency
review. Maintainers can verify these settings under **Settings → Code security**.

The configuration is validated after it reaches the default branch by checking
the Dependabot update log or the first generated update pull request. If GitHub
reports a configuration error, dependency automation is not considered healthy
until that error is corrected.
