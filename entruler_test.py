import spacy


# try adding entityruler on top of ner

nlp = spacy.load('Model/scibert_scivocab_uncased')


# add entity ruler after ner
ruler = nlp.add_pipe("entity_ruler")
ruler.from_disk("input/matcher_db/entity_ruler_df.jsonl")


text = "the patient suffered a cystoid macular edema (CME) and Glistening. The suprachoroidal hemorrhage score after 3 months follow-up."

doc = nlp(text)


for ent in doc.ents:
    print(ent.text, ent.label_)