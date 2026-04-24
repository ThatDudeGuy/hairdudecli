#!/usr/bin/python3
import subprocess

def try_run_command(command):
    try:
        subprocess.run(command)
    except Exception as e:
        print("Install failure...")
        print(f"Failed to run command '{command}' | {e}")
        raise

commands = [
    "cp -r ./hairdudecli /usr/local/lib/",
    "cp ./hdcli.py /usr/local/bin/hdcli",
    "cp ./auto_complete/hdcli /usr/share/bash-completion/completions/hdcli",
]

for command in commands:
    try_run_command(command)

print("Successfully installed hdcli!")