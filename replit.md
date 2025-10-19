# Audio Helper - CamillaDSP and librespot Installation Helper

## Project Overview
An interactive terminal-based installation and update helper for CamillaDSP and librespot on Ubuntu/Debian AMD64 systems. Inspired by KIAUH (Klipper Installation And Update Helper) for its user interface design.

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
├── audio_helper.py          # Main entry point
├── src/
│   ├── ui/                  # Terminal UI components (KIAUH-style)
│   ├── installers/          # Installation modules
│   ├── config/              # Configuration file generators
│   ├── utils/               # Utility functions
│   └── services/            # Systemd service management
└── requirements.txt         # Python dependencies
```

## Key Features
1. Package manager selection (venv, poetry, conda)
2. Dependency installation for CamillaDSP and librespot
3. CamillaDSP component installation (core, gui-backend, pycamilladsp, pycamilladsp-plot)
4. librespot installation and OAuth setup
5. Audio device enumeration and selection
6. Configuration file generation
7. Systemd daemon setup
8. Installation verification

## Recent Changes
- 2025-10-19: Initial project setup with Python 3.11
- 2025-10-19: Created directory structure and project foundation

## User Preferences
- Prefer clear terminal output with visual feedback
- KIAUH-style menu interface (numbered options, clean layout)
- Automated workflows where possible, but ask for user input when needed

## Architecture
- Modular design with separate concerns (installation, configuration, UI)
- Python-based for cross-platform compatibility
- Relies on system tools (apt, systemd, rust/cargo)
