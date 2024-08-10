import sqlite3
import uuid
import os
import logging
from datetime import datetime

# Configurer le logger pour afficher les erreurs en rouge
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Définir le format d'affichage des erreurs en rouge
class RedFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.ERROR:
            record.msg = f"\033[91m{record.msg}\033[0m"  # Rouge
        return super().format(record)

handler = logging.StreamHandler()
handler.setFormatter(RedFormatter())
logger.addHandler(handler)

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
            present BOOLEAN,
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
    try:
        cursor = conn.cursor()

        # Insertion dans la base de données
        cursor.execute("""
            INSERT INTO analysis_results (
                id, run_id, segment_text, code_name, carnet_de_notes, present, intervenant_name, run_number, run_start_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()), run_id, segment, "tps_gagne", result.tps_gagne.notes, result.tps_gagne.present, intervenant_name, run_number, run_start_time
        ))

        cursor.execute("""
            INSERT INTO analysis_results (
                id, run_id, segment_text, code_name, carnet_de_notes, present, intervenant_name, run_number, run_start_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()), run_id, segment, "prod_aug", result.prod_aug.notes, result.prod_aug.present, intervenant_name, run_number, run_start_time
        ))

        cursor.execute("""
            INSERT INTO analysis_results (
                id, run_id, segment_text, code_name, carnet_de_notes, present, intervenant_name, run_number, run_start_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()), run_id, segment, "auto", result.auto.notes, result.auto.present, intervenant_name, run_number, run_start_time
        ))

        cursor.execute("""
            INSERT INTO analysis_results (
                id, run_id, segment_text, code_name, carnet_de_notes, present, intervenant_name, run_number, run_start_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()), run_id, segment, "prop_cont", result.prop_cont.notes, result.prop_cont.present, intervenant_name, run_number, run_start_time
        ))

        cursor.execute("""
            INSERT INTO analysis_results (
                id, run_id, segment_text, code_name, carnet_de_notes, present, intervenant_name, run_number, run_start_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()), run_id, segment, "biais_cult", result.biais_cult.notes, result.biais_cult.present, intervenant_name, run_number, run_start_time
        ))

        cursor.execute("""
            INSERT INTO analysis_results (
                id, run_id, segment_text, code_name, carnet_de_notes, present, intervenant_name, run_number, run_start_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()), run_id, segment, "corr_biais", result.corr_biais.notes, result.corr_biais.present, intervenant_name, run_number, run_start_time
        ))

        cursor.execute("""
            INSERT INTO analysis_results (
                id, run_id, segment_text, code_name, carnet_de_notes, present, intervenant_name, run_number, run_start_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()), run_id, segment, "eng_etu", result.eng_etu.notes, result.eng_etu.present, intervenant_name, run_number, run_start_time
        ))

        cursor.execute("""
            INSERT INTO analysis_results (
                id, run_id, segment_text, code_name, carnet_de_notes, present, intervenant_name, run_number, run_start_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()), run_id, segment, "prat_am", result.prat_am.notes, result.prat_am.present, intervenant_name, run_number, run_start_time
        ))

        cursor.execute("""
            INSERT INTO analysis_results (
                id, run_id, segment_text, code_name, carnet_de_notes, present, intervenant_name, run_number, run_start_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()), run_id, segment, "inno", result.inno.notes, result.inno.present, intervenant_name, run_number, run_start_time
        ))

        cursor.execute("""
            INSERT INTO analysis_results (
                id, run_id, segment_text, code_name, carnet_de_notes, present, intervenant_name, run_number, run_start_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()), run_id, segment, "nouv_meth", result.nouv_meth.notes, result.nouv_meth.present, intervenant_name, run_number, run_start_time
        ))

        conn.commit()
    except Exception as e:
        logger.error(f"Database error: {e}")
