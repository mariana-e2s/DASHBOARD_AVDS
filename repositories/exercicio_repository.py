from firebase_connection import get_firestore_db

from config import (
    USER_EXERCICIO_COLLECTION,
    USER_REFERENCE_FIELD,
    EXERCICIO_REFERENCE_FIELD,
    EXERCICIO_ID_FIELD,
    EXERCICIO_DIFICULDADE_FIELD,
    EXERCICIO_CONCLUSAO_FIELD,
    EXERCICIO_QUALIDADE_FIELD,
)


db = get_firestore_db()


def get_exercicios_by_user(user_doc_ref):
    user_exercicios_ref = (
        db.collection(USER_EXERCICIO_COLLECTION)
        .where(USER_REFERENCE_FIELD, "==", user_doc_ref)
        .stream()
    )

    exercicios = []

    for relation_doc in user_exercicios_ref:
        relation_data = relation_doc.to_dict()

        exercicio_ref = relation_data.get(EXERCICIO_REFERENCE_FIELD)

        if exercicio_ref is None:
            continue

        exercicio_doc = exercicio_ref.get()

        if not exercicio_doc.exists:
            continue

        exercicio_data = exercicio_doc.to_dict()

        exercicio = {
            "Dificuldade": exercicio_data.get(EXERCICIO_DIFICULDADE_FIELD, 0),
            "Conclusão": exercicio_data.get(EXERCICIO_CONCLUSAO_FIELD, False),
            "Qualidade de Execução": exercicio_data.get(EXERCICIO_QUALIDADE_FIELD, 0),
        }

        exercicios.append(exercicio)

    return exercicios