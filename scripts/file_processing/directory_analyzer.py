#!/usr/bin/env python3
"""
Directory Size Analyzer

Analyzes directory sizes and provides a breakdown of space usage.
Helpful for identifying large files and directories consuming disk space.

__author__ = "Shinydisk"
__version__ = "1.0.0"
"""

import os
import sys

def get_directory_size(directory):
    """Calculate the total size of a directory."""
    total_size = 0
    
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, IOError):
                    # Skip files we can't access
                    pass
    except (OSError, IOError):
        pass
    
    return total_size

def format_size(size_bytes):
    """Format size in bytes to human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def analyze_directory(directory):
    """Analyze directory and subdirectory sizes."""
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found.")
        return
    
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a directory.")
        return
    
    print(f"Analyzing directory: {directory}")
    print("=" * 60)
    
    items = []
    total_size = 0
    
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            
            if os.path.isdir(item_path):
                size = get_directory_size(item_path)
                items.append((item, size, "DIR"))
            elif os.path.isfile(item_path):
                try:
                    size = os.path.getsize(item_path)
                    items.append((item, size, "FILE"))
                except (OSError, IOError):
                    items.append((item, 0, "FILE"))
            
            total_size += size
    
    except PermissionError:
        print("Error: Permission denied accessing directory.")
        return
    
    # Sort by size (largest first)
    items.sort(key=lambda x: x[1], reverse=True)
    
    print(f"{'Name':<30} {'Type':<6} {'Size':<15} {'% of Total':<10}")
    print("-" * 65)
    
    for name, size, item_type in items:
        percentage = (size / total_size * 100) if total_size > 0 else 0
        print(f"{name[:29]:<30} {item_type:<6} {format_size(size):<15} {percentage:.1f}%")
    
    print("-" * 65)
    print(f"Total: {format_size(total_size)}")
    print(f"Items: {len(items)}")

def main():
    """Main function."""
    print("Directory Size Analyzer")
    print("=" * 40)
    
    # Get directory path from user
    while True:
        directory = input("Enter the directory path to analyze: ").strip()
        
        if not directory:
            print("Please enter a valid directory path.")
            continue
        
        # Expand user path if needed
        directory = os.path.expanduser(directory)
        
        if os.path.exists(directory) and os.path.isdir(directory):
            break
        else:
            print(f"Directory '{directory}' not found or is not a directory. Please try again.")
    
    print("\nAnalyzing directory structure...")
    analyze_directory(directory)

if __name__ == "__main__":
    main()