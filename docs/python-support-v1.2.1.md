# Python support validation for v1.2.1

Issue #14 validates the modernized dependency resolution on standard CPython
3.11, 3.12, 3.13, and 3.14. The package continues to declare
`requires-python = ">=3.11"` and now advertises each tested version with a PyPI
classifier.

## CI evidence

The test matrix runs the complete 216-test suite on all four versions. This
includes production-STDIO integration coverage that discovers and exercises all
20 tools, 5 prompts, and 5 resources under both the current and legacy MCP
protocol initialization paths.

Separate artifact jobs cover the oldest and newest supported interpreters,
Python 3.11 and 3.14. Each job:

1. builds both the wheel and source distribution;
2. installs each artifact into its own empty virtual environment;
3. changes to a directory outside the source checkout;
4. verifies installed version metadata and server construction; and
5. performs a calculation using the ephemeris bundled in the artifact.

Formatting, linting, and type checking run once on Python 3.11 instead of being
duplicated across the matrix.

## Dependency compatibility

The universal `uv.lock` resolves successfully for every tested interpreter.
Notably, the astronomy resolution selects NumPy 2.4.6 on Python 3.11 and NumPy
2.5.1 on Python 3.12–3.14, while Ephem 4.2.1 supplies standard CPython wheels
through Python 3.14. No package blocks the supported matrix.

Python 3.14 free-threaded builds are explicitly deferred because this patch
tests only standard CPython builds. Unreleased Python versions are not
advertised.
