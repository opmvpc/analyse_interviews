import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime


# Tableau de correspondance run_id -> nombre d'itérations
iteration_mapping = {
    "6e467237-78da-4b1f-a873-83517b9f9fd1": 10,  # Run #14
    "54a76c50-fcfe-4573-a72e-87747ccb3301": 20,  # Run #15
    "b6329cb0-360d-4880-b19a-b8899d60deeb": 40,  # Run #16
    "f2ebaa52-ea50-444f-abd1-da77eb2fcf0c": 60   # Run #17
}

# Table de correspondance code -> label en français
label_mapping = {
    "tps_gagne": "Temps Gagné",
    "prod_aug": "Productivité Augmentée",
    "auto": "Autonomie",
    "prop_cont": "Propriété du Contenu",
    "biais_err": "Biais et Erreurs",
    "corr_biais": "Correction des Biais",
    "eng_etu": "Engagement Étudiant",
    "prat_am": "Pratiques Améliorées",
    "inno_peda": "Innovation Pédagogique",
    "meth_ens": "Méthodes d'Enseignement"
}

def create_output_directory(base_dir="visualizations"):
    """Crée un dossier avec un nom basé sur la datetime actuelle."""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(base_dir, timestamp)
    os.makedirs(output_dir)
    return output_dir

def get_llmq_for_iterations(run_ids, db_path="caca.db"):
    """Calcule le Combined Code LLMq par code pour chaque run_id."""
    conn = sqlite3.connect(db_path)
    llmq_data = []
    for run_id in run_ids:
        iteration_count = iteration_mapping[run_id]
        query = """
        SELECT
            code_name,
            CAST(SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS llmq
        FROM
            analysis_results
        WHERE
            run_id = ?
        GROUP BY
            code_name
        """
        result = pd.read_sql_query(query, conn, params=(run_id,))
        result['run_id'] = run_id
        result['iteration_count'] = iteration_count
        llmq_data.append(result)
    conn.close()
    return pd.concat(llmq_data, ignore_index=True) if llmq_data else pd.DataFrame()

def create_combined_llmq_graph(llmq_df, output_dir):
    """Crée un graphique du Combined Code LLMq pour différents codes à travers les itérations."""
    if llmq_df.empty:
        print("Aucune donnée trouvée pour les run IDs spécifiés.")
        return

    plt.figure(figsize=(12, 8))

    # Graphique pour chaque code_name
    for code_name in llmq_df['code_name'].unique():
        subset = llmq_df[llmq_df['code_name'] == code_name]
        label_fr = label_mapping.get(code_name, code_name)  # Récupérer le label en français

        plt.plot(subset['iteration_count'], subset['llmq'], marker='o', label=label_fr)

    plt.xlabel('Iterations')
    plt.ylabel('Combined Code LLMq')
    plt.title('Combined Code LLMq pour tous les extraits d\'interview à travers les itérations')

    # Positionner la légende à droite du graphique
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

    plt.grid(True)

    # Ajuster les marges pour faire de la place à la légende
    plt.subplots_adjust(right=0.75)

    # Sauvegarder le graphique
    output_path = os.path.join(output_dir, 'combined_llmq_graph.png')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
