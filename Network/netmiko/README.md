# Netmiko Network Automation Scripts

This directory contains Python scripts for network device automation using the Netmiko library. These scripts are designed to work with various network equipment including switches, routers, and firewalls.

## Prerequisites

Before using these scripts, ensure you have the following installed:

```bash
pip install netmiko
```

## Script Overview

This collection includes four main automation scripts:

1. **Script4Backup.py** - Backup device configurations
2. **Script4Inventory.py** - Collect device inventory information
3. **Script4Logging.py** - Retrieve device logs
4. **Script4Push.py** - Push configuration commands to devices

## Configuration Requirements

### 1. CSV File Setup (IPv4-list.csv)

All scripts use a CSV file to define the list of devices to connect to. The CSV file should contain one IP address per line:

```csv
192.168.1.1
192.168.1.2
192.168.1.10
192.168.1.20
10.0.0.1
10.0.0.2
```

**Important**: Make sure the CSV file name matches the filename specified in each script.

### 2. Authentication Configuration

Each script requires modification of authentication credentials. Here are the exact line numbers to modify in each script:

**Script4Backup.py - Lines 113-114:**
```python
# Username and password for the connection
username = "admin"          # Change this to your username
password = "password"       # Change this to your password
```

**Script4Inventory.py - Lines to add at the end (after line 81):**
```python
if __name__ == "__main__":
    username = "your_username"    # Add your username
    password = "your_password"    # Add your password
```

**Script4Logging.py - Lines 115-116:**
```python
# Username and password for the connection
username = "admin"          # Change this to your username
password = "password"       # Change this to your password
```

**Script4Push.py - Lines 97-98:**
```python
# Username and password for the connection
username = "admin"          # Change this to your username
password = "password"       # Change this to your password
```

### 3. Device Type Configuration

All scripts default to `aruba_osswitch` but can be modified for different device types. Update the `device_type` parameter at these specific lines:

**Script4Backup.py - Line 25:**
```python
def save_switch_config(ip, username, password, device_type="aruba_osswitch"):
```

**Script4Inventory.py - Line 20:**
```python
def get_switch_info(ip, username, password, device_type="aruba_osswitch"):
```

**Script4Logging.py - Line 25:**
```python
def save_switch_logs(ip, username, password, device_type="aruba_osswitch"):
```

**Script4Push.py - Line 22:**
```python
def send_switch_config(ip, commands, username, password, device_type="device_type"):
```

**Supported device types include:**
- `cisco_ios` - Cisco IOS devices
- `cisco_iosxe` - Cisco IOS-XE devices
- `cisco_nxos` - Cisco Nexus devices
- `aruba_osswitch` - Aruba OS switches
- `hp_procurve` - HP ProCurve switches
- `juniper_junos` - Juniper devices
- `linux` - Linux devices
- And many more (see PLATFORMS.md for complete list)

## Quick Reference - Line Numbers Summary

### 📍 **Key Lines to Modify in Each Script:**

| Script | Authentication Lines | Device Type Line | Commands/CSV Line |
|--------|---------------------|------------------|-------------------|
| **Script4Backup.py** | Lines 114-115 | Line 25 | Line 118 (CSV) |
| **Script4Inventory.py** | Add after Line 81 | Line 20 | Line 30 (commands) |
| **Script4Logging.py** | Lines 116-117 | Line 25 | Line 120 (CSV) |
| **Script4Push.py** | Lines 99-100 | Line 22 | Lines 95-96 (commands) |

### 🔧 **Essential Modifications:**

1. **Change credentials** → Replace `"admin"` and `"password"` with your actual credentials
2. **Update device_type** → Change from `"aruba_osswitch"` to your device type (e.g., `"cisco_ios"`)
3. **Verify CSV file** → Ensure `"IPv4-list.csv"` exists with your device IPs
4. **Customize commands** → Modify commands based on your device vendor

---

## Script 1: Configuration Backup (Script4Backup.py)

### Purpose
Automatically backup running configurations from multiple network devices.

### Key Features
- Connects to devices listed in CSV file
- Retrieves hostname and running configuration
- Saves configurations to individual `.sh` files
- Creates backup directory automatically
- Comprehensive logging

