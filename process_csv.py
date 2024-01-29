import pandas as pd
import csv

# read CSV file
csv_file = 'script_data.csv'
df = pd.read_csv(csv_file)

# calculate LineId, which is filmname and line count for the film
df['LineId'] = df.groupby('FilmName').cumcount() + 1
df['LineId'] = df['FilmName'] + '-' + df['LineId'].astype(str)

# reorganize the columns with LineId as the first column
df = df[['LineId', 'CharacterName', 'Dialogue', 'CharacterLineNumber', 'FilmName', 'URL', 'Franchise']]
df = df.rename(columns={
    'LineId': 'line_id',
    'CharacterName': 'character_name',
    'Dialogue': 'dialogue',
    'CharacterLineNumber': 'character_line_number',
    'FilmName': 'film',
    'URL': 'url',
    'Franchise': 'franchise'
})


# additional data processing code here

# create a new CSV file with LineId
output_csv_file = 'script_data_processed.csv'
df.to_csv(output_csv_file, index=False, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
