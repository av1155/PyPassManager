# PyPassManager

PyPassManager is a command-line program that allows you to securely store and manage your passwords. It uses the Fernet encryption module from the Cryptography library to encrypt and decrypt passwords.

## Requirements

To use PyPassManager, you must have Python 3.x and the Cryptography library installed on your computer. You can install the library via pip:

`pip install cryptography`

## File System

PyPassManager utilizes a file-based system for secure password management:

1. Key File (key.key):

- When you run the PyPassManager for the first time, it generates an encryption key (Fernet key).
- This key is then written to a file named key.key.

2. Master Password File (master_password.txt):

- If the master_password.txt file does not exist, it prompts you to set a master password.
- The master password is required to access the PyPassManager program.
- The master password is stored in an encrypted form within this file.

3. Encrypted Passwords File (passwords.encrypted):

- This file stores all the passwords in an encrypted format.
- When you add a password, it is encrypted using the Fernet key and then stored in this file.
- Each line in this file contains the website, username, and the encrypted password, separated by a vertical bar `|`.

4. File Paths:

- The script uses specific file paths to locate these files, such as key_file_path, passwords_encrypted_file_path, and master_password_file_path.
- These paths are constructed based on the script's location.

5. File Existence Checks:

- The script checks for the existence of these files:
  - If the passwords.encrypted file exists but the master_password.txt file doesn't, it deletes the passwords.encrypted file. This prevents unauthorized access.
  - If neither the passwords.encrypted nor the master_password.txt file exists, it proceeds to create them.

6. Encryption and Decryption:

- The Fernet key stored in key.key is used for both encryption and decryption.
- When viewing, editing, or deleting passwords, the script decrypts the passwords from the passwords.encrypted file using the Fernet key.
- When adding a password, it encrypts the password with the Fernet key before appending it to the passwords.encrypted file.

These file-based operations ensure that the passwords are stored securely in an encrypted format, and the master password is used to control access to the program and the decrypted passwords.

## Usage

To use PyPassManager, run the program with the following command:

`python pypassmanager.py`

The program will first check if a master password has been set. If not, you will be prompted to set one. The master password must be at least 8 characters long, and must contain at least one uppercase letter, one lowercase letter, one number, and one special character.

After setting the master password, you will be prompted to enter it to access the program. Once you are logged in, you can use the following commands:

- view: view all stored passwords
- add: add a new password
- edit: edit an existing password
- delete: delete an existing password
- exit: exit the program

## Adding a Password

To add a new password, use the add command. You will be prompted to enter a username and a password. The password must be at least 8 characters long, and must contain at least one uppercase letter, one lowercase letter, one number, and one special character.

## Viewing Passwords

To view all stored passwords, use the view command. The program will display the username and password for each stored password.

## Editing a Password

To edit an existing password, use the edit command. You will be prompted to enter the username for the password you want to edit, and then to enter the new password. The new password must meet the same requirements as when adding a password.

## Deleting a Password

To delete an existing password, use the delete command. You will be prompted to enter the username for the password you want to delete.

## Security

PyPassManager uses the Fernet encryption module from the Cryptography library to encrypt and decrypt passwords. The encryption key is stored in a file named key.key, which is generated automatically if it doesn't already exist. The key is used to create a Fernet object, which is then used to encrypt and decrypt passwords.

The encrypted passwords are stored in a file named passwords.encrypted. This file is also created automatically if it doesn't already exist. The file is in plain text format, with each line containing the username and encrypted password for a single password, separated by a vertical bar `|`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
