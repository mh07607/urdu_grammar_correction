import pandas as pd
import numpy as np

# Read the CSV file into a DataFrame
file_names = ['standard_dataset.csv', 'custom_data.csv', 'c2c.csv']
dfs = [pd.read_csv(example) for example in file_names]

src = []
trg = []

# Iterate through the rows of the DataFrame
for df in dfs:
  for index, row in df.iterrows():
      src.append(row['X'].strip())
      trg.append(row['Y'].strip())
      
with open('test_src.txt', 'w', encoding='utf-8') as src_file:
    src_file.writelines('\n'.join(src))

with open('test_trg.txt', 'w', encoding='utf-8') as trg_file:
    trg_file.writelines('\n'.join(trg))