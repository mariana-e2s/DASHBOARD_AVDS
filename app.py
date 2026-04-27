import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
from fpdf import FPDF
import io
import base64
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FibriVe · Dashboard Clínico",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg:        #0d0f14;
    --surface:   #151820;
    --surface2:  #1c2030;
    --border:    #252a3a;
    --primary:   #7c6af7;
    --accent:    #e879a0;
    --teal:      #38d9c0;
    --amber:     #f5a623;
    --red:       #ff5c6c;
    --text:      #e8eaf2;
    --muted:     #7a82a0;
    --radius:    14px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Metric cards */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: transform .2s, border-color .2s;
}
.metric-card:hover { transform: translateY(-2px); border-color: var(--primary); }
.metric-card::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 4px 0 0 4px;
}
.metric-card.purple::before  { background: var(--primary); }
.metric-card.pink::before    { background: var(--accent); }
.metric-card.teal::before    { background: var(--teal); }
.metric-card.amber::before   { background: var(--amber); }
.metric-card.red::before     { background: var(--red); }

.metric-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px; font-weight: 500;
    letter-spacing: .12em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 8px;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem; font-weight: 800;
    line-height: 1; color: var(--text);
}
.metric-delta {
    font-size: 12px; margin-top: 6px;
    font-weight: 500;
}
.delta-up   { color: var(--red); }
.delta-down { color: var(--teal); }
.delta-same { color: var(--muted); }

/* Alert cards */
.alert-card {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex; align-items: flex-start; gap: 12px;
    border: 1px solid var(--border);
}
.alert-card.critical { border-left: 4px solid var(--red); }
.alert-card.warning  { border-left: 4px solid var(--amber); }
.alert-card.ok       { border-left: 4px solid var(--teal); }
.alert-icon { font-size: 18px; margin-top: 1px; }
.alert-title { font-weight: 600; font-size: 13px; }
.alert-desc  { font-size: 12px; color: var(--muted); margin-top: 2px; }

/* Section headings */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 13px; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    color: var(--muted); margin: 28px 0 14px 0;
    display: flex; align-items: center; gap: 8px;
}
.section-heading span { color: var(--primary); }

/* Patient pill */
.patient-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 6px 14px 6px 8px;
    font-size: 13px; font-weight: 500;
}
.patient-avatar {
    width: 26px; height: 26px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; color: white;
}

/* Body map container */
.bodymap-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    text-align: center;
}

/* Tabs override */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: var(--radius) var(--radius) 0 0;
    border: 1px solid var(--border) !important;
    border-bottom: none !important;
    gap: 4px; padding: 6px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
    padding: 8px 18px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius) var(--radius) !important;
    padding: 20px !important;
}

/* Selectbox & inputs */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Mock data generator ───────────────────────────────────────────────────────
@st.cache_data
def generate_mock_data(patient_id: str, days: int = 90):
    rng = random.Random(hash(patient_id))
    np.random.seed(abs(hash(patient_id)) % 2**32)
    dates = [datetime.today() - timedelta(days=days - i) for i in range(days)]

    # Simulate a "crisis" period around day 60-70
    pain_base = [rng.uniform(3, 6) for _ in range(days)]
    for i in range(55, 72):
        pain_base[i] = min(10, pain_base[i] + rng.uniform(2, 4))

    records = []
    for i, d in enumerate(dates):
        records.append({
            "date":             d,
            "pain_level":       round(min(10, max(0, pain_base[i] + rng.gauss(0, .5))), 1),
            "sleep_hours":      round(max(2, min(10, 6.5 - pain_base[i] * .15 + rng.gauss(0, .8))), 1),
            "sleep_awakenings": rng.randint(0, 5),
            "fatigue_awake":    rng.randint(1, 5),
            "stress_daily":     round(min(10, max(0, pain_base[i] * .7 + rng.gauss(0, 1.2))), 1),
            "stress_home":      round(min(10, max(0, rng.uniform(1, 7))), 1),
            "medication_taken": rng.random() > 0.1,
            "pain_locations":   rng.sample(["Cervical", "Ombros", "Costas", "Lombares", "Pernas", "Braços", "Cabeça"], k=rng.randint(1, 4)),
        })
    return pd.DataFrame(records)

