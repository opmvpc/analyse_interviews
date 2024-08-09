import sqlite3
import pandas as pd
from rich.console import Console
from rich.table import Table

# Connexion à la base de données
db_path = "results.db"
conn = sqlite3.connect(db_path)

# Initialisation de la console Rich
console = Console()

# Calcul du LLM quotient par code
llmq_query = """
SELECT
    code_name,
    COUNT(*) AS total_iterations,
    SUM(CASE WHEN est_present = 1 THEN 1 ELSE 0 END) AS positive_responses,
    SUM(CASE WHEN est_present = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS LLMq
FROM
    analysis_results
GROUP BY
    code_name
ORDER BY
    LLMq DESC;
"""
llmq_df = pd.read_sql_query(llmq_query, conn)

# Afficher le LLM quotient par code dans un tableau
llmq_table = Table(title="LLM Quotient par Code")
llmq_table.add_column("Code Name", justify="left", style="cyan", no_wrap=True)
llmq_table.add_column("Total Iterations", justify="right", style="magenta")
llmq_table.add_column("Positive Responses", justify="right", style="green")
llmq_table.add_column("LLMq", justify="right", style="yellow")

for _, row in llmq_df.iterrows():
    llmq_table.add_row(
        row["code_name"],
        str(row["total_iterations"]),
        str(row["positive_responses"]),
        f"{row['LLMq']:.2f}"
    )

console.print(llmq_table)
print("\n")

# Identifier les phrases avec le plus de correspondances positives, triées par intervenant
positive_phrases_query = """
SELECT
    r.segment_text,
    r.code_name,
    COUNT(*) AS positive_count,
    r.intervenant_name
FROM
    analysis_results r
WHERE
    est_present = 1
GROUP BY
    r.segment_text, r.code_name, r.intervenant_name
ORDER BY
    r.intervenant_name, positive_count DESC;
"""
positive_phrases_df = pd.read_sql_query(positive_phrases_query, conn)

# Afficher les segments de texte avec le plus de correspondances positives triées par intervenant
grouped = positive_phrases_df.groupby('intervenant_name')

for intervenant_name, group in grouped:
    console.print(f"\n[bold]Intervenant: {intervenant_name}[/bold]")
    phrases_table = Table(show_header=True, header_style="bold magenta")
    phrases_table.add_column("Code Name", style="cyan")
    phrases_table.add_column("Positive Count", justify="right", style="green")
    phrases_table.add_column("Segment Text", style="white")

    for _, row in group.iterrows():
        phrases_table.add_row(
            row["code_name"],
            str(row["positive_count"]),
            row["segment_text"]
        )

    console.print(phrases_table)

conn.close()
