# IPTV Dashboard (PySide6)

**Version :** 0.1 – Local IPTV Player Interface with EPG, Favorites, and Filters

## 🎯 Objectif

Créer un lecteur IPTV local sous forme d'application desktop en **Python** avec **PySide6**, intégrant la lecture de chaînes depuis une liste M3U, un guide TV (EPG), la gestion des favoris, et un filtrage par pays ou catégories.

Aucun serveur requis. Fonctionne en local avec les fichiers M3U et XML fournis par l'utilisateur.

---

## 📁 Structure du projet

```
PyIPTV/
├── main.py                             # Point d’entrée principal
│
├── ui/                                 # Interfaces Qt Designer
│   └── main_window.ui                  # UI principale
│
├── controllers/                        # Contrôleurs (interactions GUI / logique)
│   └── main_controller.py
│
├── models/                             # Modèles (objets métiers, parsing M3U)
│   └── playlist_model.py
│
├── services/                           # Services internes (lecteur, EPG, filtre)
│   ├── vlc_player.py                   # Contrôle du lecteur (VLC)
│   ├── epg_parser.py                   # Intégration EPG XMLTV/JSON
│   └── filter_service.py               # Filtrage pays / langue / catégorie
│
├── core/                               # Composants cœur logiques (config, cache, parsers)
│   ├── config.py                       # Chargement & sauvegarde des préférences utilisateur
│   └── epg.py                          # Gestion brute des données EPG
│
├── widgets/                            # Widgets personnalisés PySide6
│   ├── channel_list.py                 # Widget liste chaînes
│   └── video_widget.py                 # Zone vidéo VLC
│
├── resources/                          # Ressources statiques
│   ├── icons/                          # Icônes, logos, drapeaux
│   └── epg_cache.json                  # Cache local du guide TV
│
├── data/                               # Données utilisateurs
│   ├── channels.m3u                    # Liste brute des chaînes
│   └── favorites.json                  # Favoris utilisateur
│
├── assets/                             # Autres assets statiques (si besoin)
│   └── fonts/ or backgrounds/
│
├── README.md
├── requirements.txt
└── .gitignore
```

## ✅ Fonctionnalités prévues

| Fonction             | Description                                                             |
| -------------------- | ----------------------------------------------------------------------- |
| 🎥 Lecture IPTV      | Support M3U avec `python-vlc` ou `ffmpeg-python`                        |
| ⭐ Favoris            | Ajout/suppression de chaînes favorites dans un fichier local            |
| 🗓️ Guide TV (EPG)   | Intégration XMLTV ou JSON, avec cache et affichage dans l’interface     |
| 🌍 Tri dynamique     | Sélection des chaînes par pays, langue, ou catégorie via menu déroulant |
| 💻 Interface Qt      | Conçue avec PySide6 ou Qt Designer, thème responsive                    |
| 🌗 Mode clair/sombre | Thèmes via fichiers `.qss` pour adapter l’UI selon les préférences      |
| 🧩 Extensible        | Conception modulaire, facile à maintenir et à améliorer                 |

---

## 🚀 Étapes de développement

1. **Fenêtre principale vide (PySide6)**
2. **Chargement d’une liste M3U dans une QListView**
3. **Test de lecture via `python-vlc` ou `ffplay`**
4. **Création du fichier `favorites.json`**
5. **Implémentation du tri par pays/catégorie**
6. **Téléchargement et affichage d’un EPG**
7. **Création de thèmes clair/sombre**
8. **Ajout d’une UI traduisible (multilingue)**

---

## 🛠️ Dépendances

Fichier `requirements.txt` à générer (exemple :)

```
PySide6
python-vlc
m3u-parser
requests
lxml
```

---

## 📌 Objectifs futurs (roadmap)

* [ ] Packaging portable (`pyinstaller`, `.exe` Windows ou `.AppImage` Linux)
* [ ] Système de profils utilisateurs
* [ ] Export/import de listes M3U
* [ ] Mode plein écran + PIP
* [ ] Mise à jour automatique de l'EPG

---

## 📷 Capture d’écran (à venir)

Interface en cours de conception.

---

## 🧠 Auteur

**Dave | th3 k0D3**

Projet propulsé par passion, café et PySide6 ☕🐍
