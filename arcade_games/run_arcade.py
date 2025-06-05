#!/usr/bin/env python3
import os
import sys
from main_menu import main_menu

if __name__ == "__main__":
    # Make sure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run the main menu
    main_menu()
