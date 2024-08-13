import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

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

def get_high_llmq_segments(run_id, db_path="caca.db", threshold=0.9):
    """Récupère le nombre de segments avec un LLMq supérieur à 90% pour un run spécifique."""
    conn = sqlite3.connect(db_path)

    query = """
    WITH llmq_calculations AS (
        SELECT
            code_name,
            segment_text,
            CAST(SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS llmq
        FROM
            analysis_results
        WHERE
            run_id = ?
        GROUP BY
            code_name, segment_text
    )
    SELECT
        code_name,
        COUNT(*) AS segment_count
    FROM
        llmq_calculations
    WHERE
        llmq >= ?
    GROUP BY
        code_name;
    """
    result = pd.read_sql_query(query, conn, params=(run_id, threshold))

    conn.close()
    return result

def create_high_llmq_histogram(llmq_df, output_dir):
    """Crée un histogramme du nombre de segments avec un LLMq > 90% par code."""
    if llmq_df.empty:
        print("Aucune donnée trouvée pour le run ID spécifié.")
        return

    # Remplacer les codes par des labels en français
    llmq_df['code_name'] = llmq_df['code_name'].map(label_mapping)

    # Agréger les données par code_name
    aggregated_data = llmq_df.groupby('code_name')['segment_count'].sum().sort_values()

    # Créer l'histogramme
    plt.figure(figsize=(10, 6))
    ax = aggregated_data.plot(kind='barh', color='skyblue', edgecolor='black')

    plt.xlabel('Nombre de segments')
    plt.ylabel('Codes')
    plt.title('Nombre de segments avec un LLMq > 90% par code (40 itérations)')
    plt.grid(True)

    # Ajouter les valeurs au-dessus des barres
    for container in ax.containers:
        ax.bar_label(container)

    # Sauvegarder l'histogramme
    output_path = os.path.join(output_dir, 'high_llmq_histogram_40_iterations.png')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def get_high_llmq_segments_by_participant(run_id, db_path="caca.db", threshold=0.9):
    """Récupère le nombre de segments avec un LLMq supérieur à 90% par code et par participant."""
    conn = sqlite3.connect(db_path)

    query = """
    WITH llmq_calculations AS (
        SELECT
            code_name,
            intervenant_name,
            segment_text,
            CAST(SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS llmq
        FROM
            analysis_results
        WHERE
            run_id = ?
        GROUP BY
            code_name, intervenant_name, segment_text
    )
    SELECT
        code_name,
        intervenant_name,
        COUNT(*) AS segment_count
    FROM
        llmq_calculations
    WHERE
        llmq >= ?
    GROUP BY
        code_name, intervenant_name;
    """
    result = pd.read_sql_query(query, conn, params=(run_id, threshold))

    conn.close()
    return result
def create_high_llmq_histogram_by_participant(llmq_df, output_dir):
    """Crée un histogramme du nombre de segments avec un LLMq > 90% par code et par participant (barres séparées)."""
    if llmq_df.empty:
        print("Aucune donnée trouvée pour le run ID spécifié.")
        return

    # Remplacer les codes par des labels en français
    llmq_df['code_name'] = llmq_df['code_name'].map(label_mapping)

    # Pivot de la table pour obtenir les données dans un format de tableau croisé dynamique
    pivot_table = llmq_df.pivot_table(index='code_name', columns='intervenant_name', values='segment_count', aggfunc='sum', fill_value=0)

    # Utilisation d'une palette avec des nuances de bleu
    colors = ['#f0f9ff', '#bae6fd', '#38bdf8', '#0284c7', '#075985', '#082f49']

    ax = pivot_table.plot(kind='bar', figsize=(14, 8), color=colors, width=0.8, edgecolor='black')

    plt.xlabel('Codes')
    plt.ylabel('Nombre de segments')
    plt.title('Nombre de segments avec un LLMq > 90% par code et par participant (40 itérations)')
    plt.legend(title="Participants", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)

    # Ajouter les valeurs au-dessus des barres
    for container in ax.containers:
        ax.bar_label(container)

    # Sauvegarder l'histogramme
    output_path = os.path.join(output_dir, 'high_llmq_histogram_by_participant_40_iterations.png')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