### Configuration Steps

1. **Modify authentication credentials (Lines 113-116):**
```python
if __name__ == "__main__":
    # Username and password for the connection
    username = "your_username"    # Line 114: Change this
    password = "your_password"    # Line 115: Change this

    # CSV file containing switch IPs
    file_csv = "IPv4-list.csv"    # Line 118: Ensure this file exists
```

2. **Optional: Change device type (Line 25):**
```python
def save_switch_config(ip, username, password, device_type="cisco_ios"):
```

3. **Optional: Modify backup commands for different devices (Lines 43-49):**
```python
# Line 43: For Cisco devices, you might want:
hostname_output = connection.send_command("show running-config | include hostname")
# Line 49: Main configuration command
config_output = connection.send_command("show running-config")

# For HP/Aruba devices (same commands work):
# hostname_output = connection.send_command("show running-config | include hostname")
# config_output = connection.send_command("show running-config")
```

### Usage
```bash
python Script4Backup.py
```

### Output
- Backup files saved in `Backup/` directory
- Files named: `IP_HOSTNAME_backup.sh`
- Logs saved in `Logging/netmiko_backup.log`

---

## Script 2: Device Inventory (Script4Inventory.py)

### Purpose
Collect hardware and software inventory information from network devices.

### Key Features
- Extracts device model, firmware version, serial numbers
- Exports data to CSV format
- Supports multiple device information fields
- Automated inventory reporting

### Configuration Steps

1. **Add authentication at the bottom of the script (After line 81):**
```python
# Add these lines at the end of the script:
if __name__ == "__main__":
    username = "your_username"    # Change this
    password = "your_password"    # Change this
    
    # Read device IPs from CSV
    ip_list = []
    with open("IPv4-list.csv", mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            ip_list.append(row[0])
    
    # Process each device
    for ip in ip_list:
        get_switch_info(ip, username, password)
```

2. **Optional: Modify device type (Line 20):**
```python
def get_switch_info(ip, username, password, device_type="cisco_ios"):
```

3. **Optional: Customize information extraction commands (Line 30):**
```python
# Line 30: For Cisco devices:
output = connection.send_command("show version")

# For other vendors, you might need:
# output = connection.send_command("show system information")  # HP/Aruba
# output = connection.send_command("show chassis hardware")    # Juniper
```

### Usage
```bash
python Script4Inventory.py
```

### Output
- Inventory data saved in `SwitchInventory/switch_inventory.csv`
- Logs saved in `Logging/netmiko_inventory.log`

---

## Script 3: Log Collection (Script4Logging.py)

### Purpose
Retrieve and backup system logs from network devices.

### Key Features
- Collects device logs with timestamps
- Saves logs to individual files
- Organized file naming with date/time stamps
- Bulk log collection across multiple devices

### Configuration Steps

1. **Modify authentication credentials (Lines 115-118):**
```python
if __name__ == "__main__":
    # Username and password for the connection
    username = "your_username"    # Line 116: Change this
    password = "your_password"    # Line 117: Change this

    # CSV file containing switch IPs
    file_csv = "IPv4-list.csv"    # Line 120: Ensure this file exists
```

2. **Optional: Change device type (Line 25):**
```python
def save_switch_logs(ip, username, password, device_type="cisco_ios"):
```

3. **Optional: Modify log retrieval commands (Line 49):**
```python
# Line 49: Default command for most devices:
logs_output = connection.send_command("show logging")

# For specific devices you might need:
# logs_output = connection.send_command("show log")          # Some HP devices
# logs_output = connection.send_command("show log messages") # Juniper
# logs_output = connection.send_command("show logging syslog") # Some Cisco
```

### Usage
```bash
python Script4Logging.py
```

### Output
- Log files saved in `Logs/` directory
- Files named: `IP_HOSTNAME_logs_TIMESTAMP.log`
- Logs saved in `Logging/netmiko_logs_backup.log`

---

## Script 4: Configuration Push (Script4Push.py)

### Purpose
Push configuration commands to multiple network devices simultaneously.

### Key Features
- Bulk configuration deployment
- Customizable command sets
- Error handling and logging
- Safe configuration mode

