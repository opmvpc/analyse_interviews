import os
import json
import sqlite3
import uuid
import random
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from concurrent.futures import ProcessPoolExecutor, as_completed

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Define the JSON output schema using Pydantic (in French and camelCase without accents)
class CodeScratchpad(BaseModel):
    carnet_de_notes: str
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

# Function to get random segments
def get_random_segments(segments, count=5):
    return random.sample(segments, count)

# Function to extract JSON from GPT-4o-mini response
def extract_json_from_response(response_text):
    try:
        json_start = response_text.index("{")
        json_end = response_text.rindex("}") + 1
        json_str = response_text[json_start:json_end]
        return json_str
    except ValueError:
        raise ValueError("No valid JSON found in the response.")

# Function to analyze a segment using GPT-4o-mini
def analyze_segment(segment):
    attempt = 0
    max_retries = 3
    conversation_history = [
        {"role": "system", "content": "Vous êtes un assistant utile."},
        {"role": "user", "content": f"""
Analysez l'extrait d'entretien suivant pour identifier si l'un des codes prédéfinis est présent.
Le JSON final doit inclure une clé pour chaque code prédéfini:
- gain_de_temps
- augmentation_productivite
- autonomie
- propriete_du_contenu
- biais_culturels
- correction_des_biais
- engagement_des_etudiants
- amelioration_des_pratiques_d_enseignement
- innovation
- nouvelles_methodes_d_enseignement
Chaque clé de code doit contenir deux sous-clés :
- carnet_de_notes : Une explication textuelle détaillant le raisonnement derrière la décision pour ce code.
- est_present : Un booléen (true ou false) indiquant si le code est présent ou non.
"""}
    ]

    while attempt < max_retries:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the cost-effective model
            messages=conversation_history + [{"role": "user", "content": segment}]
        )

        try:
            response_text = completion.choices[0].message.content
            json_str = extract_json_from_response(response_text)

            # Validate the result using Pydantic
            result = CodeResult.parse_raw(json_str)
            return segment, result
        except (ValidationError, AttributeError, ValueError) as e:
            attempt += 1
            error_message = f"Attempt {attempt} failed: {e}. Output received: {response_text}"
            print(error_message)
            conversation_history.append({"role": "assistant", "content": response_text})
            conversation_history.append({"role": "user", "content": f"Erreur rencontrée: {error_message}. Veuillez corriger le format de sortie et réessayer."})

    raise Exception(f"Failed to get a valid response after {max_retries} attempts")

# Function to save results to the single-table database
def save_result(db_path, segment, code_result, run_id, file_name, intervenant_id, intervenant_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"Sauvegarde des résultats pour le segment : {segment[:30]}...")

    try:
        for code_name, code_data in code_result.dict().items():
            carnet_de_notes = code_data['carnet_de_notes']
            est_present = code_data['est_present']

            # Générer un ID unique pour chaque insertion, et non pour tout le batch
            entry_id = str(uuid.uuid4())

            cursor.execute("""
            INSERT INTO analysis_results (id, run_id, file_name, segment_text, code_name, carnet_de_notes, est_present, created_at, intervenant_id, intervenant_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (entry_id, run_id, file_name, segment, code_name, carnet_de_notes, est_present, datetime.now(), intervenant_id, intervenant_name))

    except AttributeError as e:
        print(f"Erreur lors de la sauvegarde : {e}. Assurez-vous que 'code_result' est bien un objet Pydantic.")

    conn.commit()
    conn.close()

# Function to create or reset the single-table database
def initialize_db(db_path="results.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_results (
        id TEXT PRIMARY KEY,
        run_id TEXT,
        file_name TEXT,
        segment_text TEXT,
        code_name TEXT,
        carnet_de_notes TEXT,
        est_present BOOLEAN,
        created_at DATETIME,
        intervenant_id TEXT,
        intervenant_name TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Base de données créée ou réinitialisée.")
    return db_path

# Function to find the most recent directory in 'data'
def find_most_recent_directory(base_dir="./data"):
    directories = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not directories:
        raise Exception("No directories found in the base directory.")
    most_recent_directory = max(directories, key=os.path.getmtime)
    return most_recent_directory

def process_task(task):
    segment, file_name, db_path, run_id, i, intervenant_id, intervenant_name = task
    try:
        result = analyze_segment(segment)
        save_result(db_path, segment, result[1], run_id, file_name, intervenant_id, intervenant_name)
    except Exception as e:
        print(f"Failed to process segment after retries: {e}")

def process_files(data_dir, db_path, num_segments=5, num_iterations=2, max_workers=8):
    tasks = []

    for file_name in os.listdir(data_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(data_dir, file_name)
            print(f"Processing {file_name}...")
            with open(file_path, 'r') as file:
                segments = json.load(file)
                selected_segments = get_random_segments(segments, num_segments)

                run_id = str(uuid.uuid4())
                intervenant_id = str(uuid.uuid4())  # Generate a new ID for each intervenant
                intervenant_name = file_name.replace('_grouped_3.json', '')

                for segment in selected_segments:
                    for i in range(num_iterations):
                        tasks.append((segment, file_name, db_path, run_id, i, intervenant_id, intervenant_name))

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_task, task) for task in tasks]
        for future in as_completed(futures):
            future.result()  # This will raise exceptions if any

if __name__ == "__main__":
    db_path = initialize_db()
    data_dir = find_most_recent_directory()
    process_files(data_dir, db_path)
