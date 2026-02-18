import streamlit as st
import google.generativeai as genai
import random
import time
from datetime import date

# ==========================================
# 0. CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Simulateur Parcoursup 2025",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. CSS PROFESSIONNEL
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

:root {
    --parcoursup-bleu:   #003189;
    --parcoursup-rouge:  #E1000F;
    --parcoursup-clair:  #EEF2FF;
    --bleu-fonce:        #001a4d;
    --bleu-moyen:        #1B4FBB;
    --bleu-accent:       #4B7BF5;
    --vert-ok:           #00875A;
    --vert-clair:        #E3FFF3;
    --orange-attente:    #D97706;
    --orange-clair:      #FFF8E6;
    --rouge-refus:       #C0000A;
    --rouge-clair:       #FFF0F0;
    --gris-fond:         #F4F6FA;
    --gris-bord:         #DDE3EF;
    --gris-texte:        #5A6478;
    --blanc:             #FFFFFF;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background: var(--gris-fond) !important;
}

/* ---- En-tête hero ---- */
.hero-header {
    background: linear-gradient(135deg, var(--bleu-fonce) 0%, var(--parcoursup-bleu) 60%, var(--bleu-moyen) 100%);
    padding: 1.8rem 2rem 1.4rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 280px; height: 280px;
    background: rgba(255,255,255,0.03);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    color: white !important;
    margin: 0 !important;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.72);
    margin-top: 4px;
    font-weight: 400;
    letter-spacing: 0.02em;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    color: white;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: var(--bleu-fonce) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    border-bottom: 1px solid rgba(255,255,255,0.12) !important;
    padding-bottom: 0.4rem !important;
    margin-top: 1.2rem !important;
}
[data-testid="stSidebar"] .stSelectbox > div,
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stNumberInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: white !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
}

/* ---- Cards ---- */
.card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    border: 1px solid var(--gris-bord);
    box-shadow: 0 2px 10px rgba(0,30,100,0.06);
    margin-bottom: 0.8rem;
}
.card-oui {
    border-left: 5px solid var(--vert-ok) !important;
    background: var(--vert-clair) !important;
}
.card-attente {
    border-left: 5px solid var(--orange-attente) !important;
    background: var(--orange-clair) !important;
}
.card-non {
    border-left: 5px solid var(--rouge-refus) !important;
    background: var(--rouge-clair) !important;
}
.card-accepte {
    border-left: 5px solid var(--parcoursup-bleu) !important;
    background: var(--parcoursup-clair) !important;
    border: 2px solid var(--parcoursup-bleu) !important;
}

/* ---- Étiquettes statut ---- */
.badge-oui {
    background: var(--vert-ok); color: white;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    display: inline-block;
}
.badge-oui-si {
    background: #2563EB; color: white;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    display: inline-block;
}
.badge-attente {
    background: var(--orange-attente); color: white;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    display: inline-block;
}
.badge-non {
    background: var(--rouge-refus); color: white;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    display: inline-block;
}
.badge-choisi {
    background: var(--parcoursup-bleu); color: white;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700;
    display: inline-block;
}

/* ---- Section title ---- */
.section-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    color: var(--bleu-fonce) !important;
    border-bottom: 2px solid var(--parcoursup-bleu);
    padding-bottom: 0.4rem;
    margin-bottom: 1rem !important;
}

/* ---- Calendrier ---- */
.cal-item {
    background: white;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    border: 1px solid var(--gris-bord);
    margin-bottom: 6px;
    font-size: 0.85rem;
}
.cal-active {
    background: var(--parcoursup-clair);
    border: 2px solid var(--parcoursup-bleu);
    font-weight: 600;
}

/* ---- Boutons ---- */
button[data-testid="baseButton-primary"],
.stButton > button[kind="primary"] {
    background: var(--parcoursup-bleu) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    box-shadow: 0 3px 12px rgba(0,49,137,0.25) !important;
    transition: all 0.2s !important;
}
button[data-testid="baseButton-primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 18px rgba(0,49,137,0.35) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1.5px solid var(--gris-bord) !important;
    color: var(--gris-texte) !important;
    border-radius: 8px !important;
}

/* ---- Progress bar ---- */
.stProgress > div > div {
    background: var(--parcoursup-bleu) !important;
    border-radius: 4px !important;
}

/* ---- Inputs ---- */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    border-radius: 8px !important;
    border: 1.5px solid var(--gris-bord) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ---- Voeu panel ---- */
.voeu-item {
    background: white;
    border: 1px solid var(--gris-bord);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.88rem;
}
.voeu-numero {
    background: var(--parcoursup-bleu);
    color: white;
    border-radius: 50%;
    width: 24px; height: 24px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 700;
    flex-shrink: 0;
}

/* ---- Score profil ---- */
.score-chip {
    background: var(--parcoursup-clair);
    border: 1px solid var(--parcoursup-bleu);
    color: var(--parcoursup-bleu);
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    margin: 2px;
}

