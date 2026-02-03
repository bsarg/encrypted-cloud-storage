from flask import Blueprint, redirect, request, session, url_for
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import google.auth.exceptions
import os

auth_bp = Blueprint("auth", __name__)

CLIENT_SECRETS_FILE = "credentials.json"

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
REDIRECT_URI = "http://localhost:5000/auth/callback"

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
)

@auth_bp.route("/login")
def login():
    """Redirects the user to Google's OAuth 2.0 login page."""
    authorization_url, state = flow.authorization_url(access_type="offline", prompt="consent")
    session["state"] = state
    return redirect(authorization_url)

@auth_bp.route("/auth/callback")
def callback():
    """Handles Google's OAuth callback and stores user credentials."""
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
    }

    return redirect(url_for("home"))

@auth_bp.route("/logout")
def logout():
    """Clears the session and logs out the user."""
    session.clear()
    return redirect(url_for("home"))