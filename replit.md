# CLIH - CamillaDSP librespot Install Helper

## Project Overview
An interactive terminal-based installation and update helper for CamillaDSP and librespot on Ubuntu/Debian AMD64 systems.

## Purpose
- Simplify installation and configuration of CamillaDSP (digital signal processing for audio)
- Simplify installation and configuration of librespot (Spotify Connect client)
- Provide a user-friendly terminal interface for system configuration
- Automate systemd service setup and management
- Handle audio device enumeration and configuration

## Tech Stack
- **Language**: Python 3.11
- **UI**: Rich library for terminal interface
- **Target OS**: Ubuntu/Debian Linux on AMD64

## Project Structure
```
/
├── clih.py                  # Main entry point
├── src/
│   ├── ui/                  # Terminal UI components
│   ├── installers/          # Installation modules
│   ├── config/              # Configuration file generators
│   ├── utils/               # Utility functions
│   └── services/            # Systemd service management
└── requirements.txt         # Python dependencies
```

## Key Features
1. **Batch installation** - Run steps 1-4 automatically for quick setup
2. **Package manager selection** - venv, poetry, conda
3. **Dependency installation** - Automated system dependency setup
4. **CamillaDSP installation** - Core, GUI backend, pycamilladsp, pycamilladsp-plot
5. **librespot installation** - Spotify Connect with OAuth/PKCE
6. **Audio device management** - Enumeration and selection
7. **Config review & backup** - Generate, review, edit with automatic backup
8. **Systemd service management** - Setup and start all services (CamillaDSP, GUI, librespot)
9. **Enhanced verification** - Check services, web ports, and OAuth credentials

## Recent Changes
- 2025-10-19: Initial project setup with Python 3.11
- 2025-10-19: Created directory structure and project foundation
- 2025-10-19: Renamed to "CLIH - CamillaDSP librespot Install Helper"
- 2025-10-19: Added batch install (steps 1-4), config review/edit with backup
- 2025-10-19: Enhanced status to check all services, ports, and OAuth credentials
- 2025-10-19: Reorganized menu with Install/Update, Configure, and Run sections
- 2025-10-19: Renamed main file from audio_helper.py to clih.py
- 2025-10-19: Added versioning system (currently v1.0.0) displayed below Main Menu
- 2025-10-19: Removed KIAUH references from all documentation and UI
- 2025-10-19: Renamed batch install to "Install/Update All" for clarity

## User Preferences
- Prefer clear terminal output with visual feedback
- Interactive menu interface (numbered options, clean layout)
- Automated workflows where possible, but ask for user input when needed

## Architecture
- Modular design with separate concerns (installation, configuration, UI)
- Python-based for cross-platform compatibility
- Relies on system tools (apt, systemd, rust/cargo)
