import fitz
import spacy

# Load the SpaCy model
nlp = spacy.load("Model/model-best")

# Define colors for each entity type
colors = {"OUTCOME": [0.8, 1, 0.8],  # light green color (r, g, b)
          "ADVERSE_EVENT": [1, 0.8, 0.8],  # light red color (r, g, b)
          "OTHER": [1, 1, 0.8],  # light yellow color (r, g, b)
          "DEVICE": [0.8, 0.8, 1]}  # light blue color (r, g, b)

# Open the PDF file using PyMuPDF
pdf_file = fitz.open("pdfs/test.pdf")

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
pdf_file.save("pdfs/test_highlighted.pdf")
