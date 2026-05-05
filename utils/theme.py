"""
Thème visuel DATAFIX
====================
CSS injecté dans toutes les pages pour rester cohérent avec la maquette
Figma : fond noir cinéma, accents jaune doré, typographie épurée.
"""
from __future__ import annotations

import streamlit as st


# Palette DATAFIX (à utiliser aussi dans Plotly / matplotlib)
COLORS = {
    "bg":          "#0E0E10",
    "bg_alt":      "#1A1A1D",
    "bg_card":     "#16161A",
    "primary":     "#F5C518",   # jaune signature
    "primary_2":   "#FFD24A",
    "text":        "#F5F5F5",
    "muted":       "#9A9AA0",
    "border":      "#2A2A30",
}


def inject_global_css() -> None:
    """Injecte le CSS global cohérent avec le logo DATAFIX."""
    st.markdown(
        f"""
        <style>
        /* ---------- Fond global ---------- */
        .stApp {{
            background:
              radial-gradient(1200px 600px at 80% -10%, rgba(245,197,24,0.08), transparent 60%),
              radial-gradient(900px 500px at 0% 100%, rgba(245,197,24,0.05), transparent 60%),
              {COLORS["bg"]};
            color: {COLORS["text"]};
        }}

        /* ---------- Sidebar ---------- */
        [data-testid="stSidebar"] {{
            background-color: #0A0A0C !important;
            border-right: 1px solid {COLORS["border"]};
        }}
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stCaption {{
            color: {COLORS["text"]};
        }}

        /* ---------- Boutons ---------- */
        .stButton > button {{
            background: linear-gradient(135deg, {COLORS["primary"]} 0%, {COLORS["primary_2"]} 100%);
            color: #111;
            font-weight: 700;
            border: none;
            border-radius: 12px;
            padding: 0.65rem 1.2rem;
            transition: transform .12s ease, box-shadow .12s ease;
            box-shadow: 0 4px 14px rgba(245,197,24,0.25);
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(245,197,24,0.4);
            color: #000;
        }}

        /* ---------- Inputs ---------- */
        .stTextInput input,
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {{
            background-color: {COLORS["bg_alt"]} !important;
            color: {COLORS["text"]} !important;
            border-radius: 10px !important;
            border: 1px solid {COLORS["border"]} !important;
        }}

        /* ---------- Metric ---------- */
        [data-testid="stMetric"] {{
            background: {COLORS["bg_card"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 14px;
            padding: 1rem 1.2rem;
        }}
        [data-testid="stMetricValue"] {{
            color: {COLORS["primary"]} !important;
            font-weight: 800;
        }}
        [data-testid="stMetricLabel"] {{
            color: {COLORS["muted"]} !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-size: 0.78rem !important;
        }}

        /* ---------- HERO ---------- */
        .datafix-hero {{
            text-align: center;
            padding: 2.4rem 1rem 1.4rem;
        }}
        .datafix-hero h1 {{
            font-size: clamp(2.6rem, 6vw, 4.8rem);
            font-weight: 900;
            margin: 0;
            letter-spacing: 0.02em;
            background: linear-gradient(90deg, #FFFFFF 0%, #FFFFFF 55%, {COLORS["primary"]} 56%, {COLORS["primary"]} 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }}
        .datafix-hero .subtitle {{
            font-size: 1.15rem;
            color: {COLORS["muted"]};
            margin-top: 0.6rem;
        }}
        .datafix-hero .accent-bar {{
            width: 84px;
            height: 4px;
            background: {COLORS["primary"]};
            border-radius: 4px;
            margin: 1rem auto 0;
        }}

        .datafix-tagline {{
            background: {COLORS["bg_card"]};
            border: 1px solid {COLORS["border"]};
            border-left: 4px solid {COLORS["primary"]};
            padding: 1rem 1.2rem;
            border-radius: 12px;
            color: {COLORS["text"]};
            font-size: 1rem;
            line-height: 1.6;
        }}

        /* ---------- Cartes "feature" ---------- */
        .datafix-card {{
            background: {COLORS["bg_card"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 16px;
            padding: 1.4rem 1.2rem;
            height: 100%;
            transition: transform .15s ease, border-color .15s ease;
        }}
        .datafix-card:hover {{
            transform: translateY(-3px);
            border-color: {COLORS["primary"]};
        }}
        .datafix-card-icon {{
            font-size: 2rem;
            margin-bottom: 0.4rem;
        }}
        .datafix-card-title {{
            font-size: 1.15rem;
            font-weight: 800;
            color: {COLORS["primary"]};
            margin-bottom: 0.5rem;
        }}
        .datafix-card-text {{
            color: {COLORS["text"]};
            opacity: 0.85;
            font-size: 0.95rem;
            line-height: 1.55;
        }}


        /* ---------- Cartes numérotées style éditorial ---------- */
        .datafix-card-clean {{
            background: linear-gradient(180deg, #16161A 0%, #101013 100%);
            border: 1px solid #2A2A30;
            border-radius: 16px;
            padding: 1.6rem 1.4rem 1.5rem;
            height: 100%;
            position: relative;
            overflow: hidden;
            transition: transform .15s ease, border-color .15s ease;
        }}
        .datafix-card-clean::before {{
            content: "";
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 3px;
            background: #F5C518;
            opacity: 0.85;
        }}
        .datafix-card-clean:hover {{
            transform: translateY(-3px);
            border-color: #F5C518;
        }}
        .datafix-card-clean .num {{
            display: inline-block;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            color: #F5C518;
            letter-spacing: 0.15em;
            font-weight: 700;
            margin-bottom: 0.6rem;
        }}
        .datafix-card-clean .title {{
            font-size: 1.25rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 0.8rem;
            line-height: 1.3;
        }}
        .datafix-card-clean .text {{
            color: #C4C4CC;
            font-size: 0.95rem;
            line-height: 1.55;
        }}

        /* ---------- Carte film (résultats reco) ---------- */
        .movie-card {{
            background: {COLORS["bg_card"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 14px;
            padding: 0.6rem;
            text-align: center;
            transition: transform .15s ease, border-color .15s ease;
        }}
        .movie-card:hover {{
            transform: translateY(-3px);
            border-color: {COLORS["primary"]};
        }}
        .movie-card .title {{
            font-weight: 700;
            color: {COLORS["text"]};
            margin-top: 0.5rem;
            font-size: 0.95rem;
        }}
        .movie-card .meta {{
            color: {COLORS["muted"]};
            font-size: 0.8rem;
        }}
        .movie-card .rating {{
            color: {COLORS["primary"]};
            font-weight: 700;
        }}

        /* ---------- Headings ---------- */
        h1, h2, h3, h4 {{
            color: {COLORS["text"]};
        }}
        h2 span.accent, .accent-text {{
            color: {COLORS["primary"]};
        }}

        /* ---------- Divider plus discret ---------- */
        hr {{ border-color: {COLORS["border"]} !important; }}

        /* ---------- Tabs ---------- */
        [data-baseweb="tab-list"] button[aria-selected="true"] {{
            color: {COLORS["primary"]} !important;
            border-bottom-color: {COLORS["primary"]} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero_header(title: str, subtitle: str) -> None:
    """Affiche un en-tête type cinéma cohérent avec la maquette."""
    st.markdown(
        f"""
        <div class="datafix-hero">
            <h1>{title}</h1>
            <div class="subtitle">{subtitle}</div>
            <div class="accent-bar"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
