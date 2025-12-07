# Changelog

All notable changes to this project will be documented in this file.  
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]
### Added
- (placeholder)

### Changed
- (placeholder)

### Fixed
- (placeholder)

---

## [0.1.0] – 2025-12-08
### Added
- **AI-assisted table analysis**
  - New `--ai` flag for `sqtab analyze <table>`
  - Custom analysis tasks via `--task`
  - Custom analysis rules via `--rule`
  - Load tasks/rules from files:  
    - `--tasks-file`
    - `--rules-file`
  - Prompt templates under `prompts/`
  - Markdown-formatted schema & sample rendering
- **Improved CSV import**
  - UTF-8 BOM detection and handling
  - Improved type inference (column-based)
- **Environment features**
  - `.env` loading via `python-dotenv`

### Changed
- Cleaner default README presentation
- Refactored Analyzer module:
  - Structured output (`schema`, `row_count`, `samples`)
  - Better separation of prompt formatting
- Improved database reset logic with safer file operations

### Fixed
- Missing schema and sample rows in AI prompts
- `UnicodeDecodeError` on CSV files saved in UTF-16 or with BOM
- Stability improvements for `sqtab analyze` under edge cases

---

## [0.0.1] – 2025-12-07
### Added
- Initial implementation of the `sqtab` CLI
- CSV and JSON import with automatic column normalization
- Table inspection:
  - `sqtab tables`
  - `sqtab tables --schema`
  - `sqtab analyze <table>`
  - `sqtab info`
- SQL execution:
  - `sqtab sql "<query>"`
- Export:
  - `sqtab export <table> output.csv`
- Database reset:
  - `sqtab reset`
  - `sqtab reset --hard`
- Rich CLI output formatting

---
