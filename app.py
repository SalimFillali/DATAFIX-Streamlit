"""DATAFIX – Application Streamlit (point d'entree)."""
from pathlib import Path
import streamlit as st
from utils.theme import inject_global_css

st.set_page_config(
    page_title="DATAFIX – Recommandation de comédies françaises",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

ASSETS = Path(__file__).parent / "assets"
LOGO = ASSETS / "logo.png"

# --- Sidebar -------------------------------------------------------- #
with st.sidebar:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    st.markdown("### 🎬 DATAFIX")
    st.caption("Recommandation de comédies françaises pour le cinéma de la Creuse.")
    st.divider()
    st.markdown(
        "**Navigation**\n\n"
        "- 🏠 Accueil\n"
        "- 🎯 Recommandation\n"
        "- 📊 Statistiques\n"
        "- ℹ️ À propos"
    )
    st.divider()
    st.caption("v0.2 · Sprint 4 · 2026")

# --- HERO : logo image au lieu du texte ------------------------------ #
hero_l, hero_c, hero_r = st.columns([1, 2, 1])
with hero_c:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    st.markdown(
        """<div style="text-align:center; color:#9A9AA0; font-size:1.15rem; margin-top:-0.5rem;">
            La comédie française, sublimée par la data.
        </div>
        <div style="width:84px; height:4px; background:#F5C518; border-radius:4px; margin: 1rem auto 0;"></div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

st.markdown(
    """
    <div class="datafix-tagline">
        Bienvenue dans l'application de recommandation conçue pour le futur cinéma
        de la <strong>Creuse</strong>. Notre catalogue est ciblé sur la
        <strong>comédie française post-1980</strong>, avec uniquement des films
        notés <strong>6.5/10 ou plus</strong>. D'<em>Intouchables</em> à
        <em>Astérix</em>, en passant par <em>Amélie Poulain</em> et le
        <em>Dîner de cons</em>, retrouvez la quintessence du rire à la française.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.markdown(
        """<div class="datafix-card">
            <div class="datafix-card-icon">🥖</div>
            <div class="datafix-card-title">100% comédie française</div>
            <div class="datafix-card-text">
                Catalogue trié sur le volet : uniquement des comédies françaises
                sorties <strong>après 1980</strong>, avec une note minimale de
                <strong>6.5/10</strong>.
            </div>
        </div>""",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """<div class="datafix-card">
            <div class="datafix-card-icon">🎞️</div>
            <div class="datafix-card-title">Affiches officielles</div>
            <div class="datafix-card-text">
                Toutes les affiches sont récupérées en direct depuis l'API
                <strong>TMDB</strong> pour une expérience visuelle premium.
            </div>
        </div>""",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """<div class="datafix-card">
            <div class="datafix-card-icon">🎯</div>
            <div class="datafix-card-title">Reco ciblée</div>
            <div class="datafix-card-text">
                Choisissez <em>Intouchables</em>, <em>Amélie</em> ou
                <em>Astérix</em>, l'algorithme propose en un clin d'œil les
                comédies les plus proches.
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

st.write("")
st.write("")

cta_l, cta_c, cta_r = st.columns([1, 2, 1])
with cta_c:
    if st.button("🎬 Démarrer une recommandation", use_container_width=True, type="primary"):
        st.switch_page("pages/2_🎯_Recommandation.py")

st.write("")
st.divider()

st.markdown("#### 🔢 En quelques chiffres")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Comédies sélectionnées", "30", "≥ 6.5/10")
m2.metric("Période", "1980 à 2019", "")
m3.metric("Note moyenne", "7.0", "/10")
m4.metric("Algorithme", "Cosine", "TF-IDF")

st.write("")
st.caption(
    "© 2026 DATAFIX · Projet pédagogique, Wild Code School. "
    "Sources : TMDB, IMDb (usage non commercial)."
)
