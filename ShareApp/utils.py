from cryptography.fernet import Fernet
import base64
import hashlib
import os

ALLOWED_EXTENSIONS = ['pptx', 'docx', 'xlsx']
# Generate a key (only once, then store it securely)
def generate_key():
    return base64.urlsafe_b64encode(hashlib.sha256("#$&^(&^#&*@*#&*&#@*^#(#@))".encode()).digest())

# Encrypt the user data (such as user id or email) to generate a secure URL
def encrypt_url(data):
    key = generate_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

# Decrypt function (to be used later when needed)
def decrypt_url(encrypted_data):
    key = generate_key()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data.encode()).decode()
    return decrypted_data


def is_valid_file(file_name):
    ext = os.path.splitext(file_name)[1][1:].lower()
    return ext in ALLOWED_EXTENSIONS
