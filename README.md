# Encrypted Cloud Storage

A small Flask app that encrypts files locally with Fernet before uploading them to Google Drive, and decrypts files after download. Intended as a simple educational/demo project for secure uploads/downloads.

## Quick Start

- Create and activate a Python virtual environment.
- Install dependencies (see **Requirements**).
- Add OAuth2 client credentials as `credentials.json` (Google Cloud Console) and ensure `secret.key` exists or generate it.
- Run the app and open `http://localhost:5000` in your browser.

```bash
python app.py
```

## Requirements

- Python 3.8+
- Libraries: `flask`, `google-auth`, `google-auth-oauthlib`, `google-api-python-client`, `cryptography`, `werkzeug`

Install with:

```bash
pip install flask google-auth google-auth-oauthlib google-api-python-client cryptography werkzeug
```

## Project Structure

- `app.py` — Flask application; routes: `/` (home), `/upload`, `/download/<file_id>/<filename>`.
- `auth.py` — Google OAuth2 flow; expects `credentials.json` and uses redirect `http://localhost:5000/auth/callback`.
- `drive.py` — Google Drive API wrapper; uploads encrypted files and downloads then decrypts.
- `crypto.py` — Encryption helpers using `cryptography.fernet` (`generate_key`, `load_key`, `encrypt_file`, `decrypt_file`).
- `templates/index.html` — Main web UI for upload/list/download.
- `uploads/` — Temporary local storage used during upload/download.
- `secret.key` — Fernet key file used to encrypt/decrypt files (keep private).

## How It Works

- Upload: file saved locally to `uploads/`, encrypted with Fernet (`*.enc`), then uploaded to Google Drive. Local encrypted copy is removed after upload.
- Download: encrypted file is downloaded to `uploads/`, decrypted to `*.dec`, then the encrypted local file is removed.

## Configuration & Notes

- OAuth: Create OAuth client credentials in Google Cloud Console and save as `credentials.json` in the project root. Set the redirect URI to `http://localhost:5000/auth/callback`.
- Scopes: The app requests `https://www.googleapis.com/auth/drive.file` (limited to app-created files).
- Secret key: `secret.key` must be present. Generate it using:

```bash
python -c "from crypto import generate_key; generate_key()"
```

- Session secret: `app.py` currently contains a hard-coded `app.secret_key` for convenience — replace with an environment variable for production.

## Security Considerations

- Do NOT commit `credentials.json` or `secret.key` to a public repository.
- Replace the hard-coded Flask secret with an environment-provided value in production (e.g., `FLASK_SECRET_KEY`).
- Consider more secure credential storage than the Flask session for production use.


## License

No license specified. 
