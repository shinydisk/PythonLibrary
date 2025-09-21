#!/usr/bin/env python3
"""
File Hash Generator

Generates MD5, SHA1, and SHA256 hashes for a given file.
Useful for file integrity verification and forensic analysis.

__author__ = "Shinydisk"
__version__ = "1.0.0"
"""

import hashlib
import os
import sys

def calculate_hashes(filepath):
    """Calculate MD5, SHA1, and SHA256 hashes for a file."""
    
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return None
    
    # Initialize hash objects
    md5_hash = hashlib.md5()
    sha1_hash = hashlib.sha1()
    sha256_hash = hashlib.sha256()
    
    try:
        with open(filepath, 'rb') as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
                sha1_hash.update(chunk)
                sha256_hash.update(chunk)
        
        return {
            'md5': md5_hash.hexdigest(),
            'sha1': sha1_hash.hexdigest(),
            'sha256': sha256_hash.hexdigest()
        }
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def main():
    """Main function."""
    print("File Hash Generator")
    print("=" * 40)
    
    # Get file path from user
    while True:
        filepath = input("Enter the path to the file: ").strip()
        
        if not filepath:
            print("Please enter a valid file path.")
            continue
        
        # Expand user path if needed
        filepath = os.path.expanduser(filepath)
        
        if os.path.exists(filepath):
            break
        else:
            print(f"File '{filepath}' not found. Please try again.")
    
    # Calculate hashes
    print(f"\nCalculating hashes for: {filepath}")
    print("Please wait...")
    
    hashes = calculate_hashes(filepath)
    
    if hashes:
        print(f"\nFile: {os.path.basename(filepath)}")
        print(f"Size: {os.path.getsize(filepath)} bytes")
        print("-" * 40)
        print(f"MD5:    {hashes['md5']}")
        print(f"SHA1:   {hashes['sha1']}")
        print(f"SHA256: {hashes['sha256']}")
        print("-" * 40)
        print("Hash calculation completed successfully!")
    else:
        print("Failed to calculate hashes.")

if __name__ == "__main__":
    main()