import streamlit as st
import random
import time

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Simulateur Parcoursup",
    page_icon="🎓",
    layout="wide"
)

# --- 2. INITIALISATION DE LA MÉMOIRE (SESSION STATE) ---
# On stocke ici toutes les variables qui doivent survivre aux clics

if 'simulation_state' not in st.session_state:
    st.session_state.simulation_state = "SAISIE" # États : SAISIE ou ADMISSION

if 'mon_panier' not in st.session_state:
    st.session_state.mon_panier = [] # Liste des vœux de l'élève

if 'resultats_simules' not in st.session_state:
    st.session_state.resultats_simules = {} # Les réponses (OUI, NON...)

if 'mon_choix_actuel' not in st.session_state:
    st.session_state.mon_choix_actuel = None # Le vœu accepté provisoirement

if 'compteur_jours' not in st.session_state:
    st.session_state.compteur_jours = 0 # Pour le voyage dans le temps

if 'date_affichee' not in st.session_state:
    st.session_state.date_affichee = "2 Juin"

# --- 3. BASE DE DONNÉES (CATALOGUE DES FORMATIONS) ---
# Structure : Nom -> Type (simple/multiple) -> Zone -> Sous-vœux éventuels

CATALOGUE = {
    # --- FORMATIONS RÉUNION (974) ---
    "Licence Droit - Université de La Réunion (Nord)": {
        "type": "simple", "zone": "🇷🇪 Réunion", "sous_voeux": []
    },
    "BTS MCO - Lycée Bellepierre (St-Denis)": {
        "type": "simple", "zone": "🇷🇪 Réunion", "sous_voeux": []
    },
    "BTS SAM - Lycée Le Verger (Ste-Marie)": {
        "type": "simple", "zone": "🇷🇪 Réunion", "sous_voeux": []
    },
    "BUT Techniques de Co. - IUT St-Pierre": {
        "type": "simple", "zone": "🇷🇪 Réunion", "sous_voeux": []
    },
    "CPGE Scientifique (MPSI/PCSI) - Réunion": {
        "type": "multiple", "zone": "🇷🇪 Réunion", 
        "sous_voeux": [
            "Lycée Leconte de Lisle - MPSI",
            "Lycée Leconte de Lisle - PCSI",
            "Lycée Roland Garros - PCSI"
        ]
    },
    "IFSI (Soins Infirmiers) - Regroupement 974": {
        "type": "multiple", "zone": "🇷🇪 Réunion",
        "sous_voeux": ["CHU Nord (St-Denis)", "CHU Sud (St-Pierre)"]
    },

    # --- FORMATIONS MÉTROPOLE (FR) ---
    "Licence Psychologie - Université Paris Cité": {
        "type": "simple", "zone": "🇫🇷 Métropole", "sous_voeux": []
    },
    "Licence STAPS - Université de Bordeaux": {
        "type": "simple", "zone": "🇫🇷 Métropole", "sous_voeux": []
    },
    "CPGE Littéraire (A/L) - Paris & IDF": {
        "type": "multiple", "zone": "🇫🇷 Métropole",
        "sous_voeux": [
            "Lycée Henri IV (Paris)",
            "Lycée Fénelon (Paris)",
            "Lycée Lakanal (Sceaux)",
            "Lycée Chaptal (Paris)"
        ]
    },
    "Écoles d'Ingénieurs (Concours Geipi Polytech)": {
        "type": "multiple", "zone": "🇫🇷 Métropole",
        "sous_voeux": [
            "Polytech Lyon", "Polytech Montpellier", "Polytech Nantes", "Polytech Lille"
        ]
    },
    "Sciences Po - Réseau ScPo (Concours Commun)": {
        "type": "multiple", "zone": "🇫🇷 Métropole",
        "sous_voeux": [
            "Sciences Po Lille", "Sciences Po Lyon", "Sciences Po Rennes", "Sciences Po Toulouse"
        ]
    }
}

# --- 4. FONCTIONS LOGIQUES ---

def reset_simulation():
    """Remet tout à zéro pour un nouvel élève"""
    st.session_state.simulation_state = "SAISIE"
    st.session_state.mon_panier = []
    st.session_state.resultats_simules = {}
    st.session_state.mon_choix_actuel = None
    st.session_state.compteur_jours = 0
    st.session_state.date_affichee = "2 Juin"

def ajouter_voeu(nom_formation, sous_voeux_selectionnes=None):
    """Ajoute les choix au panier de l'élève"""
    info = CATALOGUE[nom_formation]
    
    # Cas 1 : Vœu Simple
    if info['type'] == "simple":
        # On vérifie les doublons
        deja_present = any(v['titre'] == nom_formation for v in st.session_state.mon_panier)
        if not deja_present:
            st.session_state.mon_panier.append({
                "titre": nom_formation, 
                "groupe": "Vœu Unique", 
                "zone": info['zone']
            })
            st.toast("Vœu ajouté !", icon="✅")
        else:
            st.warning("Déjà dans ton dossier.")

    # Cas 2 : Vœu Multiple (On ajoute chaque sous-vœu comme une ligne distincte)
    elif info['type'] == "multiple" and sous_voeux_selectionnes:
        count = 0
        for sv in sous_voeux_selectionnes:
            deja_present = any(v['titre'] == sv for v in st.session_state.mon_panier)
            if not deja_present:
                st.session_state.mon_panier.append({
                    "titre": sv, 
                    "groupe": nom_formation, # On garde le nom du regroupement
                    "zone": info['zone']
                })
                count += 1
        if count > 0:
            st.toast(f"{count} sous-vœux ajoutés !", icon="✅")

