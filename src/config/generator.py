"""
Configuration file generator for CamillaDSP and librespot
"""

import os
import yaml
import shutil
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.syntax import Syntax

from src.utils.audio_devices import AudioDeviceManager

console = Console()


class ConfigGenerator:
    def __init__(self):
        self.home = os.path.expanduser("~")
        self.camilla_dir = f"{self.home}/camilladsp"
        self.configs_dir = f"{self.camilla_dir}/configs"
        self.audio_mgr = AudioDeviceManager()
    
    def generate_all(self):
        """Generate all configuration files"""
        console.print("[bold green]Configuration File Generation[/bold green]\n")
        
        device_config = self.audio_mgr.load_device_config()
        if not device_config:
            console.print("[yellow]No audio device configured. Please configure audio device first.[/yellow]")
            return
        
        self.generate_camilladsp_config(device_config)
        console.print("\n" + "="*60 + "\n")
        self.generate_gui_config()
        console.print("\n" + "="*60 + "\n")
        self.generate_librespot_config(device_config)
        
        console.print("\n[bold green]✓ All configuration files generated![/bold green]")
    
    def backup_config_file(self, config_file):
        """Backup existing config file with timestamp"""
        if os.path.exists(config_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"{os.path.dirname(config_file)}/backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_file = f"{backup_dir}/{os.path.basename(config_file)}.{timestamp}.bak"
            shutil.copy2(config_file, backup_file)
            console.print(f"[yellow]ℹ Backed up existing config to: {backup_file}[/yellow]")
            return backup_file
        return None
    
    def generate_all_with_review(self):
        """Generate all configuration files with review/edit capability"""
        console.print("[bold green]Generate/Review Configuration Files[/bold green]\n")
        
        device_config = self.audio_mgr.load_device_config()
        if not device_config:
            console.print("[yellow]No audio device configured. Please configure audio device first.[/yellow]")
            return
        
        configs_to_generate = [
            ("CamillaDSP", f"{self.configs_dir}/default_config.yml", 
             lambda: self.generate_camilladsp_config(device_config)),
            ("GUI Backend", f"{self.camilla_dir}/camillagui/config/camillagui.yml",
             lambda: self.generate_gui_config()),
            ("librespot", f"{self.home}/.config/librespot/config.yml",
             lambda: self.generate_librespot_config(device_config))
        ]
        
        for name, config_path, generator_func in configs_to_generate:
            console.print(f"\n[cyan]━━━ {name} Configuration ━━━[/cyan]\n")
            
            if os.path.exists(config_path):
                backup = self.backup_config_file(config_path)
            
            generator_func()
            
            if Confirm.ask(f"\nReview {name} configuration file?", default=True):
                self.review_config_file(config_path, name)
        
        console.print("\n[bold green]✓ Configuration generation complete![/bold green]")
    
    def review_config_file(self, config_file, name):
        """Review and optionally edit a configuration file"""
        if not os.path.exists(config_file):
            console.print(f"[red]Config file not found: {config_file}[/red]")
            return
        
        with open(config_file, 'r') as f:
            content = f.read()
        
        console.print(f"\n[bold]Current {name} configuration:[/bold]\n")
        syntax = Syntax(content, "yaml", theme="monokai", line_numbers=True)
        console.print(syntax)
        
        if Confirm.ask(f"\nEdit this configuration?", default=False):
            console.print(f"\n[yellow]Opening {config_file} for editing...[/yellow]")
            console.print("[dim]Use your preferred editor to modify the file.[/dim]")
            
            editor = os.environ.get('EDITOR', 'nano')
            os.system(f"{editor} {config_file}")
            
            console.print(f"\n[green]✓ Configuration saved to: {config_file}[/green]")
    
    def generate_camilladsp_config(self, device_config):
        """Generate CamillaDSP configuration file"""
        console.print("[cyan]Generating CamillaDSP configuration...[/cyan]\n")
        
        os.makedirs(self.configs_dir, exist_ok=True)
        
        backend = device_config.get('backend', 'alsa')
        device = device_config.get('device', 'hw:0,0')
        
        sample_rate = IntPrompt.ask(
            "Sample rate",
            default=44100,
            choices=["44100", "48000", "88200", "96000", "192000"]
        )
        
        channels = IntPrompt.ask(
            "Number of output channels",
            default=2
        )
        
        config = {
            'devices': {
                'samplerate': sample_rate,
                'chunksize': 1024,
                'queuelimit': 1,
                'capture': {
                    'type': backend.upper(),
                    'channels': 2,
                    'device': 'Loopback,0,0' if backend == 'alsa' else 'default',
                    'format': 'S32LE'
                },
                'playback': {
                    'type': backend.upper(),
                    'channels': channels,
                    'device': device,
                    'format': 'S32LE'
                }
            },
            'filters': {},
            'mixers': {
                'stereo_to_stereo': {
                    'channels': {
                        'in': 2,
                        'out': channels
                    },
                    'mapping': [
                        {'dest': 0, 'sources': [{'channel': 0, 'gain': 0, 'inverted': False}]},
                        {'dest': 1, 'sources': [{'channel': 1, 'gain': 0, 'inverted': False}]}
                    ]
                }
            },
            'pipeline': [
                {'type': 'Mixer', 'name': 'stereo_to_stereo'}
            ]
        }
        
        config_file = f"{self.configs_dir}/default_config.yml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        console.print(f"[green]✓ CamillaDSP config created: {config_file}[/green]")
    
    def generate_gui_config(self):
        """Generate CamillaDSP GUI backend configuration"""
        console.print("[cyan]Generating GUI backend configuration...[/cyan]\n")
        
        gui_dir = f"{self.camilla_dir}/camillagui"
        config_dir = f"{gui_dir}/config"
        os.makedirs(config_dir, exist_ok=True)
        
        port = IntPrompt.ask(
            "CamillaDSP WebSocket port",
            default=1234
        )
        
        gui_port = IntPrompt.ask(
            "GUI backend port",
            default=5005
        )
        
        config = {
            'camilla_host': '127.0.0.1',
            'camilla_port': port,
            'port': gui_port,
            'config_dir': self.configs_dir,
            'coeff_dir': f"{self.camilla_dir}/coeffs",
            'log_file': f"{self.camilla_dir}/camilladsp.log",
            'statefile_path': f"{self.camilla_dir}/statefile.yml",
            'default_config': f"{self.configs_dir}/default_config.yml",
            'update_config_symlink': True,
            'supported_capture_types': ['ALSA', 'Pulse'],
            'supported_playback_types': ['ALSA', 'Pulse']
        }
        
        config_file = f"{config_dir}/camillagui.yml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        console.print(f"[green]✓ GUI config created: {config_file}[/green]")
    
    def generate_librespot_config(self, device_config):
        """Generate librespot configuration"""
        console.print("[cyan]Generating librespot configuration...[/cyan]\n")
        
        config_dir = f"{self.home}/.config/librespot"
        os.makedirs(config_dir, exist_ok=True)
        
        backend = device_config.get('backend', 'alsa')
        device = device_config.get('device', 'hw:0,0')
        
        device_name = Prompt.ask(
            "Spotify Connect device name",
            default="AudioHelper-Librespot"
        )
        
        bitrate = Prompt.ask(
            "Audio bitrate",
            choices=["96", "160", "320"],
            default="320"
        )
        
        if backend == 'alsa':
            backend_param = 'alsa'
            device_param = device
        else:
            backend_param = 'pulseaudio'
            device_param = device
        
        config = {
            'backend': backend_param,
            'device': device_param,
            'name': device_name,
            'bitrate': int(bitrate),
            'cache': f"{self.home}/.cache/librespot",
            'enable_volume_normalisation': True,
            'initial_volume': 50,
            'volume_ctrl': 'linear'
        }
        
        config_file = f"{config_dir}/config.yml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        console.print(f"[green]✓ librespot config created: {config_file}[/green]")
        
        console.print("\n[yellow]Note: librespot will be started with these parameters:[/yellow]")
        console.print(f"[dim]--name '{device_name}' --backend {backend_param} --device '{device_param}'[/dim]")
        console.print(f"[dim]--bitrate {bitrate} --cache {self.home}/.cache/librespot[/dim]")
