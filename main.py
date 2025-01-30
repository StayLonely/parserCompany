import tkinter as tk
from tkinter import messagebox, ttk
from save_companies_toExcel import save_companies_toEscel
from scrape_companies import scrape_companies

# Список OКВЭДов
okved_codes = {
    "25.62": "Обработка металлических изделий механическая",
    "33.12": "Ремонт машин и оборудования",
    "33.20": "Монтаж промышленных машин и оборудования",
    "41.20": "Строительство жилых и нежилых зданий",
    "42.11": "Строительство автомобильных дорог и автомагистралей",
    "42.99": "Строительство прочих инженерных сооружений",
    "43.99": "Работы строительные специализированные прочие",
    "46.73.6": "Торговля оптовая прочими строительными материалами",
    "49.41": "Деятельность автомобильного грузового транспорта",
    "08.1": "Добыча камня, песка и глины"
}


def start_scraping():
    selected_code = okved_code_var.get()
    start_page = int(start_page_entry.get())
    end_page = int(end_page_entry.get())

    base_url = f"https://www.list-org.com/list?okved2={selected_code}&page="
    all_companies_data = scrape_companies(base_url, start_page, end_page)

    print(start_page)
    print(end_page)

    print(base_url)
    if all_companies_data:
        save_companies_toEscel(all_companies_data)
        messagebox.showinfo("Успех", "Данные успешно сохранены!")
    else:
        messagebox.showwarning("Предупреждение", "Нет данных для сохранения.")


root = tk.Tk()
root.title("Скрипт для сбора данных компаний")


okved_code_var = tk.StringVar(value=list(okved_codes.keys())[0])

tk.Label(root, text="Выберите код ОКВЭД:").grid(row=0, column=0, sticky=tk.W)


for idx, (code, description) in enumerate(okved_codes.items()):
    tk.Radiobutton(root, text=f"{code} - {description}", variable=okved_code_var, value=code).grid(row=idx + 1, column=0, sticky=tk.W)


tk.Label(root, text="Стартовая страница:").grid(row=len(okved_codes) + 1, column=0, sticky=tk.W)
start_page_entry = tk.Entry(root)
start_page_entry.insert(0, "0")
start_page_entry.grid(row=len(okved_codes) + 1, column=1)

tk.Label(root, text="Конечная страница:").grid(row=len(okved_codes) + 2, column=0, sticky=tk.W)
end_page_entry = tk.Entry(root)
end_page_entry.insert(0, "0")
end_page_entry.grid(row=len(okved_codes) + 2, column=1)


start_button = tk.Button(root, text="Начать сбор данных", command=start_scraping)
start_button.grid(row=len(okved_codes) + 3, columnspan=2)


root.mainloop()