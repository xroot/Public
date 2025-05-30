# main_cli.py

import argparse

from cbm_engine.utils import (
    analyze,
    regenerate_sensor_data,
    file_checksum,
    generate_report,
    SENSOR_FILE
)


def main():
    parser = argparse.ArgumentParser(description="CBM CLI - Condition-Based Maintenance")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- analyze / run ---
    analyze_parser = subparsers.add_parser("analyze", aliases=["run"], help="Analyser un fichier capteur")
    analyze_parser.add_argument("--file", required=False, help=f"Fichier JSON à analyser (défaut : {SENSOR_FILE})")

    # --- regen ---
    regen_parser = subparsers.add_parser("regen", help="Regénère les données capteurs JSON")
    regen_parser.add_argument("--file", required=False, help=f"Fichier cible (défaut : {SENSOR_FILE})")

    # --- checksum ---
    checksum_parser = subparsers.add_parser("checksum", help="Calcule le hash MD5 d’un fichier")
    checksum_parser.add_argument("--file", required=True, help="Fichier à analyser")

    # --- report ---
    report_parser = subparsers.add_parser("report", help="Génère un rapport PDF")
    report_parser.add_argument("--file", required=False, help=f"Fichier JSON (défaut : {SENSOR_FILE})")
    report_parser.add_argument("--output", required=False, help="Nom du fichier PDF de sortie (défaut: report.pdf)")

    args = parser.parse_args()

    # Analyse
    if args.command in ["analyze", "run"]:
        filepath = args.file if args.file else SENSOR_FILE
        analyze(filepath)

    # Regeneration
    elif args.command == "regen":
        filepath = args.file if args.file else SENSOR_FILE
        regenerate_sensor_data(filepath)

    # Checksum
    elif args.command == "checksum":
        checksum = file_checksum(args.file)
        print(f"[🔒] Checksum MD5 de '{args.file}' : {checksum}")

    # # Rapport PDF
    elif args.command == "report":
        filepath = args.file if args.file else SENSOR_FILE
        output = args.output if args.output else "report.pdf"
        generate_report(filepath, output)
