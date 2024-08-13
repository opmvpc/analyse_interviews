from graphs.combined_llmq_graph import create_output_directory, get_llmq_for_iterations, create_combined_llmq_graph
from graphs.high_llmq_histogram import get_high_llmq_segments, create_high_llmq_histogram
from graphs.high_llmq_histogram import get_high_llmq_segments_by_participant, create_high_llmq_histogram_by_participant

def main():
    run_ids = [
        "6e467237-78da-4b1f-a873-83517b9f9fd1",  # Run #14
        "54a76c50-fcfe-4573-a72e-87747ccb3301",  # Run #15
        "b6329cb0-360d-4880-b19a-b8899d60deeb",  # Run #16
        "f2ebaa52-ea50-444f-abd1-da77eb2fcf0c"   # Run #17
    ]

    # Générer le graphique combiné LLMq pour tous les runs
    llmq_df = get_llmq_for_iterations(run_ids)
    output_dir = create_output_directory()
    create_combined_llmq_graph(llmq_df, output_dir)

    # Générer l'histogramme pour le run à 40 itérations
    run_id_40_iterations = "b6329cb0-360d-4880-b19a-b8899d60deeb"  # Run #16 avec 40 itérations
    high_llmq_df = get_high_llmq_segments(run_id_40_iterations)
    create_high_llmq_histogram(high_llmq_df, output_dir)

    # Générer l'histogramme par participant pour le run à 40 itérations
    high_llmq_by_participant_df = get_high_llmq_segments_by_participant(run_id_40_iterations)
    create_high_llmq_histogram_by_participant(high_llmq_by_participant_df, output_dir)

    print(f"Graphiques créés et sauvegardés dans le dossier : {output_dir}")

if __name__ == "__main__":
    main()
