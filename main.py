import getpass
import hashlib
from config import *
import psycopg2
import encrypt_funcs


def listfunc(decrypt, dbcursor):
    dbcursor.execute('SELECT * FROM ' + DB_TABLE_NAME)

    rows = dbcursor.fetchall()

    if rows:
        for row in rows:
            print("-" * 20)
            print("Website:", row[0])
            print("Username:", row[1])

            if decrypt:

                print("Password:",
                      encrypt_funcs.decrypt(row[2], MASTER_PWD_HASH))

            else:
                print("Password:", row[2])
        print("-" * 20)

    else:

        print("No Records Found!")


def list_encrypted_records(dbcursor):
    listfunc(False, dbcursor)


def list_decrypted_records(dbcursor):
    user_pwd = getpass.getpass("\nEnter Master Password:").encode()
    if hashlib.sha256(user_pwd).hexdigest() == MASTER_PWD_HASH:
        listfunc(True, dbcursor)
    else:
        print("Sorry, wrong password!")


def add_record(dbcursor):
    website = input("\nWebsite: ")
    name = input("Name: ")
    password = input("Password: ")

    dbcursor.execute(f'INSERT INTO {DB_TABLE_NAME} VALUES (%s, %s, %s)',
                     (website, name,
                      encrypt_funcs.encrypt(password, MASTER_PWD_HASH)))

    print("Record Successfully Added!\n")


if __name__ == '__main__':

    print("\nSQL Password Manager")

    user_master = getpass.getpass("\nEnter Master Password:").encode()

    if hashlib.sha256(user_master).hexdigest() == MASTER_PWD_HASH:

        connection = psycopg2.connect(dbname=DB_NAME, user=DB_UNAME,
                                      password=DB_PWD)

        cursor = connection.cursor()

        print("1. List Encrypted Records")
        print("2. List Decrypted Records")
        print("3. Add Record\n")

        userChoice = input("Enter Option: ")
        if userChoice == "1":
            list_encrypted_records(cursor)
        elif userChoice == "2":
            list_decrypted_records(cursor)
        elif userChoice == "3":
            add_record(cursor)
        else:
            print("Invalid Option!")

        connection.commit()
        connection.close()

    else:
        print("Wrong Master Password!")
