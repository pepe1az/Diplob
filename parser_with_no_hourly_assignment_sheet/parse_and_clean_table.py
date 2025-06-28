import os
from bs4 import BeautifulSoup

# Функция очистки строки от HTML-тегов с сохранением пробелов между элементами
# Использует BeautifulSoup с парсером lxml
def clean_html_line(line):
    """Очищает строку от HTML и возвращает текст с пробелами между элементами."""
    soup = BeautifulSoup(line, "lxml")
    return soup.get_text(separator=" ", strip=True)

# Основная функция парсинга HTML-файлов из указанной папки
# Извлекает таблицы из каждого .html-файла, очищает строки таблиц от HTML, сохраняет текст в выходной файл
# Добавляет специальный маркер конца после каждой страницы: ====== КОНЕЦ <имя_файла>.html ======
def parse_table(folder, output_file):
    with open(output_file, "w", encoding="utf-8") as out:
        for filename in sorted(os.listdir(folder)):
            if not filename.endswith(".html"):
                continue

            print(f"Обрабатываю файл: {filename}")
            filepath = os.path.join(folder, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "lxml")
                tables = soup.find_all("table")

                if not tables:
                    print(f"Таблиц не найдено в файле: {filename}")
                    continue

                # Обработка всех таблиц в документе
                for table in tables:
                    raw_rows = table.decode().split("</tr>")  # Разделение вручную по тегу <tr>
                    for row in raw_rows:
                        row = row.strip()
                        if row:
                            cleaned = clean_html_line(row)  # Очистка строки от HTML-тегов
                            if cleaned:
                                out.write(cleaned + "\n")

                # Добавление маркера конца блока
                out.write(f"====== КОНЕЦ {filename} ======\n\n")
