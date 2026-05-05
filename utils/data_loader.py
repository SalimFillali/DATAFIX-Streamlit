"""Chargement du catalogue DATAFIX - comedies francaises post-1980, note >= 6.5."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Top 30 comedies francaises iconiques tirees du dataset officiel de l'equipe
# (dataset_comedies_1980_complet.csv - filtre : original_language=fr, year>=1980,
#  vote_average>=6.5, vote_count>=50, trie par popularite)
_SAMPLE_MOVIES = [
    (77338, "Intouchables", 2011, "Comedie Drame",
     "À la suite d'un accident de parapente, Philippe, riche aristocrate, engage Driss, un jeune de banlieue tout juste sorti de prison. Bref la personne la moins adaptée pour le job. Ensemble ils vont faire cohabiter Vivaldi et Earth Wind and Fire, le verbe et la vanne.",
     "/i97FM40bOMKvKIo3hjQviETE5yf.jpg", 8.3),
    (194, "Le Fabuleux Destin d'Amelie Poulain", 2001, "Comedie Romance",
     "Amélie, une jeune serveuse dans un bar de Montmartre, observe les gens et laisse son imagination divaguer. Elle s'est fixée un but : faire le bien de ceux qui l'entourent. Elle invente alors des stratagèmes pour intervenir incognito dans leur existence.",
     "/7dkCfOJ4rjEZNrNJQReht5od7aW.jpg", 7.9),
    (2899, "Asterix et Obelix : Mission Cleopatre", 2002, "Comedie Aventure Familial Fantastique",
     "Cléopâtre parie avec César qu'elle peut faire construire un palais somptueux en trois mois. Pour y parvenir, elle confie le projet à un architecte distrait qui appelle Astérix et Obélix à la rescousse, avec leur potion magique.",
     "/2lC9lzozlzVxCsSgPjRz5AWcz00.jpg", 7.4),
    (262391, "Qu'est-ce qu'on a fait au Bon Dieu ?", 2014, "Comedie",
     "Claude et Marie Verneuil, parents catholiques traditionnels, se sont toujours obligés à faire preuve d'ouverture d'esprit. Mais quand leurs quatre filles épousent successivement un musulman, un juif, un asiatique et un africain, leurs convictions sont mises à l'épreuve.",
     "/8OXNnKIHm3eJctx0y9KHMoKXOFw.jpg", 6.7),
    (74643, "The Artist", 2011, "Comedie Romance Drame",
     "Hollywood 1927. George Valentin est une vedette du cinéma muet à qui tout sourit. L'arrivée des films parlants va le faire sombrer dans l'oubli. Peppy Miller, jeune figurante, va elle être propulsée au firmament des stars.",
     "/khtVL4abxYczXAWbo1wAz13CLx3.jpg", 7.4),
    (382591, "Demain tout commence", 2016, "Comedie Drame",
     "Samuel vit sa vie sans attaches ni responsabilités, au bord de la mer dans le sud de la France. Jusqu'à ce qu'une de ses anciennes conquêtes lui laisse sur les bras un bébé de quelques mois, Gloria. Sa vie va basculer pour le meilleur et pour le rire.",
     "/1AoQQBmNRgOoavOeUisOPHKPDAF.jpg", 7.7),
    (2330, "Taxi", 1998, "Comedie Action Crime",
     "Daniel est un fou du volant. Cet ex-livreur de pizzas est aujourd'hui chauffeur de taxi à Marseille et sait échapper aux radars les plus perfectionnés. Pourtant un jour il croise la route d'Émilien, policier recalé pour la huitième fois à son permis de conduire.",
     "/5d16tJ2DLImAwCY2w0LYZjgWZA1.jpg", 6.7),
    (5528, "Les Choristes", 2004, "Musique Comedie Drame",
     "En 1949, Clément Mathieu, professeur de musique sans emploi, accepte un poste de surveillant dans un internat de rééducation pour mineurs. En initiant ces enfants difficiles à la musique et au chant choral, il va transformer leur quotidien gris en mélodies inoubliables.",
     "/kfWIeoVIBBxLQKhJ22LWYvcEgaP.jpg", 7.7),
    (8265, "Bienvenue chez les Ch'tis", 2008, "Comedie Romance Drame",
     "Philippe Abrams, directeur de la poste à Salon-de-Provence, est muté de force pour deux ans à Bergues, petite ville du Nord. Pour les Méridionaux le Nord c'est le froid, la pluie, et le Ch'ti incompréhensible.",
     "/dfht1lGq2ALbrRkMj35dUrj5kHG.jpg", 6.7),
    (304410, "La Famille Belier", 2014, "Musique Comedie Drame Familial",
     "Dans la famille Bélier tout le monde est sourd sauf Paula, 16 ans. Interprète indispensable pour ses parents au quotidien, elle découvre un don pour le chant et hésite : suivre son professeur à Paris ou rester à la ferme familiale ?",
     "/kAQeZUZ1pMTSjSF3d6eBZClFGgN.jpg", 6.9),
    (9421, "Le Diner de cons", 1998, "Comedie",
     "Tous les mercredis, Pierre Brochant et ses amis organisent un dîner où chacun doit amener un con. Ce soir Brochant exulte, il est sûr d'avoir trouvé la perle rare : François Pignon, comptable passionné de maquettes en allumettes. La soirée va virer au cauchemar.",
     "/7ukFDHExWul2Zz3L0OH8CaZCp2Z.jpg", 7.8),
    (11687, "Les Visiteurs", 1993, "Comedie Aventure Fantastique",
     "Le comte de Montmirail et son écuyer Jacquouille la Fripouille traversent les couloirs du temps et débarquent en plein 20e siècle. Confrontés à la modernité, ils tentent de comprendre cette époque étrange avec l'aide de leur descendante Béatrice.",
     "/aNBbenF2FXhBzJyFqtcToXuzoMg.jpg", 7.1),
    (262551, "Babysitting", 2014, "Comedie",
     "Faute de baby-sitter pour le week-end, Marc Schaudel confie son fils Rémy à Franck, son employé. Sauf que Franck a 30 ans ce soir et que Rémy est un sale gosse capricieux. Au petit matin, ses parents sont réveillés par un appel de la police.",
     "/lY5u3bvWXRk3KMrSoP0Sd3Ro5gW.jpg", 6.8),
    (8424, "Jeux d'enfants", 2003, "Comedie Romance Drame",
     "Sophie et Julien ont défini les règles du jeu. Cap ou pas cap ? Ils en sont, pour le restant de leurs vies, les arbitres et souvent les victimes. Bafouer tous les tabous, défier tous les interdits, braver tous les dangers de l'amour.",
     "/lFPxaXOPhIBumZCywpnudSusbzv.jpg", 7.2),
    (15152, "OSS 117 : Le Caire, nid d'espions", 2006, "Comedie Aventure Action Espionnage",
     "Égypte 1955, le Caire est un véritable nid d'espions. Hubert Bonisseur de La Bath, agent OSS 117, est envoyé en mission pour retrouver son ami disparu, démasquer une mystérieuse organisation et rétablir la paix au Moyen-Orient.",
     "/vxcqpokAB2bn2PzG3g4kFsL5h7V.jpg", 7.2),
    (112198, "Le Prenom", 2012, "Comedie",
     "Vincent, la quarantaine, va être père. Invité à dîner chez sa sœur et son beau-frère, il y retrouve un ami d'enfance. Quand on lui demande s'il a déjà choisi un prénom, sa réponse plonge la soirée dans le chaos.",
     "/w5JWQo7ArqmoegKYiQbv8TeAJmg.jpg", 7.3),
    (330764, "Le Tout Nouveau Testament", 2015, "Comedie Fantastique",
     "Dieu existe. Il habite à Bruxelles. Il est odieux avec sa femme et sa fille. On a beaucoup parlé de son fils, mais très peu de sa fille. Sa fille c'est moi. Je m'appelle Ea et j'ai dix ans. Pour me venger, j'ai balancé par SMS les dates de décès de tout le monde.",
     "/6kSeUr9GyR9ynuxEIQ1qbUYtkAy.jpg", 6.6),
    (48034, "Les Petits Mouchoirs", 2010, "Comedie Drame",
     "À la suite d'un événement bouleversant, une bande de copains décide malgré tout de partir en vacances au bord de la mer comme chaque année. Leur amitié, leurs certitudes, leur culpabilité, leurs amours en seront ébranlées.",
     "/qoHIdk4jZTwNjRz23ql3TO8yH9b.jpg", 7.1),
    (892, "Delicatessen", 1991, "Comedie Fantastique",
     "Au milieu d'un immense terrain vague, dans une banlieue hors du temps, se dresse un vieil immeuble. Il est habité par de drôles de gens qui n'ont qu'une préoccupation : se nourrir. Ils sont clients à la boucherie du rez-de-chaussée dont l'enseigne grince au vent.",
     "/oPlGvJFhDRYC5XrX2oqiwxTOoE8.jpg", 7.3),
    (484482, "Le Grand Bain", 2018, "Comedie Drame",
     "Bertrand, Marcus, Simon, Laurent, Thierry et les autres s'entraînent dans la piscine municipale sous l'autorité toute relative de Delphine, ancienne gloire des bassins. Ensemble ils décident de monter une équipe de natation synchronisée masculine.",
     "/tk781pgEMqRZpu0QNhxO7NGMJ6s.jpg", 6.9),
    (432068, "Le Sens de la fete", 2017, "Comedie",
     "Max est traiteur depuis 30 ans. Aujourd'hui c'est un sublime mariage dans un château du XVIIe siècle. Comme d'habitude, Max a tout coordonné. Mais la loi des séries va venir bousculer ses plans : personnel défaillant, photographe agaçant, beau-frère pénible.",
     "/6XVnhuZIZHWytsiu0GBK9nfzX9F.jpg", 7.0),
    (15588, "OSS 117 : Rio ne repond plus", 2009, "Comedie Action Espionnage",
     "Douze ans après Le Caire, OSS 117 est de retour pour une nouvelle mission à Rio. Lancé sur les traces d'un microfilm compromettant pour l'État français, le plus célèbre de nos agents va devoir faire équipe avec une lieutenant-colonel du Mossad.",
     "/sNL1aPGCMFmcnNDFWVUKehO3Vjr.jpg", 7.1),
    (393559, "Ma vie de courgette", 2016, "Comedie Animation Drame Familial",
     "Courgette n'a rien d'un légume, c'est un vaillant petit garçon. Il croit qu'il est seul au monde quand il perd sa mère. Mais c'est sans compter sur les rencontres qu'il va faire dans sa nouvelle vie au foyer pour enfants.",
     "/sDre2NQ5PYNagHww6bQTLO07MaS.jpg", 7.8),
    (170522, "Asterix : Le Domaine des dieux", 2014, "Comedie Animation Aventure Familial",
     "Pour en finir avec le village gaulois irréductible, César décide de bâtir à la place de la forêt voisine un grand ensemble résidentiel pour les Romains : Le Domaine des Dieux. Astérix et Obélix doivent contrer ce projet immobilier sournois.",
     "/lhB8cU7sHMy4ibKHVn67YcP4dI.jpg", 6.8),
    (487476, "Le Jeu", 2018, "Comedie Drame",
     "Le temps d'un dîner, des couples d'amis décident de jouer à un jeu : chacun doit poser son téléphone au milieu de la table et chaque SMS, appel, mail devra être partagé avec les autres. Les secrets vont voler en éclats.",
     "/cEYbEDrgKOtGVyO2c8R4zwXUVR0.jpg", 6.6),
    (2110, "Wasabi", 2001, "Comedie Action",
     "Flic solitaire au grand cœur mais aux méthodes musclées, l'inspecteur Hubert se retrouve en vacances forcées. Il reçoit alors un coup de fil d'un notaire japonais qui lui annonce que Miko, la femme de sa vie disparue vingt ans auparavant, vient de mourir.",
     "/7TbnpjIKzq5OKUyF72rcwNDyI5f.jpg", 6.7),
    (41211, "L'Arnacoeur", 2010, "Comedie Romance",
     "Alex est briseur de couples professionnel. Sa méthode : la séduction. Sa mission : transformer n'importe quel salaud en gros con cynique. Mais cette fois, la cible se nomme Juliette, et le pari va se compliquer pour le tombeur invétéré.",
     "/wNOFeAtXYD59NcBW09hfPEQwNJr.jpg", 6.6),
    (77459, "Un monstre a Paris", 2011, "Comedie Aventure Animation Fantastique Familial",
     "Dans le Paris inondé de 1910, un monstre sème la panique. Traqué sans relâche par le redoutable préfet Maynott, il demeure introuvable. Et si la meilleure cachette était sous les feux du cabaret L'Oiseau Rare où chante Lucille ?",
     "/iTb2Io2UaZCYVwzxwTYBVveN44l.jpg", 6.9),
    (15097, "La Cite de la peur", 1994, "Comedie",
     "Lors du festival de Cannes 1993, Odile Deray, petite attachée de presse, peine à intéresser les professionnels à son film Red is Dead, navet d'horreur. Mais quand un tueur reproduit les meurtres du film en assassinant les projectionnistes, l'acteur principal devient la prochaine cible.",
     "/jBzDbxsEiCUCiYcpDLpvbQ6kN2U.jpg", 7.5),
    (21861, "LOL (Laughing Out Loud)", 2009, "Comedie Romance",
     "Lola, surnommée LOL par ses amis, n'a pas le cœur à rire le jour de la rentrée. Arthur, son copain, la provoque en lui disant qu'il l'a trompée pendant l'été. Entre amours, mensonges et complications familiales, c'est l'adolescence dans toute sa splendeur.",
     "/mA5TBNiSK1JeLIqGgqYSfTcTHIq.jpg", 6.5),
]


def _build_sample_dataframe():
    return pd.DataFrame(
        _SAMPLE_MOVIES,
        columns=["tmdb_id", "title", "year", "genres", "overview", "poster_path", "vote_average"],
    )


@st.cache_data(show_spinner="Chargement du catalogue de comedies francaises...")
def load_movies(min_rating=6.5, after_year=1980):
    """Charge le catalogue : real data si dispo, sinon sample."""
    real_csv = DATA_DIR / "movies_final.csv"
    if real_csv.exists():
        df = pd.read_csv(real_csv)
        keep = [c for c in [
            "tmdb_id", "title", "year", "genres",
            "overview", "poster_path", "vote_average", "vote_count",
        ] if c in df.columns]
        df = df[keep]
        if "vote_average" in df.columns:
            df = df[df["vote_average"].fillna(0) >= min_rating]
        if "year" in df.columns:
            df = df[pd.to_numeric(df["year"], errors="coerce") >= after_year]
        if "genres" in df.columns:
            df = df[df["genres"].astype(str).str.contains("Com", case=False, na=False)]
        return df.reset_index(drop=True)
    return _build_sample_dataframe()


def get_genre_list(df):
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
