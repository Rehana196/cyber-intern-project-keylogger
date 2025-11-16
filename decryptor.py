import base64
from cryptography.fernet import Fernet
import sys

KEY_FILE = "secret.key"

def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

def decrypt_b64_file(b64file_path):
    key = load_key()
    fernet = Fernet(key)
    with open(b64file_path, "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            token = base64.urlsafe_b64decode(line)
            try:
                plain = fernet.decrypt(token)
                print(plain.decode("utf-8", errors="replace"))
            except Exception as e:
                print("[DECRYPT ERROR]", e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decryptor.py logs.enc")
    else:
        decrypt_b64_file(sys.argv[1])
