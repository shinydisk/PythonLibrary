"""
Menu configuration for the PythonLibrary interactive menu system.
"""

import os
from typing import Dict, List, Tuple

# Base directory for scripts
SCRIPTS_BASE_DIR = "scripts"

# Menu categories and their descriptions
MENU_CATEGORIES = {
    "file_processing": {
        "name": "File Processing",
        "description": "Tools for file manipulation, conversion, and analysis",
        "directory": "file_processing"
    },
    "network_admin": {
        "name": "Network Administration", 
        "description": "Network monitoring, configuration, and diagnostic tools",
        "directory": "network_admin"
    },
    "security_osint": {
        "name": "Security & OSINT",
        "description": "Ethical hacking tools and Open Source Intelligence gathering",
        "directory": "security_osint"
    }
}

# Menu styling
MENU_HEADER = """
╔══════════════════════════════════════════════════════════════╗
║                    Shinydisk's Python Library               ║
║                     Interactive Menu System                 ║
╚══════════════════════════════════════════════════════════════╝
"""

CATEGORY_SEPARATOR = "─" * 60

def get_script_directories() -> List[str]:
    """Get list of script directories that exist."""
    base_path = SCRIPTS_BASE_DIR
    directories = []
    
    if not os.path.exists(base_path):
        return directories
        
    for category_key, category_info in MENU_CATEGORIES.items():
        dir_path = os.path.join(base_path, category_info["directory"])
        if os.path.exists(dir_path):
            directories.append(category_key)
    
    return directories

def get_scripts_in_category(category_key: str) -> List[Tuple[str, str]]:
    """
    Get list of Python scripts in a category.
    Returns list of tuples: (script_name, script_path)
    """
    if category_key not in MENU_CATEGORIES:
        return []
    
    category_dir = os.path.join(SCRIPTS_BASE_DIR, MENU_CATEGORIES[category_key]["directory"])
    
    if not os.path.exists(category_dir):
        return []
    
    scripts = []
    for file in os.listdir(category_dir):
        if file.endswith(".py") and not file.startswith("__"):
            script_name = file[:-3]  # Remove .py extension
            script_path = os.path.join(category_dir, file)
            scripts.append((script_name, script_path))
    
    return sorted(scripts)