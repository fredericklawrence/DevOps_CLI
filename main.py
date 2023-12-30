import subprocess
import os

def generate_rsa_key_pair():
    """Generates an RSA key pair for SSH authentication."""
    subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", "/home/your_user/.ssh/id_rsa", "-q"])

def display_public_key():
    """Displays the contents of the public SSH key."""
    with open("/home/your_user/.ssh/id_rsa.pub", "r") as f:
        public_key = f.read().strip()
    print("Public SSH key:\n", public_key)

def add_public_key_to_authorized_keys():
    """Adds the public key to the authorized_keys file."""
    public_key = open("/home/your_user/.ssh/id_rsa.pub").read()
    authorized_keys = open("/home/your_user/.ssh/authorized_keys", "a")
    authorized_keys.write(public_key + "\n")
    authorized_keys.close()

def update_packages():
    """Updates package lists and upgrades packages."""
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "upgrade", "-y"])

def create_user(username):
    """Creates a new non-root user with sudo privileges."""
    subprocess.run(["sudo", "useradd", "-m", "-s", "/bin/bash", username])
    subprocess.run(["sudo", "adduser", username, "sudo"])

def install_packages(packages):
    """Installs specified packages."""
    subprocess.run(["sudo", "apt", "install", "-y"] + packages)

def configure_ssh():
    """Configures SSH with secure settings using UFW."""

    # Ensure only public key authentication
    subprocess.run(["sudo", "sed", "-i", "s/^PasswordAuthentication yes/PasswordAuthentication no/", "/etc/ssh/sshd_config"])
    subprocess.run(["sudo", "sed", "-i", "s/^PubkeyAuthentication yes/PubkeyAuthentication yes/", "/etc/ssh/sshd_config"])

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

    update_packages()

    # 3. Create a non-root user with sudo privileges
    if input("Do you want to create a new non-root user? (y/n): ").lower() == "y":
        username = input("Enter a username for the new user: ")
        create_user(username)
    else:
        username = input("Enter the username to use for SSH key operations: ")

    
    # 4. Configure SSH (optional)
    if input("Do you want to configure SSH? (y/n): ").lower() == "y":
        # Allow public key authentication, disable password authentication, and other security measures
        if not os.path.exists("/home/{}/.ssh/id_rsa".format(username)):
            generate_rsa_key_pair(username)

            add_public_key_to_authorized_keys(username)
            configure_ssh()

            display_public_key(username)  # Show the generated public key

    # Install essential packages (example)
    essential_packages = ["python3", "python3-pip", "git", "ufw", "fail2ban"]
    install_packages(essential_packages)

    # Web server (Apache or Nginx), database (MySQL, PostgreSQL), etc.

if __name__ == "__main__":
    setup_ubuntu_server()