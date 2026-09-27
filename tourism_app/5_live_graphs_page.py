import streamlit as st
import pandas as pd
import plotly.express as px

def graph_page(df):
    st.header("📊 Live Tourism Analytics")
    
    # Ensure we have the required columns
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    col1, col2 = st.columns(2)

    # Bar chart - User Distribution by Continent
    fig1 = px.bar(
        df,
        x="Continent",
        title="User Distribution by Continent",
        color="Continent",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1.update_layout(height=400)

    # Pie chart - Visit Mode Distribution
    fig2 = px.pie(
        df,
        names="VisitMode",
        title="Visit Mode Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig2.update_layout(height=400)

    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)

    # Scatter plot - Rating by Region and Visit Mode
    fig3 = px.scatter(
        df,
        x="Region",
        y="Rating",
        color="VisitMode",
        title="Rating vs Region by Visit Mode",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig3.update_layout(height=500)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Additional chart - Average Rating by Attraction Type
    st.subheader("⭐ Average Rating by Attraction Type")
    fig4 = px.bar(
        df.groupby("AttractionType")["Rating"].mean().reset_index(),
        x="AttractionType",
        y="Rating",
        title="Average Rating by Attraction Type",
        color="AttractionType",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)
