# PyPassManager

PyPassManager is a command-line program that allows you to securely store and manage your passwords. It uses the Fernet encryption module from the Cryptography library to encrypt and decrypt passwords.

## Requirements

To use PyPassManager, you must have Python 3.x and the Cryptography library installed on your computer. You can install the library via pip:

`pip install cryptography`

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

The encrypted passwords are stored in a file named passwords.encrypted. This file is also created automatically if it doesn't already exist. The file is in plain text format, with each line containing the username and encrypted password for a single password, separated by a vertical bar (|).
