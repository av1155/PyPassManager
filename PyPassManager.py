import os
import re

import colorama
import pwinput
from cryptography.fernet import Fernet
from tabulate import tabulate


# function to generate encryption key
def write_key(key_file_path):
    # check if key file exists
    if not os.path.exists(key_file_path):
        # generate key
        key = Fernet.generate_key()
        # write key to file
        with open(key_file_path, "wb") as key_file:
            key_file.write(key)
            print(f"{colorama.Fore.GREEN}Key generated.{colorama.Style.RESET_ALL}")
    else:
        print(f"\n{colorama.Fore.GREEN}Key already exists.{colorama.Style.RESET_ALL}")


# function to load encryption key from file
def load_key(key_file_path):
    return open(key_file_path, "rb").read()


# function to set the master password
def set_master_password(master_password_file_path, fernet):
    while True:
        # get user input for password
        password = pwinput.pwinput(
            f"{colorama.Fore.YELLOW}Set the master password (at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character):{colorama.Style.RESET_ALL}\n> "
        )
        # check if password meets requirements
        if len(password) < 8:
            print("\nPassword must be at least 8 characters long.\n")
        elif not re.search(r"[A-Z]", password):
            print("\nPassword must contain at least one uppercase letter.\n")
        elif not re.search(r"[a-z]", password):
            print("\nPassword must contain at least one lowercase letter.\n")
        elif not re.search(r"[0-9]", password):
            print("\nPassword must contain at least one number.\n")
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            print("\nPassword must contain at least one special character.\n")
        else:
            # encrypt password using Fernet object and write to file
            encrypted_password = fernet.encrypt(password.encode()).decode()
            with open(master_password_file_path, "w") as f:
                f.write(encrypted_password)
            break


# function to check if master password is correct
def check_master_password(master_password_file_path, fernet, max_tries=3):
    with open(master_password_file_path, "r") as f:
        encrypted_password = f.read()

    for i in range(max_tries):
        # decrypt stored password and check if input password matches
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        # get user input for password
        input_password = pwinput.pwinput(
            f"{colorama.Fore.YELLOW}\nEnter the master password to access PyPassManager (type 'exit' to quit program)\n(Attempt {i+1} of {max_tries}):{colorama.Style.RESET_ALL}\n> "
        )

        # exit program if user types 'exit'
        if input_password == "exit":
            exit_program()

        if input_password == decrypted_password:
            return True
        else:
            print(
                f"{colorama.Fore.RED}{colorama.Style.BRIGHT}\nIncorrect master password. Please try again.{colorama.Style.RESET_ALL}"
            )

    # exit program if maximum number of tries is reached
    print(
        f"\n{colorama.Fore.RED}{colorama.Style.BRIGHT}Max number of tries ({max_tries}) reached. Exiting program.{colorama.Style.RESET_ALL}"
    )
    exit_program()


# Define a function to view passwords
def view_passwords(passwords_encrypted_file_path, fernet):
    print(f"{colorama.Fore.GREEN}\nViewing passwords...{colorama.Style.RESET_ALL}\n")
    try:
        # Open the encrypted passwords file and read each line
        with open(passwords_encrypted_file_path, "r") as f:
            table_data = [["Website", "Username", "Password"]]
            for line in f.readlines():
                # Split the line into the website, username, and password
                data = line.rstrip()
                website, user, password = data.split("|")
                # Decrypt the password and add the website, username, and decrypted password to the table data
                decrypted_password = fernet.decrypt(password.encode()).decode()
                table_data.append([website, user, decrypted_password])
            # Output the table
            print(tabulate(table_data, headers="firstrow", tablefmt="psql"))

    except FileNotFoundError:
        print(
            f"{colorama.Fore.RED}No passwords found. Please create a password using the 'add' command.{colorama.Style.RESET_ALL}"
        )


# Define a function to add a password
def add_password(passwords_encrypted_file_path, fernet):
    # Prompt the user for a new website, username, and password
    website = input("\nEnter the website (type 'cancel' to quit):\n> ")
    if website == "cancel":
        print(f"{colorama.Fore.RED}Canceled adding password.{colorama.Style.RESET_ALL}")
        return
    username = input("\nEnter the username (type 'cancel' to quit):\n> ")
    if username == "cancel":
        print(f"{colorama.Fore.RED}Canceled adding password.{colorama.Style.RESET_ALL}")
        return
    password = input("\nEnter the password (type 'cancel' to quit):\n> ")
    if password == "cancel":
        print(f"{colorama.Fore.RED}Canceled adding password.{colorama.Style.RESET_ALL}")
        return

    # Encrypt the password and append the new username and encrypted password to the passwords file
    encrypted_password = fernet.encrypt(password.encode()).decode()

    with open(passwords_encrypted_file_path, "a") as f:
        f.write(f"{website} | {username} | {encrypted_password}\n")

    print(f"\n{colorama.Fore.GREEN}Password added.{colorama.Style.RESET_ALL}")


