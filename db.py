import sqlite3
import uuid
import os
import logging
from datetime import datetime
import time
import random

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
        logger.info("La base de données n'existe pas. Création de la base de données...")
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
        logger.info("Base de données créée avec succès.")
    else:
        logger.info("La base de données existe déjà. Connexion en cours...")

    return db_path

def save_result_to_db(conn, run_id, segment, result, intervenant_name, run_number, run_start_time, max_retries=5, base_delay=0.1):
    retries = 0
    while retries < max_retries:
        cursor = None
        try:
            cursor = conn.cursor()

            # Début d'une transaction
            cursor.execute("BEGIN")

            # Liste des codes à insérer
            codes = [
                ("tps_gagne", result.tps_gagne),
                ("prod_aug", result.prod_aug),
                ("auto", result.auto),
                ("prop_cont", result.prop_cont),
                ("biais_err", result.biais_err),
                ("corr_biais", result.corr_biais),
                ("eng_etu", result.eng_etu),
                ("prat_am", result.prat_am),
                ("inno_peda", result.inno_peda),
                ("meth_ens", result.meth_ens)
            ]

            # Insertion pour chaque code
            for code_name, code_result in codes:
                cursor.execute("""
                    INSERT INTO analysis_results (
                        id, run_id, segment_text, code_name, carnet_de_notes, present, intervenant_name, run_number, run_start_time
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()), run_id, segment, code_name, code_result.notes, code_result.present, intervenant_name, run_number, run_start_time
                ))

            # Commit de la transaction
            conn.commit()
            logger.info(f"Successfully saved results for segment in run {run_id}")
            return  # Succès, sortie de la fonction

        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                retries += 1
                if retries == max_retries:
                    logger.error(f"Failed to save to database after {max_retries} attempts: {e}")
                    raise

                delay = (base_delay * 2 ** retries) + (random.randint(0, 1000) / 1000.0)
                logger.warning(f"Database is locked. Retrying in {delay:.2f} seconds... (Attempt {retries}/{max_retries})")
                time.sleep(delay)
            else:
                logger.error(f"Operational error occurred: {e}")
                raise
        except Exception as e:
            logger.error(f"Unexpected error while saving to database: {e}")
            raise
        finally:
            if cursor:
                try:
                    cursor.execute("ROLLBACK")
                except sqlite3.OperationalError:
                    # Ignore l'erreur si aucune transaction n'est active
                    pass

    logger.error(f"Failed to save to database after {max_retries} attempts.")
    raise Exception("Maximum retries reached while trying to save to database")
