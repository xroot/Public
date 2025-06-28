anyeye/
├── ui/
│ ├── main_window.ui
│ ├── dark.qss
│ └── light.qss
├── controllers/
├── models/
├── services/
├── assets/
├── data/
├── main.py
├── README.md
├── setup.py
├── requirements.txt
└── .gitignore

# main.py (boot minimal PySide6)

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
import sys

app = QApplication(sys.argv)
loader = QUiLoader()
file = QFile("ui/main_window.ui")
file.open(QIODevice.ReadOnly)
window = loader.load(file)
file.close()
window.show()
sys.exit(app.exec())

# README.md

"""

# AnyEye v1.0

**AnyEye** est une application de reconnaissance faciale destinée à des environnements tels que des maisons, entreprises
ou lieux publics. Elle propose une interface épurée inspirée du style IPTV Smart TV PRO, et sera distribuée sous forme
de package PyPI.

## 🎯 Objectif principal

Détecter, reconnaître et enregistrer les visages en temps réel via webcam, caméra IP ou stream vidéo, avec une interface
claire.

## 🧩 Fonctionnalités prévues (MVP)

- **Live video feed** : Webcam / caméra IP avec affichage en direct.
- **Reconnaissance faciale** : via `face_recognition` et OpenCV.
- **Base d’utilisateurs** : Ajouter/supprimer des visages nommés.
- **Historique d’activité** : Log des visages reconnus avec timestamp et mini-photo.
- **Interface UI** : Thème sombre et clair avec navigation inspirée Smart IPTV.

## 🏗️ Structure du projet

```
anyeye/
├── ui/              # Interfaces .ui et thèmes .qss
├── controllers/     # Logique interface (PySide6)
├── models/          # Modèles d’identités, DB, reconnaissance
├── services/        # Capture vidéo, traitement
├── assets/          # Logos, icônes, photos
├── data/            # Visages enregistrés, logs
├── main.py          # Point d’entrée
├── README.md        # Cahier de charges & instructions
├── setup.py         # Pour PyPI
├── requirements.txt # Dépendances
```

## ⚙️ Stack technique

- PySide6
- OpenCV
- face_recognition (dlib)
- SQLite / JSON
- PyInstaller / build (packaging)

## 🔐 Sécurité & Respect de la vie privée

- Stockage local uniquement
- Base de visages chiffrable (future feature)
- Mode anonymisé optionnel

---
**Dave | th3 k0D3**

