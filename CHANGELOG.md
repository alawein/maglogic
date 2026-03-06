# Changelog

All notable changes to MagLogic will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.1.0] — 2026-03-06

### Added
- CI test workflow for pull requests
- CLAUDE.md agent guidance
- Test infrastructure and additional test modules
- Workspace standardization (P1-P20)

### Changed
- Consolidated configuration to `pyproject.toml`
- Added AGENTS.md governance rules
- Lazy-loaded heavy dependencies to speed up imports

### Fixed
- Resolved 24 test failures across analysis, parsers, and simulation modules
- Fixed CFL time step in `test_stable_parameters_no_warnings`

---

## [1.0.0] — 2026-01-15

### Added
- Complete MagLogic magnetohydrodynamics framework
- Magnetization analyzer and base parser infrastructure
- Parameter validation utilities
- Professional repository structure and documentation

[Unreleased]: https://github.com/alawein/maglogic/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/alawein/maglogic/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/alawein/maglogic/releases/tag/v1.0.0
