from typing import Optional, Literal

from firebase_admin import credentials, auth 
import firebase_admin

from app.settings import Settings

settings = Settings()

def initialize_firebase_admin():
     if settings.use_emulator.lower() == "true":
         # Initialize Firebase Admin SDK to connect to the emulator
         firebase_admin.initialize_app(options={
                'projectId': 'course-llm-firebase'  # Use a dummy project ID for the emulator
         })
     else:
         cred = credentials.Certificate(settings.firebase_service_account) 
         firebase_admin.initialize_app(cred)

def verify_token(id_token: str) -> Optional[str]:
    try:
        if id_token == settings.test_auth_token and settings.test_auth_token != "":
            # For testing purposes, return a dummy UID
            return settings.test_user_uid
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        # Handle error (invalid token, expired, etc.)
        return None

def get_user_role(id_token: str) -> Optional[Literal['student', 'teacher']]:
    uid = verify_token(id_token)
    if not uid:
        return None
    user = auth.get_user(uid)
    return user.custom_claims.get('role') if user.custom_claims else None