# ci-matrix-demo

A small Python text-utilities library with a GitHub Actions CI workflow
demonstrating matrix testing, dependency caching via uv, pre-commit enforcement,
and artifact handoff between jobs.

## Quick start

```bash
uv sync --extra dev
uv run pytest
```

## What the workflow shows

The workflow (`ci.yml`) has four jobs:

```
pre-commit ──┐
             ├──▶ build-sdist ──▶ verify-sdist
test (8×) ───┘
```

### pre-commit

Runs ruff (lint + format), mypy, and the standard hook set on every push and
pull request. Running this as a separate job rather than inside the matrix means
it executes once — linting the same code eight times adds no signal.

### test (matrix)

Runs pytest across four Python versions (3.11, 3.12, 3.13, 3.14) on
ubuntu-latest and windows-latest — eight parallel jobs.

**Why those Python versions?** The package declares `requires-python = ">=3.11"`,
matching the oldest version in the matrix. Testing the full 3.11–3.14 range
catches regressions across the supported spectrum and gives early warning if a
new Python release introduces a compatibility break.

**Why no macOS?** Since 2025, `macos-latest` runs on Apple Silicon (arm64).
For a pure-Python library with no native extensions, macOS adds no coverage
that Linux doesn't already provide — and costs roughly 10× the runner minutes.

**`fail-fast: false`** — by default GitHub cancels remaining cells when one
fails. Disabling it lets all eight cells run to completion, making it easy to
tell whether a failure is version-specific or OS-specific.

**Artifact upload on failure only** — JUnit XML results are uploaded per cell
only when that cell fails, keeping passing runs artifact-free. Artifact names
include the OS and Python version (`test-results-ubuntu-latest-py3.11`) because
`upload-artifact@v4+` made artifacts immutable per run: two jobs writing the
same name is a hard failure.

### build-sdist

Runs only after `pre-commit` and `test` are both fully green — `needs:
[pre-commit, test]`. Builds a source distribution with `python -m build
--sdist` and uploads it as an artifact.

### verify-sdist

Downloads the artifact from `build-sdist` and inspects it with `tar -tzf`,
asserting that `pyproject.toml` and `src/textutils/core.py` are present inside
the tarball. The build command exiting 0 doesn't guarantee the sdist is
correct — a misconfigured package can produce a tarball that installs a broken
package. This step catches that.

## Why uv

uv replaces pip + virtualenv + pip-compile in one tool. `uv sync` installs the
full locked dependency set in seconds; `uv run` executes commands in the project
virtualenv without activating it. The lockfile (`uv.lock`) is committed so CI
always reproduces the same environment.

## Why `setup-uv@v8.0.0` (exact pin)

Starting with v8, `astral-sh/setup-uv` no longer publishes floating major-version
tags (`@v8`, `@v8.0`). You must pin to an exact release. This was an explicit
upstream decision to push consumers toward reproducible, auditable action
versions — a meaningful supply-chain stance worth understanding when evaluating
third-party actions.
