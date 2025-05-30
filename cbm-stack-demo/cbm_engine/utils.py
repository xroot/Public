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

import argparse
import hashlib
import json
import os
import sys
from argparse import ArgumentParser

from fpdf import FPDF

from cbm_engine.analyzer import compute_rms, detect_threshold, compute_fft
from cbm_engine.migration import migrated_rms

SENSOR_FILE = "sensor_data/sensors_vibration.json"

__all__ = [
    "SENSOR_FILE",
    "load_sensor_data",
    "file_checksum",
    "analyze",
    "regenerate_sensor_data",
    "safe_print",
    "generate_report",
    "analyze_and_get_results",
    "display_analysis_results",
    "analyze_and_get_results_from_file"
]


def load_sensor_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data.get("vib", [])


def file_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def regenerate_sensor_data(filepath):
    from gen_captors import generate_all_sensors
    os.makedirs("sensor_data", exist_ok=True)
    with open(filepath, "w") as f:
        json.dump({"vib": generate_all_sensors()}, f, indent=2)
    print(f"[INFO] Données régénérées dans {filepath}")


def analyze(filepath):
    global signal
    try:
        signal = load_sensor_data(filepath)
        print(f"Type signal : {type(signal)}")
        print(f"Premier capteur : {signal[0]}")
        print(f"Type de sensor[0]['data'] : {type(signal[0]['data'])}")

        print(f"\n[📊] Analyse du fichier : {filepath}")
        print("-" * 40)

        all_accel = []
        for sensor in signal:
            try:
                accel = sensor['data']['acceleration']
                if isinstance(accel, list):
                    all_accel.extend(accel)
                else:
                    print(f"[WARN] Données d'accélération invalides pour {sensor.get('sensor_id', '?')}")
            except (KeyError, TypeError) as e:
                print(f"[ERREUR] Sensor mal formé : {sensor} → {e}")

        rms = compute_rms(all_accel)
        fft_vals = compute_fft(all_accel)
        alert = detect_threshold(rms, threshold=0.6)

        print(f"🔹 RMS : {rms:.4f}")
        print(f"🔹 Alerte seuil : {'⚠️ OUI' if alert else '✅ NON'}")
        print(f"🔹 FFT (10 premiers) : {fft_vals[:10]}")
        print("\n🧪 Comparaison avec RMS migré de MATLAB...")
        print(f"🔹 RMS migré : {migrated_rms(all_accel):.4f}")

    except Exception as e:
        print(f"[ERREUR] {str(e)}")
        print(f"DEBUG - signal : {type(signal)} → {str(signal)[:100]}")


def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        encoded = text.encode('utf-8', errors='ignore').decode(sys.stdout.encoding, errors='ignore')
        print(encoded)


def analyze_and_get_results(data):
    """
    Analyse les données capteurs et retourne un dict structuré pour affichage ou export JSON.

    Args:
        data (list): Liste des données capteurs.

    Returns:
        dict: Résultats RMS, FFT, seuil et RMS MATLAB.
    """
    all_accel = []
    for sensor in data:
        all_accel.extend(sensor['data']['acceleration'])

    rms_val = compute_rms(all_accel)
    fft_val = compute_fft(all_accel)
    threshold_alert = bool(detect_threshold(rms_val, threshold=0.6))
    rms_migrated = migrated_rms(all_accel)

    return {
        "rms": round(rms_val, 4),
        "threshold_alert": threshold_alert,
        "fft": fft_val[:10].tolist(),  # 🔁 convertit ndarray → list
        "migrated_rms": round(rms_migrated, 4)
    }


def analyze_and_get_results_from_file(file_path):
    """
    Lit un fichier JSON et effectue l’analyse via analyze_and_get_results.

    Args:
        file_path (str): Chemin du fichier JSON contenant les données capteurs.

    Returns:
        dict: Résultats d’analyse.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # Cas 1 : structure {"vib": [...]}
    if "vib" in json_data:
        data = json_data["vib"]
    # Cas 2 : liste directe
    elif isinstance(json_data, list):
        data = json_data
    else:
        raise ValueError("Format JSON non reconnu : clé 'vib' manquante ou format invalide.")

    return analyze_and_get_results(data)


def display_analysis_results(results):
    """
    Affiche les résultats de l’analyse dans un format lisible en console.

    Args:
        results (dict): Résultats retournés par `analyze_and_get_results`.
    """
    safe_print("\n[📊] Résultats d'analyse capteur")
    safe_print("-" * 40)
    safe_print(f"🔹 RMS : {results['rms']:.4f}")
    safe_print(f"🔹 Alerte seuil : {'⚠️ OUI' if results['threshold_alert'] else '✅ NON'}")
    safe_print(f"🔹 FFT (10 premiers) : {results['fft']}")
    safe_print("\n🧪 Comparaison avec RMS migré de MATLAB...")
    safe_print(f"🔹 RMS migré : {results['migrated_rms']:.4f}")


def generate_report(filepath, output_path="report.pdf"):
    """
    Génère un rapport PDF des résultats d’analyse.

    Args:
        filepath (str): Fichier JSON à analyser.
        output_path (str): Chemin du fichier PDF à créer.
    """
    signal = load_sensor_data(filepath)

    all_accel = []
    for sensor in signal:
        all_accel.extend(sensor['data']['acceleration'])

    rms = compute_rms(all_accel)
    fft_vals = compute_fft(all_accel)
    alert = bool(detect_threshold(rms, threshold=0.6))
    migrated = migrated_rms(all_accel)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Rapport d’Analyse CBM", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Fichier analysé : {filepath}", ln=True)
    pdf.cell(200, 10, txt=f"RMS : {rms:.4f}", ln=True)
    pdf.cell(200, 10, txt=f"Seuil d’alerte : {'OUI ⚠️' if alert else 'NON ✅'}", ln=True)
    pdf.cell(200, 10, txt=f"RMS migré (MATLAB) : {migrated:.4f}", ln=True)
    pdf.cell(200, 10, txt=f"FFT (10 premiers) : {fft_vals[:10]}", ln=True)

    pdf.output(output_path)
    print(f"[📄] Rapport PDF généré : {output_path}")


def main():
    parser: ArgumentParser = argparse.ArgumentParser(description="CBM CLI - Condition-Based Maintenance")
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze", help="Analyser un fichier de données capteur")
    analyze_parser.add_argument("--file", required=True, help="Chemin du fichier JSON")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze(args.file)
    else:
        parser.print_help()
