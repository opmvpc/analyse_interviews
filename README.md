# Analyse des Interviews avec GPT-4o-mini

Ce projet utilise GPT-4o-mini pour analyser des segments d'interviews en appliquant un codage déductif. Les résultats sont ensuite stockés dans une base de données SQLite et peuvent être visualisés à l'aide de scripts Python.

## Prérequis

- Python 3.x
- Modules Python : `sqlite3`, `pandas`, `rich`, `openai`, `dotenv`, `pydantic`
- Clé API OpenAI (à placer dans un fichier `.env`)

## Installation

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/votre-utilisateur/analyse_interviews.git
   cd analyse_interviews
   ```

2. Installez les dépendances Python :

   ```bash
   pip install -r requirements.txt
   ```

3. Créez un fichier `.env` à la racine du projet avec votre clé API OpenAI :
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Utilisation

### 1. Exécution de l'analyse

Le script principal `main.py` analyse les segments d'interviews en utilisant GPT-4o-mini. Les résultats sont enregistrés dans une base de données SQLite (`results.db`).

```bash
python3 main.py
```

### 2. Visualisation des Résultats

Utilisez le script `result.py` pour calculer et afficher les métriques LLMq et les segments de texte avec le plus de correspondances positives.

```bash
python3 result.py
```

### 3. Paramètres du Script

Vous pouvez modifier les paramètres par défaut directement dans le script `main.py` :

- `num_segments`: Nombre de segments à sélectionner aléatoirement pour chaque fichier (par défaut : 4).
- `num_iterations`: Nombre d'itérations par segment (par défaut : 10).
- `max_workers`: Nombre de threads parallèles pour le traitement (par défaut : 10).

## Structure des Fichiers

- `main.py`: Script principal pour analyser les segments d'interviews.
- `result.py`: Script pour visualiser les résultats de l'analyse.
- `results.db`: Base de données SQLite contenant les résultats de l'analyse.
- `data/`: Dossier contenant les fichiers JSON des interviews à analyser.

## Auteurs

- [Thibault Six](https://github.com/opmvpc)

## Licence

Le code de ce projet est sous licence Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). Cela signifie que vous êtes libre de partager et d'adapter le code pour des usages non commerciaux, tant que vous attribuez le crédit approprié.

### Données

Veuillez noter que les données utilisées dans ce projet ne sont pas libres de droit et ne peuvent pas être réutilisées, partagées ou distribuées sans autorisation explicite.

Pour plus de détails sur la licence du code, veuillez consulter le fichier [LICENSE](LICENSE).

[![License: CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)
