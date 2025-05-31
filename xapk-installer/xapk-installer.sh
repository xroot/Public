#!/data/data/com.termux/files/usr/bin/bash

# ▓▓ XAPK Installer - by XROOT ▓▓
# Version: 1.0
# Description: Script interactif pour installer des fichiers APK via Termux, avec ou sans root.
# Auteur: Dave (XROOT)

TITLE="📲 XAPK Installer"
VERSION="1.0"

# Vérifie que 'dialog' est installé
command -v dialog >/dev/null 2>&1 || {
  echo "❌ 'dialog' n'est pas installé. Lance : pkg install dialog"
  exit 1
}

# Interface pour choisir un fichier APK
APK_PATH=$(dialog --title "$TITLE" --fselect $HOME/ 20 70 3>&1 1>&2 2>&3)

# Si l'utilisateur annule
if [ -z "$APK_PATH" ]; then
    clear
    echo "❌ Installation annulée."
    exit 1
fi

# Vérifie l'existence du fichier
if [ ! -f "$APK_PATH" ]; then
    dialog --title "$TITLE" --msgbox "❌ Fichier introuvable : $APK_PATH" 8 50
    clear
    exit 1
fi

# Détection root
IS_ROOT=$(id -u)
RESULT=1

if [ "$IS_ROOT" -eq 0 ]; then
    dialog --title "$TITLE" --infobox "⚙️ Installation avec 'pm install'..." 5 50
    pm install "$APK_PATH"
    RESULT=$?
else
    dialog --title "$TITLE" --infobox "👤 Installation sans root via Termux..." 5 50
    termux-open "$APK_PATH"
    RESULT=$?
fi

# Résultat final
clear
if [ "$RESULT" -eq 0 ]; then
    dialog --title "$TITLE" --msgbox "✅ L'installation a été lancée avec succès !" 7 50
else
    dialog --title "$TITLE" --msgbox "❌ Échec de l'installation. Vérifie les permissions ou le fichier APK." 7 60
fi

clear
