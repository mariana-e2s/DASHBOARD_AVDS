from google.cloud.firestore_v1 import FieldFilter

from firebase_connection import get_firestore_db

from config import (
    USER_EXERCICIO_COLLECTION,
    USER_EXERCICIO_USER_REFERENCE_FIELD,
    USER_EXERCICIO_EXERCICIO_REFERENCE_FIELD,
    USER_EXERCICIO_DATA_FIELD,
    USER_EXERCICIO_DIFICULDADE_FIELD,
    EXERCICIO_RECOMENDADO_NOME_FIELD,
    EXERCICIO_RECOMENDADO_ZONA_DOR_FIELD,
    EXERCICIO_RECOMENDADO_NIVEL_DOR_FIELD,
)

db = get_firestore_db()


def get_user_exercicios_by_user(user_doc_ref):
    user_exercicio_ref = (
        db.collection(USER_EXERCICIO_COLLECTION)
        .where(filter=FieldFilter(USER_EXERCICIO_USER_REFERENCE_FIELD, "==", user_doc_ref))
        .stream()
    )

    resultados = []

    for doc in user_exercicio_ref:
        data = doc.to_dict()

        exercicio_ref = data.get(USER_EXERCICIO_EXERCICIO_REFERENCE_FIELD)
        exercicio_data = {}

        if exercicio_ref:
            exercicio_doc = exercicio_ref.get()

            if exercicio_doc.exists:
                exercicio_data = exercicio_doc.to_dict()

        resultado = {
            "Exercício": exercicio_data.get(EXERCICIO_RECOMENDADO_NOME_FIELD, "N/A"),
            "Zona da Dor": exercicio_data.get(EXERCICIO_RECOMENDADO_ZONA_DOR_FIELD, "N/A"),
            "Nível da Dor": exercicio_data.get(EXERCICIO_RECOMENDADO_NIVEL_DOR_FIELD, "N/A"),
            "Dificuldade": data.get(USER_EXERCICIO_DIFICULDADE_FIELD, 0),
            "Data": data.get(USER_EXERCICIO_DATA_FIELD, None),
        }

        resultados.append(resultado)

    return resultados


def get_user_exercicio_summary(user_doc_ref):
    exercicios = get_user_exercicios_by_user(user_doc_ref)

    if not exercicios:
        return {
            "total": 0,
            "concluidos": 0,
            "taxa_conclusao": 0,
            "dificuldade_media": 0,
            "qualidade_media": 0,
        }

    total = len(exercicios)

    concluidos = sum(
        1 for exercicio in exercicios
        if exercicio.get("Concluído") is True
    )

    dificuldades = [
        exercicio.get("Dificuldade", 0)
        for exercicio in exercicios
        if exercicio.get("Dificuldade") is not None
    ]

    qualidades = [
        exercicio.get("Qualidade de Execução", 0)
        for exercicio in exercicios
        if exercicio.get("Qualidade de Execução") is not None
    ]

    dificuldade_media = (
        sum(dificuldades) / len(dificuldades)
        if dificuldades else 0
    )

    qualidade_media = (
        sum(qualidades) / len(qualidades)
        if qualidades else 0
    )

    taxa_conclusao = (concluidos / total) * 100 if total > 0 else 0

    return {
        "total": total,
        "concluidos": concluidos,
        "taxa_conclusao": round(taxa_conclusao, 1),
        "dificuldade_media": round(dificuldade_media, 1),
        "qualidade_media": round(qualidade_media, 1),
    }