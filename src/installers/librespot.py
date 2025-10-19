"""
librespot installer module
"""

import os
import shutil
import subprocess
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

from src.utils.runner import run_command, command_exists

console = Console()


class LibrespotInstaller:
    def __init__(self):
        self.home = os.path.expanduser("~")
        self.cache_dir = f"{self.home}/.cache/librespot"
    
    def install_from_cargo(self):
        """Install librespot using cargo"""
        console.print("[bold green]Installing librespot from cargo...[/bold green]\n")
        
        if not command_exists('cargo'):
            console.print("[red]Error: Rust/Cargo not installed. Install dependencies first.[/red]")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Installing librespot (this may take several minutes)...", total=None)
            
            env = os.environ.copy()
            env['PATH'] = f"{self.home}/.cargo/bin:" + env.get('PATH', '')
            
            result = subprocess.run(
                ['cargo', 'install', 'librespot'],
                env=env,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                console.print(f"[red]Installation failed: {result.stderr}[/red]")
                return
            
            progress.update(task, completed=True)
        
        console.print("\n[green]✓ librespot installed successfully![/green]")
        console.print(f"[dim]Location: {self.home}/.cargo/bin/librespot[/dim]")
        
        returncode, version, _ = run_command(
            [f"{self.home}/.cargo/bin/librespot", '--version'],
            capture=True,
            check=False
        )
        if returncode == 0:
            console.print(f"[cyan]Version: {version.strip()}[/cyan]")
    
    def install_from_source(self):
        """Build and install librespot from source"""
        console.print("[bold green]Building librespot from source...[/bold green]\n")
        
        if not command_exists('cargo'):
            console.print("[red]Error: Rust/Cargo not installed. Install dependencies first.[/red]")
            return
        
        repo_path = "/tmp/librespot_repo"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
            
            task1 = progress.add_task("Cloning repository...", total=None)
            run_command(
                ['git', 'clone', 'https://github.com/librespot-org/librespot.git', repo_path],
                description="Cloning librespot repository"
            )
            progress.update(task1, completed=True)
            
            task2 = progress.add_task("Building (this may take several minutes)...", total=None)
            
            env = os.environ.copy()
            env['PATH'] = f"{self.home}/.cargo/bin:" + env.get('PATH', '')
            
            result = subprocess.run(
                ['cargo', 'build', '--release'],
                cwd=repo_path,
                env=env,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                console.print(f"[red]Build failed: {result.stderr}[/red]")
                return
            
            progress.update(task2, completed=True)
            
            task3 = progress.add_task("Installing binary...", total=None)
            src_binary = f"{repo_path}/target/release/librespot"
            dest_binary = f"{self.home}/.cargo/bin/librespot"
            
            if os.path.exists(src_binary):
                os.makedirs(os.path.dirname(dest_binary), exist_ok=True)
                shutil.copy(src_binary, dest_binary)
                os.chmod(dest_binary, 0o755)
                
                run_command(
                    ['sudo', 'ln', '-sf', dest_binary, '/usr/local/bin/librespot'],
                    check=False
                )
            progress.update(task3, completed=True)
        
        console.print(f"\n[green]✓ librespot built and installed successfully![/green]")
        console.print(f"[dim]Location: {dest_binary}[/dim]")
    
    def setup_oauth(self):
        """Setup librespot credentials using OAuth"""
        console.print("[bold green]Setting up librespot OAuth Credentials[/bold green]\n")
        
        librespot_bin = self._find_librespot()
        if not librespot_bin:
            console.print("[red]Error: librespot not installed. Install it first.[/red]")
            return
        
        os.makedirs(self.cache_dir, exist_ok=True)
        os.chmod(self.cache_dir, 0o700)
        
        console.print("[cyan]This will start the OAuth authentication flow.[/cyan]")
        console.print("[cyan]A URL will be displayed - open it in your browser to authenticate.[/cyan]\n")
        
        device_name = Prompt.ask(
            "Enter device name for Spotify Connect",
            default="AudioHelper-Librespot"
        )
        
        console.print(f"\n[yellow]Starting librespot OAuth flow...[/yellow]\n")
        console.print("[dim]If you're on a remote server, you may need to use --oauth-port 0[/dim]")
        console.print("[dim]and manually paste the redirect URL when prompted.[/dim]\n")
        
        use_manual = Prompt.ask(
            "Use manual redirect URL entry? (for remote/headless servers)",
            choices=["y", "n"],
            default="n"
        )
        
        cmd = [
            librespot_bin,
            '--name', device_name,
            '--cache', self.cache_dir,
            '-j'
        ]
        
        if use_manual.lower() == 'y':
            cmd.append('--oauth-port')
            cmd.append('0')
        
        try:
            console.print("\n[yellow]Running librespot OAuth...[/yellow]")
            console.print("[dim]Follow the instructions in the output below:[/dim]\n")
            
            result = subprocess.run(cmd, text=True)
            
            credentials_file = f"{self.cache_dir}/credentials.json"
            if os.path.exists(credentials_file):
                console.print(f"\n[green]✓ Credentials saved successfully![/green]")
                console.print(f"[dim]Location: {credentials_file}[/dim]")
                os.chmod(credentials_file, 0o600)
            else:
                console.print("\n[yellow]Credentials file not found. The OAuth flow may not have completed.[/yellow]")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]OAuth flow cancelled.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error during OAuth: {e}[/red]")
    
    def _find_librespot(self):
        """Find librespot binary"""
        paths = [
            '/usr/local/bin/librespot',
            f"{self.home}/.cargo/bin/librespot",
            'librespot'
        ]
        
        for path in paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
            elif command_exists(path):
                return path
        
        return None
