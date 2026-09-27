"""Premium UI theme — glassmorphism, animations, and layout helpers."""
import streamlit as st

THEMES = {
    "dark": {
        "bg1": "#030712",
        "bg2": "#0c1929",
        "bg3": "#1a0a2e",
        "card": "rgba(15, 23, 42, 0.72)",
        "card_border": "rgba(56, 189, 248, 0.35)",
        "text": "#f1f5f9",
        "muted": "#94a3b8",
        "accent": "#22d3ee",
        "accent2": "#a78bfa",
        "accent3": "#f472b6",
        "sidebar": "rgba(8, 15, 35, 0.95)",
        "input_bg": "rgba(30, 41, 59, 0.6)",
        "glow": "rgba(34, 211, 238, 0.25)",
    },
    "light": {
        "bg1": "#f0f9ff",
        "bg2": "#e0f2fe",
        "bg3": "#fdf4ff",
        "card": "rgba(255, 255, 255, 0.88)",
        "card_border": "rgba(14, 165, 233, 0.35)",
        "text": "#0f172a",
        "muted": "#64748b",
        "accent": "#0284c7",
        "accent2": "#7c3aed",
        "accent3": "#db2777",
        "sidebar": "rgba(255, 255, 255, 0.95)",
        "input_bg": "rgba(241, 245, 249, 0.9)",
        "glow": "rgba(2, 132, 199, 0.15)",
    },
}


