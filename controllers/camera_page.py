# controllers/camera_page.py

import cv2
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout

from tools.ui_loader import load_ui


class CameraPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = load_ui("ui/camera_page.ui")
        if not self.ui:
            return

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)
        self.setLayout(layout)

        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)

        if self.cap.isOpened():
            self.timer.start(30)  # ~33 FPS
            print("INFO: Caméra principale démarrée.")
        else:
            self.ui.videoFeedLabel.setText("Erreur: Impossible d'accéder à la caméra.")
            print("ERREUR: Caméra principale non accessible.")

    def stop_camera(self):
        self.timer.stop()
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            print("INFO: Caméra principale arrêtée.")

    def update_frame(self):
        if self.cap is None or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)

            self.ui.videoFeedLabel.setPixmap(pixmap.scaled(
                self.ui.videoFeedLabel.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

    def showEvent(self, event):
        super().showEvent(event)
        self.start_camera()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.stop_camera()
