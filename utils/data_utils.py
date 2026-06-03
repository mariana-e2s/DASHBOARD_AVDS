import pandas as pd

from repositories.sono_repository import get_sono_by_user
from repositories.dor_repository import get_dor_by_user
from repositories.medicacao_repository import get_medicacao_by_user
from repositories.user_exercicio_repository import get_user_exercicios_by_user


def to_dataframe(records):
    if not records:
        return pd.DataFrame()

    return pd.DataFrame(records)


def get_patient_dataframes(user_doc_ref):
    sono_df = to_dataframe(get_sono_by_user(user_doc_ref))
    exercicio_df = to_dataframe(get_user_exercicios_by_user(user_doc_ref))
    dor_df = to_dataframe(get_dor_by_user(user_doc_ref))
    medicacao_df = to_dataframe(get_medicacao_by_user(user_doc_ref))

    return sono_df, exercicio_df, dor_df, medicacao_df


def numeric_mean(df, column):
    if df.empty or column not in df.columns:
        return None

    values = pd.to_numeric(df[column], errors="coerce").dropna()

    if values.empty:
        return None

    return values.mean()


def numeric_max(df, column):
    if df.empty or column not in df.columns:
        return None

    values = pd.to_numeric(df[column], errors="coerce").dropna()

    if values.empty:
        return None

    return values.max()


def numeric_min(df, column):
    if df.empty or column not in df.columns:
        return None

    values = pd.to_numeric(df[column], errors="coerce").dropna()

    if values.empty:
        return None

    return values.min()


def calculate_patient_status(sono_df, dor_df):
    media_sono = numeric_mean(sono_df, "Horas de Sono")
    max_dor = numeric_max(dor_df, "Intensidade")
    media_dor = numeric_mean(dor_df, "Intensidade")

    if max_dor is not None and max_dor >= 8:
        return "Crítico", "Dor elevada registada.", "status-critical"

    if media_sono is not None and media_sono < 5:
        return "Crítico", "Sono médio inferior a 5 horas.", "status-critical"

    if media_dor is not None and media_dor >= 5:
        return "Atenção", "Dor média moderada/elevada.", "status-warning"

    if media_sono is not None and media_sono < 6:
        return "Atenção", "Sono médio abaixo do recomendado.", "status-warning"

    if media_dor is None and media_sono is None:
        return (
            "Sem dados suficientes",
            "Ainda não existem dados suficientes para classificar o estado clínico.",
            "status-warning"
        )

    return "Estável", "Não existem sinais críticos nos dados disponíveis.", "status-stable"