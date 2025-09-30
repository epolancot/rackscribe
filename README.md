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
