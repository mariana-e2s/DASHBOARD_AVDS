import streamlit as st


def show_page_header(title, subtitle):
    st.markdown(
        f"""
        <h1>{title}</h1>
        <p class="page-subtitle">{subtitle}</p>
        """,
        unsafe_allow_html=True
    )