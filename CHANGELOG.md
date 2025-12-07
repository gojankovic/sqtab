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

## [0.2.0] – 2025-12-08
### Added
- **AI-powered SQL generation**
  - New command: `sqtab sql-ai "<question>"`
  - Converts natural-language requests into valid SQLite SQL.
  - Integrated schema-awareness to prevent hallucinated columns/tables.
  - Automatic SQL cleaning (removal of markdown fences, hints, text noise).

- **Configurable AI model**
  - New environment variable: `SQTAB_AI_MODEL`
  - Users can override default model (`gpt-4o-mini`) locally.
  - CLI now prints which model is being used for transparency.

- **Improved README**
  - Documented new AI features.
  - Added section on environment-based model selection.
  - Clearer installation & quick start overview.

### Changed
- Refactored AI pipeline to use centralized model selection (`get_ai_model()`).
- Improved SQL cleaning logic for more consistent results.
- Enhanced internal schema export for AI prompts.

### Fixed
- Cleaned wheel packaging:
  - Removed accidental venv-related files from distributions.
  - Ensured correct package discovery via `tool.setuptools.packages.find`.

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
