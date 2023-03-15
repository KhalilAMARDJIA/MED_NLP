import json
import spacy
from spacy.matcher import PhraseMatcher
import pandas as pd
from helper_functions import extract_json_last_layer


nlp = spacy.blank("en")

def db_matcher(db_path: str, label: str) -> PhraseMatcher:
    """
    Create a PhraseMatcher object using the data in the specified JSON file.
    """
    with open(db_path) as file:
        db = json.load(file)
    phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    to_match = extract_json_last_layer(db)
    patterns = [nlp(text) for text in to_match]
    phrase_matcher.add(label, None, *patterns)
    return phrase_matcher


def apply_matchers(docs, matchers, labels):
    train_data = []
    for doc in docs:
        detections = []
        for matcher, label in zip(matchers, labels):
            detections.extend([(start, end, label) for idx, start, end in matcher(doc)])
        train_data.append({"text": doc.text, "label": detections})
    return train_data

def main(list_of_text, matchers, output_path):
    docs = nlp.pipe(list_of_text)

    train_data = []
    for doc in docs:
        detections = []
        for matcher in matchers:
            for idx, start, end in matcher[0](doc):
                detections.append((doc[start:end].start_char, doc[start:end].end_char, matcher[1]))
        train_data.append({"text": doc.text, "label": detections})
    jsonl_data = "\n".join(json.dumps(d) for d in train_data)
    with open(output_path, 'w') as f:
        f.write(jsonl_data)


df = pd.read_csv('input/raw_data.csv', sep=';')
text = df['abstract'].dropna()

if __name__ == "__main__":
    AE_matcher = db_matcher(db_path="input/matcher_db/complications_db.json", label= "ADVERSE_EVENT")
    OUTCOME_matcher = db_matcher(db_path="input/matcher_db/scores_db.json", label= "OUTCOME")
    main(
        list_of_text = text, 
        matchers = [(AE_matcher, 'ADVERSE_EVENT'), (OUTCOME_matcher, 'OUTCOME')],
        output_path="input/matcher_preprocess.jsonl")