### Configuration Steps

1. **Modify authentication credentials and commands (Lines 93-102):**
```python
if __name__ == "__main__":
    # Configuration commands to send
    commands = [
        "no https-server vrf default"  # Line 95: Modify these commands
    ]
    
    # Username and password for the connection
    username = "your_username"    # Line 99: Change this
    password = "your_password"    # Line 100: Change this

    # CSV file containing switch IPs
    file_csv = "IPv4-list.csv"    # Line 103: Ensure this file exists
```

2. **Modify the commands to push (Lines 94-96):**
```python
# Example command sets for different scenarios:

# VLAN Configuration:
commands = [
    "vlan 100",
    "name GUEST_NETWORK",
    "exit"
]

# Interface Configuration:
commands = [
    "interface GigabitEthernet1/0/1",
    "description Server_Port",
    "switchport mode access",
    "switchport access vlan 100"
]

# Security Configuration:
commands = [
    "no ip http server",
    "ip ssh version 2",
    "line vty 0 4",
    "transport input ssh"
]

# Multiple Commands Example:
commands = [
    "configure terminal",
    "hostname NEW_HOSTNAME",
    "ip domain-name company.com",
    "crypto key generate rsa modulus 2048",
    "exit"
]
```

3. **Optional: Change device type (Line 22):**
```python
def send_switch_config(ip, commands, username, password, device_type="cisco_ios"):
```

4. **Optional: Add configuration saving (After Line 40):**
```python
# Add this after sending commands (Line 40+):
connection.send_command("write memory")  # Cisco
# connection.send_command("write config")   # HP/Aruba
```

### Usage
```bash
python Script4Push.py
```

### Output
- Configuration results displayed in terminal
- Logs saved in `Logging/netmiko-push.log`

---

## Security Best Practices

### 1. Credential Management
- Never hardcode passwords in production scripts
- Use environment variables:
```python
import os
username = os.getenv('NETWORK_USERNAME')
password = os.getenv('NETWORK_PASSWORD')
```

### 2. SSH Key Authentication
- Consider using SSH keys instead of passwords:
```python
device = {
    'device_type': 'cisco_ios',
    'host': ip,
    'username': username,
    'use_keys': True,
    'key_file': '/path/to/private/key'
}
```

### 3. Connection Timeouts
- Adjust timeouts for slow networks:
```python
device = {
    'device_type': 'cisco_ios',
    'host': ip,
    'username': username,
    'password': password,
    'timeout': 30,
    'conn_timeout': 10
}
```

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Verify username and password
   - Check if account has sufficient privileges
   - Ensure SSH is enabled on target devices

2. **Connection Timeouts**
   - Verify network connectivity (`ping` the device)
   - Check if SSH port (22) is accessible
   - Increase timeout values

3. **Device Type Errors**
   - Verify correct device_type for your equipment
   - Check PLATFORMS.md for supported types
   - Some devices may require specific parameters

4. **CSV File Issues**
   - Ensure CSV file exists in the script directory
   - Check file permissions
   - Verify IP address format

5. **Command Failures**
   - Verify commands work manually on device
   - Check command syntax for specific device type
   - Some commands may require enable mode

### Debug Mode
Enable detailed logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Usage

### Custom Device Functions
You can create device-specific functions:

```python
def cisco_specific_backup(ip, username, password):
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': password,
    }
    
    connection = ConnectHandler(**device)
    
    # Cisco-specific commands
    startup_config = connection.send_command("show startup-config")
    running_config = connection.send_command("show running-config")
    version_info = connection.send_command("show version")
    
    connection.disconnect()
    
    return startup_config, running_config, version_info
```

### Error Recovery
Add retry logic for unreliable connections:

```python
import time

def connect_with_retry(device_params, max_retries=3):
    for attempt in range(max_retries):
        try:
            connection = ConnectHandler(**device_params)
            return connection
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  # Wait 5 seconds before retry
            else:
                raise
```

## Support

For device-specific configurations and command references, consult:
- Device vendor documentation
- Netmiko documentation: https://netmiko.readthedocs.io/
- PLATFORMS.md for supported device types

Remember to test scripts on a single device before running bulk operations!

