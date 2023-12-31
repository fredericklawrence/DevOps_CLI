import os
from package_management import update_packages, install_packages
from user_management import create_user
from ssh_key_management import generate_rsa_key_pair, display_public_key, add_public_key_to_authorized_keys
from ssh_configuration import check_and_install_ssh_server, configure_ssh

class ServerSetup:
    def __init__(self):
        create_user_prompt = input("Do you want to create a new non-root user? (y/n): ").lower()
        if create_user_prompt == "y":
            self.username = input("Enter a username for the new user: ")
            self.create_user()  # Create the user directly
        else:
            self.username = input("Enter the username to use for SSH key operations: ")

    def update_packages(self):
        update_packages()

    def generate_rsa_key_pair(self):
        generate_rsa_key_pair(self.username)

    def display_public_key(self):
        display_public_key(self.username)

    def add_public_key_to_authorized_keys(self):
        add_public_key_to_authorized_keys(self.username)

    def check_and_install_ssh_server(self):
        check_and_install_ssh_server()

    def configure_ssh(self):
        configure_ssh(self.username)


    def setup(self):
        self.update_packages()

        # RSA key generation and authentication
        self.generate_rsa_key_pair()
        self.add_public_key_to_authorized_keys()

        self.check_and_install_ssh_server()

        self.configure_ssh()

        self.display_public_key()

if __name__ == "__main__":
    setup = ServerSetup()  # Initialize
    setup.setup()