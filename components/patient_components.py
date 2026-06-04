import streamlit as st

from repositories.user_repository import get_user_display_name
from utils.data_utils import numeric_mean, calculate_patient_status

from config import (
    USER_ID_FIELD,
    USER_AGE_FIELD,
    USER_EMAIL_FIELD,
    USER_PHOTO_FIELD,
)


def show_user_info(user):
    nome = get_user_display_name(user)
    email = user.get(USER_EMAIL_FIELD, "N/A")
    photo_url = user.get(USER_PHOTO_FIELD, "")

    primeira_letra = nome[0].upper() if nome else "?"

    if photo_url:
        photo_html = f'<img src="{photo_url}" class="patient-photo">'
    else:
        photo_html = f'<div class="patient-placeholder">{primeira_letra}</div>'

    st.markdown(
        f"""
        <div class="patient-card">
            <div class="patient-header">
                {photo_html}
                <div>
                    <div class="patient-name">{nome}</div>
                    <a class="patient-email" href="mailto:{email}">{email}</a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



def show_patient_summary_cards(sono_df, exercicio_df, dor_df, medicacao_df):
    media_sono = numeric_mean(sono_df, "Horas de Sono")
    media_qualidade = numeric_mean(sono_df, "Qualidade")
    media_dor = numeric_mean(dor_df, "Intensidade")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Sono médio", f"{media_sono:.1f} h" if media_sono is not None else "Sem dados")

    with col2:
        st.metric("Qualidade do sono", f"{media_qualidade:.1f}" if media_qualidade is not None else "Sem dados")

    with col3:
        st.metric("Dor média", f"{media_dor:.1f}/10" if media_dor is not None else "Sem dados")

    with col4:
        st.metric("Exercícios", len(exercicio_df) if not exercicio_df.empty else 0)

    col5, col6 = st.columns(2)

    with col5:
        st.metric("Registos de medicação", len(medicacao_df) if not medicacao_df.empty else 0)

    with col6:
        total_registos = len(sono_df) + len(exercicio_df) + len(dor_df) + len(medicacao_df)
        st.metric("Total de registos", total_registos)


def show_patient_status(sono_df, dor_df):
    status, reason, css_class = calculate_patient_status(sono_df, dor_df)

    st.markdown(
        f"""
        <div class="status-card">
            <div class="status-title">
                Estado clínico atual: <span class="{css_class}">{status}</span>
            </div>
            <div class="status-text">
                {reason}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )