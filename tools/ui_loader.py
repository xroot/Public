# utils/ui_loader.py

import os

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader


def load_ui(path):
    """
    Charge un fichier .ui de manière sécurisée et retourne le widget.
    Gère les chemins relatifs pour que cela fonctionne de n'importe où.
    """
    # Construit un chemin absolu pour éviter les problèmes de répertoire de travail
    absolute_path = os.path.abspath(path)

    loader = QUiLoader()
    ui_file = QFile(absolute_path)

    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Erreur critique: Impossible d'ouvrir le fichier UI '{absolute_path}': {ui_file.errorString()}")
        return None

    widget = loader.load(ui_file)
    ui_file.close()

    if not widget:
        print(f"Erreur critique: Impossible de charger le fichier UI depuis '{absolute_path}'")
        return None

    return widget
