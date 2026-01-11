import os
from typing import Optional, Literal

from firebase_admin import credentials, auth 
import firebase_admin

def initialize_firebase_admin():
     cred = credentials.Certificate('service_accout.json') 
     firebase_admin.initialize_app(cred)

def verify_token(id_token: str) -> Optional[str]:
    try:
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