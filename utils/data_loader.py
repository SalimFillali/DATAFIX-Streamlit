"""Chargement du catalogue DATAFIX.

Source principale : data/df_concat.csv (1559 films, mots-cles enrichis).
Enrichissements   : data/movies_final.csv (322 films verifies)
                    data/posters.csv      (1339 films, large couverture)
Le merge se fait sur tmdb_id.
"""
from __future__ import annotations
from pathlib import Path
import ast
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _parse_keywords(raw):
    """Extrait les mots-cles stockes sous forme de '["a", "b"]' (string Python)."""
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


def _normalize_df_concat(df):
    """Adapte df_concat.csv au schema attendu par l'app."""
    rename_map = {
        "Titre": "title",
        "Annee": "year",
        "Note": "vote_average",
        "Votes": "vote_count",
        "id_tmdb": "tmdb_id",
        "Genres": "genres",
        "Mots cles": "keywords_raw",
    }
    # Le CSV reel utilise les accents : on remappe sur les vraies cles
    rename_map_real = {
        "Titre": "title",
        "Année": "year",
        "Note": "vote_average",
        "Votes": "vote_count",
        "id_tmdb": "tmdb_id",
        "Genres": "genres",
        "Mots clés": "keywords_raw",
    }
    df = df.rename(columns={k: v for k, v in rename_map_real.items() if k in df.columns})

    if "genres" in df.columns:
        df["genres"] = (
            df["genres"].fillna("").astype(str)
            .str.replace("|", " ", regex=False)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    df["keywords"] = (
        df["keywords_raw"].apply(_parse_keywords)
        if "keywords_raw" in df.columns else ""
    )

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
    if "vote_average" in df.columns:
        df["vote_average"] = pd.to_numeric(df["vote_average"], errors="coerce")
    if "vote_count" in df.columns:
        df["vote_count"] = pd.to_numeric(df["vote_count"], errors="coerce")
    if "tmdb_id" in df.columns:
        df["tmdb_id"] = pd.to_numeric(df["tmdb_id"], errors="coerce").astype("Int64")

    return df


def _merge_enrichment(df, enrich_path):
    """Merge un CSV d'enrichissement (overview + poster_path) sur tmdb_id.
    Ne remplace que les valeurs vides : ce qui est deja rempli reste prioritaire.
    """
    if not enrich_path.exists():
        return df

    extra = pd.read_csv(enrich_path)
    cols_extra = [c for c in ["tmdb_id", "overview", "poster_path"] if c in extra.columns]
    if "tmdb_id" not in cols_extra:
        return df

    extra = extra[cols_extra].copy()
    extra["tmdb_id"] = pd.to_numeric(extra["tmdb_id"], errors="coerce").astype("Int64")
    extra = extra.drop_duplicates(subset=["tmdb_id"])

    if "overview" not in df.columns:
        df["overview"] = ""
    if "poster_path" not in df.columns:
        df["poster_path"] = ""

    df["overview"] = df["overview"].fillna("").astype(str)
    df["poster_path"] = df["poster_path"].fillna("").astype(str)

    merged = df.merge(extra, on="tmdb_id", how="left", suffixes=("", "_ext"))

    if "overview_ext" in merged.columns:
        mask_empty = merged["overview"].str.strip() == ""
        merged.loc[mask_empty, "overview"] = (
            merged.loc[mask_empty, "overview_ext"].fillna("").astype(str)
        )
        merged = merged.drop(columns=["overview_ext"])

    if "poster_path_ext" in merged.columns:
        mask_empty = merged["poster_path"].str.strip() == ""
        merged.loc[mask_empty, "poster_path"] = (
            merged.loc[mask_empty, "poster_path_ext"].fillna("").astype(str)
        )
        merged = merged.drop(columns=["poster_path_ext"])

    return merged


def _enrich_with_movies_final(df):
    """Ajoute synopsis (overview) et poster_path depuis plusieurs sources."""
    if "overview" not in df.columns:
        df["overview"] = ""
    if "poster_path" not in df.columns:
        df["poster_path"] = ""

    df = _merge_enrichment(df, DATA_DIR / "movies_final.csv")
    df = _merge_enrichment(df, DATA_DIR / "posters.csv")

    if "overview" not in df.columns:
        df["overview"] = ""
    if "poster_path" not in df.columns:
        df["poster_path"] = ""

    df["overview"] = df["overview"].fillna("").astype(str)
    df["poster_path"] = df["poster_path"].fillna("").astype(str)

    mask_empty = df["overview"].str.strip() == ""
    if "keywords" in df.columns:
        df.loc[mask_empty, "overview"] = df.loc[mask_empty, "keywords"].fillna("")

    return df


@st.cache_data(show_spinner="Chargement du catalogue de comedies francaises...")
def load_movies(min_rating=6.5, after_year=1980):
    """Charge df_concat.csv enrichi par movies_final.csv et posters.csv."""
    csv_path = DATA_DIR / "df_concat.csv"
    if not csv_path.exists():
        return pd.DataFrame(columns=[
            "tmdb_id", "title", "year", "genres",
            "overview", "poster_path", "vote_average", "vote_count",
        ])

    df = pd.read_csv(csv_path)
    df = _normalize_df_concat(df)
    df = _enrich_with_movies_final(df)

    if "vote_average" in df.columns:
        df = df[df["vote_average"].fillna(0) >= min_rating]
    if "year" in df.columns:
        df = df[df["year"].fillna(0) >= after_year]

    keep = [c for c in [
        "tmdb_id", "title", "year", "genres",
        "overview", "keywords", "poster_path",
        "vote_average", "vote_count",
    ] if c in df.columns]
    df = df[keep].dropna(subset=["title"]).drop_duplicates(subset=["title"])

    if "vote_count" in df.columns:
        df = df.sort_values("vote_count", ascending=False)

    return df.reset_index(drop=True)


def get_genre_list(df):
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
