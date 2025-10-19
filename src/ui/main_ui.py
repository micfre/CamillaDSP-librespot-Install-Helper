"""
Main UI Module - KIAUH-style terminal interface
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box

from src.installers.package_manager import PackageManagerInstaller
from src.installers.dependencies import DependencyInstaller
from src.installers.camilladsp import CamillaDSPInstaller
from src.installers.librespot import LibrespotInstaller
from src.utils.audio_devices import AudioDeviceManager
from src.config.generator import ConfigGenerator
from src.services.systemd_manager import SystemdManager
from src.utils.system_check import SystemChecker


class MainUI:
    def __init__(self):
        self.console = Console()
        self.pkg_installer = PackageManagerInstaller()
        self.dep_installer = DependencyInstaller()
        self.camilla_installer = CamillaDSPInstaller()
        self.librespot_installer = LibrespotInstaller()
        self.audio_mgr = AudioDeviceManager()
        self.config_gen = ConfigGenerator()
        self.systemd_mgr = SystemdManager()
        self.system_checker = SystemChecker()
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        header = Text()
        header.append("╔════════════════════════════════════════════════════════════════╗\n", style="cyan bold")
        header.append("║         CLIH - CamillaDSP librespot Install Helper             ║\n", style="cyan bold")
        header.append("╚════════════════════════════════════════════════════════════════╝", style="cyan bold")
        self.console.print(header)
        self.console.print()
    
    def print_status(self):
        status = self.system_checker.get_status()
        
        table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="")
        
        for component, installed in status.items():
            status_text = "[green]✓ Installed[/green]" if installed else "[red]✗ Not Installed[/red]"
            table.add_row(component, status_text)
        
        self.console.print(Panel(table, title="System Status", border_style="blue"))
        self.console.print()
    
    def main_menu(self):
        while True:
            self.clear_screen()
            self.print_header()
            self.print_status()
            
            menu = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
            menu.add_column("Option", style="yellow bold")
            menu.add_column("Description", style="white")
            
            menu.add_row("", "[bold cyan]── Install/Update ──[/bold cyan]")
            menu.add_row("B)", "Batch Install All (steps 1-4)")
            menu.add_row("1)", "Package Manager Setup")
            menu.add_row("2)", "Install/Update System Dependencies")
            menu.add_row("3)", "Install/Update CamillaDSP")
            menu.add_row("4)", "Install/Update librespot")
            menu.add_row("", "")
            menu.add_row("", "[bold cyan]── Configure ──[/bold cyan]")
            menu.add_row("5)", "Configure Audio Devices")
            menu.add_row("6)", "Generate/Review Configuration Files")
            menu.add_row("7)", "Setup librespot Credentials (OAuth)")
            menu.add_row("", "")
            menu.add_row("", "[bold cyan]── Run ──[/bold cyan]")
            menu.add_row("8)", "Setup/Start Systemd Services")
            menu.add_row("9)", "Verify Installation")
            menu.add_row("", "")
            menu.add_row("Q)", "Quit")
            
            self.console.print(Panel(menu, title="Main Menu", border_style="green"))
            
            choice = self.console.input("\n[yellow bold]Select an option:[/yellow bold] ").strip().upper()
            
            if choice == 'B':
                self.batch_install()
            elif choice == '1':
                self.package_manager_menu()
            elif choice == '2':
                self.install_dependencies()
            elif choice == '3':
                self.camilladsp_menu()
            elif choice == '4':
                self.librespot_menu()
            elif choice == '5':
                self.configure_audio()
            elif choice == '6':
                self.generate_review_configs()
            elif choice == '7':
                self.setup_librespot_credentials()
            elif choice == '8':
                self.setup_systemd()
            elif choice == '9':
                self.verify_installation()
            elif choice == 'Q':
                self.console.print("\n[green]Thank you for using CLIH! Goodbye![/green]")
                sys.exit(0)
            else:
                self.console.print("[red]Invalid choice. Please try again.[/red]")
                self.console.input("\nPress Enter to continue...")
    
    def batch_install(self):
        """Run steps 1-4 sequentially for quick setup"""
        self.clear_screen()
        self.print_header()
        self.console.print("[bold green]Batch Install - Running Steps 1-4 Sequentially[/bold green]\n")
        
        self.console.print("[cyan]Step 1: Package Manager Setup (optional - skip or choose)...[/cyan]")
        choice = self.console.input("Install package manager? (1=venv, 2=poetry, 3=conda, S=skip): ").strip()
        if choice == '1':
            self.pkg_installer.install_venv()
        elif choice == '2':
            self.pkg_installer.install_poetry()
        elif choice == '3':
            self.pkg_installer.install_conda()
        self.console.print()
        
        self.console.print("[cyan]Step 2: Installing system dependencies...[/cyan]")
        self.dep_installer.install_all()
        self.console.print()
        
        self.console.print("[cyan]Step 3: Installing CamillaDSP components...[/cyan]")
        self.camilla_installer.install_all()
        self.console.print()
        
        self.console.print("[cyan]Step 4: Installing librespot...[/cyan]")
        self.librespot_installer.install_from_cargo()
        self.console.print()
        
        self.console.print("[green]✓ Batch installation complete![/green]")
        self.console.input("\nPress Enter to continue...")
    
    def package_manager_menu(self):
        self.clear_screen()
        self.print_header()
        
        menu = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
        menu.add_column("Option", style="yellow bold")
        menu.add_column("Description", style="white")
        
        menu.add_row("1)", "Install Python venv")
        menu.add_row("2)", "Install Poetry")
        menu.add_row("3)", "Install Conda")
        menu.add_row("B)", "Back to Main Menu")
        
        self.console.print(Panel(menu, title="Package Manager Setup", border_style="green"))
        
        choice = self.console.input("\n[yellow bold]Select an option:[/yellow bold] ").strip().upper()
        
        if choice == '1':
            self.pkg_installer.install_venv()
        elif choice == '2':
            self.pkg_installer.install_poetry()
        elif choice == '3':
            self.pkg_installer.install_conda()
        elif choice == 'B':
            return
        else:
            self.console.print("[red]Invalid choice.[/red]")
        
        self.console.input("\nPress Enter to continue...")
    
    def install_dependencies(self):
        self.clear_screen()
        self.print_header()
        self.console.print("[cyan]Installing system dependencies...[/cyan]\n")
        self.dep_installer.install_all()
        self.console.input("\nPress Enter to continue...")
    
    def camilladsp_menu(self):
        self.clear_screen()
        self.print_header()
        
        menu = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
        menu.add_column("Option", style="yellow bold")
        menu.add_column("Description", style="white")
        
        menu.add_row("1)", "Install/Update CamillaDSP (pre-built binary)")
        menu.add_row("2)", "Install/Update CamillaDSP (from source)")
        menu.add_row("3)", "Install/Update GUI Backend")
        menu.add_row("4)", "Install/Update pycamilladsp")
        menu.add_row("5)", "Install/Update pycamilladsp-plot")
        menu.add_row("6)", "Install All CamillaDSP Components")
        menu.add_row("B)", "Back to Main Menu")
        
        self.console.print(Panel(menu, title="CamillaDSP Installation", border_style="green"))
        
        choice = self.console.input("\n[yellow bold]Select an option:[/yellow bold] ").strip().upper()
        
        if choice == '1':
            self.camilla_installer.install_binary()
        elif choice == '2':
            self.camilla_installer.install_from_source()
        elif choice == '3':
            self.camilla_installer.install_gui_backend()
        elif choice == '4':
            self.camilla_installer.install_pycamilladsp()
        elif choice == '5':
            self.camilla_installer.install_pycamilladsp_plot()
        elif choice == '6':
            self.camilla_installer.install_all()
        elif choice == 'B':
            return
        else:
            self.console.print("[red]Invalid choice.[/red]")
        
        self.console.input("\nPress Enter to continue...")
    
    def librespot_menu(self):
        self.clear_screen()
        self.print_header()
        
        menu = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
        menu.add_column("Option", style="yellow bold")
        menu.add_column("Description", style="white")
        
        menu.add_row("1)", "Install/Update librespot (from cargo)")
        menu.add_row("2)", "Install/Update librespot (from source)")
        menu.add_row("B)", "Back to Main Menu")
        
        self.console.print(Panel(menu, title="librespot Installation", border_style="green"))
        
        choice = self.console.input("\n[yellow bold]Select an option:[/yellow bold] ").strip().upper()
        
        if choice == '1':
            self.librespot_installer.install_from_cargo()
        elif choice == '2':
            self.librespot_installer.install_from_source()
        elif choice == 'B':
            return
        else:
            self.console.print("[red]Invalid choice.[/red]")
        
        self.console.input("\nPress Enter to continue...")
    
    def configure_audio(self):
        self.clear_screen()
        self.print_header()
        self.console.print("[cyan]Configuring audio devices...[/cyan]\n")
        self.audio_mgr.select_device()
        self.console.input("\nPress Enter to continue...")
    
    def generate_review_configs(self):
        """Generate/Review Configuration Files with edit capability"""
        self.clear_screen()
        self.print_header()
        self.console.print("[cyan]Generate/Review Configuration Files[/cyan]\n")
        self.config_gen.generate_all_with_review()
        self.console.input("\nPress Enter to continue...")
    
    def setup_librespot_credentials(self):
        self.clear_screen()
        self.print_header()
        self.console.print("[cyan]Setting up librespot OAuth credentials...[/cyan]\n")
        self.librespot_installer.setup_oauth()
        self.console.input("\nPress Enter to continue...")
    
    def setup_systemd(self):
        """Setup and start ALL systemd services"""
        self.clear_screen()
        self.print_header()
        self.console.print("[cyan]Setting up and starting systemd services...[/cyan]\n")
        self.systemd_mgr.setup_and_start_all()
        self.console.input("\nPress Enter to continue...")
    
    def verify_installation(self):
        self.clear_screen()
        self.print_header()
        self.console.print("[cyan]Verifying installation...[/cyan]\n")
        self.system_checker.verify_all()
        self.console.input("\nPress Enter to continue...")
    
    def run(self):
        self.main_menu()
