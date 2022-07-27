import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm


def count_hi_score(dict_: dict):
    count = 0
    for k, v in dict_.items():
        if k != SNILS_KSENIYA and v >= SCORE_KSENIYA:
            count += 1
    return count


if __name__ == '__main__':

    URL = 'https://isu.ru/Abitur/rating/main/'
    SNILS_KSENIYA = '160-073-321 17'  # СНИЛС
    SCORE_KSENIYA = 230

    options = Options()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')

    s = Service(r'C:\chromedriver\chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=options)
    # driver.maximize_window()  # разворачиваем браузер на весь экран

    wait = WebDriverWait(driver, 30)
    driver.implicitly_wait(10)

    list_spec = {
        'Прикладная математика и информатика' : 'b1f77618-ae8d',
        'Математическое моделирование': 'b84f2828-ae8d',
        'Фундаментальная информатика и информационные технологии': 'bea93f09-ae8d',
        'Проектирование и разработка информационных систем': 'cbac1221-ae8d',
        'Прикладная информатика в дизайне': '1f16585e-ae8f',
        'Прикладная информатика (разработка программного обеспечения)': '1f165862-ae8f',
        'Техническая защита информации': '46b773e8-ae8f',
        'Безопасность автоматизированных систем': '4cd389f3-ae8f',
        'Электроника и наноэлектроника': '54423172-ae8f'
    }

    try:
        data = {}
        uniq_data = {}
        for spec, link in list_spec.items():
            driver.get(f'https://isu.ru/Abitur/rating/main/?uid={link}-11ec-80fa-82761dd90eed')
            time.sleep(1)
            wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="s-abitur-body"]/tr')))
            tbl_ = driver.find_elements(By.XPATH, '//*[@id="s-abitur-body"]/tr')
            len_tbl = len(tbl_)
            res = {}
            print(len_tbl)
            time.sleep(0.5)
            for i, row in tqdm(enumerate(tbl_, start=1)):
                str1 = f'//*[@id="s-abitur-body"]/tr[{i}]/td[2]'
                str2 = f'//*[@id="s-abitur-body"]/tr[{i}]/td[9]'
                snils = row.find_elements(By.XPATH, str1)[0].text
                score = int(row.find_elements(By.XPATH, str2)[0].text)
                res[snils] = score

            data[spec] = res
            uniq_data.update(res)
        print(count_hi_score(uniq_data))
        print(len(uniq_data))
        print(uniq_data)

        result_list = [(snils, score) for snils, score in uniq_data.items()
                       if snils != SNILS_KSENIYA and score >= SCORE_KSENIYA]
        df = pd.DataFrame(result_list)
        df.to_excel('C:/Users/Sasha/Downloads/list_abitur_igu.xlsx')

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
