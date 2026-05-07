"""Chargement du catalogue DATAFIX.

Source principale : data/df_concat.csv (1559 films, mots-clés enrichis).
Enrichissement    : data/movies_final.csv (synopsis + poster_path TMDB).
Le merge se fait sur tmdb_id.
"""
from __future__ import annotations
from pathlib import Path
import ast
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _parse_keywords(raw):
    """Extrait les mots-cles stockes sous forme de '[\"a\", \"b\"]' (string Python)."""
    if pd.isna(raw):
        return ""
    s = str(raw).strip()
    if not s or s == "[]":
        return ""
    try:
        kws = ast.literal_eval(s)
        if isinstance(kws, list):
            return " ".join(str(k) for k in kws)
    except (ValueError, SyntaxError):
        pass
    return s.replace("[", "").replace("]", "").replace("'", "").replace(",", " ")


def _normalize_df_concat(df: pd.DataFrame) -> pd.DataFrame:
    """Adapte df_concat.csv au schema attendu par l'app."""
    rename_map = {
        "Titre": "title",
        "Année": "year",
        "Note": "vote_average",
        "Votes": "vote_count",
        "id_tmdb": "tmdb_id",
        "Genres": "genres",
        "Mots clés": "keywords_raw",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Genres : "Comédie | Drame | Mystère" -> "Comedie Drame Mystere"
    if "genres" in df.columns:
        df["genres"] = (
            df["genres"].fillna("").astype(str)
            .str.replace("|", " ", regex=False)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    # Mots-cles : "['paris', 'love']" -> "paris love"
    df["keywords"] = (
        df["keywords_raw"].apply(_parse_keywords)
        if "keywords_raw" in df.columns else ""
    )

    # Conversions numeriques propres
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
    if "vote_average" in df.columns:
        df["vote_average"] = pd.to_numeric(df["vote_average"], errors="coerce")
    if "vote_count" in df.columns:
        df["vote_count"] = pd.to_numeric(df["vote_count"], errors="coerce")
    if "tmdb_id" in df.columns:
        df["tmdb_id"] = pd.to_numeric(df["tmdb_id"], errors="coerce").astype("Int64")

    return df


def _enrich_with_movies_final(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute synopsis (overview) et poster_path depuis movies_final.csv si dispo."""
    enrich_path = DATA_DIR / "movies_final.csv"
    if not enrich_path.exists():
        df["overview"] = df.get("keywords", "")
        df["poster_path"] = ""
        return df

    extra = pd.read_csv(enrich_path)
    cols_extra = [c for c in ["tmdb_id", "overview", "poster_path"] if c in extra.columns]
    if "tmdb_id" not in cols_extra:
        df["overview"] = df.get("keywords", "")
        df["poster_path"] = ""
        return df

    extra = extra[cols_extra].copy()
    extra["tmdb_id"] = pd.to_numeric(extra["tmdb_id"], errors="coerce").astype("Int64")

    # Merge sur tmdb_id pour ajouter overview et poster_path
    merged = df.merge(extra, on="tmdb_id", how="left", suffixes=("", "_ext"))

    # Garantit la presence des colonnes
    if "overview" not in merged.columns:
        merged["overview"] = ""
    if "poster_path" not in merged.columns:
        merged["poster_path"] = ""

    # Si overview vide, on retombe sur les mots-cles (utile pour le moteur de reco)
    merged["overview"] = merged["overview"].fillna("").astype(str)
    mask_empty = merged["overview"].str.strip() == ""
    merged.loc[mask_empty, "overview"] = merged.loc[mask_empty, "keywords"].fillna("")

    merged["poster_path"] = merged["poster_path"].fillna("").astype(str)

    return merged


@st.cache_data(show_spinner="Chargement du catalogue de comedies francaises...")
def load_movies(min_rating: float = 6.5, after_year: int = 1980) -> pd.DataFrame:
    """Charge df_concat.csv enrichi par movies_final.csv, avec filtre metier."""
    csv_path = DATA_DIR / "df_concat.csv"
    if not csv_path.exists():
        return pd.DataFrame(columns=[
            "tmdb_id", "title", "year", "genres",
            "overview", "poster_path", "vote_average", "vote_count",
        ])

    df = pd.read_csv(csv_path)
    df = _normalize_df_concat(df)
    df = _enrich_with_movies_final(df)

    # Filtre metier : note >= 6.5, annee >= 1980
    if "vote_average" in df.columns:
        df = df[df["vote_average"].fillna(0) >= min_rating]
    if "year" in df.columns:
        df = df[df["year"].fillna(0) >= after_year]

    # Colonnes finales
    keep = [c for c in [
        "tmdb_id", "title", "year", "genres",
        "overview", "keywords", "poster_path",
        "vote_average", "vote_count",
    ] if c in df.columns]
    df = df[keep].dropna(subset=["title"]).drop_duplicates(subset=["title"])

    # Tri par popularite decroissante
    if "vote_count" in df.columns:
        df = df.sort_values("vote_count", ascending=False)

    return df.reset_index(drop=True)


def get_genre_list(df: pd.DataFrame) -> list[str]:
    """Liste unique des genres presents dans le catalogue."""
    if "genres" not in df.columns:
        return []
    series = df["genres"].dropna().astype(str)
    bag = set()
    for raw in series:
        for token in raw.replace(",", " ").split():
            token = token.strip()
            if token:
                bag.add(token)
    return sorted(bag)
