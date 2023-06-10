import spacy
import pandas as pd

# Use GPU if available
spacy.prefer_gpu()
# Load pre-trained model
nlp = spacy.load('Model/scibert_scivocab_cased')

# Read text from file
with open('/home/khalil/Documents/PROJECTS/GET_PUBMED/extracted_text/34689301.pdf.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Process text with model
doc = nlp(text)

# Extract entities from processed text
entities = {'label': [], 'text': []}
for ent in doc.ents:
    entities['label'].append(ent.label_)
    entities['text'].append(ent.text)

# Remove duplicate entities
df_entities = pd.DataFrame(entities)
df_entities = df_entities.drop_duplicates()


# pivot table based on label
df_entities = df_entities.pivot(index='text', columns='label', values='text').reset_index()