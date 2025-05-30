# Suivi des Améliorations CBM Stack (CLI)

## ✅ Améliorations Immédiates

### 1. Sortie JSON des résultats d’analyse (`--json`)

* **Description** : Affiche les résultats d’analyse au format JSON.
* **Avantage** : Interopérabilité avec d'autres outils, APIs, dashboards.
* **Statut** : À implémenter
* **CLI attendu** :

  ```bash
  python main.py run --analyze --json
  ```

### 2. Ajout de tests unitaires avec `pytest`

* **Description** : Valider automatiquement les fonctions critiques.
* **Modules testés** :

  * `load_sensor_data`
  * `file_checksum`
  * `regenerate_sensor_data`
  * `compute_rms`
  * `detect_threshold`
  * `compute_fft`
* **Dossier recommandé** : `tests/`
* **Statut** : À implémenter

### 3. API Flask légère

* **Description** : Simuler un service web autour des fonctions de base.
* **Endpoints** :

  * `GET /analyze?file=...`
  * `POST /regenerate`
  * `GET /checksum?file=...`
* **Objectif** : Préparer l'intégration dans une archi distribuée ou IOT.
* **Statut** : À implémenter

### 4. Rapport PDF avec `--report`

* **Libs candidates** : `fpdf2`, `reportlab`, `WeasyPrint`
* **Contenu du rapport** :

  * RMS, FFT, seuils, horodatage, style graphique
  * Option : logo, auteur, mise en page pro
* **CLI attendu** :

  ```bash
  python main.py run --analyze --report
  ```
* **Sortie** : `reports/report_YYYYMMDD-HHMMSS.pdf`

## 💡 Autres Améliorations Proposées

### 5. Export CSV (`--csv`)

* Sauvegarde des résultats d’analyse au format `CSV`.
* Pratique pour analyse Excel, tableaux croisés, etc.

### 6. Logger Amélioré

* Utiliser `logging` pour sauvegarder les événements dans `logs/app.log`
* Niveaux : DEBUG / INFO / WARNING / ERROR

### 7. Lecture Live via Trame JSON

* Mode démon : simule une lecture temps réel de données capteur.
* Rafraîchissement automatique toutes les X secondes.

### 8. Mode "daemon"

* Surveillance continue d’un fichier capteur pour déclenchement d’analyse automatique.
* Intéressant pour de la maintenance prédictive en live.

### 9. Packaging

* **Format** : `.whl` via `setuptools` ou `.exe` via `pyinstaller`
* **Objectif** :

  * Distribution facile en interne ou clients
  * Utilisation hors Python

---

© Mai-2025, Dave | 73 k0d3
