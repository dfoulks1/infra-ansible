# Vaulted values

Ansible vault is the baked in method for encrypting variables in ansible. For now we can just use LP to manage the vault key, another option would be:
* to gpg encrypt the vault key file
* wrap the decryption process in a script that spits out the password
* set the global vault_password_file to the decryption script.
