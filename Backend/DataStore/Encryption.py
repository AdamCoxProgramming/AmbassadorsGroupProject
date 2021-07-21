from cryptography.fernet import Fernet
from Backend.RelativeRootPath import getRelativeRootPath

def generate_key():
    #Generates a key and saves it into a file
    key = Fernet.generate_key()
    with open(getRelativeRootPath()+"Backend\secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    #Load the previously generated key
    return open(getRelativeRootPath()+"Backend\secret.key", "rb").read()

def encryptString(message):
    #Encrypts a message
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message.decode()

def decryptString(encrypted_message):
    #Decrypts an encrypted message
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())
    return decrypted_message.decode()
