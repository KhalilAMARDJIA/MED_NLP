import pandas as pd

# load the data
data = pd.read_csv('input/event_data.csv', sep='|')
text = data.text.dropna()
text = '\n'.join(text)

# write the data into a text file

with open('input/training_text.txt', 'w') as file:
    file.write(text)
