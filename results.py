import sqlite3
import pandas as pd
import random
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt

# Connexion à la base de données
db_path = "caca.db"
conn = sqlite3.connect(db_path)

# Initialisation de la console Rich
console = Console()

# Fonction pour récupérer les IDs de run
def get_run_ids():
    query = """
    SELECT DISTINCT run_id, run_number, run_start_time
    FROM analysis_results
    ORDER BY run_start_time DESC;
    """
    return pd.read_sql_query(query, conn)

# Fonction pour afficher le menu de sélection des runs
def display_run_menu(run_ids):
    console.print("[bold]Sélectionnez un run à analyser:[/bold]")
    for i, row in run_ids.iterrows():
        run_id = row["run_id"]
        run_number = row["run_number"]
        run_start_time = row["run_start_time"]
        console.print(f"{i+1}. Run #{run_number} - ID: {run_id} - Start Time: {run_start_time}")

    choice = IntPrompt.ask("Entrez le numéro du run", choices=[str(i+1) for i in range(len(run_ids))])
    return run_ids.iloc[choice - 1]

# Fonction pour obtenir une justification aléatoire
def get_random_justification(run_id, segment_text, code_name):
    query = """
    SELECT carnet_de_notes
    FROM analysis_results
    WHERE run_id = ? AND segment_text = ? AND code_name = ? AND present = 1
    ORDER BY RANDOM()
    LIMIT 1
    """
    result = pd.read_sql_query(query, conn, params=(run_id, segment_text, code_name))
    return result['carnet_de_notes'].iloc[0] if not result.empty else "Pas de justification disponible"

# Fonction principale
def main():
    run_ids = get_run_ids()
    if run_ids.empty:
        console.print("[bold red]Aucun run trouvé dans la base de données.[/bold red]")
        return

    selected_run = display_run_menu(run_ids)
    selected_run_id = selected_run["run_id"]
    run_number = selected_run["run_number"]
    run_start_time = selected_run["run_start_time"]

    # Calcul du LLM quotient par code
    llmq_query = """
    SELECT
        code_name,
        COUNT(DISTINCT segment_text) AS total_segments,
        COUNT(*) AS total_iterations,
        SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END) AS positive_responses,
        SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS LLMq
    FROM
        analysis_results
    WHERE
        run_id = ?
    GROUP BY
        code_name
    ORDER BY
        LLMq DESC;
    """
    llmq_df = pd.read_sql_query(llmq_query, conn, params=(selected_run_id,))

    # Afficher le LLM quotient par code dans un tableau
    llmq_table = Table(title=f"LLM Quotient par Code pour le run {selected_run_id}")
    llmq_table.add_column("Code Name", justify="left", style="cyan", no_wrap=True)
    llmq_table.add_column("Total Segments", justify="right", style="magenta")
    llmq_table.add_column("Total Iterations", justify="right", style="magenta")
    llmq_table.add_column("Positive Responses", justify="right", style="green")
    llmq_table.add_column("LLMq", justify="right", style="yellow")

    for _, row in llmq_df.iterrows():
        llmq_table.add_row(
            row["code_name"],
            str(row["total_segments"]),
            str(row["total_iterations"]),
            str(row["positive_responses"]),
            f"{row['LLMq']:.2f}"
        )

    console.print(llmq_table)
    print("\n")

    # Créer le dossier 'results' s'il n'existe pas
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Obtenir l'heure de fin
    run_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Nom du fichier résultat avec le numéro du run et la date/heure
    output_filename = os.path.join(
        results_dir,
        f"resultats_{run_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    )

    # Ouvrir le fichier de sortie en mode écriture (écrasement)
    with open(output_filename, "w") as md_file:
        # Ajouter les informations du run au début du fichier
        md_file.write(f"# Résultats du Run #{run_number}\n\n")
        md_file.write(f"**Run ID**: {selected_run_id}\n\n")
        md_file.write(f"**Heure de début**: {run_start_time}\n\n")
        md_file.write(f"**Heure de fin**: {run_end_time}\n\n")
        md_file.write(f"**Total Segments**: {llmq_df['total_segments'].sum()}\n\n")
        md_file.write(f"**Total Iterations**: {llmq_df['total_iterations'].sum()}\n\n\n")

        # Ajouter le tableau LLMq au fichier Markdown
        md_file.write(f"## LLM Quotient par Code pour le run {selected_run_id}\n\n")

        # Ajouter les données du tableau au fichier markdown
        md_file.write("| Code Name | Total Segments | Total Iterations | Positive Responses | LLMq |\n")
        md_file.write("| --- | --- | --- | --- | --- |\n")

        for _, row in llmq_df.iterrows():
            md_file.write(f"| {row['code_name']} | {row['total_segments']} | {row['total_iterations']} | {row['positive_responses']} | {row['LLMq']:.2f} |\n")

        md_file.write("\n\n")

        # Identifier les phrases avec au moins 3 correspondances positives, triées par intervenant et limitées à 5 par code
        positive_phrases_query = """
        WITH ranked_phrases AS (
            SELECT
                r.segment_text,
                r.code_name,
                COUNT(*) AS positive_count,
                r.intervenant_name,
                ROW_NUMBER() OVER (PARTITION BY r.intervenant_name, r.code_name ORDER BY COUNT(*) DESC) AS rank
            FROM
                analysis_results r
            WHERE
                present = 1 AND run_id = ?
            GROUP BY
                r.segment_text, r.code_name, r.intervenant_name
        )
        SELECT
            segment_text,
            code_name,
            positive_count,
            intervenant_name
        FROM
            ranked_phrases
        WHERE
            rank <= 5 AND positive_count >= 3
        ORDER BY
            intervenant_name, code_name, positive_count DESC;
        """
        positive_phrases_df = pd.read_sql_query(positive_phrases_query, conn, params=(selected_run_id,))

        # Afficher les segments de texte avec le plus de correspondances positives triées par intervenant et par code
        grouped = positive_phrases_df.groupby(['intervenant_name', 'code_name'])

        for (intervenant_name, code_name), group in grouped:
            console.print(f"\n[bold]Intervenant: {intervenant_name} - Code: {code_name}[/bold]")
            phrases_table = Table(show_header=True, header_style="bold magenta")
            phrases_table.add_column("Positive Count", justify="right", style="green")
            phrases_table.add_column("Segment Text", style="white")
            phrases_table.add_column("Justification", style="yellow")

            # Écrire le titre de l'intervenant et du code dans le fichier markdown
            md_file.write(f"## Intervenant: {intervenant_name} - Code: {code_name}\n\n")

            # Ajouter l'en-tête du tableau
            md_file.write("| Nombre de positifs | Extrait positif | Justification |\n")
            md_file.write("| --- | --- | --- |\n")

            for _, row in group.iterrows():
                justification = get_random_justification(selected_run_id, row["segment_text"], code_name)
                phrases_table.add_row(
                    str(row["positive_count"]),
                    row["segment_text"],
                    justification
                )

                # Écrire chaque ligne du tableau dans le fichier markdown
                md_file.write(f"| {row['positive_count']} | {row['segment_text']} | {justification} |\n")

            console.print(phrases_table)
            md_file.write("\n")  # Ajouter un saut de ligne après chaque groupe

    console.print(f"[bold green]Résultats enregistrés dans {output_filename}[/bold green]")

if __name__ == "__main__":
    main()
    conn.close()
