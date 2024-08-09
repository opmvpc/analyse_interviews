import os
import sqlite3
import uuid
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, Field
from concurrent.futures import ProcessPoolExecutor, as_completed
import random
import json
from llm.llm_implementations import LLMFactory
import logging
import time
from collections import Counter

start_time = time.time()
stats = Counter()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
llm_model = os.getenv("LLM_MODEL")

# Initialize LLM
llm = LLMFactory.create_llm(llm_model)


# Define the JSON output schema using Pydantic (in French and camelCase without accents)
class CodeScratchpad(BaseModel):
    carnet_de_notes: str = Field(min_length=30)
    est_present: bool

class CodeResult(BaseModel):
    gain_de_temps: CodeScratchpad
    augmentation_productivite: CodeScratchpad
    autonomie: CodeScratchpad
    propriete_du_contenu: CodeScratchpad
    biais_culturels: CodeScratchpad
    correction_des_biais: CodeScratchpad
    engagement_des_etudiants: CodeScratchpad
    amelioration_des_pratiques_d_enseignement: CodeScratchpad
    innovation: CodeScratchpad
    nouvelles_methodes_d_enseignement: CodeScratchpad

# Function to analyze a segment using GPT-4o-mini with Structured Outputs
def analyze_segment(segment):
    attempt = 0
    max_retries = 3
    conversation_history = [
        {"role": "system", "content": "Vous êtes un assistant utile."},
        {"role": "user", "content": """
 Le but est de réaliser une analyse qualitative par la méthode du codage déductif. Vous devez analyser l'extrait d'entretien suivant pour identifier si l'un des codes prédéfinis est présent. 1. **Réfléchissez dans le Carnet de notes** : Analysez l'extrait en identifiant les éléments qui pourraient correspondre à chaque code. Soyez attentif aux indices subtils ou implicites qui pourraient indiquer la présence d'un code. Justifiez votre décision avec des éléments concrets. Si le code est absent, expliquez pourquoi. 2. **Prise de décision** : Décidez si le code est présent (`true`) ou absent (`false`). Si l'information est ambiguë mais qu'il y a des éléments suggérant la présence du code, considérez-le comme présent (`true`). Si l'extrait ne contient aucune indication, alors la réponse doit être `false`. **Exigences de sortie** : - Retournez un JSON valide avec les clés suivantes pour chaque code : - **carnet_de_notes** : Explication textuelle. - **est_present** : Booléen (`true` ou `false`). - Ne retournez que du JSON valide, sans texte supplémentaire ou erreurs de formatage. **Les codes à évaluer (avec leurs descriptions)** : - **gain_de_temps** : L'extrait mentionne-t-il, même de manière implicite, une réduction du temps nécessaire pour préparer les cours grâce aux modèles de langage ? - **augmentation_productivite** : L'extrait indique-t-il, même indirectement, une augmentation de la productivité, comme la création de plus de matériel pédagogique ? - **autonomie** : L'extrait reflète-t-il, explicitement ou implicitement, un sentiment d'autonomie et de contrôle sur le contenu généré par l'enseignant ? - **propriete_du_contenu** : L'extrait mentionne-t-il, directement ou indirectement, un sentiment de propriété sur le contenu créé, malgré l'assistance des modèles de langage ? - **biais_culturels** : L'extrait mentionne-t-il des biais culturels ou des erreurs dans le contenu généré ? - **correction_des_biais** : L'extrait parle-t-il de corrections de biais ou d'erreurs dans le contenu généré ? - **engagement_des_etudiants** : L'extrait indique-t-il un engagement accru des étudiants grâce aux nouveaux outils ? - **amelioration_des_pratiques_d_enseignement** : L'extrait mentionne-t-il une amélioration des pratiques pédagogiques grâce aux modèles de langage ? - **innovation** : L'extrait évoque-t-il l'introduction de nouvelles idées ou méthodes pédagogiques grâce aux modèles de langage ? - **nouvelles_methodes_d_enseignement** : L'extrait mentionne-t-il des nouvelles méthodes d'enseignement adoptées suite à l'utilisation des modèles de langage ?
"""}
    ]

    while attempt < max_retries:
        try:
            logger.debug(f"Attempting to analyze segment: {segment[:50]}...")
            result = llm.json(messages=conversation_history + [{"role": "user", "content": segment}], response_format=CodeResult)
            logger.debug(f"Successfully analyzed segment. Result: {result}")
            return result

        except (ValueError, ValidationError) as e:
            attempt += 1
            logger.error(f"Attempt {attempt} failed: {e}")
            conversation_history.append({"role": "assistant", "content": str(e)})
            conversation_history.append({"role": "user", "content": f"Erreur rencontrée: {e}. Veuillez corriger le format de sortie et réessayer."})

        except Exception as e:
            attempt += 1
            logger.error(f"Unexpected error on attempt {attempt}: {e}")

    logger.error(f"Failed to get a valid response after {max_retries} attempts")
    raise Exception(f"Failed to get a valid response after {max_retries} attempts")


