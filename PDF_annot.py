import fitz
import spacy
import os

def highlight_pdf(pdf_file_path: str, output_file_path: str, model: str, colors: dict):
    """
    Highlights named entities in a PDF file using the SpaCy NER model and saves the modified PDF file.

    Args:
        pdf_file_path (str): The path to the input PDF file.
        output_file_path (str): The path to the output PDF file.
        model (str): The name of the SpaCy model to use.
        colors (dict): A dictionary that maps entity types to colors.

    Returns:
        None
    """

    spacy.prefer_gpu()

    # Load the SpaCy model
    nlp = spacy.load(model)

    # Open the PDF file using PyMuPDF
    pdf_file = fitz.open(pdf_file_path)

    # Loop over each page in the PDF file
    for page_num in range(len(pdf_file)):
        # Load the current page
        page = pdf_file.load_page(page_num)
        # Perform NER on the page's text
        text = page.get_text()
        doc = nlp(text)

        # Loop over each named entity and find its location on the page
        for entity in doc.ents:
            # Get the coordinates of the named entity
            try:
                bbox = page.search_for(entity.text)[0]  # find the first occurrence
            except:
                pass

            # Get the color for this entity type
            if entity.label_ in colors:
                color = colors[entity.label_]
            else:
                color = colors["OTHER"]

            # Add a highlight annotation to the PDF page with the appropriate color
            highlight = page.add_highlight_annot(bbox)
            highlight.set_colors(stroke=color)
            highlight.update()

    # Save the modified PDF file
    pdf_file.save(output_file_path)

if __name__ == "__main__":
# Define the colors dictionary
    colors = {
        "OUTCOME": [0.8, 1, 0.8],         # light green color (r, g, b)
        "ADVERSE_EVENT": [1, 0.8, 0.8],   # light red color (r, g, b)
        "STUDY_DESIGN": [0.9 , 0.9 , 0.9], # light gray color (r,g,b)
        "DEVICE": [0.8, 0.8, 1],           # light blue color (r, g, b),
        "OTHER": [1, 1, 0.8],             # light yellow color (r, g, b)
        "AGE": [250/255 ,40/255 ,255/255] # purple color (r,g,b) from hex code #FA28FF
    }

    # Define the SpaCy model to use
    model = "Model/model-best"

    # Get the list of PDF files in the pdfs folder
    pdf_files = [f for f in os.listdir("pdfs") if f.endswith(".pdf")]

    # Loop over each PDF file
    for pdf_file in pdf_files:
        # Construct the input and output file paths
        input_file_path = os.path.join("pdfs", pdf_file)
        output_file_path = os.path.join("pdfs", "output", f"{os.path.splitext(pdf_file)[0]}_NER.pdf")

        # Highlight the named entities in the PDF file
        highlight_pdf(input_file_path, output_file_path, model, colors)