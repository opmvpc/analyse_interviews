import os
import json
import sqlite3
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

# Define the JSON output schema using Pydantic (in French and snake_case)
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
    if not segment.strip():  # Ensure the segment is not empty or just whitespace
        raise ValueError("Segment is empty or improperly formatted.")

    attempt = 0
    max_retries = 5
    conversation_history = [
        {"role": "system", "content": "Vous êtes un assistant utile."},
        {"role": "user", "content": f"""
Analysez l'extrait d'entretien suivant pour identifier si l'un des codes prédéfinis est présent. Pour chaque code, répondez à la question associée pour déterminer la présence ou non du code, et suivez ces étapes :

1. Réfléchir dans le Carnet de notes :
   - Considérez la question associée au code et analysez l'extrait pour voir s'il correspond.
   - Rédigez votre raisonnement de manière claire, en vous concentrant sur des phrases ou des mots spécifiques dans l'extrait qui soutiennent votre conclusion.
   - Si l'information est ambiguë ou ne correspond pas directement au code, indiquez que le code est absent (faux) dans votre raisonnement.
   - Si plusieurs codes semblent applicables, documentez votre réflexion pour chacun.

2. Prendre une Décision (Vrai/Faux) :
   - Après réflexion, décidez si le code est présent dans l'extrait en répondant à la question associée.
   - Assurez-vous que votre décision est en accord avec le raisonnement fourni dans le carnet de notes.
   - Effectuez une dernière vérification en relisant votre raisonnement pour confirmer la présence ou l'absence du code.
   - Si la décision n'est pas claire ou si l'extrait est ambigu, la réponse doit être "faux".

3. Exigences de sortie :
   - Retournez uniquement un objet JSON valide qui respecte strictement le schéma requis.
   - Il est extrêmement important que la sortie soit un JSON valide, sans texte supplémentaire ou erreurs de formatage.

L'output doit UNIQUEMENT contenir l'objet JSON {...} avec les clés et valeurs correctes.
Il ne doit contenir aucun texte supplémentaire, commentaires ou erreurs de formatage.
Il ne doit jamais être entouré de blockcode markdown (```) ou de guillemets.

Les codes prédéfinis et leurs clés JSON correspondantes en snake_case sont :

   - Gain de temps (gain_de_temps) : L'extrait mentionne-t-il une réduction du temps nécessaire pour préparer les cours grâce à l'utilisation des modèles de langage ?
   - Augmentation de la productivité (augmentation_productivite) : L'extrait mentionne-t-il une augmentation de la productivité, incluant la capacité à créer plus de matériel pédagogique ou à accomplir plus de tâches dans le même temps ?
   - Autonomie (autonomie) : L'extrait reflète-t-il un sentiment d'autonomie et de contrôle sur le contenu généré par l'enseignant ?
   - Propriété du contenu (propriete_du_contenu) : L'extrait mentionne-t-il un sentiment de propriété sur le contenu créé, malgré l'assistance des modèles de langage ?
   - Biais culturels (biais_culturels) : L'extrait mentionne-t-il des biais culturels ou des erreurs dans le contenu généré ?
   - Correction des biais (correction_des_biais) : L'extrait mentionne-t-il des corrections de biais ou des erreurs dans le contenu généré ?
   - Engagement des étudiants (engagement_des_etudiants) : L'extrait mentionne-t-il un engagement accru des étudiants grâce à l'utilisation des nouveaux outils ?
   - Amélioration des pratiques d'enseignement (amelioration_des_pratiques_d_enseignement) : L'extrait mentionne-t-il une amélioration des pratiques pédagogiques grâce à l'utilisation des modèles de langage ?
   - Innovation (innovation) : L'extrait mentionne-t-il l'introduction de nouvelles idées ou méthodes pédagogiques grâce à l'utilisation des modèles de langage ?
   - Nouvelles méthodes d'enseignement (nouvelles_methodes_d_enseignement) : L'extrait mentionne-t-il des nouvelles méthodes d'enseignement adoptées suite à l'utilisation des modèles de langage ?

Le JSON final doit inclure une clé pour chaque code prédéfini:
- **gain_de_temps**
- **augmentation_productivite**
- **autonomie**
- **propriete_du_contenu**
- **biais_culturels**
- **correction_des_biais**
- **engagement_des_etudiants**
- **amelioration_des_pratiques_d_enseignement**
- **innovation**
- **nouvelles_methodes_d_enseignement**

Chaque clé de code doit contenir deux sous-clés :
- **carnet_de_notes** : Une explication textuelle détaillant le raisonnement derrière la décision pour ce code.
- **est_present** : Un booléen (`true` ou `false`) indiquant si le code est présent ou non.

Si des erreurs sont présentes dans la réponse de l'assistant, elles lui seront transmises avec sa réponse pour qu'il puisse les corriger itérativement. Il est essentiel de respecter le rapport d'erreur reçu lors des tentatives de correction.
"""}
    ]

    while attempt < max_retries:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history + [{"role": "user", "content": segment}]
        )

        math_response = completion.choices[0].message

        if math_response.refusal:
            print(f"Refusal detected: {math_response.refusal}")
            raise Exception(f"Model refused to respond: {math_response.refusal}")

        try:
            # Extract JSON from the response
            response_text = math_response.content
            json_str = extract_json_from_response(response_text)
            result = CodeResult.parse_raw(json_str)
            return segment, result

        except (ValidationError, AttributeError, ValueError) as e:
            attempt += 1
            error_message = f"Attempt {attempt} failed: {e}. Output received: {response_text}"
            print(error_message)
            conversation_history.append({"role": "assistant", "content": response_text})
            conversation_history.append({"role": "user", "content": f"Erreur rencontrée: {error_message}. Voici l'output problématique : {response_text}. Veuillez corriger le format de sortie et réessayer. Rappelez-vous de retourner uniquement un objet JSON valide et d'utiliser les clés correctes comme spécifié précédemment."})

    raise Exception(f"Failed to get a valid response after {max_retries} attempts")

