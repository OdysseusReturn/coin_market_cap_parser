import requests
from bs4 import BeautifulSoup
import csv
import re



def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)




def write_csv(data):
    with open('cmc.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'],
                         data['url'],
                         data['price']))




def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    # trs = soup.find('div', class_ = 'cmc-table__table-wrapper-outer').find('table').find_all('tr')
    trs = soup.find('tbody').find_all('tr')
    # print(trs)

    for tr in trs:
        tds = tr.find_all('td')
        # print(tds)

        try:
            name = tds[1].find('a', class_ = 'cmc-link').text.strip()
        except:
            name = ''

        try:
            url = "https://coinmarketcap.com" + tds[1].find('a', class_ = 'cmc-link').get('href')
        except:
            url = ''

        try:
            price = tds[3].find('a', class_ = 'cmc-link').text
        except:
            price = ''

        data = {'name': name,
                'url': url,
                'price': price}

        write_csv(data)


def main():
    url = 'https://coinmarketcap.com/'

    while True:
        get_page_data(get_html(url))

        soup = BeautifulSoup(get_html(url), 'lxml')

        pattern = 'Next 100 →'

        try:
            url = 'https://coinmarketcap.com' + soup.find('div', class_='cmc-split fk32h8-0 kixxiL').find('div', class_ = 'cmc-button-group va78v0-0 RDZiS').find('a', text=re.compile(pattern)).get('href')
        except:
            break


if __name__ == '__main__':
    main()