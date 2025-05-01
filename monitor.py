import psutil
import smtplib
import time
import subprocess
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Charger les variables depuis le fichier .env
load_dotenv()

# Configuration de l'email (chargé depuis .env)
EMAIL_SENDER = os.getenv("SENDER_EMAIL")
EMAIL_RECEIVER = os.getenv("RECIPIENT_EMAIL")
EMAIL_PASSWORD = os.getenv("SENDER_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

# Seuils (chargés depuis .env)
CPU_THRESHOLD = int(os.getenv("CPU_THRESHOLD"))
MEMORY_THRESHOLD = int(os.getenv("MEMORY_THRESHOLD"))
TEMP_THRESHOLD = int(os.getenv("TEMP_THRESHOLD"))
TEMP_CRITICAL = int(os.getenv("TEMP_CRITICAL"))
MONITORED_SERVER = os.getenv("MONITORED_SERVER")

# Dictionnaire pour stocker les dernières alertes envoyées
last_alerts = {
    "cpu": None,
    "memory": None,
    "temperature": None
}

# Délai minimum entre les alertes (en secondes)
ALERT_DELAY = 300  # 5 minutes

def send_email(subject, body):
    """Fonction pour envoyer un email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, text)
            print(f"Email envoyé : {subject}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

def should_send_alert(alert_type):
    """Vérifie si une alerte doit être envoyée en fonction du délai"""
    last_alert_time = last_alerts.get(alert_type)
    if last_alert_time is None:
        return True  # La première alerte peut être envoyée

    # Vérifie si le délai entre les alertes est respecté
    if datetime.now() - last_alert_time > timedelta(seconds=ALERT_DELAY):
        return True
    return False

def update_last_alert(alert_type):
    """Met à jour l'heure de la dernière alerte envoyée"""
    last_alerts[alert_type] = datetime.now()

def shutdown_system():
    """Arrête le système en fonction du système d'exploitation"""
    platform = sys.platform
    if platform == 'win32':
        # Windows
        subprocess.call(['shutdown', '/s', '/t', '60', '/c', "Arrêt pour température critique"])
    else:
        # Linux/Mac
        subprocess.call(['sudo', 'shutdown', '-h', '+1', '"Arrêt pour température critique"'])

def check_resources():
    """Vérifie l'utilisation des ressources"""
    # Vérification de l'utilisation du CPU
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD and should_send_alert("cpu"):
        send_email("Alerte: Usage élevé du CPU", f"Le CPU est à {cpu_usage}% ! Seuil: {CPU_THRESHOLD}%")
        update_last_alert("cpu")

    # Vérification de l'utilisation de la mémoire
    memory = psutil.virtual_memory()
    if memory.percent > MEMORY_THRESHOLD and should_send_alert("memory"):
        send_email("Alerte: Usage élevé de la mémoire", f"La mémoire est à {memory.percent}% ! Seuil: {MEMORY_THRESHOLD}%")
        update_last_alert("memory")

    # Vérification de la température (si supportée)
    try:
        temperature = psutil.sensors_temperatures().get('cpu_thermal', [])
        if temperature:
            temp = temperature[0].current
            # Vérification du seuil critique
            if temp > TEMP_CRITICAL:
                critical_message = f"CRITIQUE: La température est à {temp}°C, au-dessus du seuil critique de {TEMP_CRITICAL}°C ! Le système va s'arrêter dans 1 minute."
                send_email("CRITIQUE: Arrêt système imminent", critical_message)
                print(critical_message)
                # Arrêt du système
                shutdown_system()
                return True  # Pour indiquer qu'un arrêt est en cours
            # Vérification du seuil d'alerte
            elif temp > TEMP_THRESHOLD and should_send_alert("temperature"):
                send_email("Alerte: Température élevée", f"La température est à {temp}°C ! Seuil: {TEMP_THRESHOLD}°C")
                update_last_alert("temperature")
    except AttributeError:
        pass
    
    return False  # Aucun arrêt en cours

def main():
    """Fonction principale du script"""
    print("Démarrage du script de surveillance des ressources...")

    # Collecte des données initiales
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()

    temperature_info = "Température CPU non disponible"
    try:
        temperature = psutil.sensors_temperatures().get('cpu_thermal', [])
        if temperature:
            temperature_info = f"Température CPU: {temperature[0].current}°C"
    except AttributeError:
        pass

    initial_message = f"""Le script de surveillance des ressources a démarré.
Serveur surveillé: {MONITORED_SERVER}    
État initial du système:
- CPU: {cpu_usage}% (seuil d'alerte: {CPU_THRESHOLD}%)
- Mémoire: {memory.percent}% (seuil d'alerte: {MEMORY_THRESHOLD}%)
- Température: {temperature_info} (seuil d'alerte: {TEMP_THRESHOLD}°C, critique: {TEMP_CRITICAL}°C)
    """
    print(initial_message)
    send_email("Démarrage du script", initial_message)

    try:
        while True:
            # Si la fonction check_resources renvoie True, un arrêt est en cours
            if check_resources():
                print("Arrêt du système en cours...")
                break
            
            time.sleep(60)  # Attendre 1 minute avant la prochaine vérification
    except KeyboardInterrupt:
        send_email("Arrêt du script", "Le script de surveillance des ressources a été arrêté manuellement.")
        print("Script arrêté par l'utilisateur")

if __name__ == "__main__":
    main()