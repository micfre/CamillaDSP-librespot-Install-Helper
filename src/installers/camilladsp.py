"""
CamillaDSP installer module
"""

import os
import shutil
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.utils.runner import run_command, command_exists

console = Console()


class CamillaDSPInstaller:
    def __init__(self):
        self.home = os.path.expanduser("~")
        self.install_dir = f"{self.home}/camilladsp"
        self.bin_dir = f"{self.install_dir}/bin"
        self.configs_dir = f"{self.install_dir}/configs"
        self.coeffs_dir = f"{self.install_dir}/coeffs"
    
    def _ensure_directories(self):
        """Create necessary directories"""
        os.makedirs(self.bin_dir, exist_ok=True)
        os.makedirs(self.configs_dir, exist_ok=True)
        os.makedirs(self.coeffs_dir, exist_ok=True)
    
    def install_binary(self):
        """Install pre-built CamillaDSP binary"""
        console.print("[bold green]Installing CamillaDSP (pre-built binary)...[/bold green]\n")
        
        self._ensure_directories()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task1 = progress.add_task("Downloading latest release...", total=None)
            
            binary_url = "https://github.com/HEnquist/camilladsp/releases/latest/download/camilladsp-linux-amd64.tar.gz"
            download_path = "/tmp/camilladsp.tar.gz"
            
            run_command(
                ['wget', '-O', download_path, binary_url],
                description="Downloading CamillaDSP binary"
            )
            progress.update(task1, completed=True)
            
            task2 = progress.add_task("Extracting...", total=None)
            run_command(
                ['tar', '-xzf', download_path, '-C', '/tmp/'],
                description="Extracting archive"
            )
            progress.update(task2, completed=True)
            
            task3 = progress.add_task("Installing binary...", total=None)
            src_binary = '/tmp/camilladsp'
            if os.path.exists(src_binary):
                shutil.move(src_binary, f"{self.bin_dir}/camilladsp")
                os.chmod(f"{self.bin_dir}/camilladsp", 0o755)
                
                run_command(
                    ['sudo', 'ln', '-sf', f"{self.bin_dir}/camilladsp", '/usr/local/bin/camilladsp'],
                    check=False,
                    description="Creating symlink in /usr/local/bin"
                )
            progress.update(task3, completed=True)
            
            os.remove(download_path)
        
        console.print(f"\n[green]✓ CamillaDSP installed successfully![/green]")
        console.print(f"[dim]Location: {self.bin_dir}/camilladsp[/dim]")
        
        returncode, version, _ = run_command(
            ['camilladsp', '--version'],
            capture=True
        )
        console.print(f"[cyan]Version: {version.strip()}[/cyan]")
    
    def install_from_source(self):
        """Build and install CamillaDSP from source"""
        console.print("[bold green]Building CamillaDSP from source...[/bold green]\n")
        
        if not command_exists('cargo'):
            console.print("[red]Error: Rust/Cargo not installed. Install dependencies first.[/red]")
            return
        
        self._ensure_directories()
        
        repo_path = "/tmp/camilladsp_repo"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
            
            task1 = progress.add_task("Cloning repository...", total=None)
            run_command(
                ['git', 'clone', 'https://github.com/HEnquist/camilladsp.git', repo_path],
                description="Cloning CamillaDSP repository"
            )
            progress.update(task1, completed=True)
            
            task2 = progress.add_task("Building (this may take several minutes)...", total=None)
            
            import subprocess
            result = subprocess.run(
                ['cargo', 'build', '--release'],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                console.print(f"[red]Build failed: {result.stderr}[/red]")
                return
            
            progress.update(task2, completed=True)
            
            task3 = progress.add_task("Installing binary...", total=None)
            src_binary = f"{repo_path}/target/release/camilladsp"
            if os.path.exists(src_binary):
                shutil.copy(src_binary, f"{self.bin_dir}/camilladsp")
                os.chmod(f"{self.bin_dir}/camilladsp", 0o755)
                
                run_command(
                    ['sudo', 'ln', '-sf', f"{self.bin_dir}/camilladsp", '/usr/local/bin/camilladsp'],
                    check=False
                )
            progress.update(task3, completed=True)
        
        console.print(f"\n[green]✓ CamillaDSP built and installed successfully![/green]")
        console.print(f"[dim]Location: {self.bin_dir}/camilladsp[/dim]")
    
    def install_gui_backend(self):
        """Install CamillaDSP GUI backend"""
        console.print("[bold green]Installing CamillaDSP GUI Backend...[/bold green]\n")
        
        gui_dir = f"{self.install_dir}/camillagui"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task1 = progress.add_task("Downloading GUI backend...", total=None)
            
            gui_url = "https://github.com/HEnquist/camillagui-backend/releases/latest/download/camillagui.zip"
            download_path = "/tmp/camillagui.zip"
            
            run_command(
                ['wget', '-O', download_path, gui_url],
                description="Downloading GUI backend"
            )
            progress.update(task1, completed=True)
            
            task2 = progress.add_task("Extracting...", total=None)
            
            if os.path.exists(gui_dir):
                shutil.rmtree(gui_dir)
            os.makedirs(gui_dir, exist_ok=True)
            
            run_command(
                ['unzip', '-q', download_path, '-d', gui_dir],
                description="Extracting GUI files"
            )
            progress.update(task2, completed=True)
            
            os.remove(download_path)
        
        console.print(f"\n[green]✓ GUI Backend installed successfully![/green]")
        console.print(f"[dim]Location: {gui_dir}[/dim]")
    
    def install_pycamilladsp(self):
        """Install pycamilladsp Python library"""
        console.print("[bold green]Installing pycamilladsp...[/bold green]\n")
        
        venv_path = '/opt/venv'
        if os.path.exists(venv_path):
            pip_cmd = f"{venv_path}/bin/pip3"
        else:
            pip_cmd = "pip3"
        
        run_command(
            ['sudo', pip_cmd, 'install', '--break-system-packages', 
             'git+https://github.com/HEnquist/pycamilladsp.git'],
            description="Installing pycamilladsp"
        )
        
        console.print("\n[green]✓ pycamilladsp installed successfully![/green]")
    
    def install_pycamilladsp_plot(self):
        """Install pycamilladsp-plot Python library"""
        console.print("[bold green]Installing pycamilladsp-plot...[/bold green]\n")
        
        venv_path = '/opt/venv'
        if os.path.exists(venv_path):
            pip_cmd = f"{venv_path}/bin/pip3"
        else:
            pip_cmd = "pip3"
        
        run_command(
            ['sudo', pip_cmd, 'install', '--break-system-packages',
             'git+https://github.com/HEnquist/pycamilladsp-plot.git'],
            description="Installing pycamilladsp-plot"
        )
        
        console.print("\n[green]✓ pycamilladsp-plot installed successfully![/green]")
    
    def install_all(self):
        """Install all CamillaDSP components"""
        console.print("[bold green]Installing All CamillaDSP Components...[/bold green]\n")
        
        self.install_binary()
        console.print("\n" + "="*60 + "\n")
        
        self.install_gui_backend()
        console.print("\n" + "="*60 + "\n")
        
        self.install_pycamilladsp()
        console.print("\n" + "="*60 + "\n")
        
        self.install_pycamilladsp_plot()
        
        console.print("\n[bold green]✓ All CamillaDSP components installed![/bold green]")
