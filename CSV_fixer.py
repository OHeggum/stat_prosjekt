import pandas as pd
import csv

df = pd.read_csv('lego.population.csv', encoding='latin1')

columns_to_keep = ['Item_Number', 'Set_Name', 'Theme', 'Pieces', 'Price']
df = df[columns_to_keep]

df = df.dropna()

df['Theme'] = df['Theme'].astype(str)
df['Theme'] = df['Theme'].str.replace(r'[^a-zA-Z0-9\s-]', '', regex = True)
df['Price'] = df['Price'].str.replace('\\$', '', regex = True)

df['Price'] = df['Price'].astype(float)


themes = ['Disney', 'Star Wars', 'Minecraft', 'Marvel', 'Batman',
            'LEGO Frozen 2','LEGO Super Mario', 'Harry Potter',
            'Trolls World Tour','Minions', 'Powerpuff Girls',
            'Jurassic World', 'Overwatch', 'Spider-Man', 'DC', 'Stranger Things']

unknown_theme = ['Speed Champions', 'BrickHeadz', 'Juniors', 'Architecture', 'Ideas',
                 'Creator Expert', 'LEGO Art', 'Minifigures', 'LEGO Brick Sketches']

with open("datasett_filtrert.csv", 'r') as file:
    reader = csv.reader(file)
    data = list(reader)
    header = data[0]

header.append('Theme_or_not')

target_column_name = "Theme"

target_column_index = header.index(target_column_name)

for row in data[1:]:
    item = row[target_column_index]
    if item in themes:
        value = "Yes"
    elif item in unknown_theme:
        value = "Unknown"
    else:
        value = "No"
    row.append(value)
with open("datasett_filtrert.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)