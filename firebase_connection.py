import firebase_admin
from firebase_admin import credentials, firestore

from config import SERVICE_ACCOUNT_KEY_PATH


def get_firestore_db():
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)

    return firestore.client()