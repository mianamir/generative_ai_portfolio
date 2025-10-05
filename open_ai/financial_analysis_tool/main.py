import streamlit as st
import pandas as pd
from custom_open_ai_helpers import extract_financial_data_helper

col1, col2 = st.columns([3,2])

financial_data_df = pd.DataFrame({
        "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Value": ["", "", "", "", ""]
    })

with col1:
    st.markdown(
        """
        <h4 style="color:#0073e6; text-align:center;">Modern Fintech Analysis GenAI Tool</h4>
        """,
        unsafe_allow_html=True
    )
    news_article = st.text_area("Put financial news text from sample_stocks_prompts.md", height=300)
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #0073e6; 
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            height: 40px;
            width: 100%;
            transition: background-color 0.3s;
        }
        div.stButton > button:first-child:hover {
            background-color: #1a8cff; 
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("Get Analysis"):
        financial_data_df = extract_financial_data_helper(news_article)

with col2:
    st.markdown("<br/>" * 5, unsafe_allow_html=True)
    st.dataframe(
        financial_data_df,
        column_config={
            "Measure": st.column_config.Column(width=150),
            "Value": st.column_config.Column(width=150)
        },
        hide_index=True
    )