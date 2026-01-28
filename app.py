import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Assistant Parcoursup - Réunion", page_icon="🎓")

# Titre et Introduction
st.title("🎓 Mon Assistant de Décision Parcoursup")
st.markdown("""
Bienvenue ! Cet outil vous aide à savoir **sur quel bouton cliquer** devant Parcoursup.
*Ceci est une aide à la décision, le choix final vous appartient !*
""")

st.warning("⚠️ **Rappel Réunion** : Attention au décalage horaire ! Les délais finissent souvent le matin (heure de Paris). Validez vos choix la veille au soir !")

st.divider()

# --- DÉBUT DU QUESTIONNAIRE ---

# Question 1
st.subheader("1. La situation ce matin")
situation = st.radio(
    "Avez-vous reçu une proposition d'admission pour une formation ?",
    ("Pas encore", "Oui, j'ai une proposition !")
)

if situation == "Pas encore":
    st.info("⏳ **Patience !** Consultez vos vœux en attente. Il n'y a rien à faire pour l'instant.")

else:
    # Question 2
    st.subheader("2. Votre avis sur cette formation")
    avis = st.radio(
        "Est-ce que cette formation vous plaît vraiment ?",
        ("Non, pas du tout", "Oui, c'est mon vœu favori", "Oui, mais j'espère mieux ailleurs")
    )

    if avis == "Non, pas du tout":
        st.error("🛑 **Conseil : RENONCER**")
        st.write("Ne gardez pas une place inutilement. En renonçant, vous faites un heureux sur la liste d'attente !")

    elif avis == "Oui, c'est mon vœu favori":
        st.success("🎉 **Conseil : ACCEPTER DÉFINITIVEMENT**")
        st.write("Bravo ! Vous avez votre formation. La procédure est terminée pour vous.")
        st.caption("N'oubliez pas de procéder à l'inscription administrative ensuite.")

    elif avis == "Oui, mais j'espère mieux ailleurs":
        # Question 3 - Gestion du "Panier"
        st.subheader("3. Votre panier actuel")
        panier = st.radio(
            "Avez-vous DÉJÀ accepté une autre proposition les jours précédents ?",
            ("Non, mon panier est vide", "Oui, j'ai déjà gardé une autre formation")
        )

        if panier == "Non, mon panier est vide":
            st.warning("✅ **Conseil : ACCEPTER** (Mais attention !)")
            st.write("Acceptez cette proposition pour assurer votre place.")
            st.markdown("**IMPORTANT :** Au moment de valider, cochez bien la case **'MAINTENIR MES VŒUX EN ATTENTE'** pour ne pas perdre vos autres rêves !")
        
        else:
            st.error("⚖️ **Conseil : C'EST LE DUEL !**")
            st.markdown("""
            **Règle d'or :** Vous ne pouvez garder qu'UNE SEULE formation à la fois.
            
            Vous devez choisir maintenant entre :
            1. L'ancienne formation (celle que vous aviez gardée).
            2. La nouvelle formation (celle de ce matin).
            
            👉 **Si vous acceptez la nouvelle, l'ancienne est perdue.**
            👉 **N'oubliez pas de MAINTENIR vos vœux en attente ensuite.**
            """)
