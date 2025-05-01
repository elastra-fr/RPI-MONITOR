
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

# RPI Monitor (English)

This project is a resource monitor used on Raspberry Pi that monitors CPU, memory, and temperature usage. It sends an alert email if any of these values exceed a predefined threshold and shuts down the Raspberry Pi if the temperature exceeds a critical threshold.

## Create a .env

You need to create a `.env` file at the root of the project with the following environment variables:

### Email information

SENDER_EMAIL=
SENDER_PASSWORD=
RECIPIENT_EMAIL=

### Monitoring parameters

CPU_THRESHOLD=80
MEMORY_THRESHOLD=80
TEMP_THRESHOLD=70
TEMP_CRITICAL=85

### SMTP server configuration

SMTP_SERVER=
SMTP_PORT=

### Server name

MONITORED_SERVER=

## Create the virtual environment

### Windows

python -m venv env

### Linux

python3 -m venv env

## Activate the virtual environment

# Windows

.\env\Scripts\activate

# Rpi Linux

source env/bin/activate

## Install dependencies

pip install -r requirements.txt


## Run the script

python monitor.py

## License


This project is licensed under MIT License with attribution to the original author. See the [LICENSE](LICENSE) file for details.






