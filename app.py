import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Simulateur Parcoursup 974", page_icon="🇷🇪")

# En-tête
st.title("🇷🇪 Mon Simulateur de Choix")
st.markdown("### Spécial Parents & Élèves - La Réunion")
st.info("Ce simulateur ne stocke aucune donnée. Une fois la page fermée, tout s'efface.")

st.divider()

# --- ÉTAPE 1 : LA SITUATION ---
st.header("1. La proposition du jour")

# Champ de saisie pour le nom de la formation
nouvelle_formation = st.text_input(
    "Quelle est la formation qu'on vous propose CE MATIN ?",
    placeholder="Ex: BTS SIO au Lycée Rolland Garros"
)

# On bloque la suite tant que rien n'est écrit
if not nouvelle_formation:
    st.warning("👈 Commencez par entrer le nom de la formation reçue ci-dessus.")
    st.stop()  # Arrête le script ici tant que c'est vide

st.success(f"D'accord, analysons la proposition : **{nouvelle_formation}**")

# --- ÉTAPE 2 : L'ANALYSE ---
st.header("2. Votre ressenti")
avis = st.radio(
    f"Est-ce que **{nouvelle_formation}** vous plaît ?",
    ("Non, ça ne m'intéresse pas", "Oui, c'est mon vœu favori", "Oui, mais j'hésite")
)

if avis == "Non, ça ne m'intéresse pas":
    st.error(f"🛑 **Conseil : RENONCER à {nouvelle_formation}**")
    st.write("Ne bloquez pas la place. En renonçant, vous libérez une place pour un autre élève.")

elif avis == "Oui, c'est mon vœu favori":
    st.balloons()
    st.success(f"🎉 **Conseil : ACCEPTER DÉFINITIVEMENT {nouvelle_formation}**")
    st.write("Félicitations ! La procédure est finie. Pensez à l'inscription administrative.")

elif avis == "Oui, mais j'hésite":
    # --- ÉTAPE 3 : LE PANIER ---
    st.header("3. Comparaison avec le panier")
    
    a_deja_formation = st.radio(
        "Aviez-vous DÉJÀ accepté une autre proposition les jours d'avant ?",
        ("Non, mon panier est vide", "Oui, j'ai déjà un vœu en attente")
    )
    
    if a_deja_formation == "Oui, j'ai déjà un vœu en attente":
        ancienne_formation = st.text_input(
            "Quel est le nom de cette formation que vous gardez au chaud ?",
            placeholder="Ex: Licence Droit à la fac du Moufia"
        )
        
        if ancienne_formation:
            st.warning("⚖️ **LE DUEL FINAL**")
            st.write("Vous ne pouvez garder qu'une seule place. Vous devez choisir maintenant entre :")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"🥊 L'ancienne :\n**{ancienne_formation}**")
            with col2:
                st.success(f"🥊 La nouvelle :\n**{nouvelle_formation}**")
                
            choix_final = st.radio("Qui gagne le duel ?", (ancienne_formation, nouvelle_formation))
            
            if choix_final == nouvelle_formation:
                st.write(f"👉 **Action :** Acceptez **{nouvelle_formation}**. Le système libérera automatiquement {ancienne_formation}.")
            else:
                st.write(f"👉 **Action :** Refusez **{nouvelle_formation}**. Vous gardez {ancienne_formation} en sécurité.")
                
            st.caption("⚠️ N'oubliez pas de cocher 'Maintenir mes vœux en attente' si vous attendez encore d'autres réponses !")
            
    else:
        st.success(f"✅ **Conseil : ACCEPTER {nouvelle_formation}**")
        st.write(f"Mettez **{nouvelle_formation}** dans votre panier pour sécuriser la place.")
        st.caption("⚠️ Important : Cochez bien 'Maintenir mes vœux en attente' pour ne pas perdre vos autres vœux !")

st.divider()
st.caption("Rappel : Les délais de réponse sont souvent en Heure de Paris. Ne validez pas au dernier moment !")
