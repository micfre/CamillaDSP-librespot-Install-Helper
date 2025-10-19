"""
Command execution utility with proper error handling and output capture
"""

import subprocess
import sys
from typing import Tuple, Optional, List
from rich.console import Console

console = Console()


def run_command(
    cmd: List[str],
    check: bool = True,
    capture: bool = False,
    shell: bool = False,
    sudo: bool = False,
    description: str = ""
) -> Tuple[int, str, str]:
    """
    Execute a command with proper error handling
    
    Args:
        cmd: Command to execute as list
        check: Raise exception on non-zero exit
        capture: Capture stdout/stderr
        shell: Run as shell command
        sudo: Prepend sudo to command
        description: Description to display
    
    Returns:
        (return_code, stdout, stderr)
    """
    if sudo and cmd[0] != 'sudo':
        cmd = ['sudo'] + cmd
    
    if description:
        console.print(f"[cyan]→[/cyan] {description}")
    
    try:
        if shell:
            cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
            result = subprocess.run(
                cmd_str,
                shell=True,
                capture_output=capture,
                text=True
            )
        else:
            result = subprocess.run(
                cmd,
                capture_output=capture,
                text=True
            )
        
        if check and result.returncode != 0:
            error_msg = f"Command failed with exit code {result.returncode}"
            if capture and result.stderr:
                error_msg += f"\nError: {result.stderr}"
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
        
        return result.returncode, result.stdout or "", result.stderr or ""
    
    except subprocess.CalledProcessError as e:
        console.print(f"[red]✗ Error executing command: {' '.join(cmd) if isinstance(cmd, list) else cmd}[/red]")
        if capture and e.stderr:
            console.print(f"[red]{e.stderr}[/red]")
        if check:
            raise
        return e.returncode, e.stdout or "", e.stderr or ""
    except Exception as e:
        console.print(f"[red]✗ Unexpected error: {e}[/red]")
        if check:
            raise
        return 1, "", str(e)


def command_exists(command: str) -> bool:
    """Check if a command exists in PATH"""
    returncode, _, _ = run_command(
        ['which', command],
        check=False,
        capture=True
    )
    return returncode == 0
