"""Page Accueil - DATAFIX."""
from pathlib import Path
import streamlit as st
from utils.theme import inject_global_css

st.set_page_config(page_title="DATAFIX – Accueil", page_icon="🏠", layout="wide")
inject_global_css()

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO = ASSETS / "logo.png"

with st.sidebar:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    st.caption("v0.2 · Sprint 4 · 2026")

# --- HERO : grand logo image (identique à app.py) ------------------- #
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
    """<div class="datafix-tagline">
        DATAFIX accompagne le futur cinéma de la <strong>Creuse</strong> avec
        un moteur de recommandation dédié aux meilleures
        <strong>comédies françaises</strong>. Découvrez des films cultes et
        trouvez facilement votre prochaine séance idéale.
    </div>""",
    unsafe_allow_html=True,
)

st.write("")
st.write("")
st.subheader("Que pouvez-vous faire ici ?")
st.write("")

c1, c2, c3 = st.columns(3, gap="large")
with c1:
    st.markdown(
        """<div class="datafix-card-clean">
          <div class="num">01 / Recommandation</div>
          <div class="title">Recommander une comédie</div>
          <div class="text">
            Choisissez Intouchables, Amélie Poulain, Astérix… vous obtenez
            instantanément 8 comédies françaises proches, avec leurs affiches
            et synopsis officiels.
          </div>
        </div>""",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """<div class="datafix-card-clean">
          <div class="num">02 / Catalogue</div>
          <div class="title">Explorer le catalogue FR</div>
          <div class="text">
            322 comédies françaises sélectionnées, toutes notées 6.5/10 ou plus.
            Répartition par décennie, classement, top des mieux notées.
          </div>
        </div>""",
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        """<div class="datafix-card-clean">
          <div class="num">03 / Équipe</div>
          <div class="title">À propos</div>
          <div class="text">
            Découvrez l'équipe DATAFIX, la méthodologie de sélection et la
            stack technique (Python, scikit-learn, Streamlit, TMDB).
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

st.write("")
st.write("")
if st.button("Démarrer une recommandation", use_container_width=True, type="primary"):
    st.switch_page("pages/2_🎯_Recommandation.py")
