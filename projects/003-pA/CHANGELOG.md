# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-04-24

### Added

- Initial release of RecallKit: single-operator LoRA SFT decision loop
- `pars sft start` — run full baseline → LoRA SFT → eval pipeline with mandatory 3-section report
- `pars sft resume` — cross-session resume with machine fingerprint verification (C22)
- `pars sft retry --from --hypothesis` — reproducible retry inheriting parent run config with hyperparam override
- `pars compare runA runB` — explicit verdict comparison between two runs; no intuition allowed
- `pars unlock` — clear stuck_lock after human review
- USD / wall-clock / GPU hour budget enforcement with 60 s-interval SIGINT safety net
- API key isolation via LiteLLM proxy with USD pre-reject middleware (C20)
- `.claude/` fail-closed read-only mount (C21, macOS bindfs or Linux chattr)
- Command deny-list hooks per SLA §1.4 security envelope
- Failure attribution schema (Pydantic v2) with LLM-resistant quality gate
- MIT License (D19)
- CI workflow: ruff lint + format + pytest fast suite + coverage ≥ 70% (GitHub Actions)
- Monthly pip-audit scan for CVE detection (supply chain, R5)
- License-check workflow: GPL-family rejection + artifact hygiene grep (compliance §4.4.3)

### Known Limitations

- `truly_stuck` timing fires at ~t=905 s vs spec §8.3 "cold_start 300 s + idle 900 s = 1200 s"
  nominal boundary (KNOWN_DEVIATION; does not affect O7 unit-test scene coverage)
- Cross-machine resume disabled by machine fingerprint hard-reject (C22 — by design)
- GPU artifacts (checkpoints, .pt files) require manual rsync per `docs/h200-rsync-playbook.md`
- CI `uv sync --frozen` on ubuntu-latest may fail if CUDA wheels are unavailable at build time;
  use `--no-install-project` fallback if needed (documented in `.github/workflows/ci.yml`)

[Unreleased]: https://github.com/<operator>/RecallKit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/<operator>/RecallKit/releases/tag/v0.1.0
