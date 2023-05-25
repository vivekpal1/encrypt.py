# Install cryptsetup 
# sudo pacman -S cryptsetup

import subprocess
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.hazmat.primitives import hashes, serialization

def encrypt_disk_partition(partition, public_key_file):
    command = f"cryptsetup luksFormat {partition}"
    subprocess.run(command, shell=True, check=True)

    command = f"cryptsetup open {partition} {get_mapper_name(partition)}"
    subprocess.run(command, shell=True, check=True)

    encrypt_key_with_public_key(public_key_file, get_mapper_name(partition))

def decrypt_disk_partition(partition, private_key_file):
    mapper_name = get_mapper_name(partition)

    command = f"cryptsetup close {mapper_name}"
    subprocess.run(command, shell=True, check=True)

    decrypt_key_with_private_key(private_key_file, mapper_name)

def encrypt_key_with_public_key(public_key_file, mapper_name):
    with open(public_key_file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    shared_key = ec.generate_private_key(ec.SECP256R1())
    encrypted_key = public_key.encrypt(
        shared_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ),
        ecIES(hashes.SHA256())
    )

    # Store the encrypted key securely for later decryption

def decrypt_key_with_private_key(private_key_file, mapper_name):
    with open(private_key_file, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    # Retrieve the encrypted key and decrypt it using the private key

def get_mapper_name(partition):
    partition_name = partition.split("/")[-1]
    mapper_name = f"crypt-{partition_name}"
    return mapper_name

def main():
    partition = input("Enter the partition to encrypt/decrypt (e.g., /dev/sda1): ")
    operation = input("Enter the operation (encrypt/decrypt): ")

    if operation.lower() == "encrypt":
        public_key_file = input("Enter the path to the public key file: ")
        encrypt_disk_partition(partition, public_key_file)
    elif operation.lower() == "decrypt":
        private_key_file = input("Enter the path to the private key file: ")
        decrypt_disk_partition(partition, private_key_file)
    else:
        print("Invalid operation.")

if __name__ == "__main__":
    main()
