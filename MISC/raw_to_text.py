import pandas as pd

# load the data
data = pd.read_csv('input/raw_data.csv', sep=';')
text = data.abstract.dropna()
text = '\n'.join(text)

# write the data into a text file

with open('prelabeling/training_text.txt', 'w', encoding="utf-8") as file:
    file.write(text)

