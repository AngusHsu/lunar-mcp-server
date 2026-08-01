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

The sole version exclusion is `zhdate` 1.0. PyPI advertises that release, but
its published metadata is not resolvable by uv; the initial native-uv update
run demonstrated the failure. This is not a vulnerability exception: `uv audit`
still audits `zhdate` 0.1 and the rest of the complete graph. The exclusion can
be removed when upstream publishes an installable successor.

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

The initial default-branch update ran both configured ecosystems. GitHub Actions
opened independently reviewable major-update pull requests. The uv run opened a
separate MCP 2.0 pull request, which was reviewed and deferred because MCP v2 is
outside the v1.2.1 patch scope, and exposed the invalid `zhdate` 1.0 metadata.
The exact unusable release is now excluded so subsequent uv runs can complete;
any future configuration error must likewise be corrected rather than ignored.
