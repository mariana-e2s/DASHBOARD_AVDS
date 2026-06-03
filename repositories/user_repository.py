from firebase_connection import get_firestore_db

from config import (
    USER_COLLECTION,
    USER_NAME_FIELD,
    USER_EMAIL_FIELD,
    USER_PHOTO_FIELD,
    USER_PHOTO_URL_FIELD,
    USER_DISPLAY_NAME_FIELD,
)

db = get_firestore_db()


def get_all_users():
    users_ref = db.collection(USER_COLLECTION).stream()

    users = []

    for doc in users_ref:
        data = doc.to_dict()
        data["doc_id"] = doc.id
        data["doc_ref"] = doc.reference
        users.append(data)

    return users


def get_user_display_name(user):
    nome = user.get(USER_NAME_FIELD)

    if nome:
        return nome

    display_name = user.get(USER_DISPLAY_NAME_FIELD)

    if display_name:
        return display_name

    email = user.get(USER_EMAIL_FIELD)

    if email:
        return email

    return "Paciente sem nome"


def get_user_photo(user):
    return (
        user.get(USER_PHOTO_FIELD)
        or user.get(USER_PHOTO_URL_FIELD)
        or ""
    )


def get_user_by_reference(user_doc_ref):
    user_doc = user_doc_ref.get()

    if not user_doc.exists:
        return None

    data = user_doc.to_dict()
    data["doc_id"] = user_doc.id
    data["doc_ref"] = user_doc.reference

    return data