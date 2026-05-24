
# RPI Monitor (French)  

Ce projet est un moniteur ressources utilisé sur Raspberry Pi qui surveille l'utilisation du CPU, de la mémoire, du stockage et de la température. Il envoie un e-mail d'alerte si l'une de ces valeurs dépasse un seuil prédéfini et éteint le Raspberry Pi si la température dépasse un seuil critique.


## Installation (Raspberry Pi)

```bash
git clone <repo-url>
cd RPI-MONITOR
pip3 install -r requirements.txt
chmod +x setup.sh
./setup.sh
```

`setup.sh` crée le `.env` interactivement et propose d'installer un service systemd pour le lancement automatique au démarrage.

> Si un `.env` existe déjà, il ne sera pas écrasé.

---

## Installation manuelle

### 1. Créer le `.env`

Créer un fichier `.env` à la racine du projet :

```env
SENDER_EMAIL=
SENDER_PASSWORD=
RECIPIENT_EMAIL=
SMTP_SERVER=
SMTP_PORT=

CPU_THRESHOLD=80
MEMORY_THRESHOLD=80
TEMP_THRESHOLD=70
TEMP_CRITICAL=85
STORAGE_THRESHOLD=80

MONITORED_SERVER=
```

### 2. Environnement virtuel (optionnel)

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 3. Lancer le script

```bash
python3 monitor.py
```

# RPI Monitor (English)

This project is a resource monitor used on Raspberry Pi that monitors CPU, memory, storage and temperature usage. It sends an alert email if any of these values exceed a predefined threshold and shuts down the Raspberry Pi if the temperature exceeds a critical threshold.

## Installation (Raspberry Pi)

```bash
git clone <repo-url>
cd RPI-MONITOR
pip3 install -r requirements.txt
chmod +x setup.sh
./setup.sh
```

`setup.sh` creates the `.env` interactively and offers to install a systemd service for automatic startup.

> An existing `.env` will not be overwritten.

---

## Manual installation

### 1. Create `.env`

```env
SENDER_EMAIL=
SENDER_PASSWORD=
RECIPIENT_EMAIL=
SMTP_SERVER=
SMTP_PORT=

CPU_THRESHOLD=80
MEMORY_THRESHOLD=80
TEMP_THRESHOLD=70
TEMP_CRITICAL=85
STORAGE_THRESHOLD=80

MONITORED_SERVER=
```

### 2. Virtual environment (optional)

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 3. Run

```bash
python3 monitor.py
```

## License


This project is licensed under MIT License with attribution to the original author. See the [LICENSE](LICENSE) file for details.






