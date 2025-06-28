import argparse
from parser_form_hourly_assignment_sheet.html_to_json import parse_html_folder
from parser_form_hourly_assignment_sheet.regular_expressions_parser import process_all_files
from parser_form_hourly_assignment_sheet.date_dynamics import process_date_dynamics
from RuBioBert_model.RuBioBert import search_medicine 
from parser_with_no_hourly_assignment_sheet.parse_and_clean_table import parse_table
from parser_with_no_hourly_assignment_sheet.sort_by_date import sort_by_date
from parser_with_no_hourly_assignment_sheet.end_parser import process_file

# Основная функция, запускающая весь пайплайн обработки HTML-файлов с назначениями
# Принимает путь к папке с HTML-таблицами как аргумент
# Последовательно выполняет:
# - парсинг таблиц с датами
# - извлечение регулярных структур
# - восстановление динамики лечения
# - парсинг html-файлов без таблиц и выделение лекарств
# - сортировку по наличию дат
# - построение структуры по дням из модели

def main(table_dir):
    # Каталоги и пути по умолчанию
    output_table_dir = r"table"                       # JSON-файлы с таблицами, содержащими id
    no_table_dir = r"no_table"                        # HTML-файлы без нужной таблицы
    table_id = "tab_lhp"                              # Идентификатор таблицы
    output_reg_dir = r"no_date_dynamics"             # Выход регулярного парсера
    end_dir = r"end"                                # Выход восстановления по дням
    no_table_res_txt = r"parser_with_no_hourly_assignment_sheet/result_parser.txt"  # Результат парсинга no_table
    model_result = r"parser_with_no_hourly_assignment_sheet/model_result.txt"       # Отобранные моделью строки
    medicine_with_date = r"parser_with_no_hourly_assignment_sheet/medicine_with_date.txt"  # Строки с датами

    # Шаг 1: Парсинг HTML-файлов с таблицами
    parse_html_folder(table_dir, output_table_dir, no_table_dir, table_id)

    # Шаг 2: Обработка таблиц регулярными выражениями
    process_all_files(output_table_dir, output_reg_dir)

    # Шаг 3: Восстановление динамики лечения по дням
    process_date_dynamics(output_reg_dir, end_dir)

    # Шаг 4: Обработка HTML-файлов без таблиц, сохранение строк в текстовый файл
    parse_table(no_table_dir, no_table_res_txt)

    # Шаг 5: Отбор строк с лекарствами моделью (по умолчанию отключен)
    search_medicine(no_table_res_txt, model_result)

    # Шаг 6: Отбор строк, содержащих даты (обработка после модели)
    sort_by_date(model_result, medicine_with_date)

    # Шаг 7: Формирование структуры лечения из текстовых блоков без табличной формы
    process_file(medicine_with_date, end_dir)

# Точка входа в скрипт с argparse: принимает путь до папки с HTML-файлами
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка HTML-документов с назначениями")
    parser.add_argument("table_dir", help="Путь к директории с HTML-файлами")
    args = parser.parse_args()
    main(args.table_dir)
