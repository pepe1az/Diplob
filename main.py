import argparse
from parser_form_hourly_assignment_sheet.html_to_json import parse_html_folder
from parser_form_hourly_assignment_sheet.regular_expressions_parser import process_all_files
from parser_form_hourly_assignment_sheet.date_dynamics import process_date_dynamics
#from RuBioBert_model.RuBioBert import search_medicine
from parser_with_no_hourly_assignment_sheet.parse_and_clean_table import parse_table
from parser_with_no_hourly_assignment_sheet.sort_by_date import sort_by_date
from parser_with_no_hourly_assignment_sheet.end_parser import process_file

def main(table_dir):
    output_table_dir = r"table"
    no_table_dir = r"no_table"
    table_id = "tab_lhp"
    output_reg_dir = r"no_date_dynamics"
    end_dir = r"end_2"
    no_table_res_txt = r"parser_with_no_hourly_assignment_sheet/result_parser.txt"
    model_result = r"parser_with_no_hourly_assignment_sheet/model_result.txt"
    medicine_with_date = r"parser_with_no_hourly_assignment_sheet/medicine_with_date.txt"
    parse_date_dynamics = r"date_dynamics"
    parse_html_folder(table_dir, output_table_dir, no_table_dir, table_id)
    process_all_files(output_table_dir, output_reg_dir)
    process_date_dynamics(output_reg_dir, end_dir)
    parse_table(no_table_dir, no_table_res_txt)
    #search_medicine(no_table_res_txt, model_result)
    sort_by_date(model_result, medicine_with_date)
    process_file(medicine_with_date, parse_date_dynamics)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка HTML-документов с назначениями")
    parser.add_argument("table_dir", help="Путь к директории с HTML-файлами")
    args = parser.parse_args()
    main(args.table_dir)