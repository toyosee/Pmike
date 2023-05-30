import requests, csv
from bs4 import BeautifulSoup



collection = {
    'years': [],
    'seasons': {}
}

def fetch_page(url):
    page = requests.get(url)
    return page


def get_html_from_page(page):
    return page.content


def make_soup(html) -> BeautifulSoup:
    soup = BeautifulSoup(html, 'html.parser')
    return soup



def scrape_data():
    try:
        page = fetch_page("https://www.basketball-reference.com/playoffs/series.html")
        soup = make_soup(page.content)
        table = soup.find_all('table', id='playoffs_series')[0]
        rows = table.find_all('tr')

        def get_seaons():
            for row in rows:
                yearCol = row.find('th', class_='left')
                if not yearCol == None:
                    year = yearCol.getText()
                    if not year in collection['years']:
                        collection['seasons'][year] = {'rows': [], 'data': {}}
                        collection['years'].append(year)
            return collection['years']
        
        seasons = get_seaons()

        for row in rows:
            year = row.find('th', class_='left')
            if not year == None: # row has year
                currentYear = year.getText()
                year_rows = collection['seasons'][currentYear]['rows']
                year_rows.append(row)
        

            csv_headers = ['year', 'playoffs_date', 'west_winner', 'east_winner']
            with open('data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Write the column headers to the CSV file
                writer.writerow(csv_headers)

                for year in seasons:
                    rows = collection['seasons'][year]['rows']
                    try:
                        playoff = rows[0]
                        east_champ = rows[-2]
                        west_champ = rows[-3]

                        playoff = playoff.find_all('td')[2].getText()
                        playoff = playoff.split(' - ')[0]
                        west_champ = west_champ.find_all('td')[4].getText().split(' (')[0]
                        east_champ = east_champ.find_all('td')[4].getText().split(' (')[0]

                        writer.writerow([year, playoff, west_champ, east_champ])
                    except Exception as e:
                        pass

    except Exception as error:
        print("Error:", error)



if __name__ == '__main__':
    scrape_data()
