import subprocess
def configure_ssh():
    """Configures SSH with secure settings using UFW."""

    # Disable password authentication
    subprocess.run(["sudo", "sed", "-i", "s/PasswordAuthentication yes/PasswordAuthentication no/", "/etc/ssh/sshd_config"])

    # Disable root login
    subprocess.run(["sudo", "sed", "-i", "s/#PermitRootLogin yes/PermitRootLogin no/", "/etc/ssh/sshd_config"])

    # Implement rate limiting (using UFW)
    subprocess.run(["sudo", "ufw", "limit", "ssh/tcp", "6/min"])

    # Allow SSH only from private IP ranges (using UFW)
    subprocess.run(["sudo", "ufw", "allow", "from", "10.0.0.0/8", "to", "any", "port", "22"])
    subprocess.run(["sudo", "ufw", "allow", "from", "172.16.0.0/12", "to", "any", "port", "22"])
    subprocess.run(["sudo", "ufw", "allow", "from", "192.168.0.0/16", "to", "any", "port", "22"])

    # Deny all other SSH traffic (using UFW)
    subprocess.run(["sudo", "ufw", "deny", "22"])

    # Enable UFW
    subprocess.run(["sudo", "ufw", "enable"])

    # Restart SSH service
    subprocess.run(["sudo", "systemctl", "restart", "ssh"])
def setup_ubuntu_server():
    """Performs essential setup tasks on a new Ubuntu server."""

    # 1. Update package lists and upgrade packages
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "upgrade", "-y"])

    # 2. Create a non-root user with sudo privileges
    username = input("Enter a username for the new user: ")
    subprocess.run(["sudo", "useradd", "-m", "-s", "/bin/bash", username])
    subprocess.run(["sudo", "adduser", username, "sudo"])

    # 3. Configure SSH (optional)
    if input("Do you want to configure SSH? (y/n): ").lower() == "y":
        # Allow public key authentication, disable password authentication, and other security measures
        configure_ssh()
    
    # 4. Install essential packages
    essential_packages = ["python3", "python3-pip", "git", "ufw", "fail2ban"]  # Add more as needed
    subprocess.run(["sudo", "apt", "install", "-y"] + essential_packages)

    # 5. Set up a firewall (optional)
    if input("Do you want to enable UFW firewall? (y/n): ").lower() == "y":
        subprocess.run(["sudo", "ufw", "enable"])
        # Allow necessary ports (SSH, HTTP, HTTPS, etc.)

    # 6. Install additional software (optional)
    # Web server (Apache or Nginx), database (MySQL, PostgreSQL), etc.

if __name__ == "__main__":
    setup_ubuntu_server()