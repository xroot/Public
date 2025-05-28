# cbmcli.py

import argparse
import json
from cbm_engine.analyzer import compute_rms, detect_threshold, compute_fft
from cbm_engine.migration import migrated_rms


def load_sensor_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data.get("vibration", [])


def analyze(filepath):
    signal = load_sensor_data(filepath)

    print(f"\n[📊] Analyse du fichier : {filepath}")
    print("-" * 40)

    rms = compute_rms(signal)
    fft_vals = compute_fft(signal)
    alert = detect_threshold(rms, threshold=0.6)

    print(f"🔹 RMS : {rms:.4f}")
    print(f"🔹 Alerte seuil : {'⚠️ OUI' if alert else '✅ NON'}")
    print(f"🔹 FFT (10 premiers) : {fft_vals[:10]}")
    print("\n🧪 Comparaison avec RMS migré de MATLAB...")
    print(f"🔹 RMS migré : {migrated_rms(signal):.4f}")


def main():
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
