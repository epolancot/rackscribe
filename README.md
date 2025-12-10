<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/Rackscribe_banner3_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="assets/Rackscribe_banner3_light.png">
  <img alt="RackScribe — Get configs & serials" src="assets/banner-light.svg" width="100%">
</picture>

<br/>
RackScribe is a fast and efficient way to collect running configurations and serial numbers from your network devices using Netmiko. Tested on Cisco IE3300 and Cisco Modeling Labs 2.9.0 CSR1000v.

## Installation

### Prerequisites
- **Python 3.10+** (tested on **3.13 / 3.14**)
- `git`
- SSH reachability to network devices (TCP/22)
- Valid device credentials

### Recommended: Upgrade Packaging Tooling

```bash
python -m pip install -U pip setuptools wheel
```

### 1) Clone & create a virtual environment
```bash
git clone https://github.com/epolancot/rackscribe.git
cd rackscribe
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows (CMD)
.\.venv\Scripts\activate

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

### 2) Install RackScribe
```bash
pip install -e .
```

This installs:
- The rackscribe CLI
- All required runtime dependencies:
  - Netmiko
  - Pandas
  - PyYAML
  - TextFSM
  - OpenPyXL

### 3) Environment Variables & Inventory File
#### Quick Start (Recommended)
RackScribe can automatically generate **starter configuration files** for you.
```bash
rackscribe --auto-setup
```
This creates:
- A **sample inventory file** under `inventory/devices.yaml`
- A `.env` **template** in the project root.

Existing files are not overwritten.

### Manual Start
Create an inventory file
Example: inventory/devices.yaml
```yaml
---
inventory:
   - "10.0.1.10"
   - "10.0.1.11"
   - "10.0.1.12"
```
Create a .env file in the project root folder:
```env
DEVICE_TYPE=cisco_ios
DEVICE_USERNAME=YOUR-USERNAME
DEVICE_PASSWORD=YOUR-PASSWORD
DEVICE_SECRET=YOUR-SECRET-PASSWORD  # optional
```

### 4) Edit Your `.env` and `Inventory` Files



## Usage

#### Show Help
```bash
rackscribe --help
```
#### Save Running Configurations
```bash
rackscribe -r
```
**Default behavior**
RackScribe searches for the inventory file at the default location and saves collected running configurations to the default output directory.

- Inventory file: inventory/devices.yaml
- Output directory: outputs/

***Custom Inventory & Output Location***

You can customize both the inventory file location and the output directory:
```bash
rackscribe -r -i path/to/inventory.yaml -o path/to/output/
```
| Flag   | Description                               |
| ------ | --------------------                      |
| `-r`   | Gather running configurations operation   |
| `-i`   | Custom inventory YAML file path           |
| `-o`   | Custom output directory                   |

Final configuration filenames are generated dynamically from each device’s hostname.

#### Collect Serial Numbers (Excel Export)
```bash
rackscribe -s
```
**Default behavior**
RackScribe searches for the inventory file at the default location and saves collected serial numbers to the default output directory.

- Inventory file: inventory/devices.yaml
- Output directory: outputs/

***Custom Inventory & Output Location***

You can customize both the inventory file location and the output directory:
```bash
rackscribe -s -i path/to/inventory.yaml -o path/to/output/inventory
```
| Flag   | Description                               |
| ------ | --------------------                      |
| `-s`   | Gather Serial Numbers operation           |
| `-i`   | Custom inventory YAML file path           |
| `-o`   | Custom output directory                   |

Final excel report filename is generated dynamically using the date and time when the report was generated.

Timestamped Excel file name example:

_output/inventory/Inventory_YYYYMMDD-HHMMSS.xlsx_

## Stats for geeks
```bash
rackscribe -r --stats
```
or
```bash
rackscribe -s --stats
```

Optional `--stats` flag to show operation statistics:
  - Elapsed time per operation.
  - Number of devices processed.
  - Success / failure counts.
  - Derived success rate (devices per second).

Note: Example above assumes default `Inventory` and `Ouput` locations. Use additional flags if needed.
### Example
```bash
rackscribe -r --stats
```
Stats are logged at the end of:
  - `gather_running_configs()`
  - `gather_serial_numbers()`

## Increase logging verbosity
Default console logging level controlled via the -l flag, 0-4.

### Example
```bash
rackscribe -r -l 4
```

### Levels

| Level | Name      | Meaning                                     |
|------:|-----------|---------------------------------------------|
| 0     | CRITICAL  | Unrecoverable error; abort immediately.     |
| 1     | ERROR     | Operation failed; continue to next item.    |
| 2     | WARNING   | Unexpected but non-fatal condition.         |
| 3     | INFO *(default)* | High-level progress messages.        |
| 4     | DEBUG     | Verbose diagnostic details for troubleshooting. |

A detailed log file is always written to `rackscribe.log` at the root folder level.

## Default CLI Values:
| Option | Default                  |
| ------ | --------------------     |
| `-i`   | `inventory/devices.yaml` |
| `-o`   | `outputs/`               |
| `-l`   | `INFO (3)`               |
| `--stats`   | `FALSE`              |


## Optional: Dev Quality Tooling

RackScribe uses modern Python dev tooling:
- mypy (strict typing)
- ruff (lint & format)
- pre-commit (automated checks)

Install RackScribe with dev tools enabled:
```bash
pip install -e .[dev]
```

Pre-Commit Hooks
```bash
pre-commit install
pre-commit run -a
```

## Project Structure
```bash
rackscribe/
├─ assets/                 # banners / branding
├─ inventory/              # user inventories (untracked)
│  └─ devices.yaml
├─ outputs/                # generated output (ignored)
├─ src/
│  └─ rackscribe/          # installable Python package
│     ├─ __init__.py
│     ├─ __main__.py       # CLI entrypoint
│     ├─ auto_setup.py
│     ├─ commands.py
│     ├─ connection.py
│     ├─ inventory.py
│     ├─ logging_setup.py
│     ├─ operations.py
│     ├─ output.py
│     └─ sanitize.py
├─ mypy.ini
├─ pyproject.toml
├─ .pre-commit-config.yaml
└─ .env                    # untracked secrets
```
