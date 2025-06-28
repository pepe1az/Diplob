import re

# Регулярное выражение для поиска строки, содержащей ровно две даты формата ДД.ММ.ГГГГ в конце строки
date_pattern = re.compile(r'\d{2}\.\d{2}\.\d{4}\s+\d{2}\.\d{2}\.\d{4}$')

# Функция сортировки строк по наличию дат
# Копирует только те строки из входного файла, которые содержат пару дат в конце
# Также сохраняет маркер конца блока '====== КОНЕЦ ... ======'
def sort_by_date(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            stripped = line.strip()
            # Сохраняем маркер конца блока без изменений
            if stripped.startswith("====== КОНЕЦ"):
                outfile.write(line)
                continue
            # Записываем строку только если она содержит шаблон с двумя датами в конце
            if date_pattern.search(stripped):
                outfile.write(line)