# Define a function to edit a password
def edit_password(passwords_encrypted_file_path, fernet):
    try:
        # Prompt the user for the website of the password they want to edit
        website = input(
            "\nEnter the website for the password you want to edit:\n> "
        ).strip()

        # Open the encrypted password file for reading
        with open(passwords_encrypted_file_path, "r") as f:
            lines = f.readlines()

        found = False
        # Find the line corresponding to the website and replace it with a new encrypted password
        for i, line in enumerate(lines):
            data = line.rstrip().split("|")
            if re.sub(r"\s", "", data[0].lower()) == re.sub(r"\s", "", website.lower()):
                found = True
                # Prompt the user for the new password and encrypt it
                new_password = input("\nEnter the new password:\n> ")
                encrypted_password = fernet.encrypt(new_password.encode()).decode()
                # Replace the old password with the new encrypted password in the file
                lines[i] = f"{data[0]} | {data[1]} | {encrypted_password}\n"
                with open(passwords_encrypted_file_path, "w") as f:
                    f.write("".join(lines))
                print(
                    f"{colorama.Fore.GREEN}Password edited successfully.{colorama.Style.RESET_ALL}"
                )
                break

        if not found:
            print(
                f"{colorama.Fore.RED}No password found for that website.{colorama.Style.RESET_ALL}"
            )

    except FileNotFoundError:
        print(
            f"{colorama.Fore.RED}No passwords found. Please create a password using the 'add' command.{colorama.Style.RESET_ALL}"
        )


# Define a function to delete a password
def delete_password(passwords_encrypted_file_path, fernet):
    try:
        # Prompt the user for the website of the password they want to delete
        website = input(
            "\nEnter the website for the password you want to delete:\n> "
        ).strip()

        # Open the encrypted password file for reading
        with open(passwords_encrypted_file_path, "r") as f:
            lines = f.readlines()

        found = False
        # Find the line corresponding to the website and delete it
        for i, line in enumerate(lines):
            data = line.rstrip().split("|")
            if re.sub(r"\s", "", data[0].lower()) == re.sub(r"\s", "", website.lower()):
                found = True
                del lines[i]
                # Write the updated password file without the deleted line
                with open(passwords_encrypted_file_path, "w") as f:
                    f.write("".join(lines))
                print(
                    f"{colorama.Fore.GREEN}Password deleted successfully.{colorama.Style.RESET_ALL}"
                )
                break

        if not found:
            print(
                f"{colorama.Fore.RED}No password found for that website.{colorama.Style.RESET_ALL}"
            )

    except FileNotFoundError:
        print(
            f"{colorama.Fore.RED}No passwords found. Please create a password using the 'add' command.{colorama.Style.RESET_ALL}"
        )


# Function to exit the program
def exit_program():
    print(f"{colorama.Fore.GREEN}\nExiting the program...{colorama.Style.RESET_ALL}")
    exit()


# Define a function to handle the main program logic
def main():
    # Set paths for key.key, passwords.encrypted, and master_password.txt files.
    key_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "key.key")
    passwords_encrypted_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "passwords.encrypted"
    )
    master_password_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "master_password.txt"
    )

    # Generate and load the key from the key file if it doesn't already exist.
    write_key(key_file_path)
    key = load_key(key_file_path)

    # Create the Fernet object using the key
    fernet = Fernet(key)

    # Check if passwords.encrypted file exists
    try:
        # if master_password.txt does not exist, but passwords.encrypted file exists... delete passwords.encrypted file.
        if os.path.exists(passwords_encrypted_file_path) and not os.path.exists(
            master_password_file_path
        ):
            os.remove(passwords_encrypted_file_path)
            print(
                f"\n{colorama.Fore.RED}{colorama.Style.BRIGHT}Master password file not found. Deleting existing passwords file...{colorama.Style.RESET_ALL}\n"
            )

        # if master password file doesn't exist, prompt user to set one
        if not os.path.exists(master_password_file_path):
            set_master_password(master_password_file_path, fernet)

    except FileNotFoundError:
        os.remove(passwords_encrypted_file_path)
        print(
            f"\n{colorama.Fore.RED}{colorama.Style.BRIGHT}Master password file not found. Deleting existing passwords file...{colorama.Style.RESET_ALL}\n"
        )
        set_master_password(master_password_file_path, fernet)

    # Flag to keep track of whether the user has entered the correct master password
    password_entered = False

    while True:
        if not password_entered:
            # Check the master password
            if check_master_password(master_password_file_path, fernet):
                password_entered = True
            else:
                print(
                    f"{colorama.Fore.RED}{colorama.Style.BRIGHT}Incorrect master password. Please try again.{colorama.Style.RESET_ALL}"
                )
                continue

        # Prompt the user for the program mode
        program_mode = input(
            f"{colorama.Fore.BLUE}{colorama.Style.BRIGHT}\nEnter... \n- 'view' to view passwords.\n- 'add' to add a password.\n- 'edit' to edit a password.\n- 'delete' to delete a password.\n- 'exit' to quit.{colorama.Style.RESET_ALL}\n> "
        ).lower()

        # Determine which mode the user has selected and call the appropriate function
        if program_mode == "view":
            view_passwords(passwords_encrypted_file_path, fernet)

        elif program_mode == "add":
            add_password(passwords_encrypted_file_path, fernet)

        elif program_mode == "edit":
            edit_password(passwords_encrypted_file_path, fernet)

        elif program_mode == "delete":
            delete_password(passwords_encrypted_file_path, fernet)

        elif program_mode == "exit":
            exit_program()

        else:
            print(
                f"\n{colorama.Fore.RED}{colorama.Style.BRIGHT}Invalid input. Please try again.{colorama.Style.RESET_ALL}"
            )


# Check if this script is being run as the main program
if __name__ == "__main__":
    # Call the main function to start the program
    main()
