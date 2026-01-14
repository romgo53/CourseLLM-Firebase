from typing import Optional, Literal

from firebase_admin import credentials, auth 
import firebase_admin

from settings import Settings

settings = Settings()

def initialize_firebase_admin():
     cred = credentials.Certificate(settings.firebase_service_account) 
     firebase_admin.initialize_app(cred)

def verify_token(id_token: str) -> Optional[str]:
    try:
        if id_token == settings.test_auth_token and settings.test_auth_token != "":
            # For testing purposes, return a dummy UID
            return "mWoZ0DurppZXg5yY5HUui4RnQfT2"
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        # Handle error (invalid token, expired, etc.)
        return None

def get_user_role(id_token: str) -> Optional[Literal['student', 'teacher']]:
    print("Verifying token in auth.py:", id_token)
    uid = verify_token(id_token)
    if not uid:
        return None
    user = auth.get_user(uid)
    return user.custom_claims.get('role') if user.custom_claims else None