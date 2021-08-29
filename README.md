# sql-password-manager
## Description:
This is a secure username and password manager that stores salted and hashed passwords in a PostgreSQL database. The encryption used relies on the PBKDF2 Key Derivation algorithm
that is derived from a master password of your choice.

### Note:
Hash your master password of choice and store it's SHA256 hash in the config.py file. Next, once you've setup your PostgreSQL database fill in the necessary information in config.py
as specified.

