import smtplib
from email.message import EmailMessage

# 🔐 REMPLACE CES INFOS PAR LES TIENNES
EMAIL_SENDER = "tonemail@gmail.com"
EMAIL_PASSWORD = "mot_de_passe_application"

def send_verification_code(recipient_email, code):
    msg = EmailMessage()
    msg['Subject'] = 'Code de vérification - Réinitialisation de mot de passe'
    msg['From'] = EMAIL_SENDER
    msg['To'] = recipient_email
    msg.set_content(f"""
Bonjour,

Voici votre code de vérification pour réinitialiser votre mot de passe :

🔐 Code : {code}

Si vous n'avez pas demandé cette opération, ignorez cet email.

Cordialement,
L'équipe de sécurité
""")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Erreur d'envoi de mail : {e}")
        return False
