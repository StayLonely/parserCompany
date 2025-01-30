import time

from fetch_company_data import fetch_company_data
from get_company_names import get_company_names


def scrape_companies(base_url, start_page, end_page):
    """
    Функция для сбора данных о компаниях с указанного диапазона страниц.

    :param base_url: Базовый URL для запросов.
    :param start_page: Начальная страница.
    :param end_page: Конечная страница.
    :return: Список данных о компаниях.
    """
    all_companies_data = []
    page_number = start_page

    while page_number <= end_page:
        url = f"{base_url}{page_number}"
        print(f"Обрабатываем страницу: {url}")

        company_info = get_company_names(url)

        if not company_info:
            print("Больше нет компаний на следующих страницах.")
            break

        for company_name, company_link in company_info:
            print(f"Обрабатываем компанию: {company_name}")
            company_data = fetch_company_data(company_link)

            if company_data:
                all_companies_data.append(company_data)

            time.sleep(30)

        page_number += 1


        time.sleep(60)

    return all_companies_data