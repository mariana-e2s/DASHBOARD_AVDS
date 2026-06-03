from google.cloud.firestore_v1 import FieldFilter

from firebase_connection import get_firestore_db

from config import (
    MEDICACAO_COLLECTION,
    MEDICACAO_USER_REFERENCE_FIELD,
    MEDICACAO_NOME_FIELD,
    MEDICACAO_TIPO_FIELD,
    MEDICACAO_QUANTIDADE_FIELD,
    MEDICACAO_HORARIO_FIELD,
)

db = get_firestore_db()


def get_medicacao_by_user(user_doc_ref):
    medicacao_ref = (
        db.collection(MEDICACAO_COLLECTION)
        .where(filter=FieldFilter(MEDICACAO_USER_REFERENCE_FIELD, "==", user_doc_ref))
        .stream()
    )

    medicacoes = []

    for doc in medicacao_ref:
        data = doc.to_dict()

        medicacao = {
            "Medicação": data.get(MEDICACAO_NOME_FIELD, "N/A"),
            "Tipo": data.get(MEDICACAO_TIPO_FIELD, "N/A"),
            "Quantidade": data.get(MEDICACAO_QUANTIDADE_FIELD, "N/A"),
            "Horário": data.get(MEDICACAO_HORARIO_FIELD, "N/A"),
        }

        medicacoes.append(medicacao)

    return medicacoes


def get_medicacao_sos_by_user(user_doc_ref):
    medicacao_ref = (
        db.collection(MEDICACAO_COLLECTION)
        .where(filter=FieldFilter(MEDICACAO_USER_REFERENCE_FIELD, "==", user_doc_ref))
        .where(filter=FieldFilter(MEDICACAO_TIPO_FIELD, "==", "sos"))
        .stream()
    )

    medicacoes_sos = []

    for doc in medicacao_ref:
        data = doc.to_dict()

        medicacao = {
            "Medicação SOS": data.get(MEDICACAO_NOME_FIELD, "N/A"),
            "Quantidade": data.get(MEDICACAO_QUANTIDADE_FIELD, "N/A"),
            "Horário": data.get(MEDICACAO_HORARIO_FIELD, "N/A"),
        }

        medicacoes_sos.append(medicacao)

    return medicacoes_sos


def get_medicacao_habitual_by_user(user_doc_ref):
    medicacao_ref = (
        db.collection(MEDICACAO_COLLECTION)
        .where(filter=FieldFilter(MEDICACAO_USER_REFERENCE_FIELD, "==", user_doc_ref))
        .where(filter=FieldFilter(MEDICACAO_TIPO_FIELD, "==", "habitual"))
        .stream()
    )

    medicacoes_habituais = []

    for doc in medicacao_ref:
        data = doc.to_dict()

        medicacao = {
            "Medicação Habitual": data.get(MEDICACAO_NOME_FIELD, "N/A"),
            "Quantidade": data.get(MEDICACAO_QUANTIDADE_FIELD, "N/A"),
            "Horário": data.get(MEDICACAO_HORARIO_FIELD, "N/A"),
        }

        medicacoes_habituais.append(medicacao)

    return medicacoes_habituais