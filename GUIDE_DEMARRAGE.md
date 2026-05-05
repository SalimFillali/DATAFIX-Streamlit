# 🚀 Guide pas-à-pas — DATAFIX Streamlit

> Ce guide reprend **exactement** les étapes de l'énoncé du Sprint 4. Tu peux le suivre du début à la fin, en copiant les blocs de code dans ton terminal. Tout est déjà prêt dans le dossier `DATAFIX-Streamlit/` que je t'ai créé.

---

## ✅ Étape 0 — Pré-requis

| Outil | Pourquoi | Installation |
|-------|----------|--------------|
| **Python 3.10+** | Faire tourner Streamlit | <https://www.python.org/downloads/> |
| **Git** | Versionner le projet | <https://git-scm.com/downloads> |
| **VS Code** (recommandé) | Éditer le code | <https://code.visualstudio.com/> |
| **Compte GitHub** | Hébergement du repo | <https://github.com/signup> |
| **Clé API TMDB** (optionnel) | Affiches en direct | <https://www.themoviedb.org/settings/api> |

Vérifie que Python est bien installé :
```bash
python --version
# ou
python3 --version
```

---

## 🎨 Étape 1 — La maquette

> **Bonne nouvelle :** ta maquette Figma est déjà faite ✅
> Lien : [Maquette DATAFIX – Figma Make](https://www.figma.com/make/uqyMucZ3CHStLNQEpuaUq0/Maquette-DATAFIX?p=f&fullscreen=1)

L'app que je t'ai codée respecte la maquette :
- **Fond noir cinéma** (`#0E0E10`) + **accents jaune doré** (`#F5C518`) — exactement le code couleur du logo DATAFIX.
- **Pages :** Accueil · Recommandation · Statistiques · À propos.
- **Logo DATAFIX** affiché dans la sidebar de chaque page.
- **Navigation** automatique via le menu Streamlit (les pages sont dans `pages/`).

**Découpage des responsabilités** (à remplir avec ton équipe) :

| Page | Responsable | Rôle |
|------|-------------|------|
| 🏠 Accueil | … | Pitch, CTA, chiffres clés |
| 🎯 Recommandation | … | Sélection film + grille de résultats |
| 📊 Statistiques | … | Tableaux de bord catalogue |
| ℹ️ À propos | … | Équipe, méthodo, stack |

---

## 🏗️ Étape 2 — Mise en place de la structure technique

### 2.1 — L'arborescence (déjà créée)

```
DATAFIX-Streamlit/
├── app.py
├── pages/
│   ├── 1_🏠_Accueil.py
│   ├── 2_🎯_Recommandation.py
│   ├── 3_📊_Statistiques.py
│   └── 4_ℹ️_À_propos.py
├── utils/
│   ├── theme.py
│   ├── data_loader.py
│   ├── tmdb_api.py
│   └── recommender.py
├── assets/        ← logo.png déjà placé
├── data/          ← y déposer movies_final.csv (optionnel)
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── requirements.txt
├── README.md
├── GUIDE_DEMARRAGE.md  ← ce fichier
└── .gitignore
```

### 2.2 — Créer l'environnement virtuel

Ouvre un terminal **dans le dossier du projet** :

```bash
cd Downloads/DATAFIX-Streamlit
```

#### Option A — `venv` (standard, fonctionne partout)

```bash
# Créer le venv
python -m venv .venv

# L'activer
# Windows (PowerShell) :
.venv\Scripts\Activate.ps1
# Windows (CMD) :
.venv\Scripts\activate.bat
# macOS / Linux :
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

#### Option B — `uv` (plus rapide, moderne)

```bash
# Installer uv si tu ne l'as pas
pip install uv

# Créer + installer en une commande
uv venv .venv
source .venv/bin/activate     # ou .venv\Scripts\activate sur Windows
uv pip install -r requirements.txt
```

### 2.3 — (Optionnel) Configurer la clé API TMDB

```bash
# Copier le modèle
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Éditer et coller ta clé
# (le fichier secrets.toml est déjà dans .gitignore)
```

### 2.4 — Initialiser Git & GitHub

```bash
# Dans le dossier du projet
git init
git add .
git commit -m "🎬 Initial commit – structure DATAFIX-Streamlit"

# Créer un repo VIDE sur github.com (sans README ni .gitignore)
# puis :
git branch -M main
git remote add origin https://github.com/<ton-user>/DATAFIX-Streamlit.git
git push -u origin main
```

> **Travailler à plusieurs sur GitHub** — workflow simple :
> ```bash
> git checkout -b feature/page-stats     # nouvelle branche par feature
> # ... tu codes ...
> git add .
> git commit -m "📊 Ajout graphique répartition genres"
> git push origin feature/page-stats
> ```
> Puis ouvrir une **Pull Request** sur GitHub → review d'un binôme → merge.

---

## ▶️ Étape 3 — Tester l'application en local

```bash
# Avec ton venv activé
streamlit run app.py
```

Ton navigateur s'ouvre sur <http://localhost:8501>.

**Checklist de validation :**

- [ ] La sidebar affiche le logo DATAFIX.
- [ ] Le fond est noir, les accents jaunes — cohérent avec la maquette Figma.
- [ ] Les 4 pages sont accessibles depuis le menu de gauche.
- [ ] Page Recommandation : choisir "Inception" → 8 films apparaissent avec affiches.
- [ ] Page Statistiques : 4 KPIs en haut + 2 graphes barres.
- [ ] Aucun message d'erreur en bas de page (ni dans le terminal).

**Erreurs fréquentes :**

| Symptôme | Cause | Solution |
|----------|-------|----------|
| `ModuleNotFoundError: streamlit` | venv non activé | Ré-activer le venv |
| Pages absentes du menu | Mauvais dossier `pages/` | Bien lancer `streamlit run app.py` depuis la racine du projet |
| Affiches grises (placeholder) | Pas de clé TMDB | Renseigner `.streamlit/secrets.toml` |
| Encodage cassé sur Windows (`É`) | Console en cp1252 | `chcp 65001` avant `streamlit run` |

---

## 📦 Étape 4 — Brancher tes vraies données (optionnel)

L'app marche en mode démo avec 20 films codés en dur. Pour utiliser le **vrai catalogue** de l'équipe :

1. À partir de `df_movies_final.csv` + `id_movie_Tmdb.csv`, fusionne et renomme :
   ```python
   import pandas as pd

   imdb = pd.read_csv("df_movies_final.csv")
   tmdb = pd.read_csv("id_movie_Tmdb.csv")

   # Si tu as un id IMDb (tconst) qu'on retrouve dans TMDB via /find :
   merged = imdb.merge(tmdb, left_on="title", right_on="title", how="inner")

   merged = merged.rename(columns={
       "id": "tmdb_id",
       "vote_average": "vote_average",
   })
   merged["year"] = pd.to_datetime(merged["release_date"], errors="coerce").dt.year

   merged = merged[[
       "tmdb_id", "title", "year", "genres",
       "overview", "poster_path", "vote_average", "vote_count",
   ]].dropna(subset=["title"])

   merged.to_csv("data/movies_final.csv", index=False)
   ```

2. Recharge l'app : `data_loader.py` détecte automatiquement le CSV.

---

## 🎬 Étape 5 — Préparer la démo client

1. Lance `streamlit run app.py`.
2. Choisis un film "locomotive" (`Inception`, `The Dark Knight`...).
3. Fais **8 captures d'écran** :
   - Accueil hero + cartes
   - Page Reco — sélection
   - Page Reco — résultats
   - Page Stats — KPIs
   - Page Stats — graphes
   - Page À propos — équipe
   - Mobile (responsive)
   - Code (extrait `recommender.py`)
4. Ces captures alimentent ton **livrable de présentation écrit** (`Presentation_DATAFIX_Streamlit.docx`).

---

## 🎯 Récap : ordre des commandes (à copier-coller)

```bash
cd Downloads/DATAFIX-Streamlit
python -m venv .venv
.venv\Scripts\activate            # ou source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

C'est tout. Bonne projection 🍿
