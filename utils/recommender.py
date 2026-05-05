"""
Moteur de recommandation – Content-based
=========================================
Approche : TF-IDF sur la concaténation `genres + overview`, puis cosine
similarity entre le film sélectionné et l'ensemble du catalogue.

Adapté au catalogue DATAFIX : comédies françaises post-1980 (texte FR).
"""
from __future__ import annotations

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _build_corpus(df: pd.DataFrame) -> pd.Series:
    """Construit le 'sac de mots' qui décrira chaque film."""
    genres = df.get("genres", pd.Series([""] * len(df))).fillna("").astype(str)
    overview = df.get("overview", pd.Series([""] * len(df))).fillna("").astype(str)
    # On donne plus de poids au genre en le répétant (heuristique simple)
    return (genres + " " + genres + " " + overview).str.lower()


@st.cache_resource(show_spinner="Construction du moteur de recommandation...")
def build_similarity_matrix(df: pd.DataFrame):
    """Calcule (et met en cache) la matrice de similarité cosine."""
    corpus = _build_corpus(df)
    # Liste minimaliste de stop-words FR pour ne pas polluer la similarité.
    french_stops = [
        "le", "la", "les", "un", "une", "des", "de", "du", "et", "ou",
        "ce", "ces", "cette", "se", "sa", "son", "ses", "il", "elle", "on",
        "ils", "elles", "qui", "que", "dans", "sur", "pour", "par", "avec",
        "sans", "mais", "ne", "pas", "est", "sont", "ete", "etre", "avoir",
        "fait", "tout", "tous", "toute", "toutes", "plus", "moins", "tres",
        "leur", "leurs", "au", "aux", "a",
    ]
    vectorizer = TfidfVectorizer(
        stop_words=french_stops,
        max_features=20000,
        ngram_range=(1, 2),
        min_df=1,
        lowercase=True,
        strip_accents="unicode",
    )
    matrix = vectorizer.fit_transform(corpus)
    sim = cosine_similarity(matrix, matrix)
    return sim


def recommend(
    df: pd.DataFrame,
    title: str,
    n: int = 8,
    same_genre_boost: bool = True,
) -> pd.DataFrame:
    """Renvoie les `n` films les plus similaires à `title`."""
    if "title" not in df.columns:
        return pd.DataFrame()

    matches = df.index[df["title"].str.lower() == title.lower()].tolist()
    if not matches:
        return pd.DataFrame()
    idx = matches[0]

    sim = build_similarity_matrix(df)
    scores = list(enumerate(sim[idx]))
    scores.sort(key=lambda x: x[1], reverse=True)

    # On retire le film lui-même
    scores = [s for s in scores if s[0] != idx]

    if same_genre_boost and "genres" in df.columns:
        ref_genres = set(str(df.at[idx, "genres"]).lower().split())
        if ref_genres:
            def has_common_genre(i: int) -> bool:
                cand = set(str(df.at[i, "genres"]).lower().split())
                return bool(cand & ref_genres)
            preferred = [s for s in scores if has_common_genre(s[0])]
            if len(preferred) >= n:
                scores = preferred

    top_idx = [s[0] for s in scores[:n]]
    top_scores = [s[1] for s in scores[:n]]

    out = df.iloc[top_idx].copy().reset_index(drop=True)
    out["similarity"] = top_scores
    return out
