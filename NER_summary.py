import spacy
import pandas as pd

def extract_ner_from_data(input_file, output_file, model_name, id_col, text_col, separator=','):
    # load spacy model
    nlp = spacy.load(model_name)

    # load data
    data = pd.read_csv(input_file, sep=separator)

    # remove rows where abstract is null
    data = data[data[text_col].notna()].sample(10)

    # create a empty columns for each nlp ner label name in the data
    for column in nlp.pipe_labels['ner']:
        data[column] = ""

    # for each pmid matching pubmed_id, store doc.ents in its corresponding column
    # when multiple entities are found, separate them by a tab
    zip_data = zip(data[text_col], data[id_col])
    for doc, pmid in nlp.pipe(zip_data, as_tuples=True):
        for ent in doc.ents:
            if ent.label_ in data.columns:
                if data.loc[data[id_col] == pmid, ent.label_].empty:
                    data.loc[data[id_col] == pmid, ent.label_] = ent.text
                else:
                    data.loc[data[id_col] == pmid, ent.label_] += ent.text + '\t'

    # remove duplicate row wise and keep the longest string
    for column in nlp.pipe_labels['ner']:
        data[column] = data[column].apply(lambda x: remove_duplicate_keep_longest(x))

    # save data to csv file
    data.to_csv(output_file, sep=separator, index=False)
    
def remove_duplicate_keep_longest(text):
    """
    Remove duplicate and keep the longest string from a tab-separated string
    """
    if isinstance(text, str):
        entities = text.split('\t')
        entities = sorted(entities, key=len, reverse=True) # sort by length in descending order
        dedup_entities = []
        for entity in entities:
            if not any(entity in e for e in dedup_entities):
                dedup_entities.append(entity)
        return '\t'.join(dedup_entities)
    else:
        return text


extract_ner_from_data('input/raw_data.csv', 'output/NER_summary.csv', 'Model/scibert_scivocab_cased', id_col='pubmed_id', text_col='abstract', separator=';')