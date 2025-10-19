"""
Systemd service management
"""

import os
from rich.console import Console
from rich.prompt import Confirm

from src.utils.runner import run_command
from src.utils.audio_devices import AudioDeviceManager

console = Console()


class SystemdManager:
    def __init__(self):
        self.home = os.path.expanduser("~")
        self.user = os.environ.get('USER')
        self.audio_mgr = AudioDeviceManager()
    
    def setup_all(self):
        """Setup all systemd services"""
        console.print("[bold green]Systemd Service Setup[/bold green]\n")
        
        if Confirm.ask("Setup CamillaDSP service?", default=True):
            self.setup_camilladsp_service()
            console.print()
        
        if Confirm.ask("Setup CamillaDSP GUI backend service?", default=True):
            self.setup_gui_service()
            console.print()
        
        if Confirm.ask("Setup librespot service?", default=True):
            self.setup_librespot_service()
            console.print()
        
        console.print("[bold green]✓ All services configured![/bold green]")
    
    def setup_camilladsp_service(self):
        """Create and enable CamillaDSP systemd service"""
        console.print("[cyan]Setting up CamillaDSP service...[/cyan]\n")
        
        service_content = f"""[Unit]
Description=CamillaDSP Audio Processor
After=network.target sound.target
Wants=network.target sound.target

[Service]
Type=simple
User={self.user}
ExecStart={self.home}/.cargo/bin/camilladsp -p1234 -a0.0.0.0 -s {self.home}/camilladsp/statefile.yml -o {self.home}/camilladsp/camilladsp.log
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
        
        service_file = '/tmp/camilladsp.service'
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        run_command(
            ['sudo', 'mv', service_file, '/etc/systemd/system/camilladsp.service'],
            description="Installing service file"
        )
        
        run_command(
            ['sudo', 'systemctl', 'daemon-reload'],
            description="Reloading systemd"
        )
        
        run_command(
            ['sudo', 'systemctl', 'enable', 'camilladsp.service'],
            description="Enabling service"
        )
        
        if Confirm.ask("Start CamillaDSP service now?", default=True):
            run_command(
                ['sudo', 'systemctl', 'restart', 'camilladsp.service'],
                description="Starting service"
            )
        
        console.print("[green]✓ CamillaDSP service configured![/green]")
    
    def setup_gui_service(self):
        """Create and enable GUI backend systemd service"""
        console.print("[cyan]Setting up CamillaDSP GUI backend service...[/cyan]\n")
        
        venv_python = '/opt/venv/bin/python3'
        if not os.path.exists(venv_python):
            venv_python = '/usr/bin/python3'
        
        service_content = f"""[Unit]
Description=CamillaDSP GUI Backend
After=network.target camilladsp.service
Wants=network.target

[Service]
Type=simple
User={self.user}
WorkingDirectory={self.home}/camilladsp/camillagui
ExecStart={venv_python} {self.home}/camilladsp/camillagui/backend/main.py
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
        
        service_file = '/tmp/camillagui.service'
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        run_command(
            ['sudo', 'mv', service_file, '/etc/systemd/system/camillagui.service'],
            description="Installing service file"
        )
        
        run_command(
            ['sudo', 'systemctl', 'daemon-reload'],
            description="Reloading systemd"
        )
        
        run_command(
            ['sudo', 'systemctl', 'enable', 'camillagui.service'],
            description="Enabling service"
        )
        
        if Confirm.ask("Start GUI backend service now?", default=True):
            run_command(
                ['sudo', 'systemctl', 'restart', 'camillagui.service'],
                description="Starting service"
            )
        
        console.print("[green]✓ GUI backend service configured![/green]")
    
    def setup_librespot_service(self):
        """Create and enable librespot systemd service"""
        console.print("[cyan]Setting up librespot service...[/cyan]\n")
        
        device_config = self.audio_mgr.load_device_config()
        
        if not device_config:
            console.print("[yellow]No audio device configured. Using defaults.[/yellow]")
            backend = 'alsa'
            device = 'default'
        else:
            backend = device_config.get('backend', 'alsa')
            device = device_config.get('device', 'default')
        
        if backend == 'pulse':
            backend = 'pulseaudio'
        
        librespot_bin = f"{self.home}/.cargo/bin/librespot"
        cache_dir = f"{self.home}/.cache/librespot"
        
        service_content = f"""[Unit]
Description=Librespot Spotify Connect
After=network.target sound.target
Wants=network.target sound.target

[Service]
Type=simple
User={self.user}
ExecStart={librespot_bin} --name "AudioHelper-Librespot" --backend {backend} --device "{device}" --bitrate 320 --cache {cache_dir} --enable-volume-normalisation
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
        
        service_file = '/tmp/librespot.service'
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        run_command(
            ['sudo', 'mv', service_file, '/etc/systemd/system/librespot.service'],
            description="Installing service file"
        )
        
        run_command(
            ['sudo', 'systemctl', 'daemon-reload'],
            description="Reloading systemd"
        )
        
        run_command(
            ['sudo', 'systemctl', 'enable', 'librespot.service'],
            description="Enabling service"
        )
        
        if Confirm.ask("Start librespot service now?", default=True):
            run_command(
                ['sudo', 'systemctl', 'restart', 'librespot.service'],
                description="Starting service"
            )
        
        console.print("[green]✓ librespot service configured![/green]")
