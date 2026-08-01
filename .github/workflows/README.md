# GitHub Actions Workflows

## ci.yaml - Continuous Integration Workflow

This workflow runs code quality checks and tests on every pull request and push to main/develop branches.

### Workflow Jobs

1. **Lockfile and Vulnerability Validation** (runs first)
   - Confirms `pyproject.toml` and `uv.lock` are consistent
   - Installs without changing the lockfile
   - Audits the complete frozen dependency graph

2. **Code Quality Checks** (runs after dependency validation)
   - Black formatting validation
   - Ruff lint and import-sorting validation
   - Ruff linting
   - Mypy type checking

All subsequent uv installs and tool runs are also frozen.

3. **Test Matrix** (runs in parallel after quality checks)
   - Runs the full unit and integration suite on standard CPython 3.11–3.14
   - Validates all 20 tools, 5 prompts, and 5 resources on every version
   - Generates and uploads coverage once, from Python 3.11

4. **Built Artifact Tests** (runs in parallel after quality checks)
   - Builds both the wheel and source distribution
   - Installs each artifact in an isolated environment on Python 3.11 and 3.14
   - Smoke-tests version metadata, server construction, and bundled ephemeris
     access from outside the repository

### Triggers

- **Pull Requests** to `main` or `develop` branches
- **Direct pushes** to `main` or `develop` branches

### Usage

No setup required - the workflow runs automatically when:
- You create a pull request targeting main/develop
- You push commits to main/develop branches

All PR checks must pass before the PR can be merged (if branch protection is enabled).

`dependency-review.yaml` runs only for pull requests and rejects newly
introduced vulnerable dependencies. Dependabot policy and repository security
settings are documented in [`docs/dependency-automation.md`](../../docs/dependency-automation.md).

## publish.yaml - PyPI Publishing Workflow

This workflow automatically publishes the package to PyPI when a new GitHub release is created.

### Workflow Steps

1. **Code Quality Checks** (runs first)
   - Black formatting validation
   - Ruff lint and import-sorting validation
   - Ruff linting
   - Mypy type checking

2. **Test Suite** (runs after quality checks pass)
   - Comprehensive MCP server tests (20 tools, 5 prompts, and 5 resources)
   - Unit tests with pytest
   - Code coverage reporting

3. **Publish to PyPI** (runs after all tests pass)
   - Builds the package with `uv build`
   - Verifies package contents
   - Publishes to PyPI

### Setup Instructions

#### Option 1: Trusted Publisher (Recommended - No tokens needed)

1. Go to https://pypi.org/manage/account/publishing/
2. Add a new pending publisher with these details:
   - **PyPI Project Name**: `lunar-mcp-server`
   - **Owner**: `AngusHsu`
   - **Repository**: `lunar-mcp-server`
   - **Workflow name**: `publish.yaml`
   - **Environment name**: `pypi`

3. The workflow is already configured for Trusted Publishers (no changes needed)

#### Option 2: API Token (Alternative)

1. Generate a PyPI API token:
   - Go to https://pypi.org/manage/account/token/
   - Create a new token with scope limited to `lunar-mcp-server` project

2. Add the token to GitHub repository secrets:
   - Go to repository Settings → Secrets and variables → Actions
   - Create a new secret named `PYPI_API_TOKEN`
   - Paste the PyPI token value

3. Update `.github/workflows/publish.yaml`:
   - Comment out the trusted publisher publish step
   - Uncomment the token-based publish step

#### Optional: Code Coverage (Codecov)

If you want code coverage reporting:

1. Sign up at https://codecov.io with your GitHub account
2. Add the repository to Codecov
3. Get the upload token from Codecov
4. Add to GitHub secrets as `CODECOV_TOKEN`

### Triggering the Workflow

The workflow triggers automatically when you publish a GitHub release:

```bash
# Create and push a tag
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0

# Then create a release on GitHub:
# 1. Go to https://github.com/AngusHsu/lunar-mcp-server/releases/new
# 2. Select the tag v0.2.0
# 3. Add release notes (copy from CHANGELOG.md)
# 4. Click "Publish release"

# The workflow will automatically:
# - Run quality checks
# - Run tests
# - Publish to PyPI if all pass
```

### Manual Testing

You can test the workflow without publishing by creating a test release or running individual steps locally:

```bash
# Test quality checks
uv run black --check src/ tests/
uv run ruff check src/ tests/
uv run mypy src/

# Test MCP server
./scripts/test_mcp_final.sh

# Test unit tests
uv run pytest --cov

# Test build
uv build
```

### Troubleshooting

**Issue**: Quality checks fail
- **Solution**: Run `uv run black src/ tests/` and `uv run ruff check --fix src/ tests/`

**Issue**: Tests fail
- **Solution**: Run `./scripts/test_mcp_final.sh` locally to debug

**Issue**: PyPI publish fails with 403 error
- **Solution**: Check that Trusted Publisher is configured correctly or API token is valid

**Issue**: Package already exists on PyPI
- **Solution**: Bump version in `pyproject.toml` and create a new release

### Version Workflow

1. Update the version once in `pyproject.toml`, the canonical version source.
2. Run `uv lock` so the local package entry in `uv.lock` matches it.
3. Update `CHANGELOG.md` with the same version entry.
4. Run the version tests; the package and MCP initialization response derive
   their version from installed distribution metadata and must match.
5. Commit the changes and create the matching `vX.Y.Z` tag.
6. Create the GitHub release; the workflow publishes that tagged version to
   PyPI.
