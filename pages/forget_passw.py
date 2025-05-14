import streamlit as st
import random
import string
from database.db import store_reset_code, verify_reset_code, clear_reset_code, reset_password
from email_sender import send_verification_code

st.set_page_config(page_title="🔐 Mot de passe oublié", layout="centered")

st.session_state.setdefault("step", 1)

# Étape 1 : Saisie de l’email
if st.session_state.step == 1:
    st.title("🔐 Mot de passe oublié")
    st.write("Veuillez entrer votre adresse email pour recevoir un code de vérification.")
    email = st.text_input("Adresse email")

    if st.button("Envoyer le code"):
        code = ''.join(random.choices(string.digits, k=6))
        if send_verification_code(email, code):
            store_reset_code(email, code)
            st.session_state.email = email
            st.session_state.step = 2
            st.success("📧 Code envoyé à votre adresse email.")
        else:
            st.error("Erreur lors de l'envoi de l'email. Veuillez réessayer plus tard.")

# Étape 2 : Vérification du code
elif st.session_state.step == 2:
    st.title("📩 Vérification du code")
    code = st.text_input("Entrez le code reçu par email")

    if st.button("Vérifier le code"):
        if verify_reset_code(st.session_state.email, code):
            st.session_state.step = 3
            st.success("Code vérifié. Vous pouvez maintenant changer votre mot de passe.")
        else:
            st.error("❌ Code incorrect.")

# Étape 3 : Nouveau mot de passe
elif st.session_state.step == 3:
    st.title("🔒 Nouveau mot de passe")
    username = st.text_input("Nom d'utilisateur")
    new_password = st.text_input("Nouveau mot de passe", type="password")
    confirm_password = st.text_input("Confirmer le mot de passe", type="password")

    if st.button("Réinitialiser le mot de passe"):
        if new_password != confirm_password:
            st.error("❌ Les mots de passe ne correspondent pas.")
        else:
            # Tu peux ici appeler la fonction pour mettre à jour le mot de passe
            if reset_password(st.session_state.email, new_password):
                st.success("✅ Mot de passe réinitialisé avec succès.")
                st.session_state.step = 1  # Retour à l'étape 1 pour la prochaine réinitialisation
            else:
                st.error("❌ Une erreur est survenue lors de la réinitialisation du mot de passe.")
