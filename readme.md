
# RPI Monitor (French)  

Ce projet est un moniteur ressources utilisé sur Raspberry Pi qui surveille l'utilisation du CPU, de la mémoire et de la température. Il envoie un e-mail d'alerte si l'une de ces valeurs dépasse un seuil prédéfini et éteint le Raspberry Pi si la température dépasse un seuil critique.


## Créer un .env

Vous devez créer un fichier `.env` à la racine du projet avec les variables d'environnement suivantes :

### Informations d'email
SENDER_EMAIL=
SENDER_PASSWORD=
RECIPIENT_EMAIL=
### Paramètres de surveillance
CPU_THRESHOLD=80
MEMORY_THRESHOLD=80
TEMP_THRESHOLD=70
TEMP_CRITICAL=85

### Configuration du serveur SMTP
SMTP_SERVER=
SMTP_PORT=

###Nom du serveur
MONITORED_SERVER= 



## Créer l'environnement virtuel

### Windows


python -m venv env


### Linux

python3 -m venv env

## Activer l'environnement virtuel

# Windows
.\env\Scripts\activate

# Rpi Linux

source env/bin/activate

## Installer les dépendances

pip install -r requirements.txt

## Exécuter le script

python monitor.py