PATIENTS = {
    "P001 — Ana Ferreira":    {"age": 42, "since": "2021-03", "medication": "Duloxetina 60mg + Pregabalina 150mg", "gender": "F"},
    "P002 — Miguel Costa":    {"age": 35, "since": "2022-07", "medication": "Amitriptilina 25mg",                  "gender": "M"},
    "P003 — Sofia Rodrigues": {"age": 51, "since": "2019-11", "medication": "Pregabalina 300mg + Tramadol 50mg",   "gender": "F"},
    "P004 — Rui Teixeira":    {"age": 28, "since": "2023-02", "medication": "Duloxetina 30mg",                     "gender": "M"},
}

# ── Plotly theme helper ───────────────────────────────────────────────────────
PLOT_BG   = "#151820"
PLOT_GRID = "#252a3a"
PLOT_TEXT = "#7a82a0"
COLORS    = {"pain": "#e879a0", "sleep": "#7c6af7", "stress": "#f5a623", "medication": "#38d9c0"}

def dark_layout(fig, title="", height=320):
    fig.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=dict(family="DM Sans", color=PLOT_TEXT, size=12),
        title=dict(text=title, font=dict(family="Syne", size=14, color="#e8eaf2"), x=0),
        xaxis=dict(gridcolor=PLOT_GRID, showgrid=True, zeroline=False, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=PLOT_GRID, showgrid=True, zeroline=False, tickfont=dict(size=11)),
        margin=dict(l=8, r=8, t=40 if title else 8, b=8),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=PLOT_GRID, font=dict(size=11)),
    )
    return fig

# ── Alert engine ─────────────────────────────────────────────────────────────
def compute_alerts(df: pd.DataFrame):
    alerts = []
    last7   = df.tail(7)
    last30  = df.tail(30)

    avg_pain_7  = last7["pain_level"].mean()
    avg_pain_30 = last30["pain_level"].mean()
    avg_sleep_7 = last7["sleep_hours"].mean()

    if avg_pain_7 >= 7:
        alerts.append(("critical", "🔴", "Crise de dor activa",
                        f"Média de dor nos últimos 7 dias: {avg_pain_7:.1f}/10"))
    elif avg_pain_7 > avg_pain_30 * 1.25:
        alerts.append(("warning", "🟠", "Tendência de aumento da dor",
                        f"Dor +{((avg_pain_7/avg_pain_30)-1)*100:.0f}% vs. média mensal"))
    else:
        alerts.append(("ok", "🟢", "Dor estável",
                        f"Média de dor nos últimos 7 dias: {avg_pain_7:.1f}/10"))

    if avg_sleep_7 < 5:
        alerts.append(("critical", "🔴", "Sono insuficiente",
                        f"Média de {avg_sleep_7:.1f}h/noite nos últimos 7 dias"))
    elif avg_sleep_7 < 6:
        alerts.append(("warning", "🟠", "Sono abaixo do recomendado",
                        f"Média de {avg_sleep_7:.1f}h/noite"))

    missed = int((~last7["medication_taken"]).sum())
    if missed >= 3:
        alerts.append(("critical", "🔴", f"Adesão terapêutica baixa",
                        f"{missed}/7 tomas em falta nos últimos 7 dias"))
    elif missed >= 1:
        alerts.append(("warning", "🟠", f"Tomas em falta: {missed}",
                        "Verificar adesão à medicação"))

    avg_stress_7 = last7["stress_daily"].mean()
    if avg_stress_7 >= 7:
        alerts.append(("warning", "🟠", "Stress elevado",
                        f"Média de stress diário: {avg_stress_7:.1f}/10"))

    return alerts

