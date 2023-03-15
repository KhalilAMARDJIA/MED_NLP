import spacy
import pandas as pd
from spacy.matcher import Matcher
import json


df = pd.read_csv("input/raw_data.csv", sep=";")
texts = df.dropna(subset="abstract")["abstract"]



nlp = spacy.blank("en")
matcher = Matcher(nlp.vocab)


with open("input/matcher_db/patterns.json", "r") as f:
    patterns = json.load(f)

matcher.add("SAMPLE_SIZE", patterns['SAMPLE_SIZE'], greedy="LONGEST")
matcher.add("ADVERSE_EVENT", patterns['ADVERSE_EVENT'],greedy="LONGEST")


docs = nlp.pipe(texts)
entities = []
for doc in docs:
    matches = matcher(doc)
    entity = {"text": doc.text, "label": []}
    for match_id, start, end in matches:
        
        entity["label"].append([doc[start:end].start_char, doc[start:end].end_char, matcher.vocab.strings[match_id]])
    entities.append(entity)



with open("input/test.jsonl", "w") as outfile:
    for entity in entities:
        json.dump(entity, outfile)
        outfile.write("\n")
