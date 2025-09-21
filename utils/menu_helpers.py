"""
Helper utilities for the interactive menu system.
"""

import os
import sys
import subprocess
import importlib.util
from typing import Optional, Dict, Any

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input(prompt: str, valid_options: list = None) -> str:
    """
    Get user input with validation.
    
    Args:
        prompt: Input prompt to display
        valid_options: List of valid input options (optional)
    
    Returns:
        User input string
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if valid_options is None:
                return user_input
            
            if user_input.lower() in [opt.lower() for opt in valid_options]:
                return user_input.lower()
            
            print(f"Invalid option. Please choose from: {', '.join(valid_options)}")
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)
        except EOFError:
            print("\n\nExiting...")
            sys.exit(0)

def run_script(script_path: str) -> bool:
    """
    Execute a Python script safely.
    
    Args:
        script_path: Path to the Python script to run
    
    Returns:
        True if script ran successfully, False otherwise
    """
    if not os.path.exists(script_path):
        print(f"Error: Script not found at {script_path}")
        return False
    
    try:
        print(f"\n{'='*60}")
        print(f"Running: {os.path.basename(script_path)}")
        print(f"{'='*60}")
        
        # Run the script in a subprocess
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False, 
                              text=True)
        
        print(f"\n{'='*60}")
        if result.returncode == 0:
            print("Script completed successfully!")
        else:
            print(f"Script exited with code: {result.returncode}")
        print(f"{'='*60}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running script: {e}")
        return False

def get_script_info(script_path: str) -> Dict[str, Any]:
    """
    Extract information from a Python script's docstring and metadata.
    
    Args:
        script_path: Path to the Python script
    
    Returns:
        Dictionary with script information
    """
    info = {
        "name": os.path.basename(script_path)[:-3],  # Remove .py extension
        "description": "No description available",
        "author": "Unknown",
        "version": "1.0.0"
    }
    
    try:
        # Read the file to extract docstring and metadata
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to extract module docstring
        lines = content.split('\n')
        in_docstring = False
        docstring_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('"""') or line.startswith("'''"):
                if in_docstring:
                    break
                in_docstring = True
                if len(line) > 3:  # Docstring starts and ends on same line
                    docstring_lines.append(line[3:-3])
                    break
                continue
            
            if in_docstring:
                docstring_lines.append(line)
        
        if docstring_lines:
            info["description"] = ' '.join(docstring_lines).strip()
        
        # Look for common metadata patterns
        for line in lines:
            line = line.strip().lower()
            if line.startswith('__author__'):
                info["author"] = line.split('=')[1].strip().strip('"\'')
            elif line.startswith('__version__'):
                info["version"] = line.split('=')[1].strip().strip('"\'')
    
    except Exception:
        pass  # If we can't read the file, use defaults
    
    return info

def pause_for_user():
    """Pause execution and wait for user to press Enter."""
    try:
        input("\nPress Enter to continue...")
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)

def display_script_info(script_path: str):
    """Display detailed information about a script."""
    info = get_script_info(script_path)
    
    print(f"\n{'='*60}")
    print(f"Script: {info['name']}")
    print(f"Description: {info['description']}")
    print(f"Author: {info['author']}")
    print(f"Version: {info['version']}")
    print(f"Path: {script_path}")
    print(f"{'='*60}")