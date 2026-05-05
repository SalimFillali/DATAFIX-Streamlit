"""Page Accueil - DATAFIX."""
from pathlib import Path
import streamlit as st
from utils.theme import inject_global_css, hero_header

st.set_page_config(page_title="DATAFIX – Accueil", page_icon="🏠", layout="wide")
inject_global_css()

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO = ASSETS / "logo.png"

with st.sidebar:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    st.caption("v0.2 · Sprint 4 · 2026")

hero_header(
    title="DATAFIX",
    subtitle="La comedie francaise, sublimee par la data.",
)

st.markdown(
    """<div class="datafix-tagline">
        DATAFIX accompagne le futur cinema de la <strong>Creuse</strong> avec
        un moteur de recommandation specialise en <strong>comedie francaise
        post-1980</strong> (note ≥ 6.5/10). De <em>La Boum</em> a
        <em>Hors normes</em>, en passant par les <em>Visiteurs</em> et
        <em>OSS 117</em>, retrouvez la quintessence du rire a la francaise.
    </div>""",
    unsafe_allow_html=True,
)

st.write("")
st.subheader("🎬 Que pouvez-vous faire ici ?")

c1, c2, c3 = st.columns(3, gap="large")
with c1:
    st.markdown(
        """<div class="datafix-card">
          <div class="datafix-card-icon">🎯</div>
          <div class="datafix-card-title">Recommander une comedie</div>
          <div class="datafix-card-text">
            Choisissez <em>Intouchables</em>, <em>Amelie Poulain</em>,
            <em>Asterix</em>… et obtenez 8 comedies francaises proches,
            avec affiches et synopsis officiels.
          </div>
        </div>""",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """<div class="datafix-card">
          <div class="datafix-card-icon">📊</div>
          <div class="datafix-card-title">Explorer le catalogue FR</div>
          <div class="datafix-card-text">
            30 comedies francaises iconiques, toutes notees ≥ 6.5/10.
            Repartition par decennie, classement, top des mieux notes.
          </div>
        </div>""",
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        """<div class="datafix-card">
          <div class="datafix-card-icon">ℹ️</div>
          <div class="datafix-card-title">A propos</div>
          <div class="datafix-card-text">
            Decouvrez l'equipe DATAFIX, la methodologie de selection et la
            stack (Python · scikit-learn · Streamlit · TMDB).
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

st.write("")
if st.button("🎬 Demarrer une recommandation", use_container_width=True, type="primary"):
    st.switch_page("pages/2_🎯_Recommandation.py")
