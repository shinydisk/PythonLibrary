# Netmiko Network Automation Scripts

This directory contains Python scripts for network device automation using the Netmiko library.

These scripts are designed for bulk operations on network devices (switches, routers, firewalls) and now use **secure runtime authentication** (no hardcoded credentials).

---

# 🔐 Security Update (Important)

All scripts now:

* ✅ Prompt for username at runtime
* ✅ Prompt for password (masked input)
* ❌ No credentials stored in clear text
* ❌ No need to edit authentication lines manually

You no longer need to modify the scripts to insert credentials.

---

# Prerequisites

Install Netmiko:

```bash
pip install netmiko
```

Python 3.8+ recommended.

---

# Script Overview

This collection includes four automation scripts:

1. **Script4Backup.py** – Backup running configurations
2. **Script4Inventory.py** – Collect device inventory information
3. **Script4Logging.py** – Retrieve device logs
4. **Script4Push.py** – Push configuration commands

---

# CSV File Requirement

All scripts use a CSV file containing one IP address per line:

```csv
192.168.1.1
192.168.1.2
10.0.0.1
10.0.0.2
```

Default filenames:

* `iplist.csv`
* or `IPv4-list.csv` (depending on script)

Ensure the filename matches the one defined in the script.

---

# Authentication

When running any script:

```bash
python Script4Backup.py
```

You will be prompted:

```
Login:
Password:
```

The password input is masked and not stored.

---

# Device Type Configuration

Each script defines a default `device_type`.

Example:

```python
device_type = "aruba_osswitch"
```

You can change this in the `__main__` section.

Common supported device types:

* `cisco_ios`
* `cisco_iosxe`
* `cisco_nxos`
* `aruba_osswitch`
* `aruba_aoscx`
* `hp_procurve`
* `juniper_junos`
* `linux`

Full list available in Netmiko documentation.

---

# Script Details

---

## 1️⃣ Script4Backup.py – Configuration Backup

### Purpose

Backup running configurations from multiple devices.

### What it does

* Connects to each IP in CSV
* Retrieves hostname
* Downloads running-config
* Saves file in `Backup/`
* Adds timestamp to avoid overwrite
* Logs activity in `Logging/netmiko_backup.log`

### Output Example

```
Backup/
192.168.1.10_SW01_backup_20260301_101530.cfg
```

---

## 2️⃣ Script4Inventory.py – Device Inventory

### Purpose

Collect hardware and software information.

### What it collects

* Hostname
* Model
* Firmware version
* Release date
* MAC address
* Serial number
* Uptime
* Total ports
* Manufacturer
* Last reboot

### Output

CSV file:

```
SwitchInventory/switch_inventory.csv
```

Log file:

```
Logging/netmiko_inventory.log
```

---

## 3️⃣ Script4Logging.py – Log Collection

### Purpose

Retrieve device logs in bulk.

### What it does

* Connects to devices
* Retrieves hostname
* Executes `show logging`
* Saves logs with timestamp

### Output Example

```
Logs/
192.168.1.10_SW01_logs_20260301_103012.log
```

---

## 4️⃣ Script4Push.py – Configuration Push

### Purpose

Push configuration commands to multiple devices.

### Customize Commands

Edit the `commands` list:

```python
commands = [
    "vlan 100",
    "name GUEST",
    "exit"
]
```

### Example Scenarios

**VLAN creation**

```python
commands = [
    "vlan 200",
    "name VOICE",
    "exit"
]
```

**Security hardening**

```python
commands = [
    "no ip http server",
    "ip ssh version 2"
]
```

### Log File

```
Logging/netmiko-push.log
```

---

# Directory Structure

```
.
├── Logging/
├── Backup/
├── Logs/
├── SwitchInventory/
├── Script4Backup.py
├── Script4Inventory.py
├── Script4Logging.py
├── Script4Push.py
├── iplist.csv
└── README.md
```

All directories are created automatically if missing.

---

# Security Best Practices

## 1️⃣ Do Not Hardcode Credentials

Already implemented ✅

## 2️⃣ Use SSH Keys (Optional)

```python
device = {
    'device_type': 'cisco_ios',
    'host': ip,
    'username': username,
    'use_keys': True,
    'key_file': '/path/to/private/key'
}
```

## 3️⃣ Use Environment Variables (Advanced)

```python
import os
username = os.getenv("NETWORK_USERNAME")
password = os.getenv("NETWORK_PASSWORD")
```

---

# Troubleshooting

## Authentication Failure

* Verify credentials
* Ensure SSH enabled
* Check privilege level

## Timeout

* Ping device
* Check port 22
* Increase timeout:

```python
'timeout': 30,
'conn_timeout': 10
```

## Wrong device_type

* Verify platform
* Check Netmiko supported platforms

---

# Recommended Workflow

1. Test script on **one device**
2. Validate output
3. Run bulk operation
4. Review logs

---

# Future Improvements (Optional Ideas)

* Multi-threading (faster execution)
* Retry logic
* Enable mode support
* Unified automation menu
* Email reporting
* API integration

---

# Netmiko Documentation

[https://netmiko.readthedocs.io/](https://netmiko.readthedocs.io/)

---

# Final Note

These scripts are designed for controlled internal network automation.

Always test in lab before production deployment.

---
