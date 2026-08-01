# v1.2.1 dependency baseline

This document records the clean-checkout dependency baseline for Issue #10. It
is an inventory only: no dependency or lockfile versions are changed here.

## Environment

- Date: 2026-08-01
- Platform: macOS 14.8.4, arm64
- Python: CPython 3.11.15 (uv-managed)
- uv: 0.12.1
- Base commit: `6614c9d` (`main`)

The previously installed uv 0.7.11 did not provide `uv audit`; the baseline was
therefore run with uv 0.12.1, the current release on the audit date.

## Required command results

| Command | Result | Notes |
| --- | --- | --- |
| `uv lock --check` | Failed | uv reports that `uv.lock` needs an update. The lockfile was intentionally not rewritten in this audit-only issue. |
| `uv sync --frozen` | Passed | Installed the existing 68-package resolution without changing `uv.lock`. |
| `uv tree` | Passed | Confirmed duplicate dev-extra/dev-group tool declarations and the duplicate dev-group `mcp` declaration. |
| `uv audit --frozen` | Failed | 50 advisories across 11 packages; no adverse project statuses. Runtime-only audit found 37 advisories across 6 packages. |
| `uv run black --check src tests` | Passed | 18 files unchanged. |
| `uv run isort --check src tests` | Passed | No import-order changes required. |
| `uv run ruff check src tests` | Passed | All checks passed. |
| `uv run mypy src` | Passed | No issues in 9 source files. |
| `uv run pytest` | Passed | 182 tests passed; 5 MCP resource-return deprecation warnings; 78% total coverage. |
| `./scripts/test_mcp_final.sh` | Failed | Exit 127 before startup because the script requires GNU `timeout`, which is not available by default on macOS. This portability issue should be removed when #11 replaces shell-only protocol coverage. |

The failing lock, audit, and portable MCP checks are baseline findings, not
regressions introduced by this issue.

## Runtime dependencies

Targets are the newest stable releases visible on PyPI on 2026-08-01 unless a
release-specific constraint is stated. They remain proposals until their
dedicated issue validates behavior and Python 3.11 compatibility.

| Package | Declared constraint | Locked | Proposed target | Owner | Risk and notes |
| --- | --- | ---: | ---: | --- | --- |
| `mcp` | `>=1.0.0` | 1.15.0 | `>=1.28.1,<2` | #11 | High protocol/security risk. Six advisories affect the locked release. The `<2` ceiling prevents an accidental SDK v2 migration. |
| `skyfield` | `>=1.48` | 1.53 | 1.54 | #12 | Calculation-sensitive; validate phase boundaries and ephemeris behavior. |
| `ephem` | `>=4.1.5` | 4.2 | 4.2.1 | #12 | Calculation-sensitive; imported as an optional astronomy backend. |
| `astropy` | `>=6.0.0` | 7.1.0 | 8.0.1 | #12 | High transitive/calculation risk. No source import was found, so #12 should prove it is needed or remove it. |
| `lunardate` | `>=0.2.2` | 0.2.2 | 0.3.0 | #18 | Calendar-output risk, especially leap months and supported date ranges. |
| `zhdate` | `>=0.1` | 0.1 | 1.0 | #18 | Major-version jump and calendar-output risk; requires independent golden-fixture validation. |
| `chinese-calendar` | `>=1.9.0` | 1.10.0 | 1.11.0 | #18 | Festival/holiday dataset changes may alter results. |
| `python-dateutil` | `>=2.8.2` | 2.9.0.post0 | retain 2.9.0.post0 | #20 | Already current. No direct source import was found; prove direct use or remove. |
| `pytz` | `>=2023.3` | 2025.2 | 2026.3.post1 | #20 | Date/time behavior risk. No direct source import was found; `zoneinfo` migration remains out of scope. |
| `pydantic` | `>=2.5.0` | 2.11.9 | 2.13.4 | #20 | MCP schema compatibility risk. No direct source import was found; currently also supplied transitively by MCP. |
| `typing-extensions` | `>=4.8.0` | 4.15.0 | 4.16.0 | #20 | Low runtime risk. No direct source import was found; prove direct use or remove. |

### #20 implementation outcome

The core-utility review found no source or test imports of `python-dateutil`,
`pytz`, `pydantic`, or `typing-extensions`. All four direct requirements were
removed rather than publishing dependencies the application does not use.

- `python-dateutil` 2.9.0.post0 and `pytz` 2025.2 leave the resolution entirely.
- Pydantic remains a required MCP SDK transitive and is upgraded to 2.13.4,
  with Pydantic Core 2.46.4 and `typing-inspection` 0.4.2.
- `typing-extensions` remains a shared transitive and is upgraded to 4.16.0.
- The existing date parsing, timezone-offset, MCP schema, frozen-install, and
  clean-artifact integration tests provide the removal evidence.

## Development and build dependencies

The project currently publishes a `dev` extra and also defines a uv `dev`
dependency group. Their minimum versions conflict, and the uv group additionally
duplicates the runtime `mcp` dependency.

