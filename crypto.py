from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_file(file_path):
    key = load_key()
    cipher = Fernet(key)

    with open(file_path, "rb") as f:
        encrypted_data = cipher.encrypt(f.read())

    encrypted_path = file_path + ".enc"
    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    return encrypted_path

def decrypt_file(file_path):
    key = load_key()
    cipher = Fernet(key)

    with open(file_path, "rb") as f:
        decrypted_data = cipher.decrypt(f.read())

    decrypted_path = file_path.replace(".enc", ".dec")
    with open(decrypted_path, "wb") as f:
        f.write(decrypted_data)

    return decrypted_path