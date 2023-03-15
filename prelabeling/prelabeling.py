import spacy
import jsonlines
import pandas as pd

nlp = spacy.load('Model/model-best')

dat = pd.read_csv('input/raw_data.csv', sep=";")
dat = dat.abstract.dropna()
dat = dat.drop_duplicates()

with jsonlines.open('prelabeling/autolabeled.jsonl', mode='w') as writer:
    for i, doc in enumerate(nlp.pipe(dat)):
        entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
        writer.write({
            "id": i + 1,
            "text": doc.text,
            "label": entities
        })
