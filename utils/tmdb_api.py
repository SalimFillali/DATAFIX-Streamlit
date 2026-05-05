"""Module d'acces a l'API TMDB pour les affiches officielles."""
from __future__ import annotations
import os
from urllib.parse import quote
import requests
import streamlit as st

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMG_BASE = "https://image.tmdb.org/t/p"
PLACEHOLDER_BG = "0E0E10"
PLACEHOLDER_FG = "F5C518"


def _get_api_key():
    """Lit la cle API depuis les secrets Streamlit ou l'env."""
    try:
        if "TMDB_API_KEY" in st.secrets:
            return st.secrets["TMDB_API_KEY"]
    except (FileNotFoundError, KeyError):
        pass
    return os.environ.get("TMDB_API_KEY")


def _placeholder(title="DATAFIX"):
    """Genere une URL placeholder fiable avec le titre du film."""
    safe_title = quote(str(title)[:30].replace(" ", "\\n"))
    return f"https://placehold.co/500x750/{PLACEHOLDER_BG}/{PLACEHOLDER_FG}.png?text={safe_title}&font=montserrat"


@st.cache_data(ttl=86400, show_spinner=False)
def _fetch_poster_path_from_tmdb(tmdb_id):
    """Recupere le vrai poster_path depuis TMDB via l'ID. Retourne None si echec."""
    api_key = _get_api_key()
    if not api_key or not tmdb_id:
        return None
    try:
        resp = requests.get(
            f"{TMDB_BASE_URL}/movie/{int(tmdb_id)}",
            params={"api_key": api_key, "language": "fr-FR"},
            timeout=5,
        )
        if resp.status_code == 200:
            return resp.json().get("poster_path")
    except (requests.RequestException, ValueError):
        return None
    return None


def poster_url(poster_path=None, size="w500", tmdb_id=None, title="Film"):
    """Construit l'URL d'une affiche TMDB avec fallback intelligent.

    Ordre de priorite :
    1. URL complete si fournie (commence par http)
    2. poster_path TMDB statique (si valide)
    3. API TMDB si tmdb_id fourni et cle API dispo
    4. Placeholder colore avec le titre
    """
    if poster_path and str(poster_path).startswith("http"):
        return str(poster_path)

    if poster_path and str(poster_path).strip() not in ("", "nan", "None"):
        return f"{TMDB_IMG_BASE}/{size}{poster_path}"

    if tmdb_id:
        fetched = _fetch_poster_path_from_tmdb(tmdb_id)
        if fetched:
            return f"{TMDB_IMG_BASE}/{size}{fetched}"

    return _placeholder(title)


def poster_url_for_row(row, size="w500"):
    """Helper : recupere l'URL d'affiche pour une ligne du DataFrame."""
    return poster_url(
        poster_path=row.get("poster_path"),
        size=size,
        tmdb_id=row.get("tmdb_id"),
        title=row.get("title", "Film"),
    )


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_movie_details(tmdb_id, language="fr-FR"):
    """Recupere les details d'un film via l'API TMDB."""
    api_key = _get_api_key()
    if not api_key:
        return {}
    try:
        resp = requests.get(
            f"{TMDB_BASE_URL}/movie/{int(tmdb_id)}",
            params={"api_key": api_key, "language": language},
            timeout=8,
        )
        if resp.status_code == 200:
            return resp.json()
    except (requests.RequestException, ValueError):
        return {}
    return {}
