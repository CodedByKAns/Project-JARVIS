import os
import time
import threading
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from flask import Flask, send_file, request, render_template_string
import qrcode
from PIL import Image
import zipfile
import socket
import tempfile
from plyer import notification
import platform
import subprocess
import requests
import traceback

# Jarvis Integration (Optional)
try:
    from core.registry import register_command
    from voice.tts import speak
except:
    def register_command(*args, **kwargs):
        def decorator(func): return func
        return decorator
    def speak(msg): print("Jarvis:", msg)

# === Paths ===
TEMP_DIR = tempfile.gettempdir()
ZIP_FILE = os.path.join(TEMP_DIR, "shared_files.zip")
UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop", "by jarvis")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === Flask Setup ===
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server_thread = None

# === Notify and Open File ===
def show_notification(title, message):
    try:
        notification.notify(title=title, message=message, timeout=5)
    except:
        pass

def open_file(filepath):
    try:
        if platform.system() == "Windows":
            os.startfile(filepath)
        elif platform.system() == "Darwin":
            subprocess.call(["open", filepath])
        else:
            subprocess.call(["xdg-open", filepath])
    except Exception as e:
        print(f"⚠️ Error opening file: {e}")

# === Flask Routes ===
@app.route('/', methods=['GET'])
def file_page():
    file_exists = os.path.exists(ZIP_FILE)
    return render_template_string('''
        <html>
        <head>
            <title>File Share</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
            <style>
                body {
                    font-family: 'Poppins', sans-serif;
                    background-color: #f4f7fb;
                    color: #333;
                    text-align: center;
                    padding: 50px;
                }
                h2 {
                    color: #3f4a75;
                    font-weight: 600;
                    margin-bottom: 20px;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 12px 30px;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: 0.3s;
                }
                button:hover {
                    background-color: #45a049;
                }
                .file-upload {
                    background-color: #007BFF;
                    color: white;
                    padding: 12px 30px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .file-upload:hover {
                    background-color: #0069d9;
                }
                .file-info {
                    font-size: 14px;
                    margin-top: 20px;
                    color: #555;
                }
            </style>
        </head>
        <body>
            <h2><i class="fas fa-share-alt"></i> File Sharing</h2>
            {% if file_exists %}
                <a href="/receive"><button><i class="fas fa-download"></i> 📥 Receive File</button></a><br><br>
            {% else %}
                <p><i>No file to download.</i></p>
            {% endif %}
            <form method="POST" action="/send" enctype="multipart/form-data">
                <input type="file" name="file" class="file-upload" multiple><br><br>
                <button type="submit"><i class="fas fa-upload"></i> 📤 Send File to PC</button>
            </form>
            <div class="file-info">
                <p>Share files easily with QR code and download/upload via the web interface.</p>
            </div>
        </body>
        </html>
    ''', file_exists=file_exists)

@app.route('/receive')
def receive_file():
    if os.path.exists(ZIP_FILE):
        return send_file(ZIP_FILE, as_attachment=True)
    return "⚠️ No file to download!", 404

@app.route('/send', methods=['POST'])
def upload_file():
    try:
        uploaded_files = request.files.getlist('file')
        if not uploaded_files:
            return "⚠️ No files uploaded!"

        saved_files = []
        for uploaded in uploaded_files:
            filename = uploaded.filename
            if not filename:
                continue
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded.save(save_path)
            saved_files.append(save_path)

        for saved_file in saved_files:
            show_notification("📥 File Received", f"File saved: {saved_file}")
            open_file(saved_file)

        return f"✅ Files uploaded successfully: {', '.join(saved_files)}"

    except Exception as e:
        traceback.print_exc()
        return f"❌ Server error: {str(e)}", 500

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    return "🔌 Server shutting down..."

# === Utilities ===
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def generate_qr(ip):
    url = f"http://{ip}:5000/"
    qr_path = os.path.join(TEMP_DIR, f"file_qr_{int(time.time())}.png")
    qrcode.make(url).save(qr_path)
    return qr_path

def open_qr(qr_path):
    try:
        Image.open(qr_path).show()
    except Exception as e:
        print(f"⚠️ Error opening QR Code: {e}")

def create_zip(files, progress_bar):
    try:
        with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i, file in enumerate(files, start=1):
                zipf.write(file, os.path.basename(file))
                progress_bar['value'] = (i / len(files)) * 100
                progress_bar.update_idletasks()
    except Exception as e:
        print(f"⚠️ Error creating ZIP: {e}")

def auto_cleanup(delay=300):
    time.sleep(delay)
    try:
        if os.path.exists(ZIP_FILE):
            os.remove(ZIP_FILE)
        for f in os.listdir(TEMP_DIR):
            if f.startswith("file_qr_") and f.endswith(".png"):
                os.remove(os.path.join(TEMP_DIR, f))
    except Exception as e:
        print(f"⚠️ Error in cleanup: {e}")
    try:
        requests.post("http://127.0.0.1:5000/shutdown")
    except:
        pass

def start_flask_server():
    global server_thread
    def flask_runner():
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    server_thread = threading.Thread(target=flask_runner, daemon=True)
    server_thread.start()
    time.sleep(1)

# === Tkinter GUI ===
def on_drop(event, file_list, label):
    files = event.data.split()
    valid_files = [f.strip('{}') for f in files if os.path.exists(f.strip('{}'))]
    if valid_files:
        file_list.clear()
        file_list.extend(valid_files)
        label.config(text=f"Selected Files: {len(file_list)}")
    else:
        label.config(text="⚠ No valid files found!")

@register_command(r"share file", needs_input=False)
def share_files_with_qr():
    speak("Drag and drop files to share")

    file_list = []
    root = TkinterDnD.Tk()
    root.title("Drag & Drop Files to Share and ensure vpn is disabled")
    root.geometry("400x300")
    root.resizable(False, False)

    label = tk.Label(root, text="Drag & Drop Files Here", pady=20)
    label.pack()

    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', lambda event: on_drop(event, file_list, label))

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate')
    progress_bar.pack(pady=10)

    def process_files():
        if not file_list:
            label.config(text="⚠ No files selected. Starting server for upload only...")
            start_flask_server()
            qr_path = generate_qr(get_local_ip())
            label.config(text="🟢 Upload Only Mode\nScan QR to send file to PC")
            open_qr(qr_path)
            threading.Thread(target=auto_cleanup, daemon=True).start()
            return

        create_zip(file_list, progress_bar)
        label.config(text=f"✅ ZIP Created: {ZIP_FILE}")
        start_flask_server()
        qr_path = generate_qr(get_local_ip())
        label.config(text=f"✅ QR Generated!\nScan to Download or Upload")
        open_qr(qr_path)
        threading.Thread(target=auto_cleanup, daemon=True).start()

    tk.Button(root, text="📤 Share Files", command=process_files).pack(pady=20)
    root.mainloop()

# share_files_with_qr()