from google.cloud.firestore_v1 import FieldFilter

from firebase_connection import get_firestore_db

from config import (
    SONO_COLLECTION,
    SONO_USER_REFERENCE_FIELD,
    SONO_QUALIDADE_FIELD,
    SONO_HORAS_FIELD,
    SONO_DESPERTARES_FIELD,
    SONO_DATA_FIELD,
)

db = get_firestore_db()


def get_sono_by_user(user_doc_ref):
    sono_ref = (
        db.collection(SONO_COLLECTION)
        .where(filter=FieldFilter(SONO_USER_REFERENCE_FIELD, "==", user_doc_ref))
        .stream()
    )

    sonos = []

    for doc in sono_ref:
        data = doc.to_dict()

        sono = {
            "Horas de Sono": data.get(SONO_HORAS_FIELD, 0),
            "Qualidade": data.get(SONO_QUALIDADE_FIELD, 0),
            "Despertares Noturnos": data.get(SONO_DESPERTARES_FIELD, 0),
            "Data": data.get(SONO_DATA_FIELD, None),
        }

        sonos.append(sono)

    return sonos


def get_latest_sono_by_user(user_doc_ref):
    sono_ref = (
        db.collection(SONO_COLLECTION)
        .where(filter=FieldFilter(SONO_USER_REFERENCE_FIELD, "==", user_doc_ref))
        .order_by(SONO_DATA_FIELD, direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in sono_ref:
        data = doc.to_dict()
        data["doc_id"] = doc.id
        data["doc_ref"] = doc.reference
        return data

    return None