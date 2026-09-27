import streamlit as st
import pandas as pd

def continent_page(df):
    st.header("🌍 Select Continent")

    continent = st.multiselect(
        "Choose Continent",
        options=sorted(df["Continent"].unique()),
        default=sorted(df["Continent"].unique())
    )

    return df[df["Continent"].isin(continent)]
