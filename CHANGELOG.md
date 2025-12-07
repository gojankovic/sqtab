# Changelog

All notable changes to this project will be documented in this file.

The format follows [Semantic Versioning](https://semver.org/).

---

## [0.0.1] – 2025-12-07
### Added
- Initial implementation of the `sqtab` CLI.
- CSV and JSON import functionality with type inference.
- Table inspection commands:
  - `sqtab tables`
  - `sqtab tables --schema`
  - `sqtab analyze <table>`
  - `sqtab info`
- SQL execution via `sqtab sql "<query>"`.
- Table export to CSV and JSON.
- Database reset options (`--hard` and soft reset).
- Rich-formatted output for improved readability.

---

## [Unreleased]
### Planned
- `sqtab head <table>` command  
- `sqtab describe <table>` command  
- AI-assisted analysis  
- Expanded import options (delimiter, no-header, etc.)  
