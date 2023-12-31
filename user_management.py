from utils import subprocess

def create_user(username):
    """Creates a new non-root user with sudo privileges."""
    subprocess.run(["sudo", "useradd", "-m", "-s", "/bin/bash", username])
    subprocess.run(["sudo", "adduser", username, "sudo"])
