"""
System dependency installer for CamillaDSP and librespot
"""

import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.utils.runner import run_command, command_exists

console = Console()


class DependencyInstaller:
    def __init__(self):
        self.home = os.path.expanduser("~")
    
    def install_all(self):
        """Install all system dependencies"""
        console.print("[bold green]Installing System Dependencies[/bold green]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task1 = progress.add_task("Updating package lists...", total=None)
            run_command(
                ['sudo', 'apt-get', 'update'],
                description="Updating apt package lists"
            )
            progress.update(task1, completed=True)
            
            packages = [
                'build-essential',
                'git',
                'pkg-config',
                'libasound2-dev',
                'libssl-dev',
                'python3',
                'python3-pip',
                'python3-setuptools',
                'curl',
                'wget',
                'libjack-dev',
                'libavahi-compat-libdnssd-dev'
            ]
            
            task2 = progress.add_task("Installing build tools and libraries...", total=None)
            run_command(
                ['sudo', 'apt-get', 'install', '-y'] + packages,
                description=f"Installing {len(packages)} packages"
            )
            progress.update(task2, completed=True)
            
            if not command_exists('cargo'):
                task3 = progress.add_task("Installing Rust toolchain...", total=None)
                self._install_rust()
                progress.update(task3, completed=True)
            else:
                console.print("[yellow]Rust/Cargo already installed, skipping...[/yellow]")
            
            task4 = progress.add_task("Loading ALSA loopback module...", total=None)
            self._setup_alsa_loopback()
            progress.update(task4, completed=True)
        
        console.print("\n[green]✓ All system dependencies installed successfully![/green]")
    
    def _install_rust(self):
        """Install Rust toolchain using rustup"""
        console.print("\n[cyan]Installing Rust toolchain...[/cyan]")
        
        rustup_init = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
        run_command(
            [rustup_init],
            shell=True,
            description="Running rustup installer"
        )
        
        cargo_env = f"{self.home}/.cargo/env"
        if os.path.exists(cargo_env):
            import subprocess
            subprocess.run(f"source {cargo_env}", shell=True, executable='/bin/bash')
        
        console.print("[green]✓ Rust installed. You may need to restart your shell or run:[/green]")
        console.print(f"[dim]source {cargo_env}[/dim]")
    
    def _setup_alsa_loopback(self):
        """Setup ALSA loopback module"""
        console.print("\n[cyan]Setting up ALSA loopback module...[/cyan]")
        
        run_command(
            ['sudo', 'modprobe', 'snd-aloop'],
            check=False,
            description="Loading snd-aloop module"
        )
        
        modules_conf = '/etc/modules-load.d/snd-aloop.conf'
        if not os.path.exists(modules_conf):
            run_command(
                ['sudo', 'sh', '-c', f'echo "snd-aloop" > {modules_conf}'],
                shell=True,
                description="Configuring snd-aloop to load on boot"
            )
            console.print(f"[green]✓ ALSA loopback configured in {modules_conf}[/green]")
        else:
            console.print(f"[yellow]ALSA loopback already configured[/yellow]")
