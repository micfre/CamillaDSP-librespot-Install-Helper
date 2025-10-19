"""
System status checker
"""

import os
import subprocess
from typing import Dict
from rich.console import Console
from rich.table import Table
from rich import box

from src.utils.runner import command_exists, run_command

console = Console()


class SystemChecker:
    def __init__(self):
        self.home = os.path.expanduser("~")
    
    def get_status(self) -> Dict[str, bool]:
        """Get installation status of all components"""
        return {
            "Rust/Cargo": command_exists("cargo"),
            "Python venv": command_exists("python3-venv") or os.path.exists("/opt/venv"),
            "Poetry": command_exists("poetry"),
            "Conda": command_exists("conda"),
            "CamillaDSP": command_exists("camilladsp"),
            "GUI Backend": os.path.exists(f"{self.home}/camilladsp/camillagui"),
            "pycamilladsp": self._check_python_package("pycamilladsp"),
            "librespot": command_exists("librespot"),
            "systemd (CamillaDSP)": self._check_systemd_service("camilladsp"),
            "systemd (GUI)": self._check_systemd_service("camillagui"),
            "systemd (librespot)": self._check_systemd_service("librespot"),
        }
    
    def _check_python_package(self, package: str) -> bool:
        """Check if Python package is installed"""
        try:
            result = subprocess.run(
                ['python3', '-c', f'import {package}'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _check_systemd_service(self, service: str) -> bool:
        """Check if systemd service exists"""
        returncode, _, _ = run_command(
            ['systemctl', 'status', f'{service}.service'],
            check=False,
            capture=True
        )
        return returncode in [0, 3]
    
    def verify_all(self):
        """Comprehensive installation verification"""
        console.print("[bold cyan]Installation Verification Report[/bold cyan]\n")
        
        status = self.get_status()
        
        table = Table(box=box.ROUNDED, show_header=True)
        table.add_column("Component", style="cyan bold")
        table.add_column("Status", style="")
        table.add_column("Notes", style="dim")
        
        for component, installed in status.items():
            if installed:
                status_text = "[green]✓ Installed[/green]"
                notes = ""
            else:
                status_text = "[red]✗ Not Installed[/red]"
                notes = "Use menu options to install"
            
            table.add_row(component, status_text, notes)
        
        console.print(table)
        console.print()
        
        self._check_services()
        self._check_ports()
        self._check_oauth_credentials()
    
    def _check_services(self):
        """Check running services status (CamillaDSP, GUI backend, librespot)"""
        console.print("[bold cyan]Service Status (CamillaDSP, GUI backend, librespot):[/bold cyan]\n")
        
        services = {
            'camilladsp': 'CamillaDSP',
            'camillagui': 'GUI Backend',
            'librespot': 'librespot (Spotify Connect)'
        }
        
        for service_name, display_name in services.items():
            returncode, stdout, _ = run_command(
                ['systemctl', 'is-active', f'{service_name}.service'],
                check=False,
                capture=True
            )
            
            if returncode == 0 and stdout.strip() == 'active':
                console.print(f"  [green]✓[/green] {display_name} is [green bold]running[/green bold]")
            else:
                console.print(f"  [yellow]○[/yellow] {display_name} is [yellow]not running[/yellow]")
        
        console.print()
    
    def _check_ports(self):
        """Check if web services are listening on configured ports"""
        console.print("[bold cyan]Web Service Port Status:[/bold cyan]\n")
        
        ports = {
            '1234': 'CamillaDSP WebSocket',
            '5005': 'CamillaDSP GUI Backend'
        }
        
        returncode, stdout, _ = run_command(
            ['ss', '-tln'],
            check=False,
            capture=True
        )
        
        for port, service in ports.items():
            if returncode == 0 and f':{port}' in stdout:
                console.print(f"  [green]✓[/green] {service} [green]listening[/green] on port {port}")
                console.print(f"     [dim]→ http://localhost:{port}[/dim]")
            else:
                console.print(f"  [yellow]○[/yellow] {service} [yellow]not listening[/yellow] on port {port}")
        
        console.print()
    
    def _check_oauth_credentials(self):
        """Check if valid librespot OAuth credentials exist"""
        console.print("[bold cyan]librespot/Spotify OAuth Credentials:[/bold cyan]\n")
        
        cache_dir = f"{self.home}/.cache/librespot"
        credentials_file = f"{cache_dir}/credentials.json"
        
        if os.path.exists(credentials_file):
            file_size = os.path.getsize(credentials_file)
            if file_size > 0:
                console.print(f"  [green]✓[/green] Valid OAuth credentials found")
                console.print(f"     [dim]Location: {credentials_file}[/dim]")
            else:
                console.print(f"  [yellow]○[/yellow] Credentials file exists but is empty")
                console.print(f"     [dim]Run step 7 to setup OAuth credentials[/dim]")
        else:
            console.print(f"  [yellow]○[/yellow] No OAuth credentials found")
            console.print(f"     [dim]Run step 7 (Setup librespot Credentials) to authenticate[/dim]")
        
        console.print()
