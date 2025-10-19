"""
Package manager installer (venv, poetry, conda)
"""

import os
import subprocess
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.utils.runner import run_command, command_exists

console = Console()


class PackageManagerInstaller:
    def __init__(self):
        self.home = os.path.expanduser("~")
    
    def install_venv(self):
        """Install Python venv and create environment"""
        console.print("[bold green]Installing Python venv...[/bold green]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task1 = progress.add_task("Installing python3-venv package...", total=None)
            run_command(
                ['sudo', 'apt-get', 'install', '-y', 'python3-venv'],
                description="Installing python3-venv"
            )
            progress.update(task1, completed=True)
            
            venv_path = '/opt/venv'
            if not os.path.exists(venv_path):
                task2 = progress.add_task("Creating virtual environment...", total=None)
                run_command(
                    ['sudo', 'python3', '-m', 'venv', '--system-site-packages', venv_path],
                    description=f"Creating venv at {venv_path}"
                )
                progress.update(task2, completed=True)
            else:
                console.print(f"[yellow]venv already exists at {venv_path}[/yellow]")
        
        console.print("\n[green]✓ Python venv installed successfully![/green]")
        console.print(f"[dim]Location: {venv_path}[/dim]")
    
    def install_poetry(self):
        """Install Poetry package manager"""
        console.print("[bold green]Installing Poetry...[/bold green]\n")
        
        if command_exists('poetry'):
            console.print("[yellow]Poetry is already installed![/yellow]")
            returncode, version, _ = run_command(
                ['poetry', '--version'],
                capture=True
            )
            console.print(f"[dim]Version: {version.strip()}[/dim]")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Installing Poetry...", total=None)
            
            install_script = "curl -sSL https://install.python-poetry.org | python3 -"
            run_command(
                [install_script],
                shell=True,
                description="Downloading and installing Poetry"
            )
            
            progress.update(task, completed=True)
        
        console.print("\n[green]✓ Poetry installed successfully![/green]")
        console.print("[yellow]Note: You may need to add Poetry to your PATH:[/yellow]")
        console.print(f"[dim]export PATH=\"{self.home}/.local/bin:$PATH\"[/dim]")
    
    def install_conda(self):
        """Install Miniconda"""
        console.print("[bold green]Installing Conda (Miniconda)...[/bold green]\n")
        
        if command_exists('conda'):
            console.print("[yellow]Conda is already installed![/yellow]")
            returncode, version, _ = run_command(
                ['conda', '--version'],
                capture=True
            )
            console.print(f"[dim]Version: {version.strip()}[/dim]")
            return
        
        import platform
        arch = platform.machine()
        
        if arch == 'x86_64':
            installer_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        elif arch == 'aarch64':
            installer_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"
        else:
            console.print(f"[red]Unsupported architecture: {arch}[/red]")
            return
        
        installer_path = f"/tmp/miniconda_installer.sh"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task1 = progress.add_task("Downloading Miniconda...", total=None)
            run_command(
                ['wget', installer_url, '-O', installer_path],
                description="Downloading Miniconda installer"
            )
            progress.update(task1, completed=True)
            
            task2 = progress.add_task("Installing Miniconda...", total=None)
            run_command(
                ['bash', installer_path, '-b', '-p', f'{self.home}/miniconda3'],
                description="Running Miniconda installer"
            )
            progress.update(task2, completed=True)
            
            os.remove(installer_path)
        
        console.print("\n[green]✓ Conda installed successfully![/green]")
        console.print("[yellow]Note: To activate conda, run:[/yellow]")
        console.print(f"[dim]{self.home}/miniconda3/bin/conda init bash[/dim]")
        console.print("[dim]Then restart your shell.[/dim]")
