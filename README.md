# Audio Helper - CamillaDSP & librespot Installation Helper

An interactive terminal-based installation and update helper for CamillaDSP and librespot on Ubuntu/Debian AMD64 systems.

## Features

- 🎯 **KIAUH-style menu interface** - Easy-to-use numbered menu navigation
- 📦 **Package manager support** - Choose between venv, Poetry, or Conda
- 🔧 **Automated installation** - Handles all dependencies and build processes
- 🎵 **Audio device management** - Enumerate and select audio devices
- ⚙️ **Configuration generation** - Create config files with sensible defaults
- 🔐 **OAuth integration** - Set up librespot credentials with OAuth/PKCE
- 🚀 **Systemd services** - Automatically configure services to start on boot
- ✅ **Installation verification** - Check status and running services

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
./audio_helper.py
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

1. **Package Manager Setup** - Install venv, Poetry, or Conda
2. **Install/Update System Dependencies** - Install all required system packages
3. **Install/Update CamillaDSP** - Install CamillaDSP and components
4. **Install/Update librespot** - Install librespot
5. **Configure Audio Devices** - Enumerate and select audio output device
6. **Generate Configuration Files** - Create config files with your settings
7. **Setup librespot Credentials** - OAuth authentication flow
8. **Setup Systemd Services** - Configure auto-start services
9. **Verify Installation** - Check installation status and running services

## Usage Flow

Recommended installation order:

1. Start with **Option 2** to install system dependencies
2. Optionally use **Option 1** to set up your preferred package manager
3. Use **Option 3** to install CamillaDSP components
4. Use **Option 4** to install librespot
5. Use **Option 5** to configure your audio device
6. Use **Option 6** to generate configuration files
7. Use **Option 7** to set up librespot credentials (OAuth)
8. Use **Option 8** to configure systemd services
9. Use **Option 9** to verify everything is working

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
- [KIAUH](https://github.com/dw-0/kiauh) (UI inspiration)

## License

This project is provided as-is for personal use.

## Support

For issues with:
- CamillaDSP: See the [official repository](https://github.com/HEnquist/camilladsp)
- librespot: See the [official repository](https://github.com/librespot-org/librespot)
- This helper: Open an issue in this repository