/* ---- Alerte règle ---- */
.alerte-regle {
    background: #FFF8E6;
    border: 1px solid #F59E0B;
    border-left: 4px solid #F59E0B;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}

/* ---- Tabs ---- */
.stTabs [data-baseweb="tab-list"] {
    background: var(--gris-bord) !important;
    border-radius: 10px !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    color: var(--gris-texte) !important;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: var(--parcoursup-bleu) !important;
    font-weight: 700 !important;
}

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: var(--bleu-accent); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. GEMINI API
# ==========================================
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    GEMINI_OK = True
except:
    GEMINI_OK = False

# ==========================================
# 3. CATALOGUE FORMATIONS 2025
# ==========================================
CATALOGUE = {

    # ============================================================
    # RÉUNION — LICENCES
    # ============================================================
    "Licence Droit — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Droit & Sciences Po",
        "selectivite": "Modérée", "profil_ideal": "TB en Histoire-Géo, Philo, Français",
        "debouches": "Avocat, Magistrat, Notaire, Juriste d'entreprise", "capacite": 280, "taux_acces": 62
    },
    "Licence Psychologie — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Sciences Humaines",
        "selectivite": "Élevée", "profil_ideal": "SVT, Philo, SES. Bonne moyenne générale",
        "debouches": "Psychologue, RH, Éducateur spécialisé", "capacite": 120, "taux_acces": 38
    },
    "Licence Sociologie — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Sciences Humaines",
        "selectivite": "Faible", "profil_ideal": "SES, HGGSP, ouverture aux sciences sociales",
        "debouches": "Chargé d'études, Animateur socioculturel, Travailleur social", "capacite": 150, "taux_acces": 72
    },
    "Licence Histoire — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Lettres & Sciences Humaines",
        "selectivite": "Faible", "profil_ideal": "Passion pour l'histoire, HGGSP, Humanités",
        "debouches": "Enseignant, Archiviste, Journaliste, Musées", "capacite": 130, "taux_acces": 75
    },
    "Licence Géographie & Aménagement — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Sciences Humaines",
        "selectivite": "Faible", "profil_ideal": "HGGSP, curiosité environnementale et territoriale",
        "debouches": "Urbaniste, Cartographe, Géomaticien, Aménagement du territoire", "capacite": 100, "taux_acces": 78
    },
    "Licence LLCER Anglais — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Lettres & Langues",
        "selectivite": "Faible", "profil_ideal": "Excellent niveau en anglais, LLCE ou LV1/LV2",
        "debouches": "Traducteur, Enseignant, Commerce international", "capacite": 90, "taux_acces": 80
    },
    "Licence Lettres Modernes — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Lettres & Langues",
        "selectivite": "Faible", "profil_ideal": "Humanités, Français, passion littérature",
        "debouches": "Enseignant, Journaliste, Edition, Communication", "capacite": 100, "taux_acces": 80
    },
    "Licence Sciences de l'Éducation — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Sciences Humaines",
        "selectivite": "Faible", "profil_ideal": "Goût pour la pédagogie, SES ou Philo",
        "debouches": "Formateur, Conseiller pédagogique, Éducateur", "capacite": 120, "taux_acces": 74
    },
    "Licence AES (Administration Économique et Sociale) — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Économie & Gestion",
        "selectivite": "Faible", "profil_ideal": "SES, profil polyvalent gestion/social",
        "debouches": "Ressources Humaines, Administration, Travail social", "capacite": 140, "taux_acces": 73
    },
    "Licence Économie-Gestion — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Économie & Gestion",
        "selectivite": "Modérée", "profil_ideal": "SES + Maths. Esprit analytique",
        "debouches": "Économiste, Contrôleur de gestion, Analyste", "capacite": 200, "taux_acces": 60
    },
    "Licence STAPS — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Sport & Santé",
        "selectivite": "Modérée", "profil_ideal": "Pratique sportive régulière, SVT",
        "debouches": "Professeur EPS, Kinésithérapeute, Coach sportif", "capacite": 180, "taux_acces": 55
    },
    "Licence Biologie — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Sciences",
        "selectivite": "Modérée", "profil_ideal": "SVT + Maths ou PC. Solide en sciences",
        "debouches": "Chercheur, Biologiste, Industrie pharmaceutique", "capacite": 160, "taux_acces": 58
    },
    "Licence Chimie — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Sciences",
        "selectivite": "Modérée", "profil_ideal": "Physique-Chimie + Maths obligatoires",
        "debouches": "Chimiste, Ingénieur procédés, Cosmétique, Agroalimentaire", "capacite": 90, "taux_acces": 60
    },
    "Licence Physique — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Sciences",
        "selectivite": "Modérée", "profil_ideal": "Maths + Physique-Chimie solides",
        "debouches": "Ingénieur, Chercheur, Enseignant", "capacite": 80, "taux_acces": 58
    },
    "Licence Informatique — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Numérique & Informatique",
        "selectivite": "Modérée", "profil_ideal": "Maths + NSI très appréciés",
        "debouches": "Développeur, Data Scientist, Ingénieur logiciel", "capacite": 100, "taux_acces": 52
    },
    "Licence Mathématiques — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Sciences",
        "selectivite": "Modérée", "profil_ideal": "Excellent en Maths, rigueur analytique",
        "debouches": "Enseignant, Actuaire, Data Analyst, Finance", "capacite": 80, "taux_acces": 55
    },

    # ============================================================
    # RÉUNION — BTS
    # ============================================================
    "BTS MCO (Management Commercial Opérationnel) — Lycée Bellepierre": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Commerce & Gestion",
        "selectivite": "Faible", "profil_ideal": "Bac STMG ou général, sens commercial",
        "debouches": "Manager commercial, Responsable rayon, Entrepreneur", "capacite": 60, "taux_acces": 78
    },
    "BTS NDRC (Négociation et Digitalisation Relation Client) — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "multiple",
        "sous_voeux": [
            "BTS NDRC — Lycée Bellepierre (St-Denis)",
            "BTS NDRC — Lycée Ambroise Vollard (St-Pierre)",
        ],
        "domaine": "Commerce & Gestion",
        "selectivite": "Faible", "profil_ideal": "Commercial, digital, relation client",
        "debouches": "Commercial B2B, Téléconseiller, Business Developer", "capacite": 60, "taux_acces": 76
    },
    "BTS Comptabilité et Gestion (CG) — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "multiple",
        "sous_voeux": [
            "BTS CG — Lycée Leconte de Lisle (St-Denis)",
            "BTS CG — Lycée Ambroise Vollard (St-Pierre)",
            "BTS CG — Lycée Mahatma Gandhi (St-André)"
        ],
        "domaine": "Commerce & Gestion",
        "selectivite": "Faible", "profil_ideal": "STMG ou général, rigueur, goût chiffres",
        "debouches": "Comptable, Assistant de gestion, Contrôleur", "capacite": 54, "taux_acces": 77
    },
    "BTS SAM (Support à l'Action Managériale) — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "multiple",
        "sous_voeux": [
            "BTS SAM — Lycée Le Verger (Ste-Marie)",
            "BTS SAM — Lycée Bellepierre (St-Denis)"
        ],
        "domaine": "Commerce & Gestion",
        "selectivite": "Faible", "profil_ideal": "Organisation, communication, bureautique",
        "debouches": "Assistant de direction, Office Manager", "capacite": 48, "taux_acces": 80
    },
    "BTS SIO (Services Informatiques aux Organisations) — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "multiple",
        "sous_voeux": [
            "BTS SIO SLAM — Lycée Roland Garros (Le Tampon)",
            "BTS SIO SISR — Lycée Roland Garros (Le Tampon)",
            "BTS SIO SLAM — Lycée Leconte de Lisle (St-Denis)"
        ],
        "domaine": "Numérique & Informatique",
        "selectivite": "Faible", "profil_ideal": "NSI, Maths, curiosité informatique",
        "debouches": "Développeur, Technicien réseau, Admin systèmes", "capacite": 48, "taux_acces": 80
    },
    "BTS SNIR (Systèmes Numériques, Informatique et Réseaux) — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Numérique & Informatique",
        "selectivite": "Faible", "profil_ideal": "STI2D, Maths, Sciences de l'ingénieur",
        "debouches": "Technicien réseaux, Électronicien, Maintenance", "capacite": 36, "taux_acces": 82
    },
    "BTS GPME (Gestion PME) — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Commerce & Gestion",
        "selectivite": "Faible", "profil_ideal": "Polyvalence gestion, STMG ou général",
        "debouches": "Assistant PME, Gestionnaire administratif", "capacite": 48, "taux_acces": 79
    },
    "BTS Tourisme — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Tourisme & Hôtellerie",
        "selectivite": "Faible", "profil_ideal": "Langues vivantes, sens de l'accueil, culture générale",
        "debouches": "Agent de voyage, Responsable tourisme, Guide", "capacite": 36, "taux_acces": 75
    },
    "BTS Hôtellerie-Restauration — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Tourisme & Hôtellerie",
        "selectivite": "Faible", "profil_ideal": "Passion cuisine/service, dynamisme",
        "debouches": "Chef cuisinier, Responsable salle, Directeur hôtel", "capacite": 48, "taux_acces": 74
    },
    "BTS ESF (Économie Sociale et Familiale) — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Social & Santé",
        "selectivite": "Faible", "profil_ideal": "ST2S, sens du social, empathie",
        "debouches": "Conseiller ESF, CCAS, CAF, associations", "capacite": 30, "taux_acces": 76
    },
    "BTS Professions Immobilières — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Commerce & Gestion",
        "selectivite": "Faible", "profil_ideal": "Droit, SES, sens commercial",
        "debouches": "Agent immobilier, Gestionnaire de biens", "capacite": 36, "taux_acces": 77
    },
    "BTS Communication — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Communication & Média",
        "selectivite": "Modérée", "profil_ideal": "Créativité, Français, culture digitale",
        "debouches": "Chargé de communication, Community manager", "capacite": 30, "taux_acces": 58
    },
    "BTS Diététique — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Social & Santé",
        "selectivite": "Élevée", "profil_ideal": "SVT + Chimie, passion alimentation/santé",
        "debouches": "Diététicien(ne), Nutritionniste, Conseil en entreprise", "capacite": 24, "taux_acces": 40
    },
    "BTS Analyse de Biologie Médicale — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Social & Santé",
        "selectivite": "Élevée", "profil_ideal": "SVT + Chimie. Rigueur scientifique",
        "debouches": "Technicien de laboratoire médical", "capacite": 24, "taux_acces": 35
    },

    # ============================================================
    # RÉUNION — BUT (Bachelor Universitaire de Technologie)
    # ============================================================
    "BUT Techniques de Commercialisation — IUT de St-Pierre": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Commerce & Gestion",
        "selectivite": "Modérée", "profil_ideal": "Maths + SES, esprit analytique, moyenne ≥ 12",
        "debouches": "Chef de projet marketing, Commercial B2B, Data analyst marketing", "capacite": 72, "taux_acces": 50
    },
    "BUT Génie Civil — IUT de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Sciences & Ingénierie",
        "selectivite": "Modérée", "profil_ideal": "Maths + PC ou SI. STI2D bienvenu",
        "debouches": "Ingénieur BTP, Conducteur de travaux, Urbanisme", "capacite": 60, "taux_acces": 52
    },
    "BUT Réseaux & Télécommunications — IUT de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Numérique & Informatique",
        "selectivite": "Modérée", "profil_ideal": "Maths + NSI ou STI2D, curiosité technique",
        "debouches": "Ingénieur réseau, Administrateur système, Cybersécurité", "capacite": 48, "taux_acces": 54
    },
    "BUT Informatique — IUT de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Numérique & Informatique",
        "selectivite": "Modérée", "profil_ideal": "Maths + NSI. Logique algorithmique",
        "debouches": "Développeur full-stack, Data Scientist, Ingénieur IA", "capacite": 60, "taux_acces": 50
    },
    "BUT Gestion des Entreprises et Administration (GEA) — IUT Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Commerce & Gestion",
        "selectivite": "Modérée", "profil_ideal": "SES + Maths, esprit de gestion",
        "debouches": "Contrôleur de gestion, Responsable comptable, RH", "capacite": 60, "taux_acces": 55
    },
    "BUT Carrières Sociales — IUT de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Social & Santé",
        "selectivite": "Modérée", "profil_ideal": "Goût pour le social, empathie, SES",
        "debouches": "Éducateur spécialisé, Assistant social, Animateur", "capacite": 48, "taux_acces": 48
    },

    # ============================================================
    # RÉUNION — FORMATIONS PARAMÉDICALES & SOCIALES
    # ============================================================
    "IFSI Soins Infirmiers — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "multiple",
        "sous_voeux": [
            "IFSI — CHU Nord (St-Denis)",
            "IFSI — CHU Sud (St-Pierre)"
        ],
        "domaine": "Social & Santé",
        "selectivite": "Élevée", "profil_ideal": "SVT, sens du soin, bonne communication, résistance au stress",
        "debouches": "Infirmier(e) hospitalier, libéral, spécialisé (IADE, IBODE)", "capacite": 80, "taux_acces": 30
    },
    "Formation Aide-Soignant(e) — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "multiple",
        "sous_voeux": [
            "IFAS — CHU Nord (St-Denis)",
            "IFAS — CHU Sud (St-Pierre)",
            "IFAS — Clinique Jeanne d'Arc"
        ],
        "domaine": "Social & Santé",
        "selectivite": "Modérée", "profil_ideal": "Empathie, ST2S apprécié, motivation pour le soin",
        "debouches": "Aide-soignant(e) en EHPAD, hôpital, domicile", "capacite": 100, "taux_acces": 45
    },
    "BTS SP3S (Services et Prestations des Secteurs Sanitaire et Social)": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Social & Santé",
        "selectivite": "Faible", "profil_ideal": "ST2S, sens du social et de l'organisation",
        "debouches": "Coordinateur secteur médico-social, Gestionnaire EHPAD", "capacite": 36, "taux_acces": 72
    },
    "BPJEPS Animation — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Sport & Social",
        "selectivite": "Faible", "profil_ideal": "Dynamisme, sens de l'animation, BAFA apprécié",
        "debouches": "Animateur socioculturel, Responsable structure jeunesse", "capacite": 40, "taux_acces": 75
    },

    # ============================================================
    # RÉUNION — CPGE
    # ============================================================
    "CPGE Scientifique — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "multiple",
        "sous_voeux": [
            "MPSI — Lycée Leconte de Lisle (St-Denis)",
            "PCSI — Lycée Leconte de Lisle (St-Denis)",
            "PCSI — Lycée Roland Garros (Le Tampon)",
            "MP2I — Lycée Leconte de Lisle (St-Denis)"
        ],
        "domaine": "Classes Préparatoires",
        "selectivite": "Très élevée", "profil_ideal": "TB ou B en Maths + PC. Moyenne ≥ 15. Mention TB conseillée",
        "debouches": "Grandes Écoles d'Ingénieurs (CentraleSupélec, Mines, Ponts...)", "capacite": 35, "taux_acces": 22
    },
    "CPGE Économique et Commerciale (ECG) — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "multiple",
        "sous_voeux": [
            "ECG — Lycée Leconte de Lisle (St-Denis)",
            "ECG — Lycée Roland Garros (Le Tampon)"
        ],
        "domaine": "Classes Préparatoires",
        "selectivite": "Très élevée", "profil_ideal": "Maths + SES ou Histoire. Profil polyvalent. Mention TB",
        "debouches": "HEC, ESSEC, EM Lyon, Grandes Écoles de Commerce", "capacite": 30, "taux_acces": 25
    },

    # ============================================================
    # RÉUNION — DIVERS
    # ============================================================
    "École d'Architecture de La Réunion (ENSA)": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Arts & Architecture",
        "selectivite": "Élevée", "profil_ideal": "Arts plastiques, Maths, portfolio requis",
        "debouches": "Architecte DPLG, Urbaniste, Designer d'espace", "capacite": 60, "taux_acces": 35
    },
    "Formation Éducateur Spécialisé — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Social & Santé",
        "selectivite": "Modérée", "profil_ideal": "Empathie, résistance, engagement social",
        "debouches": "Éducateur spécialisé en IME, ITEP, protection de l'enfance", "capacite": 50, "taux_acces": 42
    },

    # ============================================================
    # MÉTROPOLE — LICENCES
    # ============================================================
    "Licence Droit — Université Paris Panthéon-Assas (Paris 2)": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Droit & Sciences Po",
        "selectivite": "Élevée", "profil_ideal": "Mention TB recommandée. Excellents résultats",
        "debouches": "Avocat, Magistrat, Notaire (Paris)", "capacite": 350, "taux_acces": 40
    },
    "Licence Droit — Université de Bordeaux": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Droit & Sciences Po",
        "selectivite": "Modérée", "profil_ideal": "TB en Histoire, Philo. Rédaction soignée",
        "debouches": "Avocat, Juriste, Notaire, Fonctionnaire catégorie A", "capacite": 400, "taux_acces": 55
    },
    "Licence Psychologie — Université Lyon 2 Lumière": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Sciences Humaines",
        "selectivite": "Élevée", "profil_ideal": "SVT + Philo + SES. Dossier très sélectif",
        "debouches": "Psychologue clinicien, scolaire, du travail", "capacite": 200, "taux_acces": 35
    },
    "Licence Psychologie — Université Rennes 2": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Sciences Humaines",
        "selectivite": "Élevée", "profil_ideal": "SVT + Philo, motivation pour la clinique",
        "debouches": "Psychologue, Neuropsychologue, Chargé d'insertion", "capacite": 180, "taux_acces": 37
    },
    "Licence STAPS — Université de Montpellier": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Sport & Santé",
        "selectivite": "Modérée", "profil_ideal": "Pratique sportive de haut niveau souhaitée, SVT",
        "debouches": "Entraîneur, Kinésithérapeute, Préparateur physique", "capacite": 250, "taux_acces": 52
    },
    "Licence Informatique — Université de Bordeaux": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Numérique & Informatique",
        "selectivite": "Modérée", "profil_ideal": "Maths + NSI obligatoires. Logique algorithmique",
        "debouches": "Développeur, Data Scientist, Ingénieur IA", "capacite": 160, "taux_acces": 48
    },
    "Licence Informatique — Université Paris Cité": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Numérique & Informatique",
        "selectivite": "Élevée", "profil_ideal": "Excellent en Maths + NSI. Paris très sélectif",
        "debouches": "Développeur, Chercheur, Ingénieur IA, Data Engineer", "capacite": 120, "taux_acces": 38
    },
    "Licence Mathématiques — Université de Paris-Saclay": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Sciences",
        "selectivite": "Très élevée", "profil_ideal": "Niveau d'excellence en Maths. Mention TB exigée",
        "debouches": "Recherche, Finance quantitative, Actuaire, Data Science", "capacite": 150, "taux_acces": 25
    },
    "Licence Physique-Chimie — Université de Strasbourg": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Sciences",
        "selectivite": "Modérée", "profil_ideal": "PC + Maths indispensables",
        "debouches": "Ingénieur, Chercheur, Chimiste industriel", "capacite": 160, "taux_acces": 50
    },
    "Licence SVT — Université Claude Bernard Lyon 1": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Sciences",
        "selectivite": "Modérée", "profil_ideal": "SVT + Maths ou PC. Projet scientifique clair",
        "debouches": "Enseignant, Chercheur, Environnement, Médecine (passerelle)", "capacite": 200, "taux_acces": 55
    },
    "Licence SES — Université Paris 1 Panthéon-Sorbonne": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Économie & Gestion",
        "selectivite": "Élevée", "profil_ideal": "SES + Maths. Profil analytique. Sorbonne très sélective",
        "debouches": "Économiste, Chargé d'études, Finance, Recherche", "capacite": 250, "taux_acces": 38
    },
    "Licence AES — Université de Nantes": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Économie & Gestion",
        "selectivite": "Faible", "profil_ideal": "Profil polyvalent, goût gestion et social",
        "debouches": "RH, Administration, Travail social, Collectivités", "capacite": 220, "taux_acces": 68
    },
    "Licence Histoire — Université de Bordeaux Montaigne": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Lettres & Sciences Humaines",
        "selectivite": "Faible", "profil_ideal": "Passion pour l'histoire, HGGSP, culture générale",
        "debouches": "Enseignant, Journaliste, Patrimoine, Archiviste", "capacite": 250, "taux_acces": 72
    },
    "Licence Géographie — Université de Toulouse Jean Jaurès": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Sciences Humaines",
        "selectivite": "Faible", "profil_ideal": "HGGSP, curiosité pour l'environnement et les territoires",
        "debouches": "Urbaniste, Géomaticien, Aménagement territorial", "capacite": 200, "taux_acces": 70
    },

    # ============================================================
    # MÉTROPOLE — BTS & BUT
    # ============================================================
    "BUT Informatique — IUT Paris-Rives de Seine": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Numérique & Informatique",
        "selectivite": "Élevée", "profil_ideal": "Maths + NSI. Très sélectif à Paris",
        "debouches": "Développeur, DevOps, Chef de projet SI", "capacite": 80, "taux_acces": 30
    },
    "BUT Informatique — IUT de Bordeaux": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Numérique & Informatique",
        "selectivite": "Modérée", "profil_ideal": "Maths + NSI appréciés",
        "debouches": "Développeur, Data Engineer, Chef de projet numérique", "capacite": 100, "taux_acces": 48
    },
    "BUT MMI (Métiers Multimédias et Internet) — France": {
        "zone": "🇫🇷 Métropole", "type": "multiple",
        "sous_voeux": [
            "BUT MMI — IUT Bordeaux Montaigne",
            "BUT MMI — IUT Nancy-Charlemagne",
            "BUT MMI — IUT de Tours",
            "BUT MMI — IUT de Troyes"
        ],
        "domaine": "Communication & Média",
        "selectivite": "Modérée", "profil_ideal": "Créativité + maîtrise digitale + curiosité web",
        "debouches": "Développeur web, UX Designer, Community manager, Journaliste numérique", "capacite": 90, "taux_acces": 45
    },
    "BTS Communication — Métropole": {
        "zone": "🇫🇷 Métropole", "type": "multiple",
        "sous_voeux": [
            "BTS Communication — Lycée Dorian (Paris)",
            "BTS Communication — Lycée Fresnel (Paris)",
            "BTS Communication — Lycée Émile Zola (Rennes)"
        ],
        "domaine": "Communication & Média",
        "selectivite": "Modérée", "profil_ideal": "Créativité, Français, culture digitale, dossier artistique",
        "debouches": "Chargé de communication, Community manager, Publicitaire", "capacite": 35, "taux_acces": 45
    },
    "BTS Design Graphique — Métropole": {
        "zone": "🇫🇷 Métropole", "type": "multiple",
        "sous_voeux": [
            "BTS Design Graphique — ESAIP (Paris)",
            "BTS Design Graphique — Lycée des Métiers d'Art (Lyon)",
            "BTS Design Graphique — Lycée Touchard (Le Mans)"
        ],
        "domaine": "Arts & Architecture",
        "selectivite": "Élevée", "profil_ideal": "Portfolio requis. Arts plastiques. Maîtrise logiciels graphiques",
        "debouches": "Graphiste, Directeur artistique, Motion designer", "capacite": 30, "taux_acces": 32
    },

    # ============================================================
    # MÉTROPOLE — CPGE & GRANDES ÉCOLES
    # ============================================================
    "CPGE Scientifique (MPSI/PCSI/MP2I) — Paris & IDF": {
        "zone": "🇫🇷 Métropole", "type": "multiple",
        "sous_voeux": [
            "MPSI — Lycée Louis-le-Grand (Paris)",
            "MPSI — Lycée Pierre de Fermat (Toulouse)",
            "PCSI — Lycée Chaptal (Paris)",
            "MP2I — Lycée Carnot (Paris)",
            "MPSI — Lycée Kléber (Strasbourg)"
        ],
        "domaine": "Classes Préparatoires",
        "selectivite": "Très élevée", "profil_ideal": "Mention TB exigée. Excellence en Maths + PC. Classement top 5%",
        "debouches": "Polytechnique, CentraleSupélec, Mines ParisTech, Ponts", "capacite": 48, "taux_acces": 15
    },
    "CPGE Économique et Commerciale (ECG) — Métropole": {
        "zone": "🇫🇷 Métropole", "type": "multiple",
        "sous_voeux": [
            "ECG — Lycée Henri IV (Paris)",
            "ECG — Lycée Carnot (Paris)",
            "ECG — Lycée Thiers (Marseille)",
            "ECG — Lycée du Parc (Lyon)"
        ],
        "domaine": "Classes Préparatoires",
        "selectivite": "Très élevée", "profil_ideal": "Maths + SES ou Histoire. Polyvalence. Mention TB",
        "debouches": "HEC Paris, ESSEC, ESCP, EM Lyon, Audencia", "capacite": 45, "taux_acces": 18
    },
    "CPGE Littéraire (AL/BL) — Métropole": {
        "zone": "🇫🇷 Métropole", "type": "multiple",
        "sous_voeux": [
            "AL — Lycée Henri IV (Paris)",
            "AL — Lycée Fénelon (Paris)",
            "AL — Lycée Lakanal (Sceaux)",
            "BL — Lycée Hoche (Versailles)",
            "AL — Lycée Chaptal (Paris)"
        ],
        "domaine": "Classes Préparatoires",
        "selectivite": "Très élevée", "profil_ideal": "TB en Lettres, Philo, Langues. Mention TB absolument nécessaire",
        "debouches": "ENS Ulm, ENS Lyon, Sciences Po Paris, Hautes fonctions publiques", "capacite": 40, "taux_acces": 18
    },
    "Sciences Po — Réseau IEP (Concours Commun)": {
        "zone": "🇫🇷 Métropole", "type": "multiple",
        "sous_voeux": [
            "IEP Sciences Po Lille",
            "IEP Sciences Po Lyon",
            "IEP Sciences Po Rennes",
            "IEP Sciences Po Toulouse",
            "IEP Sciences Po Grenoble",
            "IEP Sciences Po Aix-en-Provence"
        ],
        "domaine": "Droit & Sciences Po",
        "selectivite": "Très élevée", "profil_ideal": "Profil polyvalent, culture générale excellente, SES + Histoire",
        "debouches": "Diplomatie, Hauts fonctionnaires, Journalisme, ONG, Conseil", "capacite": 300, "taux_acces": 20
    },
    "Sciences Po Paris — Procédure Lycées Conventionnés": {
        "zone": "🇫🇷 Métropole", "type": "simple", "sous_voeux": [], "domaine": "Droit & Sciences Po",
        "selectivite": "Très élevée", "profil_ideal": "Dossier exceptionnel, engagement citoyen, entretien de motivation",
        "debouches": "Diplomatie, Cabinet ministériel, Conseil, Finance internationale", "capacite": 100, "taux_acces": 12
    },
    "Écoles d'Ingénieurs (Concours Geipi Polytech)": {
        "zone": "🇫🇷 Métropole", "type": "multiple",
        "sous_voeux": [
            "Polytech Lyon", "Polytech Nantes",
            "Polytech Montpellier", "Polytech Lille",
            "Polytech Nice Sophia", "Polytech Clermont"
        ],
        "domaine": "Sciences & Ingénierie",
        "selectivite": "Modérée", "profil_ideal": "Maths + Physique-Chimie. Moyenne ≥ 13",
        "debouches": "Ingénieur dans tous secteurs (industrie, numérique, énergie, BTP)", "capacite": 200, "taux_acces": 52
    },

    # ============================================================
    # MÉTROPOLE — SANTÉ
    # ============================================================
    "PASS (Parcours Accès Santé Spécifique) — Médecine/Pharmacie": {
        "zone": "🇫🇷 Métropole", "type": "multiple",
        "sous_voeux": [
            "PASS — Université Paris Cité",
            "PASS — Université de Bordeaux",
            "PASS — Université de Lyon 1",
            "PASS — Université de Montpellier",
            "PASS — Université de Strasbourg",
            "PASS — Université de Nantes"
        ],
        "domaine": "Social & Santé",
        "selectivite": "Très élevée", "profil_ideal": "Excellence absolue en SVT + PC + Maths. Mention TB exigée. Travail acharné",
        "debouches": "Médecin, Pharmacien, Chirurgien-dentiste, Sage-femme", "capacite": 150, "taux_acces": 18
    },
    "PASS — Université de La Réunion": {
        "zone": "🇷🇪 Réunion", "type": "simple", "sous_voeux": [], "domaine": "Social & Santé",
        "selectivite": "Très élevée", "profil_ideal": "SVT + PC + Maths. Mention TB indispensable. Travail intense",
        "debouches": "Médecin, Pharmacien, Chirurgien-dentiste, Sage-femme", "capacite": 80, "taux_acces": 20
    },
    "L.AS (Licence Accès Santé) — Réunion": {
        "zone": "🇷🇪 Réunion", "type": "multiple",
        "sous_voeux": [
            "L.AS Biologie — Université de La Réunion",
            "L.AS STAPS — Université de La Réunion",
            "L.AS Chimie — Université de La Réunion"
        ],
        "domaine": "Social & Santé",
        "selectivite": "Très élevée", "profil_ideal": "Voie alternative au PASS, même niveau d'exigence scientifique",
        "debouches": "Médecin, Pharmacien, Kinésithérapeute, Sage-femme", "capacite": 40, "taux_acces": 22
    },
    "IFMK (Kinésithérapie) — Métropole": {
        "zone": "🇫🇷 Métropole", "type": "multiple",
        "sous_voeux": [
            "IFMK de Bordeaux",
            "IFMK de Paris — Assas",
            "IFMK de Lyon",
            "IFMK de Toulouse"
        ],
        "domaine": "Social & Santé",
        "selectivite": "Très élevée", "profil_ideal": "Après PASS/LAS ou bac S avec mention TB. Sport requis",
        "debouches": "Kinésithérapeute libéral, hospitalier, sportif", "capacite": 50, "taux_acces": 15
    },
}

