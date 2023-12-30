import subprocess
import os

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

def generate_rsa_key_pair(username):
    """Generates an RSA key pair for the specified username."""
    key_path = "/home/{}/.ssh/id_rsa".format(username)
    if not os.path.exists(key_path):
        subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", key_path, "-q"])

def display_public_key(username):
    """Displays the contents of the public SSH key for the specified username."""
    public_key_path = "/home/{}/.ssh/id_rsa.pub".format(username)
    with open(public_key_path, "r") as f:
        public_key = f.read().strip()
    print("Public SSH key:\n", public_key)

def add_public_key_to_authorized_keys(username):
    """Adds the public key to the authorized_keys file for the specified username."""
    public_key_path = "/home/{}/.ssh/id_rsa.pub".format(username)
    authorized_keys_path = "/home/{}/.ssh/authorized_keys".format(username)
    public_key = open(public_key_path).read()
    with open(authorized_keys_path, "a") as authorized_keys:
        authorized_keys.write(public_key + "\n")

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
    
def setup_ubuntu_server():
    """Performs essential setup tasks, using prompted username."""

    update_packages()

    create_user_prompt = input("Do you want to create a new non-root user? (y/n): ").lower()
    if create_user_prompt == "y":
        username = input("Enter a username for the new user: ")
        create_user(username)
    else:
        username = input("Enter the username to use for SSH key operations: ")

    # RSA key generation and authentication
    if not os.path.exists("/home/{}/.ssh/id_rsa".format(username)):
        generate_rsa_key_pair(username)

    add_public_key_to_authorized_keys(username)
    configure_ssh()

    display_public_key(username)  # Show the generated public key

if __name__ == "__main__":
    setup_ubuntu_server()