# CLIH - CamillaDSP librespot Install Helper

An interactive terminal-based installation and update helper for CamillaDSP and librespot on Ubuntu/Debian AMD64 systems.

## Project Overview
- Simplify installation and configuration of CamillaDSP (digital signal processing for audio)
- Simplify installation and configuration of librespot (Spotify Connect client)
- Provide a user-friendly terminal interface for system configuration
- Automate systemd service setup and management
- Handle audio device enumeration and configuration

## Tech Stack
- **Language**: Python 3.12+ (compatible with Python 3.11+)
- **UI**: Rich library for terminal interface
- **Target OS**: Ubuntu/Debian Linux on AMD64
- **Development**: VS Code with WSL support

## Features

- 🎯 **Interactive menu interface** - Easy-to-use numbered menu navigation with organized sections
- ⚡ **Batch installation** - Run steps 1-4 automatically for quick setup
- 📦 **Package manager support** - Choose between venv, Poetry, or Conda
- 🔧 **Automated installation** - Handles all dependencies and build processes
- 🎵 **Audio device management** - Enumerate and select audio devices
- ⚙️ **Config review & backup** - Review, edit, and save configs with automatic backup
- 🔐 **OAuth integration** - Set up librespot credentials with OAuth/PKCE
- 🚀 **Systemd services** - Start all services (CamillaDSP, GUI, librespot) automatically
- ✅ **Enhanced verification** - Check services, web ports, and OAuth credentials

## Prerequisites

- Ubuntu/Debian-based Linux distribution (AMD64)
- Python 3.12+ installed
- Sudo access
- Internet connection

## Development Setup

### Quick Development Start
```bash
# Clone and setup
cd /path/to/project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
chmod +x clih.py

# Run the application
./clih.py

### Development Dependencies
The project requires the following system dependencies:
- `libyaml-dev` (for YAML processing)
- Python development headers

Install on Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y libyaml-dev python3-dev
```

### Project Structure
```
/
├── clih.py                  # Main entry point
├── src/
│   ├── ui/                  # Terminal UI components
│   ├── installers/          # Installation modules
│   ├── config/              # Configuration file generators
│   ├── utils/               # Utility functions
│   └── services/            # Systemd service management
├── requirements.txt         # Python dependencies
├── .vscode/                 # VS Code configuration
│   ├── launch.json         # Debug configurations
│   ├── tasks.json          # Development tasks
│   └── settings.json       # Editor settings
└── .gitattributes          # Git line ending configuration
```

### Development Commands

#### Using VS Code Tasks (Ctrl+Shift+P -> "Tasks: Run Task")
- **Run CLIH**: Execute the main application
- **Install Dependencies**: Install Python requirements
- **Set Execute Permissions**: Make scripts executable

#### Manual Commands
```bash
# Activate virtual environment
source .venv/bin/activate

# Run main application
./clih.py
# or
python3 clih.py

# Install/update dependencies
pip install -r requirements.txt

# Make executable
chmod +x clih.py
```

### Debugging
Use VS Code debug configurations:
- **"CLIH - Run Main"**: Debug the main application with integrated terminal
- **"CLIH - Debug with Console"**: Debug with detailed output
- **"CLIH - External Terminal"**: Run in external terminal for full interaction

## Prerequisites

- Ubuntu/Debian-based Linux distribution (AMD64)
- Sudo access
- Internet connection

## Quick Start

```bash
# Clone or download this repository
git clone <repository-url>
cd <repository-directory>

# Run the helper
./clih.py
```

## What Gets Installed

### CamillaDSP Components
- **CamillaDSP** - High-performance audio DSP engine
- **GUI Backend** - Web-based configuration interface
- **pycamilladsp** - Python library for CamillaDSP
- **pycamilladsp-plot** - Plotting tools for CamillaDSP

### librespot
- Open-source Spotify Connect client
- OAuth/PKCE authentication support

### System Dependencies
- Rust toolchain (cargo)
- Build essentials (gcc, make, etc.)
- Audio libraries (ALSA, JACK, PulseAudio)
- Python development tools

## Menu Options

### Install/Update
- **B)** **Install/Update All** - Run steps 1-4 sequentially (recommended for new installs)
- **1)** Package Manager Setup - Install venv, Poetry, or Conda
- **2)** Install/Update System Dependencies - Install all required system packages
- **3)** Install/Update CamillaDSP - Install CamillaDSP and components
- **4)** Install/Update librespot - Install librespot

### Configure
- **5)** Configure Audio Devices - Enumerate and select audio output device
- **6)** Generate/Review Configuration Files - Create, review, and edit configs (with backup)
- **7)** Setup librespot Credentials (OAuth) - OAuth authentication flow

### Run
- **8)** Setup/Start Systemd Services - Configure and start all services
- **9)** Verify Installation - Check services, ports, and OAuth credentials

## Usage Flow

### Quick Start (Recommended)
1. Use **Option B** (Batch Install) to install everything automatically
2. Use **Option 5** to configure your audio device
3. Use **Option 6** to generate and review configuration files
4. Use **Option 7** to set up librespot OAuth credentials
5. Use **Option 8** to start all services
6. Use **Option 9** to verify everything is working

### Manual Installation
1. Start with **Option 2** to install system dependencies
2. Optionally use **Option 1** to set up your preferred package manager
3. Use **Option 3** to install CamillaDSP components
4. Use **Option 4** to install librespot
5. Continue with steps 5-9 as above

## Configuration Files

Configuration files are created in:
- CamillaDSP: `~/camilladsp/configs/default_config.yml`
- GUI Backend: `~/camilladsp/camillagui/config/camillagui.yml`
- librespot: `~/.config/librespot/config.yml`

## Services

After setup, the following systemd services will be available:

```bash
# Check service status
systemctl status camilladsp
systemctl status camillagui
systemctl status librespot

# Start/stop services
sudo systemctl start camilladsp
sudo systemctl stop camilladsp

# View logs
journalctl -u camilladsp -f
```

## Default Ports

- **CamillaDSP WebSocket**: 1234
- **GUI Backend**: 5005

Access the GUI at: `http://localhost:5005`

## Troubleshooting

### Rust/Cargo not found after installation
```bash
source ~/.cargo/env
```

### librespot OAuth issues
If running on a remote server, use the manual redirect URL option when setting up credentials.

### Services won't start
Check logs:
```bash
journalctl -u camilladsp -n 50
journalctl -u librespot -n 50
```

### Audio device not found
Make sure your audio device is connected and recognized by the system:
```bash
aplay -l    # List ALSA devices
pactl list sinks  # List PulseAudio/PipeWire devices
```

## References

- [CamillaDSP](https://github.com/HEnquist/camilladsp)
- [CamillaDSP GUI Backend](https://github.com/HEnquist/camillagui-backend)
- [librespot](https://github.com/librespot-org/librespot)

## License

This project is provided as-is for personal use.

## Support

For issues with:
- CamillaDSP: See the [official repository](https://github.com/HEnquist/camilladsp)
- librespot: See the [official repository](https://github.com/librespot-org/librespot)
- This helper: Open an issue in this repository

## Architecture

- Modular design with separate concerns (installation, configuration, UI)
- Python-based for cross-platform compatibility
- Relies on system tools (apt, systemd, rust/cargo)
- Supports both direct execution and development environments

## User Preferences

- Prefer clear terminal output with visual feedback
- Interactive menu interface (numbered options, clean layout)
- Automated workflows where possible, but ask for user input when needed

## Contributing

1. Ensure Python 3.12+ is available
2. Set up virtual environment as described above
3. Use VS Code with recommended extensions
4. Follow existing code style and structure