# Domaines disponibles pour le filtre
DOMAINES = sorted(set(v["domaine"] for v in CATALOGUE.values()))

# ==========================================
# 4. CALENDRIER OFFICIEL PARCOURSUP 2025
# ==========================================
CALENDRIER = [
    {"date": "20 janv", "label": "Ouverture de la plateforme", "done": True},
    {"date": "13 mars", "label": "Clôture des vœux (minuit)", "done": True},
    {"date": "3 avril", "label": "Dossiers finalisés", "done": True},
    {"date": "27 mai", "label": "Résultats : Phase principale", "done": False, "key": "phase1"},
    {"date": "2 juin", "label": "Réponses initiales disponibles", "done": False, "key": "J0"},
    {"date": "6 juin", "label": "1ère vague de désistements", "done": False, "key": "J4"},
    {"date": "10 juin", "label": "2ème vague — listes d'attente avancent", "done": False, "key": "J8"},
    {"date": "17 juin", "label": "3ème vague — fin Bac approche", "done": False, "key": "J15"},
    {"date": "24 juin", "label": "Résultats du Bac", "done": False, "key": "J22"},
    {"date": "30 juin", "label": "Fin de la Phase Principale", "done": False, "key": "J28"},
    {"date": "10 juil", "label": "Phase Complémentaire (PASUP)", "done": False, "key": "PASUP"},
]