# Function to save results to the relational database
def save_results_batch(db_path, results_batch):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for segment, result, run_id in results_batch:
        print(f"Saving results for segment ID {run_id}...")
        segment_text, code_result = segment, result
        cursor.execute("""
        INSERT INTO segments (run_id, segment_text) VALUES (?, ?)
        """, (run_id, segment_text))
        segment_id = cursor.lastrowid

        for code_name, code_data in code_result.dict().items():
            print(f"Inserting code data: {code_name}...")
            cursor.execute("""
            INSERT INTO codes (segment_id, code_name, carnet_de_notes, est_present)
            VALUES (?, ?, ?, ?)
            """, (segment_id, code_name, code_data['carnet_de_notes'], code_data['est_present']))

    conn.commit()
    conn.close()

# Function to create or reset the database schema
def initialize_db(db_path="results.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create runs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        run_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create segments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS segments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id INTEGER,
        segment_text TEXT NOT NULL,
        FOREIGN KEY (run_id) REFERENCES runs(id)
    )
    """)

    # Create codes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        segment_id INTEGER,
        code_name TEXT NOT NULL,
        carnet_de_notes TEXT,
        est_present BOOLEAN,
        FOREIGN KEY (segment_id) REFERENCES segments(id)
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
    return most_recent_directory

def process_task(task):
    segment, file_name, db_path, run_id, i = task
    print(f"Processing segment {i} for file {file_name}...")
    try:
        result = analyze_segment(segment)
        print(f"Successfully processed segment {i} for file {file_name}")
        return (segment, result, run_id)
    except Exception as e:
        print(f"Failed to process segment after retries: {e}")
        return None

def process_files(data_dir, db_path, num_segments=5, num_iterations=2, max_workers=5):  # Set to 5 segments
    tasks = []
    results_batch = []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for file_name in os.listdir(data_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(data_dir, file_name)
            print(f"Processing {file_name}...")
            with open(file_path, 'r') as file:
                segments = json.load(file)
                selected_segments = get_random_segments(segments, num_segments)

                # Insert run info
                cursor.execute("""
                INSERT INTO runs (file_name) VALUES (?)
                """, (file_name,))
                run_id = cursor.lastrowid
                conn.commit()

                for segment in selected_segments:
                    for i in range(num_iterations):
                        tasks.append((segment, file_name, db_path, run_id, i))

    conn.close()

    # Process in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_task, task) for task in tasks]
        for future in as_completed(futures):
            result = future.result()
            if result:
                results_batch.append(result)

            if len(results_batch) >= 4:  # Save to DB in batches of 4
                save_results_batch(db_path, results_batch)
                results_batch = []  # Clear the batch after saving

    # Final save for any remaining results
    if results_batch:
        save_results_batch(db_path, results_batch)

if __name__ == "__main__":
    # Find the most recent directory in the 'data' folder
    data_dir = find_most_recent_directory()
    db_path = initialize_db()
    process_files(data_dir, db_path)