| Package | Published dev extra | uv dev group | Locked | Proposed disposition/target | Owner |
| --- | --- | --- | ---: | --- | --- |
| `black` | `>=23.0.0` | `>=25.9.0` | 25.9.0 | 26.5.1 | #13 |
| `isort` | `>=5.12.0` | `>=6.0.1` | 6.0.1 | Remove if Ruff becomes the import-sorting source of truth; otherwise 8.0.1 | #13 |
| `mypy` | `>=1.6.0` | `>=1.18.2` | 1.18.2 | 2.3.0 | #13 |
| `pre-commit` | `>=3.5.0` | `>=4.3.0` | 4.3.0 | 4.6.1 | #13 |
| `pytest` | `>=7.4.0` | `>=8.4.2` | 8.4.2 | 9.1.1 | #13 |
| `pytest-asyncio` | `>=0.21.0` | `>=1.2.0` | 1.2.0 | 1.4.0 | #13 |
| `pytest-cov` | `>=4.1.0` | `>=7.0.0` | 7.0.0 | 7.1.0 | #13 |
| `ruff` | `>=0.1.0` | `>=0.13.2` | 0.13.2 | 0.16.1 | #13 |
| `mcp` | none (runtime dependency applies) | `>=1.15.0` | 1.15.0 | Remove duplicate; #11 owns the runtime constraint | #11/#13 |
| `hatchling` | build requirement | n/a | build-isolated | 1.31.0 | #13 |

#13 should choose one contributor dependency model. The preferred baseline
direction is uv-first (`[dependency-groups].dev`) because CI and contributor
commands already use `uv sync --dev`. If the published extra is retained, it
must be generated or kept intentionally identical.

Ruff already enables `I` rules while CI separately runs isort. Unless #13 finds
an uncovered behavior, Ruff should become the single import-sorting source of
truth and isort should be removed.

### #13 implementation outcome

- Adopted the uv-first model and removed the conflicting published `dev` extra.
- Upgraded the retained tools to Black 26.5.1, mypy 2.3.0, pre-commit 4.6.1,
  pytest 9.1.1, pytest-asyncio 1.4.0, pytest-cov 7.1.0, and Ruff 0.16.1.
- Upgraded the build backend requirement to Hatchling 1.31.0.
- Made Ruff the single lint/import-sorting source of truth and removed isort.
- Added local pre-commit hooks that invoke the same uv-managed Black, Ruff, and
  mypy tools used by contributors and CI.

## Vulnerability baseline

`uv audit --frozen` reported 50 advisory records. Some CVEs appear under both
GHSA and PYSEC identifiers, so this is an advisory count rather than a count of
unique defects.

| Package | Locked | Advisory records | Fixed-version direction | Classification |
| --- | ---: | ---: | --- | --- |
| `mcp` | 1.15.0 | 6 | 1.28.1 or newer v1 | Runtime; #11 release blocker |
| `python-multipart` | 0.0.20 | 14 | 0.0.31 or newer | MCP transitive runtime; #11 |
| `starlette` | 0.48.0 | 12 | 1.3.1 or newer | MCP transitive runtime; #11 |
| `click` | 8.3.0 | 1 | 8.3.3 or newer | MCP transitive runtime; #11 |
| `idna` | 3.10 | 2 | 3.15 or newer | MCP transitive runtime; #11 |
| `python-dotenv` | 1.1.1 | 2 | 1.2.2 or newer | MCP transitive runtime; #11 |
| `black` | 25.9.0 | 3 | 26.3.1 or newer | Development; #13 |
| `pytest` | 8.4.2 | 2 | 9.0.3 or newer | Development; #13 |
| `pygments` | 2.19.2 | 2 | 2.20.0 or newer | Development transitive; #13 |
| `filelock` | 3.19.1 | 4 | 3.20.3 or newer | Development transitive; #13 |
| `virtualenv` | 20.34.0 | 2 | 20.36.1 or newer | Development transitive; #13 |

No vulnerability exception is proposed. All known fixable findings remain
release-blocking until the owning issue upgrades or removes the affected
dependency and `uv audit --frozen` passes.

## Risk groups and issue ownership

1. **Version metadata — #19:** remove the hardcoded runtime version before SDK
   integration work so later installed-artifact tests have one source of truth.
2. **MCP protocol/runtime — #11:** upgrade MCP and only required transitives;
   replace shell/`grep`-only checks with supported Python client integration.
3. **Core runtime utilities — #20:** validate Pydantic and date/time behavior
   against the selected MCP v1 release; remove unused direct requirements only
   with import and artifact evidence.
4. **Development/build tooling — #13:** consolidate duplicate declarations,
   resolve Ruff/isort overlap, remediate dev-only vulnerabilities, and validate
   Hatchling builds.
5. **Chinese calendar — #18:** isolate upgrades and preserve conversion,
   festival, zodiac, sexagenary-cycle, leap-month, and BaZi fixtures.
6. **Astronomy — #12:** isolate upgrades and preserve astronomical results
   within documented tolerances; verify offline ephemeris behavior.
7. **Compatibility and automation — #14/#15:** test the selected resolution on
   Python 3.11–3.14, then enforce frozen lock and audit checks continuously.

## Baseline conclusions

- Do not perform an unrestricted lockfile refresh. The current lock is stale
  according to uv 0.12.1 and contains many vulnerable transitives, so each
  owning issue must use targeted upgrades and review the resulting diff.
- Preserve Python 3.11 and STDIO-only production transport.
- Do not rewrite calculation fixtures merely to accommodate new dependency
  output.
- The duplicate dev declarations, duplicate MCP declaration, unused-direct
  candidates, shell portability failure, five MCP deprecation warnings, and
  vulnerability set are explicitly assigned to follow-up issues above.
