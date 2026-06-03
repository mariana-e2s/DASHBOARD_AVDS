import streamlit as st


def apply_styles():
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