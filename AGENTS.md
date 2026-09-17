# AGENTS.md

Instructions for AI coding agents (and the humans directing them) contributing to PlantCV.
This file is the canonical source; if you're reading this via `CLAUDE.md` or another
tool-specific pointer file, treat it as identical to this document.

Human contributors should read `CONTRIBUTING.md` (https://docs.plantcv.org/CONTRIBUTING/,
also mirrored under `docs/`) — this file is a condensed, agent-oriented supplement to that
guide, not a replacement for it. Where the two conflict, `CONTRIBUTING.md` and a maintainer's
direct instruction win.

## What PlantCV is

PlantCV is an open-source Python package for image-based plant phenotyping, co-developed
by the Donald Danforth Plant Science Center and a broader community. It is used directly
in published research pipelines, so correctness and reproducibility matter more than in a
typical application: a silent change in output values (a mask, a measurement, a threshold)
is worse than a loud crash, because it can propagate into someone's dataset undetected.
Keep that asymmetry in mind — prefer raising an error to guessing, and never "fix" a test
by loosening its assertion instead of understanding why it failed.

## Required workflow: issue first, always

**Do not open a pull request without a linked, assigned issue.** This applies equally to
human-authored and agent-authored PRs. The flow is:

1. **Find or file an issue.**
   - Search open issues first: https://github.com/danforthcenter/plantcv/issues
   - If an existing open issue covers the work, comment on it to volunteer.
   - If none exists, open a new issue describing the bug or proposed feature clearly
     enough for a maintainer to evaluate scope before code is written.
2. **Wait to be assigned.** Do not start implementation, and do not open a PR, until a
   maintainer has assigned the issue to you (or to the account/agent acting on your
   behalf). This is a hard gate, not a formality — unsolicited PRs against unassigned
   issues, or with no issue at all, will be closed and re-requested through this process.
3. **Reference the issue in the PR.** Once assigned, open your PR against the correct
   base branch (see below) and include `Closes #<issue-number>` (or `Refs #<issue-number>`
   if it doesn't fully resolve it) in the description.

## Attribution: co-authored-by is required

Every commit or PR with agent-generated contributions must include a
`Co-authored-by:` trailer identifying the agent, in addition to the human directing it.
For example:

```
Co-authored-by: <agent-name> <agent-identifier>
```

This applies whether the agent wrote the whole PR or just a meaningful part of it. Don't
drop this to make a contribution look fully human-authored — reviewers rely on it to
calibrate scrutiny, and PRs missing it when agent involvement is evident may be sent back.

If you are an agent operating autonomously (e.g., picking up work proactively rather than
at a human's explicit direction), this means your very first action on a task must be
checking issue status — not writing code. If no assignment exists yet, stop and surface
that to the person you're working with rather than proceeding.

## Which branch to work from

PlantCV maintains two active lines of development:

- **`main`** — the current stable line. Most bug fixes and incremental features target this.
- **`v5.0`** — an active development branch where new features are being staged ahead of
  the next major release. **Check `v5.0` in addition to `main`** before starting work:
  a feature, refactor, or fix relevant to your issue may already exist there, be in
  progress there, or supersede the approach you'd otherwise take against `main`.

Before writing code:
- Check both branches for existing work related to your assigned issue (open PRs, recent
  commits, TODO markers).
- If the issue is about new functionality that conceptually belongs with what's being
  staged for the next major version, ask (in the issue thread) whether the target branch
  should be `v5.0` rather than `main` — don't assume.
- Never merge or rebase across `main` and `v5.0` on your own judgment call; branch topology
  between a stable line and a staged major release is a maintainer decision.

## Environment setup

- Create a fresh environment (conda/mamba recommended) and install the project's declared
  dependencies from `environment.yml`.
- Install PlantCV in editable mode from the repo root (`pip install -e .` or the equivalent
  per `pyproject.toml`) so code changes are picked up without reinstalling.
- Confirm the import works and the test suite collects before making changes:
  a broken environment produces confusing failures that look like your code's fault.

## Running tests

Run the full suite with coverage before opening (or updating) a PR:

```
py.test --cov=plantcv --cov-report=term-missing
```

This reports pass/fail as well as which lines are not covered. **PlantCV maintains 100%
test coverage, and PRs are expected to maintain it** — check the `term-missing` output for
any line you touched or added, and write tests until nothing you introduced is listed as
missing. A PR that drops coverage should be treated as incomplete, not ready for review.

## Making changes

- **Every new or changed function needs tests.** PlantCV's test suite (`tests/`) is the
  primary safety net for a package with heavy numerical/image-processing logic, and the
  project's 100% coverage bar (see "Running tests" above) means this isn't optional. A PR
  that adds functionality without corresponding tests should be treated as incomplete, not
  ready for review.
- **Follow existing module conventions.** New analysis functions are namespaced under
  `plantcv.plantcv.<module>` following the patterns already present in the `plantcv/`
  directory — match the argument style, docstring format (numpy-style), and return-value
  conventions of neighboring functions rather than inventing a new pattern.
- **Run linting before opening a PR.** This repo uses DeepSource for code quality checks
  in CI; run your local linter/formatter and resolve warnings on any lines you touch
  rather than leaving them for CI to catch.
- **Update documentation alongside code.** If you add or change a user-facing function,
  add or update its corresponding page under `docs/` (the docs site is built with MkDocs;
  see `mkdocs.yml` for the nav structure) — a function without a docs page is not
  considered complete.
- **Do not modify** release/version metadata, CI workflow files (`.github/`), or the
  license without an explicit maintainer instruction in the issue thread — these are
  maintainer-controlled regardless of what the code change otherwise touches.

## Before opening the PR

Run through this checklist:

- [ ] Issue exists, is linked, and is assigned to you.
- [ ] PR targets the correct branch (`main` or `v5.0` — confirmed, not assumed).
- [ ] New/changed behavior has tests, and `py.test --cov=plantcv --cov-report=term-missing`
      passes locally with no new lines reported as missing coverage.
- [ ] Linter has been run and warnings on touched lines are resolved.
- [ ] Docs updated for any user-facing change.
- [ ] Commit/PR includes a `Co-authored-by:` trailer for the agent, if applicable.
- [ ] PR description explains *why*, not just *what*, and references the issue number.

## A note on scope

Keep PRs scoped to the assigned issue. Agents in particular tend to "helpfully" fix
adjacent things they notice along the way (a typo two functions over, an unrelated
refactor) — don't. File a separate issue for anything out of scope and let a maintainer
triage it; bundling unrelated changes makes review slower and harder to reason about,
which works against the goal of making agent contributions genuinely useful rather than
just numerous.