def generer_premiers_resultats():
    """Génère les résultats du 2 Juin (Situation initiale)"""
    etats = ["OUI", "OUI-SI", "EN ATTENTE", "REFUS"]
    poids = [0.15, 0.05, 0.60, 0.20] # 60% de chance d'être en attente (réaliste)
    
    res = {}
    for item in st.session_state.mon_panier:
        statut = random.choices(etats, weights=poids)[0]
        details = {}
        
        # Si en attente, on génère des rangs
        if statut == "EN ATTENTE":
            mon_rang = random.randint(100, 600)
            # Pour qu'il y ait du suspense, le dernier admis doit être inférieur à mon rang
            dernier_admis = mon_rang - random.randint(10, 150) 
            if dernier_admis < 0: dernier_admis = 0
            
            details = {"rang": mon_rang, "dernier_admis": dernier_admis}
            
        res[item['titre']] = {
            "statut": statut, 
            "details": details, 
            "groupe": item['groupe'], 
            "zone": item['zone']
        }
    
    st.session_state.resultats_simules = res
    st.session_state.simulation_state = "ADMISSION"

def avancer_le_temps():
    """Simule le passage des jours et la libération des places"""
    st.session_state.compteur_jours += 2
    
    # Liste des dates simulées
    calendrier = ["4 Juin", "6 Juin", "8 Juin", "10 Juin", "12 Juin", "15 Juin", "18 Juin", "25 Juin"]
    idx = min(st.session_state.compteur_jours // 2, len(calendrier) - 1)
    st.session_state.date_affichee = calendrier[idx]

    # Mise à jour des rangs pour les vœux en attente
    changements = 0
    for nom, data in st.session_state.resultats_simules.items():
        if data['statut'] == "EN ATTENTE":
            # Le rang du dernier admis augmente (des gens se sont désistés)
            progression = random.randint(5, 40) # Avancée aléatoire
            data['details']['dernier_admis'] += progression
            
            # CHECK : Est-ce que je suis pris ?
            if data['details']['dernier_admis'] >= data['details']['rang']:
                data['statut'] = "OUI" # Libération !
                changements += 1
    
    if changements > 0:
        st.balloons() # Effet visuel
        st.toast(f"🎉 {changements} vœu(x) débloqué(s) !", icon="📬")
    else:
        st.toast("Rien de nouveau aujourd'hui... Patience.", icon="⏳")

# --- 5. INTERFACE UTILISATEUR ---

st.title("🎓 Entraînement Parcoursup")

# ====== ÉTAPE 1 : LA SAISIE DES VŒUX ======
if st.session_state.simulation_state == "SAISIE":
    st.header("1. Constitue ton dossier de vœux")
    st.caption("Choisis des formations à La Réunion ou en Métropole.")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("🔍 Catalogue")
        
        # Filtre géographique
        zone_filter = st.radio("Zone :", ["Tout", "🇷🇪 Réunion", "🇫🇷 Métropole"], horizontal=True)
        
        # Filtrage de la liste
        choix_possibles = [k for k,v in CATALOGUE.items() if zone_filter == "Tout" or v['zone'] == zone_filter]
        
        formation_choisie = st.selectbox("Rechercher une formation...", choix_possibles)
        
        # Logique d'affichage selon le type (Simple vs Multiple)
        info = CATALOGUE[formation_choisie]
        
        with st.container(border=True):
            st.markdown(f"**{formation_choisie}**")
            st.caption(f"📍 {info['zone']}")
            
            if info['type'] == "simple":
                if st.button("Ajouter ce vœu"):
                    ajouter_voeu(formation_choisie)
            
            elif info['type'] == "multiple":
                st.info("📚 C'est un vœu multiple (regroupement).")
                sous_voeux = st.multiselect("Coche les établissements visés :", info['sous_voeux'])
                if st.button("Valider les sous-vœux"):
                    if sous_voeux:
                        ajouter_voeu(formation_choisie, sous_voeux)
                    else:
                        st.error("Sélectionne au moins un établissement.")

    with col2:
        st.subheader("🎒 Mon Panier")
        if not st.session_state.mon_panier:
            st.info("Ton dossier est vide.")
        else:
            # Affichage propre du panier
            for v in st.session_state.mon_panier:
                flag = v['zone'].split(" ")[0]
                if v['groupe'] == "Vœu Unique":
                    st.text(f"{flag} {v['titre']}")
                else:
                    st.text(f"{flag} {v['groupe']} \n ↳ {v['titre']}")
            
            st.divider()
            st.markdown(f"**Total : {len(st.session_state.mon_panier)} vœux**")
            
            if st.button("🚀 VALIDER & LANCER LA SIMULATION (2 Juin)", type="primary"):
                with st.spinner("Calcul de l'algorithme..."):
                    time.sleep(1.5)
                    generer_premiers_resultats()
                    st.rerun()

# ====== ÉTAPE 2 : L'ADMISSION (RÉSULTATS) ======
elif st.session_state.simulation_state == "ADMISSION":
    
    # --- BARRE DE CONTRÔLE TEMPOREL ---
    c_time1, c_time2 = st.columns([3, 1])
    with c_time1:
        st.title(f"📅 Date : {st.session_state.date_affichee}")
    with c_time2:
        if st.button("⏩ Avancer de 2 jours"):
            avancer_le_temps()
            st.rerun()
    
    # --- RAPPEL DU CHOIX ACTUEL ---
    st.info("💡 RÈGLE D'OR : Tu ne peux garder qu'un seul 'OUI' (ou 'OUI-SI') à la fois !")
    
    with st.container(border=True):
        col_sac, col_etat = st.columns([1, 4])
        with col_sac:
            st.image("https://cdn-icons-png.flaticon.com/512/2910/2910768.png", width=50) # Icone sac à dos
        with col_etat:
            if st.session_state.mon_choix_actuel:
                st.markdown(f"### ✅ Proposition acceptée : **{st.session_state.mon_choix_actuel}**")
                st.caption("Si tu acceptes une autre proposition 'OUI' ci-dessous, celle-ci sera perdue.")
            else:
                st.markdown("### ⚠️ Aucune proposition acceptée.")
                st.caption("Attention : si tu ne valides rien avant la date limite, tu perds tes propositions.")

    st.divider()

    # --- LISTE DES RÉSULTATS (CARTES) ---
    # Tri : OUI en premier, puis EN ATTENTE, puis REFUS
    liste_triee = sorted(
        st.session_state.resultats_simules.items(), 
        key=lambda x: 0 if x[1]['statut'] in ['OUI', 'OUI-SI'] else 1 if x[1]['statut'] == 'EN ATTENTE' else 2
    )

    for nom, data in liste_triee:
        statut = data['statut']
        flag = data['zone'].split(" ")[0]
        
        # Couleur de la bordure selon le statut
        couleur = "green" if "OUI" in statut else "blue" if statut == "EN ATTENTE" else "red"
        
        with st.expander(f"{flag} {nom}  --  {statut}", expanded=True):
            c1, c2 = st.columns([2, 1])
            
            with c1: # Informations
                st.caption(f"Regroupement : {data['groupe']}")
                
                if "OUI" in statut:
                    st.success(f"🎉 **ADMISSION PROPOSÉE : {statut}**")
                    if statut == "OUI-SI":
                        st.warning("Attention : Remise à niveau obligatoire.")
                
                elif statut == "EN ATTENTE":
                    st.info("⏳ **EN LISTE D'ATTENTE**")
                    rang = data['details']['rang']
                    dernier = data['details']['dernier_admis']
                    places_restantes = rang - dernier
                    
                    st.write(f"Ton classement : **{rang}**")
                    st.write(f"Dernier candidat appelé : **{dernier}**")
                    st.markdown(f"👉 Il reste **{places_restantes}** places à remonter.")
                    
                    # Barre de progression visuelle
                    if rang > 0:
                        prog = min(1.0, dernier / rang)
                        st.progress(prog)
                
                elif statut == "REFUS":
                    st.error("⛔ **NON RETENU**")
                    st.caption("L'établissement n'a pas retenu ta candidature.")

            with c2: # Boutons d'action
                # Cas : C'est mon choix actuel
                if st.session_state.mon_choix_actuel == nom:
                    if st.button("❌ Renoncer", key=f"renonc_{nom}"):
                        st.session_state.mon_choix_actuel = None
                        st.rerun()

                # Cas : Proposition disponible
                elif "OUI" in statut:
                    if st.button("✅ Accepter (Provisoirement)", key=f"acc_{nom}"):
                        st.session_state.mon_choix_actuel = nom
                        st.rerun()
                    if st.button("🗑️ Refuser définitivement", key=f"ref_{nom}"):
                        st.session_state.resultats_simules[nom]['statut'] = "REFUSÉ PAR L'ÉLÈVE"
                        st.rerun()

                # Cas : En attente
                elif statut == "EN ATTENTE":
                    if st.button("🚪 Démissionner (Stop)", key=f"dem_{nom}"):
                        st.session_state.resultats_simules[nom]['statut'] = "REFUSÉ PAR L'ÉLÈVE"
                        st.rerun()

    st.divider()
    if st.button("🔄 Nouvelle Simulation (Reset Complet)"):
        reset_simulation()
        st.rerun()
