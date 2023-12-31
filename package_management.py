from utils import subprocess

def update_packages():
    """Updates package lists and upgrades packages."""
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "upgrade", "-y"])

def install_packages(packages):
    """Installs specified packages."""
    subprocess.run(["sudo", "apt", "install", "-y"] + packages)