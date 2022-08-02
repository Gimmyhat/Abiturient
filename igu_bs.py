import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup


def count_hi_score(dict_: dict):
    count = 0
    for k, v in dict_.items():
        if k != SNILS_KSENIYA and v >= SCORE_KSENIYA:
            count += 1
    return count


if __name__ == '__main__':

    URL = 'https://isu.ru/Abitur/rating/main/'

    options = Options()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')

    s = Service(r'C:\chromedriver\chromedriver.exe')
    browser = webdriver.Chrome(service=s, options=options)

    wait = WebDriverWait(browser, 30)
    browser.implicitly_wait(10)

    list_spec = {
        # 'Прикладная математика и информатика': 'b1f77618-ae8d',
        # 'Математическое моделирование': 'b84f2828-ae8d',
        # 'Фундаментальная информатика и информационные технологии': 'bea93f09-ae8d',
        # 'Проектирование и разработка информационных систем': 'cbac1221-ae8d',
        'Прикладная информатика в дизайне': '1f16585e-ae8f',
        # 'Прикладная информатика (разработка программного обеспечения)': '1f165862-ae8f',
        # 'Техническая защита информации': '46b773e8-ae8f',
        # 'Безопасность автоматизированных систем': '4cd389f3-ae8f',
        # 'Электроника и наноэлектроника': '54423172-ae8f'
    }

    try:
        for spec, link in list_spec.items():
            browser.get(f'https://isu.ru/Abitur/rating/main/?uid={link}-11ec-80fa-82761dd90eed')
            wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="s-abitur-body"]/tr')))
            html = browser.page_source
            soup = BeautifulSoup(html, "html.parser")
            elem = soup.select_one('#s-abitur > table')
            content = pd.read_html(str(elem))
            content = pd.DataFrame(content[0])
            content.columns = ['Место в конкурсе',
                               'СНИЛС / код',
                               'Участие в конкурсе',
                               'Состояние заявления',
                               'Согласие на зачисление',
                               'Согласие в другой конкурсной группе',
                               'Оригинал документов',
                               'Вступительные испытания',
                               'Индивидуальные достижения',
                               'Сумма баллов']
            table = pd.DataFrame(content)
            table.to_excel(f'Списки ИГУ {spec}.xlsx', index=False)

    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()
