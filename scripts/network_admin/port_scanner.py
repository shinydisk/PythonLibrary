#!/usr/bin/env python3
"""
Network Port Scanner

Simple port scanner for checking open ports on a target host.
Useful for network reconnaissance and security assessments.

WARNING: Only use this tool on networks you own or have explicit permission to test.

__author__ = "Shinydisk"
__version__ = "1.0.0"
"""

import socket
import threading
import time
from datetime import datetime

def scan_port(host, port, timeout=3):
    """Scan a single port on the target host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        result = sock.connect_ex((host, port))
        sock.close()
        
        return result == 0  # 0 means connection successful
    
    except socket.gaierror:
        return False
    except Exception:
        return False

def scan_ports(host, ports, max_threads=50):
    """Scan multiple ports using threading."""
    
    print(f"Starting port scan on {host}")
    print(f"Time started: {datetime.now()}")
    print("-" * 50)
    
    open_ports = []
    lock = threading.Lock()
    
    def worker(port):
        if scan_port(host, port):
            with lock:
                open_ports.append(port)
                print(f"Port {port}: OPEN")
    
    # Create and start threads
    threads = []
    for port in ports:
        if len(threads) >= max_threads:
            # Wait for some threads to complete
            for thread in threads:
                thread.join()
            threads = []
        
        thread = threading.Thread(target=worker, args=(port,))
        thread.start()
        threads.append(thread)
    
    # Wait for remaining threads
    for thread in threads:
        thread.join()
    
    return sorted(open_ports)

def get_common_ports():
    """Return list of commonly used ports."""
    return [
        21,    # FTP
        22,    # SSH
        23,    # Telnet
        25,    # SMTP
        53,    # DNS
        80,    # HTTP
        110,   # POP3
        143,   # IMAP
        443,   # HTTPS
        993,   # IMAPS
        995,   # POP3S
        1433,  # MSSQL
        3306,  # MySQL
        3389,  # RDP
        5432,  # PostgreSQL
        8080,  # HTTP Alternative
        8443,  # HTTPS Alternative
    ]

def main():
    """Main function."""
    print("Network Port Scanner")
    print("=" * 40)
    print("WARNING: Only use on networks you own or have permission to test!")
    print("=" * 40)
    
    # Get target host
    while True:
        host = input("Enter target host (IP or hostname): ").strip()
        if host:
            break
        print("Please enter a valid host.")
    
    # Validate host
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Error: Cannot resolve hostname '{host}'")
        return
    
    # Get scan type
    print("\nScan options:")
    print("1. Common ports (17 ports)")
    print("2. Custom port range")
    print("3. Specific ports")
    
    while True:
        choice = input("Choose scan type (1-3): ").strip()
        
        if choice == "1":
            ports = get_common_ports()
            break
        elif choice == "2":
            try:
                start = int(input("Start port: "))
                end = int(input("End port: "))
                if 1 <= start <= end <= 65535:
                    ports = list(range(start, end + 1))
                    break
                else:
                    print("Port range must be between 1-65535 and start <= end")
            except ValueError:
                print("Please enter valid port numbers")
        elif choice == "3":
            try:
                port_list = input("Enter ports separated by commas: ")
                ports = [int(p.strip()) for p in port_list.split(",")]
                if all(1 <= p <= 65535 for p in ports):
                    break
                else:
                    print("All ports must be between 1-65535")
            except ValueError:
                print("Please enter valid port numbers")
        else:
            print("Please choose 1, 2, or 3")
    
    # Confirm scan
    print(f"\nTarget: {host}")
    print(f"Ports to scan: {len(ports)}")
    
    confirm = input("Proceed with scan? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Scan cancelled.")
        return
    
    # Perform scan
    start_time = time.time()
    open_ports = scan_ports(host, ports)
    end_time = time.time()
    
    # Display results
    print("\n" + "=" * 50)
    print("SCAN RESULTS")
    print("=" * 50)
    print(f"Host: {host}")
    print(f"Scanned {len(ports)} ports")
    print(f"Scan time: {end_time - start_time:.2f} seconds")
    print(f"Open ports found: {len(open_ports)}")
    
    if open_ports:
        print("\nOpen ports:")
        for port in open_ports:
            print(f"  {port}/tcp")
    else:
        print("\nNo open ports found.")

if __name__ == "__main__":
    main()