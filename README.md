<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/Rackscribe_banner3_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="assets/Rackscribe_banner3_light.png">
  <img alt="RackScribe — Get configs & serials" src="assets/banner-light.svg" width="100%">
</picture>

## Installation
RackScribe is a fast and simple way to collect running configurations and serial numbers from your network devices using Netmiko. Tested on Cisco IE3300 and Cisco Modeling Labs 2.9.0 CSR1000v.

### Prerequisites
- Python **3.10+** (tested on 3.13)
- `git`
- Network reachability to your devices (SSH/22)

Tip: upgrade packaging tooling first:
> ```bash
> python -m pip install -U pip setuptools wheel
> ```

### 1) Clone & create a virtual environment
```bash
git clone https://github.com/epolancot/rackscribe.git
cd rackscribe
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```
### 3) Configure device credentials (recommended via env vars)
```bash
# .env (example)
DEVICE_TYPE=cisco_ios
USERNAME=**USERNAME**
PASSWORD=**PASSWORD**
SECRET=**SECRET-PASSWORD**
```

### 4) Create an inventory file
```bash
# inventory/lab.yaml
devices:
   - "10.0.1.10"
   - "10.0.1.11"
   - "10.0.1.12"
```

### 5) Run
```bash

# Get Help
python rackscribe.py --help

# Save running-configs to ./configs
python rackscribe.py -r -i inventory/lab.yaml --out-dir ./configs

# Collect serial numbers to Excel
python rackscribe.py -s -i inventory/lab.yaml --out-file ./reports/serials.xlsx

```
## Optional: Dev Quality Tooling

Pre-commit (Ruff lint/format on each commit)
```bash
pip install pre-commit
pre-commit install
pre-commit run -a
```

## Project Structure
```bash
rackscribe/
├─ assets/                 # banner images
├─ inventory/              # untracked real inventories
│  └─ lab.yaml
├─ reports/                # output reports (ignored)
├─ configs/                # config dumps (ignored)
├─ src/
│  ├─ commands.py
│  ├─ connection.py
│  ├─ inventory.py
│  ├─ loggin_setup.py
│  ├─ output.py
│  └─ sanitize.py
├─ pyproject.toml
├─ .pre-commit-config.yaml
├─ .venv
├─ .env                   # untracked real device variables
├─ rackscribe.py          # argparse CLI
└─ requirements.txt
```

## Logging
Default console logging level controlled via the --log_level 0-4 (eg. <i>rackscribe --log_level 2 [...]</i> to collect Warning messages)

A log file is automatically created at the root folder level (logging.log).

### Levels

| Level | Name      | Meaning                                     |
|------:|-----------|---------------------------------------------|
| 0     | CRITICAL  | Unrecoverable error; abort immediately.     |
| 1     | ERROR     | Operation failed; continue to next item.    |
| 2     | WARNING   | Unexpected but non-fatal condition.         |
| 3     | INFO *(default)* | High-level progress messages.   |
| 4     | DEBUG     | Verbose diagnostic details for troubleshooting. |
