from flask import Flask, render_template, request, redirect, url_for, session
from drive import DriveService
from auth import auth_bp  # Import auth blueprint
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "ODQ7mm_9_ZdNEl_bdPwXoVzMnbcXv0gMtjZdlLvDMy4="

app.register_blueprint(auth_bp)  # Register the auth blueprint

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    if "credentials" not in session:
        return redirect(url_for("auth.login"))

    drive = DriveService(session["credentials"])
    files = drive.list_files()
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "credentials" not in session:
        return redirect(url_for("auth.login"))

    file = request.files["file"]
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        drive = DriveService(session["credentials"])
        drive.upload_file(file_path)
        os.remove(file_path)  # Remove original file after upload

    return redirect(url_for("home"))

@app.route("/download/<file_id>/<filename>")
def download_file(file_id, filename):
    if "credentials" not in session:
        return redirect(url_for("auth.login"))

    drive = DriveService(session["credentials"])
    decrypted_path = drive.download_file(file_id, filename)

    return redirect(url_for("home"))  # Redirect to home after download

if __name__ == "__main__":
    app.run(debug=True)