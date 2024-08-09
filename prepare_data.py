import os
import re
import json
from datetime import datetime
from docx import Document

def load_and_segment_text(file_path):
    doc = Document(file_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

    # Remove leading and trailing whitespace and normalize spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Split text into sentences using regex to match end of sentence punctuation
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences

def group_sentences(sentences, group_size=3):
    grouped_sentences = [' '.join(sentences[i:i + group_size]) for i in range(0, len(sentences), group_size)]
    return grouped_sentences

def save_grouped_sentences_to_json(grouped_sentences, output_path):
    with open(output_path, 'w') as file:
        json.dump(grouped_sentences, file, ensure_ascii=False, indent=4)

def process_files(data_dir, output_dir, group_size=3):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(data_dir):
        if file_name.endswith('.docx') and not file_name.startswith('~$'):
            file_path = os.path.join(data_dir, file_name)
            output_file_name = file_name.replace('.docx', f'_grouped_{group_size}.json')
            output_path = os.path.join(output_dir, output_file_name)

            print(f"Processing {file_name}...")
            sentences = load_and_segment_text(file_path)
            grouped_sentences = group_sentences(sentences, group_size)
            save_grouped_sentences_to_json(grouped_sentences, output_path)
            print(f"Saved grouped file to {output_path}")

if __name__ == "__main__":
    data_dir = "./data/cleaned"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"./data/outputs_{timestamp}"

    process_files(data_dir, output_dir, group_size=3)
