# 🧠 Projet – Extraction de données structurées à partir de fichiers PDF

## Objectif général :
Système d’extraction des données à partir de fichiers PDF et de les transformer en structures JSON normalisées.
___
📁 Deux ensembles de fichiers PDF :
1.	Premier ensemble :
Ces fichiers contiennent des règles décrivant comment analyser les fichiers du second ensemble.
👉 Ils définissent les modèles de structure ou les schémas d’extraction.
2.	Deuxième ensemble :
Ces fichiers contiennent des données diverses sous différents formats.
👉 Chaque type de PDF devra être analysé selon les règles issues du premier ensemble.
___
🔄 Processus global :
1.	Analyser le premier ensemble de PDF afin d’en extraire des règles d’analyse dynamiques
2.	En déduire des structures de données adaptées (par exemple : JSON Schema ou dictionnaire clé/valeur)
3.	Analyser le deuxième ensemble de PDF selon ces règles
4.	Extraire les données pertinentes et les convertir en JSON standardisé
5.	Injecter ces données dans une base de données pour exploitation ultérieure
___
💡 Exemple :
* Fichier de règles PDF : décrit qu’un “Facture Client” contient un champ Nom, Date, Montant TTC, etc.
* Fichier de données PDF : contient une facture réelle → on extrait les données selon le modèle
* Résultat JSON :
````
{
  "nom": "Société ABC",
  "date": "2025-05-08",
  "montant_ttc": 14250.75
}
````
___
📂 Structure de dossier proposée
````
Pdf2Json/
│
├── data/                  # Contiendra les fichiers PDF (modèles de règles et données)
│   ├── rules/             # Dossier pour les fichiers PDF de règles
│   └── input_pdfs/        # Dossier pour les fichiers PDF contenant les données à extraire
│
├── pdf2json/              # Code principal de l'application
│   ├── __init__.py        # Fichier d'initialisation du module
│   ├── extractor.py       # Code pour extraire les données des PDF
│   ├── parser.py          # Code pour parser les règles et appliquer la structure
│   ├── utils.py           # Fonctions utilitaires (ex: conversion PDF → texte)
│   ├── json_schema.py     # Pour valider ou générer le JSON final
│   ├── config.py          # Paramètres de configuration (API, chemins, etc.)
│   └── main.py            # Fichier principal pour exécuter l'application
│
├── tests/                 # Tests unitaires et d'intégration
│   ├── test_extractor.py  # Tests pour le module d'extraction de données
│   └── test_parser.py     # Tests pour le module de parsing des règles
│
├── requirements.txt       # Liste des dépendances du projet (PyMuPDF, etc.)
├── README.md              # Document d'introduction et d'installation
└── setup.py               # Script d'installation du projet via pip


````

________________________________________
📦 Contenu de requirements.txt
````
PyMuPDF
pdfminer.six
pydantic
jsonschema
python-dateutil
````
________________________________________

🧩 Modules en détail   
* rule_parser.py → lit les PDF du dossier rulesets/ et en déduit des structures logiques (clé, type, position, etc.)
*	pdf_parser.py → lit les PDF à analyser et extrait les champs selon le modèle
*	normalizer.py → nettoie/formatte les données extraites (dates, montants, noms)
*	exporter.py → sauvegarde les données en .json dans parsed_json/
*	main.py → gère le process de bout en bout ou lance selon argument
________________________________________
⚙️ Exemple d’appel dans main.py
````
from pdf2json import rule_parser, pdf_parser, normalizer, exporter

rules = rule_parser.load_rules("rulesets/sample_ruleset.pdf")
data = pdf_parser.parse_pdf("pdfs_to_parse/invoice_example.pdf", rules)
clean_data = normalizer.clean(data)
exporter.to_json(clean_data, "parsed_json/invoice_example.json")
````
________________________________________


🚀 Explication rapide de ce fichier main.py :
Lecture des fichiers PDF :

On commence par lister tous les fichiers PDF dans INPUT_PDFS_PATH (le dossier des fichiers à traiter).

Extraction du texte :

On utilise la fonction extract_text_from_pdf() pour extraire le texte de chaque fichier PDF.

Application des règles :

La fonction parse_rules_from_pdf() appliquera les règles issues des PDF de règles sur le texte extrait, en vue de structurer les données.

Génération du JSON :

Ensuite, avec generate_json_schema(), les données sont converties en JSON, en suivant la structure définie.

Sauvegarde dans un fichier :

Enfin, le JSON généré est enregistré dans le dossier de sortie défini dans OUTPUT_PATH.

🧰 Prochaines étapes :
Définir les chemins dans config.py :

On va définir les chemins d'entrée (INPUT_PDFS_PATH) et de sortie (OUTPUT_PATH).

Commencer avec l’extraction de texte PDF :

L'implémentation de la fonction extract_text_from_pdf() dans extractor.py.