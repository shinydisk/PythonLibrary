#!/usr/bin/env python3
"""
DNS Lookup Tool

Performs various DNS queries for domain analysis and OSINT.
Useful for domain reconnaissance and security assessments.

__author__ = "Shinydisk"
__version__ = "1.0.0"
"""

import socket
import sys
import re

def is_valid_domain(domain):
    """Check if domain name is valid."""
    pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    )
    return pattern.match(domain) is not None

def dns_lookup(domain, record_type="A"):
    """Perform DNS lookup for specified record type."""
    try:
        if record_type.upper() == "A":
            # A record (IPv4)
            result = socket.gethostbyname_ex(domain)
            return {
                'canonical_name': result[0],
                'aliases': result[1],
                'addresses': result[2]
            }
        elif record_type.upper() == "AAAA":
            # AAAA record (IPv6)
            try:
                result = socket.getaddrinfo(domain, None, socket.AF_INET6)
                addresses = list(set([addr[4][0] for addr in result]))
                return {'addresses': addresses}
            except socket.gaierror:
                return None
        else:
            # For other record types, we'd need dnspython
            return None
    
    except socket.gaierror as e:
        return None
    except Exception as e:
        return None

def reverse_dns_lookup(ip_address):
    """Perform reverse DNS lookup."""
    try:
        hostname = socket.gethostbyaddr(ip_address)
        return {
            'hostname': hostname[0],
            'aliases': hostname[1],
            'addresses': hostname[2]
        }
    except socket.herror:
        return None
    except Exception:
        return None

def get_domain_info(domain):
    """Get comprehensive domain information."""
    
    print(f"DNS Lookup for: {domain}")
    print("=" * 50)
    
    # A Record (IPv4)
    print("A Records (IPv4):")
    a_result = dns_lookup(domain, "A")
    if a_result:
        print(f"  Canonical Name: {a_result['canonical_name']}")
        if a_result['aliases']:
            print(f"  Aliases: {', '.join(a_result['aliases'])}")
        print(f"  IP Addresses:")
        for addr in a_result['addresses']:
            print(f"    {addr}")
    else:
        print("  No A records found")
    
    print()
    
    # AAAA Record (IPv6)
    print("AAAA Records (IPv6):")
    aaaa_result = dns_lookup(domain, "AAAA")
    if aaaa_result and aaaa_result['addresses']:
        for addr in aaaa_result['addresses']:
            print(f"  {addr}")
    else:
        print("  No AAAA records found")
    
    print()
    
    # Reverse DNS for each IP
    if a_result and a_result['addresses']:
        print("Reverse DNS Lookup:")
        for ip in a_result['addresses']:
            reverse_result = reverse_dns_lookup(ip)
            if reverse_result:
                print(f"  {ip} -> {reverse_result['hostname']}")
            else:
                print(f"  {ip} -> No reverse DNS found")
        print()
    
    # Additional information
    try:
        # Try to get more detailed info
        addr_info = socket.getaddrinfo(domain, 80, socket.AF_UNSPEC, socket.SOCK_STREAM)
        print("Additional Address Information:")
        for info in addr_info:
            family = "IPv6" if info[0] == socket.AF_INET6 else "IPv4"
            print(f"  {family}: {info[4][0]}")
    except:
        pass

def main():
    """Main function."""
    print("DNS Lookup Tool")
    print("=" * 40)
    print("Useful for domain reconnaissance and OSINT")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Domain lookup")
        print("2. Reverse IP lookup")  
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            # Domain lookup
            domain = input("Enter domain name: ").strip().lower()
            
            if not domain:
                print("Please enter a valid domain name.")
                continue
            
            if not is_valid_domain(domain):
                print("Invalid domain name format.")
                continue
            
            print()
            get_domain_info(domain)
        
        elif choice == "2":
            # Reverse lookup
            ip_address = input("Enter IP address: ").strip()
            
            if not ip_address:
                print("Please enter a valid IP address.")
                continue
            
            # Basic IP validation
            try:
                socket.inet_aton(ip_address)  # IPv4 validation
            except socket.error:
                try:
                    socket.inet_pton(socket.AF_INET6, ip_address)  # IPv6 validation
                except socket.error:
                    print("Invalid IP address format.")
                    continue
            
            print(f"\nReverse DNS Lookup for: {ip_address}")
            print("=" * 50)
            
            result = reverse_dns_lookup(ip_address)
            if result:
                print(f"Hostname: {result['hostname']}")
                if result['aliases']:
                    print(f"Aliases: {', '.join(result['aliases'])}")
            else:
                print("No reverse DNS record found.")
        
        elif choice == "3":
            print("Exiting DNS Lookup Tool.")
            break
        
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()