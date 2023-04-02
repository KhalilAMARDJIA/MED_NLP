import spacy
import pandas as pd

# load spacy model
nlp = spacy.load("Model/scibert_scivocab_cased")

nlp.prefer_gpu()

data = pd.read_csv('input/raw_data.csv', sep=";")

data = data[data['abstract'].notna()].sample(100)

zip_data = zip(data['abstract'], data['pubmed_id'])


# create a empty columns for each nlp ner label name in the data

for column in  nlp.pipe_labels['ner']:
    data[column] = ""



# for each pmid matching pubmed_id, store doc.ents in its corresponding column
# when multiple entities are found, separate them by a tab
for doc, pmid in nlp.pipe(zip_data, as_tuples=True):
    for ent in doc.ents:
        if ent.label_ in data.columns:
            if data.loc[data['pubmed_id'] == pmid, ent.label_].empty:
                data.loc[data['pubmed_id'] == pmid, ent.label_] = ent.text
            else:
                data.loc[data['pubmed_id'] == pmid, ent.label_] +=  ent.text + '|' 

data.to_csv("output/NER_summary.csv", sep=',')