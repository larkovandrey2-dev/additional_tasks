from datetime import datetime
from bs4 import BeautifulSoup
from dateutil.parser import parse
import requests
import warnings
import re

warnings.filterwarnings('ignore')

VOYAGER_URL = 'https://science.nasa.gov/mission/voyager/voyager-1/'
RFC1149_URL = 'https://datatracker.ietf.org/doc/rfc1149/history/'
UNICODE_URL = 'https://unicode.org/Public/emoji/14.0/emoji-test.txt'
BTC_URL = 'https://www.blockchain.com/ru/explorer/blocks/btc/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'
ISBN_URL = 'https://www.cs.princeton.edu/~bwk/cbook.html'
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15'})


def do_request(url, timeout=10):
    try:
        page = session.get(url, timeout=timeout)
        return page
    except Exception as e:
        warnings.warn(f'Request to {url} failed: {e}')
        return None


# Находим дату запуска Вояджера
def get_voyager(page):
    if page is None:
        return None
    soup = BeautifulSoup(page.content, 'lxml')
    table_date = soup.find('figure', {'class': 'wp-block-table'}).find('table').find_all('tr')
    for tr in table_date:
        tds = tr.find_all('td')
        if 'launch' in tds[0].text.lower() and 'date' in tds[0].text.lower():
            voyager_date = parse(tds[1].text).strftime('%Y%m%d')
            return voyager_date
    return None


# Находим дату публикации rfc1149
def get_rfc1149(page):
    if page is None:
        return None
    soup = BeautifulSoup(page.content, 'lxml')
    table_rfc = soup.find('body').find('div', {'class': 'row'}).find('table').find_all('tr')
    for tr in table_rfc:
        tds = tr.find_all('td')
        if tds and any('published' in tds[i].text.lower() for i in range(len(tds))):
            return parse(tds[0].text).strftime('%Y%m%d')
    return None


# Unicode brain from offical unicode resource
def get_unicode(page):
    if page is None:
        return None
    req_unicode = page.text.split('\n')
    for row in req_unicode:
        if 'brain' in row:
            return row.split(' ')[0]
    return None


# btc-genesis date from blockchain.com
def get_btc_genesis_date(page):
    if page is None:
        return None
    soup = BeautifulSoup(page.text, 'lxml')
    btc_divs = soup.find('section').find_all('div', )
    for div in btc_divs:
        for row in div.find_all('div'):
            try:
                return parse(row.text).strftime('%Y%m%d')
            except Exception as e:
                continue
    return None


# isbn-10 from princeton offical site
def get_isbn10(page):
    if page is None:
        return None
    exp = r'ISBN [0-9]+-[0-9]+-[0-9]+-[0-9]+'
    return str(re.search(exp, page.text).group()).split()[1].replace('-', '')


# ------Немного тестов перед сборкой флага------
def is_right_date_format(date: str) -> bool:
    if not date or len(date) != 8:
        return False
    try:
        datetime.strptime(date, '%Y%m%d')
        return True
    except Exception:
        return False


def is_right_isbn_format(isbn: str) -> bool:
    if not isbn or len(isbn) != 10:
        return False
    return isbn.isdigit()


def is_right_unicode(uni: str) -> bool:
    if not uni:
        return False
    try:
        int(uni, 16)
        return True
    except Exception:
        return False


VOYAGER = get_voyager(do_request(VOYAGER_URL))
RFC1149 = get_rfc1149(do_request(RFC1149_URL))
BRAIN_CODE = get_unicode(do_request(UNICODE_URL))
BTC_DATE = get_btc_genesis_date(do_request(BTC_URL))
ISBN_10 = get_isbn10(do_request(ISBN_URL))


def run_validation():
    errors = 0
    for i in [VOYAGER, RFC1149, BTC_DATE]:
        if not is_right_date_format(i):
            print(f'{i} is not right date format')
            errors += 1
    if not is_right_isbn_format(ISBN_10):
        print(f'{ISBN_10} is not right isbn format')
        errors += 1
    if not is_right_unicode(BRAIN_CODE):
        print(f'{BRAIN_CODE} is not right unicode')
        errors += 1
    if errors:
        print('Validation failed with ', errors, ' errors. The format might be wrong.')
        return False
    print('Validation passed')
    return True


if __name__ == '__main__':
    run_validation()
    FLAG = 'FLAG{' + VOYAGER + '-' + RFC1149 + '-' + BRAIN_CODE + '-' + BTC_DATE + '-' + ISBN_10 + '}'
    print(FLAG)
