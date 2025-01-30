import re
import requests
from bs4 import BeautifulSoup
import time
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3 Edg/16.16299',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
]

headers = {
    'User-Agent': random.choice(user_agents)
}

def fetch_company_data(company_link):
    headers = {
        'User-Agent': random.choice(user_agents)
    }

    try:
        response = requests.get(company_link, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        main_div = soup.find('div', class_='main')

        if main_div:
            content_div = main_div.find('div', class_='content')

            if content_div:
                card_divs = content_div.find_all('div', class_='card w-100 p-1 p-lg-3 mt-1')

                if len(card_divs) > 1:
                    div = card_divs[1]

                    table = div.find('table')

                    if table:
                        company_info = {}
                        rows = table.find_all('tr')

                        for row in rows:
                            cells = row.find_all('td')
                            if len(cells) == 2:
                                key = cells[0].get_text(strip=True)
                                value = cells[1].get_text(strip=True)
                                company_info[key] = value
                        if ("ликвидация" in company_info.get("Статус", "").lower() or
                                "банкрот" in company_info.get("Статус", "").lower()):
                            print(
                                f"Пропускаем компанию: {company_info.get('Полное юридическое наименование')}, статус: {company_info['Статус']}")
                            return None

                        card_divs = content_div.find_all('div', class_='card w-100 p-1 p-lg-3 mt-2')

                        contact_div = card_divs[0].find_all('div')[1]
                        contact_p = contact_div.find_all("p")

                        # Извлечение телефона
                        phone = contact_p[1].find("span")

                        if phone:
                            company_info["Телефон"] = phone.get_text(strip=True)
                        else:
                            company_info["Телефон"] = "нет информации"

                        # Извлечение email
                        email = contact_p[2].find("i" , class_="fa-sm fa fa-at fa-fw")
                        if email:
                            company_info["E-mail"] = email.get_text(strip=True)
                        else:
                            company_info["E-mail"] = "нет информации"

                        # Извлечение сайта
                        site = contact_div.find('i', class_='fa-sm fa fa-link fa-fw')
                        if site:
                            company_info["Сайт"] = site.get_text(strip=True)
                        else:
                            company_info["Сайт"] = "нет информации"

                        # Извлечение данных о доходах и расходах (card_divs[8])
                        income_expense_div = card_divs[7]
                        income_expense_table = income_expense_div.find('table')

                        if income_expense_table:
                            income_expense_rows = income_expense_table.find_all('tr')
                            for income_expense_row in income_expense_rows[1:]:  # Пропускаем заголовок
                                income_expense_cells = income_expense_row.find_all('td')
                                if len(income_expense_cells) == 4:  # Год, доходы, расходы, разница
                                    income = income_expense_cells[1].get_text(strip=True)
                                    expense = income_expense_cells[2].get_text(strip=True)
                                    difference = income_expense_cells[3].get_text(strip=True)
                                    company_info["Доходы"] =income
                                    company_info["Расходы"] =expense
                                    company_info["Разница"] =difference

                        return company_info
                    else:
                        print("Таблица не найдена в карточке.")

                else:
                    print("Контентный div не найден.")
                    return []
            else:
                print("Основной div не найден.")

    except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None