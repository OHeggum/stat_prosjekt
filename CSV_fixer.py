import pandas as pd
import csv

df = pd.read_csv('lego.population.csv', encoding='latin1')

columns_to_keep = ['Item_Number', 'Set_Name', 'Theme', 'Pieces', 'Price', 'Amazon_Price']
df = df[columns_to_keep]

df = df.dropna(subset=['Pieces'])

# Hvilken av disse to du kjører utgjør om du har med de to radene eller ikke.
#df = df.dropna(subset=['Price'])
#df = df.dropna(subset=['Price', 'Amazon_Price'], how='all')

df['Theme'] = df['Theme'].astype(str)
df['Theme'] = df['Theme'].str.replace(r'[^a-zA-Z0-9\s-]', '', regex = True)
df['Price'] = df['Price'].str.replace('\\$', '', regex = True)
#df['Amazon_Price'] = df['Amazon_Price'].str.replace('\\$', '', regex = True)

df['Price'] = df['Price'].astype(float)
#df['Amazon_Price'] = df['Amazon_Price'].astype(float)


df.to_csv('datasett_filtrert.csv', index=False)


csv_file = 'datasett_filtrert.csv'

varemerker = []
theme_count = -1
no_theme_count = 0

# Henter ut antall temaer, antall rader med og uten tema og printer rader med pris som 0.
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        if row[2] != "nan" and row[2] not in varemerker:
            varemerker.append(row[2])
        elif row[2] != "nan":
            theme_count += 1
        else:
            no_theme_count += 1
        if row[3] == 0:
            print(row)

varemerker.pop(0)
print (varemerker)
print ("has theme: " + str(theme_count))
print ("no theme: " + str(no_theme_count))