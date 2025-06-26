import os
import json
import re
from parser_form_hourly_assignment_sheet.concentration import parse_medication_with_pattern

input_dir = r"C:\Users\Кирилл\Desktop\ConvertHTML\another_parc"
output_dir = r"end"
dataset_path = "dataset.jsonl"
os.makedirs(output_dir, exist_ok=True)
def clean_medication_name(name):
    name = re.sub(r"(\d+(?:[.,]\d+)?)\s*(ед|МЕ|ЕД|МГ|Мг|МЛ|Мл|Ед|мг|мл|ml|Ml|ML|mg|Mg|MG|дозсмеси)", "", name)
    name = re.sub(method_pattern, "", name)
    name = re.sub(r"\+", "", name)
    name = re.sub(r"\S*/\S*\s*", "", name)
    name = re.sub(r"[\d\(\)]([.,]?\d+)?", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name
method_pattern = r"(в/в(?: капельно| болюсно)?|п/к|инфузомат|внутрь|нет|ингаляционно|наружно|в глаза|перевязка|энтерально|Местно|изотонический гемодиализ|ТБД|внутриплеврально|эпидурально|на кожу|местно|внутрипузырно|парентерально|через зонд|промыв катетера|в/м(?: глубоко)?)"
def parse_medication(text):
    # Паттерны для поиска
    name_pattern = r"([А-Яа-яЁё0-9 %]+?)(?=\s*\d)"
    dose_pattern_all = r"(\d+\.?\d*)\s*(мл|мг|ЕД)"
    concentration_pattern = r"(\d+\.?\d*)\s*(мг|ЕД|МЕ)/мл"  # Паттерн для концентрации (например, 5 мг/мл)
    #method_pattern = r"(в/в(?: капельно| болюсно)?|п/к|внутрь|на кожу|местно|внутрипузырно|через зонд|промыв катетера|в/м(?: глубоко)?)"
    total_dose_pattern = r"(\d+(?:[.,]\d+)?)\s*(ед|МЕ|ЕД|МГ|Мг|МЛ|Мл|Ед|мг|мл|ml|Ml|ML|mg|Mg|MG|дозсмеси)"
    daily_dosage_pattern_complex = r"(\d+)\(\+\)0"
    
    medications_info = []
    med_part = text.split(":")[0]
    medications = med_part.split(", ")

    names = []
    doses = []
    concentration = None
    for medication in medications:
        name_match = re.match(name_pattern, medication.strip())
        if name_match:
            names.append(name_match.group(1).strip())

        dose_matches = re.findall(dose_pattern_all, medication)
        if dose_matches:
            for dose in dose_matches:
                if dose[1] in ["мл", "мг", "ЕД"]:
                    doses.append((float(dose[0]), dose[1]))
                    break

        # Проверка на концентрацию (например, 5 мг/мл или 100 ЕД/мл)
        concentration_match = re.search(concentration_pattern, medication)
        if concentration_match:
            concentration = (float(concentration_match.group(1)), concentration_match.group(2))

    combined_name = " + ".join(names)
    combined_name = clean_medication_name(combined_name)
    method_match = re.search(method_pattern, text)
    method = method_match.group(1) if method_match else "Not found"

    # Если есть концентрация, вызываем функцию из concentration.py
    if concentration:
        result = parse_medication_with_pattern(text)
        if result:
            # Если результат найден, просто возвращаем его
            return result
    
    dose_value = doses[0][0] if doses else 0
    dose_unit = doses[0][1] if doses else "мл"
    total_dose = 1
    total_volume = dose_value

    # Если паттерн для сложной дозировки встречается, обрабатываем его
    if re.search(daily_dosage_pattern_complex, text):
        total_dose = int(re.search(daily_dosage_pattern_complex, text).group(1))
        total_volume = dose_value * total_dose
    elif re.findall(total_dose_pattern, text):
        matches = re.findall(total_dose_pattern, text)
        raw_value, unit = matches[-1]  # Берём последнее вхождение
        raw_value = raw_value.replace(',', '.')
        total_volume = float(raw_value)

        # Если значение и единицы совпадают — frequency = 1, без расчётов
        if doses and dose_value == total_volume and unit == dose_unit:
            total_dose = 1
        elif doses:
            dose_val = doses[0][0]
            total_dose = round(total_volume / dose_val) if dose_val != 0 else 0
        else:
            total_dose = 1
    medication_info = {
        "name": combined_name,
        "dose": f"{dose_value} {dose_unit}",
        "method": method,
        "daily_dosage": total_dose,
        "total_volume": f"{total_volume} {dose_unit}"
    }

    medications_info.append(medication_info)
    return medications_info

def process_all_files(input_dir, output_dir): 
    dose_pattern = r"\d+(\.\d+)?\s*(мл|мг|ЕД|%|Ед|ед|гр|тыс|.|ME)"
    dataset_entries = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            result_by_days = {}
            for day, prescriptions in data.items():
                day_key = f"{day}"
                result_by_days[day_key] = {}
                for name, dose in prescriptions.items():
                    full_text = f"{name}: {dose}"
                    parsed = parse_medication(full_text)
                    filtered_name = re.sub(dose_pattern, "", name)  
                    filtered_name = re.sub(method_pattern, "", filtered_name)
                    filtered_name = re.sub(r"\+", "", filtered_name)
                    filtered_name = re.sub(r"\S*/\S*\s*", "", filtered_name)
                    filtered_name = re.sub(r"[\d\(\)]([.,]?\d+)?", "", filtered_name)
                    filtered_name = re.sub(r"\s+", " ", filtered_name).strip()
                    if filtered_name == "":
                        continue
                    if parsed:
                        if 'concentration' in parsed:
                            parsed_result = {
                                "route": parsed["route"],
                                "total": parsed["total"],
                                "concentration": parsed["concentration"],
                            }
                        else:
                            parsed_result = {
                                "frequency": parsed[0]["daily_dosage"],
                                "route": parsed[0]["method"],
                                "dosage": parsed[0]["dose"],
                                "total": parsed[0]["total_volume"]
                            }

                        result_by_days[day_key][filtered_name] = parsed_result
                        dataset_entries.append({
                            "input": {
                                filtered_name: parsed_result
                            },
                            "original":full_text,
                            "label": 1
                        })
                    else:
                        print(f"Не удалось обработать: {full_text}")

            final_output = {
                "treatment": result_by_days
            }
            cleaned_filename = filename.replace(".html", "")
            output_path = os.path.join(output_dir, cleaned_filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f_out:
                json.dump(final_output, f_out, ensure_ascii=False, indent=4)

            print(f"Обработан и сохранён: {cleaned_filename}")

