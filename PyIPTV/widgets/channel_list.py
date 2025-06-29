import os
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal

class ChannelListItem(QWidget):
    favoriteToggled = Signal(str, bool)  # nom chaîne, nouvel état favori

    def __init__(self, logo_path, country_flag_path, country_name, channel_name, resolution, availability, is_favorite=False, parent=None):
        super().__init__(parent)

        self.channel_name = channel_name
        self.is_favorite = is_favorite

        # Logo chaîne
        self.logo_label = QLabel()
        if logo_path and os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(64, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        else:
            self.logo_label.setText("No logo")

        # Drapeau + pays
        self.flag_label = QLabel()
        if country_flag_path and os.path.exists(country_flag_path):
            flag_pix = QPixmap(country_flag_path).scaled(24, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.flag_label.setPixmap(flag_pix)
        else:
            self.flag_label.setText(country_name or "")

        self.country_label = QLabel(country_name)

        # Nom + résolution
        self.name_label = QLabel(f"{channel_name} ({resolution})")

        # Disponibilité
        self.availability_label = QLabel(availability)

        # Favori : étoile cliquable
        self.favorite_label = QLabel("★" if is_favorite else "☆")
        self.favorite_label.setStyleSheet("color: gold; font-weight: bold; font-size: 18px;")
        self.favorite_label.setCursor(Qt.PointingHandCursor)
        self.favorite_label.mousePressEvent = self.toggle_favorite  # clic sur l’étoile

        # Layouts
        text_layout = QVBoxLayout()
        text_layout.addWidget(self.name_label)
        text_layout.addWidget(self.availability_label)

        left_layout = QHBoxLayout()
        left_layout.addWidget(self.logo_label)
        left_layout.addSpacing(5)
        left_layout.addWidget(self.flag_label)
        left_layout.addWidget(self.country_label)
        left_layout.addSpacing(10)
        left_layout.addLayout(text_layout)
        left_layout.addStretch()
        left_layout.addWidget(self.favorite_label)

        self.setLayout(left_layout)

    def toggle_favorite(self, event):
        self.is_favorite = not self.is_favorite
        self.favorite_label.setText("★" if self.is_favorite else "☆")
        self.favoriteToggled.emit(self.channel_name, self.is_favorite)
