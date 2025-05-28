# 🛠️ CBM Stack Demo – Condition-Based Maintenance Python Stack

## 📌 Objectif

Cette démonstration illustre la **migration d’algorithmes MATLAB vers Python** et la **construction d’une mini stack CBM (Condition-Based Maintenance)** exploitant des données de capteurs vibratoires. Elle montre aussi l’organisation propre d’un projet prêt à l’industrialisation (CI/CD, Docker, TDD).

---

## 📁 Structure du projet

```
cbm-stack-demo/
│
├── main.py                    → Point d’entrée du projet (lecture + analyse)
├── cbmcli.py                 → Interface CLI basique pour manipuler la stack
├── requirements.txt          → Dépendances Python
├── Dockerfile                → Conteneurisation du projet
├── .gitignore
├── README.md
│
├── cbm_engine/               → Moteur CBM
│   ├── __init__.py
│   ├── migration.py          → Contient une fonction migrée depuis MATLAB
│   └── analyzer.py           → Algorithmes CBM simples (RMS, FFT, seuils)
│
├── sensor_data/              → Échantillon de données JSON simulées
│   └── sample_vibration.json
│
└── tests/                    → Tests unitaires
    ├── test_analyzer.py
    └── test_migration.py
```

---

## ⚙️ Fonctionnement général

### 🔀 1. Traitement de données capteurs

* Le fichier `sample_vibration.json` simule un capteur IoT fournissant une série temporelle vibratoire (accélération, fréquence, etc.).
* Le fichier `main.py` lit ces données et les traite avec le module `cbm_engine`.

### 🧐 2. Moteur d’analyse CBM

* `analyzer.py` implémente :

  * Le calcul du **RMS** (Root Mean Square) des signaux.
  * L’application d’un **filtrage fréquentiel** simplifié (FFT).
  * Un système de **détection de seuil** personnalisable.
* Le but est de démontrer la logique de maintenance conditionnelle.

### 🔀 3. Migration MATLAB > Python

* `migration.py` contient un équivalent Python d’une fonction MATLAB (ex : RMS ou spectre).
* Le style de codage suit les normes `PEP8` et les meilleures pratiques Python.

### 💻 4. Interface CLI

* `cbmcli.py` offre une petite interface en ligne de commande pour :

  * Lancer une analyse sur un fichier.
  * Afficher des statistiques.
  * Simuler une alerte de maintenance.

Exemple :

```bash
python cbmcli.py analyze --file sensor_data/sample_vibration.json
```

---

## 🧪 5. Tests

Les tests unitaires sont dans `tests/` :

* `test_analyzer.py` vérifie les calculs RMS / seuils.
* `test_migration.py` valide la fidélité de la fonction migrée depuis MATLAB.

---

## 🐳 6. Docker

Le `Dockerfile` permet d'exécuter le projet dans un conteneur propre :

```bash
docker build -t cbm-stack .
docker run cbm-stack
```

---

## 🧐 Stack utilisée

* **Python 3.12+**
* `numpy`, `scipy`, `json`, `argparse`
* Docker pour l’exécution isolée
* Pytest pour les tests
* Exemple simple mais extensible à :

  * des microservices
  * une base de données
  * une ingestion IoT via MQTT ou Kafka

---

## 🌟 Objectifs atteints

✔️ Migration MATLAB > Python
✔️ Stack CBM de démonstration prête à pousser
✔️ Testable et extensible (TDD-friendly)
✔️ Organisation claire pour une industrialisation future

---

**Dave | 73 k0d3**
