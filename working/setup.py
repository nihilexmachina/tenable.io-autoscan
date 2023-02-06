import os
import subprocess
import pip

def setup():
    # Check if the .env file exists
    if not os.path.exists('.env'):
        # Get the secret key, access key, and target group values from the user
        access_key = input("Enter the value for the TIO_ACCESS_KEY: ")
        secret_key = input("Enter the value for the TIO_SECRET_KEY: ")
        target_group = input("Enter the value for the TARGET_GROUP: ")

        # Create the .env file
        with open('.env', 'w') as f:
            f.write(f"TIO_ACCESS_KEY='{access_key}'\n")
            f.write(f"TIO_SECRET_KEY='{secret_key}'\n")            
            f.write(f"TARGET_GROUP='{target_group}'\n")

# Check if the requirements.txt file exists
if os.path.exists('requirements.txt'):
    # Get the set of installed packages
    installed_packages = set(subprocess.run(['pip', 'freeze'], capture_output=True, text=True).stdout.strip().split('\n'))

    # Get the set of dependencies
    with open('requirements.txt', 'r') as f:
        dependencies = set(line.strip() for line in f)

    # Calculate the set of dependencies to install
    dependencies_to_install = dependencies - installed_packages

    # Install dependencies if they do not already exist
    if dependencies_to_install:
        subprocess.call(['pip', 'install'] + list(dependencies_to_install))
    else:
        print("All dependencies are already installed.")
        
if __name__ == '__main__':
    setup()
