#!/usr/bin/python3
import subprocess
import pathlib

def try_run_command(command):
    try:
        subprocess.run(command.split(','))
        print(" ".join(command))
    except Exception as e:
        raise Exception(f"Failed to run command '{command}'") from e

cwd = pathlib.Path.cwd()

commands = [
    ["cp", "-r", f"{cwd}/hairdudecli/", "/usr/local/lib/"],
    ["cp", f"{cwd}/hdcli.py", "/usr/local/bin/hdcli"],
    ["chmod", "+x", "/usr/local/bin/hdcli"],
    ["cp", f"{cwd}/auto_complete/hdcli", "/usr/share/bash-completion/completions/hdcli"],
]

for command in commands:
    try_run_command(command)

print("Successfully installed hdcli!")