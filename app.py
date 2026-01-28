import streamlit as st
import pandas as pd
from datetime import datetime, date

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Bernado - Assistant PsyEN",
    page_icon="🦉",
    layout="wide"
)

# --- 2. GESTION DE LA MÉMOIRE (SESSION STATE) ---
# Stockage des vœux de l'élève tant que l'appli est ouverte
if 'liste_voeux' not in st.session_state:
    st.session_state.liste_voeux = []

# --- 3. FONCTION CERVEAU : DÉTERMINER LA PHASE ---
def get_global_context(current_date):
    """
    Détermine la phase exacte (Année scolaire + Focus Admission Parcoursup)
    """
    m = current_date.month
    d = current_date.day
    y = current_date.year

    # PHASE 1 : Rentrée & Diag (Août - Toussaint)
    if (m == 8 and d >= 15) or m in [9, 10]:
        return {
            "id": "P1",
            "titre": "🍂 Phase 1 : Rentrée & Diagnostic",
            "action": "Prévention décrochage & Accueil",
            "color": "green",
            "mode": "preventif"
        }
    
    # PHASE 2 : Exploration (Nov - Déc)
    elif m in [11, 12]:
        return {
            "id": "P2",
            "titre": "🧭 Phase 2 : Exploration & Construction",
            "action": "Connaissance de soi & Découverte métiers",
            "color": "orange",
            "mode": "educatif"
        }

    # PHASE 3 : Vœux & Dossiers (Janvier - Mai)
    elif m in [1, 2, 3, 4, 5]:
        return {
            "id": "P3",
            "titre": "🏗️ Phase 3 : Formulation & Confirmation",
            "action": "Saisie Parcoursup / Affelnet & Bilans",
            "color": "blue",
            "mode": "administratif"
        }

    # PHASE 4 : ADMISSION (Juin - Juillet) -> C'est là que ça se joue
    elif m in [6, 7]:
        # Sous-Phases Parcoursup (Basé sur démarrage 2 juin)
        start_admission = date(y, 6, 2)
        
        if current_date < start_admission:
             return {
                "id": "P4-WAIT",
                "titre": "⏳ Phase 4 : Veille Résultats",
                "action": "Préparation psychologique avant le J-J",
                "color": "grey",
                "mode": "admission"
            }
        
        # J+0 à J+4 : Le Rush
        elif start_admission <= current_date <= date(y, 6, 6):
            return {
                "id": "P4-RUSH",
                "titre": "🚨 ADMISSION TEMPS 1 : Réponses & Stratégie",
                "action": "Gestion des délais (J+2) & Émotions",
                "color": "red",
                "mode": "admission"
            }
            
        # J+5 à Fin Juin : Fluidification
        elif date(y, 6, 7) <= current_date <= date(y, 6, 23):
            return {
                "id": "P4-FLOW",
                "titre": "📉 ADMISSION TEMPS 2 : Listes d'Attente",
                "action": "Calcul des rangs & Patience",
                "color": "orange",
                "mode": "admission"
            }
            
        # Fin Juin + : Complémentaire
        else:
            return {
                "id": "P4-COMP",
                "titre": "🆘 ADMISSION TEMPS 3 : Phase Complémentaire",
                "action": "Saisine CAES & Nouveaux vœux",
                "color": "green",
                "mode": "admission"
            }
            
    else:
        return {"id": "OFF", "titre": "🏖️ Vacances / Hors Période", "action": "Repos", "color": "grey", "mode": "off"}

# --- 4. BARRE LATÉRALE (CONTROLES) ---
with st.sidebar:
    st.title("🎛️ Panneau de Contrôle")
    
    # A. SIMULATION TEMPORELLE
    st.markdown("### 📅 Simulateur de Date")
    mode_simulation = st.checkbox("Activer le 'Voyage dans le temps'", value=True)
    if mode_simulation:
        date_simulee = st.date_input("Date système :", value=date(2025, 6, 3)) # Par défaut en juin pour tester
    else:
        date_simulee = datetime.now().date()
    
    st.divider()

    # B. SAISIE DES VŒUX (Le "Carburant")
    st.markdown("### 📝 Dossier Élève")
    st.caption("Saisie rapide (Anonyme !)")
    
    with st.form("form_ajout_voeu"):
        formation = st.text_input("Formation", placeholder="ex: BTS MCO - Bellepierre")
        statut = st.selectbox("Statut", ["EN ATTENTE", "OUI", "OUI-SI", "REFUS", "RENONCEMENT"])
        
        c1, c2 = st.columns(2)
        rang_eleve = c1.number_input("Rang Élève", min_value=0)
        rang_last = c2.number_input("Dernier Admis (N-1)", min_value=0)
        
        submitted = st.form_submit_button("Ajouter au dossier")
        
        if submitted and formation:
            delta = rang_last - rang_eleve if rang_eleve > 0 else 0
            st.session_state.liste_voeux.append({
                "Formation": formation,
                "Statut": statut,
                "Rang Élève": rang_eleve,
                "Dernier Admis": rang_last,
                "Delta (Marge)": delta
            })
            st.success("Vœu ajouté !")

    if st.button("🗑️ Nouveau dossier (Reset)"):
        st.session_state.liste_voeux = []
        st.rerun()

