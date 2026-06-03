from google.cloud.firestore_v1 import FieldFilter

from firebase_connection import get_firestore_db

from config import (
    EXERCICIO_RECOMENDADO_COLLECTION,
    EXERCICIO_RECOMENDADO_ID_FIELD,
    EXERCICIO_RECOMENDADO_NOME_FIELD,
    EXERCICIO_RECOMENDADO_DESCRICAO_FIELD,
    EXERCICIO_RECOMENDADO_NIVEL_DOR_FIELD,
    EXERCICIO_RECOMENDADO_ZONA_DOR_FIELD,
    EXERCICIO_RECOMENDADO_VIDEO_FIELD,
)

db = get_firestore_db()


def get_all_exercicios_recomendados():
    exercicios_ref = db.collection(EXERCICIO_RECOMENDADO_COLLECTION).stream()

    exercicios = []

    for doc in exercicios_ref:
        data = doc.to_dict()
        data["doc_id"] = doc.id
        data["doc_ref"] = doc.reference

        exercicio = {
            "ID": data.get(EXERCICIO_RECOMENDADO_ID_FIELD, "N/A"),
            "Nome": data.get(EXERCICIO_RECOMENDADO_NOME_FIELD, "N/A"),
            "Descrição": data.get(EXERCICIO_RECOMENDADO_DESCRICAO_FIELD, "N/A"),
            "Zona da Dor": data.get(EXERCICIO_RECOMENDADO_ZONA_DOR_FIELD, "N/A"),
            "Nível da Dor": data.get(EXERCICIO_RECOMENDADO_NIVEL_DOR_FIELD, "N/A"),
            "Vídeo": data.get(EXERCICIO_RECOMENDADO_VIDEO_FIELD, "N/A"),
            "doc_ref": doc.reference,
        }

        exercicios.append(exercicio)

    return exercicios


def get_exercicios_by_zona_and_nivel(zona_dor, nivel_dor):
    exercicios_ref = (
        db.collection(EXERCICIO_RECOMENDADO_COLLECTION)
        .where(filter=FieldFilter(EXERCICIO_RECOMENDADO_ZONA_DOR_FIELD, "==", zona_dor))
        .where(filter=FieldFilter(EXERCICIO_RECOMENDADO_NIVEL_DOR_FIELD, "==", nivel_dor))
        .stream()
    )

    exercicios = []

    for doc in exercicios_ref:
        data = doc.to_dict()
        data["doc_id"] = doc.id
        data["doc_ref"] = doc.reference
        exercicios.append(data)

    return exercicios


def get_exercicio_by_reference(exercicio_doc_ref):
    if exercicio_doc_ref is None:
        return None

    exercicio_doc = exercicio_doc_ref.get()

    if not exercicio_doc.exists:
        return None

    data = exercicio_doc.to_dict()
    data["doc_id"] = exercicio_doc.id
    data["doc_ref"] = exercicio_doc.reference

    return data