# ── PDF export ────────────────────────────────────────────────────────────────
def generate_pdf(patient_name, patient_info, df, alerts):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(13, 15, 20)

    # Header
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(124, 106, 247)
    pdf.cell(0, 10, "FibriVe · Relatório Clínico", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 120)
    pdf.cell(0, 6, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(4)

    # Patient info
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(232, 234, 242)
    pdf.cell(0, 8, f"Paciente: {patient_name.split(' — ')[1] if ' — ' in patient_name else patient_name}", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(122, 130, 160)
    pdf.cell(0, 6, f"Idade: {patient_info['age']} anos  |  Fibromialgia desde: {patient_info['since']}  |  Medicação: {patient_info['medication']}", ln=True)
    pdf.ln(6)

    # Alerts
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(232, 234, 242)
    pdf.cell(0, 8, "Alertas Clínicos", ln=True)
    for sev, _, title, desc in alerts:
        color = (255, 92, 108) if sev == "critical" else (245, 166, 35) if sev == "warning" else (56, 217, 192)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*color)
        pdf.cell(0, 6, f"  • {title}: ", ln=False)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(122, 130, 160)
        pdf.cell(0, 6, desc, ln=True)
    pdf.ln(4)

    # Stats table
    last30 = df.tail(30)
    stats = {
        "Dor média (30d)":          f"{last30['pain_level'].mean():.1f} / 10",
        "Sono médio (30d)":         f"{last30['sleep_hours'].mean():.1f} h",
        "Stress médio (30d)":       f"{last30['stress_daily'].mean():.1f} / 10",
        "Adesão terapêutica (30d)": f"{last30['medication_taken'].mean()*100:.0f}%",
        "Despertar médio (30d)":    f"{last30['sleep_awakenings'].mean():.1f}x / noite",
    }
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(232, 234, 242)
    pdf.cell(0, 8, "Resumo Estatístico (últimos 30 dias)", ln=True)
    for k, v in stats.items():
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(122, 130, 160)
        pdf.cell(90, 7, k, border="B")
        pdf.set_text_color(232, 234, 242)
        pdf.cell(0, 7, v, border="B", ln=True)

    out = pdf.output(dest="S")
    if isinstance(out, str):
        out = out.encode("latin-1")
    return out

# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding: 16px 0 24px 0;'>
        <div style='font-family:Syne,sans-serif; font-size:22px; font-weight:800; color:#e8eaf2;'>
            Fibri<span style='color:#7c6af7;'>Ve</span>
        </div>
        <div style='font-size:11px; color:#7a82a0; letter-spacing:.1em; text-transform:uppercase; margin-top:2px;'>
            Dashboard Clínico
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Paciente**")
    selected_patient = st.selectbox("", list(PATIENTS.keys()), label_visibility="collapsed")
    patient_info = PATIENTS[selected_patient]

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    initials = "".join(w[0] for w in selected_patient.split(" — ")[1].split()[:2]) if " — " in selected_patient else "P"
    st.markdown(f"""
    <div class='patient-pill'>
        <div class='patient-avatar'>{initials}</div>
        <span>{selected_patient.split(' — ')[1] if ' — ' in selected_patient else selected_patient}</span>
    </div>
    <div style='font-size:12px; color:#7a82a0; margin-top:10px;'>
        🎂 {patient_info['age']} anos &nbsp;·&nbsp; ♀ Feminino<br>
        📅 Fibromialgia desde {patient_info['since']}<br>
        💊 <span style='color:#e8eaf2;'>{patient_info['medication']}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Período de análise**")
    period = st.selectbox("", ["Últimos 30 dias", "Últimos 60 dias", "Últimos 90 dias"], label_visibility="collapsed")
    days_map = {"Últimos 30 dias": 30, "Últimos 60 dias": 60, "Últimos 90 dias": 90}
    n_days = days_map[period]

    st.markdown("---")
    st.markdown("**Firestore**")
    st.markdown("<div style='font-size:12px; color:#7a82a0;'>🟢 Ligado (simulado)<br>Última sync: agora</div>", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
df_full = generate_mock_data(selected_patient, days=90)
df = df_full.tail(n_days).copy().reset_index(drop=True)
alerts = compute_alerts(df)

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

# ── Page header ───────────────────────────────────────────────────────────────
col_title, col_export = st.columns([5, 1])
with col_title:
    name_display = selected_patient.split(" — ")[1] if " — " in selected_patient else selected_patient
    st.markdown(f"""
    <div style='margin-bottom:4px;'>
        <span style='font-family:Syne,sans-serif; font-size:26px; font-weight:800; color:#e8eaf2;'>{name_display}</span>
        <span style='font-size:13px; color:#7a82a0; margin-left:12px;'>· {period}</span>
    </div>
    """, unsafe_allow_html=True)

with col_export:
    pdf_bytes = generate_pdf(selected_patient, patient_info, df, alerts)
    b64 = base64.b64encode(pdf_bytes).decode()
    fname = f"FibriVe_{name_display.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    st.markdown(f"""
    <a href="data:application/pdf;base64,{b64}" download="{fname}"
       style="display:inline-block; background:#7c6af7; color:white;
              padding:9px 18px; border-radius:8px; text-decoration:none;
              font-family:'DM Sans',sans-serif; font-size:13px; font-weight:600;
              margin-top:4px;">
        ⬇ Exportar PDF
    </a>
    """, unsafe_allow_html=True)

# ── KPI cards ─────────────────────────────────────────────────────────────────
last7  = df.tail(7)
prev7  = df.iloc[-14:-7] if len(df) >= 14 else df.head(7)

avg_pain   = last7["pain_level"].mean()
avg_sleep  = last7["sleep_hours"].mean()
avg_stress = last7["stress_daily"].mean()
med_adh    = last7["medication_taken"].mean() * 100

dpain  = avg_pain  - prev7["pain_level"].mean()
dsleep = avg_sleep - prev7["sleep_hours"].mean()
dstr   = avg_stress - prev7["stress_daily"].mean()

def delta_html(val, invert=False):
    arrow = "↑" if val > 0 else "↓"
    cls   = ("delta-up" if val > 0 else "delta-down") if not invert else ("delta-down" if val > 0 else "delta-up")
    return f'<span class="{cls}">{arrow} {abs(val):.1f} vs. semana anterior</span>'

c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    (c1, "purple", "Dor Média",     f"{avg_pain:.1f}", "/10",  delta_html(dpain)),
    (c2, "teal",   "Sono Médio",    f"{avg_sleep:.1f}", "h",   delta_html(dsleep, invert=True)),
    (c3, "amber",  "Stress Diário", f"{avg_stress:.1f}", "/10", delta_html(dstr)),
    (c4, "pink",   "Adesão Terapêutica", f"{med_adh:.0f}", "%", ""),
    (c5, "red",    "Despertar Noturno", f"{last7['sleep_awakenings'].mean():.1f}", "x/noite", ""),
]

for col, color, label, val, unit, delta in cards:
    with col:
        st.markdown(f"""
        <div class='metric-card {color}'>
            <div class='metric-label'>{label}</div>
            <div class='metric-value'>{val}<span style='font-size:1rem; font-weight:400; color:#7a82a0;'>{unit}</span></div>
            <div class='metric-delta'>{delta}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Alerts ────────────────────────────────────────────────────────────────────
if alerts:
    st.markdown("<div class='section-heading'><span>●</span> Alertas Clínicos</div>", unsafe_allow_html=True)
    acols = st.columns(min(len(alerts), 3))
    for i, (sev, icon, title, desc) in enumerate(alerts):
        with acols[i % len(acols)]:
            st.markdown(f"""
            <div class='alert-card {sev}'>
                <div class='alert-icon'>{icon}</div>
                <div>
                    <div class='alert-title'>{title}</div>
                    <div class='alert-desc'>{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📈 Evolução Temporal", "🗺 Mapa de Dor", "💊 Medicação & Sono", "🔗 Correlações"])

# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    # Main trend chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["pain_level"].rolling(7, min_periods=1).mean(),
        name="Dor (média 7d)", line=dict(color=COLORS["pain"], width=2.5),
        fill="tozeroy", fillcolor="rgba(232,121,160,.08)"
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["pain_level"], name="Dor (diária)",
        line=dict(color=COLORS["pain"], width=1, dash="dot"),
        opacity=0.4, showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["stress_daily"].rolling(7, min_periods=1).mean(),
        name="Stress (média 7d)", line=dict(color=COLORS["stress"], width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["sleep_hours"].rolling(7, min_periods=1).mean(),
        name="Sono horas (média 7d)", line=dict(color=COLORS["sleep"], width=2.5),
        yaxis="y2"
    ))
    # Shade crisis zones where pain > 7
    crisis_mask = df["pain_level"] > 7
    in_crisis = False
    x0 = None
    for idx, row in df.iterrows():
        if crisis_mask[idx] and not in_crisis:
            in_crisis = True; x0 = row["date"]
        elif not crisis_mask[idx] and in_crisis:
            in_crisis = False
            fig.add_vrect(x0=x0, x1=row["date"], fillcolor="rgba(255,92,108,.07)",
                          line_width=0, annotation_text="Crise", annotation_font_size=10,
                          annotation_font_color="#ff5c6c")

    fig.update_layout(
        yaxis2=dict(overlaying="y", side="right", title="Horas de Sono",
                    showgrid=False, tickfont=dict(size=11)),
        legend=dict(orientation="h", y=1.1),
    )
    dark_layout(fig, "Evolução Temporal · Dor / Stress / Sono", height=380)
    st.plotly_chart(fig, use_container_width=True)

    # Weekly heatmap
    st.markdown("<div class='section-heading'><span>●</span> Calendário de Intensidade de Dor</div>", unsafe_allow_html=True)
    df["week"] = df["date"].apply(lambda d: d.strftime("%U"))
    df["weekday"] = df["date"].apply(lambda d: d.strftime("%a"))
    pivot = df.pivot_table(index="weekday", columns="date", values="pain_level", aggfunc="mean")
    days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    # Build heatmap from last 30 days
    last30 = df.tail(30)
    last30 = last30.copy()
    last30["dow"] = last30["date"].dt.dayofweek
    last30["week_num"] = (last30["date"] - last30["date"].min()).dt.days // 7

    hm_z   = [[None]*7 for _ in range(last30["week_num"].max()+1)]
    hm_txt = [[""]*7    for _ in range(last30["week_num"].max()+1)]
    for _, row in last30.iterrows():
        w = row["week_num"]; d = row["dow"]
        hm_z[w][d]   = row["pain_level"]
        hm_txt[w][d] = f"{row['date'].strftime('%d %b')}<br>Dor: {row['pain_level']}"

    fig2 = go.Figure(go.Heatmap(
        z=hm_z, text=hm_txt, hoverinfo="text",
        x=["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"],
        colorscale=[[0,"#1c2030"],[0.4,"#7c6af7"],[0.7,"#e879a0"],[1,"#ff5c6c"]],
        zmin=0, zmax=10, showscale=True,
        colorbar=dict(tickfont=dict(color=PLOT_TEXT), outlinecolor=PLOT_GRID, thickness=12)
    ))
    dark_layout(fig2, height=220)
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("<div class='section-heading'><span>●</span> Localização da Dor (últimos 30 dias)</div>", unsafe_allow_html=True)

    # Aggregate pain locations
    location_counts = {}
    for locs in df.tail(30)["pain_locations"]:
        for loc in locs:
            location_counts[loc] = location_counts.get(loc, 0) + 1
    loc_df = pd.DataFrame(list(location_counts.items()), columns=["Zona", "Frequência"]).sort_values("Frequência", ascending=True)

    col_bmap, col_bar = st.columns([1, 1])
    with col_bmap:
        # SVG body map with pain intensity overlay
        region_freq = location_counts
        max_freq     = max(region_freq.values()) if region_freq else 1

        def opacity(zone):
            return 0.15 + 0.75 * (region_freq.get(zone, 0) / max_freq)

        st.markdown(f"""
        <div class='bodymap-container'>
            <div style='font-size:12px; color:#7a82a0; margin-bottom:12px; text-transform:uppercase; letter-spacing:.08em;'>
                Mapa de Dor · Frequência de Ocorrência
            </div>
            <svg viewBox="0 0 220 420" xmlns="http://www.w3.org/2000/svg" style="max-height:360px; width:auto;">
              <defs>
                <radialGradient id="gCervical"  cx="50%" cy="50%"><stop offset="0%" stop-color="#ff5c6c" stop-opacity="{opacity('Cervical'):.2f}"/><stop offset="100%" stop-color="#ff5c6c" stop-opacity="0"/></radialGradient>
                <radialGradient id="gOmbros"    cx="50%" cy="50%"><stop offset="0%" stop-color="#e879a0" stop-opacity="{opacity('Ombros'):.2f}"/><stop offset="100%" stop-color="#e879a0" stop-opacity="0"/></radialGradient>
                <radialGradient id="gCostas"    cx="50%" cy="50%"><stop offset="0%" stop-color="#f5a623" stop-opacity="{opacity('Costas'):.2f}"/><stop offset="100%" stop-color="#f5a623" stop-opacity="0"/></radialGradient>
                <radialGradient id="gLombares"  cx="50%" cy="50%"><stop offset="0%" stop-color="#f5a623" stop-opacity="{opacity('Lombares'):.2f}"/><stop offset="100%" stop-color="#f5a623" stop-opacity="0"/></radialGradient>
                <radialGradient id="gPernas"    cx="50%" cy="50%"><stop offset="0%" stop-color="#7c6af7" stop-opacity="{opacity('Pernas'):.2f}"/><stop offset="100%" stop-color="#7c6af7" stop-opacity="0"/></radialGradient>
                <radialGradient id="gBracos"    cx="50%" cy="50%"><stop offset="0%" stop-color="#38d9c0" stop-opacity="{opacity('Braços'):.2f}"/><stop offset="100%" stop-color="#38d9c0" stop-opacity="0"/></radialGradient>
                <radialGradient id="gCabeca"    cx="50%" cy="50%"><stop offset="0%" stop-color="#ff5c6c" stop-opacity="{opacity('Cabeça'):.2f}"/><stop offset="100%" stop-color="#ff5c6c" stop-opacity="0"/></radialGradient>
              </defs>
              <!-- Body silhouette -->
              <g opacity="0.6">
                <!-- Head -->
                <circle cx="110" cy="38" r="26" fill="#252a3a" stroke="#3a4060" stroke-width="1.5"/>
                <!-- Neck -->
                <rect x="102" y="62" width="16" height="14" rx="4" fill="#252a3a" stroke="#3a4060" stroke-width="1"/>
                <!-- Torso -->
                <rect x="74" y="74" width="72" height="90" rx="10" fill="#252a3a" stroke="#3a4060" stroke-width="1.5"/>
                <!-- Hips -->
                <rect x="78" y="158" width="64" height="30" rx="8" fill="#252a3a" stroke="#3a4060" stroke-width="1"/>
                <!-- Left arm -->
                <rect x="46" y="76" width="26" height="80" rx="10" fill="#252a3a" stroke="#3a4060" stroke-width="1"/>
                <!-- Right arm -->
                <rect x="148" y="76" width="26" height="80" rx="10" fill="#252a3a" stroke="#3a4060" stroke-width="1"/>
                <!-- Left leg -->
                <rect x="80" y="186" width="28" height="110" rx="10" fill="#252a3a" stroke="#3a4060" stroke-width="1"/>
                <!-- Right leg -->
                <rect x="112" y="186" width="28" height="110" rx="10" fill="#252a3a" stroke="#3a4060" stroke-width="1"/>
                <!-- Feet -->
                <ellipse cx="94" cy="303" rx="18" ry="10" fill="#252a3a" stroke="#3a4060" stroke-width="1"/>
                <ellipse cx="126" cy="303" rx="18" ry="10" fill="#252a3a" stroke="#3a4060" stroke-width="1"/>
              </g>
              <!-- Pain overlays -->
              <ellipse cx="110" cy="38"  rx="30" ry="30" fill="url(#gCabeca)"/>
              <ellipse cx="110" cy="72"  rx="22" ry="14" fill="url(#gCervical)"/>
              <ellipse cx="110" cy="90"  rx="54" ry="20" fill="url(#gOmbros)"/>
              <ellipse cx="110" cy="115" rx="40" ry="28" fill="url(#gCostas)"/>
              <ellipse cx="110" cy="155" rx="38" ry="22" fill="url(#gLombares)"/>
              <ellipse cx="59"  cy="116" rx="20" ry="32" fill="url(#gBracos)"/>
              <ellipse cx="161" cy="116" rx="20" ry="32" fill="url(#gBracos)"/>
              <ellipse cx="94"  cy="238" rx="18" ry="46" fill="url(#gPernas)"/>
              <ellipse cx="126" cy="238" rx="18" ry="46" fill="url(#gPernas)"/>
              <!-- Labels -->
              <text x="148" y="42"  font-family="DM Sans" font-size="9" fill="#7a82a0">Cabeça</text>
              <text x="148" y="76"  font-family="DM Sans" font-size="9" fill="#7a82a0">Cervical</text>
              <text x="148" y="94"  font-family="DM Sans" font-size="9" fill="#7a82a0">Ombros</text>
              <text x="148" y="118" font-family="DM Sans" font-size="9" fill="#7a82a0">Costas</text>
              <text x="148" y="158" font-family="DM Sans" font-size="9" fill="#7a82a0">Lombares</text>
              <text x="10"  cy="116" font-family="DM Sans" font-size="9" fill="#7a82a0">Braços</text>
              <text x="10"  y="240" font-family="DM Sans" font-size="9" fill="#7a82a0">Pernas</text>
            </svg>
            <div style='font-size:10px; color:#7a82a0; margin-top:8px;'>Intensidade proporcional à frequência de registo</div>
        </div>
        """, unsafe_allow_html=True)

    with col_bar:
        fig_loc = go.Figure(go.Bar(
            x=loc_df["Frequência"], y=loc_df["Zona"],
            orientation="h",
            marker=dict(
                color=loc_df["Frequência"],
                colorscale=[[0,"#252a3a"],[0.5,"#7c6af7"],[1,"#e879a0"]],
                showscale=False,
            ),
            text=loc_df["Frequência"], textposition="inside",
            textfont=dict(color="white", size=11),
        ))
        dark_layout(fig_loc, "Frequência por Zona (últimos 30 dias)", height=360)
        st.plotly_chart(fig_loc, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        # Sleep composition
        fig_sleep = make_subplots(specs=[[{"secondary_y": True}]])
        fig_sleep.add_trace(go.Bar(
            x=df["date"], y=df["sleep_hours"],
            name="Horas de sono", marker_color=COLORS["sleep"], opacity=0.7
        ))
        fig_sleep.add_trace(go.Scatter(
            x=df["date"], y=df["sleep_awakenings"],
            name="Despertares", line=dict(color=COLORS["stress"], width=2),
            mode="lines+markers", marker=dict(size=4)
        ), secondary_y=True)
        fig_sleep.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
            font=dict(family="DM Sans", color=PLOT_TEXT),
            title=dict(text="Sono · Horas & Despertares", font=dict(family="Syne", size=13, color="#e8eaf2"), x=0),
            margin=dict(l=8, r=8, t=40, b=8), height=300,
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
            xaxis=dict(gridcolor=PLOT_GRID),
            yaxis=dict(gridcolor=PLOT_GRID, title="Horas"),
            yaxis2=dict(gridcolor="rgba(0,0,0,0)", title="Despertares"),
        )
        st.plotly_chart(fig_sleep, use_container_width=True)

    with col_b:
        # Fatigue on wake distribution
        fig_fat = go.Figure()
        fatigue_counts = df["fatigue_awake"].value_counts().sort_index()
        fig_fat.add_trace(go.Bar(
            x=[f"Nível {i}" for i in fatigue_counts.index],
            y=fatigue_counts.values,
            marker=dict(
                color=fatigue_counts.values,
                colorscale=[[0,"#38d9c0"],[0.5,"#7c6af7"],[1,"#ff5c6c"]],
                showscale=False,
            ),
        ))
        dark_layout(fig_fat, "Cansaço ao Acordar (distribuição)", height=300)
        st.plotly_chart(fig_fat, use_container_width=True)

    # Medication adherence timeline
    st.markdown("<div class='section-heading'><span>●</span> Aderência Terapêutica</div>", unsafe_allow_html=True)
    df["med_int"] = df["medication_taken"].astype(int)
    fig_med = go.Figure()
    fig_med.add_trace(go.Bar(
        x=df["date"], y=df["med_int"],
        marker_color=[COLORS["medication"] if v else "#ff5c6c" for v in df["medication_taken"]],
        name="Tomou medicação",
        hovertext=df["medication_taken"].map({True: "✅ Tomou", False: "❌ Não tomou"}),
        hoverinfo="x+text",
    ))
    adh_roll = df["med_int"].rolling(7, min_periods=1).mean() * 100
    fig_med.add_trace(go.Scatter(
        x=df["date"], y=adh_roll,
        name="Aderência 7d (%)", line=dict(color=COLORS["stress"], width=2),
        yaxis="y2"
    ))
    fig_med.update_layout(
        yaxis2=dict(overlaying="y", side="right", range=[0, 120], showgrid=False),
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=dict(family="DM Sans", color=PLOT_TEXT),
        title=dict(text="Tomas de Medicação & Aderência (7d)", font=dict(family="Syne", size=13, color="#e8eaf2"), x=0),
        margin=dict(l=8, r=8, t=40, b=8), height=260,
        xaxis=dict(gridcolor=PLOT_GRID),
        yaxis=dict(gridcolor=PLOT_GRID, range=[0, 1.5], tickvals=[0, 1], ticktext=["Não", "Sim"]),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    )
    st.plotly_chart(fig_med, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    col_x, col_y = st.columns(2)
    with col_x:
        # Pain vs Stress scatter
        fig_sc = px.scatter(
            df, x="stress_daily", y="pain_level",
            color="sleep_hours", size="sleep_awakenings",
            color_continuous_scale=[[0,"#38d9c0"],[0.5,"#7c6af7"],[1,"#ff5c6c"]],
            labels={"stress_daily": "Stress Diário", "pain_level": "Nível de Dor", "sleep_hours": "Sono (h)"},
            hover_data={"date": "|%d/%m"},
        )
        corr_val = df["stress_daily"].corr(df["pain_level"])
        fig_sc.add_annotation(
            x=0.98, y=0.02, xref="paper", yref="paper",
            text=f"r = {corr_val:.2f}", showarrow=False,
            font=dict(size=13, color="#7c6af7", family="Syne"), xanchor="right"
        )
        dark_layout(fig_sc, "Correlação Dor × Stress", height=340)
        st.plotly_chart(fig_sc, use_container_width=True)

    with col_y:
        # Correlation heatmap
        corr_cols = ["pain_level", "sleep_hours", "sleep_awakenings", "fatigue_awake", "stress_daily", "stress_home"]
        corr_labels = ["Dor", "Sono (h)", "Despertares", "Cansaço", "Stress Diário", "Stress Casa"]
        corr_matrix = df[corr_cols].corr()

        fig_hm = go.Figure(go.Heatmap(
            z=corr_matrix.values,
            x=corr_labels, y=corr_labels,
            colorscale=[[0,"#3a1a6e"],[0.5,"#252a3a"],[1,"#7c6af7"]],
            zmin=-1, zmax=1,
            text=np.round(corr_matrix.values, 2),
            hoverinfo="text+z",
            colorbar=dict(tickfont=dict(color=PLOT_TEXT), outlinecolor=PLOT_GRID, thickness=12),
        ))
        fig_hm.update_traces(texttemplate="%{text}", textfont=dict(size=11, color="white"))
        dark_layout(fig_hm, "Matriz de Correlação", height=340)
        st.plotly_chart(fig_hm, use_container_width=True)

    # Predictive risk gauge
    st.markdown("<div class='section-heading'><span>●</span> Índice de Risco de Crise (próximos 7 dias)</div>", unsafe_allow_html=True)
    last5 = df.tail(5)
    risk_score = (
        last5["pain_level"].mean() * 0.4 +
        last5["stress_daily"].mean() * 0.3 +
        (8 - last5["sleep_hours"].mean()) * 0.2 +
        last5["sleep_awakenings"].mean() * 0.1
    ) / 10 * 100
    risk_score = min(100, max(0, risk_score))

    col_gauge, col_risk_text = st.columns([1, 2])
    with col_gauge:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            number=dict(suffix="%", font=dict(family="Syne", size=36, color="#e8eaf2")),
            gauge=dict(
                axis=dict(range=[0, 100], tickcolor=PLOT_TEXT, tickfont=dict(size=10)),
                bar=dict(color="#e879a0"),
                bgcolor=PLOT_GRID,
                steps=[
                    dict(range=[0, 33],  color="#1c2030"),
                    dict(range=[33, 66], color="#252035"),
                    dict(range=[66, 100], color="#2a1a1a"),
                ],
                threshold=dict(line=dict(color="#ff5c6c", width=3), thickness=0.8, value=75),
            )
        ))
        dark_layout(fig_gauge, height=260)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_risk_text:
        risk_level = "Alto" if risk_score > 66 else "Moderado" if risk_score > 33 else "Baixo"
        risk_color = "#ff5c6c" if risk_score > 66 else "#f5a623" if risk_score > 33 else "#38d9c0"
        st.markdown(f"""
        <div class='metric-card' style='margin-top:16px;'>
            <div class='metric-label'>Avaliação de Risco</div>
            <div style='font-family:Syne,sans-serif; font-size:2rem; font-weight:800; color:{risk_color};'>{risk_level}</div>
            <div style='font-size:13px; color:#7a82a0; margin-top:8px; line-height:1.6;'>
                Com base nos últimos 5 dias de dados:<br>
                • Dor média: <b style='color:#e8eaf2;'>{last5['pain_level'].mean():.1f}/10</b><br>
                • Stress médio: <b style='color:#e8eaf2;'>{last5['stress_daily'].mean():.1f}/10</b><br>
                • Sono médio: <b style='color:#e8eaf2;'>{last5['sleep_hours'].mean():.1f}h</b><br>
                • Despertares: <b style='color:#e8eaf2;'>{last5['sleep_awakenings'].mean():.1f}x/noite</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
