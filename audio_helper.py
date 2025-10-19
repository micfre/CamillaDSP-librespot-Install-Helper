#!/usr/bin/env python3
"""
Audio Helper - Installation and Update Helper for CamillaDSP and librespot
Main entry point for the application
"""

import sys
import os

def check_prerequisites():
    if os.geteuid() == 0:
        print("Error: Please do not run this script as root!")
        print("The script will ask for sudo password when needed.")
        sys.exit(1)
    
    if sys.platform != 'linux':
        print("Error: This script is designed for Linux (Ubuntu/Debian) only.")
        sys.exit(1)

def main():
    check_prerequisites()
    
    from src.ui import MainUI
    
    try:
        ui = MainUI()
        ui.run()
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
