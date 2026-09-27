import streamlit as st
import pandas as pd

def visit_mode_page(df):
    st.header("🧳 Visit Mode & User History")

    visit_mode = st.multiselect(
        "Select Visit Mode",
        options=df["VisitMode"].unique(),
        default=df["VisitMode"].unique()
    )

    st.dataframe(df[df["VisitMode"].isin(visit_mode)].head(10))
    return df[df["VisitMode"].isin(visit_mode)]
