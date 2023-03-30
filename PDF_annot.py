import fitz
import spacy
import os
import json


def highlight_pdf(pdf_file_path: str, output_file_path: str, model: str, config_path: str, use_gpu: bool = False):
    """
    Highlights named entities in a PDF file using the SpaCy NER model and saves the modified PDF file.

    Args:
        pdf_file_path (str): The path to the input PDF file.
        output_file_path (str): The path to the output PDF file.
        model (str): The name of the SpaCy model to use.
        config_path (str): The path to the project configuration JSON file.
        use_gpu (bool): Whether or not to use GPU acceleration. Defaults to False.

    Returns:
        None
    """
    if use_gpu:
        spacy.require_gpu()
    else:
        spacy.require_cpu()

    # Load the SpaCy model
    nlp = spacy.load(model)

    # Open the PDF file using PyMuPDF
    pdf_file = fitz.open(pdf_file_path)

    # Load the project configuration JSON file
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Extract the colors dictionary from the loaded JSON file
    colors = config['ner']['med_ner']

    # Loop over each page in the PDF file
    for page in pdf_file:
        # Perform NER on the page's text
        text = page.get_text()
        doc = nlp(text)

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


if __name__ == "__main__":
    # Load the project configuration JSON file
    with open('project_config.json', 'r') as f:
        project_config = json.load(f)

    # Define the SpaCy model to use
    model = project_config['model']

    # Define the path to the project configuration JSON file
    config_path = project_config['config_path']

    # Get the list of PDF files in the pdfs folder
    pdf_folder_path = project_config['pdf_folder_path']
    pdf_files = [f for f in os.listdir(pdf_folder_path) if f.endswith(".pdf")]

    # Loop over each PDF file
    for pdf_file in pdf_files:
        # Construct the input and output file paths
        input_file_path = os.path.join(pdf_folder_path, pdf_file)
        output_file_path = os.path.join(pdf_folder_path, "output", f"{os.path.splitext(pdf_file)[0]}_NER.pdf")

        # Apply named entity highlighting to the PDF file
        highlight_pdf(input_file_path, output_file_path, model, config_path, use_gpu=False)