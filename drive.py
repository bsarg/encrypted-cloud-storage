from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import io
from crypto import encrypt_file, decrypt_file

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class DriveService:
    def __init__(self, credentials_dict):
        self.creds = Credentials.from_authorized_user_info(credentials_dict)

        # Automatically refresh expired token
        if not self.creds.valid:
            if self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

                # Update session with refreshed credentials
                credentials_dict.update({
                    "token": self.creds.token,
                    "refresh_token": self.creds.refresh_token,
                    "token_uri": self.creds.token_uri,
                    "client_id": self.creds.client_id,
                    "client_secret": self.creds.client_secret,
                })

        self.service = build("drive", "v3", credentials=self.creds)

    def list_files(self):
        """List files stored in Google Drive."""
        try:
            results = self.service.files().list().execute()
            return results.get("files", [])
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def upload_file(self, file_path):
        """Encrypt and upload a file to Google Drive."""
        try:
            encrypted_path = encrypt_file(file_path)
            file_metadata = {"name": os.path.basename(encrypted_path)}
            media = MediaFileUpload(encrypted_path, mimetype="application/octet-stream")

            uploaded_file = self.service.files().create(body=file_metadata, media_body=media).execute()
            os.remove(encrypted_path)  # Remove encrypted file after upload
            return uploaded_file
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None

    def download_file(self, file_id, filename):
        """Download an encrypted file and decrypt it locally."""
        try:
            request = self.service.files().get_media(fileId=file_id)
            encrypted_path = os.path.join(UPLOAD_FOLDER, filename)

            with open(encrypted_path, "wb") as f:
                f.write(request.execute())

            decrypted_path = decrypt_file(encrypted_path)
            os.remove(encrypted_path)  # Remove encrypted file after decryption
            return decrypted_path
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None