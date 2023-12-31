from package_management import update_packages, install_packages
from user_management import create_user
from ssh_key_management import generate_rsa_key_pair, display_public_key, add_public_key_to_authorized_keys
from ssh_configuration import check_and_install_ssh_server, configure_ssh

class ConfigurationContext:
    def __init__(self, choice):
        self.choice = choice

def get_configuration_context():
    global choice  # Assuming choice is still a global variable for now
    return ConfigurationContext(choice)

class ServerSetup:
    def __init__(self):
        while True:
            print("Main Menu:")
            print("1. Initial Setup")
            print("2. Normal Operations")
            choice = input("Enter your choice (1 or 2): ")
            if choice in ["1", "2"]:
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

        self.choice = choice

    def get_username(self):
        while True:
            create_user_prompt = input("Do you want to create a new non-root user? (y/n): ").lower()
            if create_user_prompt == "y":
                self.username = input("Enter a username for the new user: ")
                create_user(self.username)
                break  # exit the loop after setting a valid username
            else:
                self.username = input("Enter the username to use for SSH key operations: ")
                break  # exit the loop after setting a valid username            
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
        context = ConfigurationContext(self.choice)  # Pass choice directly
        self.get_username()  # Call get_username before other methods
        self.update_packages()
        self.check_and_install_ssh_server() 

        # RSA key generation and authentication
        self.generate_rsa_key_pair()
        self.add_public_key_to_authorized_keys()

        if context.choice == "1":
            self.configure_ssh()

        self.display_public_key()

if __name__ == "__main__":
    setup = ServerSetup()  # Initialize
    setup.setup()