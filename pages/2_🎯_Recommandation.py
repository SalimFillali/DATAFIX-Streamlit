"""Page Recommandation - DATAFIX."""
from pathlib import Path
import streamlit as st
from utils.theme import inject_global_css, hero_header
from utils.data_loader import load_movies
from utils.tmdb_api import poster_url_for_row
from utils.recommender import recommend

st.set_page_config(page_title="DATAFIX – Recommandation", page_icon="🎯", layout="wide")
inject_global_css()

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO = ASSETS / "logo.png"

with st.sidebar:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    st.markdown("### 🎯 Filtres")
    n_reco = st.slider("Nombre de recommandations", 4, 16, 8, step=1)
    only_well_rated = st.checkbox("Excellence uniquement (≥ 7/10)", value=False)
    st.caption("Filtre métier : comédies françaises post-1980, notées 6.5/10 ou plus.")
    st.divider()

df = load_movies()
if only_well_rated and "vote_average" in df.columns:
    df = df[df["vote_average"].fillna(0) >= 7.0].reset_index(drop=True)

hero_header(
    title="Reco<span class='accent-text'>mmandation</span>",
    subtitle="Comédies françaises post-1980, notées 6.5/10 ou plus.",
)

titles = df["title"].dropna().astype(str).sort_values().unique().tolist()
default_idx = titles.index("Intouchables") if "Intouchables" in titles else 0

col_sel, col_btn = st.columns([4, 1])
with col_sel:
    chosen = st.selectbox(
        "🎬 Choisissez une comédie française de référence",
        titles,
        index=default_idx,
    )
with col_btn:
    st.write("")
    st.write("")
    st.button("Lancer 🚀", use_container_width=True, type="primary")

if not chosen:
    st.stop()

ref = df[df["title"].str.lower() == chosen.lower()].iloc[0]

st.write("")
st.markdown("### 📽️ Film de référence")
ref_col1, ref_col2 = st.columns([1, 3])
with ref_col1:
    st.image(poster_url_for_row(ref), use_container_width=True)
with ref_col2:
    st.markdown(f"## {ref['title']}")
    meta_bits = []
    year_val = ref.get("year")
    if year_val is not None and str(year_val) not in ("nan", "None", ""):
        try:
            meta_bits.append(f"📅 {int(float(year_val))}")
        except (ValueError, TypeError):
            meta_bits.append(f"📅 {year_val}")
    if "genres" in ref and str(ref["genres"]) not in ("nan", "None", ""):
        meta_bits.append(f"🎭 {ref['genres']}")
    if "vote_average" in ref and str(ref["vote_average"]) not in ("nan", "None", ""):
        meta_bits.append(f"⭐ {float(ref['vote_average']):.1f}/10")
    st.caption(" · ".join(meta_bits))
    if "overview" in ref and str(ref["overview"]) not in ("nan", "None", ""):
        st.write(ref["overview"])

st.divider()

recos = recommend(df, chosen, n=n_reco)
if recos.empty:
    st.warning("Pas de recommandation trouvée pour ce film.")
    st.stop()

st.markdown(f"### 🎯 Top {len(recos)} comédies similaires à *{chosen}*")
st.write("")

cols_per_row = 4
rows = (len(recos) + cols_per_row - 1) // cols_per_row
for r in range(rows):
    cols = st.columns(cols_per_row, gap="medium")
    for c in range(cols_per_row):
        i = r * cols_per_row + c
        if i >= len(recos):
            continue
        row = recos.iloc[i]
        with cols[c]:
            st.image(poster_url_for_row(row), use_container_width=True)
            st.markdown(f"**{row['title']}**")
            sub_bits = []
            year_val = row.get("year")
            if year_val is not None and str(year_val) not in ("nan", "None", ""):
                try:
                    sub_bits.append(str(int(float(year_val))))
                except (ValueError, TypeError):
                    sub_bits.append(str(year_val))
            if "vote_average" in row and str(row["vote_average"]) not in ("nan", "None", ""):
                sub_bits.append(f"⭐ {float(row['vote_average']):.1f}")
            sub_bits.append(f"sim. {row['similarity']*100:.0f}%")
            st.caption(" · ".join(sub_bits))
            if "overview" in row and str(row["overview"]) not in ("nan", "None", ""):
                with st.expander("Synopsis"):
                    st.write(row["overview"])

st.write("")
st.success(f"✅ {len(recos)} recommandations générées en quelques millisecondes.")
