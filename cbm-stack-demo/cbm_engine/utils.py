# ======================================
#   CBM Engine by Dave (David PONDA E.)
#   GitHub: https://github.com/xroot
# ======================================
#
# cbm_engine/utils.py
# --------------------
# Utilitaires pour la stack CBM (Condition-Based Maintenance)
# Inclut les fonctions de chargement, analyse, checksum
# et CLI simplifiée via argparse

SENSOR_FILE = "sensor_data/sensors_vibration.json"

__all__ = [
    "SENSOR_FILE",
    "load_sensor_data",
    "file_checksum",
    "regenerate_sensor_data"
]

import argparse
import hashlib
import json
import os
import sys

from cbm_engine.analyzer import compute_rms, detect_threshold, compute_fft
from cbm_engine.migration import migrated_rms


def load_sensor_data(filepath):
    """
    Charge les données JSON d’un fichier de capteurs.

    Args:
        filepath (str): Chemin vers le fichier JSON à charger.

    Returns:
        list: Liste de dictionnaires représentant chaque capteur.
    """
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data.get("vib", [])


def file_checksum(file_path):
    """
    Calcule le hash MD5 du fichier.

    Args:
        file_path (str): Chemin vers le fichier cible.

    Returns:
        str: Hash MD5 au format hexadécimal.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def regenerate_sensor_data(filepath):
    """
    Regénère les données des capteurs si le fichier est manquant ou corrompu.
    """
    from gen_captors import generate_all_sensors
    os.makedirs("sensor_data", exist_ok=True)
    with open(filepath, "w") as f:
        json.dump({"vib": generate_all_sensors()}, f, indent=2)
    print(f"[INFO] Données régénérées dans {filepath}")


def analyze(filepath):
    """
    Analyse les données d’un fichier capteur via RMS, FFT, seuils et comparaison RMS MATLAB.

    Args:
        filepath (str): Chemin vers le fichier JSON contenant les données capteur.
    """
    signal = load_sensor_data(filepath)

    print(f"\n[📊] Analyse du fichier : {filepath}")
    print("-" * 40)

    all_accel = []
    for sensor in signal:
        all_accel.extend(sensor['data']['acceleration'])

    rms = compute_rms(all_accel)
    fft_vals = compute_fft(all_accel)
    alert = detect_threshold(rms, threshold=0.6)

    print(f"🔹 RMS : {rms:.4f}")
    print(f"🔹 Alerte seuil : {'⚠️ OUI' if alert else '✅ NON'}")
    print(f"🔹 FFT (10 premiers) : {fft_vals[:10]}")
    print("\n🧪 Comparaison avec RMS migré de MATLAB...")
    print(f"🔹 RMS migré : {migrated_rms(all_accel):.4f}")


def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        encoded = text.encode('utf-8', errors='ignore').decode(sys.stdout.encoding, errors='ignore')
        print(encoded)


def main():
    """
    Interface CLI pour la stack CBM via argparse.

    Exemple d’utilisation :
    ------------------------
    $ python -m cbm_engine.utils analyze --file sensor_data/sensors_vibration.json
    """
    parser = argparse.ArgumentParser(description="CBM CLI - Condition-Based Maintenance")
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze", help="Analyser un fichier de données capteur")
    analyze_parser.add_argument("--file", required=True, help="Chemin du fichier JSON")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze(args.file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
