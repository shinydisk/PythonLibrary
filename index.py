#!/usr/bin/env python3
"""
Shinydisk's Python Library - Interactive Menu System

This script provides an interactive menu interface for accessing and running
various Python scripts organized by category:
- File Processing Tools
- Network Administration Tools  
- Security & OSINT Tools

Author: Shinydisk
Version: 1.0.0
"""

import os
import sys
from typing import Optional

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.menu_config import MENU_CATEGORIES, MENU_HEADER, CATEGORY_SEPARATOR, get_script_directories, get_scripts_in_category
from utils.menu_helpers import clear_screen, get_user_input, run_script, pause_for_user, display_script_info

class PythonLibraryMenu:
    """Main menu class for the Python Library interactive system."""
    
    def __init__(self):
        self.running = True
    
    def display_main_menu(self):
        """Display the main category selection menu."""
        clear_screen()
        print(MENU_HEADER)
        
        available_categories = get_script_directories()
        
        if not available_categories:
            print("No script categories found!")
            print(f"Please add Python scripts to the '{os.path.join('scripts', '[category]')}' directories.")
            print("\nAvailable categories:")
            for key, info in MENU_CATEGORIES.items():
                print(f"  - {info['name']}: scripts/{info['directory']}/")
            return
        
        print("Available Categories:")
        print(CATEGORY_SEPARATOR)
        
        for i, category_key in enumerate(available_categories, 1):
            category = MENU_CATEGORIES[category_key]
            script_count = len(get_scripts_in_category(category_key))
            print(f"{i}. {category['name']} ({script_count} scripts)")
            print(f"   {category['description']}")
            print()
        
        print(f"{len(available_categories) + 1}. Exit")
        print(CATEGORY_SEPARATOR)
    
    def display_category_menu(self, category_key: str):
        """Display scripts in a specific category."""
        clear_screen()
        
        category = MENU_CATEGORIES[category_key]
        scripts = get_scripts_in_category(category_key)
        
        print(MENU_HEADER)
        print(f"Category: {category['name']}")
        print(f"Description: {category['description']}")
        print(CATEGORY_SEPARATOR)
        
        if not scripts:
            print("No scripts found in this category.")
            print(f"Add Python scripts to: scripts/{category['directory']}/")
            print("\n1. Back to main menu")
            return ["1"]
        
        print("Available Scripts:")
        print()
        
        valid_options = []
        for i, (script_name, script_path) in enumerate(scripts, 1):
            print(f"{i}. {script_name}")
            valid_options.append(str(i))
        
        print()
        print(f"{len(scripts) + 1}. Back to main menu")
        valid_options.append(str(len(scripts) + 1))
        
        print(CATEGORY_SEPARATOR)
        return valid_options, scripts
    
    def display_script_menu(self, script_name: str, script_path: str):
        """Display options for a specific script."""
        clear_screen()
        print(MENU_HEADER)
        
        display_script_info(script_path)
        
        print("\nActions:")
        print("1. Run script")
        print("2. View script details")
        print("3. Back to category menu")
        print(CATEGORY_SEPARATOR)
        
        return ["1", "2", "3"]
    
    def run_main_loop(self):
        """Main menu loop."""
        while self.running:
            try:
                self.display_main_menu()
                
                available_categories = get_script_directories()
                if not available_categories:
                    pause_for_user()
                    continue
                
                # Get valid options for main menu
                valid_options = [str(i) for i in range(1, len(available_categories) + 2)]
                
                choice = get_user_input("Select an option: ", valid_options)
                choice_num = int(choice)
                
                if choice_num == len(available_categories) + 1:  # Exit option
                    self.running = False
                    break
                
                # Navigate to category menu
                category_key = available_categories[choice_num - 1]
                self.run_category_loop(category_key)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                pause_for_user()
    
    def run_category_loop(self, category_key: str):
        """Category menu loop."""
        while self.running:
            try:
                result = self.display_category_menu(category_key)
                
                if len(result) == 1:  # No scripts found
                    valid_options = result
                    choice = get_user_input("Select an option: ", valid_options)
                    break  # Back to main menu
                
                valid_options, scripts = result
                choice = get_user_input("Select an option: ", valid_options)
                choice_num = int(choice)
                
                if choice_num == len(scripts) + 1:  # Back to main menu
                    break
                
                # Navigate to script menu
                script_name, script_path = scripts[choice_num - 1]
                self.run_script_loop(script_name, script_path)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                pause_for_user()
    
    def run_script_loop(self, script_name: str, script_path: str):
        """Script action menu loop."""
        while self.running:
            try:
                valid_options = self.display_script_menu(script_name, script_path)
                choice = get_user_input("Select an action: ", valid_options)
                choice_num = int(choice)
                
                if choice_num == 1:  # Run script
                    clear_screen()
                    success = run_script(script_path)
                    pause_for_user()
                
                elif choice_num == 2:  # View details
                    clear_screen()
                    print("Script Details:")
                    display_script_info(script_path)
                    
                    # Try to show first few lines of the script
                    try:
                        with open(script_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()[:20]  # First 20 lines
                        
                        print(f"\nFirst 20 lines of {script_name}.py:")
                        print("─" * 40)
                        for i, line in enumerate(lines, 1):
                            print(f"{i:2d}: {line.rstrip()}")
                        
                        if len(lines) == 20:
                            print("... (truncated)")
                    
                    except Exception as e:
                        print(f"Could not read script file: {e}")
                    
                    pause_for_user()
                
                elif choice_num == 3:  # Back to category
                    break
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                pause_for_user()

def main():
    """Main entry point."""
    print("Starting Shinydisk's Python Library Interactive Menu...")
    
    # Check if we're in the right directory
    if not os.path.exists("config") or not os.path.exists("utils"):
        print("Error: Please run this script from the PythonLibrary root directory.")
        print("Required directories: config/, utils/, scripts/")
        sys.exit(1)
    
    menu = PythonLibraryMenu()
    
    try:
        menu.run_main_loop()
    except KeyboardInterrupt:
        pass
    finally:
        clear_screen()
        print("Thank you for using Shinydisk's Python Library!")
        print("Goodbye! 👋")

if __name__ == "__main__":
    main()