# --- 5. LOGIQUE PRINCIPALE ---
context = get_global_context(date_simulee)

# En-tête dynamique
st.title(context['titre'])
st.markdown(f"**Mission Prioritaire :** :{context['color']}[{context['action']}]")
st.info(f"📅 Date simulée : {date_simulee.strftime('%d/%m/%Y')}")

st.divider()

# --- 6. AFFICHAGE DU DOSSIER ÉLÈVE (TABLEAU DE BORD) ---
# Ce bloc s'affiche toujours s'il y a des données
if st.session_state.liste_voeux:
    st.subheader("📂 Synthèse des Vœux")
    df = pd.DataFrame(st.session_state.liste_voeux)
    
    # Fonction de style pour colorer les lignes
    def color_status(val):
        if val == 'OUI': return 'background-color: #d1e7dd; color: black' # Vert
        elif val == 'OUI-SI': return 'background-color: #fff3cd; color: black' # Jaune
        elif val == 'REFUS': return 'background-color: #f8d7da; color: black' # Rouge
        elif val == 'EN ATTENTE': return 'background-color: #cfe2ff; color: black' # Bleu
        return ''

    st.dataframe(df.style.map(color_status, subset=['Statut']), use_container_width=True)

    # Métriques Clés
    nb_oui = len(df[df['Statut'].isin(['OUI', 'OUI-SI'])])
    nb_attente = len(df[df['Statut'] == 'EN ATTENTE'])
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Propositions fermes", nb_oui)
    m2.metric("En Attente", nb_attente)
    
    # Calcul intelligent meilleure chance
    df_attente = df[df['Statut'] == 'EN ATTENTE']
    if not df_attente.empty:
        best_margin = df_attente['Delta (Marge)'].max()
        m3.metric("Meilleure Marge de sécurité", f"+{best_margin} places")

# --- 7. OUTILS INTELLIGENTS (SELON LA PHASE) ---

# CAS A : ADMISSION / LISTES D'ATTENTE (Juin)
if "admission" in context['mode']:
    st.subheader("🧠 Analyseur Tactique (Admission)")
    
    if context['id'] == "P4-RUSH":
        st.warning("⚠️ **Conseil J+0 :** Ne validez aucun RENONCEMENT définitif aujourd'hui sauf certitude absolue. Acceptez le meilleur 'OUI' en maintenant les vœux 'EN ATTENTE'.")
    
    elif context['id'] == "P4-FLOW":
        if not st.session_state.liste_voeux:
            st.write("👉 Remplissez les vœux à gauche pour lancer l'analyse.")
        else:
            df_attente = pd.DataFrame(st.session_state.liste_voeux)
            df_attente = df_attente[df_attente['Statut'] == "EN ATTENTE"]
            
            if not df_attente.empty:
                st.write("### 📉 Prédictions Listes d'Attente")
                for i, row in df_attente.iterrows():
                    delta = row['Delta (Marge)']
                    nom = row['Formation']
                    
                    if delta >= 20:
                        msg = "🟢 **Très Favorable** : La marge est confortable."
                    elif 0 <= delta < 20:
                        msg = "🟠 **Possible** : C'est serré, il faut attendre la mi-juin."
                    else:
                        msg = "🔴 **Compromis** : Le dernier admis de l'an dernier était mieux classé que toi."
                    
                    st.markdown(f"- **{nom}** : {msg} *(Marge: {delta})*")
            else:
                st.info("Aucun vœu en attente à analyser.")

# CAS B : FORMULATION DES VŒUX (Janvier-Mars)
elif context['id'] == "P3":
    st.subheader("🎓 Aide à la formulation")
    st.write("Le dossier est vide ? C'est le moment d'utiliser les outils d'exploration.")
    st.button("Générer une trame d'entretien 'Élève Indécis'")

# CAS C : RENTRÉE (Septembre)
elif context['id'] == "P1":
    st.subheader("🎒 Suivi de Rentrée")
    st.file_uploader("Importer liste élèves (CSV)", key="upload_p1")
