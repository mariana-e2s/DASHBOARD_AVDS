from google.cloud.firestore_v1 import FieldFilter

from firebase_connection import get_firestore_db

from config import (
    SOS_COLLECTION,
    SOS_USER_REFERENCE_FIELD,
    SOS_ID_FIELD,
    SOS_CONTACTO_FIELD,
)

db = get_firestore_db()


def get_sos_by_user(user_doc_ref):
    sos_ref = (
        db.collection(SOS_COLLECTION)
        .where(filter=FieldFilter(SOS_USER_REFERENCE_FIELD, "==", user_doc_ref))
        .stream()
    )

    contactos = []

    for doc in sos_ref:
        data = doc.to_dict()

        contacto = {
            "SOS ID": data.get(SOS_ID_FIELD, "N/A"),
            "Contacto SOS": data.get(SOS_CONTACTO_FIELD, "N/A"),
        }

        contactos.append(contacto)

    return contactos