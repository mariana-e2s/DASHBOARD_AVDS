import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from auth import check_authentication, logout_button

from repositories.user_repository import get_all_users
from repositories.sono_repository import get_sono_by_user
from repositories.exercicio_repository import get_exercicios_by_user
from repositories.medicacao_repository import get_medicacao_by_user
from repositories.dor_repository import get_dor_by_user

from config import (
    USER_ID_FIELD,
    USER_NAME_FIELD,
    USER_AGE_FIELD,
    USER_EMAIL_FIELD,
    USER_PHOTO_FIELD,
)


st.set_page_config(
    page_title="DASHBOARD CLÍNICO FIBRIVE",
    page_icon="FIBRIVE_logo.png",
    layout="wide"
)

check_authentication()

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "FIBRIVE_logo.png"


st.markdown(
    """
    <style>
        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
            color: #111111 !important;
        }

        [data-testid="stHeader"] {
            background-color: #FFFFFF !important;
        }

        [data-testid="stSidebar"] {
            background-color: #F8FAFC !important;
            border-right: 1px solid #E5E7EB;
        }

        [data-testid="stSidebar"] * {
            color: #111827 !important;
        }

        .block-container {
            padding-top: 32px;
            padding-left: 48px;
            padding-right: 48px;
        }

        h1 {
            color: #111827 !important;
            font-size: 34px !important;
            font-weight: 800 !important;
        }

        h2, h3 {
            color: #111827 !important;
            font-weight: 700 !important;
        }

        .patient-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 24px;
            padding: 26px 30px;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.06);
            margin-bottom: 24px;
        }

        .patient-header {
            display: flex;
            align-items: center;
            gap: 18px;
            margin-bottom: 20px;
        }

        .patient-photo {
            width: 86px;
            height: 86px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #BFA2DB;
            box-shadow: 0 6px 16px rgba(191, 162, 219, 0.35);
        }

        .patient-placeholder {
            width: 86px;
            height: 86px;
            border-radius: 50%;
            background-color: #F3E8FF;
            border: 3px solid #BFA2DB;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            font-weight: 800;
            color: #8E7CC3;
        }

        .patient-name {
            font-size: 32px;
            font-weight: 800;
            color: #111827;
            margin: 0;
        }

        .patient-email {
            font-size: 15px;
            color: #64748B !important;
            margin-top: 4px;
            text-decoration: none;
        }

        .patient-email:hover {
            color: #8E7CC3 !important;
            text-decoration: underline;
        }

        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 18px 20px;
            box-shadow: 0 8px 22px rgba(0, 0, 0, 0.04);
        }

        [data-testid="stMetricLabel"] {
            color: #6B7280 !important;
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: #111827 !important;
            font-weight: 800;
        }

        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            border: 1.5px solid #D1D5DB !important;
            border-radius: 12px !important;
            color: #111827 !important;
        }

        div[data-testid="stRadio"] label {
            color: #111827 !important;
            font-weight: 600 !important;
        }

        div.stButton > button {
            border-radius: 12px;
            border: none;
            background-color: #BFA2DB;
            color: white !important;
            font-weight: 700;
        }

        div.stButton > button:hover {
            background-color: #8E7CC3;
            color: white !important;
            border: none;
        }

        [data-testid="stAlert"] {
            border-radius: 14px;
        }

        hr {
            border-color: #E5E7EB !important;
            margin-top: 28px !important;
            margin-bottom: 28px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


def to_dataframe(records):
    if not records:
        return pd.DataFrame()

    return pd.DataFrame(records)


def get_user_display_name(user):
    nome = user.get(USER_NAME_FIELD)

    if nome:
        return nome

    email = user.get(USER_EMAIL_FIELD)

    if email:
        return email

    return "Paciente sem nome"


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

    col1, col2 = st.columns(2)

    with col1:
        st.metric("ID do paciente", user.get(USER_ID_FIELD, "N/A"))

    with col2:
        st.metric("Idade", user.get(USER_AGE_FIELD, "N/A"))


def show_sono_chart(user_doc_ref):
    st.subheader("Sono")

    sono_records = get_sono_by_user(user_doc_ref)
    sono_df = to_dataframe(sono_records)

    if sono_df.empty:
        st.info("Este paciente ainda não tem registos de sono.")
        return

    st.dataframe(sono_df, use_container_width=True)

    fig = px.line(
        sono_df,
        x="Horas de Sono",
        y="Qualidade",
        markers=True,
        title="Qualidade do sono por horas"
    )

    fig.update_layout(
        xaxis_title="Horas de sono",
        yaxis_title="Qualidade",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    fig.update_traces(
        line=dict(color="#BFA2DB", width=4),
        marker=dict(color="#8E7CC3", size=10)
    )

    st.plotly_chart(fig, use_container_width=True)


def show_exercicio_chart(user_doc_ref):
    st.subheader("Exercício")

    exercicio_records = get_exercicios_by_user(user_doc_ref)
    exercicio_df = to_dataframe(exercicio_records)

    if exercicio_df.empty:
        st.info("Este paciente ainda não tem exercícios associados.")
        return

    st.dataframe(exercicio_df, use_container_width=True)

    fig = px.bar(
        exercicio_df,
        x="Dificuldade",
        y="Qualidade de Execução",
        title="Qualidade de execução por dificuldade"
    )

    fig.update_layout(
        xaxis_title="Dificuldade",
        yaxis_title="Qualidade de execução",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    st.plotly_chart(fig, use_container_width=True)


def show_dor_chart(user_doc_ref):
    st.subheader("Dor")

    dor_records = get_dor_by_user(user_doc_ref)
    dor_df = to_dataframe(dor_records)

    if dor_df.empty:
        st.info("Este paciente ainda não tem registos de dor.")
        return

    st.dataframe(dor_df, use_container_width=True)

    fig = px.bar(
        dor_df,
        x="Localização",
        y="Intensidade",
        title="Intensidade da dor por localização"
    )

    fig.update_layout(
        xaxis_title="Localização",
        yaxis_title="Intensidade",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    st.plotly_chart(fig, use_container_width=True)


def show_medicacao_table(user_doc_ref):
    st.subheader("Medicação")

    medicacao_records = get_medicacao_by_user(user_doc_ref)
    medicacao_df = to_dataframe(medicacao_records)

    if medicacao_df.empty:
        st.info("Este paciente ainda não tem medicação registada.")
        return

    st.dataframe(medicacao_df, use_container_width=True)


def show_alerts_page(users):
    st.markdown(
        """
        <h1>Alertas Clínicos</h1>
        <p style="color:#6B7280; font-size:16px; margin-top:-8px;">
            Monitorização de situações que exigem maior atenção clínica.
        </p>
        <div style="height: 20px;"></div>
        """,
        unsafe_allow_html=True
    )

    alerts_found = False

    total_alertas = 0
    total_dor_alta = 0
    total_sono_baixo = 0
    total_sem_registos = 0

    alertas = []

    for user in users:
        nome = get_user_display_name(user)
        user_doc_ref = user["doc_ref"]

        dor_df = to_dataframe(get_dor_by_user(user_doc_ref))
        sono_df = to_dataframe(get_sono_by_user(user_doc_ref))
        medicacao_df = to_dataframe(get_medicacao_by_user(user_doc_ref))
        exercicio_df = to_dataframe(get_exercicios_by_user(user_doc_ref))

        if dor_df.empty and sono_df.empty and medicacao_df.empty and exercicio_df.empty:
            alerts_found = True
            total_alertas += 1
            total_sem_registos += 1
            alertas.append(("warning", nome, "Sem registos clínicos disponíveis."))
            continue

        if not dor_df.empty and "Intensidade" in dor_df.columns:
            intensidade = pd.to_numeric(dor_df["Intensidade"], errors="coerce")
            max_dor = intensidade.max()

            if pd.notna(max_dor) and max_dor >= 8:
                alerts_found = True
                total_alertas += 1
                total_dor_alta += 1
                alertas.append(("error", nome, f"Dor elevada registada. Intensidade máxima: {max_dor}/10."))

        if not sono_df.empty and "Horas de Sono" in sono_df.columns:
            horas_sono = pd.to_numeric(sono_df["Horas de Sono"], errors="coerce")
            min_sono = horas_sono.min()

            if pd.notna(min_sono) and min_sono < 5:
                alerts_found = True
                total_alertas += 1
                total_sono_baixo += 1
                alertas.append(("warning", nome, f"Sono insuficiente registado. Valor mínimo: {min_sono} horas."))

        if medicacao_df.empty:
            alerts_found = True
            total_alertas += 1
            alertas.append(("info", nome, "Sem registos de medicação."))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de alertas", total_alertas)

    with col2:
        st.metric("Dor elevada", total_dor_alta)

    with col3:
        st.metric("Sono baixo", total_sono_baixo)

    with col4:
        st.metric("Sem registos", total_sem_registos)

    st.divider()

    if not alerts_found:
        st.success("Não existem alertas clínicos relevantes de momento.")
        return

    for tipo, nome, mensagem in alertas:
        texto = f"**{nome}** — {mensagem}"

        if tipo == "error":
            st.error(texto)
        elif tipo == "warning":
            st.warning(texto)
        else:
            st.info(texto)


def show_patients_page(users):
    st.markdown(
        """
        <h1>Dashboard Clínico FIBRIVE</h1>
        <p style="color:#6B7280; font-size:16px; margin-top:-8px;">
            Monitorização clínica personalizada de pacientes com fibromialgia.
        </p>
        <div style="height: 24px;"></div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        """
        <h2 style='color: #1F2937; margin-top: 20px; margin-bottom: 20px;'>
            👤 Pacientes
        </h2>
        """,
        unsafe_allow_html=True
    )

    user_names = [get_user_display_name(user) for user in users]

    selected_user_name = st.sidebar.selectbox(
        "Selecionar paciente",
        user_names
    )

    selected_user = None

    for user in users:
        if get_user_display_name(user) == selected_user_name:
            selected_user = user
            break

    if selected_user is None:
        st.error("Não foi possível encontrar o paciente selecionado.")
        st.stop()

    user_doc_ref = selected_user["doc_ref"]

    show_user_info(selected_user)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        show_sono_chart(user_doc_ref)

    with col2:
        show_exercicio_chart(user_doc_ref)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        show_dor_chart(user_doc_ref)

    with col4:
        show_medicacao_table(user_doc_ref)


users = get_all_users()

if not users:
    st.warning("Não existem pacientes na coleção User.")
    st.stop()


if LOGO_PATH.exists():
    st.sidebar.image(str(LOGO_PATH), width=140)
else:
    st.sidebar.warning("Logo não encontrado.")


st.sidebar.markdown(
    """
    <h2 style='color: #1F2937; margin-top: 25px; margin-bottom: 15px;'>
        Menu
    </h2>
    """,
    unsafe_allow_html=True
)

selected_page = st.sidebar.radio(
    "Escolher área",
    ["👤 Pacientes", "⚠️ Alertas"]
)

st.sidebar.markdown("---")
logout_button()
st.sidebar.markdown("---")


if selected_page == "👤 Pacientes":
    show_patients_page(users)

elif selected_page == "⚠️ Alertas":
    show_alerts_page(users)