import json
import os
import sys

import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QTextEdit, QHBoxLayout, QMessageBox
)
from cbm_engine.reports import generate_report
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from cbm_engine.utils import analyze_and_get_results, load_sensor_data


class CBMAnalyzerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CBM Analyzer v2")
        self.resize(800, 600)

        self.layout = QVBoxLayout()

        self.label = QLabel("📂 Aucune analyse en cours")
        self.label.setStyleSheet("color: grey")

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)

        self.canvas = FigureCanvas(plt.Figure(figsize=(5, 3)))

        # Buttons
        button_layout = QHBoxLayout()
        self.analyze_button = QPushButton("📊 Analyser un fichier")
        self.report_button = QPushButton("📄 Exporter en PDF")
        self.compare_button = QPushButton("📁 Comparer plusieurs fichiers")

        self.analyze_button.clicked.connect(self.choose_and_analyze_file)
        self.report_button.clicked.connect(self.export_pdf)
        self.compare_button.clicked.connect(self.compare_files)

        button_layout.addWidget(self.analyze_button)
        button_layout.addWidget(self.report_button)
        button_layout.addWidget(self.compare_button)

        self.layout.addWidget(self.label)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.result_box)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)
        self.current_file = None

    def choose_and_analyze_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Ouvrir fichier capteur", "", "Fichiers JSON (*.json)")
        if not file_path:
            return

        self.current_file = file_path
        self.label.setText(f"📂 Fichier choisi : {file_path}")
        self.label.setStyleSheet("color: blue")
        self.result_box.clear()
        self.result_box.append("⏳ Analyse en cours...\n")

        try:
            results = analyze_and_get_results(file_path)
            self.result_box.append("✅ Analyse terminée !\n")
            self.result_box.append(json.dumps(results, indent=2, ensure_ascii=False))
            self.label.setStyleSheet("color: green")
            self.plot_fft(results['fft'])
        except Exception as e:
            self.label.setText(f"❌ Erreur : {str(e)}")
            self.label.setStyleSheet("color: red")

    def export_pdf(self):
        if not self.current_file:
            QMessageBox.warning(self, "Aucun fichier", "Veuillez analyser un fichier avant d'exporter.")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le rapport PDF", "report.pdf", "PDF (*.pdf)")
        if save_path:
            try:
                generate_report(self.current_file, save_path)
                QMessageBox.information(self, "Succès", f"Rapport PDF généré :\n{save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de génération : {str(e)}")

    def plot_fft(self, fft_data):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(fft_data, marker='o')
        ax.set_title("Spectre FFT (top 10)")
        ax.set_ylabel("Amplitude")
        ax.set_xlabel("Fréquence (échelle normalisée)")
        self.canvas.draw()

    def compare_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Sélectionner plusieurs fichiers JSON", "", "JSON (*.json)")
        if not files:
            return

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)

        for f in files:
            try:
                signal = load_sensor_data(f)
                all_accel = []
                for s in signal:
                    all_accel.extend(s['data']['acceleration'])
                fft_vals = analyze_and_get_results(f)['fft']
                ax.plot(fft_vals, label=os.path.basename(f))
            except Exception as e:
                print(f"Erreur fichier {f}: {e}")

        ax.set_title("Comparaison FFT")
        ax.set_ylabel("Amplitude")
        ax.set_xlabel("Fréquence")
        ax.legend()
        self.canvas.draw()


def launch_gui():
    app = QApplication(sys.argv)
    gui = CBMAnalyzerGUI()
    gui.show()
    sys.exit(app.exec())
