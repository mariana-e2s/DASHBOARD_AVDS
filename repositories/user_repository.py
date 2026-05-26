from firebase_connection import get_firestore_db
from config import USER_COLLECTION


db = get_firestore_db()


def get_all_users():
    users_ref = db.collection(USER_COLLECTION).stream()

    users = []

    for doc in users_ref:
        user = doc.to_dict()
        user["doc_id"] = doc.id
        user["doc_ref"] = doc.reference
        users.append(user)

    return users