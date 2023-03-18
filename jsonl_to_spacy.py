import jsonlines
import spacy
from random import sample 
from spacy.tokens import DocBin
import logging
import json

logging.basicConfig(level=logging.INFO)

def read_jsonlines_file(file_path:str)->list:
    """Read the jsonlines file and return the data as a list"""
    data = []
    try:
        with jsonlines.open(file_path, mode='r') as reader:
            data = [example for example in reader]
    except Exception as e:
        logging.error(f"Error in reading jsonlines file: {e}")
    return data

def extract_text_and_entities(data:list)->list:
    """Extract text and entities from the data"""
    training_data =[]
    for eg in data:
        text = eg['text']
        entities = eg['label']
        for start, end, label in entities:
            if start > len(text) or end > len(text):
                logging.warning(f"Entities index out of range for text: {text}")
                continue
        training_data.append((text, entities))
    return training_data

def rand_split_list(input_list:list, split_ratio:float)->tuple:
    """Split the input_list into train and validation datasets"""
    train_data = sample(input_list, int(len(input_list)*split_ratio))
    test_data = [i for i in input_list if i not in train_data]
    return train_data, test_data


def convert_to_spacy_format(input_list:list,output_path:str):
    """Convert the input_list to spacy format and save to disk"""
    nlp = spacy.blank("en") # load a new spacy model
    db = DocBin() # create a DocBin object
    for text, annot in input_list: # data in previous format
        doc = nlp.make_doc(text) # create doc object from text
        ents = []
        for start, end, label in annot:# add character indexes
            span = doc.char_span(start, end, label=label)
            if span is None:
                logging.warning("Skipping entity")
                continue
            else:
                ents.append(span)
        doc.ents = ents # label the text with the ents
        db.add(doc)
    db.to_disk(output_path)

def main(file_path:str, train_ratio:float, valid_ratio:float, test_ratio:float, 
         training_output_path:str, validation_output_path:str, test_output_path:str):
    data = read_jsonlines_file(file_path)
    training_data = extract_text_and_entities(data)
    train, rest = rand_split_list(training_data, train_ratio)
    valid, test = rand_split_list(rest, valid_ratio / (1 - train_ratio))
    convert_to_spacy_format(input_list= train, output_path=training_output_path)
    convert_to_spacy_format(input_list= valid, output_path=validation_output_path)
    convert_to_spacy_format(input_list= test, output_path=test_output_path)

if __name__ == "__main__":
    with open('project_config.json', 'r') as f:
        config_data = json.load(f)
    file_path = config_data['jsonl_to_convert']
    train_ratio = config_data['jsonl_train_ratio']
    valid_ratio = config_data['jsonl_valid_ratio']
    test_ratio = config_data['jsonl_test_ratio']
    main(
        file_path=file_path, 
        train_ratio=train_ratio,
        valid_ratio=valid_ratio,
        test_ratio=test_ratio,
        training_output_path='input/training.spacy',
        validation_output_path='input/validation.spacy',
        test_output_path='input/test.spacy'
        )