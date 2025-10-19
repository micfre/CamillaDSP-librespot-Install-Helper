#!/usr/bin/env python3
"""
Demo mode for CLIH - shows the UI without requiring interaction
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box

console = Console()

def clear_screen():
    console.clear()

def print_header():
    header = Text()
    header.append("╔════════════════════════════════════════════════════════════════╗\n", style="cyan bold")
    header.append("║         CLIH - CamillaDSP librespot Install Helper            ║\n", style="cyan bold")
    header.append("╚════════════════════════════════════════════════════════════════╝", style="cyan bold")
    console.print(header)
    console.print()

def demo_main_menu():
    clear_screen()
    print_header()
    
    console.print("[yellow]DEMO MODE - Showcasing UI[/yellow]\n")
    
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column("Option", style="yellow bold")
    table.add_column("Description", style="white")
    
    table.add_row("", "[bold cyan]── Install/Update ──[/bold cyan]")
    table.add_row("B)", "Batch Install All (steps 1-4)")
    table.add_row("1)", "Package Manager Setup")
    table.add_row("2)", "Install/Update System Dependencies")
    table.add_row("3)", "Install/Update CamillaDSP")
    table.add_row("4)", "Install/Update librespot")
    table.add_row("", "")
    table.add_row("", "[bold cyan]── Configure ──[/bold cyan]")
    table.add_row("5)", "Configure Audio Devices")
    table.add_row("6)", "Generate/Review Configuration Files")
    table.add_row("7)", "Setup librespot Credentials (OAuth)")
    table.add_row("", "")
    table.add_row("", "[bold cyan]── Run ──[/bold cyan]")
    table.add_row("8)", "Setup/Start Systemd Services")
    table.add_row("9)", "Verify Installation")
    table.add_row("", "")
    table.add_row("Q)", "Quit")
    
    console.print(Panel(table, title="Main Menu", border_style="green"))
    console.print()

def demo_status():
    status_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    status_table.add_column("Component", style="cyan")
    status_table.add_column("Status", style="")
    
    components = [
        ("Rust/Cargo", False),
        ("Python venv", False),
        ("CamillaDSP", False),
        ("GUI Backend", False),
        ("librespot", False),
        ("systemd (CamillaDSP)", False),
    ]
    
    for component, installed in components:
        status_text = "[green]✓ Installed[/green]" if installed else "[red]✗ Not Installed[/red]"
        status_table.add_row(component, status_text)
    
    console.print(Panel(status_table, title="System Status", border_style="blue"))
    console.print()

def main():
    console.print("\n[bold green]Audio Helper Demo[/bold green]")
    console.print("[dim]This is a demonstration of the UI - no actual installation will occur[/dim]\n")
    time.sleep(1)
    
    clear_screen()
    print_header()
    demo_status()
    demo_main_menu()
    
    console.print("[cyan]This is an interactive terminal application designed for Ubuntu/Debian systems.[/cyan]")
    console.print("[cyan]On a real system, you would:[/cyan]")
    console.print("  1. Run [yellow]./audio_helper.py[/yellow]")
    console.print("  2. Navigate using numbered menu options")
    console.print("  3. Install CamillaDSP and librespot components")
    console.print("  4. Configure audio devices and services")
    console.print()
    console.print("[dim]This helper automates installation of:[/dim]")
    console.print("[dim]  • CamillaDSP (audio DSP engine)[/dim]")
    console.print("[dim]  • CamillaDSP GUI Backend[/dim]")
    console.print("[dim]  • pycamilladsp libraries[/dim]")
    console.print("[dim]  • librespot (Spotify Connect)[/dim]")
    console.print("[dim]  • Systemd services for auto-start[/dim]")
    console.print()
    console.print("[green]✓ Demo complete![/green]")
    console.print("\n[cyan]Features:[/cyan]")
    console.print("  • [yellow]Batch Install[/yellow] - Run steps 1-4 automatically")
    console.print("  • [yellow]Generate/Review[/yellow] - Review and edit configs with backup")
    console.print("  • [yellow]Start All Services[/yellow] - Start CamillaDSP, GUI, and librespot")
    console.print("  • [yellow]Enhanced Status[/yellow] - Check services, ports, and OAuth credentials")

if __name__ == "__main__":
    main()
