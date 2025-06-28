# main.py (mis à jour)

import os
import sys

from PySide6.QtCore import QFile
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget

from controllers.camera_page import CameraPage
# --- Importe tes pages/contrôleurs ---
from controllers.face_manager import FaceManagerPage
from tools.ui_loader import load_ui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = load_ui("ui/main_window.ui")
        if not self.main_widget:
            sys.exit("Impossible de charger l'interface principale. Arrêt.")

        self.setCentralWidget(self.main_widget.centralWidget())
        self.setWindowTitle("AnyEye v1.0 - xRootMiel Edition")
        self.resize(1024, 768)

        self.pages_widget = self.findChild(QStackedWidget, "pagesWidget")
        if not self.pages_widget:
            sys.exit("Erreur: 'pagesWidget' (QStackedWidget) non trouvé dans main_window.ui. Vérifie le nom.")

        # Créer les instances des pages
        self.camera_page = CameraPage()
        self.face_manager_page = FaceManagerPage()
        self.history_page = QWidget()
        self.settings_page = QWidget()

        # Ajouter les pages au QStackedWidget
        self.pages_widget.addWidget(self.camera_page)
        self.pages_widget.addWidget(self.face_manager_page)
        self.pages_widget.addWidget(self.history_page)
        self.pages_widget.addWidget(self.settings_page)

        # Connecter les boutons du menu
        self.findChild(QWidget, "btnCamera").clicked.connect(
            lambda: self.pages_widget.setCurrentWidget(self.camera_page))
        self.findChild(QWidget, "btnFaces").clicked.connect(
            lambda: self.pages_widget.setCurrentWidget(self.face_manager_page))
        self.findChild(QWidget, "btnHistory").clicked.connect(
            lambda: self.pages_widget.setCurrentWidget(self.history_page))
        self.findChild(QWidget, "btnSettings").clicked.connect(
            lambda: self.pages_widget.setCurrentWidget(self.settings_page))

        # Définir la page de démarrage
        self.pages_widget.setCurrentWidget(self.camera_page)

        self.apply_stylesheet("ui/dark.qss")

    def apply_stylesheet(self, path):
        style_file = QFile(path)
        if style_file.open(QFile.ReadOnly | QFile.Text):
            stream = style_file.readAll()
            self.setStyleSheet(stream.data().decode("utf-8"))
            style_file.close()
        else:
            print(f"Avertissement: Impossible de charger le fichier de style '{path}'")


if __name__ == "__main__":
    # S'assurer que les chemins relatifs fonctionnent correctement
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
