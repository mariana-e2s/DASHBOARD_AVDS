import streamlit as st
import pandas as pd
import plotly.express as px

from repositories.user_repository import get_user_display_name
from repositories.dor_repository import get_dor_by_user
from utils.data_utils import to_dataframe
from components.layout import show_page_header


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