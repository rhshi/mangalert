import requests
from bs4 import BeautifulSoup

page = requests.get('https://mangadex.org/updates/')
soup = BeautifulSoup(page.text, 'html.parser')
table = soup.find('table', class_='table table-striped table-sm')
table_body = table.find('tbody')
rows = table_body.find_all('tr')

data = []
for row in rows[:2]:
    eles = row.find_all('a')
    for ele in eles:
        try:
            title = ele['title']

        print(ele['href'])
        text = ele.text.strip()
        if text:
            print(text)
    print('------------')
    #cols = [ele.text.strip() for ele in cols]
    #data.append([ele for ele in cols if ele])


asdfasdfasdfasdf

