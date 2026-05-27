import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from io import BytesIO
from datetime import datetime

from streamlit_option_menu import option_menu

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

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle
    )

    REPORTLAB_AVAILABLE = True

except ImportError:
    REPORTLAB_AVAILABLE = False


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
            color: #111827 !important;
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

        .page-subtitle {
            color: #6B7280;
            font-size: 16px;
            margin-top: -8px;
            margin-bottom: 28px;
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

        .status-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 20px;
            padding: 20px 24px;
            box-shadow: 0 8px 22px rgba(0, 0, 0, 0.04);
            margin-bottom: 20px;
        }

        .status-title {
            font-size: 18px;
            font-weight: 800;
            color: #111827;
            margin-bottom: 6px;
        }

        .status-text {
            font-size: 15px;
            color: #6B7280;
        }

        .status-stable {
            color: #047857;
            font-weight: 800;
        }

        .status-warning {
            color: #B45309;
            font-weight: 800;
        }

        .status-critical {
            color: #B91C1C;
            font-weight: 800;
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

        div.stButton > button,
        div[data-testid="stDownloadButton"] > button {
            border-radius: 12px;
            border: none;
            background-color: #BFA2DB;
            color: white !important;
            font-weight: 700;
        }

        div.stButton > button:hover,
        div[data-testid="stDownloadButton"] > button:hover {
            background-color: #8E7CC3;
            color: white !important;
            border: none;
        }

        [data-testid="stAlert"] {
            border-radius: 14px;
        }

        [data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #E5E7EB;
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


def get_patient_dataframes(user_doc_ref):
    sono_df = to_dataframe(get_sono_by_user(user_doc_ref))
    exercicio_df = to_dataframe(get_exercicios_by_user(user_doc_ref))
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
        return "Sem dados suficientes", "Ainda não existem dados suficientes para classificar o estado clínico.", "status-warning"

    return "Estável", "Não existem sinais críticos nos dados disponíveis.", "status-stable"


def show_page_header(title, subtitle):
    st.markdown(
        f"""
        <h1>{title}</h1>
        <p class="page-subtitle">{subtitle}</p>
        """,
        unsafe_allow_html=True
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

    col1, col2 = st.columns(2)

    with col1:
        st.metric("ID do paciente", user.get(USER_ID_FIELD, "N/A"))

    with col2:
        st.metric("Idade", user.get(USER_AGE_FIELD, "N/A"))


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


def show_sono_chart(user_doc_ref):
    st.subheader("Sono")

    sono_df = to_dataframe(get_sono_by_user(user_doc_ref))

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

    exercicio_df = to_dataframe(get_exercicios_by_user(user_doc_ref))

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

    fig.update_traces(marker_color="#BFA2DB")

    st.plotly_chart(fig, use_container_width=True)


def show_dor_chart(user_doc_ref):
    st.subheader("Dor")

    dor_df = to_dataframe(get_dor_by_user(user_doc_ref))

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

    fig.update_traces(marker_color="#8E7CC3")

    st.plotly_chart(fig, use_container_width=True)


def show_medicacao_table(user_doc_ref):
    st.subheader("Medicação")

    medicacao_df = to_dataframe(get_medicacao_by_user(user_doc_ref))

    if medicacao_df.empty:
        st.info("Este paciente ainda não tem medicação registada.")
        return

    st.dataframe(medicacao_df, use_container_width=True)


def show_sono_dor_relation(sono_df, dor_df):
    st.subheader("Relação entre sono e dor")

    if sono_df.empty or dor_df.empty:
        st.info("Não existem dados suficientes para relacionar sono e dor.")
        return

    if "Horas de Sono" not in sono_df.columns or "Intensidade" not in dor_df.columns:
        st.info("Os campos necessários para cruzar sono e dor não existem nos dados.")
        return

    min_len = min(len(sono_df), len(dor_df))

    relation_df = pd.DataFrame(
        {
            "Horas de Sono": pd.to_numeric(sono_df["Horas de Sono"].head(min_len), errors="coerce"),
            "Intensidade da Dor": pd.to_numeric(dor_df["Intensidade"].head(min_len), errors="coerce"),
        }
    ).dropna()

    if relation_df.empty:
        st.info("Não existem valores numéricos suficientes para gerar o gráfico.")
        return

    fig = px.scatter(
        relation_df,
        x="Horas de Sono",
        y="Intensidade da Dor",
        title="Relação entre horas de sono e intensidade da dor"
    )

    fig.update_layout(
        xaxis_title="Horas de sono",
        yaxis_title="Intensidade da dor",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    fig.update_traces(marker=dict(color="#8E7CC3", size=10))

    st.plotly_chart(fig, use_container_width=True)


def show_general_summary(users):
    show_page_header(
        "Resumo Geral",
        "Visão global dos pacientes acompanhados no dashboard clínico."
    )

    total_pacientes = len(users)
    total_alertas = 0
    pacientes_dor_alta = 0
    pacientes_sono_baixo = 0
    pacientes_sem_registos = 0

    dores = []
    sonos = []

    for user in users:
        user_doc_ref = user["doc_ref"]

        sono_df, exercicio_df, dor_df, medicacao_df = get_patient_dataframes(user_doc_ref)

        total_registos = len(sono_df) + len(exercicio_df) + len(dor_df) + len(medicacao_df)

        if total_registos == 0:
            pacientes_sem_registos += 1
            total_alertas += 1

        max_dor = numeric_max(dor_df, "Intensidade")
        min_sono = numeric_min(sono_df, "Horas de Sono")
        media_dor = numeric_mean(dor_df, "Intensidade")
        media_sono = numeric_mean(sono_df, "Horas de Sono")

        if media_dor is not None:
            dores.append(media_dor)

        if media_sono is not None:
            sonos.append(media_sono)

        if max_dor is not None and max_dor >= 8:
            pacientes_dor_alta += 1
            total_alertas += 1

        if min_sono is not None and min_sono < 5:
            pacientes_sono_baixo += 1
            total_alertas += 1

        if medicacao_df.empty:
            total_alertas += 1

    media_geral_dor = sum(dores) / len(dores) if dores else None
    media_geral_sono = sum(sonos) / len(sonos) if sonos else None

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pacientes", total_pacientes)

    with col2:
        st.metric("Alertas ativos", total_alertas)

    with col3:
        st.metric("Dor média geral", f"{media_geral_dor:.1f}/10" if media_geral_dor is not None else "Sem dados")

    with col4:
        st.metric("Sono médio geral", f"{media_geral_sono:.1f} h" if media_geral_sono is not None else "Sem dados")

    st.divider()

    col5, col6, col7 = st.columns(3)

    with col5:
        st.metric("Pacientes com dor elevada", pacientes_dor_alta)

    with col6:
        st.metric("Pacientes com sono baixo", pacientes_sono_baixo)

    with col7:
        st.metric("Pacientes sem registos", pacientes_sem_registos)

    st.divider()

    resumo_df = pd.DataFrame(
        {
            "Indicador": [
                "Total de pacientes",
                "Alertas ativos",
                "Pacientes com dor elevada",
                "Pacientes com sono baixo",
                "Pacientes sem registos",
            ],
            "Valor": [
                total_pacientes,
                total_alertas,
                pacientes_dor_alta,
                pacientes_sono_baixo,
                pacientes_sem_registos,
            ],
        }
    )

    fig = px.bar(
        resumo_df,
        x="Indicador",
        y="Valor",
        title="Resumo de indicadores clínicos"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    fig.update_traces(marker_color="#BFA2DB")

    st.plotly_chart(fig, use_container_width=True)


def show_alerts_page(users):
    show_page_header(
        "Alertas Clínicos",
        "Monitorização de situações que exigem maior atenção clínica."
    )

    alerts_found = False

    total_alertas = 0
    total_dor_alta = 0
    total_sono_baixo = 0
    total_sem_registos = 0
    total_sem_medicacao = 0

    alertas = []

    for user in users:
        nome = get_user_display_name(user)
        user_doc_ref = user["doc_ref"]

        sono_df, exercicio_df, dor_df, medicacao_df = get_patient_dataframes(user_doc_ref)

        if dor_df.empty and sono_df.empty and medicacao_df.empty and exercicio_df.empty:
            alerts_found = True
            total_alertas += 1
            total_sem_registos += 1
            alertas.append(("warning", nome, "Sem registos clínicos disponíveis."))
            continue

        max_dor = numeric_max(dor_df, "Intensidade")
        min_sono = numeric_min(sono_df, "Horas de Sono")

        if max_dor is not None and max_dor >= 8:
            alerts_found = True
            total_alertas += 1
            total_dor_alta += 1
            alertas.append(("error", nome, f"Dor elevada registada. Intensidade máxima: {max_dor}/10."))

        if min_sono is not None and min_sono < 5:
            alerts_found = True
            total_alertas += 1
            total_sono_baixo += 1
            alertas.append(("warning", nome, f"Sono insuficiente registado. Valor mínimo: {min_sono} horas."))

        if medicacao_df.empty:
            alerts_found = True
            total_alertas += 1
            total_sem_medicacao += 1
            alertas.append(("info", nome, "Sem registos de medicação."))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de alertas", total_alertas)

    with col2:
        st.metric("Dor elevada", total_dor_alta)

    with col3:
        st.metric("Sono baixo", total_sono_baixo)

    with col4:
        st.metric("Sem medicação", total_sem_medicacao)

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


def show_body_map_page(users):
    show_page_header(
        "Mapa Corporal / Zonas de Dor",
        "Análise das zonas corporais com maior frequência e intensidade de dor."
    )

    all_pain_records = []

    for user in users:
        nome = get_user_display_name(user)
        user_doc_ref = user["doc_ref"]

        dor_df = to_dataframe(get_dor_by_user(user_doc_ref))

        if dor_df.empty:
            continue

        if "Localização" not in dor_df.columns or "Intensidade" not in dor_df.columns:
            continue

        dor_df = dor_df.copy()
        dor_df["Paciente"] = nome
        dor_df["Intensidade"] = pd.to_numeric(dor_df["Intensidade"], errors="coerce")

        all_pain_records.append(dor_df)

    if not all_pain_records:
        st.info("Ainda não existem registos de dor suficientes para gerar o mapa corporal.")
        return

    pain_df = pd.concat(all_pain_records, ignore_index=True)
    pain_df = pain_df.dropna(subset=["Localização", "Intensidade"])

    if pain_df.empty:
        st.info("Os registos de dor existentes não têm dados válidos de localização e intensidade.")
        return

    total_registos = len(pain_df)
    total_zonas = pain_df["Localização"].nunique()
    intensidade_media = pain_df["Intensidade"].mean()

    zona_mais_frequente = pain_df["Localização"].value_counts().idxmax()

    intensidade_por_zona = (
        pain_df
        .groupby("Localização")["Intensidade"]
        .mean()
        .sort_values(ascending=False)
    )

    zona_mais_intensa = intensidade_por_zona.index[0]
    valor_zona_mais_intensa = intensidade_por_zona.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Registos de dor", total_registos)

    with col2:
        st.metric("Zonas afetadas", total_zonas)

    with col3:
        st.metric("Dor média", f"{intensidade_media:.1f}/10")

    with col4:
        st.metric("Zona mais crítica", zona_mais_intensa)

    st.divider()

    st.markdown(
        f"""
        <div class="status-card">
            <div class="status-title">Resumo do mapa corporal</div>
            <div class="status-text">
                A zona com maior número de registos é <b>{zona_mais_frequente}</b>.
                A zona com maior intensidade média de dor é <b>{zona_mais_intensa}</b>,
                com uma média de <b>{valor_zona_mais_intensa:.1f}/10</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    zone_frequency = pain_df["Localização"].value_counts().reset_index()
    zone_frequency.columns = ["Localização", "N.º de registos"]

    fig_freq = px.bar(
        zone_frequency,
        x="Localização",
        y="N.º de registos",
        title="Frequência de dor por zona corporal"
    )

    fig_freq.update_layout(
        xaxis_title="Zona corporal",
        yaxis_title="N.º de registos",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    fig_freq.update_traces(marker_color="#BFA2DB")

    st.plotly_chart(fig_freq, use_container_width=True)

    zone_intensity = (
        pain_df
        .groupby("Localização", as_index=False)["Intensidade"]
        .mean()
        .sort_values(by="Intensidade", ascending=False)
    )

    fig_intensity = px.bar(
        zone_intensity,
        x="Localização",
        y="Intensidade",
        title="Intensidade média da dor por zona corporal"
    )

    fig_intensity.update_layout(
        xaxis_title="Zona corporal",
        yaxis_title="Intensidade média",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111827")
    )

    fig_intensity.update_traces(marker_color="#8E7CC3")

    st.plotly_chart(fig_intensity, use_container_width=True)

    st.divider()

    st.subheader("Análise por paciente")

    patient_names = sorted(pain_df["Paciente"].unique())

    selected_patient = st.selectbox(
        "Selecionar paciente",
        patient_names,
        key="body_map_patient_select"
    )

    patient_pain_df = pain_df[pain_df["Paciente"] == selected_patient]

    col5, col6, col7 = st.columns(3)

    with col5:
        st.metric("Registos do paciente", len(patient_pain_df))

    with col6:
        st.metric("Dor média do paciente", f"{patient_pain_df['Intensidade'].mean():.1f}/10")

    with col7:
        most_common_zone = patient_pain_df["Localização"].value_counts().idxmax()
        st.metric("Zona mais reportada", most_common_zone)

    patient_zone_summary = (
        patient_pain_df
        .groupby("Localização")
        .agg(
            Registos=("Localização", "count"),
            Intensidade_Média=("Intensidade", "mean"),
            Intensidade_Máxima=("Intensidade", "max")
        )
        .reset_index()
        .sort_values(by="Intensidade_Média", ascending=False)
    )

    patient_zone_summary["Intensidade_Média"] = patient_zone_summary["Intensidade_Média"].round(1)
    patient_zone_summary["Intensidade_Máxima"] = patient_zone_summary["Intensidade_Máxima"].round(1)

    st.dataframe(patient_zone_summary, use_container_width=True)


def get_goal_status_badge(progress):
    percentage = int(progress * 100)

    if progress >= 1:
        return """
        <span style="
            background-color: #D1FAE5;
            color: #065F46;
            border: 1.5px solid #8B5CF6;
            border-radius: 12px;
            padding: 6px 14px;
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
            display: inline-block;
        ">
            feito
        </span>
        """

    return f"""
    <span style="
        background-color: #F8DED6;
        color: #374151;
        border: 1px solid #E8B8A8;
        border-radius: 12px;
        padding: 6px 14px;
        font-size: 14px;
        font-weight: 500;
        white-space: nowrap;
        display: inline-block;
    ">
        {percentage}% concluído
    </span>
    """


def show_health_goals_page(users):
    show_page_header(
        "Metas de Saúde",
        "Acompanhamento de metas clínicas associadas ao sono, dor, exercício e monitorização."
    )

    user_names = [get_user_display_name(user) for user in users]

    selected_user_name = st.selectbox(
        "Selecionar paciente",
        user_names,
        key="goals_patient_select"
    )

    selected_user = next(
        (user for user in users if get_user_display_name(user) == selected_user_name),
        None
    )

    if selected_user is None:
        st.error("Não foi possível encontrar o paciente selecionado.")
        return

    user_doc_ref = selected_user["doc_ref"]

    sono_df, exercicio_df, dor_df, medicacao_df = get_patient_dataframes(user_doc_ref)

    media_sono = numeric_mean(sono_df, "Horas de Sono")
    media_dor = numeric_mean(dor_df, "Intensidade")

    total_exercicios = len(exercicio_df) if not exercicio_df.empty else 0
    total_medicacao = len(medicacao_df) if not medicacao_df.empty else 0
    total_registos = len(sono_df) + len(exercicio_df) + len(dor_df) + len(medicacao_df)

    st.subheader(f"Metas de {get_user_display_name(selected_user)}")

    if media_dor is not None:
        if media_dor < 5:
            dor_progress = 1.0
        else:
            dor_progress = max(0.0, min((10 - media_dor) / 5, 0.9))
    else:
        dor_progress = 0.0

    goals = [
        {
            "title": "Sono adequado",
            "description": "Objetivo: média de sono igual ou superior a 7 horas.",
            "progress": min((media_sono or 0) / 7, 1.0),
            "value": f"{media_sono:.1f} h" if media_sono is not None else "Sem dados",
        },
        {
            "title": "Controlo da dor",
            "description": "Objetivo: manter a dor média abaixo de 5/10.",
            "progress": dor_progress,
            "value": f"{media_dor:.1f}/10" if media_dor is not None else "Sem dados",
        },
        {
            "title": "Exercício físico",
            "description": "Objetivo: pelo menos 3 exercícios ou sessões registadas.",
            "progress": min(total_exercicios / 3, 1.0),
            "value": f"{total_exercicios} exercícios",
        },
        {
            "title": "Monitorização regular",
            "description": "Objetivo: ter pelo menos 7 registos clínicos no total.",
            "progress": min(total_registos / 7, 1.0),
            "value": f"{total_registos} registos",
        },
        {
            "title": "Registo de medicação",
            "description": "Objetivo: existir pelo menos 1 registo de medicação associado ao paciente.",
            "progress": 1.0 if total_medicacao > 0 else 0.0,
            "value": f"{total_medicacao} registos",
        },
    ]

    for goal in goals:
        progress = max(0, min(goal["progress"], 1))
        badge = get_goal_status_badge(progress)

        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"### {goal['title']}")
                st.markdown(goal["description"])
                st.markdown(f"**Estado atual:** {goal['value']}")

            with col2:
                st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
                st.markdown(badge, unsafe_allow_html=True)


def dataframe_to_table_data(df):
    if df.empty:
        return [["Sem dados registados"]]

    table_data = [list(df.columns)]

    for _, row in df.iterrows():
        table_data.append([str(value) for value in row.values])

    return table_data


def add_table_to_pdf(elements, title, df, styles):
    elements.append(Paragraph(title, styles["Heading2"]))
    elements.append(Spacer(1, 0.25 * cm))

    table_data = dataframe_to_table_data(df)

    table = Table(table_data, repeatRows=1)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#BFA2DB")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFFFF")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    elements.append(table)
    elements.append(Spacer(1, 0.6 * cm))


def generate_patient_pdf_report(user, user_doc_ref):
    if not REPORTLAB_AVAILABLE:
        return None

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()
    elements = []

    nome = get_user_display_name(user)
    email = user.get(USER_EMAIL_FIELD, "N/A")
    idade = user.get(USER_AGE_FIELD, "N/A")
    user_id = user.get(USER_ID_FIELD, "N/A")

    sono_df, exercicio_df, dor_df, medicacao_df = get_patient_dataframes(user_doc_ref)

    status, reason, _ = calculate_patient_status(sono_df, dor_df)

    data_relatorio = datetime.now().strftime("%d/%m/%Y %H:%M")

    elements.append(Paragraph("Relatório Clínico FIBRIVE", styles["Title"]))
    elements.append(Spacer(1, 0.4 * cm))

    elements.append(Paragraph("Dados do paciente", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * cm))

    patient_data = [
        ["Nome", nome],
        ["Email", email],
        ["Idade", str(idade)],
        ["ID do paciente", str(user_id)],
        ["Estado clínico", status],
        ["Motivo", reason],
        ["Data do relatório", data_relatorio],
    ]

    patient_table = Table(patient_data, colWidths=[4 * cm, 12 * cm])

    patient_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3E8FF")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#111111")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(patient_table)
    elements.append(Spacer(1, 0.7 * cm))

    elements.append(Paragraph("Resumo clínico", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * cm))

    media_sono = numeric_mean(sono_df, "Horas de Sono")
    media_qualidade = numeric_mean(sono_df, "Qualidade")
    media_dor = numeric_mean(dor_df, "Intensidade")

    resumo = [
        ["Média de horas de sono", f"{media_sono:.1f} h" if media_sono is not None else "Sem dados"],
        ["Média de qualidade do sono", f"{media_qualidade:.1f}" if media_qualidade is not None else "Sem dados"],
        ["Média de intensidade da dor", f"{media_dor:.1f}/10" if media_dor is not None else "Sem dados"],
        ["Total de exercícios registados", str(len(exercicio_df)) if not exercicio_df.empty else "0"],
        ["Registos de medicação", str(len(medicacao_df)) if not medicacao_df.empty else "0"],
    ]

    resumo_table = Table(resumo, colWidths=[7 * cm, 9 * cm])

    resumo_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F9FAFB")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(resumo_table)
    elements.append(Spacer(1, 0.8 * cm))

    add_table_to_pdf(elements, "Registos de sono", sono_df, styles)
    add_table_to_pdf(elements, "Registos de dor", dor_df, styles)
    add_table_to_pdf(elements, "Registos de exercício", exercicio_df, styles)
    add_table_to_pdf(elements, "Registos de medicação", medicacao_df, styles)

    elements.append(Spacer(1, 0.5 * cm))
    elements.append(
        Paragraph(
            "Relatório gerado automaticamente pelo dashboard clínico FIBRIVE.",
            styles["Normal"]
        )
    )

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf


def show_reports_page(users):
    show_page_header(
        "Relatórios",
        "Geração de relatórios clínicos em PDF por paciente."
    )

    if not REPORTLAB_AVAILABLE:
        st.error("A biblioteca reportlab não está instalada. Executa: py -m pip install reportlab")
        return

    user_names = [get_user_display_name(user) for user in users]

    selected_user_name = st.selectbox(
        "Selecionar paciente para relatório",
        user_names,
        key="reports_patient_select"
    )

    selected_user = next(
        (user for user in users if get_user_display_name(user) == selected_user_name),
        None
    )

    if selected_user is None:
        st.error("Não foi possível encontrar o paciente selecionado.")
        return

    user_doc_ref = selected_user["doc_ref"]

    show_user_info(selected_user)

    pdf_report = generate_patient_pdf_report(selected_user, user_doc_ref)

    if pdf_report is not None:
        st.download_button(
            label="Exportar relatório PDF",
            data=pdf_report,
            file_name=f"relatorio_fibrive_{get_user_display_name(selected_user).replace(' ', '_')}.pdf",
            mime="application/pdf"
        )


def show_patients_page(users):
    show_page_header(
        "Dashboard Clínico FIBRIVE",
        "Monitorização clínica personalizada de pacientes com fibromialgia."
    )

    user_names = [get_user_display_name(user) for user in users]

    selected_user_name = st.sidebar.selectbox(
        "Selecionar paciente",
        user_names
    )

    st.sidebar.markdown("---")
    logout_button()
    st.sidebar.markdown("---")

    selected_user = next(
        (user for user in users if get_user_display_name(user) == selected_user_name),
        None
    )

    if selected_user is None:
        st.error("Não foi possível encontrar o paciente selecionado.")
        st.stop()

    user_doc_ref = selected_user["doc_ref"]

    sono_df, exercicio_df, dor_df, medicacao_df = get_patient_dataframes(user_doc_ref)

    show_user_info(selected_user)

    show_patient_status(sono_df, dor_df)

    show_patient_summary_cards(sono_df, exercicio_df, dor_df, medicacao_df)

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

    st.divider()

    show_sono_dor_relation(sono_df, dor_df)


users = get_all_users()

if not users:
    st.warning("Não existem pacientes na coleção User.")
    st.stop()


if LOGO_PATH.exists():
    st.sidebar.image(str(LOGO_PATH), width=140)
else:
    st.sidebar.warning("Logo não encontrado.")


with st.sidebar:
    selected_page = option_menu(
        menu_title="Menu",
        options=[
            "Resumo Geral",
            "Pacientes",
            "Alertas",
            "Metas de Saúde",
            "Mapa Corporal",
            "Relatórios"
        ],
        icons=[
            "bar-chart-line",
            "person",
            "exclamation-triangle",
            "bullseye",
            "person-standing",
            "file-earmark-text"
        ],
        menu_icon="grid",
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#F8FAFC"
            },
            "icon": {
                "color": "#8E7CC3",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "16px",
                "color": "#111827",
                "text-align": "left",
                "margin": "4px 0",
                "border-radius": "12px",
                "padding": "10px 14px",
                "--hover-color": "#F3E8FF",
            },
            "nav-link-selected": {
                "background-color": "#EDE7F6",
                "color": "#111827",
                "font-weight": "700",
            },
            "menu-title": {
                "font-size": "22px",
                "font-weight": "800",
                "color": "#111827",
                "margin-bottom": "18px",
            },
        }
    )


if selected_page == "Resumo Geral":
    show_general_summary(users)

elif selected_page == "Pacientes":
    show_patients_page(users)

elif selected_page == "Alertas":
    show_alerts_page(users)

elif selected_page == "Metas de Saúde":
    show_health_goals_page(users)

elif selected_page == "Mapa Corporal":
    show_body_map_page(users)

elif selected_page == "Relatórios":
    show_reports_page(users)