from cbm_engine.utils import safe_print

# -*- coding: utf-8 -*-

safe_print(r"""

 ▄████▄   ▄▄▄▄    ███▄ ▄███▓   ▓█████  ███▄    █   ▄████  ██▓ ███▄    █ ▓█████ 
▒██▀ ▀█  ▓█████▄ ▓██▒▀█▀ ██▒   ▓█   ▀  ██ ▀█   █  ██▒ ▀█▒▓██▒ ██ ▀█   █ ▓█   ▀ 
▒▓█    ▄ ▒██▒ ▄██▓██    ▓██░   ▒███   ▓██  ▀█ ██▒▒██░▄▄▄░▒██▒▓██  ▀█ ██▒▒███   
▒▓▓▄ ▄██▒▒██░█▀  ▒██    ▒██    ▒▓█  ▄ ▓██▒  ▐▌██▒░▓█  ██▓░██░▓██▒  ▐▌██▒▒▓█  ▄ 
▒ ▓███▀ ░░▓█  ▀█▓▒██▒   ░██▒   ░▒████▒▒██░   ▓██░░▒▓███▀▒░██░▒██░   ▓██░░▒████▒
░ ░▒ ▒  ░░▒▓███▀▒░ ▒░   ░  ░   ░░ ▒░ ░░ ▒░   ▒ ▒  ░▒   ▒ ░▓  ░ ▒░   ▒ ▒ ░░ ▒░ ░
  ░  ▒   ▒░▒   ░ ░  ░      ░    ░ ░  ░░ ░░   ░ ▒░  ░   ░  ▒ ░░ ░░   ░ ▒░ ░ ░  ░
░         ░    ░ ░      ░         ░      ░   ░ ░ ░ ░   ░  ▒ ░   ░   ░ ░    ░   
░ ░       ░             ░         ░  ░         ░       ░  ░           ░    ░  ░
░              ░                                                               
                  Condition-Based Maintenance Engine (CBM Engine)
                by David PONDA E. | GitHub: https://github.com/xroot

                 CBM Stack - Analyse CLI des capteurs de vibrations

Ce script est le point d'entrée principal pour l'analyse des données de capteurs.
Il propose une interface en ligne de commande (CLI) pour :

- Générer ou régénérer les données de capteurs
- Lancer l'analyse RMS et détection de seuils
- Afficher le checksum MD5 du fichier capteur
- Spécifier un fichier de données personnalisé

Développé par : David PONDA E.
GitHub : https://github.com/xroot
Version : 1.0.0

Dave | 73 k0d3

Il fonctionne avec Click (UX CLI avancée) ou Argparse (fallback).
Utilisation CLI :
-----------------
$ python main.py [commande] [options]

Commandes disponibles :
  regen           Force la régénération du fichier capteurs.
  analyze         Lance l’analyse RMS + seuils pour chaque capteur.
  checksum        Affiche le hash MD5 du fichier.

Options (selon la commande) :
  --file PATH     Spécifie un fichier de capteurs à utiliser (par défaut : sensor_data/sensors_vibration.json).
  --output PATH   (pour regen) Chemin de sortie pour les données régénérées.
  
Exemples :
  python main.py run --regen      # Générer à nouveau les données
  python main.py run --analyze --file sensor_data/sensors_vibration.json  #Analyser les données depuis le fichier json
  python main.py run --checksum   # Afficher le checksum MD5 du fichier capteurs
""")

import os

try:
    import click

    USE_CLICK = True
except ImportError:
    import argparse

    USE_CLICK = False

from cbm_engine.utils import (
    load_sensor_data,
    file_checksum,
    analyze,
    regenerate_sensor_data,
    SENSOR_FILE
)

# ==================== CLICK ====================
if USE_CLICK:
    @click.group()
    def cli():
        """CLI CBM via Click"""
        pass


    @click.command()
    @click.option('--regen', is_flag=True, help="Régénérer les données capteurs")
    @click.option('--analyze', 'do_analyze', is_flag=True, help="Lancer l'analyse")  # renommer paramètre
    @click.option('--checksum', is_flag=True, help="Afficher le MD5")
    @click.option('--file', default=SENSOR_FILE, help="Chemin du fichier capteur")
    def run(regen, do_analyze, checksum, file):
        if regen:
            regenerate_sensor_data(file)

        if not os.path.exists(file):
            click.echo(f"[INFO] {file} non trouvé, génération automatique…")
            regenerate_sensor_data(file)

        if do_analyze:
            analyze(file)

        if checksum:
            click.echo(f"[INFO] Checksum MD5 : {file_checksum(file)}")


    cli.add_command(run)

    # Point d'entrée principal
    if __name__ == "__main__":
        cli()

# ==================== ARGPARSE (fallback) ====================
else:
    def main():
        parser = argparse.ArgumentParser(description="CBM Sensor Analysis CLI")
        parser.add_argument("--regen", action="store_true", help="Force la régénération")
        parser.add_argument("--analyze", action="store_true", help="Analyse les données")
        parser.add_argument("--checksum", action="store_true", help="Checksum MD5")
        parser.add_argument("--file", type=str, default=SENSOR_FILE, help="Fichier à utiliser")

        args = parser.parse_args()

        if args.regen:
            regenerate_sensor_data(args.file[0])

        if not os.path.exists(args.file[0]):
            print(f"[INFO] {args.file[0]} non trouvé, génération automatique...")
            regenerate_sensor_data(args.file[0])

        if args.analyze:
            data = load_sensor_data(args.file[0])
            analyze(data[0])

        if args.checksum:
            print(f"[INFO] Checksum MD5 : {file_checksum(args.file[0])}")

    if __name__ == "__main__":
        main()
# Exécution du script principal
# pour la stack CBM (Condition-Based Maintenance).
