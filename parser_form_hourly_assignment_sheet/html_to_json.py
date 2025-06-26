
import os
import shutil
import json
from bs4 import BeautifulSoup
def parse_html_folder(input_dir, output_dir, no_table_dir, table_id="tab_lhp"):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(no_table_dir, exist_ok=True)
    file_counter = 1
    for filename in os.listdir(input_dir):
        if filename.endswith(".html"):
            input_path = os.path.join(input_dir, filename)
            html = fetch_html_from_file(input_path)
            soup = BeautifulSoup(html, 'html.parser')
            tables = soup.find_all('table', id=table_id)
            if not tables:
                print(f"Таблица не найдена в файле {filename}. Перемещаем в 'no table' как {filename}")
                shutil.copy(input_path, os.path.join(no_table_dir, filename))
                file_counter += 1
                continue
            parsed_data = parse_tables(str(soup), table_id)
            cleaned_filename = filename.replace(".html", "")
            json_output_name = f"{cleaned_filename}.json"
            output_path = os.path.join(output_dir, json_output_name)
            save_to_json(parsed_data, output_path)

            print(f"Файл {filename} обработан и сохранён как {json_output_name}")
            file_counter += 1
def fetch_html_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()
def parse_tables(html, table_id):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', id=table_id)
    parsed_data = {}
    for index, table in enumerate(tables, start=1):
        day_key = f"day_{index}"
        parsed_data[day_key] = {}

        for tr in table.find_all('tr')[1:]:
            tds = tr.find_all('td')
            if len(tds) >= 2:
                med_name_parts = [text.strip() for text in tds[0].stripped_strings]
                med_name = " ".join(med_name_parts)
                dosage = tds[-1].text.strip()
                parsed_data[day_key][med_name] = dosage
    return parsed_data
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
