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

def get_company_names(url):
    headers = {
        'User-Agent': random.choice(user_agents)
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('body')
        main_div = body.find('div', class_='main')

        if main_div:
            content_div = main_div.find('div', class_='content')

            if content_div:
                card_div = content_div.find('div', class_='card w-100 p-1 p-lg-3 mt-1')

                if card_div:
                    org_list_div = card_div.find('div', class_='org_list')

                    if org_list_div:
                        company_info = []
                        p_elements = org_list_div.find_all('p')

                        for p in p_elements:
                            a_tag = p.find('a')
                            status_span = p.find('span', class_='status_0')

                            if a_tag and (status_span is None):
                                company_name = a_tag.get_text(strip=True)
                                company_link = "https://www.list-org.com" + a_tag['href']
                                company_info.append((company_name, company_link))

                        return company_info
                else:
                    print("Карточка не найдена.")
            else:
                print("Контент не найден.")
        else:
            print("Элемент main не найден.")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")

    return []