from utils import subprocess, os

def generate_rsa_key_pair(username):
    """Generates an RSA key pair for the specified username, creating the .ssh directory if needed."""

    # Create .ssh directory if it doesn't exist
    home_dir = "/home/{}".format(username)
    ssh_dir = os.path.join(home_dir, ".ssh")
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir, mode=0o700)  # Set secure permissions

    # Generate the key pair
    key_path = os.path.join(ssh_dir, "id_rsa")
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
