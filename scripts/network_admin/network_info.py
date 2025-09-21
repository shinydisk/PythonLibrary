#!/usr/bin/env python3
"""
Network Interface Information

Displays detailed information about network interfaces on the system.
Useful for network troubleshooting and system administration.

__author__ = "Shinydisk"  
__version__ = "1.0.0"
"""

import socket
import platform
import subprocess
import sys
import os

def get_network_interfaces():
    """Get network interface information using multiple methods."""
    
    interfaces = {}
    system = platform.system().lower()
    
    try:
        if system == "linux" or system == "darwin":  # Linux or macOS
            # Try using ip command first (Linux)
            if system == "linux":
                try:
                    result = subprocess.run(['ip', 'addr', 'show'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        return parse_ip_addr_output(result.stdout)
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
            
            # Fallback to ifconfig
            try:
                result = subprocess.run(['ifconfig'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return parse_ifconfig_output(result.stdout)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        
        elif system == "windows":
            # Use ipconfig for Windows
            try:
                result = subprocess.run(['ipconfig', '/all'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return parse_ipconfig_output(result.stdout)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
    
    except Exception as e:
        print(f"Error getting network interfaces: {e}")
    
    # Fallback method using socket
    return get_basic_network_info()

def parse_ip_addr_output(output):
    """Parse output from 'ip addr show' command."""
    interfaces = {}
    current_interface = None
    
    for line in output.split('\n'):
        line = line.strip()
        
        if ': ' in line and not line.startswith(' '):
            # Interface line
            parts = line.split(': ')
            if len(parts) >= 2:
                interface_name = parts[1].split('@')[0]  # Remove @if... suffix
                current_interface = interface_name
                interfaces[current_interface] = {
                    'name': interface_name,
                    'addresses': [],
                    'status': 'UP' if 'UP' in line else 'DOWN'
                }
        
        elif current_interface and 'inet ' in line:
            # IPv4 address
            parts = line.split()
            for i, part in enumerate(parts):
                if part == 'inet' and i + 1 < len(parts):
                    addr = parts[i + 1].split('/')[0]
                    interfaces[current_interface]['addresses'].append(f"IPv4: {addr}")
        
        elif current_interface and 'inet6 ' in line:
            # IPv6 address
            parts = line.split()
            for i, part in enumerate(parts):
                if part == 'inet6' and i + 1 < len(parts):
                    addr = parts[i + 1].split('/')[0]
                    interfaces[current_interface]['addresses'].append(f"IPv6: {addr}")
    
    return interfaces

def parse_ifconfig_output(output):
    """Parse output from ifconfig command."""
    interfaces = {}
    current_interface = None
    
    for line in output.split('\n'):
        if line and not line.startswith(' ') and not line.startswith('\t'):
            # Interface line
            interface_name = line.split(':')[0] if ':' in line else line.split()[0]
            current_interface = interface_name
            interfaces[current_interface] = {
                'name': interface_name,
                'addresses': [],
                'status': 'UP' if 'UP' in line else 'DOWN'
            }
        
        elif current_interface and ('inet ' in line or 'inet addr:' in line):
            # IPv4 address
            if 'inet addr:' in line:
                addr = line.split('inet addr:')[1].split()[0]
            else:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == 'inet' and i + 1 < len(parts):
                        addr = parts[i + 1]
                        break
                else:
                    continue
            
            interfaces[current_interface]['addresses'].append(f"IPv4: {addr}")
    
    return interfaces

def parse_ipconfig_output(output):
    """Parse output from ipconfig /all command."""
    interfaces = {}
    current_interface = None
    
    for line in output.split('\n'):
        line = line.strip()
        
        if 'adapter' in line.lower() and ':' in line:
            # Interface line
            interface_name = line.split(':')[0].strip()
            current_interface = interface_name
            interfaces[current_interface] = {
                'name': interface_name,
                'addresses': [],
                'status': 'UNKNOWN'
            }
        
        elif current_interface and 'IPv4 Address' in line:
            addr = line.split(':')[1].strip()
            interfaces[current_interface]['addresses'].append(f"IPv4: {addr}")
        
        elif current_interface and 'IPv6 Address' in line:
            addr = line.split(':')[1].strip()
            interfaces[current_interface]['addresses'].append(f"IPv6: {addr}")
    
    return interfaces

def get_basic_network_info():
    """Fallback method to get basic network information."""
    interfaces = {}
    
    # Get hostname
    hostname = socket.gethostname()
    
    # Get local IP
    try:
        # Connect to a remote address to find local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        interfaces['default'] = {
            'name': 'default',
            'addresses': [f"IPv4: {local_ip}"],
            'status': 'UP'
        }
    except Exception:
        pass
    
    return interfaces

def main():
    """Main function."""
    print("Network Interface Information")
    print("=" * 50)
    print(f"Hostname: {socket.gethostname()}")
    print(f"System: {platform.system()} {platform.release()}")
    print("=" * 50)
    
    print("Gathering network interface information...")
    interfaces = get_network_interfaces()
    
    if not interfaces:
        print("No network interfaces found or unable to retrieve information.")
        return
    
    for interface_name, info in interfaces.items():
        print(f"\nInterface: {info['name']}")
        print(f"Status: {info['status']}")
        
        if info['addresses']:
            print("Addresses:")
            for addr in info['addresses']:
                print(f"  {addr}")
        else:
            print("No addresses found")
        
        print("-" * 30)
    
    print(f"\nTotal interfaces found: {len(interfaces)}")

if __name__ == "__main__":
    main()