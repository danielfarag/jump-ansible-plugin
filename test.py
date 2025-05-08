import os
import subprocess

def main():
    ip = "10.0.2.218"
    known_hosts_path = os.path.expanduser("~/.ssh/known_hosts")

    # Build a clean single-line shell command
    cmd = f'if ! ssh-keygen -F "{ip}" > /dev/null; then ssh-keyscan -H "{ip}" >> "{known_hosts_path}"; fi'

    # Run the command
    subprocess.run(cmd, shell=True, check=True)

main()
