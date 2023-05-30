import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_NBA_champions'
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')
table = soup.find('table', {'class': 'wikitable sortable'})

rows = []
for row in table.find_all('tr')[1:]:
    row_data = [data.text.strip() for data in row.find_all('td')]
    if not row_data:
        continue
    year = row.find_all('td')[0].text.strip()
    date = row_data[0]
    print(row_data[0])
    eastern_champ = row_data[1]
    western_champ = row_data[2]
    rows.append([year, date, eastern_champ, western_champ])

df = pd.DataFrame(rows, columns=['Year', 'Date', 'Eastern Champion', 'Western Champion'])
df['Year'] = df['Year'].astype(int)
df = df.sort_values(by='Year')
print(df)
