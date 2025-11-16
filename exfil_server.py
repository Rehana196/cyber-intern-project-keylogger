from flask import Flask, request, jsonify
import base64
import os
from datetime import datetime

app = Flask(__name__)
STORE_DIR = "received"
os.makedirs(STORE_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    data = request.form.get("file")
    if not data:
        return jsonify({"error": "no file"}), 400
    try:
        raw = base64.b64decode(data)
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        fname = os.path.join(STORE_DIR, f"received_{ts}.b64")
        with open(fname, "wb") as f:
            f.write(raw)
        return jsonify({"status": "ok", "saved": fname}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