# Function to get random segments
def get_random_segments(segments, count=5):
    return random.sample(segments, count)

# Function to save results to the database
def save_result_to_db(conn, run_id, segment, result, intervenant_name):
    cursor = conn.cursor()

    for code_name, code_data in result.__dict__.items():  # Utiliser __dict__ au lieu de items()
        segment_id = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO analysis_results (id, run_id, segment_text, code_name, carnet_de_notes, est_present, intervenant_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (segment_id, run_id, segment, code_name, code_data.carnet_de_notes, code_data.est_present, intervenant_name))

    conn.commit()

# Function to create or reset the database schema
def initialize_db(db_path="results.db"):
    print("Création ou réinitialisation de la base de données...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_results (
        id TEXT PRIMARY KEY,
        run_id TEXT,
        segment_text TEXT,
        code_name TEXT,
        carnet_de_notes TEXT,
        est_present BOOLEAN,
        intervenant_name TEXT
    )
    """)

    conn.commit()
    conn.close()
    return db_path

# Function to find the most recent directory in 'data'
def find_most_recent_directory(base_dir="./data"):
    directories = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not directories:
        raise Exception("No directories found in the base directory.")
    most_recent_directory = max(directories, key=os.path.getmtime)
    print(f"Using data directory: {most_recent_directory}")
    return most_recent_directory

def extract_intervenant_name(file_name):
    # Suppression du préfixe 'Entretien ' et du suffixe '_grouped_3.json'
    intervenant = file_name.replace("Entretien ", "").replace("_grouped_3.json", "")
    # Vérifier si le nom a un nom de famille, sinon retourner juste le prénom
    if " " in intervenant:
        return intervenant
    else:
        return intervenant.split()[0]

def process_task(task):
    segment, file_name, db_path, run_id, intervenant_name, i, segment_index, total_segments, num_iterations = task
    try:
        log_progress(file_name, segment_index+1, total_segments, i+1, num_iterations)
        result = analyze_segment(segment)
        if result:
            conn = sqlite3.connect(db_path)
            save_result_to_db(conn, run_id, segment, result, intervenant_name)
            conn.close()
            stats['segments_processed'] += 1
            stats['iterations_completed'] += 1
            return f"Successfully processed segment {segment_index+1}/{total_segments} for file {file_name} during iteration {i+1}/{num_iterations}"
        else:
            stats['segments_failed'] += 1
            return f"Failed to process segment {segment_index+1}/{total_segments} due to model refusal: {segment[:50]}..."
    except Exception as e:
        stats['segments_failed'] += 1
        return f"Failed to process segment {segment_index+1}/{total_segments} after retries: {e}"


def process_files(data_dir, db_path, analyze_all=False, num_segments=4, num_iterations=10, max_workers=10):
    tasks = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for file_name in os.listdir(data_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(data_dir, file_name)
            print(f"Processing {file_name}...")
            with open(file_path, 'r') as file:
                segments = json.load(file)

            if analyze_all:
                selected_segments = segments
            else:
                selected_segments = get_random_segments(segments, num_segments)

            run_id = str(uuid.uuid4())
            intervenant_name = extract_intervenant_name(file_name)

            total_segments = len(selected_segments)
            for segment_index, segment in enumerate(selected_segments):
                for i in range(num_iterations):
                    tasks.append((segment, file_name, db_path, run_id, intervenant_name, i, segment_index, total_segments, num_iterations))

    conn.close()

    # Process in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_task, task) for task in tasks]
        for future in as_completed(futures):
            print(future.result())

    # Afficher les statistiques finales
    end_time = time.time()
    total_time = end_time - start_time
    total_segments = stats['segments_processed'] + stats['segments_failed']
    total_iterations = stats['iterations_completed']

    print("\nStatistiques finales:")
    print(f"Temps total d'exécution: {total_time:.2f} secondes")
    print(f"Nombre total de segments analysés: {total_segments}")
    print(f"Nombre total d'itérations: {total_iterations}")
    print(f"Segments traités avec succès: {stats['segments_processed']}")
    print(f"Segments échoués: {stats['segments_failed']}")
    print(f"Taux de réussite: {stats['segments_processed']/total_segments*100:.2f}%")

def log_progress(file_name, segment_index, total_segments, iteration, total_iterations):
    elapsed_time = time.time() - start_time
    logger.info(f"Temps écoulé: {elapsed_time:.2f}s - Fichier: {file_name} - Segment: {segment_index}/{total_segments} - Itération: {iteration}/{total_iterations}")

if __name__ == "__main__":
    data_dir = find_most_recent_directory()
    db_path = initialize_db()
    process_files(data_dir, db_path, analyze_all=True)
