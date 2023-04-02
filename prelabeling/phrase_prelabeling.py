import spacy
import jsonlines
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

spacy.prefer_gpu()

# load spacy model
nlp = spacy.load("en_core_sci_lg")

# read in CSV file
data = pd.read_csv('input/raw_data.csv', sep=";")

# convert abstracts to list of strings
sample_text = data['abstract'].sample(30).tolist()


# remove linebraks from sample text
sample_text = [sent.replace("\n", "") for sent in sample_text]

# process text with spacy pipeline
docs = nlp.pipe(sample_text)


# initialize list of sentences
sentences = []

# loop through docs and extract sentences
for doc in docs:
    # remove duplicate sentences
    unique_sents = list(set([sent.text for sent in doc.sents]))
    sentences.extend(unique_sents)

# calculate similarity scores between all pairs of sentences
similarity_matrix = np.zeros((len(sentences), len(sentences)))
for i in range(len(sentences)):
    for j in range(i+1, len(sentences)):
        doc1 = nlp(sentences[i])
        doc2 = nlp(sentences[j])
        similarity_score = doc1.similarity(doc2)
        similarity_matrix[i, j] = similarity_score
        similarity_matrix[j, i] = similarity_score


# cluster the sentences using K-means
n_clusters = 100
kmeans = KMeans(n_clusters=n_clusters)
clusters = kmeans.fit_predict(similarity_matrix)

# for each cluster, select the most different sentence
selected_sents = []
for cluster_id in range(n_clusters):
    cluster_indices = np.where(clusters == cluster_id)[0]
    if len(cluster_indices) == 0:
        continue
    cluster_similarities = similarity_matrix[cluster_indices][:, cluster_indices]
    most_different_idx = np.argmax(np.sum(cluster_similarities, axis=1))
    selected_sents.append(sentences[cluster_indices[most_different_idx]])


# load new spacy model
nlp = spacy.load("Model/BiomedNLP-KRISSBERT-PubMed-UMLS-EL")

# write labeled data to JSONL file
with jsonlines.open('prelabeling/sent_autolabeled.jsonl', mode='w') as writer:
    for i, doc in enumerate(nlp.pipe(selected_sents)):
        entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
        writer.write({
            "id": i + 1,
            "text": doc.text,
            "label": entities
        })
