from parser_form_hourly_assignment_sheet.html_to_json import parse_html_folder
from parser_form_hourly_assignment_sheet.regular_expressions_parser import process_all_files
from parser_form_hourly_assignment_sheet.date_dynamics import process_date_dynamics
from RuBioBert_model.RuBioBert import search_medicine
from parser_with_no_hourly_assignment_sheet.parse_and_clean_table import parse_table
from parser_with_no_hourly_assignment_sheet.sort_by_date import sort_by_date
from parser_with_no_hourly_assignment_sheet.end_parser import main as parse_data_pattern
from parser_with_no_hourly_assignment_sheet.date_dynamics import process_date_dynamics as parse_date_dynamics_no_table
table_dir = r"ConvertHTML" # Директория с html файлами которые нужно обработать
output_table_dir = r"table" #Директория с данными из файлов, содержащих листы почасовых назначений
no_table_dir = r"no_table" #Директория с файлами, не содержащими листы почасовых назначений
table_id = "tab_lhp" #Уникальный идентификатор листов почасовых назначений
output_reg_dir = r"no_date_dynamics" #Директория с результатами работы регулярных строк над данными, извлечёнынми из листов почасовых назначений
end_dir = r"end" #Директория содержащая результаты обработки всех историй болезней
no_table_res_txt = r"parser_with_no_hourly_assignment_sheet/result_parser.txt" #путь ко всем таблицам из историй, не содержащих листы почасовых назначений
model_result = r"parser_with_no_hourly_assignment_sheet/model_result.txt" #Результат работы модели RuBioBERT
medicine_with_date = r"parser_with_no_hourly_assignment_sheet/medicine_with_date.txt" #Результат сортировки выхода модели, проще говоря извлечение всех назначений с окончанием в виде дат
parse_date_dynamics = r"date_dynamics" #Директория с результатом обработки парсером по назначениям, которые не входяд в лист почасовых назначений
parse_html_folder(table_dir, output_table_dir, no_table_dir, table_id)# Функция парсинга данных с html документов, и разбиением ооных на содержащие листы почасовых назначений и нет
process_all_files(output_table_dir, output_reg_dir)# Функция разбиения данных из историй болезней в json формат, с помощью регулярных выражений
process_date_dynamics(output_reg_dir, end_dir)# Функция разбиения лекарств, из документов содержащих листты почасовых назначения, по динамике назначения
parse_table(no_table_dir, no_table_res_txt)# Функция парсинга и очистки всех таблиц из документов, не содержищих листы почасовых назначений
search_medicine(no_table_res_txt, model_result) # Функция вызова модели RuBioBERT для определения наличия лекарства в строках из таблиц документов, не содержащих листы почасовых назначений       
sort_by_date(model_result, medicine_with_date)# Функиця сортировки результатов работы модели, основывающаяся на строках, заканчивающихся на даты
parse_data_pattern(medicine_with_date, parse_date_dynamics)# Функиция распределениея отсортированных результатов работы модели в json форму
parse_date_dynamics_no_table(parse_date_dynamics, end_dir)# Функция отображения динамики лечения, данных полученных из документов не содержащих листы почасовых назначений
