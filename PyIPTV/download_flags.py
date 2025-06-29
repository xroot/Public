# download_flags.py

import os
import re

import requests

# Dossier de destination
FLAGS_DIR = "resources/icons/flags/"
os.makedirs(FLAGS_DIR, exist_ok=True)

# URL base de FlagCDN
CDN_BASE = "https://flagcdn.com"

# Taille recommandée (ex: 48px de haut)
SIZE = "48x36"

# Fichier M3U source
M3U_FILE = "data/channels.m3u"


def extract_country_codes(m3u_path):
    with open(m3u_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    codes = re.findall(r'tvg-country="([A-Za-z]{2})"', content)
    return sorted(set(code.lower() for code in codes))


def download_flag(code):
    url = f"{CDN_BASE}/{SIZE}/{code}.png"
    dest_path = os.path.join(FLAGS_DIR, f"{code}.png")
    if os.path.exists(dest_path):
        print(f"[✔] {code}.png déjà présent.")
        return
    try:
        response = requests.get(url, timeout=10)
        if response.ok:
            with open(dest_path, "wb") as f:
                f.write(response.content)
            print(f"[+] {code}.png téléchargé.")
        else:
            print(f"[!] Échec téléchargement {code} ({response.status_code})")
    except Exception as e:
        print(f"[!] Erreur : {e}")


if __name__ == "__main__":
    print("📥 Téléchargement des drapeaux depuis FlagCDN...")
    codes = extract_country_codes(M3U_FILE)
    if not codes:
        print("Aucun code pays trouvé.")
    for code in codes:
        download_flag(code)
    print("✅ Terminé.")
