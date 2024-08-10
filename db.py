import sqlite3
import uuid
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def initialize_db(db_path="caca.db"):
    # Vérifier si la base de données existe déjà
    db_exists = os.path.exists(db_path)

    # Si la base de données n'existe pas, on la crée
    if not db_exists:
        print("La base de données n'existe pas. Création de la base de données...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Création de la table avec les nouvelles colonnes run_number et run_start_time
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            id TEXT PRIMARY KEY,
            run_id TEXT,
            segment_text TEXT,
            code_name TEXT,
            carnet_de_notes TEXT,
            est_present BOOLEAN,
            intervenant_name TEXT,
            run_number INTEGER,
            run_start_time TEXT
        )
        """)

        conn.commit()
        conn.close()
        print("Base de données créée avec succès.")
    else:
        print("La base de données existe déjà. Connexion en cours...")

    return db_path

def save_result_to_db(conn, run_id, segment, result, intervenant_name, run_number, run_start_time):
    cursor = conn.cursor()

    for code_name, code_data in result.__dict__.items():
        segment_id = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO analysis_results (id, run_id, segment_text, code_name, carnet_de_notes, est_present, intervenant_name, run_number, run_start_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (segment_id, run_id, segment, code_name, code_data.carnet_de_notes, code_data.est_present, intervenant_name, run_number, run_start_time))

    conn.commit()