def inject_theme(theme: str = "dark") -> None:
    t = THEMES.get(theme, THEMES["dark"])
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,500;0,9..40,700&family=Playfair+Display:wght@600;700&display=swap');

        /* ── App shell ── */
        .stApp {{
            background: linear-gradient(145deg, {t["bg1"]} 0%, {t["bg2"]} 40%, {t["bg3"]} 100%) !important;
            color: {t["text"]};
            font-family: 'DM Sans', system-ui, sans-serif !important;
        }}

        /* Animated mesh overlay */
        .stApp::before {{
            content: '';
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse 80% 50% at 20% 20%, {t["glow"]} 0%, transparent 50%),
                radial-gradient(ellipse 60% 40% at 80% 80%, rgba(167, 139, 250, 0.12) 0%, transparent 50%),
                radial-gradient(ellipse 50% 30% at 50% 50%, rgba(244, 114, 182, 0.06) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }}

        .block-container {{
            padding-top: 1.5rem !important;
            max-width: 1400px;
        }}

        #MainMenu, footer, header[data-testid="stHeader"] {{
            visibility: hidden;
        }}

        h1, h2, h3, .page-title {{
            font-family: 'Playfair Display', Georgia, serif !important;
            color: {t["text"]} !important;
        }}

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {t["sidebar"]} 0%, {t["bg1"]} 100%) !important;
            border-right: 1px solid {t["card_border"]};
            box-shadow: 4px 0 24px rgba(0,0,0,0.15);
        }}

        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {{
            font-family: 'DM Sans', sans-serif !important;
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: {t["accent"]} !important;
        }}

        /* ── Inputs ── */
        .stTextInput input, .stNumberInput input,
        [data-baseweb="select"] > div,
        .stMultiSelect [data-baseweb="tag"] {{
            border-radius: 12px !important;
            border: 1px solid {t["card_border"]} !important;
            background: {t["input_bg"]} !important;
            color: {t["text"]} !important;
            transition: box-shadow 0.2s, border-color 0.2s;
        }}

        .stTextInput input:focus, .stNumberInput input:focus {{
            box-shadow: 0 0 0 3px {t["glow"]} !important;
            border-color: {t["accent"]} !important;
        }}

        /* ── Buttons ── */
        .stButton > button {{
            border-radius: 12px !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: 1px solid {t["card_border"]} !important;
        }}

        .stButton > button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"] {{
            background: linear-gradient(135deg, {t["accent"]}, {t["accent2"]}) !important;
            color: #fff !important;
            border: none !important;
            box-shadow: 0 4px 20px {t["glow"]};
        }}

        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 28px {t["glow"]} !important;
        }}

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: transparent;
            border-bottom: 1px solid {t["card_border"]};
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 10px 10px 0 0;
            padding: 10px 20px;
            font-weight: 600;
            color: {t["muted"]};
        }}

        .stTabs [aria-selected="true"] {{
            background: {t["card"]} !important;
            color: {t["accent"]} !important;
            border: 1px solid {t["card_border"]};
            border-bottom: none;
        }}

        /* ── Metrics (native) ── */
        [data-testid="stMetric"] {{
            background: {t["card"]};
            backdrop-filter: blur(16px);
            border: 1px solid {t["card_border"]};
            border-radius: 16px;
            padding: 1rem 1.25rem !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.12);
            transition: transform 0.25s ease;
        }}

        [data-testid="stMetric"]:hover {{
            transform: translateY(-3px);
        }}

        [data-testid="stMetricValue"] {{
            font-size: 1.75rem !important;
            font-weight: 700 !important;
            background: linear-gradient(90deg, {t["accent"]}, {t["accent2"]});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        /* ── Dataframes ── */
        [data-testid="stDataFrame"] {{
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid {t["card_border"]};
        }}

        /* ── Alerts ── */
        .stSuccess, .stInfo, .stWarning, .stError {{
            border-radius: 12px !important;
            border-left-width: 4px !important;
        }}

        /* ── Plotly charts ── */
        [data-testid="stPlotlyChart"] {{
            background: {t["card"]};
            backdrop-filter: blur(12px);
            border: 1px solid {t["card_border"]};
            border-radius: 20px;
            padding: 0.5rem;
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
            min-height: 620px;
        }}

        [data-testid="stPlotlyChart"] iframe {{
            min-height: 600px !important;
        }}

        /* Streamlit built-in map */
        [data-testid="stDeckGlJsonChart"] {{
            min-height: 450px;
            border-radius: 16px;
            border: 1px solid {t["card_border"]};
        }}

        /* Folium / Leaflet map */
        iframe[title="streamlit_folium.st_folium"],
        .folium-map {{
            min-height: 620px !important;
            border-radius: 16px;
            border: 1px solid {t["card_border"]};
        }}

        /* ── Custom components ── */
        .hero-wrap {{
            position: relative;
            text-align: center;
            padding: 2.5rem 1rem 2rem;
            margin-bottom: 1rem;
        }}

        .hero-badge {{
            display: inline-block;
            padding: 0.35rem 1rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            background: linear-gradient(135deg, rgba(34,211,238,0.2), rgba(167,139,250,0.2));
            border: 1px solid {t["card_border"]};
            color: {t["accent"]};
            margin-bottom: 1rem;
            animation: pulse-badge 2.5s ease-in-out infinite;
        }}

        @keyframes pulse-badge {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.85; transform: scale(1.02); }}
        }}

        .hero-title {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: clamp(2rem, 5vw, 3.2rem);
            font-weight: 700;
            line-height: 1.15;
            margin: 0 0 0.75rem;
            background: linear-gradient(120deg, {t["accent"]}, {t["accent2"]}, {t["accent3"]});
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient-shift 5s ease infinite;
        }}

        @keyframes gradient-shift {{
            0%, 100% {{ background-position: 0% center; }}
            50% {{ background-position: 100% center; }}
        }}

        .hero-sub {{
            color: {t["muted"]};
            font-size: 1.1rem;
            max-width: 560px;
            margin: 0 auto 1.5rem;
            line-height: 1.6;
        }}

        .glass-card, .metric-card, .feature-card, .login-panel, .chart-panel {{
            background: {t["card"]};
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid {t["card_border"]};
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.05);
            transition: transform 0.35s cubic-bezier(0.4,0,0.2,1),
                        box-shadow 0.35s ease, border-color 0.35s ease;
        }}

        .glass-card:hover, .feature-card:hover, .metric-card:hover {{
            transform: translateY(-6px);
            box-shadow: 0 20px 50px {t["glow"]};
            border-color: {t["accent"]};
        }}

        .feature-card {{
            text-align: center;
            min-height: 140px;
            animation: fade-up 0.6s ease backwards;
        }}

        .feature-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .feature-card:nth-child(2) {{ animation-delay: 0.2s; }}
        .feature-card:nth-child(3) {{ animation-delay: 0.3s; }}

        @keyframes fade-up {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .feature-icon {{
            font-size: 2.5rem;
            margin-bottom: 0.75rem;
            filter: drop-shadow(0 4px 12px {t["glow"]});
        }}

        .metric-card .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(90deg, {t["accent"]}, {t["accent2"]});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .metric-card .metric-label {{
            font-size: 0.8rem;
            color: {t["muted"]};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.25rem;
        }}

        .page-header {{
            margin-bottom: 1.75rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid {t["card_border"]};
        }}

        .page-header h1 {{
            margin: 0 !important;
            font-size: 2rem !important;
        }}

        .page-header .subtitle {{
            color: {t["muted"]};
            margin-top: 0.35rem;
            font-size: 1rem;
        }}

        .sidebar-brand {{
            text-align: center;
            padding: 1rem 0 0.5rem;
        }}

        .sidebar-brand .logo {{
            font-size: 2.5rem;
            line-height: 1;
            filter: drop-shadow(0 0 20px {t["glow"]});
        }}

        .sidebar-brand .name {{
            font-family: 'Playfair Display', serif;
            font-size: 1rem;
            font-weight: 700;
            color: {t["text"]};
            margin-top: 0.5rem;
        }}

        .sidebar-brand .user-pill {{
            display: inline-block;
            margin-top: 0.5rem;
            padding: 0.25rem 0.85rem;
            border-radius: 999px;
            font-size: 0.8rem;
            background: {t["input_bg"]};
            border: 1px solid {t["card_border"]};
            color: {t["accent"]};
        }}

        .section-label {{
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: {t["accent"]};
            margin: 1rem 0 0.5rem;
        }}

        .chart-panel-title {{
            font-size: 1rem;
            font-weight: 600;
            color: {t["text"]};
            margin-bottom: 0.5rem;
            padding-left: 0.75rem;
            border-left: 3px solid {t["accent2"]};
        }}

        .footer-bar {{
            text-align: center;
            padding: 1.5rem;
            color: {t["muted"]};
            font-size: 0.8rem;
            border-top: 1px solid {t["card_border"]};
            margin-top: 2rem;
        }}

        .stat-float {{
            position: absolute;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.4;
            pointer-events: none;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero_section(title: str, subtitle: str, badge: str = "AI Tourism Platform") -> None:
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">{badge}</div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-sub">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(icon: str, title: str, subtitle: str = "") -> None:
    sub_html = f'<p class="subtitle">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f"""
        <div class="page-header">
            <h1>{icon} {title}</h1>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand(username: str) -> None:
    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand">
            <div class="logo">🌍</div>
            <div class="name">Tourism Analytics</div>
            <div class="user-pill">👤 {username}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_section(label: str) -> None:
    st.sidebar.markdown(f'<p class="section-label">{label}</p>', unsafe_allow_html=True)


def metric_card(label: str, value: str, icon: str = "📊", color: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div style="font-size:1.75rem;margin-bottom:0.25rem">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(icon: str, title: str, desc: str) -> None:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div style="font-weight:700;font-size:1.05rem;margin-bottom:0.35rem">{title}</div>
            <div style="color:#94a3b8;font-size:0.85rem">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def glass_panel_start(title: str = "") -> None:
    title_html = f'<div class="chart-panel-title">{title}</div>' if title else ""
    st.markdown(f'<div class="glass-card login-panel">{title_html}', unsafe_allow_html=True)


def glass_panel_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def section_header(title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="chart-panel-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)


def footer() -> None:
    st.markdown(
        """
        <div class="footer-bar">
            ✦ Tourism Analytics & Recommendation System ✦<br>
            <small>Streamlit · Plotly · Machine Learning · Final Year Project</small>
        </div>
        """,
        unsafe_allow_html=True,
    )
