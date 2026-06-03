from google.cloud.firestore_v1 import FieldFilter

from firebase_connection import get_firestore_db

from config import (
    DOR_COLLECTION,
    DOR_USER_REFERENCE_FIELD,
    DOR_LOCALIZACAO_FIELD,
    DOR_INTENSIDADE_FIELD,
    DOR_NIVEL_FIELD,
    DOR_DATA_FIELD,
)

db = get_firestore_db()


def get_dor_by_user(user_doc_ref):
    dor_ref = (
        db.collection(DOR_COLLECTION)
        .where(filter=FieldFilter(DOR_USER_REFERENCE_FIELD, "==", user_doc_ref))
        .stream()
    )

    dores = []

    for doc in dor_ref:
        data = doc.to_dict()

        dor = {
            "Localização": data.get(DOR_LOCALIZACAO_FIELD, "N/A"),
            "Intensidade": data.get(DOR_INTENSIDADE_FIELD, 0),
            "Nível da Dor": data.get(DOR_NIVEL_FIELD, "N/A"),
            "Data": data.get(DOR_DATA_FIELD, None),
        }

        dores.append(dor)

    return dores


def get_latest_dor_by_user(user_doc_ref):
    dor_ref = (
        db.collection(DOR_COLLECTION)
        .where(filter=FieldFilter(DOR_USER_REFERENCE_FIELD, "==", user_doc_ref))
        .order_by(DOR_DATA_FIELD, direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in dor_ref:
        data = doc.to_dict()
        data["doc_id"] = doc.id
        data["doc_ref"] = doc.reference
        return data

    return None