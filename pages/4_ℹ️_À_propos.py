"""Page A propos - DATAFIX."""
from pathlib import Path
import streamlit as st
from utils.theme import inject_global_css, hero_header

st.set_page_config(page_title="DATAFIX – A propos", page_icon="ℹ️", layout="wide")
inject_global_css()

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO = ASSETS / "logo.png"

with st.sidebar:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    st.caption("L'equipe & la methodo")

hero_header(
    title="A <span class='accent-text'>propos</span>",
    subtitle="L'equipe DATAFIX & sa methode.",
)

st.markdown(
    """<div class="datafix-tagline">
        <strong>DATAFIX</strong> est un projet pedagogique mene dans le cadre
        de la formation Data Analyst. L'objectif : livrer un outil operationnel
        a un futur cinema independant en Creuse, avec un positionnement editorial
        affirme — la <strong>comedie francaise post-1980</strong>, selectionnee
        sur la qualite (note TMDB ≥ 6.5/10).
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
            Coordination des sprints, animation des ceremonies agiles,
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
st.markdown("### 👥 L'equipe Data")
e1, e2, e3 = st.columns(3, gap="medium")

team = [
    ("Gatien", "Code Reviewer", "Revue de code, qualite, bonnes pratiques, integration"),
    ("Jade", "Team Member", "Mots-cles, NLP, enrichissement du dataset"),
    ("Liliana", "Team Member", "Distribution, visualisations, analyses"),
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

st.markdown("### 🧭 Notre methode")
st.markdown(
    """
1. **Comprendre le besoin** — interviews client, etude de marche du cinema rural en Creuse.
2. **Definir le positionnement editorial** — comedie francaise post-1980, qualite ≥ 6.5/10.
3. **Collecter les donnees** — IMDb (titres, notes) + TMDB (affiches, synopsis, genres).
4. **Nettoyer & filtrer** — fusion `tconst` ↔ `tmdb_id`, application des criteres metier.
5. **Modeliser** — TF-IDF (FR) sur genres + synopsis, similarite cosinus.
6. **Prototyper** — maquette Figma puis application Streamlit.
7. **Livrer** — demonstration au client + documentation reproductible.
    """
)

st.markdown("### 🎯 Criteres de selection du catalogue")
st.markdown(
    """
- 🥖 **Production francaise** — pour ancrer le cinema dans son territoire.
- 📅 **Sortie apres 1980** — un cinema vivant qui parle aux generations actuelles.
- 🎭 **Genre comedie** — la comedie rassemble toutes les generations en zone rurale.
- ⭐ **Note ≥ 6.5/10 sur TMDB** — gage de qualite, valide par des dizaines de milliers de spectateurs.
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
          <div class="datafix-card-text">Manipulation des donnees, fusion IMDb / TMDB.</div>
        </div>""",
        unsafe_allow_html=True,
    )
with s2:
    st.markdown(
        """<div class="datafix-card">
          <div class="datafix-card-icon">🤖</div>
          <div class="datafix-card-title">scikit-learn</div>
          <div class="datafix-card-text">TF-IDF + cosine similarity pour le moteur.</div>
        </div>""",
        unsafe_allow_html=True,
    )
with s3:
    st.markdown(
        """<div class="datafix-card">
          <div class="datafix-card-icon">🎬</div>
          <div class="datafix-card-title">Streamlit · TMDB API</div>
          <div class="datafix-card-text">Interface multipage et affiches officielles en temps reel.</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.write("")
st.caption("© 2026 DATAFIX · Sprint 4 · Wild Code School")
