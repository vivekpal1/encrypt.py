#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from termcolor import colored
import os, random, sys

def encrypt(key, filename):
    chunksize = 64 * 1024
    outFile = os.path.join(os.path.dirname(filename), "(encrypted)" + os.path.basename(filename))
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = b''

    for i in range(16):
        IV += bytes([random.randint(0, 0xFF)])

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, "rb") as infile:
        with open(outFile, "wb") as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
    outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename[11:]))
    chunksize = 64 * 1024
    with open(filename, "rb") as infile:
        filesize = infile.read(16)
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outFile, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(int(filesize))

def allfiles():
    allFiles = []
    for root, subfiles, files in os.walk(os.getcwd()):
        for names in files:
            allFiles.append(os.path.join(root, names))

    return allFiles

def display_info():
    print(colored('\r\n¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦','green'))
    print(colored('¦','green'), '      Thank You! Please follow me up on GitHub @vivekpal1     ' , colored('¦','green'))
    print(colored('¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦','green'))

display_info()
choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").lower()
password = input("Enter the password: ")

encFiles = allfiles()

if choice == "e":
    file_path = input("Enter the file path to encrypt: ")
    if not os.path.exists(file_path):
        print("The file does not exist")
        sys.exit(0)
    elif os.path.basename(file_path).startswith("(encrypted)"):
        print("%s is already encrypted" % file_path)
        sys.exit()
    else:
        encrypt(SHA256.new(password.encode('utf-8')).digest(), file_path)
        print("Done encrypting %s" % file_path)
        os.remove(file_path)

elif choice == "d":
    file_path = input("Enter the file path to decrypt: ")
    if not os.path.exists(file_path):
        print("The file does not exist")
        sys.exit(0)
    elif not os.path.basename(file_path).startswith("(encrypted)"):
        print("%s is already not encrypted" % file_path)
        sys.exit()
    else:
        decrypt(SHA256.new(password.encode('utf-8')).digest(), file_path)
        print("Done decrypting %s" % file_path)
        os.remove(file_path)

else:
    print("Please choose a valid command.")

sys.exit()
