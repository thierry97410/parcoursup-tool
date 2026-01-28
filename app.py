import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Simulateur Complet Parcoursup 974", page_icon="🇷🇪", layout="wide")

# --- INITIALISATION DE LA MÉMOIRE (SESSION STATE) ---
# C'est ici qu'on stocke la liste des vœux pour ne pas les perdre quand on clique
if 'mes_voeux' not in st.session_state:
    st.session_state.mes_voeux = []

# --- FONCTIONS ---
def ajouter_voeu(nom, type_voeu):
    st.session_state.mes_voeux.append({
        "nom": nom,
        "type": type_voeu,
        "statut": "En attente" # Au début, tout le monde est en attente
    })

def reset_simulation():
    st.session_state.mes_voeux = []

# --- INTERFACE ---
st.title("🇷🇪 Pilotage Parcoursup - La Réunion")
st.markdown("### Simulateur de gestion de liste de vœux")
st.info("Ajoutez vos vœux à gauche, puis changez leur statut pour voir comment réagir.")

# --- BARRE LATÉRALE : SAISIE DES VŒUX ---
with st.sidebar:
    st.header("1. Saisir mes vœux")
    st.caption("Entrez ici toute votre liste de vœux confirmés.")
    
    with st.form("ajout_voeu"):
        nom_voeu = st.text_input("Nom de la formation", placeholder="Ex: BTS SIO - Le Tampon")
        type_voeu = st.radio("Type de formation", ["Sélective (BTS, BUT, CPGE...)", "Non Sélective (Licence, PASS...)"])
        submit = st.form_submit_button("Ajouter ce vœu")
        
        if submit and nom_voeu:
            ajouter_voeu(nom_voeu, type_voeu)
            st.success(f"Vœu '{nom_voeu}' ajouté !")

    st.divider()
    if st.button("🗑️ Tout effacer et recommencer"):
        reset_simulation()
        st.rerun()

# --- ZONE PRINCIPALE : LE TABLEAU DE BORD ---
st.header("2. Mon Tableau de Bord")

if not st.session_state.mes_voeux:
    st.warning("👈 Commencez par ajouter des vœux dans le menu de gauche !")
else:
    # On affiche la liste
    col1, col2 = st.columns([2, 1])
    
    nb_oui_momentane = 0
    nb_oui_definitif = 0
    
    # On parcourt la liste des vœux pour créer les contrôles
    for i, voeu in enumerate(st.session_state.mes_voeux):
        with st.container():
            c1, c2, c3 = st.columns([3, 2, 2])
            
            # Nom et Type
            with c1:
                st.subheader(f"{i+1}. {voeu['nom']}")
                if "Non Sélective" in voeu['type']:
                    st.caption("🟢 Formation Non Sélective")
                else:
                    st.caption("🔴 Formation Sélective")
            
            # Sélecteur de statut (Simulation)
            with c2:
                nouveau_statut = st.selectbox(
                    "État ce matin :",
                    ["En attente", "Proposition d'admission", "Refusé", "J'ai ACCEPTÉ cette proposition", "J'ai RENONCÉ"],
                    key=f"statut_{i}",
                    index=["En attente", "Proposition d'admission", "Refusé", "J'ai ACCEPTÉ cette proposition", "J'ai RENONCÉ"].index(voeu['statut'])
                )
                # Mise à jour de la mémoire
                st.session_state.mes_voeux[i]['statut'] = nouveau_statut

            # Analyse immédiate par ligne
            with c3:
                if nouveau_statut == "Proposition d'admission":
                    st.info("🔔 **Action :** Vous pouvez accepter ou refuser.")
                elif nouveau_statut == "Refusé":
                    if "Non Sélective" in voeu['type']:
                        st.error("Bizarre... Une non-sélective ne peut pas refuser (sauf si capacités atteintes). Vérifiez.")
                    else:
                        st.error("❌ C'est fini pour ce vœu.")
                elif nouveau_statut == "J'ai ACCEPTÉ cette proposition":
                    st.success("✅ Vœu gardé (Panier)")
                    nb_oui_momentane += 1
                elif nouveau_statut == "J'ai RENONCÉ":
                    st.write("🗑️ Abandonné")

            st.divider()

    # --- ÉTAPE 3 : ANALYSE GLOBALE (LE CERVEAU DU PSYEN) ---
    st.header("3. Analyse de votre situation")
    
    # Règle du Panier Unique
    if nb_oui_momentane > 1:
        st.error("🚨 **ALERTE ROUGE : ILLÉGAL !**")
        st.markdown(f"""
        Vous avez mis **"J'ai ACCEPTÉ"** sur {nb_oui_momentane} formations différentes.
        
        🛑 **Règle absolue :** Vous ne pouvez garder qu'**UNE SEULE** proposition à la fois.
        👉 Vous devez renoncer aux autres immédiatement, sinon Parcoursup annulera tout.
        """)
    
    elif nb_oui_momentane == 1:
        st.success("✅ **Situation Valide**")
        st.markdown("""
        Vous avez 1 formation dans votre panier. C'est parfait.
        
        👉 **Conseil Stratégique :**
        Si vous avez d'autres vœux qui sont encore "En attente" et qui vous intéressent, **n'oubliez pas de cocher "Maintenir mes vœux en attente"** lors de la validation !
        """)
        
    elif nb_oui_momentane == 0:
        # Vérifions s'il y a des propositions en attente de réponse
        propositions_dispo = [v for v in st.session_state.mes_voeux if v['statut'] == "Proposition d'admission"]
        
        if len(propositions_dispo) > 1:
            st.warning("⚖️ **Le Duel !**")
            st.write(f"Vous avez {len(propositions_dispo)} propositions sur la table. Vous devez en choisir **UNE SEULE** à accepter. Les autres devront être refusées.")
        elif len(propositions_dispo) == 1:
            st.info("👉 Vous avez une proposition. Si elle vous plaît, acceptez-la pour sécuriser.")
        else:
            st.write("⏳ En attente de propositions...")
