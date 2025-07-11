import json
import os
import re
import sys

import requests
from PySide6.QtCore import QFile, Qt, QPoint
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidgetItem, QFileDialog, QMenu
)

from core.player_controller import PlayerController
from widgets.channel_list import ChannelListItem
from PySide6.QtWidgets import QListWidgetItem



class IPTVApp:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("ui/main_window.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Impossible d'ouvrir le fichier UI")
        self.ui = loader.load(ui_file)
        ui_file.close()

        # Widgets principaux
        self.searchBar = self.ui.findChild(QWidget, "searchBar")
        self.filterCountry = self.ui.findChild(QWidget, "filterCountry")
        self.filterCategory = self.ui.findChild(QWidget, "filterCategory")
        self.channelsList = self.ui.findChild(QWidget, "channelsList")
        self.logoLabel = self.ui.findChild(QWidget, "logoLabel")
        self.videoWidget = self.ui.findChild(QWidget, "videoFrame")
        self.playButton = self.ui.findChild(QWidget, "playButton")
        self.pauseButton = self.ui.findChild(QWidget, "pauseButton")
        self.stopButton = self.ui.findChild(QWidget, "stopButton")
        self.volumeSlider = self.ui.findChild(QWidget, "volumeSlider")
        self.muteButton = self.ui.findChild(QWidget, "muteButton")
        self.progressSlider = self.ui.findChild(QWidget, "progressSlider")
        self.epgWidget = self.ui.findChild(QWidget, "epgWidget")
        self.favoritesList = self.ui.findChild(QWidget, "favoritesList")

        # Bouton ouvrir fichier M3U
        self.openFileButton = self.ui.findChild(QWidget, "openFileButton")

        # Contrôleur VLC
        self.controller = PlayerController(self.videoWidget, self.update_status)

        # Données internes
        self.channel_items = []  # (name, url, country, category, logo, tvg_id)
        self.epg_data = {}
        self.epg_loaded = False
        self.favorites = set()

        self.load_favorites()

        # Connexions
        if self.openFileButton:
            self.openFileButton.clicked.connect(self.open_m3u_file)

        self.playButton.clicked.connect(self.play_selected_channel)
        self.pauseButton.clicked.connect(self.controller.pause)
        self.stopButton.clicked.connect(self.controller.stop)
        self.muteButton.clicked.connect(self.controller.mute)
        self.volumeSlider.valueChanged.connect(self.controller.set_volume)
        self.progressSlider.sliderReleased.connect(self.seek_video)
        self.searchBar.textChanged.connect(self.filter_display)
        self.filterCountry.currentTextChanged.connect(self.filter_display)
        self.filterCategory.currentTextChanged.connect(self.filter_display)
        self.channelsList.itemDoubleClicked.connect(self.channel_selected)
        self.channelsList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.channelsList.customContextMenuRequested.connect(self.show_context_menu)

    def update_status(self, msg):
        print("[STATUS]", msg)

    def load_favorites(self):
        try:
            with open("data/favorites.json", "r", encoding="utf-8") as f:
                self.favorites = set(json.load(f))
        except Exception:
            self.favorites = set()

    def save_favorites(self):
        with open("data/favorites.json", "w", encoding="utf-8") as f:
            json.dump(list(self.favorites), f, indent=2)

    def open_m3u_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self.ui,
            "Ouvrir un fichier M3U",
            "data/",
            "Fichiers M3U (*.m3u *.m3u8)"
        )
        if filename:
            self.load_m3u(filename)
            self.update_status(f"Fichier M3U chargé : {filename}")

    def load_m3u(self, filepath):
        self.channel_items.clear()
        self.channelsList.clear()
        countries = set()
        categories = set()

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    name = re.search(r",(.+)", lines[i])
                    name = name.group(1).strip() if name else f"Channel {i}"
                    url = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    country = re.search(r'tvg-country="([^"]+)"', lines[i])
                    category = re.search(r'group-title="([^"]+)"', lines[i])
                    logo = re.search(r'tvg-logo="([^"]+)"', lines[i])
                    tvg_id = re.search(r'tvg-id="([^"]+)"', lines[i])

                    country = country.group(1) if country else "Unknown"
                    category = category.group(1) if category else "General"
                    logo_url = logo.group(1) if logo else ""
                    tvg_id = tvg_id.group(1) if tvg_id else ""

                    countries.add(country)
                    categories.add(category)

                    self.channel_items.append((name, url, country, category, logo_url, tvg_id))

        self.filterCountry.clear()
        self.filterCategory.clear()
        self.filterCountry.addItem("Tous")
        self.filterCategory.addItem("Tous")
        self.filterCountry.addItems(sorted(countries))
        self.filterCategory.addItems(sorted(categories))

        self.filter_display()

    def filter_display(self):
        text = self.searchBar.text().lower()
        selected_country = self.filterCountry.currentText()
        selected_category = self.filterCategory.currentText()

        self.channelsList.clear()

        for name, url, country, category, logo_url, tvg_id in self.channel_items:
            if text in name.lower():
                if selected_country != "Tous" and country != selected_country:
                    continue
                if selected_category != "Tous" and category != selected_category:
                    continue
                item = QListWidgetItem(name)
                flag_path = f"resources/icons/flags/{country.lower()}.png"
                if os.path.exists(flag_path):
                    item.setIcon(QIcon(flag_path))
                if name in self.favorites:
                    item.setForeground(Qt.red)
                self.channelsList.addItem(item)

    def channel_selected(self, item):
        name = item.text()
        for ch in self.channel_items:
            if ch[0] == name:
                self.show_logo(ch[4])
                self.controller.play(ch[1])
                if self.epg_loaded:
                    self.show_epg(ch[5])
                break

    def show_logo(self, logo_url):
        if logo_url.startswith("http"):
            try:
                r = requests.get(logo_url, timeout=5)
                if r.ok:
                    pixmap = QPixmap()
                    pixmap.loadFromData(r.content)
                    self.logoLabel.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            except:
                self.logoLabel.clear()
        else:
            self.logoLabel.clear()

    def show_epg(self, tvg_id):
        if not tvg_id or tvg_id not in self.epg_data:
            self.epgWidget.setText("EPG non disponible.")
            return
        lines = [f"{p['start']} - {p['stop']}: {p['title']}" for p in self.epg_data[tvg_id][:10]]
        self.epgWidget.setText("\n".join(lines))

    def play_selected_channel(self):
        item = self.channelsList.currentItem()
        if item:
            self.channel_selected(item)

    def seek_video(self):
        pos = self.progressSlider.value() / 100
        self.controller.seek(pos)

    def show_context_menu(self, pos: QPoint):
        item = self.channelsList.itemAt(pos)
        if not item:
            return

        menu = QMenu()
        name = item.text()
        if name in self.favorites:
            remove_action = QAction("Supprimer des favoris", self.ui)
            remove_action.triggered.connect(lambda: self.remove_favorite(name))
            menu.addAction(remove_action)
        else:
            add_action = QAction("Ajouter aux favoris", self.ui)
            add_action.triggered.connect(lambda: self.add_favorite(name))
            menu.addAction(add_action)

        menu.exec(self.channelsList.mapToGlobal(pos))

    def add_favorite(self, name):
        self.favorites.add(name)
        self.save_favorites()
        self.filter_display()

    def remove_favorite(self, name):
        self.favorites.discard(name)
        self.save_favorites()
        self.filter_display()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 🌙 Appliquer le style sombre si présent
    qss_path = os.path.join("resources", "themes", "dark.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())

    window = IPTVApp()
    window.ui.show()
    sys.exit(app.exec())
