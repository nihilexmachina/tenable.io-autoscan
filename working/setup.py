#for your initial setup -this will create the .env
#only keeping it separate as a just in case for simplicity down the road

import os
import subprocess

def setup():
    # Check if the .env file exists
    if not os.path.exists('.env'):
        # Get the secret key, access key, and target group values from the user
        secret_key = input("Enter the value for the TIO_SECRET_KEY: ")
        access_key = input("Enter the value for the TIO_ACCESS_KEY: ")
        target_group = input("Enter the value for the TARGET_GROUP: ")

        # Create the .env file
        with open('.env', 'w') as f:
            f.write(f"TIO_SECRET_KEY='{secret_key}'\n")
            f.write(f"TIO_ACCESS_KEY='{access_key}'\n")
            f.write(f"TARGET_GROUP='{target_group}'\n")

    # Install dependencies
    subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

if __name__ == '__main__':
    setup()
