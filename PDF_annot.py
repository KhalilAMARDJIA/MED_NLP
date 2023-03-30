import fitz
import spacy
import os
import json
from tqdm import tqdm

def load_spacy_model(model_name: str, use_gpu: bool = False) -> spacy.language.Language:
    """
    Loads a SpaCy NER model and sets up GPU acceleration if specified.

    Args:
        model_name (str): The name of the SpaCy model to load.
        use_gpu (bool): Whether or not to use GPU acceleration. Defaults to False.

    Returns:
        The loaded SpaCy model.
    """
    if use_gpu:
        spacy.require_gpu()
    else:
        spacy.require_cpu()

    return spacy.load(model_name)

def load_config(config_path: str) -> dict:
    """
    Loads a project configuration JSON file.

    Args:
        config_path (str): The path to the project configuration JSON file.

    Returns:
        A dictionary containing the loaded configuration data.
    """
    with open(config_path, 'r') as f:
        return json.load(f)

def highlight_pdf_file(pdf_file_path: str, output_file_path: str, nlp_model: spacy.language.Language, colors: dict) -> None:
    """
    Highlights named entities in a PDF file using the provided SpaCy NER model and saves the modified PDF file.

    Args:
        pdf_file_path (str): The path to the input PDF file.
        output_file_path (str): The path to the output PDF file.
        nlp_model (spacy.language.Language): The SpaCy NER model to use.
        colors (dict): The color mappings for the named entity types.

    Returns:
        None
    """
    # Open the PDF file using PyMuPDF
    pdf_file = fitz.open(pdf_file_path)

    # Loop over each page in the PDF file
    for page in pdf_file:
        # Perform NER on the page's text
        text = page.get_text()
        doc = nlp_model(text)

        # Loop over each named entity and find its location on the page
        for entity in doc.ents:
            # Get the coordinates of the named entity
            try:
                bbox = page.search_for(entity.text)[0]  # find the first occurrence
            except:
                continue

            # Get the color for this entity type
            color = colors.get(entity.label_, colors["OTHER"])

            # Add a highlight annotation to the PDF page with the appropriate color
            highlight = page.add_highlight_annot(bbox)
            highlight.set_colors(stroke=color)
            highlight.update()

    # Save the modified PDF file
    pdf_file.save(output_file_path)

from tqdm import tqdm

if __name__ == "__main__":
    # Load the project configuration JSON file
    project_config = load_config('project_config.json')

    # Define the SpaCy model to use
    model_name = project_config['model']

    # Define the path to the project configuration JSON file
    config_path = project_config['config_path']

    # Load the SpaCy model
    nlp_model = load_spacy_model(model_name, use_gpu=False)

    # Load the project configuration JSON file
    config = load_config(config_path)

    # Extract the colors dictionary from the loaded JSON file
    colors = config['ner_colors']['med_ner']

    # Get the list of PDF files in the pdfs folder
    pdf_folder_path = project_config['pdf_folder_path']
    pdf_files = [f for f in os.listdir(pdf_folder_path) if f.endswith(".pdf")]

    # Define the progress bar
    pbar = tqdm(total=len(pdf_files), desc='Highlighting PDF files')

    # Loop over each PDF file
    for pdf_file in pdf_files:
        # Construct the input and output file paths
        input_file_path = os.path.join(pdf_folder_path, pdf_file)
        output_file_name = os.path.splitext(pdf_file)[0] + '_highlighted.pdf'
        output_file_path = os.path.join(project_config['output_folder_path'], output_file_name)

        # Highlight named entities in the PDF file and save the modified file
        highlight_pdf_file(input_file_path, output_file_path, nlp_model, colors)

        # Update the progress bar
        pbar.update(1)
        
    # Close the progress bar
    pbar.close()