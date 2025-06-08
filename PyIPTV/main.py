import sys
import re
import emoji
import requests
from PySide6.QtCore import QFile, QTimer, Qt
from PySide6.QtGui import QPixmap, QKeySequence
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidget, QLineEdit, QPushButton, QStatusBar,
    QLabel, QSlider, QFileDialog, QListWidgetItem, QTextEdit, QTableWidget,
    QTableWidgetItem, QMenuBar, QMenu, QAction, QMessageBox
)
from controllers.player_controller import PlayerController
from utils.epg_parser import parse_epg  # À créer, voir plus bas

def country_code_to_emoji(code):
    if isinstance(code, str) and len(code) == 2:
        return chr(0x1F1E6 + ord(code[0].upper()) - ord('A')) + chr(0x1F1E6 + ord(code[1].upper()) - ord('A'))
    return '📺'

def extract_flag_and_name(text):
    parts = text.split()
    flag = parts[0] if parts and emoji.is_emoji(parts[0]) else '📺'
    name = ' '.join(parts[1:]) if flag != '📺' else text
    return flag, name

class IPTVApp:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("ui/main_window.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Impossible d'ouvrir le fichier UI")
        self.ui = loader.load(ui_file)
        ui_file.close()

        # Widgets
        self.videoWidget = self.ui.findChild(QWidget, "videoFrame")
        self.channelsList = self.ui.findChild(QListWidget, "channelsList")
        self.searchBar = self.ui.findChild(QLineEdit, "searchBar")
        self.clearSearchButton = self.ui.findChild(QPushButton, "clearSearchButton")
        self.openFileButton = self.ui.findChild(QPushButton, "openFileButton")
        self.playButton = self.ui.findChild(QPushButton, "playButton")
        self.pauseButton = self.ui.findChild(QPushButton, "pauseButton")
        self.stopButton = self.ui.findChild(QPushButton, "stopButton")
        self.statusBar = self.ui.findChild(QStatusBar, "statusbar")
        self.statusLabel = self.ui.findChild(QLabel, "statusLabel")
        self.volumeSlider = self.ui.findChild(QSlider, "volumeSlider")
        self.muteButton = self.ui.findChild(QPushButton, "muteButton")
        self.progressSlider = self.ui.findChild(QSlider, "progressSlider")
        self.urlLineEdit = self.ui.findChild(QLineEdit, "urlLineEdit")
        self.logoLabel = self.ui.findChild(QLabel, "logoLabel")
        self.epgWidget = self.ui.findChild(QTextEdit, "epgWidget")
        self.menuBar = self.ui.findChild(QMenuBar, "menubar")

        # Contrôleur vidéo
        self.controller = PlayerController(self.videoWidget, self.update_status)
        self.channel_items = []  # [(name, url, flag, logo_url, tvg_id)]

        # EPG
        self.epg_data = {}  # {tvg_id: [programs]}
        self.epg_loaded = False

        # Menus (ajoute dynamiquement si pas dans le .ui)
        if not self.menuBar:
            self.menuBar = QMenuBar(self.ui)
            self.ui.setMenuBar(self.menuBar)
        self.init_menus()

        # Connexions signaux/slots
        self.clearSearchButton.clicked.connect(lambda: self.searchBar.clear())
        self.openFileButton.clicked.connect(self.open_m3u_file)
        self.playButton.clicked.connect(self.play_selected_channel)
        self.pauseButton.clicked.connect(self.controller.pause)
        self.stopButton.clicked.connect(self.controller.stop)
        self.searchBar.textChanged.connect(self.filter_channels)
        self.channelsList.itemClicked.connect(self.channel_selected)
        self.channelsList.itemDoubleClicked.connect(self.channel_selected)
        self.volumeSlider.valueChanged.connect(self.controller.set_volume)
        self.muteButton.clicked.connect(self.controller.mute)
        self.progressSlider.sliderReleased.connect(self.on_seek)
        self.progressSlider.sliderPressed.connect(self.on_slider_pressed)
        self.progressSlider.sliderReleased.connect(self.on_slider_released)
        self.urlLineEdit.returnPressed.connect(self.play_url_from_input)

        # Gestion du slider de progression
        self.slider_is_pressed = False
        self.progressSlider.setRange(0, 100)
        self.progress_timer = QTimer(self.ui)
        self.progress_timer.timeout.connect(self.update_progress_slider)
        self.progress_timer.start(500)

        # Raccourcis clavier
        self.ui.keyPressEvent = self.keyPressEvent

    def init_menus(self):
        file_menu = self.menuBar.addMenu("&Fichier")
        open_action = QAction("Ouvrir M3U", self.ui)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_m3u_file)
        file_menu.addAction(open_action)
        open_epg_action = QAction("Ouvrir EPG...", self.ui)
        open_epg_action.triggered.connect(self.open_epg_file)
        file_menu.addAction(open_epg_action)
        file_menu.addSeparator()
        quit_action = QAction("Quitter", self.ui)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(QApplication.quit)
        file_menu.addAction(quit_action)

        help_menu = self.menuBar.addMenu("&Aide")
        about_action = QAction("À propos", self.ui)
        about_action.triggered.connect(lambda: QMessageBox.about(self.ui, "À propos", "IPTV Player - PySide6 + VLC"))
        help_menu.addAction(about_action)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.controller.pause()
        elif event.key() == Qt.Key_F:
            self.toggle_fullscreen()
        elif event.key() == Qt.Key_Right:
            self.controller.seek_relative(10)  # +10s
        elif event.key() == Qt.Key_Left:
            self.controller.seek_relative(-10)  # -10s
        elif event.key() == Qt.Key_Up:
            self.volumeSlider.setValue(min(self.volumeSlider.value() + 5, 100))
        elif event.key() == Qt.Key_Down:
            self.volumeSlider.setValue(max(self.volumeSlider.value() - 5, 0))
        else:
            super().keyPressEvent(event)

    def toggle_fullscreen(self):
        if self.ui.isFullScreen():
            self.ui.showNormal()
        else:
            self.ui.showFullScreen()

    def on_slider_pressed(self):
        self.slider_is_pressed = True

    def on_slider_released(self):
        self.slider_is_pressed = False
        self.on_seek()

    def update_progress_slider(self):
        # Fix bug VLC: get_length() mauvais? Ne rien faire si durée anormale
        if self.controller.is_playing() and not self.slider_is_pressed:
            length = self.controller.player.get_length()
            if length is not None and length > 0:
                pos = self.controller.player.get_time() / length
                if 0 <= pos <= 1:
                    self.progressSlider.setValue(int(pos * 100))

    def on_seek(self):
        length = self.controller.player.get_length()
        if length is not None and length > 0:
            pos = self.progressSlider.value() / 100
            self.controller.seek(pos)

    def update_status(self, message):
        if self.statusBar:
            self.statusBar.showMessage(message)
        if self.statusLabel:
            self.statusLabel.setText(f"Statut : {message}")

    def open_m3u_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self.ui, "Ouvrir un fichier M3U", "", "Fichiers M3U (*.m3u *.m3u8)"
        )
        if filename:
            self.load_channels_from_m3u(filename)

    def open_epg_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self.ui, "Ouvrir un fichier EPG XMLTV", "", "Fichiers XML (*.xml)"
        )
        if filename:
            self.epg_data = parse_epg(filename)
            self.epg_loaded = True
            self.update_status("EPG chargé.")

    def load_channels_from_m3u(self, filepath):
        self.channel_items.clear()
        self.channelsList.clear()
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                if lines[i].startswith('#EXTINF'):
                    name_match = re.search(r',(.+)', lines[i])
                    url = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    name = name_match.group(1).strip() if name_match else f"Chaîne {i}"
                    flag_match = re.search(r'tvg-country="([^"]+)"', lines[i])
                    logo_match = re.search(r'tvg-logo="([^"]+)"', lines[i])
                    tvg_id_match = re.search(r'tvg-id="([^"]+)"', lines[i])
                    flag_code = flag_match.group(1) if flag_match else ''
                    flag = country_code_to_emoji(flag_code) if flag_code else '📺'
                    logo_url = logo_match.group(1) if logo_match else ''
                    tvg_id = tvg_id_match.group(1) if tvg_id_match else ''
                    self.channel_items.append((name, url, flag, logo_url, tvg_id))
                    item = QListWidgetItem(f"{flag} {name}")
                    self.channelsList.addItem(item)
        self.update_status(f"{len(self.channel_items)} chaînes chargées.")

    def filter_channels(self, text):
        text = text.lower()
        self.channelsList.clear()
        for name, url, flag, logo_url, tvg_id in self.channel_items:
            if text in name.lower():
                self.channelsList.addItem(QListWidgetItem(f"{flag} {name}"))

    def channel_selected(self, item):
        flag, name = extract_flag_and_name(item.text())
        for n, url, f, logo_url, tvg_id in self.channel_items:
            if n == name:
                # Affichage logo
                self.show_channel_logo(logo_url)
                # Lecture vidéo
                self.controller.play(url)
                # Affichage EPG
                if self.epg_loaded and tvg_id:
                    self.show_epg(tvg_id)
                else:
                    if self.epgWidget:
                        self.epgWidget.setText("Aucun EPG disponible.")
                break

    def show_channel_logo(self, logo_url):
        if not self.logoLabel:
            return
        if logo_url.startswith("http"):
            try:
                resp = requests.get(logo_url, timeout=5)
                if resp.ok:
                    pixmap = QPixmap()
                    pixmap.loadFromData(resp.content)
                    self.logoLabel.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    self.logoLabel.clear()
            except Exception:
                self.logoLabel.clear()
        else:
            self.logoLabel.clear()

    def show_epg(self, tvg_id):
        if not self.epgWidget:
            return
        progs = self.epg_data.get(tvg_id, [])
        if not progs:
            self.epgWidget.setText("Aucun EPG trouvé pour cette chaîne.")
            return
        lines = []
        for prog in progs[:10]:  # Affiche les 10 prochains
            lines.append(f"{prog['start']} - {prog['stop']}: {prog['title']}")
        self.epgWidget.setText('\n'.join(lines))

    def play_selected_channel(self):
        item = self.channelsList.currentItem()
        if item:
            self.channel_selected(item)

    def play_url_from_input(self):
        url = self.urlLineEdit.text().strip()
        if url:
            self.controller.play(url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    iptv = IPTVApp()
    iptv.ui.show()
    sys.exit(app.exec())