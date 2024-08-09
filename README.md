# Projet d'Analyse Qualitative d'Entretiens avec GPT-4o

Ce projet vise à analyser qualitativement des entretiens en utilisant la méthode de codage déductif, en se basant sur des segments textuels extraits de documents Word. L'analyse est effectuée via l'API GPT-4o, et les résultats sont stockés dans une base de données SQLite pour une exploration et une visualisation ultérieure.

## Organisation du Projet

Le projet est structuré de la manière suivante :

├── data/
│ ├── cleaned/ # Contient les fichiers JSON des segments extraits et nettoyés
│ ├── outputs_YYYYMMDD_HHMMSS/ # Dossiers contenant les résultats des analyses précédentes
│ └── Entretien_NomIntervenant.docx # Fichiers Word contenant les entretiens originaux
│
├── .env # Fichier d'environnement contenant la clé API OpenAI
├── main.py # Script principal pour effectuer l'analyse des segments
├── results.py # Script pour visualiser et explorer les résultats stockés en base de données
├── requirements.txt # Liste des dépendances Python nécessaires pour le projet
└── README.md # Ce fichier

markdown


## Prérequis

Avant de pouvoir exécuter les scripts, assurez-vous d'avoir les éléments suivants :

1. **Python 3.8+** : Le projet nécessite Python 3.8 ou supérieur.
2. **Dépendances Python** : Installez les dépendances listées dans `requirements.txt` en utilisant la commande suivante :
   ```bash
   pip install -r requirements.txt

    Clé API OpenAI : Ajoutez votre clé API OpenAI dans un fichier .env à la racine du projet sous la forme suivante :

    makefile

    OPENAI_API_KEY=your_api_key_here

Utilisation des Scripts
1. main.py

Ce script est utilisé pour analyser les segments des entretiens. Les résultats sont enregistrés dans une base de données SQLite.
Arguments

    --analyze-all : Si ce paramètre est fourni, le script analysera tous les segments de chaque entretien. Sinon, il analysera un sous-ensemble aléatoire de segments.

Exécution

Pour analyser tous les segments de chaque entretien avec 10 itérations par segment, exécutez la commande suivante :

bash

python3 main.py --analyze-all

Pour analyser uniquement un sous-ensemble aléatoire de segments, exécutez :

bash

python3 main.py

Les résultats seront sauvegardés dans une base de données SQLite.
2. results.py

Ce script permet de visualiser les résultats de l'analyse, notamment les segments les plus pertinents pour chaque code.
Affichage des Résultats

Le script extrait les données de la base SQLite et affiche les résultats dans la console en utilisant un framework de tableau pour une meilleure lisibilité.

Pour exécuter ce script, utilisez simplement :

bash

python3 results.py

Cela affichera les résultats triés par code et par intervenant.
Auteurs

Ce projet a été développé pour l'analyse qualitative de données d'entretiens en utilisant des modèles de langage GPT-4o. Les scripts ont été conçus pour automatiser l'analyse et fournir une base de données exploitable pour l'exploration des résultats.
Licence
