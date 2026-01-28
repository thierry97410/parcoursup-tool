import streamlit as st
from datetime import datetime, date

st.set_page_config(page_title="PsyEN-EDO : Module Admission", layout="wide", page_icon="🎓")

# --- 1. SIMULATION TEMPORELLE (SIDEBAR) ---
# Indispensable pour tester le comportement de l'appli à différentes dates
with st.sidebar:
    st.header("🕰️ Zone de Test Temporel")
    mode_simulation = st.checkbox("Activer la simulation de date", value=True)
    
    if mode_simulation:
        # On fixe la date par défaut au 2 Juin (Début des réponses)
        date_simulee = st.date_input("Simuler une date :", value=date(2025, 6, 2))
    else:
        date_simulee = datetime.now().date()

    st.info(f"📅 Date active : {date_simulee.strftime('%d/%m/%Y')}")

# --- 2. LOGIQUE DES PHASES PARCOURSUP ---
def get_parcoursup_phase(current_date):
    """
    Détermine la sous-phase précise de l'admission Parcoursup.
    Basé sur le démarrage au 02 Juin.
    """
    # Avant le 2 Juin : Attente
    if current_date < date(current_date.year, 6, 2):
        return {
            "id": 0,
            "titre": "⏳ Phase d'Attente",
            "message": "Les dossiers sont remontés. On prépare les élèves au jour J.",
            "color": "grey"
        }

    # TEMPS 1 : Ouverture & Premières Réponses (2 Juin - 6 Juin)
    # C'est la période de forte charge émotionnelle et technique (délais courts)
    elif date(current_date.year, 6, 2) <= current_date <= date(current_date.year, 6, 6):
        return {
            "id": 1,
            "titre": "🚨 ADMISSION TEMPS 1 : Le Choc & Les Premiers Choix",
            "message": "Action Prioritaire : Expliquer les 'Oui', 'Oui-si' et 'En attente'. Éviter la validation précipitée.",
            "color": "red"
        }

    # TEMPS 2 : Fluidification & Listes d'Attente (7 Juin - 23 Juin)
    # Les rangs bougent, le GDD (Groupe Dossier) s'active pour les 'En attente'
    elif date(current_date.year, 6, 7) <= current_date <= date(current_date.year, 6, 23):
        return {
            "id": 2,
            "titre": "📉 ADMISSION TEMPS 2 : Stratégie & Patience",
            "message": "Action Prioritaire : Analyser l'évolution des rangs liste d'attente. Rassurer sur la vitesse de progression.",
            "color": "orange"
        }

    # TEMPS 3 : Phase Complémentaire & CAES (À partir du 24 Juin)
    # Gestion des "Sans proposition" et ouverture de la phase complémentaire
    else:
        return {
            "id": 3,
            "titre": "🆘 ADMISSION TEMPS 3 : Secours & Complémentaire",
            "message": "Action Prioritaire : Saisie des vœux en phase complémentaire et saisine CAES.",
            "color": "green"
        }

# --- 3. INTERFACE CONTEXTUELLE ---
phase_info = get_parcoursup_phase(date_simulee)

st.title(f"Assistant Admission - {phase_info['titre']}")
st.markdown(f"**Directive du jour :** :{phase_info['color']}[{phase_info['message']}]")
st.divider()

# --- 4. WIDGETS SPÉCIFIQUES PAR SOUS-PHASE ---

# WIDGETS TEMPS 1 (Urgence & Compréhension)
if phase_info['id'] == 1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💡 Aide à la Décision Immédiate")
        st.write("L'élève a reçu :")
        choix = st.multiselect("Propositions reçues", ["OUI", "OUI-SI", "EN ATTENTE", "REFUS"])
        if "OUI-SI" in choix:
            st.warning("⚠️ **OUI-SI** : Vérifier les conditions (remise à niveau) avant d'accepter !")
        if "OUI" in choix and "EN ATTENTE" in choix:
            st.success("✅ Conseil : Accepter le OUI (provisoirement) et maintenir les vœux EN ATTENTE préférés.")
            
    with col2:
        st.subheader("📞 Script d'Urgence")
        st.info("« Ne te précipite pas pour renoncer. Tu as un délai de réflexion (J+2). On regarde tes rangs ensemble. »")

# WIDGETS TEMPS 2 (Calcul & Analyse)
elif phase_info['id'] == 2:
    st.subheader("📊 Calculateur de Probabilité (Liste d'Attente)")
    col1, col2, col3 = st.columns(3)
    rang = col1.number_input("Rang de l'élève", value=150)
    dernier_pris = col2.number_input("Rang du dernier appelé (an dernier)", value=200)
    
    if col3.button("Analyser"):
        delta = dernier_pris - rang
        if delta > 20:
            st.success("🟢 Très favorable. Maintien conseillé.")
        elif delta > 0:
            st.warning("🟠 Incertain mais possible. Garder en backup.")
        else:
            st.error("🔴 Très compromis. Activer plan B.")

# WIDGETS TEMPS 3 (Secours)
elif phase_info['id'] == 3:
    st.subheader("🔎 Moteur Phase Complémentaire")
    domaine = st.text_input("Domaine recherché (ex: BTS MCO)")
    st.write("Génération de la liste des places vacantes à La Réunion...")
    # (Ici on connecterait ta base de données ou un fichier CSV des places vacantes)
    st.markdown("*Lien vers la fiche de saisine CAES (Commission d'Accès à l'Enseignement Supérieur)*")
