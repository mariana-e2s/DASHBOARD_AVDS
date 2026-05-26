from firebase_connection import get_firestore_db

from config import (
    MEDICACAO_COLLECTION,
    USER_REFERENCE_FIELD,
    MEDICACAO_ID_FIELD,
    MEDICACAO_HABITUAL_FIELD,
    MEDICACAO_SOS_FIELD,
    MEDICACAO_QUANTIDADE_FIELD,
    MEDICACAO_HORARIO_FIELD,
)


db = get_firestore_db()


def get_medicacao_by_user(user_doc_ref):
    medicacao_ref = (
        db.collection(MEDICACAO_COLLECTION)
        .where(USER_REFERENCE_FIELD, "==", user_doc_ref)
        .stream()
    )

    medicacoes = []

    for doc in medicacao_ref:
        data = doc.to_dict()

        medicacao = {
            "Medicação Habitual": data.get(MEDICACAO_HABITUAL_FIELD, "N/A"),
            "Medicação SOS": data.get(MEDICACAO_SOS_FIELD, "N/A"),
            "Quantidade": data.get(MEDICACAO_QUANTIDADE_FIELD, "N/A"),
            "Horário da Toma": data.get(MEDICACAO_HORARIO_FIELD, "N/A"),
        }

        medicacoes.append(medicacao)

    return medicacoes