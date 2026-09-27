import streamlit as st
import pickle
import pandas as pd
import os

def prediction_page():
    st.header("⭐ Predict Visit Mode (ML)")
    
    # Get the directory of the current file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load data for options
    df = pd.read_csv(os.path.join(base_dir, "..", "Tourism_Project", "final_data.csv"))
    
    # Load model and encoders
    model = pickle.load(open(os.path.join(base_dir, "..", "Tourism_Project", "visit_mode_model.pkl"), "rb"))
    le_continent = pickle.load(open(os.path.join(base_dir, "..", "Tourism_Project", "le_continent.pkl"), "rb"))
    le_region = pickle.load(open(os.path.join(base_dir, "..", "Tourism_Project", "le_region.pkl"), "rb"))
    le_attraction = pickle.load(open(os.path.join(base_dir, "..", "Tourism_Project", "le_attraction.pkl"), "rb"))
    le_visitmode = pickle.load(open(os.path.join(base_dir, "..", "Tourism_Project", "le_visitmode.pkl"), "rb"))

    col1, col2 = st.columns(2)
    with col1:
        continent = st.selectbox("Continent", sorted(df["Continent"].unique()))
    with col2:
        region = st.selectbox("Region", sorted(df[df["Continent"] == continent]["Region"].unique()))
    
    col3, col4 = st.columns(2)
    with col3:
        attraction = st.selectbox("Attraction Type", sorted(df["AttractionType"].unique()))
    with col4:
        rating = st.slider("Expected Rating", 1.0, 5.0, 3.0)

    if st.button("Predict Visit Mode"):
        try:
            c = le_continent.transform([continent])[0]
            r = le_region.transform([region])[0]
            a = le_attraction.transform([attraction])[0]
            
            pred = model.predict([[c, r, a, rating]])
            visit_mode = le_visitmode.inverse_transform(pred)
            
            st.success(f"Predicted Visit Mode: **{visit_mode[0]}** ⭐")
        except Exception as e:
            st.error(f"Error: {str(e)}")