# ==========================================
# 5. SESSION STATE
# ==========================================
defaults = {
    "etape": "PROFIL",           # PROFIL → VOEUX → ADMISSION
    "profil": {},
    "panier": [],
    "resultats": {},
    "choix_actuel": None,
    "jour_idx": 0,               # Index dans le calendrier (à partir du J0)
    "ia_conseil": "",
    "voeux_supprimes": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==========================================
# 6. FONCTIONS UTILITAIRES
# ==========================================

def reset_complet():
    for k, v in defaults.items():
        st.session_state[k] = v if not isinstance(v, list) else []
        if isinstance(v, dict): st.session_state[k] = {}
    st.session_state.etape = "PROFIL"
    st.rerun()

def nb_voeux_restants():
    return 10 - len(st.session_state.panier)

def calculer_score_admission(formation_key, profil):
    """
    Calcule la probabilité d'admission en fonction du profil élève.
    Retourne un score entre 0 et 100.
    """
    info = CATALOGUE[formation_key]
    score = 50  # base

    moy = profil.get("moyenne", 10)
    mention = profil.get("mention", "Aucune")
    bac = profil.get("bac", "Général")
    spe1 = profil.get("spe1", "")
    spe2 = profil.get("spe2", "")
    spe3 = profil.get("spe3", "")
    spes = [spe1, spe2, spe3]

    taux_base = info.get("taux_acces", 50)
    score = taux_base

    # Bonus/Malus moyenne
    if moy >= 16: score += 20
    elif moy >= 14: score += 12
    elif moy >= 12: score += 4
    elif moy < 10: score -= 20
    elif moy < 12: score -= 8

    # Bonus mention
    if mention == "Très Bien": score += 15
    elif mention == "Bien": score += 8
    elif mention == "Assez Bien": score += 3

    # Adéquation spécialités / formation
    profil_ideal = info.get("profil_ideal", "").lower()
    for s in spes:
        if s and s.lower() in profil_ideal: score += 8

    # Pénalité bac inadapté
    if "STMG" in bac and "maths" in profil_ideal.lower(): score -= 15
    if "Pro" in bac and info.get("selectivite") in ["Élevée", "Très élevée"]: score -= 25
    if "Général" in bac and info.get("selectivite") == "Très élevée": score -= 5

    # Bonus 974 (formations Réunion légèrement avantagées si élève Réunion)
    if info["zone"] == "🇷🇪 Réunion" and profil.get("academie") == "La Réunion": score += 5

    return max(5, min(95, score))

def generer_resultats_ia(profil):
    """
    Génère les résultats initiaux basés sur le profil.
    Utilise le calcul probabiliste + aléatoire réaliste.
    """
    resultats = {}
    for item in st.session_state.panier:
        # Retrouver la formation d'origine
        formation_key = item.get("formation_key", item["titre"])
        if formation_key not in CATALOGUE:
            # Sous-vœu : utiliser la formation parente
            formation_key = item.get("groupe_key", formation_key)

        score = calculer_score_admission(formation_key, profil)

        # Tirage probabiliste réaliste
        tirage = random.randint(1, 100)

        if tirage <= score * 0.3:  # ~30% du score = OUI direct
            statut = "OUI ✅"
        elif tirage <= score * 0.35:
            statut = "OUI-SI 📘"
        elif tirage <= score * 0.85:
            statut = "EN ATTENTE ⏳"
        else:
            statut = "NON ❌"

        details = {}
        if statut == "EN ATTENTE ⏳":
            # Rang cohérent avec le score
            facteur = (100 - score) / 100
            mon_rang = int(random.randint(50, 400) * (1 + facteur))
            dernier_admis = max(0, mon_rang - random.randint(20, int(mon_rang * 0.4)))
            details = {"rang": mon_rang, "dernier_admis": dernier_admis, "score_profil": score}

        resultats[item["titre"]] = {
            "statut": statut,
            "details": details,
            "groupe": item["groupe"],
            "zone": item["zone"],
            "formation_key": formation_key,
            "score_profil": score,
        }
    return resultats

def avancer_temps():
    """Simule le passage du temps et l'avancée des listes d'attente."""
    st.session_state.jour_idx = min(st.session_state.jour_idx + 1, 6)
    changements = []

    for nom, data in st.session_state.resultats.items():
        if data["statut"] == "EN ATTENTE ⏳":
            score = data.get("score_profil", 50)
            # Plus le score est élevé, plus on avance vite
            progression = random.randint(
                int(score * 0.1), int(score * 0.6)
            )
            data["details"]["dernier_admis"] += progression

            if data["details"]["dernier_admis"] >= data["details"]["rang"]:
                data["statut"] = "OUI ✅"
                changements.append(nom)

    return changements

def get_date_actuelle():
    dates = ["2 juin", "6 juin", "10 juin", "14 juin", "17 juin", "21 juin", "24 juin"]
    return dates[min(st.session_state.jour_idx, len(dates)-1)]

def generer_conseil_ia(profil, resultats):
    """Demande à Gemini un conseil stratégique personnalisé."""
    if not GEMINI_OK:
        return "⚠️ Clé API Gemini non configurée."

    # Résumé des résultats
    resume = []
    for nom, data in resultats.items():
        resume.append(f"- {nom} : {data['statut']}")

    prompt = f"""
Tu es un conseiller d'orientation expert en Parcoursup, spécialisé pour les élèves de La Réunion.

PROFIL DE L'ÉLÈVE :
- Bac : {profil.get('bac')}
- Spécialités : {profil.get('spe1')}, {profil.get('spe2')}, {profil.get('spe3', 'aucune')}
- Moyenne générale : {profil.get('moyenne')}/20
- Mention visée : {profil.get('mention')}
- Académie : {profil.get('academie')}
- Projet professionnel : {profil.get('projet', 'Non précisé')}

RÉSULTATS PARCOURSUP SIMULÉS :
{chr(10).join(resume)}

DATE ACTUELLE SIMULÉE : {get_date_actuelle()}

CONSIGNE :
Rédige un conseil stratégique clair, bienveillant et concret pour cet élève.
Structure ta réponse en 3 parties :
1. **Analyse de la situation** (2-3 phrases sur les résultats)
2. **Actions prioritaires à faire maintenant** (liste de 3-4 conseils concrets et actionnables)
3. **Point de vigilance** (1 chose importante à ne pas oublier)

Adapte le ton à un lycéen de 17-18 ans. Sois encourageant mais réaliste.
Mentionne Parcoursup.fr et les délais de réponse si pertinent.
"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"Erreur IA : {e}"

def generer_lettre_motivation(formation_key, profil):
    """Génère une lettre de motivation personnalisée."""
    if not GEMINI_OK:
        return "⚠️ Clé API Gemini non configurée."

    info = CATALOGUE.get(formation_key, {})
    prompt = f"""
Tu es expert en rédaction de lettres de motivation Parcoursup.

FORMATION VISÉE : {formation_key}
Type : {info.get('type', '')} | Zone : {info.get('zone', '')}
Débouchés : {info.get('debouches', '')}
Profil idéal attendu : {info.get('profil_ideal', '')}

PROFIL ÉLÈVE :
- Bac {profil.get('bac')} | Spécialités : {profil.get('spe1')}, {profil.get('spe2')}
- Moyenne : {profil.get('moyenne')}/20
- Académie : {profil.get('academie')}
- Projet : {profil.get('projet', 'Non précisé')}
- Activités extra-scolaires : {profil.get('activites', 'Non précisé')}

Rédige une lettre de motivation Parcoursup (1500 caractères maximum).
Structure : Accroche → Pourquoi cette formation → Pourquoi moi → Projet professionnel.
Ton : Professionnel mais naturel pour un lycéen.
NE PAS commencer par "Je me permets de..."
"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"Erreur IA : {e}"

# ==========================================
# 7. SIDEBAR — PROFIL & NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
        <div style="font-size:2rem;">🎓</div>
        <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:800;
             color:white; letter-spacing:0.05em; margin-top:4px;">SIMULATEUR</div>
        <div style="font-size:0.65rem; color:rgba(255,255,255,0.5);
             text-transform:uppercase; letter-spacing:0.1em;">Parcoursup 2025</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Étapes de navigation
    etapes = {"PROFIL": "1. Mon Profil", "VOEUX": "2. Mes Vœux", "ADMISSION": "3. Phase d'Admission"}
    for k, label in etapes.items():
        actif = st.session_state.etape == k
        couleur = "#4B7BF5" if actif else "rgba(255,255,255,0.3)"
        fond = "rgba(255,255,255,0.12)" if actif else "transparent"
        st.markdown(f"""
        <div style="background:{fond}; border-left: 3px solid {couleur};
             padding: 0.5rem 0.8rem; border-radius:0 8px 8px 0;
             margin-bottom:4px; font-size:0.85rem; font-weight:{'700' if actif else '400'};
             color:{'white' if actif else 'rgba(255,255,255,0.55)'}">
             {label}
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Calendrier officiel
    st.header("📅 Calendrier 2025")
    for item in CALENDRIER[3:]:  # Afficher à partir des dates clés
        active = item.get("key") == ["J0","J4","J8","J15","J22","J28","PASUP"][min(st.session_state.jour_idx, 6)] if st.session_state.etape == "ADMISSION" else False
        st.markdown(f"""
        <div style="padding:5px 8px; margin-bottom:3px; font-size:0.78rem;
             background:{'rgba(75,123,245,0.2)' if active else 'rgba(255,255,255,0.05)'};
             border-radius:6px; border-left: 2px solid {'#4B7BF5' if active else 'transparent'}">
             <b style="color:{'#7BA8FF' if active else 'rgba(255,255,255,0.4)'};">{item['date']}</b>
             <span style="color:rgba(255,255,255,{'0.9' if active else '0.5'});"> — {item['label']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    if st.button("🔄 Recommencer", use_container_width=True):
        reset_complet()

# ==========================================
# 8. EN-TÊTE
# ==========================================
st.markdown("""
<div class="hero-header">
    <div class="hero-badge">Simulateur Officieux · Saison 2025</div>
    <div class="hero-title">🎓 Simulateur Parcoursup</div>
    <div class="hero-sub">Prépare ta stratégie d'admission · Réunion & Métropole · IA intégrée</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 9. ÉTAPE 1 — PROFIL ÉLÈVE
# ==========================================
if st.session_state.etape == "PROFIL":
    st.markdown('<div class="section-title">Étape 1 · Mon Profil Scolaire</div>', unsafe_allow_html=True)
    st.caption("Ces informations permettront de simuler des résultats réalistes selon ton dossier.")

    with st.form("form_profil"):
        c1, c2 = st.columns(2)
        with c1:
            prenom = st.text_input("👤 Prénom", placeholder="Ex : Marie")
            bac = st.selectbox("🎓 Série du Bac", [
                "Bac Général", "Bac Technologique (STI2D)", "Bac Technologique (STMG)",
                "Bac Technologique (ST2S)", "Bac Technologique (STL)",
                "Bac Professionnel"
            ])
            academie = st.selectbox("📍 Académie", ["La Réunion", "Paris", "Aix-Marseille",
                "Bordeaux", "Lyon", "Nantes", "Lille", "Autre"])

        with c2:
            moyenne = st.slider("📊 Moyenne générale (1re + Term)", 8.0, 20.0, 13.0, 0.5)
            mention = st.selectbox("🏅 Mention visée au Bac", [
                "Aucune", "Assez Bien (≥12)", "Bien (≥14)", "Très Bien (≥16)"
            ])
            rang_classe = st.selectbox("📈 Rang approximatif en classe", [
                "Top 10%", "Top 25%", "Top 50%", "Milieu de classe", "Bas de classe"
            ])

        st.markdown("**📚 Spécialités choisies (Terminale)**")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            spe1 = st.selectbox("Spécialité 1", [
                "Mathématiques", "Physique-Chimie", "SVT", "NSI",
                "Histoire-Géographie-Géopolitique", "SES", "HGGSP",
                "Langues & Cultures de l'Antiquité", "Humanités", "Arts",
                "Management", "STMG", "ST2S", "STI2D", "Autre"
            ])
        with sc2:
            spe2 = st.selectbox("Spécialité 2", [
                "SES", "SVT", "Physique-Chimie", "Mathématiques", "NSI",
                "HGGSP", "Histoire-Géographie-Géopolitique", "Humanités",
                "Langues & Cultures de l'Antiquité", "Arts", "Autre"
            ])
        with sc3:
            spe3 = st.selectbox("3ème spé abandonnée en 1ère", [
                "Aucune",
                "Mathématiques",
                "Physique-Chimie",
                "SVT (Sciences de la Vie et de la Terre)",
                "NSI (Numérique et Sciences Informatiques)",
                "SES (Sciences Économiques et Sociales)",
                "HGGSP (Histoire-Géo, Géopolitique, Sciences Po)",
                "Humanités, Littérature et Philosophie",
                "Langues & Cultures de l'Antiquité (Latin/Grec)",
                "LLCE (Langues Vivantes et Cultures Étrangères)",
                "Arts (Plastiques, Cinéma, Théâtre, Musique)",
                "EPPCS (Éducation Physique, Pratiques et Culture Sportives)",
                "Sciences de l'Ingénieur",
                "Biotechnologies",
                "Management, Sciences de Gestion et Numérique (STMG)",
                "Sciences et Technologies de la Santé et du Social (ST2S)",
                "Biologie-Écologie (Bac STAV)",
                "Mathématiques complémentaires (option)",
                "Mathématiques expertes (option)",
                "DNL (Discipline Non Linguistique)",
                "Autre"
            ])

        projet = st.text_area("🎯 Projet professionnel ou domaine visé",
            placeholder="Ex : Je veux travailler dans la santé, le droit, le numérique...",
            height=70)
        activites = st.text_input("🏅 Activités extra-scolaires (bénévolat, sport, etc.)",
            placeholder="Ex : Bénévolat Croix-Rouge, Capitaine équipe foot...")

        submitted = st.form_submit_button("✅ Valider mon profil et choisir mes vœux →", type="primary", use_container_width=True)

        if submitted:
            if not prenom:
                st.error("Indique ton prénom !")
            else:
                st.session_state.profil = {
                    "prenom": prenom, "bac": bac, "academie": academie,
                    "moyenne": moyenne, "mention": mention, "rang": rang_classe,
                    "spe1": spe1, "spe2": spe2, "spe3": spe3,
                    "projet": projet, "activites": activites
                }
                st.session_state.etape = "VOEUX"
                st.rerun()

# ==========================================
# 10. ÉTAPE 2 — SAISIE DES VŒUX
# ==========================================
elif st.session_state.etape == "VOEUX":
    profil = st.session_state.profil
    prenom = profil.get("prenom", "")

    st.markdown(f'<div class="section-title">Étape 2 · Les Vœux de {prenom}</div>', unsafe_allow_html=True)

    # Résumé profil
    st.markdown(f"""
    <div class="card" style="margin-bottom:1rem;">
        <b>👤 {prenom}</b> · {profil['bac']} · {profil['academie']}
        <span class="score-chip">Moy. {profil['moyenne']}/20</span>
        <span class="score-chip">{profil['mention']}</span>
        <span class="score-chip">{profil['spe1']}</span>
        <span class="score-chip">{profil['spe2']}</span>
    </div>
    """, unsafe_allow_html=True)

    col_cat, col_panier = st.columns([1.6, 1])

    with col_cat:
        st.markdown("#### 🔍 Catalogue des formations")

        # Filtres
        f1, f2, f3 = st.columns(3)
        with f1:
            zone_f = st.radio("Zone", ["Toutes", "🇷🇪 Réunion", "🇫🇷 Métropole"], horizontal=True)
        with f2:
            sel_f = st.selectbox("Sélectivité", ["Toutes", "Faible", "Modérée", "Élevée", "Très élevée"])
        with f3:
            dom_f = st.selectbox("Domaine", ["Tous"] + DOMAINES)

        # Filtrage
        formations_filtrées = {
            k: v for k, v in CATALOGUE.items()
            if (zone_f == "Toutes" or v["zone"] == zone_f)
            and (sel_f == "Toutes" or v["selectivite"] == sel_f)
            and (dom_f == "Tous" or v.get("domaine") == dom_f)
        }

        formation_sel = st.selectbox("Choisir une formation", list(formations_filtrées.keys()))
        info = CATALOGUE[formation_sel]

        # Fiche formation
        score_pred = calculer_score_admission(formation_sel, profil)
        couleur_score = "#00875A" if score_pred >= 60 else "#D97706" if score_pred >= 35 else "#C0000A"

        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:start;">
                <div>
                    <b style="font-size:0.95rem;">{formation_sel}</b><br>
                    <span style="font-size:0.8rem; color:#5A6478;">{info['zone']} · Sélectivité : <b>{info['selectivite']}</b></span>
                </div>
                <div style="text-align:center; background:{couleur_score}20; border:2px solid {couleur_score};
                     border-radius:10px; padding:6px 12px; min-width:70px;">
                    <div style="font-size:1.4rem; font-weight:800; color:{couleur_score};">{score_pred}%</div>
                    <div style="font-size:0.65rem; color:{couleur_score};">Chances estimées</div>
                </div>
            </div>
            <div style="margin-top:10px; font-size:0.82rem; color:#5A6478;">
                🎯 <b>Profil idéal :</b> {info['profil_ideal']}<br>
                💼 <b>Débouchés :</b> {info['debouches']}<br>
                📊 <b>Taux d'accès historique :</b> {info['taux_acces']}% · Capacité : {info['capacite']} places
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Ajout selon type
        nb_restants = nb_voeux_restants()
        if nb_restants == 0:
            st.error("⛔ Tu as atteint la limite de 10 vœux Parcoursup.")
        else:
            if info["type"] == "simple":
                if st.button(f"➕ Ajouter ce vœu ({nb_restants} restant{'s' if nb_restants > 1 else ''})", type="primary"):
                    deja = any(v["titre"] == formation_sel for v in st.session_state.panier)
                    if deja:
                        st.warning("Déjà dans ton dossier.")
                    else:
                        st.session_state.panier.append({
                            "titre": formation_sel,
                            "groupe": "Vœu unique",
                            "groupe_key": formation_sel,
                            "formation_key": formation_sel,
                            "zone": info["zone"],
                        })
                        st.toast("✅ Vœu ajouté !", icon="🎓")
                        st.rerun()

            elif info["type"] == "multiple":
                st.info(f"📚 Vœu multiple — sélectionne les établissements")
                sous = st.multiselect("Établissements visés", info["sous_voeux"])
                if st.button(f"➕ Ajouter les sous-vœux sélectionnés", type="primary"):
                    if not sous:
                        st.error("Sélectionne au moins un établissement.")
                    else:
                        count = 0
                        for sv in sous:
                            if nb_voeux_restants() == 0:
                                st.warning("Limite de 10 vœux atteinte !")
                                break
                            deja = any(v["titre"] == sv for v in st.session_state.panier)
                            if not deja:
                                st.session_state.panier.append({
                                    "titre": sv,
                                    "groupe": formation_sel,
                                    "groupe_key": formation_sel,
                                    "formation_key": formation_sel,
                                    "zone": info["zone"],
                                })
                                count += 1
                        if count > 0:
                            st.toast(f"✅ {count} sous-vœu(x) ajouté(s) !", icon="🎓")
                            st.rerun()

    with col_panier:
        nb = len(st.session_state.panier)
        st.markdown(f"#### 🎒 Mon Dossier ({nb}/10 vœux)")

        if nb == 0:
            st.markdown("""
            <div style="text-align:center; padding:2rem; color:#9CA3AF; font-size:0.9rem;">
                Aucun vœu pour l'instant.<br>Choisis des formations dans le catalogue.
            </div>
            """, unsafe_allow_html=True)
        else:
            # Barre de progression
            st.progress(nb / 10)
            st.caption(f"{10 - nb} vœu(x) restant(s)")

            for i, v in enumerate(st.session_state.panier):
                c_item, c_del = st.columns([5, 1])
                with c_item:
                    groupe_txt = f"<br><span style='color:#9CA3AF; font-size:0.75rem;'>↳ {v['groupe']}</span>" if v['groupe'] != "Vœu unique" else ""
                    st.markdown(f"""
                    <div class="voeu-item">
                        <div class="voeu-numero">{i+1}</div>
                        <div>
                            <span style="font-size:0.84rem;">{v['zone'].split()[0]} {v['titre']}</span>
                            {groupe_txt}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c_del:
                    if st.button("×", key=f"del_{i}", help="Supprimer"):
                        st.session_state.panier.pop(i)
                        st.rerun()

        if nb > 0:
            st.divider()
            if nb < 5:
                st.warning(f"⚠️ {nb} vœu(x) seulement. Parcoursup recommande au moins 6-8 vœux.")
            elif nb < 8:
                st.info(f"💡 Conseil : ajouter encore {8-nb} vœu(x) pour sécuriser ton admission.")
            else:
                st.success(f"✅ Bon équilibre ! {nb} vœux saisis.")

            if st.button("🚀 Lancer la simulation · Phase d'Admission", type="primary", use_container_width=True):
                with st.spinner("⚙️ Calcul des résultats selon ton profil..."):
                    time.sleep(1.5)
                    st.session_state.resultats = generer_resultats_ia(profil)
                    st.session_state.etape = "ADMISSION"
                    st.rerun()

# ==========================================
# 11. ÉTAPE 3 — PHASE D'ADMISSION
# ==========================================
elif st.session_state.etape == "ADMISSION":
    profil = st.session_state.profil
    prenom = profil.get("prenom", "")
    date_actuelle = get_date_actuelle()

    # --- Barre temporelle ---
    col_date, col_avance = st.columns([3, 1])
    with col_date:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:0.5rem;">
            <div style="background: var(--parcoursup-bleu); color:white; padding:6px 16px;
                 border-radius:8px; font-family:'Syne',sans-serif; font-weight:700; font-size:1rem;">
                📅 {date_actuelle}
            </div>
            <div style="color:var(--gris-texte); font-size:0.9rem;">
                Phase Principale · Simulation en cours
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_avance:
        if st.session_state.jour_idx < 6:
            if st.button("⏩ Avancer de quelques jours", type="primary"):
                nouveaux = avancer_temps()
                if nouveaux:
                    st.balloons()
                    st.toast(f"🎉 Nouveau OUI reçu : {nouveaux[0][:30]}...", icon="📬")
                else:
                    st.toast("Rien de nouveau. Les listes avancent...", icon="⏳")
                st.rerun()
        else:
            st.info("Phase principale terminée.")

    # --- Règle d'or ---
    choix = st.session_state.choix_actuel
    if choix:
        st.markdown(f"""
        <div class="card card-accepte">
            <b>✅ Proposition acceptée provisoirement :</b> {choix}<br>
            <span style="font-size:0.82rem; color:#1B4FBB;">
            Tu peux encore accepter un meilleur vœu — l'ancien sera automatiquement abandonné.
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alerte-regle">
            ⚠️ <b>Règle importante :</b> Tu dois accepter au moins une proposition avant la date limite !
            Sans réponse, tu perds toutes tes propositions.
        </div>
        """, unsafe_allow_html=True)

    # --- Onglets ---
    tab_resultats, tab_conseil, tab_lettres = st.tabs([
        "📋 Mes Résultats", "🤖 Conseil IA", "✍️ Lettres de motivation"
    ])

    # ---- TAB 1 : Résultats ----
    with tab_resultats:

        # ---- EXPLICATION DU VRAI SYSTÈME PARCOURSUP ----
        st.markdown("""
        <div style="background:#EEF2FF; border:1px solid #93B4F5; border-left:4px solid #003189;
             border-radius:0 10px 10px 0; padding:1rem 1.2rem; margin-bottom:1rem; font-size:0.88rem;">
            <b style="color:#003189;">📋 Les 3 réponses possibles sur Parcoursup (comme dans la vraie vie) :</b><br>
            <span style="color:#1a2a3a;">
            • <b>✅ OUI DÉFINITIF</b> — Tu acceptes et <u>abandonnes automatiquement tous tes autres vœux en attente</u>. C'est terminé.<br>
            • <b>⏳ OUI MAIS J'ATTENDS</b> — Tu gardes cette proposition <u>en sécurité</u>, mais tu restes en liste d'attente pour tes vœux prioritaires.<br>
            • <b>❌ NON MERCI</b> — Tu refuses définitivement cette proposition. Elle disparaît.
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Tri : OUI > EN ATTENTE > NON
        def tri_statut(item):
            s = item[1]["statut"]
            r = item[1].get("reponse_eleve", "")
            if r == "OUI_DEFINITIF": return -1   # tout en haut
            if r == "OUI_ATTENTE": return 0
            if "OUI" in s: return 1
            if "ATTENTE" in s: return 2
            return 3

        liste_triee = sorted(st.session_state.resultats.items(), key=tri_statut)

        # Compteurs résumé
        nb_oui    = sum(1 for _, d in st.session_state.resultats.items() if "OUI" in d["statut"] and "REFUSÉ" not in d["statut"])
        nb_att    = sum(1 for _, d in st.session_state.resultats.items() if "ATTENTE" in d["statut"])
        nb_non    = sum(1 for _, d in st.session_state.resultats.items() if "NON" in d["statut"] or "REFUSÉ" in d["statut"])
        choix_def = next((nom for nom, d in st.session_state.resultats.items() if d.get("reponse_eleve") == "OUI_DEFINITIF"), None)
        choix_tmp = [(nom, d) for nom, d in st.session_state.resultats.items() if d.get("reponse_eleve") == "OUI_ATTENTE"]

        # Bannière choix définitif
        if choix_def:
            st.markdown(f"""
            <div style="background:#E3FFF3; border:2px solid #00875A; border-radius:12px;
                 padding:1rem 1.4rem; margin-bottom:1rem; display:flex; align-items:center; gap:12px;">
                <span style="font-size:2rem;">🎉</span>
                <div>
                    <b style="color:#00875A; font-size:1rem;">Félicitations ! Tu as confirmé ton inscription définitive.</b><br>
                    <span style="font-size:0.88rem; color:#1a4a2a;">Formation choisie : <b>{choix_def}</b><br>
                    Tous tes autres vœux en attente ont été abandonnés automatiquement.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""<div class="card" style="text-align:center; border-top:3px solid {'#00875A' if nb_oui>0 else '#DDE3EF'}">
                <div style="font-size:2rem; font-weight:800; color:#00875A;">{nb_oui}</div>
                <div style="font-size:0.78rem; color:#5A6478;">Proposition(s) OUI</div></div>""", unsafe_allow_html=True)
        with m2:
            nb_oui_att = len(choix_tmp)
            st.markdown(f"""<div class="card" style="text-align:center; border-top:3px solid {'#003189' if nb_oui_att>0 else '#DDE3EF'}">
                <div style="font-size:2rem; font-weight:800; color:#003189;">{nb_oui_att}</div>
                <div style="font-size:0.78rem; color:#5A6478;">Gardé en attente</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="card" style="text-align:center; border-top:3px solid {'#D97706' if nb_att>0 else '#DDE3EF'}">
                <div style="font-size:2rem; font-weight:800; color:#D97706;">{nb_att}</div>
                <div style="font-size:0.78rem; color:#5A6478;">En liste d'attente</div></div>""", unsafe_allow_html=True)
        with m4:
            st.markdown(f"""<div class="card" style="text-align:center; border-top:3px solid {'#C0000A' if nb_non>0 else '#DDE3EF'}">
                <div style="font-size:2rem; font-weight:800; color:#C0000A;">{nb_non}</div>
                <div style="font-size:0.78rem; color:#5A6478;">Refusés/Non retenus</div></div>""", unsafe_allow_html=True)

        st.divider()

        for nom, data in liste_triee:
            statut = data["statut"]
            reponse = data.get("reponse_eleve", "")  # "", "OUI_DEFINITIF", "OUI_ATTENTE", "NON"

            # Masquer les refusés définitivement
            if "REFUSÉ PAR L'ÉLÈVE" in statut or reponse == "NON":
                with st.expander(f"~~{nom}~~ — Refusé/Abandonné", expanded=False):
                    st.caption("Ce vœu a été refusé ou abandonné définitivement.")
                continue

            # Couleur de la carte selon état
            if reponse == "OUI_DEFINITIF":
                card_style = "border:2px solid #00875A; background:#E3FFF3;"
            elif reponse == "OUI_ATTENTE":
                card_style = "border:2px solid #003189; background:#EEF2FF;"
            elif "OUI" in statut:
                card_style = "border-left:5px solid #00875A; background:#F0FFF8;"
            elif "ATTENTE" in statut:
                card_style = "border-left:5px solid #D97706; background:#FFF8E6;"
            else:
                card_style = "border-left:5px solid #C0000A; background:#FFF0F0;"

            st.markdown(f'<div class="card" style="{card_style}">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns([3, 2, 2])

            with c1:
                flag = data["zone"].split()[0]
                groupe_txt = f"<br><span style='color:#9CA3AF; font-size:0.75rem;'>↳ {data['groupe']}</span>" if data['groupe'] != "Vœu unique" else ""

                # Badge statut formation
                if "OUI ✅" in statut:
                    badge = '<span class="badge-oui">ADMISSION PROPOSÉE ✅</span>'
                elif "OUI-SI" in statut:
                    badge = '<span class="badge-oui-si">OUI-SI 📘</span>'
                elif "ATTENTE" in statut:
                    badge = '<span class="badge-attente">EN LISTE D\'ATTENTE ⏳</span>'
                else:
                    badge = '<span class="badge-non">NON RETENU ❌</span>'

                # Badge réponse élève
                if reponse == "OUI_DEFINITIF":
                    badge_rep = ' &nbsp;<span style="background:#00875A;color:white;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;">✅ INSCRIPTION CONFIRMÉE</span>'
                elif reponse == "OUI_ATTENTE":
                    badge_rep = ' &nbsp;<span style="background:#003189;color:white;padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;">⏳ GARDÉ EN SÉCURITÉ</span>'
                else:
                    badge_rep = ""

                st.markdown(f"""
                <b style="font-size:0.92rem;">{flag} {nom}</b>{groupe_txt}<br>
                <div style="margin-top:6px;">{badge}{badge_rep}</div>
                """, unsafe_allow_html=True)

            with c2:
                if "ATTENTE" in statut and data.get("details"):
                    rang = data["details"]["rang"]
                    dernier = data["details"]["dernier_admis"]
                    places = max(0, rang - dernier)
                    prog = min(1.0, dernier / rang) if rang > 0 else 0
                    st.markdown(f"""
                    <div style="font-size:0.82rem;">
                        📍 Ton rang : <b>{rang}</b><br>
                        ✅ Dernier appelé : <b>{dernier}</b><br>
                        ⬆️ Encore <b>{places}</b> place(s) à remonter
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(prog)
                elif "OUI" in statut:
                    score = data.get("score_profil", 0)
                    st.markdown(f"""
                    <div style="font-size:0.82rem; color:#00875A;">
                        🎯 Score profil : <b>{score}%</b><br>
                        📌 Compatible avec ton dossier
                    </div>
                    """, unsafe_allow_html=True)
                elif "NON" in statut:
                    st.markdown(f"""
                    <div style="font-size:0.82rem; color:#C0000A;">
                        📊 Score profil : <b>{data.get('score_profil',0)}%</b><br>
                        Sélectivité trop élevée pour ton dossier.
                    </div>
                    """, unsafe_allow_html=True)

            with c3:
                # =========================================
                # VRAIS BOUTONS PARCOURSUP (3 options)
                # =========================================

                if reponse == "OUI_DEFINITIF":
                    # Inscription définitive — seul le bouton d'info reste
                    st.markdown("""
                    <div style="font-size:0.8rem; color:#00875A; font-weight:600;">
                    🎓 Inscription confirmée.<br>Rendez-vous à la rentrée !
                    </div>""", unsafe_allow_html=True)

                elif reponse == "OUI_ATTENTE":
                    # Gardé en sécurité — peut upgrader vers définitif ou libérer
                    st.markdown("<span style='font-size:0.78rem; color:#003189;'>Ce vœu est gardé en sécurité.</span>", unsafe_allow_html=True)
                    if not choix_def:
                        if st.button("✅ Confirmer définitivement", key=f"def_{nom}", type="primary"):
                            # Abandon de tous les autres vœux en attente
                            for n2, d2 in st.session_state.resultats.items():
                                if n2 != nom and d2.get("reponse_eleve") == "OUI_ATTENTE":
                                    d2["reponse_eleve"] = "NON"
                                if n2 != nom and "ATTENTE" in d2["statut"]:
                                    d2["reponse_eleve"] = "NON"  # Abandon liste d'attente aussi
                            st.session_state.resultats[nom]["reponse_eleve"] = "OUI_DEFINITIF"
                            st.session_state.choix_actuel = nom
                            st.balloons()
                            st.rerun()
                    if st.button("❌ Abandonner ce vœu", key=f"ab_{nom}"):
                        st.session_state.resultats[nom]["reponse_eleve"] = "NON"
                        st.rerun()

                elif "OUI" in statut and not choix_def:
                    # Proposition disponible, pas encore répondu
                    st.markdown("""
                    <div style="font-size:0.78rem; color:#D97706; font-weight:600; margin-bottom:6px;">
                    ⚠️ Tu dois répondre avant la date limite !
                    </div>""", unsafe_allow_html=True)

                    # BOUTON 1 : OUI DÉFINITIF
                    if st.button("✅ OUI DÉFINITIF", key=f"ouiD_{nom}", type="primary",
                                  help="J'accepte et j'abandonne tous mes autres vœux en attente"):
                        for n2, d2 in st.session_state.resultats.items():
                            if n2 != nom:
                                if d2.get("reponse_eleve") == "OUI_ATTENTE":
                                    d2["reponse_eleve"] = "NON"
                                if "ATTENTE" in d2["statut"]:
                                    d2["reponse_eleve"] = "NON"
                        st.session_state.resultats[nom]["reponse_eleve"] = "OUI_DEFINITIF"
                        st.session_state.choix_actuel = nom
                        st.balloons()
                        st.rerun()

                    # BOUTON 2 : OUI MAIS J'ATTENDS
                    already_tmp = any(d.get("reponse_eleve") == "OUI_ATTENTE"
                                      for n2, d in st.session_state.resultats.items() if n2 != nom)
                    btn_label = "⏳ OUI MAIS J'ATTENDS"
                    if st.button(btn_label, key=f"ouiA_{nom}",
                                  help="Je garde ce vœu en sécurité et j'attends mes vœux prioritaires"):
                        # On remplace l'ancien "gardé" si besoin
                        for n2, d2 in st.session_state.resultats.items():
                            if n2 != nom and d2.get("reponse_eleve") == "OUI_ATTENTE":
                                d2["reponse_eleve"] = ""  # libère l'ancien
                        st.session_state.resultats[nom]["reponse_eleve"] = "OUI_ATTENTE"
                        st.rerun()

                    # BOUTON 3 : NON MERCI
                    if st.button("❌ NON MERCI", key=f"non_{nom}",
                                  help="Je refuse définitivement cette proposition"):
                        st.session_state.resultats[nom]["reponse_eleve"] = "NON"
                        st.rerun()

                elif "OUI" in statut and choix_def:
                    st.markdown("""<span style='font-size:0.78rem; color:#9CA3AF;'>
                    Tu as déjà confirmé une inscription définitive.</span>""", unsafe_allow_html=True)

                elif "ATTENTE" in statut and not choix_def:
                    if st.button("🚪 Se retirer de la liste", key=f"ret_{nom}",
                                  help="Je me retire définitivement de cette liste d'attente"):
                        st.session_state.resultats[nom]["reponse_eleve"] = "NON"
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)


    # ---- TAB 2 : Conseil IA ----
    with tab_conseil:
        st.markdown("#### 🤖 Analyse & Conseil Stratégique par l'IA")
        st.caption("Gemini analyse ta situation et te donne des conseils personnalisés.")

        if st.button("✨ Générer mon conseil personnalisé", type="primary"):
            with st.spinner("Analyse de ta situation en cours..."):
                conseil = generer_conseil_ia(profil, st.session_state.resultats)
                st.session_state.ia_conseil = conseil

        if st.session_state.ia_conseil:
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid var(--parcoursup-bleu);">
            {st.session_state.ia_conseil.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            st.text_area("📋 Copier ce conseil :", st.session_state.ia_conseil, height=200)

    # ---- TAB 3 : Lettres de motivation ----
    with tab_lettres:
        st.markdown("#### ✍️ Générateur de Lettres de Motivation")
        st.caption("Génère une lettre personnalisée pour chaque vœu, basée sur ton profil.")

        formations_disponibles = [nom for nom, d in st.session_state.resultats.items()
                                   if "NON" not in d["statut"] and "REFUSÉ" not in d["statut"]]

        if not formations_disponibles:
            st.info("Aucune formation disponible pour une lettre.")
        else:
            formation_lettre = st.selectbox("Formation pour la lettre", formations_disponibles)
            data_lettre = st.session_state.resultats[formation_lettre]
            fk = data_lettre.get("formation_key", formation_lettre)

            if st.button("✍️ Générer la lettre de motivation", type="primary"):
                with st.spinner("Rédaction en cours..."):
                    lettre = generer_lettre_motivation(fk, profil)
                    st.session_state[f"lettre_{formation_lettre}"] = lettre

            if f"lettre_{formation_lettre}" in st.session_state:
                st.markdown(f"""
                <div class="card" style="border-left: 4px solid var(--vert-ok);">
                <b>Lettre de motivation — {formation_lettre}</b><br><br>
                {st.session_state[f'lettre_{formation_lettre}'].replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                st.text_area("📋 Copier cette lettre :",
                    st.session_state[f"lettre_{formation_lettre}"], height=300)

    # Bouton reset bas de page
    st.divider()
    c_r1, c_r2 = st.columns([4, 1])
    with c_r2:
        if st.button("🔄 Nouvelle simulation"):
            reset_complet()
