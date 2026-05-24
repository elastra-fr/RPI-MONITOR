#!/bin/bash

ENV_FILE=".env"

if [ -f "$ENV_FILE" ]; then
    echo "Le fichier .env existe déjà, configuration ignorée."
else
    echo "=== Configuration du moniteur RPI ==="
    echo ""

    # Email
    read -p "Email expéditeur           : " SENDER_EMAIL
    read -s -p "Mot de passe expéditeur    : " SENDER_PASSWORD
    echo ""
    read -p "Email destinataire         : " RECIPIENT_EMAIL
    read -p "Serveur SMTP               : " SMTP_SERVER
    read -p "Port SMTP (ex: 587)        : " SMTP_PORT

    echo ""
    echo "=== Seuils d'alerte ==="

    read -p "Seuil CPU en %       [80]  : " CPU_THRESHOLD
    CPU_THRESHOLD=${CPU_THRESHOLD:-80}

    read -p "Seuil mémoire en %   [80]  : " MEMORY_THRESHOLD
    MEMORY_THRESHOLD=${MEMORY_THRESHOLD:-80}

    read -p "Seuil stockage en %  [80]  : " STORAGE_THRESHOLD
    STORAGE_THRESHOLD=${STORAGE_THRESHOLD:-80}

    read -p "Seuil température °C [70]  : " TEMP_THRESHOLD
    TEMP_THRESHOLD=${TEMP_THRESHOLD:-70}

    read -p "Temp. critique °C    [85]  : " TEMP_CRITICAL
    TEMP_CRITICAL=${TEMP_CRITICAL:-85}

    echo ""
    read -p "Nom du serveur surveillé   : " MONITORED_SERVER

    cat > "$ENV_FILE" <<EOF
# Configuration email
SENDER_EMAIL=${SENDER_EMAIL}
SENDER_PASSWORD=${SENDER_PASSWORD}
RECIPIENT_EMAIL=${RECIPIENT_EMAIL}
SMTP_SERVER=${SMTP_SERVER}
SMTP_PORT=${SMTP_PORT}

# Seuils d'alerte
CPU_THRESHOLD=${CPU_THRESHOLD}
MEMORY_THRESHOLD=${MEMORY_THRESHOLD}
STORAGE_THRESHOLD=${STORAGE_THRESHOLD}
TEMP_THRESHOLD=${TEMP_THRESHOLD}
TEMP_CRITICAL=${TEMP_CRITICAL}

# Serveur
MONITORED_SERVER=${MONITORED_SERVER}
EOF

    chmod 600 "$ENV_FILE"
    echo ""
    echo ".env créé avec succès (permissions 600)."
fi

# Installation du service systemd
echo ""
read -p "Installer le service systemd ? [o/N] : " INSTALL_SERVICE
if [[ "$INSTALL_SERVICE" =~ ^[oO]$ ]]; then
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    PYTHON_BIN="$(which python3)"
    SERVICE_USER="$(whoami)"

    SERVICE_FILE="/etc/systemd/system/rpi-monitor.service"

    sudo tee "$SERVICE_FILE" > /dev/null <<SERVICE
[Unit]
Description=RPI Monitor - Surveillance des ressources
After=network.target

[Service]
Type=simple
User=${SERVICE_USER}
WorkingDirectory=${SCRIPT_DIR}
ExecStart=${PYTHON_BIN} ${SCRIPT_DIR}/monitor.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SERVICE

    sudo systemctl daemon-reload
    sudo systemctl enable rpi-monitor
    sudo systemctl start rpi-monitor

    echo ""
    echo "Service installé et démarré."
    echo "  Statut  : sudo systemctl status rpi-monitor"
    echo "  Logs    : sudo journalctl -u rpi-monitor -f"
fi
