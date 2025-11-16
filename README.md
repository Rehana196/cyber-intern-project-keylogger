# cyber-intern-project-keylogger
🔐 Advanced Encrypted Keylogger PoC | Local C2, AES Encryption, Log Rotation, and Decryptor — Built for Cybersecurity Internship
# 🔐 Encrypted Keylogger – Cybersecurity Internship Project

This is a safe, educational **Encrypted Keylogger Proof-of-Concept (PoC)** created for a cybersecurity internship.  
The project demonstrates how keylogging, encryption, log rotation, and secure exfiltration work in real-world scenarios — but in a **controlled, ethical, and local environment**.

The goal is to analyze keystrokes **ONLY on your own system**, encrypt them using AES-based Fernet, and safely store or exfiltrate them to a local Flask server.

# 🧩 Project Overview (Based on My Actual Workflow)

### ✔ Step 1 — Created a project folder  
I first created a folder in Windows File Explorer named:
Encrypted Keylogger

### ✔ Step 2 — Opened the folder in VS Code  
Right-click folder → “Open with VS Code”.

### ✔ Step 3 — Created the following files inside the folder:
encrypted.py → main keylogger (records + encrypts keystrokes)
exfil_server.py → local Flask server to receive encrypted logs
decryptor.py → decrypts rotated encrypted logs (.enc files)
requirements.txt → required Python modules

### ✔ Step 4 — Ran the Flask server first  
In VS Code terminal:

python exfil_server.py

This starts a **local receiver** on:

http://127.0.0.1:5000/upload

### ✔ Step 5 — Ran the keylogger  
In a new terminal:

python encrypted.py

Then I typed keystrokes in:
- Notepad  
- WhatsApp  
- Chrome  
- VS Code  
- Anywhere on the system  

The keylogger secretly logged:
- The keystrokes  
- Active window title  
- UTC timestamps  
- Encrypted everything  

### ✔ Step 6 — Log rotation & exfiltration  
Every 60 seconds the keylogger:
1. Takes `logs.enc`  
2. Sends it to the Flask server  
3. The server stores it inside `received/` folder  
4. The keylogger renames old logs to:

logs.<timestamp>.enc

### ✔ Step 7 — Decryption  
To read encrypted logs:

python decryptor.py logs.<timestamp>.enc

Example:

python decryptor.py logs.2025xxxxxxx.enc

This prints readable lines:

2025-11-16T14:14:33Z | Notepad | H
2025-11-16T14:14:34Z | Chrome | [ENTER]


# 🧠 How the Project Works (Simple Explanation)

## 1. **encrypted.py**  
This is the keylogger. It:

- Listens to keyboard input  
- Gets the active window name (Notepad, Chrome, etc.)  
- Generates a UTC timestamp  
- Formats the keystroke (letters, CTRL, SHIFT, ENTER…)  
- Encrypts the log using **Fernet (AES-128 + HMAC authentication)**  
- Saves encrypted logs to `logs.enc`  
- Every 60 seconds sends encrypted logs to server  

It also contains:
- A kill-switch file (`kill.signal`) to stop logging safely  
- Log rotation system  
- A background thread for safe exfiltration  

---

## 2. **exfil_server.py**  
A **local Flask server** that receives encrypted logs from the keylogger.

It:
- Accepts POST requests  
- Saves encrypted base64 data into `received/` folder  
- Ensures logs remain unreadable unless decrypted  

This simulates **real cyber exfiltration**, but in a safe environment.

---

## 3. **decryptor.py**  
This script:
- Reads the rotated encrypted log file  
- Loads the `secret.key`  
- Decrypts each line  
- Prints human-readable logs (timestamp + window + keystroke)

---

# 🔐 Encryption Details (Fernet)
Fernet uses:
- AES-128 in CBC mode  
- HMAC-SHA256 for integrity  
- URL-safe Base64 encoding  

So your logs are:
- Encrypted  
- Authenticated  
- Tamper-proof  
- Cannot be read without `secret.key`  

---

# 🧪 What Gets Stored?

### ✔ Files stored on your machine:

logs.enc → current encrypted log
logs.<timestamp>.enc → rotated encrypted logs
received/received_<timestamp>.b64 → exfiltrated logs
secret.key → encryption key

### ❗ These files **must NOT be uploaded to GitHub**

Your `.gitignore` already blocks them:
secret.key
*.enc
*.b64
received/
kill.signal

---

# 📁 What I Uploaded to GitHub

✔ ONLY **source code** is uploaded  
✔ NO terminal output  
✔ NO generated logs  
✔ NO encryption key  
✔ NO decrypted data  
✔ ONLY the safe educational PoC code

Uploaded files:

encrypted.py
exfil_server.py
decryptor.py
requirements.txt
README.md
LICENSE
.gitignore

This keeps the repository ethical & secure.

---

# 🛠 Installation & Running

### 1. Clone the repository
```bash
git clone https://github.com/Rehana196/cyber-intern-project-keylogger
cd cyber-intern-project-keylogger
2. Install dependencies
pip install -r requirements.txt
3. Run the local server
python exfil_server.py
4. Run the encrypted keylogger
python encrypted.py
5. Stop keylogger
Create an empty file:
kill.signal
6. Decrypt logs
python decryptor.py logs.<timestamp>.enc
🖼️ Architecture Diagram
Keyboard Input
      │
      ▼
 encrypted.py
 (Capture → Timestamp → Active Window → Encrypt)
      │
      ▼
 logs.enc
      │ (every 60 sec)
      ▼
 Exfiltration Thread
      │
      ▼
 exfil_server.py (Flask)
      │
      ▼
 received/ (Encrypted .b64 files)
      │
      ▼
 decryptor.py
 (Decrypt → Print readable logs)

🛡️ Ethical Notice
This project is strictly for cybersecurity education.
Use it only on your own systems or with explicit permission.
The author is not responsible for misuse.

📜 License
MIT License + ethical use notice.
