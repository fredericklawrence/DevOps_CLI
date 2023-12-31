from utils import subprocess, os

def check_and_install_ssh_server():
    """Checks if the SSH server is installed, installing it if necessary."""
    process = subprocess.run(["which", "sshd"], capture_output=True, text=True)
    if process.returncode != 0:
        print("SSH server not found. Installing...")
        subprocess.run(["sudo", "apt", "install", "-y", "openssh-server"])
        print("SSH server installed successfully.")
    else:
        print("SSH server already installed.")

def configure_ssh(username):
    """Configures SSH with secure settings and creates .ssh directory if needed."""

    # Add lines to sshd_config
    with open("/etc/ssh/sshd_config", "a") as f:
        f.write("\nPermitRootLogin no\n")
        f.write("StrictModes yes\n")
        f.write("MaxAuthTries 6\n")
        f.write("MaxSessions 10\n")
        f.write("PasswordAuthentication no\n")

    # Disable PAM authentication (if not already disabled)
    subprocess.run(["sudo", "sed", "-i", "s/^UsePAM yes/UsePAM no/", "/etc/ssh/sshd_config"])

    # Create .ssh directory if it doesn't exist
    home_dir = "/home/{}".format(username)
    ssh_dir = os.path.join(home_dir, ".ssh")
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir, mode=0o700)  # Set secure permissions

    # Implement rate limiting (using UFW)
    subprocess.run(["sudo", "ufw", "limit", "ssh/tcp", "6/min"])

    # Allow SSH only from private IP ranges (adjust as needed)
    subprocess.run(["sudo", "ufw", "allow", "from", "10.0.0.0/8", "to", "any", "port", "22"])
    subprocess.run(["sudo", "ufw", "allow", "from", "172.16.0.0/12", "to", "any", "port", "22"])
    subprocess.run(["sudo", "ufw", "allow", "from", "192.168.0.0/16", "to", "any", "port", "22"])

    # Deny all other SSH traffic
    subprocess.run(["sudo", "ufw", "deny", "22"])

    # Enable UFW
    subprocess.run(["sudo", "ufw", "enable"])

    # Restart SSH service
    subprocess.run(["sudo", "systemctl", "restart", "ssh"])
