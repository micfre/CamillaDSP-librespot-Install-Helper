"""
Audio device enumeration and selection
"""

import os
import re
import subprocess
from typing import List, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box

from src.utils.runner import run_command

console = Console()


class AudioDeviceManager:
    def __init__(self):
        self.selected_device = None
        self.selected_backend = None
    
    def enumerate_alsa_devices(self) -> List[Dict[str, str]]:
        """Enumerate ALSA audio devices"""
        devices = []
        
        returncode, stdout, _ = run_command(
            ['aplay', '-l'],
            capture=True,
            check=False
        )
        
        if returncode != 0:
            return devices
        
        current_card = None
        for line in stdout.split('\n'):
            card_match = re.match(r'card (\d+):\s+([^,]+),\s+device (\d+):\s+(.+)', line)
            if card_match:
                card_num, card_name, device_num, device_name = card_match.groups()
                devices.append({
                    'card': card_num,
                    'device': device_num,
                    'card_name': card_name.strip(),
                    'device_name': device_name.strip(),
                    'alsa_name': f'hw:{card_num},{device_num}'
                })
        
        return devices
    
    def enumerate_pipewire_devices(self) -> List[Dict[str, str]]:
        """Enumerate PipeWire/PulseAudio devices"""
        devices = []
        
        returncode, stdout, _ = run_command(
            ['pactl', 'list', 'sinks'],
            capture=True,
            check=False
        )
        
        if returncode != 0:
            return devices
        
        current_sink = {}
        for line in stdout.split('\n'):
            line = line.strip()
            
            if line.startswith('Sink #'):
                if current_sink:
                    devices.append(current_sink)
                current_sink = {'sink_id': line.split('#')[1]}
            elif line.startswith('Name:'):
                current_sink['name'] = line.split(':', 1)[1].strip()
            elif line.startswith('Description:'):
                current_sink['description'] = line.split(':', 1)[1].strip()
        
        if current_sink:
            devices.append(current_sink)
        
        return devices
    
    def select_device(self):
        """Interactive device selection"""
        console.print("[bold cyan]Audio Device Selection[/bold cyan]\n")
        
        console.print("Detecting audio backend...")
        
        has_pipewire = subprocess.run(['which', 'pactl'], capture_output=True).returncode == 0
        has_alsa = subprocess.run(['which', 'aplay'], capture_output=True).returncode == 0
        
        backends = []
        if has_alsa:
            backends.append('ALSA')
        if has_pipewire:
            backends.append('PulseAudio/PipeWire')
        
        if not backends:
            console.print("[red]No audio backends detected![/red]")
            return
        
        console.print(f"[green]Detected backends: {', '.join(backends)}[/green]\n")
        
        backend_choice = Prompt.ask(
            "Select audio backend",
            choices=['alsa', 'pulse'] if has_pipewire else ['alsa'],
            default='alsa'
        )
        
        self.selected_backend = backend_choice
        
        if backend_choice == 'alsa':
            self._select_alsa_device()
        else:
            self._select_pulse_device()
        
        self._save_device_config()
    
    def _select_alsa_device(self):
        """Select ALSA device"""
        devices = self.enumerate_alsa_devices()
        
        if not devices:
            console.print("[red]No ALSA devices found![/red]")
            return
        
        table = Table(box=box.ROUNDED, show_header=True)
        table.add_column("#", style="yellow bold")
        table.add_column("Card", style="cyan")
        table.add_column("Device", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("ALSA ID", style="green")
        
        for idx, device in enumerate(devices):
            table.add_row(
                str(idx + 1),
                device['card'],
                device['device'],
                f"{device['card_name']} - {device['device_name']}",
                device['alsa_name']
            )
        
        console.print(table)
        console.print()
        
        choice = Prompt.ask(
            "Select device number",
            default="1"
        )
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(devices):
                self.selected_device = devices[idx]
                console.print(f"\n[green]✓ Selected: {self.selected_device['alsa_name']}[/green]")
            else:
                console.print("[red]Invalid selection[/red]")
        except ValueError:
            console.print("[red]Invalid input[/red]")
    
    def _select_pulse_device(self):
        """Select PulseAudio/PipeWire device"""
        devices = self.enumerate_pipewire_devices()
        
        if not devices:
            console.print("[red]No PulseAudio/PipeWire devices found![/red]")
            return
        
        table = Table(box=box.ROUNDED, show_header=True)
        table.add_column("#", style="yellow bold")
        table.add_column("Sink ID", style="cyan")
        table.add_column("Name", style="white")
        
        for idx, device in enumerate(devices):
            table.add_row(
                str(idx + 1),
                device.get('sink_id', 'N/A'),
                device.get('description', device.get('name', 'Unknown'))
            )
        
        console.print(table)
        console.print()
        
        choice = Prompt.ask(
            "Select device number",
            default="1"
        )
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(devices):
                self.selected_device = devices[idx]
                console.print(f"\n[green]✓ Selected: {self.selected_device.get('name', 'Unknown')}[/green]")
            else:
                console.print("[red]Invalid selection[/red]")
        except ValueError:
            console.print("[red]Invalid input[/red]")
    
    def _save_device_config(self):
        """Save device configuration for later use"""
        config_file = os.path.expanduser("~/.audio_helper_device")
        
        with open(config_file, 'w') as f:
            f.write(f"backend={self.selected_backend}\n")
            if self.selected_device:
                if self.selected_backend == 'alsa':
                    f.write(f"device={self.selected_device.get('alsa_name', '')}\n")
                else:
                    f.write(f"device={self.selected_device.get('name', '')}\n")
        
        console.print(f"[dim]Configuration saved to {config_file}[/dim]")
    
    def load_device_config(self) -> Optional[Dict[str, str]]:
        """Load saved device configuration"""
        config_file = os.path.expanduser("~/.audio_helper_device")
        
        if not os.path.exists(config_file):
            return None
        
        config = {}
        with open(config_file, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key] = value
        
        return config
