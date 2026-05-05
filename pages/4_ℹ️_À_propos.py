"""Page A propos - DATAFIX."""
from pathlib import Path
import streamlit as st
from utils.theme import inject_global_css, hero_header

st.set_page_config(page_title="DATAFIX – À propos", page_icon="ℹ️", layout="wide")
inject_global_css()

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO = ASSETS / "logo.png"

with st.sidebar:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    st.caption("L'équipe et la méthodo")

hero_header(
    title="À <span class='accent-text'>propos</span>",
    subtitle="L'équipe DATAFIX et sa méthode.",
)

st.markdown(
    """<div class="datafix-tagline">
        <strong>DATAFIX</strong> est un projet pédagogique mené dans le cadre
        de la formation Data Analyst. L'objectif : livrer un outil opérationnel
        à un futur cinéma indépendant en Creuse, avec un positionnement éditorial
        affirmé. Notre choix : la <strong>comédie française post-1980</strong>,
        sélectionnée sur la qualité (note TMDB ≥ 6.5/10).
    </div>""",
    unsafe_allow_html=True,
)

st.write("")

# --- Scrum Master --------------------------------------------------- #
st.markdown("### 🧭 Scrum Master")
scrum_l, scrum_c, scrum_r = st.columns([1, 2, 1])
with scrum_c:
    st.markdown(
        """<div class="datafix-card" style="border-left: 4px solid #F5C518; text-align:center;">
          <div class="datafix-card-icon">🎬</div>
          <div class="datafix-card-title">Romain</div>
          <div class="datafix-card-text">
            <strong>Scrum Master</strong><br>
            Coordination des sprints, animation des cérémonies agiles,
            facilitation et suppression des obstacles.
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

st.write("")
st.divider()

# --- Product Owner -------------------------------------------------- #
st.markdown("### 🎯 Product Owner")
po_l, po_c, po_r = st.columns([1, 2, 1])
with po_c:
    st.markdown(
        """<div class="datafix-card" style="border-left: 4px solid #F5C518; text-align:center;">
          <div class="datafix-card-icon">📋</div>
          <div class="datafix-card-title">Salim</div>
          <div class="datafix-card-text">
            <strong>Product Owner</strong><br>
            Vision produit, priorisation du backlog, lien avec le client,
            arbitrage des choix fonctionnels.
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

st.write("")
st.divider()

# --- Équipe Data ---------------------------------------------------- #
st.markdown("### 👥 L'équipe Data")
e1, e2, e3 = st.columns(3, gap="medium")

team = [
    ("Gatien", "Code Reviewer", "Revue de code, qualité, bonnes pratiques, intégration."),
    ("Jade", "Team Member", "Mots-clés, NLP, enrichissement du dataset."),
    ("Liliana", "Team Member", "Distribution, visualisations, analyses."),
]

for col, (name, role, mission) in zip([e1, e2, e3], team):
    with col:
        st.markdown(
            f"""<div class="datafix-card">
              <div class="datafix-card-icon">🎬</div>
              <div class="datafix-card-title">{name}</div>
              <div class="datafix-card-text"><strong>{role}</strong><br>{mission}</div>
            </div>""",
            unsafe_allow_html=True,
        )

st.write("")
st.divider()

st.markdown("### 🧭 Notre méthode")
st.markdown(
    """
1. **Comprendre le besoin.** Interviews client, étude de marché du cinéma rural en Creuse.
2. **Définir le positionnement éditorial.** Comédie française post-1980, qualité ≥ 6.5/10.
3. **Collecter les données.** IMDb (titres, notes) et TMDB (affiches, synopsis, genres).
4. **Nettoyer et filtrer.** Fusion `tconst` ↔ `tmdb_id`, application des critères métier.
5. **Modéliser.** TF-IDF (FR) sur genres et synopsis, similarité cosinus.
6. **Prototyper.** Maquette Figma puis application Streamlit.
7. **Livrer.** Démonstration au client, documentation reproductible.
    """
)

st.markdown("### 🎯 Critères de sélection du catalogue")
st.markdown(
    """
- 🥖 **Production française.** Pour ancrer le cinéma dans son territoire.
- 📅 **Sortie après 1980.** Un cinéma vivant qui parle aux générations actuelles.
- 🎭 **Genre comédie.** La comédie rassemble toutes les générations en zone rurale.
- ⭐ **Note ≥ 6.5/10 sur TMDB.** Gage de qualité, validé par des dizaines de milliers de spectateurs.
    """
)

st.divider()
st.markdown("### 🛠️ Stack technique")
s1, s2, s3 = st.columns(3, gap="large")
with s1:
    st.markdown(
        """<div class="datafix-card">
          <div class="datafix-card-icon">🐍</div>
          <div class="datafix-card-title">Python · Pandas</div>
          <div class="datafix-card-text">Manipulation des données, fusion des sources IMDb et TMDB.</div>
        </div>""",
        unsafe_allow_html=True,
    )
with s2:
    st.markdown(
        """<div class="datafix-card">
          <div class="datafix-card-icon">🤖</div>
          <div class="datafix-card-title">scikit-learn</div>
          <div class="datafix-card-text">TF-IDF et similarité cosinus pour le moteur de recommandation.</div>
        </div>""",
        unsafe_allow_html=True,
    )
with s3:
    st.markdown(
        """<div class="datafix-card">
          <div class="datafix-card-icon">🎬</div>
          <div class="datafix-card-title">Streamlit · TMDB API</div>
          <div class="datafix-card-text">Interface multipage et affiches officielles en temps réel.</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.write("")
st.caption("© 2026 DATAFIX · Sprint 4 · Wild Code School")
