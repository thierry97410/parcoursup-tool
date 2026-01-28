import streamlit as st
import random
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Simulateur Parcoursup Élève", page_icon="🎓")

# --- INITIALISATION DE LA MÉMOIRE ---
if 'simulation_state' not in st.session_state:
    st.session_state.simulation_state = "SAISIE" # États possibles : SAISIE, ADMISSION
if 'mon_panier' not in st.session_state:
    st.session_state.mon_panier = [] # Liste des vœux choisis
if 'resultats_simules' not in st.session_state:
    st.session_state.resultats_simules = {} # Résultats (OUI, NON...) générés
if 'mon_choix_actuel' not in st.session_state:
    st.session_state.mon_choix_actuel = None # Le vœu accepté provisoirement

# --- BASE DE DONNÉES FICTIVE ---
FORMATIONS_FICTIVES = [
    "Licence Droit - Université de La Réunion (Nord)",
    "Licence Psycho - Université de La Réunion (Tampon)",
    "BTS MCO - Lycée Bellepierre",
    "BTS SAM - Lycée Le Verger",
    "BUT Informatique - IUT Saint-Pierre",
    "CPGE Littéraire - Lycée Leconte de Lisle",
    "IFSI - CHU Saint-Denis",
    "DN MADe Graphisme - Lycée Ambroise Vollard"
]

# --- FONCTIONS UTILES ---
def reset_simulation():
    st.session_state.simulation_state = "SAISIE"
    st.session_state.mon_panier = []
    st.session_state.resultats_simules = {}
    st.session_state.mon_choix_actuel = None

def generer_resultats():
    """Génère aléatoirement des réponses pour chaque vœu du panier"""
    etats_possibles = ["OUI", "OUI-SI", "EN ATTENTE", "REFUS"]
    poids = [0.3, 0.1, 0.4, 0.2] # Probabilités
    
    resultats = {}
    for v in st.session_state.mon_panier:
        statut = random.choices(etats_possibles, weights=poids)[0]
        # On ajoute des détails fictifs pour le réalisme
        details = {}
        if statut == "EN ATTENTE":
            details = {"rang": random.randint(100, 500), "dernier_admis": random.randint(150, 600)}
        resultats[v] = {"statut": statut, "details": details}
    
    st.session_state.resultats_simules = resultats
    st.session_state.simulation_state = "ADMISSION"

# --- INTERFACE ---

st.title("🎮 Simulateur d'Entraînement Parcoursup")

# === ÉCRAN 1 : LA SAISIE DES VŒUX ===
if st.session_state.simulation_state == "SAISIE":
    st.header("Étape 1 : Fais tes courses !")
    st.write("Imagine que nous sommes en Janvier. Choisis des formations pour remplir ton dossier.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        choix = st.selectbox("Rechercher une formation", FORMATIONS_FICTIVES)
        if st.button("Ajouter à ma liste de vœux"):
            if choix not in st.session_state.mon_panier:
                st.session_state.mon_panier.append(choix)
                st.success(f"{choix} ajouté !")
            else:
                st.warning("Tu as déjà demandé cette formation.")

    with col2:
        st.subheader("📋 Ma Liste")
        if not st.session_state.mon_panier:
            st.info("Ton panier est vide.")
        else:
            for v in st.session_state.mon_panier:
                st.markdown(f"- {v}")
            
            st.divider()
            if len(st.session_state.mon_panier) >= 1:
                st.write("Prêt pour les résultats ?")
                if st.button("🚀 LANCER LA SIMULATION (Juin)", type="primary"):
                    with st.spinner("L'algorithme tourne... On avance le temps jusqu'au 2 juin..."):
                        time.sleep(2) # Petit effet de suspense
                        generer_resultats()
                        st.rerun()

# === ÉCRAN 2 : L'ADMISSION (RÉPONSES) ===
elif st.session_state.simulation_state == "ADMISSION":
    st.header("Étape 2 : Le Jour des Résultats (2 Juin)")
    st.info("💡 Règle d'or : Tu ne peux garder qu'un seul 'OUI' ou 'OUI-SI' à la fois !")
    
    # Affichage du choix actuel (Le "Sac à dos")
    if st.session_state.mon_choix_actuel:
        st.success(f"🎒 Tu as accepté provisoirement : **{st.session_state.mon_choix_actuel}**")
    else:
        st.warning("🎒 Tu n'as encore rien accepté.")

    st.divider()

    # Affichage des vœux et boutons d'action
    for formation, data in st.session_state.resultats_simules.items():
        statut = data['statut']
        
        # --- CARTE DE VŒU ---
        with st.container(border=True):
            c1, c2 = st.columns([3, 2])
            
            with c1:
                st.subheader(formation)
                
                # Badges de couleur
                if statut == "OUI":
                    st.markdown(":green_heart: **Proposition d'admission (OUI)**")
                elif statut == "OUI-SI":
                    st.markdown(":large_yellow_circle: **OUI-SI (Sous condition)**")
                elif statut == "EN ATTENTE":
                    st.markdown(":hourglass: **En attente**")
                    st.caption(f"Rang : {data['details'].get('rang')} / Dernier appelé : {data['details'].get('dernier_admis')}")
                else:
                    st.markdown(":no_entry_sign: **Refusé**")

            # --- BOUTONS D'INTERACTION ---
            with c2:
                # CAS 1 : C'est déjà mon choix actuel
                if st.session_state.mon_choix_actuel == formation:
                    st.write("✅ Accepté provisoirement")
                    if st.button("❌ Renoncer finalement", key=f"renonc_{formation}"):
                        st.session_state.mon_choix_actuel = None
                        st.rerun()

                # CAS 2 : Proposition disponible (OUI ou OUI-SI) et pas encore choisie
                elif statut in ["OUI", "OUI-SI"]:
                    col_a, col_b = st.columns(2)
                    if col_a.button("Accepter", key=f"acc_{formation}"):
                        # Règle d'écrasement
                        ancien = st.session_state.mon_choix_actuel
                        st.session_state.mon_choix_actuel = formation
                        if ancien:
                            st.toast(f"⚠️ Attention : Tu as perdu '{ancien}' en acceptant celle-ci !", icon="🔄")
                        else:
                            st.toast("Félicitations ! Pense à maintenir tes vœux en attente si tu veux.", icon="🎉")
                        st.rerun()
                    
                    if col_b.button("Refuser", key=f"ref_{formation}"):
                        st.session_state.resultats_simules[formation]['statut'] = "REFUS_PAR_ELEVE"
                        st.rerun()

                # CAS 3 : En attente
                elif statut == "EN ATTENTE":
                    st.write("Vœu maintenu automatiquement.")
                    if st.button("🗑️ Renoncer (Je ne veux plus attendre)", key=f"att_renonc_{formation}"):
                         st.session_state.resultats_simules[formation]['statut'] = "REFUS_PAR_ELEVE"
                         st.rerun()
                
                # CAS 4 : Refus par l'établissement ou par l'élève
                elif statut == "REFUS":
                    st.write("❌ Formation non disponible")
                elif statut == "REFUS_PAR_ELEVE":
                    st.write("🗑️ Tu as renoncé à ce vœu.")

    st.divider()
    if st.button("🔄 Recommencer l'entraînement (Reset)"):
        reset_simulation()
        st.rerun()
