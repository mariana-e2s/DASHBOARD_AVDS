from firebase_connection import get_firestore_db

from config import (
    SONO_COLLECTION,
    USER_REFERENCE_FIELD,
    SONO_ID_FIELD,
    SONO_QUALIDADE_FIELD,
    SONO_DESPERTARES_FIELD,
    SONO_HORAS_FIELD,
)


db = get_firestore_db()


def get_sono_by_user(user_doc_ref):
    sono_ref = (
        db.collection(SONO_COLLECTION)
        .where(USER_REFERENCE_FIELD, "==", user_doc_ref)
        .stream()
    )

    sono_records = []

    for doc in sono_ref:
        data = doc.to_dict()

        sono = {
            "Horas de Sono": data.get(SONO_HORAS_FIELD, 0),
            "Qualidade": data.get(SONO_QUALIDADE_FIELD, 0),
            "Despertares Noturnos": data.get(SONO_DESPERTARES_FIELD, False),
        }

        sono_records.append(sono)

    return sono_records