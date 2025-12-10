# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by [Keep a Changelog](https://keepachangelog.com/) and this project adheres to [Semantic Versioning](https://semver.org/).

---
## [2.1.0] - 2025-12-10

### Added
- New `--auto-setup` CLI flag to bootstrap project structure.
  - Generates sample inventory (`inventory/devices.yaml`)
  - Generates `.env` template with required device variables
- Automatic creation of output directories for:
  - Running configuration exports
  - Inventory Excel reports
- Improved path handling and directory validation using `pathlib.Path`.

### Changed
- RackScribe now **refuses to run** if `.env` is missing or required variables are not set.
- CLI flag help descriptions revised for clarity.
- Output directory defaults standardized (`outputs/`).

### Fixed
- Correctly handles invalid/writable output directories.
- Fixed misleading success messages when file writes failed.
- Improved Windows path reliability.


## [2.0.1] - 2025-12-09

### Fixed

- Fixed output directory handling when `--out-dir` points to non-existent folders.
- Output folders are now created automatically for:
  - Running configuration exports
  - Inventory Excel exports
- Improved Windows compatibility for output paths (e.g., handling invalid root paths like `/output`).
- Operation statistics now correctly reflect:
  - Invalid IP failures
  - Connection/command exceptions
  - File write failures
- Improved user-facing error messages for unwritable or invalid output paths.


## [2.0.0] - 2025-12-08

### Breaking changes

- Converted RackScribe from a single script (`rackscribe.py`) into an **installable Python package** using a `src/` layout.
- CLI is now invoked as:
  - `rackscribe ...` (via console script), or
  - `python -m rackscribe ...`
- Environment variables for device credentials renamed for consistency:
  - `USERNAME` → `DEVICE_USERNAME`
  - `PASSWORD` → `DEVICE_PASSWORD`
  - `SECRET_PASSWORD` → `DEVICE_SECRET`

### Added

- **Installable package & CLI entrypoint**
  - `rackscribe` is now installed via `pip install -e .`.
  - `__main__.py` acts as the CLI entrypoint.
  - `--version` flag to display the installed RackScribe version.
- **Developer tooling**
  - `mypy` configuration with stricter typing checks.
  - `ruff` configuration for linting and formatting.
  - Optional `dev` extras via `pip install -e .[dev]`.
- **Stats for geeks**
  - Optional `--stats` flag to display elapsed time and per-operation statistics for running-config and inventory collection.
- **Excel report formatting**
  - Inventory exports now:
    - Use styled headers (bold, shaded).
    - Have auto-sized columns.
    - Include frozen header row and auto-filter.
  - Output remains `.xlsx` under `output/inventory/`.

### Changed

- **Project structure**
  - Source code moved under `src/rackscribe/`:
    - `commands.py`, `connection.py`, `inventory.py`, `logging_setup.py`, `operations.py`, `output.py`, `sanitize.py`.
  - Old `rackscribe.py` script replaced by package-based CLI.
- **Logging**
  - Centralized logging configuration in `setup_logging()`.
  - Console logs show concise messages at configurable level (default `INFO`).
  - File logs (`rackscribe.log`) capture full details at `DEBUG`, including tracebacks where appropriate.
  - Many log messages refined for clarity and consistency.
- **Exception handling**
  - `net_connection()` now:
    - Distinguishes network/connectivity errors (`NetmikoTimeoutException`, `NetmikoAuthenticationException`) from unexpected exceptions.
    - Logs user-friendly summaries plus detailed debug traces (`exc_info=True`).
    - Always re-raises exceptions so higher-level logic can decide how to proceed.
  - Per-device operations (`gather_running_configs`, `gather_serial_numbers`) now:
    - Log clear warnings when a device fails.
    - Provide detailed debug logs with full tracebacks for developers.
- **Inventory handling**
  - `load_inventory()` now:
    - Validates file format and structure more clearly.
    - Supports case-insensitive `inventory` key (e.g. `inventory`, `Inventory`, `INVENTORY`).
    - Logs descriptive errors for missing keys, invalid YAML, and bad formats.
    - Returns an empty list on user-input errors while logging details.

### Fixed

- Type hints and return types cleaned up across the codebase to satisfy `mypy` and reduce `Any` usage.
- Broad `except Exception` blocks replaced or narrowed where appropriate, while still preserving error resilience per device.
- Several log messages and behaviors updated to match the new package layout and CLI usage.
- Ensured inventory Excel generation handles empty data sets and filesystem errors gracefully, with clear logs instead of silent failures.

---

## [1.x] - Legacy

- Initial script-based version of RackScribe.
- Single-file CLI (`python rackscribe.py ...`).
- Basic inventory and running-config collection without package structure or strict typing.
