import subprocess
def configure_ssh():
    """Configures SSH with secure settings."""

    # Allow public key authentication
    subprocess.run(["sudo", "sed", "-i", "s/#PubkeyAuthentication yes/PubkeyAuthentication yes/", "/etc/ssh/sshd_config"])

    # Disable password authentication
    subprocess.run(["sudo", "sed", "-i", "s/PasswordAuthentication yes/PasswordAuthentication no/", "/etc/ssh/sshd_config"])

    # Change SSH port (optional)
    new_ssh_port = input("Enter a new SSH port (default: 22): ") or "22"
    subprocess.run(["sudo", "sed", "-i", "s/#Port 22/Port " + new_ssh_port + "/", "/etc/ssh/sshd_config"])
 
  # Implement rate limiting (using iptables)
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", "22", "-m", "limit", "--limit", "6/min", "--limit-burst", "10", "-j", "ACCEPT"])

    # Allow SSH only from private IP ranges
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", "22", "-s", "10.0.0.0/8", "-j", "ACCEPT"])
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", "22", "-s", "172.16.0.0/12", "-j", "ACCEPT"])
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", "22", "-s", "192.168.0.0/16", "-j", "ACCEPT"])
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", "22", "-j", "DROP"])  # Drop all other SSH traffic

    # Make iptables rules persistent
    subprocess.run(["sudo", "sh", "-c", "iptables-save > /etc/iptables/rules.v4"])

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