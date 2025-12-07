import os
from typing import Optional

import firebase_admin
from firebase_admin import credentials, auth as fb_auth

_firebase_app = None

def _init_firebase():
    global _firebase_app
    if _firebase_app:
        return
    cred_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
    if not cred_path:
        raise RuntimeError("FIREBASE_SERVICE_ACCOUNT environment variable not set")
    cred = credentials.Certificate(cred_path)
    _firebase_app = firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token: str) -> Optional[dict]:
    """Verify Firebase ID token and return decoded token dict on success.

    Raises RuntimeError on misconfiguration.
    Returns None if token is invalid.
    """
    if not id_token:
        return None
    if not _firebase_app:
        _init_firebase()
    try:
        decoded = fb_auth.verify_id_token(id_token)
        return decoded
    except Exception:
        return None
