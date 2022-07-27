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
    SNILS_KSENIYA = '160-073-321 17'  # СНИЛС
    SCORE_KSENIYA = 230

    dict_spec = {
        'Информатика и вычислительная техника': '23825',
        'Информационная безопасность': '23820',
        'Информационные системы и технологии': '23823',
    }

    uniq_snils = set()
    for spec, link in dict_spec.items():
        resp = requests.get(f'{BASE_URL}{link}')
        soup = BeautifulSoup(resp.text, 'lxml')
        tables = soup.find_all('table', {'class': 'rating'})[1].find_all('td')

        snils = (x.text.replace('СНИЛС: ', '') for i, x in enumerate(tables)
                 if i in range(1, len(tables) * 6 + 1, 6))
        score = (int(x.text) for i, x in enumerate(tables)
                 if x.text and (i in range(3, len(tables) * 6 + 1, 6)))

        snils_score = set(zip(snils, score))
        uniq_snils.update(snils_score)

    result_list = [x for x in uniq_snils if x[1] >= SCORE_KSENIYA and x[0] != SNILS_KSENIYA]
    print(result_list)
    print(len(result_list))

    df = pd.DataFrame(result_list)
    df.to_excel('C:/Users/Sasha/Downloads/list_abitur_irniitu.xlsx')
