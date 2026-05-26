from firebase_connection import get_firestore_db

from config import (
    DOR_COLLECTION,
    USER_REFERENCE_FIELD,
    DOR_ID_FIELD,
    DOR_LOCALIZACAO_FIELD,
    DOR_INTENSIDADE_FIELD,
)


db = get_firestore_db()


def get_dor_by_user(user_doc_ref):
    dor_ref = (
        db.collection(DOR_COLLECTION)
        .where(USER_REFERENCE_FIELD, "==", user_doc_ref)
        .stream()
    )

    dores = []

    for doc in dor_ref:
        data = doc.to_dict()

        dor = {
            "Localização": data.get(DOR_LOCALIZACAO_FIELD, "N/A"),
            "Intensidade": data.get(DOR_INTENSIDADE_FIELD, 0),
        }

        dores.append(dor)

    return dores