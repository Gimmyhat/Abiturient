import requests
from bs4 import BeautifulSoup
import pandas as pd

if __name__ == '__main__':

    BASE_URL = 'https://cis.istu.edu/served/rating.php?n='
    HEADERS = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.0.0 Safari/537.36',
        "Connection": "keep-alive"
    }

    dict_spec = {
        'Информатика и вычислительная техника': '23825',
        'Информационная безопасность': '23820',
        'Информационные системы и технологии': '23823',
    }

    for spec, link in dict_spec.items():
        resp = requests.get(f'{BASE_URL}{link}')
        soup = BeautifulSoup(resp.text, 'lxml')
        elem = soup.select_one('body > div:nth-child(2) > div > div.col-12.col-md-9 > div:nth-child(1) > table')
        content = pd.read_html(str(elem))
        content = pd.DataFrame(content[0])
        content.columns = ['П.п.',
                           'Абитуриент',
                           'Вступительные испытания',
                           'Суммарный балл',
                           'Приоритет',
                           'Согласие на зачисление',
                           'Подлинник документа об образовании']
        table = pd.DataFrame(content)
        table.to_excel(f'Списки ИРНИИТУ {spec}.xlsx', index=False)

