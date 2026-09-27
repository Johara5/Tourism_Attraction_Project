"""
Tourism Analytics & Recommendation System
Premium Streamlit dashboard with modern UI.
"""
import os
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth import load_users, register_user, update_user_profile, verify_login
from charts import build_chart, model_comparison_bar
from config import APP_TITLE, CHART_OPTIONS, PAGE_ICON
from data_loader import filter_data, load_data
from maps import build_leaflet_map, get_map_points_for_streamlit

try:
    from streamlit_folium import st_folium
    HAS_FOLIUM = True
except ImportError:
    HAS_FOLIUM = False
from ml_models import (
    build_feature_row,
    get_or_train_models,
    predict_rating,
    predict_visit_mode,
)
from recommendations import collaborative_recommendations, content_based_recommendations
from styles import (
    feature_card,
    footer,
    hero_section,
    inject_theme,
    metric_card,
    page_header,
    section_header,
    sidebar_brand,
    sidebar_section,
)

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

for key, default in [
    ("logged_in", False),
    ("username", ""),
    ("theme", "dark"),
    ("prediction_history", []),
    ("rating_history", []),
    ("ml_metrics", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


@st.cache_data(show_spinner=False)
def get_data() -> pd.DataFrame:
    return load_data()


@st.cache_resource(show_spinner=False)
def get_ml_bundle(_df_hash: str, df: pd.DataFrame):
    return get_or_train_models(df)


def render_welcome() -> None:
    inject_theme("dark")
    hero_section(
        APP_TITLE,
        "Discover global travel patterns with AI-powered analytics, "
        "interactive visualizations, and smart recommendations.",
        "✦ Premium Analytics Dashboard ✦",
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        feature_card("📊", "15+ Live Charts", "Animated Plotly visualizations")
    with c2:
        feature_card("🤖", "ML Engine", "Rating & visit mode predictions")
    with c3:
        feature_card("🗺️", "Global Map", "Interactive geo tourism insights")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    col_login, col_reg = st.columns(2)

    with col_login:
        st.markdown('<div class="glass-card login-panel">', unsafe_allow_html=True)
        st.markdown("### 🔑 Welcome Back")
        st.caption("Sign in to access your analytics dashboard")
        username = st.text_input("Username", key="login_user", placeholder="e.g. Johara or admin")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
        if st.button("🚀 Launch Dashboard", type="primary", use_container_width=True):
            if not username or not password:
                st.warning("Please enter both username and password.")
            else:
                ok, canonical_user, err = verify_login(username, password)
                if ok:
                    st.session_state.logged_in = True
                    st.session_state.username = canonical_user
                    st.balloons()
                    st.rerun()
                else:
                    st.error(err)
        if st.button("🔓 Quick Demo Login (admin / admin123)", use_container_width=True):
            ok, canonical_user, _ = verify_login("admin", "admin123")
            if ok:
                st.session_state.logged_in = True
                st.session_state.username = canonical_user
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_reg:
        st.markdown('<div class="glass-card login-panel">', unsafe_allow_html=True)
        st.markdown("### 📝 Create Account")
        st.caption("Join to unlock the full tourism platform")
        new_user = st.text_input("Username", key="reg_user", placeholder="Choose username")
        new_pass = st.text_input("Password", type="password", key="reg_pass", placeholder="Min. 4 characters")
        confirm = st.text_input("Confirm", type="password", key="reg_confirm", placeholder="Repeat password")
        email = st.text_input("Email", key="reg_email", placeholder="you@email.com (optional)")
        full_name = st.text_input("Full Name", key="reg_name", placeholder="Your name (optional)")
        if st.button("✨ Register & Continue", use_container_width=True):
            if not new_user or not new_pass:
                st.warning("Username and password are required.")
            elif new_pass != confirm:
                st.error("Passwords do not match.")
            elif len(new_pass) < 4:
                st.error("Password must be at least 4 characters.")
            else:
                ok, msg = register_user(new_user, new_pass, email, full_name)
                if ok:
                    st.success(msg)
                    # Auto sign-in after registration
                    login_ok, canonical, _ = verify_login(new_user, new_pass)
                    if login_ok:
                        st.session_state.logged_in = True
                        st.session_state.username = canonical
                        st.rerun()
                else:
                    st.error(msg)
        st.markdown("</div>", unsafe_allow_html=True)

    users = load_users()
    if users:
        with st.expander("ℹ️ Already registered? Use one of these usernames to log in"):
            for name in users:
                st.markdown(f"- **{name}**")
    else:
        st.info("💡 **First time?** Create an account on the right, or use **Quick Demo Login**.")


def render_sidebar(df: pd.DataFrame) -> dict:
    theme = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.theme == "dark")
    st.session_state.theme = "dark" if theme else "light"
    inject_theme(st.session_state.theme)

    sidebar_brand(st.session_state.username)
    st.sidebar.markdown("---")

    sidebar_section("Filters")
    all_continents = sorted(df["Continent"].unique())
    selected_continents = st.sidebar.multiselect(
        "🌐 Continent(s)",
        options=all_continents,
        default=all_continents,
        key="sidebar_continents",
    )
    all_modes = sorted(df["VisitMode"].unique())
    selected_modes = st.sidebar.multiselect(
        "✈️ Visit Mode(s)",
        options=all_modes,
        default=all_modes,
        key="sidebar_modes",
    )
    rating_range = st.sidebar.slider("⭐ Rating Range", 1, 5, (1, 5))

    st.sidebar.markdown("---")
    sidebar_section("Navigate")
    nav = st.sidebar.radio(
        "Menu",
        [
            "🏠 Overview",
            "📋 User History",
            "📈 Live Graphs",
            "🤖 ML & Predictions",
            "⭐ Recommendations",
            "🗺️ Tourism Map",
            "⚙️ Settings",
        ],
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True, type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.prediction_history = []
        st.session_state.rating_history = []
        st.rerun()

    filtered = filter_data(df, selected_continents, selected_modes, rating_range)
    st.sidebar.caption(f"📊 **{len(filtered):,}** records loaded")
    return {"nav": nav, "filtered": filtered}


def page_overview(df: pd.DataFrame) -> None:
    page_header(
        "🏠",
        "Dashboard Overview",
        f"Welcome back, {st.session_state.username} — real-time global tourism intelligence.",
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Total Records", f"{len(df):,}", "📁")
    with c2:
        metric_card("Continents", str(df["Continent"].nunique()), "🌐")
    with c3:
        metric_card("Attractions", str(df["Attraction"].nunique()), "🏛️")
    with c4:
        metric_card("Avg Rating", f"{df['Rating'].mean():.2f} ★", "⭐")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        section_header("Visit Mode Distribution")
        st.plotly_chart(build_chart("visit_mode_pie", df), use_container_width=True)
    with col_b:
        section_header("Top Countries")
        st.plotly_chart(build_chart("top_countries", df), use_container_width=True)

    section_header("Tourism Growth Trend")
    st.plotly_chart(build_chart("growth_area", df), use_container_width=True)


def page_user_history(df: pd.DataFrame) -> None:
    page_header("📋", "User History", "Browse filtered transactions and top-rated destinations.")
    section_header("Transaction Records")
    st.dataframe(df.head(500), use_container_width=True, height=380)
    st.caption(f"Displaying 500 of **{len(df):,}** records")

    c1, c2, c3 = st.columns(3)
    c1.metric("👥 Unique Users", f"{df['UserId'].nunique():,}")
    c2.metric("📍 Regions", df["Region"].nunique())
    c3.metric("🌎 Countries", df["Country"].nunique())

    st.markdown("---")
    section_header("🏆 Top Rated Attractions")
    top = (
        df.groupby(["Attraction", "Continent", "Country"])
        .agg(AvgRating=("Rating", "mean"), Reviews=("Rating", "count"))
        .reset_index()
        .sort_values("AvgRating", ascending=False)
        .head(15)
    )
    st.dataframe(top, use_container_width=True)


def page_live_graphs(df: pd.DataFrame) -> None:
    page_header("📈", "Live Graphs", "Explore 15 interactive visualizations — pick any chart below.")
    choice = st.selectbox("🎨 Select Visualization", list(CHART_OPTIONS.keys()))
    if df.empty:
        st.warning("No data available for current filters.")
        return
    section_header(choice)
    st.plotly_chart(build_chart(CHART_OPTIONS[choice], df), use_container_width=True)


def page_ml(df: pd.DataFrame, bundle) -> None:
    page_header("🤖", "Machine Learning", "Predict ratings, classify visit modes, and compare model performance.")

    if st.session_state.ml_metrics is None:
        st.session_state.ml_metrics = {
            "regression": getattr(bundle, "regression_metrics", {}),
            "classification": getattr(bundle, "classification_metrics", {}),
        }

    tab_eval, tab_rating, tab_visit = st.tabs(
        ["📊 Evaluation", "⭐ Rating Prediction", "🎯 Visit Mode"]
    )

    with tab_eval:
        reg_metrics = st.session_state.ml_metrics.get("regression", {})
        if reg_metrics:
            section_header("Regression Models")
            r2_vals = {k: v["R² Score"] for k, v in reg_metrics.items()}
            mse_vals = {k: v["Mean Squared Error"] for k, v in reg_metrics.items()}
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(
                    model_comparison_bar(r2_vals, "R² Score", "Regression — R² Score"),
                    use_container_width=True,
                )
            with c2:
                st.plotly_chart(
                    model_comparison_bar(mse_vals, "MSE", "Regression — Mean Squared Error"),
                    use_container_width=True,
                )
            st.dataframe(pd.DataFrame(reg_metrics).T, use_container_width=True)

        cls_metrics = st.session_state.ml_metrics.get("classification", {})
        if cls_metrics:
            section_header("Classification Models")
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(
                    model_comparison_bar(
                        {k: v["Accuracy"] for k, v in cls_metrics.items()},
                        "Accuracy",
                        "Classification — Accuracy",
                    ),
                    use_container_width=True,
                )
            with c2:
                st.plotly_chart(
                    model_comparison_bar(
                        {k: v["F1 Score"] for k, v in cls_metrics.items()},
                        "F1",
                        "Classification — F1 Score",
                    ),
                    use_container_width=True,
                )
            st.dataframe(pd.DataFrame(cls_metrics).T, use_container_width=True)

        if st.button("🔄 Retrain All Models", type="primary"):
            from ml_models import train_all_models

            with st.spinner("Training models — please wait…"):
                bundle = train_all_models(df)
                st.session_state.ml_metrics = {
                    "regression": bundle.regression_metrics,
                    "classification": bundle.classification_metrics,
                }
                get_ml_bundle.clear()
            st.success("✅ Models saved successfully!")
            st.rerun()

    with tab_rating:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_header("Predict User Rating")
        c1, c2, c3 = st.columns(3)
        continent = c1.selectbox("Continent", sorted(df["Continent"].unique()), key="pred_r_cont")
        region_opts_r = sorted(df[df["Continent"] == continent]["Region"].unique())
        region = c2.selectbox("Region", region_opts_r, key="pred_r_reg")
        subset_r = df[(df["Continent"] == continent) & (df["Region"] == region)]
        type_opts = sorted(subset_r["AttractionType"].unique()) if not subset_r.empty else sorted(df["AttractionType"].unique())
        attr_type = c3.selectbox("Attraction Type", type_opts, key="pred_r_type")
        c4, c5, c6 = st.columns(3)
        visit_mode = c4.selectbox("Visit Mode", sorted(df["VisitMode"].unique()), key="pred_r_vm")
        visit_time = c5.slider("Visit Time (hrs)", 1, 10, 3)
        reg_model = c6.selectbox("Model", list(bundle.regression.keys()))
        year = st.slider("Year", int(df["Year"].min()), int(df["Year"].max()), 2022)
        month = st.slider("Month", 1, 12, 6)
        if st.button("🔮 Predict Rating", type="primary"):
            try:
                features = build_feature_row(
                    continent, region, attr_type, visit_mode, visit_time, year, month, bundle.encoders
                )
                pred = predict_rating(reg_model, features, bundle)
                st.session_state.rating_history.append({
                    "Model": reg_model, "Continent": continent, "Region": region, "Rating": round(pred, 2),
                })
                st.success(f"**Predicted Rating: {pred:.2f} / 5** ⭐")
            except Exception as exc:
                st.error(f"Could not predict: {exc}")
        if st.session_state.rating_history:
            st.dataframe(pd.DataFrame(st.session_state.rating_history), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_visit:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_header("Classify Visit Mode")
        c1, c2, c3 = st.columns(3)
        continent = c1.selectbox("Continent", sorted(df["Continent"].unique()), key="pred_c_cont")
        region_opts = sorted(df[df["Continent"] == continent]["Region"].unique())
        if not region_opts:
            st.warning("No regions available for this continent with current filters.")
            region_opts = sorted(df["Region"].unique())
        region = c2.selectbox("Region", region_opts, key="pred_c_reg")
        subset = df[(df["Continent"] == continent) & (df["Region"] == region)]
        attr_types = sorted(subset["AttractionType"].unique()) if not subset.empty else []
        attr_type = c3.selectbox(
            "Attraction Type",
            attr_types if attr_types else sorted(df["AttractionType"].unique()),
            key="pred_c_type",
        )
        c4, c5, c6 = st.columns(3)
        visit_time = c4.slider("Visit Time (hrs)", 1, 10, 3, key="pred_c_time")
        year = c5.slider("Year", int(df["Year"].min()), int(df["Year"].max()), 2022, key="pred_c_year")
        month = c6.slider("Month", 1, 12, 6, key="pred_c_month")
        c7, c8 = st.columns(2)
        rating = c7.slider("Expected Rating", 1.0, 5.0, 3.5, key="pred_c_rating")
        cls_model = c8.selectbox("Classifier", list(bundle.classification.keys()))
        if st.button("🎯 Predict Visit Mode", type="primary"):
            if subset.empty:
                st.error("No data for this continent and region. Change filters or sidebar selection.")
            else:
                try:
                    # VisitMode column is dropped before prediction; placeholder satisfies encoder
                    placeholder_mode = bundle.encoders["VisitMode"].classes_[0]
                    features = build_feature_row(
                        continent, region, attr_type, placeholder_mode,
                        visit_time, year, month, bundle.encoders,
                    )
                    pred = predict_visit_mode(cls_model, features, bundle)
                    st.session_state.prediction_history.append({
                        "Model": cls_model,
                        "Continent": continent,
                        "Region": region,
                        "Attraction Type": attr_type,
                        "Rating": rating,
                        "Predicted Visit Mode": pred,
                    })
                    st.success(f"**Predicted Visit Mode: {pred}**")
                except Exception as exc:
                    st.error(f"Could not predict: {exc}. Try a different region or attraction type.")
        if st.session_state.prediction_history:
            st.dataframe(pd.DataFrame(st.session_state.prediction_history), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def page_recommendations(df: pd.DataFrame) -> None:
    page_header("⭐", "Recommendations", "Personalized attractions via collaborative & content-based AI.")
    tab_col, tab_content = st.tabs(["🤝 Collaborative", "📚 Content-Based"])

    with tab_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        user_id = st.number_input(
            "User ID",
            min_value=int(df["UserId"].min()),
            max_value=int(df["UserId"].max()),
            value=int(df["UserId"].iloc[0]),
        )
        top_n = st.slider("Recommendations", 3, 15, 8)
        if st.button("✨ Get Recommendations", type="primary"):
            with st.spinner("Finding similar travelers…"):
                recs = collaborative_recommendations(df, int(user_id), top_n)
            st.dataframe(recs, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_content:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        continent = c1.selectbox("Continent", sorted(df["Continent"].unique()))
        attr_type = c2.selectbox("Attraction Type", sorted(df["AttractionType"].unique()))
        visit_mode = c3.selectbox("Visit Mode", sorted(df["VisitMode"].unique()))
        if st.button("✨ Get Recommendations", type="primary", key="content_rec"):
            with st.spinner("Matching your preferences…"):
                recs = content_based_recommendations(df, continent, attr_type, visit_mode)
            st.dataframe(recs, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def page_map(df: pd.DataFrame) -> None:
    page_header("🗺️", "Tourism Map", "Explore destinations worldwide — hover markers for details.")

    if df.empty:
        st.warning("No data for current sidebar filters. Reset continent / visit mode filters in the sidebar.")
        return

    continent = st.selectbox(
        "Filter by Continent",
        ["All"] + sorted(df["Continent"].unique()),
        key="map_continent",
    )
    continent_filter = continent if continent != "All" else None

    map_points = get_map_points_for_streamlit(df, continent_filter)
    if map_points.empty:
        st.warning("No locations found for this continent. Try **All** or adjust sidebar filters.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("📍 Locations", len(map_points))
    c2.metric("🌎 Countries", map_points["Country"].nunique())
    c3.metric("⭐ Avg Rating", f"{map_points['Rating'].mean():.2f}")

    st.caption("🗺️ **Leaflet interactive map** — zoom, pan, click markers for details. Switch tile style in the layer control (top-right).")

    if not HAS_FOLIUM:
        st.error("Leaflet map requires: `pip install folium streamlit-folium`")
        st.map(map_points[["lat", "lon"]], latitude="lat", longitude="lon", size=80)
    else:
        leaflet_map = build_leaflet_map(df, continent_filter)
        if leaflet_map is None:
            st.warning("Could not build map for this selection.")
        else:
            st_folium(
                leaflet_map,
                width=None,
                height=620,
                returned_objects=[],
            )

    with st.expander("📋 All locations in this view"):
        st.dataframe(
            map_points[
                ["Attraction", "Country", "Region", "Continent", "VisitMode", "Rating", "Visits"]
            ].sort_values("Visits", ascending=False),
            use_container_width=True,
            height=320,
        )


def page_settings() -> None:
    page_header("⚙️", "Settings", "Manage your profile and account security.")
    user = st.session_state.username
    info = load_users().get(user, {})

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 👤 Profile")
        with st.form("profile"):
            email = st.text_input("Email", value=info.get("email", ""))
            full_name = st.text_input("Full Name", value=info.get("full_name", ""))
            if st.form_submit_button("💾 Save Profile", use_container_width=True):
                update_user_profile(user, email=email, full_name=full_name)
                st.success("Profile updated!")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Password")
        with st.form("password"):
            current = st.text_input("Current Password", type="password")
            new_pw = st.text_input("New Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            if st.form_submit_button("🔄 Update Password", use_container_width=True):
                if new_pw != confirm:
                    st.error("Passwords do not match.")
                else:
                    ok, _, err = verify_login(user, current)
                    if not ok:
                        st.error(err or "Current password is incorrect.")
                    else:
                        update_user_profile(user, new_password=new_pw)
                        st.success("Password updated!")
        st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    if not st.session_state.logged_in:
        render_welcome()
        footer()
        return

    df = get_data()
    ctx = render_sidebar(df)
    filtered = ctx["filtered"]
    nav = ctx["nav"]

    bundle = get_ml_bundle(str(df.shape), df)
    if st.session_state.ml_metrics is None and bundle.regression_metrics:
        st.session_state.ml_metrics = {
            "regression": bundle.regression_metrics,
            "classification": bundle.classification_metrics,
        }

    pages = {
        "🏠 Overview": lambda: page_overview(filtered),
        "📋 User History": lambda: page_user_history(filtered),
        "📈 Live Graphs": lambda: page_live_graphs(filtered),
        "🤖 ML & Predictions": lambda: page_ml(filtered, bundle),
        "⭐ Recommendations": lambda: page_recommendations(filtered),
        "🗺️ Tourism Map": lambda: page_map(filtered),
        "⚙️ Settings": page_settings,
    }
    pages[nav]()
    footer()


if __name__ == "__main__":
    main()
