"""
Page Statistiques – KPIs et visualisations du catalogue.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.theme import inject_global_css, hero_header, COLORS
from utils.data_loader import load_movies, get_genre_list

st.set_page_config(
    page_title="DATAFIX – Statistiques",
    page_icon="📊",
    layout="wide",
)
inject_global_css()

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO = ASSETS / "logo.png"

with st.sidebar:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    st.caption("Tableaux de bord du catalogue")

hero_header(
    title="Stat<span class='accent-text'>istiques</span>",
    subtitle="Comprendre le catalogue pour mieux programmer.",
)

df = load_movies()

# ------------------------------- KPIs --------------------------------------- #
total = len(df)
n_genres = len(get_genre_list(df))

avg_rating = (
    float(df["vote_average"].mean())
    if "vote_average" in df.columns and df["vote_average"].notna().any()
    else None
)
year_min = (
    int(pd.to_numeric(df["year"], errors="coerce").min())
    if "year" in df.columns else None
)
year_max = (
    int(pd.to_numeric(df["year"], errors="coerce").max())
    if "year" in df.columns else None
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("🎬 Films", f"{total:,}".replace(",", " "))
m2.metric("🎭 Genres", n_genres)
m3.metric("⭐ Note moyenne", f"{avg_rating:.2f}" if avg_rating else "—")
m4.metric(
    "📅 Période",
    f"{year_min}-{year_max}" if year_min and year_max else "—",
)

st.divider()

# ------------------------ Top 10 films notés -------------------------------- #
if "vote_average" in df.columns:
    st.markdown("#### ⭐ Top 10 des films les mieux notés")
    top = (
        df.dropna(subset=["vote_average"])
          .sort_values("vote_average", ascending=False)
          .head(10)[["title", "year", "genres", "vote_average"]]
          .reset_index(drop=True)
    )
    st.dataframe(top, use_container_width=True, hide_index=True)

st.write("")

# ------------------------ Répartition par genre ----------------------------- #
left, right = st.columns(2, gap="large")

with left:
    st.markdown("#### 🎭 Répartition par genre")
    if "genres" in df.columns:
        flat = (
            df["genres"].dropna().astype(str)
              .str.replace(",", " ").str.split()
              .explode()
        )
        counts = flat.value_counts().head(10)
        chart_df = pd.DataFrame({"genre": counts.index, "films": counts.values})
        st.bar_chart(chart_df, x="genre", y="films", color=COLORS["primary"])
    else:
        st.info("Colonne genres absente du dataset.")

with right:
    st.markdown("#### 📅 Films par décennie")
    if "year" in df.columns:
        years = pd.to_numeric(df["year"], errors="coerce").dropna().astype(int)
        decade = (years // 10 * 10).astype(str) + "s"
        counts = decade.value_counts().sort_index()
        chart_df = pd.DataFrame({"décennie": counts.index, "films": counts.values})
        st.bar_chart(chart_df, x="décennie", y="films", color=COLORS["primary"])
    else:
        st.info("Colonne year absente du dataset.")
