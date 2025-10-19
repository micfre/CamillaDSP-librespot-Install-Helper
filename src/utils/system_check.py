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
    
    def _check_services(self):
        """Check running services"""
        console.print("[bold cyan]Service Status:[/bold cyan]\n")
        
        services = ['camilladsp', 'camillagui', 'librespot']
        
        for service in services:
            returncode, stdout, _ = run_command(
                ['systemctl', 'is-active', f'{service}.service'],
                check=False,
                capture=True
            )
            
            if returncode == 0 and stdout.strip() == 'active':
                console.print(f"  [green]✓[/green] {service} is running")
            else:
                console.print(f"  [yellow]○[/yellow] {service} is not running")
        
        console.print()
    
    def _check_ports(self):
        """Check if services are listening on expected ports"""
        console.print("[bold cyan]Port Status:[/bold cyan]\n")
        
        ports = {
            '1234': 'CamillaDSP WebSocket',
            '5005': 'CamillaDSP GUI Backend'
        }
        
        for port, service in ports.items():
            returncode, stdout, _ = run_command(
                ['ss', '-tln'],
                check=False,
                capture=True
            )
            
            if f':{port}' in stdout:
                console.print(f"  [green]✓[/green] {service} listening on port {port}")
            else:
                console.print(f"  [yellow]○[/yellow] {service} not listening on port {port}")
        
        console.print()
