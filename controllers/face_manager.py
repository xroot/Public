# controllers/face_manager.py (mis à jour)

import cv2
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QMessageBox, QVBoxLayout

from services import faces_storage
from tools.ui_loader import load_ui


class FaceManagerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = load_ui("ui/face_manager.ui")
        if not self.ui:
            return

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)
        self.setLayout(layout)

        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.current_frame = None
        self.captured_image = None

        self.ui.captureButton.clicked.connect(self.capture_image)
        self.ui.addButton.clicked.connect(self.add_face)

        self.refresh_faces_list()

    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            self.timer.start(30)
            print("INFO: Caméra de gestion des visages démarrée.")
        else:
            print("ERREUR: Caméra de gestion non accessible.")
            self.ui.previewLabel.setText("Caméra non disponible")

    def stop_camera(self):
        self.timer.stop()
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            print("INFO: Caméra de gestion des visages arrêtée.")

    def update_frame(self):
        if self.cap is None or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.ui.previewLabel.setPixmap(
                pixmap.scaled(self.ui.previewLabel.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def capture_image(self):
        if self.current_frame is not None:
            self.captured_image = self.current_frame.copy()
            self.timer.stop()

            rgb_image = cv2.cvtColor(self.captured_image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.ui.previewLabel.setPixmap(
                pixmap.scaled(self.ui.previewLabel.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def add_face(self):
        name = self.ui.nameLineEdit.text().strip()
        if not name:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir un nom.")
            return
        if self.captured_image is None:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord capturer une image.")
            return

        path = faces_storage.save_face_image(name, self.captured_image)
        QMessageBox.information(self, "Succès", f"Visage pour '{name}' sauvegardé.")

        self.ui.nameLineEdit.clear()
        self.captured_image = None
        self.refresh_faces_list()
        self.start_camera()

    def refresh_faces_list(self):
        self.ui.facesListWidget.clear()
        faces = faces_storage.list_faces()
        for name, imgs in faces.items():
            self.ui.facesListWidget.addItem(f"{name} ({len(imgs)} photo(s))")

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_faces_list()
        self.start_camera()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.stop_camera()
