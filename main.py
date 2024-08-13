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
from prompt import system_prompt, user_prompt_1, user_prompt_2, user_prompt_3, user_prompt_4, user_prompt_5, user_prompt_6, assistant_response_1, assistant_response_2, assistant_response_3, assistant_response_4_initial, assistant_response_4_corrected, assistant_response_5,assistant_response_6, validation_error
from db import save_result_to_db, initialize_db
from multiprocessing import Manager


manager = Manager()
stats = manager.dict({
    'segments_processed': 0,
    'segments_failed': 0,
    'iterations_completed': 0
})

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
    notes: str
    present: bool

class CodeResult(BaseModel):
    tps_gagne: CodeScratchpad  # gain_de_temps
    prod_aug: CodeScratchpad  # augmentation_productivite
    auto: CodeScratchpad  # autonomie
    prop_cont: CodeScratchpad  # propriete_du_contenu
    biais_err: CodeScratchpad  # biais_erreurs
    corr_biais: CodeScratchpad  # correction_des_biais
    eng_etu: CodeScratchpad  # engagement_des_etudiants
    prat_am: CodeScratchpad  # amelioration_des_pratiques_d_enseignement
    inno_peda: CodeScratchpad  # innovation_pedagogique
    meth_ens: CodeScratchpad  # changements_methodes_d_enseignement


# Function to analyze a segment using GPT-4o-mini with Structured Outputs
def analyze_segment(segment):
    attempt = 0
    max_retries = 3
    conversation_history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_1},
        {"role": "assistant", "content": assistant_response_1},
        {"role": "user", "content": user_prompt_2},
        {"role": "assistant", "content": assistant_response_2},
        {"role": "user", "content": user_prompt_3},
        {"role": "assistant", "content": assistant_response_3},
        {"role": "user", "content": user_prompt_4},
        {"role": "assistant", "content": assistant_response_4_initial},
        {"role": "user", "content": validation_error},
        {"role": "assistant", "content": assistant_response_4_corrected},
        {"role": "user", "content": user_prompt_5},
        {"role": "assistant", "content": assistant_response_5},
        {"role": "user", "content": user_prompt_6},
        {"role": "assistant", "content": assistant_response_6}
    ]

    # Vérification des types de chaque élément
    for i, message in enumerate(conversation_history):
        if not isinstance(message['content'], str):
            logger.error(f"Message at index {i} is not a valid string: {message}")

    while attempt < max_retries:
        try:
            logger.debug(f"Attempting to analyze segment: {segment[:50]}...")
            result = llm.json(
                messages=conversation_history + [{"role": "user", "content": "Extrait : " + segment}],
                response_format=CodeResult
            )
            logger.debug(f"Successfully analyzed segment. Result: {result}")
            return result

        except Exception as e:
            logger.error(f"Error on attempt {attempt + 1}: {e}")
            attempt += 1

    logger.error("Failed to get a valid response after retries")
    return None



# Function to get random segments
def get_random_segments(segments, count=5):
    return random.sample(segments, count)


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

def get_run_number(cursor):
    cursor.execute("SELECT MAX(run_number) FROM analysis_results")
    result = cursor.fetchone()[0]
    if result:
        return result + 1
    else:
        return 1

def process_task(task):
    segment, file_name, db_path, run_id, intervenant_name, i, segment_index, total_segments, num_iterations, run_number, run_start_time = task
    try:
        log_progress(file_name, segment_index+1, total_segments, i+1, num_iterations)
        result = analyze_segment(segment)
        if result:
            conn = sqlite3.connect(db_path)
            try:
                save_result_to_db(conn, run_id, segment, result, intervenant_name, run_number, run_start_time)
            except Exception as e:
                logger.error(f"Failed to save results to database: {e}")
            conn.close()
            return 1, 0, 1  # segments_processed, segments_failed, iterations_completed
        else:
            return 0, 1, 1
    except Exception as e:
        logger.error(f"Failed to process segment {segment_index+1}/{total_segments} after retries: {e}")
        return 0, 1, 1

def process_files(data_dir, db_path, analyze_all=False, num_segments=4, num_iterations=10, max_workers=10):
    tasks = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    run_id = str(uuid.uuid4())
    run_number = get_run_number(cursor)
    run_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for file_name in os.listdir(data_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(data_dir, file_name)
            logger.info(f"Processing {file_name}...")
            with open(file_path, 'r') as file:
                segments = json.load(file)

            if analyze_all:
                selected_segments = segments
            else:
                selected_segments = get_random_segments(segments, num_segments)

            intervenant_name = extract_intervenant_name(file_name)

            total_segments = len(selected_segments)
            for segment_index, segment in enumerate(selected_segments):
                for i in range(num_iterations):
                    tasks.append((segment, file_name, db_path, run_id, intervenant_name, i, segment_index, total_segments, num_iterations, run_number, run_start_time))

    conn.close()

    logger.info(f"Created {len(tasks)} tasks")

    segments_processed = 0
    segments_failed = 0
    iterations_completed = 0

    # Process in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_task, task) for task in tasks]
        for future in as_completed(futures):
            sp, sf, ic = future.result()
            segments_processed += sp
            segments_failed += sf
            iterations_completed += ic
            print(f"Task completed. Processed: {sp}, Failed: {sf}, Iterations: {ic}")

    return segments_processed, segments_failed, iterations_completed

def log_progress(file_name, segment_index, total_segments, iteration, total_iterations):
    elapsed_time = time.time() - start_time
    logger.info(f"Temps écoulé: {elapsed_time:.2f}s - Fichier: {file_name} - Segment: {segment_index}/{total_segments} - Itération: {iteration}/{total_iterations}")

if __name__ == "__main__":
    data_dir = find_most_recent_directory()
    db_path = initialize_db()
    segments_processed, segments_failed, iterations_completed = process_files(data_dir, db_path, analyze_all=True, num_segments=10, num_iterations=20, max_workers=16)

    # Afficher les statistiques finales
    end_time = time.time()
    total_time = end_time - start_time
    total_segments = segments_processed + segments_failed

    print("\nStatistiques finales:")
    print(f"Temps total d'exécution: {total_time:.2f} secondes")
    print(f"Nombre total de segments analysés: {total_segments}")
    print(f"Nombre total d'itérations: {iterations_completed}")
    print(f"Segments traités avec succès: {segments_processed}")
    print(f"Segments échoués: {segments_failed}")
    if total_segments > 0:
        print(f"Taux de réussite: {segments_processed/total_segments*100:.2f}%")
    else:
        print("Taux de réussite: N/A (aucun segment traité)")
