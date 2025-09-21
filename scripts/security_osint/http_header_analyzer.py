#!/usr/bin/env python3
"""
HTTP Header Analyzer

Analyzes HTTP headers for security information and potential vulnerabilities.
Useful for web application security assessments and OSINT.

__author__ = "Shinydisk"
__version__ = "1.0.0"
"""

import urllib.request
import urllib.parse
import ssl
import socket
from datetime import datetime

def analyze_headers(url):
    """Analyze HTTP headers for a given URL."""
    
    # Ensure URL has a scheme
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"Analyzing headers for: {url}")
    print("=" * 60)
    
    try:
        # Create request with user agent
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Python HTTP Header Analyzer)')
        
        # Open connection
        with urllib.request.urlopen(req, timeout=10) as response:
            
            # Basic response info
            print(f"Status Code: {response.status}")
            print(f"HTTP Version: HTTP/{response.version}")
            print(f"URL: {response.url}")
            print()
            
            # Headers analysis
            headers = dict(response.headers)
            
            print("Response Headers:")
            print("-" * 40)
            for header, value in headers.items():
                print(f"{header}: {value}")
            
            print()
            
            # Security headers analysis
            analyze_security_headers(headers)
            
            # Server information
            analyze_server_info(headers)
            
            # Technology detection
            analyze_technology(headers)
    
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print("\nResponse Headers (if available):")
        if hasattr(e, 'headers'):
            headers = dict(e.headers)
            for header, value in headers.items():
                print(f"{header}: {value}")
    
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    
    except Exception as e:
        print(f"Error: {e}")

def analyze_security_headers(headers):
    """Analyze security-related headers."""
    
    print("Security Headers Analysis:")
    print("-" * 40)
    
    security_headers = {
        'Strict-Transport-Security': 'HSTS - Forces HTTPS connections',
        'Content-Security-Policy': 'CSP - Prevents XSS attacks',
        'X-Frame-Options': 'Prevents clickjacking attacks',
        'X-Content-Type-Options': 'Prevents MIME sniffing',
        'X-XSS-Protection': 'XSS filter (deprecated but still used)',
        'Referrer-Policy': 'Controls referrer information',
        'Feature-Policy': 'Controls browser features',
        'Permissions-Policy': 'Modern feature policy',
        'Cross-Origin-Embedder-Policy': 'COEP - Cross-origin isolation',
        'Cross-Origin-Opener-Policy': 'COOP - Cross-origin isolation',
        'Cross-Origin-Resource-Policy': 'CORP - Cross-origin resource access'
    }
    
    found_headers = []
    missing_headers = []
    
    for header, description in security_headers.items():
        if header in headers or header.lower() in [h.lower() for h in headers.keys()]:
            found_headers.append((header, description))
        else:
            missing_headers.append((header, description))
    
    if found_headers:
        print("✓ Present Security Headers:")
        for header, desc in found_headers:
            value = next((v for k, v in headers.items() if k.lower() == header.lower()), "")
            print(f"  {header}: {desc}")
            print(f"    Value: {value}")
    
    if missing_headers:
        print("\n⚠ Missing Security Headers:")
        for header, desc in missing_headers:
            print(f"  {header}: {desc}")
    
    print()

def analyze_server_info(headers):
    """Analyze server information from headers."""
    
    print("Server Information:")
    print("-" * 40)
    
    server_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version', 'X-Generator']
    
    found_info = False
    for header in server_headers:
        for h_name, h_value in headers.items():
            if h_name.lower() == header.lower():
                print(f"{header}: {h_value}")
                found_info = True
    
    if not found_info:
        print("No server information disclosed in headers")
    
    print()

def analyze_technology(headers):
    """Detect technology from headers."""
    
    print("Technology Detection:")
    print("-" * 40)
    
    technologies = []
    
    for header, value in headers.items():
        header_lower = header.lower()
        value_lower = value.lower()
        
        # Common technology indicators
        if 'nginx' in value_lower:
            technologies.append("Nginx web server")
        elif 'apache' in value_lower:
            technologies.append("Apache web server")
        elif 'iis' in value_lower:
            technologies.append("Microsoft IIS")
        elif 'cloudflare' in value_lower:
            technologies.append("Cloudflare CDN")
        elif 'php' in value_lower:
            technologies.append("PHP")
        elif 'asp.net' in value_lower:
            technologies.append("ASP.NET")
        elif 'express' in value_lower:
            technologies.append("Express.js")
    
    # Check specific headers
    if 'X-Powered-By' in headers:
        technologies.append(f"Powered by: {headers['X-Powered-By']}")
    
    if technologies:
        for tech in set(technologies):  # Remove duplicates
            print(f"• {tech}")
    else:
        print("No obvious technology indicators found")
    
    print()

def main():
    """Main function."""
    print("HTTP Header Analyzer")
    print("=" * 40)
    print("Analyzes HTTP headers for security and technology information")
    print("=" * 40)
    
    while True:
        url = input("\nEnter URL to analyze (or 'quit' to exit): ").strip()
        
        if url.lower() in ['quit', 'exit', 'q']:
            break
        
        if not url:
            print("Please enter a valid URL.")
            continue
        
        print()
        analyze_headers(url)
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()