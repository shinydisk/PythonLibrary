# PythonLibrary
The Shinydisk's Python Library

A collection of Python scripts for file processing, network administration tasks, and ethical hacking/OSINT operations, organized with an interactive menu system.

## Quick Start

Run the interactive menu system:

```bash
python3 index.py
```

## Features

- **Interactive Menu System**: Easy-to-use menu interface for accessing all scripts
- **Organized Categories**: Scripts are organized into logical categories
- **Extensible Architecture**: Easy to add new scripts and categories
- **Script Information**: View detailed information about each script before running
- **Error Handling**: Robust error handling and user-friendly messages

## Directory Structure

```
PythonLibrary/
├── index.py                    # Main interactive menu
├── config/
│   ├── menu_config.py         # Menu configuration and categories
│   └── __init__.py
├── utils/
│   ├── menu_helpers.py        # Helper utilities for the menu system
│   └── __init__.py
└── scripts/
    ├── file_processing/       # File manipulation and analysis tools
    │   ├── file_hasher.py     # Generate MD5, SHA1, SHA256 hashes
    │   └── directory_analyzer.py # Analyze directory sizes
    ├── network_admin/         # Network administration tools
    │   ├── port_scanner.py    # Network port scanner
    │   └── network_info.py    # Network interface information
    └── security_osint/        # Security and OSINT tools
        ├── dns_lookup.py      # DNS lookup and analysis
        └── http_header_analyzer.py # HTTP header security analysis
```

## Script Categories

### 📁 File Processing
Tools for file manipulation, conversion, and analysis:
- **File Hasher**: Generate MD5, SHA1, and SHA256 hashes for files
- **Directory Analyzer**: Analyze directory sizes and space usage

### 🌐 Network Administration  
Network monitoring, configuration, and diagnostic tools:
- **Port Scanner**: Scan for open ports on target hosts
- **Network Info**: Display network interface information

### 🔒 Security & OSINT
Ethical hacking tools and Open Source Intelligence gathering:
- **DNS Lookup**: Perform DNS queries and reverse lookups
- **HTTP Header Analyzer**: Analyze HTTP headers for security information

## Adding New Scripts

1. Create your Python script in the appropriate category directory
2. Add proper docstring with description, author, and version information
3. Make the script executable: `chmod +x your_script.py`
4. The script will automatically appear in the interactive menu

Example script structure:
```python
#!/usr/bin/env python3
"""
Script Description

Detailed description of what the script does.

__author__ = "Your Name"
__version__ = "1.0.0"
"""

def main():
    """Main function."""
    print("Hello from your script!")

if __name__ == "__main__":
    main()
```

## Requirements

- Python 3.6 or higher
- Standard library modules only (no external dependencies for core functionality)

## Security Notice

⚠️ **Important**: The network and security tools in this library are intended for:
- Educational purposes
- Network/system administration on your own systems
- Security testing with explicit permission

**Never use these tools on systems you don't own or without proper authorization.**

## License

This project is for educational and personal use. Please respect applicable laws and regulations when using these tools.
