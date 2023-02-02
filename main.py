import csv
from bs4 import BeautifulSoup

from selenium import webdriver

driver = webdriver.Chrome()


def get_url(search_text):
    template = 'https://www.amazon.in/s?k={}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
    search_term = search_text.replace(' ', '+')

    url = template.format(search_term)

    url += '&page={}'

    return url


url = get_url('bags')
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')
results = soup.find_all('div', {'data-component-type': 's-search-result'})


def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    result = (description, price, rating, review_count, url)

    return result


def main(search_term):
    driver = webdriver.Chrome()

    records = []
    additional_info = []
    url = get_url(search_term)

    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()

    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
        writer.writerows(records)


main('Bags')
